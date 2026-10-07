import re,sys,collections
rows=[l for l in open(sys.argv[1],encoding='utf-8',errors='replace') if 'DGHP' in l]
seen={}
for l in rows:
    m=re.search(r'Nro\. (DISP-\d{4}-\d+-SI-DGHP)',l)
    if not m: continue
    k=m.group(1)
    if k in seen: continue
    f=[x.strip() for x in l.split('|')]
    fecha_bo=f[1]
    ref=l.split(k,1)[1]
    t='OTRO'
    R=ref.upper()
    if 'LICENCIA' in R: t='LICENCIA'
    elif 'EXPR' in R: t='EXPRES'
    elif 'RECHAZ' in R or 'DESIST' in R: t='RECHAZO/DESIST'
    elif 'LOCALIZ' in R: t='LOCALIZACION'
    elif 'BAJA' in R: t='BAJA'
    elif 'TRANSM' in R or 'TRANSF' in R: t='TRANSMISION'
    pdf=re.search(r'https://tesi\.sanisidro\.gob\.ar/boletin/pdf/\S+',l)
    m2=re.search(r'\| (\d\d/\d\d/\d{4}) \|',ref)
    seen[k]=(fecha_bo, m2.group(1) if m2 else '', t, pdf.group(0) if pdf else '')
c=collections.Counter(); cy=collections.Counter(); cpdf=collections.Counter()
for k,(fb,fd,t,p) in seen.items():
    y=k.split('-')[1]; c[t]+=1; cy[(y,t)]+=1
    if p: cpdf[t]+=1
print('total disposiciones DGHP únicas:',len(seen))
print('por tipo:',dict(c)); print('con PDF por tipo:',dict(cpdf))
for k in sorted(cy): print(k,cy[k])
fechas=sorted(set(v[0][-4:]+v[0][3:5] for v in seen.values())); print('meses BO:',fechas[0],fechas[-1])
import json; json.dump(seen,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
