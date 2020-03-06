# coding=utf8


ROOT_RULE = 'statement -> [mquery]'

GRAMMAR_DICTIONARY = {}
GRAMMAR_DICTIONARY["statement"] = ['(mquery ws)']
GRAMMAR_DICTIONARY["mquery"] = [
    '(ws select_clause ws from_clause ws where_clause ws groupby_clause ws having_clause ws orderby_clause ws limit)',
    '(ws select_clause ws from_clause ws where_clause ws groupby_clause ws having_clause ws orderby_clause)',
    '(ws select_clause ws from_clause ws where_clause ws groupby_clause ws having_clause)',
    '(ws select_clause ws from_clause ws where_clause ws groupby_clause ws orderby_clause ws limit)',
    '(ws select_clause ws from_clause ws where_clause ws groupby_clause ws orderby_clause)',
    '(ws select_clause ws from_clause ws where_clause ws groupby_clause)',
    '(ws select_clause ws from_clause ws where_clause ws orderby_clause ws limit)',
    '(ws select_clause ws from_clause ws where_clause ws orderby_clause)',
    '(ws select_clause ws from_clause ws where_clause)',
    '(ws select_clause ws from_clause ws groupby_clause ws having_clause ws orderby_clause ws limit)',
    '(ws select_clause ws from_clause ws groupby_clause ws having_clause ws orderby_clause)',
    '(ws select_clause ws from_clause ws groupby_clause ws having_clause)',
    '(ws select_clause ws from_clause ws groupby_clause ws orderby_clause ws limit)',
    '(ws select_clause ws from_clause ws groupby_clause ws orderby_clause)',
    '(ws select_clause ws from_clause ws groupby_clause)',
    '(ws select_clause ws from_clause ws orderby_clause ws limit)',
    '(ws select_clause ws from_clause ws orderby_clause)',
    '(ws select_clause ws from_clause)'
]

# SELECT
GRAMMAR_DICTIONARY["select_clause"] = ['(select_with_distinct ws select_results)']
GRAMMAR_DICTIONARY["select_with_distinct"] = ['(ws "select" ws "distinct")', '(ws "select")']
GRAMMAR_DICTIONARY["select_results"] = ['(ws select_result ws "," ws select_results)', '(ws select_result)']
GRAMMAR_DICTIONARY["select_result"] = [
    '(subject ws selectop ws subject)',
    #'(subject wsp "as" wsp column_alias)',
    'subject',
]

# FROM
GRAMMAR_DICTIONARY["from_clause"] = ['(ws "from" ws table_source ws join_clauses)',
                                     '(ws "from" ws source)']
GRAMMAR_DICTIONARY["join_clauses"] = ['(join_clause ws join_clauses)', 'join_clause']
GRAMMAR_DICTIONARY["join_clause"] = ['joinop ws table_source ws "on" ws join_condition_clause']
GRAMMAR_DICTIONARY["joinop"] = ['"join"', '"left outer join"']
GRAMMAR_DICTIONARY["join_condition_clause"] = ['(join_condition ws "and" ws join_condition_clause)', 'join_condition']
GRAMMAR_DICTIONARY["join_condition"] = ['ws col_ref ws "=" ws col_ref']
GRAMMAR_DICTIONARY["source"] = ['(ws single_source ws "," ws source)', '(ws single_source)']
GRAMMAR_DICTIONARY["single_source"] = ['table_source', 'source_subq']
GRAMMAR_DICTIONARY["source_subq"] = ['("(" ws mquery ws ")" wsp "as" wsp table_alias)', '("(" ws mquery ws ")" wsp table_alias)', '("(" ws mquery ws ")")']
GRAMMAR_DICTIONARY["table_source"] = ['(table_name ws "as" ws table_alias)', 'table_name']

# LIMIT
GRAMMAR_DICTIONARY["limit"] = ['("limit" ws non_literal_number)']

# ORDER
GRAMMAR_DICTIONARY["orderby_clause"] = ['ws "order" ws "by" ws order_clause']
GRAMMAR_DICTIONARY["order_clause"] = ['(ordering_term ws "," ws order_clause)', 'ordering_term']
GRAMMAR_DICTIONARY["ordering_term"] = ['(ws subject ws ordering)', '(ws subject)']
GRAMMAR_DICTIONARY["ordering"] = ['(ws "asc")', '(ws "desc")']

# WHERE
GRAMMAR_DICTIONARY["where_clause"] = ['(ws "where" wsp expr ws where_conj)', '(ws "where" wsp expr)']
GRAMMAR_DICTIONARY["where_conj"] = ['(ws "and" wsp expr ws where_conj)', '(ws "and" wsp expr)', 
                                    '(ws "or" wsp expr ws where_conj)', '(ws "or" wsp expr)']

# GROUP BY
GRAMMAR_DICTIONARY["groupby_clause"] = ['(ws "group" ws "by" ws group_clause)']
GRAMMAR_DICTIONARY["group_clause"] = ['(ws subject ws "," ws group_clause)', '(ws subject)']

# HAVING
GRAMMAR_DICTIONARY["having_clause"] = ['(ws "having" wsp expr ws having_conj)', '(ws "having" wsp expr)']
GRAMMAR_DICTIONARY["having_conj"] = ['(ws "and" wsp expr ws having_conj)', '(ws "and" wsp expr)', 
                                     '(ws "or" wsp expr ws having_conj)', '(ws "or" wsp expr)']

GRAMMAR_DICTIONARY["expr"] = [
    '(subject wsp "not" wsp "in" wsp "(" ws mquery ws ")")',
    '(subject wsp "in" ws "(" ws mquery ws ")")',
    '(subject ws binaryop ws "all" ws "(" ws mquery ws ")")',
    '(subject ws binaryop ws "any" ws "(" ws mquery ws ")")',
    '(subject ws binaryop ws "(" ws mquery ws ")")',
    '(subject ws binaryop ws value)',
]
GRAMMAR_DICTIONARY["value"] = ['non_literal_number', 'col_ref', 'string']
GRAMMAR_DICTIONARY["subject"] = ['function', 'col_ref']
GRAMMAR_DICTIONARY["col_ref"] = ['(table_alias ws "." ws column_name)', 'column_name']

GRAMMAR_DICTIONARY["function"] = ['(fname ws "(" ws "distinct" ws col_ref ws ")")',
                                  '(fname ws "(" ws col_ref ws ")")']
GRAMMAR_DICTIONARY["fname"] = ['"count"', '"sum"', '"max"', '"min"', '"avg"', '"all"']

# TODO(MARK): This is not tight enough. AND/OR are strictly boolean value operators.
GRAMMAR_DICTIONARY["binaryop"] = ['"="', '"!="', '"<>"', '">="', '"<="', '">"', '"<"', '"like"', '"not like"']
GRAMMAR_DICTIONARY['selectop'] = ['"/"', '"+"', '"-"']

GRAMMAR_DICTIONARY["ws"] = ['~"\s*"i']
GRAMMAR_DICTIONARY['wsp'] = ['~"\s+"i']
GRAMMAR_DICTIONARY["table_name"] = ['"aircraft"', '"airline"', '"airport"', '"airport_service"',
                                    '"city"', '"class_of_service"', '"code_description"',
                                    '"compartment_class"', '"date_day"', '"days"',
                                    '"dual_carrier"', '"equipment_sequence"', '"fare"',
                                    '"fare_basis"', '"flight"', '"flight_fare"', '"flight_leg"',
                                    '"flight_stop"', '"food_service"', '"ground_service"',
                                    '"month"', '"restriction"', '"state"', '"time_interval"',
                                    '"time_zone"']

GRAMMAR_DICTIONARY["table_alias"] = [
    '"aircraftalias0"', '"aircraftalias1"', '"aircraftalias2"', '"aircraftalias3"', '"airlinealias0"',
    '"airportalias0"', '"airportalias1"', '"airportalias2"', '"airportalias3"', '"cityalias0"',
    '"cityalias1"', '"cityalias2"', '"cityalias3"', '"cityalias4"', '"cityalias5"', '"daysalias0"',
    '"daysalias1"', '"daysalias2"', '"daysalias3"', '"daysalias4"', '"daysalias5"', '"daysalias6"',
    '"daysalias7"', '"daysalias8"', '"daysalias9"', '"farealias0"', '"farealias1"', '"farealias2"',
    '"farealias3"', '"farealias4"', '"flightalias0"', '"flightalias1"', '"flightalias2"',
    '"flightalias3"', '"restrictionalias0"', '"statealias0"', '"statealias1"', '"statealias2"',
    '"statealias3"'
]


GRAMMAR_DICTIONARY["column_name"] = [
    '"*"', '"meal_code"', '"range_miles"', '"departure_flight_number"', '"manufacturer"',
    '"aircraft_description"', '"stop_time"', '"stop_airport"', '"fare_airline"', '"no_discounts"',
    '"engines"', '"month_name"', '"restriction_code"', '"propulsion"', '"pressurized"',
    '"from_airport"', '"wide_body"', '"flight_days"', '"time_zone_name"', '"capacity"', '"fare_id"',
    '"class_type"', '"period"', '"minimum_connect_time"', '"stops"', '"service_name"', '"city_code"',
    '"begin_time"', '"meal_description"', '"end_time"', '"minutes_distant"', '"round_trip_required"',
    '"one_direction_cost"', '"day_number"', '"flight_id"', '"time_zone_code"', '"wing_span"',
    '"length"', '"stop_number"', '"pay_load"', '"airport_code"', '"miles_distant"',
    '"hours_from_gmt"', '"departure_airline"', '"to_airport"', '"rank"', '"city_name"',
    '"dual_airline"', '"saturday_stay_required"', '"economy"', '"weight"', '"premium"',
    '"booking_class"', '"day_name"', '"airport_location"', '"ground_fare"', '"days_code"',
    '"note"', '"transport_type"', '"basic_type"', '"compartment"', '"leg_flight"',
    '"arrival_airline"', '"maximum_stay"', '"month_number"', '"minimum_stay"', '"state_name"',
    '"flight_number"', '"year"', '"airline_flight"', '"country_name"', '"arrival_flight_number"',
    '"dual_carrier"', '"meal_number"', '"class_description"', '"departure_time"', '"airline_name"',
    '"airline_code"', '"application"', '"fare_basis_code"', '"stopovers"', '"high_flight_number"',
    '"airport_name"', '"low_flight_number"', '"discounted"', '"season"', '"advance_purchase"',
    '"arrival_time"', '"basis_days"', '"leg_number"', '"main_airline"', '"aircraft_code_sequence"',
    '"stop_days"', '"time_elapsed"', '"aircraft_code"', '"connections"', '"state_code"', '"night"',
    '"cruising_speed"', '"direction"', '"round_trip_cost"', '"description"', '"code"'
]
'''
GRAMMAR_DICTIONARY['column_alias'] = [
    '"derived_fieldalias0"', '"derived_fieldalias1"'  # custom
]
'''
GRAMMAR_DICTIONARY["non_literal_number"] = ['"100"', '"734"', '"757"', '"733"']
GRAMMAR_DICTIONARY["string"] = [
    '"72s"', '"73s"', '"aa"', '"ac"', '"air taxi operation"', '"aircraft_code0"', '"airline_code0"',
    '"airline_code1"', '"airline_code2"', '"airline_name0"', '"airport_code0"', '"airport_code1"',
    '"airport_name0"', '"ap"', '"ap/55"', '"ap/57"', '"ap/58"', '"ap/68"', '"ap/80"', '"arizona"',
    '"as"', '"atlanta"', '"b"', '"baltimore"', '"basic_type0"', '"bh"', '"bna"', '"boeing"',
    '"booking_class0"', '"bos"', '"boston"', '"breakfast"', '"bur"', '"burbank"', '"business"',
    '"bwi"', '"c"', '"california"', '"canadian airlines international"', '"canadian airlines"',
    '"charlotte"', '"chicago"', '"cincinnati"', '"city_name0"', '"city_name1"', '"city_name2"',
    '"city_name3"', '"class_type0"', '"class_type1"', '"cleveland"', '"co"', '"coach"', '"colorado"',
    '"columbus"', '"continental airlines"', '"country_name0"', '"cp"', '"cvg"', '"d/s"', '"d10"',
    '"d9s"', '"daily"', '"dal"', '"dallas fort worth"', '"dallas"', '"day_name0"', '"day_name1"',
    '"day_name2"', '"day_name3"', '"day_name4"', '"dc"', '"delta"', '"denver"', '"detroit"', '"dfw"',
    '"discounted0"', '"dl"', '"dtw"', '"ea"', '"economy0"', '"ewr"', '"f"', '"f28"',
    '"fare_basis_code0"', '"ff"', '"first"', '"florida"', '"fn"', '"fort worth"',
    '"general mitchell international"', '"georgia"', '"h"', '"hou"', '"houston"', '"hp"', '"iad"',
    '"iah"', '"indianapolis"', '"jfk"', '"kansas city"', '"kw"', '"las vegas"', '"lax"',
    '"lester pearson"', '"lga"', '"lh"', '"limousine"', '"long beach"', '"los angeles"', '"ls"',
    '"m"', '"m80"', '"manufacturer0"', '"mco"', '"meal_code0"', '"meal_code1"', '"meal_description0"',
    '"memphis"', '"mia"', '"miami"', '"milwaukee"', '"minneapolis"', '"minnesota"', '"mke"', '"ml"',
    '"montreal"', '"nashville"', '"new jersey"', '"new york"', '"newark"', '"no"', '"north carolina"',
    '"nw"', '"nx"', '"oak"', '"oakland"', '"ohio"', '"ontario"', '"ord"', '"orlando"', '"philadelphia"',
    '"phl"', '"phoenix"', '"pit"', '"pittsburgh"', '"propulsion0"', '"q"', '"qo"', '"quebec"', '"qw"',
    '"qx"', '"rapid transit"', '"rental car"', '"round_trip_required0"', '"s"', '"s/"', '"sa"',
    '"salt lake city"', '"san diego"', '"san francisco"', '"san jose"', '"sd/d"', '"seattle"', '"sfo"',
    '"snack"', '"st. louis"', '"st. paul"', '"st. petersburg"', '"state_code0"', '"state_name0"',
    '"state_name1"', '"sunday"', '"tacoma"', '"tampa"', '"taxi"', '"tennessee"', '"thrift"',
    '"thursday"', '"toronto"', '"tpa"', '"transport_type0"', '"transport_type1"', '"turboprop"',
    '"tw"', '"tx"', '"ua"', '"us"', '"usair"', '"utah"', '"washington"', '"westchester county"', '"wn"',
    '"y"', '"yes"', '"yn"', '"yx"', '"yyz"'
]
