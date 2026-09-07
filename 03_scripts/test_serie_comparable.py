#!/usr/bin/env python3
"""
Tests de la serie comparable de gasto.

Lo que sostiene:
  1. La serie comparable usa UN SOLO concepto en todas sus filas.
  2. Ningun anio sin dato fue rellenado con otro concepto.
  3. La identidad que habilita derivar el concepto desde los objetos cierra en
     los anios donde se puede probar.
  4. Cada valor derivado se puede rehacer sumando y restando las filas del
     inventario, sin correr el script.
  5. La serie heterogenea quedo marcada: columna concepto_heterogeneo y
     advertencia arriba del archivo.
  6. Ningun par listado como valido compara dos conceptos distintos.

Uso:
    python3 03_scripts/test_serie_comparable.py
"""

import csv
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import serie_comparable as S

REPO = S.REPO


class FalloDeTest(Exception):
    pass


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def _cabecera_comentada(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8") as f:
        return [l for l in f if l.startswith("#")]


def test_un_solo_concepto():
    filas = _leer("data/serie_gastos_comparable.csv")
    conceptos = {f["concepto"] for f in filas}
    if conceptos != {S.CONCEPTO_TXT}:
        raise FalloDeTest("  la serie comparable tiene %d conceptos: %s"
                          % (len(conceptos), sorted(conceptos)))
    return len(filas), len([f for f in filas if f["monto_constante_dic2025"]])


def test_sin_dato_queda_vacio():
    errores = []
    for f in _leer("data/serie_gastos_comparable.csv"):
        vacio = not f["monto_constante_dic2025"]
        sin = f["origen_del_dato"] == "sin dato"
        if vacio != sin:
            errores.append("%s: origen=%r pero el importe %s"
                           % (f["anio"], f["origen_del_dato"],
                              "esta vacio" if vacio else "tiene valor"))
        if sin and (f["monto_nominal"] or f["componentes"]):
            errores.append("%s se marca sin dato pero trae valores" % f["anio"])
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return [f["anio"] for f in _leer("data/serie_gastos_comparable.csv")
            if f["origen_del_dato"] == "sin dato"]


def test_identidad():
    r = S.main()
    checks = r["checks"]
    if not checks:
        raise FalloDeTest("  no se pudo probar la identidad en ningun anio")
    cierran = [c for c in checks if c["cierra"] == "si"]
    if len(cierran) < len(checks) - 1:
        raise FalloDeTest(
            "  la identidad falla en %d de %d anios; con mas de uno no se"
            " sostiene derivar nada:\n%s"
            % (len(checks) - len(cierran), len(checks),
               "\n".join("    %d: %s" % (c["anio"], c["nota"])
                         for c in checks if c["cierra"] != "si")))
    return len(cierran), len(checks), [c for c in checks if c["cierra"] != "si"]


def test_derivados_se_rehacen():
    """
    Cada anio derivado tiene que poder rehacerse desde el inventario: sumar los
    objetos del anio y restar los financieros da el importe publicado.
    """
    inv = _leer("data/conceptos_disponibles_por_anio.csv")
    errores = []
    revisados = 0
    for f in _leer("data/serie_gastos_comparable.csv"):
        if f["origen_del_dato"] != "derivado":
            continue
        anio = f["anio"]
        objetos = [x for x in inv
                   if x["anio"] == anio and x["tipo"] == "ejecutado"
                   and "objeto" in x["familia"] and x["nivel"] == "componente"]
        if not objetos:
            errores.append("%s: no hay objetos en el inventario" % anio)
            continue
        suma = sum((Decimal(x["monto_constante_dic2025"]) for x in objetos
                    if x["concepto_en_la_fuente"].split(" ", 1)[-1].strip()
                    not in S.OBJETOS_FINANCIEROS
                    and x["concepto_en_la_fuente"] not in S.OBJETOS_FINANCIEROS),
                   Decimal(0))
        suma = suma.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if suma != Decimal(f["monto_constante_dic2025"]):
            errores.append("%s: el inventario da %s y la serie dice %s"
                           % (anio, suma, f["monto_constante_dic2025"]))
        revisados += 1
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return revisados


def test_heterogenea_marcada():
    ruta = "data/serie_gastos_totales_real.csv"
    filas = _leer(ruta)
    errores = []
    if filas and "concepto_heterogeneo" not in filas[0]:
        errores.append("falta la columna concepto_heterogeneo")
    if filas and "concepto" in filas[0]:
        errores.append("todavia existe la columna 'concepto' a secas")
    # La advertencia va cortada en varias lineas de comentario, asi que se
    # aplana antes de buscar las frases.
    cab = re.sub(r"[#\s]+", " ",
                 "".join(_cabecera_comentada(ruta))).upper()
    for frase in ("ADVERTENCIA", "MEZCLA CONCEPTOS", "NO SON COMPARACIONES"):
        if frase not in cab:
            errores.append("la advertencia de arriba del CSV no dice %r" % frase)
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return len({f["concepto_heterogeneo"] for f in filas})


def test_pares_mismo_concepto():
    """
    Ningun par de COMPARACIONES_VALIDAS.md puede juntar dos anios que midan
    conceptos distintos en la serie de la que sale.
    """
    het = {f["anio"]: f["concepto_heterogeneo"]
           for f in _leer("data/serie_gastos_totales_real.csv")}
    texto = open(os.path.join(REPO, "data/COMPARACIONES_VALIDAS.md"),
                 encoding="utf-8").read()
    seccion = texto.split("## 4.")[-1]
    errores = []
    concepto_actual = None
    revisados = 0
    for linea in seccion.splitlines():
        if linea.startswith("### "):
            concepto_actual = linea[4:].strip()
            continue
        m = re.match(r"\|\s*(\d{4})\s*\|\s*(\d{4})\s*\|", linea)
        if not m or concepto_actual is None:
            continue
        a, b = m.group(1), m.group(2)
        revisados += 1
        if het.get(a) != concepto_actual or het.get(b) != concepto_actual:
            errores.append("el par %s-%s figura bajo %r pero los anios miden "
                           "%r y %r" % (a, b, concepto_actual, het.get(a),
                                        het.get(b)))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return revisados


def main():
    try:
        S.verificar_orden_de_corrida()
    except S.ErrorDeSerie as e:
        print("ORDEN DE CORRIDA INCORRECTO\n  %s" % e)
        return 1

    print("=" * 78)
    print("SERIE COMPARABLE - VALIDACIONES")
    print("=" * 78)
    fallas = 0

    for nombre, fn in (
            ("la serie comparable usa un solo concepto", test_un_solo_concepto),
            ("los anios sin dato quedan vacios, no sustituidos",
             test_sin_dato_queda_vacio),
            ("la identidad que habilita derivar cierra", test_identidad),
            ("cada valor derivado se rehace desde el inventario",
             test_derivados_se_rehacen),
            ("la serie heterogenea quedo marcada como tal",
             test_heterogenea_marcada),
            ("ningun par valido compara dos conceptos distintos",
             test_pares_mismo_concepto)):
        try:
            r = fn()
        except FalloDeTest as e:
            print("  FALLA  %s\n%s" % (nombre, e))
            fallas += 1
            continue
        extra = ""
        if fn is test_un_solo_concepto:
            extra = "  (%d filas, %d con dato)" % r
        elif fn is test_sin_dato_queda_vacio:
            extra = "  (vacios: %s)" % (", ".join(r) or "ninguno")
        elif fn is test_identidad:
            extra = "  (%d de %d anios probables%s)" % (
                r[0], r[1], "" if not r[2] else
                "; no cierra %s y por eso ese anio usa el valor publicado"
                % ", ".join(str(c["anio"]) for c in r[2]))
        elif fn is test_derivados_se_rehacen:
            extra = "  (%d anios derivados recalculados)" % r
        elif fn is test_heterogenea_marcada:
            extra = "  (mezcla %d conceptos)" % r
        elif fn is test_pares_mismo_concepto:
            extra = "  (%d pares revisados)" % r
        print("  OK     %s%s" % (nombre, extra))

    print()
    print("=" * 78)
    print("SERIE COMPARABLE (pesos constantes de dic-2025)")
    print("=" * 78)
    print("  %-6s %22s %10s %8s  %s" % ("anio", "constante dic-2025",
                                        "var real", "brecha", "origen"))
    for f in _leer("data/serie_gastos_comparable.csv"):
        print("  %-6s %22s %10s %8s  %s"
              % (f["anio"], f["monto_constante_dic2025"] or "—",
                 (f["var_real_pct"] + "%") if f["var_real_pct"] else "—",
                 f["brecha_anios"] or "—", f["origen_del_dato"]))
    print()
    if fallas:
        print("HAY %d VALIDACION(ES) EN FALLA" % fallas)
        return 1
    print("TEST SERIE COMPARABLE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
