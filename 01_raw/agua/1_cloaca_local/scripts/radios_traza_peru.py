# Radios censales 2022 de San Isidro atravesados por (o a menos de 300 m de) la traza OSM del "Desagüe Dardo Rocha"
# (way 1503479052). OJO: la traza NO es la cuenca. Es sólo el recorrido del conducto según OSM (no oficial).
import json, csv, urllib.request, xml.etree.ElementTree as ET
from shapely.geometry import shape, LineString
from shapely.ops import transform
import math
t=ET.fromstring(urllib.request.urlopen(urllib.request.Request('https://api.openstreetmap.org/api/0.6/way/1503479052/full',headers={'User-Agent':'research-sanisidro/1.0'})).read())
nodes={n.get('id'):(float(n.get('lon')),float(n.get('lat'))) for n in t.findall('node')}
w=t.find('way'); line=LineString([nodes[x.get('ref')] for x in w.findall('nd')])
k=math.cos(math.radians(34.48))
proj=lambda x,y,z=None:(x*111320*k,y*110574)
L=transform(proj,line)
print('longitud traza OSM (m):',round(L.length))
g=json.load(open('/home/user/casares-sanisidro-2027/data/radios_censales_sanisidro.geojson'))
cen={r['radio_id']:r for r in csv.DictReader(open('../censo2022_cloaca_por_radio_sanisidro.csv'))}
out=[]
for f in g['features']:
    rid=f['properties']['radio_id']; P=transform(proj,shape(f['geometry']))
    d=P.distance(L)
    if d<=300:
        r=cen.get(rid,{})
        out.append((rid,r.get('zona'),round(d),int(r.get('hogares') or 0),int(r.get('red_publica') or 0),r.get('pct_red')))
out.sort(key=lambda x:x[2])
H=sum(o[3] for o in out); R=sum(o[4] for o in out)
print('radios a <=300 m de la traza:',len(out),'hogares',H,'con red',R,'pct',round(100*R/H,2),'sin red',H-R)
for o in sorted(out,key=lambda o: float(o[5] or 999))[:12]: print(o)
json.dump(out,open('radios_traza_peru.json','w'))
