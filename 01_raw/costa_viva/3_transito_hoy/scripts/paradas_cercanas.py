# Parada de colectivo (OSM) más cercana a cada punto de la costa, y líneas (relaciones OSM) que paran allí.
# Distancia en línea recta y a pie (OSRM peatonal FOSSGIS). OSM no oficial; recorridos OSM pueden estar desactualizados (cambios jun-2026).
import pickle, math, json, urllib.request, csv
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/'
N,W,R=pickle.load(open(B+'osm/tiles_all.pkl','rb'))
bs=json.load(open(B+'osm/bus_stops_routes.json'))
stops={e['id']:(e['lon'],e['lat'],e['tags'].get('name','')) for e in bs['elements'] if e['type']=='node'}
for nid,(x,y,t,ts) in N.items():
    if t.get('highway')=='bus_stop' or (t.get('public_transport')=='platform' and t.get('bus')=='yes'): stops[nid]=(x,y,t.get('name',''))
serve={}
for rid,(mem,t,ts) in R.items():
    if t.get('route')=='bus':
        for ty,ref,role in mem:
            if ty=='node': serve.setdefault(ref,set()).add(t.get('ref'))
def d(a,b,c,e): return math.hypot((a-c)*111320,(b-e)*111320*math.cos(math.radians(34.47)))
dest=[('D1 Pacheco y el río',-34.48553,-58.48118),('D2 Paseo del Águila',-34.47623,-58.48748),('D3 Perú Beach',-34.47174,-58.4924),('D4 Ribera Norte',-34.47015,-58.49609),
      ('D5 Roque Sáenz Peña y el río',-34.4643,-58.4964),('D6 Parque del Puerto',-34.46128,-58.50714),('D7 Bosque Alegre',-34.46229,-58.50002),('D8 Paseo del Río',-34.4577,-58.5055),('D9 Paseo 33 Orientales',-34.4504,-58.5168)]
out=[]
for n,la,lo in dest:
    cand=sorted([(d(y,x,la,lo),sid,x,y,nm) for sid,(x,y,nm) in stops.items() if serve.get(sid)],key=lambda z:z[0])[:3]
    for dist,sid,x,y,nm in cand[:2]:
        u=f'https://routing.openstreetmap.de/routed-foot/route/v1/driving/{x},{y};{lo},{la}?overview=false'
        try: w=json.load(urllib.request.urlopen(u,timeout=30))['routes'][0]['distance']
        except Exception as ex: w=None
        out.append([n,nm,sid,round(y,5),round(x,5),round(dist),round(w) if w else '',' '.join(sorted(x for x in serve[sid] if x))])
        print(out[-1])
with open(B+'paradas_colectivo_cercanas_costa.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['destino','parada_osm','nodo_osm','lat','lon','recta_m','a_pie_m','lineas_osm']); wr.writerows(out)
