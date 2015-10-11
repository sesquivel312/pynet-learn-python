#!/usr/bin/env python
import os
import sys
import pyfornet as pfn

if len(sys.argv) != 2:
    print '***\nincorrect num args'
    os._exit(1)
else:
    valid_add = pfn.ipv4_add_verify(sys.argv[1])
    if type(valid_add) is list:
        print '.'.join([ str(i) for i in  valid_add ])