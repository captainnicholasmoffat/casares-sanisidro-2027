#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from matplotlib.ticker import FuncFormatter, MaxNLocator

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

def envolver(texto, fontsize, ancho_in=None, margen_in=0.13):
    """
    Corta el texto en varias lineas para que entre en el ancho de la figura.

    El ancho disponible se mide en pulgadas contra el lienzo, no se asume. La
    estimacion es conservadora: 0,52 del cuerpo de la fuente por caracter, que
    es mas ancho que el promedio real de DejaVu Sans, asi que si se equivoca se
    equivoca cortando de mas y no de menos. Lo que quede afuera igual lo
    atrapa verificar_desborde().
    """
    import textwrap
    ancho_in = (ancho_in or ANCHO_IN) - 2 * margen_in
    por_caracter = 0.52 * fontsize / 72.0
    n = max(20, int(ancho_in / por_caracter))
    return "\n".join(textwrap.wrap(texto, n)) if texto else texto


def etiqueta_corta(texto, ancho=26, lineas=2):
    """
    Nombre largo de funcion o finalidad, listo para un eje: en minusculas con
    la inicial en mayuscula, cortado en varias lineas y con puntos suspensivos
    si aun asi no entra. Los nombres vienen del PDF y algunos ya llegan
    truncados por la fuente.
    """
    import textwrap
    t = texto.strip()
    t = t[0].upper() + t[1:].lower() if t else t
    partes = textwrap.wrap(t, ancho)[:lineas]
    if not partes:
        return t
    if len("\n".join(partes)) < len(t):
        partes[-1] = partes[-1].rstrip(" ,(") + "..."
    return "\n".join(partes)


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
    fig.text(0.012, 0.935, envolver(titulo, 11.5), ha="left", va="top",
             fontsize=11.5, color=TINTA, family="serif")
    if bajada:
        fig.text(0.012, 0.885, envolver(bajada, 7.4), ha="left", va="top",
                 fontsize=7.4, color=TINTA, alpha=0.72, family="sans-serif")


def pie(fig, fuente, nota=None):
    """Linea de fuente al pie. Sin esto el grafico no se publica."""
    texto = envolver("Fuente: " + fuente, 6.2)
    lineas_fuente = texto.count("\n") + 1
    fig.text(0.012, 0.028, texto, ha="left", va="bottom", fontsize=6.2,
             color=TINTA, alpha=0.62, family="sans-serif")
    if nota:
        # La nota se apoya encima de la fuente, cuantas lineas haga falta.
        y = 0.028 + lineas_fuente * 0.026 + 0.008
        fig.text(0.012, y, envolver(nota, 6.2), ha="left", va="bottom",
                 fontsize=6.2, color=AMBAR, family="sans-serif")


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
    DESBORDES[nombre] = verificar_desborde(fig)
    SIN_ACENTO[nombre] = verificar_acentos(fig)
    png = os.path.join(SALIDA, nombre + ".png")
    svg = os.path.join(SALIDA, nombre + ".svg")
    for ruta in (png, svg):
        fig.savefig(ruta, facecolor=PAPEL, edgecolor=PAPEL, transparent=False,
                    dpi=DPI)
    plt.close(fig)
    return png, svg


DESBORDES = {}
SIN_ACENTO = {}

# Palabras que en un documento en español SIEMPRE llevan tilde. Si alguna
# aparece sin tilde en un texto que se dibuja, el grafico no se publica.
# La clave es la forma incorrecta; el valor, la correcta.
ACENTOS_OBLIGATORIOS = {
    "anios": "años", "anio": "año", "mas": "más", "maximo": "máximo",
    "minimo": "mínimo", "elaboracion": "elaboración",
    "ejecucion": "ejecución", "rendicion": "rendición",
    "poblacion": "población", "Martinez": "Martínez", "basicas": "básicas",
    "unico": "único", "unica": "única", "limites": "límites",
    "funcion": "función", "gestion": "gestión", "publico": "público",
    "publica": "pública", "periodo": "período", "segun": "según",
    "analisis": "análisis", "dia": "día", "asi": "así", "aqui": "aquí",
    "despues": "después", "ademas": "además", "regimen": "régimen",
    "indice": "índice", "numero": "número", "fraccion": "fracción",
    "participacion": "participación", "percepcion": "percepción",
    "reasignacion": "reasignación", "coparticipacion": "coparticipación",
    "situacion": "situación", "economico": "económico",
    "proporcion": "proporción", "variacion": "variación",
    "composicion": "composición", "ecologia": "ecología",
    "critico": "crítico", "geometria": "geometría", "vacios": "vacíos",
    "Lopez": "López", "tamano": "tamaño", "senala": "señala",
}


def verificar_acentos(fig):
    """
    Recorre el texto que la figura va a DIBUJAR y falla si encuentra una
    palabra que en español lleva tilde escrita sin ella.

    Se mira lo que se dibuja y no el codigo fuente: un nombre de variable sin
    acento no importa porque no se ve, y un dato que viene del CSV tampoco es
    culpa nuestra. Lo que no puede pasar es que un titulo diga "poblacion".

    Los textos enteramente en mayusculas se saltean: son valores de datos que
    vienen asi de la fuente (SAN ISIDRO, ECOLOGIA Y MEDIO AMBIENTE) y
    corregirlos seria alterar el dato.
    """
    import unicodedata
    fallas = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible():
            continue
        texto = (t.get_text() or "").strip()
        if not texto or texto.isupper():
            continue
        for mala, buena in ACENTOS_OBLIGATORIOS.items():
            if re.search(r"(?<![A-Za-zÁÉÍÓÚÑáéíóúñ])%s(?![A-Za-zÁÉÍÓÚÑáéíóúñ])"
                         % re.escape(mala), texto):
                fallas.append("%r dice %r y va %r"
                              % (texto.replace("\n", " ")[:52], mala, buena))
    return sorted(set(fallas))


def verificar_desborde(fig, tolerancia_px=1.0):
    """
    Ningun caracter puede quedar afuera del lienzo.

    Recorre todos los objetos de texto de la figura, les pide su caja al
    renderer ya dibujado y la compara contra el lienzo. Devuelve la lista de
    los que se salen, con cuantos pixeles y para que lado.

    Es la misma idea que verificar_paleta(): que la regla sea una restriccion y
    no una intencion. Un titulo cortado no se nota hasta que alguien abre el
    PNG, y para entonces ya esta publicado.
    """
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    ancho, alto = fig.get_size_inches() * fig.dpi
    fallas = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not (t.get_text() or "").strip():
            continue
        # Los mapas apagan sus ejes con set_axis_off(): las etiquetas de los
        # ticks siguen existiendo como objetos pero no se dibujan, asi que no
        # cuentan como desborde.
        ejes = getattr(t, "axes", None)
        if ejes is not None and not getattr(ejes, "axison", True):
            continue
        try:
            caja = t.get_window_extent(renderer=ren)
        except Exception:
            continue
        fuera = []
        if caja.x0 < -tolerancia_px:
            fuera.append("izquierda %.0f px" % -caja.x0)
        if caja.x1 > ancho + tolerancia_px:
            fuera.append("derecha %.0f px" % (caja.x1 - ancho))
        if caja.y0 < -tolerancia_px:
            fuera.append("abajo %.0f px" % -caja.y0)
        if caja.y1 > alto + tolerancia_px:
            fuera.append("arriba %.0f px" % (caja.y1 - alto))
        if fuera:
            muestra = t.get_text().replace("\n", " ")[:52]
            fallas.append("%r se sale por %s" % (muestra, " y ".join(fuera)))
    return fallas


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


def podar_tick_superior(ax, eje="x", n=6):
    """
    El ultimo tick de un eje que llega al borde se dibuja medio afuera del
    lienzo. prune="upper" lo saca sin tocar la escala.
    """
    loc = MaxNLocator(nbins=n, prune="upper")
    (ax.xaxis if eje == "x" else ax.yaxis).set_major_locator(loc)


def apagar_ejes(ax):
    """
    set_axis_off() no borra los objetos de texto de los ticks: los deja
    invisibles pero existiendo. Para un mapa hay que sacarlos de verdad.
    """
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])


def rampa(desde=PAPEL, hasta=BARRANCA, n=256):
    """Rampa secuencial de PAPEL a BARRANCA para los mapas."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list("sanisidro", [desde, hasta], N=n)


def leer(ruta):
    """CSV del repo, salteando las lineas de advertencia que empiezan con #."""
    import csv
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


# Los nombres de zona en los CSV vienen sin acento porque salen de la
# geometria. Para mostrarlos se usa esta tabla: el dato no se toca, la etiqueta
# si. Cambiar el CSV para que diga "Martinez" con acento romperia las claves.
NOMBRE_ZONA = {
    "Martinez": "Martínez",
    "Beccar": "Beccar",
    "Boulogne Sur Mer": "Boulogne Sur Mer",
    "Villa Adelina": "Villa Adelina",
    "San Isidro": "San Isidro",
    "Acassuso": "Acassuso",
}


def zona_bonita(nombre):
    return NOMBRE_ZONA.get(nombre, nombre)


# Los nombres de funcion vienen en mayusculas y sin tildes del PDF del
# Municipio, y uno llega truncado por la propia fuente. El dato NO se toca: se
# muestran con esta tabla, igual que los nombres de zona. Lo que la fuente
# escribe mal no se corrige en el CSV, se corrige al mostrarlo y queda dicho.
NOMBRE_FUNCION = {
    "A CLASIFICAR": "A clasificar",
    "ADMINISTRACION FISCAL": "Administración fiscal",
    "AGRICULTURA": "Agricultura",
    "AGUA POTABLE Y ALCANTARILLADO": "Agua potable y alcantarillado",
    "CIENCIA Y TECNICA": "Ciencia y técnica",
    "COMERCIO, TURISMO Y OTROS SERVICIOS": "Comercio, turismo y otros servicios",
    "COMUNICACIONES": "Comunicaciones",
    "CONTROL DE LA GESTION PUBLICA": "Control de la gestión pública",
    "DIRECCION SUPERIOR EJECUTIVA": "Dirección superior ejecutiva",
    "ECOLOGIA Y MEDIO AMBIENTE": "Ecología y medio ambiente",
    "EDUCACION Y CULTURAL": "Educación y cultura",
    "JUDICIAL": "Judicial",
    "LEGISLATIVA": "Legislativa",
    "PROMOCION Y ASISTENCIA SOCIAL": "Promoción y asistencia social",
    "RELACIONES CON LA COMUNIDAD": "Relaciones con la comunidad",
    "RELACIONES INTERIORES": "Relaciones interiores",
    "SALUD": "Salud",
    "SEGURIDAD INTERNA": "Seguridad interna",
    "SERVICIOS DE LA DEUDA PUBLICA (INTERESES Y GAST":
        "Servicios de la deuda pública",
    "TRABAJO": "Trabajo",
    "TRANSPORTE": "Transporte",
    "URBANISMO": "Urbanismo",
    "VIVIENDA": "Vivienda",
    "VIVIENDA Y URBANISMO": "Vivienda y urbanismo",
}


def nombre_funcion(clave):
    """El nombre de la funcion listo para mostrar. El dato queda intacto."""
    return NOMBRE_FUNCION.get(clave.strip().upper(), etiqueta_corta(clave))


ORDEN_ZONAS = None


def zonas_ordenadas():
    """Las seis zonas de peor a mejor por NBI. Un solo orden para todos."""
    global ORDEN_ZONAS
    if ORDEN_ZONAS is None:
        filas = leer("data/zonas_indicadores.csv")
        filas.sort(key=lambda r: int(r["orden_peor_a_mejor"]))
        ORDEN_ZONAS = filas
    return ORDEN_ZONAS
