from seq2seq.seq2seq import Seq2seqModel
from data import GeoDataset
import torch
import torch.nn as nn
from torch.optim.lr_scheduler import ReduceLROnPlateau
from utils import PAD, sequence_loss
import torch.nn.functional as F
from os.path import join
from grammars.utils import normalize_prolog_variable_names, action_sequence_to_logical_form

class Estimator:
    def __init__(self, emb_dim, n_hidden, bidirectional,
                 n_layer, dropout, lr, decay, lr_p,
                 clip, batch_size, epoch_num, cuda, path):
        #TODO:pretrain model
        self.emb_dim = emb_dim
        self.n_hidden = n_hidden
        self.bidirectional = bidirectional
        self.n_layer = n_layer
        self.dropout = dropout
        self.lr = lr
        self.decay = decay
        self.lr_p = lr_p
        self.clip = clip
        self.batch_size = batch_size
        self.epoch_num = epoch_num
        self.path = path
        self.cuda = cuda


        self.dataset = GeoDataset(emb_dim, batch_size, cuda)
        self.vocab_size = len(self.dataset.word_vector)

    def estimate(self, grammar_dict, root_rule):
        batches, id2rule, productions = self.dataset.parse(grammar_dict, root_rule)
        nonterminal2id, id2nonterminal = self.build_decode_dict(productions)
        self.model = Seq2seqModel(vocab_size=self.vocab_size, emb_dim=self.emb_dim,
                                  n_hidden=self.n_hidden,
                                  output_size = self.dataset.grammar.num_rules + 1,
                                  bidirectional=self.bidirectional, n_layer=self.n_layer,
                                  dropout=self.dropout)
        self.model.set_embedding(torch.tensor(self.dataset.word_vector))

        state_dict = torch.load('exp/ckpt289-0.4418167173862457')
        self.model.load_state_dict(state_dict['net'])
        if self.cuda:
            self.model.cuda()

        self.compute_performance(batches[-4:], id2rule, nonterminal2id, id2nonterminal)
        exit(0)

        self.optimizer = torch.optim.SGD([p for p in self.model.parameters() if p.requires_grad],
                                         lr=self.lr)
        self.scheduler = ReduceLROnPlateau(self.optimizer, 'min', verbose=True,
                                           factor=self.decay, min_lr=0,
                                           patience=self.lr_p)

        self.smooth_loss = 0
        best_performance = 100
        for i in range(self.epoch_num):
            print('\n\n')
            print('*' * 80)
            print(f'start epoch {i}:')
            self.train(batches[:-4])
            performance = self.eval(batches[-4:])
            self.scheduler.step(performance)
            print(self.optimizer)
            if performance < best_performance:
                best_performance = performance
                save_dict = {}
                save_dict['metric'] = performance
                save_dict['net'] = self.model.state_dict()
                save_dict['optim'] = self.optimizer.state_dict()
                torch.save(save_dict, join(self.path, f'ckpt{i}-{performance}'))
            if i % 20 == 19:
                self.compute_performance(batches[-4:], id2rule, nonterminal2id, id2nonterminal)

    def train(self, batches):
        self.model.train()
        for i, batch in enumerate(batches):
            logits = self.model(batch.questions, batch.src_lens, batch.actions_in)
            loss = sequence_loss(logits, batch.actions_out, pad_idx=PAD).mean()
            self.optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_([p for p in self.model.parameters() if p.requires_grad], self.clip)
            self.optimizer.step()
            self.smooth_loss = loss if self.smooth_loss == 0 else \
                self.smooth_loss * 0.95 + loss * 0.05

            if i % 10 == 0:
                print('   ', self.smooth_loss)

    def eval(self, batches):
        self.model.eval()
        loss = 0
        for batch in batches:
            logits = self.model(batch.questions, batch.src_lens, batch.actions_in)
            loss += sequence_loss(logits, batch.actions_out, pad_idx=PAD).mean()
        print(f'loss in validation dataset: {loss / len(batches)}')
        return loss / len(batches)

    def compute_performance(self, batches, id2rule, nonterminal2id, id2nonterminal):
        self.model.eval()
        for batch in batches:
            batch_actions = self.model.batch_decode(batch.questions,
                                                    batch.src_lens, PAD, 100,
                                                    nonterminal2id, id2nonterminal)[0]
            #id2rule也许可以被production替代
            #print('!!!!')
            #print(batch_actions)
            batch_actions = torch.stack(batch_actions).transpose(0, 1)
            import pickle
            with open('tmp.pkl', 'wb') as f:
                pickle.dump((batch_actions, id2rule), f)
            #exit(0)
            for actions in batch_actions:
                for i in range(len(actions)):
                    if int(actions[i]) == 0:
                        actions = actions[:i]
                        print(actions)
                        break
                rule_str = [id2rule[int(act)] for act in actions]
                rule = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
                print(rule)

    def build_decode_dict(self, productions):
        nonterminal2id = {}
        id2nonterminal = {}
        for prod in productions:
            print(prod.lhs, prod.rhs_nonterminal, prod.rule_id)
            k, v, id = prod.lhs, prod.rhs_nonterminal, prod.rule_id
            if k not in nonterminal2id.keys():
                nonterminal2id[k] = [id]
            else:
                nonterminal2id[k].append(id)
            id2nonterminal[id] = prod.rhs_nonterminal
        return nonterminal2id, id2nonterminal


'''

    def compute_performance(self, batches, id2rule):
        for batch in batches:
            for question, src_len in zip(batch.questions, batch.src_lens):
                actions = self.model.decode(question,
                                            src_len, PAD, 1000)[0]
                rule_str = [id2rule[int(act)] for act in actions]
                rule = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
                print(rule)
'''

