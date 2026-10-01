# Transacciones SUBE de un día hábil promedio (oct-2025) en hexágonos H3 res. 8 cuyo centro cae en la zona costera
# (entre vías del Tren de la Costa y el río) o a <300 m. Dataset oficial "operaciones-sube-hexagonos". [cálculo propio]
import csv, sys, collections, h3
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/scripts')
import tramos as T
from shapely.geometry import Point, Polygon
from shapely.ops import transform
from pyproj import Transformer
tr=Transformer.from_crs(4326,32721,always_xy=True)
Z,zc=T.zona(); zcm=transform(tr.transform,zc)
agg=collections.defaultdict(lambda: collections.Counter()); cache={}
for r in csv.DictReader(open(T.B+'../sube/trx2025_hexagonos_dia_habil_oct2025.csv')):
    hid=r['id_h3']
    if hid not in cache:
        lat,lon=h3.cell_to_latlng(hid)
        if not (-34.51<lat<-34.43 and -58.55<lon<-58.46): cache[hid]=None; continue
        poly=Polygon([(b,a) for a,b in h3.cell_to_boundary(hid)])
        inter=transform(tr.transform,poly).intersection(zcm).area/transform(tr.transform,poly).area
        cache[hid]=(lat,lon,inter)
    if cache[hid] and cache[hid][2]>0.25: agg[hid][r['modo']]+=int(r['cantidad_trx'])
tot=collections.Counter()
rows=[]
for hid,c in agg.items():
    lat,lon,f=cache[hid]
    p=Point(lon,lat)
    tn='?'
    for n,t in [('Martínez','1 Martínez'),('Acassuso','2 Acassuso'),('San Isidro','3 Bajo de San Isidro'),('Béccar','4 Béccar')]:
        if Z['loc'][n].contains(p): tn=t
    if tn=='2 Acassuso' and T.s(lon,lat)>T.RSP: tn='3 Bajo de San Isidro'
    rows.append((tn,hid,round(lat,5),round(lon,5),round(f,2),dict(c)))
    tot[(tn,'COLECTIVO')]+=c.get('COLECTIVO',0); tot[(tn,'TREN')]+=c.get('TREN',0)
with open(T.B+'../sube_hexagonos_zona_costera.csv','w',newline='') as fo:
    w=csv.writer(fo); w.writerow(['tramo','id_h3','lat','lon','fraccion_en_zona','colectivo','tren','subte'])
    for r in sorted(rows): w.writerow([r[0],r[1],r[2],r[3],r[4],r[5].get('COLECTIVO',0),r[5].get('TREN',0),r[5].get('SUBTE',0)])
for r in sorted(rows): print(r)
print(dict(tot))
