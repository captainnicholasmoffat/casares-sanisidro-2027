# -*- coding: utf-8 -*-
"""Exporta entregables chicos: escenas_usadas.csv (una fila por imagen), NDVI de compuestos clave (GeoTIFF int8 = NDVI*100,
recortado al partido+franja), resultados_por_poligono.geojson (poligonos con resultados)."""
import csv, json, os
import numpy as np, rasterio
from common import *

inv = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "escenas_inventario.csv")))}
co = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "coregistro_escenas.csv")))}
rows = []
for r in csv.DictReader(open(os.path.join(OUT, "compuestos_resumen.csv"))):
    for sid in r["ids"].split(";"):
        i = inv[sid]; c = co[sid]
        rows.append({"estacion": r["estacion"], "id": sid, "fecha_utc": i["fecha_utc"], "plataforma": i["plataforma"], "sensor": "MSI L2A",
                     "baseline": i["baseline"], "nubes_escena_pct": i["nubes_escena_pct"],
                     "valido_partido_pct": round(100 * float(i["frac_valida_partido"]), 1), "nube_partido_pct": i["nube_partido_pct"],
                     "corregistro_dfila_px": c["dfila_px"], "corregistro_dcol_px": c["dcol_px"], "corregistro": c["accion"],
                     "producto_esa": i["producto"], "url_scl": i["scl_href"]})
for sid, c in co.items():
    if c["accion"] == "excluida":
        i = inv[sid]
        rows.append({"estacion": "EXCLUIDA", "id": sid, "fecha_utc": i["fecha_utc"], "plataforma": i["plataforma"], "sensor": "MSI L2A",
                     "baseline": i["baseline"], "nubes_escena_pct": i["nubes_escena_pct"], "valido_partido_pct": round(100 * float(i["frac_valida_partido"]), 1),
                     "nube_partido_pct": i["nube_partido_pct"], "corregistro_dfila_px": c["dfila_px"], "corregistro_dcol_px": c["dcol_px"],
                     "corregistro": "excluida (desplazamiento geometrico ~120 m)", "producto_esa": i["producto"], "url_scl": i["scl_href"]})
with open(os.path.join(OUT, "escenas_usadas.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("escenas usadas:", sum(1 for r in rows if r["estacion"] != "EXCLUIDA"))

T = base_transform()
os.makedirs(os.path.join(OUT, "ndvi_compuestos"), exist_ok=True)
for s in ["JJA 2023", "DJF 2023-24", "DJF 2025-26", "JJA 2026"]:  # SON omitidos por tamano (<20 MB total)
    z = np.load(os.path.join(CACHE, "comp_" + s.replace(" ", "_") + ".npz"))
    a = np.where(np.isnan(z["NDVI"]), -128, np.clip(np.round(z["NDVI"] * 100), -100, 100)).astype("int8")
    fn = os.path.join(OUT, "ndvi_compuestos", "ndvi_mediana_" + s.replace(" ", "_") + ".tif")
    with rasterio.open(fn, "w", driver="GTiff", height=HEIGHT, width=WIDTH, count=1, dtype="int8", crs=f"EPSG:{EPSG}", transform=T,
                       compress="deflate", zlevel=9, nodata=-128) as d:
        d.write(a, 1); d.update_tags(descripcion=f"NDVI*100 (int8), mediana por pixel de escenas Sentinel-2 L2A {s} (ver escenas_usadas.csv)")
    print(fn, os.path.getsize(fn))

res = {r["pid"]: r for r in csv.DictReader(open(os.path.join(OUT, "resultados_por_poligono.csv"))) if r["pid"] != ""}
P = json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))
for f in P["features"]:
    r = res.get(str(f["properties"]["pid"]))
    if r:
        for k, v in r.items():
            if k not in ("pid", "cat", "osm", "nombre", "tag", "area_vector_m2"):
                f["properties"][k] = float(v) if v not in ("", None) else None
json.dump(P, open(os.path.join(OUT, "resultados_por_poligono.geojson"), "w"))
print("ok")
