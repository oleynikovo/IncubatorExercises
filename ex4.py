""" script to automatically generate configurations for switchports """

import re

""" defined templates for configurations """
access_template = ['switchport mode access',
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan {}']

""" prompt user to configure state of the port """
int_mode = raw_input('Enter interface mode (access/trunk): ')

while int_mode not in ["access", "trunk"]:
    """ if the interface mode is not one of access or trunk, keep prompting user to enter the mode """
    int_mode = raw_input('Enter interface mode (access/trunk): ')

""" prompt user to enter the port name to be configured """
int_name = raw_input('Enter interface type and number: ')

if int_mode == "access":
    """ if switchport mode is access, prompt user to enter vlan number to which to assign the port """
    vlan_num = raw_input('Enter VLAN number: ')
    while re.match('\D', vlan_num):
        """ if the user incorrectly entered vlans (i.e., anything other than a number), prompt again """
        vlan_num = raw_input('Enter VLAN number: ')

    """ print the IOS commands """
    access_template[1] = access_template[1].replace('{}', vlan_num)
    print("Interface " + int_name)
    for command in access_template: print(command)

elif int_mode == "trunk":
    """ if switchport mode is trunk, prompt user to enter allowed vlans on the trunk """
    vlans_allowed = raw_input('Enter allowed VLANs: ')
    while not (re.match('^((\d+-\d+,?)|(\d+,?))*\d*$', vlans_allowed) and vlans_allowed[-1] != ','):
        """ if the user entered some bad list of vlans, prompt again """
        vlans_allowed = raw_input('Enter allowed VLANs: ')

    """ print the IOS commands """
    trunk_template[2] = trunk_template[2].replace('{}', vlans_allowed)
    print("Interface " + int_name)
    for command in trunk_template: print(command)
