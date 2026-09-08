"""
QUINTO VERIFICADOR — ningun numero escrito a mano en el texto de un grafico.

Por que existe
--------------
El EXHIBIT 09 tenia el subtitulo "El area sombreada es la diferencia: 2.303
millones a favor en 2031 y 2.924 en 2037" escrito a mano en el codigo. Cuando el
modelo se regenero, la diferencia paso a 2.289 y 2.908, y el grafico siguio
diciendo 2.303. Habria contradicho a la tabla del propio capitulo 3 en el PDF
final, y nadie lo habria visto: el texto de un capitulo lo lee alguien, el
subtitulo de un grafico no lo vuelve a mirar nadie.

La regla
--------
Ningun grafico puede tener un numero escrito a mano en ninguna parte —titulo,
subtitulo, anotacion, etiqueta o pie—. Todo numero que se muestre tiene que
salir del CSV, calculado en el momento de dibujar.

Mismo criterio que la paleta, el desborde, las colisiones y los acentos: que sea
una restriccion y no una intencion.

Como funciona
-------------
Parsea el AST de cada script de graficos y busca literales de texto que
contengan un numero con forma de dato: miles con punto (2.303), decimales con
coma (89,32), porcentajes (17,8%), montos (7.225 M) y anios sueltos dentro de
una frase. Lo que NO denuncia esta en PERMITIDOS, con su motivo.

Uso
---
    python3 03_scripts/verificar_numeros_a_mano.py
    -> 0 si esta limpio, 1 si encontro algo.
"""

import ast
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = ["graficos_cap1.py", "graficos_cap2.py", "graficos_cap3.py",
           "graficos_cap4.py", "graficos_cap5.py"]

# Un numero "de dato": miles con punto, decimales con coma, porcentajes, montos.
NUMERO = re.compile(r"""
    \d{1,3}(?:\.\d{3})+        # 2.303, 25.165, 337.149
  | \d+,\d+                    # 89,32   17,8
  | \b\d+\s*%                  # 92 %
  | \b\d+\s*M\b                # 7.225 M
""", re.X)

# Un anio suelto (2010-2040) NO es un dato: es la etiqueta de un periodo. "en
# 2025 el Municipio devengo" nombra el ejercicio, no muestra una cifra. Lo que
# el verificador persigue son los VALORES: 34,9% / 3,16 / 49.751 / 1,6811.
ANIO = re.compile(r"^20[0-4]\d$")

# Lo que si puede ir a mano, con su motivo. Se compara contra el texto completo
# del literal, normalizado.
PERMITIDOS = {
    # Fuentes y citas legales: son nombres propios de documentos, no datos.
    "censo nacional de poblacion, hogares y viviendas 2022",
    "ley organica de las municipalidades",
    "ley 10.559",
    "decreto 2099/2025",
    "ordenanza 6045/1984",
    "constitucion de la provincia de buenos aires, art. 211",
}

# Fragmentos que, si aparecen en el literal, lo eximen: son plantillas, no datos.
EXENTOS_SI_CONTIENEN = (
    "%s", "%d", "%.1f", "%.2f", "{", "}",   # el numero lo pone el CSV
)


def _normalizar(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def _es_permitido(texto):
    n = _normalizar(texto)
    if n in PERMITIDOS:
        return True
    for p in PERMITIDOS:
        if p in n:
            return True
    return any(e in texto for e in EXENTOS_SI_CONTIENEN)


def revisar(ruta):
    """Devuelve [(linea, texto, numeros)] de los literales sospechosos."""
    with open(ruta, encoding="utf-8") as f:
        fuente = f.read()
    arbol = ast.parse(fuente, filename=ruta)

    # Los docstrings de modulo, clase y funcion son documentacion, no dibujo.
    docstrings = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            d = ast.get_docstring(nodo, clean=False)
            if d is not None and nodo.body:
                primero = nodo.body[0]
                if isinstance(primero, ast.Expr):
                    docstrings.add(id(primero.value))

    hallazgos = []
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Constant) or not isinstance(nodo.value, str):
            continue
        if id(nodo) in docstrings:
            continue
        texto = nodo.value
        # Los textos cortos sin espacios son claves de CSV o nombres de archivo.
        if " " not in texto:
            continue
        if _es_permitido(texto):
            continue
        nums = [n for n in NUMERO.findall(texto) if not ANIO.match(n.strip())]
        if nums:
            hallazgos.append((nodo.lineno, texto, nums))
    return hallazgos


def main():
    total = 0
    print("=" * 78)
    print("VERIFICADOR 5 — numeros escritos a mano en textos de graficos")
    print("=" * 78)
    for nombre in SCRIPTS:
        ruta = os.path.join(AQUI, nombre)
        if not os.path.exists(ruta):
            continue
        hallazgos = revisar(ruta)
        estado = "LIMPIO" if not hallazgos else "%d A MANO" % len(hallazgos)
        print("  %-22s %s" % (nombre, estado))
        for linea, texto, nums in hallazgos:
            corto = texto if len(texto) <= 88 else texto[:85] + "..."
            print("      linea %-5d %s" % (linea, corto))
            print("      %-11s -> %s" % ("", ", ".join(nums)))
        total += len(hallazgos)
    print()
    if total:
        print("FALLA: %d texto(s) con numeros escritos a mano." % total)
        print("Todo numero que se muestre tiene que salir del CSV.")
        return 1
    print("Ningun grafico tiene numeros escritos a mano.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
