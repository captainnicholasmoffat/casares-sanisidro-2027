#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica el contenido de 01_raw/ contra 01_raw/INVENTARIO.txt.

INVENTARIO.txt lo genero el worker de Chrome al descargar los PDFs del portal de
transparencia de San Isidro. Cada linea util tiene tres campos separados por
espacios multiples:

    <ruta_relativa>   <bytes>   <url_de_origen>

Las rutas del inventario son las del arbol ORIGINAL de descarga. Al reordenar el
repo la carpeta de presupuestos subio un nivel (de
sanisidro_transparencia/presupuestos/ a presupuestos/), asi que el script
normaliza esa ruta antes de comparar. Los nombres de archivo NO se tocan: son la
trazabilidad contra la fuente oficial.

Los 13 .xlsx de transferencias_pba/ no estan en INVENTARIO.txt porque se bajaron
a mano desde el navegador del usuario (ver NO_DESCARGADOS.txt): el host de la
Provincia no responde desde el entorno del worker. Se los cuenta aparte y no se
reportan como sobrantes.

Uso:
    python3 03_scripts/verificar_inventario.py
Salida: 0 si no hay faltantes ni diferencias de tamano, 1 en caso contrario.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "01_raw"
INVENTARIO = RAW / "INVENTARIO.txt"

# Carpetas movidas al reorganizar el repo: ruta_en_inventario -> ruta_actual
REUBICACIONES = {
    "sanisidro_transparencia/presupuestos/": "presupuestos/",
}

# Archivos bajo 01_raw/ que no son datos descargados y por lo tanto no se
# comparan contra el inventario.
NO_DATOS = {"INVENTARIO.txt", "NO_DESCARGADOS.txt", "INDICE.md",
            "indec/DESCARGA.txt"}

# Carpetas cuyo contenido se obtuvo por fuera del worker (sin entrada en el
# inventario). No cuentan como sobrantes.
FUERA_DE_INVENTARIO = {"transferencias_pba"}

SEPARADOR = re.compile(r"\s{2,}")


def normalizar(ruta):
    """Aplica el mapa de reubicaciones a una ruta del inventario."""
    for viejo, nuevo in REUBICACIONES.items():
        if ruta.startswith(viejo):
            return nuevo + ruta[len(viejo):]
    return ruta


def leer_inventario(path):
    """Devuelve {ruta_normalizada: (bytes, url)} y la lista de lineas ilegibles."""
    esperados = {}
    ilegibles = []
    for numero, linea in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        linea = linea.rstrip()
        if not linea or linea.startswith("-") or linea.startswith("TOTAL:"):
            continue
        # Lineas de comentario: el inventario ahora explica de donde salio cada
        # bloque que no bajo el worker de Chrome.
        if linea.lstrip().startswith("#"):
            continue
        if linea.startswith("INVENTARIO") or linea.startswith("Fecha") or linea.startswith("ARCHIVO"):
            continue
        campos = SEPARADOR.split(linea.strip())
        if len(campos) < 2:
            ilegibles.append((numero, linea))
            continue
        ruta, tamano = campos[0], campos[1]
        url = campos[2] if len(campos) > 2 else ""
        if not tamano.isdigit():
            ilegibles.append((numero, linea))
            continue
        esperados[normalizar(ruta)] = (int(tamano), url)
    return esperados, ilegibles


def listar_reales(raw):
    """Devuelve {ruta_relativa_a_01_raw: bytes} para todo lo que hay en disco."""
    reales = {}
    for f in sorted(raw.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(raw).as_posix()
        if rel in NO_DATOS:
            continue
        reales[rel] = f.stat().st_size
    return reales


def main():
    if not INVENTARIO.exists():
        print("ERROR: no existe {}".format(INVENTARIO))
        return 2
    if not RAW.is_dir():
        print("ERROR: no existe {}".format(RAW))
        return 2

    esperados, ilegibles = leer_inventario(INVENTARIO)
    reales = listar_reales(RAW)

    presentes = sorted(r for r in esperados if r in reales)
    faltantes = sorted(r for r in esperados if r not in reales)

    sobrantes = []
    sin_inventario = []
    for r in sorted(reales):
        if r in esperados:
            continue
        if r.split("/", 1)[0] in FUERA_DE_INVENTARIO:
            sin_inventario.append(r)
        else:
            sobrantes.append(r)

    diferencias = []
    for r in presentes:
        esperado = esperados[r][0]
        real = reales[r]
        if esperado != real:
            diferencias.append((r, esperado, real))

    print("VERIFICACION DE INVENTARIO — 01_raw/")
    print("=" * 78)
    print("Inventario:            {}".format(INVENTARIO.relative_to(RAIZ)))
    print("Entradas en inventario: {}".format(len(esperados)))
    print("Archivos en disco:      {} (excluye {})".format(
        len(reales), ", ".join(sorted(NO_DATOS))))
    print()
    print("Presentes:              {}".format(len(presentes)))
    print("Faltantes:              {}".format(len(faltantes)))
    print("Sobrantes:              {}".format(len(sobrantes)))
    print("Diferencias de tamano:  {}".format(len(diferencias)))
    print("Fuera de inventario:    {} ({})".format(
        len(sin_inventario), ", ".join(sorted(FUERA_DE_INVENTARIO))))
    print()

    if ilegibles:
        print("LINEAS ILEGIBLES DEL INVENTARIO")
        print("-" * 78)
        for numero, linea in ilegibles:
            print("  linea {}: {}".format(numero, linea[:100]))
        print()

    if faltantes:
        print("FALTANTES (en el inventario pero no en disco)")
        print("-" * 78)
        for r in faltantes:
            print("  {}  ({} bytes)  {}".format(r, esperados[r][0], esperados[r][1]))
        print()

    if sobrantes:
        print("SOBRANTES (en disco pero no en el inventario)")
        print("-" * 78)
        for r in sobrantes:
            print("  {}  ({} bytes)".format(r, reales[r]))
        print()

    if diferencias:
        print("DIFERENCIAS DE TAMANO")
        print("-" * 78)
        for r, esperado, real in diferencias:
            print("  {}\n      inventario: {} bytes | disco: {} bytes | delta: {:+d}".format(
                r, esperado, real, real - esperado))
        print()

    if sin_inventario:
        print("FUERA DE INVENTARIO (descarga manual, ver NO_DESCARGADOS.txt)")
        print("-" * 78)
        for r in sin_inventario:
            print("  {}  ({} bytes)".format(r, reales[r]))
        print()

    # Se cuenta por extension real y no solo PDF y XLSX: desde que el censo,
    # los indices de precios y el RAFAM entraron al inventario, un recuento de
    # dos tipos dejaba veinte archivos sin contar.
    tipos = {}
    for r in reales:
        ext = r.rsplit(".", 1)[-1].lower() if "." in r else "(sin extension)"
        if r.lower().endswith(".html.gz"):
            ext = "html.gz"
        tipos[ext] = tipos.get(ext, 0) + 1
    print("RECUENTO POR TIPO")
    print("-" * 78)
    for ext in sorted(tipos, key=lambda e: (-tipos[e], e)):
        print("  {:<14} {}".format(ext.upper() + ":", tipos[ext]))
    print("  {:<14} {}".format("TOTAL:", sum(tipos.values())))
    print()

    ok = not faltantes and not diferencias and not sobrantes and not ilegibles
    print("RESULTADO: {}".format("OK" if ok else "CON OBSERVACIONES"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
