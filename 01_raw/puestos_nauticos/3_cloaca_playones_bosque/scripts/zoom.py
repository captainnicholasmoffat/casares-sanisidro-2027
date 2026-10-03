# Recorte en metros locales (e0,n0,e1,n1) del mosaico anotado con grilla fina cada 10 m (rótulos cada 20 m).
import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from geo import *
from anotar import font, AR, CONVENIO, OP
from PIL import Image, ImageDraw
def zoom(sitio,e0,n0,e1,n1,out,polys=None,grid=10,maxpx=1500,raw=False):
    I=Img(sitio); im=Image.open(f'{U}/imagenes/{sitio}_esri_z19.png').convert('RGB'); d=ImageDraw.Draw(im,'RGBA'); f=font(18); f2=font(24)
    if not raw:
        for v in range(int(e0)//grid*grid,int(e1)+1,grid):
            d.line([I.m2px(v,n0),I.m2px(v,n1)],fill=(255,255,255,70 if v%(2*grid) else 140),width=1)
        for v in range(int(n0)//grid*grid,int(n1)+1,grid):
            d.line([I.m2px(e0,v),I.m2px(e1,v)],fill=(255,255,255,70 if v%(2*grid) else 140),width=1)
        for ft in AR:
            g=shape(ft['geometry']); it=CONVENIO.get(ft['properties']['cca'])
            for p in getattr(g,'geoms',[g]):
                d.line([I.ll2px(la,lo) for lo,la in p.exterior.coords],fill=(255,140,0,255) if it else (255,255,0,220),width=3 if it else 2)
        for wid,(t,pts) in OP.items():
            d.line([I.ll2px(la,lo) for la,lo in pts],fill=(0,255,255,255) if t.get('amenity')=='parking' else (0,255,0,200),width=3 if t.get('amenity')=='parking' else 2)
        d.line([I.ll2px(la,lo) for la,lo in pp_polygon_ll()],fill=(255,0,0,255),width=4)
    if polys:
        for lab,pts,col in polys:
            xy=[I.m2px(e,n) for e,n in pts]
            d.polygon(xy,outline=col+(255,),fill=col+(70,)); d.line(xy+[xy[0]],fill=col+(255,),width=4)
            cx=sum(x for x,y in xy)/len(xy); cy=sum(y for x,y in xy)/len(xy)
            d.text((cx-20,cy-12),lab,fill=(255,255,255),font=f2,stroke_width=3,stroke_fill=(0,0,0))
    a=I.m2px(e0,n1); b=I.m2px(e1,n0)
    c=im.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1])))
    if not raw:
        dc=ImageDraw.Draw(c)
        for v in range(int(e0)//(2*grid)*(2*grid),int(e1)+1,2*grid):
            x=I.m2px(v,0)[0]-a[0]; dc.text((x+2,2),str(v),fill=(255,255,0),font=f,stroke_width=2,stroke_fill=(0,0,0))
        for v in range(int(n0)//(2*grid)*(2*grid),int(n1)+1,2*grid):
            y=I.m2px(0,v)[1]-a[1]; dc.text((2,y+2),str(v),fill=(255,255,0),font=f,stroke_width=2,stroke_fill=(0,0,0))
    if max(c.size)>maxpx: c.thumbnail((maxpx,maxpx))
    c.save(out,quality=88); return c.size
if __name__=='__main__':
    s=sys.argv[1]; e0,n0,e1,n1=map(float,sys.argv[2:6]); out=sys.argv[6]; raw=len(sys.argv)>7
    print(zoom(s,e0,n0,e1,n1,out,raw=raw))
