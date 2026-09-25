#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escenario A y escenario B de la base de valuacion de la Tasa por Alumbrado,
Limpieza y Servicios Generales (ALSG) de San Isidro. Solo la parte tierra.

Uso:
    python3 03_scripts/escenario_b_valuacion.py

Fuentes (todas en el repo, bajadas el 25/09/2026):
  01_raw/arba/parcelas_097_wfs/p_*.json.gz
      ARBA, geoservicio WFS IDERA, capa idera:Parcela, filtro cca LIKE '097%'
      (partido 097, San Isidro). 69.258 parcelas, superficie en ara1 (m2).
  01_raw/arba/VUBxMacizo_paginas_6516-6650_san_isidro.pdf
      ARBA, "Consulta de Valores por Macizos (Decreto 790/16)": valores
      unitarios basicos (VUB) del revaluo del Decreto 760/16, vigentes desde
      2018. Paginas 6516 a 6650 del PDF provincial (filas del partido 97).
  01_raw/arsi/ORDENANZA_IMPOSITIVA_2016.pdf
      Anexo I al Capitulo I: indice unitario de superficie de tierra (IUST)
      por manzana, el que fija la Ordenanza 8373/2008. Es la ultima version
      publicada con capa de texto; la de 2026 es un escaneo.
  01_raw/arsi/Ordenanza_Impositiva_2026-Nro_9415-2025_paginas_1-3.pdf
      Multiplicador 575,9141, alicuotas y minimos 2026.
  data/zonas_propuestas_sanisidro.geojson
      Las seis localidades del documento.

Formula municipal (Impositiva 2026, art. 1):
  Val. Fiscal = [(ST x IUST x CMS x CPH) + (SC x IUSC x CA)] x 575,9141
Este calculo usa solo la parte tierra, ST x IUST x 575,9141, con CMS = 1 y
CPH = 1 (no hay dato publico de superficie construida ni de la superficie
minima de cada zona), y la alicuota de vivienda, 12 por mil, para todas las
parcelas.
"""

import csv
import glob
import gzip
import json
import math
import os
import re
import statistics
from collections import defaultdict

import pymupdf
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "01_raw")
DATA = os.path.join(RAIZ, "data")

MULTIPLICADOR_2026 = 575.9141      # Impositiva 2026, art. 1
ALICUOTA = 0.012                   # vivienda, 12 por mil
MINIMO_2026 = 234000               # tasa minima anual 2026, categorias 2, 3, 4, 5, 10 y 12
FONDOS_NUEVOS = 7225.2e6           # lo que el programa necesita por anio, en pesos de dic-2025
PERCEPCION = 0.8932                # percepcion de recursos corrientes 2025 (data/parametros_modelo.csv)
TOPE_ANUAL = 0.25                  # ninguna boleta sube mas de 25% por anio por esta actualizacion
ANIOS_RAMPA = 4                    # el programa llega a su costo pleno en cuatro anios

ZONAS = ["Acassuso", "Martinez", "San Isidro", "Beccar", "Villa Adelina", "Boulogne Sur Mer"]


def _norm(num, letra=""):
    """'0012' + 'B' -> '12B'; '0000' -> ''."""
    n = str(int(num)) if num and num.strip("0") else ""
    letra = (letra or "").strip("0").upper()
    return n + letra if (n or letra) else ""


def _partir(texto):
    """'12B' -> ('12', 'B')."""
    m = re.fullmatch(r"(\d*)([A-Z]*)", texto.strip().upper())
    return (m.group(1), m.group(2)) if m else (texto, "")


def clave(circ, secc, fraccion, manzana):
    return (str(int(circ)), secc.strip().upper(), fraccion, manzana)


# --- 1. Tabla municipal: IUST por manzana ----------------------------------------
def leer_iust():
    doc = pymupdf.open(os.path.join(RAW, "arsi", "ORDENANZA_IMPOSITIVA_2016.pdf"))
    texto = " ".join(doc[i].get_text() for i in range(6, 34))   # paginas 7 a 34
    texto = re.sub(r"\s+", " ", texto)
    patron = re.compile(r"\b(\d)\s?([A-Z]{1,2})\s+(\d{4}[A-Z]?)\s+(\d{4}[A-Z]{0,2})\s+(\d{2,4})\b")
    entradas = patron.findall(texto)
    # La pagina 28 del anexo es una imagen: sus 142 filas (7B, 7C y el
    # comienzo de 7D) estan transcriptas a mano en este csv.
    transcripta = os.path.join(DATA, "valuacion_iust_2016_pagina28_transcripta.csv")
    for r in csv.DictReader(l for l in open(transcripta, encoding="utf-8") if not l.startswith("#")):
        entradas.append((r["cs"][0], r["cs"][1:], r["fraccion"], r["manzana"], r["iust"]))
    por_manzana = defaultdict(list)
    filas = []
    for circ, secc, campo2, manz, iust in entradas:
        n2, l2 = _partir(campo2)
        nm, lm = _partir(manz)
        frac = _norm(n2, l2)
        man = _norm(nm, lm)
        k = clave(circ, secc, frac, man)
        por_manzana[k].append(int(iust))
        filas.append((circ, secc, campo2, manz, iust))
    return por_manzana, filas


# --- 2. ARBA: valores unitarios basicos por macizo ----------------------------------
COLUMNAS_VUB = [("partido", 0, 150), ("circ", 150, 182), ("secc", 182, 205),
                ("chacra", 205, 240), ("quinta", 240, 270), ("fraccion", 270, 305),
                ("manzana", 305, 345), ("parcela", 345, 400), ("lados", 400, 500),
                ("vub", 500, 700)]


def leer_vub():
    doc = pymupdf.open(os.path.join(RAW, "arba", "VUBxMacizo_paginas_6516-6650_san_isidro.pdf"))
    filas = []
    for pagina in doc:
        grupos = {}
        for w in pagina.get_text("words"):
            y = round(w[1])
            k = next((g for g in grupos if abs(g - y) <= 3), y)
            grupos.setdefault(k, []).append(w)
        for y in sorted(grupos):
            r = {c: "" for c, _, _ in COLUMNAS_VUB}
            for w in sorted(grupos[y], key=lambda w: w[0]):
                for c, a, b in COLUMNAS_VUB:
                    if a <= w[0] < b:
                        r[c] = (r[c] + " " + w[4]).strip()
                        break
            if r["partido"] == "97" and r["vub"].isdigit() and r["lados"].isdigit():
                filas.append(r)
    por_macizo = defaultdict(list)
    for r in filas:
        k = clave(r["circ"], r["secc"], r["fraccion"].upper(), r["manzana"].upper())
        por_macizo[k].append((int(r["lados"]), int(r["vub"])))
    return por_macizo, filas


# --- 3. Parcelas de ARBA, con su localidad ----------------------------------------
def leer_parcelas():
    zonas = json.load(open(os.path.join(DATA, "zonas_propuestas_sanisidro.geojson"), encoding="utf-8"))
    geoms = [shape(f["geometry"]) for f in zonas["features"]]
    nombres = [f["properties"]["zona"] for f in zonas["features"]]
    arbol = STRtree(geoms)
    parcelas = []
    for f in sorted(glob.glob(os.path.join(RAW, "arba", "parcelas_097_wfs", "p_*.json.gz"))):
        for x in json.load(gzip.open(f, "rt", encoding="utf-8"))["features"]:
            p = x["properties"]
            c = p["cca"]
            frac = _norm(c[21:25], c[25:28])
            man = _norm(c[28:32], c[32:35])
            punto = shape(x["geometry"]).representative_point() if x.get("geometry") else None
            zona = None
            if punto is not None:
                for i in arbol.query(punto):
                    if geoms[i].contains(punto):
                        zona = nombres[i]
                        break
                if zona is None:   # borde o costa: la localidad mas cercana
                    i = arbol.nearest(punto)
                    zona = nombres[i]
            parcelas.append({
                "cca": c, "partida": p.get("pda") or "", "tipo": p.get("tpa") or "",
                "superficie": float(p.get("ara1") or 0),
                "clave": clave(c[3:5], c[5:7].lstrip("0"), frac, man),
                "zona": zona,
                "lon": round(punto.x, 6) if punto is not None else "",
                "lat": round(punto.y, 6) if punto is not None else "",
            })
    return parcelas


def cms(superficie, minima=300.0):
    """Coeficiente de Mayor Superficie (Anexo II), con una superficie minima
    de zona supuesta. El dato real depende de la zona del Codigo de
    Ordenamiento Urbano y no esta en este calculo."""
    exceso = superficie - minima
    for tope, coef in ((0, 1.00), (100, 0.97), (300, 0.92), (500, 0.87), (700, 0.84),
                       (1200, 0.80), (2700, 0.75), (4700, 0.70)):
        if exceso <= tope:
            return coef
    return 0.65


def _totales(ps, iust_de, peso):
    """Emision tierra hoy, escenario A, traslado bruto de B y suba pareja que
    hace falta para juntar los fondos nuevos, con un IUST y un peso dados."""
    t0 = {id(p): p["superficie"] * peso(p) * iust_de(p) * MULTIPLICADOR_2026 * ALICUOTA for p in ps}
    R = (sum(p["superficie"] * peso(p) * iust_de(p) for p in ps)
         / sum(p["superficie"] * peso(p) * p["vub"] for p in ps))
    tb = {id(p): p["superficie"] * peso(p) * R * p["vub"] * MULTIPLICADOR_2026 * ALICUOTA for p in ps}
    L0 = sum(t0.values())
    s = 1 + FONDOS_NUEVOS / L0
    por_zona = {}
    for z in ZONAS:
        zs = [p for p in ps if p["zona"] == z]
        a = sum(t0[id(p)] for p in zs)
        b = sum(s * tb[id(p)] for p in zs)
        por_zona[z] = round(100 * (b / a - 1), 1)
    return {"L0_M": round(L0 / 1e6, 1),
            "A_M": round(sum(max(0, tb[k] - t0[k]) for k in t0) / 1e6, 1),
            "A_pct": round(100 * sum(max(0, tb[k] - t0[k]) for k in t0) / L0, 1),
            "suba_pareja_B_pct": round(100 * (s - 1), 1),
            "B_mas_7225M_var_pct_por_localidad": por_zona}


def sensibilidades(ps, iust_m, vub, L0):
    uno = lambda p: 1.0
    return {
        "base_promedio_iust_cms_1": _totales(ps, lambda p: p["iust"], uno),
        "iust_minimo_de_la_manzana": _totales(ps, lambda p: min(iust_m[p["clave"]]), uno),
        "iust_maximo_de_la_manzana": _totales(ps, lambda p: max(iust_m[p["clave"]]), uno),
        "cms_con_minima_300m2": _totales(ps, lambda p: p["iust"], lambda p: cms(p["superficie"])),
        "cms_con_minima_600m2": _totales(ps, lambda p: p["iust"], lambda p: cms(p["superficie"], 600.0)),
        "emitir_para_cobrar_7225M_al_89_32pct": {
            "emision_necesaria_M": round(FONDOS_NUEVOS / 0.8932 / 1e6, 1),
            "suba_pareja_B_pct": round(100 * FONDOS_NUEVOS / 0.8932 / L0, 1)},
    }


def efecto_minimo(ps):
    """Parte de las bajas y subas del escenario B adoptado que queda por debajo
    de la tasa minima 2026, mirando solo la tierra. Si la parte construida es
    chica, esa parcela ya paga el minimo y esa baja no le llega."""
    out = {}
    for z in ZONAS + ["Todo el partido"]:
        zs = [p for p in ps if z == "Todo el partido" or p["zona"] == z]
        out[z] = {
            "parcelas": len(zs),
            "tierra_hoy_bajo_el_minimo": sum(1 for p in zs if p["t0"] < MINIMO_2026),
            "baja_B_bajo_el_minimo_M": round(sum(max(0, min(p["t0"], MINIMO_2026) - p["tbc"])
                                                 for p in zs if p["tbc"] < p["t0"] and p["tbc"] < MINIMO_2026) / 1e6, 1),
            "suba_B_bajo_el_minimo_M": round(sum(max(0, min(p["tbc"], MINIMO_2026) - p["t0"])
                                                 for p in zs if p["tbc"] > p["t0"] and p["t0"] < MINIMO_2026) / 1e6, 1),
        }
    return out


def camino_con_tope(ps, tope, anios=6):
    """Lo que rinde el escenario B adoptado cada anio con un tope de suba
    anual por boleta. Las bajas entran completas el primer anio."""
    filas = []
    for k in range(1, anios + 1):
        emision = 0.0
        topeadas = 0
        for p in ps:
            if p["tbc"] >= p["t0"]:
                techo = p["t0"] * (1 + tope) ** k
                emision += min(p["tbc"], techo) - p["t0"]
                topeadas += p["tbc"] > techo
            else:
                emision += p["tbc"] - p["t0"]
        filas.append({"anio_del_programa": k,
                      "emision_extra": round(emision),
                      "cobrado": round(PERCEPCION * emision),
                      "necesidad_de_la_rampa": round(FONDOS_NUEVOS * min(k, ANIOS_RAMPA) / ANIOS_RAMPA),
                      "parcelas_todavia_con_tope": topeadas})
    return filas


def main():
    iust_m, filas_iust = leer_iust()
    vub_m, filas_vub = leer_vub()
    parcelas = leer_parcelas()

    # Un valor por manzana. IUST: el promedio de los valores que lista el
    # anexo (si hay mas de uno, el Ejecutivo asigna cada lote; no es publico).
    # VUB: el promedio de los valores de los lados, ponderado por cantidad de
    # lados.
    iust = {k: statistics.mean(v) for k, v in iust_m.items()}
    vub = {k: sum(l * v for l, v in xs) / sum(l for l, _ in xs) for k, xs in vub_m.items()}

    with open(os.path.join(DATA, "valuacion_iust_manzanas.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["circ", "secc", "fraccion", "manzana", "iust_promedio", "valores_listados"])
        for k in sorted(iust_m):
            w.writerow(list(k) + [round(iust[k], 2), "|".join(map(str, iust_m[k]))])
    with open(os.path.join(DATA, "valuacion_vub_macizos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["circ", "secc", "fraccion", "manzana", "vub_promedio_por_lados", "lados_x_valor"])
        for k in sorted(vub_m):
            w.writerow(list(k) + [round(vub[k], 2), "|".join(f"{l}x{v}" for l, v in vub_m[k])])

    total = len(parcelas)
    sup_total = sum(p["superficie"] for p in parcelas)
    cruzadas = [p for p in parcelas if p["clave"] in iust and p["clave"] in vub]
    con_iust = sum(1 for p in parcelas if p["clave"] in iust)
    con_vub = sum(1 for p in parcelas if p["clave"] in vub)

    # Emision actual de la parte tierra, por parcela
    for p in cruzadas:
        p["iust"] = iust[p["clave"]]
        p["vub"] = vub[p["clave"]]
        p["t0"] = p["superficie"] * p["iust"] * MULTIPLICADOR_2026 * ALICUOTA
        p["varios_iust"] = len(set(iust_m[p["clave"]])) > 1
    L0 = sum(p["t0"] for p in cruzadas)

    # Escala relativa de ARBA a igual recaudacion: el IUST nuevo es R x VUB,
    # con R = cociente promedio ponderado por superficie.
    R = sum(p["superficie"] * p["iust"] for p in cruzadas) / sum(p["superficie"] * p["vub"] for p in cruzadas)
    for p in cruzadas:
        p["iust_b"] = R * p["vub"]
        p["tb0"] = p["superficie"] * p["iust_b"] * MULTIPLICADOR_2026 * ALICUOTA
        p["ta"] = max(p["t0"], p["tb0"])                     # escenario A
    # Escenario B que recauda los fondos nuevos: la misma escala, subida pareja.
    s = 1 + FONDOS_NUEVOS / L0
    for p in cruzadas:
        p["tbs"] = s * p["tb0"]
    # Escenario B adoptado: la escala sube lo justo para COBRAR los fondos
    # nuevos con la percepcion de hoy, y cada boleta sube como mucho un 25%
    # por anio hasta llegar. Las bajas se aplican el primer anio.
    sc = 1 + FONDOS_NUEVOS / PERCEPCION / L0
    for p in cruzadas:
        p["tbc"] = sc * p["tb0"]
        if p["tbc"] > p["t0"]:
            p["anios"] = max(1, math.ceil(math.log(p["tbc"] / p["t0"]) / math.log(1 + TOPE_ANUAL) - 1e-9))
        else:
            p["anios"] = 1
    rendimiento = camino_con_tope(cruzadas, TOPE_ANUAL)
    tope_minimo = next(round(100 * c) for c in [x / 100 for x in range(10, 61)]
                       if all(r["cobrado"] >= r["necesidad_de_la_rampa"] - 1
                              for r in camino_con_tope(cruzadas, c)[:ANIOS_RAMPA]))
    with open(os.path.join(DATA, "valuacion_rendimiento_por_anio.csv"), "w", newline="", encoding="utf-8") as f:
        f.write("# Escenario B adoptado: escala de ARBA subida %.2f%% (para cobrar 7.225,2 M con la\n" % (100 * (sc - 1)))
        f.write("# percepcion de %.2f%%) y tope de %d%% de suba anual por boleta. Parte tierra, pesos de\n"
                % (100 * PERCEPCION, round(100 * TOPE_ANUAL)))
        f.write("# diciembre de 2025. Lo lee 03_scripts/modelo.py.\n")
        w = csv.DictWriter(f, fieldnames=list(rendimiento[0].keys()))
        w.writeheader()
        w.writerows(rendimiento)

    resumen = {
        "parcelas": total, "superficie_ha": sup_total / 1e4,
        "parcelas_con_iust": con_iust, "parcelas_con_vub": con_vub,
        "parcelas_cruzadas": len(cruzadas),
        "superficie_cruzada_ha": sum(p["superficie"] for p in cruzadas) / 1e4,
        "manzanas_tabla_municipal": len(iust_m), "macizos_arba": len(vub_m),
        "L0": L0, "R": R, "s": s,
        "A": sum(p["ta"] - p["t0"] for p in cruzadas),
        "B0": sum(p["tb0"] - p["t0"] for p in cruzadas),
        "B0_suben": sum(p["tb0"] - p["t0"] for p in cruzadas if p["tb0"] > p["t0"]),
        "B0_bajan": sum(p["tb0"] - p["t0"] for p in cruzadas if p["tb0"] < p["t0"]),
        "Bs_suben": sum(p["tbs"] - p["t0"] for p in cruzadas if p["tbs"] > p["t0"]),
        "Bs_bajan": sum(p["tbs"] - p["t0"] for p in cruzadas if p["tbs"] < p["t0"]),
        "parcelas_varios_iust": sum(1 for p in cruzadas if p["varios_iust"]),
        "adoptado": {
            "suba_pareja_pct": round(100 * (sc - 1), 2),
            "emision_extra_M": round(sum(p["tbc"] - p["t0"] for p in cruzadas) / 1e6, 1),
            "cobrado_M": round(PERCEPCION * sum(p["tbc"] - p["t0"] for p in cruzadas) / 1e6, 1),
            "parcelas_suben": sum(1 for p in cruzadas if p["tbc"] > p["t0"] * 1.0005),
            "parcelas_bajan": sum(1 for p in cruzadas if p["tbc"] < p["t0"] * 0.9995),
            "parcelas_que_duplican": sum(1 for p in cruzadas if p["tbc"] >= 2 * p["t0"]),
            "suba_maxima_pct": round(100 * max(p["tbc"] / p["t0"] - 1 for p in cruzadas), 1),
            "tope_anual_pct": round(100 * TOPE_ANUAL),
            "tope_minimo_que_cubre_la_rampa_pct": tope_minimo,
            "parcelas_por_anios_para_llegar": {str(k): sum(1 for p in cruzadas if p["tbc"] > p["t0"] * 1.0005 and p["anios"] == k)
                                               for k in range(1, 7)},
            "rendimiento_por_anio": rendimiento,
        },
    }

    # Por localidad
    filas = []
    for z in ZONAS + ["Todo el partido"]:
        ps = [p for p in cruzadas if z == "Todo el partido" or p["zona"] == z]
        if not ps:
            continue
        t0 = sum(p["t0"] for p in ps)
        fila = {"localidad": z, "parcelas": len(ps),
                "superficie_ha": round(sum(p["superficie"] for p in ps) / 1e4, 1),
                "tierra_hoy_M": round(t0 / 1e6, 1),
                "carga_hoy_pct": round(100 * t0 / L0, 1)}
        for esc, campo in (("B0", "tb0"), ("Bs", "tbs"), ("Bc", "tbc"), ("A", "ta")):
            t = sum(p[campo] for p in ps)
            suben = [p for p in ps if p[campo] > p["t0"] * 1.0005]
            bajan = [p for p in ps if p[campo] < p["t0"] * 0.9995]
            var_suben = sorted(p[campo] / p["t0"] - 1 for p in suben)
            fila.update({
                f"{esc}_M": round(t / 1e6, 1),
                f"{esc}_carga_pct": round(100 * t / sum(p[campo] for p in cruzadas), 1),
                f"{esc}_dif_M": round((t - t0) / 1e6, 1),
                f"{esc}_dif_pct": round(100 * (t / t0 - 1), 1),
                f"{esc}_parcelas_suben": len(suben),
                f"{esc}_parcelas_bajan": len(bajan),
                f"{esc}_mediana_suba_pct": round(100 * statistics.median(var_suben), 1) if var_suben else "",
                f"{esc}_parcelas_que_duplican": sum(1 for v in var_suben if v >= 1.0),
            })
        filas.append(fila)
    with open(os.path.join(DATA, "valuacion_escenarios_localidad.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    resumen["sensibilidad"] = sensibilidades(cruzadas, iust_m, vub, L0)
    resumen["minimo"] = efecto_minimo(cruzadas)
    ids = {id(p) for p in cruzadas}
    resumen["sin_cruzar_por_localidad"] = {z: sum(1 for p in parcelas if p["zona"] == z and id(p) not in ids)
                                           for z in ZONAS}
    with open(os.path.join(DATA, "valuacion_resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    with open(os.path.join(DATA, "valuacion_parcelas.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cca", "partida", "localidad", "superficie_m2", "iust", "vub",
                    "tierra_hoy", "tierra_B_igual_recaudacion", "tierra_B_mas_7225M", "tierra_A",
                    "tierra_B_adoptado", "anios_para_llegar", "lon", "lat"])
        for p in cruzadas:
            w.writerow([p["cca"], p["partida"], p["zona"], round(p["superficie"], 2), round(p["iust"], 2),
                        round(p["vub"], 2), round(p["t0"]), round(p["tb0"]), round(p["tbs"]), round(p["ta"]),
                        round(p["tbc"]), p["anios"], p["lon"], p["lat"]])
    return resumen, filas


if __name__ == "__main__":
    resumen, filas = main()
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    for f in filas:
        print(f)
