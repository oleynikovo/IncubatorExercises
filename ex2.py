""" script that finds common and unique vlans across all trunking interfaces """

import re

""" read in trunking configurations from a source """
f = open('commands.txt', 'r')
trunking_configs = f.read()
f.close()
#trunking_configs = trunking_configs_raw.split('\n')

""" 
build a regular expression to match 
and capture the vlans allowed on each interface 
"""
vlans_re = re.compile('switchport trunk allowed vlan (.*)')
vlans_per_interface = []
for allowed_vlans in re.findall(vlans_re, trunking_configs):
    """ split vlan info by commas """
    allowed_vlans_list = allowed_vlans.split(',')
    """ remove whitespace before and after vlan numbers, if any """
    allowed_vlans_list_clean = [vlan.strip() for vlan in allowed_vlans_list]
    """ record allowed vlans on the interface """
    vlans_per_interface.append(allowed_vlans_list_clean)

""" gather union of vlans: every vlan allowed on at least one trunk """
union_vlans = []
for trunking_vlans in vlans_per_interface:
    for vlan in trunking_vlans:
        if vlan not in union_vlans:
            union_vlans.append(vlan)

""" from every interface, find the common vlans """
common_vlans = []
for union_vlan in union_vlans:
    if all([union_vlan in trunking_vlans for trunking_vlans in vlans_per_interface]):
        common_vlans.append(union_vlan)

""" from every interface, find unique vlans """
unique_vlans = []
for union_vlan in union_vlans:
    if sum([union_vlan in trunking_vlans for trunking_vlans in vlans_per_interface]) == 1:
        unique_vlans.append(union_vlan)

""" sort the resulting lists in ascending order and print them """
common_vlans.sort(key=lambda x: int(x))
unique_vlans.sort(key=lambda x: int(x))
print('List_1='+str(common_vlans))
print('List_2='+str(unique_vlans))
