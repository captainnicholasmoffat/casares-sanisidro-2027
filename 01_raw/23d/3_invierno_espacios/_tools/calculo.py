# Programa San Isidro 2027 - consulta c23d / v3 (shows en invierno y espacios cerrados) - 07/10/2026
# Uso: python3 -I calculo.py > calculo_salida.txt
# Plata en pesos de dic-2025 con el IPC del repo (ch/wt/data/ipc_indec_mensual.csv, sólo lectura). Precios posteriores a jul-2026 -> índice jul-2026.
import csv, os, collections
V = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v3_invierno_espacios'
IPCF = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/data/ipc_indec_mensual.csv'
IPC = {(int(r['anio']), int(r['mes'])): float(r['indice']) for r in csv.DictReader(open(IPCF))}
BASE = IPC[(2025, 12)]
def k(y, m):
    if (y, m) > (2026, 7): y, m = 2026, 7
    return BASE / IPC[(y, m)]
def d25(x, y, m): return x * k(y, m)
def P(x): return f'{x:,.0f}'.replace(',', '.')
def M(x): return f'{x/1e6:,.1f} M'.replace(',', 'X').replace('.', ',').replace('X', '.')
def p(*a): print(*a)
MES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
DM = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
assert abs(BASE - 10121.3715) < 1e-3 and abs(IPC[(2026, 7)] - 12076.3937) < 1e-3
p('Coeficientes IPC (dic-2025 / mes): ' + '; '.join(f'{y}-{m:02d} {k(y,m):.4f}' for y, m in [(2024,9),(2025,4),(2025,6),(2025,7),(2025,9),(2026,2),(2026,3),(2026,7)]))
p()
# ===================================================================== 1. CLIMA
p('1. CLIMA DE TARDE-NOCHE POR MES (San Fernando Aero, la estación del SMN más cercana a San Isidro)')
smn = {}
for r in csv.reader(open(f'{V}/smn/smn_normales_1991-2020_promedios_SF_AEP_OBS.csv'), delimiter=';'):
    if r[0] == 'SAN FERNANDO AERO': smn[r[2].strip()] = r[3:15]
def fila(pref):
    for kk, v in smn.items():
        if kk.startswith(pref): return [float(x.replace('< 0.1', '0.05')) for x in v]
    raise KeyError(pref)
T, TX, TN = fila('Temperatura ( °C)'), fila('Temperatura máxima'), fila('Temperatura mínima')
LL1, TOR, VEL, VF, HEL, HR = fila('Frecuencia de días con Precipitación  ≥ 1.0'), fila('Frecuencia de días con Tormenta'), fila('Velocidad del Viento'), fila('Frecuencia de días con Viento fuerte'), fila('Frecuencia de días con Helada'), fila('Humedad relativa')
isd = {}
for r in csv.reader(open(f'{V}/_tools/isd_horario_salida.txt'), delimiter=';'):
    if r[0] in MES: isd[r[0]] = r
T21 = [float(isd[m][4]) for m in MES]; T18 = [float(isd[m][2]) for m in MES]; T22 = [float(isd[m][5]) for m in MES]
V21 = [float(isd[m][6]) for m in MES]; P12 = [float(isd[m][9]) for m in MES]; P10 = [float(isd[m][8]) for m in MES]
shn = collections.defaultdict(dict)
for r in csv.DictReader(open(f'{V}/shn/SHN_sol_BUENOS_AIRES_2026_todo.csv'), delimiter=';'):
    shn[r['mes']][int(r['dia'])] = (r['puesta'], r['crep_vespertino'])
p('   Fuentes: SMN normales 1991-2020 (San Fernando, período 1996-2020; viento 2011-2020) [verificado]; NOAA ISD 2016-2025 horario [verificado el dato, promedio = cálculo propio];')
p('            SHN puesta del Sol y fin del crepúsculo civil, Buenos Aires 2026, día 15 de cada mes [verificado]')
p('   mes | T media | T máx | T mín | T 18 h | T 21 h | T 22 h | días T21<12 °C | días T21<10 °C | lluvia>=1mm (días) | tormenta (días) | viento medio km/h | viento 21 h | días viento fuerte | heladas | puesta / fin crepúsculo (día 15)')
for i, m in enumerate(MES):
    pu, cv = shn[m][15]
    p(f'   {m} | {T[i]:4.1f} | {TX[i]:4.1f} | {TN[i]:4.1f} | {T18[i]:4.1f} | {T21[i]:4.1f} | {T22[i]:4.1f} | {P12[i]:3.0f}% | {P10[i]:3.0f}% | {LL1[i]:3.1f} | {TOR[i]:3.1f} | {VEL[i]:4.1f} | {V21[i]:4.1f} | {VF[i]:3.1f} | {HEL[i]:3.1f} | {pu} / {cv}')
p()
CRIT = {
 'A estricto [supuesto]: mínima media SMN < 10 °C': [TN[i] < 10 for i in range(12)],
 'B central  [supuesto]: temperatura media a las 21 h < 14 °C': [T21[i] < 14 for i in range(12)],
 'C laxo     [supuesto]: temperatura media a las 21 h < 12 °C': [T21[i] < 12 for i in range(12)],
 'D por frecuencia [supuesto]: 1 de cada 4 noches o más con < 12 °C a las 21 h': [P12[i] >= 25 for i in range(12)],
}
p('   CRITERIOS para mandar bajo techo un show de 18 a 22 h (ninguno es norma; son supuestos marcados):')
SHOWS = 200
res = {}
for c, sel in CRIT.items():
    ms = [MES[i] for i in range(12) if sel[i]]
    n_mes = len(ms); dias = sum(DM[i] for i in range(12) if sel[i])
    s_mes = SHOWS * n_mes / 12; s_dia = SHOWS * dias / 365.25
    res[c] = (ms, s_mes, s_dia)
    p(f'   - {c}: {", ".join(ms)} -> {n_mes} meses; shows bajo techo si se reparten parejo por mes {s_mes:.1f} (por días {s_dia:.1f})')
p('   Oscuridad: en los meses B la puesta del Sol (SHN, día 15) es entre 17:49 y 18:22 y el crepúsculo civil termina antes de las 18:48: todo el show de 18 a 22 h es de noche.')
p()
N_INV = round(SHOWS * 4 / 12)   # criterio B: may-ago
p(f'   ESCENARIO CENTRAL (criterio B, mayo a agosto): {N_INV} shows bajo techo por año; 133 al aire libre de septiembre a abril.')
p()
# ===================================================================== 2. COSTOS DE REFERENCIA
p('2. REFERENCIAS DE COSTO (nominal -> pesos de dic-2025)')
refs = [
 ('Bahía Blanca, Dec. 381/2024: locación SUM «Vicente Carreño» del Club Tiro Federal, vie-sáb-dom y feriados + oficina, por mes (mar-ago 2024)', 350000, 2024, 3),
 ('Bahía Blanca, Dec. 381/2024: idem, por mes (sep-2024 a feb-2025)', 437500, 2024, 9),
 ('Bahía Blanca, Dec. 523/2022: idem, por mes (mar-2021 a feb-2024)', 62000, 2021, 3),
 ('Patagones, Dec. 555/2026: club Rampla Juniors, uso para actividades culturales, deportivas y recreativas, por mes (mar-dic 2026)', 450000, 2026, 3),
 ('Patagones, Dec. 612/2025: club La Loma, idem, por mes (mar-dic 2025)', 240000, 2025, 4),
 ('Patagones, Dec. 507/2026: Club Social y Deportivo Patagones, escuelas + actividades municipales, por mes (mar-dic 2026)', 937500, 2026, 3),
 ('Patagones, Dec. 2186/2024: club Independiente de Villalonga, lunes a viernes, por mes (jun-dic 2024)', 180000, 2024, 6),
 ('Colegio de Abogados de San Isidro: Salón de Actos, sábado, 14 jus x $53.232 (jus 1/8/2026), incluye mantenimiento, limpieza y seguridad', 14 * 53232, 2026, 8),
 ('San Isidro, Dec. 1480/2025: subsidio CASVA (una cuota)', 5000000, 2025, 12),
 ('San Isidro, Dec. 841/2025: subsidio Club Vélez Sarsfield de Martínez (4 cuotas)', 4000000, 2025, 7),
 ('San Isidro, Dec. 1053/2025: subsidio Club Juventud Unida Los Únicos de Boulogne (2 cuotas)', 18000000, 2025, 9),
 ('San Isidro, Dec. 666/2025: subsidio Sociedad Italiana Dante Alighieri de San Isidro', 1600000, 2025, 6),
 ('San Isidro, Dec. 1479/2025: subsidio Asociación Cooperadora Casa de Cultura', 20000000, 2025, 12),
]
R = {}
for n, x, y, m in refs:
    R[n] = d25(x, y, m)
    p(f'   {n}: nominal {P(x)} -> {P(R[n])} [verificado el monto; deflactado = cálculo propio]')
p()
# ===================================================================== 3. COSTO POR SHOW EN ESPACIO MUNICIPAL PROPIO
p('3. COSTO MARGINAL DE ABRIR UN ESPACIO MUNICIPAL DE NOCHE (Teatro del Viejo Concejo, Casas de Cultura)')
HORA_C7, HORA_C9 = 5919, 6548          # Dec. 189/2026 Anexo I, valor hora «tareas especiales en eventos», cat. 7 y 9 (valores de feb-2026) [verificado]
CARGAS = 0.12 + 0.048 + 0.03275        # contribuciones patronales como en c23b z4a / Y4 [supuesto heredado]
H = 6                                   # 17 a 23 h: apertura, show 18-22 y cierre [supuesto]
staff = (1 * HORA_C9 + 2 * HORA_C7) * H * (1 + CARGAS)
staff25 = d25(staff, 2026, 2)
ENERGIA = 20000                         # luz y calefacción por noche, pesos de dic-2025 [supuesto, sin fuente]
c_muni = staff25 + ENERGIA
p(f'   1 encargado (cat. 9) + 2 agentes de maestranza o control (cat. 7) x {H} h, con cargas {CARGAS:.3f}: {P(staff)} nominal feb-2026 -> {P(staff25)}')
p(f'   + energía y calefacción {P(ENERGIA)} [supuesto] = {P(c_muni)} por show [cálculo propio]')
p('   El técnico de sonido y el asistente ya están en el costo de equipos del c23c W3a (3 equipos); no se suman acá.')
p()
# ===================================================================== 4. AHORRO POR NO CANCELAR
p('4. CANCELACIONES QUE SE EVITAN AL PASAR EL INVIERNO BAJO TECHO')
ALERTA = {'May': 1.8, 'Jun': 1.3, 'Jul': 1.2, 'Ago': 2.5, 'Sep': 2.1}   # días con alerta por mes, escenario central del c23c W3a [inferencia heredada]
HORARIO = 0.6                                                         # sólo cancela la alerta que cubre el horario (supuesto del W3a)
CACHET = 980112                                                       # cachet promedio por show, pesos dic-2025 (c23b Z4a / c23c W3a)
ah = 0
for m in ['May', 'Jun', 'Jul', 'Ago']:
    f = ALERTA[m] / DM[MES.index(m)] * HORARIO
    s = SHOWS / 12
    canc = s * (f + f * f)          # regla del cliente: hasta 2 cancelaciones pagas (70% cada una); la tercera fecha va bajo techo
    ah += canc * 0.70 * CACHET
    p(f'   {m}: probabilidad de alerta en el horario {100*f:.1f}% -> {canc:.2f} cancelaciones pagas evitadas')
p(f'   Ahorro por año (70% del cachet por cancelación): {M(ah)} [cálculo propio]')
p('   Supuesto: un show bajo techo no se cancela por alerta amarilla (decisión del cliente; pregunta abierta).')
p()
# ===================================================================== 5. ESCENARIOS DE COSTO POR AÑO
p(f'5. COSTO POR AÑO DE PONER BAJO TECHO LOS {N_INV} SHOWS DE MAYO A AGOSTO (pesos de dic-2025)')
mez = {'solista': 0.40, 'dúo o trío': 0.30, 'banda': 0.30}   # mezcla de formatos del c23b Z4a [supuesto heredado]
n_sol = N_INV * mez['solista']; n_resto = N_INV - n_sol
BB = R['Bahía Blanca, Dec. 381/2024: idem, por mes (sep-2024 a feb-2025)']
PAT = R['Patagones, Dec. 555/2026: club Rampla Juniors, uso para actividades culturales, deportivas y recreativas, por mes (mar-dic 2026)']
PAT_HI = R['Patagones, Dec. 507/2026: Club Social y Deportivo Patagones, escuelas + actividades municipales, por mes (mar-dic 2026)']
CAB = R['Colegio de Abogados de San Isidro: Salón de Actos, sábado, 14 jus x $53.232 (jus 1/8/2026), incluye mantenimiento, limpieza y seguridad']
CLUBES, MESES = 4, 4
p(f'   Mezcla: {n_sol:.1f} shows de solistas y {n_resto:.1f} de dúos, tríos y bandas.')
esc = {}
esc['S1 recomendado: solistas en espacios municipales + 4 convenios con clubes o sociedades de fomento (aporte mensual tipo Bahía Blanca)'] = n_sol * c_muni + CLUBES * MESES * BB
esc['S1 bajo: idem con aporte tipo Patagones 2026 (cultura)'] = n_sol * c_muni + CLUBES * MESES * PAT
esc['S1 alto: idem con aporte tipo Patagones 2026 (club grande, escuelas + municipio)'] = n_sol * c_muni + CLUBES * MESES * PAT_HI
esc['S2 todo en espacios municipales (sólo si alcanza la capacidad: Viejo Concejo 139 butacas)'] = N_INV * c_muni
esc['S3 todo con canon por noche (referencia: Salón de Actos del Colegio de Abogados, 14 jus)'] = N_INV * CAB
esc['S4 solistas municipales + resto con canon por noche'] = n_sol * c_muni + n_resto * CAB
for n, x in esc.items():
    p(f'   {n}: {M(x)} por año ; {M(x - ah)} neto del ahorro por cancelaciones ; {P(x / N_INV)} por show')
p()
p(f'   Por show en convenio mensual (S1 central): {P(CLUBES*MESES*BB/n_resto)} si los {n_resto:.0f} shows se reparten en {CLUBES} salones x {MESES} meses ({n_resto/(CLUBES*MESES):.1f} shows por salón y por mes)')
p('   Sensibilidad S1 central con 6 salones: ' + M(n_sol * c_muni + 6 * MESES * BB) + ' ; con 2 salones: ' + M(n_sol * c_muni + 2 * MESES * BB))
p()
# ===================================================================== 6. CRITERIOS A Y C
p('6. SI EL CLIENTE ELIGE OTRO CRITERIO')
for c, (ms, s_mes, s_dia) in res.items():
    n = round(s_mes); nm = len(ms)
    x = n * mez['solista'] * c_muni + CLUBES * nm * BB
    p(f'   {c.split("[")[0].strip()}: {n} shows, {nm} meses -> S1 central {M(x)} por año')
p()
# ===================================================================== 7. FACTOR DE OCUPACIÓN
p('7. CAPACIDAD TEÓRICA POR SUPERFICIE (Dec. 351/79, Anexo VII, 3.1.2: auditorios y salas de baile 1 m2 por persona; gimnasios 5 m2) [inferencia]')
for n, m2, x in [('Carpa del CASI sobre el patio principal', 216, 1), ('Salón de 300 m2 usado como auditorio', 300, 1), ('Gimnasio de 600 m2 (como gimnasio)', 600, 5), ('Gimnasio de 600 m2 con sillas (como auditorio)', 600, 1)]:
    p(f'   {n}: {m2} m2 / {x} = {m2//x} personas')
p()
p('8. DÓLAR: $1.447,84 (BCRA, Com. A 3500, promedio dic-2025). S1 central en dólares: ' + f'US$ {esc[list(esc)[0]]/1447.84:,.0f}'.replace(',', '.'))
