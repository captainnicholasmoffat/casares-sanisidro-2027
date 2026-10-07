import sys, xml.etree.ElementTree as ET, math
f=sys.argv[1]
r=ET.parse(f).getroot()
nodes={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.iter('node')}
def tags(e): return {t.get('k'):t.get('v') for t in e.findall('tag')}
keys=('waterway','natural','water','bridge','man_made','leisure','name','landuse','place','harbour','seamark:type','coastline','highway')
for w in r.iter('way'):
    t=tags(w)
    interesting = any(k in t for k in ('waterway','natural','water','man_made','harbour','leisure','bridge')) or ('name' in t and any(s in t['name'] for s in ('Gauto','Dárs','Dars','Perú','Orientales','Reserva','Ribera','Puerto','Náutico','Nautico')))
    if not interesting: continue
    nd=[n.get('ref') for n in w.findall('nd')]
    pts=[nodes[i] for i in nd if i in nodes]
    if not pts: continue
    lat=sum(p[0] for p in pts)/len(pts); lon=sum(p[1] for p in pts)/len(pts)
    L=0
    for a,b in zip(pts,pts[1:]):
        dy=(b[0]-a[0])*111320; dx=(b[1]-a[1])*111320*math.cos(math.radians(a[0])); L+=math.hypot(dx,dy)
    print(w.get('id'), f"n={len(pts)} L={L:.0f}m c=({lat:.6f},{lon:.6f})", {k:v for k,v in t.items() if not k.startswith('source')})
for rel in r.iter('relation'):
    t=tags(rel)
    if any(k in t for k in ('waterway','natural','water','harbour','leisure')): print('REL',rel.get('id'),t)
