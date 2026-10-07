# [cálculo propio] Frecuencia mensual de días con fenómenos al nivel de los umbrales amarillos del SMN
# (provincia de Buenos Aires: lluvia 40 mm en 12 h; viento 55 km/h o ráfagas 65 km/h), con datos diarios
# NOAA GSOD 2016-2025 de San Fernando Aero (87553) y Aeroparque (87582).
import csv, glob, os, sys, collections
B = sys.argv[1]
KT = 1.852
res = {}
for st, nom in [('87553099999', 'San Fernando Aero'), ('87582099999', 'Aeroparque')]:
    m = collections.defaultdict(lambda: collections.Counter())
    for f in sorted(glob.glob(os.path.join(B, f'gsod_{st}_*.csv'))):
        for r in csv.DictReader(open(f)):
            mes = int(r['DATE'][5:7])
            c = m[mes]; c['dias'] += 1
            p = float(r['PRCP']); pmm = None if p >= 99.9 else p * 25.4
            g = float(r['GUST']); gk = None if g >= 999 else g * KT
            x = float(r['MXSPD']); xk = None if x >= 999 else x * KT
            th = r['FRSHTT'].strip()[4:5] == '1'
            if pmm is not None:
                c['p_ok'] += 1
                c['p1'] += pmm >= 1; c['p10'] += pmm >= 10; c['p20'] += pmm >= 20; c['p40'] += pmm >= 40
            c['tor'] += th
            v = (gk is not None and gk >= 65) or (xk is not None and xk >= 55)
            c['viento'] += v
            amar = (pmm is not None and pmm >= 40) or v
            c['amarillo_obs'] += amar
            c['tor_o_amar'] += amar or (th and pmm is not None and pmm >= 20)
    res[nom] = m
for nom, m in res.items():
    print(f'== {nom}: días por mes (promedio 2016-2025; GSOD) ==')
    print('mes  dias_dato  p>=1mm  p>=10mm  p>=20mm  p>=40mm  tormenta  viento>=umbral  amarillo_obs(p40|viento)  amar_o_(torm+p20)')
    tot = collections.Counter()
    for mes in range(1, 13):
        c = m[mes]; anios = c['dias'] / {1:31,2:28.25,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}[mes]
        dm = {1:31,2:28.25,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}[mes]
        f = lambda k, den='dias': c[k] / c[den] * dm if c[den] else float('nan')
        fp = lambda k: c[k] / c['p_ok'] * dm if c['p_ok'] else float('nan')
        row = [fp('p1'), fp('p10'), fp('p20'), fp('p40'), f('tor'), f('viento'), f('amarillo_obs'), f('tor_o_amar')]
        for i, k in enumerate(['p1','p10','p20','p40','tor','viento','amar','toramar']): tot[k] += row[i]
        print(f'{mes:>3}  {c["dias"]:>5} ({c["p_ok"]:>4} con lluvia)  ' + '  '.join(f'{v:6.1f}' for v in row))
    print('año ' + '  '.join(f'{tot[k]:6.1f}' for k in ['p1','p10','p20','p40','tor','viento','amar','toramar']))
    print()
