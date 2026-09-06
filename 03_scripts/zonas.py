#!/usr/bin/env python3
"""
Agrupacion de los radios censales de San Isidro en zonas vecinales.

POR QUE
  El anexo de zonas de la Ordenanza 6045/1984 no esta publicado. En vez de
  citar un anexo que nadie puede mostrar, la division se construye desde datos
  censales, con una regla escrita que cualquiera puede volver a correr.

LA REGLA, EN ORDEN
  1. Contiguidad. Dos radios son vecinos si sus poligonos comparten borde (no
     alcanza con tocarse en un punto). Toda zona tiene que ser una sola pieza.
  2. Localidades del partido. Cada radio va a la localidad donde esta la
     mayoria de sus viviendas particulares, segun VIVIENDA.CODLOC del Censo
     2022. Ninguna zona cruza el limite de una localidad.
  3. Tamano parecido. Dentro de cada localidad, los radios se parten en tantas
     zonas como haga falta para que todas queden cerca del mismo tamano.

COMO SE PARTE UNA LOCALIDAD
  Se calcula el eje principal de la localidad (la direccion en la que se
  estira, por componentes principales sobre los centroides en metros) y se
  crecen las zonas por adyacencia avanzando sobre ese eje, cortando cuando se
  llega a la cuota de poblacion. Crecer por adyacencia es lo que garantiza que
  cada zona quede de una sola pieza. Si igual queda un pedazo suelto, se pega
  a la zona vecina con la que comparte mas metros de borde.

  El eje principal no es una decision de diseno: es el resultado de la forma de
  la localidad. En San Isidro las localidades de la costa se estiran desde el
  rio hacia la Panamericana, asi que el corte natural separa el bajo del alto.

CUANTAS ZONAS
  Entre 6 y 12. Se prueba cada objetivo posible y se elige el que deja la
  relacion entre la zona mas grande y la mas chica mas cerca de 1. Si hay
  empate, gana el que tiene menos zonas. No hay ajuste a mano.

Uso:
    python3 03_scripts/zonas.py
"""

import csv
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")

ZONAS_MIN = 6
ZONAS_MAX = 12

# Metros: para centroides, ejes y longitud de bordes compartidos.
CRS_METRICO = "EPSG:32721"          # UTM 21S, cubre el AMBA
CRS_SALIDA = "EPSG:4326"

# Un borde compartido cuenta como vecindad a partir de este largo. Filtra los
# contactos de punta que no son frontera real.
BORDE_MINIMO_M = 1.0


class ErrorDeZonas(Exception):
    pass


# --------------------------------------------------------------------------

def leer():
    import geopandas as gpd
    geo = gpd.read_file(os.path.join(DATA, "radios_censales_sanisidro.geojson"))
    geo["radio_id"] = geo["radio_id"].astype(str)
    with open(os.path.join(DATA, "censo2022_sanisidro_por_radio.csv"),
              encoding="utf-8", newline="") as f:
        censo = {r["radio_id"]: r for r in csv.DictReader(f)}
    faltan = sorted(set(geo["radio_id"]) - set(censo))
    if faltan:
        raise ErrorDeZonas("radios sin fila en el censo: %s" % faltan[:5])
    return geo.to_crs(CRS_METRICO), censo


def _int(txt):
    txt = (txt or "").strip()
    return int(txt) if txt.lstrip("-").isdigit() else 0


def localidad_de_cada_radio(censo, cabecera):
    """
    La localidad de un radio es aquella donde esta la mayoria de sus viviendas
    particulares. Se lee de las columnas viviendas_localidad__*.
    """
    cols = [c for c in cabecera
            if c.startswith("viviendas_localidad__") and c != "viviendas_localidad__total"]
    if not cols:
        raise ErrorDeZonas("no hay columnas viviendas_localidad__* en el censo")
    salida = {}
    sin_dato = []
    for radio, fila in censo.items():
        conteos = [(_int(fila.get(c)), c) for c in cols]
        conteos.sort(key=lambda x: (-x[0], x[1]))
        if conteos[0][0] == 0:
            sin_dato.append(radio)
            salida[radio] = None
        else:
            salida[radio] = conteos[0][1][len("viviendas_localidad__"):]
    return salida, sin_dato, cols


def adyacencias(geo):
    """
    Grafo de vecindad por borde compartido, y los metros de borde de cada par.
    """
    import geopandas as gpd
    idx = {r: i for i, r in enumerate(geo["radio_id"])}
    vecinos = {r: set() for r in geo["radio_id"]}
    largos = {}
    sindex = geo.sindex
    for i, fila in geo.iterrows():
        a = fila.geometry
        for j in sindex.query(a, predicate="intersects"):
            if j <= i:
                continue
            b = geo.geometry.iloc[j]
            inter = a.intersection(b)
            largo = getattr(inter, "length", 0.0) or 0.0
            if largo < BORDE_MINIMO_M:
                continue
            ra, rb = geo["radio_id"].iloc[i], geo["radio_id"].iloc[j]
            vecinos[ra].add(rb)
            vecinos[rb].add(ra)
            largos[(ra, rb)] = largos[(rb, ra)] = largo
    return vecinos, largos


def componentes(nodos, vecinos):
    """Componentes conexas de un subconjunto de radios."""
    pendientes = set(nodos)
    salida = []
    while pendientes:
        semilla = min(pendientes)
        grupo, cola = {semilla}, [semilla]
        pendientes.discard(semilla)
        while cola:
            n = cola.pop()
            for v in sorted(vecinos[n]):
                if v in pendientes:
                    pendientes.discard(v)
                    grupo.add(v)
                    cola.append(v)
        salida.append(grupo)
    salida.sort(key=lambda g: (-len(g), min(g)))
    return salida


def eje_principal(coords):
    """
    Direccion en la que mas se estira la nube de centroides. Es el primer
    componente principal. El signo se fija para que apunte al este (y al norte
    si el eje fuera vertical), asi el resultado no depende del azar numerico.
    """
    import numpy as np
    c = np.asarray(coords, dtype=float)
    c = c - c.mean(axis=0)
    if len(c) < 2:
        return np.array([1.0, 0.0])
    _, _, vt = np.linalg.svd(c, full_matrices=False)
    v = vt[0]
    if abs(v[0]) > 1e-9:
        if v[0] < 0:
            v = -v
    elif v[1] < 0:
        v = -v
    return v


def partir_localidad(radios, k, poblacion, centroides, vecinos):
    """
    Parte los radios de una localidad en k zonas contiguas de poblacion
    parecida, creciendo por adyacencia a lo largo del eje principal.
    """
    import numpy as np
    if k <= 1:
        return [set(radios)]
    v = eje_principal([centroides[r] for r in radios])
    proy = {r: float(np.dot(centroides[r], v)) for r in radios}
    total = sum(poblacion[r] for r in radios)
    cuota = total / k

    libres = set(radios)
    zonas = []
    for n in range(k):
        if not libres:
            break
        if n == k - 1:
            zonas.append(set(libres))
            libres.clear()
            break
        semilla = min(libres, key=lambda r: (proy[r], r))
        zona = {semilla}
        libres.discard(semilla)
        acumulado = poblacion[semilla]
        frontera = {x for x in vecinos[semilla] if x in libres}
        while libres and acumulado < cuota and frontera:
            elegido = min(frontera, key=lambda r: (proy[r], r))
            frontera.discard(elegido)
            libres.discard(elegido)
            zona.add(elegido)
            acumulado += poblacion[elegido]
            frontera |= {x for x in vecinos[elegido] if x in libres}
        zonas.append(zona)
    return [z for z in zonas if z]


def reparar_contiguidad(asignacion, vecinos, largos):
    """
    Toda zona tiene que ser una sola pieza. Si a una le quedaron pedazos
    sueltos, cada pedazo se pega a la zona vecina con la que comparte mas
    metros de borde. Se repite hasta que no queda ninguno.
    """
    movidos = []
    for _ in range(200):
        por_zona = {}
        for radio, zona in asignacion.items():
            por_zona.setdefault(zona, set()).add(radio)
        suelto = None
        for zona, radios in sorted(por_zona.items()):
            comps = componentes(radios, vecinos)
            if len(comps) > 1:
                suelto = (zona, comps[1:])
                break
        if suelto is None:
            return movidos
        zona, pedazos = suelto
        for pedazo in pedazos:
            candidatos = {}
            for r in pedazo:
                for v in vecinos[r]:
                    z = asignacion[v]
                    if z != zona:
                        candidatos[z] = candidatos.get(z, 0.0) + largos[(r, v)]
            if not candidatos:
                raise ErrorDeZonas(
                    "el pedazo %s de la zona %s no toca ninguna otra zona"
                    % (sorted(pedazo)[:3], zona))
            destino = max(sorted(candidatos.items()), key=lambda x: x[1])[0]
            for r in pedazo:
                asignacion[r] = destino
            movidos.append((sorted(pedazo), zona, destino))
    raise ErrorDeZonas("la reparacion de contiguidad no converge")


def armar(geo, censo, localidades, vecinos, largos, objetivo):
    """Devuelve {radio: zona} para un objetivo de cantidad de zonas."""
    import numpy as np
    centroides = {r: (g.centroid.x, g.centroid.y)
                  for r, g in zip(geo["radio_id"], geo.geometry)}
    poblacion = {r: _int(censo[r]["poblacion_sexo__total"]) for r in censo}
    total = sum(poblacion.values())
    cuota = total / objetivo

    por_localidad = {}
    for radio, loc in localidades.items():
        por_localidad.setdefault(loc, []).append(radio)

    asignacion = {}
    for loc in sorted(por_localidad):
        radios = sorted(por_localidad[loc])
        pob = sum(poblacion[r] for r in radios)
        k = max(1, int(round(pob / cuota)))
        # Una localidad no puede partirse en mas pedazos que radios tiene.
        k = min(k, len(radios))
        piezas = partir_localidad(radios, k, poblacion, centroides, vecinos)
        for n, pieza in enumerate(piezas, 1):
            nombre = loc if len(piezas) == 1 else "%s %d" % (loc, n)
            for r in pieza:
                asignacion[r] = nombre
    movidos = reparar_contiguidad(asignacion, vecinos, largos)
    return asignacion, poblacion, movidos


def elegir_objetivo(geo, censo, localidades, vecinos, largos):
    """
    Prueba cada objetivo entre 6 y 12 y se queda con el que deja la relacion
    entre la zona mas grande y la mas chica mas cerca de 1.
    """
    ensayos = []
    for objetivo in range(ZONAS_MIN, ZONAS_MAX + 1):
        asignacion, poblacion, movidos = armar(
            geo, censo, localidades, vecinos, largos, objetivo)
        por_zona = {}
        for r, z in asignacion.items():
            por_zona[z] = por_zona.get(z, 0) + poblacion[r]
        n = len(por_zona)
        if not (ZONAS_MIN <= n <= ZONAS_MAX):
            ensayos.append((objetivo, n, None, "queda fuera de %d-%d zonas"
                            % (ZONAS_MIN, ZONAS_MAX)))
            continue
        ratio = max(por_zona.values()) / min(por_zona.values())
        ensayos.append((objetivo, n, ratio, ""))
    validos = [e for e in ensayos if e[2] is not None]
    if not validos:
        raise ErrorDeZonas("ningun objetivo entre %d y %d da un resultado valido"
                           % (ZONAS_MIN, ZONAS_MAX))
    mejor = min(validos, key=lambda e: (round(e[2], 6), e[1], e[0]))
    return mejor[0], ensayos
