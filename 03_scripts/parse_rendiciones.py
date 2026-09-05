#!/usr/bin/env python3
"""
Rendiciones de cuentas de San Isidro: la serie de ejecucion real.

El presupuesto dice lo proyectado; la rendicion, lo que efectivamente paso. Lee
01_raw/sanisidro_transparencia/rendicion_de_cuentas/ y escribe
data/rendiciones_2010_2021.csv, en pesos corrientes y sin deflactar.

Dos formas de leer, porque los documentos no se parecen en nada:

  tabla   Las rendiciones 2011 y 2012 y los informes ARSI publican cuadros de
          verdad: una fila por concepto, con su importe al lado. Se leen por
          linea.

  torta   La rendicion 2010 son graficos de torta y no hay lineas que valgan.
          Cada etiqueta es un bloque de texto suelto alrededor del grafico, con
          el rotulo, el importe y el porcentaje repartidos en varios renglones y
          desordenados respecto del resto de la pagina. Peor: el importe se
          parte al medio entre dos renglones, '$323.337.114,5' arriba y '1' abajo.
          Se resuelve agrupando las palabras en bloques por cercania y armando
          cada bloque por separado.

Los importes se manejan como enteros en centavos. Ningun float en la aritmetica.

Uso:
    python3 03_scripts/parse_rendiciones.py
"""

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdfplumber

import pdf_tabla as T
import parse_presupuestos as PP

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDICIONES = os.path.join(
    RAIZ, "01_raw", "sanisidro_transparencia", "rendicion_de_cuentas")
DATA = os.path.join(RAIZ, "data")

# Un resultado negativo se imprime entre parentesis: '$ (610.071.834,08)'.
RE_PARENTESIS = re.compile(r"\(\s*([\d.,]+)\s*\)")


class ErrorDeParseo(Exception):
    """El PDF no se pudo leer con la estructura esperada."""


# --------------------------------------------------------------------------
# bloques de texto (graficos de torta)
# --------------------------------------------------------------------------

# Dos palabras son del mismo bloque si estan en el mismo renglon y pegadas, o en
# renglones consecutivos y solapadas horizontalmente. Los valores salen de medir
# la rendicion 2010: los renglones de una etiqueta van cada 22.5 pt y las
# etiquetas vecinas nunca se solapan en horizontal.
SALTO_MAXIMO = 26.0
HUECO_MAXIMO = 20.0
MISMA_LINEA = 4.0


def _solapan(a, b):
    return min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]) > 0


def _vecinas(a, b):
    dv = abs(a["top"] - b["top"])
    if dv < MISMA_LINEA:
        return max(a["x0"], b["x0"]) - min(a["x1"], b["x1"]) <= HUECO_MAXIMO
    return dv <= SALTO_MAXIMO and _solapan(a, b)


def bloques_de_pagina(pagina):
    """Agrupa las palabras de la pagina en bloques de texto por cercania.

    Devuelve [(texto_espaciado, texto_junto)]. El primero une los renglones con
    un espacio y sirve para leer el rotulo; el segundo los une sin nada y sirve
    para leer el importe, porque es el unico que vuelve a pegar los pedazos de un
    numero partido entre dos renglones.
    """
    palabras = pagina.extract_words()
    if not palabras:
        return []

    padre = list(range(len(palabras)))

    def raiz(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    for i, a in enumerate(palabras):
        for j in range(i + 1, len(palabras)):
            b = palabras[j]
            if b["top"] - a["top"] > SALTO_MAXIMO and b["top"] > a["top"]:
                continue
            if _vecinas(a, b):
                ra, rb = raiz(i), raiz(j)
                if ra != rb:
                    padre[ra] = rb

    grupos = {}
    for i, w in enumerate(palabras):
        grupos.setdefault(raiz(i), []).append(w)

    salida = []
    for grupo in grupos.values():
        renglones = {}
        for w in grupo:
            clave = round(w["top"] / MISMA_LINEA)
            renglones.setdefault(clave, []).append(w)
        ordenados = []
        for clave in sorted(renglones):
            fila = sorted(renglones[clave], key=lambda w: w["x0"])
            ordenados.append(" ".join(w["text"] for w in fila))
        salida.append(_reparar_partido(" ".join(ordenados)))
    return salida


# Un importe cortado entre dos renglones deja el primer pedazo con UNA sola
# cifra decimal y el resto arranca el renglon siguiente: '$323.337.114,5' y
# despues '1 ; 58%' son 323.337.114,51. La condicion de una sola decimal es la
# que hace segura la reparacion: '$50.574.013 8%' no tiene decimales y
# '$2.577.753,19 0,5%' ya tiene las dos, asi que ninguno se toca. El
# lookahead evita pegarle un porcentaje al importe.
RE_PARTIDO = re.compile(r"(?<=\d)([.,]\d)\s+(\d)(?![\d.,%])")


def _reparar_partido(texto):
    return RE_PARTIDO.sub(r"\1\2", texto)


# --------------------------------------------------------------------------
# vocabulario
# --------------------------------------------------------------------------

RUBROS = [
    ("ingresos_no_tributarios", ["INGRESOS NO TRIBUTARIOS"]),
    ("ingresos_tributarios", ["INGRESOS TRIBUTARIOS"]),
    ("rentas_de_la_propiedad", ["RENTAS DE LA PROPIEDAD"]),
    ("transferencias_corrientes", ["TRANSFERENCIAS CORRIENTES"]),
    ("transferencias_de_capital", ["TRANSFERENCIAS DE CAPITAL"]),
    ("recursos_propios_de_capital", ["RECURSOS PROPIOS DE CAPITAL"]),
    ("disminucion_otros_activos_financieros",
     ["DISMINUCION DE OTROS ACTIVOS FINANCIEROS"]),
    ("obtencion_de_prestamos", ["OBTENCION DE PRESTAMOS"]),
]

CARACTER = [
    ("gastos_corrientes", ["GASTOS CORRIENTES", "TOTAL GASTOS CORRIENTES"]),
    ("gastos_de_capital", ["GASTOS DE CAPITAL", "TOTAL GASTOS DE CAPITAL"]),
    ("aplicaciones_financieras",
     ["APLICACIONES FINANCIERAS", "TOTAL APLICACIONES FINANCIERAS"]),
]

OBJETOS = [
    ("recursos_humanos", ["RECURSOS HUMANOS"]),
    ("bienes_de_consumo", ["BIENES DE CONSUMO", "BS. DE CONSUMO"]),
    ("servicios_no_personales", ["SERVICIOS NO PERSONALES"]),
    ("bienes_de_uso", ["BIENES DE USO", "BS. DE USO"]),
    ("transferencias", ["TRANSFERENCIAS"]),
    ("activos_financieros", ["ACTIVOS FINANCIEROS"]),
    ("servicio_de_la_deuda",
     ["SERVICIOS DE LA DEUDA Y DISMINUCION DE OTROS PASIVOS",
      "SERVICIO DE LA DEUDA Y DISMINUCION DE OTROS PASIVOS"]),
    # La lamina de 2010 abre las transferencias en corrientes y de capital y
    # suma un renglon de rentas de la propiedad. Se listan aparte para no
    # mezclarlas con la 'Transferencias' unica de 2011 y 2012.
    ("transferencias_corrientes", ["TRANSFERENCIAS CORRIENTES"]),
    ("transferencias_de_capital", ["TRANSFERENCIAS DE CAPITAL"]),
    ("rentas_de_la_propiedad", ["RENTAS DE LA PROPIEDAD"]),
]

ORIGENES = [
    ("municipal", ["ORIGEN MUNICIPAL"]),
    ("provincial", ["ORIGEN PROVINCIAL"]),
    ("nacional", ["ORIGEN NACIONAL"]),
    ("otros", ["OTROS ORIGENES"]),
]

# Las jurisdicciones cambian de nombre casi todos los anios. Se identifican por
# el numero de orden, que si se mantiene, y se guarda el rotulo tal cual salio.
RE_JURISDICCION = re.compile(r"^(\d)\s*[.\-]\s*(.+)$")


# --------------------------------------------------------------------------
# lectura
# --------------------------------------------------------------------------

def _monto_de_texto(texto):
    """Primer importe del texto, o None. Los parentesis significan negativo."""
    negativo = False
    m = RE_PARENTESIS.search(texto)
    if m:
        texto, negativo = m.group(1), True
    # El porcentaje puede venir pegado al importe sin separador ('...95985%').
    # Se corta antes de descomponer, porque si no la corrida no cierra en
    # ningun formato y el importe se pierde entero.
    texto = re.sub(r"(\d)\s*%", r"\1 %", texto)
    montos = PP.montos_de_linea(texto)
    if not montos:
        return None
    valor = PP.a_centavos(montos[0][0])
    return -valor if negativo else valor


def _porcentaje_de_texto(texto):
    """Porcentaje de la etiqueta, como texto tal cual sale del PDF."""
    m = re.search(r"(\d{1,3}(?:[.,]\d+)?)\s*%", texto)
    return m.group(1).replace(",", ".") if m else ""


def filas_tabla(ruta, pagina):
    """[(rotulo, texto_completo)] de una pagina leida por lineas."""
    with pdfplumber.open(ruta) as pdf:
        if pagina > len(pdf.pages):
            raise ErrorDeParseo("el PDF no tiene pagina %d" % pagina)
        lineas = T.lineas_de_pagina(pdf.pages[pagina - 1])
    # Un rotulo largo se parte en dos renglones y el importe queda en el
    # segundo: '3. Secretaria de Integracion Comunitaria y Desarrollo' arriba y
    # 'Social $131,185,249.56 16.47%' abajo. Por eso cada fila lleva dos
    # rotulos, el propio y el que arrastra los renglones sin importe que vienen
    # antes. Se guardan los dos y se prueba primero el propio: pegar siempre el
    # anterior romperia las tablas ARSI, donde antes de 'TOTAL RECURSOS
    # CORRIENTES' hay renglones sueltos que no son parte de su rotulo.
    salida, pendiente = [], []
    for linea in lineas:
        texto = linea["texto"].strip()
        if not texto:
            continue
        montos = PP.montos_de_linea(texto)
        corte = montos[0][1] if montos else len(texto)
        rotulo = T.normalizar(texto[:corte]).strip(" .-$;:")
        if not montos:
            pendiente.append(rotulo)
            salida.append((rotulo, rotulo, texto))
            continue
        extendido = " ".join([x for x in pendiente if x] + [rotulo]).strip()
        salida.append((rotulo, extendido, texto))
        pendiente = []
    return salida


# Una etiqueta de torta es 'rotulo; $importe ; porcentaje%'. Dos etiquetas
# vecinas pueden caer en el mismo bloque si el grafico las dibujo pegadas, asi
# que en cada bloque se buscan TODAS las apariciones y no una sola.
RE_ETIQUETA = re.compile(r"\$\s*(-?[\d][\d.,]*)")


def filas_torta(ruta, pagina):
    """[(rotulo, texto_completo)] de una pagina de graficos de torta."""
    with pdfplumber.open(ruta) as pdf:
        if pagina > len(pdf.pages):
            raise ErrorDeParseo("el PDF no tiene pagina %d" % pagina)
        bloques = bloques_de_pagina(pdf.pages[pagina - 1])

    salida = []
    for bloque in bloques:
        marcas = list(RE_ETIQUETA.finditer(bloque))
        if not marcas:
            rotulo = T.normalizar(bloque).strip(" .-")
            salida.append((rotulo, rotulo, bloque))
            continue
        for i, m in enumerate(marcas):
            inicio = marcas[i - 1].end() if i else 0
            etiqueta = bloque[inicio:m.start()]
            fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(bloque)
            resto = bloque[m.start():fin]
            # Cuando dos etiquetas cayeron en el mismo bloque, la segunda
            # arranca despues del porcentaje de la primera.
            rotulo = T.normalizar(etiqueta.rsplit("%", 1)[-1]).strip(" .-;:,")
            salida.append((rotulo, rotulo, resto))
    return salida


def _leer(ruta, pagina, modo):
    return filas_torta(ruta, pagina) if modo == "torta" else filas_tabla(ruta, pagina)


def _buscar(filas, alternativas):
    """Primera fila cuyo rotulo coincide. Devuelve (monto, porcentaje)."""
    objetivos = {T.normalizar(a) for a in alternativas}
    for rotulo, extendido, texto in filas:
        if rotulo in objetivos or extendido in objetivos:
            monto = _monto_de_texto(texto)
            if monto is not None:
                return monto, _porcentaje_de_texto(texto)
    return None, ""


def _buscar_total(filas, etiqueta):
    objetivo = T.normalizar(etiqueta)
    for rotulo, _, texto in filas:
        if rotulo == objetivo or rotulo.startswith(objetivo):
            monto = _monto_de_texto(texto)
            if monto is not None:
                return monto
    return None


def _total_del_titulo(filas):
    """Total del encabezado de la lamina: 'CARACTER ECONOMICO: $625.205.910,74'.

    Se reconoce porque el rotulo termina en dos puntos y no lleva porcentaje: las
    etiquetas de las porciones siempre traen su participacion.
    """
    for rotulo, _, texto in filas:
        if rotulo.endswith(":") and not _porcentaje_de_texto(texto):
            monto = _monto_de_texto(texto)
            if monto is not None:
                return monto
    for rotulo, _, texto in filas:
        if not _porcentaje_de_texto(texto):
            monto = _monto_de_texto(texto)
            if monto is not None:
                return monto
    return None


def jurisdicciones(filas):
    """[(nombre, monto, porcentaje)] de una lamina de jurisdicciones.

    En 2011 y 2012 las jurisdicciones vienen numeradas ('1. Sec. Gral. ...') y
    en 2010 no, porque son porciones de una torta. Se guarda el rotulo tal cual
    lo publica el documento, con su numero si lo trae: los nombres de las
    secretarias cambian casi todos los anios y homogeneizarlos seria inventar
    una correspondencia que el municipio no declara.
    """
    salida, vistos = [], set()
    for rotulo, extendido, texto in filas:
        if not rotulo or rotulo.endswith(":"):
            continue
        # La fila del total tambien trae porcentaje (100%), asi que hay que
        # sacarla a mano o el gasto por jurisdiccion suma el doble.
        if re.match(r"^TOTAL(ES)?\b", extendido):
            continue
        pct = _porcentaje_de_texto(texto)
        monto = _monto_de_texto(texto)
        if monto is None or not pct:
            continue
        m = RE_JURISDICCION.match(extendido)
        nombre = "%s. %s" % (m.group(1), m.group(2).strip()) if m else extendido
        if nombre in vistos:
            continue
        vistos.add(nombre)
        salida.append((nombre, monto, pct))
    return salida


# --------------------------------------------------------------------------
# especificacion por documento
# --------------------------------------------------------------------------
#
# 'modo' es "torta" o "tabla". 'total' es el rotulo exacto de la fila del total,
# o "titulo" cuando el total va en el encabezado de la lamina.
#
# caracter_sin_aplicaciones marca a los informes ARSI: su cuadro es una Cuenta
# Ahorro-Inversion-Financiamiento, donde las aplicaciones financieras van
# DEBAJO de la linea y no entran en 'GASTOS TOTALES'. En las rendiciones 2010 a
# 2012, en cambio, la lamina de caracter economico si las incluye en su total.
# Sin esta distincion la validacion marcaria como error una diferencia que es de
# definicion contable, no de datos.

ESPECIFICACIONES = [
    {"anio": 2010, "archivo": "rendicion2010.pdf", "modo": "torta",
     "rubro": {"pagina": 1},
     "caracter": {"pagina": 2, "total": "titulo"},
     "jurisdiccion": {"pagina": 3, "total": "titulo"},
     "objeto": {"pagina": 4, "total": "titulo"},
     "origen": {"pagina": 5, "total": "titulo"}},

    {"anio": 2011, "archivo": "rendicionctas20111.pdf", "modo": "tabla",
     "rubro": {"pagina": 3, "total": "TOTALES"},
     "caracter": {"pagina": 8, "total": "TOTALES"},
     "objeto": {"pagina": 9, "total": "TOTALES"},
     "jurisdiccion": {"pagina": 11, "total": "TOTALES"}},

    {"anio": 2012, "archivo": "rendicionctas-2012_02.pdf", "modo": "tabla",
     "rubro": {"pagina": 3, "total": "TOTALES"},
     "caracter": {"pagina": 12, "total": "TOTALES"},
     "objeto": {"pagina": 13, "total": "TOTALES"},
     "jurisdiccion": {"pagina": 15, "total": "TOTALES"}},

    {"anio": 2019, "archivo": "informe_arsi_rendicion_de_cuentas_2019.pdf",
     "modo": "tabla", "caracter_sin_aplicaciones": True,
     "rubro": {"pagina": 3, "total": "INGRESOS TOTALES"},
     "caracter": {"paginas": [3, 4], "total": "GASTOS TOTALES"},
     "resultado": {"pagina": 3, "etiqueta": "RESULTADO FINANCIERO"}},

    {"anio": 2020, "archivo": "informe_arsi_rendicion_de_cuentas_2020.pdf",
     "modo": "tabla", "caracter_sin_aplicaciones": True,
     "rubro": {"pagina": 3, "total": "INGRESOS TOTALES"},
     "caracter": {"paginas": [3, 4], "total": "GASTOS TOTALES"},
     "resultado": {"pagina": 3, "etiqueta": "RESULTADO FINANCIERO"}},

    {"anio": 2021, "archivo": "informe_arsi_rendicion_de_cuentas_2021.pdf",
     "modo": "tabla", "caracter_sin_aplicaciones": True,
     "rubro": {"pagina": 3, "total": "INGRESOS TOTALES"},
     "caracter": {"paginas": [3, 4], "total": "GASTOS TOTALES"},
     "resultado": {"pagina": 3, "etiqueta": "RESULTADO FINANCIERO"}},
]

EXCLUIDOS = [
    ("_rendicion2017.pdf.pdf",
     "Las tablas estan pegadas como imagen: 23 paginas con 836 caracteres de "
     "texto y cero importes. Sin OCR no hay nada que extraer."),
    ("msi-rendicion-2015.pdf",
     "Las tablas estan pegadas como imagen: 26 paginas con 920 caracteres de "
     "texto y cero importes."),
    ("msi-rendicion-a-o-2014.pdf",
     "Las tablas estan pegadas como imagen: 38 paginas con 1487 caracteres de "
     "texto y cero importes."),
    ("msi_rendicion_2022_1.pdf",
     "Las tablas estan pegadas como imagen: 15 paginas con 183 caracteres de "
     "texto y cero importes."),
]


def _paginas(s):
    # Con .get(clave, s["pagina"]) el default se evalua siempre y revienta en
    # las specs que solo declaran "paginas".
    return s["paginas"] if "paginas" in s else [s["pagina"]]


def extraer(spec):
    """Devuelve las filas del CSV para una rendicion."""
    ruta = os.path.join(RENDICIONES, spec["archivo"])
    if not os.path.exists(ruta):
        raise ErrorDeParseo("no existe el archivo")
    anio, fuente, modo = spec["anio"], spec["archivo"], spec["modo"]
    filas = []

    def agregar(concepto, subconcepto, monto, porcentaje, pagina):
        if monto is not None:
            filas.append({"anio": anio, "concepto": concepto,
                          "subconcepto": subconcepto, "monto": monto,
                          "porcentaje": porcentaje, "fuente": fuente,
                          "pagina": pagina})

    def total_de(s, datos):
        if s.get("total") == "titulo":
            return _total_del_titulo(datos)
        return _buscar_total(datos, s["total"]) if s.get("total") else None

    bloques = (("rubro", "recursos_por_rubro", RUBROS, "total_recursos"),
               ("caracter", "gastos_por_caracter", CARACTER, "total_gastos"),
               ("objeto", "gastos_por_objeto", OBJETOS, "total_gastos_objeto"),
               ("origen", "recursos_por_origen", ORIGENES, "total_recursos_origen"))

    for clave, concepto, vocabulario, concepto_total in bloques:
        if clave not in spec:
            continue
        s = spec[clave]
        datos = []
        for pagina in _paginas(s):
            datos.extend(_leer(ruta, pagina, modo))
        planas = datos
        pagina_ref = _paginas(s)[0]
        for sub, alternativas in vocabulario:
            monto, pct = _buscar(planas, alternativas)
            agregar(concepto, sub, monto, pct, pagina_ref)
        agregar(concepto_total, "", total_de(s, planas), "", pagina_ref)

    if "jurisdiccion" in spec:
        s = spec["jurisdiccion"]
        datos = _leer(ruta, s["pagina"], modo)
        for nombre, monto, pct in jurisdicciones(datos):
            agregar("gastos_por_jurisdiccion", nombre, monto, pct, s["pagina"])
        agregar("total_gastos_jurisdiccion", "", total_de(s, datos), "",
                s["pagina"])

    if "resultado" in spec:
        s = spec["resultado"]
        datos = _leer(ruta, s["pagina"], modo)
        agregar("resultado_del_ejercicio", "",
                _buscar_total(datos, s["etiqueta"]), "", s["pagina"])

    if not filas:
        raise ErrorDeParseo("no se extrajo ningun importe con la especificacion")
    return filas


def main():
    filas, no_parseados = [], []
    for spec in ESPECIFICACIONES:
        try:
            filas.extend(extraer(spec))
        except Exception as exc:
            no_parseados.append((spec["archivo"],
                                 "%s: %s" % (type(exc).__name__, exc)))

    filas.sort(key=lambda f: (f["anio"], f["concepto"], f["subconcepto"]))

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "rendiciones_2010_2021.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["anio", "concepto", "subconcepto", "monto", "porcentaje",
                    "fuente", "pagina"])
        for f in filas:
            w.writerow([f["anio"], f["concepto"], f["subconcepto"],
                        PP.formatear(f["monto"]), f["porcentaje"],
                        f["fuente"], f["pagina"]])

    print("  rendiciones_2010_2021.csv             %d filas" % len(filas))
    return {"filas": filas, "no_parseados": no_parseados, "excluidos": EXCLUIDOS}



# --------------------------------------------------------------------------
# presupuestado contra ejecutado
# --------------------------------------------------------------------------

def _totales(filas, concepto):
    return {f["anio"]: f for f in filas if f["concepto"] == concepto}


def escribir_comparacion(presupuestos, rendiciones):
    """Cruza presupuesto y rendicion para los anios que tienen los dos.

    Solo pone las dos cifras, la diferencia en pesos y en porcentaje. No saca
    ninguna conclusion: que el ejecutado difiera del presupuestado puede ser
    subejecucion, refuerzo presupuestario o diferencia de criterio contable, y
    eso no se decide desde una resta.
    """
    filas = []
    for concepto in ("total_recursos", "total_gastos"):
        pres = _totales(presupuestos, concepto)
        rend = _totales(rendiciones, concepto)
        for anio in sorted(set(pres) & set(rend)):
            p, r = pres[anio], rend[anio]
            diferencia = r["monto"] - p["monto"]
            pct = ("%.2f" % (diferencia * 100.0 / p["monto"])) if p["monto"] else ""
            nota = ""
            if concepto == "total_gastos" and "arsi" in r["fuente"]:
                nota = ("el ejecutado sale de la Cuenta Ahorro-Inversion, que "
                        "deja las aplicaciones financieras debajo de la linea; "
                        "el presupuestado si las incluye")
            filas.append({
                "anio": anio, "concepto": concepto,
                "presupuestado": p["monto"], "fuente_presupuesto": p["fuente"],
                "ejecutado": r["monto"], "fuente_rendicion": r["fuente"],
                "diferencia": diferencia, "diferencia_pct": pct, "nota": nota})

    filas.sort(key=lambda f: (f["anio"], f["concepto"]))
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "presupuestado_vs_ejecutado.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["anio", "concepto", "presupuestado", "ejecutado",
                    "diferencia", "diferencia_pct", "fuente_presupuesto",
                    "fuente_rendicion", "nota"])
        for f in filas:
            w.writerow([f["anio"], f["concepto"], PP.formatear(f["presupuestado"]),
                        PP.formatear(f["ejecutado"]), PP.formatear(f["diferencia"]),
                        f["diferencia_pct"], f["fuente_presupuesto"],
                        f["fuente_rendicion"], f["nota"]])
    print("  presupuestado_vs_ejecutado.csv        %d filas" % len(filas))
    return filas
if __name__ == "__main__":
    resultado = main()
    escribir_comparacion(PP.main()["filas"], resultado["filas"])
