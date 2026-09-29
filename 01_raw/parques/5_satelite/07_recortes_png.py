# -*- coding: utf-8 -*-
"""Recortes PNG para verificacion visual de cada punto de puntos_verificacion.json:
  png/<punto>_s2.png      : Sentinel-2 RGB (B04,B03,B02) de escenas individuales antes/despues (ID y fecha en el titulo),
                            NDVI de compuestos estacionales y mascara de cambio (rojo = persistente >=2 pares; naranja = 1 par;
                            azul = agua->tierra). Recorte 700 m x 700 m, pixel de 10 m.
  png/<punto>_hr.png      : Esri World Imagery Wayback (alta resolucion 0,3-0,5 m, solo verificacion VISUAL) en las capturas
                            disponibles (fecha real de captura segun metadatos), 320 m x 320 m, con contorno de pixeles S2 marcados.
  png/series_ndvi.png     : NDVI por escena (mediana en los pixeles marcados, o circulo de 30 m si no hay) 2022-10 a 2026-09.
"""
import json, csv, os, math, io, datetime as dt
import numpy as np, requests
import rasterio
from rasterio.features import rasterize, shapes
from shapely.geometry import shape, Point, mapping
from shapely.ops import transform, unary_union
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from common import *

PNG = os.path.join(OUT, "png"); os.makedirs(PNG, exist_ok=True)
PTS = json.load(open(os.path.join(OUT, "puntos_verificacion.json")))
inv = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "escenas_inventario.csv")))}
comp = {r["estacion"]: r["ids"].split(";") for r in csv.DictReader(open(os.path.join(OUT, "compuestos_resumen.csv")))}
with rasterio.open(os.path.join(OUT, "cambio_mascara_bits.tif")) as s:
    code = s.read(1)
T = base_transform()
pers = (code & 1) > 0
one = (((code >> 1) & 1) | ((code >> 2) & 1) | ((code >> 3) & 1)).astype(bool) & ~pers
a2t = ((code >> 5) & 1) > 0
P = json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))

def best(season):
    ids = comp[season]
    return max(ids, key=lambda i: float(inv[i]["frac_valida_partido"]))
SCN = [("antes verano", best("DJF 2023-24")), ("antes invierno", best("JJA 2023")), ("despues verano", best("DJF 2025-26")), ("ultimo (sep-2026)", best("SON 2026"))]

def rc(lon, lat):
    x, y = to_utm.transform(lon, lat)
    return int((Y0 - y) / RES), int((x - X0) / RES)

def rgb(sid, r0, c0, h, w):
    z = load_scene(sid)
    a = np.dstack([z[b][r0:r0 + h, c0:c0 + w].astype("float32") * 1e-4 for b in ("B04", "B03", "B02")])
    a = np.clip(a / 0.20, 0, 1) ** (1 / 1.6)
    return (a * 255).astype("uint8")

def ndvi_comp(season, r0, c0, h, w):
    z = np.load(os.path.join(CACHE, "comp_" + season.replace(" ", "_") + ".npz"))
    return z["NDVI"][r0:r0 + h, c0:c0 + w]

def cmap_ndvi(a):
    a = np.nan_to_num(a, nan=-1)
    c = plt.get_cmap("RdYlGn")((np.clip(a, -0.1, 0.9) + 0.1) / 1.0)[..., :3]
    return (c * 255).astype("uint8")

def up(a, k=5):
    return np.repeat(np.repeat(a, k, axis=0), k, axis=1)

def outline(img, mask, color, k=5):
    m = up(mask.astype(bool), k)
    e = m & ~ndimage.binary_erosion(m, iterations=2)
    img = img.copy(); img[e] = color
    return img

def poly_outline(img, r0, c0, h, w, k=5):
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    for f in P["features"]:
        if f["properties"]["cat"] not in ("publico", "caso"):
            continue
        g = transform(lambda x, y, z=None: to_utm.transform(x, y), shape(f["geometry"]))
        for gg in getattr(g, "geoms", [g]):
            xy = [(((x - X0) / RES - c0) * k, ((Y0 - y) / RES - r0) * k) for x, y in gg.exterior.coords]
            if any(0 <= px < w * k and 0 <= py < h * k for px, py in xy):
                d.line(xy, fill=(0, 255, 255), width=1)
    return np.array(im)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except Exception:
    FONT = ImageFont.load_default()

def label(img, text):
    im = Image.fromarray(img); W = im.width
    out = Image.new("RGB", (W, im.height + 30), (255, 255, 255)); out.paste(im, (0, 30))
    d = ImageDraw.Draw(out)
    for i, t in enumerate(text.split("\n")[:2]):
        d.text((3, 2 + 14 * i), t, fill=(0, 0, 0), font=FONT)
    return out

def save_small(im, fn):
    im.convert("P", palette=Image.ADAPTIVE, colors=192).save(fn, optimize=True)

# ---------- Wayback ----------
WB = [(25982, "Wayback rel. 2023-06-13"), (16453, "Wayback rel. 2024-12-12"), (49999, "Wayback rel. 2025-07-31"), (49059, "Wayback rel. 2026-04-30")]
wbd = {}
for r in csv.DictReader(open(os.path.join(OUT, "wayback_fechas_por_punto.csv"))):
    wbd[(r["punto"], int(r["release_id"]))] = r
def deg2num(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y
def num2deg(x, y, z):
    n = 2 ** z
    lon = x / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lat, lon
S = requests.Session(); S.headers["User-Agent"] = "sanisidro-research/0.1"
def wb_mosaic(rid, lat, lon, half_m=160, z=18):
    cx, cy = deg2num(lat, lon, z)
    mpp = 156543.03392 * math.cos(math.radians(lat)) / 2 ** z
    hp = half_m / mpp / 256.0  # medio lado en unidades de tile
    x0, x1, y0, y1 = cx - hp, cx + hp, cy - hp, cy + hp
    from concurrent.futures import ThreadPoolExecutor
    wbc = os.path.join(CACHE, "wb"); os.makedirs(wbc, exist_ok=True)
    def get(k):
        tx, ty = k
        fn = os.path.join(wbc, f"{rid}_{z}_{ty}_{tx}.jpg")
        if not os.path.exists(fn):
            u = f"https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{rid}/{z}/{ty}/{tx}"
            r = S.get(u, timeout=60); r.raise_for_status()
            open(fn, "wb").write(r.content)
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

def s2_mask_polys(r0, c0, h, w, mask):
    out = []
    sub = mask[r0:r0 + h, c0:c0 + w]
    if not sub.any():
        return out
    from affine import Affine
    Ts = Affine(RES, 0, X0 + c0 * RES, 0, -RES, Y0 - r0 * RES)
    for g, v in shapes(sub.astype("uint8"), mask=sub, transform=Ts):
        out.append(transform(lambda x, y, z=None: to_ll.transform(x, y), shape(g)))
    return out

series = {}
masks = {}
for name, lat, lon in PTS:
    r, c = rc(lon, lat)
    h = w = 70; r0, c0 = r - 35, c - 35
    panels = []
    for lab, sid in SCN:
        im = up(rgb(sid, r0, c0, h, w))
        im = poly_outline(im, r0, c0, h, w)
        it = inv[sid]
        panels.append(label(im, f"{lab}: {sid}\n{it['fecha_utc'][:10]} MSI nubes escena {it['nubes_escena_pct']}%"))
    nb = up(cmap_ndvi(ndvi_comp("DJF 2023-24", r0, c0, h, w))); na = up(cmap_ndvi(ndvi_comp("DJF 2025-26", r0, c0, h, w)))
    panels.append(label(nb, "NDVI mediana DJF 2023-24\n(rojo<0,1  verde>0,6)"))
    panels.append(label(na, "NDVI mediana DJF 2025-26"))
    ch = up(rgb(SCN[2][1], r0, c0, h, w))
    ch = outline(ch, one[r0:r0 + h, c0:c0 + w], (255, 165, 0))
    ch = outline(ch, a2t[r0:r0 + h, c0:c0 + w], (0, 90, 255))
    ch = outline(ch, pers[r0:r0 + h, c0:c0 + w], (255, 0, 0))
    panels.append(label(ch, "cambio: rojo=persistente(>=2 pares)\nnaranja=1 par  azul=agua->tierra"))
    W = sum(p.width for p in panels[:4]); H = panels[0].height
    sheet = Image.new("RGB", (panels[0].width * 4, H * 2), (255, 255, 255))
    for i, p in enumerate(panels):
        sheet.paste(p, ((i % 4) * panels[0].width, (i // 4) * H))
    d = ImageDraw.Draw(sheet)
    d.text((panels[0].width * 3 + 5, H + 40), f"{name}\n{lat:.5f}, {lon:.5f}\nrecorte 700 m x 700 m\npixel S2 = 10 m\ncian = poligonos OSM\n(parques/plazas/casos)", fill=(0, 0, 0), font=FONT)
    save_small(sheet, os.path.join(PNG, f"{name}_s2.png"))

    # Wayback
    wpan = []
    for rid, lab in WB:
        try:
            im, ll2px, mpp = wb_mosaic(rid, lat, lon)
        except Exception as e:
            print("wayback err", name, rid, e); continue
        d = ImageDraw.Draw(im)
        for g in s2_mask_polys(r0, c0, h, w, pers):
            d.line([ll2px(la, lo) for lo, la in g.exterior.coords], fill=(255, 0, 0), width=2)
        for g in s2_mask_polys(r0, c0, h, w, one):
            d.line([ll2px(la, lo) for lo, la in g.exterior.coords], fill=(255, 165, 0), width=1)
        for g in s2_mask_polys(r0, c0, h, w, a2t):
            d.line([ll2px(la, lo) for lo, la in g.exterior.coords], fill=(0, 120, 255), width=1)
        im = im.resize((400, 400), Image.LANCZOS)
        md = wbd.get((name, rid), {})
        wpan.append(label(np.array(im), f"{lab} (id {rid})\ncaptura {md.get('SRC_DATE','?')} {md.get('SRC_DESC','')} {md.get('SRC_RES_m','')} m"))
    if wpan:
        sheet = Image.new("RGB", (400 * len(wpan), wpan[0].height), (255, 255, 255))
        for i, p in enumerate(wpan):
            sheet.paste(p, (i * 400, 0))
        save_small(sheet, os.path.join(PNG, f"{name}_hr.png"))

    # mascara para serie NDVI por escena
    sub = pers[r - 5:r + 6, c - 5:c + 6]
    if sub.any():
        lab_, n_ = ndimage.label(pers, structure=np.ones((3, 3)))
        ids_ = np.unique(lab_[r - 5:r + 6, c - 5:c + 6]); ids_ = ids_[ids_ > 0]
        m = np.isin(lab_, ids_); how = "pixeles persistentes"
    else:
        yy, xx = np.ogrid[:HEIGHT, :WIDTH]
        m = (yy - r) ** 2 + (xx - c) ** 2 <= 9; how = "circulo 30 m"
    masks[name] = (how, m)
    print("ok", name, flush=True)

for name, (how, m) in masks.items():
    series[name] = (how, int(m.sum()), [])
for sid, it in sorted(inv.items(), key=lambda kv: kv[1]["fecha_utc"]):
    fn = os.path.join(CACHE, sid + ".npz")
    if not os.path.exists(fn):
        continue
    z = load_scene(sid)
    if z is None:
        continue
    SCLa = z["SCL"]; B4 = z["B04"]; B8 = z["B08"]
    for name, (how, m) in masks.items():
        scl = SCLa[m]; ok = np.isin(scl, SCL_VALID)
        if ok.mean() < 0.8:
            continue
        rr, nn = B4[m][ok].astype("float32"), B8[m][ok].astype("float32")
        series[name][2].append((it["fecha_utc"][:10], float(np.median((nn - rr) / (nn + rr)))))

# grafico de series
fig, axs = plt.subplots(len(series), 1, figsize=(10, 1.9 * len(series)), sharex=True)
for ax, (name, (how, npx, rows)) in zip(axs, series.items()):
    d = [dt.date.fromisoformat(a) for a, b in rows]; v = [b for a, b in rows]
    ax.plot(d, v, ".-", lw=0.7, ms=3, color="#2a6f3f")
    ax.axhline(0.4, color="green", ls=":", lw=0.8); ax.axhline(0.2, color="red", ls=":", lw=0.8)
    ax.set_ylim(-0.2, 0.95); ax.set_ylabel("NDVI", fontsize=7)
    ax.set_title(f"{name} - {how} ({npx} px)", fontsize=8, loc="left")
    for y0_, y1_ in [(dt.date(2022, 12, 1), dt.date(2023, 3, 1)), (dt.date(2025, 12, 1), dt.date(2026, 3, 1))]:
        ax.axvspan(y0_, y1_, color="orange", alpha=0.12)
    ax.tick_params(labelsize=7)
fig.suptitle("NDVI por escena Sentinel-2 L2A (SCL valido >= 80% de los pixeles). Franjas naranjas: veranos secos DJF 2022-23 y DJF 2025-26", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(PNG, "series_ndvi.png"), dpi=90)
with open(os.path.join(OUT, "series_ndvi_puntos.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["punto", "metodo", "n_px", "fecha", "ndvi_mediana"])
    for name, (how, npx, rows) in series.items():
        for a, b in rows:
            w.writerow([name, how, npx, a, round(b, 4)])
print("escenas usadas en recortes:", SCN)
