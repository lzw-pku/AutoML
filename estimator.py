from seq2seq.seq2seq import Seq2seqModel
from data import GeoDataset
import torch
import torch.nn as nn
from torch.optim.lr_scheduler import ReduceLROnPlateau
from utils import PAD, sequence_loss
import torch.nn.functional as F
from os.path import join
from grammars.utils import normalize_prolog_variable_names, action_sequence_to_logical_form
import time


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
        self.error_history = []

    def estimate(self, grammar_dict, root_rule, toy=False, name='', debug=False):
        time1 = time.time()
        (train_batches, test_batches), id2rule, productions = self.dataset.parse(grammar_dict,
                                                                                 root_rule)
        #print(id2rule)

        #return train_batches
        print('parsing time:', time.time() - time1)
        nonterminal2id, id2nonterminal = self.build_decode_dict(productions)
        self.model = Seq2seqModel(vocab_size=self.vocab_size, emb_dim=self.emb_dim,
                                  n_hidden=self.n_hidden,
                                  output_size = self.dataset.grammar.num_rules + 1,
                                  bidirectional=self.bidirectional, n_layer=self.n_layer,
                                  dropout=self.dropout)
        self.model.set_embedding(torch.tensor(self.dataset.word_vector))
        #state_dict = torch.load('initial_model')
        #state_dict['_dec_embedding.weight'] = state_dict['_dec_embedding.weight'][:self.dataset.grammar.num_rules + 1]
        #
        #self.model.load_state_dict(state_dict)
        #torch.save(self.model.state_dict(), './initial_model')
        #exit(0)
        #state_dict = torch.load('exp/ckpt289-0.4418167173862457')
        #self.model.load_state_dict(state_dict['net'])
        if self.cuda:
            self.model.cuda()

        self.optimizer = torch.optim.Adam([p for p in self.model.parameters() if p.requires_grad],
                                          lr=self.lr)
        self.scheduler = ReduceLROnPlateau(self.optimizer, 'min', verbose=True,
                                           factor=self.decay, min_lr=0,
                                           patience=self.lr_p)

        self.smooth_loss = 0
        best_performance = 100
        patience = 10
        start_train_emb = False
        best_exact_match = 0
        epoch_num = 30 if toy else self.epoch_num
        valid_loss = []
        for i in range(epoch_num):
            self.train(train_batches)
            performance = self.eval(test_batches)
            #print(performance)
            valid_loss.append(performance)
            if not toy:
                self.scheduler.step(performance)
            else:
                if i % 10 == 9:
                    self.optimizer.state_dict()['param_groups'][0]['lr'] /= 2

            #if not toy and not start_train_emb and \
            #    self.optimizer.state_dict()['param_groups'][0]['lr'] < 1e-4:
            #    self.model.train_emb()
            #    start_train_emb = True
                #print('START TRAIN EMB')
            if performance < best_performance:
                best_performance = performance
                save_dict = {}
                save_dict['metric'] = performance
                save_dict['net'] = self.model.state_dict()
                save_dict['optim'] = self.optimizer.state_dict()
                save_dict['losses'] = valid_loss
                torch.save(save_dict, join(self.path, f'model-{name}'))
                patience = 10
            else:
                patience -= 1
                if patience == 0:
                    #score0 = self.compute_performance(test_batches, id2rule,
                    #                                 nonterminal2id, id2nonterminal)
                    score = self.compute_performance_decode(test_batches, id2rule,
                                                            nonterminal2id, id2nonterminal, debug)
                    #print(score0, score)
                    best_exact_match = max(best_exact_match, score)
                    if debug:
                        with open('./error_history.pkl', 'wb') as f:
                            import pickle
                            pickle.dump(self.error_history, f)
                    #print('early stop')
                    break
            if True:
                score0 = self.compute_performance(test_batches, id2rule,
                                                 nonterminal2id, id2nonterminal, relax=True)
                score = self.compute_performance_decode(test_batches, id2rule,
                                                        nonterminal2id, id2nonterminal, debug)
                print(performance, score0, score)
                best_exact_match = max(best_exact_match, score)
        return best_exact_match

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

            #if i % 10 == 0:
            #    print('   ', self.smooth_loss)

    def eval(self, batches):
        self.model.eval()
        loss = 0
        for batch in batches:
            logits = self.model(batch.questions, batch.src_lens, batch.actions_in)
            loss += sequence_loss(logits, batch.actions_out, pad_idx=PAD).mean()
        #print(f'loss in validation dataset: {loss / len(batches)}')
        return loss.item() / len(batches)

    def compute_performance(self, batches, id2rule, nonterminal2id, id2nonterminal, relax=False):
        self.model.eval()
        total = 0
        true_example = 0
        for batch in batches:
            batch_actions = self.model.batched_beamsearch(batch.questions,
                                                    batch.src_lens, PAD, 200, 5,
                                                    nonterminal2id, id2nonterminal, diverse=0,
                                                          relax=relax)[0]
            total += len(batch_actions)
            #id2rule也许可以被production替代
            if not relax:
                batch_actions = torch.stack(batch_actions).transpose(0, 1)

                for actions, logical_form in zip(batch_actions, batch.logical_forms):
                    for i in range(len(actions)):
                        if int(actions[i]) == 0:
                            actions = actions[:i]
                            break
                    try:
                        rule_str = [id2rule[int(act)] for act in actions]
                        rule = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
                        if rule == logical_form:
                            true_example += 1
                    except:
                        continue
            else:
                for action_lists, logical_form in zip(batch_actions, batch.logical_forms):
                    for actions in action_lists:
                        try:
                            rule_str = [id2rule[int(act)] for act in actions]
                            rule = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
                            if rule == logical_form:
                                true_example += 1
                                break
                        except:
                            continue

        return true_example / total
        #print('exact match: ', true_example / total)

    def compute_performance_decode(self, batches, id2rule, nonterminal2id, id2nonterminal, debug):
        self.model.eval()
        total = 0
        true_example = 0
        if debug:
            error1 = [0 for _ in range(len(id2rule) + 10)]
            error2 = [0 for _ in range(len(id2rule) + 10)]
            total_act1 = [0 for _ in range(len(id2rule) + 10)]
            total_act2 = [0 for _ in range(len(id2rule) + 10)]
        #print(len(id2rule)+1)
        for batch in batches:
            batch_actions = self.model.batch_decode(batch.questions,
                                                    batch.src_lens, PAD, 200,
                                                    nonterminal2id, id2nonterminal)[0]
            #id2rule也许可以被production替代
            batch_actions = torch.stack(batch_actions).transpose(0, 1)
            total += len(batch_actions)
            for actions, logical_form, act_out in zip(batch_actions, batch.logical_forms, batch.actions_out):
                for i in range(len(actions)):
                    if int(actions[i]) == 0:
                        actions = actions[:i]
                        break

                rule_str = [id2rule[int(act)] for act in actions]
                try:
                    rule = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
                except:
                    continue
                if debug:
                    for act in actions:
                        #print(act)
                        total_act1[int(act)] += 1
                    for act in act_out:
                        #print(act)
                        total_act2[int(act)] += 1
                if rule == logical_form:
                    true_example += 1
                elif debug:
                    for i in range(min(len(actions), len(act_out))):
                        if int(actions[i]) != act_out[i]:
                            error1[int(actions[i])] += 1
                            error2[act_out[i]] += 1
                            break
        if debug:
            self.error_history.append((error1, error2, total_act1, total_act2))
        return true_example / total
        #print('exact match: ', true_example / total)

    def build_decode_dict(self, productions):
        nonterminal2id = {}
        id2nonterminal = {}
        for prod in productions:
            #print(prod.lhs, prod.rhs_nonterminal, prod.rule_id)
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

