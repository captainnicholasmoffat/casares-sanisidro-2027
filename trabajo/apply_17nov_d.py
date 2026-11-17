"""Actualización del 17/11/2026, parte D: las cifras que cambian porque la patrulla queda estable en la cantidad de
agentes que haya al asumir (trabajo/cuentas_agentes.py: 1.011 millones más de personal por año desde 2028)."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}

def rep(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]; assert len(hits) == 1, (eid, old[:50], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)

def cuadro(eid, old, new, ci=None):
    cs = by[eid]['cuadros']; idx = [i for i, c in enumerate(cs) if old in c['texto']] if ci is None else [ci]
    assert len(idx) == 1 and cs[idx[0]]['texto'].count(old) == 1, (eid, old[:60], idx)
    cs[idx[0]]['texto'] = cs[idx[0]]['texto'].replace(old, new, 1)

cuadro('3.6', 'Si nada cambia | 1.576 | 4.347 | 7.233 | 10.236', 'Si nada cambia | 565 | 3.336 | 6.222 | 9.225')
cuadro('3.6', 'Con este programa, pagado con la tabla nueva | 1.576 | 5.585 | 7.751 | 10.236', 'Con este programa, pagado con la tabla nueva | 565 | 4.574 | 6.739 | 9.225')
for ci, c in enumerate(by['3.6']['cuadros']):
    if c['texto'].count('Si nada cambia, ese año sobran 10.236 millones.') == 1:
        c['texto'] = c['texto'].replace('Si nada cambia, ese año sobran 10.236 millones.', 'Si nada cambia, ese año sobran 9.225 millones.')
rep('3.6', 'las cuentas de 2031 quedarían prácticamente en cero: faltarían 426 millones.', 'las cuentas de 2031 quedarían en déficit: faltarían 1.437 millones.')
rep('3.2-r2', 'en 2031 sobran 5.342 millones, en lugar de 10.236.', 'en 2031 sobran 4.331 millones, en lugar de 9.225.')
rep('3.2-r2', 'en lugar de sobrar 10.236 millones,', 'en lugar de sobrar 9.225 millones,')
rep('3.2-r2', 'faltan 3.044 millones.', 'faltan 4.055 millones.')
cuadro('6.6', 'las cuentas de 2028 cierran igual que en ese caso: sobran 1.576 millones.', 'las cuentas de 2028 cierran igual que en ese caso: sobran 565 millones.')
cuadro('6.6', 'las cuentas de 2031 quedarían casi en cero: faltarían 426 millones (3.6).', 'las cuentas de 2031 quedarían en déficit: faltarían 1.437 millones (3.6).')
cuadro('6.6', 'lo que sobra en 2031 baja de 10.236 a 5.342 millones.', 'lo que sobra en 2031 baja de 9.225 a 4.331 millones.')
rep('5.7', 'Sobre todo eso decide el intendente, y ahí se gastaron esos 32.446 millones.',
    'Sobre todo eso decide el intendente, y ahí se gastaron esos 32.446 millones. En marzo de 2026 entraron 60 agentes nuevos a la patrulla. Este programa mantiene la cantidad de agentes que haya al asumir, y eso suma unos 1.011 millones por año a las cuentas desde 2028.')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
p = by['5.7']['texto'].split('\n\n')[1]
s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', p) if x]; f = [x.split()[0].lower() for x in s]
print('5.7 p1:', f, 'REPETIDA' if any(f.count(w) > 1 for w in f) else 'ok')
