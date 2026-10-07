# Temperatura y viento a las 18, 20, 21 y 22 h (hora argentina, UTC-3) por mes, San Fernando Aero (OMM 87553),
# a partir de NOAA NCEI Integrated Surface Database (global-hourly), 2016-2025 (datos SYNOP/METAR del SMN).
# Uso: python3 -I isd_horario.py <carpeta_csv> > salida.txt
import sys, csv, os, glob, datetime, collections, math
carp = sys.argv[1]
HORAS = (18, 20, 21, 22)
obs = {}  # (fecha_local, hora_local) -> (T, viento_kmh)
for f in sorted(glob.glob(os.path.join(carp, '87553099999_*.csv'))):
    with open(f, newline='') as fh:
        for r in csv.DictReader(fh):
            dt = datetime.datetime.fromisoformat(r['DATE']) - datetime.timedelta(hours=3)
            if dt.minute > 10 and dt.minute < 50: continue
            if dt.minute >= 50: dt = dt + datetime.timedelta(minutes=60 - dt.minute)
            h = dt.hour
            if h not in HORAS: continue
            t = r['TMP'].split(',')
            if t[0] in ('+9999', '') or t[1] not in ('0','1','4','5','9','A','C','I','M','P','R','U'): continue
            T = int(t[0]) / 10
            w = r['WND'].split(',')
            ws = None
            if len(w) >= 4 and w[3] != '9999' and w[4] in ('0','1','4','5','9'):
                ws = int(w[3]) / 10 * 3.6
            k = (dt.date(), h)
            # prioridad SYNOP (FM-12) sobre METAR si hay dos
            if k not in obs or r['REPORT_TYPE'].strip() == 'FM-12':
                obs[k] = (T, ws)
def st(xs):
    xs = [x for x in xs if x is not None]
    return (sum(xs) / len(xs), len(xs)) if xs else (float('nan'), 0)
def wc(T, v):  # sensación térmica por viento (fórmula de enfriamiento por viento, T<=10 °C, v>4,8 km/h)
    if v is None or T > 10 or v <= 4.8: return T
    return 13.12 + 0.6215*T - 11.37*v**0.16 + 0.3965*T*v**0.16
MES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
print('mes;n_dias_21h;T18_media;T20_media;T21_media;T22_media;viento21_kmh;sens21_media;pct21_lt10;pct21_lt12;pct21_lt14;pct_sens21_lt10;pct22_lt10')
for m in range(1, 13):
    d = collections.defaultdict(list)
    for (fe, h), (T, ws) in obs.items():
        if fe.month == m: d[h].append((T, ws))
    T21 = [x[0] for x in d[21]]; W21 = [x[1] for x in d[21]]; S21 = [wc(*x) for x in d[21]]
    T22 = [x[0] for x in d[22]]
    n = len(T21)
    pct = lambda xs, u: 100 * sum(1 for x in xs if x < u) / len(xs) if xs else float('nan')
    print(';'.join([MES[m-1], str(n)] + [f'{st([x[0] for x in d[h]])[0]:.1f}' for h in HORAS] +
                   [f'{st(W21)[0]:.1f}', f'{st(S21)[0]:.1f}', f'{pct(T21,10):.0f}', f'{pct(T21,12):.0f}', f'{pct(T21,14):.0f}', f'{pct(S21,10):.0f}', f'{pct(T22,10):.0f}']))
anios = sorted({fe.year for (fe, h) in obs})
print('# años con datos:', anios[0], '-', anios[-1], '| observaciones usadas:', len(obs))
