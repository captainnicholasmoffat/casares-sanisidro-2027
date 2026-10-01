# Une las teselas del API de OSM en un solo diccionario (nodos, vías, relaciones con etiquetas).
import glob, pickle, xml.etree.ElementTree as ET
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/osm/'
N={};W={};R={}
for f in sorted(glob.glob(B+'api_tiles/*.osm')):
    for ev,el in ET.iterparse(f):
        if el.tag=='node':
            N[int(el.get('id'))]=(float(el.get('lon')),float(el.get('lat')),{t.get('k'):t.get('v') for t in el.findall('tag')}, el.get('timestamp'))
        elif el.tag=='way':
            W[int(el.get('id'))]=([int(n.get('ref')) for n in el.findall('nd')],{t.get('k'):t.get('v') for t in el.findall('tag')}, el.get('timestamp'))
        elif el.tag=='relation':
            R[int(el.get('id'))]=([(m.get('type'),int(m.get('ref')),m.get('role')) for m in el.findall('member')],{t.get('k'):t.get('v') for t in el.findall('tag')}, el.get('timestamp'))
        if el.tag in ('node','way','relation'): el.clear()
pickle.dump((N,W,R),open(B+'tiles_all.pkl','wb'))
print(len(N),len(W),len(R))
