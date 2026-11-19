"""Modelo fiscal, 19/11/2026, parte B: arreglo de la revisión r8 (hallazgo 3), decidido por el coordinador.
El sueldo de los agentes de tránsito que pasan a la patrulla pasa a pesos de diciembre de 2025 con el mismo factor que el
sueldo de ingreso de la misma ordenanza (fila 321: 432.624 pesos del presupuesto 2026 son 420.507 de diciembre de 2025).
Antes se subía con el IPC de noviembre y diciembre de 2025 (×1,025×1,028), el paso de los créditos presupuestarios (filas
304 y 344), y el sueldo de la fila 321 se bajaba: los dos módulos de la Ordenanza 9422 iban en sentidos opuestos.
Resultado: 1,44 y 4,66 M por agente y por año (antes 1,56 y 5,05); 57,5 y 465,6 M por año (antes 62,3 y 504,7); en 2028,
47,9 y 388,0 M (antes 51,9 y 420,6). El gasto flexible sigue en 51,9% ocupado, 48,1% libre y 44,1% en el peor caso
(44,13% en lugar de 44,08%).
Se niega a correr dos veces.
Uso: python3 -I trabajo/cuentas_19nov_b.py [ruta del xlsx]   (después: recalc.py de la skill xlsx y extract.py)"""
import sys
from pathlib import Path
import openpyxl

X = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/cuentas/modelo_fiscal.xlsx'
wb = openpyxl.load_workbook(X)
S, G = wb['Supuestos'], wb['Guía']
if 'C321/432624' in str(S['C358'].value):
    print('ya aplicado'); raise SystemExit
assert S['C321'].value == 420507 and 'Sueldo de ingreso municipal' in S['B321'].value, S['B321'].value


def nota(ws, ref, old, new):
    v = ws[ref].value
    assert isinstance(v, str) and v.count(old) == 1, (ref, old[:60], (v or '')[:120]); ws[ref] = v.replace(old, new, 1)


def formula(ref, old, new):
    v = S[ref].value
    assert isinstance(v, str) and v.count(old) == 1, (ref, v); S[ref] = v.replace(old, new, 1)


# ---------------------------------------------------------------- el factor de la fila 321, no el IPC de los créditos
formula('C358', '*1.025*1.028', '*C321/432624')
formula('C359', '*1.025*1.028', '*C321/432624')
nota(S, 'E358', 'a pesos de diciembre de 2025.',
     'a pesos de diciembre de 2025 como la fila 321: el sueldo de ingreso y las bonificaciones son módulos de la misma '
     'ordenanza (fila 354), y 432.624 módulos del presupuesto 2026 son 420.507 pesos de diciembre de 2025. 1,44 M.')
nota(S, 'E359', 'si las dos bonificaciones se suman', 'si las dos bonificaciones se suman. Mismo paso a pesos que la fila 358. 4,66 M')

# ---------------------------------------------------------------- las cifras escritas en las notas
nota(S, 'E382', '62,3 M.', '57,5 M.')
nota(S, 'E382', 'cobran la bonificación de la función que ocupan (fila 355).',
     'cobran la bonificación de la función que ocupan (fila 355). Si una compensación de tránsito que cobra hoy, como la '
     'de conductor de moto o la de la grúa, es más alta, la conserva: nadie cobra menos que hoy (Ley 14.656, artículo 8). '
     'Con esos agentes el costo baja: el cálculo supone que hoy todos cobran sólo la compensación de inspector.')
nota(S, 'E383', '504,7 M,', '465,6 M,')
nota(S, 'E385', '51,9 M', '47,9 M')
nota(S, 'E386', '420,6 M.', '388,0 M.')
nota(G, 'C12', 'de 62,3 a 504,7 M por año, de Seguridad', 'de 57,5 a 465,6 M por año, de Seguridad')

wb.save(X)
print('ok · C358, C359 y notas')
