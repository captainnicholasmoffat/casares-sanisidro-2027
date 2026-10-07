# -*- coding: utf-8 -*-
# Cálculo propio [cálculo propio]: control antirrobo del equipo de sonido municipal (San Isidro) — pesos de dic-2025.
# IPC INDEC del repo (ch/wt/data/ipc_indec_mensual.csv): dic-2025 = 10121,3715; último mes jul-2026 = 12076,3937
# (precios de ago-oct 2026 se deflactan con jul-2026 -> quedan algo altos).
# Dólar: $1.447,84 (BCRA, Com. A 3500, promedio dic-2025), regla fija del cliente.
# Euro/dólar y real/dólar: BNA 07/10/2026 (precios/bna_cotizaciones_2026-10-07.html): divisas EUR 1714,104 / USD 1520;
#   billetes Real 316 / USD 1540 (venta).
import csv
BASE = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad'
IPC = {}
for r in csv.DictReader(open(BASE + '/ch/wt/data/ipc_indec_mensual.csv')):
    IPC[(int(r['anio']), int(r['mes']))] = float(r['indice'])
B = IPC[(2025, 12)]
def k(y, m):
    if (y, m) > (2026, 7):
        y, m = 2026, 7
    return B / IPC[(y, m)]
USD = 1447.84
EUR_USD = 1714.104 / 1520.0
BRL_USD = 316.0 / 1540.0
OCT = k(2026, 10)
out = []
def p(s=''):
    out.append(s); print(s)
def P(x):
    return f'{x:,.0f}'.replace(',', '.')
def C(x, d=2):
    return f'{x:.{d}f}'.replace('.', ',')
def M(x, d=2):
    s = f'{x/1e6:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.') + ' M'

p(f'IPC: coef. oct-2026 (usa jul-2026) = {OCT:.4f}; feb-2025 = {k(2025,2):.4f}; jun-2025 = {k(2025,6):.4f}; '
  f'nov-2025 = {k(2025,11):.4f}; mar-2026 = {k(2026,3):.4f}; dic-2024 = {k(2024,12):.4f}')
p(f'Dólar {USD}; euro/dólar {EUR_USD:.4f}; real/dólar {BRL_USD:.4f}')
p()

# ------------------------------------------------------------- 0. VALOR DEL EQUIPO (del informe Z4a, recalculado)
kit_items = [  # (ítem, cant, precio nominal 06/10/2026)
 ('JBL EON ONE PRO', 2, 3032808.34), ('Behringer XR18', 1, 1450100.00), ('Monitor dB B-Hype 10', 2, 877044.11),
 ('EcoFlow Delta 3 1500', 1, 2890990.00), ('Shure SM58', 4, 266688.63), ('Shure SM57', 3, 243426.06),
 ('Caja directa Samson MD1', 2, 172549.10), ('Pie Quik Lok', 7, 89765.79), ('Cable XLR 6 m', 10, 37343.43),
 ('Cable plug 3 m', 4, 80079.35)]
sonido = sum(q * pr for _, q, pr in kit_items) * OCT * 1.05
mod_eur = 387.60 + 4 * 40.0
tarima24 = 4 * mod_eur * EUR_USD * USD * 1.8
toldo = 311992 * OCT
kit = sonido + tarima24 + toldo
van = 62170000 * OCT
van_l3 = 68080000 * OCT
p('0. VALOR A PROTEGER (precios del informe Z4a; euro con BNA 07/10/2026)')
p(f'   Sonido por kit: {M(sonido)}; tarima 2x4 m: {M(tarima24)}; toldo: {M(toldo)}; KIT: {M(kit)}')
p(f'   Camioneta Renault Master L1H1: {M(van)} (L3H2: {M(van_l3)})')
for n in (2, 3):
    p(f'   {n} kits: equipo {M(n*kit)}; equipo + camioneta {M(n*kit+van)}')
p()

# ------------------------------------------------------------- 1. RASTREO
p('1. RASTREO (precios nominales vistos 07/10/2026, deflactados con jul-2026)')
bultos = 7   # [supuesto] 2 columnas, 1 mezcladora en rack, 2 monitores, 1 EcoFlow, 1 valija de micrófonos y pies
trk = {
 'moto tag (pack 4, Frávega/Garmin, lista)': 164999 / 4,
 'moto tag (1 u, vendido por Frávega, lista)': 49999,
 'Samsung SmartTag2 (Samsung AR oficial)': 66499,
 'Samsung SmartTag2 (pack 4, Frávega, lista)': 479999 / 4,
 'Apple AirTag 2a gen (1 u, Frávega marketplace, lista)': 112299,
 'Apple AirTag 2a gen (pack 4, Frávega marketplace, lista)': 303799 / 4,
}
for n_, v in trk.items():
    p(f'   {n_}: {P(v)} nominal -> {P(v*OCT)} dic-25 por unidad; {bultos} bultos por kit = {M(bultos*v*OCT,3)}')
tag = 164999 / 4 * OCT
pila = 6390 / 2 * OCT        # Energizer CR2032 x2, Easy
tag_anual = bultos * pila + 0.10 * bultos * tag   # 1 pila por año + 10% de reposición [supuesto]
p(f'   Elegido: moto tag pack 4 -> {P(tag)} c/u; pila CR2032 {P(pila)} c/u; por kit compra {M(bultos*tag,3)}; por año {M(tag_anual,3)} (pila + 10% reposición [supuesto])')
p()
gps_hw_local = 257484 * OCT      # TKSTAR TK905 4G, lista Frávega marketplace
tat141 = 71.40 * 1.21 * EUR_USD * USD
p(f'   GPS 4G con SIM, a batería, para esconder en un bulto: TKSTAR TK905 4G lista {P(257484)} -> {P(gps_hw_local)} dic-25')
p(f'   Control: Teltonika TAT141 71,40 € sin IVA -> con IVA 21% {P(tat141)} en origen; x1,8 [supuesto importación] = {P(tat141*1.8)}')
sim = 14300 * OCT * 12
p(f'   Línea de datos (Tuenti, combo 6 GB, $14.300/mes, techo): {P(14300*OCT)} por mes = {M(sim,3)} por año')
gps_kit = 1  # [supuesto] 1 rastreador GPS escondido por kit
p(f'   Por kit ({gps_kit} GPS): compra {M(gps_kit*gps_hw_local,3)}; por año {M(gps_kit*sim,3)} (+ reposición de batería/equipo 20% [supuesto] {M(0.2*gps_kit*gps_hw_local,3)})')
p()
# Camioneta
ituran_lista = 22699 / 0.70
p('   Camioneta:')
p(f'   a) AVL municipal (SAE911, proveedor de CP 48/2025 y LPriv 40/2025): precio unitario no publicado. Proxy hardware: PlanetGPS Pluto con cortacorriente lista {P(150084)} -> {P(150084*OCT)} dic-25 + línea {M(sim,3)}/año')
p(f'   b) Ituran recupero: {P(22699)}/mes con 30% de descuento por 3 meses -> lista {P(ituran_lista)}/mes = {P(ituran_lista*OCT)} dic-25 -> {M(ituran_lista*OCT*12,3)} por año (instalación gratis; promo sólo autos particulares)')
ypf_mes = 10454400 / 160 / 2
p(f'   c) YPF telemetría (Bahía Blanca, Dec. 1837/2026, 160 vehículos x 2 meses = $10.454.400): {P(ypf_mes)} por vehículo y mes -> {P(ypf_mes*OCT)} dic-25 -> {M(ypf_mes*OCT*12,3)} por año, equipo en comodato')
van_inst = 0.10e6   # instalación con corte de corriente [supuesto]
van_compra_a = 150084 * OCT + van_inst
van_anual_a = sim + 0.1 * 150084 * OCT
van_anual_c = ypf_mes * OCT * 12
p(f'   Elegida a) compra {M(van_compra_a,3)} (incluye instalación {M(van_inst,2)} [supuesto]); por año {M(van_anual_a,3)}. Techo por servicio c): {M(van_anual_c,3)} por año sin compra')
p()
# Referencias de San Isidro (no se pueden pasar a unidad: cantidad no publicada)
p(f'   San Isidro CP 48/2025 (jun-2025) SOFLEX $12.060.000 -> {M(12060000*k(2025,6))} dic-25; LPriv 40/2025 (mar-2026) SOFLEX $61.989.000 -> {M(61989000*k(2026,3))} dic-25 (presupuesto oficial $62.997.000)')
p()

# ------------------------------------------------------------- 2. SEGURO
p('2. SEGURO (prima anual = tasa x suma asegurada)')
tasas = [('Hartford Symphony (Philadelphia Ins.), 0,53 USD por 100', 0.0053),
         ('AMBA/AFM, 777 USD por 100.000', 777/100000), ('AMBA/AFM, 249 USD por 32.000', 249/32000),
         ('American Harp Society, 0,55 USD por 100', 0.0055),
         ('Supuesto Argentina, robo en tránsito y vía pública [supuesto]', 0.02)]
for n_, t in tasas:
    p(f'   {n_}: tasa {C(t*100,2)}% -> 1 kit {M(t*kit,3)}; 2 kits {M(2*t*kit,3)}; 3 kits {M(3*t*kit,3)}')
t_piso, t_techo = 0.0078, 0.02
p(f'   Rango usado: piso 0,78% (techo de las referencias verificadas) y techo 2% [supuesto]')
p()

# ------------------------------------------------------------- 3. MARCADO
p('3. MARCADO E INVENTARIO')
dremel = 104900 * OCT
p(f'   Lápiz grabador eléctrico Dremel 290 con plantilla (Easy): {P(104900)} -> {M(dremel,3)} dic-25 (uno para todo el programa)')
brl_label = 130.0 / 200   # Brasil: etiqueta patrimonial poliéster 30x15 mm con QR, 200 u por R$130 (TRT3, mapa de precios 2026)
label = brl_label * BRL_USD * USD * 2.0   # x2 traerla o hacerla en la Argentina [supuesto]
labels_kit = 40   # [supuesto] ~27 bienes de uso + cajas y cables
p(f'   Etiqueta QR de poliéster: R$ {C(brl_label,2)} -> {P(brl_label*BRL_USD*USD)} en origen; x2 [supuesto] = {P(label)}; {labels_kit} por kit = {M(labels_kit*label,3)}')
p()

# ------------------------------------------------------------- 4. DEPÓSITO
p('4. DEPÓSITO')
lp76_total = 4252484146.48
dev_orig = 2379 / 1.2379
lp76_unit = lp76_total / dev_orig
p(f'   LP 76/2024 (EXANET): {P(lp76_total)} por {dev_orig:.0f} equipos (2.379 tras +23,79%) = {P(lp76_unit)} por equipo (precios de la oferta mejorada, feb-2025) '
  f'-> {M(lp76_unit*k(2025,2))} dic-25; incluye instalación en vía pública, integración a Milestone y 36 meses de mantenimiento 24/7')
vms_unit = 1083878028 / 2000
p(f'   LP 25/2025 (EXANET, Dec. 1397/2025): {P(1083878028)} / 2.000 licencias = {P(vms_unit)} por licencia (con licencia base y soporte) [tomado como dic-25]; ampliación 650 licencias $351.045.650,80 = {P(351045650.80/650)} c/u (incluye soporte de todo el universo)')
cam_usd = 247.38   # Hanwha QND-6022R 2 MP domo interior IR, A1 Security Cameras (EE. UU.), oferta
cam_local = cam_usd * USD * 1.8
cam_inst = 0.25e6   # cableado, puerto PoE e instalación [supuesto]
cam_b = cam_local + cam_inst + vms_unit
p(f'   Compra menor: Hanwha QND-6022R US$ {C(cam_usd,2)} x1,8 [supuesto] = {M(cam_local,3)} + instalación {M(cam_inst,2)} [supuesto] + licencia VMS {M(vms_unit,3)} = {M(cam_b,3)} por cámara')
acc = (300009 + 200000 + 35809) * OCT + 0.15e6 * 1.0
p(f'   Control de acceso: ZKTeco K20 huella+tarjeta+registro $300.009 + cerradura magnética 280 kg $200.000 (lista) + botón de salida ZKTeco $35.809 -> {M((300009+200000+35809)*OCT,3)} + fuente e instalación {M(0.15e6,2)} [supuesto] = {M(acc,3)}')
for ncam in (2, 4):
    a = ncam * lp76_unit * k(2025, 2) + ncam * vms_unit + acc
    b = ncam * cam_b + acc
    p(f'   {ncam} cámaras + control de acceso: vía ampliación LP 76 (todo incluido) {M(a)}; vía compra menor {M(b)}; por año (compra menor) 10% [supuesto] {M(0.10*b,3)}')
p()

# ------------------------------------------------------------- 5. CONTROL INTERNO
p('5. CONTROL INTERNO (horas de personal municipal)')
hora = 10.0e6 / 1760   # técnico cat. 9: 10,0 M por año (informe Z4a) / 1.760 h [supuesto]
aud_h = 4 * 12          # arqueo sorpresa mensual de 4 h por Patrimonio [supuesto]
p(f'   Hora de agente (cat. 9, Z4a): {P(hora)}; arqueo sorpresa 4 h por mes = {aud_h} h -> {M(aud_h*hora,3)} por año')
p('   Remito de salida y entrada por show (QR + firma de 2 personas): dentro de la jornada ya pagada en Z4a [inferencia]')
p()

# ------------------------------------------------------------- 6. CUENTA FINAL
p('6. CUENTA FINAL (pesos de dic-2025)')
def total(nk, ncam, tasa, van_mode):
    compra = nk * (bultos * tag + gps_kit * gps_hw_local + labels_kit * label) + dremel
    anual = nk * (tag_anual + gps_kit * sim + 0.2 * gps_kit * gps_hw_local + 0.2 * labels_kit * label) + aud_h * hora
    seg = tasa * nk * kit
    if van_mode == 'a':
        compra += van_compra_a; anual += van_anual_a
    else:
        anual += van_anual_c
    dep_c = ncam * cam_b + acc
    compra += dep_c; anual += 0.10 * dep_c
    return compra, anual, seg
for nk in (2, 3):
    for ncam in (2, 4):
        c, a, s_p = total(nk, ncam, t_piso, 'a')
        _, _, s_t = total(nk, ncam, t_techo, 'a')
        p(f'   {nk} kits + camioneta, {ncam} cámaras: COMPRA {M(c)}; POR AÑO sin seguro {M(a)}; seguro {M(s_p)} a {M(s_t)}; '
          f'POR AÑO con seguro {M(a+s_p)} a {M(a+s_t)}')
p()
for nk in (2, 3):
    c, a, s_p = total(nk, 2, t_piso, 'a')
    p(f'   Proporción: {nk} kits, compra antirrobo / valor equipo+camioneta = {C(100*c/(nk*kit+van),1)}%; por año (piso) = {C(100*(a+s_p)/(nk*kit+van),1)}%')
p()
# comparación con alquilar (de Z4a): un evento de sonido alquilado 5,3 a 39 M
p('   Referencia Z4a: alquilar un evento de sonido 5,3 M a 39,0 M (dic-25); costo anual del equipo propio con 2 kits 69,6 M')
# Variante con ampliación LP 76 en el depósito
for nk in (2, 3):
    c, a, s = total(nk, 2, t_piso, 'a')
    dep_b = 2 * cam_b + acc
    dep_a = 2 * lp76_unit * k(2025, 2) + 2 * vms_unit + acc
    p(f'   Variante depósito por ampliación LP 76 (2 cámaras), {nk} kits: COMPRA {M(c - dep_b + dep_a)} (mantenimiento incluido 36 meses)')

open(BASE + '/c23c_raw/w3b_robos_spotify/_tools/calculo_salida.txt', 'w').write('\n'.join(out) + '\n')
