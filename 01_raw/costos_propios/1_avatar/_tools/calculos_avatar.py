#!/usr/bin/env python3
# Cálculos del informe A1 (avatar). Todas las fuentes en ../FUENTES.txt. Supuestos marcados [supuesto].
USD_ARS = 1520.0                     # consigna del cliente
CNY_USD = 0.149111                   # BCRA tipoPase 02/10/2026 (bcra_cotiz_CNY_2026-10.json)
EUR_USD = 1.1255                     # BCRA tipoPase 02/10/2026 (bcra_cotiz_EUR_2026-10.json)
IPC_DIC25 = 10121.3715
IPC_JUL26 = 12076.3937               # último dato del CSV (no hay ago-oct 2026)
F_IPC = IPC_DIC25 / IPC_JUL26        # pesos oct-2026 -> pesos dic-2025 (aproximado con jul-2026)

MIN_SES = 1440   # min de sesión por alumno-año (2x20 min x 36 semanas)
MIN_HAB = 576    # min que habla el tutor por alumno-año (8 min x 2 x 36)

out = []
def p(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

p("== Conversión IPC: factor oct-2026 -> dic-2025 (con jul-2026, último dato) =", f"{IPC_DIC25}/{IPC_JUL26} = {F_IPC:.5f}")

# --- 1. precios por minuto (US$) ---
precios = [
 ("LiveAvatar LITE, Business (475/6000 créditos)", 475/6000, "verificado"),
 ("LiveAvatar LITE, excedente Business", 0.09, "verificado"),
 ("LiveAvatar LITE, Essential (99/1100)", 99/1100, "verificado"),
 ("LiveAvatar LITE, Enterprise 'desde' (piso publicado)", 0.01, "verificado como anuncio; umbral no publicado"),
 ("LiveAvatar FULL, Business (2 créditos/min)", 2*475/6000, "verificado"),
 ("Alibaba China 3D streaming 停复机 0,60 CNY/min", 0.60*CNY_USD, "verificado"),
 ("Alibaba China 2D render en dispositivo 0,06 CNY/min", 0.06*CNY_USD, "verificado"),
 ("Azure avatar tiempo real estándar (sin TTS)", 0.50, "verificado"),
 ("Tavus Growth (397/1250)", 397/1250, "verificado"),
 ("Tavus excedente Growth", 0.32, "verificado"),
 ("D-ID API Scale anual (138,6/400)", 138.6/400, "verificado"),
 ("D-ID API Scale mensual (198/400)", 198/400, "verificado"),
 ("Anam Professional (999/8000)", 999/8000, "verificado"),
 ("Anam excedente Professional", 0.11, "verificado"),
 ("Anam Enterprise (excedente publicado)", 0.04, "verificado"),
 ("Simli (anuncio: menos de 1 centavo)", 0.01, "probable (fuente secundaria / anuncio)"),
 ("Spatius Scale anual (2869/480000)", 2869/480000, "verificado"),
 ("Spatius excedente Scale", 0.0056, "verificado"),
 ("Beyond Presence €349 plan (0,0875 €/min)", 0.0875*EUR_USD, "verificado"),
 ("Beyond Presence 'a escala' 0,03 €/min", 0.03*EUR_USD, "verificado como anuncio"),
]
p("\n== Precio por minuto y por alumno-año ==")
p("opción | US$/min | ¢/min | US$/alumno-año 1440 | US$/alumno-año 576 | marca")
for n,v,m in precios:
    p(f"{n} | {v:.4f} | {v*100:.2f} | {v*MIN_SES:.2f} | {v*MIN_HAB:.2f} | {m}")

# --- precios por canal (vía simultánea) al mes ---
p("\n== Precios por canal simultáneo (US$) ==")
canales = [
 ("Alibaba China 2D nube, audio→video 2400 CNY/mes", 2400*CNY_USD),
 ("Alibaba China 2D nube, completo 3000 CNY/mes", 3000*CNY_USD),
 ("Alibaba China 3D nube UE 4800 CNY/mes", 4800*CNY_USD),
 ("Alibaba internacional Lingjing 2D 2900 CNY/mes", 2900*CNY_USD),
 ("Baidu Xiling 2D nube 2400 CNY/mes (24000/año)", 2400*CNY_USD),
 ("Tencent internacional 2D nube 500 USD/mes", 500.0),
]
MIN_MES_CENTRO = 8*60*22   # canal usado 8 h x 22 días [supuesto]
for n,v in canales:
    p(f"{n} | US$/mes {v:.2f} | US$/min si se usa 100% de 8h x 22 días ({MIN_MES_CENTRO} min): {v/MIN_MES_CENTRO:.4f} | al 40%: {v/(MIN_MES_CENTRO*0.4):.4f}")
p("Alibaba 2D render en dispositivo, licencia por equipo 3000 CNY/año =", round(3000*CNY_USD,2), "US$/equipo-año")
p("Baidu 2D render en dispositivo 3600 CNY/equipo-año =", round(3600*CNY_USD,2), "US$")
p("Tencent internacional 2D en dispositivo 1200 US$/equipo-año")

# --- 3. hardware propio ---
p("\n== Hardware propio (por placa, por año) ==")
# Edenor T3-BT, cuadro ENRE 10/2026 (sin impuestos)
pico, resto, valle = 145.007, 140.567, 139.514
pot_contr, pot_adq = 20419.14, 11240.96
energia_pond = (pico*5 + resto*13 + valle*6)/24   # pico 18-23, resto 5-18, valle 23-5 [supuesto de franjas]
p(f"Edenor T3-BT oct-2026: energía ponderada 24h = {energia_pond:.3f} $/kWh; potencia contratada+adquirida = {pot_contr+pot_adq:.2f} $/kW-mes")
PUE = 1.5      # refrigeración [supuesto]
MANT = 0.10    # mantenimiento anual / costo del equipo [supuesto]
F_IMPORT = 1.03*1.03*1.105   # flete/seguro 3% [supuesto] x tasa estadística 3% x IVA 10,5% (BIT, probable)
F_IMPORT21 = 1.03*1.03*1.21
p(f"Factor de importación con IVA 10,5%: {F_IMPORT:.4f}; con IVA 21%: {F_IMPORT21:.4f} (DIE 0% probable)")
placas = [
 # nombre, precio placa US$, host US$ [supuesto], kW placa, kW host [supuesto], sesiones simultáneas habladas [ver informe], años
 ("L40S 48 GB (CDW 10.497,99)", 10497.99, 4000, 0.350, 0.250, 2, 4),
 ("RTX PRO 6000 Blackwell Server (CDW 16.115)", 16115.00, 4000, 0.600, 0.250, 3, 4),
 ("RTX 5090 (minorista ~4.329, probable; GeForce)", 4329.00, 2500, 0.575, 0.200, 2, 4),
]
res_placas = {}
for n, pg, host, kwg, kwh, ses, anos in placas:
    hw = (pg+host)*F_IMPORT
    amort = hw/anos
    kw = (kwg+kwh)*PUE
    kwh_ano = kw*8760
    luz_pesos_oct26 = kwh_ano*energia_pond + kw*(pot_contr+pot_adq)*12
    luz_pesos_dic25 = luz_pesos_oct26*F_IPC
    luz_usd = luz_pesos_dic25/USD_ARS
    mant = hw*MANT
    total = amort + luz_usd + mant
    res_placas[n] = (total, ses)
    p(f"{n}: equipo importado US${hw:,.0f} -> amortización {anos} años US${amort:,.0f}/año; "
      f"consumo {kw:.3f} kW x 8760 h = {kwh_ano:,.0f} kWh; luz ${luz_pesos_oct26:,.0f} (oct-26) = ${luz_pesos_dic25:,.0f} (dic-25) = US${luz_usd:,.0f}/año; "
      f"mantenimiento US${mant:,.0f}; TOTAL US${total:,.0f}/año; por sesión hablada simultánea US${total/ses:,.0f}/año")

# capacidad útil: ventana de uso 5 h/día x 5 días x 36 semanas = 54.000 min/año; ocupación 50% [supuesto]
VENT = 5*60*5*36
OCC = 0.5
p(f"\nVentana de uso por sesión simultánea: {VENT} min/año; ocupación media {OCC:.0%} [supuesto]")
for n,(tot,ses) in res_placas.items():
    cap = ses*VENT*OCC
    pm = tot/cap
    p(f"{n}: capacidad {cap:,.0f} min hablados/año -> US${pm:.4f} por min hablado = US${pm*MIN_HAB:.2f} por alumno-año (576 min); "
      f"límite teórico 24x7 al 100%: US${tot/(ses*525600):.4f}/min")

# --- 4. alquiler por hora ---
p("\n== Alquiler por hora (pagando sólo los minutos hablados; idle local) ==")
alq = [
 ("RunPod RTX 4090", 0.74, 2), ("RunPod RTX 4090 con FlashHead Lite (3)", 0.74, 3),
 ("RunPod L40S", 1.09, 2), ("RunPod RTX 5090", 0.99, 2), ("RunPod RTX PRO 6000", 2.09, 3),
 ("AWS us-east-1 g6e.xlarge (L40S)", 1.861, 2), ("AWS sa-east-1 g6.xlarge (L4)", 1.368, 1),
 ("Azure brazilsouth NV36ads A10 v5", 6.40, 1), ("Azure eastus NV36ads A10 v5", 3.20, 1),
 ("RunPod H100 PCIe", 2.89, 3), ("AWS sa-east-1 p5.48xlarge por GPU (92,4672/8)", 92.4672/8, 3),
]
for n,h,s in alq:
    pm = h/60/s/OCC
    p(f"{n}: US${h}/h, {s} sesiones -> US${pm:.4f}/min hablado (ocupación {OCC:.0%}) = US${pm*MIN_HAB:.2f}/alumno-año; equivalente por min de sesión US${pm*MIN_HAB/MIN_SES:.4f}")

# --- 6. escenarios ---
p("\n== Escenarios ==")
esc = {
 "a) prueba 6 meses, 2 centros (200 alumnos, 18 semanas)": (200, 720, 288),
 "b) 6 centros (600 alumnos, año)": (600, 1440, 576),
 "c) casa, todos, uso realista 15%": (50833*0.15, 1440, 576),
 "d) casa, todos, uso pleno": (50833, 1440, 576),
}
op = {
 "LiveAvatar LITE excedente 0,09": ("ses", 0.09),
 "LiveAvatar LITE Business incluido 0,0792": ("ses", 475/6000),
 "LiveAvatar Enterprise piso 0,01": ("ses", 0.01),
 "Anam Enterprise 0,04": ("ses", 0.04),
 "Spatius Scale 0,0056-0,0060": ("ses", 2869/480000),
 "Beyond Presence 0,0985 (€0,0875)": ("ses", 0.0875*EUR_USD),
 "Tavus 0,32": ("ses", 0.32),
 "Azure 0,50 (+TTS)": ("ses", 0.50),
 "Alibaba 3D China 0,0895": ("ses", 0.60*CNY_USD),
 "MuseTalk en RunPod L40S (por min hablado)": ("hab", 1.09/60/2/OCC),
 "MuseTalk en AWS São Paulo L4 (por min hablado)": ("hab", 1.368/60/1/OCC),
 "MuseTalk en L40S propia (por min hablado)": ("hab", res_placas["L40S 48 GB (CDW 10.497,99)"][0]/(2*VENT*OCC)),
}
for e,(alum,ms,mh) in esc.items():
    p(f"\n{e}: alumnos {alum:,.0f}; min sesión {alum*ms:,.0f}; min hablados {alum*mh:,.0f}")
    for o,(base,v) in op.items():
        mins = alum*ms if base=="ses" else alum*mh
        usd = mins*v
        p(f"   {o}: US${usd:,.0f} = ${usd*USD_ARS/1e6:,.1f} M (pesos dic-2025 a $1.520) | US${usd/alum:,.2f} por alumno")

# LiveAvatar exacto con plan Business + excedente
p("\nLiveAvatar Business con excedente, cálculo exacto:")
for e,(alum,ms,mh,meses) in {"a) prueba":(200,720,288,6),"b) 6 centros":(600,1440,576,12),"c) casa 15%":(50833*0.15,1440,576,12),"d) casa pleno":(50833,1440,576,12)}.items():
    mins = alum*ms
    inc = 6000*meses
    usd = 475*meses + max(0,mins-inc)*0.09
    p(f"   {e}: {mins:,.0f} min; base {meses}x475 + excedente {max(0,mins-inc):,.0f} x 0,09 = US${usd:,.0f} (US${usd/mins:.4f}/min; US${usd/alum:,.2f}/alumno)")

# concurrencia en casa
p("\nConcurrencia en casa (ventana 5 h x 5 días x 36 semanas = 54.000 min; pico = 2,5 x promedio) [supuesto]:")
for e,(alum,ms,mh) in list(esc.items())[2:]:
    prom = alum*ms/54000; pico_s = prom*2.5
    proh = alum*mh/54000; pico_h = proh*2.5
    p(f"   {e}: sesiones simultáneas promedio {prom:,.0f}, pico {pico_s:,.0f}; habladas simultáneas promedio {proh:,.0f}, pico {pico_h:,.0f}")
    p(f"      L40S propias para el pico hablado (2 por placa): {pico_h/2:,.0f} placas -> US${pico_h/2*res_placas['L40S 48 GB (CDW 10.497,99)'][0]:,.0f}/año")
    p(f"      Canales Tencent 2D nube para el pico de sesión: {pico_s:,.0f} x 500 x 12 = US${pico_s*6000:,.0f}/año; Baidu: {pico_s:,.0f} x {2400*CNY_USD*12:,.0f} = US${pico_s*2400*CNY_USD*12:,.0f}/año")

open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y1a_avatar/_tools/calculos_avatar_salida.txt','w').write("\n".join(out)+"\n")
