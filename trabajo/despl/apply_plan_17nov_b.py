"""Plan de despliegue, 17/11/2026, parte B: pasa a acciones_def.py las acciones que se habían sumado directo en
acciones.json (C61 a C68, Ordenanzas 17 y 18, y E42), para que build.py vuelva a armar todo el plan desde una sola
fuente; suma las Ordenanzas 20 y 21 a la revisión legal."""
import json
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()
dep = {x['code']: x for x in json.loads((H.parents[1] / 'proyecto/despliegue/acciones.json').read_text())}

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]; s = s.replace(old, new, 1)

rep('act("C24", "Revisión legal de las nueve ordenanzas que faltan: la 2, la 4, la 6, la 8, la 10, la 11, la 12, la 13 y la 14",',
    'act("C24", "Revisión legal de las trece ordenanzas que faltan: la 2, la 4, la 6, la 8, la 10, la 11, la 12, la 13, la 14, la 17, la 18, la 20 y la 21",')
rep('act("V06", "Presentar la Ordenanza 20 (garantía de alquiler) y la 21 (viviendas en el lote y terrenos sin uso)", "Intendente",\n    ms=True, needs=["T07"], win=W(4, 6), fuente="6.4")',
    'act("V06", "Presentar la Ordenanza 20 (garantía de alquiler) y la 21 (viviendas en el lote y terrenos sin uso)", "Intendente",\n    ms=True, needs=["C24"], win=W(4, 6), fuente="6.4")')

def lit(v): return json.dumps(v, ensure_ascii=False)
out = ['\n# ---------------------------------------------------------------- Ordenanzas 17 y 18 y la partida de empleo (antes sólo en acciones.json)']
for c in ['C61', 'C62', 'C63', 'C64', 'C65', 'C66', 'C67', 'C68', 'E42']:
    x = dep[c]; kw = []
    needs = [n['code'] for n in x['needs']]
    if x['milestone']: kw.append('ms=True')
    else: kw.append(f"dur={x['dur']}, est=True" if 'estimada' in x['note'] else f"dur={x['dur']}")
    kw.append(f'needs={lit(needs)}')
    if c in ('C61', 'C64'): kw.append('win=W(4, 6)')
    if c == 'E42': kw.append('sne=D(2030, 1, 1)')
    if x['decision']: kw.append(f"decision={lit(x['decision'])}")
    if x['steps']: kw.append(f"steps={lit(x['steps'])}")
    nota = x['note']
    if nota and not nota.startswith('Calendario del programa'): kw.append(f'note={lit(nota)}')
    kw.append(f"fuente={lit(x['fuente'])}")
    out.append(f'act({lit(c)}, {lit(x["task"])}, {lit(x["owner"])},\n    ' + ', '.join(kw) + ')')
s += '\n'.join(out) + '\n'
P.write_text(s); print('ok')

