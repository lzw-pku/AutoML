import matplotlib.pyplot as plt
import pickle
import re
from utils import read_prolog_data
'''
(train_q, test_q), (train_l, test_l) = read_prolog_data()
ROOT_RULE = 'statement -> [answer]'

GRAMMAR_DICTIONARY = {}
GRAMMAR_DICTIONARY['statement'] = ['(answer ws)']
terminal = set()
for l in train_l + test_l:
    l = l.replace("'", "").lower().replace(" ", "").replace("(", " ( ").replace(")", " ) ").replace(",", " , ")
    l = l.split()
    terminal.update(l)


for t1 in terminal:
    for t2 in terminal:
        try:
            if t1 != '(' and t1 != ')' and t1 != t2 and re.match(t1, t2) is not None:
                print(t1, t2)
        except:
            print('!!!', t1, t2)
            exit(0)
terminal = [repr(x).replace('\'', '"') for x in terminal]
terminal = list(reversed(list(sorted(terminal))))
print(terminal)
print(len(terminal))
exit(0)
'''
'''
data = []
for i in range(10, 51, 10):
    print(i)
    with open(f'nohup_random_{i}', 'r') as f:
        l = f.readlines()
        l = list(filter(lambda x: x.startswith('0.'), l))
        l = [float(x) for x in l]
    data.append(l)
with open('random_result.pkl', 'wb') as f:
    pickle.dump(data, f)
'''
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
with open('nohup_step_100', 'r') as f:
    l = f.readlines()
    l = list(filter(lambda x: x.startswith('0.'), l))
    
    
l = [float(x) for x in l]
print(l)
'''










s = '''1 ['meta', 'unit_relation']
1 ['is_place', 'is_lake', 'is_state', 'is_major', 'is_capital', 'is_river', 'is_city', 'is_mountain']
2 ('predicate', 'conjunction')
2 ('predicate', 'conjunction')
2 ('predicate', 'conjunction')
0 "_"
0 "mountwhitney"
2 ('predicate', 'conjunction')
0 "_smallest"
3 is_low_point
2 ('predicate', 'conjunction')
3 unit_relation
3 is_city
1 ['is_place', 'is_lake', 'is_state', 'is_major', 'is_capital', 'is_river', 'is_mountain']
2 ('predicate', 'conjunction')
0 "northcarolina"
1 ['is_place', 'is_lake', 'is_state', 'is_major', 'is_capital', 'is_river', 'is_mountain']
0 "\+"
3 new_terminal3
1 ['is_high_point', 'is_located_in', 'is_longer', 'is_equal', 'is_next_to', 'is_density', 'is_lower', 'is_traverse', 'is_captial_of', 'is_area', 'is_population', 'is_higher', 'is_len', 'is_size', 'is_elevation']
2 ('new_terminal14', 'declaration')
'''

'''
from transform import Transformer
from grammars.geo.prolog_grammar import GRAMMAR_DICTIONARY, ROOT_RULE
transfer = Transformer(GRAMMAR_DICTIONARY, ROOT_RULE)
transfer.get_act_space()
exit(0)
s = s.split('\n')[:-1]
s = s[:-1]
for x in s:
    type = int(x[0])
    if type == 0:
        terminal = x[2:]
        print(type, terminal)
        transfer.creat_nt(terminal)
    elif type == 1:
        ntlist = eval(x[2:])
        print(type, ntlist)
        transfer.merge_nt(ntlist)
    elif type == 2:
        ntlist = eval(x[2:])
        print(type, ntlist)
        transfer.combine_nt(*ntlist)
    elif type == 3:
        prod = x[2:]
        print(type, prod)
        transfer.delete_prod(prod)

for k, v in transfer._grammar_dictionary.items():
    print(k, v)
exit(0)
print(s)

exit(0)



l0 = [0.6928571428571428, 0.6678571428571428, 0.6714285714285714, 0.6607142857142857, 0.7071428571428572, 0.7071428571428572, 0.5, 0.6678571428571428, 0.6535714285714286, 0.6857142857142857, 0.6928571428571428, 0.6607142857142857, 0.7, 0.6857142857142857, 0.6535714285714286, 0.6857142857142857, 0.65, 0.6607142857142857, 0.675, 0.5678571428571428, 0.7, 0.6714285714285714, 0.6642857142857143, 0.6464285714285715, 0.65, 0.6392857142857142, 0.5964285714285714, 0.6428571428571429, 0.6642857142857143, 0.6785714285714286, 0.5857142857142857, 0.6642857142857143, 0.6928571428571428, 0.675, 0.7, 0.43214285714285716, 0.6714285714285714, 0.6571428571428571, 0.6714285714285714, 0.6678571428571428, 0.65, 0.6821428571428572, 0.6714285714285714, 0.6535714285714286, 0.675, 0.6678571428571428, 0.6714285714285714, 0.6785714285714286, 0.6857142857142857, 0.6535714285714286, 0.6857142857142857, 0.6785714285714286, 0.6821428571428572, 0.6714285714285714, 0.6571428571428571, 0.6642857142857143, 0.6857142857142857, 0.6428571428571429, 0.7035714285714286, 0.675, 0.6571428571428571, 0.6928571428571428, 0.6607142857142857, 0.6821428571428572, 0.6857142857142857, 0.675, 0.6785714285714286, 0.675, 0.6428571428571429, 0.7, 0.675, 0.6785714285714286, 0.6321428571428571, 0.6464285714285715, 0.6714285714285714, 0.675, 0.525, 0.6821428571428572, 0.7178571428571429, 0.6571428571428571, 0.6607142857142857, 0.6678571428571428, 0.6892857142857143, 0.6535714285714286, 0.65, 0.6642857142857143, 0.6607142857142857, 0.6821428571428572, 0.7035714285714286, 0.6892857142857143, 0.6678571428571428, 0.675, 0.675, 0.6678571428571428, 0.6571428571428571, 0.6821428571428572, 0.6785714285714286, 0.6857142857142857, 0.6857142857142857, 0.6785714285714286, 0.6964285714285714, 0.6964285714285714, 0.6678571428571428]

l1 = [0.6892857142857143, 0.7142857142857143, 0.6678571428571428, 0.6464285714285715, 0.6928571428571428, 0.7035714285714286, 0.6928571428571428, 0.6928571428571428, 0.7035714285714286, 0.7035714285714286, 0.6857142857142857, 0.6857142857142857, 0.7, 0.6892857142857143, 0.675, 0.7214285714285714, 0.7107142857142857, 0.6642857142857143, 0.6892857142857143, 0.6892857142857143, 0.7285714285714285, 0.6892857142857143, 0.6964285714285714, 0.6892857142857143, 0.7, 0.7107142857142857, 0.725, 0.6964285714285714, 0.6892857142857143, 0.6785714285714286, 0.7107142857142857, 0.7035714285714286, 0.7107142857142857, 0.7, 0.6892857142857143, 0.725, 0.7, 0.6464285714285715, 0.6928571428571428, 0.7142857142857143, 0.6964285714285714, 0.675, 0.7285714285714285, 0.6892857142857143, 0.6714285714285714, 0.6821428571428572, 0.7, 0.7, 0.7285714285714285, 0.6714285714285714, 0.6964285714285714, 0.6821428571428572, 0.6928571428571428, 0.7178571428571429, 0.6964285714285714, 0.6964285714285714, 0.7214285714285714, 0.6964285714285714, 0.6607142857142857, 0.6714285714285714, 0.7, 0.7178571428571429, 0.6857142857142857, 0.7035714285714286, 0.7, 0.6678571428571428, 0.6928571428571428, 0.6892857142857143, 0.6821428571428572, 0.6892857142857143, 0.7142857142857143, 0.6678571428571428, 0.6821428571428572, 0.6571428571428571, 0.6785714285714286, 0.7142857142857143, 0.7107142857142857, 0.6821428571428572, 0.7107142857142857, 0.675, 0.6892857142857143, 0.6785714285714286, 0.6892857142857143, 0.7035714285714286, 0.7071428571428572, 0.6892857142857143, 0.6964285714285714, 0.6714285714285714, 0.6892857142857143, 0.7, 0.725, 0.6785714285714286, 0.6964285714285714, 0.7214285714285714, 0.7, 0.6928571428571428, 0.7035714285714286, 0.7035714285714286, 0.6964285714285714, 0.6642857142857143, 0.675, 0.6392857142857142, 0.6892857142857143, 0.7035714285714286, 0.6714285714285714, 0.7321428571428571, 0.7, 0.7, 0.6964285714285714, 0.7035714285714286, 0.7107142857142857, 0.6857142857142857, 0.7071428571428572, 0.675, 0.6892857142857143, 0.6821428571428572, 0.6821428571428572, 0.6964285714285714, 0.6928571428571428, 0.6928571428571428, 0.6821428571428572, 0.6892857142857143, 0.65, 0.6928571428571428, 0.7071428571428572, 0.6821428571428572, 0.7142857142857143, 0.7035714285714286, 0.6785714285714286, 0.7, 0.7071428571428572, 0.7035714285714286, 0.7, 0.6964285714285714, 0.6821428571428572, 0.6892857142857143, 0.7035714285714286, 0.7107142857142857, 0.6857142857142857, 0.6928571428571428, 0.6714285714285714, 0.6928571428571428, 0.6857142857142857, 0.6928571428571428, 0.7071428571428572, 0.7107142857142857, 0.7071428571428572, 0.6785714285714286, 0.7142857142857143, 0.675, 0.6785714285714286, 0.7035714285714286, 0.6821428571428572, 0.6857142857142857, 0.6821428571428572, 0.7071428571428572, 0.6964285714285714, 0.6928571428571428, 0.7142857142857143, 0.6785714285714286, 0.6642857142857143, 0.6821428571428572, 0.6964285714285714, 0.6964285714285714, 0.7142857142857143, 0.7142857142857143, 0.7178571428571429, 0.6714285714285714, 0.7071428571428572, 0.6964285714285714, 0.7142857142857143, 0.6964285714285714, 0.7035714285714286, 0.7035714285714286, 0.7107142857142857, 0.6714285714285714, 0.7035714285714286, 0.6714285714285714, 0.6785714285714286, 0.7071428571428572, 0.6964285714285714, 0.6821428571428572, 0.6892857142857143, 0.675, 0.7071428571428572, 0.6821428571428572, 0.6678571428571428, 0.6642857142857143, 0.675, 0.6928571428571428, 0.6714285714285714, 0.7071428571428572, 0.6785714285714286, 0.6714285714285714, 0.675, 0.7035714285714286, 0.6714285714285714, 0.6785714285714286, 0.6821428571428572, 0.6928571428571428, 0.6892857142857143, 0.7142857142857143, 0.6571428571428571, 0.7107142857142857, 0.6785714285714286, 0.7035714285714286, 0.6571428571428571, 0.6892857142857143, 0.7, 0.6785714285714286, 0.6892857142857143, 0.7214285714285714, 0.725]

l2 = [0.7, 0.6857142857142857, 0.6857142857142857, 0.7107142857142857, 0.6821428571428572, 0.6928571428571428, 0.7, 0.6928571428571428, 0.6821428571428572, 0.6892857142857143, 0.6607142857142857, 0.6678571428571428, 0.6964285714285714, 0.7, 0.7, 0.6892857142857143, 0.6785714285714286, 0.6821428571428572, 0.6607142857142857, 0.65, 0.7071428571428572, 0.6678571428571428, 0.6964285714285714, 0.6857142857142857, 0.7035714285714286, 0.6607142857142857, 0.7, 0.6642857142857143, 0.6607142857142857, 0.6928571428571428, 0.6714285714285714, 0.6571428571428571, 0.6857142857142857, 0.7142857142857143, 0.7, 0.7214285714285714, 0.6928571428571428, 0.6928571428571428, 0.6857142857142857, 0.675, 0.6821428571428572, 0.6892857142857143, 0.6892857142857143, 0.6892857142857143, 0.7, 0.6892857142857143, 0.6892857142857143, 0.6714285714285714, 0.6857142857142857, 0.6821428571428572, 0.6964285714285714, 0.675, 0.6928571428571428, 0.675, 0.6714285714285714, 0.6642857142857143, 0.6892857142857143, 0.7071428571428572, 0.6357142857142857, 0.6714285714285714, 0.7178571428571429, 0.675, 0.6785714285714286, 0.6821428571428572, 0.6678571428571428, 0.7, 0.6964285714285714, 0.7071428571428572, 0.6821428571428572, 0.6607142857142857, 0.6892857142857143, 0.6642857142857143, 0.7321428571428571, 0.6571428571428571, 0.7071428571428572, 0.6821428571428572, 0.6857142857142857, 0.7321428571428571, 0.675, 0.6821428571428572, 0.6785714285714286, 0.6964285714285714, 0.6642857142857143, 0.675, 0.6642857142857143, 0.6678571428571428, 0.7035714285714286, 0.6857142857142857, 0.6785714285714286, 0.6678571428571428, 0.675, 0.6821428571428572, 0.6785714285714286, 0.6928571428571428, 0.6678571428571428, 0.6714285714285714, 0.6928571428571428, 0.6892857142857143, 0.6928571428571428, 0.6714285714285714, 0.6964285714285714, 0.6571428571428571, 0.6857142857142857, 0.6821428571428572, 0.6785714285714286, 0.6714285714285714, 0.6714285714285714, 0.6857142857142857, 0.6642857142857143, 0.6821428571428572, 0.7142857142857143, 0.6642857142857143, 0.6857142857142857, 0.7035714285714286, 0.6857142857142857, 0.6714285714285714, 0.6785714285714286, 0.6821428571428572, 0.6821428571428572, 0.675, 0.6857142857142857, 0.6571428571428571, 0.6964285714285714, 0.6714285714285714, 0.6857142857142857, 0.7, 0.6857142857142857, 0.6642857142857143, 0.6857142857142857, 0.6464285714285715, 0.7, 0.6928571428571428, 0.6964285714285714, 0.675, 0.6785714285714286, 0.6928571428571428, 0.6642857142857143, 0.6785714285714286, 0.6785714285714286, 0.6928571428571428, 0.6642857142857143, 0.6714285714285714, 0.6678571428571428, 0.6892857142857143, 0.6821428571428572, 0.6928571428571428, 0.6785714285714286, 0.6785714285714286, 0.6964285714285714, 0.6857142857142857, 0.6857142857142857, 0.6964285714285714, 0.6928571428571428, 0.6964285714285714, 0.7107142857142857]

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

def readfile(name):
    with open(f'nohup_{name}', 'r') as f:
        l = f.readlines()
        l = list(filter(lambda x: x.startswith('0.'), l))
        l = [float(x) for x in l]
    return l
l0 = readfile('init_grammar_circle')
l0 = list(filter(lambda x: x>0.5, l0))

l1 = readfile('init_grammar_mannual_design')
l2 = readfile('step_10')
l3 = readfile('step_30')
l4 = readfile('step_50')
l5 = readfile('step_100')


print(len(l0), len(l1), len(l2), len(l3), len(l4), len(l5))

import numpy as np
l0 = np.asarray(l0)
l1 = np.asarray(l1)
l2 = np.asarray(l2)
l3 = np.asarray(l3)
l4 = np.asarray(l4)
l5 = np.asarray(l5)

print(l0.mean(), l1.mean(), l2.mean(), l3.mean(), l4.mean(), l5.mean())
print(l0.std(), l1.std(), l2.std(), l3.std(), l4.std(), l5.std())
#seaborn.kdeplot(l1)
seaborn.boxplot(data=[l1, l2, l3, l4, l5])
plt.show()
exit(0)

print(np.std(l0), np.std(l1), np.std(l2), np.std(l3), np.std(l4), np.std(l5), np.std(l6), np.std(l7))
print(0.016 / np.sqrt(130))
print(len(l0), len(l1), len(l2), len(l3), len(l4), len(l5), len(l6), len(l7))
'''
df0 = pd.DataFrame(l0)
df1 = pd.DataFrame(l1)
#exit(0)
df0.plot.box()
df1.plot.box()
plt.grid(linestyle="--", alpha=0.3)
plt.show()
'''