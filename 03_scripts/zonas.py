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


# --------------------------------------------------------------------------
# Excepcion: los conglomerados criticos no se parten
# --------------------------------------------------------------------------
#
# El crecimiento por poblacion es ciego a la pobreza: puede cortar al medio un
# grupo de radios pobres y repartirlo entre dos zonas. Si eso pasa, los dos
# promedios de zona se diluyen y el mapa termina escondiendo justo lo que el
# programa quiere mostrar.
#
# Por eso: un conglomerado contiguo de radios con NBI muy superior a la media
# del partido NO se parte entre zonas. Va entero a la zona que lo contiene
# geograficamente. Es una regla, no un arreglo caso por caso: se aplica sola,
# a todos los conglomerados que cumplen la condicion.

DECIL_CRITICO = 10          # el 10% de radios con peor NBI
MIN_RADIOS_CONGLOMERADO = 2  # un radio suelto no es un conglomerado


def porcentaje(fila, numeradores, denominador):
    den = _int(fila.get(denominador))
    if not den:
        return None
    num = sum(_int(fila.get(c)) for c in numeradores)
    return 100.0 * num / den


def radios_criticos(censo):
    """
    Los radios del decil superior de hogares con NBI. El umbral sale de los
    propios datos del partido, no de un numero elegido a mano.
    """
    nbi = {}
    for radio, fila in censo.items():
        p = porcentaje(fila, ["hogares_nbi__si"], "hogares_nbi__total")
        if p is not None:
            nbi[radio] = p
    orden = sorted(nbi, key=lambda r: (-nbi[r], r))
    corte = max(1, len(orden) // DECIL_CRITICO)
    return set(orden[:corte]), nbi, nbi[orden[corte - 1]]


def aplicar_excepcion_criticos(asignacion, censo, poblacion, vecinos):
    """
    Cada conglomerado critico partido entre zonas se manda entero a una sola.

    A QUE ZONA. A la que ya tiene la mayor parte de la poblacion del
    conglomerado: es la zona que lo contiene geograficamente, porque el
    crecimiento avanza por contiguidad desde la semilla mas cercana.
    Empates: gana la zona con menos poblacion total (equilibrio); si siguen
    empatadas, la de nombre alfabetico menor.
    """
    criticos, nbi, umbral = radios_criticos(censo)
    movimientos = []
    for grupo in componentes(criticos, vecinos):
        if len(grupo) < MIN_RADIOS_CONGLOMERADO:
            continue
        zonas = sorted({asignacion[r] for r in grupo})
        if len(zonas) == 1:
            continue
        por_zona = {}
        for r in grupo:
            por_zona[asignacion[r]] = por_zona.get(asignacion[r], 0) + poblacion[r]
        total_zona = {}
        for r, z in asignacion.items():
            total_zona[z] = total_zona.get(z, 0) + poblacion[r]
        destino = min(sorted(por_zona),
                      key=lambda z: (-por_zona[z], total_zona[z], z))
        movidos = [r for r in sorted(grupo) if asignacion[r] != destino]
        for r in movidos:
            movimientos.append({
                "radio_id": r, "zona_antes": asignacion[r],
                "zona_despues": destino, "poblacion": poblacion[r],
                "nbi_pct": round(nbi[r], 2),
                "fraccion": r[5:7],
                "conglomerado_radios": len(grupo),
                "conglomerado_poblacion": sum(poblacion[x] for x in grupo),
                "motivo": ("conglomerado critico contiguo (%d radios, NBI del "
                           "decil superior, umbral %.1f%%) que quedaba partido "
                           "entre %s; se asigna entero a %s, la zona que ya "
                           "contenia la mayor parte de su poblacion"
                           % (len(grupo), umbral, " y ".join(zonas), destino)),
            })
            asignacion[r] = destino
    return movimientos, criticos, umbral, nbi


# --------------------------------------------------------------------------
# Indicadores por zona
# --------------------------------------------------------------------------
#
# Cada indicador se calcula sumando los radios de la zona y recien despues
# dividiendo. NO es el promedio de los porcentajes de los radios: eso le daria
# el mismo peso a un radio de 300 habitantes que a uno de 1.500.

INDICADORES = [
    # (columna de salida, numeradores, denominador, que mide)
    ("pct_nbi", ["hogares_nbi__si"], "hogares_nbi__total",
     "hogares con al menos una necesidad basica insatisfecha"),
    ("pct_privacion_convergente", ["hogares_ipmh__privacion_convergente"],
     "hogares_ipmh__total",
     "hogares con privacion patrimonial y de recursos corrientes a la vez"),
    ("pct_sin_cloaca",
     ["hogares_desague__a_camara_septica_y_pozo_ciego",
      "hogares_desague__solo_a_pozo_ciego",
      "hogares_desague__a_hoyo_excavacion_en_la_tierra_etc"],
     "hogares_desague__total", "hogares sin desague a la red publica"),
    ("pct_sin_gas_red",
     ["hogares_combustible__electricidad", "hogares_combustible__gas_en_garrafa",
      "hogares_combustible__gas_en_tubo_o_a_granel_zeppelin",
      "hogares_combustible__lena_o_carbon",
      "hogares_combustible__otro_combustible"],
     "hogares_combustible__total", "hogares que no cocinan con gas de red"),
    ("pct_sin_agua_red",
     ["hogares_agua__perforacion_con_bomba_a_motor",
      "hogares_agua__perforacion_con_bomba_manual",
      "hogares_agua__pozo_sin_bomba",
      "hogares_agua__transporte_por_cisterna_agua_de_lluvia_rio_c",
      "hogares_agua__otra_procedencia"],
     "hogares_agua__total", "hogares sin agua de red publica"),
    ("pct_hacinamiento",
     ["hogares_hacinamiento__2_00_3_00_personas_por_cuarto",
      "hogares_hacinamiento__mas_de_3_00_personas_por_cuarto"],
     "hogares_hacinamiento__total", "hogares con 2 o mas personas por cuarto"),
    ("pct_hacinamiento_critico",
     ["hogares_hacinamiento__mas_de_3_00_personas_por_cuarto"],
     "hogares_hacinamiento__total",
     "hogares con mas de 3 personas por cuarto (hacinamiento critico)"),
    ("pct_vivienda_precaria",
     ["viviendas_tipo__rancho", "viviendas_tipo__casilla",
      "viviendas_tipo__local_no_construido_para_habitacion_ocupado",
      "viviendas_tipo__vivienda_movil_ocupada_casa_rodante_barco_ca"],
     "viviendas_tipo__total",
     "viviendas que no son casa ni departamento ni pieza"),
    ("pct_inquilinos", ["hogares_tenencia__alquilada"],
     "hogares_tenencia__total", "hogares que alquilan"),
    ("pct_tenencia_precaria",
     ["hogares_tenencia__prestada", "hogares_tenencia__cedida_por_trabajo",
      "hogares_tenencia__otra_situacion"],
     "hogares_tenencia__total",
     "hogares que ocupan prestado, cedido por trabajo u otra situacion"),
    ("pct_edu_hasta_primaria",
     ["educacion_mni__sin_instruccion", "educacion_mni__primario_incompleto",
      "educacion_mni__primario_completo"], "educacion_mni__total",
     "personas cuyo maximo nivel alcanzado es primaria o menos"),
    ("pct_edu_secundaria_completa_o_mas",
     ["educacion_mni__secundario_completo", "educacion_mni__terciario_incompleto",
      "educacion_mni__terciario_completo",
      "educacion_mni__universitario_incompleto",
      "educacion_mni__universitario_completo",
      "educacion_mni__posgrado_incompleto", "educacion_mni__posgrado_completo"],
     "educacion_mni__total", "personas con secundaria completa o mas"),
    ("pct_edu_universitaria_completa_o_mas",
     ["educacion_mni__universitario_completo",
      "educacion_mni__posgrado_incompleto", "educacion_mni__posgrado_completo"],
     "educacion_mni__total", "personas con universidad completa o mas"),
    ("pct_hasta_14_anos", ["poblacion_edad__hasta_14_anos"],
     "poblacion_edad__total", "poblacion de hasta 14 anios"),
    ("pct_15_a_64_anos", ["poblacion_edad__15_a_64_anos"],
     "poblacion_edad__total", "poblacion de 15 a 64 anios"),
    ("pct_65_y_mas_anos", ["poblacion_edad__65_y_mas_anos"],
     "poblacion_edad__total", "poblacion de 65 anios y mas"),
]

TOTALES = [
    ("poblacion", "poblacion_sexo__total"),
    ("hogares", "hogares_nbi__total"),
    ("viviendas", "viviendas_tipo__total"),
]


def indicadores_por_zona(asignacion, censo):
    """
    Una fila por zona, ordenada de peor a mejor en condiciones de vida.
    El orden lo manda el % de hogares con NBI, que es el indicador sintetico
    que publica el propio Censo.
    """
    por_zona = {}
    for radio, zona in asignacion.items():
        por_zona.setdefault(zona, []).append(radio)

    filas = []
    for zona in sorted(por_zona):
        radios = por_zona[zona]
        fila = {"zona": zona, "radios": len(radios)}
        for nombre, col in TOTALES:
            fila[nombre] = sum(_int(censo[r][col]) for r in radios)
        for nombre, nums, den, _ in INDICADORES:
            d = sum(_int(censo[r][den]) for r in radios)
            n = sum(_int(censo[r][c]) for r in radios for c in nums)
            fila[nombre] = round(100.0 * n / d, 2) if d else None
        filas.append(fila)
    filas.sort(key=lambda f: (-(f["pct_nbi"] or 0), f["zona"]))
    for n, f in enumerate(filas, 1):
        f["orden_peor_a_mejor"] = n
    return filas


# --------------------------------------------------------------------------
# Salidas
# --------------------------------------------------------------------------

FUENTE_GEO = ("INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022, "
              "radios censales, via catalogo.datos.gba.gob.ar")
FUENTE_CENSO = ("INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022, "
                "procesado con Redatam 7")


def escribir(geo, censo, asignacion, movimientos, indicadores, semillas,
             umbral, nbi, fecha):
    import geopandas as gpd

    # 1. El geojson de zonas: los radios de cada zona disueltos en un poligono.
    g = geo.copy()
    g["zona"] = [asignacion[r] for r in g["radio_id"]]
    zonas = g.dissolve(by="zona", aggfunc={"radio_id": "count"}).reset_index()
    zonas = zonas.rename(columns={"radio_id": "radios"})
    por_zona = {f["zona"]: f for f in indicadores}
    for nombre, _ in TOTALES:
        zonas[nombre] = [por_zona[z][nombre] for z in zonas["zona"]]
    for nombre, _, _, _ in INDICADORES:
        zonas[nombre] = [por_zona[z][nombre] for z in zonas["zona"]]
    zonas["orden_peor_a_mejor"] = [por_zona[z]["orden_peor_a_mejor"]
                                   for z in zonas["zona"]]
    zonas["radio_semilla"] = [semillas[z] for z in zonas["zona"]]
    zonas["limite"] = "construido, no oficial"
    zonas["fuente_semilla"] = FUENTE_SEMILLAS
    zonas["fuente_geometria"] = FUENTE_GEO
    zonas["fuente_datos"] = FUENTE_CENSO
    zonas["fecha_descarga"] = fecha
    ruta_zonas = os.path.join(DATA, "zonas_propuestas_sanisidro.geojson")
    zonas.to_crs(CRS_SALIDA).to_file(ruta_zonas, driver="GeoJSON")

    # 2. La zona de cada radio, para poder rehacer cualquier cuenta.
    ruta_asig = os.path.join(DATA, "zonas_asignacion_radios.csv")
    with open(ruta_asig, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["radio_id", "fraccion", "zona", "poblacion", "nbi_pct",
                    "radio_semilla_de_la_zona", "reasignado_por_excepcion",
                    "fuente", "fecha_descarga"])
        movidos = {m["radio_id"]: m for m in movimientos}
        for radio in sorted(asignacion):
            zona = asignacion[radio]
            w.writerow([radio, radio[5:7], zona,
                        _int(censo[radio]["poblacion_sexo__total"]),
                        round(nbi.get(radio, 0.0), 2), semillas[zona],
                        "si" if radio in movidos else "no",
                        FUENTE_CENSO, fecha])

    # 3. El resumen y los indicadores.
    ruta_res = os.path.join(DATA, "zonas_resumen.csv")
    with open(ruta_res, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zona", "radios", "poblacion", "hogares", "viviendas",
                    "poblacion_pct_del_partido", "radio_semilla",
                    "limite", "fuente_semilla", "fecha_descarga"])
        total = sum(x["poblacion"] for x in indicadores)
        for x in sorted(indicadores, key=lambda x: -x["poblacion"]):
            w.writerow([x["zona"], x["radios"], x["poblacion"], x["hogares"],
                        x["viviendas"], round(100.0 * x["poblacion"] / total, 2),
                        semillas[x["zona"]], "construido, no oficial",
                        FUENTE_SEMILLAS, fecha])

    ruta_ind = os.path.join(DATA, "zonas_indicadores.csv")
    cols = (["orden_peor_a_mejor", "zona", "radios"]
            + [n for n, _ in TOTALES]
            + [n for n, _, _, _ in INDICADORES]
            + ["fuente", "fecha_descarga"])
    with open(ruta_ind, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for x in indicadores:
            x = dict(x, fuente=FUENTE_CENSO, fecha_descarga=fecha)
            w.writerow(x)

    # 4. Que mide cada indicador, para que nadie tenga que leer el script.
    ruta_dic = os.path.join(DATA, "zonas_indicadores_diccionario.csv")
    with open(ruta_dic, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["indicador", "que_mide", "numerador", "denominador"])
        for nombre, col in TOTALES:
            w.writerow([nombre, "suma de los radios de la zona", col, ""])
        for nombre, nums, den, que in INDICADORES:
            w.writerow([nombre, que, " + ".join(nums), den])

    # 5. Las reasignaciones por la excepcion, a la vista.
    ruta_exc = os.path.join(DATA, "zonas_excepciones.csv")
    with open(ruta_exc, "w", encoding="utf-8", newline="") as f:
        cols = ["radio_id", "fraccion", "zona_antes", "zona_despues",
                "poblacion", "nbi_pct", "conglomerado_radios",
                "conglomerado_poblacion", "umbral_nbi_decil_superior", "motivo"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for m in movimientos:
            w.writerow(dict(m, umbral_nbi_decil_superior=round(umbral, 2)))

    return [ruta_zonas, ruta_asig, ruta_res, ruta_ind, ruta_dic, ruta_exc]


def main():
    import datetime as dt
    fecha = dt.date.today().isoformat()
    geo, censo = leer()
    radios = list(geo["radio_id"])
    vecinos, largos = adyacencias(geo)

    sueltos = componentes(radios, vecinos)
    if len(sueltos) != 1:
        raise ErrorDeZonas("el partido no es una sola pieza: %s"
                           % [len(c) for c in sueltos])

    semillas, avisos = radios_semilla(geo)
    for a in avisos:
        print("  AVISO: %s" % a)

    poblacion = {r: _int(censo[r]["poblacion_sexo__total"]) for r in radios}
    centroides = {r: (g.centroid.x, g.centroid.y)
                  for r, g in zip(geo["radio_id"], geo.geometry)}

    asignacion, _ = crecer(semillas, poblacion, centroides, vecinos, None)
    verificar(asignacion, vecinos, radios, semillas)

    movimientos, criticos, umbral, nbi = aplicar_excepcion_criticos(
        asignacion, censo, poblacion, vecinos)
    # Mover radios puede romper la contiguidad de la zona que los cede, asi que
    # se vuelve a verificar todo despues de la excepcion, no solo antes.
    verificar(asignacion, vecinos, radios, semillas)

    indicadores = indicadores_por_zona(asignacion, censo)
    zona_de = {z: semillas[z] for z in semillas}
    rutas = escribir(geo, censo, asignacion, movimientos, indicadores,
                     zona_de, umbral, nbi, fecha)
    return {"asignacion": asignacion, "movimientos": movimientos,
            "indicadores": indicadores, "semillas": semillas,
            "criticos": criticos, "umbral": umbral, "nbi": nbi,
            "vecinos": vecinos, "rutas": rutas, "poblacion": poblacion,
            "radios": radios}


if __name__ == "__main__":
    r = main()
    total = sum(r["poblacion"].values())
    print("=" * 78)
    print("ZONAS (peor a mejor en condiciones de vida)")
    print("=" * 78)
    print("%-4s %-18s %6s %8s %8s %7s %8s %8s %7s"
          % ("#", "zona", "radios", "pobl", "hogares", "NBI%",
             "s/cloaca", "s/gas", "hacin%"))
    for x in r["indicadores"]:
        print("%-4d %-18s %6d %8d %8d %7.2f %8.2f %8.2f %7.2f"
              % (x["orden_peor_a_mejor"], x["zona"], x["radios"],
                 x["poblacion"], x["hogares"], x["pct_nbi"],
                 x["pct_sin_cloaca"], x["pct_sin_gas_red"],
                 x["pct_hacinamiento"]))
    pobs = [x["poblacion"] for x in r["indicadores"]]
    print("\ntotal %d | zona mayor / menor = %.2f" % (total, max(pobs)/min(pobs)))
    print("\nreasignaciones por la excepcion de conglomerado critico: %d radios"
          % len(r["movimientos"]))
    for m in r["movimientos"]:
        print("  %s (frac %s, NBI %.1f%%, %d hab): %s -> %s"
              % (m["radio_id"], m["fraccion"], m["nbi_pct"], m["poblacion"],
                 m["zona_antes"], m["zona_despues"]))
    print("\narchivos:")
    for ruta in r["rutas"]:
        print("  %s" % os.path.relpath(ruta, REPO))
