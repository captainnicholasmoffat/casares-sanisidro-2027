# -*- coding: utf-8 -*-
# Cálculo propio [CP]: redes / rejas en desagües de la costa de San Isidro con costos locales.
# Pesos de diciembre de 2025 (IPC INDEC, ch/wt/data/ipc_indec_mensual.csv, dic-2025 = 10121,3715). Dólar $1.520.
# Precios de octubre de 2026 o agosto de 2026: se deflactan con jul-2026 (último IPC del repo) -> quedan algo altos.
import csv
IPC = {}
for r in csv.DictReader(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/data/ipc_indec_mensual.csv')):
    IPC[(int(r['anio']), int(r['mes']))] = float(r['indice'])
BASE = IPC[(2025, 12)]
def k(y, m):
    return BASE / IPC[(y, m)]
USD = 1520.0
out = []
def p(s=''):
    out.append(s); print(s)
def M(x):
    return f'{x/1e6:,.1f} M'.replace(',', 'X').replace('.', ',').replace('X', '.')
def P(x):
    return f'{x:,.0f}'.replace(',', '.')

p('COEFICIENTES IPC (dic-2025 / mes):')
for ym in [(2014,12),(2015,1),(2015,7),(2017,5),(2017,7),(2018,2),(2018,12),(2019,7),(2020,4),(2020,6),(2021,8),(2024,8),(2025,3),(2026,7)]:
    p(f'  {ym[0]}-{ym[1]:02d}: {k(*ym):.4f}')
p()

# ------------------------------------------------------------------ 0. LO QUE HAY HOY
p('0. HOY (informe 11): Marin County US$27.300 por red y año')
p(f'   a $1.447,84 (dólar que usó el informe) = {M(27300*1447.84)}  -> así sale 39,5 M; diez = {M(10*27300*1447.84)}')
p(f'   a $1.520 (dólar de este pedido)       = {M(27300*USD)}; diez = {M(10*27300*USD)}')
p('   Marin: 3 limpiezas por año x (2 personas x 8 h x US$100/h + grúa US$5.000 por medio día + red US$1.500).')
p(f'   Capital Marin por sitio con redes: US$523.000 a US$960.000 = {M(523000*USD)} a {M(960000*USD)}')
p()

# ------------------------------------------------------------------ 1. SUELDOS
p('1. CUADRILLA MUNICIPAL (Decreto 782/2026, anexo: art. 6 Ord. 9422 desde jul-2026; 1 módulo = $1, como en los informes previos)')
cargas = 0.12 + 0.048 + 0.03275   # IPS 12% + IOMA 4,8% + ART 3,275% (LP 44/2025)
pres = 50371                      # art. 20 presentismo, no remunerativo
esc = {'cat6_48h': 652627, 'cat7_48h': 684613, 'cat8_48h': 719501, 'cat9_48h': 755468, 'cat6_40h': 625405}
horas_pagas = {'48h': 48*52, '40h': 40*52}
efectivo = 0.85  # [supuesto] 15% de vacaciones, feriados y licencias
hora = {}
for c, b in esc.items():
    anual = b*13*(1+cargas) + pres*12
    anual_d = anual * k(2026, 7)
    hp = horas_pagas['48h' if '48h' in c else '40h'] * efectivo
    hora[c] = anual_d / hp
    p(f'   {c}: básico {P(b)}/mes (jul-26) -> costo empleador {M(anual)} por año (13 sueldos + 20,075% cargas + presentismo)'
      f' = {M(anual_d)} dic-25; por hora efectiva ({hp:.0f} h) {P(hora[c])} $')
p(f'   Tarifa municipal "hora de peón" (Ordenanza Impositiva 2026, art. 3 b 4): $12.070 [se toma como pesos de dic-25]')
p()

# ------------------------------------------------------------------ 2. CAMIÓN
cam_volmat = 33114 * k(2024, 8)
p('2. CAMIÓN')
p(f'   LP 14/2020 San Isidro (Dec. 1238/2024): camión volcador 5 m3 CON CHOFER $33.114/h IVA incl. (desde 01/08/2024) x {k(2024,8):.4f} = {P(cam_volmat)} $/h dic-25')
p(f'   Ordenanza Impositiva 2026, art. 3 b 2: hora de camión $135.400 (lo que cobra el Municipio a un tercero) = techo')
p()

# ------------------------------------------------------------------ 3. INSTALACIÓN
p('3. INSTALACIÓN DE UNA REJA-CANASTO EN LA BOCA (precios del contrato municipal LP 62/2024, Dec. 1077/2025, redet. 01/03/2025)')
c25 = k(2025, 3)
reja_lo = 223955.41 * c25   # 9.2 reja tipo perimetral, Zona 1, m2, provisión y colocación
reja_hi = 373588.27 * c25   # 9.1 reja tipo Techno, Zona 2, m2
losa_lo = 66600.22 * c25    # vereda HºAº texturado 13-15 cm, Zona 1, m2
losa_hi = 91432.08 * c25    # idem Zona 2
jornal = 294705.37 * c25    # 13.1 personal especializado reparación de herrería, Zona 1, jornal
p(f'   reja $/m2 dic-25: {P(reja_lo)} (perimetral Z1) a {P(reja_hi)} (Techno Z2); losa HºAº $/m2 {P(losa_lo)} a {P(losa_hi)}; jornal herrería {P(jornal)}')
tam = {
  'chica (caño 0,6-0,8 m)':   dict(m2=7.0,  losa=4.0, jorn=(2, 3)),   # canasto 1,0 x 1,0 x 1,5 m
  'mediana (caño 1,0-1,5 m o cajón)': dict(m2=21.2, losa=9.0, jorn=(3, 5)),   # canasto 1,8 x 1,8 x 2,5 m
}
inst = {}
for n, t in tam.items():
    lo = t['m2']*reja_lo + t['losa']*losa_lo + t['jorn'][0]*jornal
    hi = t['m2']*reja_hi + t['losa']*losa_hi + t['jorn'][1]*jornal
    inst[n] = (lo, hi)
    p(f'   {n}: {t["m2"]} m2 de reja + {t["losa"]} m2 de losa + {t["jorn"][0]}-{t["jorn"][1]} jornales = {M(lo)} a {M(hi)}')
diez_lo = 5*inst['chica (caño 0,6-0,8 m)'][0] + 5*inst['mediana (caño 1,0-1,5 m o cajón)'][0]
diez_hi = 5*inst['chica (caño 0,6-0,8 m)'][1] + 5*inst['mediana (caño 1,0-1,5 m o cajón)'][1]
p(f'   DIEZ BOCAS (5 chicas + 5 medianas) [supuesto de mezcla]: {M(diez_lo)} a {M(diez_hi)} una vez (sin proyecto hidráulico: sin precio)')
p()
p('   Alternativa: barrera flotante corta en la boca (15 m):')
osse18 = 379300 / 140 * k(2018, 12)
osse20 = 283140 / 20 * k(2020, 6)
eco_lo = 487424 * k(2026, 7); eco_hi = 980089 * k(2026, 7)
for n, v in [('OSSE 2018, lona, 140 m por $379.300 (Lonería El Vasco)', osse18), ('OSSE 2020, "dinámica" con pollera de red, 2 x 10 m por $283.140 (NUMACO)', osse20),
             ('EcoWay lista oct-2026 BRV1014', eco_lo), ('EcoWay lista oct-2026 BRV1520', eco_hi)]:
    p(f'     {n}: {P(v)} $/m dic-25 -> 15 m = {M(15*v)}')
p(f'   OSSE 2026 (CP 87/26, NUMACO): $36.960.000 (ago-2026, largo no publicado) = {M(36960000*k(2026,7))} dic-25')
p(f'   OSSE 2021 (CP 67/21, NUMACO): $1.100.000 (ago-2021) = {M(1100000*k(2021,8))} dic-25')
p(f'   OSSE 2020 mantenimiento de barrera (CP 10/20, Hydroservices, 4+4 unidades): $348.904 = {M(348904*k(2020,4))} dic-25')
p()

# ------------------------------------------------------------------ 4. OPERACIÓN
p('4. OPERACIÓN POR BOCA Y POR AÑO')
cuad = 2  # dos operarios + camión con chofer (la tarifa del camión incluye chofer)
ceamse_lo, ceamse_hi = 20817.89, 61700 * k(2024, 6)  # CEFIP 2024: período del promedio no aclarado [supuesto: mitad de 2024]
p(f'   CEAMSE: $20.817,89/t (tarifa 2026-27, Norte III, IVA incl.) a ~{P(ceamse_hi)}/t (costo real 2024, CEFIP, llevado a dic-25)')
esc_op = [
  ('semanal (52/año)', 52),
  ('dos por semana: semanal + después de cada lluvia (104/año)', 104),
  ('diario hábil, como dice hoy el documento (250/año)', 250),
]
horas_visita = (0.5, 1.0)   # [supuesto] horas de cuadrilla y camión por boca y por vaciado, con traslado en ruta de 10 bocas
ton = (0.1, 2.0)            # [supuesto con base en San Nicolás 0,5 t/año por boca y Kwinana 0,12 t/año por red]
res = {}
for n, v in esc_op:
    lo = v*horas_visita[0]*(cuad*hora['cat6_48h'] + cam_volmat) + ton[0]*ceamse_lo
    hi = v*horas_visita[1]*(cuad*hora['cat9_48h'] + cam_volmat) + ton[1]*ceamse_hi
    res[n] = (lo, hi)
    p(f'   {n}: {M(lo)} a {M(hi)} por boca y año (cuadrilla + camión + CEAMSE)')
p()
p('   Con la tarifa de la Ordenanza Impositiva (techo, lo que cobraría a un tercero): 2 peones x $12.070 + camión $135.400 = $159.540 por hora')
for n, v in esc_op:
    p(f'     {n}: {M(v*horas_visita[0]*159540)} a {M(v*horas_visita[1]*159540)} por boca y año')
p()
mant = (0.10*inst['chica (caño 0,6-0,8 m)'][0], 0.10*inst['mediana (caño 1,0-1,5 m o cajón)'][1])
p(f'   Mantenimiento y reposición de la reja: 10% de la instalación por año [supuesto] = {M(mant[0])} a {M(mant[1])} por boca')
p()

# ------------------------------------------------------------------ 5. TOTALES
p('5. TOTAL POR BOCA Y POR AÑO (operación + mantenimiento) y DIEZ BOCAS, contra 39,5 M y 395 M')
for n, v in esc_op:
    lo = res[n][0] + mant[0]; hi = res[n][1] + mant[1]
    p(f'   {n}: {M(lo)} a {M(hi)} por boca; diez = {M(10*lo)} a {M(10*hi)}; '
      f'diferencia con 395 M: -{M(395e6-10*hi)} a -{M(395e6-10*lo)}')
p()
# instalación anualizada en 10 años sin interés
for n, (lo, hi) in inst.items():
    p(f'   instalación {n} anualizada a 10 años: {M(lo/10)} a {M(hi/10)} por año')
p()

# ------------------------------------------------------------------ 6. PRECEDENTES EN PESOS DE HOY
p('6. PRECEDENTES ARGENTINOS LLEVADOS A DIC-25')
p(f'   San Isidro, desagüe Perú 2015: $524.062,50 por trimestre -> {M(524062.5*k(2015,2))} el trimestre ene-mar; un año a ese ritmo (feb, may, ago, nov) = {M(524062.5*(k(2015,2)+k(2015,5)+k(2015,8)+k(2015,11)))} (el informe 11 dice 323 M)')
p(f'   San Isidro, desagüe Perú 2017 (LPriv 121/2017): $998.426,80 desde 01/05/2017, plazo no leído -> {M(998426.8*k(2017,5))}')
p(f'   Vicente López 2017, limpieza desembocaduras Melo, Borges y Villate (LP 63/17): $2.498.767,74 -> {M(2498767.74*k(2017,7))} (tres bocas, una vez)')
p(f'   Vicente López 2018, desembocadura Corrientes (LPriv 17/18): $1.200.000 -> {M(1200000*k(2018,2))}')
p(f'   Vicente López 2019, desembocadura Corrientes (LPriv 109/19): $1.800.000 -> {M(1800000*k(2019,7))}')
p(f'   Lanús LP 23/2024: 7.500 h de camión desobstructor con 3 personas, presupuesto $345.112.500 -> {P(345112500/7500*k(2024,8))} $/h dic-25')
p(f'   CABA LPU 7162-1254-LPU23 Limpieza de arroyos (6 renglones, 48 meses desde nov-2023): $121,1 M por mes en total (oct-2023) -> {M(121105150.92*12*k(2023,10))} por año dic-25; por renglón {M(12752845.04*12*k(2023,10))} a {M(27895909.53*12*k(2023,10))} por año')
p(f'   OSSE 2018: barrera de 140 m por $379.300 -> {M(379300*k(2018,12))}; reposición 2020 de 20 m con pollera de red $283.140 -> {M(283140*k(2020,6))}')
open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y4_redes_desagues/calculo_CP.txt', 'w').write('\n'.join(out) + '\n')
