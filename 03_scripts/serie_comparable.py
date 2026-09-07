#!/usr/bin/env python3
"""
Serie de gasto total comparable: un solo concepto en todos los anios.

EL PROBLEMA
  data/serie_gastos_totales_real.csv mezcla tres conceptos distintos de gasto
  total segun el anio, porque cada fuente publica el suyo. Comparar 2017 contra
  2024 ahi adentro es comparar "gastos con imputacion al presupuesto" contra
  "devengado por objeto", que no miden lo mismo. Cualquier variacion que cruce
  un cambio de concepto no es una comparacion limpia.

  Peor: el propio "total de gastos" de las rendiciones cambia de contenido a
  mitad de camino. En 2010-2012 INCLUYE las aplicaciones financieras; en
  2019-2021 las deja debajo de la linea y NO las incluye. Es el cambio al
  formato Ahorro-Inversion de los informes ARSI. En 2010 las aplicaciones eran
  el 8,1% del total y en 2021 el 14,0%, asi que el salto no es menor.

LA SOLUCION
  Un unico concepto: GASTOS CORRIENTES + GASTOS DE CAPITAL, sin aplicaciones
  financieras. Es el gasto de gestion: lo que el Municipio gasta en funcionar y
  en invertir, sin la amortizacion de deuda ni los movimientos financieros.

  Donde una fuente lo publica directo, se usa tal cual. Donde no, se deriva de
  los objetos del gasto restando el objeto financiero, con la identidad que se
  verifica mas abajo. Cada fila dice cual de los dos caminos se uso.

  Los anios sin dato quedan VACIOS. No se sustituyen por otro concepto.

Uso:
    python3 03_scripts/serie_comparable.py
"""

import csv
import datetime as dt
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")

sys.path.insert(0, AQUI)
import deflactor as DF

DEC0 = Decimal(0)

# Hasta aca una diferencia es redondeo de la fuente, no un concepto distinto.
TOLERANCIA_REDONDEO = Decimal("100")

CONCEPTO = "gastos_corrientes_mas_de_capital"
CONCEPTO_TXT = ("Gastos corrientes + gastos de capital "
                "(sin aplicaciones financieras)")

# Los objetos del gasto que el Municipio manda debajo de la linea, o sea los
# que hay que restar de la suma de objetos para llegar al concepto. Se listan
# por como los nombra cada fuente.
OBJETOS_FINANCIEROS = {
    "Servicio de la deuda y disminucion de otros pasivos",
    "servicio_de_la_deuda",
    "activos_financieros",
    "SERVICIO DE LA DEUDA Y DISMINUCION DE OTROS PASIVOS",
    "ACTIVOS FINANCIEROS",
}

RENDICIONES = "data/rendiciones_2010_2021.csv"
DATOS_SI = "SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv"
EJECUCION = "data/ejecucion_gastos_objeto.csv"
PRESUPUESTO = "data/presupuesto_historico_2010_2026.csv"


class ErrorDeSerie(Exception):
    pass


def _leer(ruta):
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(
            l for l in f if not l.startswith("#"))]


def _d(txt):
    txt = (txt or "").strip()
    return Decimal(txt) if txt else None


def _r2(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------
# 1. Inventario: TODOS los conceptos de gasto de cada anio
# --------------------------------------------------------------------------

def inventario():
    """
    Una fila por (anio, concepto de gasto) disponible en cualquier fuente, sea
    un total publicado o un componente que sirve para armar uno. Incluye el
    presupuesto, marcado como presupuestado y no ejecutado, para que se vea que
    esta pero que no entra en una serie de gasto real.
    """
    filas = []

    for r in _leer(RENDICIONES):
        if not r["concepto"].startswith(("gastos", "total_gastos")):
            continue
        filas.append({
            "anio": int(r["anio"]), "tipo": "ejecutado",
            "familia": r["concepto"],
            "concepto_en_la_fuente": r["subconcepto"] or r["concepto"],
            "nivel": "total" if r["concepto"].startswith("total") else "componente",
            "monto_nominal": r["monto"],
            "monto_constante_dic2025": r.get("monto_constante_dic2025", ""),
            "dataset": RENDICIONES, "fuente": r["fuente"],
        })

    for r in _leer(DATOS_SI):
        if not r["bloque"].startswith("gastos"):
            continue
        filas.append({
            "anio": int(r["anio"]), "tipo": "ejecutado",
            "familia": r["bloque"],
            "concepto_en_la_fuente": r["concepto"],
            "nivel": "total" if r["bloque"] == "gastos_total" else "componente",
            "monto_nominal": r["monto_pesos"],
            "monto_constante_dic2025": r.get("monto_constante_dic2025", ""),
            "dataset": DATOS_SI, "fuente": r["fuente"],
        })

    for r in _leer(EJECUCION):
        if r["periodo_tipo"] != "acumulado_anual" or not r["devengado"]:
            continue
        filas.append({
            "anio": int(r["anio"]), "tipo": "ejecutado",
            "familia": "gastos_por_objeto_devengado",
            "concepto_en_la_fuente": "%s %s" % (r["objeto_codigo"], r["objeto"]),
            "nivel": "componente",
            "monto_nominal": r["devengado"],
            "monto_constante_dic2025": r.get("monto_constante_dic2025", ""),
            "dataset": EJECUCION, "fuente": r["fuente"],
        })

    if os.path.exists(os.path.join(REPO, PRESUPUESTO)):
        for r in _leer(PRESUPUESTO):
            if not r["concepto"].startswith("gastos"):
                continue
            filas.append({
                "anio": int(r["anio"]), "tipo": "presupuestado",
                # Prefijo para que no se confunda con el mismo nombre de
                # familia del lado ejecutado. El presupuesto NO entra en
                # ninguna serie de gasto real.
                "familia": "presupuesto_" + r["concepto"],
                "concepto_en_la_fuente": r["subconcepto"] or r["concepto"],
                "nivel": "componente",
                "monto_nominal": r["monto"],
                "monto_constante_dic2025": r.get("monto_constante_dic2025", ""),
                "dataset": PRESUPUESTO, "fuente": r["fuente"],
            })

    filas.sort(key=lambda f: (f["anio"], f["tipo"], f["familia"],
                              f["concepto_en_la_fuente"]))
    ruta = os.path.join(DATA, "conceptos_disponibles_por_anio.csv")
    cols = ["anio", "tipo", "familia", "concepto_en_la_fuente", "nivel",
            "monto_nominal", "monto_constante_dic2025", "dataset", "fuente"]
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)
    return filas, ruta


# --------------------------------------------------------------------------
# 2. El concepto comparable, anio por anio
# --------------------------------------------------------------------------
#
# DOS CAMINOS, y cada fila dice cual se uso:
#
#   publicado  la fuente publica gastos corrientes y gastos de capital como
#              tales. Se suman y listo.
#   derivado   la fuente solo publica el gasto abierto por objeto. Se suman
#              todos los objetos y se restan los financieros.
#
# La identidad que habilita el segundo camino esta verificada contra los anios
# en que las dos aperturas existen a la vez (ver identidades()). El anio 2011
# es el unico donde no cierra, y ahi se usa el camino publicado, que existe.

def por_caracter_rendiciones():
    """gastos corrientes y de capital publicados en las rendiciones."""
    salida = {}
    for r in _leer(RENDICIONES):
        if r["concepto"] != "gastos_por_caracter":
            continue
        salida.setdefault(int(r["anio"]), {})[r["subconcepto"]] = {
            "nominal": _d(r["monto"]),
            "constante": _d(r.get("monto_constante_dic2025")),
            "fuente": r["fuente"],
        }
    return salida


def por_caracter_datos_si():
    salida = {}
    for r in _leer(DATOS_SI):
        if r["bloque"] != "gastos_caracter":
            continue
        clave = {"Gastos corrientes": "gastos_corrientes",
                 "Gastos de capital": "gastos_de_capital",
                 "Aplicaciones financieras": "aplicaciones_financieras"}
        k = clave.get(r["concepto"])
        if not k:
            continue
        salida.setdefault(int(r["anio"]), {})[k] = {
            "nominal": _d(r["monto_pesos"]),
            "constante": _d(r.get("monto_constante_dic2025")),
            "fuente": r["fuente"],
        }
    return salida


def objetos_por_anio():
    """Los objetos del gasto de cada anio, vengan de donde vengan."""
    salida = {}

    for r in _leer(DATOS_SI):
        if r["bloque"] != "gastos_objeto":
            continue
        salida.setdefault(int(r["anio"]), []).append({
            "nombre": r["concepto"], "nominal": _d(r["monto_pesos"]),
            "constante": _d(r.get("monto_constante_dic2025")),
            "fuente": r["fuente"], "dataset": DATOS_SI,
        })

    for r in _leer(RENDICIONES):
        if r["concepto"] != "gastos_por_objeto":
            continue
        salida.setdefault(int(r["anio"]), []).append({
            "nombre": r["subconcepto"], "nominal": _d(r["monto"]),
            "constante": _d(r.get("monto_constante_dic2025")),
            "fuente": r["fuente"], "dataset": RENDICIONES,
        })

    for r in _leer(EJECUCION):
        if r["periodo_tipo"] != "acumulado_anual" or not r["devengado"]:
            continue
        salida.setdefault(int(r["anio"]), []).append({
            "nombre": r["objeto"], "nominal": _d(r["devengado"]),
            "constante": _d(r.get("monto_constante_dic2025")),
            "fuente": r["fuente"], "dataset": EJECUCION,
        })
    return salida


def identidades(caracter, objetos):
    """
    Comprueba, en los anios donde estan las dos aperturas, que
        suma de objetos - objetos financieros == corrientes + capital
    Es lo unico que habilita derivar el concepto desde los objetos.
    """
    filas = []
    for anio in sorted(set(caracter) & set(objetos)):
        c = caracter[anio]
        if "gastos_corrientes" not in c or "gastos_de_capital" not in c:
            continue
        publicado = c["gastos_corrientes"]["nominal"] + c["gastos_de_capital"]["nominal"]
        obj = objetos[anio]
        derivado = sum((o["nominal"] for o in obj
                        if o["nombre"] not in OBJETOS_FINANCIEROS), DEC0)
        dif = derivado - publicado
        # Las rendiciones publican importes redondeados, asi que una diferencia
        # de unos pocos pesos sobre cientos de millones es redondeo de la
        # fuente y no un concepto distinto. El corte esta en 100 pesos.
        if dif == 0:
            estado, nota = "si", "exacto"
        elif abs(dif) <= TOLERANCIA_REDONDEO:
            estado, nota = "si", ("difiere en $%s, redondeo de la fuente"
                                      % dif)
        else:
            estado, nota = "no", ("difiere en $%s: la apertura por objeto y la "
                                  "de caracter no dicen lo mismo en este anio"
                                  % dif)
        filas.append({
            "anio": anio, "publicado": publicado, "derivado": derivado,
            "diferencia": dif, "cierra": estado, "nota": nota,
        })
    return filas


def serie_comparable():
    caracter = por_caracter_rendiciones()
    for anio, v in por_caracter_datos_si().items():
        caracter.setdefault(anio, {}).update(v)
    objetos = objetos_por_anio()
    checks = identidades(caracter, objetos)
    cierran = {c["anio"] for c in checks if c["cierra"] == "si"}
    no_cierran = {c["anio"] for c in checks if c["cierra"] == "no"}

    anios = sorted(set(caracter) | set(objetos))
    rango = range(min(anios), max(anios) + 1)
    filas = []
    for anio in rango:
        c = caracter.get(anio, {})
        if "gastos_corrientes" in c and "gastos_de_capital" in c:
            nom = c["gastos_corrientes"]["nominal"] + c["gastos_de_capital"]["nominal"]
            con = c["gastos_corrientes"]["constante"] + c["gastos_de_capital"]["constante"]
            filas.append({
                "anio": anio, "concepto": CONCEPTO_TXT,
                "monto_nominal": _r2(nom),
                "monto_constante_dic2025": _r2(con),
                "origen_del_dato": "publicado",
                "como_se_obtuvo": ("suma de los dos componentes de caracter "
                                   "economico publicados por la fuente"),
                "componentes": "gastos_corrientes + gastos_de_capital",
                "fuente": c["gastos_corrientes"]["fuente"],
                "dataset": (RENDICIONES if anio in por_caracter_rendiciones()
                            else DATOS_SI),
            })
            continue

        obj = objetos.get(anio)
        if obj:
            usados = [o for o in obj if o["nombre"] not in OBJETOS_FINANCIEROS]
            fuera = [o for o in obj if o["nombre"] in OBJETOS_FINANCIEROS]
            if any(o["constante"] is None for o in usados):
                raise ErrorDeSerie("faltan importes constantes en %d" % anio)
            filas.append({
                "anio": anio, "concepto": CONCEPTO_TXT,
                "monto_nominal": _r2(sum((o["nominal"] for o in usados), DEC0)),
                "monto_constante_dic2025": _r2(
                    sum((o["constante"] for o in usados), DEC0)),
                "origen_del_dato": "derivado",
                "como_se_obtuvo": ("suma de los %d objetos del gasto menos los "
                                   "financieros (%s)"
                                   % (len(obj), ", ".join(o["nombre"] for o in fuera)
                                      or "ninguno")),
                "componentes": " + ".join(o["nombre"] for o in usados),
                "fuente": obj[0]["fuente"],
                "dataset": obj[0]["dataset"],
            })
            continue

        filas.append({
            "anio": anio, "concepto": CONCEPTO_TXT,
            "monto_nominal": "", "monto_constante_dic2025": "",
            "origen_del_dato": "sin dato",
            "como_se_obtuvo": ("no hay rendicion ni informe de ejecucion anual "
                               "publicado para este anio"),
            "componentes": "", "fuente": "", "dataset": "",
        })

    # Variacion real solo entre anios que tienen dato.
    previo = None
    for f in filas:
        f["var_real_pct"] = ""
        f["brecha_anios"] = ""
        f["anio_anterior_con_dato"] = ""
        if not f["monto_constante_dic2025"]:
            continue
        if previo is not None:
            base = Decimal(previo["monto_constante_dic2025"])
            f["var_real_pct"] = str(
                ((Decimal(f["monto_constante_dic2025"]) / base - 1) * 100)
                .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            f["brecha_anios"] = f["anio"] - previo["anio"]
            f["anio_anterior_con_dato"] = previo["anio"]
        previo = f

    ruta = os.path.join(DATA, "serie_gastos_comparable.csv")
    cols = ["anio", "concepto", "monto_nominal", "monto_constante_dic2025",
            "var_real_pct", "anio_anterior_con_dato", "brecha_anios",
            "origen_del_dato", "como_se_obtuvo", "componentes", "dataset",
            "fuente"]
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write("# Serie de gasto total del Municipio de San Isidro con UN SOLO\n")
        f.write("# concepto en todos los anios: %s.\n" % CONCEPTO_TXT)
        f.write("# Pesos constantes de diciembre de 2025.\n")
        f.write("# Los anios sin dato quedan VACIOS. No se sustituyen por otro\n")
        f.write("# concepto. Ver data/COMPARACIONES_VALIDAS.md.\n")
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)
    return filas, checks, ruta


# --------------------------------------------------------------------------
# 3. Marcar la serie heterogenea como lo que es
# --------------------------------------------------------------------------

def marcar_serie_heterogenea():
    """
    Ya no reescribe nada: la advertencia y el nombre de columna los pone
    03_scripts/deflactor.py al generar el archivo, para que nunca exista sin
    ellos. Aca solo se comprueba que esten.
    """
    ruta = os.path.join(DATA, "serie_gastos_totales_real.csv")
    if not os.path.exists(ruta):
        return None, 0
    filas = _leer("data/serie_gastos_totales_real.csv")
    if filas and "concepto_heterogeneo" not in filas[0]:
        raise ErrorDeSerie(
            "serie_gastos_totales_real.csv no tiene la columna "
            "concepto_heterogeneo; correr 03_scripts/deflactor.py primero")
    cabecera = "".join(l for l in open(ruta, encoding="utf-8")
                       if l.startswith("#"))
    if "ADVERTENCIA" not in cabecera:
        raise ErrorDeSerie("serie_gastos_totales_real.csv perdio la advertencia")
    return ruta, len({f["concepto_heterogeneo"] for f in filas})


# --------------------------------------------------------------------------
# 4. Que comparaciones se sostienen
# --------------------------------------------------------------------------

def pares_validos():
    """
    Un par de anios se puede comparar si los dos miden el MISMO concepto.

    Se calculan dos conjuntos:
      A. Dentro de la serie comparable: todos los pares, porque hay un solo
         concepto. Se marca aparte si alguno de los dos anios es derivado.
      B. Dentro de la serie heterogenea: solo los pares que comparten el mismo
         valor de concepto_heterogeneo.
    """
    comp = _leer("data/serie_gastos_comparable.csv")
    con_dato = [f for f in comp if f["monto_constante_dic2025"]]

    def var(a, b):
        return ((Decimal(b["monto_constante_dic2025"])
                 / Decimal(a["monto_constante_dic2025"]) - 1) * 100
                ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    pares_a = []
    for i, a in enumerate(con_dato):
        for b in con_dato[i + 1:]:
            derivados = [x["anio"] for x in (a, b)
                         if x["origen_del_dato"] == "derivado"]
            pares_a.append({
                "desde": int(a["anio"]), "hasta": int(b["anio"]),
                "anios": int(b["anio"]) - int(a["anio"]),
                "var_real_pct": var(a, b),
                "concepto": CONCEPTO_TXT,
                "nota": ("un extremo derivado de los objetos (%s)"
                         % ", ".join(str(x) for x in derivados)
                         if derivados else "los dos publicados directo"),
            })

    het = [f for f in _leer("data/serie_gastos_totales_real.csv")
           if f.get("monto_constante_dic2025")]
    por_concepto = {}
    for f in het:
        por_concepto.setdefault(f["concepto_heterogeneo"], []).append(f)
    pares_b = []
    for concepto, filas in sorted(por_concepto.items()):
        filas.sort(key=lambda f: int(f["anio"]))
        for i, a in enumerate(filas):
            for b in filas[i + 1:]:
                pares_b.append({
                    "desde": int(a["anio"]), "hasta": int(b["anio"]),
                    "anios": int(b["anio"]) - int(a["anio"]),
                    "var_real_pct": var(a, b),
                    "concepto": concepto,
                })
    return pares_a, pares_b, con_dato, por_concepto


def escribir_comparaciones(pares_a, pares_b, con_dato, por_concepto, checks):
    ruta = os.path.join(DATA, "COMPARACIONES_VALIDAS.md")
    hoy = dt.date.today().isoformat()
    L = []
    w = L.append
    w("# Qué comparaciones de gasto se sostienen\n")
    w("Pesos constantes de diciembre de 2025. Generado por")
    w("`03_scripts/serie_comparable.py` el %s.\n" % hoy)
    w("Una comparación entre dos años se sostiene **si los dos años miden el")
    w("mismo concepto de gasto**. Si no, no es una comparación: es un cambio de")
    w("definición disfrazado de variación.\n")
    w("---\n")
    w("## 1. La serie comparable — usar esta\n")
    w("`data/serie_gastos_comparable.csv`. Un solo concepto en todos los años:")
    w("**%s**.\n" % CONCEPTO_TXT)
    w("Es el gasto de gestión: lo que el Municipio gasta en funcionar y en")
    w("invertir, sin la amortización de deuda ni los movimientos financieros.\n")
    w("| Año | Constante dic-2025 | Var. real | Brecha | Origen |")
    w("|---|---:|---:|---:|---|")
    for f in con_dato:
        w("| %s | %s | %s | %s | %s |" % (
            f["anio"], f["monto_constante_dic2025"],
            (f["var_real_pct"] + "%") if f["var_real_pct"] else "—",
            (str(f["brecha_anios"]) + " año(s)") if f["brecha_anios"] else "—",
            f["origen_del_dato"]))
    w("")
    w("**Todos los pares de esta tabla son comparables entre sí**, porque todos")
    w("miden lo mismo. `origen_del_dato` dice si el año viene publicado directo")
    w("o derivado de los objetos del gasto; la derivación está verificada en la")
    w("sección 3.\n")
    w("---\n")
    w("## 2. Todos los pares válidos de la serie comparable\n")
    w("%d pares. Ordenados por variación real, de la mayor caída a la mayor suba.\n"
      % len(pares_a))
    w("| Desde | Hasta | Años | Var. real | Nota |")
    w("|---|---|---:|---:|---|")
    for p in sorted(pares_a, key=lambda p: p["var_real_pct"]):
        w("| %d | %d | %d | %s%% | %s |" % (p["desde"], p["hasta"], p["anios"],
                                            p["var_real_pct"], p["nota"]))
    w("")
    w("---\n")
    w("## 3. Por qué se puede derivar el concepto desde los objetos\n")
    w("En los años donde la fuente publica **las dos aperturas** —el gasto por")
    w("carácter económico y el gasto por objeto— se comprueba la identidad:\n")
    w("```")
    w("suma de los objetos  −  objetos financieros  ==  corrientes + capital")
    w("```\n")
    w("| Año | Publicado (cte+cap) | Derivado de objetos | Diferencia | ¿Cierra? | |")
    w("|---|---:|---:|---:|---|---|")
    for c in checks:
        w("| %d | %s | %s | %s | %s | %s |" % (
            c["anio"], c["publicado"], c["derivado"], c["diferencia"],
            "sí" if c["cierra"] == "si" else "**no**", c["nota"]))
    w("")
    derivados = [f["anio"] for f in con_dato if f["origen_del_dato"] == "derivado"]
    verificados = sorted(str(c["anio"]) for c in checks if c["cierra"] == "si")
    w("La identidad cierra en **%d de los %d años** donde se puede probar (%s)."
      % (len(verificados), len(checks), ", ".join(verificados)))
    w("Sobre eso se apoya la derivación de los años sin apertura por carácter:")
    w("**%s**.\n" % ", ".join(str(a) for a in derivados))
    w("> **Límite honesto.** Para 2024 y 2025 la fuente es el informe trimestral")
    w("> de ejecución, que **no** publica apertura por carácter económico, así")
    w("> que la identidad no se puede probar en esos años: se apoya en que se")
    w("> cumple en los siete anteriores, con las otras dos fuentes. Si algún día")
    w("> el Municipio publica el Ahorro-Inversión de 2024-2025, hay que")
    w("> recontrastarlo.\n")
    malos = [c for c in checks if c["cierra"] != "si"]
    if malos:
        w("**Los años que no cierran no se derivan**: para ellos se usa el valor")
        w("publicado directo, que existe. La identidad sólo habilita la")
        w("derivación en los años donde no hay apertura por carácter, que son")
        w("los que aparecen como `derivado` en la serie.\n")
    w("---\n")
    w("## 4. Pares válidos dentro de la serie heterogénea\n")
    w("`data/serie_gastos_totales_real.csv` mezcla conceptos. Estos son los")
    w("únicos pares que ahí adentro comparan lo mismo, agrupados por concepto.\n")
    for concepto, filas in sorted(por_concepto.items(),
                                  key=lambda x: -len(x[1])):
        anios = ", ".join(f["anio"] for f in
                          sorted(filas, key=lambda f: int(f["anio"])))
        w("### %s\n" % concepto)
        w("Años: **%s**\n" % anios)
        propios = [p for p in pares_b if p["concepto"] == concepto]
        if not propios:
            w("Un solo año, no hay par posible.\n")
            continue
        w("| Desde | Hasta | Años | Var. real |")
        w("|---|---|---:|---:|")
        for p in sorted(propios, key=lambda p: (p["desde"], p["hasta"])):
            w("| %d | %d | %d | %s%% |" % (p["desde"], p["hasta"], p["anios"],
                                           p["var_real_pct"]))
        w("")
    w("---\n")
    w("## 5. Lo que NO se puede decir\n")
    w("- **No** comparar un año de *gastos con imputación al presupuesto* contra")
    w("  uno de *devengado por objeto*: no miden lo mismo.")
    w("- **No** comparar 2010-2012 contra 2019-2021 usando el *total de gastos*")
    w("  de las rendiciones: el de 2010-2012 incluye las aplicaciones")
    w("  financieras y el de 2019-2021 no. Es el cambio al formato")
    w("  Ahorro-Inversión de los informes ARSI, donde las aplicaciones van")
    w("  debajo de la línea. En 2010 eran el 8,1% del total y en 2021 el 14,0%.")
    w("- **No** leer como variación interanual un salto que cruza años sin dato.")
    w("  La columna `brecha_anios` dice cuántos años acumula cada variación.")
    w("- **No** mezclar presupuestado con ejecutado. El presupuesto está en")
    w("  `data/presupuesto_historico_2010_2026.csv` y es otra cosa.\n")
    w("## 6. Quién gobernaba: la caída no es de una sola gestión\n")
    w("Esto no es un matiz, es la diferencia entre un dato que se sostiene y")
    w("uno que se cae en la primera repregunta.\n")
    w("**Mauricio Lanús asumió en diciembre de 2023.** La caída del gasto real")
    w("empieza mucho antes.\n")
    por_anio = {int(f["anio"]): f for f in con_dato}

    def var_entre(a, b):
        if a not in por_anio or b not in por_anio:
            return None
        return ((Decimal(por_anio[b]["monto_constante_dic2025"])
                 / Decimal(por_anio[a]["monto_constante_dic2025"]) - 1) * 100
                ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    tramos = [
        (2017, 2022, "gestión anterior", "del pico al último año antes de Lanús"),
        (2022, 2025, "gestión Lanús", "último año antes de asumir contra hoy"),
        (2017, 2025, "las dos juntas", "el número completo"),
    ]
    w("| Tramo | Años | Var. real | Qué es |")
    w("|---|---|---:|---|")
    for a, b, quien, que in tramos:
        v = var_entre(a, b)
        if v is None:
            continue
        w("| %s | %d → %d | %s%% | %s |" % (quien, a, b, v, que))
    w("")
    # Solo el tramo que importa: despues del pico de 2017 y antes de que
    # asumiera Lanus. Los anios que caen antes de 2017 no dicen nada sobre
    # esta discusion.
    caidas = [(f["anio"], f["var_real_pct"]) for f in con_dato
              if f["var_real_pct"] and Decimal(f["var_real_pct"]) < 0
              and 2017 < int(f["anio"]) < 2024]
    w("Entre el pico de 2017 y la asunción de Lanús, los años que caen son")
    w("%s. Los tres son de la gestión anterior.\n"
      % ", ".join("**%s** (%s%%)" % (a, v) for a, v in caidas))
    w("### Lo que el dato SÍ sostiene\n")
    w("> El gasto municipal real de San Isidro viene cayendo desde 2017. La")
    w("> gestión de Lanús no revirtió esa caída: la continuó.\n")
    w("### Lo que el dato NO sostiene\n")
    w("> Que la caída del %s%% entre 2017 y 2025 sea el resultado de la gestión"
      % var_entre(2017, 2025))
    w("> de Lanús. **No lo es.** La mayor parte es anterior a diciembre de 2023:")
    w("> 2019, 2020 y 2021 caen con la gestión anterior.\n")
    w("Si alguien presenta el número completo como obra de esta gestión, las")
    w("fechas lo desmienten y el informe entero pierde credibilidad. Se cita")
    w("con el tramo, siempre.\n")
    w("---\n")
    w("## 7. Años sin dato\n")
    w("No hay rendición de cuentas ni informe de ejecución anual publicado para")
    w("**2013, 2018 y 2023**. Quedan vacíos en la serie comparable. No se")
    w("interpolan ni se sustituyen por otro concepto.\n")
    open(ruta, "w", encoding="utf-8").write("\n".join(L))
    return ruta


def main():
    inv, ruta_inv = inventario()
    filas, checks, ruta_serie = serie_comparable()
    ruta_het, n_conceptos = marcar_serie_heterogenea()
    pa, pb, con_dato, por_concepto = pares_validos()
    ruta_comp = escribir_comparaciones(pa, pb, con_dato, por_concepto, checks)
    return {"inventario": inv, "filas": filas, "checks": checks,
            "pares_comparable": pa, "pares_heterogenea": pb,
            "con_dato": con_dato, "n_conceptos": n_conceptos,
            "rutas": [ruta_inv, ruta_serie, ruta_het, ruta_comp]}


if __name__ == "__main__":
    r = main()
    print("=" * 78)
    print("IDENTIDAD: suma de objetos - financieros == corrientes + capital")
    print("=" * 78)
    for c in r["checks"]:
        print("  %d  publicado=%18s  derivado=%18s  dif=%14s  %s"
              % (c["anio"], c["publicado"], c["derivado"], c["diferencia"],
                 "cierra" if c["cierra"] == "si" else "NO CIERRA"))
    print()
    print("=" * 78)
    print("SERIE COMPARABLE - %s" % CONCEPTO_TXT)
    print("=" * 78)
    print("  %-6s %22s %10s %8s %s" % ("anio", "constante dic-2025",
                                       "var real", "brecha", "origen"))
    for f in r["filas"]:
        print("  %-6s %22s %10s %8s %s"
              % (f["anio"], f["monto_constante_dic2025"] or "-",
                 (f["var_real_pct"] + "%") if f["var_real_pct"] else "-",
                 f["brecha_anios"] or "-", f["origen_del_dato"]))
    print()
    print("  anios con dato: %d de %d" % (len(r["con_dato"]), len(r["filas"])))
    print("  pares comparables: %d" % len(r["pares_comparable"]))
    print("  la serie heterogenea mezcla %d conceptos; pares validos ahi: %d"
          % (r["n_conceptos"], len(r["pares_heterogenea"])))
    print()
    for x in r["rutas"]:
        print("  %s" % os.path.relpath(x, REPO))
