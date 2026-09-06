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


# --------------------------------------------------------------------------
# Semillas: las 6 localidades oficiales del partido
# --------------------------------------------------------------------------
#
# Son los puntos de la capa sublocalidad_entidad_bahra del IGN (BAHRA, la base
# oficial de asentamientos que arman IGN e INDEC), con el mismo codigo que usa
# el nomenclador del INDEC. Estan copiados aca en vez de bajarlos en cada
# corrida porque son seis puntos que no cambian, y para que el script pueda
# correrse sin red. La descarga cruda queda en 01_raw/censo2022/.
#
# ES LO UNICO OFICIAL QUE HAY SOBRE LAS LOCALIDADES: son puntos, no poligonos.
# No existe limite publicado de ninguna de las seis.

SEMILLAS = [
    ("0675601005", "San Isidro",       -58.5112940171937, -34.4698826533230),
    ("0675601002", "Beccar",           -58.5313611443379, -34.4601958059158),
    ("0675601004", "Martinez",         -58.4993801358530, -34.4890104372004),
    ("0675601001", "Acassuso",         -58.5026800107625, -34.4782286640340),
    ("0675601003", "Boulogne Sur Mer", -58.5669108609788, -34.5094800482416),
    ("0675601006", "Villa Adelina",    -58.5473555040385, -34.5188556851314),
]

FUENTE_SEMILLAS = ("IGN/INDEC, BAHRA, capa sublocalidad_entidad_bahra, "
                   "departamento 06756")


def radios_semilla(geo):
    """
    El radio que contiene cada punto BAHRA. Si un punto cayera justo sobre un
    borde o fuera de todo radio, se toma el radio mas cercano y se avisa.
    """
    import geopandas as gpd
    from shapely.geometry import Point
    pts = gpd.GeoDataFrame(
        {"cod": [s[0] for s in SEMILLAS], "loc": [s[1] for s in SEMILLAS]},
        geometry=[Point(s[2], s[3]) for s in SEMILLAS],
        crs=CRS_SALIDA).to_crs(CRS_METRICO)

    salida, avisos = {}, []
    for _, p in pts.iterrows():
        dentro = geo[geo.geometry.contains(p.geometry)]
        if len(dentro) == 1:
            radio = dentro["radio_id"].iloc[0]
        else:
            d = geo.geometry.distance(p.geometry)
            radio = geo["radio_id"].iloc[int(d.idxmin())]
            avisos.append("el punto de %s no cae dentro de un unico radio; se "
                          "usa el mas cercano, %s" % (p["loc"], radio))
        if radio in salida.values():
            raise ErrorDeZonas("dos localidades comparten el radio semilla %s"
                               % radio)
        salida[p["loc"]] = radio
    return salida, avisos


# --------------------------------------------------------------------------
# Crecimiento
# --------------------------------------------------------------------------

def crecer(semillas, poblacion, centroides, vecinos, geo_idx):
    """
    Las seis zonas crecen a la vez desde su semilla, radio por radio.

    En cada paso avanza la zona que MENOS poblacion acumulada tiene entre las
    que todavia tienen algun radio libre pegado. Esa zona se queda con el radio
    libre de su frontera cuyo centroide esta mas cerca del centroide de su
    propia semilla, en metros.

    Por que asi: crecer siempre la mas chica es lo que empareja el tamano sin
    que nadie elija nada, y tomar solo radios de la frontera es lo que
    garantiza que cada zona quede de una sola pieza.

    EMPATES. Se resuelven en este orden, y siempre dan el mismo resultado:
      1. Entre zonas empatadas en poblacion, avanza la de nombre alfabetico
         menor.
      2. Entre radios de la frontera empatados en distancia (hasta el
         milimetro), entra el de radio_id menor.
    Los radio_id son unicos, asi que nunca queda un empate sin resolver.
    """
    zonas = {loc: {r} for loc, r in semillas.items()}
    asignacion = {r: loc for loc, r in semillas.items()}
    acumulado = {loc: poblacion[semillas[loc]] for loc in semillas}
    frontera = {loc: {v for v in vecinos[semillas[loc]] if v not in asignacion}
                for loc in semillas}
    orden = []

    libres = len(poblacion) - len(semillas)
    while libres > 0:
        candidatas = [loc for loc in sorted(zonas)
                      if any(v not in asignacion for v in frontera[loc])]
        if not candidatas:
            break
        loc = min(candidatas, key=lambda z: (acumulado[z], z))
        origen = centroides[semillas[loc]]
        disponibles = [v for v in frontera[loc] if v not in asignacion]
        elegido = min(disponibles,
                      key=lambda r: (round(_dist(centroides[r], origen), 3), r))
        zonas[loc].add(elegido)
        asignacion[elegido] = loc
        acumulado[loc] += poblacion[elegido]
        frontera[loc] |= {v for v in vecinos[elegido] if v not in asignacion}
        orden.append((elegido, loc))
        libres -= 1

    sueltos = [r for r in poblacion if r not in asignacion]
    if sueltos:
        raise ErrorDeZonas(
            "quedaron %d radios sin zona; no son alcanzables por adyacencia "
            "desde ninguna semilla: %s" % (len(sueltos), sorted(sueltos)[:5]))
    return asignacion, orden


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def verificar(asignacion, vecinos, radios, semillas):
    """Las tres validaciones que pide la tarea. Cualquiera que falle corta."""
    problemas = []

    sin_zona = [r for r in radios if r not in asignacion]
    if sin_zona:
        problemas.append("%d radios sin zona: %s"
                         % (len(sin_zona), sin_zona[:5]))
    de_mas = [r for r in asignacion if r not in set(radios)]
    if de_mas:
        problemas.append("hay zonas con radios que no son del partido: %s"
                         % de_mas[:5])

    por_zona = {}
    for r, z in asignacion.items():
        por_zona.setdefault(z, set()).add(r)
    for zona in sorted(por_zona):
        comps = componentes(por_zona[zona], vecinos)
        if len(comps) > 1:
            problemas.append(
                "la zona %s no es contigua: quedo en %d pedazos (%s)"
                % (zona, len(comps), [len(c) for c in comps]))
    if len(por_zona) != len(semillas):
        problemas.append("se esperaban %d zonas y hay %d"
                         % (len(semillas), len(por_zona)))
    if problemas:
        raise ErrorDeZonas("\n".join("  " + p for p in problemas))
    return por_zona
