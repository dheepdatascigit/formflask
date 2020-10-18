import ipaddress
import json

# global declarations
default_intid = 'Gi0/0/1'
default_subnet = '159.127.0.0/23'
default_description = 'none'

def version():
    """ version of the code 
    """

    ver = 1.0
    return ver


def cisco_intcfg(subnet=default_subnet, vlanid=None, intid=default_intid, desc=default_description):
    """ generate cisco interface configuration given ip subnet and vlanid
    """

    cfg_list = []

    #print("cisco_intcfg")

    try:
        varip = ipaddress.ip_network(subnet)
    except Exception as err:
        return "Error: " + str(err)

    if vlanid is not None:
        cfg_list.append("interface " + intid + "." + str(vlanid))
        cfg_list.append(" encapsulation dot1q "+ str(vlanid))
    else:
        cfg_list.append("interface " + intid )

    cfg_list.append(" ip address " + str(varip.network_address+1) + " " + str(varip.netmask))
    cfg_list.append(" description " + desc)
    cfg_list.append(" no ip redirects")
    cfg_list.append(" no ip unreachables")
    cfg_list.append(" no ip proxy-arp")

    return cfg_list


def cfglist_to_json(cfg_list):
    """ configuration in list to the JSON format
    """

    try:
        out_json = json.dumps({"genconfig": cfg_list})
    except Exception as err:
        return "Error: " + str(err)

    return out_json


def in_json_trigger(injson = '{"desc": "none"}'):
    """ API input as JSON
    output the Cisco configuration
    """
    
    # Verify if the input string is in valid JSON format
    # print(type(injson), injson)
    try:
        if type(injson) == str:
            in_json = json.loads(injson)
        else:
            in_json = injson

        #print(type(in_json))
        # intid = in_json['intid'] if in_json['intid'] else intid = default_intid
    except Exception as err:
        return "Error: " + str(err)

    # verify if interface ID is set
    try:    
        intid = in_json['intid']
    except Exception as err:
        intid = default_intid


    # verify if subnet is given
    try:
        subnet = in_json['subnet']
    except KeyError as err:
        subnet = default_subnet


    # verify if interface description is given
    try:
        desc = in_json['desc']
    except KeyError as err:
        desc = default_description

    # verify if vlan ID is set
    try:
        vlanid = in_json['vlanid']
    except KeyError as err:
        vlanid = None
    
    # generate interface configuration as list
    cfg_list = cisco_intcfg(intid=intid, vlanid=vlanid, subnet=subnet, desc=desc)
    #print(cfg_list)
    # convert the above list to JSON
    cfg_out = cfglist_to_json(cfg_list)
    
    # return configuration as JSON list in the format {"genconfig": [cfg_list]}
    return cfg_out


if __name__ == "__main__":
    print(version())
    print(cisco_intcfg())
    print(cfglist_to_json(cisco_intcfg()))
    
    eg_intdict = '''
    {
        "intid": "GigabitEthernet 0/2",
        "vlanid": 3
    }
    '''
    #print(in_json_trigger(eg_intdict))
    print(in_json_trigger())