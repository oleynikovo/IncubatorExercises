"""
script that checks the validity of entered dotted decimals IP addresses
and masks, converts the  dotted decimal format to binary,
and finds the network and broadcast address
for the entered IP/mask combination
"""

import sys, re

""" define magic numbers """
ROW_WIDTH = 10
PADDING_WIDTH = 7
BITS_IN_IP = 32
BITS_IN_SEGMENT = 8

""" prompt for and read ip address, and generate regex checking validity of the format """
ip_addr = raw_input('Enter Ip address:')
ip_re = re.compile('^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}$')

""" if the input did not match the first time, prompt again until a valid format of address is entered """
while not ip_re.match(ip_addr):
    print('Invalid IP address format')
    ip_addr = raw_input('Enter Ip address:')
    ip_re = re.compile('^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9][0-9]|[0-9]){1}$')

""" prompt for and read decimal subnet mask, and generate regex checking validity of the format """
subnet_input = raw_input('Enter subnet mask in decimal format:')
subnet_re = re.compile('^/(3[0-2]|[1-2][0-9]|[0-9])$')

""" if the input did not match the first time, prompt again until a valid format of address is entered """
while not subnet_re.match(subnet_input):
    print('Subnet mask is invalid')
    subnet_input = raw_input('Enter subnet mask in decimal format:')
    subnet_re = re.compile('^/(3[0-2]|[1-2][0-9]|[0-9])$')

""" inputs are verified to be proper """
sys.stdout.write('\n')
""" split ip string by the dots """
ip_octets = ip_addr.split('.')
""" print octets in decimal """
for octet in ip_octets:
    sys.stdout.write(octet.rjust(PADDING_WIDTH).ljust(ROW_WIDTH))
sys.stdout.write('\n')

""" convert octets to binary and print them """
ip_octets_bin = [format(int(octet), '08b') for octet in ip_octets]
for octet in ip_octets_bin:
    sys.stdout.write(octet.ljust(ROW_WIDTH))
sys.stdout.write('\n')

""" find the network address """
"""     find number of least significant bits to replace for net/bcast addresses """
trail_len = BITS_IN_IP - int(subnet_input[1:])
ip_octets_bin_string = ''.join(ip_octets_bin)
"""     replace the least significant bits with 0's """
ip_network_bin = ip_octets_bin_string[:BITS_IN_IP-trail_len]+'0'*trail_len
"""     convert network address to dotted decimal notation """
ip_network_dot_decimal = [str(int(ip_network_bin[i:i+BITS_IN_SEGMENT], 2)) for i in range(0, BITS_IN_IP, BITS_IN_SEGMENT)]
""" find the broadcast address """
"""     replace the least significant bits with 1's """
ip_bcast_bin = ip_octets_bin_string[:BITS_IN_IP-trail_len]+'1'*trail_len
"""     convert broadcast address to dotted decimal notation """
ip_bcast_dot_decimal = [str(int(ip_bcast_bin[i:i+BITS_IN_SEGMENT], 2)) for i in range(0, BITS_IN_IP, BITS_IN_SEGMENT)]

""" print network and broadcast address """
print('network address is: '+'.'.join(ip_network_dot_decimal)+subnet_input)
print('broadcast address is: '+'.'.join(ip_bcast_dot_decimal)+subnet_input)
