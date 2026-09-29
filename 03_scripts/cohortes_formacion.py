#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cohortes de la formacion laboral (5.3), mes por mes, con uno o con dos
ingresos por anio (correcciones 176 y 178).

Reproduce las cohortes que el documento ya usa (277, 494, 711 y 928) y calcula
el esquema de dos ingresos: cuantos egresan dentro del mandato, cuantos cursan,
cuantos estan de pasantes en el Municipio y cuantos en empresas, mes a mes.

Supuestos, todos del documento:
- El programa de empleo y vivienda arranca en 505,7 M y suma 7.225,2 M nuevos
  con la rampa 25/50/75/100% (anio 1 = meses 1 a 12 del mandato = 2028).
- Formacion = 60% de empleo, y empleo = 60% del programa: 0,36 del programa.
- 3 M por persona pagan los dos anios de formacion: la cohorte de cada anio es
  lo que ese anio destina a formacion dividido por 3 M (asi salen 277, 494,
  711 y 928; el documento redondea al entero mas cercano).
- La primera cohorte arranca en el mes 3 (cien dias). Cursada de 12 meses y
  pasantia de 12: se egresa 24 meses despues de entrar.
- Correccion 176: la pasantia se parte en dos, 6 meses en el Municipio y 6 en
  una empresa del partido, una contratista o una startup del semillero.
- Correccion 178: dos ingresos por anio, en los meses 3 y 9 de cada anio; en
  cada uno entra la mitad de la cohorte anual.
- Decision de Nick (29/09): los dos primeros anios la formacion usa toda la
  partida de empleo (no hay egresados que contratar todavia); desde el tercero
  vuelve el 60/40. Asi entran 462 y 824 en vez de 277 y 494, y egresan 1.286 en
  el mandato. Es el esquema "decidido"; "anual" y "semestral" quedan para
  comparar.
El mandato son 48 meses.

Uso: python3 03_scripts/cohortes_formacion.py [--csv data/cohortes_formacion.csv]
"""
import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP

BASE = Decimal("505.7")            # empleo + vivienda hoy, M de dic-2025
NUEVO = Decimal("7225.2")          # fondos nuevos en regimen
PARTE_FORMACION = Decimal("0.36")  # 60% de empleo x 60% de formacion
COSTO_PERSONA = Decimal("3")       # M por persona, los dos anios
ANIOS_RAMPA = 4
MANDATO = 48                       # meses
MES_PRIMER_INGRESO = 3
CURSADA = 12
MUNICIPIO = 6
EMPRESA = 6
DURACION = CURSADA + MUNICIPIO + EMPRESA
TOPE_MUNICIPIO = 556               # 7% de 7.946 cargos (F6, Ordenanza 9422)


def entero(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def cohorte_anual(k):
    """Personas que entran en el anio k del programa (k = 1, 2, ...)."""
    paso = Decimal(min(k, ANIOS_RAMPA)) / Decimal(ANIOS_RAMPA)
    programa = BASE + NUEVO * paso
    return programa * PARTE_FORMACION / COSTO_PERSONA


def cohorte_decidida(k):
    """Anios 1 y 2: toda la partida de empleo va a formacion. Desde el 3, 60/40."""
    if k > 2:
        return cohorte_anual(k)
    paso = Decimal(min(k, ANIOS_RAMPA)) / Decimal(ANIOS_RAMPA)
    empleo = (BASE + NUEVO * paso) * Decimal("0.6")
    return empleo / COSTO_PERSONA


def ingresos(esquema, anios=8):
    """Lista de (mes de ingreso, personas)."""
    out = []
    for k in range(1, anios + 1):
        anual = entero(cohorte_decidida(k) if esquema == "decidido" else cohorte_anual(k))
        m0 = 12 * (k - 1) + MES_PRIMER_INGRESO
        if esquema == "anual":
            out.append((m0, anual))
        else:
            # la mitad en cada semestre; si es impar, el segundo lleva uno mas
            a = anual // 2
            out.append((m0, a))
            out.append((m0 + 6, anual - a))
    return out


def estado(ings, mes, partida=True):
    """Cuantos cursan, cuantos son pasantes en el Municipio y en empresas, y
    cuantos egresaron hasta el mes dado (inclusive)."""
    c = mun = emp = eg = 0
    for m0, n in ings:
        t = mes - m0
        if t < 0:
            continue
        if t < CURSADA:
            c += n
        elif t < DURACION:
            if partida:
                if t < CURSADA + MUNICIPIO:
                    mun += n
                else:
                    emp += n
            else:
                mun += n  # pasantia de 12 meses: se reparte despues
        else:
            eg += n
    return c, mun, emp, eg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=None)
    a = ap.parse_args()

    print("Cohortes anuales de la rampa (M de formacion / 3 M por persona):")
    for k in range(1, 5):
        v = cohorte_anual(k)
        print(f"  anio {k}: {v:.2f} -> {entero(v)}")

    for esquema in ("anual", "semestral", "decidido"):
        ings = ingresos(esquema)
        eg_mandato = sum(n for m0, n in ings if m0 + DURACION <= MANDATO)
        print(f"\nEsquema {esquema}:")
        print("  ingresos (mes, personas):", [x for x in ings if x[0] <= MANDATO])
        print("  egresos en el mandato (mes, personas):",
              [(m0 + DURACION, n) for m0, n in ings if m0 + DURACION <= MANDATO])
        print(f"  EGRESAN EN EL MANDATO: {eg_mandato}")
        en_curso = sum(n for m0, n in ings if m0 <= MANDATO < m0 + DURACION)
        print(f"  al terminar el mandato siguen en formacion o pasantia: {en_curso}")

    ings = ingresos("decidido", anios=10)
    print("\nDecidido (dos ingresos, pasantia partida, formacion con toda la partida de "
          "empleo los anios 1 y 2): quienes estan en cada tramo, por mes")
    print("  mes  cursan  Municipio  empresas  egresados")
    filas = []
    max_mun_mandato = max_emp_mandato = 0
    for mes in range(1, 73):
        c, mun, emp, eg = estado(ings, mes)
        filas.append(dict(mes=mes, cursan=c, pasantes_municipio=mun,
                          pasantes_empresas=emp, egresados_acumulados=eg))
        if mes <= MANDATO:
            max_mun_mandato = max(max_mun_mandato, mun)
            max_emp_mandato = max(max_emp_mandato, emp)
        if mes in (3, 9, 15, 21, 27, 33, 39, 45, 48, 51, 57, 63):
            print(f"  {mes:>3}  {c:>6}  {mun:>9}  {emp:>8}  {eg:>9}")
    c, mun, emp, eg = estado(ings, 72)
    print(f"\n  en regimen (mes 72): cursan {c}, Municipio {mun}, empresas {emp}")
    print(f"  maximo en el Municipio dentro del mandato: {max_mun_mandato}"
          f" (margen contra el tope: {TOPE_MUNICIPIO - max_mun_mandato})")
    print(f"  maximo en empresas dentro del mandato: {max_emp_mandato}")
    print(f"  margen del tope en regimen: {TOPE_MUNICIPIO} - {mun} = {TOPE_MUNICIPIO - mun}")

    # con un ingreso por anio y la pasantia partida, el Municipio tendria a la
    # cohorte entera junta seis meses: se pasa del tope
    ings_a = ingresos("anual", anios=10)
    pico = max(estado(ings_a, m)[1] for m in range(1, 73))
    print(f"\n  con UN ingreso por anio y la pasantia partida, el Municipio tendria"
          f" hasta {pico} a la vez (tope {TOPE_MUNICIPIO})")

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            f.write("# Formacion laboral: dos ingresos por anio, pasantia partida y formacion con toda la\n")
            f.write("# partida de empleo en los anios 1 y 2 (esquema decidido el 29/09/2026).\n")
            f.write("# (6 meses en el Municipio y 6 en empresas). Generado por\n")
            f.write("# 03_scripts/cohortes_formacion.py. Mes 1 = primer mes del mandato.\n")
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
        print(f"\n-> {a.csv}")


if __name__ == "__main__":
    main()
