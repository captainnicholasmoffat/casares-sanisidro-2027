#!/usr/bin/env python3
"""
Serie presupuestaria historica de San Isidro, 2010-2026.

Lee los PDF de 01_raw/presupuestos/ y escribe data/presupuesto_historico_2010_2026.csv
con una fila por anio y concepto, en pesos corrientes. No se deflacta nada.

Por que hay una especificacion explicita por documento y no un parser generico:
los 19 PDF son de tres familias distintas y ni siquiera dentro de una familia el
formato se repite. Adivinar donde esta cada tabla con heuristicas daria numeros
plausibles y equivocados. La especificacion dice, para cada documento, en que
pagina esta cada tabla y como se llaman sus filas; es larga pero es auditable
contra el PDF.

Los importes se manejan como enteros en centavos. Ningun float en la aritmetica.

Uso:
    python3 03_scripts/parse_presupuestos.py
"""

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdfplumber

import pdf_tabla as T

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESUPUESTOS = os.path.join(RAIZ, "01_raw", "presupuestos")
DATA = os.path.join(RAIZ, "data")

# Un importe tiene que traer al menos un separador de miles. Sin esa condicion,
# los porcentajes que acompanan a cada fila ('45.54%', '0.001%') se colarian como
# montos. Todas las cifras presupuestarias de estos documentos superan los mil.
RE_MONTO = re.compile(r"-?\d{1,3}(?:[.,]\d{3})+(?:[.,]\d{1,2})?")
# El lookbehind es imprescindible: sin el, en '69.900.000,0037,61%' el regex
# engancha '0037,61%' y se lleva puestos dos digitos que son del importe,
# dejando '69.900.000,' que ya no decodifica. Un porcentaje solo cuenta si no
# arranca en medio de un numero.
RE_PORCENTAJE = re.compile(r"(?<![\d.,])-?\d{1,3}(?:[.,]\d+)?\s*%")


class ErrorDeParseo(Exception):
    """El PDF no se pudo leer con la estructura esperada."""


# --------------------------------------------------------------------------
# numeros
# --------------------------------------------------------------------------

def a_centavos(texto):
    """Convierte un importe a entero en centavos, detectando el formato.

    Estos documentos mezclan las dos convenciones sin avisar: '1,234,567.89'
    (ingles) en unos anios y '1.234.567,89' (castellano) en otros, a veces en el
    mismo PDF. La regla que las separa sin ambiguedad: si aparecen los dos
    separadores, el ULTIMO es el decimal; si aparece uno solo, es decimal
    unicamente cuando aparece una sola vez y lo siguen una o dos cifras.
    """
    limpio = texto.replace("$", "").replace(" ", "").replace(" ", "").strip()
    negativo = limpio.startswith("-")
    limpio = limpio.lstrip("-")

    pos_punto, pos_coma = limpio.rfind("."), limpio.rfind(",")
    if pos_punto >= 0 and pos_coma >= 0:
        decimal = "." if pos_punto > pos_coma else ","
    elif pos_punto >= 0 or pos_coma >= 0:
        sep = "." if pos_punto >= 0 else ","
        cola = limpio.rsplit(sep, 1)[1]
        decimal = sep if (limpio.count(sep) == 1 and len(cola) <= 2) else None
    else:
        decimal = None

    if decimal:
        entero, _, decimales = limpio.rpartition(decimal)
        entero = re.sub(r"[.,]", "", entero)
        centavos = int(entero or "0") * 100 + int(decimales.ljust(2, "0")[:2])
    else:
        centavos = int(re.sub(r"[.,]", "", limpio)) * 100
    return -centavos if negativo else centavos


def formatear(centavos):
    """Entero en centavos -> texto decimal exacto, sin separadores de miles."""
    if centavos is None:
        return ""
    signo = "-" if centavos < 0 else ""
    c = abs(centavos)
    return "%s%d.%02d" % (signo, c // 100, c % 100)


# Los reportes de sistema pegan las celdas sin separador:
# 'Total BIENES DE USO52,796,213,849.001,243,304,040.01' son DOS importes. Para
# separarlos hay que exigir que la corrida numerica se descomponga ENTERA en
# importes de un mismo formato. Se prueban los cuatro formatos que aparecen en
# el corpus y se acepta el que cubre la corrida sin dejar resto.
RE_CORRIDA = re.compile(r"[-0-9.,]{4,}")
FORMATOS = [
    re.compile(r"-?\d{1,3}(?:,\d{3})+\.\d{2}"),   # 1,234,567.89
    re.compile(r"-?\d{1,3}(?:\.\d{3})+,\d{2}"),   # 1.234.567,89
    re.compile(r"-?\d{1,3}(?:,\d{3})+"),          # 1,234,567
    re.compile(r"-?\d{1,3}(?:\.\d{3})+"),          # 1.234.567
]


# Sobra de una corrida cuando el porcentaje viene pegado al importe y sin el
# signo '%': en el presupuesto 2018 la fila sale como
# 'SERVICIOS NO PERSONALES$2,174,919,800.0036.25' y ese '36.25' es la
# participacion, no plata. Nunca puede ser un importe porque los importes de
# estos documentos exigen separador de miles.
RE_PORCENTAJE_PEGADO = re.compile(r"^\d{1,3}[.,]\d{1,2}$")


def _descomponer(corrida):
    """Parte una corrida numerica en importes, o None si sobra algo.

    Que tenga que cubrir la corrida entera es lo que evita inventar numeros: si
    ningun formato la cubre sin resto, la corrida no son importes y se descarta.
    Lo unico que se tolera como resto es un porcentaje pegado al final.
    """
    for formato in FORMATOS:
        piezas, i = [], 0
        while i < len(corrida):
            m = formato.match(corrida, i)
            if not m:
                break
            piezas.append((m.start(), m.end()))
            i = m.end()
        if not piezas:
            continue
        if i == len(corrida):
            return piezas
        if RE_PORCENTAJE_PEGADO.match(corrida[i:]):
            return piezas
    return None


def montos_de_linea(texto, unir=False):
    """Importes de la linea, sin los porcentajes, como [(texto, inicio)].

    Con unir=True se sacan los espacios antes de descomponer. Hace falta en el
    presupuesto 2013, donde el PDF parte cada importe en dos pedazos con un
    hueco en el medio: 'Recursos Humanos$    4 69.900.000,00' son 469.900.000,00
    y no un 4 seguido de 69 millones. Se activa solo donde esta verificado que
    reconstruye bien, porque pegar espacios a ciegas fusionaria importes de
    columnas distintas en los documentos que separan las celdas con espacios.
    """
    sin_pct = RE_PORCENTAJE.sub(lambda m: " " * len(m.group()), texto)
    if unir:
        sin_pct = re.sub(r"(?<=[\d.,])\s+(?=[\d.,])", "", sin_pct)
    salida = []
    for corrida in RE_CORRIDA.finditer(sin_pct):
        piezas = _descomponer(corrida.group())
        if piezas is None:
            continue
        for a, b in piezas:
            salida.append((corrida.group()[a:b], corrida.start() + a))
    return salida


def filas_de_pagina(ruta, numero_pagina, unir=False):
    """Devuelve [(rotulo, [montos])] de una pagina, en orden."""
    with pdfplumber.open(ruta) as pdf:
        if numero_pagina > len(pdf.pages):
            raise ErrorDeParseo("el PDF no tiene pagina %d" % numero_pagina)
        lineas = T.lineas_de_pagina(pdf.pages[numero_pagina - 1])

    salida = []
    for linea in lineas:
        texto = linea["texto"]
        montos = montos_de_linea(texto, unir)
        if not montos:
            salida.append((T.normalizar(texto), []))
            continue
        salida.append((T.normalizar(texto[:montos[0][1]]),
                       [m for m, _ in montos]))
    return salida


def filas_del_documento(ruta):
    """Igual que filas_de_pagina pero sobre todo el documento, con la pagina."""
    salida = []
    with pdfplumber.open(ruta) as pdf:
        for n, pagina in enumerate(pdf.pages, 1):
            for linea in T.lineas_de_pagina(pagina):
                texto = linea["texto"]
                montos = montos_de_linea(texto)
                if not montos:
                    continue
                salida.append((n, T.normalizar(texto[:montos[0][1]]),
                               [m for m, _ in montos]))
    return salida


# --------------------------------------------------------------------------
# vocabulario
# --------------------------------------------------------------------------

# Los rotulos cambian de nombre a lo largo de los anios ('Recursos Humanos' pasa
# a ser 'Gastos en Personal', 'Servicios de la Deuda' a 'Servicio de la Deuda').
# Se normalizan a un mismo subconcepto para que la serie sea comparable.
OBJETOS = [
    ("gastos_en_personal", ["GASTOS EN PERSONAL", "RECURSOS HUMANOS", "PERSONAL"]),
    ("bienes_de_consumo", ["BIENES DE CONSUMO"]),
    ("servicios_no_personales", ["SERVICIOS NO PERSONALES", "SERVICIOS NO PERS."]),
    ("bienes_de_uso", ["BIENES DE USO"]),
    ("transferencias", ["TRANSFERENCIAS"]),
    ("activos_financieros", ["ACTIVOS FINANCIEROS"]),
    ("servicio_de_la_deuda", [
        "SERVICIO DE LA DEUDA Y DISMINUCION DE OTROS PASIVOS",
        "SERVICIOS DE LA DEUDA Y DISMINUCION DE OTROS PASIVOS",
        "SERVICIO DE LA DEUDA Y DIS. DE OTROS PASIVOS"]),
]

ORIGENES = [
    ("municipal", ["ORIGEN MUNICIPAL", "1 - ORIGEN MUNICIPAL"]),
    ("provincial", ["ORIGEN PROVINCIAL", "2 - ORIGEN PROVINCIAL"]),
    ("nacional", ["ORIGEN NACIONAL", "3 - ORIGEN NACIONAL"]),
    ("otros", ["OTROS ORIGENES", "4 - OTROS ORIGENES"]),
]



def limpiar_codigo(rotulo):
    """Deja el rotulo comparable: sin codigo de partida, sin '$' y sin bordes.

    Los rotulos vienen con basura distinta en cada familia: '1.1.4 - ', '1-',
    y en los informes ARSI un '$' pegado al final porque el simbolo de moneda va
    en la celda del rotulo y no en la del importe.
    """
    r = re.sub(r"^\d+(\.\d+)*\s*[-.]?\s*", "", rotulo).strip()
    return re.sub(r"\s+", " ", r).strip(" .-$")


def buscar(filas, alternativas, columna):
    """Primer monto cuyo rotulo matchea alguna de las alternativas.

    Si la fila del rotulo no trae importes se miran las lineas pegadas, primero
    la de arriba y despues la de abajo. En el texto de la ordenanza 2024 el
    maquetado desacopla rotulo e importes: los de 'Origen Municipal' salen en la
    linea anterior y los de 'Otros Origenes' en la siguiente. Que la busqueda
    este acotada a la pagina de esa tabla, y que despues se valide que los
    cuatro origenes suman el total, es lo que hace segura esta concesion.
    """
    objetivos = {T.normalizar(a) for a in alternativas}
    for i, (rotulo, montos) in enumerate(filas):
        if limpiar_codigo(rotulo) not in objetivos and rotulo not in objetivos:
            continue
        candidatos = montos
        if not candidatos:
            for j in (i - 1, i + 1, i - 2, i + 2):
                if 0 <= j < len(filas) and filas[j][1]:
                    candidatos = filas[j][1]
                    break
        if not candidatos:
            continue
        idx = columna if columna >= 0 else len(candidatos) + columna
        if 0 <= idx < len(candidatos):
            return a_centavos(candidatos[idx])
    return None


def buscar_total(filas, etiqueta, columna):
    """Total de la tabla, por rotulo exacto y quedandose con el ultimo.

    La etiqueta va explicita en la especificacion de cada documento y no en una
    lista generica: en los reportes de sistema hay lineas 'TOTAL' sueltas que
    cierran una subseccion ('Total VENTA DE ACTIVOS' aparece como 'TOTAL' a
    secas) mucho antes del 'TOTAL GENERAL' que cierra el cuadro.
    """
    objetivo = T.normalizar(etiqueta)
    encontrado = None
    for i, (rotulo, montos) in enumerate(filas):
        if limpiar_codigo(rotulo) != objetivo:
            continue
        candidatos = montos
        if not candidatos:
            for j in (i - 1, i + 1):
                if 0 <= j < len(filas) and filas[j][1]:
                    candidatos = filas[j][1]
                    break
        if not candidatos:
            continue
        idx = columna if columna >= 0 else len(candidatos) + columna
        if 0 <= idx < len(candidatos):
            encontrado = a_centavos(candidatos[idx])
    return encontrado


def unico_monto(filas):
    """El unico importe de la pagina, o None si hay mas de uno.

    Lo usa la lamina de portada del presupuesto 2023, donde el total va solo,
    sin rotulo al lado.
    """
    todos = [m for _, montos in filas for m in montos]
    return a_centavos(todos[0]) if len(todos) == 1 else None


# --------------------------------------------------------------------------
# especificacion por documento
# --------------------------------------------------------------------------
#
# 'columna' es el indice del importe dentro de la fila: 0 el primero, -1 el
# ultimo. Importa donde la tabla abre en varias columnas, por ejemplo las de
# origen que traen LIBRE DISPONIBILIDAD / AFECTADOS / TOTALES: ahi hay que
# quedarse con la ultima.
#
# 'alcance' vale "pagina" (la tabla esta en esa pagina) o "documento" (se busca
# el rotulo en todo el PDF y se usa la ULTIMA aparicion, que es la que cierra el
# objeto en los reportes de sistema, donde antes aparecen subtotales homonimos).

ESPECIFICACIONES = [
    {"anio": 2011, "archivo": "presupuesto2011.pdf", "familia": "A",
     "origen": {"pagina": 4, "columna": -1},
     "objeto": {"pagina": 28, "columna": 0},
     "total_recursos": {"pagina": 4, "columna": -1, "etiqueta": "TOTALES"},
     "total_gastos": {"pagina": 28, "columna": 0, "etiqueta": "TOTALES"}},

    {"anio": 2012, "archivo": "presupuesto2012municipalidaddesanisidro.pdf", "familia": "A",
     "origen": {"pagina": 16, "columna": -1},
     "objeto": {"pagina": 20, "columna": 0},
     "total_recursos": {"pagina": 16, "columna": -1, "etiqueta": "TOTALES"},
     "total_gastos": {"pagina": 20, "columna": 0, "etiqueta": "TOTALES"}},

    {"anio": 2013, "archivo": "msipresupuesto2013v2.pdf", "familia": "C",
     "origen": {"pagina": 14, "columna": -1},
     "objeto": {"pagina": 17, "columna": 0, "unir_montos": True},
     "total_recursos": {"pagina": 13, "columna": 0, "etiqueta": "TOTALES"},
     "total_gastos": {"pagina": 17, "columna": 0, "etiqueta": "TOTALES",
                      "unir_montos": True}},

    {"anio": 2018, "archivo": "_presupuesto2018.pdf.pdf", "familia": "C",
     "origen": {"pagina": 3, "columna": -1},
     "objeto": {"pagina": 16, "columna": 0},
     "total_recursos": {"pagina": 3, "columna": -1, "etiqueta": "TOTAL"},
     "total_gastos": {"pagina": 16, "columna": 0, "etiqueta": "TOTAL"}},

    {"anio": 2019, "archivo": "informe_arsi_presupuesto_2019.pdf", "familia": "B",
     "origen": {"pagina": 4, "columna": -1},
     "objeto": {"pagina": 7, "columna": 0},
     "total_recursos": {"pagina": 4, "columna": -1, "etiqueta": "TOTALES"},
     "total_gastos": {"pagina": 7, "columna": 0, "etiqueta": "TOTALES"}},

    {"anio": 2020, "archivo": "informe_arsi_presupuesto_2020.pdf", "familia": "B",
     "origen": {"pagina": 4, "columna": -1},
     "objeto": {"pagina": 7, "columna": 0},
     "total_recursos": {"pagina": 4, "columna": -1, "etiqueta": "TOTALES"},
     "total_gastos": {"pagina": 7, "columna": 0, "etiqueta": "TOTALES"}},

    {"anio": 2021, "archivo": "informe_arsi_presupuesto_2021.pdf", "familia": "B",
     "origen": {"pagina": 4, "columna": -1},
     "objeto": {"pagina": 7, "columna": 0},
     "total_recursos": {"pagina": 4, "columna": -1, "etiqueta": "TOTALES"},
     "total_gastos": {"pagina": 7, "columna": 0, "etiqueta": "TOTALES"}},

    {"anio": 2023, "archivo": "presentacion_power_point_presupuesto_2023_1.pdf", "familia": "A",
     "origen": {"pagina": 15, "columna": 0},
     "total_recursos": {"pagina": 2, "unico": True},
     "total_gastos": {"pagina": 2, "unico": True}},

    {"anio": 2024, "archivo": "presupuesto_2024_hcd.pdf", "familia": "C",
     "origen": {"pagina": 3, "columna": -1},
     "total_recursos": {"pagina": 3, "columna": -1, "etiqueta": "TOTALES"}},

    {"anio": 2024, "archivo": "2024_presupuesto_de_recursos_y_gastos_por_rubro_y_objeto.pdf",
     "familia": "C",
     "objeto": {"alcance": "documento", "columna": 0},
     "total_recursos": {"pagina": 2, "columna": 0, "etiqueta": "TOTAL GENERAL"}},

    {"anio": 2025, "archivo": "presupuesto_2025_msi.pdf", "familia": "C",
     "objeto": {"alcance": "documento", "columna": 0},
     "total_recursos": {"pagina": 3, "columna": 0, "etiqueta": "TOTAL GENERAL"},
     "total_gastos": {"pagina": 10, "columna": 0, "etiqueta": "TOTAL GENERAL"}},
]

# PDF que quedan afuera a proposito, con el motivo exacto.
EXCLUIDOS = [
    ("ordenanza_del_presupuesto_2026_1.pdf",
     "Escaneo sin capa de texto (416 paginas). Excluido a proposito: son las "
     "ordenanzas completas con los anexos legales y hacer OCR sobre novecientas "
     "paginas de tablas financieras mete errores de digitos. Para 2026 ya hay "
     "ejecucion trimestral y situacion economico-financiera en texto limpio."),
    ("ordenanza_presupuesto_hcd_-_msi_2.pdf",
     "Escaneo sin capa de texto util (493 paginas). Mismo motivo que el anterior."),
    ("ordenanza_prespuesto_2024.pdf",
     "Tiene capa de texto pero es salida de OCR y ya viene con digitos mal: la "
     "fecha de emision sale como '12/1212023' en vez de '12/12/2023', y los "
     "encabezados como 'PROGRAMACiONDELOSRECURSOS'. Usar estos numeros meteria "
     "errores silenciosos. Para 2024 se usan los otros dos documentos, que "
     "estan en texto nativo."),
    ("presupuesto_de_gastos_y_calculo_de_recursos_2010.pdf",
     "Las tablas estan pegadas como imagen: la capa de texto solo trae los "
     "titulos de las laminas, cero importes. Sin OCR no hay nada que extraer."),
    ("presupuesto_municipal_2014_03.pdf",
     "Las tablas estan pegadas como imagen: la capa de texto solo trae titulos "
     "y comentarios, cero importes."),
    ("msi-presupuesto-municipal-2016.pdf",
     "Las tablas estan pegadas como imagen, cero importes en el texto. Ademas "
     "el archivo se llama 2016 y la portada dice 'AÑO 2016', pero todas las "
     "laminas de datos dicen 2015: el anio del contenido no esta claro."),
    ("_presupuesto2017.pdf.pdf",
     "Las tablas estan pegadas como imagen: la capa de texto solo trae titulos "
     "y comentarios, cero importes."),
    ("presupuesto_municipal_2022-presentacion_en_el_honorable_concejo_deliberante-"
     "noviembre_2021_1.pdf",
     "Las tablas estan pegadas como imagen: la capa de texto solo trae los "
     "titulos de las laminas, cero importes."),
]


# --------------------------------------------------------------------------
# extraccion
# --------------------------------------------------------------------------

def _filas(ruta, spec):
    """Filas del alcance que pide la spec: una pagina o el documento entero."""
    if spec.get("alcance") == "documento":
        return [(rotulo, montos) for _, rotulo, montos in filas_del_documento(ruta)]
    return filas_de_pagina(ruta, spec["pagina"], spec.get("unir_montos", False))


def _pagina(spec):
    return "" if spec.get("alcance") == "documento" else spec["pagina"]


def _ultimo(filas, alternativas, columna):
    """Como buscar() pero se queda con la ULTIMA aparicion del rotulo.

    En los reportes de sistema el mismo rotulo aparece antes como subtotal: en
    2025 hay un 'Total GASTOS EN PERSONAL' de 1.191.497.550 antes del verdadero
    de 97.684.606.849. El que cierra el objeto es siempre el ultimo.
    """
    objetivos = {T.normalizar(a) for a in alternativas}
    encontrado = None
    for rotulo, montos in filas:
        if not montos:
            continue
        limpio = limpiar_codigo(rotulo)
        limpio = re.sub(r"^TOTAL(ES)?\s+", "", limpio).strip()
        if limpio in objetivos:
            idx = columna if columna >= 0 else len(montos) + columna
            if 0 <= idx < len(montos):
                encontrado = a_centavos(montos[idx])
    return encontrado


def extraer(spec):
    """Devuelve las filas del CSV para un documento."""
    ruta = os.path.join(PRESUPUESTOS, spec["archivo"])
    if not os.path.exists(ruta):
        raise ErrorDeParseo("no existe el archivo")
    anio, fuente = spec["anio"], spec["archivo"]
    filas = []

    def agregar(concepto, subconcepto, monto, pagina):
        if monto is not None:
            filas.append({"anio": anio, "concepto": concepto,
                          "subconcepto": subconcepto, "monto": monto,
                          "fuente": fuente, "pagina": pagina})

    if "origen" in spec:
        s = spec["origen"]
        datos = _filas(ruta, s)
        for clave, alternativas in ORIGENES:
            agregar("recursos_por_origen", clave,
                    buscar(datos, alternativas, s["columna"]), _pagina(s))

    if "objeto" in spec:
        s = spec["objeto"]
        datos = _filas(ruta, s)
        for clave, alternativas in OBJETOS:
            agregar("gastos_por_objeto", clave,
                    _ultimo(datos, alternativas, s["columna"]), _pagina(s))

    for clave in ("total_recursos", "total_gastos"):
        if clave not in spec:
            continue
        s = spec[clave]
        datos = _filas(ruta, s)
        monto = (unico_monto(datos) if s.get("unico")
                 else buscar_total(datos, s["etiqueta"], s["columna"]))
        agregar(clave, "", monto, _pagina(s))

    if not filas:
        raise ErrorDeParseo("no se extrajo ningun importe con la especificacion")
    return filas


def main():
    filas, no_parseados = [], []
    for spec in ESPECIFICACIONES:
        try:
            filas.extend(extraer(spec))
        except Exception as exc:
            no_parseados.append((spec["archivo"],
                                 "%s: %s" % (type(exc).__name__, exc)))

    filas.sort(key=lambda f: (f["anio"], f["fuente"], f["concepto"], f["subconcepto"]))

    os.makedirs(DATA, exist_ok=True)
    ruta_csv = os.path.join(DATA, "presupuesto_historico_2010_2026.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["anio", "concepto", "subconcepto", "monto", "fuente", "pagina"])
        for f in filas:
            w.writerow([f["anio"], f["concepto"], f["subconcepto"],
                        formatear(f["monto"]), f["fuente"], f["pagina"]])

    print("  presupuesto_historico_2010_2026.csv   %d filas" % len(filas))
    return {"filas": filas, "no_parseados": no_parseados, "excluidos": EXCLUIDOS}


if __name__ == "__main__":
    main()
