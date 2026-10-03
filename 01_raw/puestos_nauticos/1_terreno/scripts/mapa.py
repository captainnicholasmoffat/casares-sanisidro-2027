# Dibuja un mapa de trabajo (OSM API 0.6 + parcelas ARBA) alrededor de un punto. Uso: mapa.py sitio lat lon radio_m salida.png
import sys, json
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
from shapely.geometry import shape
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/'
site=sys.argv[1]; lat=float(sys.argv[2]); lon=float(sys.argv[3]); rad=float(sys.argv[4]); out=sys.argv[5]
files=[D+f'osm/osmapi_{site}.osm']+[D+f'osm/osmapi_rel_{r}_full.osm' for r in (3623442,6603491,10343663,19648933,10343661)]
N,W,R=load(files); P=pt(lat,lon)
fig,ax=plt.subplots(figsize=(13,13))
def draw(g,**kw):
    if g is None: return
    if g.geom_type in('Polygon',):
        x,y=g.exterior.xy; ax.fill(x,y,**kw)
    elif g.geom_type=='MultiPolygon':
        for p in g.geoms: draw(p,**kw)
    elif g.geom_type in('LineString',):
        x,y=g.xy; ax.plot(x,y,**{k:v for k,v in kw.items() if k in('color','lw','ls','alpha','zorder')})
    elif g.geom_type in ('MultiLineString','GeometryCollection'):
        for p in g.geoms: draw(p,**kw)
# ARBA parcelas
try:
    A=json.load(open(D+f'arba/arba_Parcela_{site}.json'))
    conv=set(l.split(',')[1] for l in open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/01_raw/costa_viva/1_tenencia_y_canon/CALCULO_PROPIO_superficie_15_parcelas_AnexoI.csv').read().splitlines()[1:16])
    for f in A['features']:
        g=transform(lambda x,y,z=None:T.transform(x,y),shape(f['geometry']))
        c='orange' if f['properties']['cca'] in conv else 'none'
        for p in (g.geoms if g.geom_type=='MultiPolygon' else [g]):
            x,y=p.exterior.xy; ax.plot(x,y,color='grey',lw=0.5,zorder=1)
            if c!='none': ax.fill(x,y,color=c,alpha=0.15,zorder=0)
except Exception as e: print('arba',e)
for rid,r in R.items():
    t=r['tags']
    if t.get('natural')=='water' or t.get('leisure') in('marina',):
        g=rel_geom(N,W,r); draw(g,color='#9cc9f0',alpha=0.8,zorder=2)
    if t.get('leisure')=='park' or t.get('boundary')=='protected_area':
        g=rel_geom(N,W,r); draw(g,color='green',alpha=0.18,zorder=2)
    if rid=='3474227':
        for typ,ref,role in r['mem']:
            if typ=='way' and ref in W:
                g=way_geom(N,W[ref],area_ok=False); draw(g,color='blue',lw=2.5,zorder=6)
for wid,w in W.items():
    t=w['tags']; g=way_geom(N,w)
    if g is None or g.distance(P)>rad*1.3: continue
    if t.get('natural') in('water','beach','wetland','wood') or t.get('waterway'):
        draw(g,color={'water':'#9cc9f0','beach':'#f2e2a0','wetland':'#bfe3d0','wood':'#a8d5a2'}.get(t.get('natural'),'#5fa8e8'),alpha=0.8,zorder=2,lw=1)
    elif t.get('leisure') in('park','garden','pitch','playground','nature_reserve') or t.get('landuse') in('grass','recreation_ground'):
        draw(g,color='green',alpha=0.2,zorder=2)
    elif t.get('amenity')=='parking':
        draw(g,color='purple',alpha=0.35,zorder=3)
        c=g.centroid; ax.text(c.x,c.y,f"P {round(g.area)}m²\n{t.get('access','')}",fontsize=7,color='purple',zorder=9)
    elif 'building' in t:
        draw(g,color='#888',alpha=0.5,zorder=3)
    elif t.get('man_made') in('pier','breakwater','groyne') :
        draw(g,color='black',lw=2,zorder=5)
    elif t.get('man_made')=='embankment' or t.get('embankment')=='yes' or t.get('man_made')=='dyke':
        draw(g,color='brown',lw=3,ls='--',zorder=7)
    if 'highway' in t:
        hw=t['highway']
        sty={'cycleway':dict(color='red',lw=1.2,ls=':'),'footway':dict(color='#d55',lw=0.6,ls='--'),'path':dict(color='#d55',lw=0.6,ls='--'),'steps':dict(color='#d55',lw=0.6,ls='--'),'service':dict(color='#444',lw=1.2)}.get(hw,dict(color='black',lw=2.2))
        if t.get('access') in('private','no'): sty=dict(color='#c60',lw=2,ls='-.')
        draw(g,zorder=8,**sty)
        if 'name' in t and g.geom_type=='LineString' and g.length>40:
            m=g.interpolate(0.5,normalized=True); ax.text(m.x,m.y,t['name'][:22],fontsize=7,color='darkred',zorder=10)
for nid,n in N.items():
    t=n['tags']
    if not t: continue
    g=Point(*T.transform(n['lon'],n['lat']))
    if g.distance(P)>rad*1.3: continue
    if t.get('amenity') in('toilets','drinking_water'):
        ax.plot(g.x,g.y,'s',color='cyan' if t['amenity']=='toilets' else 'blue',ms=9,mec='k',zorder=11); ax.text(g.x,g.y,' WC' if t['amenity']=='toilets' else ' agua',fontsize=8,zorder=11)
    if t.get('leisure')=='slipway' or t.get('man_made') in('pumping_station','water_tower','wastewater_plant'):
        ax.plot(g.x,g.y,'^',color='red',ms=9,zorder=11); ax.text(g.x,g.y,' '+(t.get('leisure') or t.get('man_made')),fontsize=8,zorder=11)
    if t.get('amenity') in('restaurant','cafe','bar','fast_food','events_venue') or t.get('club'):
        ax.plot(g.x,g.y,'o',color='orange',ms=5,zorder=11); ax.text(g.x,g.y,' '+t.get('name','')[:18],fontsize=6,zorder=11)
ax.plot(P.x,P.y,'*',color='red',ms=18,zorder=12)
# franja 15 m desde la orilla OSM (art. 1974 CCyC) y polígono Dec. 910/2012
from shapely.ops import unary_union as _uu
_or=[]
if '3474227' in R:
    _or+=[way_geom(N,W[ref],area_ok=False) for typ,ref,role in R['3474227']['mem'] if typ=='way' and ref in W]
for _r in ('3623442','10343661'):
    if _r in R: _or.append(rel_geom(N,W,R[_r]).boundary)
_b=_uu([g for g in _or if g is not None]).buffer(15)
draw(_b,color='red',alpha=0.12,zorder=4)
try:
    _bp=json.load(open(D+'calculos/CALCULO_PROPIO_poligono_Dec910-2012_Bosque_Alegre.geojson'))
    _g=transform(lambda x,y,z=None:T.transform(x,y),shape(_bp['geometry'])); x,y=_g.exterior.xy; ax.plot(x,y,color='darkgreen',lw=2.5,ls='--',zorder=9)
except Exception as e: print(e)
ax.set_xlim(P.x-rad,P.x+rad); ax.set_ylim(P.y-rad,P.y+rad); ax.set_aspect('equal')
# grilla cada 100 m
import numpy as np
ax.set_xticks(np.arange(P.x-rad,P.x+rad+1,100)); ax.set_yticks(np.arange(P.y-rad,P.y+rad+1,100)); ax.grid(alpha=0.3); ax.set_xticklabels([]); ax.set_yticklabels([])
ax.set_title(f'{site} estrella=punto náutico {lat},{lon} | grilla 100 m | rojo claro: 15 m desde la orilla OSM | verde punteado: Paisaje Protegido Dec. 910/2012\nOSM API 0.6 (ODbL) 2026-10-03 + ARBA WFS 2026-10-03 (naranja: parcelas del convenio Res. 138/2026) | cálculo propio, no oficial',fontsize=9)
plt.savefig(out,dpi=80,bbox_inches='tight')
