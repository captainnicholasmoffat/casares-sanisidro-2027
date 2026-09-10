#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
El sistema visual del programa de gobierno. Lo importan todos los scripts de
graficos y NADIE define un color a mano.

LA PALETA — la del informe de referencia, muestreada de su PDF
  CREMA       fondo de todo
  TINTA       texto, ejes, titulares
  ACENTO      ladrillo profundo: la serie que el grafico quiere que se vea,
              los remates y las notas
  DATO        verde salvia: la serie principal
  DATO_CLARO  salvia clara: la cuarta serie, cuando hacen falta cuatro
  ARENA       bandas de encabezado y cajas
  FILA        filas alternadas y grillas

EL ACENTO ES UN ROJO LADRILLO. La regla anterior de este archivo prohibia el
rojo porque en la Argentina se lee como color politico. Queda sin efecto por
decision tomada: el sistema visual se copia entero del informe de referencia.
Lo que sigue prohibido es el rojo puro y las paletas por defecto de matplotlib:
la funcion aplicar() las desarma al importar el modulo.

NUMEROS: miles con punto y decimales con coma. 324.304 y 89,39%. Siempre con
numero(), pct() o millones(). Nunca con f-strings a mano.
"""

import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter, MaxNLocator

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")
SALIDA = os.path.join(REPO, "06_charts")

# --------------------------------------------------------------------------
# LA PALETA
# --------------------------------------------------------------------------
# Es la del informe de referencia, muestreada de su PDF pixel por pixel, y se
# usa tal cual. Se termino la busqueda de identidad propia: el sistema visual
# se copia entero y el trabajo se va a lo que si es nuestro, que son los datos.
#
# Los seis valores estan verificados contra el original: son los seis colores
# mas frecuentes de sus paginas, descontando los grises del antialias.
#
# EL ACENTO ES UN ROJO LADRILLO. La regla anterior del repo prohibia el rojo
# porque en Argentina se lee como color politico. Queda sin efecto por decision
# tomada: el ladrillo profundo de la referencia es el acento del documento.
CREMA = "#F5F0E8"        # el fondo de toda la pagina
TINTA = "#2A211C"        # el texto, negro calido
ACENTO = "#7C2E23"       # ladrillo profundo: titulos, numeros de seccion, marca
DATO = "#5E7157"         # verde salvia: la serie principal de los graficos
ARENA = "#EAE0CF"        # bandas de encabezado, cajas laterales
FILA = "#E8E4D9"         # filas alternadas de tabla

# La septima. El EXHIBIT 02 compara CUATRO series en las mismas seis
# categorias y con seis colores solo hay tres tintas que se lean sobre el
# crema. Esta es la salvia clara de la propia referencia —esta en sus paginas,
# muestreada igual que las otras seis— y no un color nuevo inventado.
# LOS DOS TONOS DE SUELO. No son colores nuevos: son la TINTA aguada sobre el
# CREMA, al 12 % y al 22 %, y caen exactos sobre la recta que une los dos. Son
# lo que sostiene un hueco de dato o separa dos filas, y estan hechos para NO
# competir con lo que va encima. Antes ese trabajo lo hacia la ARENA, que es un
# color de banda de tabla y de caja: puesta a hacer de dato quedaba a 1,15 de
# contraste contra el papel, o sea invisible, y el noveno verificador la caza.
HUECO = "#DDD7D0"        # la banda de un año sin dato
FILETE = "#C8C2BB"       # una linea que separa, no que dice

DATO_CLARO = "#7E9070"

# Nombres viejos, para no romper nada que todavia los use. NO USAR EN CODIGO
# NUEVO: dicen el color de la paleta anterior y ya no es el que pintan.
PAPEL = CREMA
RIO = DATO
BARRANCA = ACENTO
CAL = ARENA
AMBAR = ACENTO

PALETA = {"CREMA": CREMA, "TINTA": TINTA, "ACENTO": ACENTO, "DATO": DATO,
          "ARENA": ARENA, "FILA": FILA, "DATO_CLARO": DATO_CLARO}

ANCHO_PX = 1600
DPI = 300
ANCHO_IN = ANCHO_PX / DPI          # 5,333 pulgadas

# --------------------------------------------------------------------------
# LA TIPOGRAFIA DEL DOCUMENTO, TAMBIEN EN LOS GRAFICOS
# --------------------------------------------------------------------------
# Un exhibit rotulado con la fuente por defecto de matplotlib al lado de un
# texto compuesto en Spectral se ve como una captura de pantalla pegada adentro
# del documento. Asi que los graficos usan las mismas dos familias que la
# pagina, cargadas de 05_tipografia/.
#
# Spectral viene en cortes ESTATICOS: se registran tal cual, no hay nada que
# instanciar. Inter es variable y matplotlib no sabe mover un eje —carga la
# instancia por defecto y nada mas, o sea que no habria negrita—, asi que de
# Inter se instancian los dos pesos que se usan a un cache que no se versiona.
TIPOS = os.path.join(REPO, "05_tipografia")
CACHE_TIPOS = os.path.join(REPO, "_tipos_estaticos")

# Los cortes de Spectral se registran directo del repo.
_ESTATICAS = ["Spectral-Regular.ttf", "Spectral-Italic.ttf",
              "Spectral-Medium.ttf", "Spectral-MediumItalic.ttf",
              "Spectral-SemiBold.ttf", "Spectral-Bold.ttf"]

_INSTANCIAS = [
    ("Inter[opsz,wght].ttf", "Inter-Regular.ttf", {"opsz": 14, "wght": 400}),
    ("Inter[opsz,wght].ttf", "Inter-Medium.ttf", {"opsz": 14, "wght": 500}),
    ("Inter[opsz,wght].ttf", "Inter-Bold.ttf", {"opsz": 14, "wght": 700}),
]


def _instanciar_tipografia():
    """Registra las estaticas y las instancias. Devuelve (serif, sans)."""
    from fontTools import ttLib
    from fontTools.varLib import instancer
    from matplotlib import font_manager
    os.makedirs(CACHE_TIPOS, exist_ok=True)
    for nombre in _ESTATICAS:
        font_manager.fontManager.addfont(os.path.join(TIPOS, nombre))
    for origen, destino, ejes in _INSTANCIAS:
        ruta_o = os.path.join(TIPOS, origen)
        ruta_d = os.path.join(CACHE_TIPOS, destino)
        if (not os.path.exists(ruta_d)
                or os.path.getmtime(ruta_d) < os.path.getmtime(ruta_o)):
            fuente = ttLib.TTFont(ruta_o)
            instancer.instantiateVariableFont(fuente, ejes, inplace=True)
            fuente.save(ruta_d)
        font_manager.fontManager.addfont(ruta_d)
    return ["Spectral", "DejaVu Serif"], ["Inter", "DejaVu Sans"]


try:
    SERIF, SANS = _instanciar_tipografia()
except Exception as _e:                                      # pragma: no cover
    # Sin las fuentes el documento sale con otra letra y las cajas de texto
    # miden distinto: el verificador de colisiones dejaria de significar algo.
    raise RuntimeError(
        "no se pudieron cargar las tipografias de 05_tipografia/: %s" % _e)


def aplicar():
    """Desarma los valores por defecto de matplotlib y pone los nuestros."""
    plt.rcdefaults()
    plt.rcParams.update({
        "figure.facecolor": CREMA,
        "figure.edgecolor": CREMA,
        "savefig.facecolor": CREMA,
        "savefig.edgecolor": CREMA,
        "savefig.transparent": False,
        "axes.facecolor": CREMA,
        "axes.edgecolor": TINTA,
        "axes.labelcolor": TINTA,
        "axes.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": FILA,
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
        "axes.prop_cycle": matplotlib.cycler(
            color=[DATO, ACENTO, TINTA, DATO_CLARO]),
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
             color=DATO, family="sans-serif", weight="bold")
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
                 fontsize=6.2, color=ACENTO, family="sans-serif")


def _alto_en_figura(fig, artista):
    """Alto de un texto ya dibujado, en fraccion de figura."""
    fig.canvas.draw()
    caja = artista.get_window_extent(renderer=fig.canvas.get_renderer())
    return caja.transformed(fig.transFigure.inverted()).height


# Cuando PIE_EXTERNO esta activo, marco() NO dibuja la fuente ni la nota
# adentro del PNG: las registra para que las escriba quien maqueta.
#
# Un pie dibujado por matplotlib sale al mismo cuerpo y al mismo peso que el
# contenido del grafico y compite con el. Al pie de un exhibit en el documento
# va en cuerpo 7, italica y gris, que es donde tiene que estar.
PIE_EXTERNO = False
# Y LA CABECERA TAMBIEN: el rotulo, el titulo y la bajada los compone el
# armador del PDF. Ver marco(). La enciende generar_todos_los_graficos.py.
CABECERA_EXTERNA = False
PIES = {}
_PIE_PENDIENTE = {}


def marco(fig, exhibit, titulo, bajada=None, fuente=None, nota=None,
          x=0.012, aire=0.014):
    """
    Dibuja la cabecera y el pie MIDIENDO cada bloque, y devuelve el (top,
    bottom) que le queda libre al grafico.

    Antes las posiciones estaban fijas y el resultado dependia de que el titulo
    entrara en una linea: si envolvia en dos, se comia la bajada. Y el pie
    estaba clavado abajo, asi que chocaba con las etiquetas del eje. Aca cada
    bloque se dibuja, se mide y el siguiente arranca donde termina el anterior.

    Devuelve (top, bottom) para pasarle a subplots_adjust.
    """
    if CABECERA_EXTERNA:
        # LA CABECERA NO SE DIBUJA: la compone el armador del PDF con la
        # tipografia y los cuerpos de la pagina, leyendo este mismo texto de
        # 06_charts/pies.json.
        #
        # Antes se dibujaba igual y el armador se la recortaba al PNG buscando
        # la franja de fondo mas alta del tercio superior. Funcionaba mientras
        # el grafico empezaba con aire debajo del titulo. Con el mapa base
        # —agua y vecinos que llegan hasta el borde— ese aire desaparecio, el
        # recorte corto por el hueco equivocado y la bajada quedo impresa DOS
        # veces: una dibujada adentro de la imagen y otra compuesta arriba.
        # Recortar era el arreglo de un problema que no habia que tener.
        _PIE_PENDIENTE.clear()
        _PIE_PENDIENTE.update(exhibit=exhibit, titulo=titulo, bajada=bajada,
                              fuente=fuente, nota=nota)
        # No 1,0: el rotulo mas alto del eje y va CENTRADO en su marca, asi
        # que la mitad de su cuerpo queda por encima de la caja de los ejes y
        # sin este aire se sale del lienzo. Lo denunciaba el verificador de
        # desborde en cuatro exhibits.
        return 0.955, min(0.70, 0.012 + aire * 1.9)

    y = 0.985
    t = fig.text(x, y, exhibit, ha="left", va="top", fontsize=6.5,
                 color=DATO, family="sans-serif", weight="bold")
    y -= _alto_en_figura(fig, t) + aire * 0.5

    t = fig.text(x, y, envolver(titulo, 11.5), ha="left", va="top",
                 fontsize=11.5, color=TINTA, family="serif")
    y -= _alto_en_figura(fig, t) + aire * 0.6

    if bajada:
        t = fig.text(x, y, envolver(bajada, 7.4), ha="left", va="top",
                     fontsize=7.4, color=TINTA, alpha=0.72,
                     family="sans-serif")
        y -= _alto_en_figura(fig, t)
    top = max(0.30, y - aire * 1.6)

    y = 0.012
    if PIE_EXTERNO:
        _PIE_PENDIENTE.clear()
        _PIE_PENDIENTE.update(exhibit=exhibit, titulo=titulo, bajada=bajada,
                              fuente=fuente, nota=nota)
        return top, min(0.70, y + aire * 1.9)
    if fuente:
        t = fig.text(x, y, envolver("Fuente: " + fuente, 6.2), ha="left",
                     va="bottom", fontsize=6.2, color=TINTA, alpha=0.62,
                     family="sans-serif")
        y += _alto_en_figura(fig, t) + aire * 0.4
    if nota:
        t = fig.text(x, y, envolver(nota, 6.2), ha="left", va="bottom",
                     fontsize=6.2, color=ACENTO, family="sans-serif")
        y += _alto_en_figura(fig, t)
    bottom = min(0.70, y + aire * 1.9)
    return top, bottom


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
        ax.grid(True, axis=grilla, color=ARENA, linewidth=0.8, zorder=0)
    ax.tick_params(length=0, pad=3)
    ax.set_axisbelow(True)


def guardar(fig, nombre, ajuste=None, encajar=True, transparente=False):
    """
    PNG a 300 dpi y SVG, los dos con fondo CREMA y nunca transparente.

    El area libre que devuelve marco() se le pasa a tight_layout como
    rectangulo, no a subplots_adjust. La diferencia importa: subplots_adjust
    coloca la CAJA de los ejes, pero las etiquetas de los ticks y el rotulo del
    eje cuelgan por fuera de esa caja y terminan encima del pie. tight_layout
    encaja los ejes CON sus decoraciones adentro del rectangulo.

    encajar=False para los mapas, que llevan ejes agregados a mano y a los que
    tight_layout les mueve la barra de color.
    """
    os.makedirs(SALIDA, exist_ok=True)
    if ajuste:
        if encajar:
            fig.tight_layout(rect=(ajuste.get("left", 0),
                                   ajuste.get("bottom", 0),
                                   ajuste.get("right", 1),
                                   ajuste.get("top", 1)))
        else:
            fig.subplots_adjust(**ajuste)
    if PIE_EXTERNO and _PIE_PENDIENTE:
        PIES[nombre] = dict(_PIE_PENDIENTE)
        _PIE_PENDIENTE.clear()
    DESBORDES[nombre] = verificar_desborde(fig)
    SIN_ACENTO[nombre] = verificar_acentos(fig)
    COLISIONES[nombre] = verificar_colisiones(fig)
    TEXTO_TAPADO[nombre] = verificar_texto_tapado(fig)
    DERRAMADOS[nombre] = verificar_texto_derramado(fig)
    SIN_CONTRASTE[nombre] = verificar_contraste(fig)
    png = os.path.join(SALIDA, nombre + ".png")
    svg = os.path.join(SALIDA, nombre + ".svg")
    for ruta in (png, svg):
        # transparente=True solo para la imagen de tapa: el PNG lo pinta
        # matplotlib y la pagina la pinta el motor de PDF, y dos beiges que
        # deberian ser el mismo dejan ver el rectangulo de la imagen. Sin fondo
        # propio no hay rectangulo que ver.
        fig.savefig(ruta, facecolor="none" if transparente else CREMA,
                    edgecolor="none" if transparente else CREMA,
                    transparent=transparente, dpi=DPI)
    plt.close(fig)
    return png, svg


DESBORDES = {}
SIN_CONTRASTE = {}
SIN_ACENTO = {}
COLISIONES = {}


TEXTO_TAPADO = {}
DERRAMADOS = {}


def verificar_texto_tapado(fig, umbral=0.22):
    """
    SEXTO VERIFICADOR. Falla si un texto queda encima de una barra, una linea
    o un area rellena y por lo tanto no se puede leer.

    Por que existe
    --------------
    El EXHIBIT 02 rotulaba sus cuatro series sobre la PRIMERA zona. Las cuatro
    etiquetas caian una encima de otra y, peor, detras de las barras vecinas.
    Paso los cinco verificadores anteriores y nadie lo vio hasta que alguien
    miro el PDF armado: verificar_colisiones() mide texto contra TEXTO, y esto
    era texto contra BARRA.

    Que mira
    --------
    Cada texto contra cada elemento con relleno (barras, rectangulos, areas) y
    contra cada linea gruesa. Denuncia cuando se solapan y ademas:
      - el elemento se dibuja por ENCIMA del texto (zorder mayor), o
      - el texto y el relleno tienen un contraste bajo.

    Que NO mira
    -----------
    Los textos con halo (path_effects) estan hechos a proposito para ir encima
    de una forma: las etiquetas de los mapas. Se saltean.
    Tampoco los textos con caja propia (bbox), por lo mismo.
    """
    from matplotlib.patches import Rectangle

    fig.canvas.draw()
    ren = fig.canvas.get_renderer()

    def luminancia(c, sobre=None):
        """Luminancia percibida. Si el color tiene alpha, se mezcla contra el
        fondo antes de medir: un relleno al 16% no tapa nada, y tratarlo como
        opaco denunciaba gráficos que se leen perfecto."""
        try:
            r, g, b, a = mcolors.to_rgba(c)
        except Exception:
            return None
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        if sobre is not None and a < 1:
            lum = a * lum + (1 - a) * sobre
        return lum

    fondo = luminancia(CREMA)
    fuera = []

    for ax in fig.get_axes():
        formas = []
        for art in list(ax.patches) + list(ax.collections):
            if not getattr(art, "get_visible", lambda: True)():
                continue
            fc = None
            try:
                fc = art.get_facecolor()
                if hasattr(fc, "__len__") and len(fc) and hasattr(fc[0], "__len__"):
                    fc = fc[0]
            except Exception:
                pass
            if isinstance(art, Rectangle) and art.get_width() == 0:
                continue
            try:
                bb = art.get_window_extent(ren)
            except Exception:
                continue
            if bb.width < 2 or bb.height < 2:
                continue
            formas.append((bb, art.get_zorder(), fc))

        for t in ax.texts:
            if t.get_path_effects():          # halo: va encima a proposito
                continue
            if t.get_bbox_patch() is not None:  # caja propia: idem
                continue
            txt = (t.get_text() or "").strip()
            if not txt:
                continue
            try:
                tb = t.get_window_extent(ren)
            except Exception:
                continue
            area_t = max(tb.width * tb.height, 1e-9)
            lum_t = luminancia(t.get_color())
            for bb, z, fc in formas:
                ancho = min(tb.x1, bb.x1) - max(tb.x0, bb.x0)
                alto = min(tb.y1, bb.y1) - max(tb.y0, bb.y0)
                if ancho <= 0 or alto <= 0:
                    continue
                frac = (ancho * alto) / area_t
                if frac < umbral:
                    continue
                # ESTRICTAMENTE mayor: a igual zorder matplotlib dibuja el
                # texto DESPUES del relleno, asi que se lee. Con >= se
                # denunciaba cada etiqueta escrita adentro de su propia barra.
                tapado = z > t.get_zorder()
                lum_f = luminancia(fc, sobre=fondo)
                poco_contraste = (lum_t is not None and lum_f is not None
                                  and abs(lum_t - lum_f) < 0.28
                                  and (fondo is None or abs(lum_f - fondo) > 0.05))
                if tapado or poco_contraste:
                    fuera.append(
                        "%r queda %s un elemento del grafico (%d%% del texto)"
                        % (txt[:40],
                           "detras de" if tapado else "sobre",
                           round(frac * 100)))
                    break
    return fuera

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
    # Segunda tanda: las que aparecieron al mirar los titulos uno por uno.
    # "ano" va aca aunque parezca obvia, porque escrita sin tilde dice otra
    # cosa y estaba en el titulo del exhibit 14.
    "ano": "año", "anos": "años", "deficit": "déficit",
    "superavit": "superávit", "inflacion": "inflación",
    "inversion": "inversión", "terminos": "términos", "titulo": "título",
    "subio": "subió", "estan": "están", "tambien": "también",
    "millon": "millón", "codigo": "código", "grafico": "gráfico",
    "graficos": "gráficos", "numeros": "números",
    "metodologia": "metodología", "economica": "económica",
    "ultimo": "último", "ultima": "última", "ultimos": "últimos",
    "proximo": "próximo", "maximos": "máximos", "minimos": "mínimos",
    "educacion": "educación", "atencion": "atención",
    "administracion": "administración", "recaudacion": "recaudación",
    "clasificacion": "clasificación",
    "reclasificacion": "reclasificación", "comision": "comisión",
    "categoria": "categoría", "energia": "energía", "practica": "práctica",
    "publicos": "públicos", "publicas": "públicas",
}


def _es_nombre_de_archivo(texto, pos):
    """
    True si la palabra que empieza en 'pos' es parte de una ruta o de un
    nombre de archivo.

    Los identificadores en snake_case y las rutas NO llevan tilde: el archivo
    se llama ejecucion_gastos_objeto.csv y escribirlo "ejecución" en el pie de
    un grafico manda al lector a un archivo que no existe. La regla ya estaba
    escrita en el proyecto; esto la hace mecanica.
    """
    ini = texto.rfind(" ", 0, pos) + 1
    fin = texto.find(" ", pos)
    ficha = texto[ini:fin if fin >= 0 else len(texto)]
    return "/" in ficha or "_" in ficha or "." in ficha.rstrip(".,;:")


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
            # Con mayuscula inicial tambien: "Coparticipacion" al principio de
            # un rotulo se escapaba de la busqueda sensible a mayusculas.
            for m, b in ((mala, buena),
                         (mala[0].upper() + mala[1:],
                          buena[0].upper() + buena[1:])):
                if m == mala.upper():
                    continue
                for hallado in re.finditer(
                        r"(?<![A-Za-zÁÉÍÓÚÑáéíóúñ])%s"
                        r"(?![A-Za-zÁÉÍÓÚÑáéíóúñ])" % re.escape(m), texto):
                    if _es_nombre_de_archivo(texto, hallado.start()):
                        continue
                    fallas.append("%r dice %r y va %r"
                                  % (texto.replace("\n", " ")[:52], m, b))
    return sorted(set(fallas))


def caja_de_texto(t, ren):
    """
    La caja de LO ESCRITO, sin la flecha.

    Annotation.get_window_extent() devuelve la union del texto y de su flecha,
    asi que una etiqueta con linea guia larga reportaba una caja del tamaño de
    media figura y el verificador de colisiones la acusaba de pisar a todo lo
    que la linea cruzaba. Una linea guia que pasa al lado de un rotulo no es
    una colision: es para lo que existe la linea guia.
    """
    return matplotlib.text.Text.get_window_extent(t, renderer=ren)


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
            caja = caja_de_texto(t, ren)
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


def _cajas_de_texto(fig):
    """Las cajas de todos los textos que se van a dibujar, ya renderizadas."""
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    cajas = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not (t.get_text() or "").strip():
            continue
        ejes = getattr(t, "axes", None)
        if ejes is not None and not getattr(ejes, "axison", True):
            # Los mapas apagan sus ejes: sus ticks existen pero no se dibujan.
            # Los textos que pusimos a mano sobre el mapa si cuentan, y esos no
            # son ticks, asi que se distinguen por no tener eje asociado a un
            # tick.
            if t in list(ejes.get_xticklabels()) + list(ejes.get_yticklabels()):
                continue
        try:
            caja = caja_de_texto(t, ren)
        except Exception:
            continue
        if caja.width <= 0 or caja.height <= 0:
            continue
        cajas.append((t, caja))
    return cajas


def verificar_colisiones(fig, umbral=0.10, holgura_px=1.0):
    """
    Falla si dos textos se pisan.

    Controlar el borde del lienzo no alcanza: un titulo puede estar entero
    adentro de la imagen y aun asi caer encima de otro. Se comparan todas las
    cajas entre si y se reporta el par cuando el area solapada supera el
    umbral del area del texto mas chico de los dos.

    holgura_px encoge cada caja antes de comparar: las cajas de matplotlib
    traen un poco de aire alrededor de las letras y sin esto dos textos que
    apenas se rozan darian falso positivo.
    """
    cajas = _cajas_de_texto(fig)
    fallas = []
    for i in range(len(cajas)):
        t1, c1 = cajas[i]
        for j in range(i + 1, len(cajas)):
            t2, c2 = cajas[j]
            x0 = max(c1.x0, c2.x0) + holgura_px
            x1 = min(c1.x1, c2.x1) - holgura_px
            y0 = max(c1.y0, c2.y0) + holgura_px
            y1 = min(c1.y1, c2.y1) - holgura_px
            if x1 <= x0 or y1 <= y0:
                continue
            solape = (x1 - x0) * (y1 - y0)
            menor = min(c1.width * c1.height, c2.width * c2.height)
            if menor <= 0 or solape / menor < umbral:
                continue
            a = t1.get_text().replace("\n", " ")[:34]
            b = t2.get_text().replace("\n", " ")[:34]
            fallas.append("%r se pisa con %r (%.0f%% del mas chico)"
                          % (a, b, 100 * solape / menor))
    return sorted(set(fallas))


def verificar_texto_derramado(fig, holgura_px=1.5):
    """
    OCTAVO VERIFICADOR. Falla si un texto se sale de la forma que lo contiene.

    Por que existe
    --------------
    El EXHIBIT 11 rotulaba cada tramo de una barra apilada CENTRADO adentro de
    su tramo. El rotulo mas largo era mas ancho que su tramo, asi que se
    derramaba sobre los dos vecinos: la parte que caia sobre el tramo oscuro era
    texto oscuro sobre oscuro, y la que caia sobre el claro, texto claro sobre
    claro. En el PDF se leia "ontratos de servicio", sin la C, y una cifra
    partida al medio.

    Los siete verificadores anteriores lo dejaron pasar, y cada uno por su
    motivo, que conviene tener escrito porque es el hueco que este tapa:
      - verificar_colisiones mide texto contra TEXTO, y los tres rotulos no se
        tocaban entre si: se derramaban sobre BARRAS;
      - verificar_texto_tapado mide el texto contra la forma que tiene DEBAJO
        en el mismo punto, y en el centro del tramo el contraste era correcto:
        el problema estaba en las puntas;
      - verificar_desborde mide contra el borde del LIENZO, y el texto estaba
        holgadamente adentro de la imagen.

    Que mira
    --------
    Un texto cuyo centro cae adentro de una forma rellena esta rotulando esa
    forma. Entonces tiene que ENTRAR en ella. Si sobresale, sale sobre lo que
    haya al lado, que es lo que no se puede leer.

    Que NO mira
    -----------
    Los textos con halo o con caja propia: estan hechos para ir por encima de
    cualquier cosa. Y los textos cuyo centro NO cae sobre ninguna forma: esos no
    rotulan una forma, van sobre el papel, y de ellos se ocupan los otros.
    """
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    fuera = []
    for ax in fig.get_axes():
        formas = []
        for art in list(ax.patches):
            if not art.get_visible():
                continue
            try:
                bb = art.get_window_extent(ren)
            except Exception:
                continue
            if bb.width < 2 or bb.height < 2:
                continue
            formas.append(bb)
        for t in ax.texts:
            if t.get_path_effects() or t.get_bbox_patch() is not None:
                continue
            txt = (t.get_text() or "").strip()
            if not txt:
                continue
            try:
                c = caja_de_texto(t, ren)
            except Exception:
                continue
            cx, cy = (c.x0 + c.x1) / 2, (c.y0 + c.y1) / 2
            dentro = [bb for bb in formas
                      if bb.x0 <= cx <= bb.x1 and bb.y0 <= cy <= bb.y1]
            if not dentro:
                continue
            # La mas chica de las que lo contienen es la que rotula: en una
            # barra apilada, el tramo y no la barra entera.
            bb = min(dentro, key=lambda b: b.width * b.height)
            sobra_x = max(bb.x0 - c.x0, c.x1 - bb.x1)
            if sobra_x <= holgura_px:
                continue
            # Salirse no basta para denunciar: lo que no se puede leer es lo
            # que se sale ENCIMA DE OTRA FORMA. "sin rendición" del EXHIBIT 01
            # sobresale 5 px de su banda y esos 5 px caen sobre el papel que
            # separa dos barras, donde se lee perfecto. Se comprueba si el
            # sobrante pisa alguna otra forma; si no pisa nada, no es un error.
            from matplotlib.transforms import Bbox
            sobrantes = []
            if c.x0 < bb.x0 - holgura_px:
                sobrantes.append(Bbox.from_extents(c.x0, c.y0, bb.x0, c.y1))
            if c.x1 > bb.x1 + holgura_px:
                sobrantes.append(Bbox.from_extents(bb.x1, c.y0, c.x1, c.y1))
            pisadas = [o for o in formas if o is not bb
                       and any(o.overlaps(sb) for sb in sobrantes)]
            if not pisadas:
                continue
            fuera.append("%r se sale %.0f px de la forma que rotula y cae "
                         "encima de otra (la forma mide %.0f px de ancho y el "
                         "texto %.0f)"
                         % (txt.replace("\n", " ")[:40], sobra_x,
                            bb.width, c.width))
    return sorted(set(fuera))


# ==========================================================================
# LA LISTA NEGRA — ESTOS COLORES NO SON DE LA PALETA, SON LOS QUE SE BUSCAN
# ==========================================================================
# OJO AL LEER ESTO. Aca hay verdes, azules y rojos que no tienen NADA que ver
# con el sistema visual del documento: son los colores por defecto de
# matplotlib —el ciclo tab10 y sus alias— y estan escritos para BUSCARLOS en el
# SVG ya generado y fallar si aparecen.
#
# Vivian arriba, pegados a la paleta, y ahi se leen como si fueran parte de
# ella: un color muerto al lado de los vivos es el que alguien usa por error
# despues. Por eso viven aca abajo, al lado de la unica funcion que los mira.
#
# BORRARLOS NO SACA ESOS COLORES DEL DOCUMENTO: saca el control que los caza.
# Es exactamente al reves de lo que parece.
PROHIBIDOS = {"#d62728", "#ff0000", "red", "#2ca02c", "#00ff00", "green",
              "#1f77b4", "#ff7f0e", "tab:red", "tab:green", "tab:blue"}


# --------------------------------------------------------------------------
# NOVENO VERIFICADOR: CONTRASTE
# --------------------------------------------------------------------------
# El EXHIBIT 04 salio publicado con los ciento seis municipios dibujados en
# ARENA #EAE0CF sobre el papel CREMA #F5F0E8. Los dos colores estan en la
# paleta, asi que verificar_paleta dijo OK. Ninguno de los otros siete miraba
# tampoco: no hay texto tapado —no hay texto—, no hay colision, no hay
# desborde, el acento esta. Y el grafico no se veia: la relacion de contraste
# entre esos dos cremas es 1,13, y el dato del grafico son esos puntos.
#
# LA REGLA. Una SERIE es de un color; una ESCALA es de muchos. Una serie tiene
# que separarse del fondo lo suficiente para verse: se le pide 1,7 de relacion
# de contraste WCAG, que es lo que deja pasar la salvia (4,64), la salvia clara
# (3,22), el ladrillo (8,1) y la tinta (14,3), y lo que voltea a la arena
# (1,13) y al color de fila (1,10). Esos dos ultimos son fondo de banda y de
# caja, no son colores de dato, y ahi es donde se habian metido.
#
# Un artista con TRES O MAS colores distintos es una escala —la rampa de los
# mapas, por ejemplo— y ahi lo que importa no es que cada tono se separe del
# papel sino que la escala entera tenga recorrido: se le mira el extremo mas
# oscuro y se le pide lo mismo que a una serie.
UMBRAL_CONTRASTE = 1.7


def _luminancia(rgb):
    """Luminancia relativa WCAG de un color en 0..1."""
    def canal(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(float(c)) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(color_a, color_b):
    """Relacion de contraste WCAG entre dos colores, de 1 a 21."""
    from matplotlib.colors import to_rgb
    la, lb = _luminancia(to_rgb(color_a)), _luminancia(to_rgb(color_b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _colores_del_artista(art):
    """Los colores con que un artista PINTA, ya sean relleno o trazo."""
    import numpy as np
    fuera = []
    for getter in ("get_facecolor", "get_facecolors", "get_color",
                   "get_edgecolor", "get_edgecolors"):
        f = getattr(art, getter, None)
        if f is None:
            continue
        try:
            v = f()
        except Exception:                                # pragma: no cover
            continue
        if v is None:
            continue
        a = np.atleast_2d(np.asarray(v, dtype=object))
        if a.dtype == object or a.ndim != 2 or a.shape[1] < 3:
            try:
                from matplotlib.colors import to_rgba
                a = np.atleast_2d([to_rgba(v)])
            except Exception:                            # pragma: no cover
                continue
        for fila in np.asarray(a, dtype=float):
            if len(fila) >= 4 and fila[3] < 0.25:        # transparente
                continue
            fuera.append(tuple(round(float(c), 4) for c in fila[:3]))
        if fuera and getter in ("get_facecolor", "get_facecolors",
                                "get_color"):
            break                                        # el relleno manda
    return fuera


def verificar_contraste(fig, umbral=UMBRAL_CONTRASTE):
    """Denuncia todo color de serie que no se separa del fondo que lo sostiene.

    Devuelve una lista de descripciones; vacia quiere decir que todo lo que
    pinta se ve.
    """
    from matplotlib.colors import to_rgb
    fallas = []
    for ax in fig.axes:
        fondo = ax.get_facecolor()
        if len(fondo) >= 4 and fondo[3] < 0.25:
            fondo = fig.get_facecolor()
        piezas = (list(ax.collections) + list(ax.patches) + list(ax.lines))
        for art in piezas:
            if not art.get_visible():
                continue
            cols = _colores_del_artista(art)
            if not cols:
                continue
            unicos = sorted(set(cols))
            # Los halos y los bordes en el color del papel no son dato, y el
            # SUELO del mapa tampoco: el agua, los partidos vecinos y las vias
            # son la tinta aguada sobre el crema —caen exactos sobre la recta
            # que une los dos— y estan dibujados justamente para NO competir
            # con el dato que va encima. Pedirles 1,7 seria pedirle al mapa que
            # se rompa para callar al verificador. La arena y el color de fila
            # no caen sobre esa recta, asi que siguen fallando: son colores de
            # banda y de caja que se habian metido a hacer de serie.
            unicos = [c for c in unicos
                      if contraste(c, fondo) > 1.02
                      and not _es_tinta_aguada(*[x * 255 for x in c])]
            if not unicos:
                continue
            if len(unicos) >= 3:                          # es una escala
                revisar = [max(unicos, key=lambda c: contraste(c, fondo))]
                que = "la escala de %s" % type(art).__name__
            else:
                revisar = unicos
                que = type(art).__name__
            for c in revisar:
                r = contraste(c, fondo)
                if r < umbral:
                    fallas.append(
                        "%s pinta en #%02x%02x%02x sobre #%02x%02x%02x: "
                        "contraste %.2f, hace falta %.2f"
                        % (que, int(c[0] * 255), int(c[1] * 255),
                           int(c[2] * 255),
                           int(to_rgb(fondo)[0] * 255),
                           int(to_rgb(fondo)[1] * 255),
                           int(to_rgb(fondo)[2] * 255), r, umbral))
    # Un mismo color mal usado en cuatro artistas da cuatro lineas iguales.
    vistas, salida = set(), []
    for f in fallas:
        if f not in vistas:
            vistas.add(f)
            salida.append(f)
    return salida


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
        if _es_dilucion(r, g, bl):                    # tinta aguada sobre crema
            continue
        otros.add(m)
    return hallados + sorted(otros)


# --------------------------------------------------------------------------

def _es_dilucion(r, g, b, tolerancia=7):
    """True si el color es un color de la paleta aguado sobre el crema.

    El mapa base necesita tonos intermedios que no son colores nuevos: el agua
    es la tinta al 8% sobre el crema, los partidos vecinos al 5%, las vias al
    40%. Todos caen sobre la recta que une el crema con la tinta, asi que se
    reconocen y se aceptan. Un color de verdad nuevo no cae sobre ninguna de
    esas rectas y sigue fallando.

    No alcanza con la regla del gris del antialias: nuestra tinta es un negro
    CALIDO, y su dilucion tiene los tres canales separados por mas de seis
    puntos. Con esa regla sola, cada linea del mapa base era un color prohibido.
    """
    base = _hex_a_rgb(CREMA)
    for c in (TINTA, ACENTO, DATO, DATO_CLARO, ARENA, FILA):
        cr, cg, cb = _hex_a_rgb(c)
        dr, dg, db = cr - base[0], cg - base[1], cb - base[2]
        denom = dr * dr + dg * dg + db * db
        if not denom:
            continue
        # La proyeccion del color sobre la recta crema -> color de paleta.
        t = ((r - base[0]) * dr + (g - base[1]) * dg + (b - base[2]) * db) / denom
        if not -0.02 <= t <= 1.02:
            continue
        px, py, pz = (base[0] + dr * t, base[1] + dg * t, base[2] + db * t)
        if (abs(r - px) <= tolerancia and abs(g - py) <= tolerancia
                and abs(b - pz) <= tolerancia):
            return True
    return False


def _es_tinta_aguada(r, g, b, tolerancia=6):
    """True si el color cae sobre la recta que une el CREMA con la TINTA.

    Es el suelo de los mapas: el agua es la tinta al 8 % sobre el crema, los
    partidos vecinos al 5 %, las vias al 20 %. Ninguno es un color de dato.
    La ARENA no cae sobre esa recta —su azul se aparta catorce puntos— asi que
    esta funcion no la perdona.
    """
    base, fin = _hex_a_rgb(CREMA), _hex_a_rgb(TINTA)
    dr, dg, db = (fin[k] - base[k] for k in range(3))
    denom = dr * dr + dg * dg + db * db
    t = ((r - base[0]) * dr + (g - base[1]) * dg + (b - base[2]) * db) / denom
    if not -0.02 <= t <= 1.02:
        return False
    return all(abs(v - (base[k] + d * t)) <= tolerancia
               for k, (v, d) in enumerate(zip((r, g, b), (dr, dg, db))))


def _hex_a_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _en_la_rampa(r, g, b, tolerancia=8):
    """
    Los mapas pintan con la rampa CREMA -> ACENTO, asi que sus tonos
    intermedios son legitimos aunque no esten en la paleta. Se acepta un color
    si cae sobre esa recta en el espacio RGB.
    """
    for desde, hasta in ((CREMA, ACENTO), (ARENA, ACENTO), (CREMA, DATO)):
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


def sin_offset(ax):
    """
    Mata el "1e6" que matplotlib pone en la esquina cuando los valores del eje
    son grandes. En un mapa con coordenadas UTM aparece aunque el eje este
    apagado, y se planta arriba a la izquierda encima de la bajada.
    """
    for eje in (ax.xaxis, ax.yaxis):
        eje.get_offset_text().set_visible(False)
        eje.set_major_formatter(matplotlib.ticker.NullFormatter())


def podar_tick_superior(ax, eje="x", n=6, podar="upper"):
    """
    El ultimo tick de un eje que llega al borde se dibuja medio afuera del
    lienzo. prune="upper" lo saca sin tocar la escala.
    """
    loc = MaxNLocator(nbins=n, prune=podar)
    (ax.xaxis if eje == "x" else ax.yaxis).set_major_locator(loc)


def apagar_ejes(ax):
    """
    set_axis_off() no borra los objetos de texto de los ticks: los deja
    invisibles pero existiendo. Para un mapa hay que sacarlos de verdad.
    """
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])


def rampa(desde=CREMA, hasta=ACENTO, n=256):
    """Rampa secuencial de CREMA a ACENTO para los mapas."""
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


def dos_lineas(texto, maximo=11):
    """
    Parte un rotulo largo en dos lineas por el espacio mas cercano al medio.

    Es para los ejes con una categoria por columna: seis zonas en 5,3 pulgadas
    dejan unos trece caracteres por columna, y "Boulogne Sur Mer" no entra.
    Cortar por el medio y no por el ancho da dos lineas parecidas en vez de una
    larga y una de dos letras.
    """
    t = (texto or "").strip()
    if len(t) <= maximo or " " not in t:
        return t
    medio = len(t) / 2.0
    corte = min((i for i, c in enumerate(t) if c == " "),
                key=lambda i: abs(i - medio))
    return t[:corte] + "\n" + t[corte + 1:]



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


# Las ocho medidas de transparencia y sus estados. El CSV va en ASCII, igual
# que todos los datos del repo, y la tilde se pone al mostrarlo: misma tecnica
# que NOMBRE_FUNCION y NOMBRE_ZONA. Si una clave del CSV no esta en estas
# tablas, nombre_medida() y nombre_estado() la devuelven tal cual y el
# verificador de acentos la denuncia: no hay forma de que un texto sin tilde
# pase sin que alguien se entere.
NOMBRE_MEDIDA = {
    "Publicar el organigrama municipal":
        "Publicar el organigrama municipal",
    "Publicar la planta de personal y la escala salarial":
        "Publicar la planta de personal y la escala salarial",
    "Publicar compras contrataciones y licitaciones":
        "Publicar compras, contrataciones y licitaciones",
    "Publicar las declaraciones juradas de funcionarios":
        "Publicar las declaraciones juradas de funcionarios",
    "Reponer el Portal de Datos Abiertos o publicar sus datasets por otra via":
        "Reponer el Portal de Datos Abiertos o publicar sus datasets por otra vía",
    "Publicar la rendicion de cuentas":
        "Publicar la rendición de cuentas",
    "Publicar la Ordenanza Fiscal e Impositiva vigente":
        "Publicar la Ordenanza Fiscal e Impositiva vigente",
    "Publicar la ejecucion presupuestaria por zona":
        "Publicar la ejecución presupuestaria por zona",
}

NOMBRE_ESTADO = {
    "no_existe": "No existe",
    "enlace_incorrecto": "Enlace incorrecto",
    "caido": "Caído",
    "desactualizado": "Desactualizado",
    "cumplida": "Cumplida",
}

NOMBRE_EVIDENCIA = {
    "portal de transparencia municipal":
        "no está en el portal de transparencia",
    "el enlace lleva a declaraciones de contribuyentes":
        "lleva a declaraciones de contribuyentes",
    "devuelve error 504":
        "devuelve error 504",
    "la ultima publicada es de 2022":
        "la última publicada es de 2022",
    "la ultima publicada es de 2024":
        "la última publicada es de 2024",
    "no existe en ningun municipio del conurbano norte":
        "no existe en ningún municipio del norte",
}


def nombre_medida(clave):
    """La medida de transparencia lista para mostrar. El CSV queda en ASCII."""
    return NOMBRE_MEDIDA.get(clave.strip(), clave.strip())


def nombre_estado(clave):
    return NOMBRE_ESTADO.get(clave.strip(), clave.strip())


def nombre_evidencia(clave):
    return NOMBRE_EVIDENCIA.get(clave.strip(), clave.strip())


ORDEN_ZONAS = None


def zonas_ordenadas():
    """Las seis zonas de peor a mejor por NBI. Un solo orden para todos."""
    global ORDEN_ZONAS
    if ORDEN_ZONAS is None:
        filas = leer("data/zonas_indicadores.csv")
        filas.sort(key=lambda r: int(r["orden_peor_a_mejor"]))
        ORDEN_ZONAS = filas
    return ORDEN_ZONAS
