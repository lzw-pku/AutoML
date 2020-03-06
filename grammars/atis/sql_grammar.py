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
    '(subject wsp "as" wsp column_alias)',
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
GRAMMAR_DICTIONARY["table_name"] = ['"state"', '"city"', '"lake"', '"river"', '"border_info"', '"highlow"', '"mountain"']
GRAMMAR_DICTIONARY["table_alias"] = [
    '"statealias0"', '"statealias1"', '"statealias2"', '"statealias3"', '"statealias4"', '"statealias5"',
    '"cityalias0"', '"cityalias1"', '"cityalias2"',
    '"lakealias0"', '"mountainalias0"', '"mountainalias1"',
    '"riveralias0"', '"riveralias1"', '"riveralias2"', '"riveralias3"',
    '"border_infoalias0"', '"border_infoalias1"', '"border_infoalias2"', '"border_infoalias3"', 
    '"highlowalias0"', '"highlowalias1"', '"derived_tablealias0"', '"derived_tablealias1"',
    '"tmp"',
]
GRAMMAR_DICTIONARY["column_name"] = [
    '"*"', '"city_name"', '"population"', '"country_name"', '"state_name"', # city
    '"border"', # border_info
    '"highest_elevation"', '"lowest_point"', '"highest_point"', '"lowest_elevation"', # highlow
    '"lake_name"', '"area"', '"country_name"', # lake
    '"mountain_name"', '"mountain_altitude"', # mountain
    '"river_name"', '"length"', '"traverse"', # river
    '"capital"', '"density"', # state,
    '"derived_fieldalias0"', '"derived_fieldalias1"'
]
GRAMMAR_DICTIONARY['column_alias'] = [
    '"derived_fieldalias0"', '"derived_fieldalias1"'  # custom
]

GRAMMAR_DICTIONARY["non_literal_number"] = ['"150000"', '"750"', '"0"', '"1"', '"2"', '"3"', '"4"',]
GRAMMAR_DICTIONARY["string"] = [
    '"\'dc\'"',
    '"104577"', '"\'big stone lake\'"', '"\'borah peak\'"', '"\'1746\'"', '"56153"', '"\'87\'"', '"\'evanston\'"', '"\'brockton\'"', '"95322"', '"\'north charleston\'"', '"1595138"', '"\'725\'"', '"\'huntington\'"', '"158000"', '"\'royal oak\'"', '"101229"', '"\'greenville\'"', 
    '"107969"', '"\'207\'"', '"57906"', '"\'red river\'"', '"\'smoky hill\'"', '"0.6798646362098139"', '"\'newport news\'"', '"77372"', '"190037"', '"130414"', '"\'upper darby\'"', '"\'mcallen\'"', '"\'rhode island\'"', '"\'143\'"', 
    '"\'lawrence\'"', '"\'waltham\'"', '"\'lower merion\'"', '"4591000"', '"82300"', '"70700"', '"\'sterling heights\'"', '"116860"', '"\'reno\'"', '"4490"', '"108.94636924537257"', 
    '"49100"', '"\'superior\'"', '"\'danbury\'"', '"\'cranston\'"', '"\'waterbury\'"', '"346865"', '"87123"', '"\'detroit\'"', '"\'st. clair shores\'"', '"678974"', '"84901"', '"67653"', '"\'birmingham\'"', '"74111"', '"128394"', '"\'1069\'"', '"\'durham\'"', '"\'tacoma\'"', 
    '"638000"', '"\'new orleans\'"', '"83622"', '"800500"', '"4217000"', '"10460"', '"945.8071144214715"', '"\'parma\'"', '"\'largo\'"', '"56725"', '"5304"', '"403213"', '"\'simi valley\'"', '"4996"', '"101727"', '"96988"', '"1105"', '"\'mountain view\'"', '"\'maine\'"', '"1100"', 
    '"\'dearborn heights\'"', '"\'tulsa\'"', '"\'washita\'"', '"\'17\'"', '"\'3859\'"', '"100.3374795101726"', '"8.957505576015354"', '"\'erie\'"', '"\'mesquite\'"', '"152319"', '"64407"', '"\'el diente\'"', '"354635"', '"59084"', '"100427"', '"4327"', '"163034"', '"\'green bay\'"', 
    '"453085"', '"1049"', '"\'bismarck\'"', '"\'white butte\'"', '"24200"', '"3894000"', '"\'franklin township\'"', '"118690"', '"\'middletown\'"', '"523"', '"71293"', '"\'naknek\'"', '"\'salton sea\'"', '"\'longs\'"', '"\'kansas\'"', '"4520"', '"682"', '"82602"', '"\'berkeley\'"', 
    '"77500"', '"70525"', '"786700"', '"149771"', '"84400"', '"\'camden\'"', '"\'alexandria\'"', '"\'evansville\'"', '"60470"', '"131885"', '"106963"', '"\'saginaw\'"', '"\'lawton\'"', '"\'wateree catawba\'"', '"690767"', '"123351"', '"\'mesa\'"', '"61963"', '"\'wabash\'"', '"655"',
    '"63852"', '"158501"', '"57597"', '"\'kootenai river\'"', '"2889000"', '"4964"', '"\'somerville\'"', '"\'flint\'"', '"71384"', '"142513"', '"\'elgin\'"', '"638333"', '"\'garden grove\'"', '"\'wilmington\'"', '"\'oregon\'"', '"\'bear\'"', '"4345"', '"\'fall river\'"', '"762874"',
    '"33.81932962573275"', '"\'black mesa\'"', '"3005172"', '"7071639"', '"173979"', '"\'wheeler peak\'"', '"\'irvington\'"', '"\'st. louis\'"', '"271523"', '"\'shavano\'"', '"\'cheyenne\'"', '"97073"', '"58076"', '"78686"', '"92811"', '"9.231966053748232"', '"\'newark\'"', '"805"',
    '"\'bianca\'"', '"\'hayward\'"', '"72496"', '"\'irvine\'"', '"84625"', '"70893"', '"573822"', '"540920"', '"60278"', '"84603"', '"455651"', '"\'waterloo\'"', '"448159"', '"4418"', '"36200"', '"62504"', '"106618"', '"\'massive\'"', '"74542"', '"\'st. paul\'"', '"\'long beach\'"',
    '"63175"', '"\'jacksonville\'"', '"947200"', '"170876"', '"80292"', '"\'bristol township\'"', '"106919"', '"781.5181518151816"', '"63968"', '"4317"', '"64695"', '"\'kentucky\'"', '"\'new haven\'"', '"\'256\'"', '"93585"', '"\'overland park\'"', '"679"', '"\'red bluff reservoir\'"',
    '"1569000"', '"\'kenner\'"', '"131945"', '"\'west covina\'"', '"158588"', '"\'cambridge\'"', '"646356"', '"58016"', '"\'east buttress\'"', '"\'lake champlain\'"', '"\'ewa\'"', '"\'dundalk\'"', '"64632"', '"70794"', '"66713"', '"115436"', '"5.351700680272108"', '"\'scranton\'"',
    '"\'fullerton\'"', '"237177"', '"\'tempe\'"', '"\'1516\'"', '"71462"', '"\'pecos\'"', '"\'oklahoma\'"', '"11863000"', '"\'lubbock\'"', '"58056"', '"\'610\'"', '"\'belle fourche river\'"', '"\'vancouver\'"', '"\'pasadena\'"', '"28.72417982989064"', '"658"', '"\'hunter\'"', '"88820"',
    '"\'san bernardino\'"', '"\'1064\'"', '"\'waukegan\'"', '"\'casper\'"', '"77767"', '"\'santa fe\'"', '"\'omaha\'"', '"149.81012658227846"', '"\'paterson\'"', '"\'citrus heights\'"', '"\'sioux city\'"', '"110017"', '"6037"', '"87899"', '"\'132\'"', '"\'clifton\'"', '"4663"', '"\'akron\'"',
    '"\'1021\'"', '"191003"', '"\'black mountain\'"', '"\'glendale\'"', '"788"', '"\'livonia\'"', '"\'mount hood\'"', '"63952"', '"\'rock\'"', '"4442"', '"100756"', '"59651"', '"118072"', '"\'macon\'"', '"\'miami beach\'"', '"\'charlotte\'"', '"848"', '"202895"', '"112560"', '"\'joliet\'"',
    '"\'great falls\'"', '"58500"', '"\'oakland\'"', '"\'schenectady\'"', '"357.5967413441955"', '"4396"', '"102246"', '"\'santa rosa\'"', '"\'3901\'"', '"\'granite peak\'"', '"\'san francisco\'"', '"\'ann arbor\'"', '"\'cleveland\'"', '"238647"', '"\'washington\'"', '"\'nashville\'"', '"\'kit carson\'"',
    '"103758"', '"\'maryland\'"', '"7365000"', '"204165"', '"\'bayonne\'"', '"\'sunnyvale\'"', '"\'colorado\'"', '"\'amarillo\'"', '"\'district of columbia\'"', '"164674"', '"\'hudson\'"', '"\'pontchartrain\'"', '"\'cherry hill\'"', '"\'lynn\'"', '"\'taylor\'"', '"159611"', '"\'norwalk\'"', '"\'la plata\'"',
    '"\'mount sunflower\'"', '"88.17610062893081"', '"4341"', '"\'anaheim\'"', '"66382"', '"\'376\'"', '"\'859\'"', '"\'santa monica\'"', '"2286000"', '"56300"', '"4949"', '"\'philadelphia\'"', '"70193"', '"4349"', '"89233"', '"77640"', '"114000"', '"58900"', '"\'odessa\'"', '"172196"', '"\'sanford\'"',
    '"98315"', '"\'alabama\'"', '"81221"', '"\'okeechobee\'"', '"\'21\'"', '"493846"', '"69950"', '"\'austin\'"', '"73758"', '"48.29383886255924"', '"580.0"', '"31113"', '"\'irondequoit\'"', '"4439"', '"\'elyria\'"', '"\'fresno\'"', '"4785"', '"\'buffalo\'"', '"69700"', '"23.842105263157894"', '"164160"', '"\'6194\'"',
    '"\'jackson\'"', '"94162"', '"4842"', '"\'blackburn\'"', '"\'177\'"', '"63022"', '"\'montana\'"', '"\'scotts valley\'"', '"113808"', '"\'wrangell\'"', '"\'canton\'"', '"785880"', '"11.373493975903616"', '"62480"', '"\'garland\'"', '"2364000"', '"104814"', '"81784"', '"169728"', '"\'1231\'"', '"3025000"', '"684"', '"497"',
    '"\'ogden\'"', '"137970"', '"63475"', '"\'canadian\'"', '"\'evans\'"', '"51.74067495559503"', '"\'madison\'"', '"76715"', '"\'new rochelle\'"', '"\'bighorn\'"', '"\'redford\'"', '"\'little river\'"', '"\'tucson\'"', '"\'tenleytown\'"', '"\'174\'"', '"61232"', '"1638"', '"\'4418\'"', '"4382"', '"\'indianapolis\'"', '"\'portland\'"',
    '"59578"', '"\'fairfield\'"', '"\'alameda\'"', '"81371"', '"275741"', '"314447"', '"\'frankfort\'"', '"\'skokie\'"', '"102249"', '"75143"', '"\'st. petersburg\'"', '"80479"', '"\'clark fork\'"', '"72299"', '"\'472\'"', '"\'284\'"', '"170505"', '"\'1085\'"', '"\'idaho\'"', '"\'east orange\'"', '"4076000"', '"61493"', '"\'greenwich\'"',
    '"\'lynchburg\'"', '"\'virginia beach\'"', '"\'pearl\'"', '"2675"', '"\'dearborn\'"', '"\'oklahoma city\'"', '"158915"', '"\'jerimoth hill\'"', '"\'san jose\'"', '"\'lincoln\'"', '"85725"', '"110243"', '"\'south platte\'"', '"\'annapolis\'"', '"\'wisconsin\'"', '"\'tombigbee\'"', '"1953"', '"148.97233812393756"', '"\'bristol\'"', '"131.1776251226693"',
    '"\'cincinnati\'"', '"170105"', '"\'cedar rapids\'"', '"\'plano\'"', '"61572"', '"\'castle\'"', '"63982"', '"\'new york\'"', '"177857"', '"\'1339\'"', '"\'longview\'"', '"\'atlanta\'"', '"70419"', '"\'massachusetts\'"', '"\'lowell\'"', '"636212"', '"\'long island sound\'"', '"71992"', '"\'antero\'"', '"61186"', '"215150"', '"\'verdigris river\'"', '"\'4123\'"',
    '"80584"', '"92548"', '"82003"', '"27.778846153846153"', '"492365"', '"\'youngstown\'"', '"57619"', '"84910"', '"147000"', '"81230"', '"329248"', '"965"', '"203371"', '"\'163\'"', '"\'high point\'"', '"5882000"', '"4391"', '"77685"', '"205820"', '"\'pontiac\'"', '"174431"', '"67053"', '"\'1458\'"', '"121600"', '"\'waco\'"', '"\'trenton\'"', '"45308"', '"142546"',
    '"1203339"', '"\'55\'"', '"\'maroon\'"', '"62061"', '"\'wilson\'"', '"105611"', '"96298"', '"92145"', '"\'snake\'"', '"\'mille lacs\'"', '"\'north little rock\'"', '"\'allentown\'"', '"67865"', '"\'mount frissell\'"', '"83000"', '"510"', '"63684"', '"\'216\'"', '"43.24517512508935"', '"58977"', '"47700"', '"57504"', '"\'ocheyedan mound\'"', '"\'kings peak\'"',
    '"\'mobile\'"', '"68785"', '"\'-85\'"', '"\'mount marcy\'"', '"\'2025\'"', '"\'gulf of mexico\'"', '"\'harrisburg\'"', '"5180"', '"\'new britain\'"', '"\'utah\'"', '"53.203661327231124"', '"1142"', '"\'georgia\'"', '"\'becharof\'"', '"\'juneau\'"', '"\'muncie\'"', '"4.8007545317915525"', '"\'south bend\'"', '"\'monroe\'"', '"\'salt lake city\'"', '"70508"',
    '"70.53084648493544"', '"68558"', '"\'arlington heights\'"', '"\'des moines\'"', '"\'kansas city\'"', '"\'pensacola\'"', '"42140"', '"1632"', '"\'ouachita\'"', '"\'teshekpuk\'"', '"93077"', '"\'chattahoochee\'"', '"\'orange\'"', '"\'denver\'"', '"110500"', '"\'1654\'"', '"4392"', '"\'st. joseph\'"', '"103266"', '"\'richardson\'"', '"80054"', '"\'rainy\'"',
    '"156804"', '"\'mount rainier\'"', '"\'shasta\'"', '"\'fort worth\'"', '"\'portsmouth\'"', '"103763"', '"\'downey\'"', '"\'fort collins\'"', '"\'lake charles\'"', '"\'raleigh\'"', '"\'fargo\'"', '"\'salem\'"', '"218202"', '"786775"', '"\'west palm beach\'"', '"138857"', '"\'boundary peak\'"', '"\'racine\'"', '"17558000"', '"\'mount vernon\'"', '"3033"', '"109373"',
    '"\'montpelier\'"', '"68020"', '"\'125\'"', '"\'santa clara\'"', '"\'wyoming\'"', '"692.5398358281025"', '"298451"', 
    '"75632"', '"\'oak lawn\'"', '"\'alaska\'"', '"\'syracuse\'"', '"\'harney peak\'"', '"61308"', '"\'rio grande\'"', '"\'niobrara\'"', '"\'1263\'"', '"\'sacramento\'"', '"\'yonkers\'"', '"67102"', '"63189"', '"68664"', '"\'charleston\'"', '"\'pennsylvania\'"', '"202.4866785079929"', '"331767"', '"1175"', '"1810"', '"27.12391705211542"', '"\'honolulu\'"', '"483"',
    '"\'seattle\'"', '"\'4392\'"', '"3778"', '"\'cheaha mountain\'"', '"\'new hampshire\'"', '"\'louisiana\'"', '"\'minnesota\'"', '"\'north carolina\'"', '"\'mount rogers\'"', '"\'illinois\'"', '"19684"', '"702"', '"\'mount mitchell\'"', '"\'chattanooga\'"', '"87700"', '"973"', '"\'1606\'"', '"1688210"', '"4206000"', '"72563"', '"\'atlantic ocean\'"', '"511500"',
    '"25667"', '"59570"', '"\'kalamazoo\'"', '"\'elizabeth\'"', '"\'arkansas\'"', '"764"', '"\'alhambra\'"', '"64165"', '"\'greensboro\'"', '"\'ohio\'"', '"9279"', '"\'san diego\'"', '"65047"', '"67042"', '"\'clingmans dome\'"', '"82291"', '"423938"', '"\'miami\'"', '"\'nevada\'"', '"\'milwaukee\'"', '"\'29\'"', '"71133"', '"77956"', '"\'2667\'"', '"90660"', '"\'cimarron\'"',
    '"\'harvard\'"', '"90936"', '"\'lake superior\'"', '"904078"', '"\'3851\'"', '"\'north dakota\'"', '"\'helena\'"', '"158.32478632478632"', '"920600"', '"385457"', '"\'dakota\'"', '"\'tennessee\'"', '"\'worcester\'"', '"\'549\'"', '"\'westminster\'"', '"\'yellowstone\'"', '"\'brasstown bald\'"', '"\'houston\'"', '"\'brownsville\'"', '"\'powder\'"', '"284413"', '"562994"',
    '"\'huntsville\'"', '"\'arlington\'"', '"\'san angelo\'"', '"451"', '"33265"', '"\'white\'"', '"\'arvada\'"', '"77797"', '"\'driskill mountain\'"', '"\'kennedy\'"', '"\'champlain\'"', '"83.69989136822609"', '"104000"', '"64388"', '"58200"', '"360919"', '"9614"', '"81293"', '"219419"', '"\'1482\'"', '"\'mount curwood\'"', '"\'boulder\'"', '"\'woodall mountain\'"', '"\'abilene\'"',
    '"4429"', '"\'allegheny\'"', '"73892"', '"4342"', '"57648"', '"579"', '"932"', '"\'bona\'"', '"\'reading\'"', '"77508"', '"90074"', '"\'south dakota\'"', '"124160"', '"\'metairie\'"', '"740"', '"\'vermont\'"', '"4395"', '"62530"', '"\'savannah\'"', '"161148"', '"\'little missouri\'"', '"\'st. francis\'"', '"83205"', '"\'davenport\'"', '"\'wichita falls\'"', '"\'hampton\'"', '"92124"',
    '"\'734\'"', '"\'beaumont\'"', '"95172"', '"\'st. francis river\'"', '"\'topeka\'"', '"\'246\'"', '"77300"', '"\'irving\'"', '"58242"', '"964000"', '"1094"', '"\'virginia\'"', '"84054"', '"155642"', '"72893"', '"61301"', '"\'mount katahdin\'"', '"\'rochester\'"', '"126089"', '"9262000"', '"\'383\'"', '"\'boston\'"', '"76210"', '"98478"', '"103217"', '"1080"', '"\'beaver dam creek\'"', '"51700"',
    '"\'ventura\'"', '"\'hartford\'"', '"161799"', '"\'pueblo\'"', '"\'compton\'"', '"\'providence\'"', '"\'hamilton\'"', '"\'ouachita river\'"', '"\'mount whitney\'"', '"4766"', '"652700"', '"591000"', '"\'toledo\'"', '"\'4399\'"', '"52670"', '"\'rainier\'"', '"\'oxnard\'"', '"\'potomac\'"', '"67706"', '"462"', '"\'memphis\'"', '"\'niagara falls\'"', '"\'winston-salem\'"', '"4320"', '"\'magazine mountain\'"',
    '"141.93755097285333"', '"2333"', '"8284"', '"\'hollywood\'"', '"\'duluth\'"', '"66116"', '"\'albuquerque\'"', '"\'south buttress\'"', '"60.36484245439468"', '"\'neosho\'"', '"72400"', '"\'redondo beach\'"', '"\'richmond\'"', '"594000"', '"\'medford\'"', '"100538"', '"136392"', '"57632"', '"7.244343891402714"', '"57102"', '"536"', '"660"', '"557"', '"160123"', '"\'new mexico\'"', '"1461000"', '"91449"',
    '"\'gainesville\'"', '"339337"', '"92574"', '"77878"', '"401800"', '"\'whitney\'"', '"\'eugene\'"', '"64767"', '"81831"', '"175030"', '"\'iowa\'"', '"88314"', '"\'peoria\'"', '"\'decatur\'"', '"\'lexington\'"', '"78471"', '"133116"', '"231999"', '"169441"', '"57118"', '"\'abingdon\'"', '"\'hawaii\'"', '"53.330684727162335"', '"\'pierre\'"', '"\'spruce knob\'"', '"\'tahoe\'"', '"\'browne tower\'"', '"\'utica\'"',
    '"\'mckinley\'"', '"\'spokane\'"', '"4113200"', '"139060"', '"\'delaware river\'"', '"\'little rock\'"', '"5020"', '"\'rockford\'"', '"195351"', '"\'595\'"', '"\'california\'"', '"\'snake river\'"', '"\'mount davis\'"', '"\'73\'"', '"693"', '"\'warwick\'"', '"\'kenosha\'"', '"\'chula vista\'"', '"62134"', '"11400000"', '"4577"', '"93714"', '"\'cumberland\'"', '"1670"', '"\'montgomery\'"', '"91450"', '"5490000"',
    '"\'bethlehem\'"', '"\'sioux falls\'"', '"\'dallas\'"', '"130496"', '"171932"', '"61195"', '"\'945\'"', '"73240"', '"\'flathead\'"', '"\'norman\'"', '"\'540\'"', '"144903"', '"425022"', '"75568"', '"\'mount greylock\'"', '"\'85\'"', '"\'midland\'"', '"5737000"', '"290.60665362035223"', '"200452"', '"\'bloomington\'"', '"106201"', '"3968"', '"\'centerville\'"', '"\'connecticut\'"', '"76685"', '"59616"',
    '"564871"', '"1212"', '"\'san juan\'"', '"57370"', '"\'columbia\'"', '"\'altoona\'"', '"\'port arthur\'"', '"\'san antonio\'"', '"73903"', '"\'crestone\'"', '"4337"', '"64250"', '"203713"', '"57045"', '"75985"', '"40760"', '"\'tuscaloosa\'"', '"122617"', '"1950000"', '"\'sill\'"', '"94201"', '"\'839\'"', '"700807"', '"4315"', '"67972"', '"\'vallejo\'"', '"58733"', '"93939"', '"88117"', '"869"', '"114226"',
    '"\'el cajon\'"', '"\'fayetteville\'"', '"103254"', '"\'550\'"', '"\'walton county\'"', '"357870"', '"74654"', '"875538"', '"\'east los angeles\'"', '"97809"', '"\'west valley\'"', '"62321"', '"59999"', '"\'missouri\'"', '"1110"', '"944000"', '"618.9243027888448"', '"\'san mateo\'"', '"1569"', '"\'euclid\'"', '"4361"', '"\'las vegas\'"', '"118102"', '"\'columbus\'"', '"\'huntington beach\'"', '"60590"',
    '"\'colorado river\'"', '"74388"', '"\'roanoke\'"', '"\'huron\'"', '"\'new bedford\'"', '"\'crestone needle\'"', '"4372"', '"101686"', '"57078"', '"5044"', '"\'gary\'"', '"161134"', '"111797"', '"\'laredo\'"', '"62762"', '"\'mauna kea\'"', '"\'fort smith\'"', '"\'buena park\'"', '"105664"', '"149230"', '"\'2037\'"', '"119123"', '"\'98\'"', '"\'waterford\'"', '"\'norfolk\'"', '"74676"', '"70195"', '"153256"',
    '"\'tyler\'"', '"\'baton rouge\'"', '"492"', '"4316"', '"\'arkansas river\'"', '"51016"', '"53200"', '"\'levittown\'"', '"\'west allis\'"', '"75416"', '"\'manchester\'"', '"\'fremont\'"', '"\'pawtucket\'"', '"\'bellevue\'"', '"279212"', '"901"', '"\'183\'"', '"1303000"', '"\'southeast corner\'"', '"\'indiana\'"', '"6194"', '"100054"', '"262199"', '"\'mississippi river\'"', '"4357"', '"\'fort lauderdale\'"',
    '"85450"', '"109943"', '"314255"', '"223532"', '"42.969924812030065"', '"\'escondido\'"', '"3107000"', '"\'tallahassee\'"', '"\'kendall\'"', '"\'jefferson city\'"', '"\'clearwater\'"', '"\'riverside\'"', '"85911"', '"\'511\'"', '"\'framingham\'"', '"\'1024\'"', '"\'olympia\'"', '"219214"', '"59507"', '"\'mount mansfield\'"', '"131497"', '"\'146\'"', '"90027"', '"4370"', '"82362"', '"\'gila\'"', '"1119"', '"629442"',
    '"2718000"', '"75.31914893617021"', '"\'bross\'"', '"370951"', '"\'carson city\'"', '"\'quandary\'"', '"73774"', '"425259"', '"99.21327729281172"', '"84900"', '"603"', '"\'604\'"', '"74425"', '"366383"', '"72331"', '"\'el paso\'"', '"\'great salt lake\'"', '"\'lake erie\'"', '"\'clinton\'"', '"\'3424\'"', '"630"', '"73706"', '"\'mount washington\'"', '"\'78\'"', '"84997"', '"171300"', '"\'augusta\'"', '"\'corpus christi\'"',
    '"\'979\'"', '"\'fairweather\'"', '"76691"', '"\'ohio river\'"', '"149779"', '"\'lake michigan\'"', '"\'1629\'"', '"\'jersey city\'"', '"139712"', '"\'humphreys peak\'"', '"\'eagle mountain\'"', '"\'south gate\'"', '"101261"', '"92.75042444821732"', '"\'woodbridge\'"', '"58655"', '"65113"', '"83927"', '"\'orlando\'"', '"\'kettering\'"', '"\'4005\'"', '"\'guadalupe peak\'"', '"\'aurora\'"', '"\'lansing\'"', '"77116"',
    '"10.71546052631579"', '"4348"', '"\'southfield\'"', '"\'green\'"', '"\'0\'"', '"\'concord\'"', '"\'taum sauk mountain\'"', '"151.6574585635359"', '"1186"', '"816"', '"541"', '"84743"', '"9746000"', '"6471"', '"\'new jersey\'"', '"\'campbell hill\'"', '"\'north palisade\'"', '"\'winnebago\'"', '"\'chesapeake\'"', '"266979"', '"\'gannett peak\'"', '"4916000"', '"\'phoenix\'"', '"\'stamford\'"', '"261.501210653753"',
    '"92418"', '"1169"', '"\'bridgeport\'"', '"\'pittsburgh\'"', '"\'salinas\'"', '"\'70\'"', '"\'provo\'"', '"266807"', '"\'warren\'"', '"\'st. elias\'"', '"\'yale\'"', '"\'-1\'"', '"\'torreys\'"', '"73840"', '"\'pacific ocean\'"', '"\'fort wayne\'"', '"61125"', '"\'belford\'"', '"41300"', '"102466"', '"\'247\'"', '"2633000"', '"\'baltimore\'"', '"219311"', '"\'modesto\'"', '"109727"', '"\'pomona\'"', '"\'hammond\'"',
    '"\'dubuque\'"', '"\'costa mesa\'"', '"\'lafayette\'"', '"\'minneapolis\'"', '"\'south carolina\'"', '"181843"', '"23670000"', '"459"', '"2044"', '"\'champaign\'"', '"\'farmington hills\'"', '"\'grand prairie\'"', '"\'newton\'"', '"361334"', '"58099"', '"\'delaware\'"', '"52.83018867924528"', '"\'thousand oaks\'"', '"\'meriden\'"', '"\'springfield\'"', '"\'oceanside\'"', '"103328"', '"\'williamson\'"', '"\'grand rapids\'"',
    '"\'dover\'"', '"117188"', '"80.57851239669421"', '"\'alverstone\'"', '"5346800"', '"\'louisville\'"', '"\'koolaupoko\'"', '"\'westland\'"', '"\'lake of the woods\'"', '"79494"', '"\'anderson\'"', '"\'west hartford\'"', '"270230"', '"\'michigan\'"', '"\'el monte\'"', '"241741"', '"\'los angeles\'"', '"79722"', '"4399"', '"557515"', '"170616"', '"\'backbone mountain\'"', '"\'newport beach\'"', '"\'tampa\'"', '"\'albany\'"', '"3121800"',
    '"\'135\'"', '"261.8301403725611"', '"\'silver spring\'"', '"108195"', '"68139"', '"78519"', '"63668"', '"\'229\'"', '"\'105\'"', '"58267"', '"84576"', '"\'charles mound\'"', '"58441"', '"\'nebraska\'"', '"10800000"', '"\'florida\'"', '"\'grays\'"', '"\'dayton\'"', '"\'usa\'"', '"\'johnson township\'"', '"\'lakewood\'"', '"71204"', '"\'north platte\'"', '"66743"', '"\'santa barbara\'"', '"\'nashua\'"', '"\'appleton\'"', '"\'burbank\'"',
    '"\'knoxville\'"', '"\'foraker\'"', '"\'penn hills\'"', '"\'mount elbert\'"', '"\'boise\'"', '"\'independence\'"', '"330537"', '"66842"', '"81343"', '"\'timms hill\'"', '"\'cicero\'"', '"\'sassafras mountain\'"', '"\'stockton\'"', '"789704"', '"7787"', '"\'republican\'"', '"\'wichita\'"', '"\'terre haute\'"', '"5489"', '"\'arizona\'"', '"\'inglewood\'"', '"20.29754204398448"', '"469557"', '"\'bakersfield\'"', '"141654"', '"152599"', '"1114"',
    '"\'1917\'"', '"\'bethesda\'"', '"\'cheektowaga\'"', '"92742"', '"\'scottsdale\'"', '"\'santa ana\'"', '"\'quincy\'"', '"\'colorado springs\'"', '"\'texas\'"', '"\'elbert\'"', '"66784"', '"\'daly city\'"', '"4700000"', '"88622"', '"\'carson\'"', '"4354"', '"2520000"', '"80188"', '"\'701\'"', '"\'lorain\'"', '"\'mississippi\'"', '"636"', '"\'iliamna\'"', '"\'ontario\'"', '"2966850"', '"\'hubbard\'"', '"2913000"', '"111.67647617239416"',
    '"\'anchorage\'"', '"\'chicago\'"', '"385164"', '"\'churchill\'"', '"17.208480565371026"', '"152453"', '"\'uncompahgre\'"', '"14229000"', '"\'san leandro\'"', '"\'st. clair\'"', '"\'4202\'"', '"1458"', '"64107"', '"\'troy\'"', '"77216"', '"75051"', '"108999"', '"61615"', '"\'west virginia\'"', '"\'billings\'"', '"\'red\'"', '"118794"', '"\'shreveport\'"', '"81548"', '"\'potomac river\'"', '"\'princeton\'"', '"69855"', '"76698"', '"\'torrance\'"',
    '"151968"', '"\'2207\'"', '"403.1548757170172"', '"345496"', '"\'edison\'"', '"77568"', '"\'4205\'"', '"\'4011\'"', '"\'death valley\'"', '"\'mount mckinley\'"', '"5463000"', '"58913"', '"\'whittier\'"', '"1125000"']