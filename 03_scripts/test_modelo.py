#!/usr/bin/env python3
"""
Tests del modelo de flujo de caja.

Las tres validaciones que pide la tarea son duras. Si alguna falla el modelo no
sirve y el script sale distinto de cero.

  1. El anio 0 reproduce la ejecucion 2025 real, contra el Estado de Situacion
     Economico-Financiera, no contra si mismo.
  2. Identidad contable en TODOS los anios y TODOS los escenarios:
     resultado financiero = ingresos totales - gastos totales.
  3. El stock de deuda de cada anio = stock anterior + nuevo endeudamiento
     - amortizacion.

Uso:
    python3 03_scripts/test_modelo.py
"""

import csv
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import modelo as M

REPO = M.REPO
CENTAVO = Decimal("0.01")

# Leidos a mano de la cuenta Ahorro-Inversion del SEF 2025 anual, pagina 1.
DORADO_2025 = {
    "ingresos_corrientes": Decimal("301154665135.71"),
    "gastos_corrientes": Decimal("251403592133.29"),
    "ahorro_corriente": Decimal("49751073002.42"),
    "recursos_de_capital": Decimal("2030100797.22"),
    "gastos_de_capital": Decimal("57832237847.26"),
    "ingresos_totales": Decimal("303184765932.93"),
    "gastos_totales": Decimal("309235829980.55"),
    "resultado_financiero": Decimal("-6051064047.62"),
}
DORADO_PROGRAMA = {
    "gasto_empleo": Decimal("170314500.62"),
    "gasto_vivienda": Decimal("335387189.32"),
}
DORADO_DEUDA = Decimal("8960328499.00")


class FalloDeTest(Exception):
    pass


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def _d(x):
    x = (x or "").strip()
    return Decimal(x) if x else Decimal(0)


def test_anio_cero():
    """El anio 0 tiene que ser la ejecucion real, al centavo."""
    errores = []
    filas = _leer("data/modelo_flujo_caja.csv")
    escenarios = {f["escenario"] for f in filas}
    for esc in sorted(escenarios):
        cero = [f for f in filas
                if f["escenario"] == esc and int(f["anio"]) == M.ANIO_BASE]
        if len(cero) != 1:
            errores.append("%s: hay %d filas de %d" % (esc, len(cero), M.ANIO_BASE))
            continue
        f = cero[0]
        for clave, esperado in DORADO_2025.items():
            leido = _d(f[clave])
            if abs(leido - esperado) > CENTAVO:
                errores.append("%s / %s: esperado %s, el modelo dice %s"
                               % (esc, clave, esperado, leido))
        if abs(_d(f["stock_deuda"]) - DORADO_DEUDA) > CENTAVO:
            errores.append("%s: stock de deuda %s, esperado %s"
                           % (esc, f["stock_deuda"], DORADO_DEUDA))

    # Y la linea de base publicada tiene que decir lo mismo.
    base = {f["clave"]: _d(f["monto"]) for f in _leer("data/baseline_2025.csv")}
    for clave, esperado in DORADO_2025.items():
        if abs(base.get(clave, Decimal(0)) - esperado) > CENTAVO:
            errores.append("baseline_2025.csv / %s: esperado %s, dice %s"
                           % (clave, esperado, base.get(clave)))
    for clave, esperado in DORADO_PROGRAMA.items():
        if abs(base.get(clave, Decimal(0)) - esperado) > CENTAVO:
            errores.append("baseline_2025.csv / %s: esperado %s, dice %s"
                           % (clave, esperado, base.get(clave)))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return len(escenarios)


def test_identidad_contable():
    errores = []
    revisados = 0
    for f in _leer("data/modelo_flujo_caja.csv"):
        revisados += 1
        calc = _d(f["ingresos_totales"]) - _d(f["gastos_totales"])
        if abs(calc - _d(f["resultado_financiero"])) > CENTAVO:
            errores.append("%s %s: ingresos - gastos da %s y la fila dice %s"
                           % (f["escenario"], f["anio"], calc,
                              f["resultado_financiero"]))
        # Y las dos aperturas tienen que sumar sus totales.
        ing = (_d(f["ingresos_corrientes"]) + _d(f["recursos_de_capital"]))
        if abs(ing - _d(f["ingresos_totales"])) > CENTAVO:
            errores.append("%s %s: corrientes + capital no da ingresos totales"
                           % (f["escenario"], f["anio"]))
        gas = (_d(f["gastos_corrientes"]) + _d(f["gastos_de_capital"]))
        if abs(gas - _d(f["gastos_totales"])) > CENTAVO:
            errores.append("%s %s: corrientes + capital no da gastos totales"
                           % (f["escenario"], f["anio"]))
        aho = _d(f["ingresos_corrientes"]) - _d(f["gastos_corrientes"])
        if abs(aho - _d(f["ahorro_corriente"])) > CENTAVO:
            errores.append("%s %s: el ahorro corriente no cierra"
                           % (f["escenario"], f["anio"]))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores[:15]))
    return revisados


def test_deuda():
    errores = []
    revisados = 0
    filas = _leer("data/modelo_flujo_caja.csv")
    por_esc = {}
    for f in filas:
        por_esc.setdefault(f["escenario"], []).append(f)
    for esc, fs in sorted(por_esc.items()):
        fs.sort(key=lambda f: int(f["anio"]))
        for anterior, actual in zip(fs, fs[1:]):
            revisados += 1
            esperado = (_d(anterior["stock_deuda"])
                        + _d(actual["nuevo_endeudamiento"])
                        - _d(actual["amortizacion"]))
            if abs(esperado - _d(actual["stock_deuda"])) > CENTAVO:
                errores.append(
                    "%s %s: %s + %s - %s da %s, y la fila dice %s"
                    % (esc, actual["anio"], anterior["stock_deuda"],
                       actual["nuevo_endeudamiento"], actual["amortizacion"],
                       esperado, actual["stock_deuda"]))
            if _d(actual["stock_deuda"]) < 0:
                errores.append("%s %s: stock de deuda negativo"
                               % (esc, actual["anio"]))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores[:15]))
    return revisados


def test_parametros_desde_datos():
    """
    Ningun parametro puede estar escrito a mano: los tres se recalculan desde
    las series y tienen que dar lo que dice data/parametros_modelo.csv.
    """
    publicados = {f["parametro"]: Decimal(f["valor"])
                  for f in _leer("data/parametros_modelo.csv")}
    import parametros_modelo as P
    calculados = {
        "recursos_propios_tasa_real_anual": P.recursos_propios()["tasa_punta_a_punta"],
        "coparticipacion_caida_anual": P.coeficiente_coparticipacion()["caida_anual_pct"],
        "rigidez_nucleo": P.rigidez()["nucleo_pct"],
        "percepcion_recursos_corrientes": P.percepcion()["percepcion_pct"],
    }
    errores = []
    for clave, valor in calculados.items():
        if publicados.get(clave) != valor:
            errores.append("%s: publicado %s, recalculado %s"
                           % (clave, publicados.get(clave), valor))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return calculados


def main():
    print("=" * 78)
    print("MODELO DE FLUJO DE CAJA - VALIDACIONES")
    print("=" * 78)
    fallas = 0
    for nombre, fn in (
            ("el anio 0 reproduce la ejecucion 2025 real", test_anio_cero),
            ("identidad contable en todos los anios y escenarios",
             test_identidad_contable),
            ("stock de deuda = anterior + nuevo - amortizacion", test_deuda),
            ("los parametros salen de los datos, no estan escritos a mano",
             test_parametros_desde_datos)):
        try:
            r = fn()
        except FalloDeTest as e:
            print("  FALLA  %s\n%s" % (nombre, e))
            fallas += 1
            continue
        extra = ""
        if fn is test_anio_cero:
            extra = "  (%d escenarios, contra el SEF 2025)" % r
        elif fn is test_identidad_contable:
            extra = "  (%d filas, 4 identidades cada una)" % r
        elif fn is test_deuda:
            extra = "  (%d transiciones de anio)" % r
        elif fn is test_parametros_desde_datos:
            extra = "  (%d parametros recalculados)" % len(r)
        print("  OK     %s%s" % (nombre, extra))

    print()
    print("=" * 78)
    print("RESULTADO FINANCIERO POR ESCENARIO (millones de pesos de dic-2025)")
    print("=" * 78)
    filas = _leer("data/modelo_flujo_caja.csv")
    escs = sorted({f["escenario"] for f in filas})
    hitos = [2025, 2028, 2031, 2034, 2037]
    print("  %-22s %s" % ("escenario", " ".join("%12d" % h for h in hitos)))
    for esc in escs:
        vals = []
        for h in hitos:
            x = [f for f in filas if f["escenario"] == esc and int(f["anio"]) == h]
            vals.append("%12.0f" % (_d(x[0]["resultado_financiero"]) / 1_000_000)
                        if x else "%12s" % "-")
        print("  %-22s %s" % (esc, " ".join(vals)))
    print()
    if fallas:
        print("HAY %d VALIDACION(ES) EN FALLA" % fallas)
        return 1
    print("TEST MODELO OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
