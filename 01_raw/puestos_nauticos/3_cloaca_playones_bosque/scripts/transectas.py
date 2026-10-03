# [cálculo propio] Ancho de superficie sin vegetación (pavimento/tierra/autos) a lo largo de una calle OSM, medido sobre la
# imagen Esri (03/01/2026) con transectas perpendiculares cada 10 m. Criterio: píxel "no vegetado" si ExG=2G-R-B < umbral y
# no es sombra muy oscura. Se mide el tramo contiguo que contiene el eje (tolerancia 1 m de huecos).
import sys, json, math, xml.etree.ElementTree as ET, glob
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from geo import *
import numpy as np
from PIL import Image
from shapely.geometry import LineString, Point
def way_ll(wid):
    N={};nds=None
    for f in glob.glob(f'{D1}/osm/osmapi_*.osm'):
        r=ET.parse(f).getroot()
        for e in r:
            if e.tag=='node': N[e.get('id')]=(float(e.get('lat')),float(e.get('lon')))
            elif e.tag=='way' and e.get('id')==wid: nds=[n.get('ref') for n in e.findall('nd')]
    return [N[n] for n in nds]
def medir(sitio,wid,paso=10,maxhalf=25,thr=12):
    I=Img(sitio); a=np.asarray(Image.open(f'{U}/imagenes/{sitio}_esri_z19.png').convert('RGB')).astype(int)
    exg=2*a[...,1]-a[...,0]-a[...,2]; bri=a.sum(-1)/3
    nonveg=(exg<thr)&(bri>60)
    pts=[I.ll2m(la,lo) for la,lo in way_ll(wid)]; L=LineString(pts); out=[]
    for s in np.arange(0,L.length,paso):
        p=L.interpolate(s); q=L.interpolate(min(s+1,L.length)); r=L.interpolate(max(s-1,0))
        dx,dy=q.x-r.x,q.y-r.y; n=math.hypot(dx,dy); nx,ny=-dy/n,dx/n
        prof=[]
        for t in np.arange(-maxhalf,maxhalf+0.01,0.25):
            px,py=I.m2px(p.x+nx*t,p.y+ny*t)
            if 0<=int(py)<I.H and 0<=int(px)<I.W: prof.append(bool(nonveg[int(py),int(px)]))
            else: prof.append(False)
        prof=np.array(prof); c=len(prof)//2
        # cerrar huecos de hasta 1 m (4 muestras)
        f=prof.copy()
        for i in range(len(f)):
            if not f[i]:
                l=i-1
                while l>=0 and not prof[l]: l-=1
                rr=i+1
                while rr<len(prof) and not prof[rr]: rr+=1
                if l>=0 and rr<len(prof) and (rr-l-1)<=4: f[i]=True
        if not f[c]: out.append((round(s),None,None,None)); continue
        l=c
        while l>0 and f[l-1]: l-=1
        r_=c
        while r_<len(f)-1 and f[r_+1]: r_+=1
        lat,lon=I.m2ll(p.x,p.y)
        out.append((round(s),round((r_-l+1)*0.25,1),round(lat,6),round(lon,6)))
    return out
if __name__=='__main__':
    s,w=sys.argv[1],sys.argv[2]
    for r in medir(s,w): print(r)
