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
import matplotlib.colors as mcolors
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
    y = 0.985
    t = fig.text(x, y, exhibit, ha="left", va="top", fontsize=6.5,
                 color=RIO, family="sans-serif", weight="bold")
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
                     fontsize=6.2, color=AMBAR, family="sans-serif")
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
        ax.grid(True, axis=grilla, color=CAL, linewidth=0.8, zorder=0)
    ax.tick_params(length=0, pad=3)
    ax.set_axisbelow(True)


def guardar(fig, nombre, ajuste=None, encajar=True, transparente=False):
    """
    PNG a 300 dpi y SVG, los dos con fondo PAPEL y nunca transparente.

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
    png = os.path.join(SALIDA, nombre + ".png")
    svg = os.path.join(SALIDA, nombre + ".svg")
    for ruta in (png, svg):
        # transparente=True solo para la imagen de tapa: el PNG lo pinta
        # matplotlib y la pagina la pinta el motor de PDF, y dos beiges que
        # deberian ser el mismo dejan ver el rectangulo de la imagen. Sin fondo
        # propio no hay rectangulo que ver.
        fig.savefig(ruta, facecolor="none" if transparente else PAPEL,
                    edgecolor="none" if transparente else PAPEL,
                    transparent=transparente, dpi=DPI)
    plt.close(fig)
    return png, svg


DESBORDES = {}
SIN_ACENTO = {}
COLISIONES = {}


TEXTO_TAPADO = {}


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

    fondo = luminancia(PAPEL)
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
