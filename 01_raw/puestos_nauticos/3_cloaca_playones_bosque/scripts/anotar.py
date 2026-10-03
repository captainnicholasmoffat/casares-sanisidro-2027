# Dibuja sobre el mosaico Esri: grilla en metros (cada 25 m, rótulos cada 50 m, origen = centro del recorte),
# parcelas ARBA (amarillo; las del convenio Res.138/2026 en naranja con su ítem), polígono del Paisaje Protegido (rojo),
# playones de OSM (cian) y parques OSM (verde). Salida: recortes/<sitio>_anotado.jpg y work/<sitio>_vista.jpg (reducida)
import sys, json, glob, xml.etree.ElementTree as ET
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from geo import *
from PIL import Image, ImageDraw, ImageFont
def font(sz):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf']:
        try: return ImageFont.truetype(f,sz)
        except Exception: pass
    return ImageFont.load_default()
OSMF=glob.glob(f'{D1}/osm/osmapi_*.osm')
def osm_polys():
    N={};Ws=[]
    for f in OSMF:
        r=ET.parse(f).getroot()
        for e in r:
            if e.tag=='node': N[e.get('id')]=(float(e.get('lat')),float(e.get('lon')))
            elif e.tag=='way':
                t={x.get('k'):x.get('v') for x in e.findall('tag')}
                if t.get('amenity')=='parking' or t.get('leisure')=='park': Ws.append((e.get('id'),t,[n.get('ref') for n in e.findall('nd')]))
    out={}
    for wid,t,nds in Ws:
        pts=[N[n] for n in nds if n in N]
        if len(pts)>2: out[wid]=(t,pts)
    return out
OP=osm_polys(); AR=arba_features()
def anotar(sitio,extra=None,grid=25):
    I=Img(sitio); im=Image.open(f'{U}/imagenes/{sitio}_esri_z19.png').convert('RGB'); d=ImageDraw.Draw(im,'RGBA')
    f1=font(26); f2=font(34)
    # grilla
    half=I.m['semilado_m']+20
    for v in range(-int(half)//grid*grid,int(half)+1,grid):
        a=I.m2px(v,-half); b=I.m2px(v,half); d.line([a,b],fill=(255,255,255,90 if v%50 else 150),width=1 if v%50 else 2)
        a=I.m2px(-half,v); b=I.m2px(half,v); d.line([a,b],fill=(255,255,255,90 if v%50 else 150),width=1 if v%50 else 2)
    for v in range(-int(half)//50*50,int(half)+1,50):
        x,_=I.m2px(v,0); d.text((x+3,5),f'{v}',fill=(255,255,0),font=f1,stroke_width=2,stroke_fill=(0,0,0))
        _,y=I.m2px(0,v); d.text((5,y+3),f'{v}',fill=(255,255,0),font=f1,stroke_width=2,stroke_fill=(0,0,0))
    # ARBA
    for ft in AR:
        g=shape(ft['geometry']); cca=ft['properties']['cca']
        for p in getattr(g,'geoms',[g]):
            xy=[I.ll2px(la,lo) for lo,la in p.exterior.coords]
            if not any(0<=x<I.W and 0<=y<I.H for x,y in xy): continue
            it=CONVENIO.get(cca)
            d.line(xy,fill=(255,140,0,255) if it else (255,255,0,200),width=5 if it else 2)
            if it:
                c=p.representative_point(); x,y=I.ll2px(c.y,c.x)
                if 0<x<I.W and 0<y<I.H: d.text((x,y),f'conv. ítem {it}',fill=(255,140,0),font=f2,stroke_width=3,stroke_fill=(0,0,0))
    # OSM
    for wid,(t,pts) in OP.items():
        xy=[I.ll2px(la,lo) for la,lo in pts]
        if not any(0<=x<I.W and 0<=y<I.H for x,y in xy): continue
        col=(0,255,255,255) if t.get('amenity')=='parking' else (0,255,0,200)
        d.line(xy,fill=col,width=4 if t.get('amenity')=='parking' else 2)
    # PP Bosque Alegre
    pp=[I.ll2px(la,lo) for la,lo in pp_polygon_ll()]
    d.line(pp,fill=(255,0,0,255),width=6)
    if extra: extra(I,d)
    im.save(f'{U}/recortes/{sitio}_anotado.jpg',quality=88)
    v=im.copy(); v.thumbnail((1600,1600)); v.save(f'{U}/work/{sitio}_vista.jpg',quality=85)
    return I
if __name__=='__main__':
    for s in sys.argv[1:]: anotar(s); print('ok',s)
