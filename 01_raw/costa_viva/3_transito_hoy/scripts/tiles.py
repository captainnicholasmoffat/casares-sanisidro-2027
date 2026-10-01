# Descarga del API principal de OSM (api.openstreetmap.org/api/0.6/map) en teselas de 0,0125°
# sólo las que tocan la zona costera (con 150 m de margen). Datos OSM, no oficiales.
import pickle, urllib.request, os, time
from shapely.geometry import box
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/osm/'
Z=pickle.load(open(B+'zonas.pkl','rb'))
zc=sorted(Z['parts'],key=lambda p:p.area,reverse=True)[1].buffer(0.0015)
s=0.0125; tiles=[]
x0,y0,x1,y1=zc.bounds
import math
i=math.floor(x0/s)
while i*s<x1:
    j=math.floor(y0/s)
    while j*s<y1:
        b=box(i*s,j*s,(i+1)*s,(j+1)*s)
        if b.intersects(zc): tiles.append((round(i*s,4),round(j*s,4),round((i+1)*s,4),round((j+1)*s,4)))
        j+=1
    i+=1
print(len(tiles),'teselas')
for t in tiles:
    fn=B+'api_tiles/map_%s_%s_%s_%s.osm'%t
    if os.path.exists(fn) and os.path.getsize(fn)>1000: continue
    u='https://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s'%t
    for k in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'investigacion-costa-sanisidro/1.0'}),timeout=120).read()
            open(fn,'wb').write(r); print('ok',t,len(r)); break
        except Exception as e:
            print('err',t,e); time.sleep(5)
    time.sleep(1)
