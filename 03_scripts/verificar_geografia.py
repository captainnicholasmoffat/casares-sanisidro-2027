#!/usr/bin/env python3
"""
SEPTIMO VERIFICADOR — la geografia cae donde dice

    python3 03_scripts/verificar_geografia.py
    -> 0 si las cinco referencias se cumplen, 1 si alguna falla.

Por que existe
--------------
Las zonas anteriores se generaron haciendo crecer seis semillas por radios
vecinos hasta equilibrar poblacion. Nadie verifico nunca el resultado contra el
territorio: Acassuso, una localidad costera chica, terminaba midiendo el 87%
del ancho del partido; San Isidro y Beccar quedaban sin costa; el punto mas al
norte, que limita con San Fernando, caia en San Isidro y no en Beccar.

Tres fallas de cinco, visibles a simple vista en cuanto alguien superpuso el
mapa sobre un callejero, y ninguno de los seis verificadores anteriores podia
verlas: miden color, desborde, colisiones, tildes, texto tapado y numeros
escritos a mano. **Ninguno miraba si un poligono cae donde dice.**

Las cinco referencias
---------------------
Son hechos del territorio que no se discuten:

  1. El Rio de la Plata esta al noreste. San Isidro, Beccar, Acassuso y
     Martinez llegan a la costa.
  2. Boulogne Sur Mer y Villa Adelina son el oeste, sin costa.
  3. Beccar es la zona mas al norte: limita con San Fernando.
  4. Martinez es la mas al sur de la franja costera: limita con Vicente Lopez.
  5. Ninguna zona puede ser desmedida: el limite es el 70% del ancho del
     partido, y la que fallaba media el 87%.

EL TEST DE COSTA VA POR BANDA DE LATITUD
----------------------------------------
La primera version comparaba cada zona contra el punto MAS AL ESTE del partido,
que esta en la banda de Martinez, donde la costa hace una saliente. Con ese
criterio San Isidro y Beccar daban "sin costa" siendo que llegan al rio: estan
mas al norte, donde la ribera corre mas al oeste.

Un verificador que da falso negativo ensena a ignorarlo, asi que la costa se
mide contra el borde este del partido EN LA MISMA BANDA DE LATITUD que la zona.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(AQUI), "data")

COSTERAS = {"San Isidro", "Beccar", "Acassuso", "Martinez"}
INTERIORES = {"Boulogne Sur Mer", "Villa Adelina"}
MAS_AL_NORTE = "Beccar"
MAS_AL_SUR_COSTERA = "Martinez"
ANCHO_MAXIMO = 0.70          # del ancho del partido
TOLERANCIA_COSTA_M = 600     # margen contra el borde este de su banda
LARGO_COSTA_M = 400          # metros minimos de ribera para contar como costera


def _costa(partido, vecinos, holgura=250.0):
    """La linea de costa: el borde del partido que NO comparte con un vecino.

    San Isidro limita con San Fernando, Tigre, General San Martin y Vicente
    Lopez, y con el Rio de la Plata. Lo que queda del contorno despues de
    descontar los cuatro vecinos es el rio, por descarte.

    Definir la costa como "el borde este del partido" era mas simple y estaba
    mal: en la punta sur el borde este es Vicente Lopez, y Villa Adelina —que
    no tiene costa— daba costa por eso.

    holgura en metros: los contornos de dos partidos vecinos no coinciden al
    milimetro entre relaciones de OSM distintas.
    """
    grados = holgura / 91000.0
    borde = partido.boundary
    for v in vecinos.geometry:
        borde = borde.difference(v.buffer(grados))
    return borde


def verificar():
    import geopandas as gpd

    z = gpd.read_file(os.path.join(DATA, "zonas_propuestas_sanisidro.geojson"))
    z = z.set_index("zona")
    partido = z.geometry.union_all()
    vecinos = gpd.read_file(os.path.join(DATA, "partidos_vecinos_osm.geojson"))
    costa = _costa(partido, vecinos)
    minx, _, maxx, _ = partido.bounds
    ancho = maxx - minx
    fallas = []

    print("=" * 74)
    print("VERIFICADOR 7 — la geografia cae donde dice")
    print("=" * 74)

    # --- 1 y 2. costa, medida en la banda de latitud de cada zona ---
    print("\n  COSTA (borde del partido que no comparte con ningun vecino)")
    tol = TOLERANCIA_COSTA_M / 91000.0
    for n, g in z.geometry.items():
        largo = g.buffer(tol).intersection(costa).length * 91000
        toca = largo >= LARGO_COSTA_M
        debe = n in COSTERAS
        ok = toca == debe
        if not ok:
            fallas.append("%s %s costa (%.0f m de ribera, minimo %.0f)"
                          % (n, "deberia tener" if debe else "no deberia tener",
                             largo, LARGO_COSTA_M))
        print("    %-18s %-9s %6.0f m de ribera  esperado %-9s %s"
              % (n, "costa" if toca else "sin costa", largo,
                 "costa" if debe else "sin costa", "OK" if ok else "FALLA"))

    # --- 3. Beccar es la mas al norte ---
    norte = max(z.index, key=lambda k: z.geometry[k].bounds[3])
    ok = norte == MAS_AL_NORTE
    if not ok:
        fallas.append("la zona mas al norte es %s y deberia ser %s" % (norte, MAS_AL_NORTE))
    print("\n  MAS AL NORTE (limita con San Fernando)")
    print("    %-18s esperado %-18s %s" % (norte, MAS_AL_NORTE, "OK" if ok else "FALLA"))

    # --- 4. Martinez es la mas al sur de las costeras ---
    sur = min((k for k in z.index if k in COSTERAS),
              key=lambda k: z.geometry[k].bounds[1])
    ok = sur == MAS_AL_SUR_COSTERA
    if not ok:
        fallas.append("la costera mas al sur es %s y deberia ser %s"
                      % (sur, MAS_AL_SUR_COSTERA))
    print("\n  MAS AL SUR DE LA FRANJA COSTERA (limita con Vicente Lopez)")
    print("    %-18s esperado %-18s %s" % (sur, MAS_AL_SUR_COSTERA, "OK" if ok else "FALLA"))

    # --- 5. ninguna zona desmedida ---
    print("\n  COMPACIDAD (ancho de cada zona sobre el ancho del partido)")
    for n, g in z.geometry.items():
        a, _, c, _ = g.bounds
        frac = (c - a) / ancho
        ok = frac <= ANCHO_MAXIMO
        if not ok:
            fallas.append("%s mide el %.0f%% del ancho del partido (maximo %.0f%%)"
                          % (n, frac * 100, ANCHO_MAXIMO * 100))
        print("    %-18s %3.0f%%  %s" % (n, frac * 100, "OK" if ok else "FALLA"))

    print()
    if fallas:
        print("FALLA: %d referencia(s) geografica(s) no se cumplen." % len(fallas))
        for f in fallas:
            print("   ", f)
        return 1
    print("Las cinco referencias geograficas se cumplen.")
    return 0


if __name__ == "__main__":
    sys.exit(verificar())
