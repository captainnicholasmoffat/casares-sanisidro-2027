# -*- coding: utf-8 -*-
"""Arma web/data/zonas.geojson con las seis localidades, el contorno del partido
y la linea de la costa, a partir de los radios censales 2022 (shapefile del repo)
y de la asignacion radio -> localidad que uso el programa final
(data/zonas_asignacion_radios.csv en c462fcf).

Uso: python3 -I armar_zonas.py <carpeta geo> <salida.geojson> <tolerancia_m>
"""
import csv, json, math, sys
from shapely.geometry import shape, mapping, Point, LineString, Polygon
from shapely.geometry.polygon import orient
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from shapely.ops import unary_union, linemerge, polygonize, substring, transform

G, SALIDA, TOL = sys.argv[1], sys.argv[2], float(sys.argv[3])
DEC = 6

NOMBRES = {"Boulogne Sur Mer": ("boulogne", "Boulogne Sur Mer"),
           "Beccar": ("beccar", "Béccar"),
           "Villa Adelina": ("villa_adelina", "Villa Adelina"),
           "San Isidro": ("san_isidro", "San Isidro"),
           "Martinez": ("martinez", "Martínez"),
           "Acassuso": ("acassuso", "Acassuso")}
ORDEN = ["Boulogne Sur Mer", "Beccar", "Villa Adelina", "San Isidro", "Martinez", "Acassuso"]

# --- radios del shapefile (San Isidro y vecinos) -----------------------------
v = json.load(open(G + "/work/shp_vecinos.json"))
radios = {f["properties"]["LINK"]: shape(f["geometry"]) for f in v["SAN ISIDRO"]}
vecinos = unary_union([shape(f["geometry"]) for k in v if k != "SAN ISIDRO" for f in v[k]])
asig = {r["radio_id"]: r["zona"] for r in csv.DictReader(open(G + "/src/zonas_asignacion_radios.csv"))}
assert set(asig) == set(radios) and len(radios) == 360

zonas = {z: unary_union([radios[k] for k in asig if asig[k] == z]) for z in ORDEN}
for z, g in zonas.items():
    assert g.geom_type == "Polygon" and not g.interiors and g.is_valid, z
partido = unary_union(list(zonas.values()))
assert partido.geom_type == "Polygon" and not partido.interiors

# --- la costa: el borde del partido que no toca ningun partido vecino ---------
costa0 = partido.exterior.difference(vecinos.buffer(0.00005))   # ~5 m
assert costa0.geom_type == "LineString", costa0.geom_type
# los extremos se llevan al vertice del borde mas cercano (el nudo con el vecino)
verts = [Point(c) for c in partido.exterior.coords]
def al_vertice(p):
    q = min(verts, key=lambda w: w.distance(p))
    return q if q.distance(p) < 0.0001 else p
a, b = al_vertice(Point(costa0.coords[0])), al_vertice(Point(costa0.coords[-1]))

# --- simplificacion que respeta los bordes compartidos ------------------------
LAT0 = -34.49
KX, KY = math.cos(math.radians(LAT0)) * 111320.0, 110574.0
a_m = lambda x, y, z=None: (x * KX, y * KY)
a_g = lambda x, y, z=None: (x / KX, y / KY)

bordes = unary_union([g.exterior for g in zonas.values()])          # nodado
arcos = list(linemerge(bordes).geoms)
# cortar los arcos en los dos extremos de la costa, para que sean nudos fijos
def cortar(arcos, p):
    out = []
    for arc in arcos:
        d = arc.project(p)
        if arc.distance(p) < 1e-9 and 1e-12 < d < arc.length - 1e-12:
            out += [substring(arc, 0, d), substring(arc, d, arc.length)]
        else:
            out.append(arc)
    return out
arcos = cortar(cortar(arcos, a), b)
simpl = [transform(a_g, transform(a_m, arc).simplify(TOL, preserve_topology=False)) for arc in arcos]
def redondear(g):
    return transform(lambda x, y, z=None: (round(x, DEC), round(y, DEC)), g)
simpl = [redondear(s) for s in simpl]

caras = list(polygonize(simpl))
nuevas = {}
for z, g in zonas.items():
    cand = [c for c in caras if c.representative_point().within(g)]
    assert len(cand) == 1, (z, len(cand))
    nuevas[z] = orient(cand[0], 1.0)
assert len(caras) == 6, len(caras)
partido_s = orient(unary_union(list(nuevas.values())), 1.0)
assert partido_s.geom_type == "Polygon" and not partido_s.interiors

ra, rb = redondear(a), redondear(b)
def es_costa(o):
    mid = o.interpolate(0.5, normalized=True)
    return mid.distance(partido.exterior) < 1e-8 and mid.distance(vecinos) > 0.00005
costa_arcos = [s for s, o in zip(simpl, arcos) if es_costa(o)]
costa = linemerge(costa_arcos)
costa_orig = linemerge([o for o in arcos if es_costa(o)])
assert costa_orig.geom_type == "LineString"
assert costa.geom_type == "LineString", costa.geom_type
# que corra de norte a sur
if costa.coords[0][1] < costa.coords[-1][1]:
    costa = LineString(list(costa.coords)[::-1])

# --- controles de forma -------------------------------------------------------
def m(g): return transform(a_m, g)
informe = {"tolerancia_m": TOL, "decimales": DEC, "zonas": {}}
for z in ORDEN:
    o, s = zonas[z], nuevas[z]
    informe["zonas"][z] = {
        "vertices_original": len(o.exterior.coords), "vertices_final": len(s.exterior.coords),
        "area_km2_original": round(m(o).area / 1e6, 4), "area_km2_final": round(m(s).area / 1e6, 4),
        "dif_area_pct": round(100 * (m(s).area - m(o).area) / m(o).area, 3),
        "hausdorff_m": round(m(o).hausdorff_distance(m(s)), 2),
        "valida": s.is_valid}
sup = sum(m(nuevas[z]).area for z in ORDEN)
informe["solape_o_hueco_m2"] = round(sup - m(partido_s).area, 3)
informe["partido"] = {"vertices_original": len(partido.exterior.coords),
                      "vertices_final": len(partido_s.exterior.coords),
                      "hausdorff_m": round(m(partido).hausdorff_distance(m(partido_s)), 2),
                      "area_km2_final": round(m(partido_s).area / 1e6, 3)}
informe["costa"] = {"largo_km": round(m(costa).length / 1000, 2),
                    "vertices": len(costa.coords),
                    "largo_km_original": round(m(costa_orig).length / 1000, 2),
                    "hausdorff_m_contra_original": round(m(costa_orig).hausdorff_distance(m(costa)), 2),
                    "extremo_norte": [round(c, 5) for c in costa.coords[0]],
                    "extremo_sur": [round(c, 5) for c in costa.coords[-1]]}
# cada radio sigue cayendo en su zona (su punto representativo, con la geometria simplificada)
fuera = [k for k in radios if not nuevas[asig[k]].contains(radios[k].representative_point())]
informe["radios_cuyo_punto_quedo_fuera_de_su_zona"] = fuera

# --- salida -------------------------------------------------------------------
def coords(g):
    return json.loads(json.dumps(mapping(g)))

feats = []
for z in ORDEN:
    zid, nom = NOMBRES[z]
    feats.append({"type": "Feature", "id": zid,
                  "properties": {"tipo": "localidad", "id": zid, "nombre": nom},
                  "geometry": coords(nuevas[z])})
feats.append({"type": "Feature", "id": "partido",
              "properties": {"tipo": "partido", "id": "partido", "nombre": "Partido de San Isidro"},
              "geometry": coords(partido_s)})
feats.append({"type": "Feature", "id": "costa",
              "properties": {"tipo": "costa", "id": "costa", "nombre": "Costa del Río de la Plata"},
              "geometry": coords(costa)})
fc = {"type": "FeatureCollection",
      "metadata": {
          "descripcion": "Las seis localidades de San Isidro armadas con los 360 radios censales del Censo 2022, con el mismo criterio que el programa «San Isidro 2027» (cada radio va a la localidad de OpenStreetMap que contiene su punto representativo), más el contorno del partido y la costa del río.",
          "crs": "WGS84, longitud/latitud (EPSG:4326)",
          "fuente_geometria": "INDEC, Censo 2022, radios censales (catalogo.datos.gba.gob.ar), en 01_raw/censo2022/radios-censales-2022-shp.zip",
          "fuente_asignacion": "data/zonas_asignacion_radios.csv del repositorio del programa, commit c462fcf (límites de localidad de OpenStreetMap, no oficiales)",
          "costa": "Borde de los radios censales de San Isidro que no toca a ningún partido vecino; no es una línea de costa relevada.",
          "simplificacion": f"Bordes compartidos simplificados una sola vez (tolerancia {TOL:g} m), sin huecos ni solapes entre localidades; coordenadas con {DEC} decimales.",
          "aviso": "Los límites son una construcción propia sobre geografía oficial: el Municipio no publica límites de localidad."},
      "features": feats}
txt = json.dumps(fc, ensure_ascii=False, separators=(",", ":"))
open(SALIDA, "w", encoding="utf-8").write(txt)
informe["bytes"] = len(txt.encode("utf-8"))
print(json.dumps(informe, ensure_ascii=False, indent=1))
