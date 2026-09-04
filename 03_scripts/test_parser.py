#!/usr/bin/env python3
"""
Tests del parser de ejecucion presupuestaria.

El test dorado es el primero y es el que manda: si no reproduce exactamente los
siete devengados de 2025 IV, no hay nada mas que discutir.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import parse_ejecucion as P

RAIZ = P.RAIZ
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
        obtenido = fila["devengado"]
        if obtenido != esperado:
            errores.append("objeto %s (%s): devengado esperado %s, obtenido %s" % (
                codigo, nombre, P.formatear(esperado), P.formatear(obtenido)))

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
    print("-" * 68)
    for fila, (codigo, nombre, esperado) in zip(filas, DORADO):
        print("  %s %-52s %22s  OK" % (
            codigo, nombre[:52].title(), P.formatear(fila["devengado"])))
    print("  %-55s %22s  OK" % ("SUMA", P.formatear(suma)))
    print("  %-55s %22s  OK" % (
        "TOTALES GENERALES del PDF", P.formatear(total_general["devengado"])))
    print()


def main():
    test_dorado()
    print("TODO OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
