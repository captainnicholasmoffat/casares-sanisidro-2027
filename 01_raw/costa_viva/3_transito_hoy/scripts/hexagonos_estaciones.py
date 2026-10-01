# Transacciones SUBE (día hábil promedio, oct-2025) en el hexágono H3 res. 8 (~0,74 km²) que contiene cada estación. [cálculo propio]
# Ojo: el hexágono suma todas las validaciones del área (no sólo de la estación) y el Tren de la Costa valida a bordo.
import csv, collections, h3
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/'
est=[('TdlC Anchorena',-34.48915,-58.48122),('TdlC Las Barrancas',-34.47238,-58.49306),('TdlC San Isidro R',-34.4654,-58.50827),('TdlC Punta Chica',-34.45052,-58.52385),
     ('Mitre Martínez',-34.48862,-58.49641),('Mitre Acassuso',-34.47989,-58.504),('Mitre San Isidro C',-34.47201,-58.51357),('Mitre Beccar',-34.46071,-58.52658)]
hx={h3.latlng_to_cell(a,b,8):n for n,a,b in est}
agg=collections.defaultdict(collections.Counter); hora=collections.defaultdict(collections.Counter)
for r in csv.DictReader(open(B+'sube/trx2025_hexagonos_dia_habil_oct2025.csv')):
    if r['id_h3'] in hx:
        agg[r['id_h3']][r['modo']]+=int(r['cantidad_trx'])
with open(B+'sube_hexagonos_estaciones.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['estacion','id_h3','colectivo','tren','subte'])
    for h,n in hx.items():
        c=agg[h]; w.writerow([n,h,c.get('COLECTIVO',0),c.get('TREN',0),c.get('SUBTE',0)]); print(n,h,dict(c))
