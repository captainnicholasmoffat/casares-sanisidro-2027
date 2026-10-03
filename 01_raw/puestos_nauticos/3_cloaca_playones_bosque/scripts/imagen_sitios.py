# -*- coding: utf-8 -*-
"""Descarga teselas z19 de Esri World Imagery (servicio público, sin registro) y arma un mosaico por sitio.
Guarda: imagenes/<sitio>_esri_z19.png (imagen tal cual) y imagenes/<sitio>_esri_z19.json (bbox lon/lat, z, fuente).
Uso: python3 imagen_sitios.py  [sitio ...]
"""
import math, json, os, sys, io, time, subprocess
from PIL import Image
U='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque'
SITIOS={
 '1_aguila':(-34.4747,-58.4872,260),
 '2_saenzpena':(-34.4640,-58.4972,260),
 '3_centenera':(-34.4620,-58.5007,260),
 'BA_bosque_alegre':(-34.4626,-58.4998,330),
 '4_puerto':(-34.4612,-58.5068,260),
 '5_33orientales':(-34.4505,-58.5163,260),
 '6_pacheco':(-34.4850,-58.4812,260),
 '5b_33orientales_calle':(-34.4513,-58.5188,300),
}
Z=19
URL='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
def deg2num(lat,lon,z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n; return x,y
def num2deg(x,y,z):
    n=2**z; lon=x/n*360-180; lat=math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))); return lat,lon
def fetch(z,x,y):
    cache=f'{U}/work/tiles/{z}_{y}_{x}.jpg'
    os.makedirs(os.path.dirname(cache),exist_ok=True)
    if not os.path.exists(cache) or os.path.getsize(cache)<500:
        subprocess.run(['curl','-sS','-m','60','-o',cache,URL.format(z=z,x=x,y=y)],check=False)
    return Image.open(cache).convert('RGB')
for s in (sys.argv[1:] or SITIOS):
    lat,lon,h=SITIOS[s]
    dlat=h/110574; dlon=h/(111320*math.cos(math.radians(lat)))
    n,w,so,e=lat+dlat,lon-dlon,lat-dlat,lon+dlon
    x0,y0=deg2num(n,w,Z); x1,y1=deg2num(so,e,Z)
    tx0,ty0,tx1,ty1=int(x0),int(y0),int(x1),int(y1)
    W=(tx1-tx0+1)*256; H=(ty1-ty0+1)*256
    im=Image.new('RGB',(W,H))
    for tx in range(tx0,tx1+1):
        for ty in range(ty0,ty1+1):
            im.paste(fetch(Z,tx,ty),((tx-tx0)*256,(ty-ty0)*256))
    # recorte exacto al bbox
    cx0=int((x0-tx0)*256); cy0=int((y0-ty0)*256); cx1=int((x1-tx0)*256); cy1=int((y1-ty0)*256)
    im=im.crop((cx0,cy0,cx1,cy1))
    # bbox real del recorte
    la_n,lo_w=num2deg(tx0+cx0/256,ty0+cy0/256,Z); la_s,lo_e=num2deg(tx0+cx1/256,ty0+cy1/256,Z)
    out=f'{U}/imagenes/{s}_esri_z19.png'; im.save(out)
    meta=dict(sitio=s,centro=[lat,lon],semilado_m=h,bbox_lonlat=[lo_w,la_s,lo_e,la_n],px=[im.width,im.height],zoom=Z,
              m_por_px_aprox=round((2*h)/im.width,3),fuente='Esri World Imagery (servicio público de teselas, sin registro): '+URL,
              atribucion='Esri, Maxar, Earthstar Geographics, and the GIS User Community',consultado='2026-10-03')
    json.dump(meta,open(out.replace('.png','.json'),'w'),indent=1)
    print(s,im.size,meta['m_por_px_aprox'])
