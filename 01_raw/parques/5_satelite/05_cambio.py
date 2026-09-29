# -*- coding: utf-8 -*-
"""Deteccion de cambio 'verde -> no verde' (NDVI) y 'agua -> tierra' en parques, plazas, reserva, franja costera y casos.
Parametros en PARAMS (se guardan en parametros_cambio.json).
Salidas: resultados_por_poligono.csv, clusters_cambio.geojson, cambio_mascara.tif (uint8 codificado), placebo_ruido.csv
"""
import json, csv, os, datetime as dt
import numpy as np
from scipy import ndimage
import rasterio
from rasterio.features import rasterize, shapes
from shapely.geometry import shape, mapping
from shapely.ops import transform, unary_union
from common import *

PARAMS = {
    "T_verde": 0.40,          # NDVI >= T_verde en el compuesto "antes" = vegetado
    "T_noverde": 0.20,        # NDVI <= T_noverde en el compuesto "despues" = no vegetado
    "sens": [[0.35, 0.25], [0.45, 0.15]],  # umbrales alternativos para el rango de sensibilidad
    "NDWI_agua": 0.0,         # NDWI (B03-B08)/(B03+B08) > 0 => agua; se excluye como 'no verde' si es agua despues
    "WAT_frac_agua": 0.5,     # fraccion de observaciones SCL=6 (agua) >= 0.5 => agua
    "N_min_obs": 3,           # observaciones validas minimas por pixel en cada compuesto
    "pares": {                # pares de misma estacion (antes -> despues)
        "verano": ["DJF 2023-24", "DJF 2025-26"],
        "invierno": ["JJA 2023", "JJA 2026"],
        "primavera": ["SON 2023", "SON 2025"],
    },
    "par_info_otono": ["MAM 2023", "MAM 2026"],  # informativo (antes = sequia)
    "persistente_min_pares": 2,  # marcado en >= 2 de los 3 pares principales
    "cluster_min_px": 3,         # para listar clusters (>= 300 m2), 8-conectividad
    "agua_antes": ["JJA 2023", "SON 2023", "DJF 2023-24"],   # agua en los tres => agua 2023
    "agua_despues": ["SON 2025", "DJF 2025-26", "JJA 2026"], # tierra en los tres => tierra 2025/26
}
json.dump(PARAMS, open(os.path.join(OUT, "parametros_cambio.json"), "w"), indent=1, ensure_ascii=False)

SEAS = ["SON 2022", "DJF 2022-23", "MAM 2023", "JJA 2023", "SON 2023", "DJF 2023-24", "MAM 2024", "JJA 2024", "SON 2024",
        "DJF 2024-25", "MAM 2025", "JJA 2025", "SON 2025", "DJF 2025-26", "MAM 2026", "JJA 2026", "SON 2026"]
C = {s: np.load(os.path.join(CACHE, "comp_" + s.replace(" ", "_") + ".npz")) for s in SEAS}
NDVI = {s: C[s]["NDVI"] for s in SEAS}
NOBS = {s: C[s]["N"] for s in SEAS}

def is_water(s):
    return (C[s]["NDWI"] > PARAMS["NDWI_agua"]) | (C[s]["WAT"] >= PARAMS["WAT_frac_agua"])

def flag_pair(a, b, tv, tn):
    ok = (NOBS[a] >= PARAMS["N_min_obs"]) & (NOBS[b] >= PARAMS["N_min_obs"])
    return ok & (NDVI[a] >= tv) & (NDVI[b] <= tn) & ~is_water(b) & ~is_water(a)

def persist(tv, tn):
    fl = {k: flag_pair(a, b, tv, tn) for k, (a, b) in PARAMS["pares"].items()}
    cnt = sum(f.astype("uint8") for f in fl.values())
    return fl, cnt

fl, cnt = persist(PARAMS["T_verde"], PARAMS["T_noverde"])
pers = cnt >= PARAMS["persistente_min_pares"]
sens = [persist(tv, tn)[1] >= PARAMS["persistente_min_pares"] for tv, tn in PARAMS["sens"]]
# ganancia (no verde -> verde) en >= 2 pares, para contexto
def gain_pair(a, b, tv, tn):
    ok = (NOBS[a] >= PARAMS["N_min_obs"]) & (NOBS[b] >= PARAMS["N_min_obs"])
    return ok & (NDVI[a] <= tn) & (NDVI[b] >= tv) & ~is_water(a) & ~is_water(b)
gain = sum(gain_pair(a, b, PARAMS["T_verde"], PARAMS["T_noverde"]).astype("uint8") for a, b in PARAMS["pares"].values()) >= 2
fl_oto = flag_pair(*PARAMS["par_info_otono"], PARAMS["T_verde"], PARAMS["T_noverde"])
# cambio reciente (solo 2026): marcado en invierno y tambien bajo en septiembre 2026
reciente = fl["invierno"] & ~pers & (NDVI["SON 2026"] <= PARAMS["T_noverde"]) & (NOBS["SON 2026"] >= 2)
# base vegetada (para %): NDVI >= T_verde en el 'antes' de al menos 2 pares
base_verde = sum(((NDVI[a] >= PARAMS["T_verde"]) & (NOBS[a] >= PARAMS["N_min_obs"])).astype("uint8") for a, b in PARAMS["pares"].values()) >= 2

# agua -> tierra / tierra -> agua (costa)
agua23 = np.all([is_water(s) for s in PARAMS["agua_antes"]], axis=0)
tierra23 = np.all([~is_water(s) for s in PARAMS["agua_antes"]], axis=0)
agua26 = np.all([is_water(s) for s in PARAMS["agua_despues"]], axis=0)
tierra26 = np.all([~is_water(s) for s in PARAMS["agua_despues"]], axis=0)
agua_a_tierra = agua23 & tierra26
tierra_a_agua = tierra23 & agua26

# ---------- placebo (ruido): dos compuestos independientes de la MISMA estacion (escenas alternadas) ----------
rows_inv = list(csv.DictReader(open(os.path.join(OUT, "compuestos_resumen.csv"))))
ids_by = {r["estacion"]: r["ids"].split(";") for r in rows_inv}
def half_ndvi(ids):
    arr = []
    for i in ids:
        z = load_scene(i)
        scl = z["SCL"]; cloud = ndimage.binary_dilation(np.isin(scl, (3, 8, 9, 10)), iterations=2)
        valid = np.isin(scl, SCL_VALID) & ~cloud & (z["B04"] > 0)
        r_, n_ = z["B04"].astype("float32"), z["B08"].astype("float32")
        with np.errstate(invalid="ignore", divide="ignore"):
            arr.append(np.where(valid, (n_ - r_) / (n_ + r_), np.nan))
    a = np.stack(arr)
    return np.nanmedian(a, axis=0), np.sum(~np.isnan(a), axis=0)

placebo = {}
for s in ["DJF 2025-26", "JJA 2026", "SON 2025", "DJF 2023-24"]:
    ids = ids_by[s]
    a, na = half_ndvi(ids[0::2]); b, nb = half_ndvi(ids[1::2])
    ok = (na >= 2) & (nb >= 2)
    placebo[s] = ok & (((a >= PARAMS["T_verde"]) & (b <= PARAMS["T_noverde"])) | ((b >= PARAMS["T_verde"]) & (a <= PARAMS["T_noverde"])))
    placebo[s + "_base"] = ok & ((a >= PARAMS["T_verde"]) | (b >= PARAMS["T_verde"]))

# ---------- poligonos ----------
P = json.load(open(os.path.join(OUT, "poligonos_analisis.geojson")))
part = shape(json.load(open(os.path.join(OUT, "partido_osm.geojson")))["features"][0]["geometry"])
T = base_transform()
def to_u(g):
    return transform(lambda x, y, z=None: to_utm.transform(x, y), g)
part_mask = rasterize([(to_u(part), 1)], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)

# mascaras de grupo
def union_mask(cat):
    gs = [to_u(shape(f["geometry"])) for f in P["features"] if f["properties"]["cat"] == cat]
    return rasterize([(g, 1) for g in gs], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)
M = {c: union_mask(c) for c in ["publico", "club_control", "franja_costera", "caso"]}
M["resto_partido"] = part_mask & ~M["publico"] & ~M["club_control"] & ~M["franja_costera"]

lab, nlab = ndimage.label(pers, structure=np.ones((3, 3)))
sizes = ndimage.sum(pers, lab, index=np.arange(1, nlab + 1))
pers_c3 = np.isin(lab, np.where(sizes >= PARAMS["cluster_min_px"])[0] + 1)

def stats(mask):
    px = int(mask.sum())
    bv = int((base_verde & mask).sum())
    d = {"px_10m": px, "area_px_m2": px * 100, "verde_base_m2": bv * 100,
         "cambio_persistente_m2": int((pers & mask).sum()) * 100,
         "cambio_persistente_cluster3_m2": int((pers_c3 & mask).sum()) * 100,
         "sens_laxo_0.35_0.25_m2": int((sens[0] & mask).sum()) * 100,
         "sens_estricto_0.45_0.15_m2": int((sens[1] & mask).sum()) * 100,
         "solo_verano_m2": int((fl["verano"] & (cnt == 1) & mask).sum()) * 100,
         "solo_invierno_m2": int((fl["invierno"] & (cnt == 1) & mask).sum()) * 100,
         "solo_primavera_m2": int((fl["primavera"] & (cnt == 1) & mask).sum()) * 100,
         "reciente_2026_m2": int((reciente & mask).sum()) * 100,
         "par_otono_info_m2": int((fl_oto & mask).sum()) * 100,
         "ganancia_noverde_a_verde_m2": int((gain & mask).sum()) * 100,
         "tierra_base_px_m2": int((tierra23 & mask).sum()) * 100,
         "agua_a_tierra_m2": int((agua_a_tierra & mask).sum()) * 100,
         "tierra_a_agua_m2": int((tierra_a_agua & mask).sum()) * 100}
    d["pct_persistente_del_poligono"] = round(100 * d["cambio_persistente_m2"] / max(d["area_px_m2"], 1), 2)
    d["pct_persistente_del_verde_base"] = round(100 * d["cambio_persistente_m2"] / max(d["verde_base_m2"], 1), 2)
    # ruido esperado por placebo (tasa por pixel vegetado) aplicado al verde base
    d["ruido_placebo_1par_m2"] = round(bv * 100 * placebo_rate_1, 0)
    return d

# tasa de placebo (un par) en el conjunto de pixeles vegetados del partido
pr = [placebo[s][part_mask].sum() / max(placebo[s + "_base"][part_mask].sum(), 1) for s in ["DJF 2025-26", "JJA 2026", "SON 2025", "DJF 2023-24"]]
placebo_rate_1 = float(np.mean(pr))
with open(os.path.join(OUT, "placebo_ruido.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["estacion", "px_marcados_placebo", "px_vegetados_placebo", "tasa", "nota"])
    for s, r in zip(["DJF 2025-26", "JJA 2026", "SON 2025", "DJF 2023-24"], pr):
        w.writerow([s, int(placebo[s][part_mask].sum()), int(placebo[s + "_base"][part_mask].sum()), round(r, 5),
                    "dos compuestos de la misma estacion con escenas alternadas; todo lo marcado es ruido (no hay tiempo para cambio real)"])
print("tasa placebo 1 par:", pr, placebo_rate_1)

rows = []
for f in P["features"]:
    p = f["properties"]
    g = to_u(shape(f["geometry"]))
    m = rasterize([(g, 1)], out_shape=(HEIGHT, WIDTH), transform=T, fill=0, dtype="uint8").astype(bool)
    r = {"pid": p["pid"], "cat": p["cat"], "osm": p["osm"], "nombre": p["name"], "tag": p["tag"], "area_vector_m2": p["area_m2"]}
    r.update(stats(m))
    rows.append(r)
for gname, m in M.items():
    r = {"pid": "", "cat": "GRUPO", "osm": "", "nombre": "TOTAL " + gname, "tag": "", "area_vector_m2": ""}
    r.update(stats(m)); rows.append(r)
r = {"pid": "", "cat": "GRUPO", "osm": "", "nombre": "TOTAL partido", "tag": "", "area_vector_m2": ""}
r.update(stats(part_mask)); rows.append(r)
with open(os.path.join(OUT, "resultados_por_poligono.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---------- clusters (persistentes, >= 1 px) con serie estacional ----------
feats = []
for k in range(1, nlab + 1):
    mk = lab == k
    n = int(mk.sum())
    series = {s: round(float(np.nanmedian(NDVI[s][mk])), 3) for s in SEAS}
    geo = unary_union([shape(gg) for gg, v in shapes(mk.astype("uint8"), mask=mk, transform=T) if v == 1])
    gll = transform(lambda x, y, z=None: to_ll.transform(x, y), geo)
    # estacion de quiebre: primera estacion desde la cual la mediana NDVI queda <= 0.25 hasta el final (sin contar SON 2022/DJF22-23)
    br = None
    for i in range(2, len(SEAS)):
        if all(series[s] <= 0.25 for s in SEAS[i:] if not np.isnan(series[s])):
            br = SEAS[i]; break
    grp = [c for c in ["caso", "franja_costera", "publico", "club_control"] if M[c][mk].any()]
    if not grp:
        grp = ["resto_partido"] if part_mask[mk].any() else []
    if not grp:
        continue  # cluster fuera del partido y de la franja costera: no se reporta
    feats.append({"type": "Feature", "properties": {"cid": k, "px": n, "area_m2": n * 100, "grupos": ",".join(grp),
                  "lat": round(gll.centroid.y, 6), "lon": round(gll.centroid.x, 6), "estacion_quiebre": br,
                  "n_pares": int(cnt[mk].max()), "ndbi_antes": round(float(np.nanmedian(C["DJF 2023-24"]["NDBI"][mk])), 3),
                  "ndbi_despues": round(float(np.nanmedian(C["DJF 2025-26"]["NDBI"][mk])), 3),
                  "bsi_despues": round(float(np.nanmedian(C["DJF 2025-26"]["BSI"][mk])), 3),
                  **{"ndvi_" + s.replace(" ", "_"): v for s, v in series.items()}}, "geometry": mapping(gll)})
feats.sort(key=lambda f: -f["properties"]["px"])
json.dump({"type": "FeatureCollection", "features": feats}, open(os.path.join(OUT, "clusters_cambio.geojson"), "w"))

# agua->tierra clusters en franja costera
lab2, n2 = ndimage.label(agua_a_tierra & M["franja_costera"], structure=np.ones((3, 3)))
f2 = []
for k in range(1, n2 + 1):
    mk = lab2 == k
    geo = unary_union([shape(gg) for gg, v in shapes(mk.astype("uint8"), mask=mk, transform=T) if v == 1])
    gll = transform(lambda x, y, z=None: to_ll.transform(x, y), geo)
    f2.append({"type": "Feature", "properties": {"cid": k, "px": int(mk.sum()), "area_m2": int(mk.sum()) * 100, "tipo": "agua_2023->tierra_2025/26",
               "lat": round(gll.centroid.y, 6), "lon": round(gll.centroid.x, 6),
               "ndvi_despues_DJF25_26": round(float(np.nanmedian(NDVI["DJF 2025-26"][mk])), 3)}, "geometry": mapping(gll)})
f2.sort(key=lambda f: -f["properties"]["px"])
json.dump({"type": "FeatureCollection", "features": f2}, open(os.path.join(OUT, "clusters_agua_a_tierra.geojson"), "w"))

# raster de mascara (entregable chico): bit0 persistente, bit1 verano, bit2 invierno, bit3 primavera, bit4 reciente2026, bit5 agua->tierra, bit6 tierra->agua, bit7 base_verde
code = (pers.astype("uint8") | (fl["verano"].astype("uint8") << 1) | (fl["invierno"].astype("uint8") << 2) | (fl["primavera"].astype("uint8") << 3)
        | (reciente.astype("uint8") << 4) | (agua_a_tierra.astype("uint8") << 5) | (tierra_a_agua.astype("uint8") << 6) | (base_verde.astype("uint8") << 7))
with rasterio.open(os.path.join(OUT, "cambio_mascara_bits.tif"), "w", driver="GTiff", height=HEIGHT, width=WIDTH, count=1, dtype="uint8",
                   crs=f"EPSG:{EPSG}", transform=T, compress="deflate") as dst:
    dst.write(code, 1)
    dst.update_tags(bits="bit0 persistente(>=2 pares); bit1 par verano DJF23-24->DJF25-26; bit2 par invierno JJA23->JJA26; bit3 par primavera SON23->SON25; bit4 reciente 2026 (solo invierno + sep26); bit5 agua->tierra; bit6 tierra->agua; bit7 vegetado base")
print("clusters persistentes:", nlab, "agua->tierra clusters franja:", n2)
for r in rows[-6:]:
    print(r["nombre"], {k: r[k] for k in ["area_px_m2", "verde_base_m2", "cambio_persistente_m2", "cambio_persistente_cluster3_m2", "sens_laxo_0.35_0.25_m2", "sens_estricto_0.45_0.15_m2", "solo_verano_m2", "solo_invierno_m2", "solo_primavera_m2", "reciente_2026_m2", "agua_a_tierra_m2", "tierra_a_agua_m2", "ruido_placebo_1par_m2"]})
