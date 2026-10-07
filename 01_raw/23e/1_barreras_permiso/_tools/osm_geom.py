import sys, xml.etree.ElementTree as ET
f=sys.argv[1]; ids=sys.argv[2:]
r=ET.parse(f).getroot()
nodes={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.iter('node')}
ways={w.get('id'):w for w in r.iter('way')}
rels={x.get('id'):x for x in r.iter('relation')}
for i in ids:
    if i.startswith('r'):
        x=rels[i[1:]]
        print('REL',i, [(m.get('type'),m.get('ref'),m.get('role')) for m in x.findall('member')])
        continue
    w=ways.get(i)
    if w is None: print(i,'missing'); continue
    nd=[n.get('ref') for n in w.findall('nd')]
    print('WAY',i,[ (n, nodes.get(n)) for n in nd])
