import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
f=sys.argv[1]; lat=float(sys.argv[2]); lon=float(sys.argv[3]); R0=float(sys.argv[4]) if len(sys.argv)>4 else 500
N,W,R=load([f]); P=pt(lat,lon)
KEYS=('leisure','man_made','amenity','natural','waterway','landuse','boundary','club','sport','tourism','harbour','seamark:type','building','shop','highway','barrier','flood_prone','water')
out=[]
for nid,n in N.items():
    if n['tags'] and any(k in n['tags'] for k in KEYS):
        g=Point(*T.transform(n['lon'],n['lat'])); d=g.distance(P)
        if d<=R0: out.append((d,'node',nid,ll(g),0,n['tags']))
for wid,w in W.items():
    t=w['tags']
    if not t or not any(k in t for k in KEYS): continue
    if 'building' in t and len(t)<=2 and 'name' not in t: continue
    g=way_geom(N,w)
    if g is None: continue
    d=g.distance(P)
    if d<=R0: out.append((d,'way',wid,ll(g),round(g.area) if g.geom_type in('Polygon','MultiPolygon') else round(g.length),t))
for rid,r in R.items():
    t=r['tags']
    if t.get('type') in ('multipolygon','boundary') and any(k in t for k in KEYS):
        g=rel_geom(N,W,r)
        if g is None: continue
        d=g.distance(P)
        if d<=R0: out.append((d,'rel',rid,ll(g),round(g.area) if g.geom_type in('Polygon','MultiPolygon') else round(g.length),t))
flt=sys.argv[5] if len(sys.argv)>5 else None
import re
for d,typ,i,c,a,t in sorted(out,key=lambda x:x[0]):
    s=' '.join(f'{k}={v}' for k,v in t.items() if not k.startswith('source') and k not in('note',))
    if flt and not re.search(flt,s): continue
    print(f'{d:6.0f} m | {typ}/{i} | {c} | {a} | {s[:220]}')
