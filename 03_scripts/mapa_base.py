#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EL MAPA BASE — agua, vecinos, relieve y vias, con datos reales

Los mapas del documento eran poligonos planos flotando en el vacio: sin rio,
sin vecinos, sin relieve y sin una sola referencia que le dijera al lector
donde esta parado. Este modulo pone abajo de las zonas lo que un mapa tiene que
tener, y todo sale de datos que estan en el repo y se pueden abrir:

  EL AGUA        el poligono del Rio de la Plata de OpenStreetMap, recortado al
                 encuadre. Dibujado como agua —tono propio y trama de lineas
                 finas horizontales—, no como el hueco que queda cuando se
                 termina la tierra.
  LOS VECINOS    San Fernando, Tigre, General San Martin y Vicente Lopez, en
                 gris muy claro y con su nombre. Sin ellos, el partido flota;
                 con ellos, se ve que San Isidro es una franja entre el rio y
                 el conurbano.
  EL RELIEVE     LA BARRANCA. San Isidro se define por ese escalon: la ciudad
                 alta arriba, la franja costera abajo. Un modelo de elevacion
                 real —Terrain Tiles de AWS, 01_raw/relieve_srtm.npz— sombreado
                 suave por encima del color. En el perfil del propio dato se ve
                 el salto: 28 m a un kilometro de la costa y 0 m en la costa.
  LAS VIAS       la Panamericana y la Avenida del Libertador, las dos
                 referencias que cualquier vecino ubica sin pensar.

NADA DE ESTO SE GENERA NI SE DIBUJA DE MEMORIA. Un mapa inventado es
geograficamente falso, y una sola cosa falsa en un documento que se ofrece para
que le revisen las cuentas se lleva puesto todo lo demas. Si falta un dato, el
mapa se dibuja sin esa capa y se dice.

TRAZOS FINOS. Todo el mapa se dibuja con lineas de un cuarto de punto a medio
punto. Los bordes gruesos eran la mitad del problema: convertian una division
administrativa en un contorno de historieta.
"""

import json
import os

import numpy as np

import estilo as E

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")

AGUA = os.path.join(DATA, "agua_rio_de_la_plata_osm.geojson")
VIAS = os.path.join(DATA, "vias_principales_osm.geojson")
VECINOS = os.path.join(DATA, "partidos_vecinos_osm.geojson")
RELIEVE = os.path.join(REPO, "01_raw", "relieve_srtm.npz")

CRS_METRICO = "EPSG:32721"

# Cuanto se abre el encuadre alrededor del partido, en veces su propio tamaño.
# Con 0,16 entran los cuatro vecinos y la costa sin que el partido se achique.
MARGEN = 0.16


def _mezcla(color, sobre, parte):
    """`color` diluido sobre `sobre`. Para sacar tonos de la paleta sin
    agregar colores nuevos: un gris de agua es la tinta al 12% sobre el crema."""
    import matplotlib.colors as mc
    a = np.array(mc.to_rgb(color))
    b = np.array(mc.to_rgb(sobre))
    return mc.to_hex(b + (a - b) * parte)


AGUA_COLOR = None            # se calculan al importar, abajo
AGUA_TRAMA = None
VECINO_COLOR = None
VECINO_BORDE = None
VIA_COLOR = None


def _colores():
    global AGUA_COLOR, AGUA_TRAMA, VECINO_COLOR, VECINO_BORDE, VIA_COLOR
    AGUA_COLOR = _mezcla(E.TINTA, E.CREMA, 0.085)
    AGUA_TRAMA = _mezcla(E.TINTA, E.CREMA, 0.20)
    VECINO_COLOR = _mezcla(E.TINTA, E.CREMA, 0.055)
    VECINO_BORDE = _mezcla(E.TINTA, E.CREMA, 0.28)
    VIA_COLOR = _mezcla(E.TINTA, E.CREMA, 0.40)


_colores()


def _leer(ruta, crs):
    import geopandas as gpd
    if not os.path.exists(ruta):
        return None
    g = gpd.read_file(ruta)
    if g.crs is None:
        g = g.set_crs("EPSG:4326")
    return g.to_crs(crs)


def encuadre(partido):
    """El rectangulo que se dibuja, en el CRS metrico del partido."""
    x0, y0, x1, y1 = partido.total_bounds
    dx, dy = (x1 - x0) * MARGEN, (y1 - y0) * MARGEN
    return x0 - dx, y0 - dy, x1 + dx, y1 + dy


def _caja(caja):
    from shapely.geometry import box
    return box(*caja)


def dibujar(ax, partido, caja=None, vecinos=True, relieve=True, vias=True,
            nombres_vecinos=True, tam_nombre=5.6):
    """Pinta el fondo del mapa. Devuelve el encuadre usado.

    Se llama ANTES de dibujar las zonas: el agua y los vecinos van abajo. El
    relieve es la excepcion y lo pone relieve_encima(), que se llama despues.
    """
    import geopandas as gpd
    caja = caja or encuadre(partido)
    marco = _caja(caja)
    crs = partido.crs

    # --- el agua ---------------------------------------------------------
    # El rio se recorta al encuadre. Si el poligono de OSM no llegara a cubrir
    # la esquina, se ve el crema abajo y no una mancha inventada.
    agua = _leer(AGUA, crs)
    tierra = partido.union_all()
    vec_geo = _leer(VECINOS, crs)
    if vec_geo is not None:
        tierra = tierra.union(vec_geo.union_all())
    if agua is not None:
        rio = agua.union_all()
        # El contorno del rio en OSM esta generalizado y no cierra exactamente
        # contra el borde de los partidos: quedaba una cuña de papel entre el
        # agua y la costa, que se leia como un desgarro del mapa. Se agrega lo
        # que en el encuadre no es tierra y esta a menos de dos kilometros del
        # rio; mas lejos que eso hay partidos que no dibujamos y pintarlos de
        # agua seria decir algo falso.
        cerca = rio.buffer(2000)
        relleno = marco.difference(tierra).intersection(cerca)
        recorte = gpd.GeoSeries([marco.intersection(rio).union(relleno)],
                                crs=crs)
        if not recorte.is_empty.all():
            recorte.plot(ax=ax, color=AGUA_COLOR, zorder=1, linewidth=0)
            # La trama: lineas finas horizontales, que es como se dibuja el
            # agua en cartografia impresa desde antes del color.
            recorte.plot(ax=ax, facecolor="none", edgecolor=AGUA_TRAMA,
                         hatch="----", linewidth=0, zorder=1.1)

    # --- los partidos vecinos --------------------------------------------
    if vecinos:
        vec = _leer(VECINOS, crs)
        if vec is not None:
            vec = vec.copy()
            vec["geometry"] = vec.geometry.intersection(marco)
            # San Fernando y Tigre tienen jurisdiccion sobre el rio, asi que sus
            # poligonos entran al agua. Es cierto y ademas ilegible: media
            # lamina de agua pintada de tierra. Manda el agua, que es lo que el
            # lector necesita para ubicarse.
            if agua is not None:
                vec["geometry"] = vec.geometry.difference(recorte.iloc[0])
            vec = vec[~vec.geometry.is_empty]
            vec.plot(ax=ax, color=VECINO_COLOR, edgecolor=VECINO_BORDE,
                     linewidth=0.25, zorder=2)
            if nombres_vecinos:
                # El nombre va al centro de la parte del vecino que SE VE. Con
                # el punto representativo del poligono entero, "General San
                # Martin" caia sobre el borde del encuadre y salia cortado.
                mx = (caja[2] - caja[0]) * 0.035
                for _, r in vec.iterrows():
                    p = r.geometry.representative_point()
                    x = min(max(p.x, caja[0] + mx), caja[2] - mx)
                    y = min(max(p.y, caja[1] + mx), caja[3] - mx)
                    ax.annotate(
                        r["partido"].replace("Partido de ", "").upper(),
                        (x, y), ha="center", va="center",
                        fontsize=tam_nombre, color=VECINO_BORDE,
                        family="sans-serif", zorder=2.5)

    # --- las vias --------------------------------------------------------
    # Tres clases y tres pesos. Todos por debajo de medio punto: son la
    # referencia para ubicarse, no el tema del mapa, y una autopista gruesa le
    # gana la atencion al dato que el exhibit vino a mostrar.
    if vias:
        v = _leer(VIAS, crs)
        if v is not None:
            v = v.copy()
            v["geometry"] = v.geometry.intersection(marco)
            v = v[~v.geometry.is_empty]
            for clase, ancho, alfa, guion in (
                    ("ferrocarril", 0.30, 0.75, (0, (2.2, 1.4))),
                    ("avenida", 0.30, 0.55, None),
                    ("autopista", 0.55, 0.85, None)):
                sub = v[v["clase"] == clase]
                if sub.empty:
                    continue
                sub.plot(ax=ax, color=VIA_COLOR, linewidth=ancho, zorder=5.5,
                         alpha=alfa, linestyle=guion or "solid")

    ax.set_xlim(caja[0], caja[2])
    ax.set_ylim(caja[1], caja[3])
    return caja


def _difuminar(a, radio=8, pasadas=3):
    """Media movil separable, repetida. Tres pasadas aproximan una gaussiana."""
    k = 2 * radio + 1
    for _ in range(pasadas):
        acum = np.cumsum(np.pad(a, ((0, 0), (radio + 1, radio)), mode="edge"),
                         axis=1)
        a = (acum[:, k:] - acum[:, :-k]) / k
        acum = np.cumsum(np.pad(a, ((radio + 1, radio), (0, 0)), mode="edge"),
                         axis=0)
        a = (acum[k:, :] - acum[:-k, :]) / k
    return a


def relieve_encima(ax, partido, caja=None, alpha=0.16):
    """El sombreado de la barranca, POR ENCIMA del color de las zonas.

    Va encima y no debajo porque abajo lo tapa el relleno del coropleto y no se
    ve nada. Encima, a dos decimas de opacidad y en gris calido, se lee como
    relieve y no ensucia la rampa: el ojo separa la sombra del tono.
    """
    if not os.path.exists(RELIEVE):
        return False
    import matplotlib.colors as mc
    from pyproj import Transformer

    d = np.load(RELIEVE)
    altura, ext = d["altura"], d["extent"]

    # SE SUAVIZA ANTES DE SOMBREAR. El modelo tiene un pixel cada 9,5 m y en
    # una ciudad llana lo que mide a esa escala son las manzanas y el ruido del
    # sensor, no el terreno: sombreado crudo, el partido salia con una textura
    # de piedra pomez y la barranca se perdia adentro. Difuminando a unos
    # ciento cincuenta metros queda la forma del terreno y se va el resto.
    altura = _difuminar(altura, radio=8, pasadas=3)

    # Sombreado estandar: azimut noroeste, que es como se lee un relieve en
    # papel. exageracion vertical alta porque la barranca son quince metros en
    # un partido de once kilometros y sin exagerar no se ve.
    ls = mc.LightSource(azdeg=315, altdeg=35)
    sombra = ls.hillshade(altura, vert_exag=55, dx=9.5, dy=9.5)
    # Solo la parte oscura: la clara sobre crema no aporta y lava el color.
    oscuro = np.clip(1.0 - sombra, 0, 1) ** 1.25

    rgba = np.zeros(oscuro.shape + (4,))
    rgba[..., :3] = mc.to_rgb(E.TINTA)
    rgba[..., 3] = oscuro * alpha

    tr = Transformer.from_crs("EPSG:4326", partido.crs, always_xy=True)
    x0, y0 = tr.transform(ext[0], ext[2])
    x1, y1 = tr.transform(ext[1], ext[3])
    im = ax.imshow(rgba, extent=(x0, x1, y0, y1), origin="upper", zorder=5.2,
                   interpolation="bilinear")
    # Se recorta a la tierra del propio partido: sombrear el rio seria dibujar
    # olas donde el dato dice cero.
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    tierra = partido.union_all()
    trozos = getattr(tierra, "geoms", [tierra])
    verts, codes = [], []
    for g in trozos:
        for anillo in [g.exterior] + list(g.interiors):
            pts = list(anillo.coords)
            verts += pts
            codes += [Path.MOVETO] + [Path.LINETO] * (len(pts) - 2) + \
                     [Path.CLOSEPOLY]
    im.set_clip_path(PathPatch(Path(verts, codes), transform=ax.transData))
    if caja:
        ax.set_xlim(caja[0], caja[2])
        ax.set_ylim(caja[1], caja[3])
    return True


def rotulo_agua(ax, caja, texto="RÍO DE LA PLATA", tam=6.0, alto=0.30):
    """El nombre del rio, sobre el agua, en el margen de la derecha.

    `alto` es la altura relativa dentro del encuadre. Se elige por mapa: el
    partido cruza la lamina en diagonal, asi que el agua libre esta a distinta
    altura segun donde caigan las llamadas de cada exhibit.
    """
    x = caja[0] + (caja[2] - caja[0]) * 0.955
    y = caja[1] + (caja[3] - caja[1]) * alto
    ax.annotate(texto, (x, y), ha="right", va="center", fontsize=tam,
                color=_mezcla(E.TINTA, E.CREMA, 0.42), family="sans-serif",
                rotation=-31, zorder=5.6)


def clave_vias(ax, caja, x_rel=0.035, y_rel=0.155, tam=5.4):
    """Dos lineas y dos palabras: que es cada trazo del fondo.

    Sin esto, el lector ve rayas y no sabe si son calles, limites o cursos de
    agua. Va debajo de la barra de escala, que es donde se leen las claves de
    un mapa.
    """
    ancho = caja[2] - caja[0]
    alto = caja[3] - caja[1]
    x = caja[0] + ancho * x_rel
    for i, (etiqueta, guion) in enumerate((("autopista", "solid"),
                                           ("ferrocarril", (0, (2.2, 1.4))))):
        y = caja[1] + alto * (y_rel - i * 0.032)
        ax.plot([x, x + ancho * 0.038], [y, y], color=VIA_COLOR,
                linewidth=0.55 if i == 0 else 0.30, linestyle=guion, zorder=8)
        ax.text(x + ancho * 0.048, y, etiqueta, ha="left", va="center",
                fontsize=tam, color=VIA_COLOR, family="sans-serif", zorder=8)
