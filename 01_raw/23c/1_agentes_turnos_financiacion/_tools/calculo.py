# Cuentas de w1a (agentes, turnos, financiación). Correr: python3 -I calculo.py > calculo_salida.txt
# Plata: pesos de dic-2025 con IPC del repo (dic-2025 = 10121.3715; jul-2026 = 12076.3937 para precios posteriores).
IPC = {"2020-07": 328.2014, "2020-10": 359.6570, "2024-05": 6073.7170, "2025-10": 9603.8623,
       "2025-12": 10121.3715, "2026-07": 12076.3937}
DOLAR = 1447.84
def dic25(monto, mes):
    return monto * IPC["2025-12"] / IPC[mes]
def p(t, *a):
    print(t, *a)

p("=== 1. CARGOS POR PROGRAMA (F6 Presupuesto 2026, Ord. 9422) ===")
fisc = dict(sup_dirgral=4, sup_subsec=1, jer13=5, jer14=4, jer15=2, jer16=1, prof12=4,
            adm7=4, adm8=2, adm9=6, adm11=4, adm13=2, serv6=3, serv7=2, serv8=3, serv9=15, serv10=9, mens=49)
tot = sum(fisc.values())
mando = fisc["sup_dirgral"] + fisc["sup_subsec"] + fisc["jer13"] + fisc["jer14"] + fisc["jer15"] + fisc["jer16"]
adm = fisc["adm7"] + fisc["adm8"] + fisc["adm9"] + fisc["adm11"] + fisc["adm13"]
serv = fisc["serv6"] + fisc["serv7"] + fisc["serv8"] + fisc["serv9"] + fisc["serv10"]
p("Fiscalización (Sec. Gobierno): total", tot, "| conducción (superior+jerárquico)", mando, "| profesional", fisc["prof12"],
  "| administrativo", adm, "| servicio", serv, "| mensualizados", fisc["mens"])
piso = serv + fisc["mens"]
techo = tot - mando
p("Inspectores de comercio/ACSI: piso (servicio+mensualizados) =", piso, "; techo (todo menos conducción) =", techo)
patr = dict(jer15=2, adm7=1, adm8=1, adm11=1, obr7=1, serv7=2, serv8=77, serv9=17, mens=257)
p("Patrullaje (Sec. Seguridad): total", sum(patr.values()), "| calle (servicio+mensualizados) =", patr["serv7"]+patr["serv8"]+patr["serv9"]+patr["mens"])
mov = dict(subsec=1, jer14=1, jer15=1, adm7=1, adm9=1, adm10=1, adm12=2, obr8=2, serv7=1, serv8=36, serv9=27, mens=103)
p("Gestión de la Política de Movilidad: total", sum(mov.values()), "| servicio+mensualizados =", mov["serv7"]+mov["serv8"]+mov["serv9"]+mov["mens"],
  "| el Municipio dice 120 agentes de tránsito (03/08/2026)")
p("Monitoreo y videovigilancia: 158 (el Municipio dice 145 de monitoreo)")
p("Secretaría de Seguridad total: 14+92+5+158+359 =", 14+92+5+158+359)
p("Gobierno total: 15+100+120+16+20+29+43 =", 15+100+120+16+20+29+43)
p("Comparación 2024 (F6 Ord. presupuesto 2024): Inspección General 92 -> Fiscalización 2026 120: +%.0f%%" % ((120/92-1)*100))
p("                                            Tránsito 112 -> Política de Movilidad 2026 177: +%.0f%%" % ((177/112-1)*100))

p("\n=== 2. COSTO ANUAL = 13 BÁSICOS (verificación) ===")
for nombre, n, costo in [("Serv. cat 9 35h (Fiscalización)", 15, 97659962), ("Serv. cat 8 35h (Patrullaje)", 77, 477453657),
                         ("Serv. cat 8 35h (Movilidad)", 36, 223225086), ("Mensualizados Fiscalización", 49, 526621797),
                         ("Mensualizados Patrullaje", 257, 1526057130), ("Mensualizados Movilidad", 103, 632102458)]:
    p("%-35s por cargo y año %12.0f | por mes (÷13) %10.0f" % (nombre, costo/n, costo/n/13))
p("Escala Dec. 782/2026 (julio 2026): cat 8 35h = 524.675; cat 9 35h = 550.902 ; Presupuesto (oct-2025): cat 8 = %.0f, cat 9 = %.0f -> aumento %.1f%% y %.1f%%" %
  (6200697/13, 6510664/13, (524675/(6200697/13)-1)*100, (550902/(6510664/13)-1)*100))

p("\n=== 3. HORAS ===")
for reg, dias in [(35, 5), (40, 5), (48, 6)]:
    p("Régimen %d h/semana: %.2f h por día en %d días; horas al mes (x4,4) = %.1f -> divisor art. 10 Ord. 9422" % (reg, reg/dias, dias, reg*4.4))
p("Puesto de patrulla cubierto 24x7 = 168 h/semana -> agentes por puesto con 35 h: %.1f ; con 48 h: %.1f (sin contar francos, licencias ni vacaciones)" % (168/35, 168/48))
for mbps in (1.5, 2.0):
    gb_h = mbps*1e6/8*3600/1e9
    for (h, d, etiqueta) in [(7, 22, "35 h (7 h x 22 días)"), (8, 26, "48 h (8 h x 26 días)")]:
        p("Grabación de todo el turno a %.1f Mbps, %s: %.2f GB por turno; %.0f GB por mes por agente" % (mbps, etiqueta, gb_h*h, gb_h*h*d))
# subida por wifi en base: cuántos Gbps hacen falta si N agentes descargan su turno en 30 min
for n in (60, 120):
    for gb in (4.7, 7.2):
        p("Subida en base: %d agentes x %.1f GB en 30 min = %.1f Gbps" % (n, gb, n*gb*8/1800))

p("\n=== 4. FINANCIACIÓN: PRECEDENTES EN PESOS DE DIC-2025 ===")
p("PC Docente (oct-2020): tope $150.000 = %.0f ; Banco Nación $2.670 M = %.0f M ; aporte Educación $70 M = %.0f M" %
  (dic25(150000, "2020-10"), dic25(2670e6, "2020-10")/1e6, dic25(70e6, "2020-10")/1e6))
p("   subsidio de Educación / fondos del banco = %.1f%% ; descuento de las empresas: 20%% del valor" % (70/2670*100))
# cuota de un préstamo francés 36 meses al 12% TNA
i = 0.12/12; n = 36
cuota = 150000*i/(1-(1+i)**-n)
p("   cuota 36 meses al 12%% TNA de $150.000 (oct-2020) = $%.0f = %.0f de dic-2025" % (cuota, dic25(cuota, "2020-10")))
pc_a27 = 925999; naldo_a27 = 799999
p("Provincia Compras (Banco Provincia), Galaxy A27 5G 8/256 (oct-2026): $%d = %.0f de dic-2025; 24 cuotas sin interés de $%.0f = %.0f de dic-2025" %
  (pc_a27, dic25(pc_a27, "2026-07"), pc_a27/24, dic25(pc_a27/24, "2026-07")))
p("   vs. contado en Naldo $%d (oct-2026, material previo) = %.0f -> el precio en cuotas es %.1f%% más alto" %
  (naldo_a27, dic25(naldo_a27, "2026-07"), (pc_a27/naldo_a27-1)*100))
p("   cuota / básico cat 8 35h (jul-2026, $524.675): %.1f%% ; con jornada prolongada 30%% (básico x1,3): %.1f%%" %
  (pc_a27/24/524675*100, pc_a27/24/(524675*1.3)*100))
p("Samsung EE.UU., empleados públicos: hasta 30%% de descuento -> sobre $%d serían $%.0f menos (%.0f de dic-2025) [supuesto de que se replicara en Argentina]" %
  (naldo_a27, naldo_a27*0.30, dic25(naldo_a27*0.30, "2026-07")))
p("Estipendio EE.UU. por usar el teléfono propio: US$45 por mes (Capitola, Prosser) = $%.0f de dic-2025 por mes = $%.0f por año" % (45*DOLAR, 45*DOLAR*12))
p("General Pueyrredon (Dec. 557/2021): tope de tasa = promedio BCRA de préstamos personales x 1,30; gasto administrativo para el Municipio 2% de lo retenido")
p("Cuota Simple (2024): tasa = TPM BCRA x 1,25 = 40%% x 1,25 = %.0f%% (según prensa); perdió vigencia (Res. SIC 12/2026)" % (40*1.25))

p("\n=== 5. UNIVERSO DE LA PRIMERA ETAPA (inspectores + tránsito) ===")
p("Inspectores de comercio/ACSI 81 a 103 + tránsito 120 (según el Municipio) a 167 (F6, servicio+mensualizados) = %d a %d" % (81+120, 103+167))
p("Con Habilitaciones y Permisos (29 cargos, todos) el techo sería %d" % (103+167+29))
p("Carga de trabajo programada 2026, Programa 53: (10.000 fiscalizaciones de comercios + 610 de obras) / inspectores = %.0f a %.0f por inspector y año; por día hábil (220): %.2f a %.2f" %
  (10610/103, 10610/81, 10610/103/220, 10610/81/220))
p("Patrulla (segunda etapa): 359 cargos de Patrullaje (F6) ; 300 oficiales en la calle (según el Municipio, jun-2026)")
p("Grabación de todo el turno frente a los supuestos previos (59 GB/mes con 4 h y 119 GB/mes con 6 h): 104/59 = %.2f ; 187/119 = %.2f" % (104/59, 187/119))
