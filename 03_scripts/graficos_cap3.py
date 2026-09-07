#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capitulo 3 - La plata. Exhibits 08 a 12."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E

FUENTE_MODELO = ("modelo de flujo de caja, data/modelo_flujo_caja.csv. Pesos "
                 "constantes de diciembre de 2025, sin supuesto de inflación")
FUENTE_SEF = ("Municipio de San Isidro, Estado de Situación Económico-"
              "Financiera 2025, cuenta Ahorro-Inversión-Financiamiento")


def _modelo():
    por = {}
    for r in E.leer("data/modelo_flujo_caja.csv"):
        por.setdefault(r["escenario"], []).append(r)
    for v in por.values():
        v.sort(key=lambda r: int(r["anio"]))
    return por


def ex08():
    """Los tres escenarios, con el cruce por cero marcado."""
    por = _modelo()
    series = [("base", "Base", E.RIO),
              ("adverso", "Adverso", E.BARRANCA),
              ("reformista_percepcion", "Reformista, cobrando mejor", E.TINTA)]
    # Base y reformista terminan a menos de un cuerpo de distancia.
    separacion = {"base": -6, "reformista_percepcion": 6, "adverso": 0}
    fig, ax = E.figura(3.5)
    ax.axhline(0, color=E.TINTA, linewidth=0.9, zorder=4)
    cruces = []
    for clave, etiqueta, color in series:
        f = por[clave]
        xs = [int(r["anio"]) for r in f]
        ys = [float(r["resultado_financiero"]) / 1e6 for r in f]
        ax.plot(xs, ys, color=color, linewidth=1.6, zorder=3)
        E.etiqueta_serie(ax, xs[-1], ys[-1], etiqueta, color, dx=6,
                         dy=separacion.get(clave, 0))
        # Donde cruza cero, interpolando entre los dos anios que lo rodean.
        for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
            if y0 < 0 <= y1 or y0 > 0 >= y1:
                xc = x0 + (0 - y0) * (x1 - x0) / (y1 - y0)
                ax.plot([xc], [0], marker="o", markersize=4, color=color,
                        markeredgecolor=E.PAPEL, markeredgewidth=0.9, zorder=6)
                cruces.append((xc, color))

    # Base y reformista cruzan cero el mismo anio y las dos etiquetas caian
    # una encima de la otra. Se apilan, y si el anio coincide se escribe una
    # sola vez: dos veces "cruza cero en 2027" no agrega informacion.
    cruces.sort()
    escalon = 0
    visto = None
    for xc, color in cruces:
        anio = round(xc)
        if anio == visto:
            escalon += 1
        else:
            escalon, visto = 0, anio
            # El anio del cruce va como anio, no como numero con separador de
            # miles: E.numero() le metia un punto y quedaba "2.027".
            ax.annotate("cruza cero\nen %d" % anio, (xc, 0),
                        xytext=(0, -22 - escalon * 17),
                        textcoords="offset points", ha="center", fontsize=6.2,
                        color=E.TINTA)
    ax.set_xlim(2024.4, 2040.5)
    ax.set_xticks(range(2025, 2038, 2))
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylabel("resultado financiero, millones de pesos dic-2025", fontsize=6.6)
    E.limpiar(ax)
    top, bottom = E.marco(
        fig, "EXHIBIT 08",
              "Sin cambios, San Isidro vuelve al azul en 2028. En el adverso, nunca",
              "Resultado financiero proyectado. El escenario reformista por "
              "reasignación coincide con el base y no se dibuja aparte.",
        FUENTE_MODELO)
    return E.guardar(fig, "EXHIBIT_08_escenarios_resultado",
                     dict(left=0.135, right=0.775, top=top, bottom=bottom))


def ex09():
    """Base contra reformista por percepción, con el area entre medio."""
    por = _modelo()
    a, b = por["base"], por["reformista_percepcion"]
    xs = [int(r["anio"]) for r in a]
    ya = [float(r["resultado_financiero"]) / 1e6 for r in a]
    yb = [float(r["resultado_financiero"]) / 1e6 for r in b]

    fig, ax = E.figura(3.3)
    ax.fill_between(xs, ya, yb, color=E.RIO, alpha=0.16, zorder=2, linewidth=0)
    ax.axhline(0, color=E.TINTA, linewidth=0.9, zorder=4)
    ax.plot(xs, ya, color=E.TINTA, linewidth=1.4, zorder=3)
    ax.plot(xs, yb, color=E.RIO, linewidth=2.0, zorder=3)
    E.etiqueta_serie(ax, xs[-1], ya[-1], "Base", E.TINTA, dx=6, dy=-7)
    E.etiqueta_serie(ax, xs[-1], yb[-1], "Reformista\ncobrando mejor", E.RIO,
                     dx=6, dy=8)
    medio = len(xs) // 2
    ax.annotate("el programa se ejecuta entero\nY el resultado mejora",
                (xs[medio], (ya[medio] + yb[medio]) / 2), xytext=(0, 0),
                textcoords="offset points", ha="center", va="center",
                fontsize=6.6, color=E.RIO, weight="bold")
    # Arranca un poco antes de 2025 para que el primer rotulo del eje x no
    # caiga encima del ultimo numero del eje y.
    ax.set_xlim(2024.4, 2040)
    ax.set_xticks(range(2025, 2038, 2))
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylabel("resultado financiero, millones de pesos dic-2025", fontsize=6.6)
    E.limpiar(ax)
    top, bottom = E.marco(
        fig, "EXHIBIT 09",
              "Pagar el programa cobrando mejor deja al Municipio mejor que no hacerlo",
              "El area sombreada es la diferencia: 2.303 millones a favor en "
              "2031 y 2.924 en 2037.",
        FUENTE_MODELO)
    return E.guardar(fig, "EXHIBIT_09_base_vs_reformista",
                     dict(left=0.135, right=0.775, top=top, bottom=bottom))


def ex10():
    """Tornado: que mueve el resultado de 2031."""
    filas = [r for r in E.leer("data/sensibilidad.csv") if r["anio"] == "2031"]
    base = {}
    for r in E.leer("data/modelo_flujo_caja.csv"):
        if r["escenario"] == "base" and r["anio"] == "2031":
            base = float(r["resultado_financiero"]) / 1e6
    nombres = {"recursos_propios": "Recursos propios",
               "coparticipacion": "Coparticipación",
               "percepcion": "Percepción de recursos"}
    items = []
    for r in filas:
        v = float(r["resultado_financiero"]) / 1e6 - base
        if abs(v) < 1:
            continue
        items.append(("%s: %s" % (nombres[r["dimension"]], r["variante"]), v))
    items.sort(key=lambda x: abs(x[1]))

    fig, ax = E.figura(3.2)
    y = range(len(items))
    colores = [E.RIO if v >= 0 else E.BARRANCA for _, v in items]
    ax.barh(list(y), [v for _, v in items], height=0.6, color=colores, zorder=3)
    ax.axvline(0, color=E.TINTA, linewidth=0.9, zorder=4)
    for i, (_, v) in enumerate(items):
        # La etiqueta va del lado de afuera de la barra y un poco arriba: si
        # se centra, la de las barras negativas cae encima del rotulo del eje.
        dx = 5 if v >= 0 else -5
        ha = "left" if v >= 0 else "right"
        ax.annotate(("+" if v >= 0 else "") + E.numero(v) + " M", (v, i),
                    xytext=(dx, 7), textcoords="offset points", ha=ha,
                    va="center", fontsize=6.4, color=colores[i], weight="bold")
    ax.set_yticks(list(y))
    ax.set_yticklabels([n for n, _ in items], fontsize=6.8)
    ax.xaxis.set_major_formatter(E.eje_numero())
    lim = max(abs(v) for _, v in items) * 1.4
    ax.set_xlim(-lim, lim)
    E.limpiar(ax, grilla="x")
    top, bottom = E.marco(
        fig, "EXHIBIT 10",
              "Lo que manda es cuánto crecen los recursos propios",
              "Efecto sobre el resultado financiero de 2031 de mover cada "
              "variable, con las otras dos en su valor del escenario base. "
              "Base: %s millones." % E.numero(base),
        "data/sensibilidad.csv")
    return E.guardar(fig, "EXHIBIT_10_tornado_sensibilidad",
                     dict(left=0.325, right=0.93, top=top, bottom=bottom))


def ex11():
    """Rigido contra flexible, y que parte del flexible se lleva el programa."""
    par = {r["parametro"]: float(r["valor"])
           for r in E.leer("data/parametros_modelo.csv")}
    total = 0.0
    objetos = {}
    for r in E.leer("data/ejecucion_gastos_objeto.csv"):
        if (r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual"
                and r["devengado"]):
            objetos[r["objeto_codigo"]] = float(r["devengado"])
            total += float(r["devengado"])
    nucleo = objetos["1"] + objetos["7"]
    contratos = objetos["3"]
    flexible = total - nucleo - contratos
    # El costo del programa en regimen, del propio modelo.
    programa = max(float(r["reasignacion_necesaria"])
                   for r in E.leer("data/modelo_flujo_caja.csv")
                   if r["escenario"] == "reformista" and r["reasignacion_necesaria"])
    obra_vecinal = float([r["monto"] for r in E.leer("data/baseline_2025.csv")
                          if r["clave"] == "obra_publica_vecinal_anio4"][0])

    fig, ax = E.figura(2.9)
    tramos = [("Personal y deuda\nno se tocan", nucleo, E.TINTA),
              ("Contratos de servicios\nno dentro del ejercicio", contratos, E.CAL),
              ("Gasto flexible\nreasignable", flexible, E.RIO)]
    izq = 0.0
    for etiqueta, v, color in tramos:
        ax.barh([0], [v / 1e6], left=izq / 1e6, height=0.34, color=color, zorder=3)
        ax.annotate("%s\n%s M   %s" % (etiqueta, E.numero(v / 1e6),
                                       E.pct(100 * v / total, 1)),
                    ((izq + v / 2) / 1e6, 0), ha="center", va="center",
                    fontsize=6.4, weight="bold",
                    color=E.TINTA if color is E.CAL else E.PAPEL)
        izq += v
    # Debajo, que se lleva el margen flexible.
    base_x = (nucleo + contratos) / 1e6
    for i, (etiqueta, v, color) in enumerate(
            [("programa de empleo y vivienda", programa, E.BARRANCA),
             ("obra pública vecinal (cap. 4)", obra_vecinal, E.AMBAR)]):
        ax.barh([-0.55 - i * 0.24], [v / 1e6], left=base_x, height=0.17,
                color=color, zorder=3)
        # La etiqueta va a la izquierda del extremo de la barra: hacia la
        # derecha no hay lienzo y el texto se saldria de la imagen.
        ax.annotate("%s: %s M, el %s del flexible"
                    % (etiqueta, E.numero(v / 1e6), E.pct(100 * v / flexible, 1)),
                    (base_x, -0.55 - i * 0.24), xytext=(-6, 0),
                    textcoords="offset points", va="center", ha="right",
                    fontsize=6.4, color=color, weight="bold")
    ax.set_ylim(-1.15, 0.42)
    ax.set_yticks([])
    ax.set_xlim(0, total / 1e6 * 1.02)
    E.podar_tick_superior(ax)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlabel("millones de pesos devengados en 2025", fontsize=6.8)
    E.limpiar(ax, grilla=None)
    ax.spines["bottom"].set_visible(True)
    top, bottom = E.marco(
        fig, "EXHIBIT 11",
              "El 73,1% del presupuesto no se puede tocar dentro del ejercicio",
              "Composición del gasto 2025 por rigidez, y que parte del margen "
              "flexible se llevan las dos propuestas del programa.",
        "data/ejecucion_gastos_objeto.csv y data/modelo_flujo_caja.csv",
          "Las dos propuestas juntas se llevan el 41,4% del gasto flexible. "
          "Caben, pero no queda lugar para una tercera del mismo tamaño.")
    return E.guardar(fig, "EXHIBIT_11_rigidez_del_gasto",
                     dict(left=0.32, right=0.985, top=top, bottom=bottom))


def ex12():
    """Cascada: de donde sale el deficit de 6.051 millones."""
    b = {r["clave"]: float(r["monto"]) for r in E.leer("data/baseline_2025.csv")}
    # Los rotulos van en tres lineas cortas: en dos, "Ingresos corrientes" y
    # "Gastos corrientes" son mas anchos que la columna y se pisan entre si.
    pasos = [
        ("Ingresos\ncorrientes\npercibidos", b["ingresos_corrientes"], E.RIO, False),
        ("Gastos\ncorrientes\ndevengados", -b["gastos_corrientes"], E.BARRANCA, False),
        ("Ahorro\ncorriente", b["ahorro_corriente"], E.TINTA, True),
        ("Recursos\nde capital", b["recursos_de_capital"], E.RIO, False),
        ("Gastos\nde capital", -b["gastos_de_capital"], E.BARRANCA, False),
        ("Resultado\nfinanciero", b["resultado_financiero"], E.AMBAR, True),
    ]
    fig, ax = E.figura(3.3)
    acum = 0.0
    topes = [0.0]
    for i, (etiqueta, v, color, total) in enumerate(pasos):
        if total:
            ax.bar([i], [v / 1e6], width=0.6, color=color, zorder=3)
            y_texto = v / 1e6
            acum = v
        else:
            ax.bar([i], [v / 1e6], bottom=acum / 1e6, width=0.6, color=color,
                   zorder=3)
            y_texto = (acum + v) / 1e6
            acum += v
        topes.append(y_texto)
        signo = "+" if v >= 0 and not total else ("" if total else "")
        ax.annotate("%s%s M" % (signo, E.numero(v / 1e6)), (i, y_texto),
                    xytext=(0, 7 if y_texto >= 0 else -11),
                    textcoords="offset points", ha="center",
                    va="bottom" if y_texto >= 0 else "top", fontsize=6.6,
                    color=color, weight="bold")
    ax.axhline(0, color=E.TINTA, linewidth=0.9, zorder=4)
    # El eje se abre por abajo lo suficiente para que las etiquetas de las dos
    # barras negativas caigan DENTRO del grafico y no sobre los rotulos del
    # eje x, y se corta arriba justo encima de la barra mas alta para que no
    # aparezca un tick de mas que llegue hasta la bajada.
    alto = max(topes) - min(topes)
    ax.set_ylim(min(topes) - alto * 0.24, max(topes) + alto * 0.08)
    ax.set_xticks(range(len(pasos)))
    ax.set_xticklabels([p[0] for p in pasos], fontsize=6.4, linespacing=1.2)
    ax.yaxis.set_major_formatter(E.eje_numero())
    ax.set_ylabel("millones de pesos de 2025", fontsize=6.8)
    E.limpiar(ax)
    E.podar_tick_superior(ax, "y")
    top, bottom = E.marco(
        fig, "EXHIBIT 12",
              "El déficit de 2025 no viene del gasto corriente: viene de la obra",
              "El ahorro corriente fue positivo en 49.751 millones. Lo que da "
              "vuelta el resultado son los 57.832 millones de gasto de capital.",
        FUENTE_SEF,
          "Los ingresos van por lo PERCIBIDO y los gastos por lo DEVENGADO: es "
          "la convención de la cuenta Ahorro-Inversión, no una elección nuestra.")
    return E.guardar(fig, "EXHIBIT_12_cascada_resultado_2025",
                     dict(left=0.135, right=0.985, top=top, bottom=bottom))
