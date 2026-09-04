#!/usr/bin/env python3
"""
Parseo de la ejecucion presupuestaria de San Isidro a series limpias.

Lee los PDF de 01_raw/sanisidro_transparencia/ y escribe CSV en data/.
Toda la extraccion numerica se apoya en pdf_tabla.py, que ubica los importes por
posicion en la pagina y no por separacion de espacios (en estos PDF las celdas
salen pegadas: "29,028,781,538.71-12,269,908,279.0016,758,873,259.71" son tres
importes distintos).

Los importes se manejan SIEMPRE como enteros en centavos. No se usa float en
ningun punto del camino, asi que no hay redondeo posible.
"""

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdf_tabla as T

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "01_raw", "sanisidro_transparencia")
DATA = os.path.join(RAIZ, "data")

ROMANOS = {"i": "I", "ii": "II", "iii": "III", "iv": "IV"}

# Columnas de los PDF de "gastos por objeto", en el orden en que aparecen en la
# pagina. 'preventivo' viene vacia en todos los ejercicios revisados, pero se
# declara igual porque la grilla la reserva y el mapeo es por posicion absoluta.
COLUMNAS_GASTOS_OBJETO = [
    "credito_aprobado",
    "modificaciones",
    "credito_vigente",
    "preventivo",
    "compromiso",
    "devengado",
    "pagado",
    "credito_disponible",
    "credito_vig_devengado",
    "devengado_no_pagado",
]

RE_SECCION = re.compile(r"^(\d) - (.+)$")


class ErrorDeParseo(Exception):
    """El PDF no se pudo leer con la estructura esperada."""


def anio_trimestre(nombre):
    """'2025_iv_gastos_por_objeto.pdf' -> (2025, 'IV')."""
    m = re.match(r"^(\d{4})_(i{1,3}|iv)_", nombre)
    if not m:
        raise ErrorDeParseo("no se puede deducir anio y trimestre de %r" % nombre)
    return int(m.group(1)), ROMANOS[m.group(2)]


def formatear(centavos):
    """Entero en centavos -> texto decimal exacto, sin separadores de miles."""
    if centavos is None:
        return ""
    signo = "-" if centavos < 0 else ""
    c = abs(centavos)
    return "%s%d.%02d" % (signo, c // 100, c % 100)


def parse_gastos_objeto(ruta):
    """Devuelve los 7 totales por objeto del gasto, mas el total general del PDF.

    Salida: (filas, total_general). Cada fila es un dict con los importes en
    centavos. total_general es el devengado de la linea TOTALES GENERALES, que se
    usa despues para chequear que los 7 objetos sumen lo que dice el propio PDF.
    """
    nombre = os.path.basename(ruta)
    anio, trimestre = anio_trimestre(nombre)
    filas_pdf, mapa = T.leer_tabla(ruta, len(COLUMNAS_GASTOS_OBJETO))
    if mapa is None:
        raise ErrorDeParseo("no se pudo detectar la grilla de columnas")

    filas = []
    total_general = None
    seccion = None
    for linea in filas_pdf:
        rotulo = T.normalizar(linea["rotulo"])

        m = RE_SECCION.match(rotulo)
        if m:
            seccion = (m.group(1), m.group(2))
            continue

        if rotulo == "TOTALES GENERALES":
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_GASTOS_OBJETO))
            total_general = dict(zip(COLUMNAS_GASTOS_OBJETO, valores))
            continue

        if seccion and rotulo == "TOTAL " + seccion[1]:
            valores = T.asignar(linea["importes"], mapa, len(COLUMNAS_GASTOS_OBJETO))
            fila = dict(zip(COLUMNAS_GASTOS_OBJETO, valores))
            fila.update({
                "anio": anio,
                "trimestre": trimestre,
                "objeto_codigo": seccion[0],
                "objeto": seccion[1],
                "fuente": nombre,
            })
            filas.append(fila)
            seccion = None

    if len(filas) != 7:
        raise ErrorDeParseo(
            "se esperaban 7 totales por objeto y se encontraron %d" % len(filas))
    return filas, total_general


def escribir_csv(ruta, campos, filas, numericos):
    """Escribe el CSV formateando los campos numericos desde centavos."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for fila in filas:
            salida = {}
            for campo in campos:
                valor = fila.get(campo)
                salida[campo] = formatear(valor) if campo in numericos else valor
            w.writerow(salida)
    return len(filas)
