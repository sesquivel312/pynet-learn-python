'''
    This is a module to collect functions created as a result of working exercises given in the on-line class
    learning python for networkers (or something like that).  This makes then reusable which simplifies the
    exercises when they require reuse of previous work

    for now i'm importing this way:
    import pyfornet as pfn so I don't break name spaces and I save some typing - i.e. access functions this way:
    pfn.<funcname>
'''

import fileinput
import re


def parse_show_ver_ver(string):  # returns vendor name string or False
    if 'Cisco IOS Software' in string:
        return string.split(',')[2].split()[1]
    elif 'Software image version' in string:
        return string.split(': ')[1]
    else:
        return False
        # if not re.match(r'ROM', string):  # skip the line beginning "ROM"
        #     patt = re.compile(r'Version ([^,]+),')
        #     re_result = patt.search(string)
        #     if re_result:
        #         return re_result.group(1)
        #     else:
        #         return False


def parse_show_ver_vendor_model(
        string):  # returns dict {'vendor':<vendornamestring>|False, 'model':<modelstring>|False}
    vendor_model = {'vendor': False, 'model': False}
    if 'bytes of memory' in string:
        vendor_model['vendor'] = 'cisco'
        vendor_model['model'] = string.split()[1]
        return vendor_model
    elif 'Arista' in string:
        vendor_model['vendor'] = 'arista'
        vendor_model['model'] = string.split()[1]
        return vendor_model
    return vendor_model
    # detected_vendor_model = {'vendor': False, 'model': False}
    #
    # patt_cisco = re.compile(r'^Cisco ([\w-]+)')
    # patt_arista = re.compile(r'Arista ([\w-]+)')
    # patterns = {'cisco': patt_cisco, 'arista': patt_arista}
    #
    # match_results = {vendor: pattern.match(string) for vendor, pattern in patterns.items()}
    #
    # for vendor, result in match_results.items():
    #     if result:
    #         if vendor == 'cisco':  # if cisco, get the "correct" model - pattern will match undesired lines
    #             tmp_model = result.group(1)
    #             if tmp_model not in ('IOS', 'Systems'):
    #                 detected_vendor_model['vendor'] = vendor
    #                 detected_vendor_model['model'] = result.group(1)
    #         else: # currently other vendords aren't checked for undesired pattern matches
    #             detected_vendor_model['vendor'] = vendor
    #             detected_vendor_model['model'] = result.group(1)
    #
    # return detected_vendor_model


def parse_show_ver_uptime(string):
    if 'uptime is' in string:  # cisco
        return string.split(' uptime is ')[1]
    elif 'Uptime:' in string:  # arista
        return string.split(': ')[1]
    else:
        return False
        # patt = re.compile(r'uptime is (.+$)')
        # result = patt.search(string)
        # if result:
        #     return result.group(1)
        # else:
        #     return False


def parse_show_ver_serialnum(string):
    if 'board ID' in string:
        return string.split(' board ID ')[1]
    elif 'Serial number:' in string:
        return string.split(': ')[1]
    else:
        return False

        # patt = re.compile(r'board ID ([\w]+)')
        # result = patt.search(string)
        # if result:
        #     return result.group(1)
        # else:
        #     return False


def parse_uptime(device_info_dict):  # returns dict with years, weeks, etc. down to minutes
    vendor = device_info_dict['vendor']
    tmp_time = {'years': 0,
                'weeks': 0,
                'days': 0,
                'hours': 0,
                'minutes': 0, }  # holds the text based time
    if vendor == 'cisco':
        substrings = device_info_dict['uptime'].split(',')
    elif vendor == 'arista':
        substrings = device_info_dict['uptime'].split(' and ')
    else:
        return tmp_time  # vendor not recognized
    if len(substrings) > 5:
        return 'BAD TIME'
    else:
        for ss in substrings:
            sss = ss.split()
            if sss[1] in ('year', 'years'):
                tmp_time['years'] = int(sss[0])
            if sss[1] in ('weeks', 'week'):
                tmp_time['weeks'] = int(sss[0])
            if sss[1] in ('days', 'day'):
                tmp_time['days'] = int(sss[0])
            if sss[1] in ('hours', 'hour'):
                tmp_time['hours'] = int(sss[0])
            if sss[1] in ('minutes', 'minute'):
                tmp_time['minutes'] = int(sss[0])
        return tmp_time


def text_time_to_sec(text_time_dict):  # made assumption int is big enough?
    seconds = (31536000 * text_time_dict['years'] +
               604800 * text_time_dict['weeks'] +
               86400 * text_time_dict['days'] +
               3600 * text_time_dict['hours'] +
               60 * text_time_dict['minutes'])
    return seconds


def parse_show_ver(line_list):
    serialnum = vendor = model = version = uptime = False

    for line in line_list:
        tmp_version = parse_show_ver_ver(line)
        tmp_vendor_model = parse_show_ver_vendor_model(line)
        tmp_uptime = parse_show_ver_uptime(line)
        tmp_serialnum = parse_show_ver_serialnum(line)
        if tmp_version:
            version = tmp_version
        if tmp_vendor_model['vendor']:
            vendor = tmp_vendor_model['vendor']
            model = tmp_vendor_model['model']
        if tmp_uptime:
            uptime = tmp_uptime
        if tmp_serialnum:
            serialnum = tmp_serialnum

    device_data = {
        'serialnum': serialnum,
        'vendor': vendor,
        'model': model,
        'version': version,
        'uptime': uptime
    }

    return device_data


def parse_print_sh_ip_int_brie(interfaces):
    interfaces = interfaces[1:]  # assumes output always begins with header
    intf_status_dict = {}
    for interface in interfaces:
        intf_list = interface.split()
        intf_status_dict[intf_list[0]] = {'address': intf_list[1], 'link_status': intf_list[4],
                                          'proto_status': intf_list[5]}

    print '{:<15}{:<15}{:<15}{:<15}'.format('If Name', 'Address', 'Link Status', 'Protocol Status')
    for interface, params in intf_status_dict.items():
        if params['link_status'] == 'up' and params['proto_status'] == 'up':
            print '{:<15}{:<15}{:<15}{:<15}'.format(interface, params['address'], params['link_status'],
                                                    params['proto_status'])


def ipv4_add_verify(add_string):  # returns list with v4 octets in order or False (prints errors)
    '''
    take an ip address as input and verify it meets the following conditions:
    4 octets
    first octet is [1..126] or [128..223] - i.e. not 0, 127 or 224+
    is not in 169.254/16
    octet 2-4 are [1..255]

    if criteria are met print out the address
    '''

    try:
        tmp_add_list = add_string.split('.')
        if len(tmp_add_list) != 4:
            print '***\ninvalid address - num octets not 4'
            return False
        for idx, octet in enumerate(tmp_add_list):
            tmp_add_list[idx] = int(octet)
            if idx == 0:  # first octet checks
                if tmp_add_list[idx] == 0 or tmp_add_list[idx] == 127 or tmp_add_list[idx] > 223:
                    print '***\nfirst octet has "bad" value'
                    return False
            elif idx == 1:  # second octet checks
                if tmp_add_list[idx] > 254 or tmp_add_list[idx] < 0:  # valid value
                    print '***\ninvalid address - bad octet value'
                    return False
                elif tmp_add_list[0:2] == [169, 254]:  # this address is not in the link local range
                    print '***\nlink local address'
                    return False
            else:
                if tmp_add_list[idx] > 254 or tmp_add_list[idx] < 0:
                    print '***\ninvalid address - bad octet value'
                    return False
        return tmp_add_list
    except:  # this exception is to broad need to tighten up (or may not be able to stop this if it's in a loop
        print '***\nat least one octet was not a number'
        return False


def print_device_info(dev_dict):
    '''
        :param device_dict: hierarchical dictionary containing network device data formatted like so:
            { 'device_name': {'model':<model>,'type': <type>, 'intfs':[<name1>,...,<namen>] }, ...}
        :returns nothing"

        prints out formatted device data
    '''
    for dev, attribs in dev_dict.items():
        print dev
        for attrib, val in attribs.items():
            print '\t',
            if attrib == 'intfs':
                print 'intfs:\n\t\t',
                for i in val:
                    print i,
                print '\n',
            else:
                print attrib + ':', val


def devices_connected(d1, d2, e_list):
    '''
    :param d1: string
    :param d2: string
    :param e_list: list of pairs of tuples: e.g. [(('d1','i1'),('d2','i2')),...]
    :return: True/False

    determine if two devices (given by name) are connected
    '''
    connected = False
    NAME = 0
    for e in e_list:
        if e[0][NAME] in (d1, d2):  # if the interface belongs to one of the devices
            if e[1][NAME] in (d1, d2):
                connected = True
    return connected


def build_dev_dict(scnd_output_file_list):
    '''
    :param scnd_output_file_list: this is a list of fully qualified file names.  Using the fileinput module each file
     will be opened in turn, for each file each line will be interated over.  The files are the output of
     'show cdp nei detail'
    :return: completed device dictionary

    the dictionary returned is hierarchical and is formatted like so:
    { 'device_name': {
            'model':<model>,
            'type': <type>,
            'addresses': [<add1>,...,<addn>],
            'intfs': [<name1>,...,<namen>],
            'adj_devs': {'<dev1>':[<adjdevname>,<localdevintf>,<adjdevintf>],
                         '<dev2>':[<adjdevname>,<localdevintf>,<adjdevintf>], ...
                         }
                      },
        ...
    }

    NB: the intfs key has a list for a value

    I believe the 'intfs' list member for a device is redundant, you can construct it from the adj_devs dict, the device
    is likely to have other interfaces, but since this is all from CDP we'll only know about the interfaces with cdp
    adjacent devices.  I will keep it though, bc. this could be extended to include data from sources other than CDP
    '''

    dev_dict = {}
    tmp_adj_dev = tmp_local_dev = tmp_adj_intf = tmp_local_intf = ''

    for line in fileinput.input(scnd_output_file_list):
        if '>' in line:  # get local device name here
            tmp_local_dev = line.split('>')[0]
            if tmp_local_dev not in dev_dict.keys():
                dev_dict[tmp_local_dev] = {'model': '', 'type': '', 'addresses': [], 'intfs': [], 'adj_devs': {}}
        elif 'Device ID:' in line:  # grab the adj device name
            tmp_adj_dev = line.split(': ')[1].rstrip('\n')
            if tmp_adj_dev not in dev_dict.keys():
                dev_dict[tmp_adj_dev] = {'model': '', 'type': '', 'addresses': [], 'intfs': [], 'adj_devs': {}}
            if tmp_adj_dev not in dev_dict[tmp_local_dev]['adj_devs'].keys():  # add to adjacent devices dict
                dev_dict[tmp_local_dev]['adj_devs'][tmp_adj_dev] = []
        elif 'IP address: ' in line:
            tmp_adj_dev_add = line.split(': ')[1].rstrip('\n')
            if tmp_adj_dev_add not in dev_dict[tmp_adj_dev]['addresses']:
                dev_dict[tmp_adj_dev]['addresses'].append(tmp_adj_dev_add)
        elif 'Platform:' in line: # get model and type here
            tmp_list = line.split(',')
            dev_dict[tmp_adj_dev]['model'] = tmp_list[0].split()[2].rstrip('\n')
            if 'Router' in tmp_list[1].split()[1:]:  # this section should check for existing values
                dev_dict[tmp_adj_dev]['type'] = 'Router'
            else:
                dev_dict[tmp_adj_dev]['type'] = 'Switch'
        elif 'outgoing' in line:  # get two interfaces from this line "local" and "remote"
            tmp_list = line.split(',')
            tmp_local_intf = tmp_list[0].split(': ')[1].rstrip('\n')
            tmp_adj_intf = tmp_list[1].split(': ')[1].rstrip('\n')

            if tmp_local_intf not in dev_dict[tmp_local_dev]['intfs']: # add device intf if needed
                dev_dict[tmp_local_dev]['intfs'].append(tmp_local_intf)

            if tmp_adj_intf not in dev_dict[tmp_adj_dev]['intfs']:  # add dev intf if needed
                dev_dict[tmp_adj_dev]['intfs'].append(tmp_adj_intf)

            dev_dict[tmp_local_dev]['adj_devs'][tmp_adj_dev].extend([tmp_local_intf, tmp_adj_intf])

    return dev_dict


def build_dev_dict_re(scnd_output_file_list):
    '''
    :param scnd_output_file_list: this is a list of strings where ea. string is the output of 'show cdp nei detail'
    :return: completed device dictionary

    the dictionary returned is hierarchical and is formatted like so:
    { 'device_name': {
            'model':<model>,
            'type': <type>,
            'addresses': [<add1>,...,<addn>],
            'intfs': [<name1>,...,<namen>],
            'adj_devs': {'<dev1>':[<adjdevname>,<localdevintf>,<adjdevintf>],
                         '<dev2>':[<adjdevname>,<localdevintf>,<adjdevintf>], ...
                         }
                      },
        ...
    }

    NB: the intfs key has a list for a value

    I believe the 'intfs' list member for a device is redundant, you can construct it from the adj_devs dict, the device
    is likely to have other interfaces, but since this is all from CDP we'll only know about the interfaces with cdp
    adjacent devices.  I will keep it though, bc. this could be extended to include data from sources other than CDP

    This function differs from build_dev_dict in that it uses python regular expressions library rather than simple
    string methods and takes files as arguments, rather than a list of strings, hence the name build_dev_dict_re_file.

    I implemented using RE for about 85% of the function and then quickly realized it was WAY too much of a pain to
    use RE's rather than simple string methods.  I updated the "non re" version of this function to take the list of
    files (rather than a list of lines) and added the 'addresses' key to the dict.
    '''

    dev_dict = {}
    re_ip_address = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    re_local_dev_name = re.compile(r'([a-zA-Z0-9-]+)>')
    re_adj_dev_name = re.compile(r'Device ID: ([a-zA-Z0-9-]+)')
    re_model_type = re.compile(r'Platform: ([\w -]+), +Capabilities: ([\w -]+)')

    for line in fileinput.input(scnd_output_file_list):

        if '>' in line:  # get local device name here & reset temp_x variables << FIX THIS???
            tmp_adj_dev = tmp_local_dev = tmp_adj_intf = tmp_local_intf = ''
            tmp_local_dev = re_local_dev_name.search(line).group(1)
            if tmp_local_dev not in dev_dict.keys():
                dev_dict[tmp_local_dev] = {'model': '', 'type': '', 'addresses': [], 'intfs': [], 'adj_devs': {}}
        elif 'Device ID:' in line:  # grab the adj device name
            tmp_adj_dev = re_adj_dev_name.search(line).group(1)
            if tmp_adj_dev not in dev_dict.keys():
                dev_dict[tmp_adj_dev] = {'model': '', 'type': '', 'addresses': [], 'intfs': [], 'adj_devs': {}}
            if tmp_adj_dev not in dev_dict[tmp_local_dev]['adj_devs'].keys():  # add to adjacent devices dict
                dev_dict[tmp_local_dev]['adj_devs'][tmp_adj_dev] = []
        elif 'IP address: ' in line:
            tmp_adj_dev_add = re_ip_address.search(line).group()
            if tmp_adj_dev_add not in dev_dict[tmp_adj_dev]['addresses']:
                dev_dict[tmp_adj_dev]['addresses'].append(tmp_adj_dev_add)
        elif 'Platform:' in line: # get model and type here
            # tmp_list = line.split(',')
            m = re_model_type.search(line)
            dev_dict[tmp_adj_dev]['model'] =  m.group(1) # tmp_list[0].split()[2]
            if 'Router' in m.group(2):  # this section should check for existing values
                dev_dict[tmp_adj_dev]['type'] = 'Router'
            else:
                dev_dict[tmp_adj_dev]['type'] = 'Switch'
        elif 'outgoing' in line:  # get two interfaces from this line "local" and "remote"
            tmp_list = line.split(',')
            tmp_local_intf = tmp_list[0].split(': ')[1].rstrip('\n')
            tmp_adj_intf = tmp_list[1].split(': ')[1].rstrip('\n')

            if tmp_local_intf not in dev_dict[tmp_local_dev]['intfs']: # add device intf if needed
                dev_dict[tmp_local_dev]['intfs'].append(tmp_local_intf)

            if tmp_adj_intf not in dev_dict[tmp_adj_dev]['intfs']:  # add dev intf if needed
                dev_dict[tmp_adj_dev]['intfs'].append(tmp_adj_intf)

            dev_dict[tmp_local_dev]['adj_devs'][tmp_adj_dev].extend([tmp_local_intf, tmp_adj_intf])

    return dev_dict


def parse_ospf_int_params(sioi_output_list):
    '''

    :param sioi_output_list: list whose members are the lines of the output of "show ip ospf interface <ifspec>"
      i.e. it's the output for one specific interface
    :return: dictionary associating the parameters to the interface name, e.g.
    {'<ifname1>':{
        'ip_addr':<ipaddr>,
        'area':<area_id>,
        'iftype':<ospf_intf_type>,
        'cost':<integer_cost>,
        'timers':(<hello>,<dead>)
       },
       ...,
     '<ifnamen>':{
        'ip_addr':<ipaddr>,
        'area':<area_id>,
        'iftype':<ospf_intf_type>,
        'cost':<integer_cost>,
        'timers':(<hello>,<dead>)
       }
    }
    '''

    dict = {}
    ifspec = ''
    tmp_data = []

    for line in sioi_output_list:
        line = line.rstrip('\n')
        if 'line protocol' in line:
            ifspec = line.split()[0]
            dict[ifspec] = {'address': '', 'area_id':-1, 'type': '', 'cost': -1, 'timers': (-1,-1)}
            if 'Loopback' in ifspec:
               dict[ifspec]['timers'] = ('NA','NA')
        if 'Internet Address' in line:
            tmp_data = line.split(',')
            dict[ifspec]['address'] = tmp_data[0].split()[2]
            dict[ifspec]['area_id'] = int(tmp_data[1].split()[1])
        if 'Process ID' in line:
            tmp_data = line.split(',')  # extract type
            dict[ifspec]['type'] = tmp_data[2].split()[2]
            dict[ifspec]['cost'] = int(tmp_data[3].split(': ')[1])
        if 'Timer intervals' in line:
            tmp_data = line.split(',')
            t_hello = int(tmp_data[1].split()[1])
            t_dead = int(tmp_data[2].split()[1])
            dict[ifspec]['timers'] = (t_hello, t_dead)

    return dict

