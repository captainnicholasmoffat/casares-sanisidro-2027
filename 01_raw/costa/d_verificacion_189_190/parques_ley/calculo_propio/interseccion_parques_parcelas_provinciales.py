# CALCULO PROPIO [CP]. Cruza polígonos de parques costeros (OpenStreetMap, no oficiales, tomados del repo
# 01_raw/parques/5_satelite/poligonos_analisis.geojson) y el polígono de Bosque Alegre del Decreto 910/2012 (art. 2,
# 6 coordenadas) con las 15 parcelas del Anexo I de la Res. MEcon 138/2026 (catastro ARBA, repo
# 01_raw/costa_viva/1_tenencia_y_canon/ARBA_WFS_15_parcelas_AnexoI_Res138-2026_2026-10-01.json).
# Proyección métrica EPSG:5347. Las parcelas ARBA no cubren el lecho del río: "fuera de las 15 parcelas" NO significa
# "tierra municipal". Para afirmar dominio hace falta informe de dominio.
import json, csv, sys
from shapely.geometry import shape, Polygon
from shapely.ops import transform
import pyproj
REPO='/home/user/casares-sanisidro-2027/01_raw/'
g=json.load(open(REPO+'parques/5_satelite/poligonos_analisis.geojson'))
arba=json.load(open(REPO+'costa_viva/1_tenencia_y_canon/ARBA_WFS_15_parcelas_AnexoI_Res138-2026_2026-10-01.json'))
proj=pyproj.Transformer.from_crs('EPSG:4326','EPSG:5347',always_xy=True).transform
parcels=[(f['properties']['cca'], transform(proj,shape(f['geometry']))) for f in arba['features']]
def dms(d,m,s): return -(d+m/60+s/3600)
ba=[(dms(58,29,59.04),dms(34,27,41.52)),(dms(58,30,3.00),dms(34,27,44.57)),(dms(58,29,58.82),dms(34,27,47.95)),
    (dms(58,29,56.86),dms(34,27,46.57)),(dms(58,29,54.05),dms(34,27,49.08)),(dms(58,29,50.43),dms(34,27,46.34))]
targets={'Bosque Alegre (poligono Dec. 910/2012)':transform(proj,Polygon(ba))}
keep=['Parque Natural Municipal Ribera Norte','Perú Beach','Paseo del Águila','Parque Aguila Chico','Paseo Público Costero',
      'Puerto Libre','Plaza Bosque Alegre','Parque Público del Golf','Paseo de los Inmigrantes','Puerto Tablas']
for f in g['features']:
    n=f['properties']['name'] or ''
    if n in keep or n.startswith('Caso: 33 Orientales (costa') or n.startswith('Caso: Roque Saenz Pena y el rio'):
        targets[n+' (OSM '+str(f['properties'].get('osm') or 'poligono del informe 14')+')']=transform(proj,shape(f['geometry']))
w=csv.writer(sys.stdout)
w.writerow(['espacio','area_m2','m2_dentro_de_las_15_parcelas_provinciales','porcentaje','parcelas_cca_y_m2'])
for n,geom in targets.items():
    if not geom.is_valid: geom=geom.buffer(0)
    hits=[(c,round(geom.intersection(p).area)) for c,p in parcels if geom.intersection(p).area>50]
    inter=sum(h[1] for h in hits)
    w.writerow([n,round(geom.area),inter,f'{100*inter/geom.area:.0f}%',' | '.join(f'{c}:{a}' for c,a in hits)])
