import pytest
import json
from mainapp import cisco_intcfg, cfglist_to_json, in_json_trigger

right_ip = "192.168.0.0/22"
wrong_ip = "345.234.334.234/30"

class TestClass_cfgfunc:
    def test_lenofconf(self):
        assert len(cisco_intcfg(subnet=right_ip)) == 6
        assert len(cisco_intcfg(right_ip)[1].split()) == 4
        assert len(cisco_intcfg(right_ip)[-1].split()) == 3

    def test_lenwithvlan(self):
        assert len(cisco_intcfg(subnet=right_ip, vlanid=23)) == 7
        assert len(cisco_intcfg(subnet=right_ip, vlanid=23)[1].split()) == 3
        assert len(cisco_intcfg(subnet=right_ip, vlanid=23)[2].split()) == 4

    def test_type(self):
        assert type(cisco_intcfg(subnet=right_ip)) == list
        assert type(cisco_intcfg(subnet=right_ip)[1]) == str

    def test_ipreturn(self):
        assert ("192.168.0.1" in cisco_intcfg(right_ip)[1]) == True
        assert ("255.255.252.0" in cisco_intcfg(right_ip)[1]) == True
        assert ("." not in cisco_intcfg(right_ip)[0]) == True

    def test_ipvalid(self):
        assert ("Error" in cisco_intcfg(wrong_ip)) == True

class TestClass_cfgjson:
    def test_type(self):
        testout_json = cfglist_to_json(cisco_intcfg(subnet=right_ip))
        assert type(testout_json) == str
        assert type(json.loads(testout_json)) == dict
    
    def test_ipreturn(self):
        testout_json = cfglist_to_json(cisco_intcfg(subnet=right_ip))
        assert ("192.168.0.1" in json.loads(testout_json)['genconfig'][1]) == True
        assert ("255.255.252.0" in json.loads(testout_json)['genconfig'][1]) == True
        assert ("." not in json.loads(testout_json)['genconfig'][0]) == True

        #assert type(cisco_intcfg(subnet=right_ip)[1]) == str

class TestClass_injson:
    indict_noip = '''
    {
        "intid": "GigabitEthernet 0/2",
        "vlanid": 3
    }
    '''
    def test_ipreturn(self):
        testout_json = in_json_trigger(self.indict_noip)
        assert ("159.127.0.1" in json.loads(testout_json)['genconfig'][2]) == True
        assert ("255.255.254.0" in json.loads(testout_json)['genconfig'][2]) == True
        assert ("dot1q 3" in json.loads(testout_json)['genconfig'][1]) == True
        assert ("." in json.loads(testout_json)['genconfig'][0]) == True
        assert ("Ethernet 0/2" in json.loads(testout_json)['genconfig'][0]) == True