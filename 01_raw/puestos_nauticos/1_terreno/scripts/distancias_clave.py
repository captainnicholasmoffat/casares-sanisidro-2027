# Distancias clave por puesto [cálculo propio]: punto náutico (NP) -> calle pública con nombre más cercana, -> playones,
# y distancia de cada lugar candidato a la orilla OSM (para la franja de 15 m del camino de sirga, art. 1974 CCyC).
import sys, json, csv
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/scripts')
from osmlib import *
from shapely.ops import unary_union, nearest_points
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/'
ALL=[D+f'osm/osmapi_{s}.osm' for s in ('1_aguila','2_saenzpena','3_centenera','4_puerto','5_33orientales','6_pacheco')]+[D+'osm/osmapi_rel_3623442_full.osm',D+'osm/osmapi_rel_10343661_full.osm']
N,W,R=load(ALL)
rio=unary_union([way_geom(N,W[ref],area_ok=False) for typ,ref,role in R['3474227']['mem'] if typ=='way' and ref in W])
dars=rel_geom(N,W,R['3623442']).boundary
orilla=unary_union([rio,dars,rel_geom(N,W,R['10343661']).boundary])
NPS={'1_aguila':(-34.47429,-58.48668),'2_saenzpena':(-34.4645,-58.49663),'3_centenera':(-34.46151,-58.49982),'4_puerto':(-34.4614,-58.50612),'5_33orientales':(-34.45033,-58.51673),'6_pacheco':(-34.48519,-58.48044)}
CAND={ # lugares candidatos para estacionar el vehículo (OSM)
 '1_aguila':[('way','682693239','playón público Parque Águila Chico'),('way','462817720','playón 961 m2 (tierra)'),('way','462708069','Sebastián Elcano (calle)'),('way','1505731589','ciclovía paralela')],
 '2_saenzpena':[('way','682105107','playón Roque Sáenz Peña (1.585 m2, capacity=50)'),('way','435068369','playón 243 m2'),('way','139486214','rotonda final Roque Sáenz Peña'),('way','955363910','lazo sin nombre (sentido único)'),('way','682107625','Muelle Público (ferry_terminal)')],
 '3_centenera':[('way','133213059','Stella Maris (continuación hacia el río)'),('way','208358260','Del Barco Centenera (último tramo)'),('way','450116333','Centro Municipal de Exposiciones (predio)'),('way','451791683','playón privado 2.632 m2')],
 '4_puerto':[('way','303901564','Avenida Mitre (último tramo)'),('way','469319726','Avenida Tiscornia (service)'),('way','1360935458','service sin nombre junto al parque'),('way','434820818','Camino de la Ribera (service, bicycle=yes)'),('way','1360935454','ciclovía 2026'),('way','451791683','playón privado 2.632 m2'),('way','439428388','estacionamiento street_side 508 m2')],
 '5_33orientales':[('way','1240325350','Treinta y Tres Orientales (último tramo)'),('way','64376434','Bartolomé Mitre'),('way','64376475','Dársena Gauto y Pavón (service)')],
 '6_pacheco':[('way','318617047','playón Paseo Público Costero (1.419 m2)'),('way','4662576','General Pacheco (último tramo)'),('way','1331096648','Sebastián Elcano'),('way','970643939','Juan Díaz de Solís'),('way','1504433013','ciclovía Elcano (2026)'),('way','149915782','espigón (man_made=pier)'),('way','513154556','Puerto Libre (predio municipal)')],
}
rows=[]
for s,(la,lo) in NPS.items():
    P=pt(la,lo)
    for typ,i,desc in CAND[s]:
        g=way_geom(N,W[i]); 
        rows.append(dict(sitio=s,lugar=desc,osm=f'{typ}/{i}',dist_al_punto_nautico_m=round(g.distance(P)),dist_min_a_orilla_OSM_m=round(g.distance(orilla),1),dentro_15m_orilla='sí (parte)' if g.distance(orilla)<15 else 'no',tags_clave=';'.join(f'{k}={v}' for k,v in W[i]['tags'].items() if k in('highway','surface','lanes','oneway','maxspeed','access','fee','parking','capacity','amenity','name')),ultima_edicion_osm=W[i]['ts'][:10]))
with open(D+'calculos/CALCULO_PROPIO_distancias_lugares_candidatos.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
