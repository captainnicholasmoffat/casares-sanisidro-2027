#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACCION FORENSE DE UN PDF — todos sus estilos, no los que uno recuerda

    python3 04_diseno/medir/forense.py <pdf> [paginas]

Saca de un PDF TODAS las combinaciones distintas de (familia, cuerpo, color)
que aparecen, con cuantas veces aparece cada una, donde arranca, su
interletrado medio y un ejemplo de texto. Y todos los rectangulos: bandas,
filetes y puntos de guia, con su color y su grosor.

POR QUE EXISTE. Mirar un PDF y anotar lo que a uno le llama la atencion deja
afuera la mitad, y uno no sabe cual mitad. Cada vez que se corrigio una pieza
de este documento contra la referencia aparecio otra que nunca se habia
medido: el color de los cintillos del indice, el interletrado de sus
etiquetas, los cinco colores de una pagina que se habian leido como dos. Esto
las saca todas de una y deja la lista para comparar.
"""

import collections
import sys


def estilos(ruta, paginas=None):
    import pdfplumber
    pdf = pdfplumber.open(ruta)
    cuenta = collections.Counter()
    donde = collections.defaultdict(list)
    ejemplo = {}
    tracking = collections.defaultdict(list)
    for i, p in enumerate(pdf.pages):
        if paginas and i not in paginas:
            continue
        lineas = collections.defaultdict(list)
        for c in p.chars:
            lineas[round(c["top"], 1)].append(c)
        for t, cs in lineas.items():
            cs = sorted(cs, key=lambda c: c["x0"])
            for a, b in zip(cs, cs[1:]):
                if 0 <= b["x0"] - a["x1"] < 6 and a["size"] == b["size"]:
                    tracking[_clave(a)].append(b["x0"] - a["x1"])
            for c in cs:
                k = _clave(c)
                cuenta[k] += 1
                donde[k].append(round(c["x0"]))
            k = _clave(cs[0])
            ejemplo.setdefault(k, "".join(c["text"] for c in cs)[:42])
    return cuenta, donde, ejemplo, tracking, len(pdf.pages)


def _clave(c):
    col = c.get("non_stroking_color") or ()
    if len(col) >= 3:
        col = "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in col[:3])
    elif len(col) == 1:
        g = int(round(col[0] * 255))
        col = "#%02x%02x%02x" % (g, g, g)
    else:
        col = "?"
    return (c["fontname"].split("+")[-1], round(c["size"], 1), col)


def rectangulos(ruta, paginas=None):
    import pdfplumber
    pdf = pdfplumber.open(ruta)
    cuenta = collections.Counter()
    for i, p in enumerate(pdf.pages):
        if paginas and i not in paginas:
            continue
        for r in p.rects:
            alto, ancho = r["y1"] - r["y0"], r["x1"] - r["x0"]
            if alto > 200 and ancho > 200:
                continue                      # el fondo de la pagina
            col = r.get("non_stroking_color") or ()
            if isinstance(col, (int, float)):
                col = (col,)
            if not all(isinstance(v, (int, float)) for v in col):
                col = ()                      # espacios de color raros
            if len(col) >= 3:
                col = "#%02x%02x%02x" % tuple(int(round(v * 255))
                                              for v in col[:3])
            elif len(col) == 1:
                g = int(round(col[0] * 255))
                col = "#%02x%02x%02x" % (g, g, g)
            else:
                col = "?"
            if ancho < 4 and alto < 4:
                cuenta[("punto de guia", round(alto, 2), col)] += 1
            elif alto < 3:
                cuenta[("filete", round(alto, 2), col)] += 1
            else:
                cuenta[("banda", round(alto, 1), col)] += 1
    return cuenta


def main():
    ruta = sys.argv[1]
    pgs = {int(x) - 1 for x in sys.argv[2].split(",")} if len(sys.argv) > 2 else None
    cuenta, donde, ejemplo, tracking, n = estilos(ruta, pgs)
    print("=" * 92)
    print("%s — %d páginas" % (ruta.split("/")[-1], n))
    print("=" * 92)
    print("%-26s %5s %-9s %6s %5s  %5s  %s"
          % ("FAMILIA", "pt", "color", "veces", "x0", "track", "ejemplo"))
    for k, v in sorted(cuenta.items(), key=lambda t: -t[1]):
        if v < 12:
            continue
        xs = collections.Counter(donde[k]).most_common(1)[0][0]
        tr = tracking.get(k) or [0]
        print("%-26s %5.1f %-9s %6d %5d  %5.2f  %s"
              % (k[0], k[1], k[2], v, xs, sum(tr) / len(tr),
                 ejemplo.get(k, "")[:34]))
    print("\nRECTANGULOS")
    for k, v in sorted(rectangulos(ruta, pgs).items(), key=lambda t: -t[1]):
        if v < 4:
            continue
        print("  %-14s alto %6.2f pt  %-9s  x%d" % (k[0], k[1], k[2], v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
