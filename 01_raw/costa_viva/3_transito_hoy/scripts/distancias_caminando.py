# Distancias a pie desde estaciones de tren a puntos de la costa.
# Ruteo: OSRM perfil peatonal de FOSSGIS (https://routing.openstreetmap.de/routed-foot), sobre datos OSM (no oficial).
# Coordenadas de estaciones: nodos OSM (railway=station/halt). Coordenadas de destinos: rasgos OSM (ver comentario). [cálculo propio]
import json, urllib.request, csv, math
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/'
est=[('TdlC Libertador (Vicente López)',-34.50256,-58.48198),('TdlC Anchorena',-34.48915,-58.48122),('TdlC Las Barrancas',-34.47238,-58.49306),
     ('TdlC San Isidro R',-34.4654,-58.50827),('TdlC Punta Chica',-34.45052,-58.52385),('TdlC Marina Nueva (San Fernando)',-34.44455,-58.53903),
     ('Mitre La Lucila (Vicente López)',-34.49763,-58.48841),('Mitre Martínez',-34.48862,-58.49641),('Mitre Acassuso',-34.47989,-58.504),
     ('Mitre San Isidro C',-34.47201,-58.51357),('Mitre Beccar',-34.46071,-58.52658)]
dest=[('D1 Pacheco y el río / Paseo Público Costero (estac. sur)',-34.48553,-58.48118,'OSM way 318617047'),
      ('D2 Paseo del Águila',-34.47623,-58.48748,'OSM way 521940596 (centroide)'),
      ('D3 Perú Beach',-34.47174,-58.4924,'OSM way 270513456 (centroide)'),
      ('D4 Reserva Ribera Norte',-34.47015,-58.49609,'OSM node 9383625918'),
      ('D5 Roque Sáenz Peña y el río (muelle)',-34.4643,-58.4964,'OSM way 682107625'),
      ('D6 Parque del Puerto de San Isidro',-34.46128,-58.50714,'OSM node 8075785044'),
      ('D7 Bosque Alegre (plaza)',-34.46229,-58.50002,'OSM way 450116337 [probable]'),
      ('D8 Paseo del Río (calle Gaetán Gutiérrez)',-34.4577,-58.5055,'punto sobre Gaetán Gutiérrez [probable]'),
      ('D9 Paseo 33 Orientales (fin de la calle)',-34.4504,-58.5168,'extremo de OSM way 1240325350 [probable]')]
pts=est+[(d[0],d[1],d[2]) for d in dest]
coords=';'.join(f'{p[2]},{p[1]}' for p in pts)
src=';'.join(str(i) for i in range(len(est))); dst=';'.join(str(i) for i in range(len(est),len(pts)))
u=f'https://routing.openstreetmap.de/routed-foot/table/v1/driving/{coords}?sources={src}&destinations={dst}&annotations=distance,duration'
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'investigacion-costa-sanisidro/1.0'}),timeout=60))
json.dump(r,open(B+'osm/osrm_foot_table.json','w'))
def hav(a,b,c,d):
    R=6371000;p1,p2=math.radians(a),math.radians(c);dp=p2-p1;dl=math.radians(d-b)
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2;return 2*R*math.asin(math.sqrt(h))
rows=[]
for i,e in enumerate(est):
    for j,d in enumerate(dest):
        dist=r['distances'][i][j]; dur=r['durations'][i][j]
        rows.append(dict(estacion=e[0],destino=d[0],fuente_coord_destino=d[3],linea_recta_m=round(hav(e[1],e[2],d[1],d[2])),
             a_pie_m=round(dist) if dist is not None else '',minutos_a_5kmh=round(dist/83.33) if dist else '',minutos_osrm=round(dur/60) if dur else ''))
with open(B+'distancias_estaciones_costa.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# más cercana por destino
for d in dest:
    rr=sorted([x for x in rows if x['destino']==d[0] and x['a_pie_m']!=''],key=lambda x:x['a_pie_m'])[:3]
    print(d[0]); [print('   ',x['estacion'],x['a_pie_m'],'m a pie |',x['linea_recta_m'],'m recta |',x['minutos_a_5kmh'],'min') for x in rr]
