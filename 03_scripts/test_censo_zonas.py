#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests del censo por radio y de la agrupacion en zonas.

Las tres validaciones que pide la tarea son duras: si alguna falla, el script
sale distinto de cero.

  1. La poblacion de los radios de San Isidro tiene que dar 297.282. Si difiere
     mas de 0,5%, se marca y se explica.
  2. Los 360 radios se asignan sin huerfanos, sin dobles y sin sobras.
  3. Todos los radios del partido tienen que caer en exactamente una zona.

Uso:
    python3 03_scripts/test_censo_zonas.py
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import censo_radios as C
import zonas_osm as Z

REPO = Z.RAIZ
TOLERANCIA = 0.5          # por ciento
UMBRAL_DESPROPORCION = 2.0  # zona mayor sobre zona menor


class FalloDeTest(Exception):
    pass


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_codigo_de_partido():
    """El codigo 06756 sale de la fuente, no de una constante escrita a mano."""
    geo = json.load(open(os.path.join(Z.DATA,
                                      "radios_censales_sanisidro.geojson"),
                         encoding="utf-8"))
    props = [f["properties"] for f in geo["features"]]
    provs = {p["prov"] for p in props}
    deptos = {p["depto"] for p in props}
    nombres = {p["partido"] for p in props}
    if provs != {"06"} or deptos != {"756"}:
        raise FalloDeTest("  se esperaba PROV=06 DEPTO=756, hay %s / %s"
                          % (sorted(provs), sorted(deptos)))
    if nombres != {"SAN ISIDRO"}:
        raise FalloDeTest("  hay radios de otro partido: %s" % sorted(nombres))
    malos = [p["radio_id"] for p in props
             if not p["radio_id"].startswith("06756")]
    if malos:
        raise FalloDeTest("  radio_id que no arrancan con 06756: %s" % malos[:5])
    return len(props)


def test_poblacion():
    """La suma de los radios mas las viviendas colectivas da el Censo 2022."""
    radios = _leer("data/censo2022_sanisidro_por_radio.csv")
    particulares = sum(int(r["poblacion_sexo__total"] or 0) for r in radios)
    colectiva = 0
    for r in _leer("data/censo2022_sanisidro_otros_niveles.csv"):
        if r["clave"] == "poblacion_colectiva" and r["categoria"] == "Total":
            colectiva += int(r["casos"])
    total = particulares + colectiva
    dif = total - C.POBLACION_CENSO_2022
    pct = 100.0 * dif / C.POBLACION_CENSO_2022
    if abs(pct) > TOLERANCIA:
        raise FalloDeTest(
            "  la poblacion difiere %+d (%.4f%%), mas que el %.1f%% tolerado.\n"
            "  radios (viviendas particulares): %d\n"
            "  viviendas colectivas (dpto)    : %d\n"
            "  total                          : %d\n"
            "  Censo 2022                     : %d"
            % (dif, pct, TOLERANCIA, particulares, colectiva, total,
               C.POBLACION_CENSO_2022))
    return particulares, colectiva, total, dif, pct


def test_un_nivel_por_tabla():
    """La tabla por radio no puede mezclar niveles geograficos."""
    niveles = {r["nivel_geografico"]
               for r in _leer("data/censo2022_sanisidro_por_radio.csv")}
    if niveles != {"radio"}:
        raise FalloDeTest("  la tabla por radio mezcla niveles: %s"
                          % sorted(niveles))
    otros = {r["nivel_geografico"]
             for r in _leer("data/censo2022_sanisidro_otros_niveles.csv")}
    if "radio" in otros:
        raise FalloDeTest("  hay filas de nivel radio en la tabla de otros "
                          "niveles; van en la tabla por radio")
    return sorted(otros)


def test_cada_radio_en_una_zona():
    geo = json.load(open(os.path.join(Z.DATA,
                                      "radios_censales_sanisidro.geojson"),
                         encoding="utf-8"))
    radios = {f["properties"]["radio_id"] for f in geo["features"]}
    filas = _leer("data/zonas_asignacion_radios.csv")
    vistos = {}
    errores = []
    for f in filas:
        if f["radio_id"] in vistos:
            errores.append("el radio %s aparece dos veces" % f["radio_id"])
        vistos[f["radio_id"]] = f["zona"]
    faltan = sorted(radios - set(vistos))
    sobran = sorted(set(vistos) - radios)
    if faltan:
        errores.append("%d radios sin zona: %s" % (len(faltan), faltan[:5]))
    if sobran:
        errores.append("%d radios asignados que no son del partido: %s"
                       % (len(sobran), sobran[:5]))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return vistos


def test_todo_radio_en_una_zona(asignacion):
    """Ningun radio huerfano. Cada uno tiene exactamente una zona."""
    sin = [r for r, z in asignacion.items() if not z]
    if sin:
        raise AssertionError("%d radio(s) sin zona: %s" % (len(sin), sin[:5]))
    return len(asignacion)


def test_ningun_radio_repetido():
    """Ningun radio aparece dos veces en la asignacion.

    Huerfanos y dobles son fallas distintas y hay que probarlas por separado:
    un dict las esconde, asi que se cuentan las filas del CSV.
    """
    vistos, dobles = set(), []
    for f in _leer("data/zonas_asignacion_radios.csv"):
        if f["radio_id"] in vistos:
            dobles.append(f["radio_id"])
        vistos.add(f["radio_id"])
    if dobles:
        raise AssertionError("%d radio(s) repetido(s): %s" % (len(dobles), dobles[:5]))
    return len(vistos)


def test_las_zonas_cubren_el_partido(asignacion):
    """La union de las seis zonas son los 360 radios del partido y nada mas.

    Es una tercera falla, distinta de huerfanos y de dobles: que aparezca un
    radio que no pertenece al partido. Se compara contra la geometria oficial
    del INDEC, no contra el propio CSV.
    """
    import geopandas as gpd
    oficiales = set(gpd.read_file(
        os.path.join(REPO, "data/radios_censales_sanisidro.geojson"))["radio_id"])
    asignados = set(asignacion)
    sobran = asignados - oficiales
    faltan = oficiales - asignados
    if sobran or faltan:
        raise AssertionError(
            "asignados que no son del partido: %s | del partido sin asignar: %s"
            % (sorted(sobran)[:5] or "ninguno", sorted(faltan)[:5] or "ninguno"))
    return len(oficiales)


def main():
    print("=" * 78)
    print("CENSO 2022 POR RADIO Y ZONAS - VALIDACIONES")
    print("=" * 78)
    fallas = 0

    try:
        n = test_codigo_de_partido()
        print("  OK     codigo de partido 06756 y %d radios, todos de San Isidro" % n)
    except FalloDeTest as e:
        print("  FALLA  codigo de partido\n%s" % e); fallas += 1

    try:
        part, col, total, dif, pct = test_poblacion()
        print("  OK     poblacion validada contra el Censo 2022")
        print("           viviendas particulares (360 radios) : %d" % part)
        print("           viviendas colectivas (departamento) : %d" % col)
        print("           total                               : %d" % total)
        print("           Censo 2022                          : %d"
              % C.POBLACION_CENSO_2022)
        print("           diferencia                          : %+d (%.4f%%)"
              % (dif, pct))
    except FalloDeTest as e:
        print("  FALLA  poblacion\n%s" % e); fallas += 1

    try:
        otros = test_un_nivel_por_tabla()
        print("  OK     la tabla por radio es toda de nivel radio; lo que no "
              "hay por radio va aparte (%s)" % ", ".join(otros))
    except FalloDeTest as e:
        print("  FALLA  niveles geograficos\n%s" % e); fallas += 1

    asignacion = None
    try:
        asignacion = test_cada_radio_en_una_zona()
        print("  OK     los %d radios caen en exactamente una zona"
              % len(asignacion))
    except FalloDeTest as e:
        print("  FALLA  asignacion de radios\n%s" % e); fallas += 1

    if asignacion:
        try:
            n = test_todo_radio_en_una_zona(asignacion)
            print("  OK     los %d radios tienen zona, ninguno huerfano" % n)
        except FalloDeTest as e:
            print("  FALLA  radios huerfanos\n%s" % e); fallas += 1
        try:
            n = test_ningun_radio_repetido()
            print("  OK     los %d radios aparecen una sola vez" % n)
        except AssertionError as e:
            print("  FALLA  radios repetidos\n%s" % e); fallas += 1
        try:
            n = test_las_zonas_cubren_el_partido(asignacion)
            print("  OK     las zonas cubren los %d radios del partido y nada mas" % n)
        except AssertionError as e:
            print("  FALLA  cobertura del partido\n%s" % e); fallas += 1


    print()
    print("=" * 78)
    print("INDICADORES POR ZONA (peor a mejor)")
    print("=" * 78)
    print("%-3s %-18s %8s %8s %7s %8s %8s %7s %8s"
          % ("#", "zona", "pobl", "hogares", "NBI%", "s/cloaca", "s/gas",
             "hacin%", "univ+%"))
    for f in _leer("data/zonas_indicadores.csv"):
        print("%-3s %-18s %8s %8s %7s %8s %8s %7s %8s"
              % (f["orden_peor_a_mejor"], f["zona"], f["poblacion"],
                 f["hogares"], f["pct_nbi"], f["pct_sin_cloaca"],
                 f["pct_sin_gas_red"], f["pct_hacinamiento"],
                 f["pct_edu_universitaria_completa_o_mas"]))
    print()
    if fallas:
        print("HAY %d VALIDACION(ES) EN FALLA" % fallas)
        return 1
    print("TEST CENSO Y ZONAS OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
