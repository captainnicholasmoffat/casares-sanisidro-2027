#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estado de Situacion Economico-Financiera (SEF) anual, a CSV.

POR QUE HACE FALTA
  El SEF trae tres cosas que no estan en ningun otro archivo del repo y que el
  modelo de flujo de caja necesita:

    1. La cuenta Ahorro-Inversion-Financiamiento, que es la que define el
       RESULTADO FINANCIERO oficial del ejercicio. Ojo: mide los ingresos por
       lo PERCIBIDO y los gastos por lo DEVENGADO. No es un descuido, es la
       convencion del formato; comparar devengado contra devengado da otro
       numero y no es el resultado financiero.
    2. Los recursos por ORIGEN (municipal, provincial, nacional, otros), que es
       lo que permite separar recursos propios de transferencias.
    3. El gasto por PROGRAMA, que es donde estan las partidas de empleo y de
       vivienda, invisibles en la apertura por objeto.

Uso:
    python3 03_scripts/parse_sef.py
"""

import csv
import os
import re
import sys
from decimal import Decimal

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
RAW = os.path.join(REPO, "01_raw", "sanisidro_transparencia",
                   "situacion_economico_financiera")
DATA = os.path.join(REPO, "data")

# Los SEF anuales que hay en el repo. Los trimestrales no entran: el modelo
# trabaja con ejercicios cerrados.
INFORMES = [
    (2024, "sef_msi_-_2024.pdf"),
    (2025, "situacion_economico_financiera_2025_anual.pdf"),
]

# Las diez lineas de la cuenta Ahorro-Inversion, en orden y con su signo.
AIF = [
    ("I", "ingresos_corrientes", r"I\.\s*INGRESOS CORRIENTES"),
    ("II", "gastos_corrientes", r"II\.\s*GASTOS CORRIENTES"),
    ("III", "ahorro_corriente", r"III\.\s*AHORRO CORRIENTE"),
    ("IV", "recursos_de_capital", r"IV\.\s*RECURSOS DE CAPITAL"),
    ("V", "gastos_de_capital", r"V\.\s*GASTOS CAPITAL"),
    ("VI", "ingresos_totales", r"VI\.\s*INGRESOS TOTALES"),
    ("VII", "gastos_totales", r"VII\.\s*GASTOS TOTALES"),
    ("VIII", "resultado_financiero", r"VIII\.\s*RESULTADO FINANCIERO"),
    ("IX", "fuentes_financieras", r"IX\.\s*FUENTES FINANCIERAS"),
    ("X", "aplicaciones_financieras", r"X\.\s*APLICACIONES FINANCIERAS"),
]

ORIGENES = ["ORIGEN MUNICIPAL", "ORIGEN PROVINCIAL", "ORIGEN NACIONAL",
            "OTROS ORIGENES"]

OBJETOS = ["GASTOS EN PERSONAL", "BIENES DE CONSUMO", "SERVICIOS NO PERSONALES",
           "BIENES DE USO", "TRANSFERENCIAS", "ACTIVOS FINANCIEROS",
           "SERVICIO DE LA DEUDA"]


class ErrorDeSEF(Exception):
    pass


def _num(txt):
    return Decimal(txt.replace(",", ""))


def _lineas(ruta, paginas=None):
    import pdfplumber
    with pdfplumber.open(ruta) as pdf:
        txt = "\n".join((p.extract_text() or "") for p in
                       (pdf.pages if paginas is None else pdf.pages[:paginas]))
    return [re.sub(r"\s+", " ", l).strip() for l in txt.splitlines()]


def parsear(anio, archivo):
    ruta = os.path.join(RAW, archivo)
    if not os.path.exists(ruta):
        raise ErrorDeSEF("falta %s" % ruta)
    lineas = _lineas(ruta)
    filas = []

    # --- Ahorro-Inversion: una sola cifra por linea ---
    for romano, clave, patron in AIF:
        hallado = None
        for l in lineas:
            if re.match(patron, l):
                m = re.findall(r"-?[\d,]+\.\d{2}", l)
                if m:
                    hallado = _num(m[-1])
                break
        if hallado is None:
            raise ErrorDeSEF("%d: no se leyo la linea %s de la cuenta AIF"
                             % (anio, romano))
        filas.append({"anio": anio, "bloque": "ahorro_inversion",
                      "orden": romano, "concepto": clave,
                      "medida": "oficial", "monto": hallado,
                      "fuente": archivo})

    # --- Recursos por origen: vigente / devengado / percibido ---
    for l in lineas:
        for org in ORIGENES:
            if not l.startswith(org):
                continue
            m = re.findall(r"[\d,]+\.\d{2}", l)
            etiqueta = l[:l.index(m[0])].strip() if m else l
            # Cuando falta una columna el PDF simplemente no la imprime, asi
            # que se toma la ultima como percibido solo si vienen las tres.
            if len(m) == 3:
                vals = {"vigente": _num(m[0]), "devengado": _num(m[1]),
                        "percibido": _num(m[2])}
            elif len(m) == 1:
                vals = {"vigente": _num(m[0])}
            else:
                vals = {"vigente": _num(m[0]), "devengado": _num(m[1])}
            for medida, v in vals.items():
                filas.append({"anio": anio, "bloque": "recursos_por_origen",
                              "orden": "", "concepto": etiqueta,
                              "medida": medida, "monto": v,
                              "fuente": archivo})

    # --- Gastos por objeto ---
    for l in lineas:
        for obj in OBJETOS:
            if not l.startswith(obj):
                continue
            m = re.findall(r"[\d,]+\.\d{2}", l)
            if len(m) < 2:
                continue
            etiqueta = l[:l.index(m[0])].strip()
            # vigente, [preventivo], compromiso, devengado, pagado
            filas.append({"anio": anio, "bloque": "gastos_por_objeto",
                          "orden": "", "concepto": etiqueta,
                          "medida": "devengado", "monto": _num(m[-2]),
                          "fuente": archivo})
            filas.append({"anio": anio, "bloque": "gastos_por_objeto",
                          "orden": "", "concepto": etiqueta,
                          "medida": "pagado", "monto": _num(m[-1]),
                          "fuente": archivo})

    # --- Gastos por programa ---
    # Las columnas son VIGENTE, COMPROMISO, DEVENGADO, PAGADO. Cuando el PDF
    # trunca la linea quedan tres numeros y NO se puede saber cual falta, asi
    # que "el anteultimo es el devengado" agarraria el compromiso y meteria un
    # numero inflado. Se aceptan SOLO las lineas con los cuatro numeros y el
    # resto queda contado como no parseado. Un programa de menos se ve; un
    # importe equivocado, no.
    rotas, no_parseados = 0, []
    for l in lineas:
        m = re.match(r"^([\d.]+ - \d+) (.+)$", l)
        if not m:
            continue
        resto = m.group(2)
        nums = re.findall(r"[\d,]+\.\d{2}", resto)
        nombre = resto[:resto.index(nums[0])].strip() if nums else resto
        if len(nums) != 4 or re.search(r"\d", nombre[-6:]):
            rotas += 1
            no_parseados.append((m.group(1), nombre[:60], len(nums)))
            continue
        filas.append({"anio": anio, "bloque": "gastos_por_programa",
                      "orden": m.group(1), "concepto": nombre,
                      "medida": "devengado", "monto": _num(nums[2]),
                      "fuente": archivo})

    # Lo que no es un programa pero si es gasto: sin estas tres lineas el
    # bloque no suma el total del ejercicio.
    for etiqueta in ("Actividades Centrales",
                     "Partidas no asignables a programas"):
        for l in lineas:
            if not l.startswith(etiqueta):
                continue
            nums = re.findall(r"[\d,]+\.\d{2}", l)
            if len(nums) != 4:
                continue
            filas.append({"anio": anio, "bloque": "gastos_por_programa",
                          "orden": "", "concepto": etiqueta,
                          "medida": "devengado", "monto": _num(nums[2]),
                          "fuente": archivo})

    return filas, rotas, no_parseados


def verificar(filas, anio):
    """La cuenta AIF tiene que cerrar consigo misma en las tres identidades."""
    v = {f["concepto"]: f["monto"] for f in filas
         if f["anio"] == anio and f["bloque"] == "ahorro_inversion"}
    problemas = []
    checks = [
        ("ahorro corriente = ingresos ctes - gastos ctes",
         v["ingresos_corrientes"] - v["gastos_corrientes"], v["ahorro_corriente"]),
        ("ingresos totales = ingresos ctes + recursos de capital",
         v["ingresos_corrientes"] + v["recursos_de_capital"], v["ingresos_totales"]),
        ("gastos totales = gastos ctes + gastos de capital",
         v["gastos_corrientes"] + v["gastos_de_capital"], v["gastos_totales"]),
        ("resultado financiero = ingresos totales - gastos totales",
         v["ingresos_totales"] - v["gastos_totales"], v["resultado_financiero"]),
    ]
    for nombre, calculado, publicado in checks:
        if abs(calculado - publicado) > Decimal("1"):
            problemas.append("%s: da %s y el PDF dice %s"
                             % (nombre, calculado, publicado))
    return problemas, v


def main():
    todas, rotas_tot, problemas, no_parseados = [], 0, [], []
    for anio, archivo in INFORMES:
        filas, rotas, np = parsear(anio, archivo)
        no_parseados += [(anio,) + x for x in np]
        todas += filas
        rotas_tot += rotas
        p, _ = verificar(filas, anio)
        problemas += ["%d: %s" % (anio, x) for x in p]

    ruta = os.path.join(DATA, "sef_anual.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "bloque", "orden", "concepto", "medida", "monto",
                    "fuente"])
        for x in todas:
            w.writerow([x["anio"], x["bloque"], x["orden"], x["concepto"],
                        x["medida"], x["monto"], x["fuente"]])
    return todas, rotas_tot, problemas, ruta, no_parseados


if __name__ == "__main__":
    filas, rotas, problemas, ruta, no_parseados = main()
    for anio, _ in INFORMES:
        sub = [f for f in filas if f["anio"] == anio]
        print("%d: %d filas  (%s)" % (anio, len(sub), ", ".join(
            "%s=%d" % (b, len([f for f in sub if f["bloque"] == b]))
            for b in ("ahorro_inversion", "recursos_por_origen",
                      "gastos_por_objeto", "gastos_por_programa"))))
    print()
    for anio, _ in INFORMES:
        _, v = verificar(filas, anio)
        print("%d  resultado financiero oficial: %s" % (anio, v["resultado_financiero"]))
    print()
    print("lineas de programa NO parseadas (el PDF las trunca): %d" % rotas)
    for x in no_parseados:
        print("  %d  %-22s %-42s %d numeros" % x)
    if problemas:
        print("PROBLEMAS:")
        for p in problemas:
            print("  " + p)
    else:
        print("la cuenta Ahorro-Inversion cierra en las 4 identidades, los 2 anios")
    print("-> %s" % os.path.relpath(ruta, REPO))
