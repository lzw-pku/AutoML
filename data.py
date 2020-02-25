from grammars.grammar import Grammar
import torch
from utils import make_vocab, read_prolog_data, PAD, pad_batch_tensorize
import pickle



class Batch:
    def __init__(self, questions, src_lens, actions_in, actions_out):
        self.questions = questions
        self.src_lens = src_lens
        self.actions_in = actions_in
        self.actions_out = actions_out


class GeoDataset:
    def __init__(self, emb_dim, batch_size, cuda):
        self.batch_size = batch_size
        self.cuda = cuda
        self.questions, self.logical_forms = read_prolog_data()
        with open('vocab.pkl', 'rb') as f:
            self.word2id, self.id2word, self.word_vector = pickle.load(f)
        #self.word2id, self.id2word, self.word_vector = make_vocab(self.questions, emb_dim)
        #with open('vocab.pkl', 'wb') as f:
        #    pickle.dump((self.word2id, self.id2word, self.word_vector), f)
        self.questions = [[self.word2id[word] for word in q.split()]
                          for q in self.questions]
        self.questions, self.logical_forms = self.rank(self.questions, self.logical_forms)

    def parse(self, grammar_dict, root_rule):
        actions = []
        id2rule = {}
        self.grammar = Grammar(grammar_dict, root_rule)
        productions = self.grammar.get_productions()
        #print(grammar.num_rules)
        min_act = 999
        max_act = 0
        for form in self.logical_forms:
            applied_production_rules = self.grammar.parse(form)
            for r in applied_production_rules:
                max_act = max(max_act, r.rule_id)
                min_act = min(min_act, r.rule_id)
                id2rule[r.rule_id] = r.rule
            rule_ids = [rule.rule_id for rule in applied_production_rules]
            actions.append(rule_ids)
        #print(max_act, min_act)
        assert min_act == 1 and max_act == self.grammar.num_rules - 1
        leng = len(actions)
        batches = []
        for i in range(0, leng, self.batch_size):
            batch_questions = self.questions[i: min(i + self.batch_size, leng)]
            batch_actions = actions[i: min(i + self.batch_size, leng)]
            batches.append(self.padding(batch_questions, batch_actions))
        return batches, id2rule, productions

    def rank(self, questions, logical_forms):
        data = list(zip(questions, logical_forms))
        data = list(sorted(data, key=lambda x: len(x[0])))
        return [e[0] for e in data], [e[1] for e in data]

    def padding(self, batch_questions, batch_actions):
        src_lens = [len(question) for question in batch_questions]
        actions_in = [[PAD] + actions for actions in batch_actions]
        actions_out = [actions + [PAD] for actions in batch_actions]

        batch_questions = pad_batch_tensorize(batch_questions, PAD, self.cuda)
        actions_in = pad_batch_tensorize(actions_in, PAD, self.cuda)
        actions_out = pad_batch_tensorize(actions_out, PAD, self.cuda)

        return Batch(batch_questions, src_lens, actions_in, actions_out)