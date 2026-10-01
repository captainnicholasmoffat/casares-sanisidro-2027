# Define los 4 tramos costeros por "progresiva" (distancia a lo largo de un eje costero SE->NO, en metros)
# Eje: desde la esquina costera con Vicente López (calle Paraná) hasta la estación Punta Chica (límite con San Fernando).
import pickle, numpy as np
from shapely.geometry import Point
from shapely.ops import transform
from pyproj import Transformer
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/osm/'
tr=Transformer.from_crs(4326,32721,always_xy=True)
A=np.array(tr.transform(-58.4796,-34.4898)); Bp=np.array(tr.transform(-58.5240,-34.4505))
u=(Bp-A)/np.linalg.norm(Bp-A)
def s(lon,lat):
    p=np.array(tr.transform(lon,lat)); return float((p-A)@u)
def zona():
    Z=pickle.load(open(B+'zonas.pkl','rb'))
    return Z, sorted(Z['parts'],key=lambda p:p.area,reverse=True)[1]
CORTES=None
def cortes():
    Z,zc=zona()
    out={}
    for n in ['Martínez','Acassuso','San Isidro','Béccar']:
        g=Z['loc'][n].intersection(zc)
        xs=[s(x,y) for x,y in (g.exterior.coords if g.geom_type=='Polygon' else [c for gg in g.geoms for c in gg.exterior.coords])]
        out[n]=(min(xs),max(xs))
    return out
RSP=s(-58.4973,-34.4638)  # extremo costero de Roque Sáenz Peña (muelle público)
def tramo(lon,lat,c):
    v=s(lon,lat)
    if v<c['Martínez'][1]: return '1 Martínez'
    if v<RSP: return '2 Acassuso'
    if v<c['San Isidro'][1]: return '3 Bajo de San Isidro'
    return '4 Béccar'
if __name__=='__main__':
    c=cortes(); print(c); print('RSP',RSP, 'largo eje', np.linalg.norm(Bp-A))
