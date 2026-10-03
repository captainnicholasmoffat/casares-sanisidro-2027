import sys, json
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
from shapely.geometry import shape
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/'
site=sys.argv[1]
pts=[(float(a.split(',')[0]),float(a.split(',')[1])) for a in sys.argv[2:]]
N,W,R=load([D+f'osm/osmapi_{site}.osm'])
A=json.load(open(D+f'arba/arba_Parcela_{site}.json'))
conv=set(l.split(',')[1] for l in open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/01_raw/costa_viva/1_tenencia_y_canon/CALCULO_PROPIO_superficie_15_parcelas_AnexoI.csv').read().splitlines()[1:16])
for lat,lon in pts:
    P=pt(lat,lon); print('== punto',lat,lon)
    for wid,w in W.items():
        t=w['tags']
        if not t or 'highway' in t: continue
        g=way_geom(N,w)
        if g is not None and g.geom_type=='Polygon' and g.contains(P): print('  OSM way',wid,round(g.area),t)
    for rid,r in R.items():
        t=r['tags']
        if t.get('type') in('multipolygon','boundary') and t.get('admin_level') is None:
            g=rel_geom(N,W,r)
            if g is not None and g.geom_type in('Polygon','MultiPolygon') and g.contains(P): print('  OSM rel',rid,round(g.area),{k:v for k,v in t.items() if not k.startswith('name:')})
    hit=False
    for f in A['features']:
        g=transform(lambda x,y,z=None:T.transform(x,y),shape(f['geometry']))
        if g.contains(P): print('  ARBA parcela',f['properties'],'CONVENIO Res138' if f['properties']['cca'] in conv else ''); hit=True
    if not hit:
        dmin=min((transform(lambda x,y,z=None:T.transform(x,y),shape(f['geometry'])).distance(P),f['properties']['cca']) for f in A['features'])
        print('  ARBA: fuera de parcelas (vía pública o sin parcela); parcela más cercana a',round(dmin[0],1),'m',dmin[1])
