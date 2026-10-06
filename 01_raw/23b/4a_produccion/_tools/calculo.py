# -*- coding: utf-8 -*-
# Cálculo propio [cálculo propio]: equipo municipal de producción para artistas callejeros y shows de emergentes (San Isidro).
# Todo en pesos de diciembre de 2025 (IPC INDEC del repo: ch/wt/data/ipc_indec_mensual.csv; dic-2025 = 10121,3715).
# Precios posteriores a jul-2026 (último IPC del repo) se deflactan con jul-2026 = 12076,3937 -> quedan algo altos.
# Dólar: $1.447,84 (BCRA, Com. A 3500, promedio dic-2025), ya en pesos de dic-2025 (regla del cliente del 06/10/2026).
# Euro: relación euro/dólar del BNA, divisas venta 05/10/2026 (1706,504 / 1520).
import csv, os
BASE_DIR = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad'
IPC = {}
for r in csv.DictReader(open(BASE_DIR + '/ch/wt/data/ipc_indec_mensual.csv')):
    IPC[(int(r['anio']), int(r['mes']))] = float(r['indice'])
B = IPC[(2025, 12)]
def k(y, m):
    if (y, m) > (2026, 7):
        y, m = 2026, 7
    return B / IPC[(y, m)]
USD = 1447.84
EUR_USD = 1706.504 / 1520.0
out = []
def p(s=''):
    out.append(s); print(s)
def P(x):
    return f'{x:,.0f}'.replace(',', '.')
def M(x):
    return f'{x/1e6:,.1f} M'.replace(',', 'X').replace('.', ',').replace('X', '.')

p('COEFICIENTES IPC (dic-2025 / mes): ' + '; '.join(f'{y}-{m:02d} {k(y,m):.4f}' for y, m in
  [(2024,2),(2024,6),(2025,2),(2025,3),(2025,6),(2025,8),(2025,11),(2025,12),(2026,2),(2026,3),(2026,6),(2026,7)]))
p(f'Dólar {USD} ; euro/dólar {EUR_USD:.4f} ; euro en pesos dic-25 = {EUR_USD*USD:,.0f}')
p()

# ---------------------------------------------------------------- 1. EQUIPO
OCT = k(2026, 10)   # precios vistos el 06/10/2026 -> se deflactan con jul-2026
p('1. EQUIPO POR KIT (precios de comercio con precio visible, 06/10/2026, IVA incluido; deflactados con jul-2026)')
kit = [
 # (ítem, cantidad, precio nominal, fuente, vida útil años)
 ('Columna PA a batería JBL EON ONE PRO (6 h, mezcladora de 6 canales)', 2, 3032808.34, 'Todo Música', 7),
 ('Mezcladora digital Behringer X-Air XR18 (16 entradas, se maneja con tablet)', 1, 1450100.00, 'Hendrix', 7),
 ('Monitor de piso activo dB Technologies B-Hype 10', 2, 877044.11, 'Todo Música', 7),
 ('Estación de energía EcoFlow Delta 3 1500 (1.536 Wh, LFP)', 1, 2890990.00, 'EcoFlow Store AR', 8),
 ('Micrófono Shure SM58', 4, 266688.63, 'Todo Música', 10),
 ('Micrófono Shure SM57', 3, 243426.06, 'Todo Música', 10),
 ('Caja directa pasiva Samson MD1', 2, 172549.10, 'Todo Música', 7),
 ('Pie de micrófono con brazo Quik Lok Microlite', 7, 89765.79, 'Todo Música', 5),
 ('Cable XLR 6 m Quik Lok', 10, 37343.43, 'Todo Música', 3),
 ('Cable plug 3 m Planet Waves', 4, 80079.35, 'Todo Música', 3),
]
sub = 0; anual = 0
for n, q, pr, src, vu in kit:
    v = q * pr * OCT
    sub += v; anual += v / vu
    p(f'   {q} x {n} ({src}): {P(q*pr)} nominal -> {M(v)} dic-25 ; vida útil {vu} años')
misc = 0.05 * sub
p(f'   Varios (zapatillas, prolongaciones, estuches, cinta) [supuesto 5%]: {M(misc)}')
sonido = sub + misc
anual += misc / 3
p(f'   SUBTOTAL SONIDO por kit: {M(sonido)} ; amortización lineal {M(anual)} por año')
p()
# Tarima: no encontré precio local visible. Referencia: comercio de España, Contest PLTS-2x1 387,60 € sin IVA; patas ~40 €/u [supuesto].
mod_eur = 387.60 + 4 * 40.0
mod_origen = mod_eur * EUR_USD * USD
for fac in (1.6, 2.0):
    p(f'   Tarima 2x1 m (Contest PLTS-2x1 + 4 patas) puesta en la Argentina, factor de importación x{fac} [supuesto]: '
      f'{M(mod_origen*fac)} por módulo -> 2x4 m (4 módulos) {M(4*mod_origen*fac)} ; 3x4 m (6 módulos) {M(6*mod_origen*fac)}')
tarima24 = 4 * mod_origen * 1.8   # punto medio
tarima34 = 6 * mod_origen * 1.8
p(f'   -> se usa el punto medio x1,8: 2x4 m {M(tarima24)} ; 3x4 m {M(tarima34)} [cálculo propio, sin confirmar]; vida útil 10 años')
p(f'   Alquiler de referencia: General Villegas cobra $100.000 por una tarima de 4x3 m (Ord. 6742/25, tarifa 2026) = {M(100000*k(2025,12))} por día [supuesto: pesos de dic-25]')
toldo = 311992 * OCT
p(f'   Toldo/gazebo 3x6 m de caño y rafia (Easy, uso hogareño): {M(toldo)} ; vida útil 2 años [supuesto]. Un gazebo profesional reforzado: sin precio visible')
p()
kit24 = sonido + tarima24 + toldo
kit34 = sonido + tarima34 + toldo
am24 = anual + tarima24/10 + toldo/2
am34 = anual + tarima34/10 + toldo/2
p(f'   KIT COMPLETO con tarima 2x4: {M(kit24)} ; amortización {M(am24)} por año')
p(f'   KIT COMPLETO con tarima 3x4: {M(kit34)} ; amortización {M(am34)} por año')
liviano = (1997600 + 2*266688.63 + 2*89765.79 + 4*37343.43) * OCT
p(f'   Punto liviano extra (1 JBL EON ONE Compact a batería 12 h, Hendrix $1.997.600 + 2 SM58 + 2 pies + 4 cables): {M(liviano)}')
p()

# ---------------------------------------------------------------- 2. TRASLADO
p('2. TRASLADO')
master_l1 = 62170000 * OCT
master_l3 = 68080000 * OCT
p(f'   Renault Master L1H1 furgón, precio de lista oct-2026 (Autocosmos) $62.170.000 -> {M(master_l1)} dic-25 ; L3H2 $68.080.000 -> {M(master_l3)}')
for n, v, ym in [('Coronel Suárez, furgón 0 km con puertas corredizas (LPriv 6/2025)', 32790000, (2025,2)),
                 ('Trenque Lauquen, utilitario tipo furgón (CP 74/2025)', 28000000, (2025,6)),
                 ('Veinticinco de Mayo, presupuesto oficial por furgón chico ($62 M / 2)', 31000000, (2025,3))]:
    p(f'   {n}: {P(v)} -> {M(v*k(*ym))} dic-25 (furgón chico: no entra una tarima de 2 m de largo con comodidad [inferencia])')
van_op = 0.10   # [supuesto] seguro + mantenimiento + combustible, 10% del precio por año
p(f'   Costo de uso de la camioneta [supuesto 10% del precio por año]: {M(van_op*master_l1)} ; vida útil 10 años -> amortización {M(master_l1/10)}')
p()

# ---------------------------------------------------------------- 3. PERSONAS
p('3. PERSONAS (escala del Decreto 782/2026, anexo, art. 6 Ord. 9422, desde jul-2026; 1 módulo = $1 como en informes previos [supuesto])')
cargas = 0.12 + 0.048 + 0.03275   # IPS + IOMA + ART, como en el informe Y4
pres = 50371
esc40 = {6: 625405, 7: 656559, 8: 719501, 9: 723994, 10: 793785}
esc48 = {6: 652627, 7: 684613, 8: 719501, 9: 755468, 10: 793785}
def costo(b):
    return (b * 13 * (1 + cargas) + pres * 12) * k(2026, 7)
for c in sorted(esc40):
    p(f'   cat {c}: 40 h {P(esc40[c])}/mes -> {M(costo(esc40[c]))} por año dic-25 ; 48 h {P(esc48[c])} -> {M(costo(esc48[c]))}')
def equipo(n_kits, cob=0.15):
    tec = n_kits * costo(esc40[9]); asi = n_kits * costo(esc40[6])
    cho = (1 if n_kits <= 2 else 2) * costo(esc40[7])
    base = tec + asi + cho
    return base, base * (1 + cob)
for nk in (2, 3):
    b, c = equipo(nk)
    p(f'   {nk} kits: {nk} técnicos de sonido (cat 9) + {nk} asistentes (cat 6) + {1 if nk<=2 else 2} chofer (cat 7), régimen 40 h: {M(b)} por año; '
      f'con 15% de reemplazos por vacaciones y licencias [supuesto]: {M(c)}')
p()
# Opción B: personal que ya existe, pagado como «tareas especiales» (Dec. 189/2026, anexo, valores de feb-2026)
j = {7: 59186, 8: 62964, 9: 65483}
p('   Opción B: agentes actuales con «tareas especiales en eventos» (Dec. 189/2026, valor por jornada de 8 h, feb-2026):')
for dias in (120, 160, 200):
    dia2 = 2*j[9] + 2*j[7] + j[8]
    dia3 = 3*j[9] + 3*j[7] + 2*j[8]
    p(f'     {dias} días: 2 kits {M(dia2*dias*k(2026,2))} ; con cargas [supuesto +20%] {M(dia2*dias*k(2026,2)*(1+cargas))} ; '
      f'3 kits {M(dia3*dias*k(2026,2)*(1+cargas))} (con cargas)')
p()

# ---------------------------------------------------------------- 4. TOTALES
p('4. TOTAL DEL EQUIPO DE PRODUCCIÓN')
for nk, tar, kv, am in [(2, '2x4', kit24, am24), (2, '3x4', kit34, am34), (3, '2x4', kit24, am24)]:
    van = master_l1 if nk == 2 else master_l3
    compra = nk * kv + van
    b, per = equipo(nk)
    anual_t = nk * am + van/10 + van_op*van + per
    p(f'   {nk} kits con tarima {tar}: COMPRA {M(compra)} (equipos {M(nk*kv)} + camioneta {M(van)}) ; '
      f'POR AÑO {M(anual_t)} (amortización equipos {M(nk*am)} + camioneta {M(van/10+van_op*van)} + personas {M(per)})')
    for dias in (120, 160, 200):
        p(f'      por día de trabajo ({dias} días): {M(anual_t/dias)} por día para los {nk} kits ; {M(anual_t/dias/nk)} por kit y día')
p()
p('   Comparación con alquilar por evento (referencias):')
for n, v, ym in [('San Isidro, LPriv 3/2026, «servicio integral de sonido y proyección» (adjudicado mar-2026; cantidad de servicios no publicada)', 77800000, (2026,3)),
                 ('San Isidro, CP 35/2025, sonido e iluminación para el «Cierre de Verano» (1 evento)', 32200000, (2025,3)),
                 ('San Isidro, CP 7/2024, alquiler de sonido para el Carnaval 2024', 2528900, (2024,2)),
                 ('San Isidro, CP 101/2024, sistema de sonido con estructuras Layher', 5987000, (2024,6)),
                 ('Coronel Pringles, escenario secundario para shows locales con sonido, luces y pantalla (1 día)', 5900000, (2025,2))]:
    p(f'     {n}: {P(v)} -> {M(v*k(*ym))} dic-25')
p()

# ---------------------------------------------------------------- 5. CACHETS
p('5. CACHETS (pesos de dic-2025)')
sadem = 343250 * k(2026, 3)
p(f'   SADEM, tarifa mínima «festivales/fiesta municipal y/o recital» desde 1/3/2026: $343.250 por músico -> {P(sadem)} dic-25')
fmt = {'solista': 1, 'dúo': 2, 'trío': 3, 'banda de 4': 4, 'banda de 5': 5}
for f, n in fmt.items():
    p(f'     {f}: piso SADEM {P(n*sadem)}')
obs = [
 ('Coronel Suárez, banda local en «Suárez Rock» (jun-2025)', 400000, (2025,6)),
 ('Coronel Suárez, banda local en «Suárez Rock» (jun-2025)', 470000, (2025,6)),
 ('Coronel Suárez, banda en «Suárez Peatonal» (feb-2025)', 600000, (2025,2)),
 ('Coronel Suárez, banda en «Suárez Peatonal» (ago-2025)', 800000, (2025,8)),
 ('Coronel Suárez, banda en «Suárez Peatonal» (dic-2025)', 2185000, (2025,12)),
 ('Coronel Pringles, cantante solista (ago-2026)', 700000, (2026,7)),
 ('Coronel Pringles, banda soporte (jul-2026)', 975000, (2026,7)),
 ('Bahía Blanca, banda emergente, Ciclo Relámpago, subsidio de producción (jul-sep 2026)', 300000, (2026,7)),
 ('Campana, producción de un quinteto de tango (jul-2026)', 1890000, (2026,7)),
 ('Zárate (Lima), grupo musical regional, Carnaval (feb-2026)', 1000000, (2026,2)),
 ('Zárate (Lima), grupo musical regional, Carnaval (feb-2026)', 5500000, (2026,2)),
 ('Ciudad de Buenos Aires, FIBA 2026: $3.000.000 por al menos 2 funciones (feb-2026), por función', 1500000, (2026,2)),
]
for n, v, ym in obs:
    p(f'   {n}: {P(v)} -> {P(v*k(*ym))}')
p()
# Mezcla de formatos [supuesto]: 40% solistas, 30% dúos o tríos (2,5 músicos), 30% bandas de 4-5 (4,5 músicos)
mus = 0.4*1 + 0.3*2.5 + 0.3*4.5
prom_piso = mus * sadem
prom_rec = mus * sadem * 1.25   # [supuesto] piso + 25% por ensayo y traslado de instrumentos (SADEM transporte B/C ~ $25-53 mil)
p(f'   Mezcla supuesta (40% solistas, 30% dúos/tríos, 30% bandas de 4-5): {mus:.2f} músicos por show')
p(f'   Cachet promedio al piso SADEM: {P(prom_piso)} ; piso + 25% [supuesto]: {P(prom_rec)}')
for canc in (0.0, 0.10, 0.15):
    for n in (50, 100, 150, 300):
        p(f'     {n} shows, cancelaciones reprogramadas {int(canc*100)}% [supuesto]: piso {M(n*prom_piso*(1+canc))} ; piso+25% {M(n*prom_rec*(1+canc))}')
p()
p('   Capacidad: 2 kits x 160 días = 320 jornadas; si cada jornada tiene 4 turnos de 1 h -> 1.280 turnos para callejeros por año [cálculo propio]')

p()
p('6. PROGRAMA COMPLETO POR AÑO (equipo de 2 kits con tarima 2x4 + cachets piso+25% con 10% de cancelaciones reprogramadas)')
b2, per2 = equipo(2)
eq_anual = 2*am24 + master_l1/10 + van_op*master_l1 + per2
for n in (50, 100, 150):
    c = n*prom_rec*1.10
    p(f'   {n} shows: equipo {M(eq_anual)} + cachets {M(c)} = {M(eq_anual + c)} por año ; primer año con compra: {M(2*kit24 + master_l1 + per2 + van_op*master_l1 + c)}')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calculo_salida.txt'), 'w').write('\n'.join(out) + '\n')
