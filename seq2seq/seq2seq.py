import torch
from torch import nn
from torch.nn import init
from utils import PAD, pad_batch_tensorize
from .rnn import lstm_encoder
from .rnn import MultiLayerLSTMCells
from .attention import step_attention
from .util import sequence_mean, len_mask
from . import beam_search as bs

INIT = 1e-2


class Seq2seqModel(nn.Module):
    #forward: return logit(batchsize * seq_len * vocab_size)
    def __init__(self, vocab_size, emb_dim, output_size,
                 n_hidden, bidirectional, n_layer, dropout=0.0):
        super().__init__()
        # embedding weight parameter is shared between encoder, decoder,
        # and used as final projection layer to vocab logit
        # can initialize with pretrained word vectors
        self._embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=0)
        self._enc_lstm = nn.LSTM(
            emb_dim, n_hidden, n_layer,
            bidirectional=bidirectional, dropout=dropout
        )
        # initial encoder LSTM states are learned parameters
        state_layer = n_layer * (2 if bidirectional else 1)
        self._init_enc_h = nn.Parameter(
            torch.Tensor(state_layer, n_hidden)
        )
        self._init_enc_c = nn.Parameter(
            torch.Tensor(state_layer, n_hidden)
        )
        init.uniform_(self._init_enc_h, -INIT, INIT)
        init.uniform_(self._init_enc_c, -INIT, INIT)

        # vanillat lstm / LNlstm
        self.action_num = output_size
        self._dec_embedding = nn.Embedding(output_size, emb_dim, padding_idx=0)
        self._dec_lstm = MultiLayerLSTMCells(
            2*emb_dim, n_hidden, n_layer, dropout=dropout
        )
        # project encoder final states to decoder initial states
        enc_out_dim = n_hidden * (2 if bidirectional else 1)
        self._dec_h = nn.Linear(enc_out_dim, n_hidden, bias=False)
        self._dec_c = nn.Linear(enc_out_dim, n_hidden, bias=False)
        # multiplicative attention
        self._attn_wm = nn.Parameter(torch.Tensor(enc_out_dim, n_hidden))
        self._attn_wq = nn.Parameter(torch.Tensor(n_hidden, n_hidden))
        init.xavier_normal_(self._attn_wm)
        init.xavier_normal_(self._attn_wq)
        # project decoder output to emb_dim, then
        # apply weight matrix from embedding layer
        self._projection = nn.Sequential(
            nn.Linear(2*n_hidden, n_hidden),
            nn.Tanh(),
            nn.Linear(n_hidden, emb_dim, bias=False)
        )
        # functional object for easier usage
        self._decoder = AttentionalLSTMDecoder(
            self._dec_embedding, self._dec_lstm,
            self._attn_wq, self._projection
        )

    def forward(self, input_seqs, input_lens, output_seqs):
        attention, init_dec_states = self.encode(input_seqs, input_lens)
        mask = len_mask(input_lens, attention.device).unsqueeze(-2)
        logit = self._decoder((attention, mask), init_dec_states, output_seqs)
        return logit

    def encode(self, input_seqs, art_lens=None):
        size = (
            self._init_enc_h.size(0),
            len(art_lens) if art_lens else 1,
            self._init_enc_h.size(1)
        )
        init_enc_states = (
            self._init_enc_h.unsqueeze(1).expand(*size),
            self._init_enc_c.unsqueeze(1).expand(*size)
        )
        enc_art, final_states = lstm_encoder(
            input_seqs, self._enc_lstm, art_lens,
            init_enc_states, self._embedding
        )
        if self._enc_lstm.bidirectional:
            h, c = final_states
            final_states = (
                torch.cat(h.chunk(2, dim=0), dim=2),
                torch.cat(c.chunk(2, dim=0), dim=2)
            )
        init_h = torch.stack([self._dec_h(s)
                              for s in final_states[0]], dim=0)
        init_c = torch.stack([self._dec_c(s)
                              for s in final_states[1]], dim=0)
        init_dec_states = (init_h, init_c)
        attention = torch.matmul(enc_art, self._attn_wm).transpose(0, 1)
        init_attn_out = self._projection(torch.cat(
            [init_h[-1], sequence_mean(attention, art_lens, dim=1)], dim=1
        ))
        return attention, (init_dec_states, init_attn_out)

    def batch_decode(self, input_seqs, input_lens, go, max_len, nonterminal2id, id2nonterminal):
        """ greedy decode support batching"""
        #TODO:early stop by using eos
        batch_size = len(input_seqs)
        attention, init_dec_states = self.encode(input_seqs, input_lens)
        mask = len_mask(input_lens, attention.device).unsqueeze(-2)
        attention = (attention, mask)
        tok = torch.LongTensor([go]*batch_size).to(input_seqs.device)
        outputs = []
        attns = []
        states = init_dec_states

        end_flag = [False] * batch_size
        nonterminal_stack = [['statement'] for _ in range(batch_size)]
        for i in range(max_len):
            mask = torch.zeros([batch_size, self.action_num]).long().to(input_seqs.device)
            for id, nonterminal in enumerate(nonterminal_stack):
                if len(nonterminal) == 0:
                    mask[id, 0] = 1
                else:
                    #print(id, nonterminal[0], nonterminal2id[nonterminal[0]])
                    mask[id, nonterminal2id[nonterminal[0]]] = 1

            tok, states, attn_score = self._decoder.decode_step(
                tok, states, attention, mask)
            #print(tok[:, 0])
            for id, t in enumerate(tok):
                if end_flag[id]:
                    continue
                nonterminal_stack[id] = id2nonterminal[int(t[0])] + nonterminal_stack[id][1:]
                if len(nonterminal_stack[id]) == 0:
                    end_flag[id] = True
            outputs.append(tok[:, 0])
            attns.append(attn_score)
            if all(end_flag):
                break
        return outputs, attns

    def batched_beamsearch(self, input_seqs, input_lens,
                           go, max_len, beam_size, nonterminal2id,
                           id2nonterminal, diverse=0.0, relax=False):
        batch_size = len(input_lens)
        attention, init_dec_states = self.encode(input_seqs, input_lens)
        mask = len_mask(input_lens, attention.device).unsqueeze(-2)
        all_attention = (attention, mask)
        attention = all_attention
        (h, c), prev = init_dec_states
        all_beams = [bs.init_beam(go, (h[:, i, :], c[:, i, :], prev[i]))
                     for i in range(batch_size)]
        finished_beams = [[] for _ in range(batch_size)]
        outputs = [None for _ in range(batch_size)]
        for t in range(max_len):
            #print(t)
            toks = []
            all_states = []
            action_mask = []
            for beam in filter(bool, all_beams):
                token, states, stack = bs.pack_beam(beam, input_seqs.device)
                toks.append(token)
                all_states.append(states)
                m = torch.zeros([len(beam), self.action_num]).long().to(input_seqs.device)
                for id, nonterminal in enumerate(stack):
                    if len(nonterminal) == 0:
                        m[id, 0] = 1
                    else:
                        m[id, nonterminal2id[nonterminal[0]]] = 1
                action_mask.append(m)
            token = torch.stack(toks, dim=1)
            states = ((torch.stack([h for (h, _), _ in all_states], dim=2),
                       torch.stack([c for (_, c), _ in all_states], dim=2)),
                      torch.stack([prev for _, prev in all_states], dim=1))
            action_mask = torch.stack(action_mask, dim=1)
            topk, lp, states, attn_score = self._decoder.topk_step(
                token, states, attention, beam_size, action_mask)
            batch_i = 0
            #print(topk)
            #print(lp)
            for i, (beam, finished) in enumerate(zip(all_beams,
                                                     finished_beams)):
                if not beam:
                    continue
                #print(topk[:, batch_i, :])
                finished, new_beam = bs.next_search_beam(
                    beam, beam_size, finished, id2nonterminal,
                    topk[:, batch_i, :], lp[:, batch_i, :],
                    (states[0][0][:, :, batch_i, :],
                     states[0][1][:, :, batch_i, :],
                     states[1][:, batch_i, :]),
                    attn_score[:, batch_i, :],
                    diverse
                )
                batch_i += 1
                if len(finished) >= beam_size:
                    all_beams[i] = []
                    if relax:
                        outputs[i] = [f.sequence[1:] for f in finished[:beam_size]]
                    else:
                        outputs[i] = finished[0].sequence[1:]
                    # exclude finished inputs
                    attention, mask = all_attention
                    masks = [mask[j] for j, o in enumerate(outputs)
                             if o is None]
                    ind = [j for j, o in enumerate(outputs) if o is None]
                    ind = torch.LongTensor(ind).to(attention.device)
                    attention = attention.index_select(dim=0, index=ind)
                    if masks:
                        mask = torch.stack(masks, dim=0)
                    else:
                        mask = None
                    attention = (attention, mask)
                else:
                    all_beams[i] = new_beam
                    finished_beams[i] = finished
            early_stop = True
            for o in outputs:
                if o is None:
                    early_stop = False
                    break
            if early_stop:
                break
        else:
            for i, (o, f, b) in enumerate(zip(outputs,
                                              finished_beams, all_beams)):
                if o is None:
                    if relax:
                        outputs[i] = [single_f.sequence[1:] for single_f in (f + b)[:beam_size]]
                    else:
                        outputs[i] = (f+b)[:beam_size]
        if relax:
            pass
        else:
            outputs = pad_batch_tensorize(outputs, PAD,
                                          str(all_attention[0].device) != 'cpu').transpose(0, 1)
            outputs = [o for o in outputs]
        return outputs, None

    def set_embedding(self, embedding):
        """embedding is the weight matrix"""
        assert self._embedding.weight.size() == embedding.size()
        self._embedding.weight.data.copy_(embedding)
        for p in self._embedding.parameters():
            p.requires_grad = False

    def train_emb(self):
        for p in self._embedding.parameters():
            p.requires_grad = True

class AttentionalLSTMDecoder(object):
    def __init__(self, embedding, lstm, attn_w, projection):
        super().__init__()
        self._embedding = embedding
        self._lstm = lstm
        self._attn_w = attn_w
        self._projection = projection

    def __call__(self, attention, init_states, target):
        max_len = target.size(1)
        states = init_states
        logits = []
        for i in range(max_len):
            tok = target[:, i:i+1]
            logit, states, _ = self._step(tok, states, attention)
            logits.append(logit)
        logit = torch.stack(logits, dim=1)
        return logit

    def _step(self, tok, states, attention):
        prev_states, prev_out = states
        lstm_in = torch.cat(
            [self._embedding(tok).squeeze(1), prev_out],
            dim=1
        )
        states = self._lstm(lstm_in, prev_states)
        lstm_out = states[0][-1]
        query = torch.mm(lstm_out, self._attn_w)
        attention, attn_mask = attention
        context, score = step_attention(
            query, attention, attention, attn_mask)
        dec_out = self._projection(torch.cat([lstm_out, context], dim=1))
        states = (states, dec_out)
        logit = torch.mm(dec_out, self._embedding.weight.t())
        return logit, states, score

    def decode_step(self, tok, states, attention, mask):
        logit, states, score = self._step(tok, states, attention)
        logit = logit.masked_fill(mask == 0, float('-inf'))
        #print((mask == 0)[0])
        #print(logit.size())
        #print(logit[0])
        out = torch.max(logit, dim=1, keepdim=True)[1]
        return out, states, score

    def topk_step(self, tok, states, attention, k, mask):
        """tok:[BB, B], states ([L, BB, B, D]*2, [BB, B, D])"""
        (h, c), prev_out = states

        # lstm is not bemable
        nl, _, _, d = h.size()
        beam, batch = tok.size()
        lstm_in_beamable = torch.cat(
            [self._embedding(tok), prev_out], dim=-1)
        lstm_in = lstm_in_beamable.contiguous().view(beam*batch, -1)
        prev_states = (h.contiguous().view(nl, -1, d),
                       c.contiguous().view(nl, -1, d))
        h, c = self._lstm(lstm_in, prev_states)
        states = (h.contiguous().view(nl, beam, batch, -1),
                  c.contiguous().view(nl, beam, batch, -1))
        lstm_out = states[0][-1]

        # attention is beamable
        query = torch.matmul(lstm_out, self._attn_w)
        attention, attn_mask = attention
        context, score = step_attention(
            query, attention, attention, attn_mask)
        dec_out = self._projection(torch.cat([lstm_out, context], dim=-1))

        logit = torch.mm(dec_out.contiguous().view(batch*beam, -1), self._embedding.weight.t())
        logit = logit.contiguous().view(beam, batch, -1)

        logit = logit.masked_fill(mask == 0, float('-inf'))
        logit = torch.log_softmax(logit, dim=-1)
        k_lp, k_tok = logit.topk(k=k, dim=-1)
        return k_tok, k_lp, (states, dec_out), score