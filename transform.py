import copy
from grammars.grammar import Grammar
import re


class Transformer:
    def __init__(self, grammar_dict, root_rule):
        grammar = Grammar(grammar_dict, root_rule)
        self._grammar_dictionary = copy.deepcopy(grammar._grammar_dictionary)
        self.root_rule = root_rule
        self.non_terminals = set(self._grammar_dictionary.keys())
        self.productions = grammar._production_rules
        # Production: rule_id: int, rule: str, lhs: str, rhs: str(List[str]), rhs_nonterminal: List[str]
        self.terminals = set()
        productions = []
        for production in self.productions:
            rhs = production.rhs.strip('[] ').split(', ')
            key = production.lhs
            productions.append([key, rhs])
            for w in rhs:
                if w not in self.non_terminals and w not in self.terminals:
                    self.terminals.add(w)
        self.productions = productions
        #    print(production.rhs.lstrip('[').rstrip(']').split())
        self.nonterminal_num = 0

    def creat_nt(self, terminal): # 必须是“ ” 包裹！！！
        assert terminal.startswith('"') and terminal.endswith('"')
        new_t = 'new_terminal' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)
        for production in self.productions:
            production[1] = list(map(lambda x: new_t if x == terminal else x, production[1]))
        self.productions.append([new_t, [terminal]])

        for k in self._grammar_dictionary.keys():
            self._grammar_dictionary[k] = list(map(lambda s: s.replace(terminal, f' {new_t} '),
                                                   self._grammar_dictionary[k]))
        self._grammar_dictionary[new_t] = [terminal]

    def merge_nt(self, nonterminal_list):
        assert self.check_merge(nonterminal_list)
        new_t = 'new_terminal' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)
        for production in self.productions:
            production[1] = list(map(lambda x: new_t if x in nonterminal_list else x, production[1]))
        self.productions.append([new_t, nonterminal_list])

        def replace(s):
            for nonterminal in nonterminal_list:
                s = s.replace(nonterminal, new_t)
            return s

        for k in self._grammar_dictionary.keys():
            self._grammar_dictionary[k] = list(map(replace, self._grammar_dictionary[k]))
            #print(k, self._grammar_dictionary[k])
        self._grammar_dictionary[new_t] = nonterminal_list

    def combine_nt(self, nt1, nt2):
        assert self.check_combine(nt1, nt2)
        new_t = 'new_terminal' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)

        for production in self.productions:
            flag = True
            while flag:
                flag = False
                for i in range(len(production[1]) - 1):
                    if production[1][i] == nt1 and production[1][i + 1] == nt2:
                        flag = True
                        break
                if flag:
                    production[1] = production[1][:i] + [new_t] + production[1][i+2:]
        self.productions.append([new_t, [nt1, nt2]])


        for k in self._grammar_dictionary.keys():
            self._grammar_dictionary[k] = list(map(lambda x: re.sub(nt1 + ' +ws +' + nt2, new_t, x),
                                                   self._grammar_dictionary[k]))
        self._grammar_dictionary[new_t] = [f'({nt1} ws {nt2})']


    def delete_prod(self, prod_id):
        pass
        k, v = self.productions[prod_id]
        #for
        self.productions[prod_id] = None


    def get_grammar_dict(self):
        return self._grammar_dictionary, self.root_rule

    def check_merge(self, nonterminal_list):
        assert len(nonterminal_list) > 1 and all([x in self.non_terminals for x in nonterminal_list])
        for k, v in self._grammar_dictionary.items():
            for x in v:
                for nonterminal in nonterminal_list:
                    if nonterminal in x:
                        for nonterminal1 in nonterminal_list:
                            for x1 in v:
                                if nonterminal1 in x1 and x1.replace(nonterminal1, nonterminal) == x:
                                    break
                            else:
                                print(nonterminal, k, v, x)
                                return False
                        break
        return True

    def check_combine(self, nt1, nt2):
        prod_flag = False
        for _, v in self.productions:
            for i in range(len(v) - 1):
                if v[i] == nt1 and v[i + 1] == nt2:
                    prod_flag = True
                    break
            if prod_flag:
                break
        grammar_flag = False
        for _, vs in self._grammar_dictionary.items():
            for v in vs:
                if re.search(nt1 + ' +ws +' + nt2, v) is not None:
                    grammar_flag = True
                    break
            if grammar_flag:
                break
        return prod_flag and grammar_flag