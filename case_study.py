import torch
from seq2seq.seq2seq import Seq2seqModel
import argparse
from estimator import Estimator
from utils import PAD
from grammars.geo.prolog_grammar import GRAMMAR_DICTIONARY as grammar_dict, ROOT_RULE as root_rule
from utils import normalize_prolog_variable_names
from grammars.utils import action_sequence_to_logical_form


def exp(args):
    estimator = Estimator(emb_dim=args.emb_dim, n_hidden=args.n_hidden, bidirectional=args.bi,
                          n_layer=args.n_layer, dropout=args.dropout, lr=args.lr,
                          decay=args.decay, lr_p=args.lr_p, clip=args.clip,
                          batch_size=args.batch, epoch_num=args.epoch_num, cuda=args.cuda,
                          path = args.path)

    (train_batches, test_batches), id2rule, productions = estimator.dataset.parse(grammar_dict,
                                                                                  root_rule)

    nonterminal2id, id2nonterminal = estimator.build_decode_dict(productions)

    model = Seq2seqModel(vocab_size=args.vocab_size, emb_dim=args.emb_dim,
                         n_hidden=args.n_hidden,
                         output_size = estimator.dataset.grammar.num_rules + 1,
                         bidirectional=args.bidirectional, n_layer=args.n_layer,
                         dropout=args.dropout)
    m = torch.load('')

    model.load_state_dict(m)



    model.eval()
    total = 0
    true_example = 0
    for batch in test_batches:
        batch_actions = model.batch_decode(batch.questions,
                                                batch.src_lens, PAD, 200,
                                                nonterminal2id, id2nonterminal)[0]
        #id2rule也许可以被production替代
        batch_actions = torch.stack(batch_actions).transpose(0, 1)
        total += len(batch_actions)
        for actions, logical_form in zip(batch_actions, batch.logical_forms):
            for i in range(len(actions)):
                if int(actions[i]) == 0:
                    actions = actions[:i]
                    break
            rule_str = [id2rule[int(act)] for act in actions]
            rule = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
            if rule == logical_form:
                true_example += 1
            else:
                print(rule)
                print(logical_form)
                print(rule_str)
                print('*' * 80)






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

    exp(args)