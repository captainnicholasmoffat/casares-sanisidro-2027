# uso: crop_grid.py in.png x0 y0 x1 y1 escala mpp paso_m out.png
import sys
from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); k=int(sys.argv[6]); mpp=float(sys.argv[7]); step=float(sys.argv[8]); out=sys.argv[9]
c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*k,(y1-y0)*k),Image.LANCZOS)
d=ImageDraw.Draw(c); s=step/mpp*k
i=0
while i*s < c.size[0]:
    d.line([(i*s,0),(i*s,c.size[1])],fill=(255,255,0) if i%2==0 else (0,255,255),width=1); d.text((i*s+2,2),f"{i*step:.0f}",fill=(255,255,0)); i+=1
j=0
while j*s < c.size[1]:
    d.line([(0,j*s),(c.size[0],j*s)],fill=(255,255,0) if j%2==0 else (0,255,255),width=1); d.text((2,j*s+2),f"{j*step:.0f}",fill=(255,255,0)); j+=1
c.save(out); print(out,c.size,'grid',step,'m')
