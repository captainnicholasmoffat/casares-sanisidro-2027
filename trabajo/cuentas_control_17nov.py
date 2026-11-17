"""Modelo fiscal, 17/11/2026: el control interno «los mismos números que el documento» (Resumen anual, filas 67 y 70)
y tres notas guardaban las cifras de antes de sumar los 60 agentes de marzo de 2026 (trabajo/cuentas_agentes.py).
Se ponen las cifras que hoy dice el documento (cuadro 20 del 3.6, 3.2 y Supuestos)."""
import sys, openpyxl
P = sys.argv[1]
wb = openpyxl.load_workbook(P)
ra = wb['Resumen anual']
for col, v in zip('CDEF', [565, 3336, 6222, 9225]): ra[f'{col}67'] = v * 1_000_000
for col, v in zip('CDEF', [565, 4574, 6739, 9225]): ra[f'{col}70'] = v * 1_000_000
s, e = wb['Supuestos'], wb['Escenarios']
def nota(ws, ref, old, new):
    assert old in ws[ref].value, (ref, ws[ref].value); ws[ref] = ws[ref].value.replace(old, new)
nota(s, 'E221', '+1.576 M', '+565 M')
nota(e, 'F19', '+5.342 M', '+4.331 M')
nota(e, 'F20', '−426 M', '−1.437 M')
wb.save(P); print('ok')
