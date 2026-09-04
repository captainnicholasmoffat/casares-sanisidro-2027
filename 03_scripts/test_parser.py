#!/usr/bin/env python3
"""
Tests y validaciones del parser de ejecucion presupuestaria.

El test dorado va primero y es el que manda: si no reproduce exactamente los
siete devengados de 2025 IV, no hay nada mas que discutir y el resto no corre.

Despues valida cada trimestre de cada informe. Lo que no cierra NO se corrige:
se anota en data/INCONSISTENCIAS.csv con el archivo de origen y el motivo. Los
numeros salen como los publico el Municipio.

Uso:
    python3 03_scripts/test_parser.py
Sale 0 si el test dorado pasa. Las inconsistencias no hacen fallar la corrida
(son un hallazgo sobre la fuente, no un bug del parser), pero se listan.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import parse_ejecucion as P

EJECUCION = os.path.join(P.RAW, "ejecucion_presupuestaria")

# Devengado esperado por objeto del gasto en 2025 IV, en centavos.
# Fuente: 2025_iv_gastos_por_objeto.pdf, leido a mano.
DORADO = [
    ("1", "GASTOS EN PERSONAL", 11158952352490),
    ("2", "BIENES DE CONSUMO", 2209632543419),
    ("3", "SERVICIOS NO PERSONALES", 11049080168894),
    ("4", "BIENES DE USO", 5781570935026),
    ("5", "TRANSFERENCIAS", 724346998226),
    ("6", "ACTIVOS FINANCIEROS", 17009538911),
    ("7", "SERVICIO DE LA DEUDA Y DISMINUCION DE OTROS PASIVOS", 1489803003579),
]
DORADO_SUMA = 32430395540545


class FalloDeTest(Exception):
    pass


def test_dorado():
    """2025 IV gastos por objeto tiene que dar exactamente los siete numeros."""
    ruta = os.path.join(EJECUCION, "2025_iv_gastos_por_objeto.pdf")
    filas, total_general = P.parse_gastos_objeto(ruta)

    errores = []
    if len(filas) != len(DORADO):
        errores.append("se esperaban %d objetos, salieron %d" % (len(DORADO), len(filas)))

    for fila, (codigo, nombre, esperado) in zip(filas, DORADO):
        if fila["objeto_codigo"] != codigo or fila["objeto"] != nombre:
            errores.append("objeto %s: se esperaba %r y salio %r" % (
                codigo, nombre, fila["objeto"]))
        if fila["devengado"] != esperado:
            errores.append("objeto %s (%s): devengado esperado %s, obtenido %s" % (
                codigo, nombre, P.formatear(esperado), P.formatear(fila["devengado"])))

    suma = sum(f["devengado"] for f in filas)
    if suma != DORADO_SUMA:
        errores.append("suma esperada %s, obtenida %s" % (
            P.formatear(DORADO_SUMA), P.formatear(suma)))
    if total_general is None:
        errores.append("no se encontro la linea TOTALES GENERALES")
    elif total_general["devengado"] != DORADO_SUMA:
        errores.append("TOTALES GENERALES del PDF: esperado %s, obtenido %s" % (
            P.formatear(DORADO_SUMA), P.formatear(total_general["devengado"])))

    if errores:
        raise FalloDeTest("TEST DORADO FALLADO:\n  " + "\n  ".join(errores))

    print("TEST DORADO — 2025_iv_gastos_por_objeto.pdf")
    print("-" * 74)
    for fila, (codigo, nombre, _) in zip(filas, DORADO):
        print("  %s %-50s %20s  OK" % (
            codigo, nombre[:50].capitalize(), P.formatear(fila["devengado"])))
    print("  %-53s %20s  OK" % ("SUMA", P.formatear(suma)))
    print("  %-53s %20s  OK" % ("TOTALES GENERALES del PDF",
                                P.formatear(total_general["devengado"])))
    print()


# --------------------------------------------------------------------------
# validaciones por trimestre
# --------------------------------------------------------------------------

def _clave(fila):
    """Identificador legible de la fila dentro de su trimestre."""
    for campos in (("objeto_codigo", "objeto"), ("rubro_codigo", "rubro"),
                   ("codigo", "concepto")):
        if campos[0] in fila:
            return "%s %s" % (fila[campos[0]], fila[campos[1]])
    if fila.get("nivel") == "funcion":
        return "%s %s" % (fila["funcion_codigo"], fila["funcion"])
    return "%s %s" % (fila["finalidad_codigo"], fila["finalidad"])


def validar_aritmetica(filas, aprobado, modif, vigente, devengado, fallas):
    """aprobado + modificaciones == vigente, y devengado <= vigente.

    Una celda vacia en estos PDF significa cero (el Municipio no imprime los
    ceros), asi que para la suma se toma como cero. Si aun asi no cierra, se
    anota: puede ser un error de la fuente y no se toca.
    """
    for fila in filas:
        a, m, v = fila.get(aprobado), fila.get(modif), fila.get(vigente)
        d = fila.get(devengado)

        if v is None:
            fallas.append((fila, "%s vacio, no se puede validar la fila" % vigente))
            continue

        suma = (a or 0) + (m or 0)
        if suma != v:
            fallas.append((fila, "%s + %s != %s: %s + %s = %s, %s es %s" % (
                aprobado, modif, vigente, P.formatear(a or 0), P.formatear(m or 0),
                P.formatear(suma), vigente, P.formatear(v))))

        if d is not None and d > v:
            fallas.append((fila, "%s > %s: %s vs %s (diferencia %s)" % (
                devengado, vigente, P.formatear(d), P.formatear(v),
                P.formatear(d - v))))


def validar_suma_contra_total(filas, generales, columnas, etiqueta, fallas):
    """La suma de las filas de cada PDF tiene que dar el total general del PDF."""
    por_fuente = {}
    for fila in filas:
        por_fuente.setdefault(fila["fuente"], []).append(fila)

    for fuente, grupo in sorted(por_fuente.items()):
        general = generales.get(fuente)
        if general is None:
            fallas.append((grupo[0], "el PDF no trae linea de total general"))
            continue
        for columna in columnas:
            esperado = general.get(columna)
            if esperado is None:
                continue
            suma = sum(f[columna] for f in grupo if f.get(columna) is not None)
            if suma != esperado:
                fallas.append((grupo[0], "suma de %s (%s) = %s, total general = %s"
                               " (diferencia %s)" % (
                                   etiqueta, columna, P.formatear(suma),
                                   P.formatear(esperado),
                                   P.formatear(suma - esperado))))


def validar_deuda(filas, fallas):
    """La deuda consolidada tiene que ser la suma de sus rubros 1.x."""
    por_fuente = {}
    for fila in filas:
        por_fuente.setdefault(fila["fuente"], []).append(fila)

    for fuente, grupo in sorted(por_fuente.items()):
        cabecera = [f for f in grupo if f["codigo"] == "1"]
        hijos = [f for f in grupo if f["codigo"].count(".") == 1
                 and f["codigo"].startswith("1.")]
        if not cabecera or not hijos:
            continue
        for columna in ("saldo",):
            esperado = cabecera[0].get(columna)
            if esperado is None:
                continue
            suma = sum(f[columna] for f in hijos if f.get(columna) is not None)
            if suma != esperado:
                fallas.append((cabecera[0],
                               "suma de los rubros 1.x (%s) = %s, "
                               "'1. DEUDA CONSOLIDADA' dice %s (diferencia %s)" % (
                                   columna, P.formatear(suma), P.formatear(esperado),
                                   P.formatear(suma - esperado))))


def main():
    test_dorado()

    print("PARSEO DE TODOS LOS TRIMESTRES")
    print("-" * 74)
    resultado = P.main()
    print()

    objeto, gen_objeto = resultado["gastos_objeto"]
    recursos, gen_recursos = resultado["recursos"]
    fyf, gen_fyf = resultado["fyf"]
    deuda, _ = resultado["deuda"]

    fallas = []
    validar_aritmetica(objeto, "credito_aprobado", "modificaciones",
                       "credito_vigente", "devengado", fallas)
    validar_suma_contra_total(
        objeto, gen_objeto,
        ["credito_aprobado", "modificaciones", "credito_vigente", "devengado",
         "pagado"], "los objetos del gasto", fallas)

    validar_aritmetica(recursos, "calculado", "modificaciones", "vigente",
                       "devengado", fallas)
    validar_suma_contra_total(
        recursos, gen_recursos,
        ["calculado", "modificaciones", "vigente", "devengado", "percibido"],
        "los rubros de recursos", fallas)

    finalidades = [f for f in fyf if f["nivel"] == "finalidad"]
    validar_aritmetica(fyf, "credito_aprobado", "modificaciones",
                       "credito_vigente", "devengado", fallas)
    validar_suma_contra_total(
        finalidades, gen_fyf,
        ["credito_aprobado", "modificaciones", "credito_vigente", "devengado",
         "pagado"], "las finalidades", fallas)

    validar_deuda(deuda, fallas)

    ruta = os.path.join(P.DATA, "INCONSISTENCIAS.csv")
    os.makedirs(P.DATA, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fuente", "anio", "trimestre", "periodo_desde",
                    "periodo_hasta", "periodo_tipo", "fila", "motivo"])
        for fila, motivo in fallas:
            w.writerow([fila["fuente"], fila["anio"], fila["trimestre"],
                        fila.get("periodo_desde", ""), fila.get("periodo_hasta", ""),
                        fila.get("periodo_tipo", ""), _clave(fila), motivo])

    print("VALIDACIONES")
    print("-" * 74)
    print("  filas revisadas: %d gastos por objeto, %d recursos, %d finalidad y"
          " funcion, %d deuda" % (len(objeto), len(recursos), len(fyf), len(deuda)))
    print("  chequeos: aprobado+modificaciones==vigente | devengado<=vigente |"
          " suma de partes==total general del PDF")
    if fallas:
        print("  %d inconsistencias -> data/INCONSISTENCIAS.csv" % len(fallas))
        por_tipo = {}
        for fila, _ in fallas:
            clave = fila.get("periodo_tipo", "n/a")
            por_tipo[clave] = por_tipo.get(clave, 0) + 1
        print("  por tipo de periodo del informe: %s" % ", ".join(
            "%s=%d" % kv for kv in sorted(por_tipo.items())))
        print()
        for fila, motivo in fallas[:15]:
            print("    %s %s %s | %s" % (fila["fuente"], fila["anio"],
                                         fila["trimestre"], motivo))
        if len(fallas) > 15:
            print("    ... y %d mas en el CSV" % (len(fallas) - 15))
    else:
        print("  0 inconsistencias. INCONSISTENCIAS.csv queda vacio.")
    print()
    print("TEST DORADO OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
