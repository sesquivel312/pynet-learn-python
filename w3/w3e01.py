#!/usr/bin/env python
import sys

if len(sys.argv) != 2:
    print 'error\n'
else:
    add_string = sys.argv.pop()
    add_list = add_string.split('.')
    if len(add_list) != 4:
        sys.exit('invalid address')

    print '{:20}{:12}'.format('Dotted Decimal Add','Binary')
    print '{:20}{:08b}.{:08b}.{:08b}.{:08b}'.format(add_string,int(add_list[0]),int(add_list[1]),int(add_list[2]),int(add_list[3]))