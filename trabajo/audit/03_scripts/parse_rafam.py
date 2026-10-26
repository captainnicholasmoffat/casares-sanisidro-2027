#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte 01_raw/rafam_2025_106_municipios.csv en data/rafam_2025_municipios.csv.

QUE ES EL CRUDO
    Ejecucion presupuestaria 2025 de 106 de los 135 municipios de la Provincia
    de Buenos Aires, tomada del RAFAM (el sistema contable provincial). Lo
    aporto el usuario. Los 29 municipios que faltan no publicaron o no estaban
    en la planilla: el grafico dice 106 y no 135, y no se completa ninguno.

QUE HACE ESTE SCRIPT
    1. Recalcula los dos porcentajes desde los importes devengados en vez de
       creerle a las columnas pct_ ya calculadas del crudo:
           pct_personal = gastos_en_personal_dev / total_presupuestario_dev
           pct_obra     = bienes_de_uso_dev      / total_presupuestario_dev
       y verifica que coincidan con las del crudo. Si alguna difiere en mas de
       0,05 puntos, el script FALLA. Una planilla que se contradice a si misma
       no se publica.
    2. Ordena y numera:
           puesto_personal  1 = el que menos peso le da al personal
           puesto_obra      1 = el que mas invierte en bienes de uso
       Los dos ordenes van al reves a proposito, porque el sentido "mejor" es
       distinto en cada uno, y esta escrito en el CSV para que nadie lo asuma.
    3. Escribe la mediana provincial de cada indicador en la cabecera.

    La mediana es la de la definicion: con 106 valores, el promedio de los dos
    del medio. Tomar solo el 54 da 50,85% y 5,46%, dos decimas mas en personal.
    El puesto de San Isidro es el mismo con cualquiera de las dos.

Uso:
    python3 03_scripts/parse_rafam.py
"""

import csv
import os
import statistics
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
CRUDO = os.path.join(REPO, "01_raw", "rafam_2025_106_municipios.csv")
SALIDA = os.path.join(REPO, "data", "rafam_2025_municipios.csv")

# Cuanto puede diferir el porcentaje recalculado del que trae el crudo, en
# puntos porcentuales. Es tolerancia de redondeo, no de criterio.
TOLERANCIA = 0.05


def leer_crudo():
    with open(CRUDO, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def numero(fila, columna):
    v = (fila.get(columna) or "").strip()
    return float(v) if v else None


def main():
    filas = leer_crudo()
    if len(filas) != 106:
        sys.exit("el crudo tiene %d filas y se esperaban 106" % len(filas))

    datos, discrepancias = [], []
    for r in filas:
        total = numero(r, "total_presupuestario_dev")
        personal = numero(r, "gastos_en_personal_dev")
        obra = numero(r, "bienes_de_uso_dev")
        if not total or personal is None or obra is None:
            sys.exit("%s no tiene los tres importes devengados" % r["municipio"])
        pp, po = 100 * personal / total, 100 * obra / total
        for calculado, columna in ((pp, "pct_personal"), (po, "pct_obra")):
            declarado = numero(r, columna)
            if declarado is not None and abs(calculado - declarado) > TOLERANCIA:
                discrepancias.append("%s %s: la planilla dice %.2f y los "
                                     "importes dan %.2f"
                                     % (r["municipio"], columna, declarado,
                                        calculado))
        datos.append({"municipio": r["municipio"], "seccion": r["seccion"],
                      "total_presupuestario_dev": total,
                      "gastos_en_personal_dev": personal,
                      "bienes_de_uso_dev": obra,
                      "pct_personal": pp, "pct_obra": po})

    if discrepancias:
        for d in discrepancias:
            print("  " + d)
        sys.exit("el crudo se contradice a si mismo en %d casos"
                 % len(discrepancias))

    # Puesto 1 = menos personal; puesto 1 = mas obra. Sentidos opuestos porque
    # "mejor" quiere decir cosas distintas en cada indicador.
    for clave, campo, al_reves in (("pct_personal", "puesto_personal", False),
                                   ("pct_obra", "puesto_obra", True)):
        for i, d in enumerate(sorted(datos, key=lambda x: x[clave],
                                     reverse=al_reves), 1):
            d[campo] = i

    med_personal = statistics.median(d["pct_personal"] for d in datos)
    med_obra = statistics.median(d["pct_obra"] for d in datos)
    datos.sort(key=lambda d: d["municipio"])

    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        f.write("# Ejecución presupuestaria 2025 de 106 de los 135 municipios\n")
        f.write("# de la Provincia de Buenos Aires, del RAFAM provincial.\n")
        f.write("# Fuente: 01_raw/rafam_2025_106_municipios.csv (aportado, sin\n")
        f.write("# URL registrada en 01_raw/INVENTARIO.txt).\n")
        f.write("# Faltan 29 municipios. No se estima ninguno.\n")
        f.write("# pct_personal = gastos_en_personal_dev / total_presupuestario_dev\n")
        f.write("# pct_obra     = bienes_de_uso_dev      / total_presupuestario_dev\n")
        f.write("# puesto_personal: 1 = el que MENOS peso le da al personal.\n")
        f.write("# puesto_obra:     1 = el que MAS invierte en bienes de uso.\n")
        f.write("# mediana_pct_personal = %.4f\n" % med_personal)
        f.write("# mediana_pct_obra     = %.4f\n" % med_obra)
        w = csv.writer(f)
        w.writerow(["municipio", "seccion", "total_presupuestario_dev",
                    "gastos_en_personal_dev", "bienes_de_uso_dev",
                    "pct_personal", "pct_obra", "puesto_personal",
                    "puesto_obra", "fuente"])
        for d in datos:
            w.writerow([d["municipio"], d["seccion"],
                        "%.1f" % d["total_presupuestario_dev"],
                        "%.1f" % d["gastos_en_personal_dev"],
                        "%.1f" % d["bienes_de_uso_dev"],
                        "%.4f" % d["pct_personal"], "%.4f" % d["pct_obra"],
                        d["puesto_personal"], d["puesto_obra"],
                        "01_raw/rafam_2025_106_municipios.csv"])

    si = [d for d in datos if d["municipio"] == "San Isidro"][0]
    print("%d municipios -> %s" % (len(datos), os.path.relpath(SALIDA, REPO)))
    print("  mediana personal %.2f%%   mediana obra %.2f%%"
          % (med_personal, med_obra))
    print("  San Isidro: personal %.2f%% puesto %d de %d, "
          "obra %.2f%% puesto %d de %d"
          % (si["pct_personal"], si["puesto_personal"], len(datos),
             si["pct_obra"], si["puesto_obra"], len(datos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
