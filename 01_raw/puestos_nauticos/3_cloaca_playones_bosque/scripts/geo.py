# utilidades: pixel <-> lon/lat (Web Mercator z19 del mosaico) y metros locales; capas ARBA/OSM/PP
import math, json, glob
from pyproj import Transformer
from shapely.geometry import shape, Polygon, Point, LineString
from shapely.ops import transform as shp_tr
U='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque'
D1='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno'
UTM=Transformer.from_crs('EPSG:4326','EPSG:32721',always_xy=True)
def merc(lat,lon):
    return (lon+180)/360, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2
class Img:
    def __init__(s,sitio):
        s.m=json.load(open(f'{U}/imagenes/{sitio}_esri_z19.json'))
        w,so,e,n=s.m['bbox_lonlat']; s.W,s.H=s.m['px']
        s.x0,s.y0=merc(n,w); s.x1,s.y1=merc(so,e)
        s.lat0,s.lon0=s.m['centro']
        s.kx=111320*math.cos(math.radians(s.lat0)); s.ky=110574
    def ll2px(s,lat,lon):
        x,y=merc(lat,lon); return ((x-s.x0)/(s.x1-s.x0)*s.W, (y-s.y0)/(s.y1-s.y0)*s.H)
    def px2ll(s,px,py):
        x=s.x0+px/s.W*(s.x1-s.x0); y=s.y0+py/s.H*(s.y1-s.y0)
        lon=x*360-180; lat=math.degrees(math.atan(math.sinh(math.pi*(1-2*y)))); return lat,lon
    def m2ll(s,e,n):  # metros locales (este, norte) desde el centro -> lat, lon
        return s.lat0+n/s.ky, s.lon0+e/s.kx
    def ll2m(s,lat,lon): return ((lon-s.lon0)*s.kx,(lat-s.lat0)*s.ky)
    def m2px(s,e,n): return s.ll2px(*s.m2ll(e,n))
def area_m2_from_m(img,pts):
    ll=[img.m2ll(e,n) for e,n in pts]; p=Polygon([UTM.transform(lo,la) for la,lo in ll]); return p.area, p
def arba_features():
    fs={}
    for f in glob.glob(f'{D1}/arba/arba_Parcela_*.json')+glob.glob(f'{U}/arba/arba_Parcela_*.json'):
        for ft in json.load(open(f))['features']: fs[ft['properties']['cca']]=ft
    return list(fs.values())
CONVENIO={}
import csv
for r in csv.DictReader(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/01_raw/costa_viva/1_tenencia_y_canon/CALCULO_PROPIO_superficie_15_parcelas_AnexoI.csv')):
    if r['item_AnexoI']!='TOTAL': CONVENIO[r['cca_ARBA']]=r['item_AnexoI']
def pp_polygon_ll():
    g=json.load(open(f'{D1}/calculos/CALCULO_PROPIO_poligono_Dec910-2012_Bosque_Alegre.geojson'))['geometry']['coordinates'][0]
    return [(la,lo) for lo,la in g]
