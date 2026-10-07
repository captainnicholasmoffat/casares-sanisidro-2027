# Cuentas del reporte u2 (vaciado de las barreras de Perú y Alto Perú).
# Uso: python3 -I calculo.py > calculo_salida.txt
# Todo en pesos de diciembre de 2025 (IPC del repo; precios posteriores a jul-2026 con jul-2026).
import csv, os, glob, math, datetime

T = os.path.dirname(os.path.abspath(__file__))
U = os.path.dirname(T)
C = os.path.join(U, 'copias')

# ---------------------------------------------------------------- IPC
IPC = {}
for r in csv.DictReader(open(os.path.join(C, 'ipc_indec_mensual.csv'))):
    IPC[(int(r['anio']), int(r['mes']))] = float(r['indice'])
BASE = IPC[(2025, 12)]
assert abs(BASE - 10121.3715) < 1e-3 and abs(IPC[(2026, 7)] - 12076.3937) < 1e-3
def k(y, m):
    if (y, m) > (2026, 7):
        y, m = 2026, 7
    return BASE / IPC[(y, m)]
def M(x):  # millones con una decimal
    return f'{x/1e6:,.1f} M'.replace(',', 'X').replace('.', ',').replace('X', '.')
def P(x):  # pesos enteros
    return f'{x:,.0f}'.replace(',', '.')
def p(*a):
    print(*a)

p('=' * 100)
p('CÁLCULOS u2 · Vaciado de las barreras de Perú y Alto Perú · pesos de dic-2025')
p('=' * 100)

# ---------------------------------------------------------------- 1. LLUVIA
p('\n1. LLUVIA (cuántas veces hay que ir)')
smn_mes = [6.9, 6.5, 6.0, 6.5, 5.2, 4.2, 4.9, 5.3, 5.6, 7.4, 6.8, 6.6]  # SMN, San Fernando Aero 1996-2020, días >=1 mm [verificado]
SMN_D1 = 71.9
p(f'   SMN San Fernando 1996-2020, días con lluvia >=1 mm: {SMN_D1} por año (suma de meses {sum(smn_mes):.1f}); por mes: {smn_mes}')

def gsod(fn):
    rows = list(csv.DictReader(open(fn)))
    d = {}
    for r in rows:
        v = float(r['PRCP'])
        d[datetime.date.fromisoformat(r['DATE'])] = None if v >= 99 else v * 25.4
    return d

anios = []
for fn in sorted(glob.glob(os.path.join(C, 'gsod', 'gsod_*.csv'))):
    est = 'San Fernando' if '87553' in fn else 'Aeroparque'
    y = int(fn[-8:-4])
    d = gsod(fn)
    ndias = (datetime.date(y, 12, 31) - datetime.date(y, 1, 1)).days + 1
    falt = ndias - sum(1 for v in d.values() if v is not None)
    if falt > 40:
        continue  # años incompletos fuera
    # días
    days = [datetime.date(y, 1, 1) + datetime.timedelta(i) for i in range(ndias)]
    mm = [(d.get(x) or 0.0) for x in days]
    d1 = sum(1 for v in mm if v >= 1)
    d10 = sum(1 for v in mm if v >= 10)
    # episodios: rachas de días >=1 mm; total del episodio
    eps = []
    i = 0
    while i < ndias:
        if mm[i] >= 1:
            j = i
            tot = 0
            while j < ndias and mm[j] >= 1:
                tot += mm[j]; j += 1
            eps.append((days[j - 1], tot))  # fin del episodio
            i = j
        else:
            i += 1
    e1 = len(eps)
    e10 = sum(1 for e in eps if e[1] >= 10)
    # simulación de visitas: un vaciado al día siguiente del fin de cada episodio >= umbral;
    # revisión fija semanal (miércoles) sólo en las semanas sin vaciado por lluvia.
    def visitas(umbral):
        rain_v = set(e[0] + datetime.timedelta(1) for e in eps if e[1] >= umbral)
        semanas_con = set(x.isocalendar()[:2] for x in rain_v)
        semanales = set(x.isocalendar()[:2] for x in days if x.weekday() == 2)
        return len(rain_v) + len(semanales - semanas_con)
    anios.append(dict(est=est, y=y, falt=falt, d1=d1, d10=d10, e1=e1, e10=e10,
                      v1=visitas(1), v10=visitas(10), vsem=len(set(x.isocalendar()[:2] for x in days if x.weekday() == 2))))

p('   NOAA GSOD (datos SYNOP del SMN), años con <=40 días faltantes:')
for a in anios:
    p(f"     {a['est']:12s} {a['y']}: faltan {a['falt']:3d} d | días>=1mm {a['d1']:3d} | días>=10mm {a['d10']:3d} | episodios>=1mm {a['e1']:3d} | episodios con >=10mm {a['e10']:3d} | visitas sim. (semanal + c/lluvia>=1mm) {a['v1']:3d} | (semanal + c/lluvia>=10mm) {a['v10']:3d}")
sd1 = sum(a['d1'] for a in anios)
r_d10 = sum(a['d10'] for a in anios) / sd1
r_e1 = sum(a['e1'] for a in anios) / sd1
r_e10 = sum(a['e10'] for a in anios) / sd1
p(f'   Proporciones NOAA [cálculo propio]: días>=10mm / días>=1mm = {r_d10:.2f}; episodios>=1mm / días>=1mm = {r_e1:.2f}; episodios con >=10mm / días>=1mm = {r_e10:.2f}')
D10 = SMN_D1 * r_d10
E1 = SMN_D1 * r_e1
E10 = SMN_D1 * r_e10
p(f'   Llevadas a la normal del SMN (71,9 días): días>=10mm ~{D10:.0f}; episodios de lluvia >=1mm ~{E1:.0f}; episodios con >=10mm ~{E10:.0f} por año [cálculo propio]')
def vis(E):  # visitas = episodios + semanas sin episodio (Poisson)
    return E + 52 * math.exp(-E / 52)
SUD = 3  # sudestadas fuertes por año (informe 11: 2 o 3, Moreira y Simionato 2019) [verificado en el informe 11]
esc = {
    'S1 · semanal sólo (52) + sudestadas': 52 + SUD,
    'S2 · semanal + cada lluvia >=10 mm + sudestadas (RECOMENDADO)': vis(E10) + SUD,
    'S3 · semanal + cada lluvia >=1 mm + sudestadas': vis(E1) + SUD,
    'S2b · dos revisiones semanales + cada lluvia >=10 mm + sudestadas (si la boca carga mucho)': E10 + 104 * math.exp(-E10 / 104) + SUD,
    'S4 · todos los días hábiles, como ACUMAR (250) + sudestadas': 250 + SUD,
}
sim1 = sum(a['v1'] for a in anios) / len(anios)
sim10 = sum(a['v10'] for a in anios) / len(anios)
p(f'   Control con la simulación NOAA (sin sudestadas): semanal+>=1mm {sim1:.0f}; semanal+>=10mm {sim10:.0f} visitas por año (NOAA registra menos días de lluvia que el SMN)')
p('   Visitas con máquina por año, por escenario [cálculo propio]:')
for kx, v in esc.items():
    p(f'     {kx}: {v:.0f}')

# ---------------------------------------------------------------- 2. TARIFAS
p('\n2. PRECIO POR HORA (IVA incluido) llevado a dic-2025')
tar = {}
def T_(clave, nominal, y, m, fuente):
    v = nominal * k(y, m)
    tar[clave] = v
    p(f'   {clave:55s} ${P(nominal):>8s} ({m:02d}/{y}) x {k(y,m):.4f} = ${P(v):>8s}/h  | {fuente}')
T_('Rocío · camión volcador 5 m3 con grúa/brazo almeja', 52359, 2025, 5, 'LP 14/2020 renglón 4, Dec. 649/2025 [verificado]')
T_('Rocío · retroexcavadora oruga 130 HP balde 1 m3', 40396, 2025, 5, 'LP 14/2020 renglón 10, Dec. 649/2025 [verificado]')
T_('Rocío · retropala neumáticos 130 HP', 33288, 2025, 5, 'LP 14/2020 renglón 8, Dec. 649/2025 [verificado]')
T_('Rocío · camión batea >17 m3', 42824, 2025, 5, 'LP 14/2020 renglón 18, Dec. 649/2025 [verificado]')
T_('Rocío · camión volcador >=17 m3 (LP 37/2021)', 48851, 2025, 12, 'LP 37/2021 renglón 4, Dec. 150/2026 [verificado]')
T_('Volmat · camión volcador 5 m3', 40004, 2025, 7, 'LP 14/2020 renglón 1, Dec. 1184/2025 [verificado]')
T_('Proveedor persona humana LP 14/2020 · minicargadora', 39567, 2025, 5, 'LP 14/2020 renglón 12, Dec. 661/2025 [verificado]')
T_('Total Señalamiento · camión con hidrogrúa 4 t, 7,4 m', 68556, 2025, 1, 'LP 53/2022 renglón 5, Dec. 523/2025 [verificado]')
T_('Total Señalamiento · retroexcavadora oruga 130 HP', 96839, 2025, 1, 'LP 53/2022 renglón 10, Dec. 523/2025 [verificado]')
T_('Total Señalamiento · retropala 130 HP', 69479, 2025, 1, 'LP 53/2022 renglón 2, Dec. 523/2025 [verificado]')
T_('Total Señalamiento · camión batea 20 m3', 66097, 2025, 1, 'LP 53/2022 renglón 8, Dec. 523/2025 [verificado]')
T_('Proveedor persona humana LP 53/2022 · minirretro oruga 40 HP', 92235, 2025, 12, 'LP 53/2022 renglón 7, Dec. 377/2026 [verificado]')
T_('Proveedor persona humana LP 53/2022 · camión volcador 6 m3', 83506, 2025, 12, 'LP 53/2022 renglón 4, Dec. 377/2026 [verificado]')
bb1 = 28479000 / 176
bb2 = 24728000 / 176
T_('Bahía Blanca · excavadora CAT 320D2L c/chofer (jun-26)', bb1, 2026, 6, 'Dec. 1053/2026: $28.479.000 por 8 h x 22 días = 176 h [verificado]')
T_('Bahía Blanca · ídem (sep-26)', bb2, 2026, 9, 'Dec. 1863/2026: $24.728.000; 176 h [inferencia: mismas horas que el anterior]')
T_('Techo · Impositiva 2026 hora de maquinaria pesada', 124300, 2026, 1, 'Ord. 9415 art. 3 b) [verificado]; mes ene-2026 [supuesto]')
T_('Techo · Impositiva 2026 hora de camión', 135400, 2026, 1, 'Ord. 9415 art. 3 b) [verificado]')
T_('Techo · Impositiva 2026 hora de peón', 12070, 2026, 1, 'Ord. 9415 art. 3 b) [verificado]')
T_('LP 60/2024 desobstrucción (camión hidrocinético) EMSADE', 133100, 2024, 11, 'Dec. 124/2025 [verificado en Z1]')

# mano de obra municipal (Decreto 782/2026, desde jul-2026)
def obrero(mensual):
    anual = 13 * mensual * 1.20075 + 12 * 50371
    horas = 48 * 52 * 0.85
    return anual * k(2026, 7) / horas, anual * k(2026, 7)
ob6_h, ob6_a = obrero(652627)
ob9_h, ob9_a = obrero(755468)
p(f'   Obrero municipal cat. 6: ${P(ob6_h)}/h ({M(ob6_a)} por año); cat. 9: ${P(ob9_h)}/h ({M(ob9_a)} por año) [cálculo propio; Dec. 782/2026; 13 sueldos, 20,075% de cargas, presentismo, 85% de horas efectivas]')
PEON = (ob6_h, ob9_h)

# CEAMSE
ceamse = 20817.89 * k(2026, 7)
p(f'   CEAMSE Norte III 2026-2027: $20.817,89/t -> ${P(ceamse)}/t dic-25 [verificado para Colón; probable para San Isidro; mes jul-2026 supuesto]')

# ---------------------------------------------------------------- 3. TONELADAS
p('\n3. TONELADAS POR BOCA Y POR AÑO')
p('   Precedentes: ACUMAR 2022 puntos fijos 126,5 / 316,2 / 219,5 t [sin confirmar, prensa que cita a ACUMAR]; Porto Alegre (Dilúvio) 65 a 217 t por año 2016-2025 [verificado, informe previo]; ACUMAR 7.635,61 t jul-21 a may-22 en todo el contrato (puntos fijos + equipos móviles) [verificado, AGN]')
TON = {'Perú': (30, 150), 'Alto Perú': (20, 100)}  # [inferencia]
tlo = sum(v[0] for v in TON.values()); thi = sum(v[1] for v in TON.values())
p(f'   Supuesto [inferencia]: Perú {TON["Perú"][0]}-{TON["Perú"][1]} t; Alto Perú {TON["Alto Perú"][0]}-{TON["Alto Perú"][1]} t; las dos {tlo}-{thi} t por año')
p(f'   Disposición en CEAMSE: {M(tlo*ceamse)} a {M(thi*ceamse)} por año [cálculo propio]')
for kx, v in esc.items():
    p(f'     {kx}: {tlo/v:.1f} a {thi/v:.1f} t por visita (las dos bocas)')

# ---------------------------------------------------------------- 4. HORAS
p('\n4. HORAS POR VISITA (las dos bocas en una sola salida) [supuesto]')
H_VIS = (4, 6)    # horas de máquina por visita normal: mínimo 4 h por salida; 6 h con una descarga extra en CEAMSE
H_SUD = 8         # horas por equipo en un operativo de sudestada
PEONES = 2
p(f'   Visita normal: camión con almeja {H_VIS[0]}-{H_VIS[1]} h (incluye 2 bocas, traslado de 2-3 km y viaje a CEAMSE Norte III) + {PEONES} operarios municipales el mismo tiempo')
p(f'   Sudestada (x{SUD}): + retroexcavadora oruga {H_SUD} h + camión batea {H_SUD} h + almeja {H_SUD} h + {PEONES} operarios {H_SUD} h; incluye retirar y recolocar la barrera')

def horas(vis):
    hn = (vis - SUD) if vis < 250 else vis
    return hn

# ---------------------------------------------------------------- 5. COSTO POR AÑO POR OPCIÓN
p('\n5. COSTO POR AÑO DE VACIAR LAS DOS BARRERAS, por opción y escenario [cálculo propio]')

def costo_alquiler(vis, almeja, retro, batea, peon_h, sud=True):
    lo_hi = []
    for i in (0, 1):
        n = vis - (SUD if sud else 0)
        h = H_VIS[i]
        maq = n * h * almeja
        pe = n * h * PEONES * peon_h[i]
        s = 0
        if sud:
            s = SUD * H_SUD * (almeja + retro + batea + PEONES * peon_h[i])
        t = (tlo, thi)[i] * ceamse
        lo_hi.append(maq + pe + s + t)
    return lo_hi

res = {}
p('\n   Opción A · alquiler de máquina con operador + cuadrilla municipal en tierra')
for nombre, alm, ret, bat in [
        ('A1 contrato vigente LP 14/2020 (Cooperativa Rocío)', tar['Rocío · camión volcador 5 m3 con grúa/brazo almeja'], tar['Rocío · retroexcavadora oruga 130 HP balde 1 m3'], tar['Rocío · camión batea >17 m3']),
        ('A2 contrato LP 53/2022 (Total Señalamiento)', tar['Total Señalamiento · camión con hidrogrúa 4 t, 7,4 m'], tar['Total Señalamiento · retroexcavadora oruga 130 HP'], tar['Total Señalamiento · camión batea 20 m3']),
        ('A3 precio de mercado 2026 (hidrogrúa TS + excavadora Bahía Blanca)', tar['Total Señalamiento · camión con hidrogrúa 4 t, 7,4 m'], tar['Bahía Blanca · excavadora CAT 320D2L c/chofer (jun-26)'], tar['Total Señalamiento · camión batea 20 m3'])]:
    p(f'   {nombre}:')
    for kx, v in esc.items():
        lo, hi = costo_alquiler(v, alm, ret, bat, PEON)
        res[(nombre[:2], kx.split(' ')[0])] = (lo, hi)
        p(f'      {kx}: {M(lo)} a {M(hi)}')

p('\n   Opción B · cuadrilla municipal con camión propio (volcador 8 m3 con almeja)')
compra = 178000000 * k(2025, 1)
p(f'   Precio de compra: Mar Chiquita LP 14/24, Iveco 150E21 + caja 8 m3 + almeja ASTARSA, $178.000.000 (ene-2025) -> {M(compra)} dic-25 [verificado el precio; que sirva para San Isidro: inferencia]')
p(f'   Referencia San Isidro: dos camiones livianos con grúa percha (acarreo de autos) $234.777.000 (oct-2024) -> {M(234777000*k(2024,10))} los dos [verificado]')
VIDA = 10
def anualidad(v, r):
    return v / VIDA if r == 0 else v * r / (1 - (1 + r) ** -VIDA)
FIJO = (0.04, 0.06)     # seguro, patente, VTV, mantenimiento preventivo, % del valor por año [supuesto]
GASOIL_L_H = (8, 12)    # litros por hora [supuesto]
GASOIL_P = (1500, 1800) # $ por litro dic-2025 [supuesto: precio no verificado en fuente oficial]
REP = 0.25              # reparaciones y neumáticos, % del gasto de gasoil [supuesto]
for parte, lbl in [(1.0, 'B1 camión dedicado sólo a las barreras'), (0.5, 'B2 camión compartido con redes chicas y cuadrilla (50% del capital a las barreras)')]:
    p(f'   {lbl}:')
    for kx, v in esc.items():
        out = []
        for i in (0, 1):
            r = (0.0, 0.06)[i]
            cap = parte * (anualidad(compra, r) + FIJO[i] * compra)
            n = v - SUD
            h = n * H_VIS[i] + SUD * H_SUD
            var = h * GASOIL_L_H[i] * GASOIL_P[i] * (1 + REP)
            chofer = h * ob9_h
            pe = h * PEONES * PEON[i]
            sud = SUD * H_SUD * (tar['Rocío · retroexcavadora oruga 130 HP balde 1 m3'] + tar['Rocío · camión batea >17 m3'])
            t = (tlo, thi)[i] * ceamse
            out.append(cap + var + chofer + pe + sud + t)
        res[(lbl[:2], kx.split(' ')[0])] = tuple(out)
        p(f'      {kx}: {M(out[0])} a {M(out[1])}  (horas de camión por año: {(v-SUD)*H_VIS[0]+SUD*H_SUD:.0f} a {(v-SUD)*H_VIS[1]+SUD*H_SUD:.0f})')
p(f'   Capital por año: anualidad 10 años al 0% {M(anualidad(compra,0))}, al 6% real {M(anualidad(compra,0.06))}; fijos {M(FIJO[0]*compra)} a {M(FIJO[1]*compra)}')

p('\n   Opción C · contrato de servicio por resultado con cooperativa o empresa del partido (concurso)')
GG = (0.20, 0.30)  # gastos generales, seguros, supervisión y beneficio sobre el costo directo [supuesto]
DISP = 0.10        # cargo por guardia y respuesta en 24 h, incluso fines de semana [supuesto]
for kx, v in esc.items():
    lo, hi = res[('A1', kx.split(' ')[0])]
    out = (lo * (1 + GG[0] + DISP), hi * (1 + GG[1] + DISP))
    res[('C1', kx.split(' ')[0])] = out
    p(f'      C1 sobre precios Rocío · {kx}: {M(out[0])} a {M(out[1])}')
for kx, v in esc.items():
    lo, hi = res[('A2', kx.split(' ')[0])]
    out = (lo * (1 + GG[0] + DISP), hi * (1 + GG[1] + DISP))
    res[('C2', kx.split(' ')[0])] = out
    p(f'      C2 sobre precios LP 53/2022 · {kx}: {M(out[0])} a {M(out[1])}')
# techo: tarifas de la Ordenanza Impositiva
p('   Techo con la Ordenanza Impositiva 2026 (lo que el Municipio cobra a terceros):')
for kx, v in esc.items():
    out = []
    for i in (0, 1):
        n = v - SUD
        h = n * H_VIS[i]
        c = h * (tar['Techo · Impositiva 2026 hora de camión'] + PEONES * tar['Techo · Impositiva 2026 hora de peón'])
        if True:
            c += SUD * H_SUD * (tar['Techo · Impositiva 2026 hora de maquinaria pesada'] + 2 * tar['Techo · Impositiva 2026 hora de camión'] + PEONES * tar['Techo · Impositiva 2026 hora de peón'])
        c += (tlo, thi)[i] * ceamse
        out.append(c)
    p(f'      {kx}: {M(out[0])} a {M(out[1])}')

# ---------------------------------------------------------------- 6. PRECEDENTES DE SERVICIO INTEGRAL
p('\n6. PRECEDENTES DE SERVICIO INTEGRAL (guardia o presencia diaria), llevados a dic-2025')
q1 = sum(IPC[(2015, m)] for m in (1, 2, 3)) / 3
q3 = sum(IPC[(2015, m)] for m in (7, 8, 9)) / 3
peru_q1 = 524062.50 * 4 * BASE / q1
peru_q3 = 524062.50 * 4 * BASE / q3
p(f'   San Isidro, desagüe de Perú: $524.062,50 por trimestre (ene-mar 2015, Coop. Córdoba) = {M(peru_q1)} por año; (jul-sep 2015, Líneas Marítimas Riccitelli) = {M(peru_q3)} por año [cálculo propio; informe 11 decía ~323 M y el 23 bis ~326 M]')
p(f'   San Isidro, ídem 2017: $998.426,80 desde 01/05/2017 "por la vigencia del pliego" (plazo no leído) = {M(998426.80*BASE/IPC[(2017,5)])} en total [no se puede anualizar]')
acu = 428458711.68 / 4
p(f'   ACUMAR arroyos 2021 (EMISER): $428.458.711,68 por 48 meses = {M(acu*k(2021,6))} por año (jun-2021) o {M(acu*k(2021,7))} (jul-2021); 3 puntos fijos + 2 equipos móviles [cálculo propio; informe 11 decía 2.124 M]')
osse = 348904 * k(2020, 4)
p(f'   OSSE 2020: mantenimiento a demanda o emergencia de la barrera (Hydroservices) $348.904 = {M(osse)} por 4+4 unidades [verificado]')

# ---------------------------------------------------------------- 7. RESUMEN
p('\n7. RESUMEN · ESCENARIO RECOMENDADO S2 (semanal + cada lluvia >=10 mm + sudestadas)')
for key, lbl in [('A1', 'A1 alquiler con operador, contrato vigente (Rocío)'), ('A2', 'A2 alquiler con operador LP 53/2022'), ('A3', 'A3 alquiler a precio de mercado 2026'),
                 ('B1', 'B1 camión propio dedicado'), ('B2', 'B2 camión propio compartido'), ('C1', 'C1 servicio por resultado (base Rocío)'), ('C2', 'C2 servicio por resultado (base LP 53/2022)')]:
    lo, hi = res[(key, 'S2')]
    p(f'   {lbl:55s} {M(lo):>9s} a {M(hi):>9s} por año | por boca {M(lo/2)} a {M(hi/2)}')
v2 = esc['S2 · semanal + cada lluvia >=10 mm + sudestadas (RECOMENDADO)']
p(f'   Visitas por año en S2: {v2:.0f}; horas de camión con almeja {(v2-SUD)*H_VIS[0]+SUD*H_SUD:.0f} a {(v2-SUD)*H_VIS[1]+SUD*H_SUD:.0f}')
p(f'   Para comparar: servicio de Perú de 2015 x 2 bocas = {M(2*peru_q3)} a {M(2*peru_q1)} por año')
# punto de equilibrio compra vs alquiler
cap_anual = anualidad(compra, 0.06) + 0.05 * compra
dif_h = tar['Rocío · camión volcador 5 m3 con grúa/brazo almeja'] - (10 * 1650 * 1.25 + ob9_h)
p(f'   Equilibrio compra vs. alquiler Rocío: capital+fijos {M(cap_anual)} por año / (alquiler {P(tar["Rocío · camión volcador 5 m3 con grúa/brazo almeja"])} - variable propio {P(10*1650*1.25+ob9_h)}) = {P(cap_anual/dif_h)} horas por año')
dif_h2 = tar['Total Señalamiento · camión con hidrogrúa 4 t, 7,4 m'] - (10 * 1650 * 1.25 + ob9_h)
p(f'   Ídem contra la hidrogrúa de la LP 53/2022: {P(cap_anual/dif_h2)} horas por año (un turno completo son ~2.000 h)')
# desglose A1 S2
v = v2; n = v - SUD
alm = tar['Rocío · camión volcador 5 m3 con grúa/brazo almeja']; ret = tar['Rocío · retroexcavadora oruga 130 HP balde 1 m3']; bat = tar['Rocío · camión batea >17 m3']
for i in (0, 1):
    maq = n * H_VIS[i] * alm; pe = n * H_VIS[i] * PEONES * PEON[i]; sd = SUD * H_SUD * (alm + ret + bat + PEONES * PEON[i]); t = (tlo, thi)[i] * ceamse
    p(f'   Desglose A1·S2 ({"bajo" if i==0 else "alto"}): camión con almeja {M(maq)} | 2 operarios municipales {M(pe)} | 3 operativos de sudestada {M(sd)} | CEAMSE {M(t)} | total {M(maq+pe+sd+t)}')
p(f'   Por vaciado normal (las dos bocas): {M(H_VIS[0]*(alm+PEONES*PEON[0]))} a {M(H_VIS[1]*(alm+PEONES*PEON[1]))}; por operativo de sudestada: {M(H_SUD*(alm+ret+bat+PEONES*PEON[1]))}')
# sensibilidad: todo el trabajo con retroexcavadora de mercado
p(f'   Sensibilidad: si todo el trabajo se hiciera con la retroexcavadora de mercado (Bahía Blanca, {P(tar["Bahía Blanca · excavadora CAT 320D2L c/chofer (jun-26)"])}/h) en vez del camión con almeja, S2 costaría {M(n*H_VIS[0]*(tar["Bahía Blanca · excavadora CAT 320D2L c/chofer (jun-26)"]+tar["Rocío · camión batea >17 m3"]))} a {M(n*H_VIS[1]*(tar["Bahía Blanca · excavadora CAT 320D2L c/chofer (jun-26)"]+tar["Rocío · camión batea >17 m3"]))} sólo en máquinas (retro + camión aparte)')
