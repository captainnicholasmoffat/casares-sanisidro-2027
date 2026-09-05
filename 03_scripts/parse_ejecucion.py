#!/usr/bin/env python3
"""
Parseo de la ejecucion presupuestaria de San Isidro a series limpias.

Lee los PDF de 01_raw/sanisidro_transparencia/ y escribe CSV en data/.
La extraccion numerica se apoya en pdf_tabla.py, que ubica los importes por
posicion en la pagina y no por separacion de espacios (en estos PDF las celdas
salen pegadas: "29,028,781,538.71-12,269,908,279.0016,758,873,259.71" son tres
importes distintos).

Los importes se manejan SIEMPRE como enteros en centavos. No se usa float en
ningun punto de la aritmetica; el punto decimal aparece recien al escribir el
CSV. Asi no hay redondeo posible.

Cuatro informes, tres layouts distintos:

  gastos por objeto        10 columnas, grilla regular. 'Preventivo' viene vacia.
  recursos                  8 columnas. Algunas celdas se dibujan dos veces para
                            simular negrita (lo resuelve pdf_tabla).
  gastos por finalidad      10 columnas, mismo layout que gastos por objeto, pero
                            con dos niveles (finalidad y funcion).
  stock de deuda            formulario de la Ley 12.462. Miles con punto y sin
                            decimales, y columnas identificadas por el rotulo del
                            encabezado en vez de por grilla.

Uso:
    python3 03_scripts/parse_ejecucion.py
"""

import csv
import glob
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdf_tabla as T

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "01_raw", "sanisidro_transparencia")
DATA = os.path.join(RAIZ, "data")

ROMANOS = {"i": "I", "ii": "II", "iii": "III", "iv": "IV"}

COLUMNAS_GASTOS_OBJETO = [
    "credito_aprobado", "modificaciones", "credito_vigente", "preventivo",
    "compromiso", "devengado", "pagado", "credito_disponible",
    "credito_vig_devengado", "devengado_no_pagado",
]

COLUMNAS_RECURSOS = [
    "calculado", "modificaciones", "vigente", "devengado",
    "dif_vigente_devengado", "percibido", "dif_devengado_percibido",
    "dif_vigente_percibido",
]

COLUMNAS_DEUDA = [
    "saldo", "amortiz_ej1", "intereses_ej1", "amortiz_ej2", "intereses_ej2",
    "amortiz_ej3", "intereses_ej3", "amortiz_resto", "intereses_resto",
    "deuda_vencida_impaga",
]

RE_SECCION = re.compile(r"^(\d) - (.+)$")
RE_FINALIDAD = re.compile(r"^(\d) - (.+)$")
RE_FUNCION = re.compile(r"^(\d\.\d) - (.+)$")
RE_RUBRO = re.compile(r"^(\d\.\d) - (.+)$")
# Importe del formulario de deuda: miles con punto, sin decimales.
RE_DEUDA_NUM = re.compile(r"^-?\d{1,3}(?:\.\d{3})*$")
RE_CODIGO_DEUDA = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")


class ErrorDeParseo(Exception):
    """El PDF no se pudo leer con la estructura esperada."""


# --------------------------------------------------------------------------
# utilidades
# --------------------------------------------------------------------------

def anio_trimestre(nombre):
    """Deduce (anio, trimestre) del nombre del archivo.

    Cubre las dos formas que usa el Municipio:
      2025_iv_gastos_por_objeto.pdf        -> (2025, 'IV')
      stock_de_deuda_-_i_trim_2024_msi.pdf -> (2024, 'I')
    """
    m = re.match(r"^(\d{4})_(i{1,3}|iv)_", nombre)
    if m:
        return int(m.group(1)), ROMANOS[m.group(2)]
    m = re.search(r"_(i{1,3}|iv)_trim_(\d{4})", nombre)
    if m:
        return int(m.group(2)), ROMANOS[m.group(1)]
    raise ErrorDeParseo("no se puede deducir anio y trimestre del nombre")


RE_PERIODO = re.compile(
    r"(?:Desde|Del)\s*(\d{1,2}/\d{1,2}/\d{4})\s*(?:Hasta|al)\s*(\d{1,2}/\d{1,2}/\d{4})")


def periodo(texto_pagina):
    """Extrae (desde, hasta, tipo) del encabezado del informe.

    Esto no es un adorno: los informes NO son homogeneos y sumarlos a ciegas da
    cualquier cosa.

      I  trimestre  2/1 -> 31/3   arranca en enero, o sea acumulado = trimestre
      II trimestre  1/4 -> 30/6   SOLO el trimestre
      III trimestre 1/7 -> 30/9   SOLO el trimestre
      IV trimestre  2/1 -> 30/12  ACUMULADO ANUAL, no el trimestre

    Ademas los informes que arrancan en enero traen las columnas de credito
    (aprobado, modificaciones, vigente) y los que cubren un trimestre suelto las
    traen vacias. De ahi salen casi todas las inconsistencias que reporta
    test_parser.py.
    """
    m = RE_PERIODO.search(re.sub(r"\s+", " ", texto_pagina))
    if not m:
        return "", "", "desconocido"
    desde, hasta = m.group(1), m.group(2)
    mes_desde = int(desde.split("/")[1])
    mes_hasta = int(hasta.split("/")[1])
    if mes_desde != 1:
        tipo = "trimestre"
    elif mes_hasta >= 12:
        tipo = "acumulado_anual"
    elif mes_hasta == 3:
        tipo = "trimestre"
    else:
        tipo = "acumulado_parcial"
    return desde, hasta, tipo


def formatear(centavos):
    """Entero en centavos -> texto decimal exacto, sin separadores de miles."""
    if centavos is None:
        return ""
    signo = "-" if centavos < 0 else ""
    c = abs(centavos)
    return "%s%d.%02d" % (signo, c // 100, c % 100)


def cierra_seccion(candidato, seccion):
    """True si la linea 'TOTAL <candidato>' cierra la seccion <seccion>.

    Lo normal es que coincidan exactamente. La excepcion es que el PDF trunca
    los rotulos a un ancho fijo, y como la linea del total arrastra el prefijo
    'TOTAL ' le entran menos caracteres del nombre: la seccion sale como
    'SERVICIOS DE LA DEUDA PUBLICA (INTERESES Y GAST' y su total como
    'SERVICIOS DE LA DEUDA PUBLICA (INTERESES Y G'.

    Por eso el candidato solo puede ser MAS CORTO que la seccion, nunca mas
    largo. Aceptar candidatos mas largos rompe todo: dentro de la seccion
    'TRANSFERENCIAS' hay un 'TOTAL TRANSFERENCIAS AL SECTOR PRIVADO PARA
    FINANCIAR GASTOS' que la cerraria antes de tiempo y devolveria el subtotal
    equivocado.
    """
    if candidato == seccion:
        return True
    return (len(candidato) < len(seccion)
            and len(seccion) - len(candidato) <= 6
            and seccion.startswith(candidato))


# --------------------------------------------------------------------------
# gastos por objeto
# --------------------------------------------------------------------------

def parse_gastos_objeto(ruta):
    """Devuelve (filas, total_general) con los 7 totales por objeto del gasto."""
    nombre = os.path.basename(ruta)
    anio, trimestre = anio_trimestre(nombre)
    lineas, mapa = T.leer_tabla(ruta, len(COLUMNAS_GASTOS_OBJETO))
    if mapa is None:
        raise ErrorDeParseo("no se pudo detectar la grilla de columnas")
    desde, hasta, tipo = periodo(" ".join(l["texto"] for l in lineas[:12]))

    filas, total_general, seccion = [], None, None
    for linea in lineas:
        rotulo = T.normalizar(linea["rotulo"])

        m = RE_SECCION.match(rotulo)
        if m:
            seccion = (m.group(1), m.group(2))
            continue

        if rotulo == "TOTALES GENERALES":
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_GASTOS_OBJETO))
            total_general = dict(zip(COLUMNAS_GASTOS_OBJETO, valores))
            continue

        if seccion and rotulo.startswith("TOTAL ") and cierra_seccion(
                rotulo[6:], seccion[1]):
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_GASTOS_OBJETO))
            fila = dict(zip(COLUMNAS_GASTOS_OBJETO, valores))
            fila.update({"anio": anio, "trimestre": trimestre,
                         "periodo_desde": desde, "periodo_hasta": hasta,
                         "periodo_tipo": tipo,
                         "objeto_codigo": seccion[0], "objeto": seccion[1],
                         "fuente": nombre})
            filas.append(fila)
            seccion = None

    # No se exige que esten los 7 objetos. En 2024 I el Municipio no publica
    # 'Activos financieros' porque no tuvo movimiento: la fila no existe en el
    # PDF y no se inventa un cero. Que los objetos presentes sumen el total
    # general del PDF se chequea despues, en test_parser.py.
    if len(filas) < 5:
        raise ErrorDeParseo(
            "se esperaban al menos 5 totales por objeto y se encontraron %d"
            % len(filas))
    if total_general is None:
        raise ErrorDeParseo("no se encontro la linea TOTALES GENERALES")
    return filas, total_general


# --------------------------------------------------------------------------
# recursos
# --------------------------------------------------------------------------

def parse_recursos(ruta):
    """Devuelve (filas, total_general) con los totales por rubro de recursos."""
    nombre = os.path.basename(ruta)
    anio, trimestre = anio_trimestre(nombre)
    lineas, mapa = T.leer_tabla(ruta, len(COLUMNAS_RECURSOS))
    if mapa is None:
        raise ErrorDeParseo("no se pudo detectar la grilla de columnas")
    desde, hasta, tipo = periodo(" ".join(l["texto"] for l in lineas[:12]))

    filas, total_general, seccion, vistos = [], None, None, set()
    for linea in lineas:
        rotulo = T.normalizar(linea["rotulo"])

        m = RE_RUBRO.match(rotulo)
        if m:
            seccion = (m.group(1), m.group(2))
            continue

        if rotulo == "TOTAL GENERAL":
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_RECURSOS))
            total_general = dict(zip(COLUMNAS_RECURSOS, valores))
            continue

        if seccion and rotulo.startswith("TOTAL ") and cierra_seccion(
                rotulo[6:], seccion[1]):
            if seccion[0] in vistos:
                seccion = None
                continue
            vistos.add(seccion[0])
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_RECURSOS))
            fila = dict(zip(COLUMNAS_RECURSOS, valores))
            fila.update({"anio": anio, "trimestre": trimestre,
                         "periodo_desde": desde, "periodo_hasta": hasta,
                         "periodo_tipo": tipo,
                         "rubro_codigo": seccion[0], "rubro": seccion[1],
                         "fuente": nombre})
            filas.append(fila)
            seccion = None

    if not filas:
        raise ErrorDeParseo("no se encontro ningun total por rubro")
    return filas, total_general


# --------------------------------------------------------------------------
# gastos por finalidad y funcion
# --------------------------------------------------------------------------

def parse_fyf(ruta):
    """Devuelve (filas, total_general) a nivel finalidad y a nivel funcion.

    El informe anida funciones dentro de finalidades y cierra cada una con su
    propio 'TOTAL <nombre>'. Se emiten los dos niveles con una columna 'nivel',
    asi se puede validar que las funciones sumen su finalidad y las finalidades
    sumen el total general.
    """
    nombre = os.path.basename(ruta)
    anio, trimestre = anio_trimestre(nombre)
    lineas, mapa = T.leer_tabla(ruta, len(COLUMNAS_GASTOS_OBJETO))
    if mapa is None:
        raise ErrorDeParseo("no se pudo detectar la grilla de columnas")
    desde, hasta, tipo = periodo(" ".join(l["texto"] for l in lineas[:12]))

    filas, total_general = [], None
    finalidad, funcion = None, None

    def emitir(nivel, codigo, titulo, contexto, linea):
        valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_GASTOS_OBJETO))
        fila = dict(zip(COLUMNAS_GASTOS_OBJETO, valores))
        fila.update({"anio": anio, "trimestre": trimestre, "nivel": nivel,
                     "periodo_desde": desde, "periodo_hasta": hasta,
                     "periodo_tipo": tipo,
                     "finalidad_codigo": contexto[0], "finalidad": contexto[1],
                     "funcion_codigo": codigo if nivel == "funcion" else "",
                     "funcion": titulo if nivel == "funcion" else "",
                     "fuente": nombre})
        filas.append(fila)

    for linea in lineas:
        rotulo = T.normalizar(linea["rotulo"])

        m = RE_FUNCION.match(rotulo)
        if m:
            funcion = (m.group(1), m.group(2))
            continue
        m = RE_FINALIDAD.match(rotulo)
        if m:
            finalidad, funcion = (m.group(1), m.group(2)), None
            continue

        if rotulo == "TOTALES GENERALES":
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_GASTOS_OBJETO))
            total_general = dict(zip(COLUMNAS_GASTOS_OBJETO, valores))
            continue

        if not rotulo.startswith("TOTAL ") or not linea["importes"]:
            continue
        titulo = rotulo[6:]

        # Primero se intenta cerrar la funcion abierta y despues la finalidad:
        # cuando una finalidad tiene una sola funcion del mismo nombre (el caso
        # de 'A CLASIFICAR'), el orden en la pagina es funcion y despues
        # finalidad, y este orden lo respeta.
        if funcion and cierra_seccion(titulo, funcion[1]):
            emitir("funcion", funcion[0], funcion[1], finalidad or ("", ""), linea)
            funcion = None
        elif finalidad and cierra_seccion(titulo, finalidad[1]):
            emitir("finalidad", finalidad[0], finalidad[1], finalidad, linea)
            finalidad, funcion = None, None

    if not filas:
        raise ErrorDeParseo("no se encontro ninguna finalidad ni funcion")
    return filas, total_general


# --------------------------------------------------------------------------
# stock de deuda
# --------------------------------------------------------------------------

def parse_deuda(ruta):
    """Devuelve las filas del formulario de stock de deuda (Ley 12.462).

    Este informe no tiene grilla regular: la mayoria de las columnas estan
    vacias en todos los ejercicios publicados, asi que ubicar las columnas por
    orden de aparicion daria cualquier cosa. Se toman los rotulos del
    encabezado ('SALDO AL', 'AMORTIZ.', 'INTERESES', 'E IMPAGA') como anclas y
    cada importe se asigna al ancla mas cercana.
    """
    import pdfplumber

    nombre = os.path.basename(ruta)
    anio, trimestre = anio_trimestre(nombre)

    # El formulario entra en una pagina, pero alguna version escaneada trae una
    # segunda hoja con las notas al pie. Se leen todas y se ignoran las que no
    # tienen el encabezado.
    lineas = []
    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            lineas.extend(T.lineas_de_pagina(pagina))

    # Anclas: borde derecho del rotulo de cada columna, de izquierda a derecha.
    anclas, fecha_corte = [], ""
    for linea in lineas:
        for texto, primero, ultimo in T.tokens_por_hueco(linea):
            plano = T.normalizar(texto)
            # El rotulo de la primera columna es 'SALDO AL' arriba y la fecha
            # de corte abajo, las dos sobre la misma columna. Se ancla en la
            # fecha, que ademas es el dato que hay que guardar.
            if plano in ("AMORTIZ.", "INTERESES", "IMPAGA"):
                anclas.append(ultimo["x1"])
            elif re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", texto) and not fecha_corte:
                fecha_corte = texto
                anclas.append(ultimo["x1"])
    anclas = sorted(set(round(a, 1) for a in anclas))
    if len(anclas) != len(COLUMNAS_DEUDA):
        cabecera = T.normalizar(" ".join(l["texto"] for l in lineas[:8]))
        if "REGISTRO DE ENDEUDAMIENTO" not in cabecera:
            titulo = "ESTADO DE EJECUCION DEL PRESUPUESTO DE GASTOS"
            que_es = titulo if titulo in cabecera else "un informe desconocido"
            raise ErrorDeParseo(
                "no es un formulario de stock de deuda (Ley 12.462) sino %s; "
                "esta mal archivado en deuda_publica/" % que_es)
        raise ErrorDeParseo(
            "se esperaban %d columnas en el encabezado y se detectaron %d"
            % (len(COLUMNAS_DEUDA), len(anclas)))

    filas = []
    for linea in lineas:
        tokens = T.tokens_por_hueco(linea)
        if not tokens:
            continue
        rotulo, numeros = [], []
        for texto, primero, ultimo in tokens:
            if RE_DEUDA_NUM.match(texto) and primero["x0"] > anclas[0] - 60:
                numeros.append((texto, ultimo["x1"]))
            elif not numeros:
                rotulo.append(texto)
        etiqueta = " ".join(rotulo).strip()

        m = RE_CODIGO_DEUDA.match(etiqueta)
        if not m or not numeros:
            continue

        valores = [None] * len(COLUMNAS_DEUDA)
        for texto, borde in numeros:
            distancias = [(abs(a - borde), i) for i, a in enumerate(anclas)]
            distancia, indice = min(distancias)
            if distancia > 30:
                continue
            valores[indice] = int(texto.replace(".", "")) * 100

        fila = dict(zip(COLUMNAS_DEUDA, valores))
        fila.update({"anio": anio, "trimestre": trimestre,
                     "fecha_corte": fecha_corte, "codigo": m.group(1).rstrip("."),
                     "concepto": m.group(2).strip(), "fuente": nombre})
        filas.append(fila)

    if not filas:
        raise ErrorDeParseo("no se encontro ninguna fila con importes")
    return filas


# --------------------------------------------------------------------------
# recorrido de archivos y escritura
# --------------------------------------------------------------------------

def archivos(subcarpeta, patron):
    return sorted(glob.glob(os.path.join(RAW, subcarpeta, patron)))


def escribir_no_parseados(secciones):
    """Escribe NO_PARSEADOS.md con todas las secciones que le pasen.

    Lo llama parse_ejecucion.py con sus propias secciones cuando se corre
    suelto, y test_parser.py con las de los cuatro informes mas las de los
    presupuestos historicos, que es la version completa.
    """
    with open(os.path.join(RAIZ, "NO_PARSEADOS.md"), "w", encoding="utf-8") as fh:
        fh.write("# PDF no incorporados a los CSV\n\n")
        fh.write("Generado por `03_scripts/test_parser.py`. Cada archivo de esta ")
        fh.write("lista esta fuera de los CSV, con el motivo exacto.\n")
        for titulo, tipo, filas in secciones:
            fh.write("\n## %s\n\n" % titulo)
            if not filas:
                fh.write("Ninguno.\n")
                continue
            if tipo == "duplicado":
                fh.write("Mismo md5 que el original, asi que se procesa una sola ")
                fh.write("vez. Los datos estan en los CSV bajo el nombre del ")
                fh.write("original.\n\n| Archivo omitido | Copia de | md5 |\n")
                fh.write("|---|---|---|\n")
                for nombre, original, huella in filas:
                    fh.write("| `%s` | `%s` | `%s` |\n" % (nombre, original, huella))
            else:
                fh.write("| Archivo | Motivo |\n|---|---|\n")
                for nombre, motivo in filas:
                    fh.write("| `%s` | %s |\n" % (nombre, motivo))


def escribir_csv(ruta, campos, filas, numericos):
    """Escribe el CSV formateando los campos numericos desde centavos."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for fila in filas:
            w.writerow({c: (formatear(fila.get(c)) if c in numericos
                            else fila.get(c, "")) for c in campos})
    return len(filas)


def correr(parser, rutas, no_parseados, duplicados):
    """Aplica el parser a cada PDF. Lo que falla va a no_parseados con el motivo.

    Los PDF byte a byte identicos se procesan una sola vez. El caso concreto es
    2025_iii_gastos_por_fyf_0.pdf, que el Municipio publico por error como copia
    de 2025_iii_gastos_por_fyf.pdf; contarlo dos veces duplicaria el trimestre
    entero en cualquier agregacion.
    """
    filas, generales, huellas = [], {}, {}
    for ruta in rutas:
        nombre = os.path.basename(ruta)
        with open(ruta, "rb") as fh:
            huella = hashlib.md5(fh.read()).hexdigest()
        if huella in huellas:
            duplicados.append((nombre, huellas[huella], huella))
            continue
        huellas[huella] = nombre
        try:
            salida = parser(ruta)
        except Exception as exc:
            no_parseados.append((nombre, "%s: %s" % (type(exc).__name__, exc)))
            continue
        if isinstance(salida, tuple):
            nuevas, general = salida
            generales[nombre] = general
        else:
            nuevas = salida
        filas.extend(nuevas)
    return filas, generales


def main():
    no_parseados, duplicados = [], []

    objeto, gen_objeto = correr(
        parse_gastos_objeto,
        archivos("ejecucion_presupuestaria", "*gastos_por_objeto*.pdf"),
        no_parseados, duplicados)
    recursos, gen_recursos = correr(
        parse_recursos,
        archivos("ejecucion_presupuestaria", "*recursos*.pdf"),
        no_parseados, duplicados)
    fyf, gen_fyf = correr(
        parse_fyf,
        archivos("gastos_por_finalidad_y_funcion", "*.pdf"),
        no_parseados, duplicados)
    deuda, _ = correr(
        parse_deuda, archivos("deuda_publica", "*.pdf"), no_parseados, duplicados)

    n1 = escribir_csv(
        os.path.join(DATA, "ejecucion_gastos_objeto.csv"),
        ["anio", "trimestre", "periodo_desde", "periodo_hasta", "periodo_tipo",
         "objeto_codigo", "objeto", "credito_aprobado",
         "modificaciones", "credito_vigente", "devengado", "pagado", "fuente"],
        objeto, set(COLUMNAS_GASTOS_OBJETO))
    n2 = escribir_csv(
        os.path.join(DATA, "ejecucion_recursos.csv"),
        ["anio", "trimestre", "periodo_desde", "periodo_hasta", "periodo_tipo",
         "rubro_codigo", "rubro", "calculado", "vigente",
         "devengado", "percibido", "fuente"],
        recursos, set(COLUMNAS_RECURSOS))
    n3 = escribir_csv(
        os.path.join(DATA, "gastos_finalidad_funcion.csv"),
        ["anio", "trimestre", "periodo_desde", "periodo_hasta", "periodo_tipo",
         "nivel", "finalidad_codigo", "finalidad",
         "funcion_codigo", "funcion", "credito_aprobado", "modificaciones",
         "credito_vigente", "devengado", "pagado", "fuente"],
        fyf, set(COLUMNAS_GASTOS_OBJETO))
    n4 = escribir_csv(
        os.path.join(DATA, "deuda_stock.csv"),
        ["anio", "trimestre", "fecha_corte", "codigo", "concepto"]
        + COLUMNAS_DEUDA + ["fuente"],
        deuda, set(COLUMNAS_DEUDA))

    for nombre, filas in (("ejecucion_gastos_objeto.csv", n1),
                          ("ejecucion_recursos.csv", n2),
                          ("gastos_finalidad_funcion.csv", n3),
                          ("deuda_stock.csv", n4)):
        print("  %-34s %5d filas" % (nombre, filas))

    escribir_no_parseados([
        ("Ejecucion presupuestaria: no se pudieron parsear", "motivo",
         no_parseados),
        ("Ejecucion presupuestaria: omitidos por ser copia exacta de otro",
         "duplicado", duplicados),
    ])

    print("\n  %d PDF no parseados, %d omitidos por duplicado (NO_PARSEADOS.md)"
          % (len(no_parseados), len(duplicados)))

    return {"gastos_objeto": (objeto, gen_objeto),
            "recursos": (recursos, gen_recursos),
            "fyf": (fyf, gen_fyf),
            "deuda": (deuda, {}),
            "no_parseados": no_parseados,
            "duplicados": duplicados}


if __name__ == "__main__":
    main()
