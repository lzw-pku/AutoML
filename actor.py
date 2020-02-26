from estimator import Estimator
from transform import Transformer
import grammars.geo.prolog_grammar as prolog_grammar


class Actor:
    def __init__(self, args):
        self.estimator = Estimator(emb_dim=args.emb_dim, n_hidden=args.n_hidden, bidirectional=args.bi,
                                       n_layer=args.n_layer, dropout=args.dropout, lr=args.lr,
                                       decay=args.decay, lr_p=args.lr_p, clip=args.clip,
                                       batch_size=args.batch, epoch_num=args.epoch_num, cuda=args.cuda,
                                       path = args.path)

        self.transformer = Transformer(prolog_grammar.GRAMMAR_DICTIONARY,
                                       prolog_grammar.ROOT_RULE)


    def step(self):
        self.transformer.creat_nt('"_population"')
        self.transformer.merge_nt(['is_area', 'is_captial_of'])
        self.transformer.combine_nt('predicate', 'conjunction')
        grammar_dict, root_rule = self.transformer.get_grammar_dict()
        #self.estimator.estimate(*self.transformer.get_grammar_dict())
        self.estimator.estimate(grammar_dict, root_rule)