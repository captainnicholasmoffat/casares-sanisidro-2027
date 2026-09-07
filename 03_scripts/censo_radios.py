#!/usr/bin/env python3
"""
Censo 2022 por radio censal, partido de San Isidro.

QUE HACE
  1. Baja de catalogo.datos.gba.gob.ar la capa de radios censales del Censo
     2022 y recorta el partido de San Isidro.
  2. Consulta el motor Redatam del INDEC (redatam.indec.gob.ar) una vez por
     variable, con desagregacion por RADIO, y guarda cruda cada respuesta.
  3. Arma una tabla ancha por radio con poblacion, hogares, viviendas, NBI,
     IPMH, hacinamiento, tenencia, servicios, educacion y grupos de edad.

CODIGO DE PARTIDO
  San Isidro es PROV=06, DEPTO=756 -> 06756. No esta asumido: sale de la
  propia capa de la Provincia, donde NOMDEPTO='SAN ISIDRO'. Ver
  verificar_codigo_partido().

QUE NO HACE
  No estima, no interpola y no completa nada. Si una variable no vuelve para
  un radio, la celda queda vacia y el radio queda anotado. Ver
  data/NO_DISPONIBLE.md.

Uso:
    python3 03_scripts/censo_radios.py            # todo
    python3 03_scripts/censo_radios.py --sin-red  # con lo ya bajado
"""

import csv
import datetime as dt
import gzip
import hashlib
import html
import io
import json
import os
import re
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
RAW = os.path.join(REPO, "01_raw", "censo2022")
RAW_REDATAM = os.path.join(RAW, "redatam")
DATA = os.path.join(REPO, "data")

PROV = "06"
DEPTO = "756"
NOMBRE_PARTIDO = "SAN ISIDRO"
LINK_PREFIJO = PROV + DEPTO           # los LINK de radio son PROV+DEPTO+FRAC+RADIO

# Poblacion del partido segun el Censo 2022 (resultados definitivos), contra la
# que se valida la suma de los radios.
POBLACION_CENSO_2022 = 297282

# --- Geometria ------------------------------------------------------------

URL_SHP = ("https://catalogo.datos.gba.gob.ar/dataset/"
           "33b080d2-e369-4076-acd4-511db0e9bffb/resource/"
           "603ce4ba-a0da-429e-ae04-119f99556207/download/"
           "radios-censales-2022-shp.zip")
ARCH_SHP = "radios-censales-2022-shp.zip"

# --- Redatam --------------------------------------------------------------

REDATAM = "https://redatam.indec.gob.ar"
FREQ = REDATAM + "/argbin/RpWebStats.exe/Frequency"

# El motor no acepta una seleccion inline por partido, asi que se pide la
# seleccion publicada mas chica que contiene a San Isidro (los 24 partidos del
# Gran Buenos Aires) y se recorta despues por el codigo de area. La respuesta
# cruda se guarda entera, tal como la devuelve el servidor.
SELECCION = "Sels\\24GBA.sel"

# ITEM define la entidad y el universo del formulario de Redatam.
#   FREQPOBPART  personas en viviendas particulares
#   FREQPOBCOL   personas en viviendas colectivas
#   FREQHOG      hogares
#   FREQVIVPART  viviendas particulares
# ITEM define la entidad y el universo del formulario de Redatam.
#   FREQPOBPART  personas en viviendas particulares
#   FREQPOBCOL   personas en viviendas colectivas
#   FREQHOG      hogares
#   FREQVIVPART  viviendas particulares
#
# El ultimo campo es el nivel geografico MAXIMO que ofrece el formulario para
# ese item. Redatam no publica la poblacion en viviendas colectivas por radio:
# el desplegable de FREQPOBCOL llega hasta departamento. No se estima: se pide
# al nivel mas fino que existe y se marca. Ver data/NO_DISPONIBLE.md.
CONSULTAS = [
    ("poblacion_sexo",      "FREQPOBPART", "PERSONA.SEXO",     "persona",  "RADIO"),
    ("poblacion_edad",      "FREQPOBPART", "PERSONA.EDADGRU",  "persona",  "RADIO"),
    ("poblacion_edad_quinq", "FREQPOBPART", "PERSONA.EDADQUI",  "persona",  "RADIO"),
    ("educacion_mni",       "FREQPOBPART", "PERSONA.MNI",      "persona",  "RADIO"),
    ("hogares_nbi",         "FREQHOG",     "HOGAR.NBI_TOT",    "hogar",    "RADIO"),
    ("hogares_ipmh",        "FREQHOG",     "HOGAR.IPMH",       "hogar",    "RADIO"),
    ("hogares_hacinamiento","FREQHOG",     "HOGAR.HACINA",     "hogar",    "RADIO"),
    ("hogares_tenencia",    "FREQHOG",     "HOGAR.REGTEN",     "hogar",    "RADIO"),
    ("hogares_agua",        "FREQHOG",     "HOGAR.AGUAORIG",   "hogar",    "RADIO"),
    ("hogares_agua_dist",   "FREQHOG",     "HOGAR.AGUADIST",   "hogar",    "RADIO"),
    ("hogares_desague",     "FREQHOG",     "HOGAR.DESAGUE",    "hogar",    "RADIO"),
    ("hogares_combustible", "FREQHOG",     "HOGAR.COMBUS",     "hogar",    "RADIO"),
    ("viviendas_tipo",      "FREQVIVPART", "VIVIENDA.TIPOVIV", "vivienda", "RADIO"),
    ("viviendas_localidad", "FREQVIVPART", "VIVIENDA.CODLOC",  "vivienda", "RADIO"),
]

# Consultas que el motor no ofrece por radio y se piden al nivel mas fino que
# si existe. No entran a la tabla por radio: salen aparte, con su nivel.
CONSULTAS_OTRO_NIVEL = [
    ("poblacion_colectiva", "FREQPOBCOL", "PERSONA.SEXO", "persona", "DPTO"),
]

CITA_REDATAM = ("INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022, "
                "procesado con Redatam 7")


class ErrorDeFuente(Exception):
    pass


# --------------------------------------------------------------------------

def _sesion():
    import requests
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    return s


def descargar_geometria(sin_red=False):
    os.makedirs(RAW, exist_ok=True)
    destino = os.path.join(RAW, ARCH_SHP)
    if not sin_red:
        import requests
        r = requests.get(URL_SHP, timeout=600)
        r.raise_for_status()
        open(destino, "wb").write(r.content)
    if not os.path.exists(destino):
        raise ErrorDeFuente("falta %s" % destino)
    return destino


def verificar_codigo_partido(zip_shp):
    """
    El codigo de partido NO se asume: se busca por nombre en la propia capa y
    se comprueba que sea unico.
    """
    import geopandas as gpd
    # El shapefile viene dentro de una carpeta del zip; hay que nombrarla.
    with zipfile.ZipFile(zip_shp) as z:
        shp = [n for n in z.namelist() if n.lower().endswith(".shp")]
    if len(shp) != 1:
        raise ErrorDeFuente("se esperaba un solo .shp en el zip, hay %s" % shp)
    capa = gpd.read_file("zip://%s!%s" % (zip_shp, shp[0]))
    hallados = sorted({(f["PROV"], f["DEPTO"])
                       for _, f in capa.iterrows()
                       if str(f["NOMDEPTO"]).strip().upper() == NOMBRE_PARTIDO})
    if len(hallados) != 1:
        raise ErrorDeFuente("se esperaba un solo codigo para %s, hay %s"
                            % (NOMBRE_PARTIDO, hallados))
    prov, depto = hallados[0]
    if (prov, depto) != (PROV, DEPTO):
        raise ErrorDeFuente("el codigo de %s es %s%s y no %s%s"
                            % (NOMBRE_PARTIDO, prov, depto, PROV, DEPTO))
    return capa, prov, depto


def recortar_partido(capa):
    sub = capa[(capa["PROV"] == PROV) & (capa["DEPTO"] == DEPTO)].copy()
    if sub.empty:
        raise ErrorDeFuente("no quedo ningun radio de %s" % NOMBRE_PARTIDO)
    sub["radio_id"] = sub["LINK"].astype(str)
    malos = sorted(set(sub.loc[~sub["radio_id"].str.startswith(LINK_PREFIJO),
                               "radio_id"]))
    if malos:
        raise ErrorDeFuente("hay LINK que no arrancan con %s: %s"
                            % (LINK_PREFIJO, malos[:5]))
    sub = sub[["radio_id", "PROV", "DEPTO", "NOMDEPTO", "FRAC", "RADIO",
               "TIPO", "AREA", "PERIMETER", "geometry"]]
    sub = sub.rename(columns={"PROV": "prov", "DEPTO": "depto",
                              "NOMDEPTO": "partido", "FRAC": "fraccion",
                              "RADIO": "radio", "TIPO": "tipo_radio",
                              "AREA": "area_fuente",
                              "PERIMETER": "perimetro_fuente"})
    return sub.sort_values("radio_id").reset_index(drop=True)


# --------------------------------------------------------------------------
# Redatam
# --------------------------------------------------------------------------

def _ruta_cruda(clave):
    return os.path.join(RAW_REDATAM, "%s.html.gz" % clave)


def consultar(sesion, clave, item, row, areabreak, sin_red=False):
    """Corre una frecuencia por radio y guarda la respuesta cruda comprimida."""
    ruta = _ruta_cruda(clave)
    if sin_red or os.path.exists(ruta):
        if not os.path.exists(ruta):
            raise ErrorDeFuente("falta %s y se pidio --sin-red" % ruta)
        with gzip.open(ruta, "rt", encoding="utf-8") as f:
            return f.read(), False

    # El universo de cada ITEM lo define el propio formulario; se lee de ahi y
    # no se inventa, porque de el depende que casos entran a la cuenta.
    form = sesion.get(FREQ, params={"BASE": "CPV2022", "ITEM": item,
                                    "lang": "ESP"}, timeout=300)
    mu = re.search(r'name="UNIVERSE"[^>]*value="([^"]*)"', form.text)
    if not mu:
        raise ErrorDeFuente("no se pudo leer el universo del item %s" % item)
    universo = html.unescape(mu.group(1)).split(";")[0].strip()
    ab = re.search(r'<select[^>]*name="?AREABREAK"?[^>]*>(.*?)</select>',
                   form.text, re.S | re.I)
    niveles = re.findall(r'<option[^>]*value="([^"]*)"', ab.group(1)) if ab else []
    if areabreak not in niveles:
        raise ErrorDeFuente(
            "el item %s no ofrece desagregacion por %s; los niveles que "
            "publica son %s" % (item, areabreak, [n for n in niveles if n]))
    datos = {
        "MAIN": "WebServerMain.inl", "BASE": "CPV2022", "LANG": "ESP",
        "CODIGO": "XXUSUARIOXX", "ITEM": item, "MODE": "RUN",
        # Redatam rechaza guiones y puntos en el titulo, asi que va plano.
        "inputTitle": "San Isidro por radio %s" % re.sub(r"[^A-Za-z0-9 ]", " ", clave),
        "ROW": row, "AREABREAK": areabreak, "SELECTION": SELECCION,
        "INLINESELECTION": "", "UNIVERSE": universo, "FILTER": "",
        "TEXT_FILTER": "", "FORMAT": "HTML", "Submit": "Ejecutar",
    }
    r = sesion.post(FREQ + "?", data=datos, timeout=1800)
    r.raise_for_status()
    m = re.search(r"""<iframe[^>]*\ssrc=["']([^"']+)["']""", r.text)
    if not m:
        texto = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))
        raise ErrorDeFuente("Redatam no devolvio tabla para %s: %s"
                            % (clave, texto[:300]))
    tabla = sesion.get(REDATAM + m.group(1), timeout=1800)
    tabla.raise_for_status()
    os.makedirs(RAW_REDATAM, exist_ok=True)
    with gzip.open(ruta, "wt", encoding="utf-8") as f:
        f.write(tabla.text)
    return tabla.text, True


def _reparar_texto(t):
    """
    En la salida de Redatam la enie viene doblemente codificada ("aÃ±os" por
    "anios"), mientras que el resto de los acentos vienen bien. Se repara solo
    cuando la vuelta latin-1 -> utf-8 da un texto valido; si no, se deja como
    esta. No se toca ningun numero.
    """
    def _arreglar(m):
        try:
            return m.group(0).encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return m.group(0)
    # Solo los tramos que parecen utf-8 leido como latin-1. El resto del texto
    # no se toca, porque en la misma etiqueta conviven acentos sanos ("mas")
    # con la enie rota ("aÃ±os").
    return re.sub("[\u00c2\u00c3][\u0080-\u00bf]+", _arreglar, t)


def _celdas(fila):
    return [_reparar_texto(
                re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).strip())
            for c in re.findall(r"<td[^>]*>(.*?)</td>", fila, re.S)]


def _entero(txt):
    txt = (txt or "").replace("\xa0", " ").replace(" ", "").replace(".", "")
    return int(txt) if re.fullmatch(r"-?\d+", txt) else None


def parsear(texto, prefijo):
    """
    La salida de Redatam son bloques 'AREA # <codigo>' seguidos de las
    categorias y un Total. Se queda solo con las areas del prefijo pedido.

    -> {codigo_area: {"categorias": {nombre: casos}, "total": n}}
    """
    salida = {}
    actual = None
    for fila in re.findall(r"<tr>(.*?)</tr>", texto, re.S):
        c = [x for x in _celdas(fila) if x != ""]
        if not c:
            continue
        m = re.match(r"AREA # (\d+)$", c[0])
        if m:
            codigo = m.group(1)
            actual = ({"categorias": {}, "total": None}
                      if codigo.startswith(prefijo) else None)
            if actual is not None:
                salida[codigo] = actual
            continue
        if actual is None or len(c) < 2:
            continue
        etiqueta, valor = c[0], _entero(c[1])
        if valor is None:
            continue
        if etiqueta.lower() == "total":
            actual["total"] = valor
        elif etiqueta.lower() not in ("casos",):
            actual["categorias"][etiqueta] = valor
    return salida


# --------------------------------------------------------------------------
# Tabla por radio
# --------------------------------------------------------------------------

def _slug(txt):
    txt = txt.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
                 ("ñ", "n"), ("ü", "u")):
        txt = txt.replace(a, b)
    txt = re.sub(r"[^a-z0-9]+", "_", txt).strip("_")
    return txt[:44]


def construir_tabla(radios, resultados, fecha):
    """
    Una fila por radio, una columna por categoria de cada variable.
    Las columnas se nombran <clave>__<categoria>.
    """
    columnas = []
    for clave, _, row, _, _ in CONSULTAS:
        cats = []
        for datos in resultados[clave].values():
            for c in datos["categorias"]:
                if c not in cats:
                    cats.append(c)
        columnas.append((clave, row, cats))

    filas = []
    faltantes = []
    for radio in radios:
        fila = {"radio_id": radio, "nivel_geografico": "radio",
                "prov": PROV, "depto": DEPTO, "partido": NOMBRE_PARTIDO,
                "fuente": CITA_REDATAM, "fecha_descarga": fecha}
        for clave, _, cats in columnas:
            datos = resultados[clave].get(radio)
            if datos is None:
                faltantes.append((radio, clave))
                fila["%s__total" % clave] = ""
                for c in cats:
                    fila["%s__%s" % (clave, _slug(c))] = ""
                continue
            fila["%s__total" % clave] = datos["total"]
            for c in cats:
                fila["%s__%s" % (clave, _slug(c))] = datos["categorias"].get(c, 0)
        filas.append(fila)

    cabecera = ["radio_id", "nivel_geografico", "prov", "depto", "partido"]
    for clave, _, cats in columnas:
        cabecera.append("%s__total" % clave)
        cabecera += ["%s__%s" % (clave, _slug(c)) for c in cats]
    cabecera += ["fuente", "fecha_descarga"]

    ruta = os.path.join(DATA, "censo2022_sanisidro_por_radio.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cabecera, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)

    # Diccionario de columnas, para que nadie tenga que adivinar que es cada una.
    ruta_dic = os.path.join(DATA, "censo2022_diccionario_columnas.csv")
    with open(ruta_dic, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["columna", "variable_redatam", "categoria", "entidad",
                    "item_redatam"])
        por_clave = {c[0]: c for c in CONSULTAS}
        for clave, row, cats in columnas:
            _, item, _, entidad, _ = por_clave[clave]
            w.writerow(["%s__total" % clave, row, "(total)", entidad, item])
            for c in cats:
                w.writerow(["%s__%s" % (clave, _slug(c)), row, c, entidad, item])
    return filas, cabecera, faltantes, ruta


def main(sin_red=False):
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(DATA, exist_ok=True)
    fecha = dt.date.today().isoformat()

    print("PASO 1 - geometria")
    zip_shp = descargar_geometria(sin_red=sin_red)
    capa, prov, depto = verificar_codigo_partido(zip_shp)
    print("  codigo de partido verificado en la fuente: PROV=%s DEPTO=%s -> %s%s"
          % (prov, depto, prov, depto))
    sub = recortar_partido(capa)
    ruta_geo = os.path.join(DATA, "radios_censales_sanisidro.geojson")
    sub.to_file(ruta_geo, driver="GeoJSON")
    radios = list(sub["radio_id"])
    print("  radios censales de San Isidro: %d" % len(radios))
    print("  -> %s" % os.path.relpath(ruta_geo, REPO))

    print("PASO 2 - Redatam por radio")
    sesion = None if sin_red else _sesion()
    resultados = {}
    for clave, item, row, _, areabreak in CONSULTAS:
        texto, bajado = consultar(sesion, clave, item, row, areabreak,
                                  sin_red=sin_red)
        resultados[clave] = parsear(texto, LINK_PREFIJO)
        print("  %-22s %-18s %4d radios %s"
              % (clave, row, len(resultados[clave]),
                 "(bajado)" if bajado else "(cache)"))

    # Lo que Redatam no da por radio, al nivel mas fino que si publica.
    otros = {}
    for clave, item, row, _, areabreak in CONSULTAS_OTRO_NIVEL:
        texto, bajado = consultar(sesion, clave, item, row, areabreak,
                                  sin_red=sin_red)
        # A nivel departamento el codigo de area es PROV+DEPTO.
        otros[clave] = parsear(texto, LINK_PREFIJO)
        print("  %-22s %-18s %4d %s  %s  [NO hay por radio]"
              % (clave, row, len(otros[clave]), areabreak.lower(),
                 "(bajado)" if bajado else "(cache)"))

    filas, cabecera, faltantes, ruta = construir_tabla(radios, resultados, fecha)
    print("  -> %s  (%d filas, %d columnas)"
          % (os.path.relpath(ruta, REPO), len(filas), len(cabecera)))

    ruta_otro = os.path.join(DATA, "censo2022_sanisidro_otros_niveles.csv")
    with open(ruta_otro, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["clave", "variable_redatam", "nivel_geografico",
                    "codigo_area", "categoria", "casos", "fuente",
                    "fecha_descarga"])
        for clave, item, row, _, areabreak in CONSULTAS_OTRO_NIVEL:
            for codigo, datos in sorted(otros[clave].items()):
                for cat, n in datos["categorias"].items():
                    w.writerow([clave, row, areabreak.lower(), codigo, cat, n,
                                CITA_REDATAM, fecha])
                w.writerow([clave, row, areabreak.lower(), codigo, "Total",
                            datos["total"], CITA_REDATAM, fecha])
    print("  -> %s" % os.path.relpath(ruta_otro, REPO))

    return {"radios": radios, "geo": sub, "resultados": resultados,
            "otros": otros, "filas": filas, "faltantes": faltantes,
            "cabecera": cabecera, "fecha": fecha}


if __name__ == "__main__":
    r = main(sin_red="--sin-red" in sys.argv)
    pob = sum(int(f["poblacion_sexo__total"] or 0) for f in r["filas"])
    col = sum(d["total"] for d in r["otros"]["poblacion_colectiva"].values())
    total = pob + col
    dif = total - POBLACION_CENSO_2022
    print()
    print("poblacion en viviendas particulares (suma de %d radios): %d"
          % (len(r["filas"]), pob))
    print("poblacion en viviendas colectivas (departamento)       : %d" % col)
    print("total                                                  : %d" % total)
    print("Censo 2022, partido de San Isidro                      : %d"
          % POBLACION_CENSO_2022)
    print("diferencia                                             : %+d (%.4f%%)"
          % (dif, 100.0 * dif / POBLACION_CENSO_2022))
