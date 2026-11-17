"""Cuentas, 17/11/2026: la patrulla queda estable en la cantidad de agentes que haya al asumir (Nick, 16/11).
Suma al personal el costo de los 60 agentes que entraron en marzo de 2026 y no están en la base de 2025.
Cálculo: programa 46.01 del presupuesto 2026 (Ordenanza 9422), 5.743.108.868 pesos por 359 cargos = 15.997.518 por cargo;
por 60 agentes = 959,9 millones a precios de octubre de 2025; llevados a diciembre de 2025 con el IPC de noviembre (2,5%)
y diciembre (2,8%) del INDEC: 1.011,4 millones por año.
Uso: python3 -I trabajo/cuentas_agentes.py   (después: soffice recalcula y extract.py rehace cuentas.json)"""
import openpyxl, re
from pathlib import Path
X = Path(__file__).resolve().parents[1] / 'proyecto/web/cuentas/modelo_fiscal.xlsx'
por_cargo = 5743108868 / 359
costo = round(por_cargo * 60 * 1.025 * 1.028)
wb = openpyxl.load_workbook(X)
S = wb['Supuestos']
f = S.max_row + 2
S.cell(f, 2, 'AB · LA PATRULLA, ESTABLE EN LA CANTIDAD DE AGENTES QUE HAYA AL ASUMIR (5.7)')
S.cell(f + 1, 2, 'Seguridad · los 60 agentes que entraron en marzo de 2026 y no están en la base de 2025, por año')
S.cell(f + 1, 3, costo)
S.cell(f + 1, 5, 'Programa 46.01 del presupuesto 2026 (Ordenanza 9422): 5.743.108.868 pesos por 359 cargos, unos 16 M por cargo, '
                 'por 60 agentes; a pesos de diciembre de 2025 con el IPC de noviembre (2,5%) y diciembre (2,8%) de 2025. '
                 'Cálculo propio. Entra en personal y en la función 2.1; sale del resultado.')
ref = f'Supuestos!$C${f + 1}'
G = wb['Gastos objeto']; n = 0
for r in (8, 9):
    for c in G[r][2:]:
        if isinstance(c.value, str) and c.value.startswith('=Supuestos!$C$15*'):
            c.value = c.value.replace('=Supuestos!$C$15*', f'=(Supuestos!$C$15+{ref})*', 1); n += 1
F = wb['Gastos función']
for c in F[13][2:]:
    if isinstance(c.value, str) and c.value.startswith('=(Supuestos!$C$195)'):
        c.value = c.value.replace('=(Supuestos!$C$195)', f'=(Supuestos!$C$195+{ref})', 1); n += 1
wb.save(X)
print('costo por año', costo, '| fórmulas cambiadas', n, '| fila', f + 1)
