'''
    w7e01.py <directory>

    takes a directoyr passed as an argument, if provided, and iterates over the lines of all the files found parsing
    out data to create a dictionary of device data.

    The files are assumed to be output from "show cdp neig detail".

    The files are assumed to be named r*.txt or s*.txt

    If no directory is provided as an argument a default directory is chosen
'''

import glob
import sys
import pyfornet as pfn
import pprint as pp


data_file_directory = '/home/steve/dev/python-for-networkers/datafiles'  # set default dir

if len(sys.argv) == 2:
    data_file_directory = sys.argv[1]

if data_file_directory.endswith('/'):
    data_file_directory += '[rs]*.txt'
else:
    data_file_directory += '/[rs]*.txt'

file_list = glob.glob(data_file_directory)

dict = pfn.build_dev_dict(file_list)

pp.pprint(dict)