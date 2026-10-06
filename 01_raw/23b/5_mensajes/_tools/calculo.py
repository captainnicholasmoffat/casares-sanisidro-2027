#!/usr/bin/env python3
# z6_sms - "Avisar antes de multar": precio del SMS, cantidad de avisos, quien no usa la IA y costo anual.
# Pesos de dic-2025: IPC del repo (copia_ipc_indec_mensual.csv). Dolar: $1.447,84 (BCRA A 3500, promedio dic-2025).
# Uso: python3 -I calculo.py > calculo_salida.txt
import csv, os

Z = "/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23b_raw/z6_sms/"
IPC = {}
with open(Z + "copia_ipc_indec_mensual.csv") as f:
    for r in csv.DictReader(f):
        IPC[(int(r["anio"]), int(r["mes"]))] = float(r["indice"])
DIC25 = IPC[(2025, 12)]
assert abs(DIC25 - 10121.3715) < 1e-6
USD = 1447.84
IVA = 1.21

def a_dic25(pesos, anio, mes):
    return pesos * DIC25 / IPC[(anio, mes)]

def m(x):  # millones de pesos
    return f"{x/1e6:,.1f} M".replace(",", "X").replace(".", ",").replace("X", ".")

def p(x, d=1):
    s = f"{x:,.{d}f}"
    return "$" + s.replace(",", "X").replace(".", ",").replace("X", ".")

print("=" * 100)
print("1. PRECIO POR SMS, EN PESOS DE DIC-2025")
print("=" * 100)
print(f"IPC dic-2025 = {DIC25}; dolar = {USD}; IVA 21% sobre precios de lista que lo excluyen")
rows = []

# --- Compras publicas (precios con impuestos incluidos segun pliego) ---
# ANSES 63-0018-LPU19: dictamen 31/10/2019, ofertas 28/08/2019. Precio unitario por SMS, pesos, 12 M SMS por renglon.
for oferente, pu in [("Telefonica Moviles (Movistar)", 1.35), ("Telecom (Personal)", 1.60)]:
    v = a_dic25(pu, 2019, 8)
    rows.append(("ANSES 2019, adjudicado (dictamen 31/10/2019) - " + oferente, "12.000.000 SMS", f"${pu:.2f} (ago-2019)", v, "con impuestos [probable]"))

# JGM 2023 (79/6-0009-LPU23): abono 12 meses x hasta 2 M + 24 M adicionales = hasta 48 M SMS. Apertura 11/04/2023.
q_max = 12 * 2_000_000 + 24_000_000
assert q_max == 48_000_000
teleprom23 = 1_770_000 / q_max * USD
atx23 = a_dic25(275_040_000 / q_max, 2023, 4)
rows.append(("JGM 2023, oferta Teleprom (US$1.770.000 / 48 M)", "hasta 48 M", f"US${1_770_000/q_max:.4f}", teleprom23, "oferta; si se usa todo el cupo"))
rows.append(("JGM 2023, oferta ATX ($275.040.000 / 48 M)", "hasta 48 M", f"${275_040_000/q_max:.2f} (abr-2023)", atx23, "oferta; si se usa todo el cupo"))

# JGM 2025/26 (142/3-0035-LPU25, Mi Argentina, BIRF 9455): mismas cantidades. Apertura 27/01/2026. Precios con impuestos (pliego 2.3.2).
of26 = [("Movilgate", 936_015.24), ("Impresores So Mi Al", 1_401_943.80), ("ATX", 1_841_136.00),
        ("Plus Mobile Communications", 2_387_940.00), ("Teleprom Argentina", 2_784_000.00)]
for n, tot in of26:
    u48 = tot / q_max
    u24 = tot / 24_000_000
    rows.append((f"JGM 2026 (Mi Argentina), oferta {n}", "hasta 48 M", f"US${u48:.4f} (48 M) / US${u24:.4f} (24 M)", u48 * USD, "oferta; con impuestos; sin adjudicacion publicada"))

# Bahia Blanca (municipio PBA), estacionamiento medido:
bb24 = 1_117_862.60 / 25_000
rows.append(("Bahia Blanca, Skillmedia, abr-2024 (abono 25.000 SMS; factura B)", "25.000-35.000/mes", f"${bb24:.2f} (abr-2024)", a_dic25(bb24, 2024, 4), "pagado; con IVA [probable]"))
bb25 = [(2025, 3, 2_601_977.69, 41_099), (2025, 4, 1_021_506.85, 16_135), (2025, 5, 179_673.78, 2_838)]
for an, me, imp, q in bb25:
    u = imp / q
    rows.append((f"Bahia Blanca, Movilgate, SMS excedentes {me:02d}/{an}", f"{q:,} excedentes".replace(",", "."), f"${u:.2f}", a_dic25(u, an, me), "pagado; con IVA [probable]"))

# --- Precios de lista internacionales (sin impuestos), destino Argentina, consultados 06/10/2026 ---
lista = [("Sinch (lista, 02/10/2026)", 0.0906), ("AWS End User Messaging (transaccional)", 0.09449),
         ("Infobip (promedio de redes)", 0.097), ("Twilio (todas las redes)", 0.1034),
         ("Plivo, Movistar (la mas barata)", 0.0795), ("Plivo, Personal (la mas cara)", 0.1400),
         ("ClickSend Enterprise (recarga desde US$10.000)", 0.1025), ("ClickSend Scale (desde US$3.000)", 0.1089),
         ("ClickSend Growth (desde US$500)", 0.1245), ("ClickSend Boost (desde US$20)", 0.1381)]
for n, u in lista:
    rows.append((n, "por mensaje, sin compromiso", f"US${u:.4f} + IVA", u * USD * IVA, "lista; IVA 21% agregado [inferencia]"))

print(f"{'Fuente':78s} | {'Volumen':28s} | {'Precio original':38s} | {'$ dic-2025':>9s} | Nota")
for n, vol, orig, v, nota in rows:
    print(f"{n:78s} | {vol:28s} | {orig:38s} | {v:9.1f} | {nota}")

print()
print("Compras publicas: JGM 2026 por SMS si se usa todo el cupo (48 M) va de "
      f"US${of26[0][1]/q_max:.4f} a US${of26[-1][1]/q_max:.4f}; mediana de 5 ofertas = US${sorted(t for _, t in of26)[2]/q_max:.4f}")
print(f"Si solo se usa la mitad (24 M, el abono), el precio efectivo se duplica: US${of26[0][1]/24e6:.4f} a US${of26[-1][1]/24e6:.4f}")

# Precios elegidos para el costo (pesos dic-2025, con IVA)
PRECIO = {
    "bajo": sorted(t for _, t in of26)[2] / q_max * USD,  # mediana de las 5 ofertas JGM 2026 (compra grande o convenio)
    "medio": a_dic25(63.31, 2025, 4),         # proveedor local, volumen municipal, 2025 (Bahia Blanca, Movilgate)
    "alto": 0.1381 * USD * IVA,               # lista internacional sin compromiso (ClickSend Boost) + IVA
}
print("\nPrecio por SMS usado en el costo ($ dic-2025, con IVA):", {k: round(v, 1) for k, v in PRECIO.items()})

print()
print("=" * 100)
print("2. CUANTOS AVISOS POR ANO")
print("=" * 100)
ACTAS_HOY = 244_000      # informe 23, A4 bis (y informe 19: estimacion de actas labradas 2024)
TRATADAS_2024 = 218_720  # informe 19: infracciones tratadas por el Juzgado de Faltas en 2024 (todas las faltas)
pd_tot, pd_first = 2_057_280, 1_748_184  # PennDOT, totales del programa 2020-2025
print(f"PennDOT (aviso en la primera infraccion): primeras infracciones = {pd_first/pd_tot:.1%} del total; reincidencias = {1-pd_first/pd_tot:.1%}")
AVISOS = {
    # bajo: la mitad de las actas de hoy: se juntan las pasadas antes del aviso (una sola multa) y el aviso disuade
    "bajo": round(ACTAS_HOY * 0.50),
    # medio: 25% menos que hoy por las mismas dos razones
    "medio": round(ACTAS_HOY * 0.75),
    # alto: el techo que dio el cliente (cada acta validada hoy genera un aviso)
    "alto": ACTAS_HOY,
}
for k, v in AVISOS.items():
    print(f"  {k:5s}: {v:,} avisos por ano".replace(",", "."))
print(f"  Referencia: infracciones tratadas 2024 = {TRATADAS_2024:,}; rango del informe 19 para actas labradas: 13.000 a 456.000".replace(",", "."))
print(f"  Personas distintas (si 85% de los avisos son a quien no reincide, como PennDOT): medio ~ {AVISOS['medio']*pd_first/pd_tot:,.0f}".replace(",", "."))

print()
print("=" * 100)
print("3. QUIEN NO USARIA LA INTELIGENCIA ARTIFICIAL DEL MUNICIPIO")
print("=" * 100)
si_tot, si_cel, si_sin_cel = 295_978, 280_465, 15_513
si_sin_nada = 9_257  # sin celular con internet y sin internet en la vivienda
print(f"Censo 2022 San Isidro: con celular con internet {si_cel/si_tot:.1%}; sin celular con internet {si_sin_cel/si_tot:.1%}; "
      f"sin celular con internet ni internet en la vivienda {si_sin_nada/si_tot:.1%}")
print("EPH 4T2024 (31 aglomerados): 65 y mas: usa internet 74,2%, celular 85,1% -> usa celular pero no internet ~ "
      f"{85.1-74.2:.1f} puntos; partidos del GBA (4 anos y mas): no usa internet 11,1%, no usa celular 10,1%")
print(f"Mi Argentina: 26 M de usuarios (22/09/2025) / 46.044.703 habitantes (Censo 2022) = {26e6/46_044_703:.0%} [calculo propio; poblacion: probable]")
print(f"Boti: 1,3 M de usuarios por mes (OCDE-OPSI, ~2022) / 3.121.707 habitantes de la Ciudad = {1.3e6/3_121_707:.0%} (incluye no residentes) [calculo propio]")
print("ENCC 2022 (Cultura): usa WhatsApp 92% de la poblacion de 13 anos y mas en ciudades de mas de 30.000 habitantes")

ESC = {
    #        p_nores  no_IA_res  no_IA_nores  alcance_SMS_nores  segmentos  falla
    "bajo":  (0.55,   0.25,      0.70,        0.0,               1,         0.03),
    "medio": (0.55,   0.40,      0.85,        0.5,               1,         0.05),
    "alto":  (0.55,   0.60,      0.95,        1.0,               2,         0.08),
}
print("\nSupuestos por escenario [inferencia]: parte de avisos a no residentes, parte de residentes sin IA, parte de no residentes sin IA,")
print("parte de no residentes sin IA a los que se les puede mandar SMS (hace falta su celular), segmentos por aviso, reintentos/fallas")
SH = {}
for k, (pn, nr, nn, an, seg, fa) in ESC.items():
    sh = (1 - pn) * nr + pn * nn * an
    SH[k] = sh
    print(f"  {k:5s}: no_resid={pn:.0%} res_sin_IA={nr:.0%} nores_sin_IA={nn:.0%} alcance_nores={an:.0%} -> "
          f"parte de avisos por SMS = {sh:.1%}; segmentos={seg}; fallas={fa:.0%}")

print()
print("=" * 100)
print("4. COSTO POR ANO DEL SMS ($ dic-2025, con IVA)")
print("=" * 100)
FIJO = {"bajo": 0.0, "medio": 0.0,
        # alto: codigo corto dedicado (ClickSend: US$1.212,58 por mes + US$2.425,15 de alta), con IVA
        "alto": (1212.58 * 12 + 2425.15) * USD * IVA}
COSTO = {}
for k in ["bajo", "medio", "alto"]:
    pn, nr, nn, an, seg, fa = ESC[k]
    sms = AVISOS[k] * SH[k]
    envios = sms * seg * (1 + fa)
    c = envios * PRECIO[k] + FIJO[k]
    COSTO[k] = c
    print(f"  {k:5s}: {AVISOS[k]:,} avisos x {SH[k]:.1%} = {sms:,.0f} SMS; x {seg} seg x {1+fa:.2f} = {envios:,.0f} envios; "
          f"x {p(PRECIO[k])} + fijo {m(FIJO[k])} = {m(c)} por ano (US${c/USD:,.0f})".replace(",", "."))

# Sensibilidades
print("\nSensibilidades (medio, cambiando una cosa):")
base_sms = AVISOS["medio"] * SH["medio"] * 1 * 1.05
for n, pr in [("precio JGM 2026 mas bajo (US$0,0195)", of26[0][1] / q_max * USD),
              ("precio Bahia Blanca 2025", PRECIO["medio"]),
              ("precio lista Sinch + IVA", 0.0906 * USD * IVA),
              ("precio lista ClickSend Boost + IVA", PRECIO["alto"])]:
    print(f"  {n:45s}: {m(base_sms*pr)}")
print("\nSensibilidad a la parte de no residentes y al alcance (medio: 183.000 avisos, precio medio, 1 segmento, 5% fallas):")
for pn in (0.40, 0.55, 0.70):
    for an in (0.0, 0.5, 1.0):
        sh = (1 - pn) * 0.40 + pn * 0.85 * an
        print(f"  no_resid={pn:.0%} alcance_nores={an:.0%}: SMS = {sh:.1%} de los avisos -> {m(AVISOS['medio']*sh*1.05*PRECIO['medio'])} por ano")
sms_techo = ACTAS_HOY * 1.0 * 2 * 1.08
print(f"  Techo absoluto: los {ACTAS_HOY:,} avisos todos por SMS, 2 segmentos, 8% fallas, precio alto: {m(sms_techo*PRECIO['alto'] + FIJO['alto'])}".replace(",", "."))

print()
print("Otras vias, costo por aviso ($ dic-2025):")
ses = 0.16 / 1000 * USD * IVA
wa = 0.026 * USD * IVA
print(f"  Correo electronico (AWS SES Essentials US$0,16 cada 1.000, + IVA): {p(ses, 2)} por aviso -> medio {m(AVISOS['medio']*SH['medio']*ses)} por ano")
print(f"  WhatsApp, plantilla fuera de la ventana de 24 h (US$0,026, informe 23, + IVA): {p(wa)} por aviso -> medio {m(AVISOS['medio']*SH['medio']*wa)} por ano")
print(f"  SMS medio: {p(PRECIO['medio'])} por aviso; SMS alto: {p(PRECIO['alto']*2)} por aviso de 2 segmentos")
print("  Domicilio Vial Electronico de la Provincia (Res. 125/2023): sin costo para el Municipio; la Provincia avisa por correo o mensaje")
print("  Domicilio fiscal electronico municipal (Ord. Fiscal 2026, art. 5): previsto pero no implementado; mientras tanto, el correo constituido")

print()
print("Comparacion con el informe 23 (A4): avisos por WhatsApp del escenario medio = 49,9 M por ano")
for k in COSTO:
    print(f"  SMS {k}: {m(COSTO[k])} = {COSTO[k]/49.9e6:.0%} de esos 49,9 M")
