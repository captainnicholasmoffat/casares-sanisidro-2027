#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera data/zonas_propuestas_sanisidro.geojson y data/zonas_resumen.csv con
las seis localidades que usa el documento (capitulos 1 y 4): los 360 radios
censales asignados a su localidad de OpenStreetMap en
data/zonas_asignacion_radios.csv, disueltos en un poligono por localidad.

Por que existe: el geojson anterior era el de las zonas construidas por
zonas.py (semillas y crecimiento por poblacion), que el documento dejo de usar
cuando paso a las localidades de OpenStreetMap. El informe 09 y los mapas lo
seguian leyendo, y el 3.5 salio calculado sobre zonas que no son las del resto
del documento. Con este archivo regenerado, todo lo que lee el geojson ve las
mismas seis localidades.

Uso:
    python3 03_scripts/zonas_osm_geojson.py

Controla, antes de escribir, que los indicadores recalculados radio por radio
coincidan con data/zonas_indicadores.csv (poblacion, hogares y los cinco
porcentajes que publica el documento). Si no coinciden, no escribe nada.
"""

import csv
import json
import os
import sys
from collections import defaultdict

from shapely.geometry import shape, mapping
from shapely.ops import unary_union

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import zonas as Z  # noqa: E402  (INDICADORES, TOTALES, indicadores_por_zona)

DATA = Z.DATA
FECHA = "2026-09-28"
LIMITE = ("OpenStreetMap, relaciones administrativas de localidad (no es fuente "
          "oficial), proyectadas sobre los radios censales del INDEC")


def leer():
    with open(os.path.join(DATA, "radios_censales_sanisidro.geojson"), encoding="utf-8") as f:
        radios = json.load(f)
    with open(os.path.join(DATA, "censo2022_sanisidro_por_radio.csv"), encoding="utf-8", newline="") as f:
        censo = {r["radio_id"]: r for r in csv.DictReader(f)}
    with open(os.path.join(DATA, "zonas_asignacion_radios.csv"), encoding="utf-8", newline="") as f:
        asig = list(csv.DictReader(f))
    return radios, censo, asig


def main():
    radios, censo, asig = leer()
    asignacion = {r["radio_id"]: r["zona"] for r in asig}
    relacion = {r["zona"]: r["relacion_osm"] for r in asig}
    ids = {str(f["properties"]["radio_id"]) for f in radios["features"]}
    if ids != set(asignacion):
        sys.exit("!! los radios del geojson y los de la asignacion no son los mismos")

    filas = Z.indicadores_por_zona(asignacion, censo)

    # control contra lo que publica el documento
    with open(os.path.join(DATA, "zonas_indicadores.csv"), encoding="utf-8", newline="") as f:
        publicado = {r["zona"]: r for r in csv.DictReader(f)}
    malos = []
    for fila in filas:
        p = publicado[fila["zona"]]
        for k in ("radios", "poblacion", "hogares", "viviendas"):
            if int(p[k]) != fila[k]:
                malos.append((fila["zona"], k, p[k], fila[k]))
        for k in ("pct_nbi", "pct_sin_cloaca", "pct_sin_gas_red", "pct_hacinamiento",
                  "pct_edu_universitaria_completa_o_mas"):
            if abs(float(p[k]) - fila[k]) > 0.005:
                malos.append((fila["zona"], k, p[k], fila[k]))
        if int(p["orden_peor_a_mejor"]) != fila["orden_peor_a_mejor"]:
            malos.append((fila["zona"], "orden", p["orden_peor_a_mejor"], fila["orden_peor_a_mejor"]))
    if malos:
        for m in malos:
            print("  !!", m)
        sys.exit("!! los indicadores no coinciden con data/zonas_indicadores.csv: no se escribe nada")

    # un poligono por localidad
    por = defaultdict(list)
    for f in radios["features"]:
        por[asignacion[str(f["properties"]["radio_id"])]].append(shape(f["geometry"]))
    feats = []
    for fila in filas:
        props = {"zona": fila["zona"], "relacion_osm": relacion[fila["zona"]]}
        props.update({k: v for k, v in fila.items() if k != "zona"})
        props.update({"limite": LIMITE,
                      "fuente_geometria": Z.FUENTE_GEO,
                      "fuente_datos": Z.FUENTE_CENSO,
                      "fecha_descarga": FECHA})
        geom = unary_union(por[fila["zona"]])
        feats.append({"type": "Feature", "properties": props, "geometry": mapping(geom)})
    salida = {"type": "FeatureCollection", "name": "zonas_propuestas_sanisidro",
              "crs": radios.get("crs"), "features": feats}
    ruta = os.path.join(DATA, "zonas_propuestas_sanisidro.geojson")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False)

    total = sum(f["poblacion"] for f in filas)
    ruta_res = os.path.join(DATA, "zonas_resumen.csv")
    with open(ruta_res, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zona", "radios", "poblacion", "hogares", "viviendas",
                    "poblacion_pct_del_partido", "relacion_osm", "limite", "fecha"])
        for fila in sorted(filas, key=lambda x: -x["poblacion"]):
            w.writerow([fila["zona"], fila["radios"], fila["poblacion"], fila["hogares"],
                        fila["viviendas"], round(100.0 * fila["poblacion"] / total, 2),
                        relacion[fila["zona"]], LIMITE, FECHA])
    for fila in filas:
        print(f"  {fila['zona']:18s} {fila['radios']:3d} radios {fila['poblacion']:7d} hab  NBI {fila['pct_nbi']:.2f}%")
    print("->", ruta)
    print("->", ruta_res)


if __name__ == "__main__":
    main()
