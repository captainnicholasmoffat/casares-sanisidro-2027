"""Rama del PDF, 18/11/2026 (decisión 10 de Nick): los 60 agentes de la patrulla se cuentan desde marzo de 2026.
Sólo datos: suma a los gastos corrientes de 2026 (diez meses, 842,8 M) y de 2027 (1.011,4 M) de los tres escenarios de
data/modelo_flujo_caja.csv, y baja en lo mismo el ahorro corriente y el resultado. Corrige también la nota del CSV y la
de data/parametros_modelo.csv. No toca el código (03_scripts/modelo.py sigue sumándolos desde 2028: ver PENDIENTES).
Re-ejecutable: si 2026 ya lleva a los agentes, no hace nada.
Uso: python3 -I trabajo/pdf_agentes_18nov.py [carpeta de la rama del PDF]"""
import csv, io, sys
from decimal import Decimal
from pathlib import Path

R = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/pdf-sanisidro')
F, P = R / 'data/modelo_flujo_caja.csv', R / 'data/parametros_modelo.csv'
ANUAL = Decimal('1011395066')
SUMA = {2026: ANUAL * 10 / 12, 2027: ANUAL}
BASE_2026 = Decimal('251403592133.29')  # gastos corrientes de 2026 sin los agentes (los mismos de 2025)

txt = open(F, encoding='utf-8', newline='').read()  # los datos van con CRLF y los comentarios con LF
com = [l for l in txt.splitlines(keepends=True) if l.startswith('#')]
datos = ''.join(l for l in txt.splitlines(keepends=True) if not l.startswith('#'))
filas = list(csv.DictReader(io.StringIO(datos)))
r26 = [x for x in filas if x['anio'] == '2026']
if any(Decimal(x['gastos_corrientes']) != BASE_2026 for x in r26):
    print('ya aplicado'); raise SystemExit
for x in filas:
    a = int(x['anio'])
    if a in SUMA:
        s = SUMA[a]
        for k in ('gastos_corrientes', 'gastos_totales'):
            x[k] = f"{(Decimal(x[k]) + s).quantize(Decimal('0.01'))}"
        for k in ('ahorro_corriente', 'resultado_financiero'):
            x[k] = f"{(Decimal(x[k]) - s).quantize(Decimal('0.01'))}"
viejo = ['# Desde 2028 los gastos corrientes de todos los escenarios llevan\n',
         '# el personal de los 60 agentes de seguridad de marzo de 2026\n',
         '# (data/parametros_modelo.csv, personal_seguridad_agentes_2026).\n']
nuevo = ['# Desde marzo de 2026 los gastos corrientes de todos los escenarios\n',
         '# llevan el personal de los 60 agentes de seguridad que entraron ese\n',
         '# mes: 842,8 millones en 2026 (diez meses) y 1.011,4 por anio desde\n',
         '# 2027 (data/parametros_modelo.csv, personal_seguridad_agentes_2026).\n']
i = com.index(viejo[0])
assert com[i:i + 3] == viejo, com[i:i + 3]
com[i:i + 3] = nuevo
out = io.StringIO()
w = csv.DictWriter(out, fieldnames=list(filas[0].keys()), lineterminator='\r\n')
w.writeheader(); w.writerows(filas)
open(F, 'w', encoding='utf-8', newline='').write(''.join(com) + out.getvalue())

p = open(P, encoding='utf-8', newline='').read()
old = 'los agentes de marzo de 2026, fuera de la base 2025; personal desde 2028'
assert p.count(old) == 1
open(P, 'w', encoding='utf-8', newline='').write(p.replace(old, 'los agentes de marzo de 2026, fuera de la base 2025; personal desde marzo de 2026 '
                            '(en 2026, diez meses: 842829222)'))
for x in filas:
    if x['anio'] in ('2026', '2027'):
        print(x['escenario'], x['anio'], 'resultado', round(float(x['resultado_financiero']) / 1e6, 1), 'M')
