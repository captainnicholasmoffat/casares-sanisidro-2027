#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capitulo 1 - Diagnostico. Exhibits 01 a 05."""

import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E
import matplotlib.pyplot as plt

FUENTE_SERIE = ("elaboración propia sobre rendiciones de cuentas y ejecución "
                "presupuestaria del Municipio de San Isidro, deflactado con "
                "IPC INDEC empalmado (data/serie_gastos_comparable.csv)")
FUENTE_CENSO = ("INDEC, Censo Nacional de Población, Hogares y Viviendas 2022, "
                "procesado con Redatam 7 (data/zonas_indicadores.csv)")
FUENTE_PBA = ("Ministerio de Hacienda y Finanzas de la Provincia de Buenos "
              "Aires, transferencias a municipios 2021-2025")


def _pico_a_piso(con):
    """(anio del maximo, anio del minimo, valor minimo, valor maximo).

    La caida del subtitulo del EXHIBIT 01 sale de aca. Escribirla a mano seria
    lo mismo que el 2.303 del EXHIBIT 09: la serie cambia y el titulo no."""
    amax, vmax = max(con, key=lambda t: t[1])
    amin, vmin = min(con, key=lambda t: t[1])
    return amax, amin, vmin, vmax


def ex01():
    """Gasto real 2010-2025. Los años sin dato se ven vacíos."""
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
        ax.text(a, tope * 0.5, "sin\nrendición", ha="center", va="center",
                fontsize=5.6, color=E.TINTA, alpha=0.55, rotation=90)

    maxi = max(con, key=lambda x: x[1])
    mini = min(con, key=lambda x: x[1])
    for (a, v), etiqueta, color in ((maxi, "máximo", E.TINTA),
                                    (mini, "mínimo", E.BARRANCA)):
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
    top, bottom = E.marco(
        fig, "EXHIBIT 01",
              "El gasto municipal real cae %s entre %d y %d"
              % (E.pct(100 * (1 - _pico_a_piso(con)[2] / _pico_a_piso(con)[3]), 1),
                 _pico_a_piso(con)[0], _pico_a_piso(con)[1]),
              "Gasto total en pesos constantes. Un solo concepto en todos los "
              "años: gastos corrientes más de capital, sin aplicaciones financieras.",
        FUENTE_SERIE,
          "2013, 2018 y 2023 no tienen rendición de cuentas publicada. No se "
          "interpolaron: el hueco queda a la vista.")
    return E.guardar(fig, "EXHIBIT_01_gasto_real_2010_2025",
                     dict(left=0.115, right=0.985, top=top, bottom=bottom))


def _nbi_del_partido():
    """NBI del partido, contado desde los 360 radios. No se escribe a mano."""
    con = tot = 0
    for f in E.leer("data/censo2022_sanisidro_por_radio.csv"):
        con += int(float(f.get("hogares_nbi__si") or 0))
        tot += int(float(f.get("hogares_nbi__total") or 0))
    return 100.0 * con / tot if tot else 0.0


def _parte_de_la_carencia(zonas):
    """Qué parte del déficit del partido está en esas zonas.

    Es el mismo índice que reparte la plata en el capítulo 4: el promedio, sobre
    los cuatro indicadores, de la parte del partido que cae en la zona.

    Se calcula. El título decía "toda la carencia", que era una afirmación
    escrita a mano — el verificador de números no la veía porque no es un
    número, y quedó vieja cuando cambiaron las zonas.
    """
    IND = ["nbi", "sin_cloaca", "sin_gas_red", "hacinamiento"]
    z = E.leer("data/zonas_indicadores.csv")
    tot = {k: sum(int(r[k]) for r in z) for k in IND}
    return 100 * sum(sum(int(r[k]) / tot[k] for k in IND) / len(IND)
                     for r in z if r["zona"] in zonas)


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

    # --------------------------------------------------------------
    # LEYENDA, NO ETIQUETAS SOBRE LAS BARRAS
    # --------------------------------------------------------------
    # Rotular cada serie sobre su barra mas alta funciona cuando las series
    # tienen su maximo en zonas distintas. Aca NO: tres de las cuatro lo tienen
    # en Beccar, y a alturas de 10,6 / 12,7 / 37,3 sobre un eje que llega a 50.
    # Las dos primeras quedaban a dos puntos una de otra y se pisaban entre si
    # y contra las barras. El verificador de colisiones no lo denunciaba porque
    # el solape no llegaba al umbral, y el de texto tapado tampoco porque las
    # etiquetas van por encima de las barras.
    #
    # Con cuatro series que comparten las mismas seis categorias, el lugar de
    # los nombres es una leyenda: se lee una vez y vale para todo el grafico.
    # Va en una sola fila, arriba a la derecha, sobre el rincon que dejan libre
    # las zonas de menor carencia, que son las de la derecha.
    fig, ax = E.figura(3.35)
    for i, (etiqueta, col, color) in enumerate(series):
        pos = [xx - 0.39 + ancho * (i + 0.5) for xx in x]
        vals = [float(z[col]) for z in zonas]
        ax.bar(pos, vals, width=ancho * 0.9, color=color, zorder=3,
               label=etiqueta)
    leyenda = ax.legend(loc="upper right", ncols=len(series), frameon=False,
                        fontsize=6.2, handlelength=0.85, handleheight=0.85,
                        handletextpad=0.35, columnspacing=1.0,
                        borderaxespad=0.2, labelcolor="linecolor")
    for t in leyenda.get_texts():
        t.set_fontweight("bold")
    ax.set_xticks(x)
    ax.set_xticklabels([E.dos_lineas(E.zona_bonita(z["zona"])) for z in zonas],
                       fontsize=7.2, linespacing=1.25)
    ax.yaxis.set_major_formatter(E.eje_pct())
    ax.set_ylim(0, max(float(z["pct_sin_gas_red"]) for z in zonas) * 1.30)
    E.podar_tick_superior(ax, "y", 5)
    E.limpiar(ax)
    top, bottom = E.marco(
        fig, "EXHIBIT 02",
              "Boulogne y Béccar concentran el %s de la carencia del partido"
              % E.pct(_parte_de_la_carencia(("Boulogne Sur Mer", "Beccar")), 0),
              "Cuatro indicadores por zona, ordenadas de peor a mejor por NBI. "
              "El NBI del partido es %s." % E.pct(_nbi_del_partido(), 2),
        FUENTE_CENSO)
    return E.guardar(fig, "EXHIBIT_02_zonas_carencias",
                     dict(left=0.06, right=0.985, top=top, bottom=bottom))


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
    ax.set_xticklabels([E.dos_lineas(E.zona_bonita(z["zona"])) for z in zonas],
                       fontsize=7.2, linespacing=1.25)
    ax.yaxis.set_major_formatter(E.eje_pct())
    ax.set_ylim(0, max(vals) * 1.22)
    E.limpiar(ax)
    # Sin podar, el ultimo tick queda pegado al borde de arriba y la bajada le
    # pasa por encima.
    E.podar_tick_superior(ax, "y", 5)
    top, bottom = E.marco(
        fig, "EXHIBIT 03",
              "El mismo orden, dado vuelta: donde falta todo, tampoco hay título",
              "Población con universidad completa o más, por zona. Mismo orden "
              "que el exhibit 02, de peor a mejor en NBI.",
        FUENTE_CENSO)
    return E.guardar(fig, "EXHIBIT_03_educacion_por_zona",
                     dict(left=0.06, right=0.985, top=top, bottom=bottom))


def _parcial():
    """(anio, {municipio: participacion}) del ultimo anio incompleto.

    El pie del EXHIBIT 04 lo cita. Sale del CSV: cuando se publique el anual de
    ese anio, el pie se actualiza solo o desaparece."""
    filas = [f for f in E.leer("data/coparticipacion_comparada.csv")
             if int(f["meses"]) < 12]
    if not filas:
        return None, {}
    anio = max(int(f["anio"]) for f in filas)
    return anio, {f["municipio"]: float(f["participacion_pct"])
                  for f in filas if int(f["anio"]) == anio}


def ex04():
    """La participación de cuatro municipios del norte, 2021-2025."""
    filas = [f for f in E.leer("data/coparticipacion_comparada.csv")
             if int(f["meses"]) == 12]
    anios = sorted({int(f["anio"]) for f in filas})
    munis = ["SAN ISIDRO", "TIGRE", "VICENTE LOPEZ", "SAN FERNANDO"]
    colores = {"SAN ISIDRO": E.RIO, "TIGRE": E.BARRANCA,
               "VICENTE LOPEZ": E.TINTA, "SAN FERNANDO": E.AMBAR}
    bonito = {"SAN ISIDRO": "San Isidro", "TIGRE": "Tigre",
              "VICENTE LOPEZ": "Vicente López", "SAN FERNANDO": "San Fernando"}

    # Cuanto separar verticalmente cada etiqueta, en puntos. A la izquierda
    # Tigre y Vicente Lopez arrancan a menos de un punto de distancia; a la
    # derecha, en 2025, San Isidro y Tigre terminan pegados porque justo ahi
    # se cruzan, que es lo que el grafico cuenta.
    desplazo = {"SAN ISIDRO": 5, "TIGRE": -5, "VICENTE LOPEZ": 6,
                "SAN FERNANDO": 0}
    desplazo_fin = {"SAN ISIDRO": -7, "TIGRE": 7, "VICENTE LOPEZ": 0,
                    "SAN FERNANDO": 0}
    fig, ax = E.figura(3.5)
    for m in munis:
        ys = [float(f["participacion_pct"]) for a in anios
              for f in filas if int(f["anio"]) == a and f["municipio"] == m]
        ancho = 2.1 if m == "SAN ISIDRO" else 1.1
        ax.plot(anios, ys, color=colores[m], linewidth=ancho, zorder=3,
                marker="o", markersize=2.6 if m == "SAN ISIDRO" else 1.8)
        E.etiqueta_serie(ax, anios[-1], ys[-1],
                         "%s  %s" % (bonito[m], E.pct(ys[-1], 4)),
                         colores[m], dx=6, dy=desplazo_fin.get(m, 0))
        # Las de la izquierda quedan DENTRO del area del grafico: si se apoyan
        # sobre el borde caen encima de los numeros del eje y.
        E.etiqueta_serie(ax, anios[0], ys[0], E.pct(ys[0], 4),
                         colores[m], dx=-9, dy=desplazo.get(m, 0), ha="right")

    ax.set_xlim(anios[0] - 1.5, anios[-1] + 1.55)
    ax.set_xticks(anios)
    ax.set_xticklabels([str(a) for a in anios], fontsize=7)
    ax.yaxis.set_major_formatter(E.eje_pct(1))
    E.podar_tick_superior(ax, "y", 5)
    E.limpiar(ax)
    top, bottom = E.marco(
        fig, "EXHIBIT 04",
              "Tigre pasa a San Isidro en 2025: el reparto provincial se dio vuelta",
              "Participación de cada municipio en el total transferido por la "
              "Provincia a los 135 municipios. Años completos.",
        FUENTE_PBA,
          "%d va con seis meses y queda fuera del gráfico. San Isidro cae a "
          "%s y Tigre sube a %s."
          % (_parcial()[0], E.pct(_parcial()[1]["SAN ISIDRO"], 4),
             E.pct(_parcial()[1]["TIGRE"], 4)))
    return E.guardar(fig, "EXHIBIT_04_coparticipacion_comparada",
                     dict(left=0.085, right=0.80, top=top, bottom=bottom))


def ex05():
    """
    San Isidro contra los otros 105 municipios, en peso del personal y en
    peso de la obra publica.

    Los 106 municipios van como puntos, uno por fila, ordenados por valor. Un
    grafico de barras con 106 barras no se lee; una tira de puntos si, y ademas
    deja ver donde se amontonan. San Isidro va en RIO y con su puesto escrito,
    porque el numero que se cita despues es ese.

    Los dos ordenes van al reves a proposito y esta dicho en cada panel:
    en personal el puesto 1 es el que MENOS gasta en personal, en obra el
    puesto 1 es el que MAS invierte. Se leen igual de izquierda a derecha pero
    no quieren decir lo mismo.
    """
    import statistics
    from matplotlib.patheffects import withStroke
    filas = E.leer("data/rafam_2025_municipios.csv")
    n = len(filas)
    paneles = [
        ("pct_personal", "puesto_personal",
         "Peso del personal", "gastos en personal sobre gasto devengado",
         "1 = el que menos peso le da al personal"),
        ("pct_obra", "puesto_obra",
         "Peso de la obra pública", "bienes de uso sobre gasto devengado",
         "1 = el que más invierte en obra"),
    ]
    fig = E.figura(3.5, ejes=False)[0]
    ejes = fig.subplots(1, 2)
    for ax, (clave, puesto, titulo, subtitulo, sentido) in zip(ejes, paneles):
        vals = sorted(float(f[clave]) for f in filas)
        mediana = statistics.median(vals)
        si = [f for f in filas if f["municipio"] == "San Isidro"][0]
        v_si, p_si = float(si[clave]), int(si[puesto])

        ax.scatter(vals, range(1, n + 1), s=7, color=E.CAL, zorder=3,
                   edgecolors="none")
        ax.axvline(mediana, color=E.TINTA, linewidth=0.9, zorder=4,
                   linestyle=(0, (3, 2)))
        # La tira siempre va de menor a mayor, en los dos paneles: la fila del
        # punto es su lugar en ese orden. El PUESTO es otra cosa y va escrito,
        # porque en obra el 1 es el de mas arriba y en personal el de mas
        # abajo. Mezclar las dos cosas dibujaria a San Isidro cuarto desde
        # abajo cuando es cuarto desde arriba.
        y_si = vals.index(v_si) + 1
        ax.scatter([v_si], [y_si], s=34, color=E.RIO, zorder=6,
                   edgecolors=E.PAPEL, linewidths=0.8)
        # La etiqueta va del lado donde queda lienzo: si el punto esta pasada
        # la mitad del eje, a la izquierda.
        derecha = v_si < max(vals) * 0.55
        ax.annotate("San Isidro  %s\npuesto %d de %d" % (E.pct(v_si, 1), p_si, n),
                    (v_si, y_si), xytext=(7 if derecha else -7, 0),
                    textcoords="offset points",
                    ha="left" if derecha else "right", va="center",
                    fontsize=6.8, color=E.RIO, weight="bold",
                    path_effects=[withStroke(linewidth=2.6,
                                             foreground=E.PAPEL)])
        # El rotulo de la mediana se apoya en la punta de la linea que queda
        # LEJOS de San Isidro. Con las dos en el mismo extremo se pisaban, y
        # cual extremo esta libre depende del panel: en personal San Isidro
        # esta abajo, en obra arriba.
        arriba = y_si < n / 2
        ax.annotate("mediana de los %d\n%s" % (n, E.pct(mediana, 1)),
                    (mediana, n if arriba else 0),
                    xytext=(4, -2 if arriba else 3),
                    textcoords="offset points", ha="left",
                    va="top" if arriba else "bottom", fontsize=6.2,
                    color=E.TINTA)
        ax.set_title("%s\n%s" % (titulo, subtitulo), fontsize=7.2,
                     color=E.TINTA, loc="left", pad=6, linespacing=1.4)
        ax.set_xlabel(sentido, fontsize=6.2, color=E.TINTA, alpha=0.72)
        ax.xaxis.set_major_formatter(E.eje_pct(0))
        ax.set_xlim(0, max(vals) * 1.45)
        ax.set_ylim(0, n * 1.12)
        ax.set_yticks([])
        E.limpiar(ax, grilla="x")
        E.podar_tick_superior(ax, "x", 4)

    top, bottom = E.marco(
        fig, "EXHIBIT 05",
              "San Isidro gasta menos en sueldos y mucho más en obra que la "
              "mediana bonaerense",
              "Cada punto es un municipio, ordenados por valor. Ejecución "
              "2025, gasto devengado.",
        "RAFAM 2025, vía La Verdadera PBA (la-verdadera-pba.pages.dev), "
               "capturado el 3 de septiembre de 2026. "
               "data/rafam_2025_municipios.csv",
          "Son 106 de los 135 municipios: los otros 29 no están en la "
          "planilla. No se estimó ninguno. La Verdadera PBA procesa datos de "
          "RAFAM pero no es la fuente oficial: el dato de San Isidro está "
          "validado contra la ejecución del propio Municipio, el de los otros "
          "105 no.")
    return E.guardar(fig, "EXHIBIT_05_personal_y_obra_vs_provincia",
                     dict(left=0.045, right=0.985, top=top, bottom=bottom,
                          wspace=0.30))
