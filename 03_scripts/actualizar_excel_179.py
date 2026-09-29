# -*- coding: utf-8 -*-
"""Correcciones 179 y 180: actualiza MODELO_FISCAL_SAN_ISIDRO_2028_2035.xlsx sin rehacerlo,
para que de los mismos numeros que el modelo del repo y que el documento.
180: recursos corrientes por origen exactos (los de capital son todos municipales), suma exacta del
cuadro 27, el anio 1 si la tabla nueva cobra desde abril (6.6) y los cupos por zona por el resto mayor.

Uso: python3 03_scripts/actualizar_excel_179.py ORIGEN DESTINO [--habilitaciones=anual|inicial]
ORIGEN es el Excel tal como llego (commit 8358497, salida/). Lee los datos de data/.
Despues hay que recalcular con LibreOffice para que las celdas tengan valores.
"""
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L

SRC, OUT = sys.argv[1], sys.argv[2]
HAB_MODO = "inicial"    # habilitaciones y analitica: "inicial" (1.200 M una vez y 22% de mantenimiento) o "anual"
for a in sys.argv[3:]:
    if a.startswith("--habilitaciones="):
        HAB_MODO = a.split("=", 1)[1]


# ---------------------------------------------------------------- datos del repo
import csv as _csv
import pathlib as _pl
REPO = str(_pl.Path(__file__).resolve().parent.parent / "data") + "/"


def _leer(nombre):
    with open(REPO + nombre, encoding="utf-8") as fh:
        return list(_csv.DictReader(l for l in fh if not l.startswith("#")))


_rec = {r["rubro_codigo"]: r for r in _leer("ejecucion_recursos.csv")
        if r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual"}
_obj = {r["objeto_codigo"]: r for r in _leer("ejecucion_gastos_objeto.csv")
        if r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual"}
_sef = {(r["bloque"], r["concepto"], r["medida"]): float(r["monto"]) for r in _leer("sef_anual.csv")
        if r["anio"] == "2025"}
_fun = {r["funcion_codigo"]: float(r["devengado"] or 0) for r in _leer("gastos_finalidad_funcion.csv")
        if r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual" and r["nivel"] == "funcion"}
_val = {int(r["anio_del_programa"]): r for r in _leer("valuacion_rendimiento_por_anio.csv")}
_deu = {r["codigo"]: r for r in _leer("deuda_stock.csv") if r["anio"] == "2025" and r["trimestre"] == "IV"}
_mod = {(r["escenario"], int(r["anio"])): r for r in _leer("modelo_flujo_caja.csv")}


def rec(c, m):
    return float(_rec[c][m])


def obj(c, m):
    return float(_obj[c][m])


def sef_aif(c):
    return _sef[("ahorro_inversion", c, "oficial")]


def sef_org(c):
    return _sef[("recursos_por_origen", c, "percibido")]


def sef_prog(nombre):
    v = [val for (b, c, m), val in _sef.items() if b == "gastos_por_programa" and nombre in c and m == "devengado"]
    assert len(v) == 1, nombre
    return v[0]

wb = openpyxl.load_workbook(SRC)

# ---------------------------------------------------------------- estilos
WINE, GRAY, BLUE, GREEN = "FF7C2E23", "FF6E625A", "FF0000FF", "FF008000"
F_HDR = PatternFill("solid", fgColor=WINE)
F_SEC = PatternFill("solid", fgColor="FFEFE7DA")
F_TOT = PatternFill("solid", fgColor="FFEAE0CF")
F_KEY = PatternFill("solid", fgColor="FFFFFF00")
NOFILL = PatternFill(fill_type=None)
FMT_M = '\\$#,##0,,"  M";"($"#,##0,,") M";\\-'
FMT_M1 = '\\$#,##0.0,,"  M";"($"#,##0.0,,") M";\\-'
FMT_P = '\\$#,##0;"($"#,##0\\);\\-'
FMT_PCT2, FMT_PCT1, FMT_PCT0 = "0.00%", "0.0%", "0%"
FMT_N = '#,##0;(#,##0);\\-'


def font(size=9, bold=False, italic=False, color=None):
    return Font(name="Arial", size=size, bold=bold, italic=italic, color=color)


def put(ws, coord, value, f=None, fmt=None, fill=None, wrap=None, align=None):
    c = ws[coord]
    c.value = value
    if f is not None:
        c.font = f
    if fmt is not None:
        c.number_format = fmt
    if fill is not None:
        c.fill = fill
    if wrap is not None or align is not None:
        c.alignment = Alignment(wrap_text=bool(wrap), horizontal=align,
                                vertical="top" if wrap else None)
    return c


def clear_row(ws, r, c0=1, c1=None):
    c1 = c1 or ws.max_column
    for c in range(c0, c1 + 1):
        cell = ws.cell(r, c)
        cell.value = None
        cell.font = font()
        cell.fill = NOFILL
        cell.number_format = "General"


# meses: m = 1..96 en las columnas C..CT; anio y = 0..7 (2028..2035)
MESES = list(range(1, 97))


def col(m):
    return L(m + 2)


def anio(m):
    return (m - 1) // 12


def mes_del_anio(m):
    return (m - 1) % 12 + 1


def est(m):
    """columna de Estacionalidad para el mes del anio (C = enero)."""
    return L(mes_del_anio(m) + 2)


def rango_anio(y):
    return col(12 * y + 1), col(12 * y + 12)


ANIOS = list(range(8))
COL_ANIO = [L(3 + y) for y in ANIOS]          # Resumen anual: C..J


# ======================================================================
# SUPUESTOS
# ======================================================================
S = wb["Supuestos"]


def s_label(r, text, bold=False):
    put(S, f"B{r}", text, font(9, bold))


def s_in(r, value, fmt=FMT_P, key=False):
    put(S, f"C{r}", value, font(9, color=BLUE), fmt, F_KEY if key else NOFILL)


def s_fx(r, formula, fmt=FMT_P):
    put(S, f"C{r}", formula, font(9), fmt, NOFILL)


def s_note(r, text):
    put(S, f"E{r}", text, font(8, color=GRAY), wrap=True)


def s_header(r, text):
    clear_row(S, r, 2, 5)
    put(S, f"B{r}", text, font(9, True, color="FFFFFFFF"), fill=F_HDR)
    for c in "CDE":
        S[f"{c}{r}"].fill = F_HDR


def s_row(r, label, value=None, formula=None, note=None, fmt=FMT_P, key=False, bold=False):
    clear_row(S, r, 2, 5)
    s_label(r, label, bold)
    if formula is not None:
        s_fx(r, formula, fmt)
    elif value is not None:
        s_in(r, value, fmt, key)
    if note:
        s_note(r, note)


FUENTE_REC = "Estado de ejecución de recursos 2025, acumulado anual"
FUENTE_GAS = "Estado de ejecución de gastos por objeto 2025, acumulado anual"

# --- A · recursos 2025 por rubro (ejecucion oficial)
S["C6"].value = rec("1.1", "devengado")
S["C7"].value = rec("1.1", "percibido")
S["C8"].value = rec("1.2", "devengado")
S["C9"].value = rec("1.2", "percibido")
S["C10"].value = rec("1.6", "percibido")
S["C11"].value = rec("1.7", "percibido")
S["C12"].value = rec("2.1", "percibido")
assert rec("1.6", "devengado") == rec("1.6", "percibido") and rec("1.7", "devengado") == rec("1.7", "percibido")
s_note(6, "Rubro 1.1. De origen provincial: casi todo es la coparticipación, 82.268 M en 2025. " + FUENTE_REC)
s_note(7, "Rubro 1.1. Se percibió el 100% de lo devengado")
s_note(8, "Rubro 1.2. Tasas y derechos municipales: servicios generales, seguridad e higiene y el resto. " + FUENTE_REC)
s_note(9, "Rubro 1.2. Quedaron sin cobrar 35.994 millones: el 15,6% de lo devengado")
s_note(10, "Rubro 1.6. Intereses de colocaciones y alquileres. De origen municipal")
s_note(11, "Rubro 1.7. De Provincia, de Nación y de otros orígenes, fuera de la coparticipación")
s_note(12, "Rubro 2.1. Venta de activos. De origen municipal")

# --- B · gastos 2025 por objeto (ejecucion oficial)
for i, codigo in enumerate("1234567"):
    S[f"C{15 + 2 * i}"].value = obj(codigo, "devengado")
    S[f"C{16 + 2 * i}"].value = obj(codigo, "pagado")
s_note(15, "Objeto 1. El 34,4% del gasto total: el vigésimo municipio con menor peso salarial de 106. " + FUENTE_GAS)
s_note(23, "Objeto 5. Subsidios y aportes a terceros. Incluye 16,5 M de transferencias de capital (bloque M)")
s_note(25, "Objeto 6. En la cuenta Ahorro-Inversión va debajo de la línea: es una aplicación financiera")
s_note(27, "Objeto 7. En la cuenta Ahorro-Inversión va debajo de la línea: es amortización de deuda")

# --- C · parametros: la cobranza sale como forma de pagar el programa
s_row(33, "Percepción de los recursos corrientes · 2025",
      formula="=ROUND((C7+C9+C10+C11)/(C6+C8+C10+C11),4)", fmt=FMT_PCT2,
      note="301.155 percibidos sobre 337.149 facturados en 2025. El modelo del repo usa la cifra redondeada: 89,32%")
s_row(34, "Percepción · palanca de la sensibilidad", 0.8932, fmt=FMT_PCT2, key=True,
      note="En 89,32% no cambia nada. La sensibilidad del 3.6 la mueve tres puntos, a 86,32% y 92,32%, "
           "y el cambio entra en cuatro años desde 2025, como en el modelo del repo. El programa no se paga cobrando mejor")
s_note(31, "Recursos de origen municipal en pesos constantes, 2010–2025, punta a punta. La media de los seis tramos da 3,49% con desvío de 8,14 puntos")
s_note(32, "Parte de San Isidro en lo que la Provincia reparte a los 135 municipios, 2021–2025: de 1,9378% a 1,7731%. "
           "Mueve el 82,4% de lo provincial (bloque L)")
s_note(35, "Supuesto conservador, el del modelo del repo: cero recomposición salarial real")
s_note(36, "Supuesto conservador, el del modelo del repo: cero servicios nuevos, salvo el programa")

# --- E · programas del capitulo 5
s_row(49, "Empleo y vivienda · base 2025", formula="=C147+C148",
      note="170,3 M de empleo más 335,4 M de vivienda, devengado 2025")
s_row(50, "Empleo y vivienda · objetivo anual", formula="=C149*(C123+C124)",
      note="2,5% del gasto total de 2025 en la cuenta Ahorro-Inversión: 7.730,9 M, quince veces la base (cuadro 33)")
s_row(51, "Ambiente · gasto 2025 (función 4.4)", 1410000000,
      note="5.5: «Hoy: 1.410 millones, el 0,4% del presupuesto». La ejecución da 1.410,1 M (bloque S)")
s_row(52, "Ambiente · objetivo, sobre el gasto devengado de 2025", 0.015, fmt=FMT_PCT1,
      note="Meta del 6.3. 1,5% de 324.304 M menos 1.410 M: 3.455 M por año (cuadro 14). "
           "Empieza a moverse en el mes 12 y llega en el mes 36 (6.4)")
s_row(53, "Educación · recomposición anual", 2064000000,
      note="Devolver la función educativa al nivel real de 2024, que cayó 11,6%: 2.064 M (5.8, cuadro 14). Desde el mes 12 (6.4)")
s_row(54, "Habilitaciones y analítica de seguridad · inversión inicial, una vez", 1200000000,
      note="Cuadro 14 y 5.9: 1.200 M a licitar, 60% el año 1 y 40% el año 2; incluye 80 cámaras corporales. "
           "ESTIMACIÓN PROPIA, NO VERIFICADA")
s_row(55, "Apoyo escolar · costo anual por sede", 180000000,
      note="ESTIMACIÓN PROPIA, NO VERIFICADA. Seis sedes: 1.080 M (cuadro 14). Dos sedes por año es supuesto de este libro")
s_row(56, "Salud · adhesión al sistema provincial", 0,
      note="Mi Salud Digital no tiene costo de licencia para el municipio que adhiere")
s_row(57, "Habilitaciones y analítica · mantenimiento anual, sobre lo invertido", 0.22, fmt=FMT_PCT0,
      note="Desde el año siguiente a cada compra: 264 M por año en régimen. Es el soporte anual de software de lista: "
           "10.450 USD sobre una licencia de 47.500 USD (lista de precios de Oracle, 2026)")

# --- F · deuda
s_row(59, "Stock de deuda al 30/12/2025, consolidada y flotante", float(_deu["1"]["saldo"]) + float(_deu["2"]["saldo"]),
      note="Formulario Ley 12.462, cuarto trimestre de 2025: 4.984 M consolidada y 3.976 M flotante (cuadro 18). "
           "Es la deuda con que entra el modelo del repo")
s_row(60, "Deuda flotante al 30/06/2026 · no entra en el modelo", 8231000000,
      note="Informe del segundo trimestre de 2026 (cuadro 18). Es posterior al cierre del modelo y el documento no la "
           "incorpora: la flotante al 31/12/2025 ya está en la fila anterior")
S["C60"].font = font(9, color=GRAY)
s_row(61, "Amortización del ejercicio 1 (2026)", float(_deu["1"]["amortiz_ej1"]),
      note="Formulario Ley 12.462. El resto del stock se amortiza en partes iguales en 2027, 2028 y 2029, como en el "
           "modelo del repo: la deuda llega a cero en 2029 (3.5)")
s_note(62, "Constitución provincial, artículo 193, inciso 3: los servicios de amortización e intereses no pueden "
           "pasar del 25% de los recursos ordinarios")
s_row(64, "Años para amortizar el resto del stock (desde 2027)", 3, fmt="0",
      note="Supuesto declarado del modelo del repo: el formulario sólo publica el vencimiento del ejercicio 1")

# --- nota del anio base
put(S, "B69", "El año base es la ejecución 2025 oficial. Los recursos van por lo percibido y los gastos por lo devengado, "
    "como en la cuenta Ahorro-Inversión del Estado de Situación Económico-Financiera: resultado de −6.051 millones. "
    "La deuda y los activos financieros van debajo de la línea. El control está al pie de la hoja Resumen anual y da "
    "diferencia cero.", font(8, color=GRAY), wrap=True)
put(S, "B70", "Los recursos del año 1 arrancan por encima de 2025 porque entre 2025 y 2028 pasan tres años de crecimiento "
    "real. El gasto queda constante en términos reales, salvo lo que suma el programa.", font(8, color=GRAY), wrap=True)

# --- G · afectacion: la del propio Municipio en 2025
s_row(74, "Origen municipal · % de libre disponibilidad", formula="=C107/(C107+C108)", fmt=FMT_PCT2,
      note="Estado de Situación Económico-Financiera 2025: 207.565 M de libre disponibilidad sobre 207.969 M de origen municipal")
s_row(75, "Origen provincial · % de libre disponibilidad", formula="=C109/(C109+C110)", fmt=FMT_PCT2,
      note="Estado de Situación Económico-Financiera 2025: 79.683 M de libre disponibilidad sobre 87.694 M de origen provincial")
s_row(76, "Origen nacional · % de libre disponibilidad", 0, fmt=FMT_PCT2,
      note="Los 190 M de origen nacional llegan afectados. Los otros orígenes, 7.332 M, son de libre disponibilidad")

# --- I · deuda por acreedor: la composicion oficial
s_header(86, "I · LA DEUDA AL 30/12/2025, ABIERTA (formulario Ley 12.462)")
s_row(87, "Deuda consolidada", float(_deu["1"]["saldo"]),
      note="Organismos provinciales 2.923 M —IPS 2.100 e IOMA 823—, CEAMSE 465 M y otras deudas 1.596 M")
s_row(88, "Deuda flotante", float(_deu["2"]["saldo"]),
      note="Obligaciones de corto plazo. Entra en el stock del modelo y se amortiza con él")
s_row(89, "Préstamo del Banco Provincia · no entra en el modelo", 1000000000,
      note="Aparece por primera vez en el informe de junio de 2026 (3.5): es posterior al cierre del modelo")
S["C89"].font = font(9, color=GRAY)
s_row(90, "Tasa de interés real anual de la deuda", 0, fmt=FMT_PCT2,
      note="El modelo no proyecta intereses: está en pesos constantes y el del bono es nominal y variable (3.6)")
s_row(91, "Control · consolidada más flotante menos el stock del bloque F", formula="=C87+C88-C59",
      note="Tiene que dar cero")

# --- J · la cancelacion de la flotante heredada sale: esa flotante esta en el stock
clear_row(S, 97, 2, 5)

# --- K · bono
s_row(104, "Bono · capital pendiente al 1/1/2028", formula="=C100*(C102-1)/C102",
      note="Quedan siete de las ocho cuotas: el 87,5% del capital lo paga el mandato que arranca en 2028. "
           "Van en febrero, mayo, agosto y noviembre de 2028 y en febrero, mayo y agosto de 2029")

# --- bloques nuevos
r = 106
s_header(r, "L · RECURSOS 2025 POR ORIGEN (Estado de Situación Económico-Financiera 2025, percibido)")
s_row(107, "Origen municipal · de libre disponibilidad", sef_org("ORIGEN MUNICIPAL-DE LIBRE DISPONIBILIDAD"),
      note="Son exactamente los no tributarios, las rentas y los recursos de capital del bloque A")
s_row(108, "Origen municipal · afectados", sef_org("ORIGEN MUNICIPAL-AFECTADOS"))
s_row(109, "Origen provincial · de libre disponibilidad", sef_org("ORIGEN PROVINCIAL-DE LIBRE DISPONIBILIDAD"),
      note="Los tributarios del bloque A más 2.314 M de las transferencias")
s_row(110, "Origen provincial · afectados", sef_org("ORIGEN PROVINCIAL-AFECTADOS"))
s_row(111, "Origen nacional · afectados", sef_org("ORIGEN NACIONAL-AFECTADOS"))
s_row(112, "Otros orígenes · de libre disponibilidad", sef_org("OTROS ORIGENES-DE LIBRE DISPONIBILIDAD"))
s_row(113, "Control: lo municipal por origen menos no tributarios, rentas y recursos de capital", 
      formula="=(C107+C108)-(C9+C10+C12)",
      note="Tiene que dar cero: los recursos de capital (rubro 2.1) son todos de origen municipal")
s_row(114, "Origen municipal · corrientes, como en el modelo", formula="=C107+C108-C12",
      note="Los recursos de capital se restan enteros de lo municipal, como en 03_scripts/modelo.py (corrección 180)")
s_row(115, "Origen provincial · corrientes", formula="=C109+C110")
s_row(116, "Origen nacional · corrientes", formula="=C111")
s_row(117, "Otros orígenes · corrientes", formula="=C112")
s_row(118, "Parte de lo provincial que se mueve con la coparticipación", 0.824, fmt=FMT_PCT1,
      note="Calculada en 2025 en el modelo del repo. El resto son fondos específicos que no dependen del coeficiente")

s_header(120, "M · CUENTA AHORRO-INVERSIÓN 2025, OFICIAL (Estado de Situación Económico-Financiera)")
s_row(121, "I · Ingresos corrientes", sef_aif("ingresos_corrientes"), note="Percibido")
s_row(122, "IV · Recursos de capital", sef_aif("recursos_de_capital"))
s_row(123, "II · Gastos corrientes", sef_aif("gastos_corrientes"), note="Devengado")
s_row(124, "V · Gastos de capital", sef_aif("gastos_de_capital"))
s_row(125, "VIII · Resultado financiero", sef_aif("resultado_financiero"), note="El −6.051 del capítulo 3")
s_row(126, "Transferencias de capital, dentro del objeto 5", formula="=C124-C21",
      note="Lo que el gasto de capital oficial tiene por encima de la obra pública")
s_row(127, "Gasto devengado total 2025", formula="=C15+C17+C19+C21+C23+C25+C27",
      note="Los 324.304 M del documento: todos los objetos, con la deuda")
s_row(128, "Gasto flexible 2025", formula="=C17+C21+C23+C25",
      note="Bienes de consumo, bienes de uso, transferencias y activos financieros: lo único que se puede reasignar dentro del año (3.4)")

s_header(130, "N · BASE DE VALUACIÓN ACTUALIZADA (escenario B: 3.5 e informe 09)")
s_row(131, "Suba pareja de la escala de ARBA sobre la neutral", 0.1088, fmt=FMT_PCT2,
      note="Se fija para que la parte tierra emita 8.089 M más por año: un 10,9% más que hoy. La alícuota no se toca")
s_row(132, "Tope de suba por boleta y por año", 0.25, fmt=FMT_PCT0,
      note="Por eso la actualización se completa en cuatro ejercicios. Las bajas van desde el primero")
s_row(133, "Emisión extra de la parte tierra, en régimen", float(_val[4]["emision_extra"]))
for i, (v, vm) in enumerate([(float(_val[k]["cobrado"]), float(_val[k]["cobrado_si_el_minimo_frena_subas"]))
                             for k in (1, 2, 3, 4)]):
    et = ["Año 1 del programa (2028)", "Año 2 (2029)", "Año 3 (2030)", "Año 4 en adelante (2031–2035)"][i]
    s_row(134 + i, f"{et} · lo cobrado", v,
          note=("Lo cobrado a la percepción de 2025, 89,32%. data/valuacion_rendimiento_por_anio.csv" if i == 0 else None))
    s_row(138 + i, f"Si el mínimo frena subas · {et.lower()}", vm,
          note=("Si el mínimo de la tasa frena todas las subas de lotes chicos: hasta 44,5 M menos por año (3.5)"
                if i == 0 else None))
s_row(142, "¿El mínimo frena las subas de lotes chicos? 1 = sí, 0 = no", 0, fmt="0", key=True,
      note="El documento y el modelo del repo corren el 0. Con 1, lo cobrado en régimen es 7.180,7 M: "
           "el rango del 3.5 es 7.180,7 a 7.225,2 M")
s_row(143, "Lo que el programa necesita en régimen", formula="=C50-C49",
      note="Los 7.225,2 M de fondos nuevos por año")
s_row(144, "Lo cobrado en régimen, con el mínimo que frena subas, sobre lo que se necesita",
      formula="=C141/C143", fmt=FMT_PCT1, note="Lo que el programa necesita, o un 0,6% menos (3.5)")

s_header(146, "O · EMPLEO Y VIVIENDA Y LA FORMACIÓN (5.3, cuadro 33)")
s_row(147, "Empleo · devengado 2025 (Apoyo y Promoción al Empleo)", sef_prog("APOYO Y PROMOCION AL EMPLEO"))
s_row(148, "Vivienda · devengado 2025 (Infraestructura Habitacional)", sef_prog("INFRAESTRUCTURA HABITACIONAL"))
s_row(149, "Objetivo: parte del gasto total de 2025", 0.025, fmt=FMT_PCT1,
      note="La rampa lo alcanza en cuatro años: 25%, 50%, 75% y 100% de lo que falta, desde 2028")
s_row(150, "Parte de empleo; el resto es vivienda y servicios básicos", 0.60, fmt=FMT_PCT0,
      note="Empleo es gasto corriente y vivienda, gasto de capital")
s_row(151, "Parte de formación dentro de empleo, desde el año 3", 0.60, fmt=FMT_PCT0,
      note="El resto paga la contratación de desarrollos: salud y automatización de tareas de la planta")
s_row(152, "Años en que la formación usa toda la partida de empleo", 2, fmt="0",
      note="Todavía no hay egresados que contratar: entran 462 y 824 en vez de 277 y 494 (nota del cuadro 33)")
s_row(153, "Costo por persona, los dos años de formación", 3000000,
      note="Con las materias y el título de la UNSO. Cada año entran lo que paga formación dividido por esto, redondeado")
s_row(154, "Mes del primer ingreso de cada año", 3, fmt="0", note="La primera cohorte arranca a los cien días")
s_row(155, "Mes del segundo ingreso de cada año", 9, fmt="0")
s_row(156, "Meses desde el ingreso hasta el egreso", 24, fmt="0",
      note="Doce de cursada y doce de pasantía: seis en el Municipio y seis en una empresa del partido")
s_row(157, "Tope de pasantes a la vez en el Municipio: 7% de los cargos", 556, fmt=FMT_N,
      note="7% de los 7.946 cargos del presupuesto 2026 (Res. Conj. 825/2009 y 338/2009, art. 14)")

s_header(159, "P · CIENCIA Y TÉCNICA: PLATAFORMA, DISPOSITIVOS Y SEMILLERO (4.11 y 5.3)")
s_row(160, "Ciencia y Técnica · devengado 2025", formula="=C199",
      note="Función 3.5 (bloque S): los 8.155 M del documento")
s_row(161, "Plataforma: 49 personas con cargas, infraestructura y auditoría", 1585600000,
      note="Cuadro 27, suma exacta de sus filas: equipo 1.285,1 M, infraestructura y licencias 193,2 M, "
           "auditoría externa 107,3 M. Con los dispositivos, 1.676,6 M. ESTIMACIÓN PROPIA")
s_row(162, "Dispositivos", 91000000, note="Cuadro 27")
s_row(163, "Semillero de empresas", 121000000,
      note="5.3 e informe 10: 117,1 M del fondo que presta uno a uno (hasta cinco empresas por año, 23,4 M cada una) y 3,9 M para constituirlas")
s_row(164, "Parte de Ciencia y Técnica ocupada", formula="=(C161+C162+C163)/C160", fmt=FMT_PCT1,
      note="El 22,0% del documento. Sin el semillero, 20,6%")

s_header(166, "Q · PASANTÍAS Y GASTO FLEXIBLE (5.3 y 3.4)")
s_row(167, "Pasantes a la vez en el Municipio, en régimen", 464, fmt=FMT_N, note="928 por año, seis meses cada uno")
s_row(168, "De ellos, en la plataforma y los dispositivos", 17, fmt=FMT_N, note="Cuadro 31: 15 de la plataforma y 2 de dispositivos")
s_row(169, "Costo de un pasante por año, con ART y salud", 3166250,
      note="240.000 $ por mes: 1.013,2 M por 320 pasantes (5.3)")
s_row(170, "Beca de práctica por mes", 240000, note="La asignación del pasante: la misma para quien no tiene lugar en una empresa")
s_row(171, "Juniors de las áreas, por año", 720000000, note="90 puestos de operación, a escala municipal (5.3)")
s_row(172, "Lo que pagan las áreas: pasantes y juniors", formula="=(C167-C168)*C169+C171",
      note="Del presupuesto de cada área: los 2.135,3 M del cuadro 14. No es gasto nuevo")
s_row(173, "Lo que pagan las empresas por los segundos seis meses · no es gasto municipal",
      formula="=C167*C169", note="1.469,1 M por año")
s_row(174, "Beca de práctica, peor caso: ninguna empresa toma pasantes", formula="=C167*C170*12",
      note="1.336,3 M por año, del gasto flexible que queda libre")
s_row(175, "Módulo de salud de los años 1 y 2, como máximo", formula="=(C49+C143/2)*C150*(1-C151)",
      note="Lo que habría pagado la contratación de desarrollos el año 2: 988,4 M. Sale del gasto flexible libre")
s_row(176, "Reasignación del gasto flexible, en régimen", formula="=(C52*C127-C51)+C53+6*C55+C54*C57",
      note="Ambiente, educación, apoyo escolar y el mantenimiento de habilitaciones: los 6.863 M del cuadro 15. "
           "La inversión de 1.200 M va aparte, una vez")
s_row(177, "Obra vecinal del año 4", formula="=C21*C45", note="28.908 M: la mitad de la obra pública")
s_row(178, "Fondos nuevos sobre el gasto flexible", formula="=C143/C128", fmt=FMT_PCT1, note="El 8,3% del documento")
s_row(179, "Empleo y vivienda y obra vecinal sobre el gasto flexible", formula="=(C143+C177)/C128", fmt=FMT_PCT1,
      note="El 41,4% del documento")
s_row(180, "Gasto flexible ocupado, con todo", formula="=(C143+C176+C172+C228+C177)/C128", fmt=FMT_PCT1,
      note="Fondos nuevos, reasignación, áreas, cuidadores y obra vecinal: el 52,4% del documento")
s_row(181, "Gasto flexible libre", formula="=1-C180", fmt=FMT_PCT1, note="El 47,6%")
s_row(182, "Libre con la beca y el módulo de salud", formula="=C181-(C174+C175)/C128", fmt=FMT_PCT1,
      note="El 44,9%. La plataforma y el semillero se pagan dentro de Ciencia y Técnica")

s_header(184, "R · EL SISTEMA VECINAL (capítulo 4)")
s_row(185, "Funcionamiento: parte fija de la partida vecinal", 0.015, fmt=FMT_PCT1,
      note="Cuidado de chicos en cada asamblea, honorario de los tres vecinos que firman la recepción y administración "
           "de las obras de la comisión: 433,6 M el año 4 y 108,4 M el año 1 (4.6). Sale de la propia partida")
s_row(186, "Panel sorteado: honorario por panel", 3100000,
      note="40 personas, cuatro sesiones y un día del sueldo de ingreso municipal por sesión. Sale de reasignación (3.4)")

s_header(188, "S · GASTO 2025 POR FINALIDAD Y FUNCIÓN (ejecución, acumulado anual)")
FUNCIONES = [
    (189, "1.1 · Legislativa", _fun["1.1"]),
    (190, "1.2 · Judicial", _fun["1.2"]),
    (191, "1.3 · Dirección superior ejecutiva", _fun["1.3"]),
    (192, "1.5 · Relaciones con la comunidad", _fun["1.5"]),
    (193, "1.6 · Administración fiscal", _fun["1.6"]),
    (194, "1.7 · Control de la gestión pública", _fun["1.7"]),
    (195, "2.1 · Seguridad interna", _fun["2.1"]),
    (196, "3.1 · Salud", _fun["3.1"]),
    (197, "3.2 · Promoción y asistencia social", _fun["3.2"]),
    (198, "3.4 · Educación y cultura", _fun["3.4"]),
    (199, "3.5 · Ciencia y técnica", _fun["3.5"]),
    (200, "3.6 · Trabajo", _fun["3.6"]),
    (201, "3.7 · Vivienda y urbanismo", _fun["3.7"]),
    (202, "3.8 · Agua potable y alcantarillado", _fun["3.8"]),
    (203, "3.9 · Urbanismo", _fun["3.9"]),
    (204, "4.3 · Transporte", _fun["4.3"]),
    (205, "4.4 · Ecología y medio ambiente", _fun["4.4"]),
    (206, "4.7 · Comercio, turismo y otros servicios", _fun["4.7"]),
    (207, "5.1 · Servicios de la deuda pública", _fun["5.1"]),
]
for rr, lab, v in FUNCIONES:
    s_row(rr, lab, v)
s_note(189, "data/gastos_finalidad_funcion.csv, 2025, acumulado anual")
s_row(208, "Total por función", formula="=SUM(C189:C207)",
      note="Es el gasto por objeto sin los activos financieros: control en la hoja Resumen anual", bold=True)

s_header(210, "T · LOS TRES PROGRAMAS QUE CEDEN (cuadro 15)")
s_row(211, "Mantenimiento y embellecimiento del Municipio (programa 49)", sef_prog("EMBELLECIMIENTO"),
      note="Estado de ejecución de gastos por programa 2025, acumulado anual")
s_row(212, "Construcción de infraestructura deportiva (programa 35)", sef_prog("INFRAESTRUCTURA DEPORTIVA"))
s_row(213, "Mantenimiento y reposición del arbolado público (programa 23)", sef_prog("ARBOLADO"))
s_row(214, "Lo que ceden: la reasignación sobre los tres", formula="=C176/SUM(C211:C213)", fmt=FMT_PCT0,
      note="El 28% del cuadro 15")
_r12 = [r for r in _leer("ejecucion_recursos.csv") if r["anio"] == "2025" and r["rubro_codigo"] == "1.2"]
_q1 = float([r for r in _r12 if r["periodo_tipo"] == "trimestre" and r["trimestre"] == "I"][0]["percibido_const_dic2025"])
_an = float([r for r in _r12 if r["periodo_tipo"] == "acumulado_anual"][0]["percibido_const_dic2025"])
s_header(216, "U · SI LA TABLA NUEVA NO SALE EN DICIEMBRE Y COBRA DESDE ABRIL (6.6)")
s_row(217, "Parte de lo cobrado en el año que entra de abril a diciembre", round(1 - _q1 / _an, 6), fmt=FMT_PCT1,
      note="2025: el primer trimestre trajo el 27,3% de lo cobrado en el año por tasas y derechos (rubro 1.2), "
           "en pesos constantes (data/ejecucion_recursos.csv)")
s_row(218, "Año 1: lo que cobra la tabla nueva si cobra desde abril", formula="=C134*C217",
      note="1.437 M en vez de 1.976 M")
s_row(219, "Año 1: lo que suma el programa al gasto", formula="='Resumen anual'!C53", note="1.806 M")
s_row(220, "Año 1: lo que cobra menos lo que suma el programa", formula="=C218-C219", note="−369 M")
s_row(221, "Resultado 2028 con el programa, si la tabla cobra desde abril", formula="='Resumen anual'!C33-(C134-C218)",
      note="+1.207 M: peor que sin el programa (+1.576 M), y con superávit. Desde 2029 no cambia nada")
s_row(222, "Resultado 2028 si nada cambia, para comparar", formula="='Resumen anual'!C68")
s_header(224, "V · CUIDADORES DOMICILIARIOS Y EQUIPOS POR ÁREA (5.13 y 3.4)")
s_row(225, "Cuidadores domiciliarios, primera etapa", 100, fmt=FMT_N,
      note="Formados en el curso de operador de cuidados de adultos mayores del CFL 404 (380 h, DGCyE 2269/2022); "
           "unas 240 personas, cuatro horas por día cada una. Los paga Desarrollo Social")
s_row(226, "Sueldo mensual · asistencia y cuidado de personas, con retiro", 427806.54,
      note="Diciembre de 2025: Comisión Nacional de Trabajo en Casas Particulares, Resolución 3/2025, Anexo II")
s_row(227, "Cargas del empleador", 0.20075, fmt=FMT_PCT2,
      note="Las del cuadro 27: IPS 12%, IOMA 4,8% y ART 3,275%")
s_row(228, "Cuidadores · costo anual, trece sueldos", formula="=C225*C226*(1+C227)*13",
      note="667,8 M por año: entra en el gasto flexible ocupado")
s_row(230, "Ambiente · seis estaciones de monitoreo de ruido, una vez", 313491221,
      note="39.718.000 $ cada una (Ciudad, orden de compra de diciembre de 2024), a pesos de diciembre de 2025")
s_row(231, "Formación · sesenta puestos en seis centros de acceso, una vez", 137091891,
      note="Notebook, escritorio y silla: 2,28 M por puesto (compras públicas 2025 y 2026)")
s_row(232, "Formación · conexión de las seis sedes, por año", 39502616,
      note="Fibra óptica, 629.200 $ por mes (Ciudad, 2026)")
s_row(233, "Habilitaciones · ochenta cámaras corporales, una vez, dentro de los 1.200 M", 168737624,
      note="2.170.000 $ cada una (Superintendencia de Riesgos del Trabajo, enero de 2026)")
s_row(234, "Habilitaciones · licencia de monitoreo, por año", 3825756,
      note="55.878 $ por cámara y por año, desde el segundo año (lista de proveedor, 2026)")
s_row(235, "Salud · trece pantallas de ocupación de guardia, una vez", 8318978,
      note="Televisor de 43 pulgadas, soporte y mini PC: 0,64 M por pantalla (compras públicas 2025 y 2026)")
put(S, "B236", "Cada equipo entra en la línea de su área y dentro de su monto; en Ciencia y Técnica quedan las "
    "personas que los instalan (cuadro 27). Precios llevados a diciembre de 2025 con el IPC.",
    font(8, italic=True, color=GRAY))
for rr in range(106, 237):
    S.row_dimensions[rr].height = None

# ======================================================================
# ESTACIONALIDAD: cada fila suma exactamente 100%
# ======================================================================
E = wb["Estacionalidad"]
for rr in (8, 10, 15):
    for c in range(3, 15):
        E.cell(rr, c).value = 1 / 12
put(E, "B2", "PERFIL MENSUAL POR ORIGEN Y POR OBJETO", font(13, True, color=WINE))
put(E, "B6", "Tasas y derechos municipales, y la base de valuación", font(9))
put(E, "P6", "Pico en enero por el pago anual anticipado con descuento; el resto, cuota bimestral. Perfil estimado",
    font(8, italic=True, color=GRAY), wrap=True)
put(E, "B7", "Coparticipación y demás de origen provincial", font(9))
put(E, "P7", "La coparticipación y Seguridad e Higiene son continuas. Perfil estimado", font(8, italic=True, color=GRAY), wrap=True)
put(E, "B8", "Nacional y otros orígenes", font(9))
put(E, "P10", "Doce sueldos parejos: un doceavo cada mes", font(8, italic=True, color=GRAY), wrap=True)

# ======================================================================
# RECURSOS: por origen, como el modelo del repo
# ======================================================================
R = wb["Recursos"]
put(R, "B2", "RECURSOS MENSUALES POR ORIGEN · 2028–2035", font(13, True, color=WINE))
put(R, "B3", "Percibidos, por origen del dinero, como el modelo del repo. Lo facturado y no cobrado va como memo.",
    font(9, italic=True, color=GRAY))
for rr in range(7, 24):
    clear_row(R, rr)
put(R, "B7", "RECURSOS CORRIENTES PERCIBIDOS, POR ORIGEN", font(9, True), fill=F_SEC)
labels = {8: "11 · Origen municipal: tasas, derechos y rentas",
          9: "11 · Base de valuación actualizada: lo cobrado",
          10: "21 · Origen provincial: coparticipación",
          11: "21 · Origen provincial: fondos específicos",
          12: "31 y 41 · Origen nacional y otros orígenes",
          13: "Total ingresos corrientes percibidos",
          15: "RECURSOS DE CAPITAL Y PERCEPCIÓN",
          16: "Recursos de capital",
          17: "Percepción sobre lo facturado, la de la palanca",
          18: "Factor contra la percepción de 2025",
          20: "TOTAL PERCIBIDO",
          22: "Memo · facturado y no cobrado en el mes",
          23: "Memo · percepción sobre lo facturado"}
for rr, t in labels.items():
    if rr == 15:
        put(R, f"B{rr}", t, font(9, True), fill=F_SEC)
    elif rr in (13,):
        put(R, f"B{rr}", t, font(9, True))
    elif rr == 20:
        put(R, f"B{rr}", t, font(9, True), fill=F_TOT)
    elif rr in (22, 23):
        put(R, f"B{rr}", t, font(8, italic=True, color=GRAY))
    else:
        put(R, f"B{rr}", t, font(9))
for m in MESES:
    X, y, e = col(m), anio(m), est(m)
    n, k = y + 3, y + 1
    kk = min(k, 4)
    R[f"{X}8"] = f"=Supuestos!$C$114*(1+Supuestos!$C$31)^{n}*Estacionalidad!{e}$6*{X}$18"
    R[f"{X}9"] = (f"=IF(Supuestos!$C$142=1,Supuestos!$C${137 + kk},Supuestos!$C${133 + kk})"
                  f"*Estacionalidad!{e}$6*{X}$18")
    R[f"{X}10"] = f"=Supuestos!$C$115*Supuestos!$C$118*(1+Supuestos!$C$32)^{n}*Estacionalidad!{e}$7*{X}$18"
    R[f"{X}11"] = f"=Supuestos!$C$115*(1-Supuestos!$C$118)*Estacionalidad!{e}$7*{X}$18"
    R[f"{X}12"] = f"=(Supuestos!$C$116+Supuestos!$C$117)*Estacionalidad!{e}$8*{X}$18"
    R[f"{X}13"] = f"=SUM({X}8:{X}12)"
    R[f"{X}16"] = f"=Supuestos!$C$12*Estacionalidad!{e}$9"
    R[f"{X}17"] = f"=Supuestos!$C$33+(Supuestos!$C$34-Supuestos!$C$33)*MIN({n},4)/4"
    R[f"{X}18"] = f"={X}17/Supuestos!$C$33"
    R[f"{X}20"] = f"={X}13+{X}16"
    R[f"{X}22"] = (f"={X}13*((Supuestos!$C$6+Supuestos!$C$8+Supuestos!$C$10+Supuestos!$C$11)"
                   f"/(Supuestos!$C$7+Supuestos!$C$9+Supuestos!$C$10+Supuestos!$C$11)/{X}18-1)")
    R[f"{X}23"] = f"=IFERROR({X}13/({X}13+{X}22),0)"
    for rr in (8, 9, 10, 11, 12, 16, 22):
        R[f"{X}{rr}"].number_format = FMT_M
        R[f"{X}{rr}"].font = font(8, italic=True, color=GRAY) if rr == 22 else font(9)
    R[f"{X}13"].number_format = FMT_M
    R[f"{X}13"].font = font(9, True)
    R[f"{X}20"].number_format = FMT_M
    R[f"{X}20"].font = font(9, True)
    R[f"{X}20"].fill = F_TOT
    R[f"{X}17"].number_format = FMT_PCT2
    R[f"{X}18"].number_format = "0.0000"
    R[f"{X}23"].number_format = FMT_PCT2
    R[f"{X}23"].font = font(8, italic=True, color=GRAY)
    for rr in (17, 18):
        R[f"{X}{rr}"].font = font(9)

# ======================================================================
# PROGRAMAS
# ======================================================================
P = wb["Programas"]
put(P, "B3", "Lo que el programa suma a 2025 y lo que se reasigna dentro del gasto flexible. La obra vecinal no está "
    "acá: no es gasto adicional.", font(9, italic=True, color=GRAY))
put(P, "B8", "Año del programa", font(9))
put(P, "B9", "Empleo y vivienda · lo que suma a 2025", font(9))
put(P, "B10", "Ambiente · reasignación", font(9))
put(P, "B11", "Educación · recomposición", font(9))
put(P, "B12", "Apoyo escolar · seis sedes", font(9))
put(P, "B13", "Habilitaciones y analítica de seguridad", font(9))
put(P, "B14", "Salud · turno digital", font(9))
put(P, "B15", "Salud · módulo de los años 1 y 2, del gasto flexible libre", font(9))
put(P, "B16", "Contrapartida · reasignación desde el gasto flexible", font(9))
put(P, "B20", "TOTAL PROGRAMAS: lo único que suma al gasto", font(9, True), fill=F_TOT)
for m in MESES:
    X, y = col(m), anio(m)
    k = y + 1
    P[f"{X}8"] = k
    P[f"{X}8"].font = font(9)
    P[f"{X}8"].number_format = "0"
    P[f"{X}10"] = f"=(Supuestos!$C$52*Supuestos!$C$127-Supuestos!$C$51)*MIN(MAX(({m}-12)/24,0),1)/12"
    P[f"{X}11"] = f"=Supuestos!$C$53*IF({m}>=12,1,0)/12"
    if HAB_MODO == "anual":
        P[f"{X}13"] = f"=Supuestos!$C$54*{X}7/12"
    else:   # inversion inicial: 60% el anio 1, 40% el anio 2; y el mantenimiento sobre lo ya invertido
        P[f"{X}13"] = (f"=Supuestos!$C$54*{[0.6, 0.4, 0, 0, 0, 0, 0, 0][y]}/12"
                       f"+Supuestos!$C$54*Supuestos!$C$57*{[0, 0.6, 1, 1, 1, 1, 1, 1][y]}/12")
    P[f"{X}15"] = f"=IF({X}8<=Supuestos!$C$152,{X}27*Supuestos!$C$150*(1-Supuestos!$C$151),0)"
    P[f"{X}16"] = f"=-({X}10+{X}11+{X}12+{X}13+{X}15)"
    P[f"{X}20"] = f"=SUM({X}9:{X}15)+{X}16"
    for rr in (10, 11, 13, 15, 16):
        P[f"{X}{rr}"].number_format = FMT_M
        P[f"{X}{rr}"].font = font(9)

# bloque nuevo: empleo y vivienda, abierto, y la formacion
for rr in range(22, 45):
    clear_row(P, rr)
put(P, "B22", "Sólo empleo y vivienda suman al gasto: se pagan con la base de valuación. Ambiente, educación, apoyo "
    "escolar, habilitaciones y el módulo de salud se pagan moviendo partidas dentro del gasto flexible: entran en su "
    "función de destino y salen de los tres programas que ceden (cuadro 15), así que el gasto total no cambia.",
    font(8, italic=True, color=GRAY))
put(P, "B23", "Ambiente empieza a moverse en el mes 12 y llega al 1,5% en el mes 36; educación se recompone desde el "
    "mes 12 (6.4). Apoyo escolar abre dos sedes por año y habilitaciones sigue la rampa: son supuestos de este libro.",
    font(8, italic=True, color=GRAY))
put(P, "B25", "EMPLEO Y VIVIENDA, ABIERTOS (cuadro 33)", font(9, True), fill=F_SEC)
lab2 = {27: "Empleo y vivienda · total del mes",
        28: "Empleo: 60%, gasto corriente",
        29: "Vivienda y servicios básicos: 40%, gasto de capital",
        30: "Empleo · lo que suma a 2025",
        31: "Vivienda · lo que suma a 2025",
        32: "Formación, con la intermediación adentro",
        33: "Contratación de desarrollos",
        35: "LA FORMACIÓN: DOS INGRESOS POR AÑO, DOS AÑOS CADA UNO",
        36: "Entran",
        37: "Egresan",
        38: "Egresados acumulados",
        39: "Pasantes en el Municipio: los primeros seis meses",
        40: "Pasantes en empresas del partido: los segundos seis meses",
        41: "Margen contra el tope del Municipio",
        43: "El año 1 y el 2 la formación usa toda la partida de empleo; desde el 3, el 60%. Cada año entran lo que paga "
            "formación dividido por 3 M, mitad en cada ingreso: 231 y 231, 412 y 412, 355 y 356, y 464 y 464. Egresan "
            "24 meses después: 1.286 en el mandato."}
for rr, t in lab2.items():
    if rr == 35:
        put(P, f"B{rr}", t, font(9, True), fill=F_SEC)
    elif rr == 43:
        put(P, f"B{rr}", t, font(8, italic=True, color=GRAY))
    elif rr in (38,):
        put(P, f"B{rr}", t, font(9, True))
    else:
        put(P, f"B{rr}", t, font(9))
for m in MESES:
    X, y = col(m), anio(m)
    moy = mes_del_anio(m)
    prev = col(m - 1) if m > 1 else None
    P[f"{X}27"] = f"=Supuestos!$C$49/12+{X}9"
    P[f"{X}28"] = f"={X}27*Supuestos!$C$150"
    P[f"{X}29"] = f"={X}27*(1-Supuestos!$C$150)"
    P[f"{X}30"] = f"={X}28-Supuestos!$C$147/12"
    P[f"{X}31"] = f"={X}29-Supuestos!$C$148/12"
    P[f"{X}32"] = f"={X}28*IF({X}8<=Supuestos!$C$152,1,Supuestos!$C$151)"
    P[f"{X}33"] = f"={X}28-{X}32"
    per = f"ROUND({X}32*12/Supuestos!$C$153,0)"
    P[f"{X}36"] = (f"=IF({moy}=Supuestos!$C$154,INT({per}/2),IF({moy}=Supuestos!$C$155,{per}-INT({per}/2),0))")
    P[f"{X}37"] = f"=IF({m}>Supuestos!$C$156,OFFSET({X}36,0,-Supuestos!$C$156),0)"
    P[f"{X}38"] = f"={X}37" if m == 1 else f"={prev}38+{X}37"
    P[f"{X}39"] = f"=IF({m}>=13,SUM(OFFSET({X}36,0,-MIN(17,{m}-1),1,MIN(6,{m}-12))),0)"
    P[f"{X}40"] = f"=IF({m}>=19,SUM(OFFSET({X}36,0,-MIN(23,{m}-1),1,MIN(6,{m}-18))),0)"
    P[f"{X}41"] = f"=Supuestos!$C$157-{X}39"
    for rr in range(27, 34):
        P[f"{X}{rr}"].number_format = FMT_M
        P[f"{X}{rr}"].font = font(9)
    for rr in range(36, 42):
        P[f"{X}{rr}"].number_format = FMT_N
        P[f"{X}{rr}"].font = font(9, bold=(rr == 38))

# ======================================================================
# VECINAL: el 1,5% que paga el funcionamiento
# ======================================================================
V = wb["Vecinal"]
put(V, "B12", "Funcionamiento del sistema: 1,5% de la partida, dentro de ella", font(9))
for m in MESES:
    X = col(m)
    V[f"{X}12"] = f"={X}10*Supuestos!$C$185"
    V[f"{X}12"].number_format = FMT_M
    V[f"{X}12"].font = font(9)

for rr in range(27, 38):
    clear_row(V, rr, 2, 8)
put(V, "B27", "CUPOS DE FORMACIÓN POR ZONA · EXACTOS A 928 POR EL RESTO MAYOR (5.3)", font(9, True), fill=F_SEC)
put(V, "B28", "Cupos por año, en régimen", font(9))
put(V, "C28", 928, font(9, color=BLUE), FMT_N)
put(V, "D28", "Lo que compran los 2.783,1 M de formación a 3 M por persona", font(8, italic=True, color=GRAY))
for cc, t in zip("BCDEFG", ("ZONA", "ÍNDICE", "CUOTA", "ENTERA", "RESTO", "CUPOS")):
    put(V, f"{cc}29", t, font(8, True, color="FFFFFFFF"), fill=F_HDR, align="center")
for i in range(6):
    rr, zz = 30 + i, 16 + i
    put(V, f"B{rr}", f"=B{zz}", font(9, color=GREEN))
    put(V, f"C{rr}", f"=D{zz}", font(9, color=GREEN), "0.000000")
    put(V, f"D{rr}", f"=$C$28*C{rr}", font(9), "0.000")
    put(V, f"E{rr}", f"=INT(D{rr})", font(9), FMT_N)
    put(V, f"F{rr}", f"=D{rr}-E{rr}", font(9), "0.000")
    put(V, f"G{rr}", f"=E{rr}+IF(RANK(F{rr},$F$30:$F$35,0)<=$C$28-SUM($E$30:$E$35),1,0)", font(9, True), FMT_N)
put(V, "B36", "TOTAL", font(9, True), fill=F_TOT)
for cc in "CDEG":
    put(V, f"{cc}36", f"=SUM({cc}30:{cc}35)", font(9, True), FMT_N if cc in "EG" else "0.000", fill=F_TOT)
put(V, "B37", "Cada zona recibe la parte entera de su cuota; las vacantes que faltan para 928 van a los restos "
    "mayores. Da Boulogne 315, Béccar 307, Martínez 98, San Isidro 96, Villa Adelina 94 y Acassuso 18.",
    font(8, italic=True, color=GRAY))

# ======================================================================
# DEUDA: la del 31/12/2025 llega a cero en 2029; el bono, en cuotas trimestrales
# ======================================================================
D = wb["Deuda"]
put(D, "B3", "Sin nuevo endeudamiento. La deuda al 31/12/2025 se amortiza como en el modelo del repo; el bono 2026 "
    "va aparte, debajo de la línea.", font(9, italic=True, color=GRAY))
put(D, "B8", "Stock al inicio: la deuda al 31/12/2025 que queda y el bono 2026", font(9))
put(D, "B9", "Amortización del mes", font(9))
put(D, "B13", "Deuda flotante por rezago de pago · al inicio", font(9))
put(D, "B18", "Margen contra el tope del artículo 193 de la Constitución provincial", font(9))
for rr in range(24, 31):
    clear_row(D, rr)
put(D, "B24", "LA DEUDA AL 31/12/2025 Y EL BONO 2026, POR SEPARADO", font(9, True), fill=F_SEC)
for rr, t in {25: "Deuda al 31/12/2025 · stock al inicio del mes",
              26: "Deuda al 31/12/2025 · amortización del mes",
              27: "Deuda al 31/12/2025 · stock al cierre",
              28: "Bono 2026 · capital pendiente al inicio del mes",
              29: "Bono 2026 · cuota de capital",
              30: "Bono 2026 · capital pendiente al cierre"}.items():
    put(D, f"B{rr}", t, font(9, bold=rr in (27, 30)))
for m in MESES:
    X, y = col(m), anio(m)
    n = y + 3
    prev = col(m - 1) if m > 1 else None
    D[f"{X}25"] = ("=Supuestos!$C$59-Supuestos!$C$61-(Supuestos!$C$59-Supuestos!$C$61)/Supuestos!$C$64"
                   if m == 1 else f"={prev}27")
    D[f"{X}26"] = (f"=IF(AND({n}>=2,{n}<=1+Supuestos!$C$64),"
                   f"MIN({X}25,(Supuestos!$C$59-Supuestos!$C$61)/Supuestos!$C$64/12),0)")
    D[f"{X}27"] = f"={X}25-{X}26"
    D[f"{X}28"] = "=Supuestos!$C$104" if m == 1 else f"={prev}30"
    D[f"{X}29"] = f"=IF(MOD({m}-(Supuestos!$C$103-16),3)=0,MIN({X}28,Supuestos!$C$100/Supuestos!$C$102),0)"
    D[f"{X}30"] = f"={X}28-{X}29"
    D[f"{X}8"] = f"={X}25+{X}28" if m == 1 else f"={prev}11"
    D[f"{X}9"] = f"={X}26+{X}29"
    D[f"{X}13"] = "=0" if m == 1 else f"={prev}15"
    for rr in range(25, 31):
        D[f"{X}{rr}"].number_format = FMT_M
        D[f"{X}{rr}"].font = font(9, bold=rr in (27, 30))
put(D, "B20", "La deuda al 31/12/2025 —8.960 M, consolidada y flotante— se amortiza como en el modelo del repo: "
    "3.388 M en 2026 y el resto en partes iguales en 2027, 2028 y 2029. Llega a cero en 2029 (3.5). La flotante que "
    "aparece acá es la que genera el rezago de pago de este libro.", font(8, italic=True, color=GRAY))
put(D, "B22", "El bono de 30.000 M de agosto de 2026 entra con sus siete cuotas pendientes del 12,5%: febrero, mayo, "
    "agosto y noviembre de 2028, y febrero, mayo y agosto de 2029. Va debajo de la línea: no cambia el resultado. "
    "Su interés no se proyecta, porque la tasa es nominal y variable (TAMAR más 7) y el modelo está en pesos constantes (3.6).",
    font(8, italic=True, color=GRAY))

# ======================================================================
# GASTOS OBJETO: etiquetas; la cuenta oficial va en Resumen anual
# ======================================================================
G = wb["Gastos objeto"]
put(G, "B14", "6 · Activos financieros · debajo de la línea", font(9))
put(G, "B15", "7 · Deuda: amortización del stock y del bono · debajo de la línea", font(9))
put(G, "B16", "Programas del capítulo 5: lo que suma empleo y vivienda", font(9))

# ======================================================================
# GASTOS FUNCION: bases de la ejecucion 2025 y la reasignacion con contrapartida
# ======================================================================
GF = wb["Gastos función"]
BASES = {8: "C189", 9: "C191", 10: "C192", 11: "C193", 12: "C190+Supuestos!$C$194", 13: "C195",
         14: "C196", 15: "C197", 16: "C198", 17: "C199", 18: "C200", 19: "C201", 20: "C202",
         21: "C203", 22: "C204", 23: "C205", 24: "C206"}
EXTRA = {14: "+Programas!{X}$14+Programas!{X}$15", 16: "+Programas!{X}$11+Programas!{X}$12",
         18: "+Programas!{X}$30", 19: "+Programas!{X}$31", 23: "+Programas!{X}$10"}
for rr in range(26, 34):
    clear_row(GF, rr)
put(GF, "B26", "Habilitaciones y analítica de seguridad · reasignación", font(9))
put(GF, "B27", "Contrapartida: mantenimiento y embellecimiento, infraestructura deportiva y arbolado", font(9))
put(GF, "B28", "TOTAL POR FUNCIÓN", font(9, True), fill=F_TOT)
put(GF, "B30", "Memo · salud como % del gasto por función", font(8, italic=True, color=GRAY))
put(GF, "B31", "Memo · agua y cloaca contra alumbrado (dentro de urbanismo)", font(8, italic=True, color=GRAY))
put(GF, "B33", "La apertura por función usa la ejecución 2025 de cada una (Supuestos, bloque S) y le suma, en su "
    "función de destino, lo que suma empleo y vivienda y cada reasignación; lo que ceden los tres programas de "
    "origen va en su propia fila, porque la ejecución no dice en qué función está cada uno. El alumbrado es el "
    "14,67% de Urbanismo según el cuadro 5.", font(8, italic=True, color=GRAY))
for m in MESES:
    X, y = col(m), anio(m)
    n = y + 3
    for rr, b in BASES.items():
        extra = EXTRA.get(rr, "").format(X=X)
        base = "+".join(("Supuestos!$C$" + p[1:]) if not p.startswith("Supuestos") else p
                        for p in b.split("+"))
        GF[f"{X}{rr}"] = f"=({base})*(1+Supuestos!$C$36)^{n}*Estacionalidad!{est(m)}$13{extra}"
    GF[f"{X}25"] = f"=Deuda!{X}$9"
    GF[f"{X}26"] = f"=Programas!{X}$13"
    GF[f"{X}27"] = f"=Programas!{X}$16"
    GF[f"{X}28"] = f"=SUM({X}8:{X}27)"
    GF[f"{X}30"] = f"=IFERROR({X}14/{X}28,0)"
    GF[f"{X}31"] = f"=IFERROR({X}20/({X}21*0.1467),0)"
    for rr in (26, 27):
        GF[f"{X}{rr}"].number_format = FMT_M
        GF[f"{X}{rr}"].font = font(9)
    GF[f"{X}28"].number_format = FMT_M
    GF[f"{X}28"].font = font(9, True)
    GF[f"{X}28"].fill = F_TOT
    for rr in (30, 31):
        GF[f"{X}{rr}"].number_format = FMT_PCT1
        GF[f"{X}{rr}"].font = font(8, italic=True, color=GRAY)

# ======================================================================
# FLUJO MENSUAL: origen y procedencia, deuda en dos filas, cuenta oficial
# ======================================================================
FM = wb["Flujo mensual"]
put(FM, "B14", "      11 · Origen municipal — libre disponibilidad", font(9))
put(FM, "B15", "      11 · Origen municipal — afectados", font(9))
put(FM, "B16", "      21 · Origen provincial — libre disponibilidad", font(9))
put(FM, "B17", "      21 · Origen provincial — afectados", font(9))
put(FM, "B18", "      31 y 41 · Nacional, afectado, y otros orígenes, de libre disponibilidad", font(9))
put(FM, "B25", "      Amortización de la deuda al 31/12/2025", font(9))
put(FM, "B26", "      Amortización del bono 2026", font(9))
put(FM, "B59", "VIII · MEMO · CUENTA AHORRO-INVERSIÓN, COMO LA OFICIAL", font(9, True), fill=F_SEC)
FM["B65"].value = FM["B65"].value.replace("con plata que no le corresponde", "con dinero que no le corresponde")
assert "plata" not in FM["B65"].value
put(FM, "B60", "      Ingresos corrientes percibidos", font(9))
put(FM, "B61", "      Gastos corrientes devengados", font(9))
put(FM, "B63", "VIII · Resultado financiero: sin deuda ni activos financieros, que van debajo de la línea", font(9, True))
for m in MESES:
    X, e = col(m), est(m)
    FM[f"{X}14"] = f"=(Recursos!{X}8+Recursos!{X}9+Recursos!{X}16)*Supuestos!$C$74"
    FM[f"{X}15"] = f"=(Recursos!{X}8+Recursos!{X}9+Recursos!{X}16)*(1-Supuestos!$C$74)"
    FM[f"{X}16"] = f"=(Recursos!{X}10+Recursos!{X}11)*Supuestos!$C$75"
    FM[f"{X}17"] = f"=(Recursos!{X}10+Recursos!{X}11)*(1-Supuestos!$C$75)"
    FM[f"{X}18"] = f"=Recursos!{X}12"
    FM[f"{X}25"] = f"=Deuda!{X}26"
    FM[f"{X}26"] = f"=Deuda!{X}29"
    FM[f"{X}48"] = (f"={X}9*0.5+({X}15+{X}17+{X}18*Supuestos!$C$116/(Supuestos!$C$116+Supuestos!$C$117)"
                    f"*(1-Supuestos!$C$76))*0.5")
    FM[f"{X}60"] = f"=Recursos!{X}13"
    FM[f"{X}61"] = (f"='Gastos objeto'!{X}8+'Gastos objeto'!{X}9+'Gastos objeto'!{X}10+'Gastos objeto'!{X}11"
                    f"+'Gastos objeto'!{X}13-Supuestos!$C$126*Estacionalidad!{e}$15+Programas!{X}30")
    FM[f"{X}62"] = f"={X}60-{X}61"
    FM[f"{X}63"] = f"=Recursos!{X}20-('Gastos objeto'!{X}17-'Gastos objeto'!{X}14-'Gastos objeto'!{X}15)"

# ======================================================================
# RESUMEN ANUAL: la cuenta Ahorro-Inversion, como la oficial, y los controles
# ======================================================================
RA = wb["Resumen anual"]
for rr in range(7, 90):
    clear_row(RA, rr)
put(RA, "B3", "Los cuatro años del mandato y los cuatro siguientes, con el programa. Pesos constantes de diciembre "
    "de 2025. Ingresos por lo percibido y gastos por lo devengado, como la cuenta oficial.",
    font(9, italic=True, color=GRAY))


def ra_label(r, t, kind="n"):
    if kind == "sec":
        put(RA, f"B{r}", t, font(9, True), fill=F_SEC)
    elif kind == "tot":
        put(RA, f"B{r}", t, font(9, True))
    elif kind == "gtot":
        put(RA, f"B{r}", t, font(9, True), fill=F_TOT)
    elif kind == "memo":
        put(RA, f"B{r}", t, font(8, italic=True, color=GRAY))
    else:
        put(RA, f"B{r}", t, font(9))


def ra_row(r, t, fx, kind="n", fmt=FMT_M, link=True):
    ra_label(r, t, kind)
    for y in ANIOS:
        a, b = rango_anio(y)
        c = COL_ANIO[y]
        RA[f"{c}{r}"] = "=" + fx(a, b, c, y)
        bold = kind in ("tot", "gtot")
        colr = GREEN if (link and kind == "n") else None
        RA[f"{c}{r}"].font = font(9, bold, color=colr) if kind != "memo" else font(8, italic=True, color=GRAY)
        RA[f"{c}{r}"].number_format = fmt
        if kind == "gtot":
            RA[f"{c}{r}"].fill = F_TOT


ra_label(7, "I · INGRESOS CORRIENTES (percibido)", "sec")
ra_row(8, "Origen municipal: tasas, derechos y rentas", lambda a, b, c, y: f"SUM(Recursos!{a}8:{b}8)")
ra_row(9, "Base de valuación actualizada: lo cobrado", lambda a, b, c, y: f"SUM(Recursos!{a}9:{b}9)")
ra_row(10, "Origen provincial", lambda a, b, c, y: f"SUM(Recursos!{a}10:{b}11)")
ra_row(11, "Origen nacional y otros orígenes", lambda a, b, c, y: f"SUM(Recursos!{a}12:{b}12)")
ra_row(12, "Total ingresos corrientes", lambda a, b, c, y: f"SUM({c}8:{c}11)", "tot")
ra_row(13, "IV · Recursos de capital", lambda a, b, c, y: f"SUM(Recursos!{a}16:{b}16)")
ra_row(14, "VI · INGRESOS TOTALES", lambda a, b, c, y: f"{c}12+{c}13", "gtot")
ra_label(16, "II · GASTOS CORRIENTES (devengado)", "sec")
ra_row(17, "Personal y aguinaldo", lambda a, b, c, y: f"SUM('Gastos objeto'!{a}8:{b}9)")
ra_row(18, "Bienes de consumo", lambda a, b, c, y: f"SUM('Gastos objeto'!{a}10:{b}10)")
ra_row(19, "Servicios no personales", lambda a, b, c, y: f"SUM('Gastos objeto'!{a}11:{b}11)")
ra_row(20, "Transferencias corrientes", lambda a, b, c, y: f"SUM('Gastos objeto'!{a}13:{b}13)-Supuestos!$C$126")
ra_row(21, "Empleo: lo que suma el programa", lambda a, b, c, y: f"SUM(Programas!{a}30:{b}30)")
ra_row(22, "Total gastos corrientes", lambda a, b, c, y: f"SUM({c}17:{c}21)", "tot")
ra_label(23, "V · GASTOS DE CAPITAL (devengado)", "sec")
ra_row(24, "Bienes de uso: obra pública", lambda a, b, c, y: f"SUM('Gastos objeto'!{a}12:{b}12)")
ra_row(25, "  de la cual, decidida por los vecinos", lambda a, b, c, y: f"SUM(Vecinal!{a}10:{b}10)")
ra_row(26, "Transferencias de capital", lambda a, b, c, y: "Supuestos!$C$126")
ra_row(27, "Vivienda: lo que suma el programa", lambda a, b, c, y: f"SUM(Programas!{a}31:{b}31)")
ra_row(28, "Total gastos de capital", lambda a, b, c, y: f"{c}24+{c}26+{c}27", "tot")
ra_row(29, "VII · GASTOS TOTALES", lambda a, b, c, y: f"{c}22+{c}28", "gtot")
ra_label(31, "RESULTADO", "sec")
ra_row(32, "III · Ahorro corriente", lambda a, b, c, y: f"{c}12-{c}22", "tot")
ra_row(33, "VIII · Resultado financiero", lambda a, b, c, y: f"{c}14-{c}29", "gtot")
ra_label(35, "DEBAJO DE LA LÍNEA: NO ES GASTO EN LA CUENTA OFICIAL", "sec")
ra_row(36, "Amortización de la deuda al 31/12/2025", lambda a, b, c, y: f"SUM(Deuda!{a}26:{b}26)")
ra_row(37, "Amortización del bono 2026", lambda a, b, c, y: f"SUM(Deuda!{a}29:{b}29)")
ra_row(38, "Activos financieros", lambda a, b, c, y: f"SUM('Gastos objeto'!{a}14:{b}14)")
ra_row(39, "Flujo de caja del ejercicio", lambda a, b, c, y: f"SUM('Flujo mensual'!{a}46:{b}46)")
ra_row(40, "Saldo de caja al cierre", lambda a, b, c, y: f"'Flujo mensual'!{b}49")
ra_row(41, "Deuda al 31/12/2025 que queda, al cierre", lambda a, b, c, y: f"Deuda!{b}27")
ra_row(42, "Bono 2026: capital pendiente al cierre", lambda a, b, c, y: f"Deuda!{b}30")
ra_row(43, "Deuda flotante por rezago de pago, al cierre", lambda a, b, c, y: f"Deuda!{b}15")
ra_label(45, "INDICADORES", "sec")
ra_row(46, "Percepción sobre lo facturado",
       lambda a, b, c, y: f"SUM(Recursos!{a}13:{b}13)/(SUM(Recursos!{a}13:{b}13)+SUM(Recursos!{a}22:{b}22))",
       fmt=FMT_PCT2)
ra_row(47, "Obra vecinal / obra total", lambda a, b, c, y: f"IFERROR({c}25/{c}24,0)", fmt=FMT_PCT1, link=False)
ra_row(48, "Obra vecinal / gasto devengado de 2025", lambda a, b, c, y: f"IFERROR({c}25/Supuestos!$C$127,0)",
       fmt=FMT_PCT1)
ra_row(49, "Resultado financiero / ingresos totales", lambda a, b, c, y: f"IFERROR({c}33/{c}14,0)",
       fmt=FMT_PCT1, link=False)
ra_row(50, "Rigidez del gasto, en junio", lambda a, b, c, y: f"'Gastos objeto'!{col(12 * y + 6)}26", fmt=FMT_PCT1)
ra_row(51, "Salud / gasto por función, en junio", lambda a, b, c, y: f"'Gastos función'!{col(12 * y + 6)}30",
       fmt=FMT_PCT1)
ra_row(52, "Empleo y vivienda, total anual", lambda a, b, c, y: f"SUM(Programas!{a}27:{b}27)")
ra_row(53, "Lo que el programa suma al gasto", lambda a, b, c, y: f"SUM(Programas!{a}9:{b}9)")
ra_row(54, "Egresados de la formación en el año", lambda a, b, c, y: f"SUM(Programas!{a}37:{b}37)", fmt=FMT_N)

# control 1: el anio base
put(RA, "B56", "CONTROL · EL AÑO BASE REPRODUCE LA EJECUCIÓN 2025", font(9, True), fill=F_SEC)
for cc, t in (("C", "Ejecución 2025"), ("D", "El modelo, en 2025"), ("E", "Diferencia")):
    put(RA, f"{cc}56", t, font(8, True, color="FFFFFFFF"), fill=F_HDR, align="center")
ctrl = [
    (57, "I · Ingresos corrientes: los cuatro orígenes, con su estacionalidad", "Supuestos!C121",
     "Supuestos!C114*SUM(Estacionalidad!C6:N6)+Supuestos!C115*SUM(Estacionalidad!C7:N7)"
     "+(Supuestos!C116+Supuestos!C117)*SUM(Estacionalidad!C8:N8)"),
    (58, "I · Ingresos corrientes: los rubros de la ejecución", "Supuestos!C121",
     "Supuestos!C7+Supuestos!C9+Supuestos!C10+Supuestos!C11"),
    (59, "IV · Recursos de capital", "Supuestos!C122", "Supuestos!C12*SUM(Estacionalidad!C9:N9)"),
    (60, "II · Gastos corrientes: los objetos, con su estacionalidad", "Supuestos!C123",
     "Supuestos!C15*(12/13*SUM(Estacionalidad!C10:N10)+1/13*SUM(Estacionalidad!C11:N11))"
     "+Supuestos!C17*SUM(Estacionalidad!C12:N12)+Supuestos!C19*SUM(Estacionalidad!C13:N13)"
     "+Supuestos!C23*SUM(Estacionalidad!C15:N15)-Supuestos!C126"),
    (61, "V · Gastos de capital", "Supuestos!C124",
     "Supuestos!C21*SUM(Estacionalidad!C14:N14)+Supuestos!C126"),
    (62, "Gasto total por objeto, sin deuda ni activos financieros", "Supuestos!C123+Supuestos!C124",
     "Supuestos!C15+Supuestos!C17+Supuestos!C19+Supuestos!C21+Supuestos!C23"),
    (63, "Gasto por función, sin la deuda", "Supuestos!C123+Supuestos!C124", "Supuestos!C208-Supuestos!C207"),
    (64, "VIII · Resultado financiero", "Supuestos!C125", "D57+D59-D60-D61"),
]
for r, t, oficial, modelo in ctrl:
    put(RA, f"B{r}", t, font(9))
    put(RA, f"C{r}", "=" + oficial, font(9, color=GREEN), FMT_M)
    put(RA, f"D{r}", "=" + modelo, font(9), FMT_M)
    put(RA, f"E{r}", f"=ROUND(D{r}-C{r},2)", font(9, True), FMT_P)

# control 2: los mismos numeros que el modelo del repo
REPO_BASE = [float(_mod[("base", 2028 + y)]["resultado_financiero"]) for y in ANIOS]
REPO_VAL = [float(_mod[("reformista_valuacion", 2028 + y)]["resultado_financiero"]) for y in ANIOS]
REPO_GT_VAL = [float(_mod[("reformista_valuacion", 2028 + y)]["gastos_totales"]) for y in ANIOS]
put(RA, "B66", "CONTROL · LOS MISMOS NÚMEROS QUE EL MODELO DEL REPO (data/modelo_flujo_caja.csv)", font(9, True),
    fill=F_SEC)
filas = [
    (67, "Repo · resultado si nada cambia (escenario base)", REPO_BASE, None),
    (68, "Este libro · resultado si nada cambia", None, "Escenarios!{c}6"),
    (69, "Diferencia", None, "ROUND({c}68-{c}67,0)"),
    (70, "Repo · resultado con el programa (reformista_valuacion)", REPO_VAL, None),
    (71, "Este libro · resultado con el programa", None, "{c}33"),
    (72, "Diferencia", None, "ROUND({c}71-{c}70,0)"),
    (73, "Repo · gastos totales con el programa", REPO_GT_VAL, None),
    (74, "Este libro · gastos totales", None, "{c}29"),
    (75, "Diferencia", None, "ROUND({c}74-{c}73,0)"),
]
for r, t, vals, fx in filas:
    put(RA, f"B{r}", t, font(9, bold=t == "Diferencia"))
    for y in ANIOS:
        c = COL_ANIO[y]
        if vals is not None:
            put(RA, f"{c}{r}", vals[y], font(9, color=BLUE), FMT_M)
        else:
            put(RA, f"{c}{r}", "=" + fx.format(c=c), font(9, bold=t == "Diferencia"),
                FMT_P if t == "Diferencia" else FMT_M)
put(RA, "B77", "Las filas azules son el resultado del modelo del repo con los supuestos del documento, copiado de "
    "data/modelo_flujo_caja.csv. Las diferencias dan cero mientras los supuestos sean los del documento: si se "
    "mueve una palanca, se separan.", font(8, italic=True, color=GRAY))
put(RA, "B78", "El programa suma 7.225,2 M por año en régimen y la base de valuación cobra 7.225,2 M: por eso desde "
    "2031 el resultado es el mismo con y sin programa. Los tres primeros años la base cobra más de lo que pide la "
    "rampa (cuadro 20).", font(8, italic=True, color=GRAY))

# ======================================================================
# ESCENARIOS: los dos del documento y la sensibilidad
# ======================================================================
ES = wb["Escenarios"]
for rr in range(1, 40):
    clear_row(ES, rr)
put(ES, "B2", "ESCENARIOS · SI NADA CAMBIA Y CON EL PROGRAMA, Y LA SENSIBILIDAD", font(13, True, color=WINE))
put(ES, "B3", "Resultado financiero de cada año, en pesos de diciembre de 2025: es la comparación del cuadro 20. "
    "Se recalcula solo al cambiar Supuestos.", font(9, italic=True, color=GRAY))
put(ES, "B5", "ESCENARIO", font(8, True, color="FFFFFFFF"), fill=F_HDR, align="center")
for y in ANIOS:
    put(ES, f"{COL_ANIO[y]}5", str(2028 + y), font(8, True, color="FFFFFFFF"), fill=F_HDR, align="center")
put(ES, "B6", "Si nada cambia", font(9, True))
put(ES, "B7", "Con el programa, pagado con la base de valuación", font(9, True))
put(ES, "B8", "Diferencia", font(9))
put(ES, "B9", "Diferencia si el mínimo frena subas", font(9))
for y in ANIOS:
    c = COL_ANIO[y]
    a, b = rango_anio(y)
    kk = min(y + 1, 4)
    put(ES, f"{c}6", f"='Resumen anual'!{c}33-('Resumen anual'!{c}9-'Resumen anual'!{c}53)", font(9, True, color=GREEN), FMT_M)
    put(ES, f"{c}7", f"='Resumen anual'!{c}33", font(9, True, color=GREEN), FMT_M)
    put(ES, f"{c}8", f"={c}7-{c}6", font(9), FMT_M1)
    put(ES, f"{c}9", f"=Supuestos!$C${137 + kk}*Recursos!{a}18-'Resumen anual'!{c}53", font(9), FMT_M1)
put(ES, "B10", "Los dos escenarios tienen los mismos supuestos de recaudación propia y de coparticipación: lo único "
    "que cambia es el programa y lo que cobra la base de valuación. El programa empieza en 2028. Desde 2031 lo cobrado "
    "y lo gastado se igualan; la última fila supone que el mínimo de la tasa frena todas las subas de lotes chicos (3.5).",
    font(8, italic=True, color=GRAY))

put(ES, "B12", "SENSIBILIDAD · RESULTADO DE 2031 SI NADA CAMBIA (3.2, 3.6 y gráfico 19)", font(9, True), fill=F_SEC)
for cc, t in (("B", "VARIABLE"), ("C", "VARIANTE"), ("D", "RESULTADO 2031"), ("E", "CONTRA EL BASE"),
              ("F", "LO QUE MUEVE")):
    put(ES, f"{cc}13", t, font(8, True, color="FFFFFFFF"), fill=F_HDR, align="center")
BASE31 = "$F$6"
IC31 = "('Resumen anual'!$F$12-'Resumen anual'!$F$9)"
sens = [
    (14, "Lo que recauda el Municipio: crecimiento real anual", 0.0095,
     "=" + BASE31 + "+Supuestos!$C$114*((1+C{r})^6-(1+Supuestos!$C$31)^6)",
     "Un punto menos por año: el mandato termina en déficit (3.6)"),
    (15, "", "=Supuestos!C31", None, "El valor del documento: 1,95%"),
    (16, "", 0.0295, "=" + BASE31 + "+Supuestos!$C$114*((1+C{r})^6-(1+Supuestos!$C$31)^6)", ""),
    (17, "La coparticipación: caída real anual", -0.015,
     "=" + BASE31 + "+Supuestos!$C$115*Supuestos!$C$118*((1+C{r})^6-(1+Supuestos!$C$32)^6)",
     "Lo único de los tres que no depende del Municipio"),
    (18, "", -0.025, "=" + BASE31 + "+Supuestos!$C$115*Supuestos!$C$118*((1+C{r})^6-(1+Supuestos!$C$32)^6)", ""),
    (19, "", -0.035, "=" + BASE31 + "+Supuestos!$C$115*Supuestos!$C$118*((1+C{r})^6-(1+Supuestos!$C$32)^6)",
     "Si cae 3,5% por año, 2031 queda en +5.514 M (3.2)"),
    (20, "Qué parte de lo facturado se cobra", 0.8632,
     "=" + BASE31 + "+" + IC31 + "*(C{r}/Supuestos!$C$34-1)", "Tres puntos menos: −292 M en 2031 (3.6)"),
    (21, "", "=Supuestos!C34", None, "La de 2025: 89,32%"),
    (22, "", 0.9232, "=" + BASE31 + "+" + IC31 + "*(C{r}/Supuestos!$C$34-1)", ""),
]
for r, lab, var, fx, nota in sens:
    put(ES, f"B{r}", lab, font(9, bold=bool(lab)))
    if isinstance(var, str):
        put(ES, f"C{r}", var, font(9, color=GREEN), FMT_PCT2)
        put(ES, f"D{r}", "=" + BASE31, font(9), FMT_M)
    else:
        put(ES, f"C{r}", var, font(9, color=BLUE), FMT_PCT2)
        put(ES, f"D{r}", fx.format(r=r), font(9), FMT_M)
    put(ES, f"E{r}", f"=D{r}-{BASE31}", font(9), FMT_M)
    if nota:
        put(ES, f"F{r}", nota, font(8, italic=True, color=GRAY), wrap=True)
put(ES, "B24", "Cada variable se mueve sola, con las otras dos en su valor de hoy, como en el modelo del repo "
    "(data/sensibilidad.csv, que también da 2037; este libro llega a 2035). Las variantes azules se pueden cambiar.",
    font(8, italic=True, color=GRAY))
put(ES, "B25", "El bono de 2026 no está en la sensibilidad: para 2031 ya está pagado, y su tasa es nominal y "
    "variable (3.6).", font(8, italic=True, color=GRAY))
ES.column_dimensions["B"].width = 48
ES.column_dimensions["F"].width = 60
for cc in "CDE":
    ES.column_dimensions[cc].width = 15
for cc in "GHIJ":
    ES.column_dimensions[cc].width = 15

# ======================================================================
# METAS: las trece del 6.3
# ======================================================================
MT = wb["Metas"]
for rr in range(1, 40):
    clear_row(MT, rr)
put(MT, "B2", "LAS TRECE METAS DEL MANDATO (6.3)", font(13, True, color=WINE))
put(MT, "B3", "Línea de base de hoy, lo que proyecta este libro donde lo hay y la fuente pública que la comprueba.",
    font(9, italic=True, color=GRAY))
for cc, t in (("B", "META"), ("C", "LÍNEA DE BASE"), ("D", "AÑO 4 · 2031"), ("E", "AÑO 8 · 2035"),
              ("F", "FUENTE DE VERIFICACIÓN")):
    put(MT, f"{cc}5", t, font(8, True, color="FFFFFFFF"), fill=F_HDR, wrap=True, align="center")
NP = "No la proyecta el modelo"
metas = [
    ("Reducir a la mitad los hogares sin cloacas en Boulogne y Béccar", "4.616 hogares (Censo 2022)",
     "Depende de ejecución", "—", "Registro de conexiones y próximo censo"),
    ("Llevar el gasto conjunto en empleo y vivienda a 7.730,9 M anuales", "505,7 M (2025)",
     "='Resumen anual'!F52", "='Resumen anual'!J52", "Ejecución presupuestaria por programa"),
    ("Llevar la función ambiental al 1,5% del presupuesto", "0,4% (2025)",
     "=SUM('Gastos función'!AM23:AX23)/Supuestos!$C$127", "=SUM('Gastos función'!CI23:CT23)/Supuestos!$C$127",
     "Gastos por finalidad y función"),
    ("50% de la obra pública decidida por comisiones vecinales", "0%",
     "='Resumen anual'!F47", "='Resumen anual'!J47", "Ordenanza y ejecución presupuestaria"),
    ("Imputar el gasto municipal con referencia territorial, de modo que exista el dato de cuánto se gastó en "
     "cada zona", "El dato no existe: ningún municipio del conurbano norte lo produce", NP, NP,
     "Cuánto se gastó en cada zona: se le pregunta a la inteligencia artificial del Municipio"),
    ("La inteligencia artificial del Municipio en producción, con la partida vecinal, las asambleas transcriptas "
     "y cada dato cargado el día que ocurre", "No existe. Hoy el Municipio publica en PDF y su portal de datos "
     "abiertos devuelve error", NP, NP, "Se le pregunta a la inteligencia artificial del Municipio: cualquiera puede hacerlo"),
    ("Turno médico en línea en los tres hospitales, el odontológico y los nueve centros de atención primaria",
     "Cero efectores de salud humana con turno en línea", NP, NP, "La propia plataforma, consultable por cualquiera"),
    ("Que cada compra de insumos se compare sola contra la compra anterior y contra los otros dos hospitales, y "
     "avise cuando se sale del rango", "Hoy se publica el total del expediente, no el precio por unidad", NP, NP,
     "Se le pregunta a la inteligencia artificial del Municipio, con el histórico y las alertas"),
    ("Adjudicar el servicio de recolección de residuos por licitación pública, con el pliego discutido antes del "
     "llamado", "Dos licitaciones llamadas desde 2008 y ninguna adjudicada", NP, NP, "Boletín Oficial municipal"),
    ("Detección en vivo de hechos violentos y reconstrucción de recorrido sobre las cámaras que el Municipio ya "
     "tiene, y que cualquiera pueda preguntar cuántas órdenes judiciales se recibieron y cuántas se cumplieron",
     "No hay registro público de que ninguno de los dos usos opere", NP, NP,
     "Se le pregunta a la inteligencia artificial del Municipio: tiempo de respuesta y órdenes"),
    ("Partida presupuestaria propia para género, separada del programa que hoy comparte",
     "Género no tiene partida propia; discapacidad sí, y devengó 65,9 M en 2025", NP, NP, "Estado de ejecución por programa"),
    ("Un centro de apoyo escolar gratuito en cada una de las seis localidades", "Cero centros municipales",
     "=SUM(Programas!AM12:AX12)/Supuestos!$C$55", "=SUM(Programas!CI12:CT12)/Supuestos!$C$55",
     "Ejecución por programa; la matrícula por sede se le pregunta a la inteligencia artificial del Municipio"),
    ("La tecnicatura de dos años de la UNSO en las seis zonas, el segundo como pasante —seis meses en el Municipio "
     "y seis en una empresa del partido—: desde el mes 27 egresa una cohorte cada seis meses; 1.286 en el mandato "
     "y 928 por año en régimen; y 250 a 300 egresados con empleo pago por año. En el año 4, egresados acumulados; "
     "en el 8, egresados del año",
     "Una sede, la del Barrio La Cava", "=Programas!AX38", "=SUM(Programas!CI37:CT37)",
     "Ejecución por programa y convenios de pasantías; la matrícula por sede se le pregunta a la inteligencia "
     "artificial del Municipio; el empleo, al registro de inserción laboral"),
]
FMTS = {1: FMT_M, 2: FMT_PCT1, 3: FMT_PCT1, 11: "0", 12: FMT_N}
for i, (meta, base, a4, a8, fuente) in enumerate(metas):
    r = 6 + i
    put(MT, f"B{r}", meta, font(9), wrap=True)
    put(MT, f"C{r}", base, font(9), wrap=True)
    for cc, v in (("D", a4), ("E", a8)):
        if isinstance(v, str) and v.startswith("="):
            put(MT, f"{cc}{r}", v, font(9, color=GREEN), FMTS.get(i, "General"), align="center")
        else:
            put(MT, f"{cc}{r}", v, font(9), wrap=True, align="center")
    put(MT, f"F{r}", fuente, font(8, italic=True, color=GRAY), wrap=True)
put(MT, "B20", "Las metas que no proyecta el modelo se comprueban en su fuente: el modelo dice que hay fondos, no que "
    "la obra se haga.", font(8, italic=True, color=GRAY))
MT.column_dimensions["B"].width = 60
MT.column_dimensions["C"].width = 26
MT.column_dimensions["D"].width = 16
MT.column_dimensions["E"].width = 16
MT.column_dimensions["F"].width = 42

# ======================================================================
# GUIA: reescrita
# ======================================================================
GU = wb["Guía"]
for rr in range(1, 60):
    clear_row(GU, rr)
put(GU, "B2", "MODELO FISCAL · MUNICIPIO DE SAN ISIDRO", font(15, True, color=WINE))
put(GU, "B3", "Proyección mensual 2028–2035 · ocho ejercicios · los mismos números que el documento y que el modelo del repo",
    font(9, italic=True, color=GRAY))
guia = [
    ("QUÉ ES", "La cuenta del Municipio mes a mes para los cuatro años del mandato (2028–2031) y los cuatro "
     "siguientes, con el programa del documento aplicado. Sumada por año, da lo mismo que el modelo del repo "
     "(03_scripts/modelo.py) y que el capítulo 3: el cuadro 20, el gráfico 13 y la sensibilidad del 3.2 y el 3.6."),
    ("UNIDAD", "Pesos constantes de diciembre de 2025. Sin supuesto de inflación: todo crecimiento que aparece es real."),
    ("AÑO BASE", "2025 es la ejecución real, no una estimación: los estados de ejecución de recursos y de gastos, "
     "acumulado anual, y el Estado de Situación Económico-Financiera 2025. Reproduce la cuenta oficial con "
     "diferencia cero: el control está al pie de la hoja Resumen anual."),
    ("LA CUENTA", "Ingresos por lo percibido y gastos por lo devengado, como la cuenta Ahorro-Inversión oficial: "
     "2025 cerró en −6.051 M. La amortización de la deuda y los activos financieros van debajo de la línea, igual "
     "que en la cuenta oficial."),
    ("QUÉ CRECE", "Lo que recauda el Municipio crece 1,95% real por año. La coparticipación, el 82,4% de lo "
     "provincial, cae 2,196% por año; el resto de lo provincial, lo nacional y los recursos de capital quedan "
     "constantes. El gasto queda constante en términos reales —cero recomposición salarial y cero servicios "
     "nuevos—, salvo el programa."),
    ("EL PROGRAMA", "Empleo y vivienda pasan de 505,7 M a 7.730,9 M en cuatro años desde 2028 (25%, 50%, 75% y 100% "
     "de lo que falta): 7.225,2 M de fondos nuevos por año, 60% a empleo —gasto corriente— y 40% a vivienda —gasto "
     "de capital—. Los dos primeros años la formación usa toda la partida de empleo: dos ingresos por año y 1.286 "
     "egresados en el mandato."),
    ("CÓMO SE PAGA", "Con la base de valuación actualizada, escenario B: la escala de ARBA 10,9% por encima de la "
     "neutral y un tope de 25% de suba por boleta y por año. Cobra 1.976, 5.858 y 7.168 M los tres primeros años y "
     "7.225,2 M desde el cuarto; entre 7.180,7 y 7.225,2 M según cuántas subas frene el mínimo. La cobranza no "
     "paga el programa."),
    ("LO QUE SE REASIGNA", "Ambiente, educación, apoyo escolar y el mantenimiento de habilitaciones —6.863 M en "
     "régimen, y la inversión de 1.200 M una vez—, la plataforma y "
     "el semillero —dentro de Ciencia y Técnica, 22,0%—, las pasantías de las áreas —2.135,3 M—, los cuidadores de "
     "Desarrollo Social —667,8 M—, la beca de práctica "
     "y el módulo de salud de los años 1 y 2 —del gasto flexible libre— y el funcionamiento del sistema vecinal —1,5% "
     "de la partida— no cambian el gasto total: mueven lo que el Municipio ya gasta. Lo que pagan las empresas por "
     "los pasantes, 1.469,1 M, no es gasto municipal."),
    ("ESCENARIOS", "Dos: si nada cambia, y con el programa pagado con la base de valuación. Más la sensibilidad del "
     "resultado de 2031 a lo que recauda el Municipio, a la coparticipación y a la percepción."),
    ("EL BONO", "El bono de 30.000 M de agosto de 2026 entra en la deuda y en la caja, no en el resultado: su capital "
     "va debajo de la línea, en siete cuotas trimestrales entre 2028 y 2029, y su interés no se proyecta porque la "
     "tasa es nominal y variable. El documento lo trata igual (3.5 y 3.6)."),
    ("LO QUE AGREGA", "El mes a mes: estacionalidad, rezago de pago y la deuda flotante que genera, retenciones de "
     "terceros, fondos de libre disponibilidad y afectados, caja y alerta de mínimo. Son supuestos de este libro: "
     "no cambian ningún número anual de la cuenta."),
]
r = 5
for tit, txt in guia:
    put(GU, f"B{r}", tit, font(10, True))
    put(GU, f"C{r}", txt, font(10), wrap=True)
    r += 1
r += 1
put(GU, f"B{r}", "COLORES", font(10, True))
for t, colr, fill in (("Azul: dato de entrada o palanca. Las únicas celdas editables.", BLUE, None),
                      ("Negro: fórmula dentro de la misma hoja.", None, None),
                      ("Verde: vínculo a otra hoja.", GREEN, None),
                      ("Fondo amarillo: palanca clave.", None, F_KEY)):
    put(GU, f"C{r}", t, font(10, color=colr), fill=fill)
    r += 1
r += 1
put(GU, f"B{r}", "HOJAS", font(10, True))
r += 1
hojas = [
    ("Supuestos", "Todos los parámetros, con fuente y nota. Única hoja donde se escribe."),
    ("Estacionalidad", "Perfil mensual de cada origen de recursos y de cada objeto del gasto. Cada fila suma 100%."),
    ("Recursos", "96 meses por origen, percibidos, con lo que cobra la base de valuación y lo facturado y no cobrado."),
    ("Gastos objeto", "96 meses por objeto del gasto, devengado y pagado con rezago."),
    ("Gastos función", "Los mismos gastos por finalidad y función, cada reasignación en su función de destino."),
    ("Flujo mensual", "Caja mes a mes: origen y afectación, retenciones, deuda y alerta de mínimo."),
    ("Vecinal", "La rampa del 12,5% al 50%, el reparto entre las seis zonas y el 1,5% del funcionamiento."),
    ("Programas", "Los programas del capítulo 5, empleo y vivienda abiertos, y la formación: ingresos, pasantes y egresados."),
    ("Deuda", "La deuda al 31/12/2025, que llega a cero en 2029; el bono 2026; la flotante del rezago; el margen contra el tope de la Constitución provincial."),
    ("Resumen anual", "Los ocho ejercicios en la cuenta Ahorro-Inversión, con los dos controles: año base y modelo del repo."),
    ("Escenarios", "Si nada cambia y con el programa, año por año (cuadro 20), y la sensibilidad de 2031."),
    ("Metas", "Las trece metas del 6.3, con lo que proyecta el modelo donde lo hay."),
]
for h, t in hojas:
    put(GU, f"B{r}", h, font(10, True, color=WINE))
    put(GU, f"C{r}", t, font(10), wrap=True)
    r += 1
r += 1
put(GU, f"C{r}", "Este modelo proyecta el marco fiscal, no el resultado de las políticas. Que haya fondos para una "
    "obra no significa que la obra se haga bien ni a tiempo.", font(10, italic=True), wrap=True)
GU.column_dimensions["B"].width = 22
GU.column_dimensions["C"].width = 110
for rr in range(5, r + 1):
    GU.row_dimensions[rr].height = None

wb.save(OUT)
print("guardado", OUT)
