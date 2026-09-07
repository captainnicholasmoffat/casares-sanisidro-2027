#!/usr/bin/env python3
"""
El sistema visual del programa de gobierno. Lo importan todos los scripts de
graficos y NADIE define un color a mano.

LA PALETA
  PAPEL     fondo de todo
  TINTA     texto, ejes, titulares
  RIO       serie primaria
  BARRANCA  serie secundaria y contraste
  CAL       fondos, bandas, grillas
  AMBAR     SOLO advertencias y notas

PROHIBIDO el rojo y el verde. En la Argentina el rojo se lee como color
politico y el verde como su respuesta. Un grafico de gasto publico no puede
tener ninguno de los dos. Tampoco se usa ninguna paleta por defecto de
matplotlib: la funcion aplicar() las desarma al importar el modulo.

NUMEROS: miles con punto y decimales con coma. 324.304 y 89,39%. Siempre con
numero(), pct() o millones(). Nunca con f-strings a mano.
"""

import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")
SALIDA = os.path.join(REPO, "06_charts")

PAPEL = "#FAF8F4"
TINTA = "#16293A"
RIO = "#2D6E7E"
BARRANCA = "#A8763F"
CAL = "#EDE9E2"
AMBAR = "#8A6A1F"

PALETA = {"PAPEL": PAPEL, "TINTA": TINTA, "RIO": RIO,
          "BARRANCA": BARRANCA, "CAL": CAL, "AMBAR": AMBAR}

# Colores que no pueden aparecer en ningun grafico. verificar_paleta() los
# busca en el SVG generado y falla si encuentra alguno.
PROHIBIDOS = {"#d62728", "#ff0000", "red", "#2ca02c", "#00ff00", "green",
              "#1f77b4", "#ff7f0e", "tab:red", "tab:green", "tab:blue"}

ANCHO_PX = 1600
DPI = 300
ANCHO_IN = ANCHO_PX / DPI          # 5,333 pulgadas

SERIF = ["DejaVu Serif", "Georgia", "serif"]
SANS = ["DejaVu Sans", "Helvetica", "sans-serif"]


def aplicar():
    """Desarma los valores por defecto de matplotlib y pone los nuestros."""
    plt.rcdefaults()
    plt.rcParams.update({
        "figure.facecolor": PAPEL,
        "figure.edgecolor": PAPEL,
        "savefig.facecolor": PAPEL,
        "savefig.edgecolor": PAPEL,
        "savefig.transparent": False,
        "axes.facecolor": PAPEL,
        "axes.edgecolor": TINTA,
        "axes.labelcolor": TINTA,
        "axes.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": CAL,
        "grid.linewidth": 0.8,
        "grid.alpha": 1.0,
        "axes.axisbelow": True,
        "text.color": TINTA,
        "xtick.color": TINTA,
        "ytick.color": TINTA,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "font.family": "sans-serif",
        "font.sans-serif": SANS,
        "font.serif": SERIF,
        "font.size": 7.5,
        "legend.frameon": False,
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        # Sin ciclo de color por defecto: el que quiera un color lo pide.
        "axes.prop_cycle": matplotlib.cycler(color=[RIO, BARRANCA, TINTA, AMBAR]),
    })


aplicar()


# --------------------------------------------------------------------------
# Numeros a la castellana
# --------------------------------------------------------------------------

def numero(x, decimales=0):
    """1234567.5 -> '1.234.567,5'. Miles con punto, decimales con coma."""
    if x is None:
        return ""
    s = ("{:,.%df}" % decimales).format(float(x))
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def pct(x, decimales=1):
    return numero(x, decimales) + "%"


def millones(x, decimales=0):
    """Pesos a millones, ya formateados."""
    return numero(float(x) / 1_000_000, decimales)


def eje_numero(decimales=0):
    return FuncFormatter(lambda v, _: numero(v, decimales))


def eje_pct(decimales=0):
    return FuncFormatter(lambda v, _: pct(v, decimales))


def eje_millones(decimales=0):
    return FuncFormatter(lambda v, _: numero(v / 1_000_000, decimales))


# --------------------------------------------------------------------------
# El armazon de cada grafico
# --------------------------------------------------------------------------

def figura(alto_in=3.2, ejes=True):
    fig = plt.figure(figsize=(ANCHO_IN, alto_in))
    if not ejes:
        return fig, None
    ax = fig.add_subplot(111)
    return fig, ax


def titular(fig, exhibit, titulo, bajada=None):
    """
    Numero de exhibit chiquito arriba, titulo descriptivo en serif, y una
    bajada opcional que dice que hay que mirar.
    """
    fig.text(0.012, 0.975, exhibit, ha="left", va="top", fontsize=6.5,
             color=RIO, family="sans-serif", weight="bold")
    fig.text(0.012, 0.935, titulo, ha="left", va="top", fontsize=11.5,
             color=TINTA, family="serif")
    if bajada:
        fig.text(0.012, 0.885, bajada, ha="left", va="top", fontsize=7.4,
                 color=TINTA, alpha=0.72, family="sans-serif")


def pie(fig, fuente, nota=None):
    """Linea de fuente al pie. Sin esto el grafico no se publica."""
    fig.text(0.012, 0.028, "Fuente: " + fuente, ha="left", va="bottom",
             fontsize=6.2, color=TINTA, alpha=0.62, family="sans-serif")
    if nota:
        fig.text(0.012, 0.002, nota, ha="left", va="bottom", fontsize=6.2,
                 color=AMBAR, family="sans-serif")


def etiqueta_serie(ax, x, y, texto, color, dx=4, dy=0, **kw):
    """Etiqueta la serie al lado del dato en vez de mandarla a una leyenda."""
    ax.annotate(texto, (x, y), xytext=(dx, dy), textcoords="offset points",
                color=color, fontsize=7.5, va="center", weight="bold", **kw)


def limpiar(ax, grilla="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(TINTA)
    ax.spines["bottom"].set_linewidth(0.7)
    ax.grid(False)
    if grilla:
        ax.grid(True, axis=grilla, color=CAL, linewidth=0.8, zorder=0)
    ax.tick_params(length=0, pad=3)
    ax.set_axisbelow(True)


def guardar(fig, nombre, ajuste=None):
    """PNG a 300 dpi y SVG, los dos con fondo PAPEL y nunca transparente."""
    os.makedirs(SALIDA, exist_ok=True)
    if ajuste:
        fig.subplots_adjust(**ajuste)
    png = os.path.join(SALIDA, nombre + ".png")
    svg = os.path.join(SALIDA, nombre + ".svg")
    for ruta in (png, svg):
        fig.savefig(ruta, facecolor=PAPEL, edgecolor=PAPEL, transparent=False,
                    dpi=DPI)
    plt.close(fig)
    return png, svg


def verificar_paleta(nombre):
    """
    Abre el SVG generado y busca colores prohibidos. Es la red que atrapa un
    rojo que se colo por un valor por defecto que no desarmamos.
    """
    ruta = os.path.join(SALIDA, nombre + ".svg")
    if not os.path.exists(ruta):
        return ["no se genero %s.svg" % nombre]
    txt = open(ruta, encoding="utf-8").read().lower()
    # Solo se miran los atributos que pintan: fill, stroke y style. Si se
    # buscara en todo el SVG, la palabra "red" de "sin gas de red" daria un
    # falso positivo y el chequeo dejaria de servir.
    pintura = " ".join(re.findall(
        r'(?:fill|stroke|stop-color)\s*[:=]\s*"?([^;"\s>]+)', txt))
    hallados = [c for c in PROHIBIDOS if re.search(r"\b%s\b" % re.escape(c.lower()),
                                                   pintura)]
    permitidos = {c.lower() for c in PALETA.values()}
    otros = set()
    for m in re.findall(r"#[0-9a-f]{6}", pintura):
        if m in permitidos:
            continue
        r, g, bl = int(m[1:3], 16), int(m[3:5], 16), int(m[5:7], 16)
        if abs(r - g) <= 6 and abs(g - bl) <= 6:      # gris del antialias
            continue
        if _en_la_rampa(r, g, bl):                    # tono de los mapas
            continue
        otros.add(m)
    return hallados + sorted(otros)


# --------------------------------------------------------------------------

def _hex_a_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _en_la_rampa(r, g, b, tolerancia=8):
    """
    Los mapas pintan con la rampa PAPEL -> BARRANCA, asi que sus tonos
    intermedios son legitimos aunque no esten en la paleta. Se acepta un color
    si cae sobre esa recta en el espacio RGB.
    """
    for desde, hasta in ((PAPEL, BARRANCA), (CAL, BARRANCA), (PAPEL, RIO)):
        d, h = _hex_a_rgb(desde), _hex_a_rgb(hasta)
        # Proyeccion del color sobre el segmento d-h.
        vx = [h[i] - d[i] for i in range(3)]
        px = [(r, g, b)[i] - d[i] for i in range(3)]
        largo2 = sum(c * c for c in vx)
        if not largo2:
            continue
        t = max(0.0, min(1.0, sum(px[i] * vx[i] for i in range(3)) / largo2))
        cerca = [d[i] + t * vx[i] for i in range(3)]
        if all(abs(cerca[i] - (r, g, b)[i]) <= tolerancia for i in range(3)):
            return True
    return False


def rampa(desde=PAPEL, hasta=BARRANCA, n=256):
    """Rampa secuencial de PAPEL a BARRANCA para los mapas."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list("sanisidro", [desde, hasta], N=n)


def leer(ruta):
    """CSV del repo, salteando las lineas de advertencia que empiezan con #."""
    import csv
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


ORDEN_ZONAS = None


def zonas_ordenadas():
    """Las seis zonas de peor a mejor por NBI. Un solo orden para todos."""
    global ORDEN_ZONAS
    if ORDEN_ZONAS is None:
        filas = leer("data/zonas_indicadores.csv")
        filas.sort(key=lambda r: int(r["orden_peor_a_mejor"]))
        ORDEN_ZONAS = filas
    return ORDEN_ZONAS
