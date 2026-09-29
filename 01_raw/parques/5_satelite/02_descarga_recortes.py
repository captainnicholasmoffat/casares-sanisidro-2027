# -*- coding: utf-8 -*-
"""Descarga (lectura HTTP por rangos de los COG) de las bandas B02,B03,B04,B08 (10 m), B11 y SCL (20 m)
SOLO en la ventana del partido (1224 x 1240 px de 10 m) para cada escena con >= 90% de pixeles validos
en el partido. Guarda un .npz por escena en el cache temporal (NO entregable).
"""
import csv, os, sys, time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import rasterio
from rasterio.windows import Window
from common import *

rows = list(csv.DictReader(open(os.path.join(OUT, "escenas_inventario.csv"))))
ok = [r for r in rows if r["frac_valida_partido"] and float(r["frac_valida_partido"]) >= AOI_CLEAR_MIN]
BANDS10 = {"B02": "blue", "B03": "green", "B04": "red", "B08": "nir"}
BANDS20 = {"B11": "swir16", "SCL": "scl"}

def base(r):
    return r["scl_href"].rsplit("/", 1)[0]

def read(href, res):
    for k in range(4):
        try:
            with rasterio.open(href) as s:
                assert abs(s.transform.a - res) < 1e-6
                col = int(round((X0 - s.transform.c) / res)); row = int(round((s.transform.f - Y0) / res))
                f = int(round(RES / res)) if res < RES else 1
                w = WIDTH if res == 10 else WIDTH // 2
                h = HEIGHT if res == 10 else HEIGHT // 2
                return s.read(1, window=Window(col, row, w, h))
        except Exception as e:
            err = e; time.sleep(3)
    raise err

def work(r):
    fn = os.path.join(CACHE, r["id"] + ".npz")
    if os.path.exists(fn):
        return r["id"], "cache"
    b = base(r)
    d = {}
    for k in BANDS10:
        d[k] = read(f"{b}/{k}.tif", 10)
    for k in BANDS20:
        a = read(f"{b}/{k}.tif", 20)
        d[k] = np.repeat(np.repeat(a, 2, axis=0), 2, axis=1)  # 20 m -> grilla 10 m (vecino mas cercano)
    np.savez_compressed(fn, **d)
    return r["id"], "ok"

t = time.time()
with ThreadPoolExecutor(6) as ex:
    for i, (sid, st) in enumerate(ex.map(work, ok)):
        if i % 10 == 0:
            print(i, sid, st, round(time.time() - t), flush=True)
print("listo", len(ok), round(time.time() - t))
