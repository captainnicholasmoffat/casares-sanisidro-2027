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

    # Algunos PDF (los de recursos) dibujan ciertas celdas dos veces, caracter
    # sobre caracter, para simular negrita. Sin deduplicar, "70,846,672,293.00"
    # se lee "7700,,884466,,667722,,229933..0000" y no hay regex que lo salve.
    # El calco no siempre cae exacto: se corre entre 0.01 y 0.1 pt, asi que hay
    # que deduplicar por proximidad. La tolerancia es holgada frente al ancho de
    # un digito (3.3 pt), asi que dos digitos iguales y contiguos de verdad, como
    # el "11" de 1.185, nunca se confunden con un calco.
    TOL_CALCO = 0.5
    chars.sort(key=lambda c: (round(c["top"], 1), c["x0"]))
    unicos = []
    for c in chars:
        previo = unicos[-1] if unicos else None
        if (previo is not None
                and previo["text"] == c["text"]
                and abs(previo["top"] - c["top"]) <= TOL_CALCO
                and abs(previo["x0"] - c["x0"]) <= TOL_CALCO):
            continue
        unicos.append(c)
    chars = unicos

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

    # El texto de la linea es la concatenacion cruda de los caracteres, sin
    # meter separadores donde el PDF deja un hueco. Es a proposito: los importes
    # se detectan por regex sobre este texto, y un espacio inventado en el lugar
    # equivocado partiria un importe en dos y devolveria numeros que no existen.
    # Para lo que si necesita separar por hueco esta tokens_por_hueco().
    salida = []
    for grupo in lineas:
        grupo.sort(key=lambda c: c["x0"])
        piezas, mapa = [], []
        for c in grupo:
            piezas.append(c["text"])
            mapa.extend([c] * len(c["text"]))
        salida.append({"texto": "".join(piezas), "chars": mapa})
    return salida


def tokens_por_hueco(linea, umbral=2.0):
    """Parte la linea en tokens cortando por espacio o por hueco horizontal.

    Lo usa el formulario de stock de deuda, que no separa las celdas con
    espacios: 'CONSOLIDADA4.983.984.3943.388.144.415' son un rotulo y dos
    importes de columnas distintas, y lo unico que los distingue es que entre
    ellos hay 25 pt de hueco.

    Devuelve [(texto, primer_char, ultimo_char)].
    """
    mapa = linea["chars"]
    tokens, actual = [], []
    anterior = None
    for i, ch in enumerate(linea["texto"]):
        c = mapa[i]
        corta = (c is None or ch.isspace()
                 or (anterior is not None and c["x0"] - anterior["x1"] > umbral))
        if corta and actual:
            tokens.append(("".join(x[0] for x in actual), actual[0][1], actual[-1][1]))
            actual = []
        if c is not None and not ch.isspace():
            actual.append((ch, c))
            anterior = c
    if actual:
        tokens.append(("".join(x[0] for x in actual), actual[0][1], actual[-1][1]))
    return tokens


RE_CORRIDA = re.compile(r"[-0-9.,]+")


def _descomponer(corrida):
    """Parte una corrida de digitos y signos en importes, o None si sobra algo.

    Es lo que separa un importe de verdad de un numero que vive dentro de un
    rotulo. 'LEY 13.010' termina en una corrida '13.010': el regex de importes
    engancha '13.01' y queda un '0' suelto, asi que la corrida NO son importes y
    se descarta entera. En cambio '97,684,606,849.0014,477,501,892.00' se
    descompone sin resto en dos importes, que es justo el caso pegado que hay
    que leer bien.
    """
    piezas, i = [], 0
    while i < len(corrida):
        m = RE_IMPORTE.match(corrida, i)
        if not m:
            return None
        piezas.append((m.start(), m.end()))
        i = m.end()
    return piezas or None


def partir_linea(linea):
    """Separa la linea en (rotulo, importes).

    La zona numerica arranca despues de la ultima letra, y ademas cada corrida
    numerica tiene que descomponerse entera en importes. Con las dos condiciones,
    ni un codigo de partida ni una ley citada en el rotulo se cuelan como dato.
    """
    texto, mapa = linea["texto"], linea["chars"]
    # El corte entre rotulo y numeros se toma por POSICION EN EL TEXTO, no por
    # coordenada. Con coordenadas falla: en 'TOTALES GENERALES155,971,165,667.00'
    # el kerning hace que el primer digito empiece 1.2 pt ANTES del borde
    # derecho de la ultima letra, y la fila entera se descartaba.
    ultima_letra = -1
    for i, ch in enumerate(texto):
        if ch.isalpha():
            ultima_letra = i

    importes, corte = [], len(texto)
    for corrida in RE_CORRIDA.finditer(texto):
        if corrida.start() < ultima_letra:
            continue
        chars = [mapa[i] for i in range(corrida.start(), corrida.end())
                 if mapa[i] is not None]
        if not chars:
            continue
        piezas = _descomponer(corrida.group())
        if piezas is None:
            continue
        if not importes:
            corte = corrida.start()
        for a, b in piezas:
            ini_abs, fin_abs = corrida.start() + a, corrida.start() + b
            cs = [mapa[i] for i in range(ini_abs, fin_abs) if mapa[i] is not None]
            if cs:
                importes.append((texto[ini_abs:fin_abs], cs[-1]["x1"]))
    return texto[:corte].strip(), importes


def detectar_columnas(bordes, n_columnas):
    """Mapea bordes derechos de importes a indices de columna 0..n_columnas-1.

    Los importes van alineados a la derecha, asi que sus bordes derechos se
    agrupan en cumulos, uno por columna ocupada. El problema es que una columna
    puede estar vacia en TODAS las filas ('Preventivo' en gastos por objeto,
    'Recurso Estimado' en algunos trimestres de recursos), y entonces hay menos
    cumulos que columnas y contarlos en orden corre todo el resto.

    Se resuelve midiendo el paso de la grilla y avanzando de cumulo en cumulo:
    un hueco de un paso es la columna siguiente, uno de dos pasos significa que
    quedo una columna vacia en el medio. Al final se ancla la ultima columna
    ocupada contra la ultima columna de la tabla.

    Devuelve [(centro, indice)] o None si no cierra.
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
    estimado = statistics.median(huecos)
    if estimado <= 0:
        return None
    # Un hueco puede valer mas de un paso si quedaron columnas vacias en el
    # medio; se refina el paso dividiendo cada hueco por la cantidad de pasos
    # que representa.
    saltos = [max(1, int(round(h / estimado))) for h in huecos]
    paso = statistics.median([h / k for h, k in zip(huecos, saltos)])
    if paso <= 0:
        return None

    indices, actual_i = [0], 0
    for h, k in zip(huecos, saltos):
        if abs(h / paso - k) > 0.25:
            return None
        actual_i += k
        indices.append(actual_i)

    corrimiento = (n_columnas - 1) - indices[-1]
    if corrimiento < 0:
        return None
    indices = [i + corrimiento for i in indices]
    if indices[0] < 0:
        return None
    return list(zip(centros, indices))


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
