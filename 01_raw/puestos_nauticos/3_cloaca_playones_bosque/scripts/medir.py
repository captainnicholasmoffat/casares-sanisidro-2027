# [cálculo propio] Medición asistida de superficies abiertas sin vegetación sobre la imagen Esri (03/01/2026).
# Para cada polígono dibujado a mano (en metros locales sobre la grilla), informa: área del polígono (UTM 21S) y área de
# píxeles "sin vegetación" (ExG=2G-R-B<12, brillo>60) dentro de él, más el tono medio (para distinguir pavimento gris de tierra).
import sys, json, math
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from geo import *
import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import Polygon, Point, shape
from shapely.ops import transform as T2
_cache={}
def arrays(sitio):
    if sitio not in _cache:
        a=np.asarray(Image.open(f'{U}/imagenes/{sitio}_esri_z19.png').convert('RGB')).astype(int)
        exg=2*a[...,1]-a[...,0]-a[...,2]; bri=a.sum(-1)/3
        _cache[sitio]=(a,(exg<12)&(bri>60))
    return _cache[sitio]
AR=arba_features()
ARU=[(ft['properties']['cca'],T2(lambda x,y,z=None: UTM.transform(x,y),shape(ft['geometry']))) for ft in AR]
def pp_utm(): return Polygon([UTM.transform(lo,la) for la,lo in pp_polygon_ll()])
def medir(sitio,pts):
    I=Img(sitio); a,nv=arrays(sitio)
    area,pu=area_m2_from_m(I,pts)
    xy=[I.m2px(e,n) for e,n in pts]
    m=Image.new('L',(I.W,I.H),0); ImageDraw.Draw(m).polygon(xy,fill=1); m=np.asarray(m).astype(bool)
    pix_m2=area/m.sum() if m.sum() else 0
    nvarea=(nv&m).sum()*pix_m2
    col=a[nv&m].mean(0) if (nv&m).sum() else [0,0,0]
    # parcela ARBA que más se superpone
    best=sorted([(pu.intersection(g).area,c) for c,g in ARU if pu.intersects(g)],reverse=True)
    parc=[(c,CONVENIO.get(c),round(ar/area*100)) for ar,c in best[:3]]
    fuera=round((area-sum(ar for ar,c in best))/area*100) if area else 0
    dpp=pu.distance(pp_utm())
    c=pu.centroid; lo,la=UTM.transform(c.x,c.y,direction='INVERSE')
    return dict(area_poligono_m2=round(area),area_sin_veg_m2=round(nvarea),rgb_medio=[int(v) for v in col],parcelas_ARBA=parc,
                pct_fuera_de_parcelas=fuera,dist_PP_BosqueAlegre_m=round(dpp,1),centroide=[round(la,6),round(lo,6)])
