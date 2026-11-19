"""Plan de despliegue, 19/11/2026: las dos últimas decisiones de Nick (19/11).
A. G29 y G30: los agentes de tránsito que pasan a la patrulla cobran lo mismo que sus compañeros de la patrulla, con el
   presupuesto de Seguridad: de 62,3 a 504,7 millones por año (5.7). G29 ya no dice que conservan su compensación de
   tránsito.
B. P13 (la ordenanza fiscal e impositiva 2029, la acción de la ordenanza de tasas): la tasa de los terrenos sin uso, desde
   que se declaran, es 4 veces la de una casa en un terreno igual, y 6 si no está mantenido, como Pilar y Avellaneda; lo
   que se cobra de más va al fondo de la garantía de alquiler. Nota: los terrenos notificados en 2028 (V09) la pagan desde
   enero de 2029, con esta ordenanza (pendiente para el coordinador en rev/aplicar_19nov/CAMBIOS.md).
Requiere apply_plan_18nov_c.py ya aplicado. Si ya se corrió, se detiene.
Uso: python3 apply_plan_19nov.py   (después: build.py y gen_revision.py)"""
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()
assert 'sólo con el fondo, en el orden en que se reclaman' in s, 'falta apply_plan_18nov_c.py'
if '4 veces la de una casa en un terreno igual' in s:
    print('ya aplicado'); raise SystemExit


def rep(old, new, cuantas=1):
    global s
    assert s.count(old) == cuantas, (old[:70], s.count(old)); s = s.replace(old, new)


# ---------------------------------------------------------------- A. G29 y G30: cobran como sus compañeros
rep('''    steps=("Pasan con el mismo sueldo y conservan su compensación de inspector de tránsito (Ley 14.656, artículo 8). "
           "Formarlos cuesta''',
    '''    steps=("El pase no les baja el sueldo (Ley 14.656, artículo 8): desde que pasan, cobran lo mismo que sus compañeros de la patrulla (G30). "
           "Formarlos cuesta''')
rep('''    steps=("Los agentes de tránsito que quedan ordenan la salida de las escuelas, los accidentes y los cortes, sin parar a nadie para multar. "
           "Se redefinen funciones, no se perdona la ley (Ley 24.449, artículo 2)."))''',
    '''    steps=("Los agentes de tránsito que quedan ordenan la salida de las escuelas, los accidentes y los cortes, sin parar a nadie para multar. "
           "Se redefinen funciones, no se perdona la ley (Ley 24.449, artículo 2). "
           "Los que pasan cobran lo mismo que sus compañeros de la patrulla, con el presupuesto de Seguridad: dejan la compensación de "
           "inspector de tránsito y cobran la bonificación de la función que ocupan (Ordenanza 9422, artículo 17). Suma de 62,3 a 504,7 "
           "millones por año, según cuántos pasan y qué función ocupan (5.7)."),
    note="Decisión del 19/11/2026: cobran lo mismo que sus compañeros de la patrulla.")''')

# ---------------------------------------------------------------- B. P13: la tasa de los terrenos sin uso
rep('''     "Tasa más alta para los baldíos y las obras paradas, como en Bahía Blanca: es la base del recargo a los terrenos sin uso (5.4)."),''',
    '''     "Tasa más alta para los baldíos, las ruinas y las obras paradas desde que se declaran: 4 veces la de una casa en un terreno igual, "
     "y 6 si no está mantenido, como ya cobran Pilar y Avellaneda. Es la base del recargo a los terrenos sin uso, y lo que cobra de más "
     "va al fondo de la garantía de alquiler (5.4; decisión del 19/11/2026). Los terrenos notificados en 2028 (V09) la pagan desde "
     "enero de 2029, con esta ordenanza."),''')

P.write_text(s); print('ok')
