#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correccion 176: la pasantia de doce meses, partida en dos (seis meses en el
Municipio y seis en una empresa del partido). Calcula los lugares en proyectos
que faltan, los supervisores, lo que paga cada area y lo que ocupa el gasto
flexible (3.4). No toca el documento: imprime las cifras para decidir.

Fuentes de cada supuesto:
- Cargos por jurisdiccion y programa: Formulario F6 del presupuesto 2026
  (Ordenanza 9422), leidos pagina por pagina; suman 7.946 en el Departamento
  Ejecutivo (data/f6_cargos_2026.csv).
- Tope del Municipio: 7% de la planta financiada (Res. Conj. 825/2009 y
  338/2009, art. 14): 556.
- Regla del cuadro de proyectos del 5.3: un equipo de automatizacion cada 200
  cargos del area, equipos de diez pasantes y un supervisor.
- Pasante: 240.000 $ por mes, con salud (6%) y ART; 3,1663 M por anio, la cifra
  con que el 5.3 y el 3.4 ya calculan (1.013,2 M por 320 pasantes de las areas).
- Juniors de las areas: 720 M por anio (5.3). Gasto flexible: 87.326 M (3.4).
"""
import csv
import pathlib
from decimal import Decimal as D, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parent.parent
F6 = ROOT / "data" / "f6_cargos_2026.csv"

PASANTES_A_LA_VEZ = 464          # 928 por anio, seis meses cada uno
TOPE = 556
PLATAFORMA = 17                  # 15 de la plataforma y 2 de dispositivos (4.11)
COSTO_PASANTE = (D("1013.2") / 320)
JUNIORS_AREAS = D("720")
FLEXIBLE = D("87326")
NUEVOS, REASIGNACION, OBRA_VECINAL = D("7225.2"), D("7799"), D("28908")
AREAS_HOY = D("1733.2")

# Cuadro de proyectos de hoy (337): area -> (automatizacion, relevamiento)
HOY = {"Salud": (17, 1), "Seguridad": (3, 1), "Educacion": (3, 1),
       "Obra": (1, 2), "Habilitaciones": (1, 1), "Comunicacion": (0, 1)}

# Propuesta: 13 equipos nuevos, en proyectos que el documento ya propone.
NUEVOS_EQUIPOS = [
    ("Hacienda y recaudacion", 1, 1,
     "automatizar liquidacion y cobranza; relevar y cargar cada gasto con su zona (meta del 6.3)"),
    ("Ambiente y espacio publico", 2, 1,
     "automatizar la programacion de barrido y poda y los reclamos; medir el servicio de "
     "recoleccion zona por zona (5.5)"),
    ("Movilidad", 1, 1,
     "automatizar licencias de conducir; medir el ruido con sensores donde esta el problema (5.11)"),
    ("Desarrollo social, ninez, mujer y personas mayores", 1, 1,
     "automatizar la gestion; relevar hogar por hogar a los mayores que no pueden salir (5.13)"),
    ("Gobierno", 0, 1, "reponer el padron de asociaciones vecinales (6.4, meses 4 a 6)"),
    ("Legal y tecnica", 1, 0, "el digesto de ordenanzas y decretos, consultable"),
    ("Jefatura de gabinete", 1, 0,
     "la planta de personal y la escala salarial, consultables (5.12)"),
    ("Cultura", 0, 1, "los espacios culturales y lo que traba su habilitacion (5.8)"),
]


def q(x, n=1):
    return D(x).quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)


def cargos_por_jurisdiccion():
    tot = {}
    with open(F6, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("poder", "Departamento Ejecutivo") and "CONCEJO" in r["jurisdiccion_nombre"]:
                continue
            tot[r["jurisdiccion_nombre"]] = tot.get(r["jurisdiccion_nombre"], 0) + int(r["cargos_subtotal"])
    return tot


def main():
    if F6.exists():
        tot = cargos_por_jurisdiccion()
        print(f"F6: {sum(tot.values())} cargos del Departamento Ejecutivo en {len(tot)} jurisdicciones")
        print(f"tope del Municipio: 7% de {sum(tot.values())} = {sum(tot.values()) * 7 // 100}")
    hoy = sum(10 * (a + r) for a, r in HOY.values()) + PLATAFORMA
    faltan = PASANTES_A_LA_VEZ - hoy
    print(f"\nlugares en proyectos hoy: {hoy}; hacen falta {PASANTES_A_LA_VEZ}; faltan {faltan}")
    nuevos = 0
    for area, a, r, que in NUEVOS_EQUIPOS:
        nuevos += 10 * (a + r)
        print(f"  + {10 * (a + r):>3}  {area}: {que}")
    lugares = hoy + nuevos
    print(f"equipos nuevos: {nuevos // 10}, lugares nuevos: {nuevos}; total {lugares} "
          f"para {PASANTES_A_LA_VEZ} pasantes (margen {lugares - PASANTES_A_LA_VEZ})")
    print(f"tope {TOPE}: sobran {TOPE - PASANTES_A_LA_VEZ} lugares legales")

    sup_hoy = sum(a + r for a, r in HOY.values())
    sup = sup_hoy + nuevos // 10
    print(f"\nsupervisores de planta reasignada: {sup_hoy} -> {sup}; "
          f"planta reasignada total: {sup_hoy + 32} -> {sup + 32} (26 de noche y fin de semana, 6 por zona)")
    print(f"supervisores en el Municipio con los 3 seniors de la plataforma: {sup + 3}; "
          f"en empresas: {-(-PASANTES_A_LA_VEZ // 10)}; total {sup + 3 + -(-PASANTES_A_LA_VEZ // 10)}")

    en_areas = PASANTES_A_LA_VEZ - PLATAFORMA
    pas = COSTO_PASANTE * en_areas
    areas = pas + JUNIORS_AREAS
    print(f"\ncosto por pasante y por anio: {q(COSTO_PASANTE, 4)} M")
    print(f"pasantes en las areas a la vez: {en_areas} (hoy 320): {q(pas)} M (hoy 1.013,2)")
    print(f"3.4, pasantias y primer empleo en las areas: {q(areas)} M (hoy {AREAS_HOY}); "
          f"diferencia {q(areas - AREAS_HOY)} M")
    occ = (NUEVOS + REASIGNACION + areas + OBRA_VECINAL) / FLEXIBLE * 100
    print(f"gasto flexible ocupado: {q(occ)}% (hoy 52,3%); libre {q(100 - occ)}% (hoy 47,7%)")
    print(f"lo que pagan las empresas por los segundos seis meses: {q(COSTO_PASANTE * PASANTES_A_LA_VEZ)} M "
          f"por anio (hoy, por 591: {q(COSTO_PASANTE * 591)} M)")

    # Decisiones del 29/09: la beca de practica y el modulo de salud de los anios
    # 1 y 2 salen del gasto flexible libre.
    beca = D(PASANTES_A_LA_VEZ) * D("0.24") * 12          # peor caso: nadie en empresas
    salud_max = (D("505.7") + D("7225.2") / 2) * D("0.6") * D("0.4")  # contratacion del anio 2
    occ_beca = occ + beca / FLEXIBLE * 100
    occ_todo = occ_beca + salud_max / FLEXIBLE * 100
    print(f"\nbeca de practica, peor caso (464 a la vez, 240.000 $ por mes): {q(beca)} M por anio")
    print(f"libre con la beca: {q(100 - occ_beca)}%")
    print(f"modulo de salud de los anios 1 y 2, como maximo la contratacion del anio 2: {q(salud_max)} M")
    print(f"libre con las dos cosas: {q(100 - occ_todo)}%")


if __name__ == "__main__":
    main()
