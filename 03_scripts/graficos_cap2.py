#!/usr/bin/env python3
"""Capitulo 2 - La gestion. Exhibits 06 y 07."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E

FUENTE_EJEC = ("elaboracion propia sobre la ejecucion presupuestaria "
               "trimestral del Municipio de San Isidro, informes anuales "
               "2024 y 2025")

# Estas tres funciones cambian de contenido entre 2024 y 2025 por
# reclasificacion contable, no porque haya cambiado el gasto. Compararlas seria
# publicar una variacion que no ocurrio.
RECLASIFICADAS = {"TRANSPORTE", "COMERCIO, TURISMO Y OTROS SERVICIOS",
                  "AGUA POTABLE Y ALCANTARILLADO"}


def _anual(anio):
    """Recursos corrientes devengados y percibidos de un ejercicio."""
    dev = per = 0.0
    for r in E.leer("data/ejecucion_recursos.csv"):
        if int(r["anio"]) != anio or r["periodo_tipo"] != "acumulado_anual":
            continue
        if not r["rubro_codigo"].startswith("1."):
            continue
        dev += float(r["devengado"] or 0)
        per += float(r["percibido"] or 0)
    return dev, per


def ex06():
    """Percepcion 2024 contra 2025, con lo no cobrado a la vista."""
    datos = [(a,) + _anual(a) for a in (2024, 2025)]
    fig, ax = E.figura(3.1)
    x = [0, 1]
    for i, (anio, dev, per) in enumerate(datos):
        ax.bar([i], [per / 1e6], width=0.42, color=E.RIO, zorder=3)
        ax.bar([i], [(dev - per) / 1e6], width=0.42, bottom=per / 1e6,
               color=E.CAL, zorder=3)
        ax.bar([i], [(dev - per) / 1e6], width=0.42, bottom=per / 1e6,
               color="none", edgecolor=E.BARRANCA, linewidth=0.9,
               linestyle=(0, (2.5, 1.5)), zorder=4)
        ax.annotate("percibido\n%s M  (%s)" % (E.numero(per / 1e6),
                                               E.pct(100 * per / dev, 2)),
                    (i, per / 2e6), ha="center", va="center", fontsize=6.8,
                    color=E.PAPEL, weight="bold")
        ax.annotate("sin cobrar %s M" % E.numero((dev - per) / 1e6),
                    (i, (per + (dev - per) / 2) / 1e6), ha="center",
                    va="center", fontsize=6.8, color=E.BARRANCA, weight="bold")
        ax.annotate("devengado %s M" % E.numero(dev / 1e6), (i, dev / 1e6),
                    xytext=(0, 5), textcoords="offset points", ha="center",
                    fontsize=7, color=E.TINTA, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(["2024", "2025"], fontsize=9)
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, max(d[1] for d in datos) / 1e6 * 1.16)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylabel("millones de pesos corrientes de cada anio", fontsize=6.8)
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 06",
              "En 2025 quedaron 35.994 millones sin cobrar de lo ya facturado",
              "Recursos corrientes devengados contra percibidos. La franja "
              "punteada es mora: plata que el Municipio tiene derecho a cobrar "
              "y no entro.")
    E.pie(fig, FUENTE_EJEC)
    return E.guardar(fig, "EXHIBIT_06_percepcion_2024_2025",
                     dict(left=0.085, right=0.985, top=0.685, bottom=0.11))


def ex07():
    """Variacion real por funcion, divergente desde cero."""
    defl = {int(r["anio"]): float(r["coef_anual"])
            for r in E.leer("data/deflactor.csv") if r["coef_anual"]}
    por = {}
    for r in E.leer("data/gastos_finalidad_funcion.csv"):
        if r["periodo_tipo"] != "acumulado_anual" or r["nivel"] != "funcion":
            continue
        if not r["devengado"]:
            continue
        anio = int(r["anio"])
        if anio not in (2024, 2025):
            continue
        por.setdefault(r["funcion"], {})[anio] = (float(r["devengado"])
                                                  * defl[anio])
    filas = []
    for funcion, v in por.items():
        if funcion.upper() in RECLASIFICADAS or 2024 not in v or 2025 not in v:
            continue
        if v[2024] <= 0:
            continue
        filas.append((funcion, 100 * (v[2025] / v[2024] - 1)))
    filas.sort(key=lambda x: x[1])

    fig, ax = E.figura(3.6)
    y = range(len(filas))
    colores = [E.RIO if v >= 0 else E.BARRANCA for _, v in filas]
    ax.barh(list(y), [v for _, v in filas], height=0.62, color=colores, zorder=3)
    ax.axvline(0, color=E.TINTA, linewidth=0.8, zorder=4)
    for i, (nombre, v) in enumerate(filas):
        dx = 4 if v >= 0 else -4
        ha = "left" if v >= 0 else "right"
        ax.annotate(E.pct(v, 1), (v, i), xytext=(dx, 0),
                    textcoords="offset points", ha=ha, va="center",
                    fontsize=6.6, color=colores[i], weight="bold")
    ax.set_yticks(list(y))
    ax.set_yticklabels([n.title() for n, _ in filas], fontsize=6.8)
    ax.xaxis.set_major_formatter(E.eje_pct())
    lim = max(abs(v) for _, v in filas) * 1.35
    ax.set_xlim(-lim, lim)
    E.limpiar(ax, grilla="x")
    E.titular(fig, "EXHIBIT 07",
              "Que subio y que bajo en terminos reales entre 2024 y 2025",
              "Variacion real del gasto devengado por funcion, en pesos "
              "constantes de diciembre de 2025.")
    E.pie(fig, FUENTE_EJEC,
          "Se excluyen Transporte, Comercio y Agua potable: cambian de "
          "contenido entre los dos anios por reclasificacion contable, no "
          "porque haya cambiado el gasto.")
    return E.guardar(fig, "EXHIBIT_07_variacion_por_funcion",
                     dict(left=0.235, right=0.975, top=0.735, bottom=0.115))
