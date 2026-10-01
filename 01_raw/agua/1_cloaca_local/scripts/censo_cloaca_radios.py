# Cobertura de desagüe cloacal por radio censal, San Isidro, Censo 2022 (INDEC, Redatam).
# Lee (solo lectura) data/censo2022_sanisidro_por_radio.csv y data/radios_censales_sanisidro.geojson del repo.
import csv, json
R='/home/user/casares-sanisidro-2027/data/'
rows={r['radio_id']:r for r in csv.DictReader(open(R+'censo2022_sanisidro_por_radio.csv',encoding='utf-8-sig'))}
g=json.load(open(R+'radios_censales_sanisidro.geojson'))
def centroid(geom):
    cs=geom['coordinates']
    pts=[]
    def walk(c):
        if isinstance(c[0],(int,float)): pts.append(c)
        else:
            for x in c: walk(x)
    walk(cs)
    return sum(p[1] for p in pts)/len(pts), sum(p[0] for p in pts)/len(pts)
cent={f['properties']['radio_id']:centroid(f['geometry']) for f in g['features']}
area={f['properties']['radio_id']:f['properties'].get('area_fuente') for f in g['features']}
zon={}
try:
    for r in csv.DictReader(open(R+'zonas_asignacion_radios.csv',encoding='utf-8-sig')):
        zon[r.get('radio_id')]=r
except Exception as e: pass
out=[]; T=dict(tot=0,red=0,cam=0,pozo=0,hoyo=0,na=0)
for rid,r in rows.items():
    if r.get('nivel_geografico','radio')!='radio' and not rid.startswith('06756'): continue
    def v(k):
        x=r.get(k,'') or '0'
        try: return int(float(x))
        except: return 0
    tot=v('hogares_desague__total'); red=v('hogares_desague__a_red_publica_cloaca')
    cam=v('hogares_desague__a_camara_septica_y_pozo_ciego'); pozo=v('hogares_desague__solo_a_pozo_ciego')
    hoyo=v('hogares_desague__a_hoyo_excavacion_en_la_tierra_etc'); na=v('hogares_desague__no_aplica')
    for k,x in zip(['tot','red','cam','pozo','hoyo','na'],[tot,red,cam,pozo,hoyo,na]): T[k]+=x
    lat,lon=cent.get(rid,(None,None))
    out.append(dict(radio_id=rid,hogares=tot,red_publica=red,camara_septica_pozo=cam,solo_pozo=pozo,hoyo=hoyo,no_aplica=na,
        pct_red=round(100*red/tot,1) if tot else '',sin_red=tot-red,lat=round(lat,5) if lat else '',lon=round(lon,5) if lon else '',
        zona=(zon.get(rid) or {}).get('zona','')))
out.sort(key=lambda d:(d['pct_red'] if d['pct_red']!='' else 999))
with open('../censo2022_cloaca_por_radio_sanisidro.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('TOTAL', T, 'pct red', round(100*T['red']/T['tot'],2))
print('radios', len(out))
for d in out[:30]: print(d)
import collections
b=collections.Counter()
for d in out:
    p=d['pct_red']
    if p=='' : b['sin hogares']+=1
    elif p<50: b['<50']+=1
    elif p<80: b['50-80']+=1
    elif p<95: b['80-95']+=1
    else: b['>=95']+=1
print(b)
