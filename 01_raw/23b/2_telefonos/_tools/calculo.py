#!/usr/bin/env python3
# Cuentas del tema Z2: teléfonos en vez de cámaras corporales (Programa San Isidro 2027).
# Todo en pesos de diciembre de 2025. Fuentes: ver ../FUENTES.txt
# Marcas: [verificado] dato leído en la fuente; [supuesto] decisión mía; [cálculo propio].

IPC_DIC25 = 10121.3715          # ch/wt/data/ipc_indec_mensual.csv
IPC_JUL26 = 12076.3937          # último mes del archivo; se usa para precios posteriores
F_POST = IPC_DIC25 / IPC_JUL26  # deflactor para precios de oct-2026
USD = 1447.84                   # pesos de dic-2025 por dólar (BCRA, Com. A 3500, promedio dic-2025; corrección del coordinador; antes 1.274)

def dic25(p):                   # precio observado el 06/10/2026 -> pesos de dic-2025
    return p * F_POST

def M(x):                       # millones con un decimal
    return f"{x/1e6:,.1f} M".replace(",", "X").replace(".", ",").replace("X", ".")

def P(x):
    return f"{x:,.0f}".replace(",", ".")

out = []
def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.append(s)

pr("== 0. Deflactor ==")
pr(f"IPC dic-2025 {IPC_DIC25} / IPC jul-2026 {IPC_JUL26} = {F_POST:.5f} (precios de oct-2026 se deflactan con jul-2026, consigna)")

# ---------------------------------------------------------------- 1. Teléfonos
pr("\n== 1. Teléfonos de gama media (precio de venta con IVA, 06/10/2026) [verificado] ==")
telefonos = {
    "Samsung Galaxy A27 5G 8/256 (Naldo)": 799999,   # IP64, OIS, 5.000 mAh, 6 años de seguridad (Samsung AR)
    "Motorola Moto G56 5G 8/256 (tienda Motorola)": 729999,  # IP68, 'certificación militar', 5.200 mAh
    "Motorola Moto G Max 8/256 (tienda Motorola)": 769999,   # IP68/IP69, 5.200 mAh
    "Motorola Moto G86 5G 8/256 (tienda Motorola)": 779999,  # IP68, 5.200 mAh, video 4K
    "Motorola Moto G67 4/256 (tienda Motorola)": 569999,     # IP64, 4 GB de RAM
    "Samsung Galaxy A56 5G 8/256 (Naldo)": 899999,
    "Samsung Galaxy A37 5G 8/256 (Naldo)": 999999,
}
for k, v in telefonos.items():
    pr(f"  {k}: {P(v)} oct-2026 -> {P(dic25(v))} dic-2025")
TEL = dic25(telefonos["Samsung Galaxy A27 5G 8/256 (Naldo)"])
TEL_ALT = dic25(telefonos["Motorola Moto G56 5G 8/256 (tienda Motorola)"])

# ---------------------------------------------------------------- 2. Accesorios
pr("\n== 2. Accesorios ==")
soporte_usd = 20.99 + 4.99      # Telesin vest chest strap + phone clip (EE. UU.) [verificado]
soporte_usd_alt = 32.99         # Telesin Universal Neck Mount for Phones [verificado]
IMPORT = 1.5                    # [supuesto] flete, aranceles y margen del importador (rango 1,0 a 2,0)
SOPORTE = soporte_usd * USD * IMPORT
pr(f"  Soporte de pecho: US$ {soporte_usd:.2f} x {USD} x {IMPORT} (importación, supuesto) = {P(SOPORTE)}; rango x1,0..x2,0: {P(soporte_usd*USD)} a {P(soporte_usd*USD*2)}")
pr(f"  Alternativa de cuello para teléfono: US$ {soporte_usd_alt} -> {P(soporte_usd_alt*USD*IMPORT)}")
FUNDA = dic25(51999)            # funda Samsung de silicona (Cetrogar/Naldo, A36/A56) como referencia [verificado el precio; usarla para A27 es supuesto]
BATEXT = dic25(49999)           # batería externa Miccell 10.000 mAh 20 W (Cetrogar) [verificado]
BATEXT20 = dic25(54999)         # Miccell 20.000 mAh (Cetrogar) [verificado]
MIC = 49.99 * USD * IMPORT      # micrófono corbatero inalámbrico Ulanzi A200 (EE. UU.) - opcional
pr(f"  Funda: {P(FUNDA)} | batería externa 10.000 mAh: {P(BATEXT)} | 20.000 mAh: {P(BATEXT20)} | micrófono opcional: {P(MIC)}")
ACC = SOPORTE + FUNDA + BATEXT
pr(f"  Kit de accesorios por agente (soporte + funda + batería 10.000): {P(ACC)}")
KIT = TEL + ACC
pr(f"  Equipo completo por agente (Galaxy A27 + kit): {P(KIT)}  (con Moto G56: {P(TEL_ALT+ACC)})")

# ---------------------------------------------------------------- 3. Batería
pr("\n== 3. Horas de video en vivo con una carga [inferencia sobre Sci Rep 2023, videollamadas] ==")
# Vivo V9 3.260 mAh: 3,6 a 4,8 h ; Motorola Droid Turbo 3.900 mAh: 2,9 a 5,0 h
consumos = [3260/4.8, 3260/3.6, 3900/5.0, 3900/2.9]
cmin, cmax = min(consumos), max(consumos)
cmed = 900.0  # [supuesto] valor central
pr(f"  Consumo medido en videollamada: {cmin:.0f} a {cmax:.0f} mAh por hora; central {cmed:.0f}")
for cap in (5000, 5200):
    pr(f"  Batería {cap} mAh: {cap/cmax:.1f} a {cap/cmin:.1f} h (central {cap/cmed:.1f} h)")
EF = 0.6  # [supuesto] energía útil que entrega una batería externa al teléfono
pr(f"  + batería externa 10.000 mAh x {EF} = {10000*EF:.0f} mAh útiles: +{10000*EF/cmax:.1f} a +{10000*EF/cmin:.1f} h")

# ---------------------------------------------------------------- 4. Datos
pr("\n== 4. Datos móviles por hora y por mes ==")
def gb_h(mbps):                 # Mbps -> GB por hora (1 GB = 1000 MB)
    return mbps * 3600 / 8 / 1000
OVER = 1.10                     # [supuesto] 10% de sobrecarga de protocolo y reenvíos
AUDIO = 0.1                     # Mbps de audio [supuesto]
calidades = {
    "480p a 0,7 Mbps (mínimo práctico)": 0.7,
    "480p a 1,0 Mbps": 1.0,
    "720p a 2,0 Mbps (H.265, mínimo YouTube)": 2.0,
    "720p a 3,0 Mbps (H.264, mínimo YouTube)": 3.0,
    "1080p a 8 Mbps (grabación local de respaldo)": 8.0,
}
for k, v in calidades.items():
    pr(f"  {k}: {gb_h(v+AUDIO)*OVER:.2f} GB por hora")
DIAS = 22                       # días hábiles por mes [supuesto]
planes = [(2, 24800), (4, 31085), (8, 49745), (15, 69755), (30, 77395), (50, 87525)]  # Movistar Empresas, sin impuestos, oct-2026 [verificado]
IMP_TEL = 1.235                 # final/sin impuestos en la página de Personal: 1,222 a 1,240 [verificado]; uso 1,235 [supuesto]
def plan_para(gb):
    for cap, precio in planes:
        if cap >= gb * 1.2:     # 20% de margen [supuesto]
            return cap, precio
    cap, precio = planes[-1]
    extra = gb * 1.2 - cap      # bonos extra al mismo precio por GB del plan de 50 GB [supuesto]
    return cap, precio + extra * (precio / cap)
pr("  Plan necesario (Movistar Empresas, lista sin impuestos, con impuestos x1,235, en pesos de dic-2025):")
pr(f"  Control: Personal (personas) 30 GB precio de lista final 104.950 -> {P(dic25(104950))} dic-2025; Movistar Empresas 30 GB x1,235 -> {P(dic25(77395*IMP_TEL))}")
escenarios = {}
for horas in (1, 2, 4):
    for k, v in (("480p 1,0 Mbps", 1.0), ("720p 2,0 Mbps", 2.0)):
        gb = gb_h(v+AUDIO) * OVER * horas * DIAS
        cap, precio = plan_para(gb)
        mes = dic25(precio * IMP_TEL)
        escenarios[(horas, k)] = (gb, cap, mes)
        pr(f"   {horas} h/día, {k}: {gb:.1f} GB/mes -> plan {cap} GB -> {P(mes)} por mes, {P(mes*12)} por año")
DATOS_ANUAL = escenarios[(2, "480p 1,0 Mbps")][2] * 12   # escenario central
DATOS_ANUAL_MIN = escenarios[(1, "480p 1,0 Mbps")][2] * 12
DATOS_ANUAL_MAX = escenarios[(4, "720p 2,0 Mbps")][2] * 12

# ---------------------------------------------------------------- 5. Gestión de dispositivos
pr("\n== 5. Gestión de dispositivos (MDM), por agente y por año ==")
mdm = {
    "Headwind MDM Community (Apache-2.0, servidor propio; lo opera el equipo ya pagado)": 0.0,
    "Headwind MDM Cloud US$19 por equipo y por año": 19 * USD,
    "Headwind MDM Premium US$2.990 una vez + US$1.490/año (hasta 300 equipos), 80 equipos, año 1": (2990 + 1490) * USD / 80,
    "Headwind MDM Premium, 80 equipos, años siguientes": 1490 * USD / 80,
    "Microsoft Intune Plan 1 US$8 por usuario y por mes": 8 * 12 * USD,
}
for k, v in mdm.items():
    pr(f"  {k}: {P(v)}")
MDM = 0.0
MDM_ALT = 19 * USD

# ---------------------------------------------------------------- 6. Almacenamiento
pr("\n== 6. Volumen de archivo (sin precio encontrado) ==")
for horas in (1, 2, 4):
    for k, v in (("480p 1,0", 1.0), ("720p 2,0", 2.0), ("1080p 8", 8.0)):
        gb_ano = gb_h(v+AUDIO) * horas * DIAS * 12
        pr(f"  {horas} h/día, {k} Mbps: {gb_ano/1000:.2f} TB por agente y por año; 80 agentes {gb_ano*80/1000:.0f} TB; 331 agentes {gb_ano*331/1000:.0f} TB")

# ---------------------------------------------------------------- 7. Comparación por agente y por año
pr("\n== 7. Costo por agente: teléfono municipal frente a reintegro (teléfono propio) ==")
VIDA_TEL = 4   # años [supuesto]; Samsung promete 6 años de seguridad, la batería es el límite
VIDA_ACC = 2   # años [supuesto]
anual_tel = TEL / VIDA_TEL + ACC / VIDA_ACC + DATOS_ANUAL + MDM
pr(f"  A) Teléfono municipal: compra {P(KIT)}; anualizado {P(TEL/VIDA_TEL)} (teléfono/{VIDA_TEL}) + {P(ACC/VIDA_ACC)} (accesorios/{VIDA_ACC}) + datos {P(DATOS_ANUAL)} + MDM {P(MDM)} = {P(anual_tel)} por año")
# Reintegro: el agente usa su teléfono; el Municipio paga el plan y un desgaste equivalente
reint = TEL / VIDA_TEL + ACC / VIDA_ACC + DATOS_ANUAL + MDM
pr(f"  B) Reintegro al empleado (mismo plan, desgaste del teléfono y accesorios, MDM de perfil de trabajo): {P(reint)} por año, sin compra inicial del teléfono")
pr("     -> B no ahorra: el Municipio igual paga el desgaste y los datos; pierde control del equipo y de la prueba [inferencia]")
pr(f"  Rango de datos: {P(DATOS_ANUAL_MIN)} (1 h/día, 480p) a {P(DATOS_ANUAL_MAX)} (4 h/día, 720p) por año")

# ---------------------------------------------------------------- 8. Totales 80 y 331
pr("\n== 8. Totales: teléfonos (óptima) frente a cámaras corporales del programa ==")
BC_80 = 168737624.0       # Excel, Supuestos fila 233 (80 cámaras, dic-2025) [tomado del material previo]
BC_LIC_80 = 3825756.0     # Excel, Supuestos fila 234 (licencia por año)
bc_unit = BC_80 / 80
bc_lic_unit = BC_LIC_80 / 80
pr(f"  Cámara corporal del programa: {P(bc_unit)} c/u; licencia {P(bc_lic_unit)} por cámara y por año")
for N in (80, 331):
    tel_capex = KIT * N
    tel_opex = (DATOS_ANUAL + MDM) * N
    tel_opex_min = (DATOS_ANUAL_MIN + MDM) * N
    tel_opex_max = (DATOS_ANUAL_MAX + MDM_ALT) * N
    repos = (TEL / VIDA_TEL + ACC / VIDA_ACC) * N
    bc_capex = bc_unit * N
    bc_opex = bc_lic_unit * N
    pr(f"\n  N = {N} agentes")
    pr(f"   Teléfonos: compra {M(tel_capex)}; por año datos+MDM {M(tel_opex)} (rango {M(tel_opex_min)} a {M(tel_opex_max)}); reposición anualizada {M(repos)}")
    pr(f"   Cámaras corporales (programa): compra {M(bc_capex)}; por año licencia {M(bc_opex)}  [sin datos móviles ni almacenamiento]")
    pr(f"   Cámaras corporales con los mismos datos móviles (transmiten por 4G igual): por año {M(bc_opex + DATOS_ANUAL*N)}")
    pr(f"   Diferencia de compra (teléfonos - cámaras): {M(tel_capex - bc_capex)}")
    pr(f"   Diferencia por año contra el programa tal como está presupuestado: {M(tel_opex - bc_opex)}")
    pr(f"   Diferencia por año contra cámaras con datos: {M(tel_opex - (bc_opex + DATOS_ANUAL*N))}")
    # costo anual equivalente con vida útil: cámaras 4 años [supuesto] igual que el teléfono
    eq_tel = tel_capex / VIDA_TEL + tel_opex
    eq_bc = bc_capex / 4 + bc_opex + DATOS_ANUAL * N
    pr(f"   Costo anual equivalente (compra/4 años + gasto anual): teléfonos {M(eq_tel)}; cámaras con datos {M(eq_bc)}; diferencia {M(eq_tel-eq_bc)}")

# ---------------------------------------------------------------- 9. Referencias
pr("\n== 9. Referencias de precio de cámaras corporales ==")
pr(f"  Quito 2021: US$179.000 / 100 = US$1.790 por cámara con sistema -> {P(1790*USD)} (dólares de 2021 sin ajustar)")
pr(f"  Programa: {P(bc_unit)} = US$ {bc_unit/USD:,.0f}")
pr(f"  T-Mobile + Visual Labs 2021 (EE. UU.): US$45 por mes y por equipo + US$50 de alta -> {P(45*12*USD)} por año (software y nube, sin teléfono ni datos)")


# ---------------------------------------------------------------- 10. Alternativa: transmitir a Milestone (ya comprado) con XProtect Mobile
pr("\n== 10. Alternativa: XProtect Mobile (gratis) con 'Video Push' a Milestone ==")
IPC_ABR26 = 11363.0904
lic_techo = 351045650.80 / 650 * IPC_DIC25 / IPC_ABR26   # Dec. 416/2026: 650 licencias + soporte de todo el universo -> techo
pr(f"  Licencia de dispositivo por teléfono (techo): 351.045.650,80 / 650 (abr-2026) -> {P(lic_techo)} dic-2025 [cálculo propio; incluye soporte, por eso es techo]")
for N in (80, 331):
    pr(f"  {N} teléfonos: hasta {M(lic_techo*N)} una vez (frente a 0 de licencia con MediaMTX, MIT)")

open(__file__.replace("calculo.py", "calculo_salida.txt"), "w").write("\n".join(out) + "\n")
