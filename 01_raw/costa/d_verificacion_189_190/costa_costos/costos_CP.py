# Cálculos propios [CP] del pedido "costa_costos" (consulta 02/10/2026).
# Todo en pesos de diciembre de 2025: precio nominal x coef_deflactor del mes del precio (data/deflactor_periodos.csv del repo).
# Para precios posteriores a junio de 2026 (último mes disponible) se usa el coeficiente de junio de 2026.
# Dólares a $1.447,84 (dato del pedido); un precio en dólares se pasa a pesos con ese tipo y no se deflacta.
import csv, io, sys

DEF = {}
for r in csv.DictReader(open('/home/user/casares-sanisidro-2027/data/deflactor_periodos.csv')):
    if r['periodo_tipo'] == 'mes':
        d, m, y = r['periodo_desde'].split('/')
        DEF[f'{y}-{int(m):02d}'] = float(r['coef_deflactor'])
USD = 1447.84
out = io.StringIO()
def p(*a):
    print(*a); print(*a, file=out)
def f(x):
    return f'{x:,.0f}'.replace(',', '.')
def k(mes):
    return DEF[mes]

p('COEFICIENTES USADOS (data/deflactor_periodos.csv, base dic-2025 = 1):')
for m in ['2021-05','2022-02','2022-10','2024-07','2024-09','2024-12','2025-03','2025-10','2026-06']:
    p(f'  {m}: {DEF[m]:.8f}')
p('  Precios de octubre de 2026 (avisos consultados el 02/10/2026): se usa jun-2026 =', DEF['2026-06'], '(último mes disponible)')
p('  Dólar: $', USD)
p()

# ---------------------------------------------------------------- 1. PLAYONES
p('=' * 100)
p('1. COSTO DE HACER UN PLAYÓN, POR AUTO (25 m2 por auto, superficie bruta con circulación)')
p('=' * 100)
# Precios unitarios San Isidro LP 62/2024 (Dec. 1077/2025, anexos I y II), redeterminados desde 01/03/2025
Z1 = dict(excav=12430.01, base=89935.75, tosca=34000.75, granza=208137.64, compact=7458.00, intertrabado=46839.59,
          contrapiso=171855.98, vereda_ha=66600.22, cribado=52782.51, bolardo=291919.41, cartel=298732.08)
Z2 = dict(excav=69778.68, base=107628.82, tosca=50769.77, granza=162719.67, compact=43814.48, intertrabado=45707.03,
          contrapiso=44245.72, vereda_ha=91432.08, cribado=17639.11, bolardo=345808.15, cartel=1069090.22)
# LP 30/2024 (Zona 1, Salvatori), precios de oferta, apertura 03/07/2024 (RESFC-2026-1-SI-SECAMEP, anexo)
L30 = dict(excav=26809.83, tosca=21691.59, subrasante=1224.82, pav_h38=65020.82, calzada=95443.16, contrapiso=27389.70,
           vereda_estr=86741.63, sumidero=810351.88, camara=315016.88, pvc110=14677.86, demarc=42895.72)
# Alumbrado (Dec. 405/2025, anexo I: P.U. del Dec. 35/2025, valores a septiembre de 2024)
ALU = dict(col8=1468741.07, col6=1301512.71, led120=1323609.95, tablero=96127.31, jabalina=69697.61, cable2x4=31401.15)

c25 = k('2025-03'); c24j = k('2024-07'); c24s = k('2024-09')
p('A) Granular: excavación 0,20 m + base de tosca compactada 0,20 m (ítem 7.1, incluye provisión y compactación) + granza 0,05 m')
res = {}
for nom, Z in [('Zona 2 (La Mantovana, incluye la costa)', Z2), ('Zona 1 (Salvatori)', Z1)]:
    m2 = 0.20 * Z['excav'] + 0.20 * Z['base'] + 0.05 * Z['granza']
    p(f'   {nom}: 0,20 x {f(Z["excav"])} + 0,20 x {f(Z["base"])} + 0,05 x {f(Z["granza"])} = {f(m2)} $/m2 (mar-25)'
      f' x {c25:.4f} = {f(m2*c25)} $/m2 dic-25 -> por auto (25 m2): {f(m2*c25*25)}')
    res['gran_' + nom[:6]] = m2 * c25 * 25
p('B) Pavimento')
for nom, Z in [('Zona 2', Z2), ('Zona 1', Z1)]:
    m2 = 0.25 * Z['excav'] + 0.15 * Z['base'] + Z['intertrabado']
    p(f'   B1 intertrabado 8 cm, {nom}: 0,25 x {f(Z["excav"])} + 0,15 x {f(Z["base"])} + {f(Z["intertrabado"])} = {f(m2)} $/m2 (mar-25)'
      f' -> {f(m2*c25)} $/m2 dic-25 -> por auto {f(m2*c25*25)}')
    res['inter_' + nom] = m2 * c25 * 25
for nom, item in [('pavimento de hormigón H38 0,19-0,24 m (ítem 2.1.2)', 'pav_h38'), ('construcción de calzada de hormigón (ítem 2.1.1)', 'calzada')]:
    m2 = 0.35 * L30['excav'] + 0.15 * L30['tosca'] + L30['subrasante'] + L30[item]
    p(f'   B2 LP 30/2024 {nom}: 0,35 x {f(L30["excav"])} + 0,15 x {f(L30["tosca"])} + {f(L30["subrasante"])} + {f(L30[item])} = {f(m2)} $/m2 (jul-24)'
      f' x {c24j:.4f} = {f(m2*c24j)} $/m2 dic-25 -> por auto {f(m2*c24j*25)}')
    res['horm_' + item] = m2 * c24j * 25
p('C) Desagüe, por playón de 25 autos (625 m2) [supuesto de diseño]')
d1 = L30['sumidero'] + L30['camara'] + 30 * L30['pvc110']
p(f'   C1 pavimentado: 1 sumidero 50x100 con rejas {f(L30["sumidero"])} + 1 cámara 40x60 {f(L30["camara"])} + 30 m caño PVC 110 x {f(L30["pvc110"])}'
  f' = {f(d1)} (jul-24) -> {f(d1*c24j)} dic-25 -> por auto {f(d1*c24j/25)}')
for nom, Z in [('Zona 2', Z2), ('Zona 1', Z1)]:
    d2 = 62.5 * Z['cribado']
    p(f'   C2 granular, {nom}: 62,5 m de caño cribado (1 m cada 10 m2) x {f(Z["cribado"])} = {f(d2)} (mar-25) -> {f(d2*c25)} dic-25 -> por auto {f(d2*c25/25)}')
    res['dren_' + nom] = d2 * c25 / 25
res['dren_pav'] = d1 * c24j / 25
p('D) Iluminación básica: 1 columna de acero 8 m + luminaria LED hasta 120 W + tablero + jabalina + 30 m de cable subterráneo 2x4,')
p('   una cada 500 m2 (20 autos) [supuesto de diseño]. El anexo dice "precios unitarios de materiales"; no aclara si incluye montaje [SC].')
col = ALU['col8'] + ALU['led120'] + ALU['tablero'] + ALU['jabalina'] + 30 * ALU['cable2x4']
p(f'   {f(ALU["col8"])} + {f(ALU["led120"])} + {f(ALU["tablero"])} + {f(ALU["jabalina"])} + 30 x {f(ALU["cable2x4"])} = {f(col)} (sep-24)'
  f' x {c24s:.4f} = {f(col*c24s)} dic-25 por columna -> por auto {f(col*c24s/20)}')
luz = col * c24s / 20
gran_lo = min(res['gran_Zona 2'], res['gran_Zona 1']) + min(res['dren_Zona 2'], res['dren_Zona 1']) + luz
gran_hi = max(res['gran_Zona 2'], res['gran_Zona 1']) + max(res['dren_Zona 2'], res['dren_Zona 1']) + luz
pav_lo = min(res['inter_Zona 2'], res['inter_Zona 1'], res['horm_pav_h38']) + res['dren_pav'] + luz
pav_hi = max(res['inter_Zona 2'], res['inter_Zona 1'], res['horm_calzada']) + res['dren_pav'] + luz
p(f'TOTAL POR AUTO, granular con desagüe y luz: {f(gran_lo)} a {f(gran_hi)}  (US$ {f(gran_lo/USD)} a {f(gran_hi/USD)})')
p(f'TOTAL POR AUTO, pavimentado con desagüe y luz: {f(pav_lo)} a {f(pav_hi)}  (US$ {f(pav_lo/USD)} a {f(pav_hi/USD)})')
p(f'Ejemplo: playón de 2.000 m2 (80 autos): granular {f(80*gran_lo)} a {f(80*gran_hi)}; pavimentado {f(80*pav_lo)} a {f(80*pav_hi)}')
p()
p('Lugares candidatos: autos = superficie / 25 (rango /30 a /20)')
cands = [('San Isidro R: playón subsuelo + frente (OSM 434818625 + 439428388)', 702 + 508),
         ('Las Barrancas: franja junto a las vías (OSM 437690570)', 635),
         ('Las Barrancas: jardín de la estación (2.018 - 635 m2, con árboles)', 2018 - 635),
         ('Anchorena: franja oeste (OSM 312158334 + 312158332 + 312158333)', 697 + 147 + 75),
         ('Béccar (Mitre): terreno junto a las vías, fuera de 6 m de vía (OSM 439569614)', 2002),
         ('Acassuso (Mitre): playón del supermercado (OSM 435067923)', 2579),
         ('Martínez (Mitre): playón Av. Santa Fe 2399 (OSM 435022138)', 1297),
         ('San Isidro centro: playón Maipú 501 (OSM 436484625)', 723)]
for n, a in cands:
    p(f'   {n}: {f(a)} m2 -> {round(a/25)} autos ({round(a/30)} a {round(a/20)})')
p()

# ---------------------------------------------------------------- 2. CONTEO
p('=' * 100)
p('2. CONTAR AUTOS: 1 cámara con conteo por cruce de línea en cada acceso, en columna propia, con energía y 4G')
p('=' * 100)
cam_lo, cam_hi = 994.24 * USD, 1247.48 * USD
col6 = ALU['col6'] * c24s; tab = ALU['tablero'] * c24s; jab = ALU['jabalina'] * c24s; cab = 30 * ALU['cable2x4'] * c24s
rout = 237 * USD
p(f'   cámara HD (CABA, DANAIDE S.A., set-2025, US$ 994,24 a 1.247,48 [moneda inferida]) = {f(cam_lo)} a {f(cam_hi)}')
p(f'   columna acero 6 m: {f(ALU["col6"])} x {c24s:.4f} = {f(col6)}; tablero {f(tab)}; jabalina {f(jab)}; 30 m cable {f(cab)}')
p(f'   router 4G industrial (Teltonika RUT241, aviso EE.UU. US$ 237) = {f(rout)}')
acc_lo = cam_lo + col6 + tab + jab + cab + rout; acc_hi = cam_hi + col6 + tab + jab + cab + rout
p(f'   POR ACCESO: {f(acc_lo)} a {f(acc_hi)} (sin mano de obra de montaje ni integración de software [SC])')
p(f'   21 playones con 1 acceso: {f(21*acc_lo)} a {f(21*acc_hi)};  con 26 accesos (5 playones grandes con 2): {f(26*acc_lo)} a {f(26*acc_hi)}')
m2m = 8000 * 12 * DEF['2026-06']
p(f'   Por año: línea de datos ~$8.000/mes [SC] x 12 x {DEF["2026-06"]:.4f} = {f(m2m)} por acceso -> 21 accesos {f(21*m2m)}')
p(f'   Mantenimiento: sin precio público; supuesto 10% de la inversión por año = {f(0.1*21*acc_lo)} a {f(0.1*21*acc_hi)} [supuesto]')
s_lo, s_hi = 1090 * 115 * USD, 1090 * 160 * USD
p(f'   Alternativa sensor por plaza: 1.090 plazas x US$ 115 a 160 = {f(s_lo)} a {f(s_hi)} (sólo sensores; faltan gateways e instalación)')
p()

# ---------------------------------------------------------------- 3. BICIS
p('=' * 100)
p('3. BICICLETEROS Y BICISENDAS')
p('=' * 100)
bl = 1178900 / 100 * DEF['2022-02']; bm = 60000 / 5 * DEF['2022-10']
p(f'   Bicicletero por lugar: Lobos 100 "monociclos" por $1.178.900 (feb-22) = $11.789 c/u x {DEF["2022-02"]:.4f} = {f(bl)}')
p(f'                          Gral. Pueyrredon, 5 bicicleteros valuados en $60.000 (oct-22) = $12.000 c/u x {DEF["2022-10"]:.4f} = {f(bm)}')
nb = 4 * 10 + 9 * 10
p(f'   Propuesta de cantidades [supuesto]: 10 lugares en cada estación del TdlC (40) + 10 en cada uno de 9 accesos a la costa (90) = {nb} lugares -> {f(nb*bm)} a {f(nb*bl)}')
# largos
mit = {'Martínez -> Pacheco y el río': (1700, 1669), 'Acassuso -> Perú Beach': (1626, 1588), 'San Isidro C -> Parque del Puerto': (1906, 1906), 'Béccar -> Paseo 33 Orientales': (1983, 1983)}
tdc = {'Anchorena -> Pacheco y el río': (544, 511), 'Las Barrancas -> Perú Beach': (307, 134), 'San Isidro R -> Parque del Puerto': (536, 536), 'Punta Chica -> Paseo 33 Orientales': (820, 820)}
km_m = sum(v[1] for v in mit.values()) / 1000; km_t = sum(v[1] for v in tdc.values()) / 1000
p(f'   Largos (OSRM bicicleta sobre OSM): Mitre {sum(v[0] for v in mit.values())} m, sin ciclovía existente {km_m*1000:.0f} m; TdlC {sum(v[0] for v in tdc.values())} m, sin ciclovía {km_t*1000:.0f} m')
# costo por km
lp = 43784344 * DEF['2021-05']
for L in (5582, 5642):
    p(f'   La Plata LP 15/2021 ciclovías Diag. 73 y 74 con separadores: $43.784.344 (may-21) x {DEF["2021-05"]:.4f} = {f(lp)} / {L/1000:.3f} km = {f(lp/(L/1000))} por km')
pint_lo = (250 * L30['demarc'] * c24j) + (100 * Z1['bolardo'] * c25) + (10 * Z1['cartel'] * c25)
pint_hi = (250 * L30['demarc'] * c24j) + (100 * Z2['bolardo'] * c25) + (10 * Z2['cartel'] * c25)
p(f'   Armado con precios de San Isidro: demarcación 250 m2/km x {f(L30["demarc"])} (jul-24) + 100 bolardos/km x {f(Z1["bolardo"])} a {f(Z2["bolardo"])} (mar-25)'
  f' + 10 carteles/km x {f(Z1["cartel"])} a {f(Z2["cartel"])} (mar-25) = {f(pint_lo)} a {f(pint_hi)} por km')
pint_lo5 = pint_lo + 100 * Z1['bolardo'] * c25; pint_hi5 = pint_hi + 100 * Z2['bolardo'] * c25
p(f'      con un bolardo cada 5 m: {f(pint_lo5)} a {f(pint_hi5)} por km')
bs = {}
bs['LP30 contrapiso'] = (L30['contrapiso'] + L30['subrasante'] + 0.10 * L30['tosca']) * 2500 * c24j
bs['LP30 vereda estructural'] = (L30['vereda_estr'] + L30['subrasante'] + 0.10 * L30['tosca']) * 2500 * c24j
bs['LP62 Z2 contrapiso'] = (Z2['contrapiso'] + 0.10 * Z2['base']) * 2500 * c25
bs['LP62 Z2 vereda HA'] = (Z2['vereda_ha'] + 0.10 * Z2['base']) * 2500 * c25
for n, v in bs.items():
    p(f'   Bicisenda construida 2,5 m ({n}): {f(v)} por km')
b_lo, b_hi = min(bs.values()), max(bs.values())
pnt_lo, pnt_hi = pint_lo, lp / 5.582
p(f'   RANGO pintada con separadores: {f(pnt_lo)} a {f(pnt_hi)} por km;  construida: {f(b_lo)} a {f(b_hi)} por km')
p(f'   Mitre ({km_m:.3f} km): pintada {f(km_m*pnt_lo)} a {f(km_m*pnt_hi)}; construida {f(km_m*b_lo)} a {f(km_m*b_hi)}')
p(f'   TdlC ({km_t:.3f} km): pintada {f(km_t*pnt_lo)} a {f(km_t*pnt_hi)}; construida {f(km_t*b_lo)} a {f(km_t*b_hi)}')
p()

# ---------------------------------------------------------------- 4. NÁUTICA
p('=' * 100)
p('4. ESCUELA NÁUTICA: UN GRUPO MÁS DE 10 ALUMNOS, 2 CLASES DE 4 HORAS POR SEMANA, TODO EL AÑO')
p('=' * 100)
cargas = 0.12 + 0.048 + 0.03275
p(f'   Cargas patronales: IPS 12% + IOMA 4,8% + ART 3,275% = {cargas*100:.3f}%')
c12 = 579809 * DEF['2025-10']
c12_anual = c12 * 13 * (1 + cargas)
p(f'   Cat. 12 (35 h): 579.809 módulos/mes (Presupuesto 2026, tratado como oct-25) x {DEF["2025-10"]:.4f} = {f(c12)}/mes; x 13 (con aguinaldo) x {1+cargas:.5f} = {f(c12_anual)} por año el cargo entero')
p(f'      prorrateado a 8 de 35 horas: {f(c12_anual*8/35)} por año por grupo')
prof = 29806 * 8 * DEF['2025-10']
prof_anual = prof * 13 * (1 + cargas)
p(f'   Profesor de Deportes (cat. 991, clase A): 29.806 módulos por hora semanal x 8 h = 238.448/mes x {DEF["2025-10"]:.4f} = {f(prof)}/mes; por año con aguinaldo y cargas {f(prof_anual)}')
kay = 10 * (928935 + 64703 + 71764) * DEF['2026-06']
sup = 10 * (672516 + 71764) * DEF['2026-06']
p(f'   Equipo kayak: 10 x (kayak Rocker One $928.935 + pala $64.703 + chaleco $71.764) = {f(10*(928935+64703+71764))} (oct-26) x {DEF["2026-06"]:.4f} = {f(kay)}')
p(f'   Equipo SUP: 10 x (tabla Z-Ray E10 $672.516 + chaleco $71.764) = {f(10*(672516+71764))} x {DEF["2026-06"]:.4f} = {f(sup)}')
si24 = 14840000 * DEF['2024-12']
p(f'   Compra del Municipio dic-2024 (kayaks, remos y chalecos, cantidades no publicadas): $14.840.000 x {DEF["2024-12"]:.4f} = {f(si24)}')
opt = 5 * 3550 * USD
p(f'   Vela: 5 Optimist x US$ 3.550 [SC] = {f(opt)}; ILCA/Laser: sin precio argentino encontrado')
p(f'   Reposición y mantenimiento del equipo: supuesto 10% por año = {f(0.1*kay)}')
p()

# ---------------------------------------------------------------- TOTALES
p('=' * 100)
p('TOTALES DEL PAQUETE DE REFERENCIA [supuesto: qué se incluye]')
p('=' * 100)
inv = {
 'Playón nuevo de 80 autos (ej. Béccar), granular': (80 * gran_lo, 80 * gran_hi),
 'Conteo en los 21 playones (1 acceso c/u)': (21 * acc_lo, 21 * acc_hi),
 'Bicicleteros: 130 lugares': (nb * bm, nb * bl),
 'Ciclovía pintada con separadores, 4 tramos del Mitre': (km_m * pnt_lo, km_m * pnt_hi),
 'Escuela náutica: equipo kayak para 1 grupo': (kay, kay),
}
anual = {
 'Conteo: datos móviles (21 líneas)': (21 * m2m, 21 * m2m),
 'Conteo: mantenimiento (10% de la inversión, supuesto)': (0.1 * 21 * acc_lo, 0.1 * 21 * acc_hi),
 'Escuela náutica: instructor (cat. 12 prorrateada a profesor 8 h)': (c12_anual * 8 / 35, prof_anual),
 'Escuela náutica: reposición de equipo (10%, supuesto)': (0.1 * kay, 0.1 * kay),
}
ti = [0, 0]; ta = [0, 0]
for n, (a, b) in inv.items():
    p(f'   INVERSIÓN  {n}: {f(a)} a {f(b)}'); ti[0] += a; ti[1] += b
p(f'   TOTAL INVERSIÓN UNA VEZ: {f(ti[0])} a {f(ti[1])}  (US$ {f(ti[0]/USD)} a {f(ti[1]/USD)})')
for n, (a, b) in anual.items():
    p(f'   POR AÑO    {n}: {f(a)} a {f(b)}'); ta[0] += a; ta[1] += b
p(f'   TOTAL GASTO POR AÑO: {f(ta[0])} a {f(ta[1])}  (US$ {f(ta[0]/USD)} a {f(ta[1]/USD)})')
p('   Fuera del paquete: tramos del TdlC, bicisenda construida en vez de pintada, playón pavimentado, mantenimiento de ciclovías y bicicleteros (sin dato).')

open('/tmp/claude-0/-home-user-casares-sanisidro-2027/857d907d-1df2-5f28-86f9-ac141afedba7/scratchpad/costa_costos/calculo/calculo_CP.txt', 'w').write(
    'Cálculos propios [CP] - generado por calculo/costos_CP.py - pesos de diciembre de 2025\n\n' + out.getvalue())
