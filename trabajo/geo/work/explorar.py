import json, csv, sys
from shapely.geometry import shape, MultiLineString, LineString
from shapely.ops import unary_union, linemerge
G = sys.argv[1]
v = json.load(open(G + "/work/shp_vecinos.json"))
si = {f["properties"]["LINK"]: shape(f["geometry"]) for f in v["SAN ISIDRO"]}
asig = {r["radio_id"]: r["zona"] for r in csv.DictReader(open(G + "/src/zonas_asignacion_radios.csv"))}
zonas = {}
for z in sorted(set(asig.values())):
    zonas[z] = unary_union([si[k] for k in asig if asig[k] == z])
for z, g in zonas.items():
    print(z, g.geom_type, "huecos:", len(g.interiors) if g.geom_type == "Polygon" else "?", "vertices:", len(g.exterior.coords), "valida:", g.is_valid)
part = unary_union(list(zonas.values()))
print("partido", part.geom_type, "huecos", len(part.interiors), "vertices", len(part.exterior.coords), part.bounds)
suma = sum(g.area for g in zonas.values())
print("suma areas / area union:", suma / part.area)
vec = {}
for k in v:
    if k == "SAN ISIDRO": continue
    vec[k] = unary_union([shape(f["geometry"]) for f in v[k]])
borde = part.exterior
for k, g in vec.items():
    inter = borde.intersection(g.buffer(0.0003))
    print(k, "largo del borde compartido (grados):", round(inter.length, 5))
todos = unary_union([g.buffer(0.0003) for g in vec.values()])
costa = borde.difference(todos)
print("costa:", costa.geom_type, round(costa.length, 5))
parts = list(costa.geoms) if hasattr(costa, "geoms") else [costa]
parts = [linemerge(p) if p.geom_type == "MultiLineString" else p for p in parts]
import math
kx = math.cos(math.radians(-34.48)) * 111320
for p in sorted(parts, key=lambda p: -p.length):
    print("  tramo", round(p.length * 111320), "m aprox", [tuple(round(c, 5) for c in p.coords[0]), tuple(round(c, 5) for c in p.coords[-1])], len(p.coords))
osm = json.load(open(G + "/src/partido_osm.geojson"))
og = shape(osm["features"][0]["geometry"])
print("osm partido bounds", og.bounds, "area osm / area radios", og.area / part.area)
print("dif sim osm vs radios / area:", og.symmetric_difference(part).area / part.area)
