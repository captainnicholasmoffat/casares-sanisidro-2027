import re,html,glob,os
rows={}
for f in sorted(glob.glob('sanisidro_novedades_listado/p*.html'),key=lambda x:int(re.findall(r'p(\d+)',x)[-1])):
    t=open(f,encoding='utf-8',errors='ignore').read()
    # split by views-row
    parts=re.split(r'<div class="views-row ',t)
    for p in parts[1:]:
        m=re.search(r'<h2><a href="(/novedades/[^"]+)">(.*?)</a></h2>',p,re.S)
        if not m: continue
        href,title=m.group(1),html.unescape(re.sub('<[^>]+>','',m.group(2))).strip()
        d=re.search(r'(20[12]\d-[01]\d-[0-3]\d)',p) or re.search(r'(\d{2}-\d{2}-20\d{2})',p)
        area=re.search(r'field-name-field-area-noticia.*?field-item even">(.*?)</div>',p,re.S)
        txt=re.sub(r'(?is)<(script|style).*?</\1>',' ',p); txt=html.unescape(re.sub('<[^>]+>',' ',txt)); txt=re.sub(r'\s+',' ',txt)
        summ=txt.replace(title,'').strip()[:300]
        key=href
        if key not in rows:
            rows[key]=(d.group(1) if d else '',area.group(1).strip() if area else '',title,'https://www.sanisidro.gob.ar'+href,summ,os.path.basename(f))
with open('sanisidro_novedades_indice_2020-2026.tsv','w') as o:
    o.write('fecha\tarea\ttitulo\turl\tresumen\tpagina_listado\n')
    for r in sorted(rows.values(),key=lambda r:r[0],reverse=True):
        o.write('\t'.join(x.replace('\t',' ') for x in r)+'\n')
print(len(rows))
