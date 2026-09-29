# -*- coding: utf-8 -*-
"""Serie NDVI/NDWI por escena del mayor parche con caida fuerte de NDVI dentro del poligono OSM del Parque Natural Municipal
Ribera Norte (relation/10343663), cerca de -34.4660,-58.4935. Salida: serie_ribera_norte_parche.csv"""
import json, os, csv, numpy as np
from rasterio.features import rasterize
from shapely.geometry import shape
from shapely.ops import transform
from scipy import ndimage
from common import *
PARES = [("DJF 2023-24", "DJF 2025-26"), ("JJA 2023", "JJA 2026"), ("SON 2023", "SON 2025")]
C = {s: np.load(os.path.join(CACHE, "comp_" + s.replace(" ", "_") + ".npz")) for p in PARES for s in p}
d = np.stack([np.where((C[a]["N"] >= 3) & (C[b]["N"] >= 3), C[b]["NDVI"] - C[a]["NDVI"], np.nan) for a, b in PARES])
strong = (np.nan_to_num(d, nan=0) <= -0.2).sum(0) >= 2
P = json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))
g = [shape(f["geometry"]) for f in P["features"] if f["properties"]["osm"] == "relation/10343663"][0]
m = rasterize([(transform(lambda x, y, z=None: to_utm.transform(x, y), g), 1)], out_shape=(HEIGHT, WIDTH), transform=base_transform(), fill=0, dtype="uint8").astype(bool)
lab, n = ndimage.label(strong & m, structure=np.ones((3, 3)))
k = np.argmax(ndimage.sum(strong & m, lab, range(1, n + 1))) + 1
pk = lab == k
print("px parche:", int(pk.sum()))
inv = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "escenas_usadas.csv"))) if r["estacion"] != "EXCLUIDA"}
out = []
for sid, r in sorted(inv.items(), key=lambda kv: kv[1]["fecha_utc"]):
    z = load_scene(sid)
    ok = np.isin(z["SCL"][pk], SCL_VALID)
    if ok.mean() < 0.8:
        continue
    b3, b4, b8 = (z[b][pk][ok].astype(float) for b in ("B03", "B04", "B08"))
    out.append({"fecha": r["fecha_utc"][:10], "id": sid, "ndvi_mediana": round(float(np.median((b8 - b4) / (b8 + b4))), 3),
                "ndwi_mediana": round(float(np.median((b3 - b8) / (b3 + b8))), 3), "px_validos": int(ok.sum())})
with open(os.path.join(OUT, "serie_ribera_norte_parche.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
for o in out[::3]:
    print(o["fecha"], o["ndvi_mediana"], o["ndwi_mediana"])
