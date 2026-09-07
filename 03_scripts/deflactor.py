#!/usr/bin/env python3
"""
Deflactor de precios para las series fiscales de San Isidro.

Todo lo que hay en el repo esta en pesos corrientes y cubre 2010-2026, un
periodo con anios de inflacion superior al 200%. Sin deflactar, la serie no se
puede comparar entre anios ni proyectar.

QUE HACE
  1. Baja el IPC del INDEC (nacional, nivel general, mensual) y el IPC de la
     Provincia de San Luis (nivel general, mensual).
  2. Los empalma en un solo indice mensual continuo 2010-01 -> ultimo mes
     publicado, con base diciembre 2016 = 100 (la base del INDEC).
  3. Construye el deflactor con base diciembre 2025 = 100.
  4. Aplica el deflactor a los datasets del repo.

POR QUE HAY EMPALME
  El IPC nacional del INDEC arranca en diciembre de 2016. Para 2010-2016 no hay
  serie oficial nacional continua por el periodo de intervencion del organismo.
  Se empalma con el IPC de San Luis, que es oficial, provincial, mensual y
  continuo desde octubre de 2005. Ver data/METODOLOGIA_DEFLACTOR.md.

  NINGUN valor se estima ni se interpola. El empalme es una multiplicacion por
  un coeficiente unico y publicado; cualquiera lo puede rehacer con las dos
  series publicas.

Uso:
    python3 03_scripts/deflactor.py              # baja, construye y aplica
    python3 03_scripts/deflactor.py --sin-red    # usa lo ya bajado en 01_raw/
"""

import csv
import datetime as dt
import hashlib
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
RAW_IPC = os.path.join(REPO, "01_raw", "indec")
DATA = os.path.join(REPO, "data")

# --------------------------------------------------------------------------
# Fuentes. Las URL son las de descarga directa; quedan registradas en
# 01_raw/indec/DESCARGA.txt junto con el md5 y la fecha de bajada.
# --------------------------------------------------------------------------

URL_INDEC = ("https://www.indec.gob.ar/ftp/cuadros/economia/"
             "serie_ipc_divisiones.csv")
ARCH_INDEC = "serie_ipc_divisiones.csv"

# El IPC de San Luis lo publica la Direccion Provincial de Estadistica y Censos
# de San Luis y se distribuye por el portal oficial de datos abiertos del Estado
# nacional (serie 197.1). Esa es la URL estable de la distribucion.
URL_SANLUIS = ("https://infra.datos.gob.ar/catalog/sspm/dataset/197/"
               "distribution/197.1/download/"
               "indice-precios-consumidor-san-luis-2003-100.csv")
ARCH_SANLUIS = "indice-precios-consumidor-san-luis-2003-100.csv"

# Mes en que las dos series se solapan y donde se calcula el coeficiente de
# empalme. Es el primer mes del IPC nacional del INDEC.
MES_EMPALME = (2016, 12)
# Primer mes de la serie deflactora. Antes de esto no hay dato fiscal en el repo.
MES_INICIO = (2010, 1)
# Base del deflactor.
BASE_DEFLACTOR = (2025, 12)

DEC0 = Decimal(0)


class ErrorDeFuente(Exception):
    pass


# --------------------------------------------------------------------------
# Descarga
# --------------------------------------------------------------------------

def _bajar(url, destino):
    import requests
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    with open(destino, "wb") as f:
        f.write(r.content)
    return len(r.content)


def descargar(sin_red=False):
    """Deja los dos CSV crudos en 01_raw/indec/ y escribe DESCARGA.txt."""
    os.makedirs(RAW_IPC, exist_ok=True)
    registro = []
    for url, nombre in ((URL_INDEC, ARCH_INDEC), (URL_SANLUIS, ARCH_SANLUIS)):
        destino = os.path.join(RAW_IPC, nombre)
        if sin_red:
            if not os.path.exists(destino):
                raise ErrorDeFuente("falta %s y se pidio --sin-red" % destino)
        else:
            _bajar(url, destino)
        crudo = open(destino, "rb").read()
        registro.append({
            "archivo": nombre,
            "url": url,
            "bytes": len(crudo),
            "md5": hashlib.md5(crudo).hexdigest(),
        })
    if not sin_red:
        hoy = dt.date.today().isoformat()
        with open(os.path.join(RAW_IPC, "DESCARGA.txt"), "w",
                  encoding="utf-8") as f:
            f.write("Descargas de indices de precios. Fecha: %s\n\n" % hoy)
            for r in registro:
                f.write("archivo : %s\n" % r["archivo"])
                f.write("url     : %s\n" % r["url"])
                f.write("bytes   : %d\n" % r["bytes"])
                f.write("md5     : %s\n\n" % r["md5"])
    return registro


# --------------------------------------------------------------------------
# Lectura de las dos series
# --------------------------------------------------------------------------

def leer_indec():
    """IPC nacional, nivel general, mensual. -> {(anio, mes): Decimal}"""
    ruta = os.path.join(RAW_IPC, ARCH_INDEC)
    serie = {}
    with open(ruta, encoding="latin-1", newline="") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            if fila["Codigo"].strip() != "0":
                continue
            if fila["Region"].strip() != "Nacional":
                continue
            periodo = fila["Periodo"].strip()
            indice = fila["Indice_IPC"].strip().replace(",", ".")
            if not indice or indice == "NA":
                continue
            clave = (int(periodo[:4]), int(periodo[4:6]))
            serie[clave] = Decimal(indice)
    if not serie:
        raise ErrorDeFuente("no se leyo ninguna fila nacional de %s" % ruta)
    if MES_EMPALME not in serie:
        raise ErrorDeFuente("falta %s en la serie del INDEC" % (MES_EMPALME,))
    return serie


def leer_sanluis():
    """IPC San Luis, nivel general, mensual. -> {(anio, mes): Decimal}"""
    ruta = os.path.join(RAW_IPC, ARCH_SANLUIS)
    serie = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            fecha = fila["indice_tiempo"].strip()
            valor = fila["nivel_general"].strip()
            if not fecha or not valor:
                continue
            serie[(int(fecha[:4]), int(fecha[5:7]))] = Decimal(valor)
    if not serie:
        raise ErrorDeFuente("no se leyo ninguna fila de %s" % ruta)
    if MES_EMPALME not in serie:
        raise ErrorDeFuente("falta %s en la serie de San Luis" % (MES_EMPALME,))
    return serie


# --------------------------------------------------------------------------
# Empalme
# --------------------------------------------------------------------------

def coeficiente_de_empalme(indec, sanluis):
    """
    El coeficiente unico que lleva la serie de San Luis a la base del INDEC.

        k = IPC_INDEC(dic-2016) / IPC_SanLuis(dic-2016)

    Se aplica a todos los meses de San Luis anteriores a dic-2016. Como es una
    multiplicacion por una constante, las variaciones mensuales del tramo
    2010-2016 son exactamente las de San Luis: el empalme no inventa inflacion,
    solo cambia la unidad de medida.
    """
    return indec[MES_EMPALME] / sanluis[MES_EMPALME]


def meses_entre(desde, hasta):
    a, m = desde
    while (a, m) <= hasta:
        yield (a, m)
        m += 1
        if m == 13:
            a, m = a + 1, 1


def serie_empalmada(indec, sanluis):
    """
    Indice mensual continuo desde 2010-01 hasta el ultimo mes del INDEC.
    Base diciembre 2016 = 100.

    Devuelve lista de dicts ordenada, con el origen de cada mes marcado.
    """
    k = coeficiente_de_empalme(indec, sanluis)
    ultimo = max(indec)
    filas = []
    anterior = None
    for clave in meses_entre(MES_INICIO, ultimo):
        anio, mes = clave
        if clave >= MES_EMPALME:
            if clave not in indec:
                raise ErrorDeFuente("hueco en la serie del INDEC: %s" % (clave,))
            indice = indec[clave]
            origen = "IPC INDEC nacional nivel general (base dic-2016=100)"
            fuente = ARCH_INDEC
        else:
            if clave not in sanluis:
                raise ErrorDeFuente("hueco en la serie de San Luis: %s" % (clave,))
            indice = sanluis[clave] * k
            origen = ("IPC San Luis nivel general, empalmado a la base del "
                      "INDEC (x %s)" % _fmt(k, 10))
            fuente = ARCH_SANLUIS
        # La variacion mensual sale de la serie de origen, no del indice
        # empalmado, para que el mes de empalme no invente un salto.
        previo = (anio, mes - 1) if mes > 1 else (anio - 1, 12)
        if clave > MES_EMPALME or (clave == MES_EMPALME and previo in indec):
            base_var = indec.get(previo)
        else:
            base_var = None
        if base_var is None and previo in sanluis and clave <= MES_EMPALME:
            base_var = sanluis[previo] * k
        var = None
        if base_var and base_var != DEC0:
            var = (indice / base_var - 1) * 100
        filas.append({
            "anio": anio,
            "mes": mes,
            "indice": indice,
            "variacion_mensual": var,
            "fuente": fuente,
            "serie_origen": origen,
        })
        anterior = indice
    return filas, k


# --------------------------------------------------------------------------
# Formato
# --------------------------------------------------------------------------

def _fmt(d, decimales):
    if d is None:
        return ""
    q = Decimal(1).scaleb(-decimales)
    return str(Decimal(d).quantize(q, rounding=ROUND_HALF_UP))


def escribir_ipc(filas):
    ruta = os.path.join(DATA, "ipc_indec_mensual.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "mes", "indice", "variacion_mensual", "fuente",
                    "serie_origen"])
        for x in filas:
            w.writerow([x["anio"], "%02d" % x["mes"], _fmt(x["indice"], 4),
                        _fmt(x["variacion_mensual"], 4), x["fuente"],
                        x["serie_origen"]])
    return ruta


def leer_ipc():
    """Vuelve a leer data/ipc_indec_mensual.csv. -> {(anio,mes): Decimal}"""
    ruta = os.path.join(DATA, "ipc_indec_mensual.csv")
    serie = {}
    origen = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            clave = (int(fila["anio"]), int(fila["mes"]))
            serie[clave] = Decimal(fila["indice"])
            origen[clave] = fila["serie_origen"]
    return serie, origen



# --------------------------------------------------------------------------
# El deflactor
# --------------------------------------------------------------------------
#
# Convencion: coeficiente = IPC(dic-2025) / IPC(periodo).
#   monto_constante_dic2025 = monto_nominal * coeficiente
# Diciembre 2025 se deflacta a si mismo: su coeficiente es exactamente 1.
#
# El coeficiente se PUBLICA redondeado a 8 decimales y es ese valor publicado
# el que se usa para multiplicar. Asi cualquiera reproduce el importe constante
# exacto tomando el CSV, sin tener que reconstruir la aritmetica interna.

DECIMALES_COEF = 8
DECIMALES_MONTO = 2

MESES_DIAS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _q(d, decimales):
    return Decimal(d).quantize(Decimal(1).scaleb(-decimales),
                               rounding=ROUND_HALF_UP)


def _dias_del_mes(anio, mes):
    if mes == 2 and (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)):
        return 29
    return MESES_DIAS[mes - 1]


def _parse_fecha(txt):
    """d/m/aaaa -> date. Es el formato que usan los CSV del repo."""
    d, m, a = [int(x) for x in txt.strip().split("/")]
    return dt.date(a, m, d)


def ipc_base(serie):
    if BASE_DEFLACTOR not in serie:
        raise ErrorDeFuente("la serie no llega a la base %s" % (BASE_DEFLACTOR,))
    return serie[BASE_DEFLACTOR]


def ipc_promedio_de_periodo(serie, desde, hasta):
    """
    Nivel de precios medio de un periodo, ponderado por dias.

    Cada dia del periodo aporta el indice de SU mes. Un informe acumulado de
    enero a diciembre pondera los doce meses; uno de un trimestre suelto, solo
    los tres meses del trimestre. Es asi como se respeta periodo_tipo: el
    coeficiente sale del rango de fechas real del informe, no de la etiqueta
    del trimestre. Un acumulado anual nunca se deflacta con un solo trimestre.

    Devuelve (promedio, detalle) donde detalle lista (anio, mes, dias).
    """
    if hasta < desde:
        raise ErrorDeFuente("periodo invertido: %s a %s" % (desde, hasta))
    total_dias = 0
    acumulado = DEC0
    detalle = []
    anio, mes = desde.year, desde.month
    while (anio, mes) <= (hasta.year, hasta.month):
        primero = dt.date(anio, mes, 1)
        ultimo = dt.date(anio, mes, _dias_del_mes(anio, mes))
        ini = max(primero, desde)
        fin = min(ultimo, hasta)
        dias = (fin - ini).days + 1
        if dias > 0:
            if (anio, mes) not in serie:
                raise ErrorDeFuente(
                    "el IPC no cubre %04d-%02d, necesario para el periodo "
                    "%s a %s" % (anio, mes, desde, hasta))
            acumulado += serie[(anio, mes)] * dias
            total_dias += dias
            detalle.append((anio, mes, dias))
        mes += 1
        if mes == 13:
            anio, mes = anio + 1, 1
    if total_dias == 0:
        raise ErrorDeFuente("periodo sin dias: %s a %s" % (desde, hasta))
    return acumulado / total_dias, detalle


def coef_de_periodo(serie, desde, hasta):
    promedio, detalle = ipc_promedio_de_periodo(serie, desde, hasta)
    return _q(ipc_base(serie) / promedio, DECIMALES_COEF), promedio, detalle


def coef_de_mes(serie, anio, mes):
    if (anio, mes) not in serie:
        raise ErrorDeFuente("el IPC no cubre %04d-%02d" % (anio, mes))
    return _q(ipc_base(serie) / serie[(anio, mes)], DECIMALES_COEF)


def construir_deflactor(serie, origen):
    """
    data/deflactor.csv: un coeficiente anual (promedio del anio) y uno a
    diciembre, para cada anio de la serie. Base diciembre 2025 = 100.
    """
    base = ipc_base(serie)
    anios = sorted({a for a, _ in serie})
    filas = []
    for anio in anios:
        meses = sorted(m for a, m in serie if a == anio)
        # Promedio anual ponderado por dias del mes, misma regla que los
        # periodos, para que un acumulado enero-diciembre y el coeficiente
        # anual den lo mismo.
        dias_tot = 0
        acum = DEC0
        for m in meses:
            d = _dias_del_mes(anio, m)
            acum += serie[(anio, m)] * d
            dias_tot += d
        prom = acum / dias_tot
        dic = serie.get((anio, 12))
        origenes = sorted({origen[(anio, m)].split(",")[0].split(" (")[0]
                           for m in meses})
        filas.append({
            "anio": anio,
            "meses_usados": len(meses),
            "cobertura": "completo" if len(meses) == 12 else "parcial",
            "ipc_promedio_anual": prom,
            "ipc_diciembre": dic,
            "coef_anual": _q(base / prom, DECIMALES_COEF),
            "coef_diciembre": _q(base / dic, DECIMALES_COEF) if dic else None,
            "serie_origen": " + ".join(origenes),
        })
    ruta = os.path.join(DATA, "deflactor.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "meses_usados", "cobertura", "ipc_promedio_anual",
                    "ipc_diciembre", "coef_anual", "coef_diciembre",
                    "base", "serie_origen"])
        for x in filas:
            w.writerow([
                x["anio"], x["meses_usados"], x["cobertura"],
                _fmt(x["ipc_promedio_anual"], 4), _fmt(x["ipc_diciembre"], 4),
                _fmt(x["coef_anual"], DECIMALES_COEF),
                _fmt(x["coef_diciembre"], DECIMALES_COEF),
                "diciembre 2025 = 100", x["serie_origen"]])
    return filas, ruta


# --------------------------------------------------------------------------
# Aplicacion a los datasets
# --------------------------------------------------------------------------
#
# A cada dataset se le agregan columnas nuevas y NO se pisa ninguna nominal:
#
#   coef_deflactor          el multiplicador usado en esa fila
#   base_coef               de que periodo salio el coeficiente, en texto
#   monto_constante_dic2025 la columna principal del dataset, ya deflactada
#   <col>_const_dic2025     lo mismo para cada otra columna de importes
#
# La columna principal de cada dataset esta en "principal" mas abajo: es la
# cifra que se lee cuando se lee una sola. El resto queda igual de disponible.

DATASETS = [
    {
        # Presupuesto votado para cada anio. Es un flujo planificado a lo largo
        # del ejercicio, asi que va con el coeficiente anual, igual que la
        # ejecucion. La columna "pagina" no es plata y no se toca.
        "ruta": "data/presupuesto_historico_2010_2026.csv",
        "modo": "anual",
        "principal": "monto",
        "col_anio": "anio",
        "montos": ["monto"],
    },
    {
        # Rendicion de cuentas anual. OJO: la columna "porcentaje" es un
        # porcentaje, no un importe. Deflactarla seria un disparate, asi que
        # no entra en "montos".
        "ruta": "data/rendiciones_2010_2021.csv",
        "modo": "anual",
        "principal": "monto",
        "col_anio": "anio",
        "montos": ["monto"],
    },
    {
        # Cruce de lo presupuestado contra lo ejecutado. Las tres columnas de
        # plata se deflactan; "diferencia_pct" es un porcentaje y queda afuera.
        "ruta": "data/presupuestado_vs_ejecutado.csv",
        "modo": "anual",
        "principal": "ejecutado",
        "col_anio": "anio",
        "montos": ["presupuestado", "ejecutado", "diferencia"],
    },
    {
        "ruta": "data/ejecucion_gastos_objeto.csv",
        "modo": "periodo",
        "principal": "devengado",
        "montos": ["credito_aprobado", "modificaciones", "credito_vigente",
                   "devengado", "pagado"],
    },
    {
        "ruta": "data/ejecucion_recursos.csv",
        "modo": "periodo",
        "principal": "percibido",
        "montos": ["calculado", "vigente", "devengado", "percibido"],
    },
    {
        "ruta": "data/gastos_finalidad_funcion.csv",
        "modo": "periodo",
        "principal": "devengado",
        "montos": ["credito_aprobado", "modificaciones", "credito_vigente",
                   "devengado", "pagado"],
    },
    {
        "ruta": "data/deuda_stock.csv",
        "modo": "stock",
        "principal": "saldo",
        "col_fecha": "fecha_corte",
        "montos": ["saldo", "amortiz_ej1", "intereses_ej1", "amortiz_ej2",
                   "intereses_ej2", "amortiz_ej3", "intereses_ej3",
                   "amortiz_resto", "intereses_resto",
                   "deuda_vencida_impaga"],
    },
    {
        "ruta": "SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv",
        "modo": "anual",
        "principal": "monto_pesos",
        "col_anio": "anio",
        "montos": ["monto_pesos"],
    },
    {
        # Copia byte a byte de la anterior que quedo en la raiz del repo. Se
        # deflacta tambien para que no haya dos versiones del mismo archivo.
        "ruta": "DATOS_SanIsidro_2014-2022.csv",
        "modo": "anual",
        "principal": "monto_pesos",
        "col_anio": "anio",
        "montos": ["monto_pesos"],
    },
    {
        # Transferencias de la Provincia, mensuales. Van con el coeficiente del
        # mes, que sale del rango de fechas de la propia fila (periodo_desde y
        # periodo_hasta son el primero y el ultimo dia del mes).
        "ruta": "02_clean/transferencias_pba_2021_2026.csv",
        "modo": "periodo",
        "principal": "monto",
        "montos": ["monto", "total_publicado_de_la_hoja"],
    },
]

SUFIJO = "_const_dic2025"
COL_PRINCIPAL = "monto_constante_dic2025"


def _num(txt):
    txt = (txt or "").strip()
    if not txt:
        return None
    return Decimal(txt)


def _detalle_txt(detalle):
    return " ".join("%04d-%02d:%dd" % x for x in detalle)


def aplicar(serie, spec, periodos_vistos):
    """Reescribe un dataset con las columnas constantes. Devuelve un resumen."""
    ruta = os.path.join(REPO, spec["ruta"])
    if not os.path.exists(ruta):
        return {"ruta": spec["ruta"], "estado": "no existe en el repo",
                "filas": 0, "deflactados": 0}

    # Algunos CSV arrancan con lineas de advertencia que empiezan con "#". Se
    # separan para poder leer la tabla, y se vuelven a escribir tal cual al
    # final: la advertencia no se puede perder al deflactar.
    with open(ruta, encoding="utf-8", newline="") as f:
        crudo = f.readlines()
    comentarios = []
    while crudo and crudo[0].startswith("#"):
        comentarios.append(crudo.pop(0))
    lector = csv.DictReader(crudo)
    cabecera = list(lector.fieldnames or [])
    filas = list(lector)

    montos = [c for c in spec.get("montos") or [] if c in cabecera]
    if not montos:
        return {"ruta": spec["ruta"],
                "estado": "sin columnas de importe reconocidas",
                "filas": len(filas), "deflactados": 0}
    principal = spec.get("principal")
    if principal not in montos:
        principal = montos[0]

    nuevas = ["coef_deflactor", "base_coef", COL_PRINCIPAL]
    nuevas += [c + SUFIJO for c in montos]
    salida = [c for c in cabecera if c not in nuevas] + nuevas

    deflactados = 0
    for fila in filas:
        if spec["modo"] == "periodo":
            desde = _parse_fecha(fila["periodo_desde"])
            hasta = _parse_fecha(fila["periodo_hasta"])
            coef, prom, detalle = coef_de_periodo(serie, desde, hasta)
            base = "%s a %s (%s) promedio ponderado por dias | %s" % (
                fila["periodo_desde"], fila["periodo_hasta"],
                fila.get("periodo_tipo", ""), _detalle_txt(detalle))
            periodos_vistos.setdefault(
                (fila["periodo_desde"], fila["periodo_hasta"],
                 fila.get("periodo_tipo", "")),
                (coef, prom, detalle))
        elif spec["modo"] == "stock":
            fecha = _parse_fecha(fila[spec["col_fecha"]])
            coef = coef_de_mes(serie, fecha.year, fecha.month)
            base = "stock al %s, indice de %04d-%02d" % (
                fila[spec["col_fecha"]], fecha.year, fecha.month)
        else:
            anio = int(fila[spec["col_anio"]])
            meses = sorted(m for a, m in serie if a == anio)
            if not meses:
                raise ErrorDeFuente("el IPC no cubre el anio %d" % anio)
            desde = dt.date(anio, meses[0], 1)
            hasta = dt.date(anio, meses[-1], _dias_del_mes(anio, meses[-1]))
            coef, prom, detalle = coef_de_periodo(serie, desde, hasta)
            base = "anual %d, promedio de %d meses ponderado por dias" % (
                anio, len(meses))

        fila["coef_deflactor"] = _fmt(coef, DECIMALES_COEF)
        fila["base_coef"] = base
        for col in montos:
            v = _num(fila.get(col))
            fila[col + SUFIJO] = ("" if v is None
                                  else _fmt(v * coef, DECIMALES_MONTO))
        fila[COL_PRINCIPAL] = fila[principal + SUFIJO]
        if fila[COL_PRINCIPAL]:
            deflactados += 1

    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.writelines(comentarios)
        w = csv.DictWriter(f, fieldnames=salida, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)

    return {"ruta": spec["ruta"], "estado": "deflactado",
            "filas": len(filas), "deflactados": deflactados,
            "principal": principal, "montos": montos}


def escribir_periodos(periodos_vistos):
    """
    data/deflactor_periodos.csv: un renglon por cada rango de fechas distinto
    que aparece en los informes trimestrales, con su coeficiente y los meses
    que lo componen. Es la tabla que hace auditable la eleccion de coeficiente
    para los acumulados.
    """
    ruta = os.path.join(DATA, "deflactor_periodos.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["periodo_desde", "periodo_hasta", "periodo_tipo",
                    "meses_cubiertos", "ipc_promedio_ponderado",
                    "coef_deflactor", "detalle_dias_por_mes", "base"])
        for clave in sorted(periodos_vistos,
                            key=lambda k: _parse_fecha(k[0])):
            coef, prom, detalle = periodos_vistos[clave]
            w.writerow([clave[0], clave[1], clave[2], len(detalle),
                        _fmt(prom, 4), _fmt(coef, DECIMALES_COEF),
                        _detalle_txt(detalle), "diciembre 2025 = 100"])
    return ruta


# --------------------------------------------------------------------------
# Serie real de gastos totales y deteccion de saltos
# --------------------------------------------------------------------------
#
# La serie se arma leyendo los CSV YA deflactados, no recalculando nada: cada
# valor de aca se puede ir a buscar a su fila en el dataset de origen.
#
# Los conceptos no son identicos en todos los anios y eso esta a la vista en la
# columna "concepto". Donde una rendicion publica mas de una cifra de gasto
# total se elige, en este orden:
#   1) "Gastos con imputacion al presupuesto" (el concepto del fallo del HTC),
#   2) la cifra del Tribunal de Cuentas por sobre la del propio Municipio,
#   3) para 2024 y 2025, la suma del devengado de los objetos del gasto del
#      informe acumulado anual, que es el mismo universo.
# Nada se promedia ni se corrige: se elige una fila publicada y se dice cual.

PREFERENCIA_CONCEPTO = [
    "Gastos con imputacion al presupuesto (HTC)",
    "Gastos con imputacion al presupuesto",
    "Gastos ejecutados (incluye aplicaciones financieras)",
]

UMBRAL_SALTO = Decimal("40")

# Esta serie mezcla conceptos y no sirve para comparar entre anios. La
# advertencia va dentro del archivo, no solo en la documentacion, porque el CSV
# viaja solo.
ADVERTENCIA_SERIE_HETEROGENEA = """\
# ADVERTENCIA. Esta serie MEZCLA CONCEPTOS DE GASTO distintos segun el anio,
# porque cada fuente publica el suyo. La columna concepto_heterogeneo dice cual
# es el de cada fila.
#
# LAS VARIACIONES INTERANUALES QUE CRUZAN UN CAMBIO DE CONCEPTO NO SON
# COMPARACIONES LIMPIAS. Comparar un anio de "gastos con imputacion al
# presupuesto" contra uno de "devengado por objeto" es comparar cosas que no
# miden lo mismo.
#
# Ademas el "total de gastos" de las rendiciones cambia de contenido a mitad de
# camino: en 2010-2012 INCLUYE las aplicaciones financieras y en 2019-2021 NO
# las incluye.
#
# Para comparar entre anios usar data/serie_gastos_comparable.csv, que tiene un
# solo concepto. Los pares que si se pueden comparar dentro de ESTA serie estan
# en data/COMPARACIONES_VALIDAS.md.
#
# Este archivo queda como material de trabajo, no para publicar.
"""


def _leer_csv(ruta):
    # Algunos CSV llevan una advertencia en lineas que arrancan con "#".
    with open(os.path.join(REPO, ruta), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def serie_gastos_totales():
    """
    Gasto total del Municipio por anio, en pesos de dic-2025.

    Hay tres fuentes distintas y no todas cubren los mismos anios. Cuando dos
    coinciden en un anio, gana la de MENOR rango de esta lista, y el rango
    queda escrito en la columna "prioridad_fuente" del CSV:

      1. Fallo del Tribunal de Cuentas o rendicion de cuentas, concepto
         "Gastos con imputacion al presupuesto" (DATOS_SanIsidro_2014-2022).
      2. Rendicion de cuentas parseada del PDF, fila total_gastos
         (rendiciones_2010_2021).
      3. Informe trimestral de ejecucion, acumulado anual: suma del devengado
         de los objetos del gasto (ejecucion_gastos_objeto).

    Nada se promedia ni se corrige: se elige una fila publicada y se dice cual.
    """
    candidatos = {}

    def proponer(anio, rango, dato):
        actual = candidatos.get(anio)
        if actual is None or rango < actual["prioridad_fuente"]:
            dato["prioridad_fuente"] = rango
            candidatos[anio] = dato

    # 1. Rendiciones y fallos del HTC, 2014-2022.
    datos = "SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv"
    if os.path.exists(os.path.join(REPO, datos)):
        por_anio = {}
        for fila in _leer_csv(datos):
            if fila.get("bloque") != "gastos_total":
                continue
            por_anio.setdefault(int(fila["anio"]), []).append(fila)
        for anio, filas in por_anio.items():
            def rango(f):
                c = f["concepto"]
                for n, pref in enumerate(PREFERENCIA_CONCEPTO):
                    if c.startswith(pref):
                        return n
                return len(PREFERENCIA_CONCEPTO)
            elegida = sorted(filas, key=rango)[0]
            proponer(anio, 1, {
                "anio": anio,
                "concepto": elegida["concepto"],
                "monto_nominal": Decimal(elegida["monto_pesos"]),
                "monto_constante_dic2025": Decimal(elegida[COL_PRINCIPAL]),
                "coef_deflactor": elegida["coef_deflactor"],
                "fuente": elegida["fuente"],
                "dataset": datos,
                "filas_sumadas": 1,
            })

    # 2. Rendiciones de cuentas parseadas de los PDF, 2010-2021.
    rend = "data/rendiciones_2010_2021.csv"
    if os.path.exists(os.path.join(REPO, rend)):
        for fila in _leer_csv(rend):
            if fila.get("concepto") != "total_gastos":
                continue
            if not fila.get("monto") or not fila.get(COL_PRINCIPAL):
                continue
            proponer(int(fila["anio"]), 2, {
                "anio": int(fila["anio"]),
                "concepto": "Total de gastos de la rendicion de cuentas%s" % (
                    " (%s)" % fila["subconcepto"] if fila.get("subconcepto")
                    else ""),
                "monto_nominal": Decimal(fila["monto"]),
                "monto_constante_dic2025": Decimal(fila[COL_PRINCIPAL]),
                "coef_deflactor": fila["coef_deflactor"],
                "fuente": fila["fuente"],
                "dataset": rend,
                "filas_sumadas": 1,
            })

    # 3. Ejecucion presupuestaria, informes acumulados anuales.
    eje = "data/ejecucion_gastos_objeto.csv"
    if os.path.exists(os.path.join(REPO, eje)):
        por_anio = {}
        for fila in _leer_csv(eje):
            if fila.get("periodo_tipo") != "acumulado_anual":
                continue
            if not fila.get("devengado"):
                continue
            por_anio.setdefault(int(fila["anio"]), []).append(fila)
        for anio, filas in por_anio.items():
            proponer(anio, 3, {
                "anio": anio,
                "concepto": ("Devengado, suma de los %d objetos del gasto del "
                             "informe acumulado anual" % len(filas)),
                "monto_nominal": sum(
                    (Decimal(f["devengado"]) for f in filas), DEC0),
                "monto_constante_dic2025": sum(
                    (Decimal(f[COL_PRINCIPAL]) for f in filas), DEC0),
                "coef_deflactor": filas[0]["coef_deflactor"],
                "fuente": filas[0]["fuente"],
                "dataset": eje,
                "filas_sumadas": len(filas),
            })

    return [candidatos[a] for a in sorted(candidatos)]


def escribir_serie_y_saltos(serie):
    anteriores = None
    for p in serie:
        if anteriores is None:
            p["brecha_anios"] = ""
            p["var_real_pct"] = None
        else:
            p["brecha_anios"] = p["anio"] - anteriores["anio"]
            base = anteriores["monto_constante_dic2025"]
            p["var_real_pct"] = ((p["monto_constante_dic2025"] / base - 1) * 100
                                 if base else None)
            p["anio_anterior"] = anteriores["anio"]
        anteriores = p

    ruta_serie = os.path.join(DATA, "serie_gastos_totales_real.csv")
    cols = ["anio", "concepto_heterogeneo", "monto_nominal", "coef_deflactor",
            "monto_constante_dic2025", "var_real_pct", "brecha_anios",
            "filas_sumadas", "prioridad_fuente", "dataset", "fuente"]
    with open(ruta_serie, "w", encoding="utf-8", newline="") as f:
        # La advertencia la escribe el propio generador, para que el archivo
        # nunca exista sin ella.
        f.write(ADVERTENCIA_SERIE_HETEROGENEA)
        w = csv.writer(f)
        w.writerow(cols)
        for p in serie:
            w.writerow([p["anio"], p["concepto"],  # concepto_heterogeneo
                        _fmt(p["monto_nominal"], 2), p["coef_deflactor"],
                        _fmt(p["monto_constante_dic2025"], 2),
                        _fmt(p["var_real_pct"], 2), p["brecha_anios"],
                        p["filas_sumadas"], p["prioridad_fuente"],
                        p["dataset"], p["fuente"]])

    saltos = [p for p in serie
              if p.get("var_real_pct") is not None
              and abs(p["var_real_pct"]) > UMBRAL_SALTO]
    ruta_saltos = os.path.join(DATA, "SALTOS_REALES.csv")
    with open(ruta_saltos, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "anio_anterior", "brecha_anios", "var_real_pct",
                    "monto_constante_dic2025", "monto_constante_anterior",
                    "concepto", "concepto_anterior", "comparacion", "motivo"])
        por_anio = {p["anio"]: p for p in serie}
        for p in saltos:
            prev = por_anio[p["anio_anterior"]]
            comp = ("adyacente" if p["brecha_anios"] == 1
                    else "no adyacente (%d anios de hueco)" % (
                        p["brecha_anios"] - 1))
            motivos = ["variacion real de %s%% supera el umbral de %s%%" % (
                _fmt(p["var_real_pct"], 2), UMBRAL_SALTO)]
            if p["brecha_anios"] != 1:
                motivos.append("los anios no son consecutivos: la variacion "
                               "acumula %d anios" % p["brecha_anios"])
            if p["concepto"] != prev["concepto"]:
                motivos.append("el concepto de gasto total cambia entre los "
                               "dos anios")
            if p["dataset"] != prev["dataset"]:
                motivos.append("los dos anios salen de datasets distintos")
            w.writerow([p["anio"], p["anio_anterior"], p["brecha_anios"],
                        _fmt(p["var_real_pct"], 2),
                        _fmt(p["monto_constante_dic2025"], 2),
                        _fmt(prev["monto_constante_dic2025"], 2),
                        p["concepto"], prev["concepto"], comp,
                        "; ".join(motivos)])
    return ruta_serie, ruta_saltos, saltos


def construir_todo(sin_red=False):
    descargar(sin_red=sin_red)
    indec = leer_indec()
    sanluis = leer_sanluis()
    filas, k = serie_empalmada(indec, sanluis)
    escribir_ipc(filas)

    serie, origen = leer_ipc()
    deflactor, _ = construir_deflactor(serie, origen)

    periodos = {}
    resumenes = [aplicar(serie, spec, periodos) for spec in DATASETS]
    escribir_periodos(periodos)

    gastos = serie_gastos_totales()
    _, _, saltos = escribir_serie_y_saltos(gastos)
    return {"ipc": filas, "k": k, "deflactor": deflactor,
            "resumenes": resumenes, "saltos": saltos, "gastos": gastos}


if __name__ == "__main__":
    r = construir_todo(sin_red="--sin-red" in sys.argv)
    f = r["ipc"]
    print("IPC mensual empalmado : %d meses, %d-%02d a %d-%02d" % (
        len(f), f[0]["anio"], f[0]["mes"], f[-1]["anio"], f[-1]["mes"]))
    print("coeficiente de empalme: %s  (= IPC_INDEC dic-2016 / "
          "IPC_SanLuis dic-2016)" % _fmt(r["k"], 10))
    print("deflactor             : %d anios, base diciembre 2025 = 100"
          % len(r["deflactor"]))
    print()
    print("DATASETS")
    for x in r["resumenes"]:
        print("  %-58s %s" % (x["ruta"], x["estado"]), end="")
        if x["estado"] == "deflactado":
            print("  (%d filas, %d importes principales)"
                  % (x["filas"], x["deflactados"]))
        else:
            print()
    print()
    print("serie real de gastos totales: %d anios" % len(r["gastos"]))
    print("saltos reales >40%%          : %d -> data/SALTOS_REALES.csv"
          % len(r["saltos"]))
