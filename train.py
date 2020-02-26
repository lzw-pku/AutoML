import torch
import argparse
from grammars.geo import prolog_grammar
from transform import Transformer


from actor import Actor

def train(args):
    actor = Actor(args)
    actor.step()
    #b1 = estimator.dataset.parse(prolog_grammar.GRAMMAR_DICTIONARY, prolog_grammar.ROOT_RULE)
    exit(0)
    t = Transformer(prolog_grammar.GRAMMAR_DICTIONARY, prolog_grammar.ROOT_RULE)
    #b2 = estimator.dataset.parse(*t.get_grammar_dict())

    #print(t.get_grammar_dict())
    #t.creat_nt('"("')
    grammar_dict, _ = t.get_grammar_dict()
    #print(grammar_dict)
    #exit(0)
    '''
    for k, v in prolog_grammar.GRAMMAR_DICTIONARY.items():
        v1 = grammar_dict[k]
        for s in v:
            if s not in v1:
                print(k)
                print(v)
                print(v1)
                #continue
        
        for s in v1:
            if s not in v:
                print(k)
                print(v)
                print(v1)
                #exit(0)
    '''
    #for key, value in grammar_dict.items():
    #    print(key, value)
    #estimator.estimate(prolog_grammar)
    #Actor = pass

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
    parser.add_argument('--lr', type=float, action='store', default=1e-1,
                        help='learning rate')
    parser.add_argument('--dropout', type=float, action='store', default=0,
                        help='dropout')
    parser.add_argument('--decay', type=float, action='store', default=0.5,
                        help='learning rate decay ratio')
    parser.add_argument('--lr_p', type=int, action='store', default=0,
                        help='patience for learning rate decay')
    parser.add_argument('--clip', type=float, action='store', default=2.0,
                        help='gradient clipping')
    parser.add_argument('--batch', type=int, action='store', default=32,
                        help='the training batch size')
    parser.add_argument('--epoch_num', type=int, action='store', default=1000,
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