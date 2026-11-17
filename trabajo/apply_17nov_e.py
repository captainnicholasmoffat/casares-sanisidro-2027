"""Actualización del 17/11/2026, parte E: arreglos chicos de redacción después de las partes A a D."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
def rep(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n'); hits = [i for i, p in enumerate(ps) if old in p]; assert len(hits) == 1, (eid, old[:50])
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta: raise SystemExit(f'marca {eid} p{i} {m}')
    ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)
rep('5.7', 'En marzo de 2026 entraron 60 agentes nuevos a la patrulla.', 'Además, en marzo de 2026 entraron 60 agentes nuevos a la patrulla.')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
