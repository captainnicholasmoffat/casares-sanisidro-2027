# Cálculo propio: rubro 1.2.6 MULTAS, ejecución presupuestaria de recursos MSI (devengado = percibido en todos los renglones)
import csv
ipc={}
for r in csv.DictReader(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/data/ipc_indec_mensual.csv')):
    ipc[(int(r['anio']),int(r['mes']))]=float(r['indice'])
DIC25=10121.3715
R=['1.2.6.01 Multas por contravenciones','1.2.6.02 Infracción a obligaciones y deberes fiscales','1.2.6.03 Otras multas, recargos e intereses','1.2.6.04 Otras multas en vía pública']
# percibido por trimestre (pesos corrientes); Q4 = anual - (Q1+Q2+Q3)
q={
 (2024,1):[150165957.82,18759716.86,278456852.77,89256364.40],
 (2024,2):[342520346.89,33348098.96,305495962.19,182847789.62],
 (2024,3):[-320611918.05,48729174.58,468873817.22,1042282453.33],
 (2025,1):[98914384.00,328374424.61,1000846390.94,784086648.70],
 (2025,2):[147360148.00,110782915.25,949486128.20,943023648.88],
 (2025,3):[130997495.16,118885618.07,663541861.67,876060850.80],
 (2026,1):[135862843.50,62628371.82,766047130.19,608868008.34],
 (2026,2):[193970198.00,50799363.42,985736725.86,664621168.81],
}
anual={2024:[280331632.70,220149914.92,1419622770.68,2207909477.16],2025:[535746200.27,644006624.31,3315368035.58,3361831639.00]}
estim={2024:[98742000,82756000,1135192000,671754000],2025:[309588923,181421627,1894223119,2364788520],2026:[504094275,745632435,3392543882,3478242894]}
vig={2024:[98742000,82756000,1135192000,1314754000],2025:[481599318,629856812,3170290092,3220424926]}
for y in (2024,2025):
    q[(y,4)]=[anual[y][i]-sum(q[(y,t)][i] for t in (1,2,3)) for i in range(4)]
def coef(y,t):
    ms=[(y,m) for m in range(3*t-2,3*t+1)]
    return DIC25/(sum(ipc[k] for k in ms)/3)
out=csv.writer(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/m2_san_isidro_hoy/calculos/recaudacion_multas_2024_2026.csv','w'))
out.writerow(['anio','trimestre','rubro','percibido_pesos_corrientes','coef_a_dic2025_(IPC_prom_trim)','percibido_pesos_dic2025','fuente'])
fu={2024:'2024_i/ii/iii_recursos.pdf; IV derivado de 2024_iv_recursos_-_anual.pdf',2025:'2025_i/ii/iii_recursos.pdf; IV derivado de 2025_iv_recursos.pdf',2026:'2026_i_recursos.pdf, 2026_ii_recursos.pdf'}
tot={}
for (y,t) in sorted(q):
    c=coef(y,t)
    for i,rn in enumerate(R):
        v=q[(y,t)][i]; out.writerow([y,t,rn,round(v,2),round(c,4),round(v*c,0),fu[y]])
        tot.setdefault(y,[0,0,0,0]); tot[y][i]+=v*c
print('Coeficientes trimestrales:',{k:round(coef(*k),3) for k in sorted(q)})
print('\nTotales anuales en pesos de dic-2025 (suma de trimestres deflactados):')
for y in sorted(tot):
    print(y,[round(x/1e6,1) for x in tot[y]],'total',round(sum(tot[y])/1e6,1))
print('\nTrimestres Q4 derivados:',{y:[round(x/1e6,1) for x in q[(y,4)]] for y in (2024,2025)})
print('\nTotal nominal por trimestre (M$):',{k:round(sum(v)/1e6,1) for k,v in sorted(q.items())})
print('Tránsito-candidatos (01+04) por trimestre, M$ dic-2025:',{k:round((q[k][0]+q[k][3])*coef(*k)/1e6,1) for k in sorted(q)})
print('Nominal 01+04 anual:',{y:round((anual[y][0]+anual[y][3])/1e6,1) for y in anual})
# estimado anual a dic-2025 usando IPC promedio anual
for y in (2024,2025,2026):
    ms=[(y,m) for m in range(1,13) if (y,m) in ipc]
    c=DIC25/(sum(ipc[k] for k in ms)/len(ms))
    print('Estimado',y,'total nominal M$',round(sum(estim[y])/1e6,1),'coef prom',round(c,3),'(meses usados',len(ms),')')
