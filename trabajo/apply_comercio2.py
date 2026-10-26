import json
from pathlib import Path
P = Path('/home/claude/proyecto/web/data/programa.json'); d = json.loads(P.read_text()); by = {e['id']: e for e in d}
log = []
def rep_text(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1, (eid, old[:50], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    ps[i] = ps[i].replace(old, new, 1)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and not (new.startswith(old) and m[1] <= end): raise SystemExit(f'marca dentro del cambio en {eid} p{i}: {m}')
    e['texto'] = '\n\n'.join(ps); log.append((eid, old, new))
rep_text('5.11-r4', 'Como mucho, 312 millones por año. Es el 5% de los 6.237 millones, si todo se le comprara a comercios de San Isidro y todos cotizaran 5% más caro.',
         'Entre cero y 312 millones por año, según quién gane cada compra. Lo máximo es el 5% de los 6.237 millones, si todo se le comprara a comercios de San Isidro y todos cotizaran 5% más caro.')
o = 'Por cada 10% que bajen en promedio, se usa otro 0,4% de esa parte del presupuesto (5.11).'
rep_text('3.4', o, o + ' Las compras al comercio de San Isidro pueden usar hasta otro 0,4%, unos 312 millones por año, si todas se le hicieran a comercios de acá a un precio 5% más alto (5.11).')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
L = Path('/home/claude/proyecto/CAMBIOS_WEB_COMERCIO.md')
out = [L.read_text().rstrip(), '', '## Segunda vuelta (Nick, 05:29): el costo de las compras es «entre cero y 312 millones», sin tocar el 51,8%', '']
for eid, a, b in log: out += [f'## {eid}', f'- Antes: «{a}»', f'- Después: «{b}»', '']
L.write_text('\n'.join(out)); print(len(log))
