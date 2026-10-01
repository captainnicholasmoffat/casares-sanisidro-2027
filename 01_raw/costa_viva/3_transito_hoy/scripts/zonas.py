# Construye: polígono del Partido de San Isidro, localidades, línea del Tren de la Costa,
# "zona costera" = parte del partido entre las vías del Tren de la Costa y el río.
# Fuente: OpenStreetMap vía Overpass (no oficial). Salida: zonas.pkl
import json, pickle
from shapely.geometry import LineString, Polygon, Point, MultiPolygon
from shapely.ops import linemerge, polygonize, unary_union, split
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/osm/'
def relpoly(e):
    outer=[LineString([(p['lon'],p['lat']) for p in m['geometry']]) for m in e['members'] if m['type']=='way' and m.get('role')=='outer']
    polys=list(polygonize(linemerge(unary_union(outer))))
    return unary_union(polys)
d=json.load(open(B+'boundary_coast.json'))
SI=[relpoly(e) for e in d['elements'] if e['type']=='relation'][0]
r=json.load(open(B+'rail_localidades.json'))
loc={}
for e in r['elements']:
    if e['type']=='relation' and e['tags'].get('admin_level')=='8':
        loc[e['tags']['name']]=relpoly(e)
tdlc=[LineString([(p['lon'],p['lat']) for p in e['geometry']]) for e in r['elements'] if e['type']=='way' and e['tags'].get('name')=='Tren de la Costa']
mitre=[LineString([(p['lon'],p['lat']) for p in e['geometry']]) for e in r['elements'] if e['type']=='way' and e['tags'].get('name') in ('FC Mitre','Mitre') and e['tags'].get('service') is None]
T=unary_union(tdlc)
# zona costera: partes de SI separadas por las vías del TdlC que tocan el borde costero (lado este/norte)
parts=split(SI, linemerge(T) if linemerge(T).geom_type=='LineString' else T)
print('partes', len(parts.geoms), sorted([round(p.area*1e6,2) for p in parts.geoms],reverse=True)[:6])
pickle.dump({'SI':SI,'loc':loc,'tdlc':T,'mitre':unary_union(mitre),'parts':list(parts.geoms)}, open(B+'zonas.pkl','wb'))
for k,v in loc.items(): print(k, round(v.area*1e6,2), v.intersects(SI))
