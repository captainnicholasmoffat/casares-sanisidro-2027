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
# inventa ninguno: quedan explicados en 06_charts/FALTAN_DATOS.md. Hoy no hay
# ninguno: los veinte estan hechos. El diccionario queda porque es donde se
# declara un faltante el dia que aparezca.
SIN_DATO = {}

EXHIBITS = [
    ("01", 1, C1.ex01), ("02", 1, C1.ex02), ("03", 1, C1.ex03),
    ("04", 1, C1.ex04), ("05", 1, C1.ex05),
    ("06", 2, C2.ex06), ("07", 2, C2.ex07),
    ("08", 3, C3.ex08), ("09", 3, C3.ex09), ("10", 3, C3.ex10),
    ("11", 3, C3.ex11), ("12", 3, C3.ex12),
    ("13", 4, C4.ex13), ("14", 4, C4.ex14), ("15", 4, C4.ex15),
    ("16", 4, C4.ex16),
    ("17", 5, C5.ex17), ("18", 5, C5.ex18), ("19", 5, C5.ex19),
    ("20", 5, C5.ex20),
]


try:
    from verificar_numeros_a_mano import revisar as _revisar_a_mano
except Exception:                                    # pragma: no cover
    _revisar_a_mano = None

try:
    from verificar_geografia import verificar as _verificar_geografia
except Exception:                                    # pragma: no cover
    _verificar_geografia = None

SCRIPTS_DE_GRAFICOS = ["graficos_cap1.py", "graficos_cap2.py",
                       "graficos_cap3.py", "graficos_cap4.py",
                       "graficos_cap5.py"]


def numeros_a_mano():
    """Quinto verificador: ningun numero escrito a mano en el texto de un
    grafico. Corre sobre los scripts, no sobre la figura, porque el defecto
    esta en el codigo: un subtitulo con el numero escrito sobrevive a todas
    las corridas siguientes diciendo lo que ya no es cierto."""
    if _revisar_a_mano is None:
        return []
    aqui = os.path.dirname(os.path.abspath(__file__))
    fuera = []
    for nombre in SCRIPTS_DE_GRAFICOS:
        ruta = os.path.join(aqui, nombre)
        if not os.path.exists(ruta):
            continue
        for linea, texto, nums in _revisar_a_mano(ruta):
            fuera.append("%s:%d  %s  -> %s"
                         % (nombre, linea,
                            texto if len(texto) <= 60 else texto[:57] + "...",
                            ", ".join(nums)))
    return fuera


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
        pisados = E.COLISIONES.get(nombre) or []
        if pisados:
            problemas.append((nombre, "textos que se pisan", pisados))
        tapados = E.TEXTO_TAPADO.get(nombre) or []
        if tapados:
            problemas.append((nombre, "texto tapado por el grafico", tapados))
        hechos.append((numero, capitulo, nombre, time.time() - t0))
        print("  %s  cap.%d  %-46s %5.1fs  %s"
              % (numero, capitulo, nombre, time.time() - t0,
                 "FALLA" if (sucios or fuera or sin_tilde or pisados
                             or tapados) else "OK"))
    return hechos, problemas


if __name__ == "__main__":
    pedidos = {a.zfill(2) for a in sys.argv[1:]} or None
    print("=" * 84)
    print("FABRICA DE GRAFICOS - paleta única, 1600 px, PNG a 300 dpi y SVG")
    print("=" * 84)
    hechos, problemas = main(pedidos)
    a_mano = numeros_a_mano()
    if a_mano:
        problemas.append(("los scripts", "numeros escritos a mano", a_mano))
    # SEPTIMO. Los seis anteriores controlan COMO se dibuja un grafico; ninguno
    # si lo que dibuja es cierto. Se puede tener un grafico perfectamente
    # formado que miente, y eso fue exactamente lo que paso con el mapa.
    if _verificar_geografia is not None and _verificar_geografia():
        problemas.append(("el mapa", "la geografia no cae donde dice",
                          ["ver: python3 03_scripts/verificar_geografia.py"]))
    print()
    if not pedidos and SIN_DATO:
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
    print("los %d gráficos: paleta correcta, ningún carácter fuera del lienzo, "
          "ninguna palabra sin tilde, ningún texto pisado, ningún texto "
          "tapado por el gráfico y ningún número escrito a mano" % len(hechos))
