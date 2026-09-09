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


def _dif(anio):
    """Diferencia reformista_percepcion - base, en millones. Se calcula, no se
    escribe a mano: cada corrida del modelo la mueve."""
    v = {}
    for r in E.leer("data/modelo_flujo_caja.csv"):
        if int(r["anio"]) == anio and r["escenario"] in ("base",
                                                         "reformista_percepcion"):
            v[r["escenario"]] = float(r["resultado_financiero"])
    return round((v["reformista_percepcion"] - v["base"]) / 1e6)


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
    # La anotacion iba centrada sobre el area sombreada, que en este grafico
    # tiene el ancho de una linea: el texto quedaba encima de las dos curvas.
    # Va abajo a la derecha, en el hueco vacio, con una guia hasta la franja.
    medio = len(xs) // 2
    ax.annotate("el programa se ejecuta entero\nY el resultado mejora",
                xy=(xs[medio], (ya[medio] + yb[medio]) / 2),
                xytext=(xs[medio] + 1.2, min(ya) * 0.55),
                ha="left", va="center", fontsize=6.6, color=E.RIO,
                weight="bold",
                arrowprops=dict(arrowstyle="-", color=E.RIO, linewidth=0.7,
                                shrinkA=2, shrinkB=3, alpha=0.75))
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
              "El area sombreada es la diferencia: %s millones a favor en "
              "2031 y %s en 2037." % (E.numero(_dif(2031)), E.numero(_dif(2037))),
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

    # --------------------------------------------------------------
    # LOS ROTULOS VAN AFUERA DE LOS SEGMENTOS, NO ADENTRO
    # --------------------------------------------------------------
    # Antes cada tramo llevaba su nombre CENTRADO adentro de su segmento. El
    # nombre mas largo —"Contratos de servicios / no dentro del ejercicio"— es
    # mas ancho que su segmento, asi que se derramaba sobre los dos vecinos: la
    # parte que caia sobre el tramo oscuro era texto oscuro sobre oscuro y la
    # que caia sobre el tramo claro era texto claro sobre claro. Desaparecian
    # letras enteras y se leia "ontratos de servicio".
    #
    # Ahora el nombre y la cifra van ARRIBA de la barra, alineados al borde de
    # su tramo, cada uno en el color de su tramo. Nada queda adentro, asi que
    # el ancho del texto deja de depender del ancho del segmento.
    fig, ax = E.figura(2.9)
    tramos = [("Personal y deuda\nno se tocan", nucleo, E.TINTA),
              ("Contratos de servicios\nno dentro del ejercicio", contratos,
               E.CAL, E.TINTA),
              ("Gasto flexible\nreasignable", flexible, E.RIO)]
    izq = 0.0
    for tramo in tramos:
        etiqueta, v, color = tramo[0], tramo[1], tramo[2]
        # El tramo claro se rotula en Tinta: su propio color no se lee sobre
        # papel.
        tinta_rotulo = tramo[3] if len(tramo) > 3 else color
        ax.barh([0], [v / 1e6], left=izq / 1e6, height=0.30, color=color,
                zorder=3)
        # El ultimo tramo llega al borde derecho del eje: si se alineara a la
        # izquierda como los otros, su cifra se saldria del lienzo.
        ultimo = izq + v >= total - 1
        ax.annotate("%s\n%s M · %s" % (etiqueta, E.numero(v / 1e6),
                                       E.pct(100 * v / total, 1)),
                    ((izq + v) / 1e6 if ultimo else izq / 1e6, 0.20),
                    xytext=(-2 if ultimo else 2, 3), textcoords="offset points",
                    ha="right" if ultimo else "left", va="bottom",
                    fontsize=6.4, weight="bold", color=tinta_rotulo,
                    linespacing=1.3)
        izq += v

    # --------------------------------------------------------------
    # LAS DOS PROPUESTAS CUELGAN DEL TRAMO FLEXIBLE
    # --------------------------------------------------------------
    # Antes flotaban abajo sin nada que las atara al tramo del que salen, y se
    # leian como un segundo grafico pegado. La guia vertical punteada baja
    # desde el borde izquierdo del tramo flexible y las dos barras arrancan
    # exactamente ahi: se ve que salen de ese tramo y de ningun otro.
    base_x = (nucleo + contratos) / 1e6
    y_ultima = -0.55 - 0.24
    ax.plot([base_x, base_x], [-0.16, y_ultima - 0.13], color=E.RIO,
            linewidth=0.8, linestyle=(0, (2, 2)), zorder=2)
    ax.annotate("de ese margen flexible salen las dos propuestas",
                (base_x, -0.30), xytext=(6, 0), textcoords="offset points",
                ha="left", va="center", fontsize=6.0, color=E.RIO,
                style="italic")
    for i, (etiqueta, v, color) in enumerate(
            [("programa de empleo y vivienda", programa, E.BARRANCA),
             ("obra pública vecinal (cap. 4)", obra_vecinal, E.AMBAR)]):
        ax.barh([-0.55 - i * 0.24], [v / 1e6], left=base_x, height=0.17,
                color=color, zorder=3)
        # La etiqueta va a la izquierda del arranque de la barra: hacia la
        # derecha queda menos de un cuarto del eje y el texto se saldria.
        ax.annotate("%s: %s M, el %s del flexible"
                    % (etiqueta, E.numero(v / 1e6), E.pct(100 * v / flexible, 1)),
                    (base_x, -0.55 - i * 0.24), xytext=(-6, 0),
                    textcoords="offset points", va="center", ha="right",
                    fontsize=6.4, color=color, weight="bold")
    ax.set_ylim(-1.05, 0.72)
    ax.set_yticks([])
    ax.set_xlim(0, total / 1e6 * 1.02)
    E.podar_tick_superior(ax)
    ax.xaxis.set_major_formatter(E.eje_numero())
    ax.set_xlabel("millones de pesos devengados en 2025", fontsize=6.8)
    E.limpiar(ax, grilla=None)
    ax.spines["bottom"].set_visible(True)
    top, bottom = E.marco(
        fig, "EXHIBIT 11",
              "El %s del presupuesto no se puede tocar dentro del ejercicio"
              % E.pct(100 * (nucleo + contratos) / total, 1),
              "Composición del gasto 2025 por rigidez, y que parte del margen "
              "flexible se llevan las dos propuestas del programa.",
        "data/ejecucion_gastos_objeto.csv y data/modelo_flujo_caja.csv",
          "Las dos propuestas juntas se llevan el %s del gasto flexible. "
          "Caben, pero no queda lugar para una tercera del mismo tamaño."
          % E.pct(100 * (programa + obra_vecinal) / flexible, 1))
    # left=0.32 reservaba un tercio del lienzo para las etiquetas de las dos
    # propuestas y dejaba la barra apilada metida en el 68% de la derecha, con
    # los segmentos mas angostos todavia que sus rotulos. Ahora los rotulos
    # estan afuera y la barra usa el ancho entero.
    return E.guardar(fig, "EXHIBIT_11_rigidez_del_gasto",
                     dict(left=0.06, right=0.985, top=top, bottom=bottom))


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
        # La etiqueta va SIEMPRE del lado de afuera de la barra. En un paso
        # negativo el extremo esta abajo, y poner el texto "arriba del punto"
        # lo metia adentro de la barra, en el mismo color: se leia "-2" y "M"
        # y el resto desaparecia. Lo encontro el verificador de texto tapado.
        hacia_arriba = (v >= 0) if not total else (y_texto >= 0)
        ax.annotate("%s%s M" % (signo, E.numero(v / 1e6)), (i, y_texto),
                    xytext=(0, 7 if hacia_arriba else -11),
                    textcoords="offset points", ha="center",
                    va="bottom" if hacia_arriba else "top", fontsize=6.6,
                    color=color, weight="bold", zorder=6)
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
              "El ahorro corriente fue positivo en %s millones. Lo que da "
              "vuelta el resultado son los %s millones de gasto de capital."
              % (E.numero(b["ahorro_corriente"] / 1e6),
                 E.numero(b["gastos_de_capital"] / 1e6)),
        FUENTE_SEF,
          "Los ingresos van por lo PERCIBIDO y los gastos por lo DEVENGADO: es "
          "la convención de la cuenta Ahorro-Inversión, no una elección nuestra.")
    return E.guardar(fig, "EXHIBIT_12_cascada_resultado_2025",
                     dict(left=0.135, right=0.985, top=top, bottom=bottom))
