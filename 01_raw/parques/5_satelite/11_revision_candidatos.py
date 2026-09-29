# -*- coding: utf-8 -*-
"""Revision visual (Esri World Imagery Wayback, 0,3-0,5 m) de los candidatos del ranking blando (10_ranking_blando.py) y de un
sitio detectado a ojo en la revision (cancha nueva en Boulogne). Dibuja el poligono OSM (cian) y los pixeles S2 con caida fuerte
persistente (magenta). Salida: png/rev_<pid>_hr.png
"""
import json, csv, os, math, io
import numpy as np, requests
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape, Point
from shapely.ops import transform
from rasterio.features import shapes
from affine import Affine
from concurrent.futures import ThreadPoolExecutor
from common import *

PNG = os.path.join(OUT, "png")
P = {f["properties"]["pid"]: f for f in json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))["features"]}
import sys
CAND = [int(a) for a in sys.argv[1:]] or [48, 85, 5, 153, 87, 8, 50, 128, 174]  # 174 = Parque Natural Municipal Ribera Norte
EXTRA = [] if sys.argv[1:] else [("rev_cancha_Boulogne", -34.49084, -58.58287), ("rev_RiberaNorte_caida_NDVI", -34.4662, -58.4940)]
REL = [(25982, "rel. 2023-06-13"), (16453, "rel. 2024-12-12"), (49999, "rel. 2025-07-31"), (49059, "rel. 2026-04-30")]
S = requests.Session(); S.headers["User-Agent"] = "sanisidro-research/0.1"
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except Exception:
    FONT = ImageFont.load_default()

# pixeles con caida fuerte persistente (mismo criterio que 10_ranking_blando.py)
PARES = [("DJF 2023-24", "DJF 2025-26"), ("JJA 2023", "JJA 2026"), ("SON 2023", "SON 2025")]
Cc = {s: np.load(os.path.join(CACHE, "comp_" + s.replace(" ", "_") + ".npz")) for p in PARES for s in p}
d = np.stack([np.where((Cc[a]["N"] >= 3) & (Cc[b]["N"] >= 3), Cc[b]["NDVI"] - Cc[a]["NDVI"], np.nan) for a, b in PARES])
strong = (np.nan_to_num(d, nan=0) <= -0.20).sum(axis=0) >= 2

def deg2num(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n

def mosaic(rid, lat, lon, half_m, z=19):
    cx, cy = deg2num(lat, lon, z)
    mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
    hp = half_m / mpp / 256.0
    x0, x1, y0, y1 = cx - hp, cx + hp, cy - hp, cy + hp
    wbc = os.path.join(CACHE, "wb"); os.makedirs(wbc, exist_ok=True)
    def get(k):
        tx, ty = k
        fn = os.path.join(wbc, f"{rid}_{z}_{ty}_{tx}.jpg")
        if not os.path.exists(fn):
            r = S.get(f"https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{rid}/{z}/{ty}/{tx}", timeout=60)
            r.raise_for_status(); open(fn, "wb").write(r.content)
        return k, Image.open(fn).convert("RGB")
    keys = [(tx, ty) for tx in range(int(x0), int(x1) + 1) for ty in range(int(y0), int(y1) + 1)]
    with ThreadPoolExecutor(8) as ex:
        tiles = dict(ex.map(get, keys))
    big = Image.new("RGB", ((int(x1) - int(x0) + 1) * 256, (int(y1) - int(y0) + 1) * 256))
    for (tx, ty), im in tiles.items():
        big.paste(im, ((tx - int(x0)) * 256, (ty - int(y0)) * 256))
    ox, oy = (x0 - int(x0)) * 256, (y0 - int(y0)) * 256
    crop = big.crop((int(ox), int(oy), int(ox + 2 * hp * 256), int(oy + 2 * hp * 256)))
    def ll2px(la, lo):
        X, Y = deg2num(la, lo, z)
        return (X - x0) * 256, (Y - y0) * 256
    return crop, ll2px, mpp

def strong_polys(lat, lon, half_m):
    x, y = to_utm.transform(lon, lat)
    r, c = int((Y0 - y) / RES), int((x - X0) / RES)
    k = int(half_m / RES) + 2
    sub = strong[r - k:r + k, c - k:c + k]
    Ts = Affine(RES, 0, X0 + (c - k) * RES, 0, -RES, Y0 - (r - k) * RES)
    return [transform(lambda a, b, z=None: to_ll.transform(a, b), shape(g)) for g, v in shapes(sub.astype("uint8"), mask=sub, transform=Ts)]

jobs = [(f"rev_pid{pid}", P[pid]) for pid in CAND] + [(n, (la, lo)) for n, la, lo in EXTRA]
for name, obj in jobs:
    if isinstance(obj, dict):
        g = shape(obj["geometry"]); c = g.centroid; lat, lon = c.y, c.x
        gu = transform(lambda a, b, z=None: to_utm.transform(a, b), g)
        half = max(60, min(450, 0.6 * max(gu.bounds[2] - gu.bounds[0], gu.bounds[3] - gu.bounds[1])))
        title = f"pid {obj['properties']['pid']} {obj['properties']['osm']} {obj['properties']['name'][:30]} ({obj['properties']['area_m2']:.0f} m2)"
    else:
        lat, lon = obj; g = None; half = 80; title = name
    sp = strong_polys(lat, lon, half)
    pans = []
    for rid, lab in REL:
        im, ll2px, mpp = mosaic(rid, lat, lon, half)
        dr = ImageDraw.Draw(im)
        if g is not None:
            for gg in getattr(g, "geoms", [g]):
                dr.line([ll2px(la, lo) for lo, la in gg.exterior.coords], fill=(0, 255, 255), width=2)
        for q in sp:
            dr.line([ll2px(la, lo) for lo, la in q.exterior.coords], fill=(255, 0, 255), width=2)
        im = im.resize((380, 380), Image.LANCZOS)
        out = Image.new("RGB", (380, 410), (255, 255, 255)); out.paste(im, (0, 30))
        ImageDraw.Draw(out).text((3, 2), f"Wayback {lab} (id {rid})\nlado {2*half:.0f} m", fill=(0, 0, 0), font=FONT)
        pans.append(out)
    sheet = Image.new("RGB", (380 * len(pans), 430), (255, 255, 255))
    for i, p in enumerate(pans):
        sheet.paste(p, (i * 380, 20))
    ImageDraw.Draw(sheet).text((3, 3), f"{title}  {lat:.5f},{lon:.5f}  cian=poligono OSM  magenta=pixeles S2 con caida NDVI<=-0,2 en >=2 pares", fill=(0, 0, 0), font=FONT)
    sheet.convert("P", palette=Image.ADAPTIVE, colors=192).save(os.path.join(PNG, f"{name}_hr.png"), optimize=True)
    print("ok", name, flush=True)
