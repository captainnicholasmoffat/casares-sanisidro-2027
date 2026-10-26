"""Dibuja el mapa de las seis zonas como bloques en relieve (SVG estático, para la propuesta C).
Altura de cada bloque = dinero de obra que decide la zona en el cuarto año (4.4 · Gráfico 23).
Uso: python3 -I mapa3d.py <zonas.geojson> <zonas_datos.json> <salida.svg>
"""
import json, math, sys

geo = json.load(open(sys.argv[1]))
datos = json.load(open(sys.argv[2]))["zonas"]
OUT = sys.argv[3]

lat0 = -34.49
KX = 111320 * math.cos(math.radians(lat0))
KY = 110540

def to_m(lon, lat):
    return ((lon + 58.54) * KX, (lat - lat0) * KY)

# Vista: girada para que el río quede arriba a la derecha, en perspectiva isométrica suave
SQ = 0.5
S = 0.075          # px por metro
H_MAX = 64         # px de alto para el monto mayor
_c = [to_m(*q) for q in [f for f in geo["features"] if f["properties"]["id"] == "costa"][0]["geometry"]["coordinates"]]
_a = math.atan2(_c[-1][1] - _c[0][1], _c[-1][0] - _c[0][0])
ROT = -_a
# el río (al noreste de la costa) tiene que quedar adelante, abajo en la pantalla
_mx = sum(x for x, _ in _c) / len(_c); _my = sum(y for _, y in _c) / len(_c)
_rx, _ry = _mx + 3000, _my + 3000
_yr = lambda x, y: x * math.sin(ROT) + y * math.cos(ROT)
if _yr(_rx, _ry) > _yr(_mx, _my):
    ROT += math.pi

def proj(x, y, h=0.0):
    xr = x * math.cos(ROT) - y * math.sin(ROT)
    yr = x * math.sin(ROT) + y * math.cos(ROT)
    return (xr * S, -yr * S * SQ - h)

feats = {f["properties"]["id"]: f for f in geo["features"]}
ring = lambda f: f["geometry"]["coordinates"][0]

zonas = ["boulogne", "beccar", "villa_adelina", "san_isidro", "martinez", "acassuso"]
monto = {z: datos[z]["cifras"]["obra_vecinal_anio4_monto"]["valor"] for z in zonas}
mmax = max(monto.values())

# Colores por necesidad (índice del 4.4): más necesidad, más oscuro
TOP = {"boulogne": "#7C2E23", "beccar": "#9A4334", "villa_adelina": "#C98A5C",
       "san_isidro": "#C49A62", "martinez": "#B9A47A", "acassuso": "#A9AE8E"}

def shade(hexc, f):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))

pts_all = []
shapes = {}
for z in zonas:
    m = [to_m(*p) for p in ring(feats[z])]
    h = H_MAX * monto[z] / mmax
    shapes[z] = (m, h)
    pts_all += [proj(x, y, h) for x, y in m] + [proj(x, y) for x, y in m]

part = [to_m(*p) for p in ring(feats["partido"])]
costa = [to_m(*p) for p in feats["costa"]["geometry"]["coordinates"]]
pts_all += [proj(x, y) for x, y in part]

minx = min(p[0] for p in pts_all) - 40; maxx = max(p[0] for p in pts_all) + 40
miny = min(p[1] for p in pts_all) - 40; maxy = max(p[1] for p in pts_all) + 70
W, Hh = maxx - minx, maxy - miny
P = lambda x, y, h=0.0: "%.1f,%.1f" % (proj(x, y, h)[0] - minx, proj(x, y, h)[1] - miny)

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {Hh:.0f}" width="{W:.0f}" height="{Hh:.0f}">']
# Río: del lado de la costa, hacia el noreste
c0, c1 = costa[0], costa[-1]
far = [(c1[0] + 6000, c1[1] + 6000), (c0[0] + 6000, c0[1] + 6000)]
river = costa + far
svg.append('<polygon points="%s" fill="#C9D3CF"/>' % " ".join(P(x, y) for x, y in river))
# Base: todo San Isidro, plano
svg.append('<polygon points="%s" fill="#E7E0D3" stroke="#CFC5B4" stroke-width="1"/>' % " ".join(P(x, y) for x, y in part))

def depth(z):
    m, h = shapes[z]
    return sum(proj(x, y)[1] for x, y in m) / len(m)

for z in sorted(zonas, key=depth):
    m, h = shapes[z]
    top = TOP[z]
    # sombra
    svg.append('<polygon points="%s" fill="#000" opacity="0.08" transform="translate(6,5)"/>' % " ".join(P(x, y) for x, y in m))
    # paredes: de atrás hacia adelante
    segs = list(zip(m, m[1:] + m[:1]))
    segs.sort(key=lambda s: (proj(*s[0])[1] + proj(*s[1])[1]) / 2)
    for (a, b) in segs:
        ax, ay = proj(*a); bx, by = proj(*b)
        # luz desde arriba a la izquierda: las caras que miran a la derecha, más oscuras
        nx = (by - ay); f = 0.72 if nx > 0 else 0.86
        svg.append('<polygon points="%s %s %s %s" fill="%s" stroke="%s" stroke-width="0.4"/>' % (
            P(*a), P(*b), P(b[0], b[1], h), P(a[0], a[1], h), shade(top, f), shade(top, f)))
    svg.append('<polygon points="%s" fill="%s" stroke="#F5F0E8" stroke-width="1.2" stroke-linejoin="round"/>' % (
        " ".join(P(x, y, h) for x, y in m), top))

# Nombres y montos, sobre cada bloque
for z in zonas:
    m, h = shapes[z]
    cx = sum(x for x, _ in m) / len(m); cy = sum(y for _, y in m) / len(m)
    px, py = proj(cx, cy, h); px -= minx; py -= miny
    nombre = datos[z]["nombre"]
    fig = datos[z]["cifras"]["obra_vecinal_anio4_monto"]["como_figura"].replace(" al año", "")
    svg.append(f'<g font-family="Inter, Arial, sans-serif" text-anchor="middle">'
               f'<text x="{px:.1f}" y="{py - 6:.1f}" font-size="15" font-weight="600" fill="#1F1915" stroke="#F5F0E8" stroke-width="3.5" paint-order="stroke">{nombre}</text>'
               f'<text x="{px:.1f}" y="{py + 12:.1f}" font-size="13" fill="#1F1915" stroke="#F5F0E8" stroke-width="3" paint-order="stroke">{fig}</text></g>')
svg.append('<text x="%.1f" y="%.1f" font-family="Spectral, Georgia, serif" font-style="italic" font-size="17" fill="#3F5560" text-anchor="middle">Río de la Plata</text>' % (W / 2, Hh - 18))
svg.append("</svg>")
open(OUT, "w").write("\n".join(svg))
print("ok", round(W), round(Hh))
