#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOS DATOS DEL MAPA BASE — se bajan una vez y quedan en el repo

    python3 03_scripts/mapa_datos.py          # baja lo que falte y avisa

Los dos mapas del documento se dibujaban como poligonos planos sobre el vacio:
sin agua, sin vecinos, sin relieve y sin una sola referencia que le dijera al
lector donde esta parado. Este modulo trae lo que faltaba, y lo trae de fuentes
reales y citables. NINGUNA parte del mapa se inventa ni se genera: un mapa
generado es geograficamente falso, y un dato falso en un documento que se ofrece
para que le revisen las cuentas se lleva puesto todo lo demas.

QUE SE BAJA, Y DE DONDE
--------------------------------------------------------------------------
  agua         El poligono del Rio de la Plata, de OpenStreetMap via Nominatim.
               Se recorta al encuadre del mapa; no se dibuja de memoria.
  vias         La red vial principal —autopistas, troncales y avenidas— y el
               ferrocarril, de OpenStreetMap via Overpass. La Panamericana y el
               Mitre son las dos referencias que cualquier vecino ubica sin
               pensar, y el tren corre pegado a la barranca.
  relieve      Un modelo de elevacion, de las Terrain Tiles publicas de AWS
               (registro de datos abiertos, derivadas de SRTM y otras fuentes).
               Se baja el mosaico que cubre el partido y se guarda como un solo
               array de alturas en metros.

               ES LA BARRANCA. San Isidro se define por ese escalon: la ciudad
               alta arriba y la franja costera abajo. Dibujado como sombreado
               suave, el mapa deja de ser un rompecabezas de colores y pasa a
               tener la forma del terreno que explica el partido.

LOS LIMITES YA ESTABAN
--------------------------------------------------------------------------
data/localidades_osm.geojson y data/partidos_vecinos_osm.geojson vienen de
zonas_osm.py y no se tocan aca.

LO QUE SE BAJA SE VERSIONA
--------------------------------------------------------------------------
Queda en data/ y en 01_raw/relieve_srtm.npz, asi que el armado no necesita red.
Bajarlo de nuevo solo hace falta si se cambia el encuadre.
"""

import io
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")
CRUDO = os.path.join(REPO, "01_raw")

AGUA = os.path.join(DATA, "agua_rio_de_la_plata_osm.geojson")
VIAS = os.path.join(DATA, "vias_principales_osm.geojson")
RELIEVE = os.path.join(CRUDO, "relieve_srtm.npz")

# El encuadre: el partido y un margen de vecinos alrededor. En grados.
CAJA = (-58.62, -34.55, -58.40, -34.40)      # oeste, sur, este, norte
ZOOM_RELIEVE = 14                             # ~9,5 m por pixel a esta latitud

CABECERA = {"User-Agent": "casares-sanisidro-2027 (mapa base del programa de "
                          "gobierno; contacto via el repositorio)"}

# Overpass, para la red vial y ferroviaria. Se prueban varios espejos: el
# oficial no responde desde aca, kumi da 504, y overpass.osm.ch contesta 200
# pero con CERO elementos porque solo tiene datos de Suiza — un espejo que
# contesta bien y devuelve nada es peor que uno caido, asi que el que baja
# comprueba que efectivamente vengan trazas. La consulta queda escrita para que
# cualquiera la repita y obtenga lo mismo.
OVERPASS = ["https://maps.mail.ru/osm/tools/overpass/api/interpreter",
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter"]
CONSULTA_VIAS = """[out:json][timeout:120];
(
  way["highway"~"^(motorway|trunk|primary)$"](%(s)f,%(o)f,%(n)f,%(e)f);
  way["railway"="rail"](%(s)f,%(o)f,%(n)f,%(e)f);
);
out geom;"""

# Como se dibuja cada tipo. El orden es el de importancia en el mapa.
CLASE_VIA = {"motorway": "autopista", "trunk": "autopista",
             "primary": "avenida", "rail": "ferrocarril"}


def _nominatim(consulta):
    url = ("https://nominatim.openstreetmap.org/search?format=jsonv2"
           "&polygon_geojson=1&limit=3&q=" + urllib.parse.quote(consulta))
    pedido = urllib.request.Request(url, headers=CABECERA)
    with urllib.request.urlopen(pedido, timeout=60) as r:
        return json.load(r)


def bajar_agua():
    if os.path.exists(AGUA):
        return "ya estaba"
    for r in _nominatim("Río de la Plata"):
        g = r.get("geojson") or {}
        if g.get("type") in ("Polygon", "MultiPolygon"):
            with open(AGUA, "w", encoding="utf-8") as f:
                json.dump({"type": "FeatureCollection", "features": [
                    {"type": "Feature", "geometry": g,
                     "properties": {"nombre": "Río de la Plata",
                                    "osm_id": r.get("osm_id"),
                                    "fuente": "OpenStreetMap vía Nominatim"}}]},
                          f, ensure_ascii=False)
            return "bajado"
    raise RuntimeError("Nominatim no devolvió el polígono del Río de la Plata")


def bajar_vias():
    """La red vial y ferroviaria del encuadre, de Overpass.

    Nominatim devolvia un TRAMO suelto de cada calle —quinientos metros de la
    Panamericana— porque busca por nombre y contesta con el primer objeto que
    coincide. Para una referencia de mapa hace falta la traza entera, y eso lo
    da Overpass.

    El ferrocarril entra porque en San Isidro es una referencia tan fuerte como
    la Panamericana: el Mitre y el Tren de la Costa corren paralelos a la
    barranca y son el limite que todo el mundo usa para ubicarse.
    """
    if os.path.exists(VIAS):
        return "ya estaba"
    o, s_, e, n = CAJA
    consulta = CONSULTA_VIAS % {"o": o, "s": s_, "e": e, "n": n}
    datos = None
    for espejo in OVERPASS:
        try:
            pedido = urllib.request.Request(
                espejo, data=urllib.parse.urlencode({"data": consulta}).encode(),
                headers=CABECERA)
            with urllib.request.urlopen(pedido, timeout=200) as r:
                d = json.load(r)
            if d.get("elements"):
                datos = d
                break
        except Exception:
            continue
    if datos is None:
        raise RuntimeError("ningún espejo de Overpass devolvió vías")
    rasgos = []
    for el in datos.get("elements", []):
        geom = el.get("geometry")
        if not geom or len(geom) < 2:
            continue
        t = el.get("tags", {})
        clase = CLASE_VIA.get(t.get("highway") or ("rail" if t.get("railway")
                                                   else ""))
        if not clase:
            continue
        rasgos.append({
            "type": "Feature",
            "geometry": {"type": "LineString",
                         "coordinates": [[g["lon"], g["lat"]] for g in geom]},
            "properties": {"clase": clase, "nombre": t.get("name", ""),
                           "osm_way": el.get("id"),
                           "fuente": "OpenStreetMap vía Overpass"}})
    if not rasgos:                                        # pragma: no cover
        raise RuntimeError("Overpass no devolvió ninguna vía")
    with open(VIAS, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": rasgos}, f,
                  ensure_ascii=False)
    return "bajadas %d trazas" % len(rasgos)


def _xy(lat, lon, z):
    n = 2 ** z
    la = math.radians(lat)
    return ((lon + 180) / 360 * n,
            (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * n)


def bajar_relieve():
    """El mosaico de alturas que cubre el encuadre, en metros."""
    if os.path.exists(RELIEVE):
        return "ya estaba"
    import numpy as np
    from PIL import Image
    o, s, e, n = CAJA
    x0, y0 = _xy(n, o, ZOOM_RELIEVE)
    x1, y1 = _xy(s, e, ZOOM_RELIEVE)
    tx0, ty0, tx1, ty1 = int(x0), int(y0), int(x1), int(y1)
    ancho, alto = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    mosaico = Image.new("RGB", (ancho, alto))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            url = ("https://s3.amazonaws.com/elevation-tiles-prod/terrarium/"
                   "%d/%d/%d.png" % (ZOOM_RELIEVE, tx, ty))
            pedido = urllib.request.Request(url, headers=CABECERA)
            with urllib.request.urlopen(pedido, timeout=60) as r:
                tile = Image.open(io.BytesIO(r.read())).convert("RGB")
            mosaico.paste(tile, ((tx - tx0) * 256, (ty - ty0) * 256))
    a = np.asarray(mosaico).astype(np.float32)
    # El formato terrarium guarda la altura en el color: esta es su formula.
    altura = (a[:, :, 0] * 256 + a[:, :, 1] + a[:, :, 2] / 256) - 32768
    # Los bordes del mosaico en grados, que es lo que necesita imshow.
    n_t = 2 ** ZOOM_RELIEVE

    def lon_de(x):
        return x / n_t * 360 - 180

    def lat_de(y):
        return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n_t))))

    np.savez_compressed(
        RELIEVE, altura=altura.astype(np.float32),
        extent=np.array([lon_de(tx0), lon_de(tx1 + 1),
                         lat_de(ty1 + 1), lat_de(ty0)], dtype=np.float64),
        zoom=np.array([ZOOM_RELIEVE]))
    return "bajado %dx%d px" % (altura.shape[1], altura.shape[0])


def main():
    os.makedirs(CRUDO, exist_ok=True)
    print("=" * 74)
    print("DATOS DEL MAPA BASE")
    print("=" * 74)
    for nombre, fn in (("agua (Río de la Plata)", bajar_agua),
                       ("vías principales", bajar_vias),
                       ("relieve (Terrain Tiles de AWS)", bajar_relieve)):
        print("  %-34s %s" % (nombre, fn()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
