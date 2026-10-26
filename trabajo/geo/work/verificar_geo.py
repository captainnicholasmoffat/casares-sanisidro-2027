import json, sys
from shapely.geometry import shape
from shapely.geometry.polygon import LinearRing
d = json.load(open(sys.argv[1]))
print("features:", [(f["properties"]["tipo"], f["properties"]["nombre"], f["geometry"]["type"]) for f in d["features"]])
for f in d["features"]:
    g = shape(f["geometry"])
    if g.geom_type == "Polygon":
        print(f["properties"]["nombre"], "valida", g.is_valid, "antihorario", LinearRing(g.exterior.coords).is_ccw, "huecos", len(g.interiors))
    else:
        print(f["properties"]["nombre"], g.geom_type, len(g.coords))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 7))
cols = ["#7C2E23", "#B4675A", "#E4C6BC", "#C9CFBE", "#5F7057", "#B4863A"]
i = 0
for f in d["features"]:
    g = shape(f["geometry"]); t = f["properties"]["tipo"]
    if t == "localidad":
        x, y = g.exterior.xy; ax.fill(x, y, color=cols[i], ec="white", lw=.8); i += 1
        c = g.representative_point(); ax.text(c.x, c.y, f["properties"]["nombre"], ha="center", fontsize=8)
    elif t == "partido":
        x, y = g.exterior.xy; ax.plot(x, y, color="black", lw=1.2)
    else:
        x, y = g.xy; ax.plot(x, y, color="#1E6FB0", lw=3, alpha=.7)
ax.set_aspect(1 / 0.824); ax.set_title("zonas.geojson")
fig.savefig(sys.argv[2], dpi=110, bbox_inches="tight")
