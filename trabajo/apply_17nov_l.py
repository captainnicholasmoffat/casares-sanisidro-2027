"""Actualización del 17/11/2026, parte L (revisión completa, al verificar dos hallazgos):
- La nota del capítulo 4 decía que la auditoría externa es el 10% «del equipo de las primeras 49 personas»; los 135,4
  millones del cuadro 28 son el 10% de lo que cobra el equipo entero de 59 personas, sin cargas (Supuestos, E161; cálculo:
  10 × 3,40 + 17 × 2,43 + 17 × 1,50 millones por 13 meses, más 15 pasantes × 240.000 por 12, = 1.353,7 millones).
- El 6.3 (cuadro 41) ocupa las hojas 111 a 113 de la A4, no sólo la 111 (el 6.4 empieza en la 113)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
e = by['metodo-notas-4']; ps = e['texto'].split('\n\n')
old, new = 'es el 10% del equipo de las primeras 49 personas, sin cargas.', 'es el 10% de lo que cobra el equipo de 59 personas, sin cargas.'
i = [k for k, p in enumerate(ps) if old in p]; assert len(i) == 1; i = i[0]
pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
for m in e.get('marcas', {}).get(str(i), []):
    if m[0] >= end: m[0] += delta; m[1] += delta
    elif m[1] > pos: raise SystemExit(f'marca {m}')
ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)
assert by['6.3']['hoja_a4_fin'] == 111 and by['6.4']['hoja_a4'] == 113; by['6.3']['hoja_a4_fin'] = 113
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
