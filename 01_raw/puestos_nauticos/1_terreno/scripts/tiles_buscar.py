# Busca en los tiles OSM (API 0.6) ya bajados al repo (01_raw/costa_viva/3_transito_hoy/osm/api_tiles, 2026-10-01) elementos por nombre/etiqueta.
import glob, re, sys, xml.etree.ElementTree as ET
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/01_raw/costa_viva/3_transito_hoy/osm/api_tiles/'
pat=re.compile(sys.argv[1], re.I)
nodes={}; seen=set()
for f in sorted(glob.glob(D+'*.osm')):
    r=ET.parse(f).getroot()
    for n in r.findall('node'):
        nodes[n.get('id')]=(float(n.get('lat')),float(n.get('lon')))
for f in sorted(glob.glob(D+'*.osm')):
    r=ET.parse(f).getroot()
    for e in r:
        if e.tag not in('node','way','relation'): continue
        tags={t.get('k'):t.get('v') for t in e.findall('tag')}
        s=' '.join(f'{k}={v}' for k,v in tags.items())
        if pat.search(s):
            key=(e.tag,e.get('id'))
            if key in seen: continue
            seen.add(key)
            if e.tag=='node': c=(float(e.get('lat')),float(e.get('lon')))
            elif e.tag=='way':
                pts=[nodes[nd.get('ref')] for nd in e.findall('nd') if nd.get('ref') in nodes]
                c=(sum(p[0] for p in pts)/len(pts),sum(p[1] for p in pts)/len(pts)) if pts else None
            else: c=None
            print(e.tag,e.get('id'),c and (round(c[0],5),round(c[1],5)),'|',s[:300])
