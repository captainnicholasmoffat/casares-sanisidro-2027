import json, csv, sys, math
from shapely.geometry import shape
from shapely.ops import unary_union, linemerge
G = sys.argv[1]
v = json.load(open(G + "/work/shp_vecinos.json"))
part = unary_union([shape(f["geometry"]) for f in v["SAN ISIDRO"]])
vec = unary_union([shape(f["geometry"]) for k in v if k != "SAN ISIDRO" for f in v[k]])
for b in (0.00002, 0.00005, 0.0001, 0.0002, 0.0003, 0.0005):
    c = part.exterior.difference(vec.buffer(b))
    ps = list(c.geoms) if hasattr(c, "geoms") else [c]
    print(b, len(ps), [round(p.length * 1e5) for p in sorted(ps, key=lambda p: -p.length)][:6])
# distancia de los vertices del borde de San Isidro al vecino mas cercano
d = [vec.distance(__import__("shapely.geometry", fromlist=["Point"]).Point(c)) for c in part.exterior.coords]
import statistics
cerca = [x for x in d if x < 0.001]
print("vertices cerca de vecinos:", len(cerca), "max dist entre esos:", max(cerca))
