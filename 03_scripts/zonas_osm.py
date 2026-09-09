#!/usr/bin/env python3
"""
LAS ZONAS, A PARTIR DE LOS LIMITES DE OPENSTREETMAP

    python3 03_scripts/zonas_osm.py

Reemplaza a zonas.py, que hacia crecer seis semillas BAHRA por radios vecinos
hasta equilibrar poblacion.

--------------------------------------------------------------------------
POR QUE SE CAMBIO
--------------------------------------------------------------------------
El metodo anterior optimizaba lo que se le pidio —seis zonas de poblacion
pareja, entre 41.213 y 55.157 habitantes— y para lograrlo tuvo que estirar las
zonas costeras hacia el oeste. El resultado no era un mapa: Acassuso, una
localidad costera chica entre Martinez y San Isidro, terminaba midiendo el 87%
del ancho del partido y llegando hasta el limite oeste, a diez kilometros del
rio. San Isidro y Beccar quedaban sin costa. El punto mas al norte del partido,
que limita con San Fernando, caia en San Isidro y no en Beccar.

Nadie lo habia verificado nunca contra un mapa base.

**El equilibrio poblacional nunca fue necesario.** La formula de reparto del
capitulo 4 ya pondera por poblacion y por necesidad: zonas desparejas no rompen
nada, porque la formula les da montos distintos y eso es exactamente lo que
hace. Asi que la restriccion se da vuelta: la geografia manda, y la poblacion
es un resultado que se reporta, no una meta que se persigue.

--------------------------------------------------------------------------
DE DONDE SALEN LOS LIMITES AHORA
--------------------------------------------------------------------------
De OpenStreetMap, que tiene las seis localidades del partido mapeadas como
relaciones administrativas con poligono:

    San Isidro       relation 1877221
    Beccar           relation 1770851
    Martinez         relation 1770849
    Acassuso         relation 1877206
    Boulogne Sur Mer relation 1770848
    Villa Adelina    relation 1770850

Cualquiera puede abrirlas. **OSM no es fuente oficial** y el documento lo dice
en el anexo, en la nota del capitulo 4 y al pie de los exhibits 15 y 16. Aun
asi es mejor que lo anterior: se pasa de "los limites son nuestros" a "los
limites son de una fuente publica que cualquiera puede verificar".

La capa es sana: cubre el 99,63% del partido, las seis no se solapan entre si,
y los 360 radios censales caen cada uno dentro de exactamente un poligono.

--------------------------------------------------------------------------
LA REGLA DE ASIGNACION, Y EL DESEMPATE
--------------------------------------------------------------------------
Cada radio va a la localidad que contiene su PUNTO REPRESENTATIVO. El punto
representativo, y no el centroide, porque en un poligono con forma de L el
centroide puede caer afuera.

Desempate, para el 0,37% del partido que la capa no cubre: si un radio no cae
dentro de ninguna de las seis, va a la localidad mas cercana por distancia
desde ese mismo punto. **Hoy no se usa —los 360 caen dentro— y se documenta
igual**, porque una regla decidida sobre la marcha el dia que haga falta no es
una regla.

El resultado sigue siendo una union de radios censales enteros, asi que los
indicadores se agregan sin partir ninguno y el resto del pipeline no cambia.
"""

import csv
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DATA = os.path.join(RAIZ, "data")

FUENTE_OSM = ("OpenStreetMap, relaciones administrativas de localidad "
              "(no es fuente oficial)")
FUENTE_CENSO = ("INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022, "
                "procesado con Redatam 7")

RELACIONES = {
    "San Isidro": 1877221, "Beccar": 1770851, "Martinez": 1770849,
    "Acassuso": 1877206, "Boulogne Sur Mer": 1770848, "Villa Adelina": 1770850,
}

# Los cuatro indicadores que entran al indice de necesidad del capitulo 4, con
# las columnas del censo que los componen y su total.
CARENCIAS = [
    ("nbi", ["hogares_nbi__si"], "hogares_nbi__total"),
    ("sin_cloaca", ["hogares_desague__a_camara_septica_y_pozo_ciego",
                    "hogares_desague__solo_a_pozo_ciego",
                    "hogares_desague__a_hoyo_excavacion_en_la_tierra_etc"],
     "hogares_desague__total"),
    ("sin_gas_red", ["hogares_combustible__electricidad",
                     "hogares_combustible__gas_en_garrafa",
                     "hogares_combustible__gas_en_tubo_o_a_granel_zeppelin",
                     "hogares_combustible__lena_o_carbon",
                     "hogares_combustible__otro_combustible"],
     "hogares_combustible__total"),
    ("hacinamiento", ["hogares_hacinamiento__2_00_3_00_personas_por_cuarto",
                      "hogares_hacinamiento__mas_de_3_00_personas_por_cuarto"],
     "hogares_hacinamiento__total"),
]
EDUCACION = (["educacion_mni__universitario_completo",
              "educacion_mni__posgrado_incompleto",
              "educacion_mni__posgrado_completo"], "educacion_mni__total")


def _num(fila, col):
    return int(float(fila.get(col) or 0))


def asignar():
    """{radio_id: zona}, y la lista de los que necesitaron el desempate."""
    import geopandas as gpd

    osm = gpd.read_file(os.path.join(DATA, "localidades_osm.geojson"))
    rad = gpd.read_file(os.path.join(DATA, "radios_censales_sanisidro.geojson"))

    pts = gpd.GeoDataFrame(rad[["radio_id"]],
                           geometry=rad.geometry.representative_point(),
                           crs=rad.crs)
    j = gpd.sjoin(pts, osm[["zona", "geometry"]], how="left", predicate="within")

    por_cercania = []
    for i, r in j[j["zona"].isna()].iterrows():
        d = osm.geometry.distance(r.geometry)
        j.loc[i, "zona"] = osm.loc[d.idxmin(), "zona"]
        por_cercania.append(r["radio_id"])

    return dict(zip(j["radio_id"], j["zona"])), por_cercania


def agregar(asignacion, censo):
    """Los totales de cada zona: poblacion, hogares, y cada carencia CONTADA."""
    z = {}
    for radio, zona in asignacion.items():
        f = censo.get(radio)
        if not f:
            continue
        d = z.setdefault(zona, {"radios": 0, "poblacion": 0, "hogares": 0,
                                "viviendas": 0, "univ": 0, "univ_total": 0})
        d["radios"] += 1
        d["poblacion"] += _num(f, "poblacion_sexo__total")
        d["hogares"] += _num(f, "hogares_nbi__total")
        d["viviendas"] += _num(f, "viviendas_tipo__total")
        d["univ"] += sum(_num(f, c) for c in EDUCACION[0])
        d["univ_total"] += _num(f, EDUCACION[1])
        for nombre, cols, total in CARENCIAS:
            d[nombre] = d.get(nombre, 0) + sum(_num(f, c) for c in cols)
            d[nombre + "_total"] = d.get(nombre + "_total", 0) + _num(f, total)
    return z


def main():
    censo_path = os.path.join(DATA, "censo2022_sanisidro_por_radio.csv")
    with open(censo_path, encoding="utf-8-sig") as f:
        censo = {r["radio_id"]: r for r in csv.DictReader(f)}

    asignacion, por_cercania = asignar()
    z = agregar(asignacion, censo)

    print("=" * 74)
    print("ZONAS DESDE LOS LIMITES DE OPENSTREETMAP")
    print("=" * 74)
    print("  radios asignados      : %d" % len(asignacion))
    print("  dentro de un poligono : %d" % (len(asignacion) - len(por_cercania)))
    print("  por la regla de cercania: %d %s"
          % (len(por_cercania), por_cercania or ""))
    print()

    pct = lambda a, b: round(100.0 * a / b, 2) if b else 0.0
    filas = sorted(z.items(), key=lambda kv: -kv[1]["poblacion"])
    print("  %-18s %6s %8s %8s %6s %6s %6s %6s %6s"
          % ("ZONA", "radios", "poblac", "hogares", "NBI%", "clo%", "gas%",
             "hac%", "uni%"))
    for n, d in filas:
        print("  %-18s %6d %8d %8d %6.2f %6.2f %6.2f %6.2f %6.2f"
              % (n, d["radios"], d["poblacion"], d["hogares"],
                 pct(d["nbi"], d["nbi_total"]),
                 pct(d["sin_cloaca"], d["sin_cloaca_total"]),
                 pct(d["sin_gas_red"], d["sin_gas_red_total"]),
                 pct(d["hacinamiento"], d["hacinamiento_total"]),
                 pct(d["univ"], d["univ_total"])))

    # --- zonas_asignacion_radios.csv ---
    ruta = os.path.join(DATA, "zonas_asignacion_radios.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["radio_id", "fraccion", "zona", "poblacion", "nbi_pct",
                    "relacion_osm", "asignado_por", "fuente_limites",
                    "fuente_datos"])
        for radio in sorted(asignacion):
            fila = censo.get(radio, {})
            nbi_t = _num(fila, "hogares_nbi__total")
            w.writerow([radio, radio[6:8], asignacion[radio],
                        _num(fila, "poblacion_sexo__total"),
                        pct(_num(fila, "hogares_nbi__si"), nbi_t),
                        RELACIONES[asignacion[radio]],
                        "cercania" if radio in por_cercania else "contiene",
                        FUENTE_OSM, FUENTE_CENSO])
    print("\n  -> %s" % ruta)

    # --- zonas_indicadores.csv ---
    ruta = os.path.join(DATA, "zonas_indicadores.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["orden_peor_a_mejor", "zona", "relacion_osm", "radios",
                    "poblacion", "hogares", "viviendas",
                    "nbi", "sin_cloaca", "sin_gas_red", "hacinamiento",
                    "pct_nbi", "pct_sin_cloaca", "pct_sin_gas_red",
                    "pct_hacinamiento", "pct_edu_universitaria_completa_o_mas",
                    "fuente_limites", "fuente_datos"])
        peor = sorted(z.items(),
                      key=lambda kv: -pct(kv[1]["nbi"], kv[1]["nbi_total"]))
        for i, (n, d) in enumerate(peor, 1):
            w.writerow([i, n, RELACIONES[n], d["radios"], d["poblacion"],
                        d["hogares"], d["viviendas"],
                        d["nbi"], d["sin_cloaca"], d["sin_gas_red"],
                        d["hacinamiento"],
                        pct(d["nbi"], d["nbi_total"]),
                        pct(d["sin_cloaca"], d["sin_cloaca_total"]),
                        pct(d["sin_gas_red"], d["sin_gas_red_total"]),
                        pct(d["hacinamiento"], d["hacinamiento_total"]),
                        pct(d["univ"], d["univ_total"]),
                        FUENTE_OSM, FUENTE_CENSO])
    print("  -> %s" % ruta)

    # --- el geojson que dibujan los exhibits ---
    import geopandas as gpd
    osm = gpd.read_file(os.path.join(DATA, "localidades_osm.geojson"))
    osm["radios"] = osm["zona"].map(lambda n: z[n]["radios"])
    osm["poblacion"] = osm["zona"].map(lambda n: z[n]["poblacion"])
    osm["hogares"] = osm["zona"].map(lambda n: z[n]["hogares"])
    osm["pct_nbi"] = osm["zona"].map(
        lambda n: pct(z[n]["nbi"], z[n]["nbi_total"]))
    ruta = os.path.join(DATA, "zonas_propuestas_sanisidro.geojson")
    osm.to_file(ruta, driver="GeoJSON")
    print("  -> %s" % ruta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
