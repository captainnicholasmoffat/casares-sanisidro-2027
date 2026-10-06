#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Los mismos graficos de charts.py, para la version A4 (dispatch 3, D): al ancho de la
caja de texto de A4 (482 pt) y con ninguna letra por debajo de 8 pt impresa (se dibujan
con 8,6 pt porque los mas anchos se achican un poco al entrar en la caja). Salen a
assets/svg_a4/; la version de pantalla sigue usando assets/svg/. Los dos mapas no se
rehacen aca (sus datos no estan en esta rama): build_a4.py les agranda la letra."""
import pathlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.text import Text

import charts as C

MIN_PT = 8.6
C.W = 482 / 72.0
C.OUT = pathlib.Path(__file__).parent.parent / "assets" / "svg_a4"
C.OUT.mkdir(parents=True, exist_ok=True)
matplotlib.rcParams.update({
    "font.size": MIN_PT, "axes.labelsize": MIN_PT, "legend.fontsize": MIN_PT,
    "xtick.labelsize": MIN_PT, "ytick.labelsize": MIN_PT,
})


def ajustes(fig, name):
    """Con letra mas grande, dos graficos necesitan acomodar rotulos para no pisarse."""
    ax = fig.axes[0]
    if name == "g_gasto_real":
        ax.tick_params(axis="x", labelrotation=90)
        for t in ax.texts:
            if "nivel de 2010" in t.get_text():
                t.set_text(" ".join(t.get_text().split()).replace("2010 ", "2010: "))
                t.set_va("bottom")
                t.set_position((13.6, t.get_position()[1] + 0.03))
    if name == "g_reformista":
        for t in ax.texts:
            if "Sin cambios" in t.get_text():
                t.set_position((t.get_position()[0], t.get_position()[1] - 4.5))


def save(fig, name):
    ajustes(fig, name)
    fig.canvas.draw()                     # crea los rotulos de los ejes
    for t in fig.findobj(Text):
        if t.get_text().strip() and t.get_fontsize() < MIN_PT:
            t.set_fontsize(MIN_PT)
    fig.savefig(C.OUT / f"{name}.svg", format="svg", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("  ", name)


C.save = save

if __name__ == "__main__":
    print("graficos A4:")
    for f in (C.g_indicadores, C.g_universitario, C.g_gasto_real, C.g_copa, C.g_percepcion,
              C.g_cascada, C.g_escenarios, C.g_rigidez, C.g_reformista, C.g_tornado, C.g_obra,
              C.g_reparto, C.g_funcion, C.g_variacion, C.g_empleo, C.g_gas, C.g_dots):
        # el de funciones lleva rotulos largos a la izquierda: se dibuja mas angosto para que,
        # con ellos, entre en la caja sin achicarse
        C.W = (430 if f is C.g_funcion else 482) / 72.0
        f()
