"""Actualización del 17/11/2026, parte I: «el fondo no queda en rojo» era una metáfora de color para un resultado
fiscal, que el documento no usa; queda «el fondo alcanza»."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); e = [x for x in d if x['id'] == '5.4-r1'][0]
old, new = 'el fondo no queda en rojo aunque deje de pagar', 'el fondo alcanza aunque deje de pagar'
ps = e['texto'].split('\n\n'); i = [k for k, p in enumerate(ps) if old in p]; assert len(i) == 1; i = i[0]
pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
for m in e.get('marcas', {}).get(str(i), []):
    if m[0] >= end: m[0] += delta; m[1] += delta
    elif m[1] > pos: raise SystemExit(f'marca {m}')
ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
