from estimator import Estimator
from transform import Transformer
import grammars.geo.prolog_grammar as prolog_grammar
import random
import pickle
import os
'''
t = Transformer(prolog_grammar.GRAMMAR_DICTIONARY, prolog_grammar.ROOT_RULE)
t.merge_nt(['is_capital', 'is_mountain', 'is_major', 'is_place', 'is_river', 'is_state', 'is_lake', 'is_city'])
for k, v in t.get_grammar_dict()[0].items():
    print(k, v)
exit(0)
'''
'''
t.creat_nt('"_capital"')
t.delete_prod('is_captial_of')
t.creat_nt('"1.0"')
t.creat_nt('"_stateid"')
t.delete_prod('len')
t.delete_prod('is_city')
t.creat_nt('"_longer"')
t.merge_nt(['is_capital', 'is_mountain', 'is_major', 'is_place', 'is_river', 'is_state', 'is_lake'])
t.delete_prod('longest')
t.delete_prod('unit_relation')
for k, v in t.productions:
    print(k, v)
exit(0)
'''
class Actor:
    def __init__(self, args):
        self.estimator = Estimator(emb_dim=args.emb_dim, n_hidden=args.n_hidden, bidirectional=args.bi,
                                       n_layer=args.n_layer, dropout=args.dropout, lr=args.lr,
                                       decay=args.decay, lr_p=args.lr_p, clip=args.clip,
                                       batch_size=args.batch, epoch_num=args.epoch_num, cuda=args.cuda,
                                       path = args.path)

        self.transformer = Transformer(prolog_grammar.GRAMMAR_DICTIONARY,
                                       prolog_grammar.ROOT_RULE)

        self.performances = []
        self.actions = []
        self.path = args.path

    def search(self):
        self.perform('initial')
        #exit(0)
        for i in range(25):
            print(i)
            try:
                self.step()
                self.perform(i)
            except BaseException as e:
                print(e)
                print(self.actions)
                print(self.performances)
                with open('gra.pkl', 'wb') as f:
                    pickle.dump(self.transformer.get_grammar_dict(), f)
                exit(-1)
        print(self.performances)
            #exit(0)

    def step(self):
        import time
        t1 = time.time()
        action_space = self.transformer.get_act_space()
        t2 = time.time()
        method = []
        i = -1
        while len(method) == 0:
            i = random.randint(0, 3)
            method = action_space[i]
        action = random.choice(method)
        print(i, action)
        if i == 0:
            self.transformer.creat_nt(action)
        elif i == 1:
            self.transformer.merge_nt(action)
        elif i == 2:
            self.transformer.combine_nt(*action)
        else:
            assert i == 3
            self.transformer.delete_prod(action)
        self.actions.append((i, action))

    def perform(self, name):
        grammar_dict, root_rule = self.transformer.get_grammar_dict()
        with open(os.path.join(self.path, f'grammar-{name}'), 'wb') as f:
            pickle.dump(self.transformer, f)
        perform = self.estimator.estimate(grammar_dict, root_rule, toy=False, name=repr(name))
        self.performances.append(perform)
        return perform


    def exp(self, name):
        for _ in range(30):
            self.step()
        self.perform(name)
