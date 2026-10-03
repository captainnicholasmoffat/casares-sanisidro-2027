import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
site=sys.argv[1]; lat=float(sys.argv[2]); lon=float(sys.argv[3]); R0=float(sys.argv[4])
N,W,R=load([f'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/osm/osmapi_{site}.osm'])
P=pt(lat,lon)
rows=[]
for wid,w in W.items():
    t=w['tags']
    if 'highway' not in t: continue
    g=way_geom(N,w,area_ok=False)
    if g is None: continue
    d=g.distance(P)
    if d>R0: continue
    a=ll(Point(g.coords[0])); b=ll(Point(g.coords[-1]))
    rows.append((d,wid,round(g.length),a,b,{k:v for k,v in t.items() if not k.startswith('source') and k not in('tiger:cfcc',)},w['ts']))
for r in sorted(rows): print(f'{r[0]:5.0f} m way/{r[1]} L={r[2]} m {r[3]}->{r[4]} {r[6][:10]} {r[5]}')
