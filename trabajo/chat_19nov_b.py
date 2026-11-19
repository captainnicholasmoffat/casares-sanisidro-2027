"""Chat, 19/11/2026, parte B: arreglos de la revisión r8 con lo que decidió el coordinador. Sólo cambia cómo contesta el chat.
- Regla 12 (patrulla): de 57,5 a 465,6 millones por año (el sueldo pasa a pesos de diciembre de 2025 como el sueldo de
  ingreso de la misma ordenanza); nadie cobra menos que hoy: si una bonificación de tránsito, como la de la moto o la de
  la grúa, es más alta, la conserva.
- Regla 13 (terrenos): San Isidro ya le cobra a un baldío 26 por mil (2,2 veces una casa, que paga 12); con la ordenanza
  de tasas de 2029 pasa a 4 veces lo de una casa (48 por mil) y a 6 (72) si no está mantenido; los que ya pagan 48 o más
  siguen igual; los declarados en 2028 la pagan desde enero de 2029 y los declarados después, desde que se declaran; Pilar
  y Avellaneda, como antecedentes; al fondo va lo que se cobra por encima de lo que esos terrenos pagan hoy.
Se niega a correr dos veces."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/ajustes_chat.json'
a = json.loads(P.read_text())
if any('465,6 millones' in r for r in a['reglas']):
    raise SystemExit('ya aplicado: no se toca nada')
CAMBIOS = [
    ('en total, de 62,3 a 504,7 millones por año, según cuántos pasan y qué función ocupan (5.7).',
     'en total, de 57,5 a 465,6 millones por año, según cuántos pasan y qué función ocupan (5.7). Nadie cobra menos que hoy: '
     'si una bonificación de tránsito que cobra hoy, como la de la moto o la de la grúa, es más alta, la conserva.'),
    ('desde que se declaran, una tasa de 4 veces la de una casa en un terreno igual, y de 6 veces si el terreno no está '
     'mantenido (Pilar ya cobra 3,7 y 5,6 veces, y Avellaneda, 3,8), y, si el dueño no cumple el plazo, sobre ella un recargo',
     'una tasa más alta: San Isidro ya le cobra a un baldío 26 por mil de su valuación, 2,2 veces lo que a una casa, que paga '
     '12, y con la ordenanza de tasas de 2029 pasa a 4 veces lo de una casa por cada peso de valuación, 48 por mil, y a 6 '
     'veces, 72 por mil, si el terreno no está mantenido, salvo los inmuebles que ya pagan 48 por mil o más, como los '
     'abandonados, que siguen igual; los terrenos declarados en 2028 la pagan desde enero de 2029, y los declarados después, '
     'desde que se declaran (hay antecedentes: Pilar le cobra a un baldío 3,7 veces lo de una casa por cada peso de '
     'valuación, y 5,6 si no está mantenido, y Avellaneda les fija a los baldíos una alícuota 3,8 veces la de una casa); '
     'si el dueño no cumple el plazo, sobre esa tasa corre un recargo'),
    ('Lo que se cobra de más va al fondo de la garantía de alquiler; cuánto suma',
     'Lo que se cobra por encima de lo que esos terrenos pagan hoy va al fondo de la garantía de alquiler, y lo que pagan hoy '
     'sigue en las cuentas del Municipio; cuánto suma'),
]
for old, new in CAMBIOS:
    hits = [i for i, r in enumerate(a['reglas']) if old in r]
    assert len(hits) == 1 and a['reglas'][hits[0]].count(old) == 1, old[:60]
    a['reglas'][hits[0]] = a['reglas'][hits[0]].replace(old, new, 1)
P.write_text(json.dumps(a, ensure_ascii=False, indent=2) + '\n'); print('reglas', len(a['reglas']))
