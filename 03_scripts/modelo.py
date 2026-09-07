#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de flujo de caja del Municipio de San Isidro, 2026-2037.

TODO EN PESOS CONSTANTES DE DICIEMBRE DE 2025.
  No hay supuesto de inflacion y no hace falta: lo que se proyecta son
  cantidades reales. Poner un sendero de inflacion a diez anios en la Argentina
  seria inventar el numero mas fragil del modelo y colgar todo lo demas de el.

EL ANIO 0 ES 2025 Y ES LA EJECUCION REAL, no una estimacion. Sale de la cuenta
Ahorro-Inversion del Estado de Situacion Economico-Financiera 2025, que mide
los ingresos por lo PERCIBIDO y los gastos por lo DEVENGADO. Esa asimetria es
del formato oficial, no una eleccion nuestra, y es la que da el resultado
financiero de -6.051 millones.

Uso:
    python3 03_scripts/modelo.py
"""

import csv
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")

sys.path.insert(0, AQUI)
import parametros_modelo as P

D0 = Decimal(0)
ANIO_BASE = 2025
FIN_MANDATO = 2031          # 2028-2031
FIN_LARGO = 2037            # diez anios desde 2028

# Parte de las transferencias provinciales que se mueve con el coeficiente de
# coparticipacion. El resto son fondos especificos que no dependen de el.
# Calculado en 2025: 82,4%.
SHARE_COPARTICIPABLE = Decimal("0.824")

# Objetivo del programa para empleo + vivienda, como proporcion del gasto
# total. El pedido es entre 2% y 3%; el modelo corre el punto medio y publica
# las dos puntas.
OBJETIVO_MIN = Decimal("0.02")
OBJETIVO_MEDIO = Decimal("0.025")
OBJETIVO_MAX = Decimal("0.03")

# Meta de percepcion del escenario que se financia cobrando mejor. En 2025 la
# percepcion fue 89,32%: subirla a 92% son menos de tres puntos y ya cubre el
# programa entero. No requiere subir ninguna alicuota, solo cobrar lo que ya
# se factura.
PERCEPCION_OBJETIVO = Decimal("92")

# Capitulo 4: las comisiones vecinales manejan el 50% de la obra publica en el
# anio 4. Sobre los bienes de uso devengados de 2025 son 28.908 millones. Es
# REASIGNACION DENTRO de bienes de uso, no gasto nuevo: no cambia ninguna linea
# del flujo de caja, cambia quien decide en que se gasta.
SHARE_OBRA_VECINAL = Decimal("0.50")
ANIOS_RAMPA = 4

# Amortizacion del stock existente. El formulario de deuda publica el
# vencimiento del ejercicio 1 y nada mas, asi que de 2027 en adelante se supone
# que el remanente de deuda consolidada se amortiza en partes iguales en tres
# anios. ES UN SUPUESTO y esta declarado: el stock es el 2,9% del gasto anual,
# asi que mueve poco.
ANIOS_AMORTIZACION_REMANENTE = 3

# Costo real del credito nuevo. EL REPO NO TIENE NINGUN DATO sobre a que tasa
# se financia el Municipio, asi que no se elige una: la opcion de
# endeudamiento se corre con las tres y se muestran las tres.
TASAS_REALES_CREDITO = [Decimal("0"), Decimal("0.05"), Decimal("0.10")]
ANIOS_AMORTIZACION_CREDITO = 5


def _q(x, n=2):
    return Decimal(x).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


# --------------------------------------------------------------------------
# Linea de base: la ejecucion 2025 real
# --------------------------------------------------------------------------

def baseline():
    sef = {(r["bloque"], r["concepto"], r["medida"]): Decimal(r["monto"])
           for r in _leer("data/sef_anual.csv") if r["anio"] == str(ANIO_BASE)}

    def aif(clave):
        return sef[("ahorro_inversion", clave, "oficial")]

    origen = {}
    for (bloque, concepto, medida), v in sef.items():
        if bloque == "recursos_por_origen" and medida == "percibido":
            k = concepto.split("-")[0].strip()
            origen[k] = origen.get(k, D0) + v

    ing_ctes = aif("ingresos_corrientes")
    rec_cap = aif("recursos_de_capital")
    total_rec = ing_ctes + rec_cap

    # El SEF abre el origen del total de recursos, no de los corrientes por
    # separado. Se prorratea con la misma estructura. Los recursos de capital
    # son el 0,67% del total, asi que la eleccion no mueve el resultado.
    bloques = {}
    for k, v in origen.items():
        bloques[k] = _q(v * ing_ctes / total_rec)

    deuda = deuda_inicial()
    perc = P.percepcion(ANIO_BASE)

    b = {
        "anio": ANIO_BASE,
        "ingresos_corrientes": ing_ctes,
        "ing_origen_municipal": bloques.get("ORIGEN MUNICIPAL", D0),
        "ing_origen_provincial": bloques.get("ORIGEN PROVINCIAL", D0),
        "ing_origen_nacional": bloques.get("ORIGEN NACIONAL", D0),
        "ing_otros_origenes": bloques.get("OTROS ORIGENES", D0),
        "recursos_de_capital": rec_cap,
        "gastos_corrientes": aif("gastos_corrientes"),
        "gastos_de_capital": aif("gastos_de_capital"),
        "ahorro_corriente": aif("ahorro_corriente"),
        "ingresos_totales": aif("ingresos_totales"),
        "gastos_totales": aif("gastos_totales"),
        "resultado_financiero": aif("resultado_financiero"),
        "fuentes_financieras": aif("fuentes_financieras"),
        "aplicaciones_financieras": aif("aplicaciones_financieras"),
        "devengado_corriente": perc["devengado"],
        "percepcion_pct": perc["percepcion_pct"],
        "stock_deuda": deuda["stock"],
        "amortizacion_prox_ejercicio": deuda["amortizacion_ej1"],
    }
    # Programas del programa de gobierno.
    prog = {r["concepto"]: Decimal(r["monto"])
            for r in _leer("data/sef_anual.csv")
            if r["anio"] == str(ANIO_BASE) and r["bloque"] == "gastos_por_programa"}
    b["gasto_empleo"] = prog.get("APOYO Y PROMOCION AL EMPLEO", D0)
    b["gasto_vivienda"] = prog.get("INFRAESTRUCTURA HABITACIONAL", D0)

    # Capitulo 4: obra publica manejada por las comisiones vecinales.
    obra = D0
    for r in _leer("data/ejecucion_gastos_objeto.csv"):
        if (int(r["anio"]) == ANIO_BASE and r["periodo_tipo"] == "acumulado_anual"
                and r["objeto_codigo"] == "4" and r["devengado"]):
            obra = Decimal(r["devengado"])
    b["obra_publica_total"] = obra
    b["obra_publica_vecinal_anio4"] = _q(obra * SHARE_OBRA_VECINAL)
    return b


def deuda_inicial():
    stock = D0
    amort = D0
    for r in _leer("data/deuda_stock.csv"):
        if r["anio"] != str(ANIO_BASE) or r["trimestre"] != "IV":
            continue
        if r["codigo"] in ("1", "2"):        # consolidada y flotante
            stock += Decimal(r["saldo"] or 0)
        if r["codigo"] == "1" and r["amortiz_ej1"]:
            amort += Decimal(r["amortiz_ej1"])
    return {"stock": stock, "amortizacion_ej1": amort}


# De donde sale cada linea de la base. No todo viene del mismo lado y decir
# "SEF" en una fila que sale de la ejecucion por objeto seria mentir en la
# columna que existe justamente para que se pueda ir a buscar el numero.
FUENTE_SEF = "SEF 2025 anual, cuenta Ahorro-Inversion"
FUENTE_DEUDA = "formulario Ley 12.462, 2025 IV"
FUENTE_PROGRAMA = "SEF 2025 anual, gastos por programa"
FUENTE_OBJETO = "data/ejecucion_gastos_objeto.csv, 2025 acumulado anual"


def escribir_baseline(b):
    ruta = os.path.join(DATA, "baseline_2025.csv")
    orden = [
        ("ingresos", "ingresos_corrientes", "I. Ingresos corrientes (percibido)"),
        ("ingresos", "ing_origen_municipal", "  de origen municipal"),
        ("ingresos", "ing_origen_provincial", "  de origen provincial"),
        ("ingresos", "ing_origen_nacional", "  de origen nacional"),
        ("ingresos", "ing_otros_origenes", "  de otros origenes"),
        ("ingresos", "recursos_de_capital", "IV. Recursos de capital"),
        ("ingresos", "ingresos_totales", "VI. Ingresos totales"),
        ("gastos", "gastos_corrientes", "II. Gastos corrientes (devengado)"),
        ("gastos", "gastos_de_capital", "V. Gastos de capital (devengado)"),
        ("gastos", "gastos_totales", "VII. Gastos totales"),
        ("resultado", "ahorro_corriente", "III. Ahorro corriente"),
        ("resultado", "resultado_financiero", "VIII. Resultado financiero"),
        ("financiamiento", "fuentes_financieras", "IX. Fuentes financieras"),
        ("financiamiento", "aplicaciones_financieras", "X. Aplicaciones financieras"),
        ("deuda", "stock_deuda", "Stock de deuda al 30/12/2025"),
        ("deuda", "amortizacion_prox_ejercicio", "Amortizacion del ejercicio 1"),
        ("programa", "gasto_empleo", "Apoyo y promocion al empleo"),
        ("programa", "gasto_vivienda", "Infraestructura habitacional"),
        ("programa", "obra_publica_total", "Bienes de uso (obra publica)"),
        ("programa", "obra_publica_vecinal_anio4",
         "  de la cual, a comisiones vecinales en el anio 4 (50%)"),
    ]
    FUENTE_DE = {c: FUENTE_SEF for _, c, _ in orden}
    FUENTE_DE["stock_deuda"] = FUENTE_DEUDA
    FUENTE_DE["amortizacion_prox_ejercicio"] = FUENTE_DEUDA
    FUENTE_DE["gasto_empleo"] = FUENTE_PROGRAMA
    FUENTE_DE["gasto_vivienda"] = FUENTE_PROGRAMA
    FUENTE_DE["obra_publica_total"] = FUENTE_OBJETO
    FUENTE_DE["obra_publica_vecinal_anio4"] = FUENTE_OBJETO + " x 50%"

    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Linea de base del modelo: la EJECUCION REAL de 2025, no una\n")
        f.write("# estimacion. Pesos constantes de diciembre de 2025, que para\n")
        f.write("# el anio base coinciden con los corrientes.\n")
        f.write("# Los ingresos van por lo PERCIBIDO y los gastos por lo\n")
        f.write("# DEVENGADO: es la convencion de la cuenta Ahorro-Inversion.\n")
        w = csv.writer(f)
        w.writerow(["bloque", "clave", "concepto", "monto", "pct_del_gasto_total",
                    "fuente"])
        for bloque, clave, etiqueta in orden:
            v = b[clave]
            w.writerow([bloque, clave, etiqueta, _q(v),
                        _q(100 * v / b["gastos_totales"], 4),
                        FUENTE_DE[clave]])
    return ruta


# --------------------------------------------------------------------------
# La proyeccion
# --------------------------------------------------------------------------
#
# Que crece y que no, y por que:
#
#   recursos de origen municipal   crecen a la tasa real historica. Es lo unico
#                                  que el Municipio maneja.
#   recursos de origen provincial  el 82,4% se mueve con el coeficiente de
#                                  coparticipacion, que viene cayendo; el 17,6%
#                                  restante son fondos especificos y queda
#                                  constante. SUPUESTO DECLARADO: la masa
#                                  provincial a repartir se mantiene constante
#                                  en terminos reales. No hay dato para
#                                  proyectarla y suponer que crece seria
#                                  regalarle al modelo un ingreso que nadie
#                                  garantizo.
#   nacional y otros               constantes en terminos reales. Son el 2,5%.
#   recursos de capital            constantes. Son el 0,67%.
#   gastos                         constantes en terminos reales salvo que el
#                                  escenario diga otra cosa. "Sin cambios de
#                                  politica" es exactamente eso, y ES UN
#                                  SUPUESTO: implica que no hay recomposicion
#                                  salarial real ni ampliacion de servicios.


class Escenario:
    def __init__(self, nombre, g_propios, d_copa, percepcion_objetivo=None,
                 g_gasto_corriente=Decimal("0"), g_gasto_capital=Decimal("0"),
                 objetivo_programa=None, anios_rampa=ANIOS_RAMPA,
                 financiamiento="reasignacion", descripcion=""):
        self.nombre = nombre
        self.g_propios = g_propios
        self.d_copa = d_copa
        self.percepcion_objetivo = percepcion_objetivo
        self.g_gasto_corriente = g_gasto_corriente
        self.g_gasto_capital = g_gasto_capital
        self.objetivo_programa = objetivo_programa
        self.anios_rampa = anios_rampa
        # Como se paga el programa:
        #   reasignacion  sale del gasto flexible. El gasto TOTAL no cambia, y
        #                 por eso el resultado financiero es igual al del base.
        #   percepcion    se paga cobrando mejor. El gasto total SI sube, pero
        #                 los ingresos suben mas, asi que el resultado mejora.
        self.financiamiento = financiamiento
        self.descripcion = descripcion


def _pot(base, tasa, n):
    return base * (1 + tasa) ** n


def proyectar(b, esc, hasta=FIN_LARGO):
    perc_base = b["percepcion_pct"] / 100
    filas = []
    stock = b["stock_deuda"]
    remanente_amortizable = stock - b["amortizacion_prox_ejercicio"]

    for anio in range(ANIO_BASE, hasta + 1):
        n = anio - ANIO_BASE

        if n == 0:
            # El anio 0 es la ejecucion real, sin tocar. Es el ancla del test.
            fila = dict(b)
            fila.update({"escenario": esc.nombre, "anio": anio,
                         "nuevo_endeudamiento": D0,
                         "amortizacion": D0,
                         "gasto_programa_empleo_vivienda":
                             b["gasto_empleo"] + b["gasto_vivienda"],
                         "reasignacion_necesaria": D0,
                         "percepcion_pct": b["percepcion_pct"]})
            filas.append(fila)
            continue

        mun = _pot(b["ing_origen_municipal"], esc.g_propios, n)
        factor_prov = (SHARE_COPARTICIPABLE * (1 + esc.d_copa) ** n
                       + (1 - SHARE_COPARTICIPABLE))
        prov = b["ing_origen_provincial"] * factor_prov
        nac = b["ing_origen_nacional"]
        otros = b["ing_otros_origenes"]
        ing_ctes = mun + prov + nac + otros

        perc = perc_base
        if esc.percepcion_objetivo is not None:
            # La mejora entra gradualmente en la misma cantidad de anios que la
            # rampa del programa: cobrar mejor tampoco es instantaneo.
            paso = min(n, esc.anios_rampa) / Decimal(esc.anios_rampa)
            perc = perc_base + (esc.percepcion_objetivo - perc_base) * paso
        ing_ctes = ing_ctes * perc / perc_base

        rec_cap = b["recursos_de_capital"]
        ing_totales = ing_ctes + rec_cap

        g_ctes = _pot(b["gastos_corrientes"], esc.g_gasto_corriente, n)
        g_cap = _pot(b["gastos_de_capital"], esc.g_gasto_capital, n)

        # El programa: empleo es gasto corriente, vivienda es gasto de capital.
        prog_base = b["gasto_empleo"] + b["gasto_vivienda"]
        prog = prog_base
        reasignacion = D0
        if esc.objetivo_programa is not None:
            paso = Decimal(min(n, esc.anios_rampa)) / Decimal(esc.anios_rampa)
            objetivo = (g_ctes + g_cap) * esc.objetivo_programa
            prog = prog_base + (objetivo - prog_base) * paso
            reasignacion = prog - prog_base
            if esc.financiamiento == "reasignacion":
                # Sale del gasto flexible: el gasto TOTAL no se toca, lo que
                # cambia es su composicion. Por eso este escenario da el mismo
                # resultado financiero que el base.
                pass
            else:
                # Se paga cobrando mejor: el gasto total SUBE. Los ingresos
                # suben mas, por la mejora de percepcion ya aplicada arriba.
                # Empleo es gasto corriente y vivienda es gasto de capital, asi
                # que el incremento se reparte con la misma proporcion que
                # tienen hoy las dos partidas.
                parte_corriente = (b["gasto_empleo"] / prog_base
                                   if prog_base else Decimal("0.5"))
                g_ctes += reasignacion * parte_corriente
                g_cap += reasignacion * (1 - parte_corriente)

        g_totales = g_ctes + g_cap
        resultado = ing_totales - g_totales

        amort = (b["amortizacion_prox_ejercicio"] if n == 1
                 else (remanente_amortizable / ANIOS_AMORTIZACION_REMANENTE
                       if 2 <= n <= 1 + ANIOS_AMORTIZACION_REMANENTE else D0))
        amort = min(amort, stock)
        nuevo = D0
        stock = stock + nuevo - amort

        filas.append({
            "escenario": esc.nombre, "anio": anio,
            "ing_origen_municipal": _q(mun),
            "ing_origen_provincial": _q(prov),
            "ing_origen_nacional": _q(nac),
            "ing_otros_origenes": _q(otros),
            "ingresos_corrientes": _q(ing_ctes),
            "recursos_de_capital": _q(rec_cap),
            "ingresos_totales": _q(ing_totales),
            "gastos_corrientes": _q(g_ctes),
            "gastos_de_capital": _q(g_cap),
            "gastos_totales": _q(g_totales),
            "ahorro_corriente": _q(ing_ctes - g_ctes),
            "resultado_financiero": _q(resultado),
            "stock_deuda": _q(stock),
            "amortizacion": _q(amort),
            "nuevo_endeudamiento": _q(nuevo),
            "percepcion_pct": _q(perc * 100),
            "gasto_programa_empleo_vivienda": _q(prog),
            "reasignacion_necesaria": _q(reasignacion),
        })
    return filas


# --------------------------------------------------------------------------
# Los tres escenarios
# --------------------------------------------------------------------------

def escenarios(par):
    g = par["recursos_propios"] / 100
    d = par["coparticipacion"] / 100
    return [
        Escenario("base", g, d,
                  descripcion="parametros historicos, sin cambios de politica"),
        Escenario("adverso", g - Decimal("0.02"), Decimal("-0.035"),
                  descripcion="recursos propios crecen 2 puntos menos y la "
                              "coparticipacion cae 3,5% anual en vez de 2,2%"),
        Escenario("reformista", g, d, objetivo_programa=OBJETIVO_MEDIO,
                  financiamiento="reasignacion",
                  descripcion="base mas el programa de empleo y vivienda "
                              "llevado al 2,5% del gasto en 4 anios, "
                              "financiado por reasignacion dentro del gasto "
                              "flexible"),
        Escenario("reformista_percepcion", g, d,
                  objetivo_programa=OBJETIVO_MEDIO,
                  percepcion_objetivo=PERCEPCION_OBJETIVO / 100,
                  financiamiento="percepcion",
                  descripcion="el mismo programa, pero pagado cobrando mejor: "
                              "la percepcion de recursos corrientes sube de "
                              "89,32%% a %s%% en 4 anios. No se le saca plata "
                              "a ninguna partida" % PERCEPCION_OBJETIVO),
    ]


# --------------------------------------------------------------------------
# De donde sale la plata: las tres opciones, cuantificadas por separado
# --------------------------------------------------------------------------

def opciones_financiamiento(b, filas_reformista):
    """
    i)   reasignar desde otras partidas
    ii)  cobrar mejor
    iii) endeudarse
    No se elige ninguna: se cuantifican las tres contra el mismo costo.
    """
    costo = {f["anio"]: Decimal(str(f["reasignacion_necesaria"]))
             for f in filas_reformista if f["anio"] > ANIO_BASE}
    costo_regimen = max(costo.values())
    filas = []

    # --- i) reasignacion ---
    # Solo se puede reasignar desde el gasto flexible: personal, deuda y los
    # contratos de servicios no se tocan dentro del ejercicio.
    rig = P.rigidez(ANIO_BASE)
    flexible = rig["flexible"]
    for anio, c in sorted(costo.items()):
        filas.append({
            "opcion": "i_reasignacion", "anio": anio,
            "aporte": _q(c),
            "costo_del_programa": _q(c),
            "cubre_pct": _q(100),
            "detalle": ("sale del gasto flexible del ejercicio, que en %d fue "
                        "%s (%s%% del gasto). El programa en regimen se lleva "
                        "el %s%% de ese margen"
                        % (ANIO_BASE, _q(flexible), rig["flexible_pct"],
                           _q(100 * costo_regimen / flexible))),
            "efecto_en_resultado_financiero": _q(0),
            "supuesto": "el gasto total no cambia; cambia su composicion",
        })

    # --- ii) cobrar mejor ---
    perc = P.percepcion(ANIO_BASE)
    base_pct = perc["percepcion_pct"]
    for objetivo in (Decimal("92"), Decimal("95"), Decimal("97")):
        extra = perc["devengado"] * (objetivo - base_pct) / 100
        for anio, c in sorted(costo.items()):
            n = anio - ANIO_BASE
            paso = Decimal(min(n, ANIOS_RAMPA)) / Decimal(ANIOS_RAMPA)
            aporte = extra * paso
            filas.append({
                "opcion": "ii_percepcion_%s" % objetivo.quantize(Decimal("1")),
                "anio": anio, "aporte": _q(aporte),
                "costo_del_programa": _q(c),
                "cubre_pct": _q(100 * aporte / c) if c else D0,
                "detalle": ("subir la percepcion de %s%% a %s%% sobre los %s "
                            "devengados de 2025 da %s por anio en regimen"
                            % (base_pct, objetivo, _q(perc["devengado"]),
                               _q(extra))),
                "efecto_en_resultado_financiero": _q(aporte),
                "supuesto": "la mejora entra en %d anios, igual que la rampa "
                            "del programa" % ANIOS_RAMPA,
            })

    # --- iii) endeudamiento ---
    # Se toma credito por el costo del programa en regimen y se carga su
    # servicio en los anios siguientes.
    for tasa in TASAS_REALES_CREDITO:
        saldo = D0
        cuotas = []
        for anio in sorted(costo):
            n = anio - ANIO_BASE
            paso = Decimal(min(n, ANIOS_RAMPA)) / Decimal(ANIOS_RAMPA)
            toma = costo_regimen * paso
            interes = saldo * tasa
            amort = sum(c for (a0, c) in cuotas
                        if a0 <= anio < a0 + ANIOS_AMORTIZACION_CREDITO)
            cuotas.append((anio, toma / ANIOS_AMORTIZACION_CREDITO))
            saldo = saldo + toma - amort
            servicio = amort + interes
            filas.append({
                "opcion": "iii_credito_%s" % _q(tasa * 100, 0),
                "anio": anio, "aporte": _q(toma),
                "costo_del_programa": _q(costo[anio]),
                "cubre_pct": _q(100 * toma / costo[anio]) if costo[anio] else D0,
                "detalle": ("saldo de la deuda nueva %s, servicio del anio %s "
                            "(amortizacion %s + intereses %s)"
                            % (_q(saldo), _q(servicio), _q(amort), _q(interes))),
                "efecto_en_resultado_financiero": _q(toma - servicio),
                "supuesto": ("tasa real %s%% anual, amortizacion en %d anios. "
                             "EL REPO NO TIENE DATO del costo del credito del "
                             "Municipio: por eso se corren tres tasas."
                             % (_q(tasa * 100, 0), ANIOS_AMORTIZACION_CREDITO)),
            })

    ruta = os.path.join(DATA, "financiamiento_opciones.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Las tres formas de pagar el programa de empleo y vivienda,\n")
        f.write("# cuantificadas por separado. NO se elige ninguna.\n")
        w = csv.DictWriter(f, fieldnames=[
            "opcion", "anio", "aporte", "costo_del_programa", "cubre_pct",
            "efecto_en_resultado_financiero", "detalle", "supuesto"])
        w.writeheader()
        w.writerows(filas)
    return filas, ruta, costo_regimen, flexible


# --------------------------------------------------------------------------
# Sensibilidad
# --------------------------------------------------------------------------

def sensibilidad(b, par):
    g = par["recursos_propios"] / 100
    d = par["coparticipacion"] / 100
    perc_base = b["percepcion_pct"]
    filas = []

    def correr(dim, etiqueta, esc):
        f = proyectar(b, esc, FIN_LARGO)
        por_anio = {x["anio"]: x for x in f}
        for hito, nombre in ((FIN_MANDATO, "fin del mandato"),
                             (FIN_LARGO, "a diez anios")):
            x = por_anio[hito]
            filas.append({
                "dimension": dim, "variante": etiqueta, "anio": hito,
                "hito": nombre,
                "resultado_financiero": x["resultado_financiero"],
                "ingresos_totales": x["ingresos_totales"],
                "gastos_totales": x["gastos_totales"],
                "ahorro_corriente": x["ahorro_corriente"],
            })

    for delta in (Decimal("-0.01"), D0, Decimal("0.01")):
        correr("recursos_propios",
               "%s%% anual" % _q((g + delta) * 100, 2),
               Escenario("s", g + delta, d))
    for caida in (Decimal("-0.015"), Decimal("-0.025"), Decimal("-0.035")):
        correr("coparticipacion", "%s%% anual" % _q(caida * 100, 1),
               Escenario("s", g, caida))
    for delta in (Decimal("-3"), D0, Decimal("3")):
        correr("percepcion", "%s%%" % _q(perc_base + delta, 2),
               Escenario("s", g, d, percepcion_objetivo=(perc_base + delta) / 100))

    ruta = os.path.join(DATA, "sensibilidad.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Sensibilidad del resultado financiero. Pesos constantes de\n")
        f.write("# diciembre de 2025. Cada dimension se mueve sola, con las\n")
        f.write("# otras dos en su valor del escenario base.\n")
        w = csv.DictWriter(f, fieldnames=[
            "dimension", "variante", "anio", "hito", "resultado_financiero",
            "ingresos_totales", "gastos_totales", "ahorro_corriente"])
        w.writeheader()
        w.writerows(filas)
    return filas, ruta


# --------------------------------------------------------------------------

COLUMNAS = ["escenario", "anio", "ing_origen_municipal", "ing_origen_provincial",
            "ing_origen_nacional", "ing_otros_origenes", "ingresos_corrientes",
            "recursos_de_capital", "ingresos_totales", "gastos_corrientes",
            "gastos_de_capital", "gastos_totales", "ahorro_corriente",
            "resultado_financiero", "stock_deuda", "amortizacion",
            "nuevo_endeudamiento", "percepcion_pct",
            "gasto_programa_empleo_vivienda", "reasignacion_necesaria"]


def main():
    b = baseline()
    ruta_base = escribir_baseline(b)

    rp = P.recursos_propios()
    cop = P.coeficiente_coparticipacion()
    par = {"recursos_propios": rp["tasa_punta_a_punta"],
           "coparticipacion": cop["caida_anual_pct"]}

    todas = []
    por_escenario = {}
    for esc in escenarios(par):
        f = proyectar(b, esc, FIN_LARGO)
        por_escenario[esc.nombre] = f
        todas += f

    ruta = os.path.join(DATA, "modelo_flujo_caja.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Modelo de flujo de caja del Municipio de San Isidro.\n")
        f.write("# PESOS CONSTANTES DE DICIEMBRE DE 2025, sin supuesto de\n")
        f.write("# inflacion. El anio 2025 es la EJECUCION REAL, no una\n")
        f.write("# proyeccion. Ver data/METODOLOGIA_MODELO.md.\n")
        f.write("#\n")
        f.write("# NO ES UN ERROR DE COPIADO: el escenario reformista tiene el\n")
        f.write("# MISMO resultado financiero que el base, porque se financia\n")
        f.write("# integramente por reasignacion dentro del gasto flexible. El\n")
        f.write("# gasto TOTAL no cambia, cambia su composicion. Difiere del base\n")
        f.write("# solo en las columnas gasto_programa_empleo_vivienda y\n")
        f.write("# reasignacion_necesaria.\n")
        f.write("#\n")
        f.write("# El escenario reformista_percepcion es el MISMO programa pagado\n")
        f.write("# cobrando mejor (percepcion de 89,32%% a 92%% en 4 anios). Ese SI\n")
        f.write("# mueve el resultado financiero, y hacia arriba.\n")
        w = csv.DictWriter(f, fieldnames=COLUMNAS, extrasaction="ignore")
        w.writeheader()
        for x in todas:
            w.writerow({k: (_q(x[k]) if isinstance(x.get(k), Decimal) else x.get(k, ""))
                        for k in COLUMNAS})

    opciones, ruta_op, costo_reg, flexible = opciones_financiamiento(
        b, por_escenario["reformista"])
    sens, ruta_sens = sensibilidad(b, par)
    return {"baseline": b, "par": par, "por_escenario": por_escenario,
            "opciones": opciones, "costo_regimen": costo_reg,
            "flexible": flexible, "sensibilidad": sens,
            "rutas": [ruta_base, ruta, ruta_op, ruta_sens]}


if __name__ == "__main__":
    r = main()
    b = r["baseline"]
    print("=" * 90)
    print("MODELO DE FLUJO DE CAJA - pesos constantes de diciembre de 2025")
    print("parametros: recursos propios %s%% anual | coparticipacion %s%% anual"
          % (r["par"]["recursos_propios"], r["par"]["coparticipacion"]))
    print("=" * 90)
    for nombre, filas in r["por_escenario"].items():
        print("\n--- %s ---" % nombre.upper())
        print("  %-6s %16s %16s %16s %14s" % ("anio", "ing.totales",
                                              "gastos totales", "resultado",
                                              "ahorro cte"))
        for x in filas:
            if x["anio"] in (2025, 2028, 2031, 2034, 2037):
                print("  %-6s %16s %16s %16s %14s"
                      % (x["anio"], _q(x["ingresos_totales"], 0),
                         _q(x["gastos_totales"], 0),
                         _q(x["resultado_financiero"], 0),
                         _q(x["ahorro_corriente"], 0)))
    print()
    print("=" * 90)
    print("EL PROGRAMA: empleo + vivienda al %s%% del gasto en %d anios"
          % (_q(OBJETIVO_MEDIO * 100, 1), ANIOS_RAMPA))
    print("=" * 90)
    print("  hoy (2025)        : %s  (%s%% del gasto)"
          % (_q(b["gasto_empleo"] + b["gasto_vivienda"]),
             _q(100 * (b["gasto_empleo"] + b["gasto_vivienda"])
                / b["gastos_totales"], 3)))
    print("  costo en regimen  : %s por anio" % _q(r["costo_regimen"]))
    print("  gasto flexible    : %s  ->  el programa se lleva el %s%%"
          % (_q(r["flexible"]), _q(100 * r["costo_regimen"] / r["flexible"], 1)))
    print()
    for x in r["rutas"]:
        print("  -> %s" % os.path.relpath(x, REPO))
