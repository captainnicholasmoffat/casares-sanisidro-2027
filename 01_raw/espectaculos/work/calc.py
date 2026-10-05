import csv,sys
O=sys.argv[1]
def p(x): return "$"+f"{round(x):,}".replace(",",".")
rows=[("concepto","base","cantidad","resultado","nota")]
t=246
for m2,lab in [(2,"2 m2 (superficie de Melbourne, área general)"),(4,"4 m2 (dúo o trío)"),(5,"5 m2 (módulo CABA Ley 4950 art. 5 h)"),(10,"10 m2 (ronda o 'circle act')"),(30,"30 m2 (teatro de calle chico)")]:
    rows.append((f"Tasa art. 17 d.1 Impositiva 2026 por día, {lab}","$246 por m2 y por día",f"{m2} m2",p(m2*t),"[cálculo propio]; que la tasa se aplique a artistas: inferencia"))
dias=round(52/12*4,1)
for m2 in (2,5,10):
    rows.append((f"Tasa art. 17 d.1, lunes a jueves de todo un mes ({dias} días promedio), {m2} m2","$246 por m2 y por día",f"{m2} m2 x {dias} días",p(m2*t*dias),"[cálculo propio]"))
rows.append(("Ferias artesanales (art. 17 f) llevado a mes","$22.500 por puesto y por trimestre","1 puesto","$7.500 por mes","[cálculo propio]"))
for area in (600,1500,9500):
    rows.append((f"Capacidad con la regla ACSI de 1 persona cada 3 m2, área de {area} m2","1 persona / 3 m2",f"{area} m2",f"{area//3} personas","[cálculo propio]; regla del permiso RS-2026-2 (Expo Mate); 9.500 m2 = predio de Expo Mate 2026 según el Municipio"))
smam=475886
for art,mn,mx,fmn,fmx in [("art. 81 ruidos molestos (con intimación previa)","$500","$100.000",0.025,20),("art. 123 espectáculo sin permiso","$2.000","$300.000",0.1,60),("art. 137 venta ambulante sin permiso","$2.000","$250.000",0.1,50),("art. 145 ocupación indebida de plazas o riberas","$1.000","$250.000",0.05,50)]:
    rows.append((f"Ord. 5182 {art}: multa {mn} a {mx} en módulos de la Ord. 5939","módulo = $475.886 (valor 35 h desde 1/7/2026 tomado del informe de ruidos)",f"{fmn} a {fmx} módulos",p(fmn*smam)+" a "+p(fmx*smam),"[cálculo propio]; $500 no figura en la tabla de la Ord. 5939 (se tomó la mitad de $1.000 = 1/20); necesita dictamen de un abogado"))
rows.append(("Tránsito para eventos no oficiales (Impositiva 2026 art. 27 d)","$7.000 por hora-hombre lunes a viernes 8 a 20 h; $10.500 en otros horarios","2 agentes de 18 a 22 h un martes","2x2x7.000 + 2x2x10.500 = $70.000","[cálculo propio]; ejemplo de un corte de calle chico"))
with open(O+"/CALCULO_PROPIO_tasas_multas_capacidad.csv","w",newline="") as f:
    csv.writer(f,delimiter=";").writerows(rows)
for r in rows: print(" | ".join(map(str,r)))
