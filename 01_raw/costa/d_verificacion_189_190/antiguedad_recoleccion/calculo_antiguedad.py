#!/usr/bin/env python3
"""Estimacion del pasivo por antiguedad (LCT art. 245) del personal de la UTE de
recoleccion de San Isidro, en pesos de diciembre de 2025.

Todo supuesto esta marcado [SC]; todo dato con su fuente en el informe que acompana.
No modifica el repositorio: solo lee data/ del repo y escribe en esta carpeta.
"""
import csv, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/user/casares-sanisidro-2027"

# ---------------------------------------------------------------- deflactor del repo
def ipc_mensual():
    d = {}
    with open(f"{REPO}/data/ipc_indec_mensual.csv") as f:
        for r in csv.DictReader(f):
            d[(int(r["anio"]), int(r["mes"]))] = float(r["indice"])
    return d

IPC = ipc_mensual()
IPC_DIC25 = IPC[(2025, 12)]

def a_dic25(monto, anio, mes):
    return monto * IPC_DIC25 / IPC[(anio, mes)]

# coeficiente anual 2025 (fila acumulado_anual de data/deflactor_periodos.csv)
COEF_2025 = None
with open(f"{REPO}/data/deflactor_periodos.csv") as f:
    for r in csv.DictReader(f):
        if r["periodo_tipo"] == "acumulado_anual" and r["periodo_hasta"].endswith("2025"):
            COEF_2025 = float(r["coef_deflactor"])
assert COEF_2025 is not None

# ---------------------------------------------------------------- escalas CCT 40/89
ESC = {}
with open(f"{AQUI}/escalas_cct4089_recoleccion_2025_2026.csv") as f:
    for r in csv.DictReader(f):
        if r["recolector_basico"]:
            ESC[r["vigencia_desde"][:7]] = {k: float(r[k]) for k in
                ("conductor_1ra_basico", "recolector_basico", "peon_barrido_basico", "comida_item_4112_diaria")}

DIC25 = ESC["2025-12"]
MESES_2025 = [f"2025-{m:02d}" for m in range(1, 13)]
PROM25 = {k: sum(ESC[m][k] for m in MESES_2025) / 12 for k in DIC25}

RAMA = 1.15                 # CCT 40/89 items 5.3.3, 5.3.6, 5.3.8 (+15% sobre el basico)
AMPLIACION = 4 * (52 / 12) * 2 / 192   # item 5.3.10: 4 h/semana al 100%; hora = mensual/24/8 (item 6.1.6)
MEZCLA = {"conductor_1ra_basico": 0.30, "recolector_basico": 0.50, "peon_barrido_basico": 0.20}  # [SC]
DIAS_COMIDA = 26            # [SC] 6 dias por semana

def basico_rama(esc):
    return sum(MEZCLA[k] * esc[k] for k in MEZCLA) * RAMA

# ---------------------------------------------------------------- tope art. 245
# Disp. DTRT 1835/2025, anexo: CCT 40/89 alcance general, vigencia 01/05/2025
PROMEDIO_CCT_MAY25 = 801_690.45
TOPE_MAY25 = 2_405_071.35
# estimacion propia a dic-2025: se escala el promedio con el basico del conductor
PROMEDIO_CCT_DIC25_EST = PROMEDIO_CCT_MAY25 * ESC["2025-12"]["conductor_1ra_basico"] / ESC["2025-05"]["conductor_1ra_basico"]
TOPE_DIC25_EST = 3 * PROMEDIO_CCT_DIC25_EST

# ---------------------------------------------------------------- gasto del programa
GASTO_PROG_2025 = 49_270_113_057.86          # devengado 2025, programa 19 (informe 12)
GASTO_PROG_2025_DIC25 = GASTO_PROG_2025 * COEF_2025

# ---------------------------------------------------------------- dotacion por costo laboral
SERV_PRINCIPAL_2025 = 29_305e6   # IVA incluido, [CP] informe 12
COMPLEMENTARIOS_2025 = {"contenedores_1725_2023": 3_526e6, "diferenciada_17_2014": 1_598e6}  # IVA incl., informe 12
IVA = 0.21
CONTRIB = 0.204 + 0.06 + 0.07     # Ley 27.541 art. 19 a) 20,40% + obra social 6% + ART 7% [SC]

def costo_anual_trabajador_2025(anios):
    """Costo anual del empleador por trabajador operativo, con salarios promedio 2025."""
    remun_mes = basico_rama(PROM25) * (1 + 0.01 * anios) * (1 + AMPLIACION)
    plus_vac = 21 * 18_000           # plus vacacional item 3.3.2 (~$16.000-19.900/dia en 2025) x 21 dias [SC]
    remun_anual = remun_mes * 13 + plus_vac
    contrib = remun_anual * CONTRIB
    comida = DIAS_COMIDA * PROM25["comida_item_4112_diaria"] * RAMA * 12   # item 5.3.11, no remunerativa (item 4.2.11)
    no_remun_otros = 20_000 * 12 + 700_000   # contrib. extraordinaria obra social + asignacion anual no remunerativa [SC]
    return remun_anual + contrib + comida + no_remun_otros

def dotacion_por_costo(share, anios=12, incluir_complementarios=True):
    base = SERV_PRINCIPAL_2025
    if incluir_complementarios:
        base += sum(COMPLEMENTARIOS_2025.values())
    costo_laboral = base / (1 + IVA) * share
    return costo_laboral / costo_anual_trabajador_2025(anios)

# ---------------------------------------------------------------- indemnizacion art. 245
NOCTURNIDAD_ALTO = 0.14   # [SC] promedio: jornada nocturna de 8 h (LCT art. 200) en ~65% del personal

ESCENARIOS = {
    "bajo":  {"N": 350, "anios": 8,  "ampliacion": False, "nocturnidad": 0.0},
    "medio": {"N": 475, "anios": 12, "ampliacion": True,  "nocturnidad": 0.0},
    "alto":  {"N": 600, "anios": 16, "ampliacion": True,  "nocturnidad": 0.0},
}

def base_245(esc, anios, ampliacion, nocturnidad):
    b = basico_rama(esc) * (1 + 0.01 * anios)
    if ampliacion:
        b *= (1 + AMPLIACION)
    b *= (1 + nocturnidad)
    return min(b, TOPE_DIC25_EST), b

def main():
    out = {}
    out["dic25_basicos"] = DIC25
    out["dic25_con_rama"] = {k: v * RAMA for k, v in DIC25.items() if k != "comida_item_4112_diaria"}
    out["dic25_comida_mensual_recoleccion"] = DIC25["comida_item_4112_diaria"] * RAMA * DIAS_COMIDA
    out["ampliacion_jornada_pct"] = AMPLIACION * 100
    out["promedio_basicos_2025"] = PROM25
    out["tope_may25_oficial"] = TOPE_MAY25
    out["tope_dic25_estimado"] = TOPE_DIC25_EST
    out["coef_2025_deflactor_periodos"] = COEF_2025
    out["gasto_programa_2025_en_pesos_dic25"] = GASTO_PROG_2025_DIC25

    # dotacion
    out["costo_anual_trabajador_2025"] = {a: costo_anual_trabajador_2025(a) for a in (8, 12, 16)}
    dot = {}
    for share in (0.35, 0.40, 0.45, 0.50, 0.55):
        dot[f"share_{share}"] = {
            "solo_principal": dotacion_por_costo(share, 12, False),
            "principal_mas_complementarios": dotacion_por_costo(share, 12, True),
        }
    out["dotacion_por_costo_laboral"] = dot

    # dotacion por cuadrillas [CP], cada rango con sus supuestos [SC]
    costo12 = costo_anual_trabajador_2025(12)
    neto = SERV_PRINCIPAL_2025 / (1 + IVA)
    precio_dia = {"recoleccion": 76.3, "contenedores": 6.9, "barrido": 12.7}   # DECRE-2026-639, $M/dia
    tot = sum(precio_dia.values())
    cuad = {
        "recoleccion_domiciliaria": (30 * 3 * 1.15, 32 * 4 * 1.15),            # rutas BRA x (1 chofer + 2/3) x reemplazos
        "barrido_UTE": (neto * precio_dia["barrido"] / tot * 0.60 / costo12,  # 60-80% mano de obra [SC]
                        neto * precio_dia["barrido"] / tot * 0.80 / costo12),
        "contenedores": (neto * precio_dia["contenedores"] / tot * 0.35 / costo12,
                         neto * precio_dia["contenedores"] / tot * 0.50 / costo12),
        "poda_verdes_voluminosos_sumideros_hidrolavado": (50, 120),          # [SC]
        "taller_supervision_admin_convenio": (25, 40),                      # [SC]
        "complementarios_diferenciada_bilateral_cestos_trituradora": (50, 95),  # [SC]
    }
    out["dotacion_por_cuadrillas"] = {k: (round(a), round(b)) for k, (a, b) in cuad.items()}
    out["dotacion_por_cuadrillas_total"] = (round(sum(a for a, b in cuad.values())), round(sum(b for a, b in cuad.values())))

    # escenarios
    res = {}
    for nom, e in ESCENARIOS.items():
        base, base_sin_tope = base_245(DIC25, e["anios"], e["ampliacion"], e["nocturnidad"])
        por_trab = base * e["anios"]
        total = por_trab * e["N"]
        res[nom] = {
            **e,
            "base_mensual_245": base,
            "tope_aplica": base_sin_tope > TOPE_DIC25_EST,
            "indemnizacion_por_trabajador": por_trab,
            "total": total,
            "pct_gasto_programa_2025_en_pesos_dic25": total / GASTO_PROG_2025_DIC25 * 100,
            "pct_gasto_programa_2025_nominal": total / GASTO_PROG_2025 * 100,
        }
    out["escenarios"] = res

    # sensibilidad N x anios, con la base del escenario medio (ampliacion si, sin nocturnidad)
    sens = {}
    for N in (300, 350, 400, 475, 500, 550, 600, 650):
        for a in (6, 8, 10, 12, 14, 16, 18, 20):
            b, _ = base_245(DIC25, a, True, 0.0)
            sens[f"N{N}_a{a}"] = b * a * N
    out["sensibilidad_N_anios_base_media"] = sens

    # devengamiento anual del pasivo (escenario medio): un anio mas de servicio
    b12, _ = base_245(DIC25, 12, True, 0.0)
    b13, _ = base_245(DIC25, 13, True, 0.0)
    out["devengo_anual_medio_por_trab"] = b13 * 13 - b12 * 12
    out["devengo_anual_medio_total"] = (b13 * 13 - b12 * 12) * 475

    # comida como remunerativa (riesgo judicial), sumada al escenario alto
    com = DIC25["comida_item_4112_diaria"] * RAMA * DIAS_COMIDA
    e = ESCENARIOS["alto"]
    b, _ = base_245(DIC25, e["anios"], e["ampliacion"], e["nocturnidad"])
    out["alto_con_comida_remunerativa_total"] = min(b + com, TOPE_DIC25_EST) * e["anios"] * e["N"]

    # referencias, a pesos de dic-2025
    ref = {}
    # Ciudad 2012 (AGCBA 1.13.07, cuadro 32): Cliba 100% de cuotas; resto solo cuotas 3 y 4 (60%)
    cliba = 130_457_359.13
    otros_60 = 35_380_750.67 + 22_155_114.75 + 38_595_776.65 + 41_168_148.37
    total_2012 = cliba + otros_60 / 0.60
    ref["caba2012_total_nominal"] = total_2012
    for n in (7000, 4000):
        ref[f"caba2012_por_trab_nominal_N{n}"] = total_2012 / n
        ref[f"caba2012_por_trab_dic25_N{n}"] = a_dic25(total_2012 / n, 2012, 2)
    ref["caba2012_total_dic25"] = a_dic25(total_2012, 2012, 2)
    ref["caba2012_cliba_dic25"] = a_dic25(cliba, 2012, 2)
    # implicito: anios promedio con salario minimo de convenio (nov-2011: recolector 2903,43; chofer 3148,66; barrido 2875,72)
    base2012 = (0.30 * 3148.66 + 0.50 * 2903.43 + 0.20 * 2875.72) * RAMA * (1 + AMPLIACION)
    for n in (7000, 6000, 4000):
        pt = total_2012 / n
        # resolver anios: pt = base2012*(1+0.01a)*a
        a = 0.0
        while base2012 * (1 + 0.01 * a) * a < pt:
            a += 0.01
        ref[f"caba2012_anios_implicitos_N{n}"] = a
    # Ciudad 2024: US$200 M / 6.000, BCRA 05/09/2024 = 954,50
    usd = 200e6 / 6000
    ref["caba2024_por_trab_pesos_sep24"] = usd * 954.50
    ref["caba2024_por_trab_dic25"] = a_dic25(usd * 954.50, 2024, 9)
    ref["caba2024_total_dic25"] = a_dic25(200e6 * 954.50, 2024, 9)
    # Cordoba 2016: $70.000 promedio, 7 anios
    ref["cordoba2016_por_trab_dic25"] = a_dic25(70_000, 2016, 6)
    ref["cordoba2016_por_anio_dic25"] = a_dic25(70_000 / 7, 2016, 6)
    ref["cordoba2016_prestamo_dic25"] = a_dic25(120e6, 2016, 6)
    # Quilmes 2014: ejemplo del Municipio, 9 anios -> 50 a 80 mil
    ref["quilmes2014_ejemplo_dic25"] = (a_dic25(50_000, 2014, 5), a_dic25(80_000, 2014, 5))
    # gruas CABA 2022: hasta $4 M por trabajador, ~$2.000 M en total
    ref["gruas2022_por_trab_dic25"] = a_dic25(4e6, 2022, 9)
    ref["gruas2022_total_dic25"] = a_dic25(2000e6, 2022, 9)
    # San Isidro, escenario medio: por anio de servicio
    ref["sanisidro_medio_por_anio"] = res["medio"]["indemnizacion_por_trabajador"] / 12
    out["referencias"] = ref

    with open(f"{AQUI}/resultados_antiguedad.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    return out

if __name__ == "__main__":
    o = main()
    def m(x): return f"{x/1e6:,.1f} M"
    print("Base con rama dic-25:", {k: round(v) for k, v in o["dic25_con_rama"].items()})
    print("Comida mensual recoleccion dic-25:", round(o["dic25_comida_mensual_recoleccion"]))
    print("Ampliacion jornada %:", round(o["ampliacion_jornada_pct"], 2))
    print("Tope may-25 oficial / dic-25 estimado:", o["tope_may25_oficial"], round(o["tope_dic25_estimado"]))
    print("Gasto programa 2025 en pesos dic-25:", m(o["gasto_programa_2025_en_pesos_dic25"]), "coef", o["coef_2025_deflactor_periodos"])
    print("Costo anual por trabajador 2025:", {k: m(v) for k, v in o["costo_anual_trabajador_2025"].items()})
    for k, v in o["dotacion_por_costo_laboral"].items():
        print("Dotacion", k, {kk: round(vv) for kk, vv in v.items()})
    for k, v in o["escenarios"].items():
        print(k, "N", v["N"], "anios", v["anios"], "base", round(v["base_mensual_245"]), "tope?", v["tope_aplica"],
              "por trab", m(v["indemnizacion_por_trabajador"]), "TOTAL", m(v["total"]),
              f"{v['pct_gasto_programa_2025_en_pesos_dic25']:.1f}% (dic25) / {v['pct_gasto_programa_2025_nominal']:.1f}% (nominal)")
    print("Devengo anual medio por trab / total:", m(o["devengo_anual_medio_por_trab"]), m(o["devengo_anual_medio_total"]))
    print("Alto con comida remunerativa:", m(o["alto_con_comida_remunerativa_total"]))
    for k, v in o["referencias"].items():
        print(k, v if isinstance(v, tuple) else (m(v) if v > 1e5 else round(v, 2)))
