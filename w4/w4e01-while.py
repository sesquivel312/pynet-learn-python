'''
take an ip address as input and verify it meets the following conditions:
4 octets
first octet is [1..126] or [128..223] - i.e. not 0, 127 or 224+
is not in 169.254/16
octet 2-4 are [1..255]

if criteria are met print out the address

Continue to prompt for a valid address until you get one
'''
#!/usr/bin/env python
import sys
import os

add_valid = False
while (not add_valid):
    try:
        add_string = raw_input('Enter an IP address: ')
        add_list = add_string.split('.')
        if len(add_list) != 4:
            print '***\ninvalid address - num octets not 4'
            continue
        for idx, octet in enumerate(add_list):
            add_list[idx] = int(octet)
            if idx == 0:  # first octet checks
                    if add_list[idx] == 0 or add_list[idx] == 127 or add_list[idx] > 223:
                        print '***\nfirst octet has "bad" value'
                        continue
            elif idx == 1:  # second octet checks
                if add_list[idx] > 254 or add_list[idx] < 0:  # valid value
                    print '***\ninvalid address - bad octet value'
                    continue
                elif add_list[0:2] == [169, 254]:  # this address is not in the link local range
                    print '***\nlink local address'
                    continue
            else:
                if add_list[idx] > 254 or add_list[idx] < 0:
                    print '***\ninvalid address - bad octet value'
                    continue
        print '.'.join([ str(i) for i in add_list ])
        add_valid = True
        # print '{:20}{:12}'.format('Dotted Decimal Add','Binary')
        # print '{:20}{:08b}.{:08b}.{:08b}.{:08b}'.format(add_string,int(add_list[0]),int(add_list[1]),int(add_list[2]),int(add_list[3]))
    except:
        print '***\nat least one octet was not a number'