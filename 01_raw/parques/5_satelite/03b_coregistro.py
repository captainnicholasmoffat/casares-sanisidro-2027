# -*- coding: utf-8 -*-
"""Corregistro relativo entre escenas. Se detecto que las escenas S2A de 2022-10 a 2023-11 estan desplazadas ~1 pixel (10 m)
en N-S respecto de las posteriores, y que S2B_21HUB_20250318_0_L2A esta desplazada ~11 px N-S y ~5 px E-O (error geometrico).
Metodo: correlacion de fase subpixel (scikit-image, upsample 20) de la banda B08 en una ventana central de 1024x1024 px
contra la escena de referencia S2A_21HUB_20250325_1_L2A. Se aplica el desplazamiento (bilineal; SCL vecino mas cercano) si |d|>=0,2 px.
Escenas con |d| > 3 px se EXCLUYEN (error geometrico grosero). Salida: coregistro_escenas.csv
"""
import csv, os
import numpy as np
from skimage.registration import phase_cross_correlation
from common import *

REF = "S2A_21HUB_20250325_1_L2A"
rows = list(csv.DictReader(open(os.path.join(OUT, "escenas_inventario.csv"))))
ok = [r for r in rows if r["frac_valida_partido"] and float(r["frac_valida_partido"]) >= AOI_CLEAR_MIN]
ref = np.load(os.path.join(CACHE, REF + ".npz"))["B08"][100:1124, 100:1124].astype(float)
out = []
for r in ok:
    a = np.load(os.path.join(CACHE, r["id"] + ".npz"))["B08"][100:1124, 100:1124].astype(float)
    s, err, _ = phase_cross_correlation(ref, a, upsample_factor=20)
    mag = float(np.hypot(*s))
    out.append({"id": r["id"], "fecha": r["fecha_utc"][:10], "dfila_px": round(float(s[0]), 2), "dcol_px": round(float(s[1]), 2),
                "desplazamiento_m": round(mag * 10, 1), "accion": "excluida" if mag > 3 else ("corregida" if mag >= 0.2 else "sin cambio")})
with open(os.path.join(OUT, "coregistro_escenas.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
import collections
print(collections.Counter(o["accion"] for o in out))
for o in out:
    if o["accion"] != "sin cambio":
        print(o)
