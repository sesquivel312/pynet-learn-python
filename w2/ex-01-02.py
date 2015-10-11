__author__ = 'steve'

input_net = raw_input('enter a /24 in dotted decimal: ')
input_net_list = input_net.split('.')
net_final = input_net_list[0:3]
net_final.append('0')
print '{:20}{:20}{:20}'.format('NETWORK NUMBER','FIRST OCTET BIN', 'FIRST OCTET HEX')
print '{:20}{first:<#20b}{first:<#20x}'.format('.'.join(net_final),first=int(net_final[0]))

print '{:12}{:12}{:12}{:12}'.format('First','Second', 'Third', 'Fourth')
print '{:<#12b}{:<#12b}{:<#12b}{:<#12b}'.format(int(net_final[0]),int(net_final[1]),int(net_final[2]),int(net_final[3]))
