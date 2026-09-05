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
import parse_presupuestos as PP
import parse_rendiciones as PR

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

# Ancla de la serie historica: recursos por origen del presupuesto 2011, en
# centavos. Fuente: presupuesto2011.pdf pagina 4, verificado a mano.
ANCLA_2011 = [
    ("municipal", 39798500000),
    ("provincial", 21331040000),
    ("nacional", 614400000),
    ("otros", 1311500000),
]


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


def test_ancla_2011():
    """Los cuatro origenes de recursos del presupuesto 2011, exactos."""
    spec = next(s for s in PP.ESPECIFICACIONES if s["archivo"] == "presupuesto2011.pdf")
    filas = PP.extraer(spec)
    obtenido = {f["subconcepto"]: f["monto"] for f in filas
                if f["concepto"] == "recursos_por_origen"}

    errores = []
    for clave, esperado in ANCLA_2011:
        if obtenido.get(clave) != esperado:
            errores.append("%s: esperado %s, obtenido %s" % (
                clave, PP.formatear(esperado), PP.formatear(obtenido.get(clave))))
    if errores:
        raise FalloDeTest("ANCLA 2011 FALLADA:\n  " + "\n  ".join(errores))

    print("ANCLA 2011 — presupuesto2011.pdf, recursos por origen")
    print("-" * 74)
    total = sum(v for _, v in ANCLA_2011)
    for clave, esperado in ANCLA_2011:
        print("  %-12s %22s   %5.1f%%  OK" % (
            clave, PP.formatear(esperado), esperado * 100.0 / total))
    print("  %-12s %22s          OK" % ("TOTAL", PP.formatear(total)))
    print()


# Ancla de la serie de ejecucion: rendicion de cuentas 2010, en centavos.
# Fuente: rendicion2010.pdf, paginas 1 y 2, verificado a mano.
ANCLA_2010_GASTOS = [
    ("gastos_corrientes", 53139595900),
    ("aplicaciones_financieras", 5057401300),
    ("gastos_de_capital", 4323593700),
]
ANCLA_2010_RECURSOS = [
    ("ingresos_no_tributarios", 32333711451),
    ("ingresos_tributarios", 16706280420),
    ("transferencias_corrientes", 3628531792),
    ("transferencias_de_capital", 2798860762),
    ("recursos_propios_de_capital", 348694680),
    ("rentas_de_la_propiedad", 22380116),
]
ANCLA_2010_TOTAL_GASTOS = 62520591074


def test_ancla_2010():
    """Los gastos y recursos de la rendicion 2010, exactos."""
    spec = next(s for s in PR.ESPECIFICACIONES if s["archivo"] == "rendicion2010.pdf")
    filas = PR.extraer(spec)
    obtenido = {}
    for f in filas:
        obtenido.setdefault(f["concepto"], {})[f["subconcepto"]] = f["monto"]

    errores = []
    for concepto, esperados in (("gastos_por_caracter", ANCLA_2010_GASTOS),
                                ("recursos_por_rubro", ANCLA_2010_RECURSOS)):
        for clave, esperado in esperados:
            real = obtenido.get(concepto, {}).get(clave)
            if real != esperado:
                errores.append("%s/%s: esperado %s, obtenido %s" % (
                    concepto, clave, PP.formatear(esperado), PP.formatear(real)))
    total = obtenido.get("total_gastos", {}).get("")
    if total != ANCLA_2010_TOTAL_GASTOS:
        errores.append("total_gastos: esperado %s, obtenido %s" % (
            PP.formatear(ANCLA_2010_TOTAL_GASTOS), PP.formatear(total)))
    if errores:
        raise FalloDeTest("ANCLA 2010 FALLADA:\n  " + "\n  ".join(errores))

    print("ANCLA 2010 — rendicion2010.pdf")
    print("-" * 74)
    print("  gastos por caracter economico")
    for clave, esperado in ANCLA_2010_GASTOS:
        print("    %-30s %20s  OK" % (clave, PP.formatear(esperado)))
    print("    %-30s %20s  OK" % ("TOTAL", PP.formatear(ANCLA_2010_TOTAL_GASTOS)))
    print("  recursos por rubro")
    for clave, esperado in ANCLA_2010_RECURSOS:
        print("    %-30s %20s  OK" % (clave, PP.formatear(esperado)))
    print()


def chequeo_arsi(rendiciones):
    """Si el error del informe ARSI de presupuesto 2020 tambien esta en el de rendicion.

    En la tarea anterior aparecio que informe_arsi_presupuesto_2020.pdf no cierra
    consigo mismo: sus seis objetos del gasto suman 90.000.000 mas que su propia
    linea TOTALES. La pregunta es si eso es un defecto del formato ARSI o un
    error puntual de ese documento.
    """
    print("CHEQUEO CRUZADO — el error de ARSI presupuesto 2020, en las rendiciones")
    print("-" * 74)
    por_anio = {}
    for f in rendiciones:
        if "arsi" in f["fuente"]:
            por_anio.setdefault(f["anio"], {}).setdefault(f["concepto"], {})[
                f["subconcepto"]] = f["monto"]

    hay_error = False
    for anio in sorted(por_anio):
        d = por_anio[anio]
        rubros = sum(d.get("recursos_por_rubro", {}).values())
        total_r = d.get("total_recursos", {}).get("")
        caracter = d.get("gastos_por_caracter", {})
        gastos = caracter.get("gastos_corrientes", 0) + caracter.get("gastos_de_capital", 0)
        total_g = d.get("total_gastos", {}).get("")
        ok_r = total_r is not None and rubros == total_r
        ok_g = total_g is not None and gastos == total_g
        hay_error = hay_error or not (ok_r and ok_g)
        print("  %s  rubros vs total recursos: %-2s   gastos vs total gastos: %-2s" % (
            anio, "OK" if ok_r else "NO", "OK" if ok_g else "NO"))
    if hay_error:
        print("  -> alguna rendicion ARSI tampoco cierra: el problema es del formato.")
    else:
        print("  -> las tres rendiciones ARSI cierran consigo mismas. El error de")
        print("     90.000.000 es del informe de PRESUPUESTO 2020, no del formato ARSI.")
    print()


def validar_rendiciones(filas, fallas):
    """Por anio: rubros suman recursos, caracter suma gastos, jurisdicciones tambien."""
    por_doc = {}
    for f in filas:
        por_doc.setdefault((f["anio"], f["fuente"]), []).append(f)

    for (anio, fuente), grupo in sorted(por_doc.items()):
        partes = {}
        for f in grupo:
            partes.setdefault(f["concepto"], {})[f["subconcepto"]] = f["monto"]
        arsi = "arsi" in fuente

        for concepto, clave_total, etiqueta in (
                ("recursos_por_rubro", "total_recursos", "los rubros de recursos"),
                ("gastos_por_caracter", "total_gastos", "los gastos por caracter"),
                ("gastos_por_jurisdiccion", "total_gastos_jurisdiccion",
                 "las jurisdicciones"),
                ("recursos_por_origen", "total_recursos_origen",
                 "los origenes de recursos"),
                ("gastos_por_objeto", "total_gastos_objeto",
                 "los objetos del gasto")):
            detalle = partes.get(concepto)
            total = partes.get(clave_total, {}).get("")
            if not detalle or total is None:
                continue
            if concepto == "gastos_por_caracter" and arsi:
                # En la Cuenta Ahorro-Inversion las aplicaciones financieras van
                # debajo de la linea y no entran en GASTOS TOTALES.
                suma = (detalle.get("gastos_corrientes", 0)
                        + detalle.get("gastos_de_capital", 0))
            else:
                suma = sum(detalle.values())
            if suma != total:
                fallas.append(({"fuente": fuente, "anio": anio, "trimestre": "",
                                "fila": concepto},
                               "suma de %s = %s, %s del documento = %s "
                               "(diferencia %s)" % (
                                   etiqueta, PP.formatear(suma), clave_total,
                                   PP.formatear(total), PP.formatear(suma - total))))


# --------------------------------------------------------------------------
# validaciones por trimestre
# --------------------------------------------------------------------------

def _clave(fila):
    """Identificador legible de la fila dentro de su trimestre."""
    if "fila" in fila:
        return fila["fila"]
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


def validar_presupuestos(filas, fallas):
    """Por documento: los origenes suman el total, los objetos suman el total."""
    por_doc = {}
    for f in filas:
        por_doc.setdefault((f["anio"], f["fuente"]), []).append(f)

    for (anio, fuente), grupo in sorted(por_doc.items()):
        partes = {}
        for f in grupo:
            partes.setdefault(f["concepto"], {})[f["subconcepto"]] = f["monto"]

        for concepto, clave_total, etiqueta in (
                ("recursos_por_origen", "total_recursos", "los origenes"),
                ("gastos_por_objeto", "total_gastos", "los objetos del gasto")):
            detalle = partes.get(concepto)
            total = partes.get(clave_total, {}).get("")
            if not detalle or total is None:
                continue
            suma = sum(detalle.values())
            if suma != total:
                fallas.append(({"fuente": fuente, "anio": anio, "trimestre": "",
                                "fila": concepto},
                               "suma de %s = %s, %s del documento = %s "
                               "(diferencia %s)" % (
                                   etiqueta, PP.formatear(suma), clave_total,
                                   PP.formatear(total), PP.formatear(suma - total))))


def main():
    test_dorado()
    test_ancla_2011()
    test_ancla_2010()

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

    print("PARSEO DE LOS PRESUPUESTOS HISTORICOS")
    print("-" * 74)
    presupuestos = PP.main()
    print()
    validar_presupuestos(presupuestos["filas"], fallas)

    print("PARSEO DE LAS RENDICIONES DE CUENTAS")
    print("-" * 74)
    rendiciones = PR.main()
    PR.escribir_comparacion(presupuestos["filas"], rendiciones["filas"])
    print()
    validar_rendiciones(rendiciones["filas"], fallas)
    chequeo_arsi(rendiciones["filas"])

    P.escribir_no_parseados([
        ("Ejecucion presupuestaria: no se pudieron parsear", "motivo",
         resultado["no_parseados"]),
        ("Ejecucion presupuestaria: omitidos por ser copia exacta de otro",
         "duplicado", resultado["duplicados"]),
        ("Presupuestos historicos: no se pudieron parsear", "motivo",
         presupuestos["no_parseados"]),
        ("Presupuestos historicos: excluidos a proposito", "motivo",
         presupuestos["excluidos"]),
        ("Rendiciones de cuentas: no se pudieron parsear", "motivo",
         rendiciones["no_parseados"]),
        ("Rendiciones de cuentas: excluidas a proposito", "motivo",
         rendiciones["excluidos"]),
    ])

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
          " funcion, %d deuda, %d presupuesto historico, %d rendiciones"
          % (len(objeto), len(recursos), len(fyf), len(deuda),
             len(presupuestos["filas"]), len(rendiciones["filas"])))
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
    print("TEST DORADO OK — ANCLA 2011 OK — ANCLA 2010 OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
