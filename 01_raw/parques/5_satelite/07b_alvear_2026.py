# -*- coding: utf-8 -*-
"""Recorte S2 RGB (10 m) en Alvear y el rio (-34.48067,-58.48391) para fechas 2026 (cambio detectado en feb-2026).
Salida: png/alvear_y_el_rio_2026_s2.png"""
import numpy as np, os, csv
from PIL import Image, ImageDraw, ImageFont
from common import *
inv = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "escenas_inventario.csv")))}
IDS = ["S2B_21HUB_20260112_0_L2A", "S2C_21HUB_20260206_0_L2A", "S2C_21HUB_20260308_0_L2A", "S2C_21HUB_20260616_0_L2A", "S2B_21HUB_20260919_0_L2A"]
IDS = [i for i in IDS if i in inv] or IDS
lat, lon = -34.480666, -58.483913
x, y = to_utm.transform(lon, lat); r, c = int((Y0 - y) / RES), int((x - X0) / RES)
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
pans = []
for sid in IDS:
    fn = os.path.join(CACHE, sid + ".npz")
    if not os.path.exists(fn):
        print("falta", sid); continue
    z = load_scene(sid)
    a = np.dstack([z[b][r - 20:r + 20, c - 20:c + 20].astype("float32") * 1e-4 for b in ("B04", "B03", "B02")])
    a = (np.clip(a / 0.2, 0, 1) ** (1 / 1.6) * 255).astype("uint8")
    im = Image.fromarray(np.repeat(np.repeat(a, 8, 0), 8, 1)); d = ImageDraw.Draw(im)
    d.rectangle([19 * 8, 19 * 8, 21 * 8, 21 * 8], outline=(255, 0, 0))
    out = Image.new("RGB", (320, 350), (255, 255, 255)); out.paste(im, (0, 30))
    ImageDraw.Draw(out).text((3, 2), f"{sid}\n{inv[sid]['fecha_utc'][:10]} nubes escena {inv[sid]['nubes_escena_pct']}%", fill=(0, 0, 0), font=FONT)
    pans.append(out)
sh = Image.new("RGB", (320 * len(pans), 350), (255, 255, 255))
for i, p in enumerate(pans): sh.paste(p, (i * 320, 0))
sh.save(os.path.join(OUT, "png", "alvear_y_el_rio_2026_s2.png"), optimize=True)
print("ok", len(pans))
