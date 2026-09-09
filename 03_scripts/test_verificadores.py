#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOS VERIFICADORES DE FIGURA, PROBADOS CONTRA EL ERROR QUE LOS ORIGINO

    python3 03_scripts/test_verificadores.py

Un verificador que nunca vio fallar a nadie no sirve de nada: no se sabe si
pasa porque el grafico esta bien o porque el verificador no mira. Cada prueba
de aca arma a proposito la figura rota que el verificador tiene que denunciar,
comprueba que la denuncia, y despues arma la version arreglada y comprueba que
se calle.

El caso del EXHIBIT 11 es el motivo de que este archivo exista. El grafico
salio publicado con tres rotulos derramados sobre los tramos vecinos —se leia
"ontratos de servicio", sin la C— y los siete verificadores que habia dijeron
OK, cada uno por un motivo distinto y cada uno con razon:

  - verificar_colisiones mide texto contra TEXTO, y los tres rotulos no se
    tocaban entre si: se derramaban sobre BARRAS;
  - verificar_texto_tapado mide el texto contra lo que tiene DEBAJO en el mismo
    punto, y en el centro del tramo el contraste estaba bien: el problema
    estaba en las puntas;
  - verificar_desborde mide contra el borde del LIENZO, y el texto estaba
    holgadamente adentro de la imagen.

De ahi salio verificar_texto_derramado, el octavo, y de ahi sale esta prueba.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import estilo as E                                          # noqa: E402


def _barra_apilada(rotulo_adentro):
    """La barra apilada del EXHIBIT 11, con los rotulos donde se pidan.

    rotulo_adentro=True reproduce el error: cada nombre CENTRADO adentro de su
    tramo, mas ancho que el tramo. False es el arreglo: los nombres arriba.
    """
    fig, ax = E.figura(2.4)
    tramos = [("Personal y deuda no se tocan", 39.0, E.TINTA),
              ("Contratos de servicios no dentro del ejercicio", 34.1, E.CAL),
              ("Gasto flexible reasignable", 26.9, E.RIO)]
    izq = 0.0
    for etiqueta, v, color in tramos:
        ax.barh([0], [v], left=izq, height=0.3, color=color, zorder=3)
        if rotulo_adentro:
            ax.annotate(etiqueta, (izq + v / 2, 0), ha="center", va="center",
                        fontsize=6.4, weight="bold",
                        color=E.TINTA if color is E.CAL else E.PAPEL)
        else:
            ax.annotate(etiqueta, (izq, 0.2), xytext=(2, 3),
                        textcoords="offset points", ha="left", va="bottom",
                        fontsize=6.4, weight="bold", color=E.TINTA)
        izq += v
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 0.7)
    ax.set_yticks([])
    return fig


def test_derramado_denuncia_el_error_del_exhibit_11():
    fig = _barra_apilada(rotulo_adentro=True)
    fallas = E.verificar_texto_derramado(fig)
    assert fallas, ("el octavo verificador no vio el rotulo derramado: es "
                    "exactamente el error con el que salio publicado el "
                    "EXHIBIT 11")
    assert any("Contratos" in f for f in fallas), fallas
    return fallas


def test_derramado_se_calla_con_los_rotulos_afuera():
    fig = _barra_apilada(rotulo_adentro=False)
    fallas = E.verificar_texto_derramado(fig)
    assert not fallas, ("el verificador denuncia la version arreglada, o sea "
                        "que denunciaria cualquier cosa: %s" % fallas)


def test_derramado_perdona_el_sobrante_sobre_papel():
    """Salirse no alcanza: tiene que salirse ENCIMA de otra forma.

    "sin rendición" del EXHIBIT 01 va rotado adentro de una banda mas angosta
    que el alto de su linea, y sobresale unos pixeles a cada lado. Esos pixeles
    caen sobre el papel que separa dos barras, donde el texto se lee perfecto.
    Denunciarlo seria pedirle al grafico que se rompa para callar al verificador.
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5.33, 2.0), dpi=E.DPI)
    fig.patch.set_facecolor(E.PAPEL)
    ax.set_facecolor(E.PAPEL)
    ax.bar([0], [10], width=0.2, color=E.CAL, zorder=2)
    ax.text(0, 5, "sin rendición", ha="center", va="center", rotation=90,
            fontsize=5.6, color=E.TINTA)
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 12)
    fallas = E.verificar_texto_derramado(fig)
    assert not fallas, ("denuncia un sobrante que cae sobre papel: %s" % fallas)


def main():
    pruebas = [test_derramado_denuncia_el_error_del_exhibit_11,
               test_derramado_se_calla_con_los_rotulos_afuera,
               test_derramado_perdona_el_sobrante_sobre_papel]
    print("=" * 74)
    print("VERIFICADORES DE FIGURA — probados contra el error que los originó")
    print("=" * 74)
    malas = 0
    for t in pruebas:
        try:
            extra = t()
            print("  OK    %s" % t.__name__)
            if extra:
                for f in extra:
                    print("          denunció: %s" % f)
        except AssertionError as e:                          # pragma: no cover
            malas += 1
            print("  FALLA %s\n          %s" % (t.__name__, e))
    print("\n%d de %d" % (len(pruebas) - malas, len(pruebas)))
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main())
