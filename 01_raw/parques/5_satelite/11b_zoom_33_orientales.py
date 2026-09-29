# -*- coding: utf-8 -*-
"""Zoom Wayback (z19, lado 140 m) sobre el paseo 33 Orientales (Beccar) en 3 capturas: 2023-03-12 WV03, 2025-05-11 LG01, 2025-12-28 WV02.
Solo verificacion visual (las capturas Wayback no estan corregistradas entre si: se ven corrimientos de ~10-20 m).
Salida: png/zoom_33_Orientales_hr.png"""
exec(open("11_revision_candidatos.py").read().split("jobs = [")[0])  # reutiliza mosaic(), FONT, etc.
from PIL import Image, ImageDraw
lat, lon = -34.4503, -58.5172
pans = []
for rid, lab in [(16453, "captura 2023-03-12 WV03 0,31 m"), (49999, "captura 2025-05-11 LG01 0,34 m"), (49059, "captura 2025-12-28 WV02 0,5 m")]:
    im, ll2px, mpp = mosaic(rid, lat, lon, 70, z=19)
    im = im.resize((560, 560), Image.LANCZOS); s = 560 / 140.0
    d = ImageDraw.Draw(im)
    d.rectangle([10, 540, 10 + 20 * s, 546], fill=(255, 255, 255)); d.text((12, 524), "20 m", fill=(255, 255, 255), font=FONT)
    for k in range(0, 141, 10):
        d.line([(k * s, 0), (k * s, 6)], fill=(255, 255, 0))
    out = Image.new("RGB", (560, 590), (255, 255, 255)); out.paste(im, (0, 30))
    ImageDraw.Draw(out).text((3, 5), f"33 Orientales (Beccar) {lat},{lon} - {lab} - lado 140 m (marcas cada 10 m)", fill=(0, 0, 0), font=FONT)
    pans.append(out)
sh = Image.new("RGB", (560 * 3, 590), (255, 255, 255))
for i, p in enumerate(pans): sh.paste(p, (i * 560, 0))
sh.convert("P", palette=Image.ADAPTIVE, colors=192).save("png/zoom_33_Orientales_hr.png", optimize=True)
