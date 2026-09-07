#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capitulo 5 - Sectorial. Exhibits 17, 18 y 20. El 19 no se genera."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E

FUENTE_EJEC = ("Municipio de San Isidro, ejecución presupuestaria 2025, "
               "informe anual. Gasto devengado")
FUENTE_CENSO = ("INDEC, Censo Nacional de Población, Hogares y Viviendas 2022, "
                "procesado con Redatam 7")

# Se destacan porque son las dos funciones que el programa señala como
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

    fig, ax = E.figura(5.4)
    y = range(len(filas))
    colores = [E.BARRANCA if n.upper() in DESTACAR else E.RIO for n, _ in filas]
    ax.barh(list(y), [v / 1e6 for _, v in filas], height=0.66, color=colores,
            zorder=3)
    for i, (nombre, v) in enumerate(filas):
        destacada = nombre.upper() in DESTACAR
        ax.annotate("%s M   %s" % (E.numero(v / 1e6), E.pct(100 * v / total, 1)),
                    (v / 1e6, i), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=6.4,
                    color=E.BARRANCA if destacada else E.TINTA,
                    weight="bold" if destacada else "normal")
    ax.set_yticks(list(y))
    ax.set_yticklabels([E.envolver(E.nombre_funcion(n), 6.2, 1.15)
                        for n, _ in filas], fontsize=6.2, linespacing=1.15)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlim(0, max(v for _, v in filas) / 1e6 * 1.42)
    ax.set_xlabel("millones de pesos devengados en 2025", fontsize=6.8)
    E.limpiar(ax, grilla="x")
    top, bottom = E.marco(
        fig, "EXHIBIT 17",
              "Ecología y agua potable juntas no llegan al 1,5% del presupuesto",
              "Gasto por función, ejercicio 2025. En BARRANCA las dos "
              "funciones que el programa señala como desatendidas.",
        FUENTE_EJEC)
    return E.guardar(fig, "EXHIBIT_17_gasto_por_funcion",
                     dict(left=0.30, right=0.90, top=top, bottom=bottom))


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
    # Las dos partidas son tan chicas que hay que sacarlas con lineas guia.
    # El texto va en coordenadas de DATO y no en puntos: con un desplazamiento
    # fijo de 62 puntos el rotulo de abajo se salia del area del grafico y
    # caia encima de los numeros del eje x.
    for i, (etiqueta, medio, color) in enumerate(
            (("Vivienda: %s M, el %s del presupuesto"
              % (E.numero(vivienda / 1e6, 1), E.pct(100 * vivienda / total, 2)),
              (resto + vivienda / 2) / 1e6, E.RIO),
             ("Empleo: %s M, el %s del presupuesto"
              % (E.numero(empleo / 1e6, 1), E.pct(100 * empleo / total, 2)),
              (resto + vivienda + empleo / 2) / 1e6, E.BARRANCA))):
        ax.annotate(etiqueta, (medio, 0.16 if i == 0 else -0.16),
                    xytext=(total / 1e6 * 0.93, 0.60 if i == 0 else -0.60),
                    textcoords="data", ha="right",
                    va="center", fontsize=7.2, color=color, weight="bold",
                    arrowprops=dict(arrowstyle="-", color=color, linewidth=0.8))
    ax.set_ylim(-1.05, 1.05)
    ax.set_yticks([])
    ax.set_xlim(0, total / 1e6 * 1.005)
    E.podar_tick_superior(ax)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlabel("millones de pesos devengados en 2025", fontsize=6.8)
    E.limpiar(ax, grilla=None)
    ax.spines["bottom"].set_visible(True)
    top, bottom = E.marco(
        fig, "EXHIBIT 18",
              "Empleo y vivienda son 5 de cada 3.000 pesos que gasta el Municipio",
              "Las dos partidas juntas suman el 0,16% del presupuesto "
              "ejecutado en 2025.",
        "Estado de Situación Económico-Financiera 2025, gastos por programa")
    return E.guardar(fig, "EXHIBIT_18_empleo_vivienda_vs_resto",
                     dict(left=0.055, right=0.90, top=top, bottom=bottom))


# Los cinco estados posibles, de peor a mejor. "cumplida" esta en la lista a
# proposito aunque hoy no la tenga ninguna: es el estado al que hay que llegar
# y el CSV tiene que poder decirlo el dia que pase.
ESTADOS = ["no_existe", "enlace_incorrecto", "caido", "desactualizado",
           "cumplida"]

# Las columnas del cuerpo, en fraccion del ancho del eje. El casillero, el
# texto de la medida y, una linea mas abajo, el estado y la evidencia.
X_CASILLA, X_TEXTO, X_EVIDENCIA = 0.008, 0.045, 0.30


def ex19():
    """
    Las ocho medidas de transparencia y el estado de cada una.

    No hay cantidades que medir: hay ocho cosas y ninguna esta hecha. Va como
    una lista con un casillero por medida, y los ocho casilleros estan vacios.
    Ocho cuadrados sin tildar se leen antes que cualquier numero, y asi el
    lector no tiene que creerle a la bajada: lo ve.

    Las ocho salen de data/transparencia_medidas.csv. El CSV esta en ASCII,
    igual que todos los datos del repo, y los acentos se ponen al MOSTRAR con
    las tablas de estilo.py.
    """
    filas = E.leer("data/transparencia_medidas.csv")
    orden = {e: i for i, e in enumerate(ESTADOS)}
    filas.sort(key=lambda r: (orden[r["estado_actual"]], r["medida"]))
    n = len(filas)
    cumplidas = sum(1 for r in filas if r["estado_actual"] == "cumplida")

    # Alto: cada medida ocupa DOS lineas de texto, la medida y su estado.
    # Con la figura mas baja las dos lineas de una fila se tocaban.
    fig, ax = E.figura(4.5)
    for i, r in enumerate(filas):
        y = n - 1 - i
        # El casillero: un cuadrado sin rellenar. Si alguna vez una medida se
        # cumple, el CSV lo dira y el cuadrado se pinta solo.
        hecha = r["estado_actual"] == "cumplida"
        ax.plot([X_CASILLA], [y + 0.22], marker="s", markersize=6.4,
                markerfacecolor=E.RIO if hecha else "none",
                markeredgecolor=E.RIO if hecha else E.TINTA,
                markeredgewidth=1.0, zorder=5, clip_on=False)
        ax.annotate(E.nombre_medida(r["medida"]), (X_TEXTO, y + 0.22),
                    ha="left", va="center", fontsize=7.4, color=E.TINTA)
        ax.annotate(E.nombre_estado(r["estado_actual"]), (X_TEXTO, y - 0.22),
                    ha="left", va="center", fontsize=6.4, color=E.BARRANCA,
                    weight="bold")
        ax.annotate(E.nombre_evidencia(r["fuente_verificacion"]),
                    (X_EVIDENCIA, y - 0.24), ha="left", va="center",
                    fontsize=6.2, color=E.TINTA, alpha=0.66)
        if i:
            ax.axhline(y + 0.58, color=E.CAL, linewidth=0.8, zorder=2)

    ax.annotate("cumplidas hoy: %d de %d" % (cumplidas, n),
                (X_CASILLA, n - 0.30), ha="left", va="center", fontsize=6.4,
                color=E.TINTA, alpha=0.66)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.55, n - 0.15)
    E.limpiar(ax, grilla=None)
    for lado in ax.spines.values():
        lado.set_visible(False)
    top, bottom = E.marco(
        fig, "EXHIBIT 19",
              "Las ocho medidas de transparencia: hoy no hay ninguna cumplida",
              "Estado verificado en septiembre de 2026 contra el portal de "
              "transparencia del Municipio. Ninguna de las ocho cuesta un peso "
              "de presupuesto y las ocho se cumplen en cien días.",
        "data/transparencia_medidas.csv. Las ocho medidas son definición del "
               "programa de gobierno, no un dato público; el estado de cada "
               "una sí se verificó",
          "Los ocho casilleros están vacíos porque ninguna medida está "
          "cumplida. El día que una se cumpla, lo dice el CSV y el cuadrado "
          "se pinta solo.")
    return E.guardar(fig, "EXHIBIT_19_medidas_transparencia",
                     dict(left=0.022, right=0.985, top=top, bottom=bottom))


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
    ax.set_xticklabels([E.dos_lineas(E.zona_bonita(n)) for n, _ in datos],
                       fontsize=7.2, linespacing=1.25)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylim(0, max(v for _, v in datos) * 1.30)
    E.podar_tick_superior(ax, "y", 5)
    ax.set_ylabel("hogares", fontsize=6.8)
    E.limpiar(ax)
    top, bottom = E.marco(
        fig, "EXHIBIT 20",
              "%s hogares de San Isidro cocinan sin gas de red" % E.numero(total),
              "Boulogne y Beccar concentran %s, el %s del total del partido."
              % (E.numero(dos), E.pct(100 * dos / total, 1)),
        FUENTE_CENSO,
          "En cantidad de hogares, no en porcentaje: un porcentaje chico sobre "
          "una zona grande sigue siendo mucha gente.")
    return E.guardar(fig, "EXHIBIT_20_hogares_sin_gas",
                     dict(left=0.115, right=0.985, top=top, bottom=bottom))
