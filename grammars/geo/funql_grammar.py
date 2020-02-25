# coding=utf-8
"""
FunQL Grammar
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
GRAMMAR_DICTIONARY['answer'] = ['("answer" ws "(" ws predicate ws ")" )']

GRAMMAR_DICTIONARY['predicate'] = [
    'meta', 'object', 'collection', 'relation', '("intersection" ws "(" ws predicate ws "," ws predicate ws ")")', 
    '("exclude" ws "(" ws predicate ws "," ws predicate ws ")")', 
]

# Meta Predicates
GRAMMAR_DICTIONARY['meta'] = [
    'largest', 'smallest', 'highest', 'lowest', 'longest', 'shortest', 'count', 'most', 'fewest',
    'largest_one_area', 'largest_one_density', 'largest_one_population', 
    'smallest_one_area', 'smallest_one_density', 'smallest_one_population', 'sum'
]
GRAMMAR_DICTIONARY['largest'] = ['("largest" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['smallest'] = ['("smallest" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['highest'] = ['("highest" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['lowest'] = ['("lowest" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['longest'] = ['("longest" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['shortest'] = ['("shortest" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['count'] = ['("count" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['most'] = ['("most" ws "(" ws predicate ws")")']
GRAMMAR_DICTIONARY['fewest'] = ['("fewest" ws "(" ws predicate ws")")']
GRAMMAR_DICTIONARY['largest_one_area'] = ['("largest_one" ws "(" ws "area_1" ws "(" ws predicate ws ")" ws")")']
GRAMMAR_DICTIONARY['largest_one_density'] = ['("largest_one" ws "(" ws "density_1" ws "(" ws predicate ws ")" ws")")']
GRAMMAR_DICTIONARY['largest_one_population'] = ['("largest_one" ws "(" ws "population_1" ws "(" ws predicate ws ")" ws")")']
GRAMMAR_DICTIONARY['smallest_one_area'] = ['("smallest_one" ws "(" ws "area_1" ws "(" ws predicate ws ")" ws")")']
GRAMMAR_DICTIONARY['smallest_one_density'] = ['("smallest_one" ws "(" ws "density_1" ws "(" ws predicate ws ")" ws")")']
GRAMMAR_DICTIONARY['smallest_one_population'] = ['("smallest_one" ws "(" ws "population_1" ws "(" ws predicate ws ")" ws")")']
GRAMMAR_DICTIONARY['sum'] = ['("sum" ws "(" ws predicate ws")")']

# Object
GRAMMAR_DICTIONARY['object'] = ['country', 'city', 'state', 'river', 'place']
GRAMMAR_DICTIONARY['country'] = ['("countryid" ws "(" ws country_name ws ")")']
GRAMMAR_DICTIONARY['city'] = ['("cityid" ws "(" ws city_name ws "," ws state_abbre ws ")")']
GRAMMAR_DICTIONARY['state'] = ['("stateid" ws "(" ws state_name ws ")")']
GRAMMAR_DICTIONARY['river'] = ['("riverid" ws "(" ws river_name ws ")")']
GRAMMAR_DICTIONARY['place'] = ['("placeid" ws "(" ws place_name ws ")")']

# Collection
GRAMMAR_DICTIONARY['collection'] = ['all_capital_cities', 'all_cities', 'all_lakes', 'all_mountains', 'all_places', 'all_rivers', 'all_states']
GRAMMAR_DICTIONARY['all_capital_cities'] = ['("capital" ws "(" ws "all" ws ")")',]
GRAMMAR_DICTIONARY['all_cities'] = ['("city" ws "(" ws "all" ws ")")',]
GRAMMAR_DICTIONARY['all_lakes'] = ['("late" ws "(" ws "all" ws ")")',]
GRAMMAR_DICTIONARY['all_mountains'] = ['("mountain" ws "(" ws "all" ws ")")',]
GRAMMAR_DICTIONARY['all_places'] = ['("place" ws "(" ws "all" ws ")")',]
GRAMMAR_DICTIONARY['all_rivers'] = ['("river" ws "(" ws "all" ws ")")',]
GRAMMAR_DICTIONARY['all_states'] = ['("state" ws "(" ws "all" ws ")")',]

# Relations
GRAMMAR_DICTIONARY['relation'] = [
    'is_captial', 'is_city', 'is_lake', 'is_major', 'is_mountain', 'is_place',
    'is_river', 'is_state', 'is_area_state', 'is_captial_country', 'is_captial_city',
    'is_density_place', 'is_elevation_place', 'is_elevation_value', 'is_high_point_state', 'is_high_point_place',
    'is_higher_place_2', 'is_loc_x', 'is_loc_y', 'is_longer', 'is_lower_place_2', 'is_len', 'is_next_to_state_1', 'is_next_to_state_2',
    'is_population', 'is_size', 'is_traverse_river', 'is_traverse_state', 'is_low_point_state', 'is_low_point_place',
]
GRAMMAR_DICTIONARY['is_captial'] = ['("capital" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_city'] = ['("city" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_lake'] = ['("lake" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_major'] = ['("major" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_mountain'] = ['("mountain" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_place'] = ['("place" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_river'] = ['("river" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_state'] = ['("state" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_area_state'] = ['("area_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_captial_country'] = ['("capital_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_captial_city'] = ['("capital_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_density_place'] = ['("density_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_elevation_place'] = ['("elevation_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_elevation_value'] = ['("elevation_2" ws "(" ws number ws ")")']
GRAMMAR_DICTIONARY['is_high_point_state'] = ['("high_point_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_high_point_place'] = ['("high_point_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_low_point_state'] = ['("low_point_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_low_point_place'] = ['("low_point_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_higher_place_2'] = ['("higher_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_loc_x'] = ['("loc_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_loc_y'] = ['("loc_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_longer'] = ['("longer" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_lower_place_2'] = ['("lower_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_len'] = ['("len" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_next_to_state_1'] = ['("next_to_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_next_to_state_2'] = ['("next_to_2" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_population'] = ['("population_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_size'] = ['("size" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_traverse_river'] = ['("traverse_1" ws "(" ws predicate ws ")")']
GRAMMAR_DICTIONARY['is_traverse_state'] = ['("traverse_2" ws "(" ws predicate ws ")")']

# Terminal
GRAMMAR_DICTIONARY['number'] = ['"0.0"', '"1.0"', '"0"']
GRAMMAR_DICTIONARY['country_name'] = ['"usa"', '"us"']
GRAMMAR_DICTIONARY['city_name'] = ['"plano"', '"sacramento"', '"fortwayne"', '"neworleans"', '"houston"', '"scottsvalley"', '"desmoines"', '"riverside"', '"newyork"', '"chicago"', '"sanantonio"', '"austin"', '"sandiego"', '"rochester"', '"durham"', '"dover"', '"seattle"', '"boston"', '"flint"', '"washington"', '"portland"', '"pittsburgh"', '"tempe"', '"boulder"', '"kalamazoo"', '"springfield"', '"erie"', '"indianapolis"', '"albany"', '"spokane"', '"minneapolis"', '"sanfrancisco"', '"miami"', '"detroit"', '"saltlakecity"', '"montgomery"', '"denver"', '"columbus"', '"sanjose"', '"tucson"', '"atlanta"', '"salem"', '"batonrouge"', '"dallas"']
GRAMMAR_DICTIONARY['state_abbre'] = ['"ma"', '"mo"', '"_"', '"ga"', '"dc"', '"mn"', '"az"', '"sd"', '"tx"', '"pa"', '"me"', '"wa"']
GRAMMAR_DICTIONARY['state_name'] = ['"montana"', '"newhampshire"', '"northcarolina"', '"westvirginia"', '"nebraska"', '"newjersey"', '"oregon"', '"newyork"', '"pennsylvania"', '"wisconsin"', '"texas"', '"kansas"', '"ohio"', '"utah"', '"colorado"', '"vermont"', '"arkansas"', '"california"', '"nevada"', '"alabama"', '"maryland"', '"louisiana"', '"northdakota"', '"michigan"', '"washington"', '"massachusetts"', '"wyoming"', '"kentucky"', '"mississippi"', '"georgia"', '"alaska"', '"iowa"', '"southcarolina"', '"virginia"', '"idaho"', '"missouri"', '"indiana"', '"newmexico"', '"rhodeisland"', '"minnesota"', '"delaware"', '"arizona"', '"hawaii"', '"florida"', '"illinois"', '"oklahoma"', '"maine"', '"southdakota"', '"tennessee"']
GRAMMAR_DICTIONARY['river_name'] = ['"riogrande"', '"ohio"', '"potomac"', '"colorado"', '"delaware"', '"mississippi"', '"northplatte"', '"red"', '"chattahoochee"', '"missouri"']
GRAMMAR_DICTIONARY['place_name'] = ['"guadalupepeak"', '"mountwhitney"', '"deathvalley"', '"mountmckinley"']
GRAMMAR_DICTIONARY["ws"] = ['~"\s*"i']