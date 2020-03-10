import matplotlib.pyplot as plt
import pickle
import numpy as np
import re

from utils import read_sql_data
from grammars.grammar import Grammar
import grammars.atis.sql_grammar as sql_grammar




s = [    "'0'", "'12'", "'1200'", "'1630'", "'1759'", "'1800'", "'1991'", "'2000'", "'201'", "'21'", "'2200'",
         "'2400'", "'416'", "'430'", "'539'", "'600'", "'630'", "'746'", "'800'", "'838'", "'98'",
         "'arrival_time0'", "'arrival_time1'", "'arrival_time2'", "'connections0'", "'day_number0'",
         "'day_number1'", "'departure_time0'", "'departure_time1'", "'departure_time2'", "'departure_time3'",
         "'flight_number0'", "'flight_number1'", "'month_number0'", "'one_direction_cost0'",
         "'round_trip_cost0'", "'stops0'", "'time_elapsed0'", "'year0'", "'year1'"]
s = [x.replace('\'', '"') for x in s]
print(s)
exit(0)

(train_question, test_question), (train_logic, test_logic) =read_sql_data()
for i in range(2930, 2936):
    print(i, train_question[i])
string = set()
for i, logic in enumerate(train_logic + test_logic):
    #if i == 2932:
    #    print(logic)
    #    print([x[0] for x in re.findall('= ([^\.]*?)( |\)|$)', logic)])
    #    exit(0)
    string.update([x[0] for x in re.findall('= ([^\.]*?)( |\)|$)', logic)])
#assert '\'airport_code0\'' in string
#for s in string:
#    print(s)
#x = 'AS AIRPORTalias0 WHERE AIRPORTalias0.AIRPORT_CODE = "YYZ" ;'
#print(re.findall('= ([^\.]*?)( |\))', x))
#exit(0)
#print(string)
#exit(0)
string.remove('select')
string.remove('(select')
print(len(string))
#for s in string:
#    print(s)
string = [repr(x) for x in string]
string2 = sql_grammar.GRAMMAR_DICTIONARY['string']
print(len(string), len(string2))
for s in string2:
    if s not in string:
        print(s)
    #assert s in string
#print(string)
string = list(sorted(list(set(string + string2))))
print(len(string))
print(string)
exit(0)

'''

m = sql_grammar.GRAMMAR_DICTIONARY
string = m['string']
table = m['table_name']
tabel_alias = m['table_alias']
col = m['column_name']
#col_alias = m['column_alias']

#terminal = string #+ table + tabel_alias + col #+ col_alias
terminal = col
terminal = [x.strip('"').strip('\'') for x in terminal][1:]
print(terminal)
print(len(terminal))
for t1 in terminal:
    for t2 in terminal:
        if t1 != t2 and re.match(t1, t2):
            print(t1, t2)
            break
exit(0)




with open('data/atis/sql_table.pkl', 'rb') as f:
    table = pickle.load(f)
    col_name = set()
    for cols in table.values():
        for col in cols:
            col_name.add(col)
    col_name = list(col_name)
    col_name = [f'"{x.lower()}"' for x in col_name]



    col_name = [x.strip('"') for x in col_name]
    table_name = [x.lower() for x in table.keys()]

print(col_name)
print(table_name)

(train_question, test_question), (train_logic, test_logic) =read_sql_data()

string = set()
for logic in train_logic + test_logic:
    logic = logic.lower()
    #print(logic)
    s = re.findall('\'(.*?)\'', logic)
    string.update(s)
    s = re.findall('\"(.*?)\"', logic)
    string.update(s)
string = list(sorted([f'"{x}"' for x in string]))
print(string)
#exit(0)
alias = set()
for logic in train_logic + test_logic:
    logic = logic.lower()
    s = re.findall(' as ([^ ]*?alias[0-9]+) ', logic)
    alias.update(s)
print(alias)
print(len(alias))
table_ali = []
col_ali = []
for ali in alias:
    assert ali[-2] not in [str(i) for i in range(10)]
    assert ali[:-1].endswith('alias')
    tmp = ali[:-6]
    #print(tmp)
    assert tmp in table_name or tmp in col_name
    if tmp in table_name:
        table_ali.append(ali)
    if tmp in col_name:
        col_ali.append(ali)

table_ali = list(sorted(table_ali))
col_ali = list(sorted(col_ali))
table_ali = [f'"{x}"' for x in table_ali]
print(table_ali)
print(col_ali)
exit(0)
'''



grammar = Grammar(sql_grammar.GRAMMAR_DICTIONARY, sql_grammar.ROOT_RULE)
(train_question, test_question), (train_logic, test_logic) =read_sql_data()


d = set()
#print(grammar.get_production_rule_by_id(222))
for logic in train_logic + test_logic:
    applied_production_rules = grammar.parse(logic)
    rule_ids = [rule.rule_id for rule in applied_production_rules]
    for i in rule_ids:
        if i >= 120 and i <= 1446:
            d.add(i)
print(d)
print(len(d))
from grammars.geo.sql_grammar import GRAMMAR_DICTIONARY
m = GRAMMAR_DICTIONARY['string']
new_m = set()
for i in d:
    s = eval(grammar.get_production_rule_by_id(i).rhs)[0]
    flag = False
    for v in m:
        if re.search(s, v) is not None and v not in new_m:
            assert not flag
            flag = True
            new_m.add(v)
    assert flag


#print(train_logic[0])
print(new_m)
assert len(new_m) == len(d)
print(m)
print(list(new_m))
exit(0)
#print(len(m))
'''
for i in range(120, 1447):
    p = grammar.get_production_rule_by_id(i)
    print(p.lhs)
    assert grammar.get_production_rule_by_id(i).lhs == 'string'

for k, v in grammar._rule2id.items():
    if k.startswith('string'):
        print(k, v)
exit(0)
'''


def read(name):
    with open(f'result/nohup_{name}') as f:
        l = f.readlines()
        l = list(filter(lambda x: x.startswith('0.'), l))
        l = np.asarray([float(x) for x in l])
    return l

data = []
for i in [30, 50, 100]:
    l = read(f'new_random_{i}_new')
    data.append(l)

for l in data:
    print(len(l), np.mean(l), np.max(l), np.min(l), np.std(l))

print('\n\n')
l = read('max_10000')
print(len(l), np.mean(l), np.max(l), np.min(l), np.std(l))
l = read('min_10000')
print(len(l), np.mean(l), np.max(l), np.min(l), np.std(l))



'''
l1 = [0.6821428571428572, 0.6678571428571428, 0.675, 0.6892857142857143, 0.6892857142857143, 0.7,
     0.6428571428571429, 0.6714285714285714, 0.6571428571428571, 0.6928571428571428,
     0.6571428571428571, 0.6892857142857143, 0.675, 0.7142857142857143, 0.6857142857142857,
     0.6892857142857143, 0.7107142857142857, 0.7142857142857143, 0.6642857142857143,
     0.6928571428571428, 0.6857142857142857, 0.6857142857142857, 0.6785714285714286,
     0.6642857142857143, 0.6892857142857143, 0.6642857142857143]

l2 = [0.6821428571428572, 0.6714285714285714, 0.6571428571428571, 0.6892857142857143, 0.675,
      0.6928571428571428, 0.6642857142857143, 0.6964285714285714, 0.675, 0.6892857142857143,
      0.7285714285714285, 0.7, 0.6821428571428572, 0.6428571428571429, 0.6607142857142857,
      0.6714285714285714, 0.6785714285714286, 0.675, 0.6892857142857143, 0.6821428571428572,
      0.6464285714285715, 0.6535714285714286, 0.6821428571428572, 0.675, 0.6642857142857143,
      0.6785714285714286]

l3 = [0.6821428571428572, 0.6785714285714286, 0.6857142857142857, 0.6785714285714286,
      0.6642857142857143, 0.6607142857142857, 0.6892857142857143, 0.6714285714285714,
      0.6428571428571429, 0.6964285714285714, 0.6964285714285714, 0.6892857142857143,
      0.6535714285714286, 0.6821428571428572, 0.6857142857142857, 0.6892857142857143,
      0.6678571428571428, 0.6857142857142857, 0.675, 0.6892857142857143, 0.65, 0.6892857142857143,
      0.65, 0.6928571428571428, 0.6714285714285714, 0.675]

l4 = [0.6821428571428572, 0.6892857142857143, 0.6785714285714286, 0.6857142857142857,
      0.6714285714285714, 0.6928571428571428, 0.6928571428571428, 0.6714285714285714,
      0.6642857142857143, 0.6678571428571428, 0.6678571428571428, 0.7, 0.6785714285714286,
      0.6892857142857143, 0.6642857142857143, 0.6321428571428571, 0.6678571428571428,
      0.6857142857142857, 0.6607142857142857, 0.6785714285714286, 0.6785714285714286,
      0.6714285714285714, 0.675, 0.6571428571428571, 0.6785714285714286, 0.6714285714285714]

l5 = [0.6821428571428572, 0.6785714285714286, 0.6892857142857143, 0.6857142857142857,
      0.6678571428571428, 0.7035714285714286, 0.6714285714285714, 0.7071428571428572,
      0.7071428571428572, 0.6607142857142857, 0.7142857142857143, 0.6964285714285714,
      0.6821428571428572, 0.6892857142857143, 0.675, 0.6607142857142857, 0.7107142857142857,
      0.6857142857142857, 0.6857142857142857, 0.6857142857142857, 0.6857142857142857,
      0.7035714285714286, 0.625]
x = [i for i in range(1000)]
#y = [71.07,   66.79,  70,   69.64,   68.57,    70,   67.5]
y = [0.7071428571428572, 0.6964285714285714, 0.65, 0.6714285714285714, 0.6821428571428572,
     0.6821428571428572, 0.6928571428571428, 0.6607142857142857, 0.6607142857142857,
     0.6928571428571428, 0.6964285714285714, 0.6785714285714286, 0.6642857142857143,
     0.6642857142857143, 0.675, 0.6857142857142857, 0.6428571428571429, 0.7142857142857143,
     0.6571428571428571, 0.6357142857142857, 0.6678571428571428, 0.6642857142857143, 0.675,
     0.6821428571428572, 0.6714285714285714, 0.6857142857142857, 0.7071428571428572, 0.65,
     0.6821428571428572, 0.6571428571428571, 0.6642857142857143, 0.7, 0.7, 0.6892857142857143,
     0.6714285714285714, 0.6785714285714286, 0.6821428571428572, 0.6785714285714286,
     0.6964285714285714, 0.6928571428571428, 0.6964285714285714, 0.6535714285714286,
     0.7142857142857143, 0.6928571428571428]

yy = [0.7035714285714286, 0.6964285714285714, 0.7214285714285714, 0.6678571428571428,
      0.6428571428571429, 0.675, 0.7035714285714286, 0.7107142857142857, 0.6571428571428571,
      0.6857142857142857, 0.7071428571428572, 0.6857142857142857, 0.6928571428571428,
      0.6642857142857143, 0.6892857142857143, 0.6857142857142857, 0.6857142857142857,
      0.675, 0.6821428571428572, 0.6928571428571428, 0.6928571428571428, 0.6642857142857143,
      0.6964285714285714, 0.6785714285714286, 0.6857142857142857, 0.6714285714285714,
      0.6892857142857143, 0.675, 0.6857142857142857, 0.6928571428571428, 0.6642857142857143,
      0.6571428571428571, 0.6714285714285714, 0.6821428571428572, 0.6678571428571428, 0.7,
      0.6714285714285714, 0.675, 0.6857142857142857, 0.6821428571428572, 0.6535714285714286,
      0.6607142857142857, 0.6785714285714286, 0.6821428571428572, 0.6642857142857143,
      0.6178571428571429, 0.6607142857142857, 0.6821428571428572, 0.6892857142857143,
      0.6535714285714286, 0.675, 0.6678571428571428, 0.675, 0.675, 0.6428571428571429,
      0.6714285714285714, 0.675, 0.6821428571428572, 0.6964285714285714, 0.6785714285714286,
      0.6928571428571428, 0.7, 0.6714285714285714, 0.6964285714285714, 0.6535714285714286, 0.675]
print(sum(yy) / len(yy))
plt.plot(x[:len(yy)],yy,color='red')
#plt.plot(x[:len(l2)],l2,color='y')
#plt.plot(x[:len(l3)],l3,color='b')
#plt.plot(x[:len(l4)],l4,color='g')
#plt.plot(x[:len(l5)],l5,color='black')
#plt.plot(x_data,y_data2,color='blue',linewidth=3.0,linestyle='-.')
plt.show()
'''




'''
with open('nohup_random_20', 'r') as f:
    l = f.readlines()
    l = list(filter(lambda x: x.startswith('0'), l))
    
    
l = [float(x) for x in l]
print(l)

'''