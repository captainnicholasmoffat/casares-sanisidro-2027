#!/usr/bin/env python3
"""
Transferencias de la Provincia de Buenos Aires al Municipio de San Isidro.

FUENTE
  Los 13 XLSX de 01_raw/transferencias_pba/, bajados a mano del sitio de la
  Provincia (el host bloquea al worker, ver 01_raw/NO_DESCARGADOS.txt). Son de
  dos familias:

    transferencias    Un XLSX por anio, una hoja por mes. Cada hoja trae, por
                      municipio, la coparticipacion bruta y los fondos
                      especificos, y una columna Total.
    descentralizacion Un XLSX por anio, una hoja por mes. Abre la columna
                      "Descentralizacion" de la familia anterior en sus
                      componentes de la Ley 13.010.

  La descentralizacion NO se suma a las transferencias: ya esta adentro. Las
  dos familias van al mismo CSV con la columna "familia" para distinguirlas, y
  quien sume tiene que filtrar por una sola.

QUE HACE
  Busca la celda "Municipio" para ubicar el encabezado, lee los conceptos de la
  fila de abajo, encuentra la fila de San Isidro y saca una fila por concepto y
  por mes. No se corrige ningun numero: si la suma de los conceptos no da el
  Total publicado, la diferencia queda anotada y el numero se deja como esta.

Uso:
    python3 03_scripts/parse_transferencias.py
"""

import csv
import datetime as dt
import glob
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
RAW = os.path.join(REPO, "01_raw", "transferencias_pba")
CLEAN = os.path.join(REPO, "02_clean")

MUNICIPIO = "SAN ISIDRO"

MESES = {"ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5,
         "JUNIO": 6, "JULIO": 7, "AGOSTO": 8, "SEPTIEMBRE": 9,
         "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12}

DIAS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# Estas hojas no son un mes: son acumulados o restos de trabajo. Se saltean y
# queda dicho cuales.
HOJAS_NO_MENSUALES = {"ACUMULADO", "HOJA1", "MUNICIPIO"}

# Este archivo es el acumulado por municipio, con otro armado de encabezado y
# los mismos numeros que ya salen de las hojas mensuales. No se parsea para no
# duplicar; queda anotado en el informe.
ARCHIVOS_OMITIDOS = {"06-26 - Transferencias Ac. x Municipio.xlsx":
                     "acumulado por municipio, redundante con las hojas "
                     "mensuales del mismo anio"}

TOLERANCIA_TOTAL = Decimal("1")   # pesos


class ErrorDeParseo(Exception):
    pass


def _limpiar(txt):
    return re.sub(r"\s+", " ", str(txt)).strip()


def _dias_del_mes(anio, mes):
    if mes == 2 and (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)):
        return 29
    return DIAS[mes - 1]


def familia_de(nombre):
    n = nombre.lower()
    if "descentralizacion" in n or "descentralización" in n:
        return "descentralizacion"
    return "transferencias"


def anio_de_la_hoja(ws, nombre_archivo):
    """
    El anio sale del titulo de la hoja ("MES DE ENERO 2025"). Si no esta, del
    nombre del archivo ("12-25 - ..." -> 2025). Nunca se asume.
    """
    for fila in ws.iter_rows(min_row=1, max_row=10, values_only=True):
        for celda in fila:
            if celda is None:
                continue
            m = re.search(r"MES DE\s+[A-ZÁÉÍÓÚÑ]+\s+(\d{4})",
                          _limpiar(celda).upper())
            if m:
                return int(m.group(1)), "titulo de la hoja"
    m = re.match(r"(\d{2})-(\d{2})\s", nombre_archivo)
    if m:
        return 2000 + int(m.group(2)), "nombre del archivo"
    raise ErrorDeParseo("no se pudo determinar el anio de %s" % nombre_archivo)


def ubicar_encabezado(filas):
    """
    Devuelve (fila_conceptos, columna_municipio). El encabezado es la celda que
    dice exactamente "Municipio"; los conceptos estan en la fila siguiente,
    desde la columna de al lado.
    """
    for i, fila in enumerate(filas):
        for j, celda in enumerate(fila):
            if celda is not None and _limpiar(celda).lower() == "municipio":
                return i + 1, j
    raise ErrorDeParseo("no aparece la celda 'Municipio' en la hoja")


def parsear_hoja(ws, archivo, hoja):
    filas = list(ws.iter_rows(values_only=True))
    anio, origen_anio = anio_de_la_hoja(ws, archivo)
    mes = MESES[hoja.strip().upper()]
    i_conceptos, j_muni = ubicar_encabezado(filas)

    conceptos = []
    for j in range(j_muni + 1, len(filas[i_conceptos])):
        c = filas[i_conceptos][j]
        if c is None or not _limpiar(c):
            continue
        conceptos.append((j, _limpiar(c)))
    if not conceptos:
        raise ErrorDeParseo("no se leyo ningun concepto")

    fila_muni = None
    for fila in filas[i_conceptos + 1:]:
        if len(fila) <= j_muni or fila[j_muni] is None:
            continue
        if _limpiar(fila[j_muni]).upper() == MUNICIPIO:
            fila_muni = fila
            break
    if fila_muni is None:
        raise ErrorDeParseo("no aparece %s en la hoja" % MUNICIPIO)

    salida, total_publicado = [], None
    for j, nombre in conceptos:
        if j >= len(fila_muni) or fila_muni[j] is None:
            continue
        try:
            valor = Decimal(str(fila_muni[j])).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP)
        except Exception:
            continue
        if nombre.lower().startswith("total"):
            total_publicado = valor
            continue
        salida.append({"concepto": nombre, "monto": valor})
    return anio, mes, origen_anio, salida, total_publicado


def main():
    os.makedirs(CLEAN, exist_ok=True)
    hoy = dt.date.today().isoformat()
    filas, avisos, omitidos = [], [], []

    for ruta in sorted(glob.glob(os.path.join(RAW, "*.xlsx"))):
        nombre = os.path.basename(ruta)
        if nombre in ARCHIVOS_OMITIDOS:
            omitidos.append((nombre, ARCHIVOS_OMITIDOS[nombre]))
            continue
        import openpyxl
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        familia = familia_de(nombre)
        for hoja in wb.sheetnames:
            if hoja.strip().upper() in HOJAS_NO_MENSUALES:
                omitidos.append(("%s / %s" % (nombre, hoja),
                                 "la hoja no es un mes"))
                continue
            if hoja.strip().upper() not in MESES:
                omitidos.append(("%s / %s" % (nombre, hoja),
                                 "nombre de hoja desconocido"))
                continue
            try:
                anio, mes, origen, conceptos, total = parsear_hoja(
                    wb[hoja], nombre, hoja)
            except ErrorDeParseo as e:
                avisos.append("%s / %s: %s" % (nombre, hoja, e))
                continue

            # Los XLSX traen las hojas de los meses que todavia no ocurrieron
            # como plantillas vacias: la fila del municipio existe pero no hay
            # ningun importe distinto de cero. No son un mes con transferencias
            # nulas, son un mes sin publicar, y meterlos falsea el anio en
            # curso. Se descartan y queda anotado cuales.
            if not any(c["monto"] != 0 for c in conceptos):
                omitidos.append(("%s / %s" % (nombre, hoja),
                                 "plantilla sin cargar: la fila de %s no tiene "
                                 "ningun importe distinto de cero" % MUNICIPIO))
                continue

            suma = sum((c["monto"] for c in conceptos), Decimal(0))
            if total is not None and abs(suma - total) > TOLERANCIA_TOTAL:
                avisos.append(
                    "%s / %s: la suma de los conceptos da %s y el Total "
                    "publicado dice %s (diferencia %s). No se corrigio."
                    % (nombre, hoja, suma, total, suma - total))

            desde = dt.date(anio, mes, 1)
            hasta = dt.date(anio, mes, _dias_del_mes(anio, mes))
            for c in conceptos:
                filas.append({
                    "anio": anio, "mes": "%02d" % mes,
                    "periodo_desde": "%d/%d/%d" % (desde.day, desde.month, anio),
                    "periodo_hasta": "%d/%d/%d" % (hasta.day, hasta.month, anio),
                    "periodo_tipo": "mes",
                    "municipio": MUNICIPIO,
                    "familia": familia,
                    "concepto": c["concepto"],
                    "monto": str(c["monto"]),
                    "total_publicado_de_la_hoja": str(total) if total else "",
                    "archivo": nombre, "hoja": hoja,
                    "anio_tomado_de": origen,
                    "fuente": ("Ministerio de Hacienda y Finanzas de la "
                               "Provincia de Buenos Aires, %s" % nombre),
                    "fecha_descarga": hoy,
                })
        wb.close()

    filas.sort(key=lambda f: (f["familia"], f["anio"], f["mes"], f["concepto"]))
    ruta = os.path.join(CLEAN, "transferencias_pba_2021_2026.csv")
    cols = ["anio", "mes", "periodo_desde", "periodo_hasta", "periodo_tipo",
            "municipio", "familia", "concepto", "monto",
            "total_publicado_de_la_hoja", "archivo", "hoja", "anio_tomado_de",
            "fuente", "fecha_descarga"]
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Transferencias de la Provincia de Buenos Aires al Municipio "
                "de San Isidro.\n")
        f.write("# OJO AL SUMAR: la familia 'descentralizacion' YA ESTA adentro "
                "de la columna\n")
        f.write("# Descentralizacion de la familia 'transferencias'. Sumar las "
                "dos cuenta dos\n")
        f.write("# veces. Filtrar por familia antes de totalizar.\n")
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)
    return filas, avisos, omitidos, ruta


if __name__ == "__main__":
    filas, avisos, omitidos, ruta = main()
    anios = sorted({f["anio"] for f in filas})
    print("filas: %d  |  anios: %s" % (len(filas), "-".join(
        [str(anios[0]), str(anios[-1])])))
    for fam in sorted({f["familia"] for f in filas}):
        sub = [f for f in filas if f["familia"] == fam]
        meses = sorted({(f["anio"], f["mes"]) for f in sub})
        print("  %-18s %4d filas, %2d meses, %d conceptos"
              % (fam, len(sub), len(meses),
                 len({f["concepto"] for f in sub})))
    print()
    if omitidos:
        print("omitidos (%d):" % len(omitidos))
        for n, por in omitidos[:6]:
            print("  %-52s %s" % (n[:52], por))
        if len(omitidos) > 6:
            print("  ... y %d mas" % (len(omitidos) - 6))
    print()
    if avisos:
        print("AVISOS (%d), no se corrigio nada:" % len(avisos))
        for a in avisos[:10]:
            print("  %s" % a)
    else:
        print("sin avisos: la suma de conceptos da el Total publicado en todas "
              "las hojas")
    print()
    print("-> %s" % os.path.relpath(ruta, REPO))
