#!/usr/bin/env python3
"""Capitulo 1 - Diagnostico. Exhibits 01 a 05."""

import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E
import matplotlib.pyplot as plt

FUENTE_SERIE = ("elaboracion propia sobre rendiciones de cuentas y ejecucion "
                "presupuestaria del Municipio de San Isidro, deflactado con "
                "IPC INDEC empalmado (data/serie_gastos_comparable.csv)")
FUENTE_CENSO = ("INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022, "
                "procesado con Redatam 7 (data/zonas_indicadores.csv)")
FUENTE_PBA = ("Ministerio de Hacienda y Finanzas de la Provincia de Buenos "
              "Aires, transferencias a municipios 2021-2025")


def ex01():
    """Gasto real 2010-2025. Los anios sin dato se ven vacios."""
    filas = E.leer("data/serie_gastos_comparable.csv")
    anios = [int(f["anio"]) for f in filas]
    vals = [float(f["monto_constante_dic2025"]) / 1e6 if f["monto_constante_dic2025"]
            else None for f in filas]

    fig, ax = E.figura(3.35)
    con = [(a, v) for a, v in zip(anios, vals) if v is not None]
    sin = [a for a, v in zip(anios, vals) if v is None]

    ax.bar([a for a, _ in con], [v for _, v in con], width=0.68,
           color=E.RIO, zorder=3)
    # Los anios sin dato: banda vertical en CAL y la palabra, para que el hueco
    # se vea como hueco y no como un cero.
    tope = max(v for _, v in con)
    for a in sin:
        ax.bar([a], [tope], width=0.68, color=E.CAL, zorder=2)
        ax.text(a, tope * 0.5, "sin\nrendicion", ha="center", va="center",
                fontsize=5.6, color=E.TINTA, alpha=0.55, rotation=90)

    maxi = max(con, key=lambda x: x[1])
    mini = min(con, key=lambda x: x[1])
    for (a, v), etiqueta, color in ((maxi, "maximo", E.TINTA),
                                    (mini, "minimo", E.BARRANCA)):
        ax.bar([a], [v], width=0.68, color=color, zorder=4)
        ax.annotate("%s %d\n%s M" % (etiqueta, a, E.numero(v)),
                    (a, v), xytext=(0, 7), textcoords="offset points",
                    ha="center", fontsize=6.8, color=color, weight="bold")

    ax.set_ylim(0, tope * 1.22)
    ax.set_xticks(anios)
    ax.set_xticklabels([str(a) for a in anios], fontsize=6.5)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylabel("millones de pesos de diciembre de 2025", fontsize=6.8)
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 01",
              "El gasto municipal real cae 34,9% entre 2017 y 2024",
              "Gasto total en pesos constantes. Un solo concepto en todos los "
              "anios: gastos corrientes mas de capital, sin aplicaciones financieras.")
    E.pie(fig, FUENTE_SERIE,
          "2013, 2018 y 2023 no tienen rendicion de cuentas publicada. No se "
          "interpolaron: el hueco queda a la vista.")
    return E.guardar(fig, "EXHIBIT_01_gasto_real_2010_2025",
                     dict(left=0.075, right=0.985, top=0.70, bottom=0.155))


def ex02():
    """Las seis zonas, cuatro indicadores, de peor a mejor."""
    zonas = E.zonas_ordenadas()
    series = [("% hogares con NBI", "pct_nbi", E.RIO),
              ("% sin cloaca", "pct_sin_cloaca", E.BARRANCA),
              ("% sin gas de red", "pct_sin_gas_red", E.TINTA),
              ("% con hacinamiento", "pct_hacinamiento", E.AMBAR)]
    n = len(series)
    ancho = 0.78 / n
    x = list(range(len(zonas)))

    fig, ax = E.figura(3.35)
    for i, (etiqueta, col, color) in enumerate(series):
        pos = [xx - 0.39 + ancho * (i + 0.5) for xx in x]
        vals = [float(z[col]) for z in zonas]
        ax.bar(pos, vals, width=ancho * 0.9, color=color, zorder=3)
        # Etiqueta la serie sobre la primera zona, sin leyenda flotante.
        ax.annotate(etiqueta, (pos[0], vals[0]), xytext=(0, 5),
                    textcoords="offset points", ha="center", fontsize=6.2,
                    color=color, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([z["zona"] for z in zonas], fontsize=7.2)
    ax.yaxis.set_major_formatter(E.eje_pct())
    ax.set_ylim(0, max(float(z["pct_sin_gas_red"]) for z in zonas) * 1.28)
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 02",
              "Boulogne y Beccar concentran toda la carencia del partido",
              "Cuatro indicadores por zona, ordenadas de peor a mejor por NBI. "
              "El NBI del partido es 3,16%.")
    E.pie(fig, FUENTE_CENSO)
    return E.guardar(fig, "EXHIBIT_02_zonas_carencias",
                     dict(left=0.06, right=0.985, top=0.70, bottom=0.13))


def ex03():
    """El espejo del 02: educacion universitaria, mismo orden."""
    zonas = E.zonas_ordenadas()
    vals = [float(z["pct_edu_universitaria_completa_o_mas"]) for z in zonas]
    fig, ax = E.figura(3.0)
    ax.bar(range(len(zonas)), vals, width=0.62, color=E.RIO, zorder=3)
    for i, v in enumerate(vals):
        ax.annotate(E.pct(v, 1), (i, v), xytext=(0, 4),
                    textcoords="offset points", ha="center", fontsize=7,
                    color=E.TINTA, weight="bold")
    ax.set_xticks(range(len(zonas)))
    ax.set_xticklabels([z["zona"] for z in zonas], fontsize=7.2)
    ax.yaxis.set_major_formatter(E.eje_pct())
    ax.set_ylim(0, max(vals) * 1.22)
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 03",
              "El mismo orden, dado vuelta: donde falta todo, tampoco hay titulo",
              "Poblacion con universidad completa o mas, por zona. Mismo orden "
              "que el exhibit 02, de peor a mejor en NBI.")
    E.pie(fig, FUENTE_CENSO)
    return E.guardar(fig, "EXHIBIT_03_educacion_por_zona",
                     dict(left=0.06, right=0.985, top=0.685, bottom=0.145))


def ex04():
    """La participacion de cuatro municipios del norte, 2021-2025."""
    filas = [f for f in E.leer("data/coparticipacion_comparada.csv")
             if int(f["meses"]) == 12]
    anios = sorted({int(f["anio"]) for f in filas})
    munis = ["SAN ISIDRO", "TIGRE", "VICENTE LOPEZ", "SAN FERNANDO"]
    colores = {"SAN ISIDRO": E.RIO, "TIGRE": E.BARRANCA,
               "VICENTE LOPEZ": E.TINTA, "SAN FERNANDO": E.AMBAR}
    bonito = {"SAN ISIDRO": "San Isidro", "TIGRE": "Tigre",
              "VICENTE LOPEZ": "Vicente Lopez", "SAN FERNANDO": "San Fernando"}

    fig, ax = E.figura(3.3)
    for m in munis:
        ys = [float(f["participacion_pct"]) for a in anios
              for f in filas if int(f["anio"]) == a and f["municipio"] == m]
        ancho = 2.1 if m == "SAN ISIDRO" else 1.1
        ax.plot(anios, ys, color=colores[m], linewidth=ancho, zorder=3,
                marker="o", markersize=2.6 if m == "SAN ISIDRO" else 1.8)
        E.etiqueta_serie(ax, anios[-1], ys[-1],
                         "%s  %s" % (bonito[m], E.pct(ys[-1], 4)),
                         colores[m], dx=6)
        E.etiqueta_serie(ax, anios[0], ys[0], E.pct(ys[0], 4),
                         colores[m], dx=-6, ha="right")

    ax.set_xlim(anios[0] - 0.55, anios[-1] + 1.55)
    ax.set_xticks(anios)
    ax.set_xticklabels([str(a) for a in anios], fontsize=7)
    ax.yaxis.set_major_formatter(E.eje_pct(1))
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 04",
              "Tigre pasa a San Isidro en 2025: el reparto provincial se dio vuelta",
              "Participacion de cada municipio en el total transferido por la "
              "Provincia a los 135 municipios. Anios completos.")
    E.pie(fig, FUENTE_PBA,
          "2026 va con seis meses y queda fuera del grafico. San Isidro cae a "
          "1,6811% y Tigre sube a 1,8370%.")
    return E.guardar(fig, "EXHIBIT_04_coparticipacion_comparada",
                     dict(left=0.085, right=0.80, top=0.70, bottom=0.13))
