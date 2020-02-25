import copy
from grammars.grammar import Grammar
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
        new_t = 'NEW_TERMINAL' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)
        for production in self.productions:
            production[1] = list(map(lambda x: new_t if x == terminal else x, production[1]))
        self.productions.append((new_t, [terminal]))
        return self.get_grammar_dict()

    def merge_nt(self, nontermnal_list):
        new_t = 'NEW_TERMINAL' + str(self.nonterminal_num)
        self.nonterminal_num += 1
        self.non_terminals.add(new_t)

    def get_grammar_dict(self):
        grammar_dict = {}
        for production in self.productions:
            key, rhs = production
            tmp = ' ws '.join(rhs)
            '''
            for s in rhs:
                if s in self.non_terminals:
                    tmp = '(' + tmp + ')'
                    break
            '''
            #if rhs[0] not in self.terminals:
            #    tmp = '(' + tmp + ')'
            if len(rhs) > 1:
                tmp = f'({tmp})'
            if key not in grammar_dict:
                grammar_dict[key] = [tmp]
            else:
                grammar_dict[key].append(tmp)
        grammar_dict["ws"] = ['~"\s*"i']
        return (grammar_dict, self.root_rule)
#from grammars.geo import prolog_grammar
#t = Transformer(prolog_grammar)