# Informe 23 quinquies, punto 2: al aire libre del 20 de septiembre al 15 de abril; el resto del año, bajo techo (decisión de Nick).
# Pesos de dic-2025. Insumos verificados en los informes 23 ter y 23 quáter (cachet promedio, % de días con alerta por mes,
# factor 0,6 «sólo la alerta del horario», costo de abrir un espacio municipal y aportes mensuales a clubes).
import datetime as dt
CACHET=0.980112                     # M por show (piso SADEM + 25%, mezcla 40/30/30)
ALERTA={'central':[13,14,10,10,6,4,4,8,7,12,11,13],'bajo':[5,7,5,5,4,1,1,3,3,4,3,4],'alto':[20,21,14,14,8,7,6,13,11,19,19,22]}
HORARIO=0.6
C_MUNI=145128/1e6                   # M por show en espacio municipal (3 agentes 6 h + luz y calefacción)
APORTE={'central (Bahía Blanca)':0.621728,'bajo (Patagones)':0.411176,'alto (Patagones, club grande)':0.856616}  # M por salón y por mes
SOLISTAS=0.40
dias=[dt.date(2027,1,1)+dt.timedelta(d) for d in range(365)]
afuera=[x for x in dias if (x.month,x.day)>=(9,20) or (x.month,x.day)<=(4,15)]
techo=[x for x in dias if x not in afuera]
n_af=200*len(afuera)/365; n_te=200*len(techo)/365
print(f"Días al aire libre {len(afuera)}, bajo techo {len(techo)} -> shows al aire libre {n_af:.1f}, bajo techo {n_te:.1f}")
meses_techo=len(techo)/(365/12)
sol=n_te*SOLISTAS; resto=n_te-sol
print(f"Bajo techo: {sol:.1f} solistas en espacios municipales y {resto:.1f} dúos, tríos y bandas en clubes; {meses_techo:.2f} meses")
for salones in (4,5,6):
    print(f"  con {salones} salones: {resto/(salones*meses_techo):.1f} shows por salón y por mes")
for k,a in APORTE.items():
    sal=4*meses_techo*a; tot=sol*C_MUNI+sal
    print(f"Salas, aporte {k}: municipales {sol*C_MUNI:.1f} M + 4 clubes {sal:.1f} M = {tot:.1f} M por año")
for esc,a in ALERTA.items():
    extra=sum(CACHET*(200/365)*(0.7*p+0.7*p*p) for x in afuera for p in [a[x.month-1]/100*HORARIO])
    print(f"Cachets, alertas {esc}: 196,0 M + cancelaciones {extra:.1f} M = {196.0+extra:.1f} M")
