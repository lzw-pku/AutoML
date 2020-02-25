# coding=utf-8
"""
Prolog Grammar
"""
import copy
from typing import List, Dict
from pprint import pprint
from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar as _Grammar

# First-order logical form

ROOT_RULE = 'statement -> [answer]'

GRAMMAR_DICTIONARY = {}
GRAMMAR_DICTIONARY['statement'] = ['(answer ws)']
GRAMMAR_DICTIONARY['answer'] = ['("_answer" ws "(" ws var ws "," ws goal ws ")" )']
# Goal
GRAMMAR_DICTIONARY['conjunction'] = [
    '("," ws predicate ws conjunction)',
    '""'
]
GRAMMAR_DICTIONARY['goal'] = ['unit_relation', 'meta', '("(" ws predicate ws conjunction ws ")")']
GRAMMAR_DICTIONARY['predicate'] = ['meta', 'unit_relation', 'binary_relation', 'declaration', '("\+" ws declaration)', '("\+" ws "(" ws predicate ws conjunction ws ")")']

# Meta Predicates
GRAMMAR_DICTIONARY['meta'] = [
    'largest', 'smallest', 'highest', 'lowest', 'longest', 'shortest', 'count', 'most', 'fewest', 'sum'
]
GRAMMAR_DICTIONARY['largest'] = ['("_largest" ws "(" ws var ws "," ws goal ws ")")']
GRAMMAR_DICTIONARY['smallest'] = ['("_smallest" ws "(" ws var ws "," ws goal ws ")")']
GRAMMAR_DICTIONARY['highest'] = ['("_highest" ws "(" ws var ws "," ws goal ws ")")']
GRAMMAR_DICTIONARY['lowest'] = ['("_lowest" ws "(" ws var ws "," ws goal ws ")")']
GRAMMAR_DICTIONARY['longest'] = ['("_longest" ws "(" ws var ws "," ws goal ws ")")']
GRAMMAR_DICTIONARY['shortest'] = ['("_shortest" ws "(" ws var ws "," ws goal ws ")")']
GRAMMAR_DICTIONARY['count'] = ['("_count" ws "(" ws var ws "," ws goal ws "," ws var ws ")")']
GRAMMAR_DICTIONARY['most'] = ['("_most" ws "(" ws var ws "," ws var ws "," ws goal ws")")']
GRAMMAR_DICTIONARY['fewest'] = ['("_fewest" ws "(" ws var ws "," ws var ws "," ws goal ws")")']
GRAMMAR_DICTIONARY['sum'] = ['("_sum" ws "(" ws var ws "," ws goal ws "," ws retrieve ws "," ws var ws ")")']

# Declaration
GRAMMAR_DICTIONARY['declaration'] = ['("_const" ws "(" ws var ws "," ws object ws ")")']

# Object
GRAMMAR_DICTIONARY['object'] = ['country', 'city', 'state', 'river', 'place']
GRAMMAR_DICTIONARY['country'] = ['("_countryid" ws "(" ws country_name ws ")")']
GRAMMAR_DICTIONARY['city'] = ['("_cityid" ws "(" ws city_name ws "," ws state_abbre ws ")")']
GRAMMAR_DICTIONARY['state'] = ['("_stateid" ws "(" ws state_name ws ")")']
GRAMMAR_DICTIONARY['river'] = ['("_riverid" ws "(" ws river_name ws ")")']
GRAMMAR_DICTIONARY['place'] = ['("_placeid" ws "(" ws place_name ws ")")']

# Retrieve
GRAMMAR_DICTIONARY['retrieve'] = [
    'area', 'len', 'population'
]
GRAMMAR_DICTIONARY['area'] = ['("_area" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['len'] = ['("_len" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['population'] = ['("_population" ws "(" ws var ws ")")']

# Relation
GRAMMAR_DICTIONARY['unit_relation'] = [
    'is_capital', 
    'is_city', 
    'is_major', 
    'is_place', 
    'is_river',
    'is_state',
    'is_lake',
    'is_mountain',
]
GRAMMAR_DICTIONARY['is_capital'] = ['("_capital" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_city'] = ['("_city" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_major'] = ['("_major" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_place'] = ['("_place" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_river'] = ['("_river" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_lake'] = ['("_lake" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_state'] = ['("_state" ws "(" ws var ws ")")']
GRAMMAR_DICTIONARY['is_mountain'] = ['("_mountain" ws "(" ws var ws ")")']


GRAMMAR_DICTIONARY['binary_relation'] = [
    'is_area',
    'is_captial_of',
    'is_equal',
    'is_density',
    'is_elevation',
    'is_high_point',
    'is_low_point',
    'is_higher',
    'is_lower',
    'is_longer',
    'is_located_in',
    'is_len',
    'is_next_to',
    'is_size',
    'is_traverse',
    'is_population'
]
GRAMMAR_DICTIONARY['is_area'] = ['"_area" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_captial_of'] = ['"_capital" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_equal'] = ['"_equal" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_density'] = ['"_density" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_elevation'] = ['("_elevation" ws "(" ws var ws "," ws var ws ")")', '("_elevation" ws "(" ws var ws "," ws literal ws ")")']
GRAMMAR_DICTIONARY['is_high_point'] = ['"_high_point" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_low_point'] = ['"_low_point" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_higher'] = ['"_higher" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_lower'] = ['"_lower" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_longer'] = ['"_longer" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_located_in'] = ['"_loc" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_len'] = ['"_len" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_next_to'] = ['"_next_to" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_size'] = ['"_size" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_traverse'] = ['"_traverse" ws "(" ws var ws "," ws var ws ")"']
GRAMMAR_DICTIONARY['is_population'] = ['"_population" ws "(" ws var ws "," ws var ws ")"']

# Terminal
# GRAMMAR_DICTIONARY['var'] = ['"a"', '"b"', '"c"', '"d"', '"e"', '"f"', '"g"'] # Original Variable
GRAMMAR_DICTIONARY['var'] = ['"nv"', '"v0"', '"v1"', '"v2"', '"v3"', '"v4"', '"v5"', '"v6"', '"v7"'] # Normalized Variable
GRAMMAR_DICTIONARY['literal'] = ['"0.0"', '"1.0"']
GRAMMAR_DICTIONARY['country_name'] = ['"usa"', '"us"']
GRAMMAR_DICTIONARY['city_name'] = ['"albany"', '"tempe"', '"chicago"', '"montgomery"', '"columbus"', '"kalamazoo"', '"neworleans"', '"riverside"', '"fortwayne"', '"scottsvalley"', '"boston"', '"flint"', '"dallas"', '"atlanta"', '"sanjose"', '"denver"', '"plano"', '"boulder"', '"minneapolis"', '"seattle"', '"batonrouge"', '"sacramento"', '"washington"', '"desmoines"', '"rochester"', '"springfield"', '"indianapolis"', '"dover"', '"detroit"', '"tucson"', '"houston"', '"portland"', '"salem"', '"durham"', '"miami"', '"sandiego"', '"salt_lake_city"', '"spokane"', '"austin"', '"pittsburgh"', '"erie"', '"newyork"', '"sanfrancisco"', '"sanantonio"']
GRAMMAR_DICTIONARY['state_abbre'] = ['"_"', '"dc"', '"sd"', '"az"', '"mo"', '"wa"', '"tx"', '"mn"', '"me"', '"ma"', '"pa"']
GRAMMAR_DICTIONARY['state_name'] = ['"newhampshire"', '"utah"', '"delaware"', '"tennessee"', '"newmexico"', '"oregon"', '"arizona"', '"iowa"', '"southdakota"', '"georgia"', '"arkansas"', '"pennsylvania"', '"oklahoma"', '"illinois"', '"kentucky"', '"wisconsin"', '"newjersey"', '"hawaii"', '"minnesota"', '"nebraska"', '"maryland"', '"massachusetts"', '"mississippi"', '"nevada"', '"southcarolina"', '"kansas"', '"idaho"', '"michigan"', '"alabama"', '"louisiana"', '"virginia"', '"washington"', '"california"', '"alaska"', '"texas"', '"colorado"', '"missouri"', '"vermont"', '"montana"', '"florida"', '"wyoming"', '"ohio"', '"westvirginia"', '"indiana"', '"northcarolina"', '"rhodeisland"', '"maine"', '"newyork"', '"northdakota"']
GRAMMAR_DICTIONARY['river_name'] = ['"ohio"', '"riogrande"', '"delaware"', '"northplatte"', '"chattahoochee"', '"mississippi"', '"colorado"', '"missouri"', '"red"', '"potomac"']
GRAMMAR_DICTIONARY['place_name'] = ['"deathvalley"', '"mountwhitney"', '"mountmckinley"', '"guadalupepeak"']
GRAMMAR_DICTIONARY["ws"] = ['~"\s*"i']