from estimator import Estimator
from transform import Transformer
import grammars.geo.prolog_grammar as prolog_grammar
import random
import pickle

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

    def search(self):
        self.perform('initial')
        for i in range(30):
            print(i)
            try:
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
        action_space = self.transformer.get_act_space()
        method = []
        i = -1
        while len(method) == 0:
            i = random.randint(0, 3)
            method = action_space[i]
        action = random.choice(method)
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
        perform = self.estimator.estimate(grammar_dict, root_rule, toy=False, name=repr(name))
        self.performances.append(perform)
        print(perform)
        #self.estimator.estimate(*self.transformer.get_grammar_dict())
        #self.transformer.creat_nt('"_population"')
        #self.transformer.merge_nt(['is_area', 'is_captial_of'])
        #self.transformer.combine_nt('predicate', 'conjunction')
        #self.transformer.delete_prod('largest')

    def exp(self):
        for _ in range(10):
            self.step()
        self.perform()