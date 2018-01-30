""" script to exctract routing info from router's routing table """

import re

""" 
define a static dictionary to 
map routing protocol code to the actual protocol name 
"""
protocol_map = {
    "R": "RIP",
    "M": "mobile",
    "B": "BGP",
    "D": "EIGRP",
    "EX": "EIGRP external",
    "O": "OSPF",
    "IA": "OSPF inter area",
    "N1": "OSPF NSSA external type 1",
    "N2": "OSPF NSSA external type 2",
    "E1": "OSPF external type 1",
    "E2": "OSPF external type 2",
    "E": "EGP",
    "i": "IS-IS",
    "su": "IS-IS summary",
    "L1": "IS-IS level: 1",
    "L2": "IS-IS level: 2",
    "ia": "IS-IS inter area",
    "H": "NHRP",
    "l": "LISP"
}

""" define magic numbers """
COLUMN_WIDTH = 20

""" read in routing table from the source """
f = open("ShowIpRoute.txt")
routing_info = f.read()
f.close()

"""
build a regular expression to match on a destination network address 
for routes learned from dynamic protocols

re part 1: group capture protocol code (capture group 2, because group 1 is redundant)
    (\w[\s\*]){0,1}(\w+)
re part 2: group capture ip address of destination network (capture group 3)
    ((?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1})
re part 3: group capture metric (capture group 4)
    (\d+/\d+)
re part 4: group capture next hop address (capture group 5)
    ((?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1})
re part 5: group capture time since last update (capture group 6)
    (\d+:[0-5]\d:[0-5]\d)    
re part 6: group capture exit interface (capture group 7)
    (.*)
"""
dynamic_protocol_info_re = re.compile("(\w[\s\*]){0,1}(\w+) "
                                      "((?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}) "
                                      "\[(\d+/\d+)\] via "
                                      "((?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}), "
                                      "(\d+:[0-5]\d:[0-5]\d), "
                                      "(.*)")

""" capture groups and build a dictionary for each route """
routes = []
for dynamic_route_match in re.findall(dynamic_protocol_info_re, routing_info):
    """ capture each group """
    route = dict()
    route["Protocol:"] = protocol_map[dynamic_route_match[1]]
    route["Prefix:"] = dynamic_route_match[2]
    route["AD/Metric:"] = dynamic_route_match[3]
    route["Next-Hop:"] = dynamic_route_match[4]
    route["Last Update:"] = dynamic_route_match[5]
    route["Outbound interface:"] = dynamic_route_match[6]
    routes.append(route)

""" print out routing info of each dynamic route """
for route in routes:
    """ print the key and print the value """
    for route_key in ["Protocol:", "Prefix:", "AD/Metric:",
                      "Next-Hop:", "Last Update:", "Outbound interface:"]:
        print(route_key.ljust(COLUMN_WIDTH)+route[route_key])
    print("\n")
