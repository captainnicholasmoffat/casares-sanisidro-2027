# -*- coding: utf-8 -*-
# Z1 · Redes y rejas en los desagües de la costa de San Isidro, sin que tapen ni inunden.
# Cálculo propio [cálculo propio]. Pesos de diciembre de 2025 con el IPC del repo
# (ch/wt/data/ipc_indec_mensual.csv; dic-2025 = 10121,3715; último mes jul-2026 = 12076,3937, usado para precios posteriores).
# Dólar: $1.274 (ya en pesos de dic-2025, consigna del cliente). Los US$ se convierten sin actualizar por inflación de EE. UU.
# Salida: ../calculo.txt
import csv, os

RAIZ = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad'
IPC = {}
for r in csv.DictReader(open(RAIZ + '/ch/wt/data/ipc_indec_mensual.csv')):
    IPC[(int(r['anio']), int(r['mes']))] = float(r['indice'])
BASE = IPC[(2025, 12)]
ULT = max(IPC)


def k(y, m):
    """coeficiente para llevar pesos del mes (y,m) a pesos de dic-2025; meses sin IPC usan el último (jul-2026)"""
    return BASE / IPC.get((y, m), IPC[ULT])


USD = 1447.84
out = []


def p(s=''):
    out.append(s)
    print(s)


def M(x):
    return (f'{x/1e6:,.1f} M').replace(',', 'X').replace('.', ',').replace('X', '.')


def P(x):
    return f'{x:,.0f}'.replace(',', '.')


p('Z1 · CÁLCULO PROPIO. Pesos de dic-2025. Dólar $1.447,84 (BCRA Com. A 3500, promedio dic-2025; rehecho por el coordinador). Todo lo marcado [supuesto] es una hipótesis mía, no un dato.')
p()
p('0. COEFICIENTES IPC (dic-2025 / mes)')
for ym in [(2014, 12), (2018, 12), (2020, 6), (2020, 9), (2021, 9), (2024, 8), (2024, 11), (2025, 3), (2025, 6),
           (2025, 11), (2026, 2), (2026, 7)]:
    p(f'   {ym[0]}-{ym[1]:02d}: {k(*ym):.4f}')
p()

# ---------------------------------------------------------------- 1. CHEQUEOS DE DISEÑO
p('1. CHEQUEOS DE DISEÑO (para ver si la reja-canasto del informe anterior pasa las reglas)')
import math
canasto = {'chica': dict(d=(0.6, 0.8), area_reja=7.0, vol=1.0 * 1.0 * 1.5),
           'mediana': dict(d=(1.0, 1.5), area_reja=21.2, vol=1.8 * 1.8 * 2.5)}
for n, c in canasto.items():
    a_lo = math.pi * c['d'][1] ** 2 / 4  # caño más grande -> relación más chica
    a_hi = math.pi * c['d'][0] ** 2 / 4
    p(f'   {n}: área de reja {c["area_reja"]} m2 / área del caño {a_hi:.2f}-{a_lo:.2f} m2 = '
      f'{c["area_reja"]/a_lo:.0f} a {c["area_reja"]/a_hi:.0f} veces  '
      f'(Environment Agency 2009, guía clave 21: entre 3 y 30 veces) [cálculo propio]')
p('   OJO: la regla de 3-30 veces es para rejas de 150 mm entre barrotes. Un canasto que retiene botellas (≤50 mm, MSMA)')
p('   se tapa mucho antes: por eso tiene que llevar alivio que deje pasar TODO el caudal con la reja 100% tapada')
p('   (ARR 2019, tabla 6.6.6: abertura menor que el largo de la basura -> bloqueo de diseño 100% con mucha basura). [inferencia]')
p()
p('   Cuántas veces hay que vaciar, según la carga de basura gruesa:')
carga = 0.28  # m3/ha/año, Ecosol Net Tech (Urban Asset Solutions), "typical pollution loads ... for gross pollutants"
areas = (20, 200)  # ha de cuenca por boca chica/mediana [supuesto: no hay dato de cuencas]
util = {'chica': 0.5 * canasto['chica']['vol'], 'mediana': 0.5 * canasto['mediana']['vol']}  # se vacía al 50% [supuesto]
for n in canasto:
    v_lo, v_hi = carga * areas[0], carga * areas[1]
    p(f'   {n}: cuenca {areas[0]}-{areas[1]} ha [supuesto] x 0,28 m3/ha/año = {v_lo:.1f}-{v_hi:.1f} m3/año; '
      f'canasto útil {util[n]:.2f} m3 (vaciar al 50%) -> {v_lo/util[n]:.0f} a {v_hi/util[n]:.0f} vaciados por año')
p('   Kwinana (Australia): 3.660,5 kg en 2x32 + 3x19 = 121 vaciados -> '
  f'{3660.5/121:.0f} kg por vaciado; cada 2 semanas en invierno y 1 vez por mes el resto (≈ 18 por año). [verificado; cálculo propio]')
p()

# ---------------------------------------------------------------- 2. COSTOS UNITARIOS LOCALES
p('2. COSTOS UNITARIOS LOCALES')
cargas = 0.12 + 0.048 + 0.03275  # como el informe anterior (IPS, IOMA, ART)
pres = 50371
efectivo = 0.85  # [supuesto] 15% vacaciones, feriados y licencias
hora = {}
for c, b in {'cat6_48h': 652627, 'cat9_48h': 755468}.items():
    anual = (b * 13 * (1 + cargas) + pres * 12) * k(2026, 7)
    hora[c] = anual / (48 * 52 * efectivo)
    p(f'   Obrero municipal {c} (Dec. 782/2026, jul-2026): {M(anual)} por año dic-25; {P(hora[c])} $/hora efectiva')
cam = 33114 * k(2024, 8)
p(f'   Camión volcador 5 m3 con chofer (Dec. 1238/2024, $33.114/h desde 01/08/2024): {P(cam)} $/h dic-25')
emsade = 133100 * k(2024, 11)
p(f'   Servicio contratado de desobstrucción (LP 60/2024, EMSADE S.A., $133.100/h, oferta nov-2024): {P(emsade)} $/h dic-25 [techo de un servicio con equipo]')
p(f'   Tasa municipal a terceros (Ord. Impositiva 2026): camión $135.400/h + 2 peones x $12.070 = {P(135400 + 2 * 12070)} $/h')
p()
p('   Contratos con cooperativas de trabajo (para comparar, no es el mismo alcance):')
for n, v, ym in [('San Isidro CP 118/2024, Coop. de Trabajo Rocío, limpieza y desobstrucción de conductos pluviales', 27795000, (2024, 8)),
                 ('San Isidro CP 79/2025, Coop. de Trabajo Rocío, ídem', 32483700, (2025, 6)),
                 ('San Isidro CP 131/2025, Coop. de Trabajo Rocío, ídem', 32483700, (2026, 2)),
                 ('Bahía Blanca CP 5752/2025, Coop. de Trabajo Villa Rosas, desagües y espacios verdes de escuelas, nov-dic 2025', 20559000, (2025, 11)),
                 ('Bahía Blanca LPriv 3373/2021, Coop. de Trabajo Villa Rosas, ídem (plazo no leído)', 3680121.75, (2021, 9)),
                 ('Viedma 2020, canastos en la estación elevadora de Av. Ayacucho ("casi dos millones")', 2000000, (2020, 9))]:
    p(f'     {n}: ${P(v)} -> {M(v*k(*ym))} dic-25')
p(f'     Bahía Blanca 2025 por mes: {M(20559000*k(2025,11)/2)} dic-25 por mes (2 meses)')
p('     San Isidro: los tres concursos de Rocío no dicen el plazo; si cada uno cubre 8 a 10 meses (la distancia entre adjudicaciones) [supuesto],')
roc = 32483700 * k(2025, 6)
p(f'     serían {M(roc*12/10)} a {M(roc*12/8)} por año.')
p()

# ---------------------------------------------------------------- 3. INSTALACIÓN POR BOCA
p('3. INSTALACIÓN POR BOCA (precios del contrato municipal LP 62/2024, Dec. 1077/2025, redeterminados al 01/03/2025)')
c25 = k(2025, 3)
reja = (223955.41 * c25, 373588.27 * c25)      # perimetral Z1 / Techno Z2, m2
horm = (66600.22 * c25, 91432.08 * c25)         # vereda HºAº 13-15 cm Z1/Z2, m2 (proxy de losa o tabique delgado) [supuesto]
exc = (18645.01 * c25, 44364.39 * c25)          # excavación m3 Z1/Z2
jornal = 294705.37 * c25                       # jornal herrería Z1
p(f'   reja {P(reja[0])}-{P(reja[1])} $/m2; hormigón (vereda HºAº como proxy) {P(horm[0])}-{P(horm[1])} $/m2; '
  f'excavación {P(exc[0])}-{P(exc[1])} $/m3; jornal herrería {P(jornal)} $')
base = {'chica': dict(m2=7.0, losa=4.0, jorn=(2, 3)), 'mediana': dict(m2=21.2, losa=9.0, jorn=(3, 5))}
aliv = {'chica': dict(exc=(4, 6), horm=(4, 6), jorn=(1, 2)), 'mediana': dict(exc=(8, 12), horm=(8, 12), jorn=(2, 3))}  # [supuesto]
proy = (0.10, 0.20)  # proyecto hidráulico, relevamiento e inspección, % de la obra [supuesto]
inst = {}
for n in base:
    b, a = base[n], aliv[n]
    canasto_lo = b['m2'] * reja[0] + b['losa'] * horm[0] + b['jorn'][0] * jornal
    canasto_hi = b['m2'] * reja[1] + b['losa'] * horm[1] + b['jorn'][1] * jornal
    al_lo = a['exc'][0] * exc[0] + a['horm'][0] * horm[0] + a['jorn'][0] * jornal
    al_hi = a['exc'][1] * exc[1] + a['horm'][1] * horm[1] + a['jorn'][1] * jornal
    obra_lo, obra_hi = canasto_lo + al_lo, canasto_hi + al_hi
    tot_lo, tot_hi = obra_lo * (1 + proy[0]), obra_hi * (1 + proy[1])
    inst[n] = (tot_lo, tot_hi)
    p(f'   {n}: canasto {M(canasto_lo)}-{M(canasto_hi)} (como el informe anterior) + vertedero de alivio {M(al_lo)}-{M(al_hi)} [supuesto de cantidades]'
      f' + proyecto {int(proy[0]*100)}-{int(proy[1]*100)}% [supuesto] = {M(tot_lo)} a {M(tot_hi)}')
diez = (5 * inst['chica'][0] + 5 * inst['mediana'][0], 5 * inst['chica'][1] + 5 * inst['mediana'][1])
p(f'   DIEZ BOCAS con alivio (5 chicas + 5 medianas) [supuesto de mezcla]: {M(diez[0])} a {M(diez[1])} una vez (antes: 52,4 a 85,3 M sin alivio ni proyecto)')
p()
p('   Otras opciones por boca, para comparar:')
osse18 = 379300 / 140 * k(2018, 12)
eco = (487424 * k(2026, 7), 980089 * k(2026, 7))
p(f'   a) Barrera flotante de 15 m en el canal de salida: {M(15*osse18)} (lona, OSSE 2018) a {M(15*eco[1])} (EcoWay BRV1520, lista oct-2026); anclaje a pilotes sin precio')
# Marin 2022: red US$2.500/cfs + instalación 3x; HDS US$3.000/cfs + instalación 4x; CPS US$2.500 c/u
cfs = (10, 35)  # caudal de diseño 1 año-1 hora de una boca chica-mediana, en pies3/s (0,3-1,0 m3/s) [supuesto]
p(f'   b) Red grande al final del caño (Marin 2022: US$2.500 por pie3/s + instalación 3 veces): {cfs[0]}-{cfs[1]} pie3/s [supuesto] = '
  f'US${P(2500*4*cfs[0])}-{P(2500*4*cfs[1])} = {M(2500*4*cfs[0]*USD)} a {M(2500*4*cfs[1]*USD)}')
p(f'   c) Separador hidrodinámico tipo CDS (Marin: US$3.000 por pie3/s + instalación 4 veces): US${P(3000*5*cfs[0])}-{P(3000*5*cfs[1])} = '
  f'{M(3000*5*cfs[0]*USD)} a {M(3000*5*cfs[1]*USD)}')
p(f'      EPA 2021 (US$ de ene-2019): equipo US$6.000-450.000 + obra ≈ 2 veces el equipo -> US$18.000-1.350.000 = {M(18000*USD)} a {M(1350000*USD)}; vaciado ≈ US$4.000 = {M(4000*USD)} cada vez')
p('   d) Red con desenganche tipo Ecosol Net Tech (hasta caños de 900 mm): sin precio publicado. [no encontrado]')
p()

# ---------------------------------------------------------------- 4. CANASTOS EN SUMIDEROS (OPCIONAL)
p('4. CANASTOS EN SUMIDEROS AGUAS ARRIBA (opcional, sólo en puntos calientes)')
ins_local = (0.6 * reja[0] + 0.25 * jornal, 1.0 * reja[1] + 0.5 * jornal)  # 0,6-1,0 m2 de malla/reja + 1/4-1/2 jornal [supuesto]
p(f'   Local, a medida (0,6-1,0 m2 de reja + 1/4-1/2 jornal) [supuesto]: {M(ins_local[0])} a {M(ins_local[1])} cada uno')
p(f'   Marin 2022, connector pipe screen: US$2.500 = {M(2500*USD)}; EPA 2021: US$300-10.000 + US$1.800 de colocación = {M(2100*USD)} a {M(11800*USD)}')
n_ins = (100, 200)  # 10-20 sumideros calientes por boca [supuesto]
v_ins = 24          # 2 veces por mes, como la prioridad alta de la Ciudad (PET 2021) [verificado como pauta]
h_ins = (0.15, 0.25)  # horas por canasto y visita, dentro de la ruta de sumideros [supuesto]
op_ins = (n_ins[0] * v_ins * h_ins[0] * (2 * hora['cat6_48h'] + cam), n_ins[1] * v_ins * h_ins[1] * (2 * hora['cat9_48h'] + cam))
p(f'   {n_ins[0]}-{n_ins[1]} canastos [supuesto]: instalación {M(n_ins[0]*ins_local[0])} a {M(n_ins[1]*ins_local[1])}; '
  f'vaciado {v_ins} veces por año, {h_ins[0]}-{h_ins[1]} h con 2 obreros y camión = {M(op_ins[0])} a {M(op_ins[1])} por año')
piloto = 20  # canastos de prueba en 1-2 cuencas [supuesto]
p(f'   Piloto de {piloto} canastos [supuesto]: instalación {M(piloto*ins_local[0])} a {M(piloto*ins_local[1])}; '
  f'vaciado {M(piloto*v_ins*h_ins[0]*(2*hora["cat6_48h"]+cam))} a {M(piloto*v_ins*h_ins[1]*(2*hora["cat9_48h"]+cam))} por año')
p()

# ---------------------------------------------------------------- 5. OPERACIÓN DE LAS BOCAS
p('5. OPERACIÓN POR BOCA Y POR AÑO (vaciado + disposición + mantenimiento)')
ceamse = (20817.89, 98318.0)  # $/t: tarifa CEAMSE 2026-27 a costo real 2024 llevado a dic-25 (del informe anterior)
ton = (0.1, 2.0)   # t por boca y año [supuesto, con San Nicolás y Kwinana]
hv = (0.5, 1.0)    # horas por boca y visita [supuesto, como el informe anterior]
mant = {n: (0.10 * inst[n][0], 0.10 * inst[n][1]) for n in inst}  # 10% de la instalación por año [supuesto]
mant_prom = ((mant['chica'][0] + mant['mediana'][0]) / 2, (mant['chica'][1] + mant['mediana'][1]) / 2)
frec = [('cada 2 semanas (26/año)', 26), ('semanal (52/año)', 52), ('semanal + después de cada lluvia (104/año)', 104)]
res = {}
for n, v in frec:
    mun = (v * hv[0] * (2 * hora['cat6_48h'] + cam) + ton[0] * ceamse[0] + mant_prom[0],
           v * hv[1] * (2 * hora['cat9_48h'] + cam) + ton[1] * ceamse[1] + mant_prom[1])
    con = (v * hv[0] * emsade + ton[0] * ceamse[0] + mant_prom[0], v * hv[1] * emsade + ton[1] * ceamse[1] + mant_prom[1])
    res[n] = (mun, con)
    p(f'   {n}: cuadrilla municipal + camión alquilado {M(mun[0])} a {M(mun[1])}; servicio contratado a $/h de LP 60/2024 {M(con[0])} a {M(con[1])} (por boca)')
p(f'   (mantenimiento 10% de la instalación por año [supuesto]: {M(mant_prom[0])} a {M(mant_prom[1])} por boca, promedio chica/mediana)')
p()

# ---------------------------------------------------------------- 6. TOTALES
p('6. TOTALES PARA LAS DIEZ BOCAS')
p(f'   Instalación una vez (reja-canasto con alivio + proyecto): {M(diez[0])} a {M(diez[1])}')
for n, v in frec:
    mun, con = res[n]
    p(f'   Por año, {n}: municipal {M(10*mun[0])} a {M(10*mun[1])}; contratado {M(10*con[0])} a {M(10*con[1])}')
p(f'   Opcional, canastos en {n_ins[0]}-{n_ins[1]} sumideros: {M(n_ins[0]*ins_local[0])} a {M(n_ins[1]*ins_local[1])} una vez + {M(op_ins[0])} a {M(op_ins[1])} por año')
p()
p('   Comparación:')
p('   - Informe 11 (Marin): 395 M por año las diez. Informe anterior (Y4): 33 a 75 M por año + 52 a 85 M una vez, sin alivio.')
mid = res['semanal (52/año)'][0]
hi = res['semanal + después de cada lluvia (104/año)'][0]
p(f'   - Recomendado (semanal + lluvias, municipal): {M(10*hi[0])} a {M(10*hi[1])} por año; semanal: {M(10*mid[0])} a {M(10*mid[1])} por año.')
p(f'   - Separador hidrodinámico en las diez: {M(10*3000*5*cfs[0]*USD)} a {M(10*3000*5*cfs[1]*USD)} una vez (Marin), sin contar vaciado.')
p(f'   - Red grande tipo Marin en las diez: {M(10*2500*4*cfs[0]*USD)} a {M(10*2500*4*cfs[1]*USD)} una vez.')

open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'calculo_dolar_1447.txt'), 'w').write('\n'.join(out) + '\n')
