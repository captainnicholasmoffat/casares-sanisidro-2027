"""Modelo fiscal, 19/11/2026: decisión A de Nick (19/11). Los agentes de tránsito que pasan a la patrulla (de 40 a 100, en
los meses 4 a 6; cuántos lo fija el relevamiento) cobran lo mismo que sus compañeros de la patrulla, con el presupuesto de
Seguridad. Bloque AI nuevo: el mínimo (40 agentes con la bonificación de la Patrulla Municipal, 62,3 M por año) y el máximo
(100 con esa y la del Cuerpo de Patrulla a pie, 504,7 M por año), y lo de 2028 si pasan en el mes 4 (marzo).
Como todo lo que un área paga con su presupuesto (filas 228, 240, 260 y 273), entra en el gasto flexible ocupado: el
mínimo en la fila 180 y lo que va del mínimo al máximo en el peor caso (fila 182). No cambia ningún flujo ni el resultado.
Notas al día: filas 357 a 359 (ya no es una opción), 346 (la formación), 180 a 182, 257 y 270 (el 44,1%), y la Guía (C12).
Se niega a correr dos veces.
Uso: python3 -I trabajo/cuentas_19nov.py [ruta del xlsx]   (después: recalc.py de la skill xlsx y extract.py)"""
import copy, sys
from pathlib import Path
import openpyxl

X = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/cuentas/modelo_fiscal.xlsx'
wb = openpyxl.load_workbook(X)
S, G = wb['Supuestos'], wb['Guía']
if any(isinstance(c.value, str) and c.value.startswith('AI · ') for c in S['B']):
    print('ya aplicado'); raise SystemExit


def nota(ws, ref, old, new):
    v = ws[ref].value
    assert isinstance(v, str) and v.count(old) == 1, (ref, old[:60], (v or '')[:120]); ws[ref] = v.replace(old, new, 1)


def formula(ref, old, new):
    v = S[ref].value
    assert isinstance(v, str) and v.count(old) == 1, (ref, v); S[ref] = v.replace(old, new, 1)


EST = {'h': S['B361'], 'b': S['B371'], 'dato': S['C369'], 'f': S['C371'], 'e': S['E371']}
r = S.max_row + 2
assert r == 379, r


def fila(b, c=None, e=None, h=False, dato=False):
    global r
    S.cell(r, 2, b)._style = copy.copy(EST['h' if h else 'b']._style)
    if c is not None:
        S.cell(r, 3, c)._style = copy.copy(EST['dato' if dato else 'f']._style)
    if e is not None:
        S.cell(r, 5, e)._style = copy.copy(EST['e']._style)
    r += 1
    return r - 1


fila('AI · AGENTES DE TRÁNSITO QUE PASAN A LA PATRULLA: COBRAN LO MISMO QUE SUS COMPAÑEROS (5.7)', h=True)
mn = fila('Agentes que pasan, el mínimo', 40, 'Lo fija el relevamiento de lo que hace falta para ordenar el tránsito (acción G31 del '
          'plan): de 40 a 100 de los 120 (5.7)', dato=True)
mx = fila('Agentes que pasan, el máximo', 100, 'Mismo relevamiento', dato=True)
amin = fila('Lo que suma por año, el mínimo: el mínimo de agentes, con la bonificación de la Patrulla Municipal',
            f'=C{mn}*C358',
            'Decisión de Nick del 19/11/2026: cobran lo mismo que sus compañeros de la patrulla, con el presupuesto de Seguridad. '
            'Dejan la compensación de inspector de tránsito (fila 354) y cobran la bonificación de la función que ocupan (fila 355). '
            '62,3 M. Como lo que pagan otras áreas con su presupuesto (filas 228, 240, 260 y 273), entra en el gasto flexible '
            'ocupado (fila 180): no cambia el gasto total ni el resultado')
amax = fila('Lo que suma por año, el máximo: el máximo de agentes, con la de la Patrulla Municipal y la del Cuerpo de Patrulla a pie',
            f'=C{mx}*C359',
            '504,7 M, si las dos bonificaciones se suman: la ordenanza no lo dice (fila 356). Lo que va del mínimo al máximo entra '
            'en el peor caso (fila 182). Depende de cuántos pasan, de la función de cada uno y de los montos que fije cada año la '
            'ordenanza de presupuesto (hoy, los de 2026)')
mes = fila('Meses de 2028 con la diferencia, si pasan en el mes 4', 10,
           'El mes 4 del mandato es marzo de 2028 (el mes 1 es diciembre de 2027, como en la fila 376). Pasan en los meses 4 a 6 '
           '(acciones G29 y G30 del plan): se toma el primero. Durante los dos meses del curso cobrarían la compensación del '
           'aspirante a la patrulla, 152.779 módulos por mes (Ordenanza 9422, artículo 17), que queda entre las dos bonificaciones',
           dato=True)
a28min = fila('En 2028, el mínimo', f'=ROUND(C{amin}*C{mes}/12,-5)', '51,9 M')
a28max = fila('En 2028, el máximo', f'=ROUND(C{amax}*C{mes}/12,-5)', '420,6 M. Desde 2029, el año entero (filas '
              f'{amin} y {amax})')

# ---------------------------------------------------------------- el gasto flexible: el mínimo ocupa, el resto es peor caso
formula('C180', '+C281-C296)', f'+C281+C{amin}-C296)')
formula('C182', '+C339)/C128', f'+C339+C{amax}-C{amin})/C128')
nota(S, 'E180', 'espectáculos de Cultura y obra vecinal,',
     f'espectáculos de Cultura, lo que suma el sueldo de los agentes de tránsito que pasan a la patrulla, el mínimo (fila {amin}), '
     'y obra vecinal,')
nota(S, 'E180', 'el 51,8% del documento', 'el 51,9% del documento')
nota(S, 'E181', 'El 48,2%', 'El 48,1%')
nota(S, 'E182', 'El 44,7%: el peor caso,', 'El 44,1%: el peor caso,')
nota(S, 'E182', 'lo que falta para la certificación del escalón del año 4 (fila 339).',
     'lo que falta para la certificación del escalón del año 4 (fila 339) y el sueldo de los agentes de tránsito que pasan a '
     f'la patrulla en el máximo, en lugar del mínimo (filas {amax} y {amin}).')
nota(S, 'E182', 'que paga Seguridad (filas 345 y 346)', 'que paga Seguridad con el programa 47.01, que ya existe (filas 345 y 346)')
nota(S, 'E257', 'el gasto flexible libre no cambia (44,7%)', 'el gasto flexible libre no cambia (44,1%)')
nota(S, 'E270', 'puntos del margen libre (44,7%)', 'puntos del margen libre (44,1%)')

# ---------------------------------------------------------------- notas que decían «opción, no decidida»
nota(S, 'E357', 'Es lo decidido (sueldos iguales): la Ley 14.656, artículo 8, no permite que el pase lo afecte materialmente, y no lo afecta',
     'Ya no es lo decidido: desde el 19/11/2026 cobran lo mismo que sus compañeros de la patrulla (bloque AI). La Ley 14.656, '
     'artículo 8, sólo pide que el pase no lo afecte materialmente')
nota(S, 'E358', 'Opción, no decidida', f'Lo decidido el 19/11/2026, en el mínimo (fila {amin})')
nota(S, 'E359', 'Opción, no decidida. Con 40 agentes, por 40; con 100, por 100',
     f'El máximo de lo decidido el 19/11/2026 (fila {amax}), si las dos bonificaciones se suman')
nota(S, 'E346', 'Lo paga el presupuesto de Seguridad y no entra en el resultado hasta que se decida',
     'Lo paga el presupuesto de Seguridad, con el programa 47.01, que ya forma a quienes entran a la patrulla: no entra en el '
     'resultado ni en el gasto flexible ocupado')

# ---------------------------------------------------------------- Guía: lo que se reasigna
nota(G, 'C12', 'las clases de la costa —23,5 M por año, de Deportes—,',
     'las clases de la costa —23,5 M por año, de Deportes—, el sueldo de los agentes de tránsito que pasan a la patrulla —de '
     '62,3 a 504,7 M por año, de Seguridad—,')

wb.save(X)
print('ok · bloque AI, filas', mn, 'a', a28max)
