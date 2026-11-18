"""Actualización del 18/11/2026, parte B: lo que encontró la búsqueda de lo viejo después de la parte A.
- Decisión 10: los 60 agentes se cuentan desde marzo de 2026 en el modelo y en el gráfico 13; sale «desde 2028» del 3.3,
  del 5.7 y de las notas del capítulo 3 (el costo anual, unos 1.011 millones, no cambia).
- Decisión 8: el cuadro 14 decía que todas las multas van al fondo de seguridad vial; sale la parte del vecino que avisó.
- Decisión 1: con la votación, en el mes 3 funcionan cuatro partes de la inteligencia artificial del Municipio (cuadro 43).
- 5.7 p1: la oración de la parte A sobre los agentes de tránsito pasa al final del párrafo, para que «esos 60» siga
  justo después de los 60 agentes.
Re-ejecutable sólo una vez: si ya se aplicó, se detiene sin tocar nada.
Uso: python3 trabajo/apply_18nov_b.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if 'desde que empezaron, en marzo de 2026' in by['5.7']['texto']:
    raise SystemExit('ya aplicado: no se toca nada')


def _ps(e): return e['texto'].split('\n\n')


def rep(eid, old, new):
    """Cambia old por new en el único párrafo que lo tiene; corre las marcas que siguen y se niega si toca una."""
    e = by[eid]; ps = _ps(e)
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


def cuadro(eid, old, new):
    cs = by[eid]['cuadros']; idx = [k for k, c in enumerate(cs) if old in c['texto']]
    assert len(idx) == 1 and cs[idx[0]]['texto'].count(old) == 1, (eid, old[:60], idx)
    cs[idx[0]]['texto'] = cs[idx[0]]['texto'].replace(old, new, 1)


rep('5.7', ' La patrulla va a crecer con los agentes de tránsito que pasan a ella, sin sumar empleados al Municipio (punto 1).', '')
rep('5.7', 'las cuentas del capítulo 3 les suman unos 1.011 millones por año desde 2028. No es un gasto de este programa:'
    ' está también en la cuenta de lo que pasa si nada cambia.',
    'las cuentas del capítulo 3 les suman unos 1.011 millones por año desde que empezaron, en marzo de 2026. No es un'
    ' gasto de este programa: está también en la cuenta de lo que pasa si nada cambia. La patrulla va a crecer, además,'
    ' con los agentes de tránsito que pasan a ella, sin sumar empleados al Municipio (punto 1).')
rep('3.3', 'más los 60 agentes que se sumaron a la patrulla en 2026: unos 1.011 millones por año desde 2028 (5.7).',
    'más los 60 agentes que se sumaron a la patrulla en marzo de 2026: unos 1.011 millones por año (5.7).')
rep('metodo-notas-3', 'más los 60 agentes que se sumaron a la patrulla en 2026: unos 1.011 millones por año desde 2028 (5.7).',
    'más los 60 agentes que se sumaron a la patrulla en marzo de 2026: unos 1.011 millones por año (5.7).')
cuadro('3.4', 'Todas las multas que se cobren van a ir a un fondo de seguridad vial, que no se puede usar para otra cosa y tiene'
       ' un renglón propio en el presupuesto.',
       'Todas las multas que se cobren van a ir a un fondo de seguridad vial, que no se puede usar para otra cosa, salvo la'
       ' parte del vecino que avisó la falta (4.11), y tiene un renglón propio en el presupuesto.')
cuadro('6.5', 'Después de las tres primeras partes, la inteligencia artificial del Municipio suma sus funciones nuevas',
       'Después de las cuatro primeras partes, la inteligencia artificial del Municipio suma sus funciones nuevas')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
