"""Cuentas, 17/11/2026 (revisión completa): sólo textos del modelo fiscal, sin tocar fórmulas ni datos de entrada.
- Metas: la meta de los espectáculos dice lo mismo que el cuadro 41 (hueco 19); falta un punto en la meta del CFL 404;
  las hojas de la A4 del cuadro 41 son la 111 a la 113.
- Guía y Supuestos: el gasto queda como en 2025 más los 60 agentes de 2026 (fila 304); la patrulla de la segunda etapa
  de las grabaciones, con 359 a unos 390 agentes (5.9); las referencias a cuadros que se renumeraron (27 → 28, 32 → 33,
  34 → 35); el bloque de la patrulla es el AC, no un segundo AB.
Uso: python3 -I trabajo/cuentas_textos_17nov.py   (después: soffice recalcula y extract.py rehace cuentas.json)"""
import openpyxl
from pathlib import Path
X = Path(__file__).resolve().parents[1] / 'proyecto/web/cuentas/modelo_fiscal.xlsx'
wb = openpyxl.load_workbook(X)
n = 0


def rep(hoja, celda, old, new):
    global n
    c = wb[hoja][celda]; v = c.value
    assert isinstance(v, str) and not v.startswith('=') and v.count(old) == 1, (hoja, celda, old[:50], v[:80] if isinstance(v, str) else v)
    c.value = v.replace(old, new, 1); n += 1


rep('Metas', 'B3', 'hojas 104 a 106 de la A4', 'hojas 111 a 113 de la A4')
rep('Metas', 'B18', 'consigan empleo pago En esta hoja', 'consigan empleo pago. En esta hoja')
rep('Metas', 'B22', 'Además, espectáculos al aire libre todas las semanas, de lunes a jueves, en los parques y plazas de San Isidro',
    'Además, espectáculos todas las semanas, de lunes a jueves: al aire libre en los parques y plazas de San Isidro de septiembre a abril, y bajo techo el resto del año')
rep('Guía', 'C9', '—cero recomposición salarial y cero servicios nuevos—, salvo el programa.',
    '—cero recomposición salarial y cero servicios nuevos—, salvo el programa y, desde 2028, los 60 agentes que se sumaron a la patrulla en 2026: 1.011,4 M por año (Supuestos, fila 304).')
rep('Supuestos', 'B70', 'El gasto queda constante en términos reales, salvo lo que suma el programa.',
    'El gasto queda constante en términos reales, salvo lo que suma el programa y, desde 2028, los 60 agentes que se sumaron a la patrulla en 2026 (fila 304).')
rep('Supuestos', 'E54', 'La patrulla, en la segunda etapa (29,5 a 35,3 M una vez y 135,7 a 162,4 M por año), no está sumada',
    'La patrulla, en la segunda etapa (de 359 a unos 390 agentes: 35,3 a 38,4 M una vez y 162,4 a 176,9 M por año), no está sumada')
rep('Supuestos', 'E50', '(cuadro 34)', '(cuadro 35)')
rep('Supuestos', 'B146', '(5.3, cuadro 34)', '(5.3, cuadro 35)')
rep('Programas', 'B25', '(cuadro 34)', '(cuadro 35)')
rep('Supuestos', 'E161', 'Cuadro 27, suma exacta', 'Cuadro 28, suma exacta')
rep('Supuestos', 'E161', 'puente con los laboratorios', 'puente con las empresas de inteligencia artificial')
rep('Supuestos', 'E162', 'Cuadro 27', 'Cuadro 28')
rep('Supuestos', 'E168', 'Cuadro 27: 15 de la plataforma y 2 de dispositivos, los 17 del cuadro 32', 'Cuadro 28: 15 de la plataforma y 2 de dispositivos, los 17 del cuadro 33')
rep('Supuestos', 'E227', 'del cuadro 27', 'del cuadro 28')
rep('Supuestos', 'B236', '(cuadro 27)', '(cuadro 28)')
rep('Supuestos', 'E271', 'del cuadro 27', 'del cuadro 28')
rep('Supuestos', 'B303', 'AB · LA PATRULLA', 'AC · LA PATRULLA')
wb.save(X)
print('textos cambiados', n)
