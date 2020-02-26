# coding=utf8

import copy
from typing import List, Dict
from pprint import pprint
from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar as _Grammar
from grammars.basic import ProductionRule
from grammars.utils import format_grammar_string, initialize_valid_actions, SqlVisitor
from grammars.geo import prolog_grammar, funql_grammar, sql_grammar


class Grammar:

    def __init__(self, grammar_dictionary: Dict, root_rule: str):
        self._grammar_dictionary = copy.deepcopy(grammar_dictionary)

        # Non terminals
        self._non_terminals = sorted(list(self._grammar_dictionary.keys()))
        _grammar = _Grammar(format_grammar_string(self._grammar_dictionary))
        self._grammar = _grammar
        valid_actions = initialize_valid_actions(_grammar)
        all_actions = set()
        for action_list in valid_actions.values():
            all_actions.update(action_list)
        production_rule_strs = sorted(all_actions)

        self._root_rule = root_rule

        self._production_rules = list()
        self._nonterminals_dict = dict()
        self._rule2id = dict()
        self._id2rule = dict()
        rule_id = 1
        for production_rule_str in production_rule_strs:
            nonterminal, rhs = production_rule_str.split(' -> ')
            production_rule_str = ' '.join(production_rule_str.split(' '))
            assert nonterminal in self._non_terminals
            rhs_nonterminal = [term for term in rhs.strip('[] ').split(', ') if term in self._non_terminals]
            self._production_rules.append(ProductionRule(rule_id, production_rule_str, nonterminal, rhs, rhs_nonterminal))
            self._rule2id[production_rule_str] = rule_id
            self._id2rule[rule_id] = self._production_rules[-1]
            if nonterminal not in self._nonterminals_dict:
                self._nonterminals_dict[nonterminal] = list()
            self._nonterminals_dict[nonterminal].append(self._production_rules[-1])
            rule_id += 1

    @property
    def production_rules(self):
        return self._production_rules
    
    @property
    def root_rule_id(self):
        return self._rule2id[self._root_rule]

    @property
    def root_rule_rhs(self):
        return self.get_non_terminal_id('answer')

    @property
    def num_rules(self):
        return len(self._rule2id)

    @property
    def num_non_terminals(self):
        return len(self._non_terminals)

    def parse(self, query: str):
        sql_visitor = SqlVisitor(self._grammar)
        q = query.lower().replace("``", "'").replace("''", "'")
        try:
            applied_production_rules = sql_visitor.parse(q) if query else []
        except ParseError as e:
            print(e)
            applied_production_rules = list()
        rules = list()
        for rule in applied_production_rules:
            lhs, rhs = rule.split(' -> ')
            rule_str = rule
            rules.append(copy.deepcopy(self.get_production_rule_by_id(self.get_production_rule_id(rule_str))))
        return rules

    def get_production_rule_by_id(self, rule_id) -> ProductionRule:
        if rule_id not in self._id2rule:
            return None
        return self._id2rule[rule_id]

    def get_production_rule_ids_by_nonterminal_id(self, nonterminal_id: int) -> List[int]:
        nonterminal = self._non_terminals[nonterminal_id]
        production_rules = self._nonterminals_dict[nonterminal]
        return [p.rule_id for p in production_rules]
    
    def get_production_rule_ids_by_nonterminal(self, nonterminal: str) -> List[int]:
        production_rules = self._nonterminals_dict[nonterminal]
        return [p.rule_id for p in production_rules]

    def get_production_rules_by_nonterminal(self, nonterminal: str) -> List[ProductionRule]:
        return self._nonterminals_dict[nonterminal]

    def get_production_rule_id(self, production_rule: str) -> int:
        return self._rule2id[production_rule]

    def get_non_terminal_id(self, nonterminal):
        return self._non_terminals.index(nonterminal)

    def get_non_terminal(self, nonterminal_id):
        if nonterminal_id >= len(self._non_terminals):
            return None
        return self._non_terminals[nonterminal_id]

    def get_productions(self):
        return self._production_rules

def get_grammar(dataset, language):
    if dataset == 'geo':
        if language == 'funql':
            return Grammar(funql_grammar.GRAMMAR_DICTIONARY, funql_grammar.ROOT_RULE)
        elif language == 'prolog':
            return Grammar(prolog_grammar.GRAMMAR_DICTIONARY, prolog_grammar.ROOT_RULE)
        elif language == 'sql':
            return Grammar(sql_grammar.GRAMMAR_DICTIONARY, sql_grammar.ROOT_RULE)
    return None
