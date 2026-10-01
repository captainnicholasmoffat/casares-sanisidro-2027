# Paradas de colectivo y recorridos (relaciones route=bus de OSM) que entran en la zona costera
# (entre vías del Tren de la Costa y el río) o pasan a menos de 150 m. OSM, no oficial; los recorridos de OSM
# pueden no reflejar los cambios de junio de 2026.
import pickle, sys, collections, csv
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/scripts')
import tramos as T
from shapely.geometry import Point, LineString
from shapely.ops import transform
from pyproj import Transformer
tr=Transformer.from_crs(4326,32721,always_xy=True)
N,W,R=pickle.load(open(T.B+'tiles_all.pkl','rb'))
Z,zc=T.zona(); zcm=transform(tr.transform,zc)
def tramo_of(p):
    for n,tn in [('Martínez','1 Martínez'),('Acassuso','2 Acassuso'),('San Isidro','3 Bajo de San Isidro'),('Béccar','4 Béccar')]:
        if Z['loc'][n].contains(p):
            if n=='Acassuso' and T.s(p.x,p.y)>T.RSP: return '3 Bajo de San Isidro'
            return tn
    return 'fuera'
stops={}
for nid,(x,y,t,ts) in N.items():
    if t.get('highway')=='bus_stop' or (t.get('public_transport')=='platform' and t.get('bus')=='yes'):
        p=Point(x,y); d=transform(tr.transform,p).distance(zcm)
        stops[nid]=(x,y,t.get('name',''),d,tramo_of(p))
routes=collections.defaultdict(lambda: {'stops_zona':set(),'ways_zona':0.0})
for rid,(mem,t,ts) in R.items():
    if t.get('route')!='bus': continue
    for ty,ref,role in mem:
        if ty=='node' and ref in stops and stops[ref][3]==0: routes[rid]['stops_zona'].add(ref)
        if ty=='way' and ref in W:
            pts=[N[n][:2] for n in W[ref][0] if n in N]
            if len(pts)>=2:
                g=LineString(pts)
                if g.intersects(zc): routes[rid]['ways_zona']+=transform(tr.transform,g.intersection(zc)).length
    routes[rid]['tags']=t
out=[]
for rid,v in routes.items():
    if v['stops_zona'] or v['ways_zona']>50:
        t=v['tags']; tram=sorted(set(stops[s][4] for s in v['stops_zona']))
        out.append((t.get('ref'),t.get('name'),t.get('operator'),len(v['stops_zona']),round(v['ways_zona']),tram,rid))
out.sort(key=lambda x:str(x[0]))
with open(T.B+'../colectivos_zona_costera_osm.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['ref','nombre_osm','operador_osm','paradas_en_zona','metros_de_recorrido_en_zona','tramos','relacion_osm'])
    for o in out: w.writerow(o); print(o)
zs=[(k,v) for k,v in stops.items() if v[3]==0]
print('paradas en zona:',len(zs)); 
for k,v in sorted(zs,key=lambda kv:kv[1][4]): print(k,v[4],v[2],round(v[1],5),round(v[0],5))
