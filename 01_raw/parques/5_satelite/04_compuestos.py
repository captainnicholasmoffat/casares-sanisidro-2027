# -*- coding: utf-8 -*-
"""Compuestos estacionales (mediana por pixel) de NDVI, NDWI, NDBI, BSI y reflectancias, con mascara SCL.
Estaciones meteorologicas: DJF (dic-feb), MAM, JJA, SON. Solo escenas con >= 90% de pixeles validos en el partido.
Mascara por escena: validos = SCL en {4,5,6}; se excluyen ademas los pixeles a <= 20 m de nube (8,9,10) o sombra de nube (3).
Salida: <CACHE>/comp_<estacion>.npz y compuestos_resumen.csv (escenas usadas por estacion).
"""
import csv, os, datetime as dt
import numpy as np
from scipy import ndimage
from common import *

rows = list(csv.DictReader(open(os.path.join(OUT, "escenas_inventario.csv"))))
ok = [r for r in rows if r["frac_valida_partido"] and float(r["frac_valida_partido"]) >= AOI_CLEAR_MIN]
# una sola escena por fecha (en 2024-2026 hay duplicados S2A/S2C en tandem o reprocesados '_1_'): se queda la de mayor fraccion valida
best = {}
for r in ok:
    k = r["fecha_utc"][:10]
    if k not in best or float(r["frac_valida_partido"]) > float(best[k]["frac_valida_partido"]):
        best[k] = r
ok = sorted(best.values(), key=lambda r: r["fecha_utc"])
_co = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "coregistro_escenas.csv")))}
ok = [r for r in ok if _co[r["id"]]["accion"] != "excluida"]  # escenas con error geometrico grosero

def season_of(d):
    m, y = d.month, d.year
    if m == 12:
        return f"DJF {y}-{str(y+1)[2:]}"
    if m in (1, 2):
        return f"DJF {y-1}-{str(y)[2:]}"
    if m in (3, 4, 5):
        return f"MAM {y}"
    if m in (6, 7, 8):
        return f"JJA {y}"
    return f"SON {y}"

groups = {}
for r in ok:
    d = dt.datetime.fromisoformat(r["fecha_utc"])
    groups.setdefault(season_of(d), []).append(r)

def idx(a, b):
    with np.errstate(invalid="ignore", divide="ignore"):
        return (a - b) / (a + b)

summ = []
for s, rr in sorted(groups.items(), key=lambda kv: kv[1][0]["fecha_utc"]):
    stack = {k: [] for k in ["NDVI", "NDWI", "NDBI", "BSI", "B02", "B03", "B04", "B08", "B11", "WAT"]}
    for r in rr:
        z = load_scene(r["id"])  # corregistrada
        B = {k: z[k].astype("float32") * 1e-4 for k in ["B02", "B03", "B04", "B08", "B11"]}
        scl = z["SCL"]
        cloud = np.isin(scl, (3, 8, 9, 10))
        cloud = ndimage.binary_dilation(cloud, iterations=2)
        valid = np.isin(scl, SCL_VALID) & ~cloud & (z["B04"] > 0) & (z["B08"] > 0)
        nan = np.float32(np.nan)
        stack["NDVI"].append(np.where(valid, idx(B["B08"], B["B04"]), nan))
        stack["NDWI"].append(np.where(valid, idx(B["B03"], B["B08"]), nan))
        stack["NDBI"].append(np.where(valid, idx(B["B11"], B["B08"]), nan))
        stack["BSI"].append(np.where(valid, idx(B["B11"] + B["B04"], B["B08"] + B["B02"]), nan))
        for k in ["B02", "B03", "B04", "B08", "B11"]:
            stack[k].append(np.where(valid, B[k], nan))
        stack["WAT"].append(np.where(valid, (scl == 6).astype("float32"), nan))
    out = {}
    for k, v in stack.items():
        a = np.stack(v)
        out[k] = (np.nanmean(a, axis=0) if k == "WAT" else np.nanmedian(a, axis=0)).astype("float32")
        if k == "NDVI":
            out["N"] = np.sum(~np.isnan(a), axis=0).astype("uint8")
    np.savez_compressed(os.path.join(CACHE, "comp_" + s.replace(" ", "_") + ".npz"), **out)
    summ.append({"estacion": s, "n_escenas": len(rr), "ids": ";".join(r["id"] for r in rr),
                 "fechas": ";".join(r["fecha_utc"][:10] for r in rr),
                 "nubes_escena_pct": ";".join(r["nubes_escena_pct"] for r in rr),
                 "valido_partido_pct": ";".join(str(round(100 * float(r["frac_valida_partido"]), 1)) for r in rr)})
    print(s, len(rr), flush=True)
with open(os.path.join(OUT, "compuestos_resumen.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summ[0].keys())); w.writeheader(); w.writerows(summ)
