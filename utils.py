from grammars.utils import normalize_prolog_variable_names
import random
import torch
import torch.nn.functional as F
import math


PAD = 0

def make_vocab(sentences, emb_dim):
    word2id = {}
    word2id['<pad>'] = PAD
    id2word = ['<pad>']
    word_vector = []
    for _ in id2word:
        word_vector.append([random.random() - 0.5 for _ in range(emb_dim)])
    num = 1
    for s in sentences:
        s = s.split()
        for w in s:
            if w not in word2id.keys():
                word2id[w] = num
                id2word.append(w)
                num += 1

    with open(f'data/wordvector/glove.6B.{emb_dim}d.txt', 'r') as f:
        w2v = f.readlines()
        w2v = [w.split() for w in w2v]
        w2v = {w[0]: [float(x) for x in w[1:]] for w in w2v}

    for w in id2word[num:]:
        if w in w2v.keys():
            word_vector.append(w2v[w])
        else:
            word_vector.append([random.random() - 0.5 for _ in range(emb_dim)])

    return word2id, id2word, word_vector





def read_tsv(path, preprocess=None):
    questions, logical_forms = list(), list()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            questions.append(line.split('\t')[0])
            if preprocess is None:
                logical_forms.append(line.split('\t')[1].replace(' ', '').replace("'", "").lower())
            else:
                logical_forms.append(preprocess(line.split('\t')[1]))
    return questions, logical_forms


def read_prolog_data():
    test_data = './data/geo/geo_prolog_test.tsv'
    train_data = './data/geo/geo_prolog_train.tsv'
    train_questions, train_logical_forms = read_tsv(train_data)
    test_questions, test_logical_forms = read_tsv(test_data)

    for idx, p in enumerate(train_logical_forms):
        train_logical_forms[idx] = normalize_prolog_variable_names(p).lower()
    for idx, p in enumerate(test_logical_forms):
        test_logical_forms[idx] = normalize_prolog_variable_names(p).lower()

    #quesetions, prologs = train_questions + test_questions, train_logical_forms + test_logical_forms
    #for idx, p in enumerate(prologs):
    #    prologs[idx] = normalize_prolog_variable_names(p).lower()
    return (train_questions, test_questions), (train_logical_forms, test_logical_forms)


def pad_batch_tensorize(inputs, pad, cuda=True):
    """pad_batch_tensorize

    :param inputs: List of size B containing torch tensors of shape [T, ...]
    :type inputs: List[np.ndarray]
    :rtype: TorchTensor of size (B, T, ...)
    """
    tensor_type = torch.cuda.LongTensor if cuda else torch.LongTensor
    batch_size = len(inputs)
    max_len = max(len(ids) for ids in inputs)
    tensor_shape = (batch_size, max_len)
    tensor = tensor_type(*tensor_shape)
    tensor.fill_(pad)
    for i, ids in enumerate(inputs):
        tensor[i, :len(ids)] = tensor_type(ids)
    return tensor


def sequence_loss(logits, targets, pad_idx=0):
    """ functional interface of SequenceLoss"""
    assert logits.size()[:-1] == targets.size()
    mask = targets != pad_idx
    target = targets.masked_select(mask)
    logit = logits.masked_select(
        mask.unsqueeze(2).expand_as(logits)
    ).contiguous().view(-1, logits.size(-1))
    loss = F.cross_entropy(logit, target)
    assert (not math.isnan(loss.mean().item())
            and not math.isinf(loss.mean().item()))
    return loss