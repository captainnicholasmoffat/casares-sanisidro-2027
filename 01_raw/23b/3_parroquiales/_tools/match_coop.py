import json,csv,re,sys,unicodedata
Z,D=sys.argv[1],sys.argv[2]
def norm(s):
    s=unicodedata.normalize('NFD',s.upper()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^A-Z0-9 ]',' ',s)
coops=json.load(open(Z+'/inaes_coop_PBA_vigentes.json'))
r=[x for x in csv.DictReader(open(D+'/pba_establecimientos_SanIsidro_28092026.csv',encoding='utf-8')) if x['sector']=='Privado']
stop={'COLEGIO','ESCUELA','INSTITUTO','DE','LA','LOS','LAS','DEL','EL','SAN','SANTA','NTRA','NUESTRA','SENORA','JARDIN','INFANTES','N','Nº','EDUCACION','SECUNDARIA','PRIMARIA','CENTRO','FORMACION','INTEGRAL','EDUCACIONAL','Y','ESCOLAR','PRIVADO','NIVEL','INICIAL','MATERNAL','ESPECIAL','SUPERIOR','PROFESORADO','TECNICO','INST'}
names=sorted(set(x['establecimiento_nombre'] for x in r))
hits=[]
for n in names:
    toks=[t for t in norm(n).split() if t not in stop and len(t)>2]
    if not toks: continue
    key=' '.join(toks)
    for c in coops:
        cn=norm(c['Nombre'])
        if re.search(r'\b'+re.escape(key)+r'\b',cn):
            hits.append((n,c['Matricula'],c['Nombre'],c['Localidad'],c['Partido_Depto'],c['Actividad']))
for h in hits: print(' | '.join(map(str,h)))
print('schools',len(names),'hits',len(hits))
kw=re.compile(r'ENSE|EDUC|ESCOL|ESCUEL|COLEGI|INSTITUT|DOCEN|MAESTR|JARDIN|APRENDI|PEDAGOG|CAPACIT')
k=[c for c in coops if kw.search(norm(c['Nombre'])) and c['Partido_Depto'] in ('SAN ISIDRO','VICENTE LOPEZ','SAN FERNANDO (BA)','TIGRE','SAN MARTIN (BA)','GENERAL SAN MARTIN','SAN FERNANDO')]
for c in k: print('VECINO',c['Matricula'],c['Nombre'],'|',c['Localidad'],'|',c['Partido_Depto'],'|',c['Actividad'])
print(sorted(set(c['Partido_Depto'] for c in coops if 'SAN' in c['Partido_Depto'] or 'LOPEZ' in c['Partido_Depto'] or 'TIGRE' in c['Partido_Depto'])))
