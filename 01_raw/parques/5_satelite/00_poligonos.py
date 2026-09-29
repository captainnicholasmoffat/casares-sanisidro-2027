# -*- coding: utf-8 -*-
"""Construye los poligonos de analisis a partir de OpenStreetMap (Overpass, espejo maps.mail.ru; descarga 2026-09-29).
Salidas: poligonos_analisis.geojson (EPSG:4326), partido_osm.geojson
Categorias:
  publico      : leisure=park|garden|common|nature_reserve, boundary=protected_area, place=square (dentro del partido)
  club_control : leisure=golf_course|recreation_ground|sports_centre|horse_riding, landuse=recreation_ground (clubes/golf; control)
  franja_costera: banda entre la via del Tren de la Costa y 1,5 km rio adentro, desde calle Parana (limite V. Lopez)
                  hasta el limite con San Fernando (Beccar), dividida en tramos de ~500 m.
  caso         : zonas de obra conocidas (inventario paralelo / noticias municipales), buffer de 100 m si no hay poligono OSM.
"""
import json, math
import numpy as np
from shapely.geometry import Polygon, LineString, Point, mapping, shape, MultiPolygon
from shapely.ops import unary_union, polygonize, linemerge, transform
from common import OUT, to_utm, to_ll
import os

def ll2utm(g):
    return transform(lambda x, y, z=None: to_utm.transform(x, y), g)
def utm2ll(g):
    return transform(lambda x, y, z=None: to_ll.transform(x, y), g)

# --- Partido ---
aux = json.load(open(os.path.join(OUT, "osm_aux_overpass_raw.json")))
rel = [e for e in aux["elements"] if e["type"] == "relation" and e["id"] == 1769044][0]
lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]]) for m in rel["members"] if m["type"] == "way" and m.get("geometry")]
polys = list(polygonize(unary_union(lines)))
partido = unary_union(polys)
print("partido: n poligonos", len(polys), "area km2", round(ll2utm(partido).area / 1e6, 2))
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Partido de San Isidro", "osm": "relation/1769044"}, "geometry": mapping(partido)}]},
          open(os.path.join(OUT, "partido_osm.geojson"), "w"))
partido_u = ll2utm(partido)

# --- Verdes OSM ---
v = json.load(open(os.path.join(OUT, "osm_verdes_overpass_raw.json")))
feats = []
costeros = []
def cat_of(t):
    le = t.get("leisure"); lu = t.get("landuse"); b = t.get("boundary"); pl = t.get("place")
    if le in ("park", "garden", "common", "nature_reserve") or b == "protected_area" or pl == "square":
        return "publico"
    if le in ("golf_course", "recreation_ground", "sports_centre", "horse_riding", "pitch") or lu in ("recreation_ground", "village_green"):
        return "club_control"
    return None

for e in v["elements"]:
    t = e.get("tags", {})
    cat = cat_of(t)
    if cat is None:
        continue
    geom = None
    if e["type"] == "way":
        g = e.get("geometry", [])
        if len(g) >= 4 and (g[0]["lat"], g[0]["lon"]) == (g[-1]["lat"], g[-1]["lon"]):
            geom = Polygon([(p["lon"], p["lat"]) for p in g])
    else:
        outer = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]]) for m in e.get("members", []) if m["type"] == "way" and m.get("role") in ("outer", "") and m.get("geometry")]
        inner = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]]) for m in e.get("members", []) if m["type"] == "way" and m.get("role") == "inner" and m.get("geometry")]
        po = unary_union(list(polygonize(unary_union(outer)))) if outer else None
        if po is not None and not po.is_empty:
            if inner:
                pi = unary_union(list(polygonize(unary_union(inner))))
                po = po.difference(pi)
            geom = po
    if geom is None or geom.is_empty:
        continue
    if not geom.is_valid:
        geom = geom.buffer(0)
    gu = ll2utm(geom)
    inside = gu.intersection(partido_u.buffer(50)).area / max(gu.area, 1)
    if inside < 0.5:
        # candidato costero (p.ej. Parque Natural Ribera Norte: 54% sobre agua/juncal fuera del poligono OSM del partido);
        # se decide despues de construir la franja costera
        costeros.append({"osm": f"{e['type']}/{e['id']}", "name": t.get("name", ""), "tag": t.get("leisure") or t.get("boundary") or t.get("landuse") or t.get("place"),
                         "cat": cat, "geom_u": gu})
        continue
    feats.append({"osm": f"{e['type']}/{e['id']}", "name": t.get("name", ""), "tag": t.get("leisure") or t.get("boundary") or t.get("landuse") or t.get("place"),
                  "cat": cat, "geom_u": gu})
print("verdes dentro del partido:", len(feats))

# --- Franja costera ---
tc = json.load(open(os.path.join(OUT, "osm_tren_costa_coastline_raw.json")))
pts = []
for e in tc["elements"]:
    t = e.get("tags", {})
    if t.get("railway") == "light_rail" and "Costa" in (t.get("name") or ""):
        for p in e["geometry"]:
            pts.append(to_utm.transform(p["lon"], p["lat"]))
pts = np.array(pts)
A = np.array(to_utm.transform(-58.4814173, -34.4905322))  # extremo costero calle Parana (limite con Vicente Lopez)
B = np.array(to_utm.transform(-58.5285, -34.4460))       # Beccar, cerca del limite con San Fernando (se recorta con el poligono del partido)
axis = (B - A) / np.linalg.norm(B - A)
normal = np.array([axis[1], -axis[0]])  # hacia el rio (NE)
if normal[0] < 0:
    normal = -normal
s = (pts - A) @ axis
sel = (s >= -30) & (s <= np.linalg.norm(B - A) + 400)
pts = pts[sel]; s = s[sel]
order = np.argsort(s); pts = pts[order]; s = s[order]
# linea suavizada: promedio de la via por tramos de 50 m (hay doble via)
bins = np.arange(s.min(), s.max() + 50, 50)
line = []
for i in range(len(bins) - 1):
    m = (s >= bins[i]) & (s < bins[i + 1])
    if m.sum():
        line.append(pts[m].mean(axis=0))
line = np.array(line)
off = line + normal * 1500
strip = Polygon(list(map(tuple, line)) + list(map(tuple, off[::-1])))
if not strip.is_valid:
    strip = strip.buffer(0)
# recorte: extremo sur = perpendicular en Parana; extremo norte = limite partido (poligono del partido extendido al rio)
# el poligono OSM del partido llega a la orilla; se extiende hacia el rio con un 'barrido' en la direccion normal
part_ext = unary_union([partido_u] + [transform(lambda x, y, z=None, k=k: (x + normal[0] * k, y + normal[1] * k), partido_u) for k in range(0, 1600, 100)])
strip = strip.intersection(part_ext)
# corte sur perpendicular en A
big = 20000
half_sur = Polygon([tuple(A - normal * big), tuple(A + normal * big), tuple(A + normal * big - axis * big), tuple(A - normal * big - axis * big)])
strip = strip.difference(half_sur)
print("franja costera area ha", round(strip.area / 1e4, 1))

# tramos de 500 m a lo largo de la costa
tramos = []
L = np.linalg.norm(B - A) + 400
for i, s0 in enumerate(np.arange(0, L, 500)):
    s1 = s0 + 500
    q = Polygon([tuple(A + axis * s0 - normal * 3000), tuple(A + axis * s1 - normal * 3000), tuple(A + axis * s1 + normal * 3000), tuple(A + axis * s0 + normal * 3000)])
    g = strip.intersection(q)
    if g.area > 1000:
        c = utm2ll(g.centroid)
        tramos.append({"osm": "", "name": f"Franja costera tramo {i+1:02d} ({int(s0)}-{int(s1)} m desde calle Parana)", "tag": "franja_costera", "cat": "franja_costera", "geom_u": g})

# --- Casos (obras conocidas) ---
casos_pts = [
    ("Caso: 33 Orientales (costa de Beccar) - paseo inaugurado 05/2025", -58.5170, -34.4505),
    ("Caso: Roque Saenz Pena y el rio (bajo de San Isidro) - demoliciones 06/2025", -58.4976, -34.4640),
    ("Caso: Alvear y el rio / Sebastian Elcano (Martinez) - 1400 m2 09/2025 y predio 01/2025", -58.4830, -34.4805),
]
casos = []
for n, lon, lat in casos_pts:
    casos.append({"osm": "", "name": n, "tag": "caso_buffer100m", "cat": "caso", "geom_u": Point(to_utm.transform(lon, lat)).buffer(100, 32)})

# Caso Aguila - Alvear - Puerto Libre (obra iniciada 07/2026): franja entre perpendiculares por Paseo del Aguila y Puerto Libre,
# hasta 400 m rio adentro desde la via
def perp_cut(lon1, lat1, lon2, lat2, width):
    p1 = np.array(to_utm.transform(lon1, lat1)); p2 = np.array(to_utm.transform(lon2, lat2))
    s1, s2 = sorted([(p1 - A) @ axis, (p2 - A) @ axis])
    q = Polygon([tuple(A + axis * s1 - normal * 3000), tuple(A + axis * s2 - normal * 3000), tuple(A + axis * s2 + normal * 3000), tuple(A + axis * s1 + normal * 3000)])
    band = Polygon(list(map(tuple, line)) + list(map(tuple, (line + normal * width)[::-1]))).buffer(0)
    return strip.intersection(q).intersection(band)
casos.append({"osm": "", "name": "Caso: Parque del Aguila - Alvear y el rio - Puerto Libre (obra desde 07/2026; 907 m de costa)", "tag": "caso_franja400m",
              "cat": "caso", "geom_u": perp_cut(-58.4885, -34.4745, -58.4800, -34.4845, 400)})
casos.append({"osm": "", "name": "Caso: Bajo de Roque Saenz Pena (Catalejo/Barisidro) - franja 300 m a cada lado, 400 m rio adentro", "tag": "caso_franja400m",
              "cat": "caso", "geom_u": perp_cut(-58.4995, -34.4615, -58.4955, -34.4665, 400)})
casos.append({"osm": "", "name": "Caso: 33 Orientales / Puerto de San Isidro - franja 300 m a cada lado, 400 m rio adentro", "tag": "caso_franja400m",
              "cat": "caso", "geom_u": perp_cut(-58.5195, -34.4485, -58.5145, -34.4530, 400)})

# agregados al final (para no alterar los pid previos): poligonos con >= 50% dentro de (partido U franja costera)
extra = [f for f in costeros if f["geom_u"].intersection(unary_union([partido_u.buffer(50), strip])).area / f["geom_u"].area >= 0.5]
print("poligonos costeros agregados:", [(f["name"], f["osm"]) for f in extra])
allf = feats + tramos + casos + extra
out = {"type": "FeatureCollection", "features": []}
for i, f in enumerate(allf):
    g = utm2ll(f["geom_u"])
    out["features"].append({"type": "Feature", "properties": {"pid": i, "osm": f["osm"], "name": f["name"], "tag": f["tag"], "cat": f["cat"],
                            "area_m2": round(f["geom_u"].area, 0)}, "geometry": mapping(g)})
json.dump(out, open(os.path.join(OUT, "poligonos_analisis.geojson"), "w"))
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "franja costera (Tren de la Costa -> 1,5 km rio adentro)"}, "geometry": mapping(utm2ll(strip))}]},
          open(os.path.join(OUT, "franja_costera.geojson"), "w"))
import collections
print(collections.Counter(f["cat"] for f in allf))
print("area publico ha (disuelta):", round(unary_union([f["geom_u"] for f in feats if f["cat"] == "publico"]).area / 1e4, 1))
