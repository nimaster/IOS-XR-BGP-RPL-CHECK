
bla = "[OrderedDict([('neighbor-group-name', 'ISP'), ('neighbor-group-afs', OrderedDict([('neighbor-group-af', OrderedDict([('af-name', 'ipv4-unicast'), ('route-policy-in', 'BGP-IN'), ('route-policy-out', 'BGP-OUT')]))]))]), OrderedDict([('neighbor-group-name', 'IBGP'), ('neighbor-group-afs', OrderedDict([('neighbor-group-af', OrderedDict([('af-name', 'ipv4-unicast'), ('route-policy-in', 'ACCEPT-ALL'), ('route-policy-out', 'PASS')]))]))]), OrderedDict([('neighbor-group-name', 'TEST'), ('neighbor-group-afs', OrderedDict([('neighbor-group-af', OrderedDict([('af-name', 'ipv4-unicast'), ('route-policy-in', 'drop'), ('route-policy-out', 'ACCEPT-ALL')]))]))])]"

print(bla)

print(bla.count('neighbor-group-name'))

