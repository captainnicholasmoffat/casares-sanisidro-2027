#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recalcula las siete cifras que se contradecian entre capitulos.

No toca ningun capitulo ni ningun dataset: lee data/ y 01_raw/ y escribe por
pantalla el valor correcto de cada una con su cuenta, para que
CORRECCIONES_NUMERICAS.md no tenga ni un numero escrito a mano.

Uso:
    python3 03_scripts/correcciones_numericas.py
"""

import os
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estilo as E

M = D("1000000")


def m(x, dec=1):
    """Millones, a la castellana."""
    return E.numero(D(x) / M, dec)


def titulo(n, texto):
    print()
    print("=" * 78)
    print("%d. %s" % (n, texto))
    print("=" * 78)


# --------------------------------------------------------------------------
# Recursos 2025
# --------------------------------------------------------------------------

def recursos(anio, prefijos):
    """Devengado y percibido de los rubros que empiezan con esos prefijos."""
    dev = per = D(0)
    for r in E.leer("data/ejecucion_recursos.csv"):
        if r["anio"] != str(anio) or r["periodo_tipo"] != "acumulado_anual":
            continue
        if not any(r["rubro_codigo"].startswith(p) for p in prefijos):
            continue
        dev += D(r["devengado"] or 0)
        per += D(r["percibido"] or 0)
    return dev, per


def uno():
    titulo(1, "PERCEPCION 2025: cual de las dos bases")
    d1, p1 = recursos(2025, ("1.",))
    dt, pt = recursos(2025, ("1.", "2.", "3."))
    print("  A) solo rubro 1, RECURSOS CORRIENTES")
    print("     devengado %s M   percibido %s M   ->  %s%%"
          % (m(d1), m(p1), E.numero(100 * p1 / d1, 4)))
    print("  B) rubros 1+2+3, RECURSOS TOTALES")
    print("     devengado %s M   percibido %s M   ->  %s%%"
          % (m(dt), m(pt), E.numero(100 * pt / dt, 4)))
    print()
    for r in E.leer("data/ejecucion_recursos.csv"):
        if r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual" \
                and not r["rubro_codigo"].startswith("1."):
            print("  la diferencia es el rubro %s %s: dev %s M = per %s M"
                  % (r["rubro_codigo"], r["rubro"],
                     m(r["devengado"] or 0), m(r["percibido"] or 0)))
    print()
    print("  Se cobra entero, por eso las dos dan el mismo sin-cobrar: %s M"
          % m(d1 - p1))
    sef = {r["clave"]: D(r["monto"]) for r in E.leer("data/baseline_2025.csv")}
    print("  El SEF, cuenta Ahorro-Inversion:")
    print("     I  ingresos corrientes (percibido) %s M  = base A" % m(sef["ingresos_corrientes"]))
    print("     VI ingresos totales               %s M  = base B" % m(sef["ingresos_totales"]))
    return d1, p1


def dos(d25, p25):
    titulo(2, "VOLVER A COBRAR COMO 2024")
    d24, p24 = recursos(2024, ("1.",))
    t24 = p24 / d24
    print("  tasa 2024 = %s / %s = %s%%"
          % (m(p24), m(d24), E.numero(100 * t24, 4)))
    print("  %s%% x %s M devengados 2025 = %s M"
          % (E.numero(100 * t24, 4), m(d25), m(t24 * d25)))
    print("  menos el percibido real   - %s M" % m(p25))
    print("  APORTE                    = %s M" % m(t24 * d25 - p25, 1))
    # De donde salian las otras dos cifras
    dtB, ptB = recursos(2025, ("1.", "2.", "3."))
    d24B, p24B = recursos(2024, ("1.", "2.", "3."))
    print()
    print("  [el 13.984 M de los capitulos sale de la base B: %s M]"
          % m(p24B / d24B * dtB - ptB))
    return t24


def tres(d25, p25):
    titulo(3, "LLEVAR LA PERCEPCION AL 92%")
    print("  0,92 x %s M = %s M" % (m(d25), m(D("0.92") * d25)))
    print("  menos el percibido real - %s M" % m(p25))
    print("  APORTE                  = %s M" % m(D("0.92") * d25 - p25))
    dtB, ptB = recursos(2025, ("1.", "2.", "3."))
    print()
    print("  [el 8.860 M sale de la base B: %s M]" % m(D("0.92") * dtB - ptB))
    print("  [el 9.036 M sale de redondear la tasa base a 89,32 antes de restar:")
    print("   (0,92 - 0,8932) x %s M = %s M]"
          % (m(d25), m((D("0.92") - D("0.8932")) * d25)))
    print("   la tasa real es %s%%, no 89,32%%. La diferencia son %s M."
          % (E.numero(100 * p25 / d25, 6),
             m((D("0.92") - D("0.8932")) * d25 - (D("0.92") * d25 - p25))))


def cuatro():
    titulo(4, "DE DONDE SALEN LOS 7.225 M DE EMPLEO Y VIVIENDA")
    b = {r["clave"]: D(r["monto"]) for r in E.leer("data/baseline_2025.csv")}
    gtot = b["gastos_corrientes"] + b["gastos_de_capital"]
    base = b["gasto_empleo"] + b["gasto_vivienda"]
    objetivo = gtot * D("0.025")
    nueva = objetivo - base
    print("  El modelo fija la meta como 2,5%% del gasto total, no como un")
    print("  multiplo de la base. 03_scripts/modelo.py, OBJETIVO_MEDIO = 0.025.")
    print()
    print("  gasto total 2025 (corrientes + capital)   %s M" % m(gtot))
    print("  x 2,5%%  = PROGRAMA COMPLETO en regimen    %s M" % m(objetivo))
    print("  empleo %s M + vivienda %s M    =      %s M   (lo de hoy)"
          % (m(b["gasto_empleo"]), m(b["gasto_vivienda"]), m(base)))
    print("  PLATA NUEVA = completo - lo de hoy        %s M" % m(nueva))
    print()
    print("  El 7.225 M es la PLATA NUEVA, no el programa completo.")
    print("  completo / base = %s x   <- este es el 'por quince'"
          % E.numero(objetivo / base, 2))
    print("  nueva    / base = %s x" % E.numero(nueva / base, 2))
    print("  505 x 15 = 7.575 M no da 7.225 M porque 7.225 M no es el total.")
    flex = D(0)
    for r in E.leer("data/ejecucion_gastos_objeto.csv"):
        if (r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual"
                and r["objeto_codigo"] in ("2", "4", "5", "6") and r["devengado"]):
            flex += D(r["devengado"])
    print()
    print("  gasto flexible 2025 %s M" % m(flex))
    print("  plata nueva / flexible      = %s%%   <- el 8,3%% del cap. 3 §3.8"
          % E.numero(100 * nueva / flex, 2))
    print("  programa completo / flexible = %s%%" % E.numero(100 * objetivo / flex, 2))
    print()
    print("  Se cruza contra data/financiamiento_opciones.csv, columna")
    print("  costo_del_programa del anio 4 (2029): %s"
          % [r["costo_del_programa"] for r in E.leer("data/financiamiento_opciones.csv")
             if r["opcion"] == "i_reasignacion" and r["anio"] == "2029"][0])


# --------------------------------------------------------------------------
# Censo
# --------------------------------------------------------------------------

# Cada indicador tiene su propio universo en el Censo y no el total de hogares
# de la zona: por eso combinar dos zonas se hace sumando numerador y
# denominador radio por radio, y no promediando dos porcentajes.
INDICADORES = [
    ("pct_nbi", ["hogares_nbi__si"], "hogares_nbi__total", "hogares"),
    ("pct_sin_cloaca",
     ["hogares_desague__a_camara_septica_y_pozo_ciego",
      "hogares_desague__solo_a_pozo_ciego",
      "hogares_desague__a_hoyo_excavacion_en_la_tierra_etc"],
     "hogares_desague__total", "hogares"),
    ("pct_sin_gas_red",
     ["hogares_combustible__electricidad",
      "hogares_combustible__gas_en_garrafa",
      "hogares_combustible__gas_en_tubo_o_a_granel_zeppelin",
      "hogares_combustible__lena_o_carbon",
      "hogares_combustible__otro_combustible"],
     "hogares_combustible__total", "hogares"),
    ("pct_hacinamiento",
     ["hogares_hacinamiento__2_00_3_00_personas_por_cuarto",
      "hogares_hacinamiento__mas_de_3_00_personas_por_cuarto"],
     "hogares_hacinamiento__total", "hogares"),
    ("pct_edu_universitaria_completa_o_mas",
     ["educacion_mni__universitario_completo",
      "educacion_mni__posgrado_incompleto",
      "educacion_mni__posgrado_completo"],
     "educacion_mni__total", "personas"),
]


def _censo_por_zona():
    censo = {r["radio_id"]: r
             for r in E.leer("data/censo2022_sanisidro_por_radio.csv")}
    zona = {r["radio_id"]: r["zona"]
            for r in E.leer("data/zonas_asignacion_radios.csv")}
    acum = {}
    for rid, z in zona.items():
        f = censo.get(rid)
        if not f:
            continue
        d = acum.setdefault(z, {})
        for col in set(sum([n for _, n, _, _ in INDICADORES], [])
                       + [den for _, _, den, _ in INDICADORES]):
            d[col] = d.get(col, 0) + int(float(f.get(col) or 0))
    return acum


def _pct(d, nums, den):
    t = d.get(den, 0)
    return (D(sum(d.get(c, 0) for c in nums)) * 100 / D(t)) if t else None


def cinco(acum):
    titulo(5, "HACINAMIENTO POR ZONA (2 o mas personas por cuarto)")
    orden = [z["zona"] for z in E.zonas_ordenadas()]
    publicado = {z["zona"]: z["pct_hacinamiento"] for z in E.zonas_ordenadas()}
    nums = dict((c, (n, den)) for c, n, den, _ in INDICADORES)
    n, den = nums["pct_hacinamiento"]
    print("  %-18s %10s %10s %10s   %s"
          % ("zona", "hogares", "con hac.", "%", "publicado"))
    for z in orden:
        d = acum[z]
        print("  %-18s %10s %10s %10s   %s"
              % (E.zona_bonita(z), E.numero(d[den]),
                 E.numero(sum(d[c] for c in n)),
                 E.numero(_pct(d, n, den), 2), publicado[z]))


def seis(acum):
    titulo(6, "BOULOGNE + BECCAR, LAS DOS ZONAS JUNTAS")
    dos_zonas = ["Boulogne Sur Mer", "Beccar"]
    comb = {}
    for z in dos_zonas:
        for k, v in acum[z].items():
            comb[k] = comb.get(k, 0) + v
    pub = {z["zona"]: z for z in E.zonas_ordenadas()}
    print("  %-40s %9s %9s %9s" % ("indicador", "Boulogne", "Beccar", "JUNTAS"))
    for col, n, den, unidad in INDICADORES:
        print("  %-40s %9s %9s %9s"
              % (col, pub[dos_zonas[0]][col], pub[dos_zonas[1]][col],
                 E.numero(_pct(comb, n, den), 2)))
        print("  %-40s %9s %9s %9s"
              % ("   universo (%s)" % unidad,
                 E.numero(acum[dos_zonas[0]][den]),
                 E.numero(acum[dos_zonas[1]][den]), E.numero(comb[den])))
    sin_gas_cols = [c for c, n, d, _ in INDICADORES if c == "pct_sin_gas_red"]
    n = [x for c, x, _, _ in INDICADORES if c == "pct_sin_gas_red"][0]
    print()
    print("  HOGARES SIN GAS DE RED, en numero:")
    for z in dos_zonas:
        print("     %-18s %s" % (E.zona_bonita(z),
                                 E.numero(sum(acum[z][c] for c in n))))
    dos_total = sum(comb[c] for c in n)
    partido = sum(sum(d[c] for c in n) for d in acum.values())
    print("     %-18s %s" % ("LAS DOS JUNTAS", E.numero(dos_total)))
    print("     %-18s %s   -> las dos son el %s%% del partido"
          % ("TODO EL PARTIDO", E.numero(partido),
             E.numero(D(dos_total) * 100 / D(partido), 1)))
    print()
    print("     El EXHIBIT 20 titula 25.166: sale de multiplicar los hogares de")
    print("     cada zona por su porcentaje publicado a dos decimales. Contando")
    print("     hogar por hogar en los 360 radios da %s." % E.numero(partido))


def siete():
    titulo(7, "LOS DOS TOTALES DE GASTO 2025")
    obj = {}
    for r in E.leer("data/ejecucion_gastos_objeto.csv"):
        if (r["anio"] == "2025" and r["periodo_tipo"] == "acumulado_anual"
                and r["devengado"]):
            obj[r["objeto_codigo"]] = (r["objeto"], D(r["devengado"]))
    total = sum(v for _, v in obj.values())
    financieros = obj["6"][1] + obj["7"][1]
    print("  Los 7 objetos del gasto devengado 2025, NOMINALES:")
    for c in sorted(obj):
        print("     %s  %-52s %s M" % (c, obj[c][0][:52], m(obj[c][1])))
    print("     %s M  <- 324.304 M, el total POR OBJETO, con los financieros"
          % m(total))
    print("   - %s M  activos financieros + servicio de la deuda" % m(financieros))
    print("   = %s M  <- gasto corriente + de capital, nominal (AIF VII)"
          % m(total - financieros))
    fila = [r for r in E.leer("data/serie_gastos_comparable.csv")
            if r["anio"] == "2025"][0]
    coef = [r["coef_anual"] for r in E.leer("data/deflactor.csv")
            if r["anio"] == "2025"][0]
    print()
    print("   x %s  coeficiente anual del deflactor 2025" % coef)
    print("   = %s M  <- 348.876 M, ese mismo gasto en PESOS DE DIC-2025"
          % m(fila["monto_constante_dic2025"]))
    print()
    print("  O sea que los dos numeros difieren en DOS cosas a la vez:")
    print("  el concepto (con o sin los financieros) y la unidad (nominal o")
    print("  constante). Comparados de a uno por vez no se contradicen.")


def main():
    d25, p25 = uno()
    dos(d25, p25)
    tres(d25, p25)
    cuatro()
    acum = _censo_por_zona()
    cinco(acum)
    seis(acum)
    siete()
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
