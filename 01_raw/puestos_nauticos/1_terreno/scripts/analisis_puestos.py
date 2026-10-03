# Análisis por puesto [cálculo propio]. Entradas: OSM API 0.6 (ODbL, bajado 2026-10-03), ARBA WFS idera:Parcela (2026-10-03),
# radios Censo 2022 (data/ del repo, solo lectura), Copernicus GLO-30 DSM (recorte). Salida: CSV/JSON en ../calculos/
import sys, json, csv, math
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
from shapely.geometry import shape, LineString, Point
from shapely.ops import nearest_points, unary_union
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/'
REPO='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/'
CONV=set(l.split(',')[1] for l in open(REPO+'01_raw/costa_viva/1_tenencia_y_canon/CALCULO_PROPIO_superficie_15_parcelas_AnexoI.csv').read().splitlines()[1:16])
CONVITEM={l.split(',')[1]:l.split(',')[0] for l in open(REPO+'01_raw/costa_viva/1_tenencia_y_canon/CALCULO_PROPIO_superficie_15_parcelas_AnexoI.csv').read().splitlines()[1:16]}
ALL=[D+f'osm/osmapi_{s}.osm' for s in ('1_aguila','2_saenzpena','3_centenera','4_puerto','5_33orientales','6_pacheco')]+[D+f'osm/osmapi_rel_{r}_full.osm' for r in (3623442,6603491,10343663,19648933,10343661)]
N,W,R=load(ALL)
SITES=[
 dict(id='1_aguila',nombre='Parque del Águila (Martínez/Acassuso)',anchor=('way','682693239'),anchor_desc='playón público del Parque Águila Chico (OSM way 682693239)',agua=['rio'],alt=[('El Águila (edificio, Elcano 1301)',-34.47568,-58.48669)]),
 dict(id='2_saenzpena',nombre='Roque Sáenz Peña y el río',anchor=('way','139486214'),anchor_desc='rotonda final de Roque Sáenz Peña (OSM way 139486214)',agua=['rio','darsena_barrancas'],alt=[('Muelle Público (OSM way 682107625, amenity=ferry_terminal)',-34.4643,-58.4964)]),
 dict(id='3_centenera',nombre='Final de Del Barco Centenera',anchor=('node_end','208358260'),anchor_desc='extremo NE de Del Barco Centenera (OSM way 208358260)',agua=['rio','darsena']),
 dict(id='4_puerto',nombre='Dársena del Puerto de San Isidro',anchor=('pt',(-34.46140,-58.50712)),anchor_desc='rotonda Av. Mitre / Primera Junta (cabecera "Puerto de San Isidro")',agua=['darsena']),
 dict(id='5_33orientales',nombre='Paseo 33 Orientales',anchor=('node','1628455605'),anchor_desc='bajada (leisure=slipway, OSM node 1628455605) al final de Treinta y Tres Orientales',agua=['darsena']),
 dict(id='6_pacheco',nombre='General Pacheco y el río',anchor=('pt',(-34.48515,-58.48129)),anchor_desc='final de General Pacheco en Sebastián Elcano / Juan Díaz de Solís (nodo de OSM way 4662576)',agua=['rio'],alt=[('raíz del Espigón de Martínez (OSM node 4580715561)',-34.48436,-58.47958)]),
]
# agua
rio_lines=[way_geom(N,W[ref],area_ok=False) for typ,ref,role in R['3474227']['mem'] if typ=='way' and ref in W] if '3474227' in R else []
rio=unary_union([g for g in rio_lines if g is not None])
dars=rel_geom(N,W,R['3623442'])
AGUA={'rio':rio,'darsena':dars.boundary,'darsena_barrancas':rel_geom(N,W,R['10343661']).boundary}
def anchor_point(s):
    k,v=s['anchor']
    if k=='way': return way_geom(N,W[v]).centroid
    if k=='node': n=N[v]; return Point(*T.transform(n['lon'],n['lat']))
    if k=='node_end':
        w=W[v]; a=xy(N,w['nds'][0]); b=xy(N,w['nds'][-1]); return Point(*b)
    if k=='pt': return pt(*v)
PUB=('residential','tertiary','secondary','primary','unclassified','living_street','service','trunk')
roads=[]
for wid,w in W.items():
    t=w['tags']; h=t.get('highway')
    if h in PUB and t.get('access') not in ('private','no') and t.get('area')!='yes':
        g=way_geom(N,w,area_ok=False)
        if g is not None: roads.append((wid,t,g))
cyc=[(wid,w['tags'],way_geom(N,w,area_ok=False)) for wid,w in W.items() if w['tags'].get('highway')=='cycleway' or (w['tags'].get('highway') in ('footway','path') and w['tags'].get('bicycle') in ('yes','designated'))]
parks=[]
for wid,w in W.items():
    t=w['tags']
    if t.get('leisure') in ('park','nature_reserve') or t.get('boundary')=='protected_area' or t.get('landuse') in ('recreation_ground',):
        g=way_geom(N,w)
        if g is not None and g.geom_type in('Polygon','MultiPolygon'): parks.append(('way/'+wid,t,g))
for rid,r in R.items():
    t=r['tags']
    if t.get('leisure') in ('park','nature_reserve','marina') or t.get('boundary')=='protected_area' or t.get('landuse') in ('recreation_ground',):
        g=rel_geom(N,W,r)
        if g is not None and g.geom_type in('Polygon','MultiPolygon'): parks.append(('rel/'+rid,t,g))
parkings=[]
for wid,w in W.items():
    t=w['tags']
    if t.get('amenity')=='parking':
        g=way_geom(N,w)
        if g is not None and g.geom_type=='Polygon': parkings.append((wid,t,g))
pois=[]
for nid,n in N.items():
    t=n['tags']
    if t: pois.append(('node/'+nid,t,Point(*T.transform(n['lon'],n['lat']))))
for wid,w in W.items():
    t=w['tags']
    if t and ('amenity' in t or 'club' in t or 'leisure' in t or 'man_made' in t or (t.get('landuse')=='recreation_ground' and 'name' in t)):
        g=way_geom(N,w)
        if g is not None: pois.append(('way/'+wid,t,g))
# ARBA
parc=[]
for s in SITES:
    A=json.load(open(D+f"arba/arba_Parcela_{s['id']}.json"))
    for f in A['features']:
        parc.append((f['properties'],transform(lambda x,y,z=None:T.transform(x,y),shape(f['geometry']))))
seen=set(); parc2=[]
for p,g in parc:
    if p['cca'] in seen: continue
    seen.add(p['cca']); parc2.append((p,g))
parc=parc2; PU=unary_union([g for p,g in parc])
def parcela_en(P):
    for p,g in parc:
        if g.contains(P): return p['cca']+(' [CONVENIO Res.138/2026 ítem %s]'%CONVITEM[p['cca']] if p['cca'] in CONV else '')+f" ({round(p['ara1'])} m2)"
    d=PU.distance(P); return f'fuera de parcela ARBA (vía pública/sin parcelar); parcela más cercana a {d:.1f} m'
def ancho_lm(g,P,maxd=60):
    # ancho entre parcelas perpendicular a la calle en el punto de la calle más cercano a P
    d=g.project(P); d0=max(0.5,min(g.length-0.5,d))
    a=g.interpolate(d0-0.5); b=g.interpolate(d0+0.5); c=g.interpolate(d0)
    dx,dy=b.x-a.x,b.y-a.y; L=math.hypot(dx,dy); nx,ny=-dy/L,dx/L
    line=LineString([(c.x-nx*maxd,c.y-ny*maxd),(c.x+nx*maxd,c.y+ny*maxd)])
    free=line.difference(PU)
    segs=[free] if free.geom_type=='LineString' else list(getattr(free,'geoms',[]))
    for sg in segs:
        if sg.distance(c)<0.5:
            ends=[Point(sg.coords[0]),Point(sg.coords[-1])]
            abierto=any(e.distance(Point(line.coords[0]))<0.5 or e.distance(Point(line.coords[-1]))<0.5 for e in ends)
            return round(sg.length,1),abierto,ll(c)
    return None,None,ll(c)
# censo
rad=json.load(open(REPO+'data/radios_censales_sanisidro.geojson'))
cen={r['radio_id']:r for r in csv.DictReader(open(REPO+'data/censo2022_sanisidro_por_radio.csv',encoding='utf-8-sig'))}
radg=[(f['properties']['radio_id'],transform(lambda x,y,z=None:T.transform(x,y),shape(f['geometry']))) for f in rad['features']]
def iv(r,k):
    try: return int(float(r.get(k) or 0))
    except: return 0
def censo(P,buf=300):
    out=[]
    for rid,g in radg:
        d=g.distance(P)
        if d<=buf:
            r=cen.get(rid,{})
            ht=iv(r,'hogares_agua__total'); ha=iv(r,'hogares_agua__red_publica_agua_corriente'); dt=iv(r,'hogares_desague__total'); dc=iv(r,'hogares_desague__a_red_publica_cloaca')
            out.append(dict(radio=rid,dist_m=round(d),hogares=dt,pct_agua_red=round(100*ha/ht,1) if ht else None,pct_cloaca_red=round(100*dc/dt,1) if dt else None))
    return sorted(out,key=lambda x:x['dist_m'])
def cota(P): return None
RES={}
for s in SITES:
    A=anchor_point(s); r=dict(sitio=s['id'],nombre=s['nombre'],anchor=s['anchor_desc'],anchor_ll=ll(A))
    # punto náutico: punto de agua relevante más cercano al anchor
    best=None
    for k in s['agua']:
        g=AGUA[k]; q=nearest_points(A,g)[1]; d=A.distance(g)
        r[f'dist_anchor_a_{k}_m']=round(d)
        if best is None or d<best[0]: best=(d,k,q)
    NP=best[2]; r['punto_nautico_ll']=ll(NP); r['punto_nautico_tipo']=best[1]
    if s['id']=='5_33orientales': NP=A; r['punto_nautico_ll']=ll(A); r['punto_nautico_tipo']='slipway OSM'
    r['parcela_ARBA_punto_nautico']=parcela_en(NP); r['parcela_ARBA_anchor']=parcela_en(A)
    # calles públicas cercanas al punto náutico
    cs=[]
    for wid,t,g in roads:
        d=g.distance(NP)
        if d<=250: cs.append((round(d),wid,t,g))
    cs.sort(key=lambda x:x[0])
    r['calles']=[]
    usados=set()
    for d,wid,t,g in cs:
        key=t.get('name') or wid
        if key in usados and len(r['calles'])>=1: continue
        usados.add(key)
        an,ab,cll=ancho_lm(g,NP)
        r['calles'].append(dict(dist_m=d,osm='way/'+wid,nombre=t.get('name','(sin nombre)'),highway=t.get('highway'),service=t.get('service',''),superficie=t.get('surface',''),carriles=t.get('lanes',''),sentido_unico=t.get('oneway',''),vel_max=t.get('maxspeed',''),ancho_tag=t.get('width',''),estacionamiento_tags={k:v for k,v in t.items() if k.startswith('parking')},ancho_entre_parcelas_m=an,sin_parcela_de_un_lado=ab,punto_medicion=cll))
        if len(r['calles'])>=6: break
    # playones
    r['playones']=[]
    for wid,t,g in parkings:
        d=g.distance(NP)
        if d<=450: r['playones'].append(dict(dist_borde_m=round(d),osm='way/'+wid,nombre=t.get('name',''),sup_m2=round(g.area),autos_aprox_25m2=round(g.area/25),acceso=t.get('access',''),cobro=t.get('fee',''),superficie=t.get('surface',''),tipo=t.get('parking',''),capacidad_tag=t.get('capacity',''),parcela=parcela_en(g.centroid)))
    r['playones'].sort(key=lambda x:x['dist_borde_m'])
    # ciclovías
    r['ciclovias_50m']=sorted([dict(dist_m=round(g.distance(NP)),osm='way/'+wid,tipo=t.get('highway'),nombre=t.get('name','')) for wid,t,g in cyc if g is not None and g.distance(NP)<=60],key=lambda x:x['dist_m'])
    # parques
    r['espacios_que_contienen_o_lindan_10m']=[dict(osm=i,dist_m=round(g.distance(NP)),tags={k:v for k,v in t.items() if k in('name','leisure','landuse','boundary','protect_class','protection_title','operator','alt_name')}) for i,t,g in parks if g.distance(NP)<=10]
    rn=[g for i,t,g in parks if i=='rel/10343663']
    if rn: r['dist_reserva_ribera_norte_m']=round(rn[0].distance(NP))
    # servicios
    r['banos_agua_1200m']=sorted([dict(dist_m=round(g.distance(NP)),osm=i,tags={k:v for k,v in t.items() if k in('amenity','access','toilets:disposal','toilets:type','unisex','wheelchair','fee','name')}) for i,t,g in pois if t.get('amenity') in('toilets','drinking_water','shower','water_point') and g.distance(NP)<=1200],key=lambda x:x['dist_m'])
    r['locales_clubes_300m']=sorted([dict(dist_m=round(g.distance(NP)),osm=i,nombre=t.get('name',''),tipo=t.get('amenity') or t.get('club') or t.get('leisure')) for i,t,g in pois if (t.get('amenity') in('restaurant','cafe','bar','fast_food','events_venue','pub','ice_cream','nightclub') or t.get('club') or t.get('leisure') in('marina','sports_centre') or (t.get('landuse')=='recreation_ground' and 'name' in t)) and g.distance(NP)<=300],key=lambda x:x['dist_m'])
    r['infra_hidraulica_2500m']=sorted([dict(dist_m=round(g.distance(NP)),osm=i,tags=t) for i,t,g in pois if t.get('man_made') in('pumping_station','water_tower','wastewater_plant','water_works','storage_tank','reservoir_covered','pipeline','manhole') or 'pumping_station' in t or t.get('pipeline') or 'substance' in t],key=lambda x:x['dist_m'])[:8]
    r['censo_radios_300m_anchor']=censo(A)
    if 'alt' in s:
        r['alternativos']=[]
        for nm,la,lo in s['alt']:
            Q=pt(la,lo); r['alternativos'].append(dict(nombre=nm,ll=(la,lo),dist_a_rio_m=round(Q.distance(rio)),dist_a_punto_nautico_m=round(Q.distance(NP)),parcela=parcela_en(Q)))
    RES[s['id']]=r
json.dump(RES,open(D+'calculos/CALCULO_PROPIO_puestos_terreno.json','w'),ensure_ascii=False,indent=1)
for k,r in RES.items():
    print('=========',k,r['nombre']); 
    for kk,v in r.items():
        if isinstance(v,list):
            print(' ',kk)
            for x in v: print('    ',x)
        else: print(' ',kk,':',v)
