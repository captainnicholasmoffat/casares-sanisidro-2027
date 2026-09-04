#!/usr/bin/env python3
"""
Extraccion posicional de tablas de los PDF de transparencia de San Isidro.

Por que posicional y no por split de espacios: en estos PDF las celdas numericas
vienen pegadas sin separador cuando el importe es largo, p.ej.

    29,028,781,538.71-12,269,908,279.0016,758,873,259.71

son TRES importes, no uno. Partir por espacios da basura. Lo que si es estable es
la geometria: los importes estan alineados a la derecha sobre una grilla de
columnas regular. Entonces:

  1. Se reconstruye cada linea visual a partir de los caracteres (no del texto ya
     serializado), conservando la coordenada x de cada caracter.
  2. Se buscan importes con un regex sobre el texto de la linea, y a cada importe
     se le toma el borde DERECHO del ultimo caracter que lo compone.
  3. Esos bordes derechos se agrupan en columnas a lo largo de todo el documento.
     Como la grilla es regular, se puede saber que columna ocupa cada importe
     aunque una columna intermedia venga vacia en todas las filas.

Solo depende de pdfplumber.
"""

import re
import statistics
import unicodedata

import pdfplumber

# Importe con separador de miles "," y dos decimales: 1,234,567.89 o -1,234.00
RE_IMPORTE = re.compile(r"-?\d{1,3}(?:,\d{3})*\.\d{2}")

# Tolerancia vertical para considerar que dos caracteres estan en la misma linea.
TOL_LINEA = 2.0
# Tolerancia horizontal para agrupar bordes derechos en una misma columna.
TOL_COLUMNA = 6.0


def normalizar(texto):
    """Mayusculas sin acentos y con espacios colapsados, para comparar rotulos."""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t).strip().upper()


def a_centavos(texto):
    """'1,234,567.89' -> 123456789 (entero, en centavos). Sin floats."""
    negativo = texto.startswith("-")
    limpio = texto.lstrip("-").replace(",", "")
    entero, _, decimales = limpio.partition(".")
    valor = int(entero) * 100 + int(decimales.ljust(2, "0")[:2])
    return -valor if negativo else valor


def lineas_de_pagina(pagina):
    """Agrupa los caracteres de la pagina en lineas visuales.

    Devuelve una lista de dicts {texto, chars}. El texto se reconstruye en orden
    de x, insertando un espacio solo donde hay un hueco real entre caracteres,
    para que los importes pegados queden pegados (que es lo que necesitamos para
    detectarlos por regex y despues separarlos por posicion).
    """
    chars = [c for c in pagina.chars if c.get("text") is not None]
    chars.sort(key=lambda c: (round(c["top"], 1), c["x0"]))

    lineas, actual, tope = [], [], None
    for c in chars:
        if tope is None or abs(c["top"] - tope) <= TOL_LINEA:
            if tope is None:
                tope = c["top"]
            actual.append(c)
        else:
            lineas.append(actual)
            actual, tope = [c], c["top"]
    if actual:
        lineas.append(actual)

    salida = []
    for grupo in lineas:
        grupo.sort(key=lambda c: c["x0"])
        piezas, mapa, anterior = [], [], None
        for c in grupo:
            if anterior is not None and c["x0"] - anterior["x1"] > 0.9:
                piezas.append(" ")
                mapa.append(None)
            piezas.append(c["text"])
            mapa.extend([c] * len(c["text"]))
        salida.append({"texto": "".join(piezas), "chars": mapa})
    return salida


def partir_linea(linea):
    """Separa la linea en (rotulo, importes).

    La zona numerica arranca despues de la ultima letra, asi un codigo de partida
    como '1.1.10' nunca se confunde con un importe. El rotulo es todo lo que hay
    a la izquierda del primer importe, que es lo que hace falta para reconocer
    filas como 'TOTAL BIENES DE CONSUMO17,057,360,033.00...', donde el texto y el
    numero salen pegados sin espacio.
    """
    texto, mapa = linea["texto"], linea["chars"]
    limite = 0.0
    for i, ch in enumerate(texto):
        if ch.isalpha() and mapa[i] is not None:
            limite = max(limite, mapa[i]["x1"])

    importes, corte = [], len(texto)
    for m in RE_IMPORTE.finditer(texto):
        ini, fin = m.start(), m.end()
        chars = [mapa[i] for i in range(ini, fin) if mapa[i] is not None]
        if not chars:
            continue
        if chars[0]["x0"] < limite:
            continue
        if not importes:
            corte = ini
        importes.append((m.group(), chars[-1]["x1"]))
    return texto[:corte].strip(), importes


def detectar_columnas(bordes, n_columnas):
    """Mapea bordes derechos observados a indices de columna 0..n_columnas-1.

    Agrupa los bordes en cumulos y, usando el paso regular de la grilla, calcula
    el indice de cada cumulo contando desde la ULTIMA columna hacia la izquierda.
    Contar desde la derecha es lo que permite que una columna intermedia vacia no
    corra todo el resto (que es justo lo que pasa con 'Preventivo', vacia en los
    PDF de gastos por objeto).

    Devuelve [(centro, indice)] o None si la grilla no es regular.
    """
    if not bordes:
        return None
    ordenados = sorted(bordes)
    cumulos, actual = [], [ordenados[0]]
    for b in ordenados[1:]:
        if b - actual[-1] <= TOL_COLUMNA:
            actual.append(b)
        else:
            cumulos.append(actual)
            actual = [b]
    cumulos.append(actual)

    centros = [statistics.median(c) for c in cumulos]
    if len(centros) > n_columnas:
        return None
    if len(centros) == 1:
        return [(centros[0], n_columnas - 1)]

    huecos = [b - a for a, b in zip(centros, centros[1:])]
    paso = min(huecos)
    if paso <= 0:
        return None

    derecha = centros[-1]
    mapa = []
    for c in centros:
        desplazamiento = (derecha - c) / paso
        indice = n_columnas - 1 - int(round(desplazamiento))
        # La grilla tiene que ser regular: si un centro no cae sobre un multiplo
        # del paso, no confiamos en el mapeo y abortamos.
        if abs(desplazamiento - round(desplazamiento)) > 0.2:
            return None
        if not 0 <= indice < n_columnas:
            return None
        mapa.append((c, indice))
    if len({i for _, i in mapa}) != len(mapa):
        return None
    return mapa


def asignar(importes, mapa_columnas, n_columnas):
    """Ubica cada importe en su columna. Devuelve una lista de largo n_columnas."""
    fila = [None] * n_columnas
    for texto, borde in importes:
        centro, indice = min(mapa_columnas, key=lambda m: abs(m[0] - borde))
        if abs(centro - borde) > TOL_COLUMNA:
            continue
        fila[indice] = a_centavos(texto)
    return fila


def unir_continuaciones(lineas):
    """Une a la fila anterior las lineas que son solo numeros.

    Algunas filas se dibujan en dos baselines distintas con las columnas
    alternadas: el caso claro es 'TOTALES GENERALES', que deja aprobado, vigente,
    compromiso, pagado y credito-vigente-devengado en una linea y modificaciones,
    devengado, disponible y devengado-no-pagado en la siguiente. Son una sola
    fila logica. Se unen solo los importes; el rotulo queda el de la primera.
    """
    salida = []
    for linea in lineas:
        sin_letras = not any(c.isalpha() for c in linea["rotulo"])
        if salida and sin_letras and linea["importes"] and salida[-1]["importes"]:
            salida[-1]["importes"] = salida[-1]["importes"] + linea["importes"]
            continue
        salida.append(dict(linea))
    return salida


def leer_tabla(ruta, n_columnas):
    """Abre el PDF y devuelve (filas, mapa_columnas).

    filas: lista de dicts {rotulo, texto, importes, pagina}
    mapa_columnas: la grilla detectada, o None si no se pudo detectar.
    """
    lineas = []
    bordes = []
    with pdfplumber.open(ruta) as pdf:
        for n, pagina in enumerate(pdf.pages, 1):
            for linea in lineas_de_pagina(pagina):
                rotulo, imps = partir_linea(linea)
                lineas.append({"rotulo": rotulo, "texto": linea["texto"],
                               "importes": imps, "pagina": n})
                bordes.extend(b for _, b in imps)
    return unir_continuaciones(lineas), detectar_columnas(bordes, n_columnas)
