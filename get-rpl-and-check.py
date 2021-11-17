__author__ = "Niall Masterson"
__author_email__ = "nimaster@cisco.com"
__copyright__ = "Copyright (c) 2021 Cisco Systems, Inc."
__version__ = "1.1"

#Caveats with version 1.1
#Only checks for neighbor-groups and not neighbors
#Must be at least two neighbor-groups configured on the router


from ncclient import manager
import xmltodict
from collections import OrderedDict
import json

nc = manager.connect_ssh(host='10.225.251.6', username='cisco', password='cisco', device_params={"name": "iosxr"})

with open('rpl-bgp-peers.xml', 'r') as fp:
    payload=fp.read()

reply = nc.get(filter=('subtree', payload))

print(reply.xml)

ng = 0

rpl = xmltodict.parse(reply.xml)['rpc-reply']['data']['bgp']['instance']['instance-as']['four-byte-as']['default-vrf']['bgp-entity']['neighbor-groups']['neighbor-group']

rplstring = json.dumps(rpl)
neighborcount = rplstring.count('neighbor-group-name')
print('Number of Neighbor-Groups:', neighborcount)

while ng < neighborcount:
    peername = rpl[ng]
    rplpeer = peername['neighbor-group-afs']['neighbor-group-af']
    #rplpeerv4 = peername['neighbor-group-afs']['neighbor-group-af'][0]
    #rplpeerv6 = peername['neighbor-group-afs']['neighbor-group-af'][1]
    print('\n')
    #print(rplpeer)
    for key, value in peername.items():
        if key == 'neighbor-group-name':
            print('NEIGHBOR-GROUP:', value)
    ng+=1
    rplpeerstring = json.dumps(rplpeer)
    afcount = rplpeerstring.count('af-name')
    print('Number of address-families:', afcount)
    if afcount == 1:
        for key, value in rplpeer.items():
            if key == 'route-policy-in':
                #print(key, value)
                if value.endswith('-IN'):
                    print('  POLICY-INBOUND:', value, "-", 'IS OK')
                else:
                    print('  POLICY-INBOUND:', value, "-", 'DOES NOT CONFORM TO THE NAMING STANDARD FOR AN INBOUND RPL')
            if key == 'route-policy-out':
                #print(key, value)
                if value.endswith('-OUT'):
                    print('  POLICY-OUTBOUND:', value, "-", 'IS OK')
                else:
                    print('  POLICY-OUTBOUND:', value, "-", 'DOES NOT CONFORM TO THE NAMING STANDARD FOR AN OUTBOUND RPL')
    if afcount == 2:
        rplpeerv4 = peername['neighbor-group-afs']['neighbor-group-af'][0]
        rplpeerv6 = peername['neighbor-group-afs']['neighbor-group-af'][1]
        for key, value in rplpeerv4.items():
            if key == 'route-policy-in':
                #print(key, value)
                if value.endswith('-IN'):
                    print('  v4_POLICY-INBOUND:', value, "-", 'IS OK')
                else:
                    print('  v4_POLICY-INBOUND:', value, "-", 'DOES NOT CONFORM TO THE NAMING STANDARD FOR AN INBOUND RPL')
            if key == 'route-policy-out':
                #print(key, value)
                if value.endswith('-OUT'):
                    print('  v4_POLICY-OUTBOUND:', value, "-", 'IS OK')
                else:
                    print('  v4_POLICY-OUTBOUND:', value, "-", 'DOES NOT CONFORM TO THE NAMING STANDARD FOR AN OUTBOUND RPL')
        for key, value in rplpeerv6.items():
            if key == 'route-policy-in':
                #print(key, value)
                if value.endswith('-IN'):
                    print('  v6_POLICY-INBOUND:', value, "-", 'IS OK')
                else:
                    print('  v6_POLICY-INBOUND:', value, "-", 'DOES NOT CONFORM TO THE NAMING STANDARD FOR AN INBOUND RPL')
            if key == 'route-policy-out':
                #print(key, value)
                if value.endswith('-OUT'):
                    print('  v6_POLICY-OUTBOUND:', value, "-", 'IS OK')
                else:
                    print('  v6_POLICY-OUTBOUND:', value, "-", 'DOES NOT CONFORM TO THE NAMING STANDARD FOR AN OUTBOUND RPL')    
    if afcount > 2:
        print("NEIGHBOR-GROUP EXCEEDS THE NUMBER OF ADDRESS_FAMILIES ALLOWED")
    if afcount == 0:
        print("NO ADRESS-FAMILIES CONFIGURED FOR THIS NEIGHBOR-GROUP")
