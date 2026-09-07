#!/usr/bin/env python3
"""Capitulo 5 - Sectorial. Exhibits 17, 18 y 20. El 19 no se genera."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E

FUENTE_EJEC = ("Municipio de San Isidro, ejecución presupuestaria 2025, "
               "informe anual. Gasto devengado")
FUENTE_CENSO = ("INDEC, Censo Nacional de Población, Hogares y Viviendas 2022, "
                "procesado con Redatam 7")

# Se destacán porque son las dos funciones que el programa señala como
# desatendidas. No se eligen por su valor: están escritas acá y el grafico
# resalta las que coincidan.
DESTACAR = {"ECOLOGIA Y MEDIO AMBIENTE", "AGUA POTABLE Y ALCANTARILLADO"}


def ex17():
    """Gasto por función 2025, ordenado."""
    filas = []
    total = 0.0
    for r in E.leer("data/gastos_finalidad_funcion.csv"):
        if (r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual"
                and r["nivel"] == "funcion" and r["devengado"]):
            filas.append((r["funcion"], float(r["devengado"])))
            total += float(r["devengado"])
    filas.sort(key=lambda x: x[1])

    fig, ax = E.figura(4.0)
    y = range(len(filas))
    colores = [E.BARRANCA if n.upper() in DESTACAR else E.RIO for n, _ in filas]
    ax.barh(list(y), [v / 1e6 for _, v in filas], height=0.66, color=colores,
            zorder=3)
    for i, (nombre, v) in enumerate(filas):
        destacáda = nombre.upper() in DESTACAR
        ax.annotate("%s M   %s" % (E.numero(v / 1e6), E.pct(100 * v / total, 1)),
                    (v / 1e6, i), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=6.4,
                    color=E.BARRANCA if destacáda else E.TINTA,
                    weight="bold" if destacáda else "normal")
    ax.set_yticks(list(y))
    ax.set_yticklabels([E.etiqueta_corta(n, 24) for n, _ in filas],
                       fontsize=6.2, linespacing=1.15)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlim(0, max(v for _, v in filas) / 1e6 * 1.42)
    ax.set_xlabel("millones de pesos devengados en 2025", fontsize=6.8)
    E.limpiar(ax, grilla="x")
    E.titular(fig, "EXHIBIT 17",
              "Ecología y agua potable juntas no llegan al 1,5% del presupuesto",
              "Gasto por función, ejercicio 2025. En BARRANCA las dos "
              "funciónes que el programa señala como desatendidas.")
    E.pie(fig, FUENTE_EJEC)
    return E.guardar(fig, "EXHIBIT_17_gasto_por_funcion",
                     dict(left=0.30, right=0.90, top=0.755, bottom=0.10))


def ex18():
    """Empleo y vivienda contra todo lo demás."""
    b = {r["clave"]: float(r["monto"]) for r in E.leer("data/baseline_2025.csv")}
    total = b["gastos_totales"]
    empleo, vivienda = b["gasto_empleo"], b["gasto_vivienda"]
    resto = total - empleo - vivienda

    fig, ax = E.figura(2.8)
    izq = 0.0
    for etiqueta, v, color in (("Todo el resto del presupuesto", resto, E.CAL),
                               ("Vivienda", vivienda, E.RIO),
                               ("Empleo", empleo, E.BARRANCA)):
        ax.barh([0], [v / 1e6], left=izq / 1e6, height=0.3, color=color, zorder=3)
        izq += v
    ax.annotate("Todo el resto del presupuesto\n%s M   %s"
                % (E.numero(resto / 1e6), E.pct(100 * resto / total, 2)),
                (resto / 2e6, 0), ha="center", va="center", fontsize=7.4,
                color=E.TINTA, weight="bold")
    # Las dos partidas son tan chicas que hay que sacárlas con lineas guia.
    for i, (etiqueta, v, color) in enumerate(
            (("Vivienda: %s M, el %s del presupuesto"
              % (E.numero(vivienda / 1e6, 1), E.pct(100 * vivienda / total, 2)),
              vivienda, E.RIO),
             ("Empleo: %s M, el %s del presupuesto"
              % (E.numero(empleo / 1e6, 1), E.pct(100 * empleo / total, 2)),
              empleo, E.BARRANCA))):
        x = (total - (vivienda + empleo) / 2) / 1e6
        ax.annotate(etiqueta, (x, 0.16 if i == 0 else -0.16),
                    xytext=(-40, 46 if i == 0 else -46),
                    textcoords="offset points", ha="right",
                    va="center", fontsize=7.2, color=color, weight="bold",
                    arrowprops=dict(arrowstyle="-", color=color, linewidth=0.8))
    ax.set_ylim(-0.75, 0.75)
    ax.set_yticks([])
    ax.set_xlim(0, total / 1e6 * 1.005)
    E.podar_tick_superior(ax)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlabel("millones de pesos devengados en 2025", fontsize=6.8)
    E.limpiar(ax, grilla=None)
    ax.spines["bottom"].set_visible(True)
    E.titular(fig, "EXHIBIT 18",
              "Empleo y vivienda son 5 de cada 3.000 pesos que gasta el Municipio",
              "Las dos partidas juntas suman el 0,16% del presupuesto "
              "ejecutado en 2025.")
    E.pie(fig, "Estado de Situación Económico-Financiera 2025, gastos por programa")
    return E.guardar(fig, "EXHIBIT_18_empleo_vivienda_vs_resto",
                     dict(left=0.055, right=0.90, top=0.665, bottom=0.185))


def ex20():
    """Hogares sin gas de red, en cantidad, no en porcentaje."""
    zonas = E.zonas_ordenadas()
    datos = [(z["zona"], int(z["hogares"]) * float(z["pct_sin_gas_red"]) / 100)
             for z in zonas]
    datos.sort(key=lambda x: -x[1])
    total = sum(v for _, v in datos)
    dos = datos[0][1] + datos[1][1]

    fig, ax = E.figura(3.1)
    colores = [E.BARRANCA if i < 2 else E.RIO for i in range(len(datos))]
    ax.bar(range(len(datos)), [v for _, v in datos], width=0.62, color=colores,
           zorder=3)
    for i, (_, v) in enumerate(datos):
        ax.annotate(E.numero(v), (i, v), xytext=(0, 5),
                    textcoords="offset points", ha="center", fontsize=7,
                    color=colores[i], weight="bold")
    ax.set_xticks(range(len(datos)))
    ax.set_xticklabels([E.zona_bonita(n) for n, _ in datos], fontsize=7.2)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylim(0, max(v for _, v in datos) * 1.24)
    ax.set_ylabel("hogares", fontsize=6.8)
    E.limpiar(ax)
    E.titular(fig, "EXHIBIT 20",
              "%s hogares de San Isidro cocinan sin gas de red" % E.numero(total),
              "Boulogne y Beccar concentran %s, el %s del total del partido."
              % (E.numero(dos), E.pct(100 * dos / total, 1)))
    E.pie(fig, FUENTE_CENSO,
          "En cantidad de hogares, no en porcentaje: un porcentaje chico sobre "
          "una zona grande sigue siendo mucha gente.")
    return E.guardar(fig, "EXHIBIT_20_hogares_sin_gas",
                     dict(left=0.115, right=0.985, top=0.685, bottom=0.13))
