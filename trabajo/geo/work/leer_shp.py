import shapefile, json, sys
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
G = sys.argv[1]
r = shapefile.Reader(G + "/shp/shp22/radios-censales", encoding="utf-8")
names = [f[0] for f in r.fields[1:]]
from collections import defaultdict
deptos = defaultdict(list)
for sr in r.iterShapeRecords():
    rec = dict(zip(names, sr.record))
    nd = str(rec["NOMDEPTO"]).strip().upper()
    if nd in ("SAN ISIDRO", "VICENTE LÓPEZ", "VICENTE LOPEZ", "GENERAL SAN MARTÍN", "GENERAL SAN MARTIN", "TIGRE", "SAN FERNANDO", "MALVINAS ARGENTINAS", "TRES DE FEBRERO", "SAN MIGUEL", "JOSÉ C. PAZ"):
        deptos[nd].append((rec, sr.shape.__geo_interface__))
for k, v in deptos.items():
    print(k, len(v), v[0][0]["PROV"], v[0][0]["DEPTO"])
out = {k: [{"type": "Feature", "properties": rec, "geometry": g} for rec, g in v] for k, v in deptos.items()}
json.dump(out, open(G + "/work/shp_vecinos.json", "w"), ensure_ascii=False)
