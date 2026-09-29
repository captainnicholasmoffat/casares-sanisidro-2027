# -*- coding: utf-8 -*-
"""Parametros y utilidades comunes - p4_satelite (San Isidro, verde -> no verde 2023-2026).
Fuente de imagenes: Sentinel-2 L2A (Element84 Earth Search v1, coleccion sentinel-2-l2a, tile MGRS 21HUB).
Reflectancia = DN * 0.0001 (en Earth Search v1, para baseline >= 04.00 'earthsearch:boa_offset_applied'=True:
el offset BOA -1000 ya esta aplicado en los COG; verificado comparando distribucion de DN con escena 2021 baseline 02.14).
"""
import os
os.environ.update({
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif",
    "GDAL_HTTP_MULTIRANGE": "YES",
    "GDAL_HTTP_MERGE_CONSECUTIVE_RANGES": "YES",
    "GDAL_CURL_CA_BUNDLE": "/root/.ccr/ca-bundle.crt",
    "GDAL_HTTP_MAX_RETRY": "5",
    "GDAL_HTTP_RETRY_DELAY": "2",
})
from pyproj import Transformer

OUT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.dirname(OUT), "..", "p4_cache")  # cache temporal (NO entregable, se borra al final)
CACHE = os.path.abspath(CACHE)
os.makedirs(CACHE, exist_ok=True)

STAC = "https://earth-search.aws.element84.com/v1"
COLL = "sentinel-2-l2a"
TILE = "MGRS-21HUB"
EPSG = 32721
# Ventana de analisis (partido de San Isidro + margen) en UTM 21S, alineada a la grilla de 10 m del tile 21HUB
TILE_X0, TILE_Y0 = 300000.0, 6200020.0
COL_OFF, ROW_OFF, WIDTH, HEIGHT = 5316, 1026, 1224, 1240  # pares: alineado a la grilla de 20 m  # grilla 10 m
X0 = TILE_X0 + COL_OFF * 10
Y0 = TILE_Y0 - ROW_OFF * 10
RES = 10.0
# Clases SCL consideradas validas (4 vegetacion, 5 no vegetado, 6 agua). Excluidas: 0 nodata, 1 saturado,
# 2 sombra oscura/topografica, 3 sombra de nube, 7 no clasificado, 8/9 nube media/alta, 10 cirro, 11 nieve.
SCL_VALID = (4, 5, 6)
AOI_CLEAR_MIN = 0.90  # fraccion minima de pixeles validos dentro del partido para usar la escena (<10% nubes/sombras)

to_utm = Transformer.from_crs(4326, EPSG, always_xy=True)
to_ll = Transformer.from_crs(EPSG, 4326, always_xy=True)

def base_transform():
    from affine import Affine
    return Affine(RES, 0, X0, 0, -RES, Y0)

# ---------- carga de escena corregistrada (ver 03b_coregistro.py) ----------
_SHIFTS = None
def load_scene(sid):
    """Devuelve dict de bandas (uint16/uint8) de la escena ya corregistrada; None si la escena esta excluida."""
    import csv, numpy as np
    from scipy import ndimage
    global _SHIFTS
    if _SHIFTS is None:
        fn = os.path.join(OUT, "coregistro_escenas.csv")
        _SHIFTS = {r["id"]: r for r in csv.DictReader(open(fn))} if os.path.exists(fn) else {}
    z = dict(np.load(os.path.join(CACHE, sid + ".npz")))
    r = _SHIFTS.get(sid)
    if r is None:
        return z
    if r["accion"] == "excluida":
        return None
    if r["accion"] == "corregida":
        s = (float(r["dfila_px"]), float(r["dcol_px"]))
        for k in list(z):
            order = 0 if k == "SCL" else 1
            z[k] = ndimage.shift(z[k].astype("float32"), s, order=order, mode="constant", cval=0).round().astype(z[k].dtype)
    return z
