# Cuenta estacionamientos mapeados en OpenStreetMap (NO es dato oficial) en la zona costera
# (parte del partido entre las vías del Tren de la Costa y el río), por tramo.
# Capacidad: etiqueta capacity si existe; si no, estimación = superficie / 25 m² por auto (rango 20-30 m²) [cálculo propio].
import json, pickle, csv, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/scripts')
import tramos as T
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import transform
from pyproj import Transformer
B=T.B
tr=Transformer.from_crs(4326,32721,always_xy=True)
Z,zc=T.zona(); zcm=transform(tr.transform,zc); c=T.cortes()
d=json.load(open(B+'parking_geom.json'))
rows=[]
def loc_of(p):
    for n in ['Martínez','Acassuso','San Isidro','Béccar']:
        if Z['loc'][n].contains(p): return n
    return '?'
for e in d['elements']:
    t=e.get('tags',{})
    if e['type']=='node':
        geom=Point(e['lon'],e['lat']); area=0
    elif e['type']=='way':
        pts=[(g['lon'],g['lat']) for g in e['geometry']]
        geom=Polygon(pts) if len(pts)>=4 and pts[0]==pts[-1] else LineString(pts)
    else:
        outs=[Polygon([(g['lon'],g['lat']) for g in m['geometry']]) for m in e.get('members',[]) if m.get('role')=='outer' and m.get('geometry') and len(m['geometry'])>=4]
        geom=outs[0] if outs else None
        if geom is None: continue
    gm=transform(tr.transform,geom)
    dist=gm.distance(zcm)
    if dist>50: continue
    area=gm.area if geom.geom_type=='Polygon' else 0
    cen=geom.centroid
    loc=loc_of(cen)
    tramo={'Martínez':'1 Martínez','Acassuso':'2 Acassuso','San Isidro':'3 Bajo de San Isidro','Béccar':'4 Béccar'}.get(loc,'?')
    if loc=='Acassuso' and T.s(cen.x,cen.y)>T.RSP: tramo='3 Bajo de San Isidro'
    cap=t.get('capacity')
    est=round(area/25) if area else None
    rows.append(dict(osm=f"{e['type']}/{e['id']}",tramo=tramo,localidad_osm=loc,dentro_zona='si' if dist==0 else f'a {round(dist)} m',
        amenity=t.get('amenity'),parking=t.get('parking'),nombre=t.get('name',''),operador=t.get('operator',''),access=t.get('access',''),fee=t.get('fee',''),
        capacity_tag=cap or '',superficie_m2=round(area),autos_est_25m2=est or '',autos_est_rango=f"{round(area/30)}-{round(area/20)}" if area else '',
        lat=round(cen.y,6),lon=round(cen.x,6)))
rows.sort(key=lambda r:(r['tramo'],-(r['superficie_m2'])))
with open(B+'../estacionamientos_osm_zona_costera.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r['tramo'],r['osm'],r['dentro_zona'],r['amenity'],r['parking'],r['nombre'],'|acc',r['access'],'|fee',r['fee'],'|cap',r['capacity_tag'],'|m2',r['superficie_m2'],'|est',r['autos_est_25m2'],r['autos_est_rango'])
print('OSM timestamp', d['osm3s']['timestamp_osm_base'])
