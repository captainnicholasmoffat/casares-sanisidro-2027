# [cálculo propio] Propuesta de canon - la inteligencia artificial del Municipio
# Fuentes: pba_establecimientos_SanIsidro_28092026.csv (padrón con % de subvención y matrícula, Relevamiento Inicial 2026)
#          matrícula 2025 DGCyE (dato del cliente): primaria 23.122 (15.142 privada), secundaria 27.711 (16.978 privada)
#          topes PV-2026-26081548 (septiembre 2026); dólar $1.520; IPC INDEC (ipc_indec_mensual.csv)
USD=1520
IPC_dic25=10121.3715; IPC_jul26=12076.3937  # último dato disponible en el archivo (jul-2026)
f_dic25=IPC_dic25/IPC_jul26
pad={ # matrícula Inicial 2026 por tramo (padrón)
 'prim':{'100':1905,'80':1233,'70':1252,'60':2689,'50':0,'40':334,'sin':7070},
 'sec': {'100':2130,'80':5189,'70':645,'60':1005,'50':0,'40':0,'sin':7782}}
secc={'prim':{'100':72,'80':54,'70':58,'60':114,'50':0,'40':12,'sin':325},
      'sec': {'100':76,'80':183,'70':22,'60':30,'50':0,'40':0,'sin':330}}
unid={'prim':{'100':6,'80':4,'70':4,'60':10,'50':0,'40':1,'sin':29},
      'sec': {'100':7,'80':14,'70':2,'60':3,'50':0,'40':0,'sin':31}}
tot2025={'prim':15142,'sec':16978}
total_alumnos_2025=23122+27711
# escalar a 2025
m25={l:{t:pad[l][t]*tot2025[l]/sum(pad[l].values()) for t in pad[l]} for l in pad}
tramo_of={'100':'A','80':'B','70':'B','60':'C','50':'C','40':'C','sin':'DE'}
def agg(d):
    out={'A':0,'B':0,'C':0,'DE':0}
    for l in d:
        for t,v in d[l].items(): out[tramo_of[t]]+=v
    return out
A_pad=agg(pad); A25=agg(m25); A_secc=agg(secc); A_unid=agg(unid)
print('Alumnos prim+sec por tramo (padrón Inicial 2026):',A_pad, sum(A_pad.values()))
print('Alumnos prim+sec por tramo (escalado a 2025):',{k:round(v) for k,v in A25.items()}, round(sum(A25.values())))
print('Secciones por tramo:',A_secc,'Unidades por tramo:',A_unid)
for l in ['prim','sec']:
    tt=sum(pad[l].values())
    print(l,'shares',{t:round(100*v/tt,1) for t,v in pad[l].items()})
# propuesta
canon_alumno_mes={'A':0,'B':1000,'C':2500,'D':10000,'E':25000}
canon_seccion_anio={'A':0,'B':50000,'C':120000,'D':300000,'E':600000}
MESES=10
print('\nCanon alumno por año ($ y US$):',{k:(v*MESES, round(v*MESES/USD,1)) for k,v in canon_alumno_mes.items()})
print('Canon por sección por año (US$):',{k:round(v/USD) for k,v in canon_seccion_anio.items()})
# % de la cuota de referencia (topes septiembre 2026 PV-2026-26081548)
topes_sep={'prim':{'100':38070,'80':70260,'70':89880,'60':134600,'50':156620,'40':172180},
           'sec':{'100':41980,'80':79550,'70':110360,'60':162260,'50':179010,'40':223740}}
for l in topes_sep:
    for t,v in topes_sep[l].items():
        k=tramo_of[t]
        print(f'  {l} {t}%: tope ${v:,} canon ${canon_alumno_mes[k]:,} = {100*canon_alumno_mes[k]/v:.1f}% del tope; 10% del tope (límite Res.34/17 mod. 2381/18 equip. didáctico) = ${0.1*v:,.0f}; tope en $ dic-2025 = ${v*f_dic25:,.0f}')
for ref in [600000,1161860,1764000]:
    print(f'  sin aporte cuota ${ref:,}: D {100*10000/ref:.1f}% / E {100*25000/ref:.1f}%')
# escenarios de reparto sin aporte entre D y E
cost_pa={30:30*USD,100:100*USD}
print('\nCosto total servicio (todos los alumnos prim+sec 2025 =',total_alumnos_2025,')')
for c,v in cost_pa.items(): print(f'  US${c}/alumno/año -> ${v:,}/alumno/año -> total ${v*total_alumnos_2025/1e6:,.1f} M/año (US${c*total_alumnos_2025:,})')
priv_tot=sum(tot2025.values())
for shareE in [0.0,0.5,1.0]:
  for adh in [1.0,0.5]:
    al=dict(A25); al['D']=A25['DE']*(1-shareE); al['E']=A25['DE']*shareE
    se=dict(A_secc); se['D']=A_secc['DE']*(1-shareE); se['E']=A_secc['DE']*shareE
    ing_al=sum(al[k]*canon_alumno_mes[k]*MESES for k in 'ABCDE')*adh
    ing_co=sum(se[k]*canon_seccion_anio[k] for k in 'ABCDE')*adh
    ing=ing_al+ing_co
    print(f'\nEscenario: sin aporte en tramo E={shareE:.0%}, adhesión={adh:.0%}: ingresos alumnos ${ing_al/1e6:,.1f} M + colegios ${ing_co/1e6:,.1f} M = ${ing/1e6:,.1f} M/año (US${ing/USD:,.0f})')
    for c,v in cost_pa.items():
        print(f'   costo US${c}: cubre {100*ing/(v*total_alumnos_2025):.1f}% del costo total (50.833 alumnos) y {100*ing/(v*priv_tot*adh):.1f}% del costo de los alumnos privados que adhieren ({priv_tot*adh:,.0f})')

# ---- Opción 2: canon por alumno indexado al costo (porcentaje del costo por alumno) ----
pct={'A':0,'B':0.2,'C':0.5,'D':1.0,'E':1.5}
print('\n=== Opción 2: canon alumno = % del costo por alumno/año ===')
for c,v in cost_pa.items():
    print(f' costo US${c}: canon alumno/mes (10 meses):',{k:round(v*p/MESES) for k,p in pct.items()})
for shareE in [0.0,0.5,1.0]:
    al=dict(A25); al['D']=A25['DE']*(1-shareE); al['E']=A25['DE']*shareE
    se=dict(A_secc); se['D']=A_secc['DE']*(1-shareE); se['E']=A_secc['DE']*shareE
    for c,v in cost_pa.items():
        ing_al=sum(al[k]*v*pct[k] for k in 'ABCDE')
        ing_co=sum(se[k]*canon_seccion_anio[k] for k in 'ABCDE')
        ing=ing_al+ing_co
        print(f' E={shareE:.0%} costo US${c}: alumnos ${ing_al/1e6:,.1f} M + colegios ${ing_co/1e6:,.1f} M = ${ing/1e6:,.1f} M -> {100*ing/(v*total_alumnos_2025):.1f}% del costo total; {100*ing_al/(v*priv_tot):.1f}% del costo de privados (sólo canon alumnos)')
