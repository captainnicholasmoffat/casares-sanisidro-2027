"""Rehace «orden» (la lista que la web usa para mostrar párrafos, títulos, recuadros, fotos y cuadros) en los apartados
donde ya no coincide con el texto. Desde el 17/11 (202be6a) los scripts que agregaron párrafos no tocaron «orden», y la web
muestra sólo lo que está en «orden»: los párrafos nuevos no se veían y los títulos caían en otro párrafo.
Método: alinea los párrafos de hoy con los de 46c68e2 (última versión coherente) por parecido de texto, en orden; un
párrafo nuevo va detrás del párrafo viejo que lo precede, y antes de los recuadros, fotos y cuadros que seguían a ese
párrafo. Un párrafo nuevo es título (h3) si es corto y no termina en puntuación, como hace la web cuando no hay «orden».
Uso: python3 -I trabajo/orden_18nov.py [--aplicar]   (sin --aplicar sólo muestra)
Re-ejecutable: sólo toca los apartados incoherentes."""
import json, re, subprocess, sys, difflib
from pathlib import Path

R = Path(__file__).resolve().parent.parent
F = R / 'proyecto/web/data/programa.json'
BASE = '46c68e2'
SOLO_CUADROS = {'6.3', '6.4', '6.5'}  # orden de sólo cuadros, a propósito

def parr(e): return e['texto'].split('\n\n')
def coherente(e):
    o = e.get('orden') or []
    if not o or e['id'] in SOLO_CUADROS: return True
    return sorted(x[1] for x in o if x[0] in ('p', 'h3')) == list(range(len(parr(e))))
def titulo(t): return len(t) < 110 and '\n' not in t and not re.search(r'[.:;!?»”)]$', t)
def sim(a, b): return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()

def alinear(viejos, nuevos):
    """m[i_nuevo] = i_viejo o None, monótono."""
    m, j = [], 0
    for t in nuevos:
        best = None
        for k in range(j, min(j + 4, len(viejos))):
            r = sim(t, viejos[k])
            if r >= 0.55 and (best is None or r > best[1]): best = (k, r)
        if best: m.append(best[0]); j = best[0] + 1
        else: m.append(None)
    return m

def rehacer(e, v):
    pv, pn, ov = parr(v), parr(e), v['orden']
    m = alinear(pv, pn)
    tipo_v = {x[1]: x[0] for x in ov if x[0] in ('p', 'h3')}
    # lo que no es texto, colgado del último párrafo viejo que lo precede (-1 = al principio)
    colgado, ult = {}, -1
    for x in ov:
        if x[0] in ('p', 'h3'): ult = x[1]
        else: colgado.setdefault(ult, []).append(x)
    viejo_a_nuevo = {k: i for i, k in enumerate(m) if k is not None}
    out = list(colgado.get(-1, []))
    pend = []  # cosas colgadas de un párrafo viejo, que salen después de los párrafos nuevos que lo siguen
    for i, k in enumerate(m):
        if k is not None:
            out += pend; pend = []
            out.append([tipo_v.get(k, 'p'), i])
            pend = list(colgado.get(k, []))
        else:
            out.append(['h3' if titulo(pn[i]) else 'p', i])
    out += pend
    # cosas colgadas de párrafos viejos que ya no existen
    for k, xs in colgado.items():
        if k != -1 and k not in viejo_a_nuevo: out += xs
    return out, m

viejo = {e['id']: e for e in json.loads(subprocess.run(['git', '-C', str(R), 'show', f'{BASE}:proyecto/web/data/programa.json'],
                                                       capture_output=True, text=True, check=True).stdout)}
d = json.load(open(F, encoding='utf-8'))
cambios = 0
for e in d:
    if coherente(e): continue
    v = viejo.get(e['id'])
    if not v or not v.get('orden'):
        print('SIN BASE', e['id']); continue
    o, m = rehacer(e, v)
    nuevos = [i for i, k in enumerate(m) if k is None]
    print(f"{e['id']}: {len(parr(v))} -> {len(parr(e))} párrafos; nuevos {nuevos}; borrados "
          f"{sorted(set(range(len(parr(v)))) - set(k for k in m if k is not None))}")
    for i in nuevos:
        print('   +', [x[0] for x in o if x[0] in ('p', 'h3') and x[1] == i][0], i, parr(e)[i][:90])
    e['orden'] = o; cambios += 1
    assert coherente(e), e['id']
if '--aplicar' in sys.argv and cambios:
    json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('aplicado en', cambios, 'apartados')
