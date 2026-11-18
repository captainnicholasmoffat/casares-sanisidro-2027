"""Chat, 18/11/2026, parte D: arreglos de la segunda revisión (scratchpad rev/r6/HALLAZGOS.md) y decisiones del
coordinador. Sólo cambia cómo contesta el chat.
- Regla 11: dos oraciones empezaban con «Si». Regla 12: dos empezaban con «No».
- Regla 13 (terrenos): vender no es cumplir, el que compra hereda el plazo; la tasa más alta corre desde que se declara,
  y el recargo, si el dueño no cumple el plazo (5.4-r3 y Ordenanza 21, artículo 5).
- Regla 14 (acompañantes): nadie queda liberado hasta el mes 27 (5.3); la tecnicatura pide el secundario completo, que se
  termina gratis con el Plan FinEs; el resumen de la conversación de salud mental va sólo al profesional hasta que hay
  acompañantes (mes 37), y desde entonces también al acompañante (5.6).
Se niega a correr dos veces."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/ajustes_chat.json'
a = json.loads(P.read_text())
if any('sólo al profesional hasta que hay acompañantes' in r for r in a['reglas']):
    raise SystemExit('ya aplicado: no se toca nada')
CAMBIOS = [
    ('Si preguntan si la inteligencia artificial del Municipio opina o recomienda qué votar,',
     'Cuando preguntan si la inteligencia artificial del Municipio opina o recomienda qué votar,'),
    ('No se retiene un vehículo por una falta menor:', 'Ningún vehículo se retiene por una falta menor:'),
    ('tres años para empezar a construir o vender; una tasa más alta para esos terrenos, como en Bahía Blanca, y sobre ella '
     'un recargo',
     'tres años para empezar a construir (si lo vende, el que compra hereda el tiempo que quedaba); una tasa más alta para '
     'esos terrenos desde que se declaran, como en Bahía Blanca, y, si el dueño no cumple el plazo, sobre ella un recargo'),
    ('el primer año nadie queda liberado, y el trabajo de todos los días lo sigue haciendo el personal actual hasta el mes 27.',
     'hasta el mes 27 nadie queda liberado, y el trabajo de todos los días lo sigue haciendo el personal actual (5.3).'),
    ('durante un año lectivo en un instituto superior público, y empieza a acompañar cerca del mes 37.',
     'durante un año lectivo en un instituto superior público (hace falta el secundario completo, que se puede terminar '
     'gratis con el Plan FinEs), y empieza a acompañar cerca del mes 37. La conversación de salud mental de la '
     'inteligencia artificial del Municipio, con permiso del vecino, le pasa un resumen sólo al profesional hasta que hay '
     'acompañantes formados; desde el mes 37, también a su acompañante (5.6).'),
]
for old, new in CAMBIOS:
    hits = [i for i, r in enumerate(a['reglas']) if old in r]
    assert len(hits) == 1 and a['reglas'][hits[0]].count(old) == 1, old[:60]
    a['reglas'][hits[0]] = a['reglas'][hits[0]].replace(old, new, 1)
P.write_text(json.dumps(a, ensure_ascii=False, indent=2) + '\n'); print('reglas', len(a['reglas']))
