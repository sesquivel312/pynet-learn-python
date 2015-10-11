show_output_string = '''entry1 = "*  1.0.192.0/18   157.130.10.233        0 701 38040 9737 i"
entry2 = "*  1.1.1.0/24       157.130.10.233        0 701 1299 15169 i"
entry3 = "*  1.1.42.0/24     157.130.10.233        0 701 9505 17408 21465 i"
entry4 = "*  1.0.192.0/19   157.130.10.233        0 701 6762 6762 6762 6762 38040 9737 i"'''

show_output_list = show_output_string.split("\n")
print '{:20}{:20}'.format('prefix','as path')
for line in show_output_list:
    temp = line.split()
    #print temp
    print '{:20}{:<}'.format(temp[3],temp[6:-1])
    #print temp[6:-1]