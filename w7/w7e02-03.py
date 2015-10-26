'''
    w7e02-03.py <file>

    takes a file name passed as an argument, if provided, and iterates over the lines of the file creating a dict that
    contains a few ospf parameters per interface.

    The files are assumed to be output from "sh ip ospf inter".

    if a fully qualified file name is not provided then it's assumed to be /home/steve/dev/python-for-networkers/datafiles

    NB: Not doing any error checking on the input parameter
    NB: This is really just exercise #3, but, it's really no different from ex. #2 so I've not included code for #2
'''

import sys
import pyfornet as pfn
import pprint as pp


data_file = '/home/steve/dev/python-for-networkers/datafiles/ospf_data.txt'  # set default filename

if len(sys.argv) == 2:
    if sys.argv[1].startswith('/'):
        data_file = sys.argv[1]
    else:
        print '\n*** Something wrong with the file name or the associated path\n'
        sys.exit()

with open(data_file,'r') as t_file:
    lines = t_file.readlines()

dict = pfn.parse_ospf_int_params(lines)

pp.pprint(dict)