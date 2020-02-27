import torch
import argparse
from grammars.geo import prolog_grammar
from transform import Transformer


from actor import Actor
from utils import read_prolog_data
def train(args):
    actor = Actor(args)
    for i in range(100):
        actor.exp(i)
        #exit(0)

    #actor.search()
    '''
    t = Transformer(prolog_grammar.GRAMMAR_DICTIONARY, prolog_grammar.ROOT_RULE)
    t.creat_nt('"_population"')
    t.merge_nt(['is_area', 'is_captial_of'])
    t.combine_nt('predicate', 'conjunction')
    grammar_dict, root_rule = t.get_grammar_dict()
    from grammars.grammar import Grammar
    g1 = Grammar(grammar_dict, root_rule)
    (train_questions, test_questions), \
    (train_logical_forms, test_logical_forms) = read_prolog_data()
    logical_forms = train_logical_forms + test_logical_forms
    for form in logical_forms:
        g1.parse(form)
    '''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='training of the AutoML'
    )
    parser.add_argument('--path', required=True, help='root of the model')
    parser.add_argument('--model', required=False, help='path of the saved model')

    parser.add_argument('--emb_dim', type=int, action='store', default=200,
                        help='the dimension of word embedding')
    parser.add_argument('--n_hidden', type=int, action='store', default=128,
                        help='the number of hidden units of LSTM')
    parser.add_argument('--n_layer', type=int, action='store', default=1,
                        help='the number of layers of LSTM')
    parser.add_argument('--no-bi', action='store_true',
                        help='disable bidirectional LSTM encoder')

    # length limit
    #parser.add_argument('--max_input_len', type=int, action='store', default=200,
    #                    help='maximun words in a single sentence')
    #parser.add_argument('--max_action_len', type=int, action='store', default=30,
    #                    help='maximun actions in an output action sequence')
    # training options
    parser.add_argument('--lr', type=float, action='store', default=1e-3,
                        help='learning rate')
    parser.add_argument('--dropout', type=float, action='store', default=0,
                        help='dropout')
    parser.add_argument('--decay', type=float, action='store', default=0.5,
                        help='learning rate decay ratio')
    parser.add_argument('--lr_p', type=int, action='store', default=6,
                        help='patience for learning rate decay')
    parser.add_argument('--clip', type=float, action='store', default=2.0,
                        help='gradient clipping')
    parser.add_argument('--batch', type=int, action='store', default=32,
                        help='the training batch size')
    parser.add_argument('--epoch_num', type=int, action='store', default=500,
                        help='the number of training epoches')
    #parser.add_argument(
    #    '--ckpt_freq', type=int, action='store', default=3000,
    #    help='number of update steps for checkpoint and validation'
    #)
    parser.add_argument('--patience', type=int, action='store', default=5,
                        help='patience for early stopping')

    parser.add_argument('--no-cuda', action='store_true',
                        help='disable GPU training')
    args = parser.parse_args()
    args.bi = not args.no_bi
    args.cuda = torch.cuda.is_available() and not args.no_cuda

    train(args)