#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera todos los graficos del programa de gobierno, de cero.

Cada capitulo vive en su propio modulo y cada exhibit en su propia función, asi
que se puede regenerar uno solo sin correr los veinte:

    python3 03_scripts/generar_todos_los_graficos.py            # todos
    python3 03_scripts/generar_todos_los_graficos.py 15         # solo el 15
    python3 03_scripts/generar_todos_los_graficos.py 08 09 10   # varios

Al final verifica la paleta de cada SVG generado. Si algun grafico tiene un
color que no es de la paleta, el script sale distinto de cero: es la red que
atrapa un rojo colado por un valor por defecto.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E
import graficos_cap1 as C1
import graficos_cap2 as C2
import graficos_cap3 as C3
import graficos_cap4 as C4
import graficos_cap5 as C5

# Los exhibits que NO se generan porque el dato no existe en el repo. No se
# inventa ninguno: quedan explicados en 06_charts/FALTAN_DATOS.md.
SIN_DATO = {
    "05": ("San Isidro contra la mediana provincial en % personal y % obra "
           "publica", "no hay ejecución presupuestaria de los otros 134 "
           "municipios en el repo"),
    "19": ("Las ocho medidas de transparencia, cumplidas contra pendientes",
           "no existe el dataset de medidas de transparencia"),
}

EXHIBITS = [
    ("01", 1, C1.ex01), ("02", 1, C1.ex02), ("03", 1, C1.ex03),
    ("04", 1, C1.ex04),
    ("06", 2, C2.ex06), ("07", 2, C2.ex07),
    ("08", 3, C3.ex08), ("09", 3, C3.ex09), ("10", 3, C3.ex10),
    ("11", 3, C3.ex11), ("12", 3, C3.ex12),
    ("13", 4, C4.ex13), ("14", 4, C4.ex14), ("15", 4, C4.ex15),
    ("16", 4, C4.ex16),
    ("17", 5, C5.ex17), ("18", 5, C5.ex18), ("20", 5, C5.ex20),
]


def main(pedidos=None):
    hechos, problemas = [], []
    for numero, capitulo, fn in EXHIBITS:
        if pedidos and numero not in pedidos:
            continue
        t0 = time.time()
        png, svg = fn()
        nombre = os.path.basename(png)[:-4]
        sucios = E.verificar_paleta(nombre)
        if sucios:
            problemas.append((nombre, "paleta", sucios))
        fuera = E.DESBORDES.get(nombre) or []
        if fuera:
            problemas.append((nombre, "texto fuera del lienzo", fuera))
        sin_tilde = E.SIN_ACENTO.get(nombre) or []
        if sin_tilde:
            problemas.append((nombre, "palabras sin tilde", sin_tilde))
        hechos.append((numero, capitulo, nombre, time.time() - t0))
        print("  %s  cap.%d  %-46s %5.1fs  %s"
              % (numero, capitulo, nombre, time.time() - t0,
                 "FALLA" if (sucios or fuera or sin_tilde) else "OK"))
    return hechos, problemas


if __name__ == "__main__":
    pedidos = {a.zfill(2) for a in sys.argv[1:]} or None
    print("=" * 84)
    print("FABRICA DE GRAFICOS - paleta única, 1600 px, PNG a 300 dpi y SVG")
    print("=" * 84)
    hechos, problemas = main(pedidos)
    print()
    if not pedidos:
        print("no generados por falta de dato: %s" % ", ".join(sorted(SIN_DATO)))
        for n, (titulo, por) in sorted(SIN_DATO.items()):
            print("  %s  %s" % (n, por))
        print("  -> 06_charts/FALTAN_DATOS.md")
    print()
    print("%d graficos, %d PNG y %d SVG en 06_charts/"
          % (len(hechos), len(hechos), len(hechos)))
    if problemas:
        print()
        print("PROBLEMAS:")
        for nombre, tipo, detalle in problemas:
            print("  %s  [%s]" % (nombre, tipo))
            for d in detalle[:6]:
                print("      %s" % d)
        sys.exit(1)
    print("los %d gráficos: paleta correcta, ningún carácter fuera del lienzo "
          "y ninguna palabra sin tilde" % len(hechos))
