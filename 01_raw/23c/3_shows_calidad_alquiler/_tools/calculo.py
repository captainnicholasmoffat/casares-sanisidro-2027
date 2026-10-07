# -*- coding: utf-8 -*-
# [cálculo propio] 200 shows por año: cancelaciones por clima, calidad del sonido, equipos de producción y alquiler.
# Programa San Isidro 2027 - consulta c23c / w3a - 07/10/2026.
# Plata: pesos de diciembre de 2025 (IPC INDEC del repo: ch/wt/data/ipc_indec_mensual.csv; dic-2025 = 10121,3715).
# Precios de comercios vistos en oct-2026 (sin IPC publicado) -> se deflactan con jul-2026 (12076,3937): quedan algo altos.
# Uso: python3 -I calculo.py  (escribe la salida en calculo_salida.txt)
import csv, glob, os, math, collections
SCR = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad'
W = SCR + '/c23c_raw/w3a_shows_calidad_alquiler'
IPC = {(int(r['anio']), int(r['mes'])): float(r['indice']) for r in csv.DictReader(open(SCR + '/ch/wt/data/ipc_indec_mensual.csv'))}
B = IPC[(2025, 12)]
def k(y, m):
    if (y, m) > (2026, 7): y, m = 2026, 7
    return B / IPC[(y, m)]
OCT26 = k(2026, 10)
out = []
def p(s=''):
    out.append(s); print(s)
def M(x): return f'{x/1e6:,.1f} M'.replace(',', 'X').replace('.', ',').replace('X', '.')
def P(x): return f'{x:,.0f}'.replace(',', '.')
def pc(x): return f'{100*x:.1f}%'.replace('.', ',')
DM = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

p('COEFICIENTES IPC (dic-2025 / mes): ' + '; '.join(f'{y}-{m:02d} {k(y,m):.4f}' for y, m in
  [(2024,2),(2024,5),(2024,12),(2025,2),(2025,11),(2025,12),(2026,2),(2026,3),(2026,4),(2026,7)]) + ' ; oct-2026 -> jul-2026')
p()
# =====================================================================================================
p('1. CLIMA: ¿CUÁNTOS DÍAS CON ALERTA AMARILLA O MAYOR (LLUVIA, TORMENTA, VIENTO) EN SAN ISIDRO?')
# SMN, Estadísticas Climatológicas Normales 1991-2020 (repositorio SMN, handle 2506), promedios mensuales leídos de
# las tablas (pág. PDF 190, 193, 195 San Fernando; 278, 281, 283 Aeroparque; 286, 289, 291 Observatorio) [verificado]
SMN = {
 'San Fernando Aero (1996-2020)': {'p1': [6.9,6.5,6.0,6.5,5.2,4.2,4.9,5.3,5.6,7.4,6.8,6.6], 'torm': [5.3,4.5,3.6,3.6,2.3,1.8,1.8,3.4,2.8,5.0,5.1,6.0], 'vf': [6.7,5.5,3.7,4.6,2.3,2.8,2.5,5.0,6.6,9.0,6.8,7.6]},
 'Aeroparque Aero':              {'p1': [6.7,6.0,5.9,6.6,5.0,4.5,5.0,5.0,5.5,7.5,6.8,6.6], 'torm': [5.9,4.7,4.3,3.9,2.6,2.5,1.9,3.7,2.7,5.5,4.8,6.3], 'vf': [14.6,12.8,9.2,8.6,5.5,6.8,5.4,7.7,11.1,14.5,13.8,12.1]},
 'Buenos Aires Observatorio':    {'p1': [7.5,6.8,6.7,7.1,5.2,4.9,5.6,4.9,5.8,7.9,7.2,6.9], 'torm': [6.2,5.0,4.4,3.7,2.5,2.5,2.0,3.5,3.0,5.7,4.8,6.1], 'vf': [2.6,2.2,1.8,2.0,0.9,1.4,1.0,2.0,3.1,3.5,3.0,3.4]},
}
p('   SMN normales 1991-2020 (días por año): ' + ' ; '.join(f"{n}: lluvia>=1 mm {sum(v['p1']):.1f}, tormenta {sum(v['torm']):.1f}, viento fuerte (2011-20) {sum(v['vf']):.1f}" for n, v in SMN.items()))
# NOAA GSOD 2016-2025, San Fernando (87553): días por mes con fenómenos al nivel de los umbrales amarillos para la provincia
# (lluvia >= 40 mm en el día; viento >= 55 km/h o ráfaga >= 65 km/h) o tormenta con >= 20 mm.
KT = 1.852
def gsod(st):
    c = collections.defaultdict(collections.Counter)
    for f in sorted(glob.glob(f'{W}/smn/noaa_gsod/gsod_{st}_*.csv')):
        for r in csv.DictReader(open(f)):
            m = int(r['DATE'][5:7]); x = c[m]; x['d'] += 1
            pr = float(r['PRCP']); pmm = None if pr >= 99.9 else pr * 25.4
            g = float(r['GUST']); g = None if g >= 999 else g * KT
            v = float(r['MXSPD']); v = None if v >= 999 else v * KT
            th = r['FRSHTT'].strip()[4:5] == '1'
            vi = (g is not None and g >= 65) or (v is not None and v >= 55)
            x['viento'] += vi; x['torm'] += th
            x['obs'] += ((pmm is not None and pmm >= 40) or vi or (th and pmm is not None and pmm >= 20))
    return [c[m+1]['obs'] / c[m+1]['d'] * DM[m] for m in range(12)], [c[m+1]['viento'] / c[m+1]['d'] * DM[m] for m in range(12)], [c[m+1]['torm'] / c[m+1]['d'] * DM[m] for m in range(12)]
obs_sf, vto_sf, tor_sf = gsod('87553099999')
p(f'   GSOD 2016-2025 San Fernando: días/año con fenómeno al umbral amarillo observado en el lugar {sum(obs_sf):.1f}; con viento al umbral {sum(vto_sf):.1f}; con tormenta {sum(tor_sf):.1f}')
sf = SMN['San Fernando Aero (1996-2020)']
esc = {
 'bajo':    [obs_sf[m] for m in range(12)],                                   # sólo días en que el fenómeno ocurrió en el lugar
 'alto':    [sf['torm'][m] + vto_sf[m] for m in range(12)],                     # alerta todos los días de tormenta + días de viento fuerte
}
esc['central'] = [(esc['bajo'][m] + esc['alto'][m]) / 2 for m in range(12)]
p('   ESCENARIOS de días con alerta amarilla o mayor para la zona San Isidro [inferencia; el SMN no publica conteos por zona]:')
p('     bajo = días con el fenómeno observado en San Fernando (GSOD); alto = días con tormenta (SMN 1991-2020) + días con viento al umbral (GSOD); central = promedio')
p('     mes    ' + '  '.join(f'{x:>5}' for x in MES) + '   año')
for e in ('bajo', 'central', 'alto'):
    p(f'     {e:<7}' + '  '.join(f'{x:5.1f}' for x in esc[e]) + f'   {sum(esc[e]):5.1f}')
for e in ('bajo', 'central', 'alto'):
    p(f'     {e:<7} % de días con alerta: ' + '  '.join(f'{100*esc[e][m]/DM[m]:4.0f}%' for m in range(12)))
TEMP = {'oct-abr': [0,1,2,3,9,10,11], 'todo el año': list(range(12))}
def frac(e, meses):
    dias = sum(DM[m] for m in meses)
    return sum(esc[e][m] for m in meses) / dias
F = {}
for t, ms in TEMP.items():
    for e in ('bajo', 'central', 'alto'):
        F[(t, e)] = frac(e, ms)
    p(f'   Temporada {t}: fracción de shows que caen en día con alerta: bajo {pc(F[(t,"bajo")])} ; central {pc(F[(t,"central")])} ; alto {pc(F[(t,"alto")])}')
p('   Sensibilidad: si sólo cancela la alerta que cubre el bloque horario del show (tarde-noche) [supuesto: x0,6]: ' + ' ; '.join(f"{t} central {pc(0.6*F[(t,'central')])}" for t in TEMP))
p()
# =====================================================================================================
p('2. CACHETS Y COSTO DE CANCELAR (regla del cliente: cancelar con alerta amarilla, pagar 70% y después el show entero en la nueva fecha)')
SADEM = 313636           # piso SADEM por músico, festivales/fiestas municipales, en pesos de dic-2025 [verificado en c23b z4a]
CACHET_MUS = SADEM * 1.25
mezcla = [('solista', 0.40, 1.0), ('dúo o trío', 0.30, 2.5), ('banda de 4-5', 0.30, 4.5)]
mus = sum(s * n for _, s, n in mezcla)
prom = CACHET_MUS * mus
p(f'   Cachet por músico (piso SADEM + 25%): {P(CACHET_MUS)} ; músicos por show {mus:.2f} ; cachet promedio por show {P(prom)}')
for n, s, m in mezcla:
    p(f'     {n}: {m} músicos -> {P(CACHET_MUS*m)} por show ; {int(200*s)} shows -> {M(200*s*CACHET_MUS*m)}')
BASE = 200 * prom
p(f'   200 shows hechos: {M(BASE)} por año')
CANC = {}
for t in TEMP:
    for e in ('bajo', 'central', 'alto'):
        f = F[(t, e)]
        n_c = 200 * f / (1 - f)          # cancelaciones esperadas: cada fecha nueva también puede caer en alerta
        extra = n_c * 0.70 * prom
        CANC[(t, e)] = (n_c, extra)
        p(f'   {t:<11} {e:<7}: cancelaciones {n_c:5.1f} por año ; pago del 70% {M(extra)} ; total cachets {M(BASE+extra)} (+{pc(extra/BASE)})')
p()
# =====================================================================================================
p('3. CALIDAD: SPL A DISTANCIA Y KITS')
# SPL continuo aprox. = SPL máx (pico, ficha) - 6 dB (factor de cresta) - 20 log10(d) + 10 log10(N cajas) [cálculo propio; campo libre, sin ganancia de sala]
fichas = {'JBL EON ONE PRO (118 dB pico)': 118, 'JBL EON ONE Compact (112 dB)': 112, 'dB B-Hype 10 (121 dB)': 121,
          'dB B-Hype 12 (126 dB)': 126, 'dB B-Hype 15 (126,5 dB)': 126.5, 'dB KL 12 (127 dB)': 127}
for n, spl in fichas.items():
    s = '; '.join(f'{d} m: {spl - 6 - 20*math.log10(d) + 10*math.log10(2):.0f} dB' for d in (5, 10, 15, 20))
    p(f'   par de {n}: {s}')
p('   Meta [inferencia]: 50-300 personas al aire libre ~ 17 x 17 m; banda con batería ~95 dB(A) en la mesa (10-15 m) y >=90 dB al fondo; solista 80-85 dB.')
p()
# Precios nominales oct-2026 con IVA (Todo Música / Hendrix / EcoFlow Store), vida útil en años
def kit(items, nombre):
    tot = 0; am = 0
    p(f'   {nombre}:')
    for q, n, pr, src, vu in items:
        v = q * pr * OCT26; tot += v; am += v / vu
        p(f'     {q} x {n} ({src}) {P(pr)} c/u -> {M(v)} ; vida útil {vu}')
    return tot, am
show = [
 (2, 'dB Technologies B-Hype 12 (12", 126 dB, 61 Hz-19,5 kHz)', 1051483.80, 'Todo Música', 7),
 (1, 'dB Technologies SUB 615 (15", 600 W RMS, 131 dB)', 2452214.70, 'Todo Música', 7),
 (1, 'Par de pies de bafle dB SK 25 TT', 325092.84, 'Todo Música', 5),
 (4, 'Monitor dB Technologies B-Hype 10 (121 dB)', 877044.11, 'Todo Música', 7),
 (1, 'Mezcladora digital Behringer XR18 (16 previos, 6 envíos aux)', 1450100.00, 'Hendrix', 7),
 (4, 'Shure SM58', 266688.63, 'Todo Música', 10),
 (3, 'Shure SM57', 243426.06, 'Todo Música', 10),
 (1, 'Kit de micrófonos de batería Shure PGADRUMKIT5', 683753.06, 'Todo Música', 8),
 (1, 'Inalámbrico Sennheiser XSW 1-825-A', 1030852.26, 'Todo Música', 7),
 (4, 'Caja directa activa Samson MDA1', 150988.72, 'Todo Música', 7),
 (12, 'Pie de micrófono con brazo Quik Lok', 89765.79, 'Todo Música', 5),
 (20, 'Cable XLR 6 m', 37343.43, 'Todo Música', 3),
 (6, 'Cable plug 3 m', 80079.35, 'Todo Música', 3),
 (2, 'Estación de energía EcoFlow Delta 3 1500 (1.536 Wh)', 2890990.00, 'EcoFlow Store', 8),
]
st, sa = kit(show, 'KIT SHOW propuesto (50-300 personas, bandas de hasta 5)')
st *= 1.05; sa += st * 0.05 / 1.05 / 3
tarima34 = 9.6e6     # tarima 3x4 m (6 módulos), estimación del informe c23b z4a [sin confirmar]
toldo = 2 * 311992 * OCT26
show_tot = st + tarima34 + toldo
show_am = sa + tarima34 / 10 + toldo / 2
p(f'     + 5% varios; sonido {M(st)} ; + tarima 3x4 {M(tarima34)} [sin confirmar] + 2 toldos {M(toldo)} = KIT SHOW {M(show_tot)} ; amortización {M(show_am)} por año')
kit23 = 13.8e6; kit23_t = 20.4e6; kit23_am = 2.9e6
p(f'   Kit del 23 bis (c23b z4a): sonido {M(kit23)} ; con tarima 2x4 {M(kit23_t)} ; amortización {M(kit23_am)}')
p(f'   Diferencia por kit (show propuesto - 23 bis completo): {M(show_tot - kit23_t)}')
call = [
 (2, 'JBL EON ONE Compact (112 dB, 12 h de batería)', 1997600.00, 'Hendrix', 7),
 (2, 'Shure SM58', 266688.63, 'Todo Música', 10),
 (1, 'Shure SM57', 243426.06, 'Todo Música', 10),
 (1, 'Caja directa activa Samson MDA1', 150988.72, 'Todo Música', 7),
 (3, 'Pie de micrófono con brazo Quik Lok', 89765.79, 'Todo Música', 5),
 (6, 'Cable XLR 6 m', 37343.43, 'Todo Música', 3),
 (1, 'Par de pies de bafle Samson LS2', 146557.60, 'Todo Música', 5),
]
ct, ca = kit(call, 'KIT CALLEJERO propuesto (turnos de 1 h, 65-72 dB, sin enchufe)')
ct *= 1.05; ca += ct * 0.05 / 1.05 / 3
p(f'     + 5% varios = KIT CALLEJERO {M(ct)} ; amortización {M(ca)} por año')
p()
# =====================================================================================================
p('4. EQUIPOS DE PRODUCCIÓN: JORNADAS Y PERSONAS')
cargas = 0.12 + 0.048 + 0.03275; pres = 50371   # como c23b z4a / informe Y4
esc40 = {6: 625405, 7: 656559, 9: 723994}        # Decreto 782/2026, régimen 40 h, desde jul-2026 [verificado en c23b z4a]
def costo(b): return (b * 13 * (1 + cargas) + pres * 12) * k(2026, 7)
def personas(tec, asi, cho, rep=0.15):
    b = tec * costo(esc40[9]) + asi * costo(esc40[6]) + cho * costo(esc40[7])
    return b, b * (1 + rep)
JOR_PERS = 222   # jornadas por persona por año: 260 hábiles - 15 feriados - 15 vacaciones - 8 enfermedad [supuesto]
p(f'   Jornadas útiles por persona: {JOR_PERS} por año [supuesto]; equipo = 1 técnico (cat. 9) + 1 asistente (cat. 6); chofer (cat. 7) aparte')
p('   Duración de jornadas [supuesto]: callejeros 7 h (carga 0,5 + traslado 0,5 + armado 0,5 + 4 turnos de 1 h con cambios 4,5 + desarme y vuelta 1);')
p('                                    show 9 h (carga 0,5 + traslado 0,5 + tarima 0,75 + sonido 1,25 + prueba 1 + show 1,5 + desarme 1,5 + vuelta y descarga 1 + margen 1)')
CALLE = 2 * 160
for t in TEMP:
    for e in ('central', 'alto'):
        n_c, _ = CANC[(t, e)]
        for por_j in (1, 2):
            shows_j = (200 + n_c) / por_j + 0.5 * n_c / por_j     # la mitad de las cancelaciones se decide el mismo día y gasta la jornada [supuesto]
            dem = (CALLE + shows_j) * 1.10                       # +10% mantenimiento, carga y reparación [supuesto]
            p(f'   {t:<11} {e:<7} {por_j} show(s) por jornada: callejeros {CALLE} + shows {shows_j:5.1f} + 10% mant. = {dem:5.0f} jornadas-equipo ;'
              f' capacidad 2 equipos {2*JOR_PERS} -> {"ALCANZA" if dem <= 2*JOR_PERS else "NO alcanza"} ; 3 equipos {3*JOR_PERS} -> {"ALCANZA" if dem <= 3*JOR_PERS else "NO alcanza"} ; equipos necesarios {dem/JOR_PERS:.2f}')
libre2 = 2 * JOR_PERS - CALLE * 1.10
p(f'   Con 2 equipos quedan {libre2:.0f} jornadas para shows después de los callejeros -> unos {libre2/1.10/1.06:.0f} shows por año (con 10% de mantenimiento y 6% de reprogramación)')
# Semana pico (temporada de shows oct-abr, 30,3 semanas, con callejeros en paralelo)
sem = 212 / 7
n_c = CANC[('oct-abr', 'central')][0]
pico = 8 + (200 + n_c) / sem + 0.5 * n_c / sem
p(f'   Semana pico oct-abr (central): callejeros 8 + shows {(200+n_c)/sem + 0.5*n_c/sem:.1f} = {pico:.1f} jornadas-equipo (+10% = {pico*1.1:.1f}); 2 equipos x 5 días = 10 ; x 6 días (48 h) = 12 ; 3 equipos x 5 = 15')
pico_all = 8 + (200 + CANC[('todo el año','central')][0]) * 1.25 / 52
p(f'   Semana típica todo el año (central): callejeros 8 + shows {pico_all-8:.1f} (con 25% más en verano) = {pico_all:.1f} (+10% = {pico_all*1.1:.1f}) vs 3 equipos x 5 = 15')
b2, c2 = personas(2, 2, 1); b2b, c2b = personas(2, 2, 2); b3, c3 = personas(3, 3, 2)
p(f'   Costo por año: 2 equipos (2 téc + 2 asist + 1 chofer) {M(b2)} ; +15% reemplazos {M(c2)}')
p(f'                  2 equipos con 2 choferes (si hay shows el fin de semana) {M(b2b)} ; +15% {M(c2b)}')
p(f'                  3 equipos (3 téc + 3 asist + 2 choferes) {M(b3)} ; +15% {M(c3)}')
p()
# =====================================================================================================
p('5. ALQUILAR LOS SHOWS POR LICITACIÓN vs EQUIPO PROPIO')
refs = [
 ('Ciudad de Bs. As., DG Festivales, BAC 3190-1544-CME24: 7 espacios x 5 días en la Usina del Arte (bafles en trípode, consola, micrófonos, operador, traslado y armado) -> por espacio y día', 12758000/35, (2024,5)),
 ('General Paz, Res. 110/2025: sonido e iluminación para un acto del Concejo en el SUM', 600000, (2025,11)),
 ('Patagones, Dec. 2994 (30/12/2024): sonido para el «Mercado Municipal»', 300000, (2024,12)),
 ('Lobería, Dec. 750-26: subsidio para sonido de un desfile', 120000, (2026,4)),
 ('Lobería, Dec. 827-26: subsidio para sonido en la Sociedad Rural', 380000, (2026,4)),
 ('General Paz, Dec. 169/2026: sonido + iluminación + generador, festival (1 noche)', 3500000, (2026,2)),
 ('Coronel Pringles, Dec. 272/25: escenario secundario para shows locales con sonido, luces y pantalla (1 día)', 5900000, (2025,2)),
 ('San Isidro, CP 7/2024: alquiler de sonido para el Carnaval 2024', 2528900, (2024,2)),
 ('San Isidro, CP 101/2024: sistema de sonido con estructuras Layher', 5987000, (2024,6)),
 ('San Isidro, CP 35/2025: estructuras, sonido e iluminación, Cierre de Verano (1 evento)', 32200000, (2025,3)),
]
for n, v, ym in refs:
    p(f'   {n}: {P(v)} nominal -> {M(v*k(*ym))} dic-25')
lp3 = 77800000 * k(2026, 3)
p(f'   San Isidro, LP 3/2026 (servicio integral de sonido y proyección): {M(lp3)} dic-25; cantidad de servicios no publicada. Si cubriera N eventos:')
p('     ' + ' ; '.join(f'{n} eventos -> {M(lp3/n)} c/u' for n in (50, 100, 150, 200, 300)))
p('   Precio de alquiler por show con sonido, técnico, tarima, traslado y armado [supuesto, a partir de las referencias]:')
tarima_alq = 100000 * k(2025, 12)
caba = 12758000 / 35 * k(2024, 5)
PRECIO = {'bajo': caba + tarima_alq, 'alto': 3.5e6 * k(2026, 2)}
PRECIO['central'] = math.sqrt(PRECIO['bajo'] * PRECIO['alto'])   # punto medio geométrico [supuesto]
PRECIO = {kk: PRECIO[kk] for kk in ('bajo', 'central', 'alto')}
p(f'     bajo = Ciudad por espacio y día + tarima de General Villegas ($100.000/día) = {M(PRECIO["bajo"])} ; central = punto medio geométrico {M(PRECIO["central"])} ; alto = festival chico de General Paz = {M(PRECIO["alto"])}')
t = 'oct-abr'; e = 'central'
n_c = CANC[(t, e)][0]
for pe, pr in PRECIO.items():
    alq = pr * 200 + pr * 0.5 * (0.5 * n_c)     # se paga cada show hecho; la mitad de las cancelaciones es en el día y paga 50% [supuesto]
    p(f'   Alquilar los 200 shows (precio {pe}): {M(alq)} por año')
# Equipo propio: costo incremental de hacer los shows en casa (3.er equipo + kits de show) frente a sólo callejeros con 2 equipos
van_l1 = 62170000 * OCT26; van_l3 = 68080000 * OCT26
def anual_equipo(n_show_kits, n_call_kits, tec, asi, cho, van):
    _, pers = personas(tec, asi, cho)
    return pers + n_show_kits * show_am + n_call_kits * ca + van / 10 + 0.10 * van
A = anual_equipo(2, 2, 3, 3, 2, van_l3)
Bc = anual_equipo(0, 2, 2, 2, 1, van_l1)
C = anual_equipo(2, 2, 2, 2, 2, van_l1)
p(f'   Opción A, todo propio (3 equipos, 2 kits de show, 2 kits callejeros, 1 camioneta L3H2): {M(A)} por año ; compra {M(2*show_tot + 2*ct + van_l3)}')
p(f'   Opción B, 2 equipos sólo callejeros (2 kits callejeros, 1 camioneta L1H1): {M(Bc)} por año ; compra {M(2*ct + van_l1)}')
p(f'   -> costo propio incremental de los 200 shows (A - B): {M(A - Bc)} por año = {M((A - Bc)/200)} por show')
A23 = A - 2 * show_am + 2 * kit23_am
p(f'   (con el kit del 23 bis en lugar del kit de show, la opción A costaría {M(A23)} por año: la mejora de calidad suma {M(A - A23)} por año y {M(2*(show_tot-kit23_t))} de compra)')
for pe, pr in PRECIO.items():
    alq = pr * 200 + pr * 0.25 * n_c
    p(f'      B + alquilar 200 shows ({pe}): {M(Bc + alq)} por año vs A {M(A)} -> diferencia {M(Bc + alq - A)}')
shows_propios = round(libre2 / 1.10 / 1.06)
for pe, pr in PRECIO.items():
    alq = pr * (200 - shows_propios) * (1 + 0.25 * n_c / 200)
    p(f'   Opción C, 2 equipos + 2 kits de show, {shows_propios} shows propios y {200-shows_propios} alquilados ({pe}): {M(C + alq)} por año')
p()
p('6. PROGRAMA COMPLETO POR AÑO (cachets + producción), temporada oct-abr, escenario central de clima')
cach = BASE + CANC[('oct-abr', 'central')][1]
p(f'   Cachets {M(cach)} + opción A {M(A)} = {M(cach + A)} ; primer año + compra {M(cach + A + 2*show_tot + 2*ct + van_l3)}')
open(os.path.join(W, '_tools', 'calculo_salida.txt'), 'w').write('\n'.join(out) + '\n')
