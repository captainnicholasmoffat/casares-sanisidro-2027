"""Chat, 19/11/2026: las dos últimas decisiones de Nick (19/11). Sólo cambia cómo contesta el chat.
- Regla 12 (patrulla): quien pasa de tránsito a la patrulla cobra lo mismo que sus compañeros, con el presupuesto de
  Seguridad: de 62,3 a 504,7 millones por año en total (5.7).
- Regla 13 (terrenos): la tasa, desde que se declara, es 4 veces la de una casa en un terreno igual, y 6 si no está
  mantenido (Pilar y Avellaneda); el recargo va encima; lo que se cobra de más va al fondo de la garantía de alquiler; cuánto
  suma se va a saber con el registro de terrenos del primer año (5.4-r3 y Ordenanza 21, artículo 5).
Se niega a correr dos veces."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/ajustes_chat.json'
a = json.loads(P.read_text())
if any('4 veces la de una casa' in r for r in a['reglas']):
    raise SystemExit('ya aplicado: no se toca nada')
CAMBIOS = [
    ('y el resto pasa a la patrulla, con formación.',
     'y el resto pasa a la patrulla, con formación. Quien pasa cobra lo mismo que sus compañeros de la patrulla, con el '
     'presupuesto de Seguridad: en total, de 62,3 a 504,7 millones por año, según cuántos pasan y qué función ocupan (5.7).'),
    ('una tasa más alta para esos terrenos desde que se declaran, como en Bahía Blanca, y, si el dueño no cumple el plazo, '
     'sobre ella un recargo',
     'desde que se declaran, una tasa de 4 veces la de una casa en un terreno igual, y de 6 veces si el terreno no está '
     'mantenido (Pilar ya cobra 3,7 y 5,6 veces, y Avellaneda, 3,8), y, si el dueño no cumple el plazo, sobre ella un recargo'),
    ('y la tasa más alta y el recargo siguen corriendo (5.4 y Ordenanza 21).',
     'y la tasa más alta y el recargo siguen corriendo. Lo que se cobra de más va al fondo de la garantía de alquiler; '
     'cuánto suma se va a saber con el registro de terrenos del primer año, y no des un número (5.4 y Ordenanza 21).'),
]
for old, new in CAMBIOS:
    hits = [i for i, r in enumerate(a['reglas']) if old in r]
    assert len(hits) == 1 and a['reglas'][hits[0]].count(old) == 1, old[:60]
    a['reglas'][hits[0]] = a['reglas'][hits[0]].replace(old, new, 1)
P.write_text(json.dumps(a, ensure_ascii=False, indent=2) + '\n'); print('reglas', len(a['reglas']))
