# coding=utf8

from pprint import pprint
from grammars.geo import prolog_grammar, funql_grammar, sql_grammar
from grammars.grammar import Grammar
from grammars.parse_ast import AST
from grammars.utils import action_sequence_to_logical_form, normalize_prolog_variable_names, normalize_sql


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
    quesetions, prologs = train_questions + test_questions, train_logical_forms + test_logical_forms
    for idx, p in enumerate(prologs):
        prologs[idx] = normalize_prolog_variable_names(p).lower()
    return quesetions, prologs


def read_funql_data():
    test_data = './data/geo/geo_funql_test.tsv'
    train_data = './data/geo/geo_funql_train.tsv'
    train_questions, train_logical_forms = read_tsv(train_data)
    test_questions, test_logical_forms = read_tsv(test_data)
    return train_questions + test_questions, train_logical_forms + test_logical_forms


def read_sql_data():
    test_data = './data/geo/geo_sql_question_based_test.tsv'
    train_data = './data/geo/geo_sql_question_based_train.tsv'
    train_questions, train_logical_forms = read_tsv(train_data, normalize_sql)
    test_questions, test_logical_forms = read_tsv(test_data, normalize_sql)
    return train_questions + test_questions, train_logical_forms + test_logical_forms


if __name__ == '__main__':
    from data import GeoDataset
    import torch
    dataset = GeoDataset(200, torch.tensor(1).device)
    for q, p in zip(dataset.questions, dataset.logical_forms):
        print(q, p)
        exit(0)
    exit(0)
    #grammar = Grammar(sql_grammar.GRAMMAR_DICTIONARY, sql_grammar.ROOT_RULE)
    #questions, logical_forms = read_sql_data()
    grammar = Grammar(prolog_grammar.GRAMMAR_DICTIONARY, prolog_grammar.ROOT_RULE)
    questions, logical_forms = read_prolog_data()

    for pid, (q, p) in enumerate(zip(questions, logical_forms)):
        print(pid)
        print(q)
        print(p)
        pprint(q.split())
        # Sequence to Action
        applied_production_rules = grammar.parse(p)
        rule_ids = [rule.rule_id for rule in applied_production_rules]
        print(rule_ids)
        print(torch.tensor(rule_ids).float())
        exit(0)
        pprint(applied_production_rules)
        #exit(0)
        # AST
        ast = AST(
            root_rule=grammar.get_production_rule_by_id(grammar.root_rule_id),
        )
        for rule in applied_production_rules[1:]:
            ast.add_rule(rule)
        ast_rules = ast.get_production_rules()
        print(len(ast_rules))
        pprint(ast_rules)
        assert ast.is_complete

        # Action to Sequence
        rule_str = list()
        for rule in applied_production_rules:
            rule_str.append(rule.rule)
        _p = normalize_prolog_variable_names(action_sequence_to_logical_form(rule_str))
        print(_p)
        print(p)
        assert _p == p
        print('===\n\n')
        exit(0)
