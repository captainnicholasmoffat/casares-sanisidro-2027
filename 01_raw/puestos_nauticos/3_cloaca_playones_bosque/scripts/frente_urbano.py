# [cálculo propio / inferencia] Proxy de "colectora más cercana probable": parcela urbana chica (ARBA, < 2.500 m2,
# no incluida en el convenio Res. 138/2026) más cercana a cada borde (playón o calle candidata). La colectora
# domiciliaria de AySA corre por la calle frente a esas parcelas; la distancia es una estimación, no un dato de AySA.
import sys, json
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from geo import *
from shapely.geometry import shape, Point
from shapely.ops import transform as T2
toU=lambda g: T2(lambda x,y,z=None: UTM.transform(x,y),g)
AR=arba_features()
P=[]
for ft in AR:
    c=ft['properties']['cca']; a=ft['properties'].get('ara1') or 0
    if c in CONVENIO: continue
    g=toU(shape(ft['geometry']))
    if g.area<2500: P.append((c,ft['properties'].get('pda'),round(g.area),g))
BORDES={
 '1_aguila playón Águila Chico':(-34.47489,-58.48772),
 '2_saenzpena playón grande':(-34.46397,-58.49703),
 '2_saenzpena rotonda/playón O':(-34.46363,-58.49792),
 '3/BA Stella Maris (punto medio)':(-34.46226,-58.50077),
 '3/BA Stella Maris (extremo río)':(-34.46164,-58.50004),
 'BA cruce DBC-Stella Maris-V.Obligado':(-34.46287,-58.50150),
 'BA lote ripio CME':(-34.46283,-58.50103),
 '4_puerto rotonda Mitre':(-34.4614,-58.50712),
 '4_puerto explanada acceso':(-34.46142,-58.50686),
 '5_33orientales final de calle':(-34.45042,-58.51683),
 '6_pacheco playón':(-34.48554,-58.48124),
}
res={}
for k,(la,lo) in BORDES.items():
    p=Point(UTM.transform(lo,la))
    best=sorted((g.distance(p),c,pd,a) for c,pd,a,g in P)[:3]
    res[k]=[dict(dist_m=round(d,1),cca=c,partida=pd,area_m2=a) for d,c,pd,a in best]
    print(k,res[k][0])
json.dump(res,open(f'{U}/calculos/CALCULO_PROPIO_frente_urbano_mas_cercano.json','w'),indent=1,ensure_ascii=False)

# --- segunda variante: parcela no-convenio con edificio (OSM building) más cercana, y si entre medio cruzan las vías
import xml.etree.ElementTree as ET, glob
from shapely.geometry import LineString, Polygon
N={};B=[];RL=[]
for f in glob.glob(f'{D1}/osm/osmapi_*.osm'):
    for e in ET.parse(f).getroot():
        if e.tag=='node': N[e.get('id')]=(float(e.get('lat')),float(e.get('lon')))
        elif e.tag=='way':
            t={x.get('k'):x.get('v') for x in e.findall('tag')}; nds=[n.get('ref') for n in e.findall('nd')]
            if 'building' in t: B.append(nds)
            if t.get('railway') in ('rail','light_rail'): RL.append(nds)
BU=[]
for nds in B:
    pts=[UTM.transform(N[n][1],N[n][0]) for n in nds if n in N]
    if len(pts)>3: BU.append(Polygon(pts).buffer(0))
RLU=[LineString([UTM.transform(N[n][1],N[n][0]) for n in nds if n in N]) for nds in RL]
NC=[(ft['properties']['cca'],toU(shape(ft['geometry']))) for ft in AR if ft['properties']['cca'] not in CONVENIO]
res2={}
for k,(la,lo) in BORDES.items():
    p=Point(UTM.transform(lo,la)); best=None
    for c,g in NC:
        if g.distance(p)>600: continue
        bs=[b for b in BU if g.intersects(b.centroid)]
        if not bs: continue
        d=g.distance(p)
        if best is None or d<best[0]: best=(d,c,round(g.area),len(bs),g)
    if best:
        q=best[4].boundary.interpolate(best[4].boundary.project(p))
        cruza=any(LineString([p,q]).intersects(r) for r in RLU)
        res2[k]=dict(dist_m=round(best[0],1),cca=best[1],area_m2=best[2],edificios_osm=best[3],cruza_vias_tren=cruza)
        print('B',k,res2[k])
json.dump(dict(parcela_chica_mas_cercana=res,parcela_con_edificio_mas_cercana=res2),open(f'{U}/calculos/CALCULO_PROPIO_frente_urbano_mas_cercano.json','w'),indent=1,ensure_ascii=False)
