# -*- coding: utf-8 -*-
"""Esri World Imagery Wayback: para cada punto de interes, consulta el servicio de metadatos de cada version (release)
2022-2026 y obtiene la FECHA REAL DE CAPTURA (SRC_DATE), resolucion (SRC_RES) y proveedor (SRC_DESC) de la imagen de
alta resolucion que se muestra en ese punto. Solo sirve para VERIFICACION VISUAL (no es un producto de medicion calibrado).
Salida: wayback_fechas_por_punto.csv
"""
import json, csv, os, requests, time
from concurrent.futures import ThreadPoolExecutor
from common import OUT

CFG_URL = "https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json"
cfg = requests.get(CFG_URL, timeout=60).json()
rels = sorted([(k, v) for k, v in cfg.items() if v["itemTitle"][-11:-7] in ("2022", "2023", "2024", "2025", "2026")], key=lambda kv: kv[1]["itemTitle"])
PTS = json.load(open(os.path.join(OUT, "puntos_verificacion.json")))

def q(args):
    (rid, v), (name, lat, lon) = args
    url = v.get("metadataLayerUrl")
    if not url:
        return None
    for layer in (3, 4, 5, 6):
        try:
            r = requests.get(f"{url}/{layer}/query", params={"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326,
                             "spatialRel": "esriSpatialRelIntersects", "outFields": "SRC_DATE,SRC_RES,SRC_DESC,NICE_DESC", "returnGeometry": "false", "f": "json"}, timeout=60)
            fs = r.json().get("features", [])
        except Exception:
            fs = []
        if fs:
            a = fs[0]["attributes"]
            return {"punto": name, "release_id": rid, "release": v["itemTitle"][-11:-1], "capa": layer, "SRC_DATE": a.get("SRC_DATE"),
                    "SRC_RES_m": a.get("SRC_RES"), "SRC_DESC": a.get("SRC_DESC"), "NICE_DESC": a.get("NICE_DESC")}
    return None

jobs = [(r, p) for p in PTS for r in rels]
out = []
with ThreadPoolExecutor(8) as ex:
    for res in ex.map(q, jobs):
        if res:
            out.append(res)
out.sort(key=lambda r: (r["punto"], r["release"]))
with open(os.path.join(OUT, "wayback_fechas_por_punto.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
# resumen: fechas de captura distintas por punto y primer release que la muestra
seen = {}
for r in out:
    k = (r["punto"], r["SRC_DATE"])
    if k not in seen:
        seen[k] = r
for k, r in sorted(seen.items()):
    print(r["punto"], r["SRC_DATE"], r["SRC_RES_m"], r["SRC_DESC"], "desde release", r["release"], r["release_id"])
