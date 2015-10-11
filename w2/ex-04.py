show_out = 'cisco_ios = "Cisco IOS Software, C880 Software (C880DATA-UNIVERSALK9-M), Version 15.0(1)M4, RELEASE SOFTWARE (fc1)"'

show_out_list = show_out.split(',')
version = show_out_list[2]
print 'ios version: ' + version[8:]

