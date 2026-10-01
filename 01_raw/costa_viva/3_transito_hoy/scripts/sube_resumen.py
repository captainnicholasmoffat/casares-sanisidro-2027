# Resume usos SUBE por línea y tipo de día (hábil / sábado / domingo) para las semanas extraídas. [cálculo propio]
import csv, glob, datetime, collections
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/sube/'
L={'FFCC_TREN_COSTA':'Tren de la Costa','FCC MITRE_TIGRE':'Mitre ramal Tigre','BSAS_LINEA_060':'Colectivo 60','BSAS_LINEA_168':'Colectivo 168',
   'BSAS_LINEA_228':'Colectivo 228','BSAS_LINEA_343':'Colectivo 343','BSAS_LINEA_365':'Colectivo 365','BSAS_LINEA_371':'Colectivo 371',
   'BSAS_LINEA_338':'Colectivo 338','BSAS_LINEA_314':'Colectivo 314','BSAS_LINEA_430':'Colectivo 430'}
data=collections.defaultdict(dict); prel={}
for f in sorted(glob.glob(B+'sube_usos_*.csv')):
    for r in csv.reader(open(f)):
        if not r or len(r)<10: continue
        lin=r[2].strip()
        for k,v in L.items():
            if lin==k or lin.replace(' ','')==k.replace(' ',''):
                data[r[0]][v]=data[r[0]].get(v,0)+int(r[8]); prel[r[0]]=r[9]
        if '228' in lin and 'BSAS' in lin: data[r[0]]['Colectivo 228']=data[r[0]].get('Colectivo 228',0)+int(r[8])
rows=[]
for d in sorted(data):
    wd=datetime.date.fromisoformat(d).weekday()
    tipo='domingo' if wd==6 else 'sábado' if wd==5 else 'hábil'
    rows.append((d,tipo,prel[d],data[d]))
with open(B+'../sube_usos_lineas_costa_por_dia.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['fecha','tipo_dia','dato_preliminar']+list(dict.fromkeys(L.values())))
    for d,t,p,v in rows: w.writerow([d,t,p]+[v.get(x,'') for x in dict.fromkeys(L.values())])
semanas={'ene-2025 (13-19)':'2025-01','nov-2025 (10-16)':'2025-11','ene-2026 (12-18)':'2026-01','mar-2026 (9-15)':'2026-03','sep-2026 (7-13)':'2026-09'}
print('semana | línea | prom. hábil | sábado | domingo | sáb/hábil | dom/hábil')
for sn,pre in semanas.items():
    for lin in dict.fromkeys(L.values()):
        hab=[v.get(lin) for d,t,p,v in rows if d.startswith(pre) and t=='hábil' and v.get(lin)]
        sab=[v.get(lin) for d,t,p,v in rows if d.startswith(pre) and t=='sábado' and v.get(lin)]
        dom=[v.get(lin) for d,t,p,v in rows if d.startswith(pre) and t=='domingo' and v.get(lin)]
        if not hab: continue
        h=sum(hab)/len(hab); s=sab[0] if sab else None; dm=dom[0] if dom else None
        print(sn,'|',lin,'|',round(h),'|',s,'|',dm,'|',round(s/h,2) if s else '','|',round(dm/h,2) if dm else '')
