# Largo de calles públicas dentro de la zona costera, por tramo (OSM, no oficial) [cálculo propio]
# Cota superior teórica de lugares en cordón = largo x 2 lados / 6 m por auto (sin descontar esquinas, garajes, prohibiciones).
import pickle, sys, collections
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/scripts')
import tramos as T
from shapely.geometry import LineString, Point
from shapely.ops import transform
from pyproj import Transformer
tr=Transformer.from_crs(4326,32721,always_xy=True)
N,W,R=pickle.load(open(T.B+'tiles_all.pkl','rb'))
Z,zc=T.zona()
tipos={'primary','secondary','tertiary','residential','unclassified','living_street'}
L=collections.defaultdict(float); Lpriv=collections.defaultdict(float); calles=collections.defaultdict(set)
def tramo_of(p):
    for n,tn in [('Martínez','1 Martínez'),('Acassuso','2 Acassuso'),('San Isidro','3 Bajo de San Isidro'),('Béccar','4 Béccar')]:
        if Z['loc'][n].contains(p):
            if n=='Acassuso' and T.s(p.x,p.y)>T.RSP: return '3 Bajo de San Isidro'
            return tn
    return '?'
for wid,(nds,t,ts) in W.items():
    if t.get('highway') not in tipos: continue
    pts=[N[n][:2] for n in nds if n in N]
    if len(pts)<2: continue
    g=LineString(pts)
    if not g.intersects(zc): continue
    gi=g.intersection(zc)
    segs=[gi] if gi.geom_type=='LineString' else [x for x in getattr(gi,'geoms',[]) if x.geom_type=='LineString']
    for sg in segs:
        tn=tramo_of(sg.interpolate(0.5,normalized=True))
        ln=transform(tr.transform,sg).length
        if t.get('access') in ('private','no','destination') : Lpriv[tn]+=ln
        else: L[tn]+=ln; calles[tn].add(t.get('name','(sin nombre)'))
print('tramo | km calles públicas | km acceso privado/restringido | cota teórica autos en cordón (2 lados/6 m)')
for k in sorted(L):
    print(k,'|',round(L[k]/1000,2),'|',round(Lpriv[k]/1000,2),'|',round(L[k]*2/6))
print('TOTAL',round(sum(L.values())/1000,2),round(sum(Lpriv.values())/1000,2),round(sum(L.values())*2/6))
for k in sorted(calles): print(k, sorted(calles[k])[:40])
