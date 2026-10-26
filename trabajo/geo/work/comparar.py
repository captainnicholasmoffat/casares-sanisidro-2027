import json, csv, sys
from shapely.geometry import shape
from shapely.ops import unary_union
G = sys.argv[1]
v = json.load(open(G + "/work/shp_vecinos.json"))
si = {f["properties"]["LINK"]: shape(f["geometry"]) for f in v["SAN ISIDRO"]}
geo = json.load(open(G + "/src/radios_censales_sanisidro.geojson"))
gj = {f["properties"]["radio_id"]: shape(f["geometry"]) for f in geo["features"]}
print("shp:", len(si), "geojson:", len(gj), "mismos ids:", set(si) == set(gj))
maxd = 0
for k in si:
    d = si[k].symmetric_difference(gj[k]).area / si[k].area
    maxd = max(maxd, d)
print("max diferencia relativa de area shp vs geojson:", maxd)
print("validos shp:", sum(g.is_valid for g in si.values()), "tipos:", set(g.geom_type for g in si.values()))
asig = {r["radio_id"]: r for r in csv.DictReader(open(G + "/src/zonas_asignacion_radios.csv"))}
print("asignacion:", len(asig), set(asig) == set(si))
from collections import Counter
print(Counter(r["zona"] for r in asig.values()))
print(Counter(r["asignado_por"] for r in asig.values()))
print(Counter(r["relacion_osm"] + " " + r["zona"] for r in asig.values()))
zp = json.load(open(G + "/src/zonas_propuestas_sanisidro.geojson"))
for f in zp["features"]:
    z = f["properties"]["zona"]
    u = unary_union([gj[k] for k in asig if asig[k]["zona"] == z])
    g = shape(f["geometry"])
    print(z, f["geometry"]["type"], "dif vs zonas_propuestas:", round(u.symmetric_difference(g).area / g.area, 8), "pob", f["properties"]["poblacion"], "radios", f["properties"]["radios"])
