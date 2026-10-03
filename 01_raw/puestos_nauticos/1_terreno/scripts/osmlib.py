# Carga archivos .osm (API 0.6) y arma geometrías en UTM 21S (EPSG:32721) para medir en metros. [cálculo propio]
import xml.etree.ElementTree as ET
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely.ops import transform, unary_union, linemerge, polygonize
from pyproj import Transformer
T=Transformer.from_crs('EPSG:4326','EPSG:32721',always_xy=True)
TI=Transformer.from_crs('EPSG:32721','EPSG:4326',always_xy=True)
def load(files):
    N={};W={};R={}
    for f in files:
        r=ET.parse(f).getroot()
        for e in r:
            tags={t.get('k'):t.get('v') for t in e.findall('tag')}
            if e.tag=='node': N[e.get('id')]=dict(lat=float(e.get('lat')),lon=float(e.get('lon')),tags=tags,ts=e.get('timestamp'))
            elif e.tag=='way': W[e.get('id')]=dict(nds=[n.get('ref') for n in e.findall('nd')],tags=tags,ts=e.get('timestamp'))
            elif e.tag=='relation': R[e.get('id')]=dict(mem=[(m.get('type'),m.get('ref'),m.get('role')) for m in e.findall('member')],tags=tags,ts=e.get('timestamp'))
    return N,W,R
def xy(N,nid):
    n=N[nid]; return T.transform(n['lon'],n['lat'])
def way_geom(N,w,area_ok=True):
    pts=[xy(N,i) for i in w['nds'] if i in N]
    if len(pts)<2: return None
    closed=w['nds'][0]==w['nds'][-1] and len(pts)>=4
    t=w['tags']
    is_area = closed and (t.get('area')=='yes' or any(k in t for k in ('amenity','leisure','landuse','building','natural','parking','man_made','place','area:highway','boundary')) and t.get('area')!='no' and not t.get('highway') or (t.get('highway')=='pedestrian' and t.get('area')=='yes'))
    if is_area and area_ok:
        try:
            p=Polygon(pts); 
            if not p.is_valid: p=p.buffer(0)
            return p
        except Exception: return LineString(pts)
    return LineString(pts)
def rel_geom(N,W,r):
    outers=[];inners=[]
    for typ,ref,role in r['mem']:
        if typ=='way' and ref in W:
            pts=[xy(N,i) for i in W[ref]['nds'] if i in N]
            if len(pts)>=2: (inners if role=='inner' else outers).append(LineString(pts))
    if not outers: return None
    polys=list(polygonize(unary_union(outers)))
    if not polys: return unary_union(outers)
    g=unary_union(polys)
    if inners:
        ip=list(polygonize(unary_union(inners)))
        if ip: g=g.difference(unary_union(ip))
    return g
def pt(lat,lon): return Point(*T.transform(lon,lat))
def ll(g):
    c=g.centroid if not isinstance(g,Point) else g
    lon,lat=TI.transform(c.x,c.y); return round(lat,5),round(lon,5)
