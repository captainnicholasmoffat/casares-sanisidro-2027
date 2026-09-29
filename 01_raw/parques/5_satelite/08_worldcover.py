# -*- coding: utf-8 -*-
"""Referencia ESA WorldCover 10 m v200 (2021): clase de cobertura 2021 en los grupos de poligonos y en los pixeles marcados.
Se reproyecta (vecino mas cercano) a la grilla UTM 21S de 10 m del analisis. Salida: worldcover2021_por_grupo.csv
Clases: 10 arboles, 20 arbustos, 30 pastizal, 40 cultivo, 50 construido, 60 suelo desnudo, 80 agua, 90 humedal herbaceo, 95 manglar, 100 musgo.
"""
import json, csv, os
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.features import rasterize
from shapely.geometry import shape
from shapely.ops import transform
from common import *

URL = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_S36W060_Map.tif"
T = base_transform()
dst = np.zeros((HEIGHT, WIDTH), "uint8")
with rasterio.open(URL) as s:
    w = rasterio.windows.from_bounds(-58.62, -34.55, -58.44, -34.40, s.transform)
    a = s.read(1, window=w)
    reproject(a, dst, src_transform=s.window_transform(w), src_crs=s.crs, dst_transform=T, dst_crs=f"EPSG:{EPSG}", resampling=Resampling.nearest)
with rasterio.open(os.path.join(OUT, "cambio_mascara_bits.tif")) as s:
    code = s.read(1)
pers = (code & 1) > 0
P = json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))
part = shape(json.load(open(os.path.join(OUT, "partido_osm.geojson")))["features"][0]["geometry"])
tu = lambda g: transform(lambda x, y, z=None: to_utm.transform(x, y), g)
pm = rasterize([(tu(part), 1)], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)
def um(cat):
    return rasterize([(tu(shape(f["geometry"])), 1) for f in P["features"] if f["properties"]["cat"] == cat], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)
G = {"publico (parques/plazas/reserva OSM)": um("publico"), "club_control": um("club_control"), "franja_costera": um("franja_costera"),
     "partido": pm, "pixeles cambio persistente (partido+franja)": pers & (pm | um("franja_costera"))}
CL = {10: "arboles", 20: "arbustos", 30: "pastizal", 40: "cultivo", 50: "construido", 60: "desnudo", 80: "agua", 90: "humedal"}
rows = []
for g, m in G.items():
    v = dst[m]; n = len(v)
    r = {"grupo": g, "px": n}
    for k, nm in CL.items():
        r[nm + "_pct"] = round(100 * float((v == k).mean()), 1) if n else 0
    rows.append(r); print(r)
with open(os.path.join(OUT, "worldcover2021_por_grupo.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
