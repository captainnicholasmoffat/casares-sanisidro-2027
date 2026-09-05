#!/usr/bin/env python3
"""
Tests del deflactor.

Igual que en el parser, primero va el test dorado: si el empalme no reproduce
el coeficiente que sale a mano de las dos series publicas, no hay nada mas que
discutir. Despues se valida que todo importe nominal tenga su constante, que
diciembre de 2025 se deflacte a si mismo, y que el coeficiente elegido para
cada fila respete periodo_tipo.

Lo que NO se corrige: los saltos reales de la serie de gastos totales. Si un
anio varia mas de 40% en terminos reales contra el anterior queda anotado en
data/SALTOS_REALES.csv para revision humana, y el test no falla por eso.

Uso:
    python3 03_scripts/test_deflactor.py
Sale 0 si el test dorado y las validaciones duras pasan.
"""

import csv
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import deflactor as D

REPO = D.REPO

# El coeficiente de empalme leido a mano de los dos CSV crudos:
#   IPC INDEC nacional nivel general, dic-2016 = 100
#   IPC San Luis nivel general,       dic-2016 = 1350,48
# k = 100 / 1350,48
DORADO_INDEC_DIC2016 = Decimal("100")
DORADO_SANLUIS_DIC2016 = Decimal("1350.48")

# Fila leida a mano de data/ejecucion_gastos_objeto.csv, 2025 IV, objeto 1.
DORADO_FILA = {
    "nominal": Decimal("111589523524.90"),
    "coef": Decimal("1.12818726"),
    "constante": Decimal("125893878790.26"),
}


class FalloDeTest(Exception):
    pass


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _num(txt):
    txt = (txt or "").strip()
    return Decimal(txt) if txt else None


def _r2(d):
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def test_dorado():
    """El empalme tiene que reproducirse con las dos series publicas."""
    errores = []

    indec = D.leer_indec()
    sanluis = D.leer_sanluis()
    if indec[D.MES_EMPALME] != DORADO_INDEC_DIC2016:
        errores.append("IPC INDEC dic-2016: esperado %s, leido %s"
                       % (DORADO_INDEC_DIC2016, indec[D.MES_EMPALME]))
    if sanluis[D.MES_EMPALME] != DORADO_SANLUIS_DIC2016:
        errores.append("IPC San Luis dic-2016: esperado %s, leido %s"
                       % (DORADO_SANLUIS_DIC2016, sanluis[D.MES_EMPALME]))

    k = D.coeficiente_de_empalme(indec, sanluis)
    k_mano = DORADO_INDEC_DIC2016 / DORADO_SANLUIS_DIC2016
    if k != k_mano:
        errores.append("coeficiente de empalme: a mano %s, del script %s"
                       % (k_mano, k))

    # El empalme no puede inventar inflacion: la variacion de dic-2016 tiene
    # que ser la de San Luis, no un salto de nivel entre las dos series.
    ipc = _leer("data/ipc_indec_mensual.csv")
    por_mes = {(int(f["anio"]), int(f["mes"])): f for f in ipc}
    var_publicada = Decimal(por_mes[(2016, 12)]["variacion_mensual"])
    var_sanluis = (sanluis[(2016, 12)] / sanluis[(2016, 11)] - 1) * 100
    if abs(var_publicada - var_sanluis) > Decimal("0.0001"):
        errores.append("la variacion de dic-2016 (%s%%) no coincide con la de "
                       "San Luis (%s%%): el empalme esta metiendo un salto"
                       % (var_publicada, var_sanluis))

    if Decimal(por_mes[(2016, 12)]["indice"]) != Decimal("100.0000"):
        errores.append("dic-2016 tiene que valer 100 (es la base del INDEC)")

    # Y la fila dorada del dataset aplicado.
    fila = None
    for f in _leer("data/ejecucion_gastos_objeto.csv"):
        if (f["anio"] == "2025" and f["periodo_tipo"] == "acumulado_anual"
                and f["objeto_codigo"] == "1"):
            fila = f
    if fila is None:
        errores.append("no esta la fila 2025 IV objeto 1 en gastos por objeto")
    else:
        for campo, esperado, col in (
                ("nominal", DORADO_FILA["nominal"], "devengado"),
                ("coef", DORADO_FILA["coef"], "coef_deflactor"),
                ("constante", DORADO_FILA["constante"],
                 "monto_constante_dic2025")):
            leido = Decimal(fila[col])
            if leido != esperado:
                errores.append("2025 IV objeto 1, %s: esperado %s, leido %s"
                               % (col, esperado, leido))

    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))
    return k


def test_serie_mensual_sin_huecos():
    ipc = _leer("data/ipc_indec_mensual.csv")
    claves = [(int(f["anio"]), int(f["mes"])) for f in ipc]
    esperado = list(D.meses_entre(claves[0], claves[-1]))
    faltan = [c for c in esperado if c not in set(claves)]
    if faltan:
        raise FalloDeTest("  faltan meses en la serie: %s" % (faltan[:12],))
    orig = {f["serie_origen"] for f in ipc}
    if len(orig) != 2:
        raise FalloDeTest("  se esperaban 2 series de origen, hay %d: %s"
                          % (len(orig), sorted(orig)))
    return len(claves), claves[0], claves[-1]


def test_diciembre_2025_se_deflacta_a_si_mismo():
    errores = []
    fila = None
    for f in _leer("data/deflactor.csv"):
        if f["anio"] == "2025":
            fila = f
    if fila is None:
        errores.append("no hay fila 2025 en deflactor.csv")
    elif Decimal(fila["coef_diciembre"]) != Decimal(1):
        errores.append("coef_diciembre de 2025 tiene que ser exactamente 1, "
                       "es %s" % fila["coef_diciembre"])

    # Y el stock de deuda al 30/12/2025, que se deflacta por el indice del mes
    # de la fecha de corte, tiene que quedar igual que su nominal.
    for f in _leer("data/deuda_stock.csv"):
        if f["fecha_corte"] != "30/12/2025":
            continue
        if Decimal(f["coef_deflactor"]) != Decimal(1):
            errores.append("deuda al 30/12/2025: coeficiente %s, deberia ser 1"
                           % f["coef_deflactor"])
            break
        if _num(f["saldo"]) != _num(f["monto_constante_dic2025"]):
            errores.append("deuda al 30/12/2025 concepto %s: nominal %s != "
                           "constante %s" % (f["codigo"], f["saldo"],
                                             f["monto_constante_dic2025"]))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores))


def test_todo_nominal_tiene_constante():
    """
    Ningun importe nominal puede quedarse sin su constante, y ningun constante
    puede aparecer donde no habia nominal. Ademas el constante tiene que ser
    exactamente nominal * coeficiente publicado: cualquiera reproduce la
    cuenta con el CSV en la mano, sin correr el script.
    """
    errores = []
    revisados = 0
    for spec in D.DATASETS:
        ruta = os.path.join(REPO, spec["ruta"])
        if not os.path.exists(ruta) or not spec.get("montos"):
            continue
        filas = _leer(spec["ruta"])
        for n, f in enumerate(filas, 2):
            if "coef_deflactor" not in f or not f["coef_deflactor"]:
                errores.append("%s fila %d: sin coef_deflactor"
                               % (spec["ruta"], n))
                continue
            coef = Decimal(f["coef_deflactor"])
            if coef <= 0:
                errores.append("%s fila %d: coeficiente %s"
                               % (spec["ruta"], n, coef))
            for col in spec["montos"]:
                if col not in f:
                    continue
                nom = _num(f[col])
                con = _num(f.get(col + D.SUFIJO))
                if nom is None and con is not None:
                    errores.append("%s fila %d col %s: hay constante sin "
                                   "nominal" % (spec["ruta"], n, col))
                elif nom is not None and con is None:
                    errores.append("%s fila %d col %s: nominal %s sin "
                                   "constante" % (spec["ruta"], n, col, nom))
                elif nom is not None:
                    revisados += 1
                    if _r2(nom * coef) != con:
                        errores.append(
                            "%s fila %d col %s: %s * %s = %s, publicado %s"
                            % (spec["ruta"], n, col, nom, coef,
                               _r2(nom * coef), con))
            # La columna principal tiene que ser el espejo de una de las otras.
            principal = spec.get("principal")
            if principal and principal in f:
                if f.get(D.COL_PRINCIPAL) != f.get(principal + D.SUFIJO):
                    errores.append("%s fila %d: monto_constante_dic2025 no "
                                   "coincide con %s" % (spec["ruta"], n,
                                                        principal + D.SUFIJO))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores[:20]))
    return revisados


def test_periodo_tipo_respetado():
    """
    Un acumulado anual no se puede deflactar con el indice de un trimestre.
    El coeficiente de cada fila tiene que salir de tantos meses como cubre el
    rango de fechas del informe.
    """
    errores = []
    esperados = {"acumulado_anual": 12, "trimestre": 3}
    for spec in D.DATASETS:
        if spec["modo"] != "periodo":
            continue
        ruta = os.path.join(REPO, spec["ruta"])
        if not os.path.exists(ruta):
            continue
        for n, f in enumerate(_leer(spec["ruta"]), 2):
            tipo = f.get("periodo_tipo", "")
            meses = f["base_coef"].count("d ") + 1 if "|" in f["base_coef"] else 0
            meses = len([x for x in f["base_coef"].split("|")[-1].split()
                         if ":" in x])
            if tipo in esperados and meses != esperados[tipo]:
                errores.append("%s fila %d: periodo_tipo=%s pero el "
                               "coeficiente sale de %d meses"
                               % (spec["ruta"], n, tipo, meses))
    if errores:
        raise FalloDeTest("\n".join("  " + e for e in errores[:20]))


def revisar_saltos():
    """No falla: reporta. Los saltos son un hallazgo, no un bug."""
    serie = _leer("data/serie_gastos_totales_real.csv")
    saltos = _leer("data/SALTOS_REALES.csv")
    return serie, saltos


def test_columnas_presentes():
    """
    Guardia de orden de corrida.

    03_scripts/test_parser.py reescribe los CSV de ejecucion desde los PDF, asi
    que borra las columnas del deflactor. El orden es: parser primero,
    deflactor despues. Si las columnas no estan, se dice por que y no se
    escupen 500 errores.
    """
    faltan = []
    for spec in D.DATASETS:
        ruta = os.path.join(REPO, spec["ruta"])
        if not os.path.exists(ruta) or not spec.get("montos"):
            continue
        filas = _leer(spec["ruta"])
        if filas and "coef_deflactor" not in filas[0]:
            faltan.append(spec["ruta"])
    if faltan:
        raise FalloDeTest(
            "  Estos datasets no tienen las columnas del deflactor:\n"
            + "\n".join("    " + r for r in faltan)
            + "\n  Pasa cuando se corre test_parser.py despues de deflactor.py:"
              "\n  el parser reescribe los CSV desde los PDF y se las lleva "
              "puestas.\n  Correr:  python3 03_scripts/deflactor.py")


def main():
    try:
        test_columnas_presentes()
    except FalloDeTest as e:
        print("ORDEN DE CORRIDA INCORRECTO\n%s" % e)
        return 1

    print("=" * 74)
    print("TEST DORADO DEL DEFLACTOR")
    print("=" * 74)
    try:
        k = test_dorado()
    except FalloDeTest as e:
        print("FALLO\n%s" % e)
        return 1
    print("  IPC INDEC dic-2016    = 100 (base)")
    print("  IPC San Luis dic-2016 = 1350.48")
    print("  coeficiente empalme k = 100 / 1350.48 = %s" % D._fmt(k, 10))
    print("  dic-2016 empalmado sin salto artificial: OK")
    print("  fila dorada 2025 IV objeto 1: %s * %s = %s  OK" % (
        DORADO_FILA["nominal"], DORADO_FILA["coef"], DORADO_FILA["constante"]))
    print()

    print("=" * 74)
    print("VALIDACIONES")
    print("=" * 74)
    fallas = 0
    for nombre, fn in (
            ("serie mensual continua y con dos origenes declarados",
             test_serie_mensual_sin_huecos),
            ("diciembre 2025 se deflacta a si mismo (coef = 1)",
             test_diciembre_2025_se_deflacta_a_si_mismo),
            ("todo nominal tiene su constante y la cuenta cierra",
             test_todo_nominal_tiene_constante),
            ("periodo_tipo respetado al elegir el coeficiente",
             test_periodo_tipo_respetado)):
        try:
            r = fn()
        except FalloDeTest as e:
            print("  FALLA  %s\n%s" % (nombre, e))
            fallas += 1
            continue
        extra = ""
        if fn is test_serie_mensual_sin_huecos:
            extra = "  (%d meses, %d-%02d a %d-%02d)" % (
                r[0], r[1][0], r[1][1], r[2][0], r[2][1])
        if fn is test_todo_nominal_tiene_constante:
            extra = "  (%d importes recalculados uno por uno)" % r
        print("  OK     %s%s" % (nombre, extra))
    print()

    print("=" * 74)
    print("SERIE REAL DE GASTOS TOTALES (pesos constantes de dic-2025)")
    print("=" * 74)
    serie, saltos = revisar_saltos()
    print("  %-6s %-22s %-10s %s" % ("anio", "constante dic-2025",
                                     "var real", "brecha"))
    for f in serie:
        print("  %-6s %-22s %-10s %s" % (
            f["anio"], f["monto_constante_dic2025"],
            (f["var_real_pct"] + "%") if f["var_real_pct"] else "-",
            (f["brecha_anios"] + " anio(s)") if f["brecha_anios"] else "-"))
    print()
    if saltos:
        print("  %d salto(s) de mas de 40%% real -> data/SALTOS_REALES.csv"
              % len(saltos))
        for s in saltos:
            print("    %s vs %s: %s%% (%s)" % (s["anio"], s["anio_anterior"],
                                               s["var_real_pct"],
                                               s["comparacion"]))
        print("  NO se corrigieron. Van a revision humana.")
    else:
        print("  Ningun anio varia mas de 40% real contra el anterior.")
        print("  data/SALTOS_REALES.csv queda con la cabecera y sin filas.")
    print()

    if fallas:
        print("HAY %d VALIDACION(ES) EN FALLA" % fallas)
        return 1
    print("TEST DEFLACTOR OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
