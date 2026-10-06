#!/usr/bin/env python3
# Z2 ampliación: teléfono propio del inspector, datos pagos por el Municipio, guarda de 2 años, 4 a 6 h por día.
# Pesos de dic-2025. Dólar $1.447,84 (BCRA, Com. A 3500, promedio dic-2025; consigna del coordinador).
# Marcas: [verificado] dato de fuente; [supuesto]; [cálculo propio].

IPC_DIC25 = 10121.3715
IPC_JUL26 = 12076.3937          # último del repo; para precios de oct-2026
IPC_ABR26 = 11363.0904
F = IPC_DIC25 / IPC_JUL26
USD = 1447.84

def d(p): return p * F
def M(x): return f"{x/1e6:,.1f} M".replace(",", "X").replace(".", ",").replace("X", ".")
def P(x): return f"{x:,.0f}".replace(",", ".")
out = []
def pr(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

pr(f"Deflactor oct-2026 -> dic-2025: {F:.5f}; dólar {USD}")

# ------------------------------------------------ 1. Agentes
pr("\n== 1. Agentes (según el Municipio) ==")
pr("  Patrulla: 331 efectivos (16/01/2026); 'superará los 390 en calle y monitoreo' (03/03/2026); 300 oficiales de seguridad + 145 de monitoreo (página San Isidro Seguro, 09/06/2026)")
pr("  Agentes de tránsito: 120 (03/08/2026). Inspectores de comercio/obras/Agencia de Control: sin cifra pública")
NS = {"programa (80)": 80, "patrulla ene-2026 (331)": 331, "en calle con fuente: 300 patrulla + 120 tránsito (420)": 420}
for k, v in NS.items(): pr(f"  {k}: {v}")

# ------------------------------------------------ 2. Equipo
pr("\n== 2. Equipo ==")
TEL = d(799999)        # Galaxy A27 5G 8/256 (Naldo) [verificado]
TEL_ALT = d(729999)    # Moto G56 5G 8/256 (Motorola) [verificado]
FUNDA = d(51999)       # funda Samsung de silicona (referencia) [verificado precio]
SOPORTE = (20.99 + 4.99) * USD * 1.5   # Telesin, EE. UU., x1,5 importación [supuesto]
BATEXT = d(49999)      # Miccell 10.000 mAh (Cetrogar) [verificado]
pr(f"  Teléfono Galaxy A27: {P(TEL)} | Moto G56: {P(TEL_ALT)} | funda {P(FUNDA)}")
pr(f"  Soporte de pecho: US$25,98 x {USD} x 1,5 = {P(SOPORTE)} (rango x1,0..x2,0: {P(25.98*USD)} a {P(25.98*USD*2)})")
pr(f"  Batería externa 10.000 mAh: {P(BATEXT)}")
IPC = {"2026-03": 11077.0608, "2026-05": 11607.3937, "2026-06": 11826.4103, "2026-07": 12076.3937}
def dm(p, mes): return p * IPC_DIC25 / IPC[mes]
pr("  Compra pública de referencia (Ciudad de Buenos Aires, convenio marco 623-0849-LPU25, 'alquiler única vez', precios adjudicados) [verificado]:")
CABA_G3 = (dm(689000.01, "2026-06"), dm(745215, "2026-06"))     # renglón 24, Gama 3 (8 GB, 4K, 5.000 mAh), AMX
CABA_G4 = (dm(450000, "2026-06"), dm(500343.69, "2026-06"))     # renglón 25, Gama 4, Telecom
CABA_A36 = (dm(453750, "2026-07"), dm(471714.33, "2026-07"))   # renglón 38, gama alta dual SIM A36/G75, Telecom (ago-2026, deflactado con jul-2026)
pr(f"   Gama 3: {P(CABA_G3[0])} a {P(CABA_G3[1])} | Gama 4: {P(CABA_G4[0])} a {P(CABA_G4[1])} | 'A36 - G75' doble SIM: {P(CABA_A36[0])} a {P(CABA_A36[1])} (dic-2025)")
TEL_PUB = sum(CABA_A36)/2
KIT_TODOS = SOPORTE + BATEXT
KIT_TEL = TEL + FUNDA
KIT_TEL_PUB = TEL_PUB + FUNDA
pr(f"  Kit para todos (soporte + batería): {P(KIT_TODOS)}; teléfono municipal con funda: {P(KIT_TEL)}")

# batería: 4 a 6 h
cmin, cmax = 3260/4.8, 3900/2.9
pr(f"  Batería 5.000 mAh: {5000/cmax:.1f} a {5000/cmin:.1f} h; con 10.000 mAh externa (60% útil) +{6000/cmax:.1f} a +{6000/cmin:.1f} h -> 6 h cubiertas en el peor caso: {5000/cmax+6000/cmax:.1f} h")

# ------------------------------------------------ 3. Datos
pr("\n== 3. Datos por agente y por mes (Movistar Empresas, legales vigentes 2026, sin impuestos) ==")
IMP = 1.235            # final/sin impuestos en Personal (1,222 a 1,240) [verificado]; central [supuesto]
PLAN60 = 96495         # Plan Comunidad Empresas 60GB [verificado]
PLAN50 = 85310
PACK15 = 14469         # pack 15 GB x 30 días [verificado]
esc = {"4 h/día a 1,5 Mbps": 59, "6 h/día a 2,0 Mbps": 119}   # GB/mes (material previo y3)
DATOS = {}
for k, gb in esc.items():
    if gb <= 60:
        sin = PLAN60; detalle = "plan 60 GB"
    else:
        packs = -(-(gb - 60) // 15)
        sin = PLAN60 + packs * PACK15; detalle = f"plan 60 GB + {packs} packs de 15 GB"
    mes = d(sin * IMP)
    DATOS[k] = mes
    pr(f"  {k}: {gb} GB -> {detalle}: ${P(sin)} + imp. -> {P(mes)} por mes, {P(mes*12)} por año (dic-2025)")
CABA80 = dm(103474.69, "2026-07")   # renglón 1, 80 GB, Telecom [verificado]
CABA50 = (dm(94013, "2026-03"), dm(99355.40, "2026-03"))
CABA30 = (dm(59672, "2026-07"), dm(63173.81, "2026-07"))
M2M50 = (dm(76009.50, "2026-03"), dm(85170, "2026-03"))
pr(f"  Compra pública de referencia (Ciudad, convenio LPU25, por línea y mes, Telecom): 80 GB {P(CABA80)}; 50 GB {P(CABA50[0])}-{P(CABA50[1])}; 30 GB {P(CABA30[0])}-{P(CABA30[1])}; solo datos M2M 50 GB (Telefónica) {P(M2M50[0])}-{P(M2M50[1])} (dic-2025)")
DATOS_PUB = {"4 h/día a 1,5 Mbps": CABA80, "6 h/día a 2,0 Mbps": CABA80 * 119 / 80}
for k, v in DATOS_PUB.items():
    pr(f"   {k}: {P(v)} por mes, {P(v*12)} por año (6 h: 80 GB prorrateado a 119 GB [supuesto])")
pr(f"  Precio por GB del pack: ${PACK15/15:,.0f} + imp.; del plan de 60 GB: ${PLAN60/60:,.0f} + imp.")

# ------------------------------------------------ 4. Almacenamiento 2 años
pr("\n== 4. Guarda de 2 años ==")
NAS = 4699999          # QNAP 12 bahías rack 2U, 2 fuentes (Necxus) [verificado]
HDD = 1649999          # Toshiba MG 22 TB (Necxus) [verificado]
UTIL = 22 * 10 * 0.91  # RAID 6 (10 de 12 discos) y formato [supuesto]
COPIAS = 2             # original + copia en otro edificio [supuesto]
VIDA = 5               # años [supuesto]
OPEX = 0.10            # energía, reparaciones, por año sobre la compra [supuesto]
local_tb = d(NAS + 12 * HDD) / UTIL * COPIAS
pr(f"  Local: QNAP 12 bahías + 12 x 22 TB = ${P(NAS+12*HDD)} (oct-2026) por {UTIL:.0f} TB útiles -> {P(local_tb)} por TB con 2 copias (dic-2025)")
nube = {
    "Azure Archive LRS, Europa Occidental": 0.0018,
    "Azure Archive LRS, Suecia Central": 0.00099,
    "Azure Cold LRS, Europa Occidental": 0.0045,
    "AWS S3 Glacier Flexible Retrieval, Irlanda": 0.0036,
    "AWS S3 Intelligent-Tiering Deep Archive Access, Irlanda": 0.00099,
}
ALM = {}
for k, gb in esc.items():
    tb = gb * 24 / 1000
    pr(f"  {k}: {tb:.2f} TB por agente acumulados en 2 años")
    for nombre, N in NS.items():
        TB = tb * N
        capex = local_tb * TB
        anual_local = capex / VIDA + capex * OPEX
        linea = f"   {nombre}: {TB:,.0f} TB | local: compra {M(capex)}, por año {M(anual_local)}"
        for nn, usd in nube.items():
            linea += f" | {nn}: {M(TB*1000*usd*12*USD)}/año"
        pr(linea)
        cap_h = local_tb / COPIAS * TB * 3 / 24     # 3 meses en el Municipio, una copia [supuesto]
        anual_h = cap_h / VIDA + cap_h * OPEX + TB*1000*0.0018*12*USD
        pr(f"     híbrido (3 meses en el Municipio + 2 años en Azure Archive Europa Occidental): compra {M(cap_h)}, por año {M(anual_h)}")
        ALM[(k, N)] = (TB, capex, anual_local, TB*1000*0.0018*12*USD, TB*1000*0.0045*12*USD, cap_h, anual_h)
pr("  Salida a internet (vecinos que miran los videos), Azure Europa Occidental: US$0,087 por GB tras los primeros 100 GB [verificado]")

# ------------------------------------------------ 5. Licencias
pr("\n== 5. Licencias ==")
lic = 351045650.80 / 650 * IPC_DIC25 / IPC_ABR26
pr(f"  XProtect Mobile con Video Push: licencia de dispositivo por teléfono, techo {P(lic)} (Dec. 416/2026)")
for N in NS.values(): pr(f"   {N}: hasta {M(lic*N)}")
pr("  MediaMTX (MIT), RootEncoder y StreamPack (Apache-2.0), OpenSSL (Apache-2.0), certificado de aplicación AC ONTI (gratis): 0")
INTUNE = 8 * 12 * USD
pr(f"  Opcional, perfil de trabajo en el teléfono propio (Microsoft Intune Plan 1, US$8/mes): {P(INTUNE)} por agente y por año")

# ------------------------------------------------ 6. Cuenta final
pr("\n== 6. Cuenta final (pesos de dic-2025) ==")
pr("  Supuestos: soporte y batería externa para todos; teléfono con funda sólo para la fracción sin teléfono apto; datos a precio de compra pública de la Ciudad (y entre paréntesis, de lista de Movistar); guarda híbrida")
for k in esc:
    for nombre, N in NS.items():
        TB, capex, anual_local, arch, cold, cap_h, anual_h = ALM[(k, N)]
        datos_pub = DATOS_PUB[k] * 12 * N
        datos_lista = DATOS[k] * 12 * N
        for p in (0.25, 0.5):
            equipos = N * KIT_TODOS + p * N * KIT_TEL_PUB
            equipos_ret = N * KIT_TODOS + p * N * KIT_TEL
            repos = N * KIT_TODOS / 2 + p * N * KIT_TEL_PUB / 4
            pr(f"  {k} | {nombre} | {int(p*100)}% sin teléfono apto:")
            pr(f"     COMPRA: equipos {M(equipos)} (con teléfono de comercio {M(equipos_ret)}) + guarda híbrida {M(cap_h)} = {M(equipos+cap_h)}  [guarda toda local: {M(capex)}]")
            pr(f"     POR AÑO: datos {M(datos_pub)} (lista {M(datos_lista)}) + guarda híbrida {M(anual_h)} [local {M(anual_local)}; nube archivo {M(arch)}] + reposición {M(repos)} = {M(datos_pub+anual_h+repos)} (con datos de lista {M(datos_lista+anual_h+repos)})")

pr("\n== 7. Contra las cámaras corporales del programa (80) ==")
pr(f"  Cámaras: 168,7 M de compra y 3,8 M por año, sin datos ni guarda")

open(__file__.replace("calculo2.py", "calculo2_salida.txt"), "w").write("\n".join(out) + "\n")
