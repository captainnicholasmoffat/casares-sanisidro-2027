# -*- coding: utf-8 -*-
# [cálculo propio] Tope de volumen para shows municipales al aire libre y el equipo que corresponde.
# Programa San Isidro 2027 - consulta c23d / v4 - 07/10/2026.
# Plata: pesos de diciembre de 2025 (IPC INDEC del repo: ch/wt/data/ipc_indec_mensual.csv; dic-2025 = 10121,3715).
# Precios vistos en oct-2026 -> se deflactan con jul-2026 (12076,3937, último mes publicado): quedan algo altos.
# Dólar: $1.447,84 (BCRA, Com. A 3500, promedio dic-2025). Euro: tipo de pase EUR/USD promedio dic-2025 de la API del BCRA x $1.447,84.
# Uso: python3 -I calculo.py   (escribe calculo_salida.txt al lado)
import csv, json, math, os
SCR = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad'
V = SCR + '/c23d_raw/v4_volumen'
out = []
def p(s=''):
    out.append(s); print(s)
def M(x): return f'{x/1e6:,.2f} M'.replace(',', 'X').replace('.', ',').replace('X', '.')
def P(x): return f'{x:,.0f}'.replace(',', '.')
def d1(x): return f'{x:.1f}'.replace('.', ',')
def d0(x): return f'{x:.0f}'
def lg(x): return math.log10(x)

# ------------------------------------------------------------------------------------------------
IPC = {(int(r['anio']), int(r['mes'])): float(r['indice']) for r in csv.DictReader(open(SCR + '/ch/wt/data/ipc_indec_mensual.csv'))}
B = IPC[(2025, 12)]; J = IPC[(2026, 7)]
K_OCT26 = B / J
USD = 1447.84
eur = json.load(open(V + '/medicion/bcra_api_cotizacion_EUR_dic2025.json'))['results']
pases = [d['detalle'][0]['tipoPase'] for d in eur]
EURUSD = sum(pases) / len(pases)
EUR = EURUSD * USD
p('0. COEFICIENTES')
p(f'   IPC dic-2025 {B} / jul-2026 {J} -> coeficiente para precios de oct-2026: {K_OCT26:.4f}')
p(f'   Dólar $1.447,84; euro: tipo de pase promedio dic-2025 {EURUSD:.4f} USD/EUR ({len(pases)} días hábiles, API BCRA) -> ${d1(EUR)} por euro')
p()

# ------------------------------------------------------------------------------------------------
p('1. TOPES EN LA FACHADA SEGÚN CADA NORMA O GUÍA (dB(A); LAeq salvo indicación)')
p('   1.a IRAM 4062:2016 (Res. 159/96 y 94/2002 PBA; método según UTN-AJEA): LC = 40 + Kz + Ku + Kh; ruido molesto si LE - LC >= 8')
KZ = {'suburbana con poco tránsito (Kz 0)': 0, 'urbana residencial (Kz 5)': 5, 'residencial con rutas principales (Kz 10)': 10}
KU = {'exterior (jardín/patio, Ku +5)': 5, 'interior lindero con la calle (Ku 0)': 0}
KH = {'hábil 8-20 y sáb 8-14 (Kh +5)': 5, 'descanso: hábil 20-22, sáb 14-22, dom/feriado 6-22 (Kh 0)': 0, 'noche 22-6 (Kh -5)': -5}
for zn, kz in KZ.items():
    for un, ku in KU.items():
        s = '; '.join(f'{hn.split(" (")[0]}: LC {40+kz+ku+kh} -> molesto desde {40+kz+ku+kh+8}' for hn, kh in KH.items())
        p(f'     {zn}, {un}: {s}')
p('   1.b COU San Isidro, Anexo IV (dBA hábil / feriado / noche; «Observaciones: IRAM 4062»):')
COU = {'Cb, Rb (residencial baja)': (45, 40, 35), 'APP/1, Rm1/4, Rma2/4/5, Rma1, CR1': (45, 40, 35),
       'APP/2, Cmb1, Cm1, Cm4, Cm5, Cma, Ca1': (50, 45, 40), 'CmbB, Cmb3, Cm3, Rmb3, Rm3, Rma3': (55, 50, 45),
       'Cm2, CE1': (60, 55, 50), 'Zonas de AC': (55, 50, 45)}
for z, v in COU.items():
    p(f'     {z}: literal {v[0]}/{v[1]}/{v[2]}; si son el LC de IRAM 4062 (lectura [inferencia]: coinciden con Kz 0/5/10 y Ku 0), molesto desde {v[0]+8}/{v[1]+8}/{v[2]+8}')
p('     Nota: los valores de Cb/Rb (45/40/35) son exactamente LC = 40 + 0 + 0 + (5/0/-5): la tabla parece ser el «nivel calculado» de IRAM 4062 [inferencia].')
p('   1.c Ciudad de Buenos Aires, Ley 1540 art. 46 (exterior, LAeq,T; día 07-22 / noche 22-07): Tipo II residencial 65/50; Tipo III 70/60; Tipo V (incluye «espectáculos al aire libre») 80/75')
p('   1.d Reino Unido, Noise Council 1995 (LAeq 15 min en receptores): 1-3 días/año: 75 estadios urbanos, 65 otros lugares; 4-12 días/año: LA90 + 15')
p('   1.e Alemania, LAI Freizeitlärm-Richtlinie 2015 (fuera, frente a ventanas): residencial general 55 hábil fuera de descanso / 50 descanso y domingo / 40 noche; '
  'residencial puro 50/45/35; mixto 60/55/45; «eventos raros» (máx. 18 días/año por lugar): 70 día / 55 noche, picos 90/65')
p('   1.f Londres, Lambeth (Brockwell Park 2025): grandes eventos 75 dBA y 90 dBC LCeq 15 min; eventos comunitarios chicos 65 dBA y 75 dBC (o +3 dB sobre el nivel existente)')
p('   1.g Victoria (Australia), EPA 1826: 65 dB(A) afuera en área sensible, 55 dB(A) adentro, en horario estándar')
for bg in (45, 50, 55):
    p(f'   Con un fondo LA90 de {bg} dBA [supuesto: calle residencial de día]: «fondo + 15» = {bg+15}; «fondo + 10» = {bg+10}; «fondo + 5» = {bg+5}')
p()

# ------------------------------------------------------------------------------------------------
p('2. CUÁNTO VOLUMEN HACE FALTA SEGÚN EL PÚBLICO (fuente puntual, 6 dB por duplicación de distancia)')
p('   Supuestos [supuesto]: 1,5 m² por persona (mezcla de sentados y parados); público en rectángulo de ancho 1,2 x profundidad;')
p('   primera fila a 4 m de los bafles; mezcla a 4 m + 60% de la profundidad (mín. 8 m); par de bafles (+3 dB); margen de pico de la música en vivo 12 dB sobre el LAeq.')
SPK = {'JBL EON ONE Compact (112)': 112, 'JBL EON ONE MK2 a batería (119)': 119, 'B-Hype 10 (121)': 121,
       'JBL EON ONE MK2 con 220 V (123)': 123, 'B-Hype 12 (126)': 126}
GEO = {}
for N, Lm in ((50, 80), (300, 85), (1000, 88)):
    A = 1.5 * N; D = math.sqrt(A / 1.2); W = 1.2 * D
    dm = max(8.0, 4 + 0.6 * D); df = 4.0; db = 4 + D
    GEO[N] = (dm, D)
    p(f'   {N} personas: superficie neta {P(A)} m² (bruta con la regla de 1 persona cada 3 m²: {P(3*N)} m²); {d1(W)} m de ancho x {d1(D)} m de fondo; '
      f'mezcla a {d1(dm)} m; última fila a {d1(db)} m')
    for L in (80, 85, 88, 90):
        Lf = L + 20 * lg(dm / df); Lb = L - 20 * lg(db / dm)
        need = L + 20 * lg(dm) - 3 + 12
        ok = [n for n, s in SPK.items() if s >= need]
        p(f'     mezcla {L} dBA -> primera fila {d1(Lf)} | última fila {d1(Lb)} | pico necesario por bafle a 1 m: {d1(need)} dB -> alcanzan: {", ".join(ok) if ok else "ninguno de la lista"}')
    # columna (fuente lineal): en campo cercano cae 3 dB por duplicación
    Lfc = Lm + 10 * lg(dm / df)
    p(f'     con columnas (caída 3 dB por duplicación en campo cercano, cota optimista): mezcla {Lm} -> primera fila {d1(Lfc)} (vs {d1(Lm + 20*lg(dm/df))} con bafles)')
# 1000 personas con retardos
N = 1000; dm, D = GEO[N]; dd = 4 + D / 2
p(f'   1000 personas con 2 bafles de retardo a {d1(dd)} m (los principales cubren la mitad delantera; mezcla dentro de esa zona a 15 m):')
for L in (85, 88):
    Lf = L + 20 * lg(15 / 4)
    p(f'     mezcla {L} dBA a 15 m -> primera fila {d1(Lf)} dBA (sin retardos y mezcla a {d1(dm)} m: {d1(L + 20*lg(dm/4))})')
p('   Topes en el público: OMS 100 LAeq 15 min (nunca superar); Suiza 93 sin obligaciones, 96 con aviso y medición; Bruselas 85 sin condiciones; menores de 13 años (Países Bajos) 91.')
p()

# ------------------------------------------------------------------------------------------------
p('3. DISTANCIA MÍNIMA A LA FACHADA PARA CUMPLIR EL TOPE (dBA): d = d_mezcla x 10^((L_mezcla - L_tope + DI)/20)')
p('   DI = ventaja por directividad hacia la casa [supuesto]: 0 dB si la casa está delante; -5 de costado; -10 si está detrás del escenario (sólo medios y agudos).')
def dist(Lm, dm, Lt, di=0.0, ex=0.0):
    return dm * 10 ** ((Lm - Lt + di - ex) / 20)
casos = [('a) plaza chica, 50 personas', 50, 80), ('a) plaza chica, 300 personas', 300, 80),
         ('b) plaza o parque grande, 300 personas', 300, 85), ('b) plaza o parque grande, 1000 personas', 1000, 85),
         ('c) costa, 1000 personas', 1000, 88)]
for nom, N, Lm in casos:
    dm = GEO[N][0]
    for Lt in (65, 60, 58, 55, 50):
        dd = [dist(Lm, dm, Lt, di) for di in (0, -5, -10)]
        p(f'   {nom}: mezcla {Lm} dBA a {d1(dm)} m, tope {Lt} en fachada -> delante {d0(dd[0])} m | costado {d0(dd[1])} m | detrás {d0(dd[2])} m')
p('   Con 5 dB extra de atenuación (suelo blando, arboleda, edificios en el medio) las distancias se dividen por 1,8 [cálculo].')
p()
p('   Al revés: tope operativo en la mezcla para que la fachada cumpla, según la distancia real (casa delante / detrás):')
for dm, dfs in ((8.7, (20, 30, 40, 60)), (15.6, (40, 80, 120, 150)), (25.2, (150, 250, 400, 600))):
    for Lt in (65, 60, 55):
        s = ' | '.join(f'{df} m: {d1(Lt + 20*lg(df/dm))} / {d1(Lt + 20*lg(df/dm) + 10)}' for df in dfs)
        p(f'     mezcla a {d1(dm)} m, tope fachada {Lt}: {s}')
p()

# ------------------------------------------------------------------------------------------------
p('4. GRAVES: dB(C) FRENTE A dB(A), CON Y SIN SUBWOOFER, DELANTE Y DETRÁS DEL ESCENARIO')
F = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000]
AW = [-39.4, -26.2, -16.1, -8.6, -3.2, 0.0, 1.2, 1.0, -1.1]       # ponderación A (IEC 61672), por octava
CW = [-3.0, -0.8, -0.2, 0.0, 0.0, 0.0, -0.2, -0.8, -3.0]          # ponderación C
AIR = [0.02, 0.1, 0.4, 1.0, 1.9, 3.7, 9.7, 32.8, 117.0]           # dB/km, 20 °C, 70% HR (ISO 9613-1, valores redondeados)
REAR = [0, 0, 2, 5, 8, 12, 15, 18, 20]                            # atenuación detrás de un bafle de 2 vías [supuesto]
CON_SUB = [-6, 2, 0, -4, -7, -10, -12, -15, -21]                   # espectro Z relativo de banda en vivo con sub [supuesto]
SIN_SUB = [-30, -10, -2, -4, -7, -10, -12, -15, -21]               # sólo bafles, corte en ~80 Hz [supuesto]
def suma(levels): return 10 * lg(sum(10 ** (l / 10) for l in levels))
def ponder(spec, w): return suma([s + x for s, x in zip(spec, w)])
def a_dist(spec, d0_, d, rear=False):
    return [s - 20 * lg(d / d0_) - a * d / 1000 - (r if rear else 0) for s, a, r in zip(spec, AIR, REAR)]
ESC = [('a) plaza chica, 300 personas', 80, 15.6, 30), ('b) parque grande, 1000 personas', 85, 25.2, 120), ('c) costa, 1000 personas', 88, 25.2, 400)]
for nombre, spec in (('con subwoofer', CON_SUB), ('sin subwoofer', SIN_SUB)):
    for esc, Lm, dm, df in ESC:
        off = Lm - ponder(spec, AW); s_ = [x + off for x in spec]
        lc = ponder(s_, CW)
        r = []
        for rear in (False, True):
            t = a_dist(s_, dm, df, rear); A_ = ponder(t, AW); C_ = ponder(t, CW)
            r.append(f'{"detrás" if rear else "delante"} {d1(A_)} dBA / {d1(C_)} dBC (LC-LA {d1(C_-A_)})')
        p(f'   {nombre}, {esc}: mezcla {Lm} dBA = {d1(lc)} dBC (LC-LA {d1(lc-Lm)}) a {dm} m; fachada a {df} m: ' + ' | '.join(r))
p('   Lectura: el sub casi no mueve el dBA pero sube el dBC; detrás del escenario el dBA baja mucho más que el dBC.')
p()

# ------------------------------------------------------------------------------------------------
p('5. PRECIOS (pesos de dic-2025; vistos el 07/10/2026 en comercios con precio visible, con IVA)')
PR = [
 ('dB Technologies B-Hype 10 (121 dB pico, 85°-120° x 85°)', 877044.11, 'Todo Música'),
 ('dB Technologies B-Hype 10', 1127100, 'Hendrix'),
 ('dB Technologies B-Hype 12 (126 dB)', 1051483.80, 'Todo Música'),
 ('dB Technologies B-Hype 12', 1351300, 'Hendrix'),
 ('dB Technologies B-Hype 8', 903000, 'Hendrix'),
 ('dB Technologies SUB 615 (131 dB)', 2452214.70, 'Todo Música'),
 ('dB Technologies SUB 612 (129 dB)', 1989324.75, 'Todo Música'),
 ('Par de pies dB SK 25 TT', 325092.84, 'Todo Música'),
 ('Behringer XR18', 1450100, 'Hendrix'),
 ('JBL EON ONE Compact (112 dB, batería)', 1997600, 'Hendrix'),
 ('JBL EON ONE PRO (discontinuado)', 3032808.34, 'Todo Música'),
 ('Bose L1 Pro8 (180° horizontal)', 5343500, 'Hendrix'),
 ('dB Technologies ES 503 (columna + sub 12")', 3952042.78, 'Todo Música'),
 ('dB Technologies ES 1002 (columna + 2 sub 12")', 7877193.16, 'Todo Música'),
 ('dbx DriveRack VENU360 (limitador con bloqueo y clave)', 2505962.46, 'Todo Música'),
 ('Decibelímetro Nisuta NSDEC (no es clase IEC)', 50819, 'Frávega'),
]
for n, x, c in PR:
    p(f'   {n} ({c}): ${P(x)} -> {M(x*K_OCT26)}')
E10C2 = 1999; E10C1 = 2499; ETRO = 317.15
p(f'   10EaZy clase 2 (Dinamarca, sin IVA, envío ni impuestos): {E10C2} € -> ${P(E10C2*EUR)} = {M(E10C2*EUR)} (dic-2025, sin derechos de importación)')
p(f'   10EaZy clase 1: {E10C1} € -> {M(E10C1*EUR)}')
p(f'   Sonómetro clase 2 con registro, Trotec (Infoagro, España, sin IVA; no informa LAeq): {ETRO} € -> {M(ETRO*EUR)}')
p('   No encontré con precio visible en comercios argentinos: JBL EON ONE MK2, Bose L1 Pro16, sonómetro integrador clase 2, calibrador acústico, micrófono de medición.')
p()

# ------------------------------------------------------------------------------------------------
p('6. KITS POR LUGAR (sólo sonido y control de nivel; pesos de dic-2025)')
k = K_OCT26
bh10 = 877044.11 * k; bh12 = 1051483.80 * k; sub = 2452214.70 * k; pies = 325092.84 * k
venu = 2505962.46 * k; eazy = E10C2 * EUR; eon = 1997600 * k; l1 = 5343500 * k
p(f'   Kit de show del 23 ter (sonido): 19,4 M; con tarima y toldos: 29,5 M (dato del c23c, no recalculado)')
p(f'   A) Modo plaza = kit de show sin SUB 615 ni B-Hype 12; principales = 2 B-Hype 10; se compran 2 B-Hype 10 más para no perder monitores:')
a_extra = 2 * bh10 + pies
p(f'      2 B-Hype 10 + 1 par de pies: {M(a_extra)}')
p(f'   B) Limitador con bloqueo para cada kit de show: dbx VENU360 {M(venu)}')
p(f'   C) Medición permanente en la mezcla con registro (10EaZy clase 2, sin importación): {M(eazy)}')
tot = a_extra + venu + eazy
p(f'   Total por kit de show (A + B + C): {M(tot)}; para 2 kits: {M(2*tot)}  (+ notebook Windows para el 10EaZy: no cotizada)')
p(f'   Sin 10EaZy (si se usa app validada + micrófono externo, sin precio local): {M(a_extra + venu)} por kit')
p(f'   Retardos para 1000 personas: 2 B-Hype 10 + pies = {M(a_extra)} (el VENU360 trae retardo de torre)')
p(f'   Alternativas para plaza (2 unidades): JBL EON ONE Compact {M(2*eon)} (no alcanza para 300 a 80 dBA); Bose L1 Pro8 {M(2*l1)} (dispersión de 180°)')
p(f'   Ahorro por no comprar el SUB 615 en un kit sólo de plazas: {M(sub)}; en B-Hype 12: {M(2*bh12)}')
p()

# ------------------------------------------------------------------------------------------------
p('7. CUÁNTOS SHOWS POR LUGAR: 200 shows por año repartidos')
for n in (8, 12, 17, 25, 40):
    p(f'   en {n} lugares: {d1(200/n)} shows por lugar y por año')
p('   Para quedar en «hasta 12 por año» (Reino Unido) hacen falta 17 lugares; para «hasta 18» (Alemania), 12 lugares.')


# ------------------------------------------------------------------------------------------------
p()
p('8. PROPUESTA [inferencia] Y CHEQUEO: tope del lugar en la mezcla vs. tope que permite la fachada (casa delante / detrás del escenario)')
PROP = [('a) plaza chica junto a casas', 80, 8.7, 60, (20, 30, 40)), ('a) plaza chica, 300 personas', 80, 15.6, 60, (30, 40, 60)),
        ('b) plaza o parque grande', 85, 15.6, 60, (80, 120, 150)), ('b) idem, lugar con hasta 12 shows/año', 85, 15.6, 65, (80, 120, 150)),
        ('c) costa lejos de casas', 88, 25.2, 60, (250, 400, 600)), ('c) idem, lugar con hasta 12 shows/año', 88, 25.2, 65, (250, 400, 600))]
for nom, Lp, dm, Lt, dfs in PROP:
    r = []
    for df in dfs:
        fr = Lt + 20 * lg(df / dm); bk = fr + 10
        r.append(f'{df} m: {d1(min(Lp, fr))} / {d1(min(Lp, bk))}')
    p(f'   {nom}: tope del lugar {Lp} dBA en la mezcla ({dm} m), fachada {Lt} dBA -> tope operativo ' + ' | '.join(r))
p('   (el tope operativo es el menor entre el del lugar y el que deja la fachada; con la casa detrás se suma la ventaja de 10 dB supuesta)')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calculo_salida.txt'), 'w').write('\n'.join(out) + '\n')
