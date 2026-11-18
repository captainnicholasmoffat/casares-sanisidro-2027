"""Modelo fiscal, 18/11/2026, parte B: arreglos de la segunda revisión (scratchpad rev/r6 y rev/r7, HALLAZGOS.md) y
decisiones del coordinador. Sólo notas y dos celdas nuevas: no cambia ningún número que ya estaba.
1. Inspecciones grabadas (E54, E57): de 40 a 100 de los 120 agentes de tránsito pasan a la patrulla en los meses 4 a 6.
   Primera etapa: 108 a 193 agentes, 10,6 a 19,0 M una vez y 51,1 a 96,3 M por año; la patrulla, de 399 a unos 490,
   39,2 a 48,3 M una vez y 180,5 a 222,2 M por año. El modelo sigue con el tope de antes del pase (C54 y C57, 280
   agentes): queda un margen, y no se mueve ninguna cifra que ya usan el texto y el documento.
2. Funciones nuevas de la inteligencia artificial del Municipio en 2028 y 2029 (bloque AH): 14,7 y 65,4 M, cada función
   desde el primer mes de su ventana del cuadro 42, con el mismo método que la fila 317 (decisión 11 del coordinador).
3. La certificación se paga con la partida del mismo año (E324, E328, E332, E336); el comparable son costos directos con
   gestión ambiental y social (E320).
4. RENAPER: validación del DNI y prueba de vida, no «la foto» (B363, E363, E366); tablets (B369, E369); cuadro 28 (E161);
   los 60 agentes empezaron a formarse en marzo de 2026 (B70, Guía C9); qué no entra en el 44,7% (E182).
Se niega a correr dos veces.
Uso: python3 -I trabajo/cuentas_18nov_b.py [ruta del xlsx]   (después: soffice recalcula y extract.py rehace cuentas.json)"""
import copy, sys
from pathlib import Path
import openpyxl

X = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/cuentas/modelo_fiscal.xlsx'
wb = openpyxl.load_workbook(X)
S, G = wb['Supuestos'], wb['Guía']
if any(isinstance(c.value, str) and c.value.startswith('AH · ') for c in S['B']):
    print('ya aplicado'); raise SystemExit


def nota(ws, ref, old, new):
    v = ws[ref].value
    assert isinstance(v, str) and v.count(old) == 1, (ref, old[:60], (v or '')[:120]); ws[ref] = v.replace(old, new, 1)


# ---------------------------------------------------------------- 1. inspecciones grabadas, con el pase de agentes
nota(S, 'E54', 'de 20,5 a 27,5 M para la primera etapa completa, 208 a 280 agentes (inspectores de comercio y de la Agencia de '
     'Control, los de Habilitaciones y de Obras Particulares que salen a inspeccionar, y agentes de tránsito), más 9,5 M por '
     'cada base de descarga (tránsito tiene 2); se toma el tope: 27,5 + 19.',
     'de 10,6 a 19,0 M para la primera etapa completa, 108 a 193 agentes (88 a 113 inspectores de comercio y de la Agencia '
     'de Control, de Habilitaciones y de Obras Particulares que salen a inspeccionar, y los 20 a 80 agentes que quedan en '
     'tránsito, porque de los 120 pasan de 40 a 100 a la patrulla en los meses 4 a 6), a 98.327 pesos por agente, más 9,5 M '
     'por cada base de descarga (tránsito tiene 2). En el modelo queda el tope de antes del pase, 27,5 + 19 (280 agentes): '
     'un margen de 8,5 M.')
nota(S, 'E54', 'La patrulla, en la segunda etapa (de 359 a unos 390 agentes: 35,3 a 38,4 M una vez y 162,4 a 176,9 M por año), '
     'no está sumada',
     'La patrulla, en la segunda etapa (de 359 a unos 390 agentes, más los 40 a 100 que pasan de tránsito: de 399 a unos 490, '
     '39,2 a 48,3 M una vez y 180,5 a 222,2 M por año), no está sumada')
nota(S, 'E57', 'de 107,6 a 145,5 M por año en régimen para la primera etapa completa,',
     'de 51,1 a 96,3 M por año en régimen para la primera etapa completa (108 a 193 agentes, fila 54: 452.463 pesos por año '
     'el inspector y 564.952 el agente de tránsito),')
nota(S, 'E57', 'se toman los topes: 145,5 + 23.',
     'el modelo sigue con los topes de antes del pase de agentes de tránsito a la patrulla, 145,5 + 23: queda un margen de '
     '49,2 M por año.')

# ---------------------------------------------------------------- 2. funciones nuevas en 2028 y 2029 (bloque AH)
EST = {'h': S['B308'], 'b': S['B317'], 'n': S['C317'], 'e': S['E317']}
r = S.max_row + 2
assert r == 375, r


def fila(b, c=None, e=None, h=False):
    global r
    S.cell(r, 2, b)._style = copy.copy(EST['h' if h else 'b']._style)
    if c is not None:
        S.cell(r, 3, c)._style = copy.copy(EST['n']._style)
    if e is not None:
        S.cell(r, 5, e)._style = copy.copy(EST['e']._style)
    r += 1
    return r - 1


fila('AH · FUNCIONES NUEVAS DE LA INTELIGENCIA ARTIFICIAL DEL MUNICIPIO: LO QUE SUMAN EN 2028 Y 2029 (4.11)', h=True)
f28 = fila('Las seis funciones en 2028, en pesos, con 15% de contingencia',
           '=ROUND((C310*8/12+C312*8/12+C311*7/12+C315*7/12+C314*2/12)*(1+0.15)*Supuestos!$C$289,-5)',
           'Mismo método que la fila 317, con cada función desde el primer mes de su ventana (cuadro 42): las denuncias y las '
           'historias desde el mes 6, ocho meses de 2028; los power users y los contratos de alquiler desde el mes 7, siete '
           'meses; la conversación de salud mental desde el mes 12, dos meses. La consulta de lugares empieza en 2029. 14,7 M')
f29 = fila('Las seis funciones en 2029, en pesos, con 15% de contingencia',
           '=ROUND((C310+C311+C312+C314+C315+C313*8/12)*(1+0.15)*Supuestos!$C$289,-5)',
           'Todas el año entero, salvo la consulta de lugares, desde el mes 18: ocho meses de 2029. Desde 2030, la fila 317. 65,4 M')
nota(S, 'E317', 'El primer año (2028) suma menos: cada función empieza en su fecha',
     f'El primer año (2028) suma menos: cada función empieza en su fecha (14,7 M en 2028 y 65,4 M en 2029, filas {f28} y {f29})')

# ---------------------------------------------------------------- 3. la certificación
nota(S, 'E320', 'contra 230.600 mil de costos directos (obras).',
     'contra 230.600 mil de costos directos (obras y gestión ambiental y social).')
for ref in ('E324', 'E328', 'E332', 'E336'):
    nota(S, ref, 'Se paga cuando se certifica, hacia marzo del año siguiente',
         'Se paga con la partida del mismo año, aunque se certifique hacia marzo del siguiente')

# ---------------------------------------------------------------- 4. RENAPER, tablets, cuadro 28, los 60 agentes, el 44,7%
nota(S, 'B363', 'prueba de vida pasiva (la foto), por persona', 'prueba de vida pasiva, por persona')
nota(S, 'E363', 'Mismo cuadro tarifario, ítem 14: 70 pesos',
     'Mismo cuadro tarifario, ítem 14: 70 pesos. El cuadro no le pone precio a una validación por foto de rostro: el programa '
     'usa la validación del DNI y la prueba de vida')
nota(S, 'E366', 'se toma la tarifa entera', 'se toma la tarifa entera (la reducida es sólo para la Administración Pública '
     'Nacional, ítems 16 a 19)')
nota(S, 'B369', 'una por asamblea y una por delegación', 'una por asamblea y una en la delegación de cada zona')
nota(S, 'E369', 'Supuesto: seis asambleas a la vez, una por zona, y seis delegaciones.',
     'Supuesto: seis asambleas a la vez, una por zona, y una delegación por zona (de las once sedes: nueve delegaciones y dos '
     'subdelegaciones).')
nota(S, 'E161', 'infraestructura y licencias 243,5 M (cálculo propio', 'infraestructura y licencias 318,7 M: 243,5 M de antes (cálculo propio')
nota(S, 'E161', 'usadas enteras, las 160 asociaciones suman hasta 66 M más);',
     'usadas enteras, las 160 asociaciones suman hasta 66 M más), 70,7 M de las funciones nuevas (fila 317) y 4,5 M de la '
     'votación (fila 373);')
nota(S, 'E161', ' Desde el 18/11/2026 suma el uso de las seis funciones nuevas de la inteligencia artificial del Municipio '
     '(fila 317) y la votación con el RENAPER y las tablets (fila 373).', '')
nota(S, 'B70', 'los 60 agentes que se sumaron a la patrulla en marzo de 2026',
     'los 60 agentes que empezaron a formarse para la patrulla en marzo de 2026')
nota(G, 'C9', 'los 60 agentes que se sumaron a la patrulla en marzo de 2026',
     'los 60 agentes que empezaron a formarse para la patrulla en marzo de 2026')
nota(S, 'E182', 'La plataforma y el semillero se pagan dentro de Ciencia y Técnica',
     'La plataforma y el semillero se pagan dentro de Ciencia y Técnica. No entran: la formación de los agentes de tránsito '
     'que pasan a la patrulla, que paga Seguridad (filas 345 y 346), y lo que se deja de cobrar en multas, que no se puede '
     'calcular (5.7 y 5.11)')

wb.save(X)
print('ok · funciones nuevas en 2028 y 2029: filas', f28, f29)
