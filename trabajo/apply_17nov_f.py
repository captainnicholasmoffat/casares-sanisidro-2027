"""Actualización del 17/11/2026, parte F: los resúmenes (Qué proponemos hacer, 4.13 y 5.15) suman vivienda, denuncias,
power users y salud mental."""
import json, re
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
def ins(eid, ancla, texto):
    """Inserta texto justo después de ancla; corre las marcas que empiezan después."""
    e = by[eid]; ps = e['texto'].split('\n\n'); hits = [i for i, p in enumerate(ps) if ps[i].count(ancla) == 1]; assert len(hits) == 1, (eid, ancla)
    i = hits[0]; k = ps[i].index(ancla) + len(ancla)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= k: m[0] += len(texto); m[1] += len(texto)
        elif m[1] > k: raise SystemExit(f'marca {eid} p{i} {m}')
    ps[i] = ps[i][:k] + texto + ps[i][k:]; e['texto'] = '\n\n'.join(ps)
ins('proponemos', 'se va a multiplicar por quince.',
    ' Para que los jóvenes puedan quedarse, quien no consigue garantía para alquilar va a tener la del Municipio, y va a haber más lugares para alquilar en las casas que ya existen.')
rep('proponemos', 'Así llegará a la reunión entendiendo de qué se trata.',
    'Así llegará a la reunión entendiendo de qué se trata. Si necesita reclamar o denunciar algo, ella lo va a ayudar a hacerlo. Quien la use para mejorar el Municipio va a cobrar una parte de lo que le haga ganar o ahorrar.')
rep('4.13', 'La va a construir gente de San Isidro, con dinero que ya tiene Ciencia y Técnica.',
    'La va a construir gente de San Isidro, con dinero que ya tiene Ciencia y Técnica. Quien la use para mejorar el Municipio va a cobrar una parte de lo que le haga ganar o ahorrar.')
rep('5.15', 'Las redes las eligen los vecinos de cada zona, y el Municipio paga la conexión de cada casa.',
    'Las redes las eligen los vecinos de cada zona, y el Municipio paga la conexión de cada casa. Para alquilar, una garantía del Municipio, más lugares en las casas que ya existen y terrenos sin uso que se construyen o se venden.')
rep('5.15', 'a la vista, y tomógrafos propios.', 'a la vista, tomógrafos propios y acompañamiento en salud mental cerca de casa.')
rep('5.15', 'todo lo que el Municipio publica se le puede preguntar a su inteligencia artificial.',
    'todo lo que el Municipio publica se le puede preguntar a su inteligencia artificial. Cuando un vecino necesita reclamar o denunciar, ella lo ayuda.')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
for k in ['proponemos', '4.13', '5.15']:
    for p in by[k]['texto'].split('\n\n'):
        s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', re.sub(r'^\d+\. ', '', p)) if x]; f = [x.split()[0].lower() for x in s]
        if any(f.count(w) > 1 for w in f) or any(re.match(r'^(Y|Que)\b', x) for x in s): print('FALLA', k, p[:60], f)
print('ok')
