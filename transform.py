import copy
from grammars.grammar import Grammar
import re


def safe_replace(string, old, new):
    def replace(matched):
        s = matched.group()
        return s.replace(old, new)
    return re.sub(f'(\(| |^){old}(\)| |$)', replace, string)


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
        assert terminal.startswith('"') and terminal.endswith('"') and terminal in self.terminals
        new_t = 'new_terminal' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)
        for production in self.productions:
            production[1] = list(map(lambda x: new_t if x == terminal else x, production[1]))
        self.productions.append([new_t, [terminal]])

        for k in self._grammar_dictionary.keys():
            self._grammar_dictionary[k] = list(map(lambda s: safe_replace(s, terminal, f' {new_t} '),
                                                   self._grammar_dictionary[k]))
        self._grammar_dictionary[new_t] = [terminal]

    def merge_nt(self, nonterminal_list):
        assert self.check_merge(nonterminal_list)
        new_t = 'new_terminal' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)
        for production in self.productions:
            production[1] = list(map(lambda x: new_t if x in nonterminal_list else x, production[1]))
        tmp_productions = []
        for production in self.productions:
            if production not in tmp_productions:
                tmp_productions.append(production)
        self.productions = tmp_productions
        for nonterminal in nonterminal_list:
            self.productions.append([new_t, [nonterminal]])

        def replace(s):
            for nonterminal in nonterminal_list:
                s = safe_replace(s, nonterminal, new_t)
            return s

        for k in self._grammar_dictionary.keys():
            self._grammar_dictionary[k] = list(map(replace, self._grammar_dictionary[k]))
            self._grammar_dictionary[k] = list(set(self._grammar_dictionary[k]))
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


    def delete_prod(self, nonterminal):
        #pass
        #k, v = self.productions[prod_id]
        #for
        #self.productions[prod_id] = None
        assert len(self._grammar_dictionary[nonterminal]) == 1
        rhs = None
        for k, v in self.productions:
            if k == nonterminal:
                rhs = copy.deepcopy(v) # !!!
                break
        self.productions.remove([nonterminal, rhs])
        self.non_terminals.remove(nonterminal)
        for production in self.productions:
            flag = True
            while flag:
                flag = False
                for i in range(len(production[1])):
                    if production[1][i] == nonterminal:
                        flag = True
                        break
                if flag:
                    production[1] = production[1][:i] + rhs + production[1][(i + 1):]

        rhs = self._grammar_dictionary[nonterminal][0].strip('()') # str
        self._grammar_dictionary.pop(nonterminal)
        for k in self._grammar_dictionary.keys():
            self._grammar_dictionary[k] = list(map(lambda x:
                                                   '(' + rhs + ')' if x == nonterminal
                                                   else safe_replace(x, nonterminal, rhs),
                                                   self._grammar_dictionary[k]))

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
                                #print(nonterminal, k, v, x)
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

    def get_act_space(self):
        import time
        t1 = time.time()
        creat_nt = list(self.terminals)
        merge_nt = []
        non_terminals = copy.deepcopy(self.non_terminals)
        for nt1 in self.non_terminals:
            if any([nt1 in group for group in merge_nt]):
                continue
            tmp = [nt1]
            for nt2 in non_terminals:
                if nt1 != nt2 and self.check_merge([nt1, nt2]):
                    tmp.append(nt2)
            if len(tmp) > 1:
                merge_nt.append(copy.deepcopy(tmp))
            for nt in tmp:
                non_terminals.remove(nt)
        t2 = time.time()
        combine_nt = []
        for nt1 in self.non_terminals:
            for nt2 in self.non_terminals:
                if nt1 != nt2 and self.check_combine(nt1, nt2):
                    combine_nt.append((nt1, nt2))
        t3 = time.time()
        delete_nt = []
        m = {}
        for k, _ in self.productions:
            if k in m.keys():
                m[k] += 1
            else:
                m[k] = 1
        for k in m.keys():
            if m[k] == 1 and k != 'statement' and k != 'answer':
                delete_nt.append(k)
        return creat_nt, merge_nt, combine_nt, delete_nt