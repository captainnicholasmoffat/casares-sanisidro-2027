"""Lee el modelo fiscal (Excel) y deja los datos de la página «Las cuentas» en cuentas.json.
Uso: python3 -I extract.py <modelo.xlsx> <salida.json>"""
import json, sys
import openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
M = ('Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic')
Y4, Y8 = (2028, 2029, 2030, 2031), tuple(range(2028, 2036))
mill = lambda v: round(v / 1e6, 1)
def rows(ws, **kw): return [r[1:] for r in ws.iter_rows(values_only=True, **kw)]

def by_label(ws, col=0):
    out = {}
    for r in rows(ws):
        if r[col] is not None and str(r[col]).strip() not in out:
            out[str(r[col]).strip()] = r
    return out

def monthly(ws):
    rows = list(ws.iter_rows(values_only=True)); y = None; c = {}
    for j in range(2, len(rows[4])):
        if rows[4][j] is not None and str(rows[4][j]).isdigit(): y = int(rows[4][j])
        if rows[5][j] in M: c[(y, rows[5][j])] = j
    lab = {}
    for r in rows[6:]:
        if r[1] and str(r[1]).strip() not in lab: lab[str(r[1]).strip()] = r
    def annual(label, years=Y4):
        r = lab[label]; return [mill(sum(r[c[(y, m)]] or 0 for m in M)) for y in years]
    return lab, annual

def find(d, prefix):
    for k in d:
        if k.startswith(prefix): return k
    raise KeyError(prefix)

R = by_label(wb['Resumen anual'])
def rrow(prefix, n=8): r = R[find(R, prefix)]; return [mill(x) for x in r[1:1 + n]]
def rpct(prefix, n=8): r = R[find(R, prefix)]; return [round(x, 6) for x in r[1:1 + n]]
D = {}
D['years'] = list(Y8)
D['ingresos'] = {k: rrow(p) for k, p in [('municipal', 'Origen municipal'), ('tabla', 'Base de valuación actualizada'), ('provincial', 'Origen provincial'), ('nacional', 'Origen nacional'), ('capital', 'IV · Recursos de capital'), ('total', 'VI · INGRESOS TOTALES')]}
D['gastos'] = {k: rrow(p) for k, p in [('total', 'VII · GASTOS TOTALES'), ('obra', 'Bienes de uso: obra pública'), ('vecinos', 'de la cual, decidida por los vecinos'), ('empleo', 'Empleo: lo que suma el programa'), ('vivienda', 'Vivienda: lo que suma el programa')]}
D['resultado'] = rrow('VIII · Resultado financiero')
D['ahorro'] = rrow('III · Ahorro corriente')
D['empleo_vivienda'] = rrow('Empleo y vivienda, total anual')
D['programa_suma'] = rrow('Lo que el programa suma al gasto')
D['egresados'] = [int(x) for x in R[find(R, 'Egresados de la formación')][1:9]]
D['deuda2025'] = rrow('Deuda al 31/12/2025 que queda')
D['bono'] = rrow('Bono 2026: capital pendiente')
D['flotante'] = rrow('Deuda flotante por rezago')
D['caja'] = rrow('Saldo de caja al cierre')
D['base2025'] = {'resultado': mill(R[find(R, 'VIII · Resultado financiero')][1]) if False else None}
ctl = R[find(R, 'VIII · Resultado financiero')]
# control del año base: la fila de control repite la etiqueta; se toma de la sección CONTROL
for r in rows(wb['Resumen anual'], min_row=56, max_row=64):
    if r[0] and str(r[0]).startswith('VIII · Resultado financiero'): D['base2025'] = {'resultado': mill(r[1]), 'modelo': mill(r[2]), 'dif': r[3]}
cuadro20 = {}
for r in rows(wb['Resumen anual'], min_row=66, max_row=75):
    if r[0] and str(r[0]).startswith('Diferencia'): cuadro20.setdefault('dif', []).append([x for x in r[1:5]])
D['control_cuadro20'] = cuadro20
# Tabla de la cuenta completa (filas con números en 2028)
tabla = []
for r in rows(wb['Resumen anual'], min_row=7, max_row=54):
    if r[0] is None: continue
    vals = r[1:9]
    if all(v is None for v in vals): tabla.append({'h': str(r[0]).strip()}); continue
    pct = all(isinstance(v, (int, float)) and abs(v) < 2 for v in vals)
    tabla.append({'l': str(r[0]).strip(), 'v': [round(v, 4) if pct else (mill(v) if isinstance(v, (int, float)) and abs(v) >= 1e4 else v) for v in vals], 'pct': pct})
D['tabla_cuenta'] = tabla
E = by_label(wb['Escenarios'])
D['escenarios'] = {k: [mill(x) for x in E[find(E, p)][1:9]] for k, p in [('nada', 'Si nada cambia'), ('programa', 'Con el programa'), ('dif', 'Diferencia')]}
sens = []
srows = rows(wb['Escenarios'], min_row=14, max_row=22); cur = None
for r in srows:
    if r[0]: cur = {'var': str(r[0]).strip(), 'v': []}; sens.append(cur)
    if cur is not None and r[1] is not None: cur['v'].append({'x': r[1], 'res': mill(r[2]), 'nota': r[4] or ''})
D['sensibilidad'] = sens
P, pa = monthly(wb['Programas'])
D['programas'] = {k: pa(find(P, p)) for k, p in [('total', 'TOTAL PROGRAMAS'), ('ambiente', 'Ambiente · reasignación'), ('educacion', 'Educación · recomposición'), ('apoyo', 'Apoyo escolar'), ('inspecciones', 'Inspecciones grabadas'), ('contrapartida', 'Contrapartida'), ('flex_tabla', 'Empleo y vivienda · lo que la tabla no cobra'), ('empleo', 'Empleo: 60%'), ('vivienda', 'Vivienda y servicios básicos: 40%')]}
D['programas_labels'] = {'contrapartida': find(P, 'Contrapartida')}

zonas = []
vrows = list(rows(wb['Vecinal'], min_row=16, max_row=21))
crow = {r[0]: r for r in rows(wb['Vecinal'], min_row=30, max_row=35)}
for r in vrows:
    zonas.append({'zona': r[0], 'poblacion': r[1], 'indice': round(r[2], 4), 'peso': round(r[3], 4), 'obra': [mill(x) for x in r[4:8]], 'cupos': crow[r[0]][5]})
D['zonas'] = zonas
Vl, va = monthly(wb['Vecinal'])
D['vecinal_funcionamiento'] = va(find(Vl, 'Funcionamiento del sistema'))
F, fa = monthly(wb['Gastos función'])
D['funciones'] = [{'f': k, 'v': fa(k)} for k in F if k[:1].isdigit() and '·' in k]
D['metas'] = []
for r in rows(wb['Metas'], min_row=6, max_row=25):
    if r[0]: D['metas'].append({'meta': r[0], 'hoy': r[1], 'a4': r[2], 'a8': r[3], 'como': r[4]})
G = by_label(wb['Guía'], 0)
D['guia'] = {k: G[k][1] for k in ('QUÉ ES', 'UNIDAD', 'AÑO BASE', 'LA CUENTA', 'QUÉ CRECE', 'EL PROGRAMA', 'CÓMO SE PAGA', 'EL BONO')}
D['guia']['aviso'] = next(c for r in rows(wb['Guía']) for c in r if isinstance(c, str) and c.startswith('Este modelo proyecta'))
D['nota_tabla'] = R[find(R, 'El programa pide')][0]
json.dump(D, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
print('ok', len(json.dumps(D)))
