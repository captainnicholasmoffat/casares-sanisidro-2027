import json, csv, math, collections
from shapely.geometry import shape, LineString, Point
from shapely.ops import unary_union
g=json.load(open('em/data/radios_censales_sanisidro.geojson'))
polys={f['properties']['radio_id']:shape(f['geometry']) for f in g['features']}
U=unary_union(list(polys.values())).buffer(0)
geoms=[U] if U.geom_type=='Polygon' else list(U.geoms)
coords=[c for p in geoms for c in p.exterior.coords]
print('union bounds',U.bounds)
# river edge: for each lat band, easternmost exterior point
bands=collections.defaultdict(list)
for x,y in coords: bands[round(y/0.002)].append((x,y))
edge=sorted([max(v) for v in bands.values()], key=lambda p:p[1])
edge=[p for p in edge if p[1]>=-34.4839]
print('edge pts',len(edge), edge[0], edge[-1])
E=LineString(edge)
lat0=-34.48; kx=111320*math.cos(math.radians(lat0)); ky=110540
def dist_m(pt,line):
    # approximate by scaling coords
    from shapely.affinity import scale
    return scale(line,kx,ky,origin=(0,0)).distance(scale(pt,kx,ky,origin=(0,0)))
res={k:dist_m(p.representative_point(),E) for k,p in polys.items()}
json.dump(res,open('costa_viva_raw/v5_semana_invierno/CEP_empleo_AMBA/radios2022_distancia_borde_rio_m.json','w'))
rows=list(csv.DictReader(open('costa_viva_raw/v5_semana_invierno/CEP_empleo_AMBA/Empleo-AMBA_SanIsidro_06756_extracto.csv')))
tot_all=collections.Counter()
for r in rows: tot_all[r['clae2']]+=int(r['Cantidad_trabajadores'] or 0)
interest=[('56','Servicio de comidas y bebidas'),('47','Comercio minorista'),('55','Alojamiento'),('93','Deportivas, recreativas y de entretenimiento'),('94','Asociaciones (incl. clubes)'),('50','Transporte por agua'),('85','Enseñanza'),('87','Atención a personas mayores u otros (residencias)')]
out=open('costa_viva_raw/v5_semana_invierno/calculo_propio_empleo_formal_franja_costera_SanIsidro_oct2021.csv','w')
out.write('umbral_m,radios_2022_en_franja,trabajadores_georref_total,clae2,descripcion,trabajadores_franja,trabajadores_partido_georref\n')
for th in (400,600,800):
    coast={k for k,v in res.items() if v<=th}
    c=collections.Counter(); tot=0
    for r in rows:
        if r['LINK'] in coast:
            n=int(r['Cantidad_trabajadores'] or 0); c[r['clae2']]+=n; tot+=n
    print(f'--- franja <= {th} m del borde con el río: {len(coast)} radios, trabajadores georref. {tot}')
    for k,v in interest:
        print(f'   {k} {v}: {c[k]} (partido: {tot_all[k]})'); out.write(f'{th},{len(coast)},{tot},{k},{v},{c[k]},{tot_all[k]}\n')
    if th==600:
        for k in sorted(coast):
            pt=polys[k].representative_point(); print('     ',k,round(pt.y,4),round(pt.x,4),round(res[k]))
out.close()
