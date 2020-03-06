from grammars.grammar import Grammar
import torch
from utils import make_vocab, read_prolog_data, PAD, pad_batch_tensorize, read_sql_data
import pickle



class Batch:
    def __init__(self, questions, src_lens, actions_in, actions_out, logical_forms):
        self.questions = questions
        self.src_lens = src_lens
        self.actions_in = actions_in
        self.actions_out = actions_out
        self.logical_forms = logical_forms


class GeoDataset:
    def __init__(self, emb_dim, batch_size, cuda):
        self.batch_size = batch_size
        self.cuda = cuda
        (self.train_questions, self.test_questions), \
        (self.train_logical_forms, self.test_logical_forms) = read_sql_data()
        with open('vocab.pkl', 'rb') as f:
            self.word2id, self.id2word, self.word_vector = pickle.load(f)
        #print('start')
        #self.word2id, self.id2word, self.word_vector = make_vocab(self.train_questions + self.test_questions, emb_dim)
        #with open('vocab.pkl', 'wb') as f:
        #    pickle.dump((self.word2id, self.id2word, self.word_vector), f)
        #print('end')
        self.train_questions, self.train_logical_forms = self.pre_process(self.train_questions,
                                                                          self.train_logical_forms)
        self.test_questions, self.test_logical_forms = self.pre_process(self.test_questions,
                                                                        self.test_logical_forms)


        #import pickle
        #with open('split_train_test', )

    def parse(self, grammar_dict, root_rule):
        actions = []
        id2rule = {}
        self.grammar = Grammar(grammar_dict, root_rule)
        productions = self.grammar.get_productions()
        print(self.grammar.num_rules)
        min_act = 999
        max_act = 0
        train_size = len(self.train_questions)
        logical_forms = self.train_logical_forms + self.test_logical_forms
        for form in logical_forms:
            applied_production_rules = self.grammar.parse(form)
            for r in applied_production_rules:
                max_act = max(max_act, r.rule_id)
                min_act = min(min_act, r.rule_id)
                id2rule[r.rule_id] = r.rule
            rule_ids = [rule.rule_id for rule in applied_production_rules]
            actions.append(rule_ids)
        tran_actions = actions[:train_size]
        test_actions = actions[train_size:]
        train_batches = self.get_batch(self.train_questions, tran_actions, self.train_logical_forms)
        test_batches = self.get_batch(self.test_questions, test_actions, self.test_logical_forms)
        print(max_act, min_act)
        assert min_act == 1 and max_act == self.grammar.num_rules - 1
        print(tran_actions[0:5])
        exit(0)
        return (train_batches, test_batches), id2rule, productions

    def pre_process(self, questions, logical_forms):
        questions = [[self.word2id[word] for word in q.split()]
                          for q in questions]
        data = list(zip(questions, logical_forms))
        data = list(sorted(data, key=lambda x: len(x[0])))
        #data = list(sorted(data, key=lambda x: random.random()))
        return [e[0] for e in data], [e[1] for e in data]

    def get_batch(self, questions, actions, logical_forms):
        leng = len(actions)
        batches = []
        for i in range(0, leng, self.batch_size):
            batch_questions = questions[i: min(i + self.batch_size, leng)]
            batch_actions = actions[i: min(i + self.batch_size, leng)]
            batches.append(self.padding(batch_questions, batch_actions,
                                        logical_forms[i: min(i + self.batch_size, leng)]))
        return batches

    def padding(self, batch_questions, batch_actions, batch_logical_forms):
        src_lens = [len(question) for question in batch_questions]
        actions_in = [[PAD] + actions for actions in batch_actions]
        actions_out = [actions + [PAD] for actions in batch_actions]

        batch_questions = pad_batch_tensorize(batch_questions, PAD, self.cuda)
        actions_in = pad_batch_tensorize(actions_in, PAD, self.cuda)
        actions_out = pad_batch_tensorize(actions_out, PAD, self.cuda)

        return Batch(batch_questions, src_lens, actions_in, actions_out, batch_logical_forms)
