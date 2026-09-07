#!/usr/bin/env python3
"""
Los parametros del modelo de flujo de caja, calculados desde los datos.

Ninguno se inventa. Cada uno sale de una serie del repo, se publica con su
desvio y queda escrito de donde salio en data/parametros_modelo.csv y en
data/METODOLOGIA_MODELO.md.

  a) crecimiento real de los recursos propios
  b) caida del coeficiente de coparticipacion
  c) rigidez del gasto

TODO EN PESOS CONSTANTES DE DICIEMBRE DE 2025. El modelo no lleva supuesto de
inflacion: a diez anios en la Argentina no es defendible, y ademas no hace
falta, porque lo que se proyecta son cantidades reales.
"""

import csv
import glob
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")
RAW_PBA = os.path.join(REPO, "01_raw", "transferencias_pba")

D0 = Decimal(0)
MESES = {"ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5,
         "JUNIO": 6, "JULIO": 7, "AGOSTO": 8, "SEPTIEMBRE": 9,
         "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12}

# La fila del XLSX de la Provincia que trae el total de los 135 municipios. NO
# es un municipio: si se la suma como si lo fuera, el total sale al doble y la
# participacion a la mitad.
FILA_CONSOLIDADO = "CONSOLIDADO"


class ErrorDeParametros(Exception):
    pass


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def _q(x, n=4):
    return Decimal(x).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)


def coeficientes_anuales():
    """coef_anual del deflactor, por anio."""
    return {int(r["anio"]): Decimal(r["coef_anual"])
            for r in _leer("data/deflactor.csv") if r["coef_anual"]}


# --------------------------------------------------------------------------
# a) Crecimiento real de los recursos propios
# --------------------------------------------------------------------------
#
# "Recursos propios" = recursos de ORIGEN MUNICIPAL. No se puede usar la
# apertura por rubro como sustituto: la coparticipacion provincial esta
# adentro de "ingresos no tributarios", asi que sumar tributarios + no
# tributarios contaria como propio lo que manda la Provincia. En 2025 eso
# serian 291.319 millones en vez de 207.969: un 40% de mas.

def recursos_propios():
    coef = coeficientes_anuales()
    puntos = {}

    # Rendicion 2010, apertura por origen.
    for r in _leer("data/rendiciones_2010_2021.csv"):
        if r["concepto"] == "recursos_por_origen" and r["subconcepto"] == "municipal":
            puntos[int(r["anio"])] = {
                "nominal": Decimal(r["monto"]),
                "constante": Decimal(r["monto_constante_dic2025"]),
                "fuente": r["fuente"], "dataset": "data/rendiciones_2010_2021.csv"}

    # Rendiciones y fallos del HTC 2014-2022.
    for r in _leer("SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv"):
        if r["bloque"] == "recursos_origen" and r["concepto"] == "Origen municipal":
            puntos[int(r["anio"])] = {
                "nominal": Decimal(r["monto_pesos"]),
                "constante": Decimal(r["monto_constante_dic2025"]),
                "fuente": r["fuente"],
                "dataset": "SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv"}

    # SEF 2024 y 2025: municipal de libre disponibilidad + afectados, percibido.
    sef = {}
    for r in _leer("data/sef_anual.csv"):
        if (r["bloque"] == "recursos_por_origen" and r["medida"] == "percibido"
                and r["concepto"].startswith("ORIGEN MUNICIPAL")):
            sef[int(r["anio"])] = sef.get(int(r["anio"]), D0) + Decimal(r["monto"])
    for anio, nominal in sef.items():
        puntos[anio] = {
            "nominal": nominal,
            "constante": (nominal * coef[anio]).quantize(Decimal("0.01"),
                                                         rounding=ROUND_HALF_UP),
            "fuente": "SEF anual", "dataset": "data/sef_anual.csv"}

    anios = sorted(puntos)
    # Tasa anual compuesta entre puntos consecutivos, anotando la brecha.
    tramos = []
    for a, b in zip(anios, anios[1:]):
        n = b - a
        base = puntos[a]["constante"]
        if base <= 0:
            continue
        tasa = (float(puntos[b]["constante"] / base) ** (1.0 / n) - 1) * 100
        tramos.append({"desde": a, "hasta": b, "anios": n,
                       "tasa_anual_pct": _q(tasa, 2)})
    # Tasa de punta a punta, que es la que va al modelo.
    n = anios[-1] - anios[0]
    punta = (float(puntos[anios[-1]]["constante"] / puntos[anios[0]]["constante"])
             ** (1.0 / n) - 1) * 100
    tasas = [float(t["tasa_anual_pct"]) for t in tramos]
    media = sum(tasas) / len(tasas)
    desvio = (sum((x - media) ** 2 for x in tasas) / (len(tasas) - 1)) ** 0.5
    return {"puntos": puntos, "anios": anios, "tramos": tramos,
            "tasa_punta_a_punta": _q(punta, 2),
            "media_de_tramos": _q(media, 2), "desvio_de_tramos": _q(desvio, 2)}


# --------------------------------------------------------------------------
# b) Caida del coeficiente de coparticipacion
# --------------------------------------------------------------------------

def coeficiente_coparticipacion():
    """
    Participacion de San Isidro en el total transferido por la Provincia a los
    135 municipios, anio por anio, desde los XLSX crudos.
    """
    import openpyxl

    def lim(t):
        return re.sub(r"\s+", " ", str(t)).strip()

    por_anio = {}
    for ruta in sorted(glob.glob(os.path.join(RAW_PBA, "*Transferencias*.xlsx"))):
        if "Ac. x Municipio" in os.path.basename(ruta):
            continue
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        for hoja in wb.sheetnames:
            if hoja.strip().upper() not in MESES:
                continue
            filas = list(wb[hoja].iter_rows(values_only=True))
            anio = None
            for f in filas[:10]:
                for c in f:
                    if c and "MES DE" in lim(c).upper():
                        m = re.search(r"(\d{4})", lim(c))
                        anio = int(m.group(1)) if m else None
                if anio:
                    break
            ic = jm = None
            for i, f in enumerate(filas):
                for j, c in enumerate(f):
                    if c and lim(c).lower() == "municipio":
                        ic, jm = i + 1, j
                        break
                if ic:
                    break
            if ic is None or anio is None:
                continue
            jtot = None
            for j, c in enumerate(filas[ic]):
                if c and lim(c).lower().startswith("total"):
                    jtot = j
            if jtot is None:
                continue
            si = cons = None
            for f in filas[ic + 1:]:
                if (len(f) <= jm or f[jm] is None or jtot >= len(f)
                        or f[jtot] is None):
                    continue
                nombre = lim(f[jm]).upper()
                try:
                    x = Decimal(str(f[jtot]))
                except Exception:
                    continue
                if nombre == "SAN ISIDRO":
                    si = x
                elif nombre.startswith(FILA_CONSOLIDADO):
                    cons = x
            if si is None or not cons:
                continue
            d = por_anio.setdefault(anio, {"san_isidro": D0, "provincia": D0,
                                           "meses": 0})
            d["san_isidro"] += si
            d["provincia"] += cons
            d["meses"] += 1
        wb.close()

    for anio, d in por_anio.items():
        d["participacion_pct"] = _q(100 * d["san_isidro"] / d["provincia"], 4)

    completos = sorted(a for a, d in por_anio.items() if d["meses"] == 12)
    a0, a1 = completos[0], completos[-1]
    n = a1 - a0
    caida = (float(por_anio[a1]["participacion_pct"]
                   / por_anio[a0]["participacion_pct"]) ** (1.0 / n) - 1) * 100
    return {"por_anio": por_anio, "anios_completos": completos,
            "desde": a0, "hasta": a1,
            "caida_anual_pct": _q(caida, 3)}


# --------------------------------------------------------------------------
# c) Rigidez del gasto
# --------------------------------------------------------------------------
#
# Tres niveles, porque "rigido" no es una sola cosa:
#   nucleo      personal y servicio de la deuda. No se toca dentro del anio sin
#               romper un contrato de trabajo o un contrato de credito.
#   contratos   + servicios no personales. Son contratos plurianuales de
#               servicios; se renegocian, pero no en el ejercicio en curso.
#   flexible    el resto: bienes de consumo, bienes de uso, transferencias y
#               activos financieros. Es lo unico reasignable en el corto plazo.

RIGIDO_NUCLEO = {"1", "7"}
RIGIDO_CONTRATOS = {"3"}


def rigidez(anio=2025):
    g = {}
    for r in _leer("data/ejecucion_gastos_objeto.csv"):
        if (int(r["anio"]) == anio and r["periodo_tipo"] == "acumulado_anual"
                and r["devengado"]):
            g[r["objeto_codigo"]] = {"nombre": r["objeto"],
                                     "monto": Decimal(r["devengado"])}
    if not g:
        raise ErrorDeParametros("no hay ejecucion anual por objeto de %d" % anio)
    total = sum(v["monto"] for v in g.values())
    nucleo = sum(v["monto"] for k, v in g.items() if k in RIGIDO_NUCLEO)
    contratos = sum(v["monto"] for k, v in g.items() if k in RIGIDO_CONTRATOS)
    flexible = total - nucleo - contratos
    return {"anio": anio, "objetos": g, "total": total,
            "nucleo": nucleo, "contratos": contratos, "flexible": flexible,
            "nucleo_pct": _q(100 * nucleo / total, 2),
            "con_contratos_pct": _q(100 * (nucleo + contratos) / total, 2),
            "flexible_pct": _q(100 * flexible / total, 2)}


# --------------------------------------------------------------------------
# d) Percepcion de recursos corrientes
# --------------------------------------------------------------------------
#
# Lo devengado es lo que el Municipio tiene derecho a cobrar; lo percibido es
# lo que entro. La diferencia es mora y es una palanca de financiamiento sin
# subir una sola tasa.

def percepcion(anio=2025):
    dev = per = D0
    for r in _leer("data/ejecucion_recursos.csv"):
        if int(r["anio"]) != anio or r["periodo_tipo"] != "acumulado_anual":
            continue
        if not r["rubro_codigo"].startswith("1."):     # solo corrientes
            continue
        if r["devengado"]:
            dev += Decimal(r["devengado"])
        if r["percibido"]:
            per += Decimal(r["percibido"])
    if not dev:
        raise ErrorDeParametros("no hay recursos corrientes de %d" % anio)
    return {"anio": anio, "devengado": dev, "percibido": per,
            "sin_cobrar": dev - per,
            "percepcion_pct": _q(100 * per / dev, 2)}


# --------------------------------------------------------------------------

def escribir(rp, cop, rig, perc):
    ruta = os.path.join(DATA, "parametros_modelo.csv")
    filas = []

    def add(clave, valor, unidad, de_donde, nota=""):
        filas.append({"parametro": clave, "valor": valor, "unidad": unidad,
                      "calculado_desde": de_donde, "nota": nota})

    add("recursos_propios_tasa_real_anual", rp["tasa_punta_a_punta"], "% anual",
        "recursos de origen municipal en pesos constantes, %d a %d (%d puntos)"
        % (rp["anios"][0], rp["anios"][-1], len(rp["anios"])),
        "punta a punta; la media de los tramos da %s con desvio %s"
        % (rp["media_de_tramos"], rp["desvio_de_tramos"]))
    add("recursos_propios_desvio_tramos", rp["desvio_de_tramos"], "puntos",
        "desvio estandar de las tasas de los %d tramos" % len(rp["tramos"]), "")
    add("coparticipacion_caida_anual", cop["caida_anual_pct"], "% anual",
        "participacion de San Isidro en el total transferido a los 135 "
        "municipios, %d a %d" % (cop["desde"], cop["hasta"]),
        "de %s%% a %s%%"
        % (cop["por_anio"][cop["desde"]]["participacion_pct"],
           cop["por_anio"][cop["hasta"]]["participacion_pct"]))
    add("rigidez_nucleo", rig["nucleo_pct"], "% del gasto",
        "personal + servicio de la deuda, devengado %d" % rig["anio"], "")
    add("rigidez_con_contratos", rig["con_contratos_pct"], "% del gasto",
        "nucleo + servicios no personales, devengado %d" % rig["anio"], "")
    add("gasto_flexible", rig["flexible_pct"], "% del gasto",
        "bienes de consumo + bienes de uso + transferencias + activos "
        "financieros, devengado %d" % rig["anio"],
        "es el unico margen reasignable dentro del ejercicio")
    add("percepcion_recursos_corrientes", perc["percepcion_pct"], "%",
        "percibido sobre devengado de recursos corrientes, %d" % perc["anio"],
        "quedaron sin cobrar %s" % perc["sin_cobrar"].quantize(Decimal("1")))

    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["parametro", "valor", "unidad",
                                          "calculado_desde", "nota"])
        w.writeheader()
        w.writerows(filas)

    # La serie de recursos propios, aparte, para que se pueda auditar.
    ruta2 = os.path.join(DATA, "recursos_propios_serie.csv")
    with open(ruta2, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "monto_nominal", "monto_constante_dic2025",
                    "var_real_anual_pct", "brecha_anios", "dataset", "fuente"])
        prev = None
        for a in rp["anios"]:
            p = rp["puntos"][a]
            var = brecha = ""
            if prev is not None:
                n = a - prev
                var = _q((float(p["constante"] / rp["puntos"][prev]["constante"])
                          ** (1.0 / n) - 1) * 100, 2)
                brecha = n
            w.writerow([a, p["nominal"], p["constante"], var, brecha,
                        p["dataset"], p["fuente"]])
            prev = a

    # La serie del coeficiente de coparticipacion.
    ruta3 = os.path.join(DATA, "coparticipacion_serie.csv")
    with open(ruta3, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "meses", "san_isidro", "total_135_municipios",
                    "participacion_pct", "var_anual_pct", "fuente"])
        prev = None
        for a in sorted(cop["por_anio"]):
            d = cop["por_anio"][a]
            var = ""
            if prev is not None:
                var = _q(100 * (d["participacion_pct"] / prev - 1), 2)
            w.writerow([a, d["meses"], d["san_isidro"].quantize(Decimal("1")),
                        d["provincia"].quantize(Decimal("1")),
                        d["participacion_pct"], var,
                        "01_raw/transferencias_pba/*Transferencias*.xlsx"])
            prev = d["participacion_pct"]
    return [ruta, ruta2, ruta3]


def main():
    rp = recursos_propios()
    cop = coeficiente_coparticipacion()
    rig = rigidez()
    perc = percepcion()
    rutas = escribir(rp, cop, rig, perc)
    return rp, cop, rig, perc, rutas


if __name__ == "__main__":
    rp, cop, rig, perc, rutas = main()
    print("=" * 78)
    print("a) RECURSOS PROPIOS (origen municipal), pesos constantes dic-2025")
    print("=" * 78)
    for a in rp["anios"]:
        print("  %d  %20s" % (a, rp["puntos"][a]["constante"]))
    print("  tasa punta a punta %d-%d : %s%% anual"
          % (rp["anios"][0], rp["anios"][-1], rp["tasa_punta_a_punta"]))
    print("  media de los %d tramos    : %s%% anual, desvio %s puntos"
          % (len(rp["tramos"]), rp["media_de_tramos"], rp["desvio_de_tramos"]))
    print()
    print("=" * 78)
    print("b) COPARTICIPACION: participacion de San Isidro")
    print("=" * 78)
    for a in sorted(cop["por_anio"]):
        d = cop["por_anio"][a]
        print("  %d  %s%%  (%d meses)" % (a, d["participacion_pct"], d["meses"]))
    print("  caida compuesta %d-%d: %s%% anual"
          % (cop["desde"], cop["hasta"], cop["caida_anual_pct"]))
    print()
    print("=" * 78)
    print("c) RIGIDEZ DEL GASTO (devengado %d)" % rig["anio"])
    print("=" * 78)
    print("  nucleo (personal + deuda)          : %s%%" % rig["nucleo_pct"])
    print("  + contratos (servicios no personales): %s%%" % rig["con_contratos_pct"])
    print("  flexible en el corto plazo         : %s%%" % rig["flexible_pct"])
    print()
    print("=" * 78)
    print("d) PERCEPCION DE RECURSOS CORRIENTES (%d)" % perc["anio"])
    print("=" * 78)
    print("  devengado  %s" % perc["devengado"])
    print("  percibido  %s" % perc["percibido"])
    print("  sin cobrar %s  ->  percepcion %s%%"
          % (perc["sin_cobrar"], perc["percepcion_pct"]))
    print()
    for r in rutas:
        print("  -> %s" % os.path.relpath(r, REPO))
