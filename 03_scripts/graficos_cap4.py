#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capitulo 4 - El mecanismo. Exhibits 13 a 16, incluidos los dos mapas."""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E
import matplotlib.pyplot as plt

FUENTE_CENSO = ("INDEC, Censo Nacional de Población, Hogares y Viviendas 2022, "
                "procesado con Redatam 7; zonas propias sobre radios censales")

# --------------------------------------------------------------------------
# Regla de reparto de la partida vecinal
# --------------------------------------------------------------------------
#
# POOL = bienes de uso devengados en 2025 x 50%. Es la mitad de la obra publica
# que el capitulo 4 pone a decidir a las comisiones vecinales.
#
# INDICE DE NECESIDAD, sobre CUATRO indicadores y no sobre uno:
#     para cada indicador k, max_k = el mayor valor entre las seis zonas
#     need_zona = promedio( valor_zona[k] / max_k )  sobre los cuatro
#
# Normalizar cada indicador por su propio maximo es lo que permite promediarlos:
# sin eso, "sin gas de red" (que llega al 41%) aplastaria a "NBI" (que llega al
# 5,8%) y el indice seria en los hechos un solo indicador disfrazado de cuatro.
#
# PESO de cada zona:
#     w = 0,5 x (poblacion_zona / poblacion_total)
#       + 0,5 x (need_zona / suma_need)
#
# La mitad por poblacion reconoce que cada vecino cuenta igual; la otra mitad,
# que no todas las zonas arrancan del mismo lugar.
#
# La poblacion es la de zonas_indicadores.csv, que suma 295.978: son las
# personas en viviendas PARTICULARES. Los 297.282 del partido incluyen 1.304 en
# viviendas colectivas, que el Censo no publica por radio y por lo tanto no se
# pueden asignar a ninguna zona.

INDICADORES_NECESIDAD = ["pct_nbi", "pct_sin_cloaca", "pct_sin_gas_red",
                         "pct_hacinamiento"]
PESO_POBLACION = 0.5
PESO_NECESIDAD = 0.5

# La parte de la obra publica que administran las comisiones en el anio 4. Se
# importa del modelo: es la MISMA constante, no una copia.
try:
    from modelo import SHARE_OBRA_VECINAL as _SHARE
    SHARE_OBRA_VECINAL = float(_SHARE)
except Exception:                                     # pragma: no cover
    SHARE_OBRA_VECINAL = 0.50


def _nbi_del_partido():
    """NBI del partido, contado desde los 360 radios. No se escribe a mano."""
    con = tot = 0
    for f in E.leer("data/censo2022_sanisidro_por_radio.csv"):
        con += int(float(f.get("hogares_nbi__si") or 0))
        tot += int(float(f.get("hogares_nbi__total") or 0))
    return 100.0 * con / tot if tot else 0.0


def indice_de_necesidad(zonas):
    """Promedio de los cuatro indicadores, cada uno sobre su propio máximo."""
    maximos = {k: max(float(z[k]) for z in zonas) for k in INDICADORES_NECESIDAD}
    return {z["zona"]: sum(float(z[k]) / maximos[k]
                           for k in INDICADORES_NECESIDAD) / len(INDICADORES_NECESIDAD)
            for z in zonas}, maximos


def reparto_vecinal():
    zonas = E.zonas_ordenadas()
    total = float([r["monto"] for r in E.leer("data/baseline_2025.csv")
                   if r["clave"] == "obra_publica_vecinal_anio4"][0])
    need, maximos = indice_de_necesidad(zonas)
    pob = {z["zona"]: int(z["poblacion"]) for z in zonas}
    sp, sn = sum(pob.values()), sum(need.values())

    filas = []
    for z in zonas:
        n = z["zona"]
        w = PESO_POBLACION * pob[n] / sp + PESO_NECESIDAD * need[n] / sn
        monto = total * w
        filas.append({"zona": n, "poblacion": pob[n],
                      "indice_necesidad": need[n], "peso": w, "monto": monto,
                      "pesos_por_habitante": monto / pob[n]})
    filas.sort(key=lambda f: -f["pesos_por_habitante"])

    ruta = os.path.join(E.DATA, "reparto_vecinal_por_zona.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Reparto de la partida vecinal: el %d%%%% de la obra pública del\n"
                % (SHARE_OBRA_VECINAL * 100))
        f.write("# año 4, o sea %s pesos de diciembre de 2025.\n"
                % E.numero(total, 2))
        f.write("# Peso = %d%% por población + %d%% por índice de necesidad.\n"
                % (PESO_POBLACION * 100, PESO_NECESIDAD * 100))
        f.write("# El índice promedia %d indicadores, cada uno dividido por su\n"
                % len(INDICADORES_NECESIDAD))
        f.write("# máximo entre las seis zonas: %s.\n"
                % ", ".join(INDICADORES_NECESIDAD))
        f.write("# Población en viviendas particulares, %s personas.\n"
                % E.numero(sp))
        w_csv = csv.writer(f)
        w_csv.writerow(["zona", "poblacion"]
                       + ["max_" + k for k in INDICADORES_NECESIDAD]
                       + ["indice_necesidad", "peso_pct", "monto",
                          "pesos_por_habitante", "fuente"])
        for x in filas:
            w_csv.writerow([x["zona"], x["poblacion"]]
                           + [round(maximos[k], 4) for k in INDICADORES_NECESIDAD]
                           + [round(x["indice_necesidad"], 6),
                              round(100 * x["peso"], 4), round(x["monto"], 2),
                              round(x["pesos_por_habitante"], 2),
                              "data/baseline_2025.csv y data/zonas_indicadores.csv"])
    return filas, total


def ex13():
    filas, total = reparto_vecinal()
    fig, ax = E.figura(3.15)
    vals = [f["pesos_por_habitante"] for f in filas]
    colores = [E.BARRANCA if f["zona"] in ("Beccar", "Martinez") else E.RIO
               for f in filas]
    ax.bar(range(len(filas)), vals, width=0.62, color=colores, zorder=3)
    for i, f in enumerate(filas):
        destacar = f["zona"] in ("Beccar", "Martinez")
        ax.annotate(E.numero(f["pesos_por_habitante"]), (i, vals[i]),
                    xytext=(0, 5), textcoords="offset points", ha="center",
                    fontsize=7.4 if destacar else 6.8,
                    color=E.BARRANCA if destacar else E.TINTA,
                    weight="bold")
    ax.set_xticks(range(len(filas)))
    # "Boulogne Sur Mer" no entra en una columna al lado de "Villa Adelina":
    # los nombres largos van partidos en dos lineas.
    ax.set_xticklabels([E.dos_lineas(E.zona_bonita(f["zona"])) for f in filas],
                       fontsize=7.2, linespacing=1.25)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylim(0, max(vals) * 1.2)
    ax.set_ylabel("pesos de dic-2025 por habitante", fontsize=6.8)
    E.limpiar(ax)
    top, bottom = E.marco(
        fig, "EXHIBIT 13",
              "La partida vecinal reparte casi el doble por vecino en Beccar que en Martínez",
              "Reparto de los %s millones del año 4. Mitad por población y "
              "mitad por un índice que promedia NBI, cloacas, gas de red y "
              "hacinamiento." % E.numero(total / 1e6),
        "data/reparto_vecinal_por_zona.csv, calculado de "
               "data/baseline_2025.csv y data/zonas_indicadores.csv")
    return E.guardar(fig, "EXHIBIT_13_reparto_vecinal",
                     dict(left=0.125, right=0.985, top=top, bottom=bottom))


def _rotulo_de_tramo(fig, ax, texto, x0, x1, y, color_dentro, color_afuera,
                     pegado_a_la_derecha=False):
    """
    Escribe el rotulo centrado dentro del tramo si entra, y si no entra lo
    saca a la derecha del tramo.

    Se MIDE, no se supone: el tramo del año 1 es el 12,5% de la barra y el
    texto es mas ancho que eso, asi que centrado se derramaba hacia la
    izquierda encima del rotulo "Año 1" del eje. El del año 4 es el 50% y ahi
    entra holgado. La misma regla sirve para los dos y para cualquier valor
    que traiga el modelo mañana.
    """
    from matplotlib.patheffects import withStroke
    if pegado_a_la_derecha:
        ax.annotate(texto, (x1, y), xytext=(-6, 0),
                    textcoords="offset points", ha="right", va="center",
                    fontsize=6.6, color=color_dentro, weight="bold", zorder=6)
        return False
    t = ax.annotate(texto, ((x0 + x1) / 2.0, y), ha="center", va="center",
                    fontsize=6.6, color=color_dentro, weight="bold", zorder=6)
    fig.canvas.draw()
    caja = t.get_window_extent(renderer=fig.canvas.get_renderer())
    px0 = ax.transData.transform((x0, y))[0]
    px1 = ax.transData.transform((x1, y))[0]
    if caja.width <= (px1 - px0) - 8:
        return False
    t.remove()
    ax.annotate(texto, (x1, y), xytext=(5, 0),
                textcoords="offset points", ha="left", va="center",
                fontsize=6.6, color=color_afuera, weight="bold", zorder=6,
                path_effects=[withStroke(linewidth=2.2, foreground=E.PAPEL)])
    return True


def ex14():
    """Obra pública: cuanto deciden los vecinos en el año 1 y en el año 4."""
    b = {r["clave"]: float(r["monto"]) for r in E.leer("data/baseline_2025.csv")}
    obra = b["obra_publica_total"]
    vecinal4 = b["obra_publica_vecinal_anio4"]
    # La rampa del programa es de cuatro anios, asi que el anio 1 lleva un
    # cuarto del objetivo. Sale del modelo, no de un numero elegido.
    vecinal1 = vecinal4 / 4

    fig, ax = E.figura(2.85)
    for i, (etiqueta, v) in enumerate((("Año 1", vecinal1), ("Año 4", vecinal4))):
        ax.barh([i], [v / 1e6], height=0.42, color=E.RIO, zorder=4)
        ax.barh([i], [(obra - v) / 1e6], left=v / 1e6, height=0.42,
                color=E.CAL, zorder=3)
        afuera = _rotulo_de_tramo(
            fig, ax, "deciden los vecinos\n%s M   %s"
            % (E.numero(v / 1e6), E.pct(100 * v / obra, 1)),
            0, v / 1e6, i, E.PAPEL, E.RIO)
        # Si el rotulo azul tuvo que salirse del tramo, el gris se corre al
        # extremo derecho para dejarle lugar en vez de quedar centrado encima.
        _rotulo_de_tramo(fig, ax, "decide el Ejecutivo   %s M   %s"
                         % (E.numero((obra - v) / 1e6),
                            E.pct(100 * (obra - v) / obra, 1)),
                         v / 1e6, obra / 1e6, i, E.TINTA, E.TINTA,
                         pegado_a_la_derecha=afuera)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Año 1", "Año 4"], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, obra / 1e6 * 1.01)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlabel("millones de pesos de diciembre de 2025", fontsize=6.8)
    E.limpiar(ax, grilla=None)
    ax.spines["bottom"].set_visible(True)
    top, bottom = E.marco(
        fig, "EXHIBIT 14",
              "En el año 4, la mitad de la obra pública la deciden las comisiones vecinales",
              "Sobre la obra pública ejecutada en 2025: %s millones. Es "
              "reasignación de quien decide, no gasto nuevo."
              % E.numero(obra / 1e6),
        "data/baseline_2025.csv, bienes de uso devengados en 2025")
    return E.guardar(fig, "EXHIBIT_14_obra_publica_vecinal",
                     dict(left=0.085, right=0.945, top=top, bottom=bottom))


# --------------------------------------------------------------------------
# Los mapas
# --------------------------------------------------------------------------
#
# Rampa secuencial de PAPEL a BARRANCA. Secuencial y no divergente porque el
# NBI no tiene un centro natural: no hay un "bien" y un "mal" a los lados de
# cero, hay más y menos carencia. Una rampa divergente inventaria un punto
# medio que no existe.

CRS_METRICO = "EPSG:32721"


def _barra_escala(ax, geo, metros=2000):
    """Barra de escala en metros. Un mapa sin escala no se puede auditar."""
    x0, y0, x1, y1 = geo.total_bounds
    ancho = x1 - x0
    bx = x0 + ancho * 0.035
    by = y0 + (y1 - y0) * 0.045
    ax.plot([bx, bx + metros], [by, by], color=E.TINTA, linewidth=2.2,
            solid_capstyle="butt", zorder=8)
    ax.text(bx + metros / 2, by + (y1 - y0) * 0.012,
            "%s km" % E.numero(metros / 1000, 0), ha="center", va="bottom",
            fontsize=6, color=E.TINTA)


def _norte(ax, geo):
    x0, y0, x1, y1 = geo.total_bounds
    nx = x1 - (x1 - x0) * 0.045
    ny = y0 + (y1 - y0) * 0.055
    alto = (y1 - y0) * 0.075
    ax.annotate("", xy=(nx, ny + alto), xytext=(nx, ny),
                arrowprops=dict(arrowstyle="-|>", color=E.TINTA, linewidth=1.1),
                zorder=8)
    ax.text(nx, ny + alto + (y1 - y0) * 0.012, "N", ha="center", va="bottom",
            fontsize=6.5, color=E.TINTA, weight="bold")


def _leyenda_rampa(fig, vmin, vmax, etiqueta, y, x=0.035, ancho=0.30,
                   alto=0.016):
    """
    Barra de color horizontal, sin colorbar de matplotlib.

    La 'y' la manda quien llama y sale de marco(): antes estaba clavada en
    0.905, o sea adentro del bloque de cabecera, y la bajada le pasaba por
    encima. Ahora se apoya debajo de la cabecera, dentro del area del mapa,
    donde el partido no dibuja nada porque es una franja diagonal.

    Va a la IZQUIERDA. A la derecha el partido llega hasta arriba de todo y el
    numero de la punta izquierda de la barra quedaba escrito sobre el contorno.
    """
    import numpy as np
    cax = fig.add_axes([x, y, ancho, alto])
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    cax.imshow(grad, aspect="auto", cmap=E.rampa(), origin="lower")
    cax.set_xticks([]); cax.set_yticks([])
    for lado in cax.spines.values():
        lado.set_color(E.TINTA); lado.set_linewidth(0.5)
    fig.text(x, y - 0.010, E.pct(vmin, 1), fontsize=6, color=E.TINTA,
             ha="left", va="top")
    fig.text(x + ancho, y - 0.010, E.pct(vmax, 1), fontsize=6, color=E.TINTA,
             ha="right", va="top")
    fig.text(x + ancho / 2, y + alto + 0.005, etiqueta, fontsize=6.2,
             color=E.TINTA, ha="center", va="bottom")


def _cajas_de_figura(fig, salvo=()):
    """Las cajas de los textos ya dibujados en la figura, en pixeles."""
    import matplotlib.text
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    cajas = []
    for t in fig.findobj(matplotlib.text.Text):
        if t in salvo or not t.get_visible() or not (t.get_text() or "").strip():
            continue
        ejes = getattr(t, "axes", None)
        if ejes is not None and not getattr(ejes, "axison", True):
            if t in list(ejes.get_xticklabels()) + list(ejes.get_yticklabels()):
                continue
        try:
            c = E.caja_de_texto(t, ren)
        except Exception:
            continue
        if c.width > 0 and c.height > 0:
            cajas.append(c)
    return cajas


def _etiquetas_sin_pisarse(fig, ax, items, geo, fontsize=7.6, ocupadas=None):
    """
    Coloca las etiquetas de zona en el centro de cada poligono y, cuando dos
    quedan encima, aparta la que llega despues y le deja una linea guia.

    Centrar siempre en el poligono es lo correcto mientras las zonas sean
    parejas; en cuanto dos comparten frontera y una es angosta, o hay una
    llamada al lado, las etiquetas se tocan. La regla: se mide, y solo se mueve
    la que hace falta.

    Se prueban ocho direcciones a tres distancias, empezando por la que saca la
    etiqueta del centro del partido. Antes se probaba una sola direccion y si
    esa estaba tomada la etiqueta no se dibujaba: en el mapa por radio
    desaparecian "Beccar" y "San Isidro", que es peor que un solape. Si
    despues de las 32 pruebas no hay lugar, se dibuja igual en su sitio
    original y el verificador de colisiones lo denuncia.
    """
    import math
    from matplotlib.patheffects import withStroke
    x0, y0, x1, y1 = geo.total_bounds
    ancho, alto = x1 - x0, y1 - y0
    # Las cajas que ya estan en la figura (cabecera, pie, barra de color,
    # llamadas) cuentan como ocupadas: una etiqueta de zona no puede caer
    # encima de ellas tampoco.
    puestos = list(ocupadas or [])
    # De mayor a menor area: las grandes se quedan en su lugar.
    items = sorted(items, key=lambda it: -it["area"])
    for it in items:
        # Direccion de salida: la que aleja del centro del partido. Las otras
        # siete se prueban despues, en orden de cercania a esa.
        base = math.atan2(it["y"] - (y0 + y1) / 2, it["x"] - (x0 + x1) / 2)
        vueltas = [0, 1, -1, 2, -2, 3, -3, 4]
        intentos = [(0.0, 0.0)]
        for r in (0.055, 0.10, 0.155, 0.215):
            for k in vueltas:
                a = base + k * math.pi / 4
                intentos.append((math.cos(a) * ancho * r,
                                 math.sin(a) * alto * r))
        fig.canvas.draw()
        ren = fig.canvas.get_renderer()
        for k, (dx, dy) in enumerate(intentos):
            px, py = it["x"] + dx, it["y"] + dy
            movida = k > 0
            t = ax.annotate(
                it["texto"], xy=(it["x"], it["y"]), xytext=(px, py),
                textcoords="data", ha="center", va="center",
                fontsize=fontsize, color=it["color"], weight="bold",
                zorder=6, linespacing=1.35,
                arrowprops=(dict(arrowstyle="-", color=E.TINTA, linewidth=0.7,
                                 alpha=0.75, shrinkA=1, shrinkB=1)
                            if movida else None),
                path_effects=[withStroke(linewidth=4.2,
                                         foreground=it["halo"])])
            # Una Annotation no sabe donde cae su texto hasta que se le
            # actualizan las posiciones: antes de eso devuelve la caja apoyada
            # en el punto de destino de la flecha y no en el del texto. Medir
            # sin esto daba por buenas posiciones que despues se pisaban.
            t.update_positions(ren)
            caja = E.caja_de_texto(t, ren)
            if not any(caja.overlaps(c) for c in puestos):
                puestos.append(caja)
                break
            if k < len(intentos) - 1:
                t.remove()
            else:
                # Ultimo recurso: se dibuja igual. Un nombre de zona que falta
                # es peor que un nombre de zona apretado.
                puestos.append(caja)
    fig.canvas.draw()


def ex15():
    """EL MAPA. Las seis zonas coloreadas por NBI."""
    import geopandas as gpd
    from matplotlib.patheffects import withStroke

    z = gpd.read_file(os.path.join(E.DATA, "zonas_propuestas_sanisidro.geojson"))
    z = z.to_crs(CRS_METRICO)
    z["pct_nbi"] = z["pct_nbi"].astype(float)
    vmin, vmax = z["pct_nbi"].min(), z["pct_nbi"].max()

    fig, ax = E.figura(4.6)
    z.plot(ax=ax, column="pct_nbi", cmap=E.rampa(), vmin=vmin, vmax=vmax,
           edgecolor=E.PAPEL, linewidth=1.6, zorder=3)
    z.dissolve().boundary.plot(ax=ax, edgecolor=E.TINTA, linewidth=1.1, zorder=4)

    items = []
    for _, r in z.iterrows():
        p = r.geometry.representative_point()
        prop = (r["pct_nbi"] - vmin) / (vmax - vmin) if vmax > vmin else 0
        items.append({
            "x": p.x, "y": p.y, "area": r.geometry.area,
            "texto": "%s\n%s NBI" % (E.zona_bonita(r["zona"]),
                                     E.pct(r["pct_nbi"], 2)),
            "color": E.PAPEL if prop > 0.55 else E.TINTA,
            "halo": E.TINTA if prop > 0.55 else E.PAPEL})

    E.apagar_ejes(ax)
    E.sin_offset(ax)
    _barra_escala(ax, z)
    _norte(ax, z)
    top, bottom = E.marco(
        fig, "EXHIBIT 15",
              "Las seis zonas vecinales de San Isidro",
              "Coloreadas por porcentaje de hogares con necesidades básicas "
              "insatisfechas. El partido entero promedia %s."
              % E.pct(_nbi_del_partido(), 2),
        FUENTE_CENSO,
          "Los límites de las zonas son propios, no oficiales. Lo único oficial "
          "es la geometría de los 360 radios censales del INDEC y los seis "
          "puntos BAHRA de las localidades. Ver data/METODOLOGIA_ZONAS.md.")
    _leyenda_rampa(fig, vmin, vmax, "% de hogares con NBI", y=top - 0.055)
    # El area del mapa se fija ANTES de colocar los nombres. Si se movia
    # despues, cada etiqueta cambiaba de lugar y de tamaño relativo y el
    # trabajo de medirlas para que no se pisaran se perdia entero.
    fig.subplots_adjust(left=0.02, right=0.98, top=top, bottom=bottom)
    _etiquetas_sin_pisarse(fig, ax, items, z, ocupadas=_cajas_de_figura(fig))
    return E.guardar(fig, "EXHIBIT_15_mapa_zonas_nbi")


def ex16():
    """Mapa por radio censal, con el conglomerado de la fracción 32."""
    import geopandas as gpd
    from matplotlib.patheffects import withStroke

    radios = gpd.read_file(os.path.join(E.DATA,
                                        "radios_censales_sanisidro.geojson"))
    radios = radios.to_crs(CRS_METRICO)
    censo = {r["radio_id"]: r for r in E.leer("data/censo2022_sanisidro_por_radio.csv")}
    zona = {r["radio_id"]: r["zona"]
            for r in E.leer("data/zonas_asignacion_radios.csv")}

    def nbi(rid):
        f = censo.get(rid)
        if not f or not f.get("hogares_nbi__total"):
            return None
        t = float(f["hogares_nbi__total"])
        return 100 * float(f["hogares_nbi__si"]) / t if t else None

    radios["pct_nbi"] = [nbi(r) for r in radios["radio_id"]]
    radios["zona"] = [zona.get(r, "") for r in radios["radio_id"]]
    con = radios[radios["pct_nbi"].notna()]
    vmin, vmax = con["pct_nbi"].min(), con["pct_nbi"].max()

    # El conglomerado critico: los radios de la fraccion 32 que están en el
    # decil superior de NBI del partido.
    umbral = con["pct_nbi"].quantile(0.9)
    critico = con[(con["fraccion"] == "32") & (con["pct_nbi"] >= umbral)]

    fig, ax = E.figura(4.6)
    radios.plot(ax=ax, column="pct_nbi", cmap=E.rampa(), vmin=vmin, vmax=vmax,
                edgecolor=E.PAPEL, linewidth=0.25, zorder=3,
                missing_kwds={"color": E.CAL})
    z = gpd.read_file(os.path.join(E.DATA, "zonas_propuestas_sanisidro.geojson"))
    z = z.to_crs(CRS_METRICO)
    z.boundary.plot(ax=ax, edgecolor=E.TINTA, linewidth=0.8, zorder=4,
                    alpha=0.55)
    critico.dissolve().boundary.plot(ax=ax, edgecolor=E.TINTA, linewidth=2.0,
                                     zorder=6)

    E.apagar_ejes(ax)
    E.sin_offset(ax)
    _barra_escala(ax, radios)
    _norte(ax, radios)
    top, bottom = E.marco(
        fig, "EXHIBIT 16",
              "La carencia no está repartida: esta concentrada en nueve radios",
              "Los 360 radios censales del partido. El contorno grueso es el "
              "conglomerado de la fracción 32, dentro de Beccar.",
        FUENTE_CENSO,
          "Los nueve radios se identifican por código y fracción censal, nunca "
          "por nombre de barrio: los barrios no tienen geometría oficial.")
    _leyenda_rampa(fig, vmin, vmax, "% de hogares con NBI, por radio censal",
                   y=top - 0.055)
    # El area del mapa se fija ANTES de la llamada y de los nombres de zona:
    # todo eso va en coordenadas de dato y se corre si el eje se mueve despues.
    fig.subplots_adjust(left=0.02, right=0.98, top=top, bottom=bottom)

    # La llamada de la fracción 32 va DESPUES de la cabecera y de la barra de
    # color, y se apoya en el rincon de abajo a la derecha, que es el unico
    # pedazo grande de lienzo vacio: el partido es una franja en diagonal.
    # Pegada al conglomerado no entra por ningun lado, porque ahi al lado
    # estan "Beccar" y "San Isidro", las dos zonas mas angostas del partido.
    p = critico.dissolve().geometry.representative_point().iloc[0]
    x0, y0, x1, y1 = radios.total_bounds
    llamada = ax.annotate(
        "fracción censal 32\n%d radios, %s hab\nel peor NBI del partido"
        % (len(critico), E.numero(sum(int(censo[r]["poblacion_sexo__total"])
                                      for r in critico["radio_id"]))),
        (p.x, p.y), xytext=(x0 + (x1 - x0) * 0.99, y0 + (y1 - y0) * 0.34),
        ha="right",
        fontsize=7, color=E.TINTA, weight="bold", va="center",
        linespacing=1.35, zorder=7,
        arrowprops=dict(arrowstyle="-", color=E.TINTA, linewidth=0.9,
                        shrinkA=1, shrinkB=1),
        path_effects=[withStroke(linewidth=3.4, foreground=E.PAPEL)])

    # Los nombres de zona se colocan al final y esquivan todo lo anterior.
    items = [{"x": r.geometry.representative_point().x,
              "y": r.geometry.representative_point().y,
              "area": r.geometry.area, "texto": E.zona_bonita(r["zona"]),
              "color": E.TINTA, "halo": E.PAPEL} for _, r in z.iterrows()]
    _etiquetas_sin_pisarse(fig, ax, items, radios, fontsize=6.6,
                           ocupadas=_cajas_de_figura(fig))
    return E.guardar(fig, "EXHIBIT_16_mapa_radios_nbi")
