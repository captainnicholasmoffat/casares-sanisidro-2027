# Ancho de la vía pública entre líneas de parcelas ARBA (L.M. a L.M.), medido en perpendicular cada 10 m a lo largo
# de un tramo de calle de OSM, evitando cruces. [cálculo propio]. Si de un lado no hay parcela hasta 60 m se informa
# la distancia del eje a la parcela del otro lado y al borde de agua (OSM) si corresponde.
import sys, json, math, statistics, csv
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
from shapely.geometry import shape, LineString, Point
from shapely.ops import unary_union, linemerge
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/'
ALL=[D+f'osm/osmapi_{s}.osm' for s in ('1_aguila','2_saenzpena','3_centenera','4_puerto','5_33orientales','6_pacheco')]+[D+'osm/osmapi_rel_3623442_full.osm']
N,W,R=load(ALL)
parc={}
for s in ('1_aguila','2_saenzpena','3_centenera','4_puerto','5_33orientales','6_pacheco'):
    for f in json.load(open(D+f'arba/arba_Parcela_{s}.json'))['features']:
        parc[f['properties']['cca']]=transform(lambda x,y,z=None:T.transform(x,y),shape(f['geometry']))
PU=unary_union(list(parc.values()))
dars=rel_geom(N,W,R['3623442'])
rio=unary_union([way_geom(N,W[ref],area_ok=False) for typ,ref,role in R['3474227']['mem'] if typ=='way' and ref in W]) if '3474227' in R else None
TRAMOS=[ # sitio, descripción, way ids (en orden), desde_m, hasta_m medidos desde el extremo indicado ('ini' o 'fin' del primer way)
 ('1_aguila','Sebastián Elcano frente al Águila (±150 m del club)',['462708069'],None,None,(-34.47568,-58.48669),150),
 ('2_saenzpena','Roque Sáenz Peña, último tramo antes de la rotonda (doble mano separada)',['434820824'],None,None,(-34.46383,-58.49744),200),
 ('2_saenzpena','Roque Sáenz Peña, calzada mano contraria',['955363909'],None,None,(-34.46383,-58.49744),200),
 ('3_centenera','Del Barco Centenera, último tramo',['208358260'],None,None,(-34.46287,-58.5015),200),
 ('3_centenera','Stella Maris (hacia el río)',['133213059'],None,None,(-34.46151,-58.49982),250),
 ('4_puerto','Avenida Mitre, último tramo al puerto',['303901564'],None,None,(-34.4614,-58.50712),150),
 ('4_puerto','Primera Junta, último tramo',['22663996'],None,None,(-34.4614,-58.50712),150),
 ('5_33orientales','Treinta y Tres Orientales, último tramo junto al canal',['1240325350'],None,None,(-34.45033,-58.51673),250),
 ('6_pacheco','General Pacheco, últimos 150 m',['255861798'],None,None,(-34.48515,-58.48129),150),
 ('6_pacheco','Sebastián Elcano al norte de Pacheco (150 m)',['1331096648'],None,None,(-34.48515,-58.48129),150),
 ('6_pacheco','Juan Díaz de Solís al sur de Pacheco (150 m)',['970643939'],None,None,(-34.48515,-58.48129),150),
]
def corte(g,d,maxd=60):
    a=g.interpolate(max(0,d-1)); b=g.interpolate(min(g.length,d+1)); c=g.interpolate(d)
    dx,dy=b.x-a.x,b.y-a.y; L=math.hypot(dx,dy); nx,ny=-dy/L,dx/L
    izq=LineString([(c.x,c.y),(c.x+nx*maxd,c.y+ny*maxd)]); der=LineString([(c.x,c.y),(c.x-nx*maxd,c.y-ny*maxd)])
    def hasta(lado,obj):
        x=lado.intersection(obj)
        if x.is_empty: return None
        return round(min(Point(c.x,c.y).distance(p) for p in ([x] if x.geom_type=='Point' else [Point(q) for gg in getattr(x,'geoms',[x]) for q in gg.coords])),1)
    out={}
    for nombre,lado in (('izq',izq),('der',der)):
        out[nombre]=dict(parcela=hasta(lado,PU.boundary if not PU.contains(Point(c.x,c.y)) else PU.boundary),darsena=hasta(lado,dars.boundary),rio=hasta(lado,rio) if rio is not None else None)
    return c,out
rows=[]
for sitio,desc,ways,_,_,ref,lim in TRAMOS:
    g=way_geom(N,W[ways[0]],area_ok=False); P=pt(*ref)
    dref=g.project(P)
    for d in range(5,int(g.length)-4,10):
        if abs(d-dref)>lim: continue
        c,o=corte(g,d)
        if PU.contains(c): continue
        pi,pd=o['izq']['parcela'],o['der']['parcela']
        ancho=round(pi+pd,1) if pi is not None and pd is not None else None
        lat,lon=ll(c)
        rows.append(dict(sitio=sitio,tramo=desc,osm_way=ways[0],dist_al_punto_ref_m=round(abs(d-dref)),lat=lat,lon=lon,ancho_LM_LM_m=ancho,eje_a_parcela_izq_m=pi,eje_a_parcela_der_m=pd,eje_a_darsena_izq=o['izq']['darsena'],eje_a_darsena_der=o['der']['darsena'],eje_a_rio_izq=o['izq']['rio'],eje_a_rio_der=o['der']['rio']))
with open(D+'calculos/CALCULO_PROPIO_anchos_via_publica_ARBA.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
G=collections.defaultdict(list)
for r in rows: G[(r['sitio'],r['tramo'])].append(r)
for k,v in G.items():
    an=[r['ancho_LM_LM_m'] for r in v if r['ancho_LM_LM_m'] is not None]
    print(k, 'n=',len(v),'anchos L.M.-L.M. (m):', (min(an),statistics.median(an),max(an)) if an else 'sin parcelas a ambos lados')
    if not an or len(an)<len(v):
        for r in v[:12]: print('    ',{x:r[x] for x in ('dist_al_punto_ref_m','ancho_LM_LM_m','eje_a_parcela_izq_m','eje_a_parcela_der_m','eje_a_darsena_izq','eje_a_darsena_der','eje_a_rio_izq','eje_a_rio_der')})
