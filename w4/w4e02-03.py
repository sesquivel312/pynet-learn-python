import pprint
import re
import pyfornet as pfn

cisco_output = '''Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)
Technical Support:
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Fri 29-Oct-10 00:02 by prod_rel_team
ROM: System Bootstrap, Version 12.4(22r)YB5, RELEA2SE SOFTWARE (fc1)

twb-sf-881 uptime is 7 weeks, 5 days, 19 hours, 23 minutes
System returned to ROM by reload at 15:33:36 PST Fri Feb 28 2014
System restarted at 15:34:09 PST Fri Feb 28 2014
System image file is "flash:c880data-universalk9-mz.150-1.M4.bin"
Last reload type: Normal Reload
Last reload reason: Reload Command

Cisco 881 (MPC8300) processor (revision 1.0) with 236544K/25600K bytes of memory.
Processor board ID FTX1000038X

5 FastEthernet interfaces
1 Virtual Private Network (VPN) Module
256K bytes of non-volatile configuration memory.
126000K bytes of ATA CompactFlash (Read/Write)

License Info:
License UDI:
-------------------------------------------------
Device#   PID                   SN
-------------------------------------------------
*0        CISCO881-SEC-K9       FTX1000038X

License Information for 'c880-data'
    License Level: advipservices   Type: Permanent
    Next reboot license Level: advipservices

Configuration register is 0x2102'''

arista_output = '''Arista DCS-7150S-64-CL-F
Hardware version: 01.01
Serial number: JPE13120819
System MAC address: 001c.7326.fd0c
Software image version: 4.13.2F
Architecture: i386
Internal build version: 4.13.2F-1649184.4132F.2
Internal build ID: eeb3c212-b4bd-4c19-ba34-1b0aa36e43f1
Uptime: 1 hour and 36 minutes
Total memory: 4017088 kB
Free memory: 1473280 kB'''


show_output_lines = arista_output.split('\n')

device_data = pfn.parse_show_ver(show_output_lines)
uptime_dict = pfn.parse_uptime(device_data)

pprint.pprint(device_data)
pprint.pprint(uptime_dict)
print pfn.text_time_to_sec(uptime_dict)
