# -*- coding: utf-8 -*-
"""Inventario de escenas Sentinel-2 L2A (Earth Search v1) sobre San Isidro, 2022-10-01 a 2026-09-28.
Para cada escena lee la banda SCL (20 m) solo en la ventana del partido y calcula la fraccion de pixeles validos
(SCL 4/5/6) dentro del poligono del partido (OSM relation 1769044).
Salida: escenas_inventario.csv
"""
import json, csv, os, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import rasterio
from rasterio.windows import Window
from rasterio.features import rasterize
from shapely.geometry import shape
from shapely.ops import transform
from pystac_client import Client
from common import *

DT = "2022-10-01/2026-09-28"
c = Client.open(STAC)
items = list(c.search(collections=[COLL], bbox=[-58.60, -34.535, -58.465, -34.425], datetime=DT,
                      query={"eo:cloud_cover": {"lt": 80}}, max_items=5000).items())
items = [it for it in items if it.properties.get("grid:code") == TILE]
print("items", len(items))

part = shape(json.load(open(os.path.join(OUT, "partido_osm.geojson")))["features"][0]["geometry"])
part_u = transform(lambda x, y, z=None: to_utm.transform(x, y), part)
from affine import Affine
T20 = Affine(20, 0, X0, 0, -20, Y0)
mask20 = rasterize([(part_u, 1)], out_shape=(HEIGHT // 2, WIDTH // 2), transform=T20, fill=0, dtype="uint8").astype(bool)

def work(it):
    href = it.assets["scl"].href
    try:
        with rasterio.open(href) as s:
            assert s.transform.a == 20
            col = int(round((X0 - s.transform.c) / 20)); row = int(round((s.transform.f - Y0) / 20))
            a = s.read(1, window=Window(col, row, WIDTH // 2, HEIGHT // 2))
        v = a[mask20]
        valid = np.isin(v, SCL_VALID)
        frac = valid.mean()
        cnt = {k: float((v == k).mean()) for k in range(12)}
        return it, frac, cnt, None
    except Exception as e:
        return it, None, None, str(e)

rows = []
with ThreadPoolExecutor(8) as ex:
    for it, frac, cnt, err in ex.map(work, items):
        p = it.properties
        rows.append({"id": it.id, "fecha_utc": p["datetime"][:19], "plataforma": p["platform"], "sensor": "MSI",
                     "nubes_escena_pct": round(p["eo:cloud_cover"], 2), "baseline": p.get("s2:processing_baseline"),
                     "frac_valida_partido": None if frac is None else round(float(frac), 4),
                     "nube_partido_pct": None if cnt is None else round(100 * (cnt[8] + cnt[9] + cnt[10]), 2),
                     "sombra_partido_pct": None if cnt is None else round(100 * (cnt[3] + cnt[2]), 2),
                     "noclasif_partido_pct": None if cnt is None else round(100 * cnt[7], 2),
                     "producto": p.get("s2:product_uri"), "scl_href": it.assets["scl"].href, "error": err})
rows.sort(key=lambda r: r["fecha_utc"])
with open(os.path.join(OUT, "escenas_inventario.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
ok = [r for r in rows if r["frac_valida_partido"] is not None and r["frac_valida_partido"] >= AOI_CLEAR_MIN]
print("escenas con >= %.0f%% validos en el partido: %d" % (100 * AOI_CLEAR_MIN, len(ok)))
