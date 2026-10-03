# [cálculo propio] Superficie sin vegetación a lo largo de una calle (buffer del eje OSM), fuera del polígono del Paisaje
# Protegido (Dec. 910/2012) y fuera de un margen de seguridad respecto de ese polígono.
import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from medir import *
from transectas import way_ll
from shapely.geometry import LineString
import numpy as np
from PIL import Image, ImageDraw
def franja(sitio,wid,half=12,margenes=(0,3,5,10),s0=None,s1=None):
    I=Img(sitio); a,nv=arrays(sitio)
    Lm=LineString([I.ll2m(la,lo) for la,lo in way_ll(wid)])
    if s0 is not None:
        from shapely.ops import substring
        Lm=substring(Lm,s0,s1)
    buf=Lm.buffer(half,cap_style=2)
    ppm=Polygon([I.ll2m(la,lo) for la,lo in pp_polygon_ll()])
    # área por píxel en m2 (UTM) aprox: usar polígono buf
    area_buf,_=area_m2_from_m(I,list(buf.exterior.coords))
    def mask_of(geom):
        m=Image.new('L',(I.W,I.H),0); d=ImageDraw.Draw(m)
        for g in getattr(geom,'geoms',[geom]):
            if g.is_empty: continue
            d.polygon([I.m2px(e,n) for e,n in g.exterior.coords],fill=1)
            for h in g.interiors: d.polygon([I.m2px(e,n) for e,n in h.coords],fill=0)
        return np.asarray(m).astype(bool)
    mb=mask_of(buf); pxa=area_buf/mb.sum()
    out={'largo_m':round(Lm.length,1),'buffer_m':half,'area_buffer_m2':round(area_buf),'sin_veg_total_m2':round((nv&mb).sum()*pxa)}
    for mg in margenes:
        g=buf.difference(ppm.buffer(mg)) if mg>0 else buf.difference(ppm)
        mm=mask_of(g); out[f'sin_veg_fuera_PP_margen_{mg}m_m2']=round((nv&mm).sum()*pxa)
    return out
if __name__=='__main__':
    print(franja(sys.argv[1],sys.argv[2]))
