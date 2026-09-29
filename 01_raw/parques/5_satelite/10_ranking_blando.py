# -*- coding: utf-8 -*-
"""Indicador 'blando' para encontrar cambios PARCIALES (menores a un pixel entero) en parques/plazas:
por pixel, caida de NDVI dNDVI = NDVI_despues - NDVI_antes en cada par de misma estacion; 'caida fuerte persistente' = dNDVI <= -0,20
en >= 2 de los 3 pares (verano DJF23-24->DJF25-26, invierno JJA23->JJA26, primavera SON23->SON25).
Se calcula por poligono publico y, como referencia de ruido, en clubes/golf y en todos los pixeles vegetados del partido.
Salida: ranking_caida_ndvi_publicos.csv (ordenado por m2 con caida fuerte persistente).
Esto NO mide m2 de solado: marca candidatos para revisar con imagen de alta resolucion.
"""
import json, csv, os
import numpy as np
from rasterio.features import rasterize
from shapely.geometry import shape
from shapely.ops import transform
from common import *

PARES = [("DJF 2023-24", "DJF 2025-26"), ("JJA 2023", "JJA 2026"), ("SON 2023", "SON 2025")]
C = {s: np.load(os.path.join(CACHE, "comp_" + s.replace(" ", "_") + ".npz")) for p in PARES for s in p}
d = []
for a, b in PARES:
    ok = (C[a]["N"] >= 3) & (C[b]["N"] >= 3)
    d.append(np.where(ok, C[b]["NDVI"] - C[a]["NDVI"], np.nan))
d = np.stack(d)
strong = (np.nan_to_num(d, nan=0) <= -0.20).sum(axis=0) >= 2
dmean = np.nanmean(d, axis=0)
T = base_transform()
tu = lambda g: transform(lambda x, y, z=None: to_utm.transform(x, y), g)
P = json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))
part = shape(json.load(open(os.path.join(OUT, "partido_osm.geojson")))["features"][0]["geometry"])
pm = rasterize([(tu(part), 1)], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)
veg = (C["DJF 2023-24"]["NDVI"] >= 0.4)
rows = []
for f in P["features"]:
    p = f["properties"]
    if p["cat"] not in ("publico", "club_control", "caso"):
        continue
    m = rasterize([(tu(shape(f["geometry"])), 1)], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)
    n = int(m.sum())
    if n < 5:
        continue
    g = shape(f["geometry"]).centroid
    rows.append({"pid": p["pid"], "cat": p["cat"], "osm": p["osm"], "nombre": p["name"], "area_vector_m2": p["area_m2"], "px": n,
                 "dNDVI_medio_verano": round(float(np.nanmean(d[0][m])), 3), "dNDVI_medio_invierno": round(float(np.nanmean(d[1][m])), 3),
                 "dNDVI_medio_primavera": round(float(np.nanmean(d[2][m])), 3),
                 "caida_fuerte_persistente_m2": int(strong[m].sum()) * 100, "caida_fuerte_pct": round(100 * float(strong[m].mean()), 1),
                 "lat": round(g.y, 6), "lon": round(g.x, 6)})
rows.sort(key=lambda r: (-r["caida_fuerte_persistente_m2"], r["dNDVI_medio_verano"]))
with open(os.path.join(OUT, "ranking_caida_ndvi_publicos.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for grp in ("publico", "club_control", "caso"):
    rr = [r for r in rows if r["cat"] == grp]
    tot = sum(r["px"] for r in rr) * 100; st = sum(r["caida_fuerte_persistente_m2"] for r in rr)
    print(grp, "n", len(rr), "area m2", tot, "caida fuerte persistente m2", st, "pct", round(100 * st / tot, 2))
vm = pm & veg
print("partido vegetado (NDVI DJF23-24>=0.4): pct con caida fuerte persistente", round(100 * float(strong[vm].mean()), 2))
for r in [r for r in rows if r["cat"] == "publico"][:15]:
    print(r)
