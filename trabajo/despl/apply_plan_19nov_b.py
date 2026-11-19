"""Plan de despliegue, 19/11/2026, parte B: arreglos de la revisión r8 con lo que decidió el coordinador.
A. G30: de 57,5 a 465,6 millones por año (antes 62,3 a 504,7: el sueldo pasa a pesos de diciembre de 2025 como el sueldo
   de ingreso de la misma ordenanza), y nadie cobra menos que hoy: si una bonificación de tránsito (moto, grúa) es más
   alta, la conserva (Ley 14.656, artículo 8). G31: también se releva la categoría y las bonificaciones de cada agente que
   pasa.
B. P13 (ordenanza fiscal e impositiva 2029): hoy un baldío paga 26 por mil y una casa 12 (Ordenanza 9415, artículo 2);
   pasa a 4 veces lo de una casa (48 por mil) y a 6 (72) si no está mantenido; los que ya pagan 48 o más siguen igual;
   Pilar y Avellaneda como antecedentes, sin «como ya cobran»; al fondo va lo que se cobra por encima de lo que esos
   terrenos pagan hoy; los declarados en 2028 la pagan desde enero de 2029 y los declarados después, desde que se declaran
   (sin el «desde que se declaran» del principio, que contradecía la nota).
Requiere apply_plan_19nov.py ya aplicado. Si ya se corrió, se detiene.
Uso: python3 apply_plan_19nov_b.py   (después: build.py ../../proyecto/despliegue/acciones.json y gen_revision.py)"""
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()
assert '4 veces la de una casa en un terreno igual' in s or '465,6' in s, 'falta apply_plan_19nov.py'
if '465,6' in s:
    print('ya aplicado'); raise SystemExit


def rep(old, new, cuantas=1):
    global s
    assert s.count(old) == cuantas, (old[:70], s.count(old)); s = s.replace(old, new)


# ---------------------------------------------------------------- A. G30 y G31
rep('''"inspector de tránsito y cobran la bonificación de la función que ocupan (Ordenanza 9422, artículo 17). Suma de 62,3 a 504,7 "
           "millones por año, según cuántos pasan y qué función ocupan (5.7)."),''',
    '''"inspector de tránsito y cobran la bonificación de la función que ocupan (Ordenanza 9422, artículo 17). Suma de 57,5 a 465,6 "
           "millones por año, según cuántos pasan y qué función ocupan (5.7). "
           "Si una bonificación de tránsito que cobran hoy, como la de la moto o la de la grúa, es más alta, la conservan: nadie cobra "
           "menos que hoy (Ley 14.656, artículo 8)."),''')
rep('''    steps="De los 120 agentes de tránsito de hoy, el resto pasa a la patrulla.",''',
    '''    steps=("De los 120 agentes de tránsito de hoy, el resto pasa a la patrulla. "
           "También se relevan la categoría y las bonificaciones que cobra hoy cada agente que pasa: de eso depende lo que suma su sueldo (G30)."),''')

# ---------------------------------------------------------------- B. P13: la tasa de los terrenos sin uso
rep('''     "Tasa más alta para los baldíos, las ruinas y las obras paradas desde que se declaran: 4 veces la de una casa en un terreno igual, "
     "y 6 si no está mantenido, como ya cobran Pilar y Avellaneda. Es la base del recargo a los terrenos sin uso, y lo que cobra de más "
     "va al fondo de la garantía de alquiler (5.4; decisión del 19/11/2026). Los terrenos notificados en 2028 (V09) la pagan desde "
     "enero de 2029, con esta ordenanza."),''',
    '''     "Tasa más alta para los baldíos, las ruinas y las obras paradas con la obligación de construir: hoy un baldío paga 26 por mil "
     "de su valuación y una casa, 12 (Ordenanza 9415, artículo 2); pasa a 4 veces lo de una casa, 48 por mil, y a 6 veces, 72 por mil, "
     "si no está mantenido. Siguen igual los que ya pagan 48 por mil o más, como los inmuebles abandonados. Hay antecedentes en Pilar "
     "(3,7 y 5,6 veces por cada peso de valuación) y Avellaneda (3,8). Es la base del recargo a los terrenos sin uso, y lo que se cobra "
     "por encima de lo que esos terrenos pagan hoy va al fondo de la garantía de alquiler (5.4 y Ordenanza 21, artículo 5; decisión del "
     "19/11/2026). Los terrenos declarados en 2028 (V09) la pagan desde enero de 2029, con esta ordenanza, y los declarados después, "
     "desde que se declaran."),''')

P.write_text(s); print('ok')
