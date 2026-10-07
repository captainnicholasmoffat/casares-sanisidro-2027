import sys, math, io, urllib.request, ssl
from PIL import Image, ImageDraw
lat=float(sys.argv[1]); lon=float(sys.argv[2]); z=int(sys.argv[3]); R=int(sys.argv[4]); out=sys.argv[5]
marks=[tuple(map(float,m.split(','))) for m in sys.argv[6].split(';')] if len(sys.argv)>6 else []
def xy(lat,lon):
    n=2**z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return x,y
def qk(x,y,z):
    s=''
    for i in range(z,0,-1):
        d=0; m=1<<(i-1)
        if x&m: d+=1
        if y&m: d+=2
        s+=str(d)
    return s
x,y=xy(lat,lon); X0=int(x)-R; Y0=int(y)-R; N=2*R+1
ctx=ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
img=Image.new('RGB',(256*N,256*N))
for i in range(N):
    for j in range(N):
        url=f"https://ecn.t{(i+j)%4}.tiles.virtualearth.net/tiles/a{qk(X0+i,Y0+j,z)}.jpeg?g=1"
        d=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),context=ctx,timeout=60).read()
        img.paste(Image.open(io.BytesIO(d)).convert('RGB'),(256*i,256*j))
mpp=156543.03392*math.cos(math.radians(lat))/2**z
dr=ImageDraw.Draw(img)
for (la,lo) in marks:
    px,py=xy(la,lo); px=(px-X0)*256; py=(py-Y0)*256
    dr.ellipse([px-5,py-5,px+5,py+5],outline=(255,0,0),width=2)
L=20/mpp; dr.rectangle([10,10,10+L,16],fill=(255,255,0)); dr.text((12,20),"20 m",fill=(255,255,0))
img.save(out); print(out,img.size,'m/px=%.4f'%mpp,'X0',X0,'Y0',Y0)
