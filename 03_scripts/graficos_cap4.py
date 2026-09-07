#!/usr/bin/env python3
"""Capitulo 4 - El mecanismo. Exhibits 13 a 16, incluidos los dos mapas."""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E
import matplotlib.pyplot as plt

FUENTE_CENSO = ("INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022, "
                "procesado con Redatam 7; zonas propias sobre radios censales")

# Regla de reparto de la partida vecinal. Mitad por poblacion y mitad por
# hogares con NBI: la mitad reconoce que cada vecino cuenta igual y la otra
# mitad que no todas las zonas arrancan del mismo lugar. Es una REGLA, no un
# reparto negociado, y esta escrita para que cualquiera la recalcule.
PESO_POBLACION = 0.5
PESO_NBI = 0.5


def reparto_vecinal():
    zonas = E.zonas_ordenadas()
    total = float([r["monto"] for r in E.leer("data/baseline_2025.csv")
                   if r["clave"] == "obra_publica_vecinal_anio4"][0])
    pob = {z["zona"]: int(z["poblacion"]) for z in zonas}
    nbi = {z["zona"]: int(z["hogares"]) * float(z["pct_nbi"]) / 100 for z in zonas}
    sp, sn = sum(pob.values()), sum(nbi.values())
    filas = []
    for z in zonas:
        n = z["zona"]
        parte = PESO_POBLACION * pob[n] / sp + PESO_NBI * nbi[n] / sn
        monto = total * parte
        filas.append({"zona": n, "poblacion": pob[n],
                      "hogares_con_nbi": round(nbi[n]),
                      "participacion": parte, "monto": monto,
                      "pesos_por_habitante": monto / pob[n]})
    filas.sort(key=lambda f: -f["pesos_por_habitante"])
    ruta = os.path.join(E.DATA, "reparto_vecinal_por_zona.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Reparto de la partida vecinal (50%% de la obra publica del\n")
        f.write("# anio 4) entre las seis zonas. Regla: %d%% por poblacion y\n"
                % (PESO_POBLACION * 100))
        f.write("# %d%% por hogares con NBI. Pesos de diciembre de 2025.\n"
                % (PESO_NBI * 100))
        w = csv.writer(f)
        w.writerow(["zona", "poblacion", "hogares_con_nbi", "participacion_pct",
                    "monto", "pesos_por_habitante", "fuente"])
        for x in filas:
            w.writerow([x["zona"], x["poblacion"], x["hogares_con_nbi"],
                        round(100 * x["participacion"], 4), round(x["monto"], 2),
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
    ax.set_xticklabels([f["zona"] for f in filas], fontsize=7.2)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylim(0, max(vals) * 1.2)
    ax.set_ylabel("pesos de dic-2025 por habitante", fontsize=6.8)
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 13",
              "La partida vecinal reparte casi el doble por vecino en Beccar que en Martinez",
              "Reparto de los %s millones del anio 4. Regla: mitad por "
              "poblacion, mitad por hogares con NBI." % E.numero(total / 1e6))
    E.pie(fig, "data/reparto_vecinal_por_zona.csv, calculado de "
               "data/baseline_2025.csv y data/zonas_indicadores.csv")
    return E.guardar(fig, "EXHIBIT_13_reparto_vecinal",
                     dict(left=0.085, right=0.985, top=0.685, bottom=0.13))


def ex14():
    """Obra publica: cuanto deciden los vecinos en el anio 1 y en el anio 4."""
    b = {r["clave"]: float(r["monto"]) for r in E.leer("data/baseline_2025.csv")}
    obra = b["obra_publica_total"]
    vecinal4 = b["obra_publica_vecinal_anio4"]
    # La rampa del programa es de cuatro anios, asi que el anio 1 lleva un
    # cuarto del objetivo. Sale del modelo, no de un numero elegido.
    vecinal1 = vecinal4 / 4

    fig, ax = E.figura(2.85)
    for i, (etiqueta, v) in enumerate((("Ano 1", vecinal1), ("Ano 4", vecinal4))):
        ax.barh([i], [v / 1e6], height=0.42, color=E.RIO, zorder=4)
        ax.barh([i], [(obra - v) / 1e6], left=v / 1e6, height=0.42,
                color=E.CAL, zorder=3)
        ax.annotate("deciden los vecinos\n%s M   %s"
                    % (E.numero(v / 1e6), E.pct(100 * v / obra, 1)),
                    (v / 2e6, i), ha="center", va="center", fontsize=6.6,
                    color=E.PAPEL, weight="bold")
        ax.annotate("decide el Ejecutivo   %s M   %s"
                    % (E.numero((obra - v) / 1e6), E.pct(100 * (obra - v) / obra, 1)),
                    ((v + (obra - v) / 2) / 1e6, i), ha="center", va="center",
                    fontsize=6.6, color=E.TINTA)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Ano 1", "Ano 4"], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, obra / 1e6 * 1.01)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlabel("millones de pesos de diciembre de 2025", fontsize=6.8)
    E.limpiar(ax, grilla=None)
    ax.spines["bottom"].set_visible(True)
    E.titular(fig, "EXHIBIT 14",
              "En el ano 4, la mitad de la obra publica la deciden las comisiones vecinales",
              "Sobre la obra publica ejecutada en 2025: %s millones. Es "
              "reasignacion de quien decide, no gasto nuevo."
              % E.numero(obra / 1e6))
    E.pie(fig, "data/baseline_2025.csv, bienes de uso devengados en 2025")
    return E.guardar(fig, "EXHIBIT_14_obra_publica_vecinal",
                     dict(left=0.075, right=0.985, top=0.68, bottom=0.155))


# --------------------------------------------------------------------------
# Los mapas
# --------------------------------------------------------------------------
#
# Rampa secuencial de PAPEL a BARRANCA. Secuencial y no divergente porque el
# NBI no tiene un centro natural: no hay un "bien" y un "mal" a los lados de
# cero, hay mas y menos carencia. Una rampa divergente inventaria un punto
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


def _leyenda_rampa(fig, vmin, vmax, etiqueta, x=0.70, y=0.905, ancho=0.26,
                   alto=0.018):
    """Barra de color horizontal arriba a la derecha, sin colorbar de matplotlib."""
    import numpy as np
    cax = fig.add_axes([x, y, ancho, alto])
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    cax.imshow(grad, aspect="auto", cmap=E.rampa(), origin="lower")
    cax.set_xticks([]); cax.set_yticks([])
    for lado in cax.spines.values():
        lado.set_color(E.TINTA); lado.set_linewidth(0.5)
    fig.text(x, y - 0.022, E.pct(vmin, 1), fontsize=6, color=E.TINTA,
             ha="left", va="top")
    fig.text(x + ancho, y - 0.022, E.pct(vmax, 1), fontsize=6, color=E.TINTA,
             ha="right", va="top")
    fig.text(x + ancho / 2, y + alto + 0.006, etiqueta, fontsize=6.2,
             color=E.TINTA, ha="center", va="bottom")


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

    for _, r in z.iterrows():
        p = r.geometry.representative_point()
        # Texto claro sobre las zonas oscuras y oscuro sobre las claras.
        prop = (r["pct_nbi"] - vmin) / (vmax - vmin) if vmax > vmin else 0
        color = E.PAPEL if prop > 0.55 else E.TINTA
        halo = E.TINTA if prop > 0.55 else E.PAPEL
        ax.text(p.x, p.y, "%s\n%s NBI" % (r["zona"], E.pct(r["pct_nbi"], 2)),
                ha="center", va="center", fontsize=7.6, color=color,
                weight="bold", zorder=6, linespacing=1.35,
                path_effects=[withStroke(linewidth=2.0, foreground=halo)])

    ax.set_axis_off()
    _barra_escala(ax, z)
    _norte(ax, z)
    _leyenda_rampa(fig, vmin, vmax, "% de hogares con NBI")
    E.titular(fig, "EXHIBIT 15",
              "Las seis zonas vecinales de San Isidro",
              "Coloreadas por porcentaje de hogares con necesidades basicas "
              "insatisfechas. El partido entero promedia 3,16%.")
    E.pie(fig, FUENTE_CENSO,
          "Los limites de las zonas son propios, no oficiales. Lo unico oficial "
          "es la geometria de los 360 radios censales del INDEC y los seis "
          "puntos BAHRA de las localidades. Ver data/METODOLOGIA_ZONAS.md.")
    return E.guardar(fig, "EXHIBIT_15_mapa_zonas_nbi",
                     dict(left=0.02, right=0.98, top=0.865, bottom=0.055))


def ex16():
    """Mapa por radio censal, con el conglomerado de la fraccion 32."""
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

    # El conglomerado critico: los radios de la fraccion 32 que estan en el
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

    p = critico.dissolve().geometry.representative_point().iloc[0]
    x0, y0, x1, y1 = radios.total_bounds
    ax.annotate("fraccion censal 32\n%d radios, %s hab\nel peor NBI del partido"
                % (len(critico),
                   E.numero(sum(int(censo[r]["poblacion_sexo__total"])
                                for r in critico["radio_id"]))),
                (p.x, p.y), xytext=(p.x + (x1 - x0) * 0.24, p.y + (y1 - y0) * 0.14),
                fontsize=7, color=E.TINTA, weight="bold", ha="left",
                linespacing=1.35, zorder=7,
                arrowprops=dict(arrowstyle="-", color=E.TINTA, linewidth=0.9))

    for _, r in z.iterrows():
        q = r.geometry.representative_point()
        ax.text(q.x, q.y, r["zona"], ha="center", va="center", fontsize=6.6,
                color=E.TINTA, alpha=0.85, zorder=5,
                path_effects=[withStroke(linewidth=2.2, foreground=E.PAPEL)])

    ax.set_axis_off()
    _barra_escala(ax, radios)
    _norte(ax, radios)
    _leyenda_rampa(fig, vmin, vmax, "% de hogares con NBI, por radio censal")
    E.titular(fig, "EXHIBIT 16",
              "La carencia no esta repartida: esta concentrada en nueve radios",
              "Los 360 radios censales del partido. El contorno grueso es el "
              "conglomerado de la fraccion 32, dentro de Beccar.")
    E.pie(fig, FUENTE_CENSO,
          "Los nueve radios se identifican por codigo y fraccion censal, nunca "
          "por nombre de barrio: los barrios no tienen geometria oficial.")
    return E.guardar(fig, "EXHIBIT_16_mapa_radios_nbi",
                     dict(left=0.02, right=0.98, top=0.865, bottom=0.055))
