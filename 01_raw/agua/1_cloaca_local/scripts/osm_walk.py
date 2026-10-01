# Recorre en la API 0.6 de OpenStreetMap las vías waterway conectadas al "Desagüe Dardo Rocha" (way 1503479052).
import urllib.request, xml.etree.ElementTree as ET, json, math, time, sys
API='https://api.openstreetmap.org/api/0.6/'
H={'User-Agent':'research-sanisidro/1.0'}
def get(p):
    for i in range(3):
        try:
            return ET.fromstring(urllib.request.urlopen(urllib.request.Request(API+p,headers=H),timeout=60).read())
        except Exception as e:
            time.sleep(2)
    return None
seen={}; nodes={}; queue=[1503479052]; req=0
while queue and req<150:
    wid=queue.pop(0)
    if wid in seen: continue
    t=get('way/%d/full'%wid); req+=1
    if t is None: continue
    for n in t.findall('node'): nodes[n.get('id')]=(float(n.get('lat')),float(n.get('lon')))
    w=[x for x in t.findall('way') if x.get('id')==str(wid)][0]
    tags={x.get('k'):x.get('v') for x in w.findall('tag')}
    nds=[x.get('ref') for x in w.findall('nd')]
    seen[wid]=dict(tags=tags,nds=nds)
    for end in (nds[0],nds[-1]):
        t2=get('node/%s/ways'%end); req+=1
        if t2 is None: continue
        for w2 in t2.findall('way'):
            tg={x.get('k'):x.get('v') for x in w2.findall('tag')}
            if 'waterway' in tg and int(w2.get('id')) not in seen:
                queue.append(int(w2.get('id')))
def L(nds):
    pts=[nodes[n] for n in nds if n in nodes]
    return sum(math.hypot((a[0]-b[0])*111.32,(a[1]-b[1])*111.32*math.cos(math.radians(34.5))) for a,b in zip(pts,pts[1:]))
tot=0
res=[]
for wid,d in seen.items():
    l=L(d['nds']); tot+=l
    a=nodes.get(d['nds'][0]); b=nodes.get(d['nds'][-1])
    res.append(dict(way=wid,name=d['tags'].get('name',''),waterway=d['tags'].get('waterway'),tunnel=d['tags'].get('tunnel',''),km=round(l,3),start=a,end=b))
for r in res: print(r)
print('ways',len(seen),'km total',round(tot,2),'requests',req)
json.dump(dict(ways=res,nodes={k:v for k,v in nodes.items()}),open('osm_dardo_rocha_network.json','w'))
