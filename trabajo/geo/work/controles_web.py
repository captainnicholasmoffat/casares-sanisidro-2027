# -*- coding: utf-8 -*-
"""Controles de web/data: que las cifras de zonas_datos.json coincidan con lo que da el censo por radio
sumado con la asignacion del programa, con los datos del repo y con los cuadros y graficos del programa
final; y que zonas.geojson sea coherente con todo eso.

Uso: python3 -I controles_web.py <carpeta geo> <zonas_datos.json> <zonas.geojson> <final.txt> <charts.py> <salida.json>
"""
import csv, json, math, re, sys
from shapely.geometry import shape

G, DATOS, GEO, FINAL, CHARTS, SAL = sys.argv[1:7]
D = json.load(open(DATOS, encoding="utf-8"))
GJ = json.load(open(GEO, encoding="utf-8"))
FT = open(FINAL, encoding="utf-8").read()
CH = open(CHARTS, encoding="utf-8").read()

def leer(p):
    return list(csv.DictReader([l for l in open(p, encoding="utf-8") if not l.startswith("#")]))

censo = {r["radio_id"]: r for r in leer(G + "/src/censo2022_sanisidro_por_radio.csv")}
asig = {r["radio_id"]: r["zona"] for r in leer(G + "/src/zonas_asignacion_radios.csv")}
I = lambda r, c: int(r[c] or 0)
CLO = ["hogares_desague__a_camara_septica_y_pozo_ciego", "hogares_desague__solo_a_pozo_ciego",
       "hogares_desague__a_hoyo_excavacion_en_la_tierra_etc"]
GAS = ["hogares_combustible__electricidad", "hogares_combustible__gas_en_garrafa",
       "hogares_combustible__gas_en_tubo_o_a_granel_zeppelin", "hogares_combustible__lena_o_carbon",
       "hogares_combustible__otro_combustible"]
HAC = ["hogares_hacinamiento__2_00_3_00_personas_por_cuarto", "hogares_hacinamiento__mas_de_3_00_personas_por_cuarto"]
UNI = ["educacion_mni__universitario_completo", "educacion_mni__posgrado_incompleto", "educacion_mni__posgrado_completo"]
ID = {"boulogne": "Boulogne Sur Mer", "beccar": "Beccar", "villa_adelina": "Villa Adelina",
      "san_isidro": "San Isidro", "martinez": "Martinez", "acassuso": "Acassuso"}

def agg(ks):
    s = lambda cols: sum(I(censo[k], c) for k in ks for c in cols)
    return {"radios": len(ks), "pob": s(["poblacion_sexo__total"]), "hog": s(["hogares_nbi__total"]),
            "nbi": s(["hogares_nbi__si"]), "nbi_d": s(["hogares_nbi__total"]),
            "clo": s(CLO), "clo_d": s(["hogares_desague__total"]), "gas": s(GAS), "gas_d": s(["hogares_combustible__total"]),
            "hac": s(HAC), "hac_d": s(["hogares_hacinamiento__total"]), "uni": s(UNI), "uni_d": s(["educacion_mni__total"]),
            "m14": s(["poblacion_edad__hasta_14_anos"]), "m65": s(["poblacion_edad__65_y_mas_anos"]), "ed": s(["poblacion_edad__total"])}

A = {z: agg([k for k in asig if asig[k] == ID[z]]) for z in ID}
T = agg(list(asig))
res = []
def chk(n, ok, det=""):
    res.append({"control": n, "bien": bool(ok), "detalle": str(det)})

v = lambda z, k: D["zonas"][z]["cifras"][k]["valor"]
pct = lambda a, b: 100.0 * a / b
idx = {z: sum(A[z][k] / T[k] for k in ("nbi", "clo", "gas", "hac")) / 4 for z in ID}
OBRA4 = 28907854675.13          # data/reparto_vecinal_por_zona.csv: el 50% de la obra publica 2025

for z in ID:
    a = A[z]
    chk(f"{z}: poblacion", v(z, "poblacion") == a["pob"], f'{v(z, "poblacion")} / censo {a["pob"]}')
    for k, kk in (("nbi", "pct_hogares_nbi"), ("clo", "pct_hogares_sin_cloaca"), ("gas", "pct_hogares_sin_gas_de_red"),
                  ("hac", "pct_hogares_con_hacinamiento")):
        x = round(pct(a[k], a[k + "_d"]), 2)
        chk(f"{z}: {kk}", abs(v(z, kk) - x) < 1e-9, f"{v(z, kk)} / censo {x}")
    for k, kk in (("nbi", "hogares_nbi"), ("clo", "hogares_sin_cloaca"), ("gas", "hogares_sin_gas_de_red"),
                  ("hac", "hogares_con_hacinamiento")):
        chk(f"{z}: {kk}", v(z, kk) == a[k], f"{v(z, kk)} / censo {a[k]}")
        x = round(pct(a[k], T[k]), 1)
        chk(f"{z}: {kk}_parte_del_total", abs(v(z, kk + "_parte_del_total") - x) < 1e-9, f"{v(z, kk + '_parte_del_total')} / censo {x}")
    chk(f"{z}: indice_de_necesidad", abs(v(z, "indice_de_necesidad") - round(100 * idx[z], 1)) < 1e-9,
        f"{v(z, 'indice_de_necesidad')} / censo {100 * idx[z]:.2f}")
    monto = OBRA4 * (0.5 * a["pob"] / T["pob"] + 0.5 * idx[z])
    chk(f"{z}: obra año 4 monto", v(z, "obra_vecinal_anio4_monto") == round(monto / 1e6), f"{v(z, 'obra_vecinal_anio4_monto')} / {monto / 1e6:.1f}")
    chk(f"{z}: obra año 4 por habitante", v(z, "obra_vecinal_anio4_por_habitante") == round(monto / a["pob"]),
        f"{v(z, 'obra_vecinal_anio4_por_habitante')} / {monto / a['pob']:.1f}")
    u_exacto = pct(a["uni"], a["uni_d"])
    u_grafico = float(f"{round(u_exacto, 2):.1f}")       # el grafico redondea a 2 decimales y despues a 1
    chk(f"{z}: universidad (como la muestra el Gráfico 3)", abs(v(z, "pct_personas_con_universidad_terminada") - u_grafico) < 1e-9,
        f"{v(z, 'pct_personas_con_universidad_terminada')} / censo {u_exacto:.3f}")
    # geojson: misma zona, mismo id
    f = [f for f in GJ["features"] if f["properties"].get("id") == z]
    chk(f"{z}: está en zonas.geojson", len(f) == 1 and f[0]["properties"]["nombre"] == D["zonas"][z]["nombre"])

# formacion: 928 por indice, restos mayores
base = {z: int(928 * idx[z]) for z in ID}
for z in sorted(ID, key=lambda z: -(928 * idx[z] - base[z]))[:928 - sum(base.values())]:
    base[z] += 1
chk("formación: 928 lugares con el índice (restos mayores)", all(v(z, "formacion_lugares_por_anio") == base[z] for z in ID), base)
chk("formación: suman 928", sum(v(z, "formacion_lugares_por_anio") for z in ID) == 928)
chk("obra año 4: suma de zonas = 28.908 M (±1 por redondeo)", abs(sum(v(z, "obra_vecinal_anio4_monto") for z in ID) - 28908) <= 1,
    sum(v(z, "obra_vecinal_anio4_monto") for z in ID))
chk("población: suma de zonas = 295.978", sum(v(z, "poblacion") for z in ID) == 295978 == T["pob"])
chk("295.978 + 1.304 = 297.282", 295978 + 1304 == 297282)
chk("hogares del partido = 110.559", T["hog"] == D["san_isidro"]["cifras"]["hogares"]["valor"], T["hog"])
chk("NBI del partido = 3,16%", round(pct(T["nbi"], T["nbi_d"]), 2) == 3.16)
for k, kk in (("nbi", "hogares_nbi"), ("clo", "hogares_sin_cloaca"), ("gas", "hogares_sin_gas_de_red"), ("hac", "hogares_con_hacinamiento")):
    chk(f"partido: {kk}", T[k] == D["san_isidro"]["cifras"][kk]["valor"] == sum(v(z, kk) for z in ID), T[k])
chk("partido: hasta 14 años 51.388 (17,4%)", T["m14"] == 51388 and round(pct(T["m14"], T["ed"]), 1) == 17.4)
chk("partido: 65 y más 52.769 (17,8%)", T["m65"] == 52769 and round(pct(T["m65"], T["ed"]), 1) == 17.8)
for z, k, kk in (("beccar", "m14", "pct_personas_hasta_14_anios"), ("boulogne", "m14", "pct_personas_hasta_14_anios"),
                 ("acassuso", "m65", "pct_personas_65_y_mas"), ("martinez", "m65", "pct_personas_65_y_mas")):
    chk(f"{z}: {kk}", round(pct(A[z][k], A[z]["ed"]), 1) == v(z, kk), f"{v(z, kk)} / censo {pct(A[z][k], A[z]['ed']):.2f}")
# Boulogne + Beccar
g = D["grupos"][0]["cifras"]
bb = ("boulogne", "beccar")
chk("Boulogne+Béccar: población 138.551", sum(A[z]["pob"] for z in bb) == g["poblacion"]["valor"])
chk("Boulogne+Béccar: hogares 47.193", sum(A[z]["hog"] for z in bb) == g["hogares"]["valor"])
chk("Boulogne+Béccar: 46,8% y 46,6%", round(pct(138551, 295978), 1) == 46.8 and round(pct(138551, 297282), 1) == 46.6)
chk("Boulogne+Béccar: 4.616 sin cloaca", sum(A[z]["clo"] for z in bb) == g["hogares_sin_cloaca"]["valor"])
chk("Boulogne+Béccar: 71% de los sin cloaca", round(pct(4616, 6488)) == 71)
chk("Boulogne+Béccar: 60% de los sin gas", round(pct(sum(A[z]["gas"] for z in bb), 25165)) == 60)
# radios citados
chk("Acassuso: 16 radios", A["acassuso"]["radios"] == 16)
f32 = ["067563202", "067563203", "067563204", "067563205", "067563206", "067563207", "067563208", "067563209", "067563211"]
chk("fracción 32: 9 radios en Béccar, 8.749 hab", all(asig[k] == "Beccar" for k in f32) and
    sum(I(censo[k], "poblacion_sexo__total") for k in f32) == 8749)
r = censo["067562205"]
chk("radio 067562205: en Boulogne, 13,7% NBI, 95,8% sin gas", asig["067562205"] == "Boulogne Sur Mer" and
    round(pct(I(r, "hogares_nbi__si"), I(r, "hogares_nbi__total")), 1) == 13.7 and
    round(pct(sum(I(r, c) for c in GAS), I(r, "hogares_combustible__total")), 1) == 95.8)
r = censo["067560403"]
chk("radio 067560403: en Acassuso, 17,4% sin cloaca sobre 316, 0,6% NBI", asig["067560403"] == "Acassuso" and
    I(r, "hogares_desague__total") == 316 and round(pct(sum(I(r, c) for c in CLO), 316), 1) == 17.4 and
    round(pct(I(r, "hogares_nbi__si"), I(r, "hogares_nbi__total")), 1) == 0.6)
aca = [k for k in asig if asig[k] == "Acassuso"]
nb = [pct(I(censo[k], "hogares_nbi__si"), I(censo[k], "hogares_nbi__total")) for k in aca]
chk("Acassuso: NBI de los radios de 0,0% a 2,4%", round(min(nb), 1) == 0.0 and round(max(nb), 1) == 2.4)
tres = ["067560203", "067560204", "067560205"]
nb = [pct(I(censo[k], "hogares_nbi__si"), I(censo[k], "hogares_nbi__total")) for k in tres]
gs = [pct(sum(I(censo[k], c) for c in GAS), I(censo[k], "hogares_combustible__total")) for k in tres]
chk("San Isidro, fracción 02 (03-05): NBI 4,3-11,8%, sin gas 24,8-63,1%", all(asig[k] == "San Isidro" for k in tres) and
    (round(min(nb), 1), round(max(nb), 1), round(min(gs), 1), round(max(gs), 1)) == (4.3, 11.8, 24.8, 63.1))

# Cuadro 22, fila por fila, contra el texto final
fmt = lambda n: f"{n:,}".replace(",", ".")
fc = lambda x: f"{x:.1f}".replace(".", ",")
NOMC22 = {"boulogne": "Boulogne Sur Mer", "beccar": "Béccar", "villa_adelina": "Villa Adelina", "san_isidro": "San Isidro",
          "martinez": "Martínez", "acassuso": "Acassuso"}
for z in ID:
    fila = f" | {NOMC22[z]} | " + " | ".join(f"{fmt(v(z, k))} ({fc(v(z, k + '_parte_del_total'))}%)" for k in
                                         ("hogares_nbi", "hogares_sin_cloaca", "hogares_sin_gas_de_red", "hogares_con_hacinamiento")) \
           + f" | {fc(v(z, 'indice_de_necesidad'))}%"
    chk(f"Cuadro 22, fila {z}", fila in FT, fila)
# Cuadro 17, fila por fila, contra el texto final y contra data/valuacion_ratios_localidad.csv
NOMC17 = dict(NOMC22, san_isidro="Localidad de San Isidro", boulogne="Boulogne Sur Mer, la referencia")
rat = {r["localidad"]: r for r in leer(G + "/src/valuacion_ratios_localidad.csv")}
f2 = lambda x: (f"{x:.2f}".replace(".", ",")).rstrip("0").rstrip(",") if x == 1 else f"{x:.2f}".replace(".", ",")
for z in ID:
    ct = D["zonas"][z]["cifras"]
    rec = f"{ct['tierra_reconocido']['valor']}%" if "tierra_reconocido" in ct else "—"
    fila = f" | {NOMC17[z]} | {f2(v(z, 'tierra_veces_boulogne_tabla_municipal'))}× | {f2(v(z, 'tierra_veces_boulogne_valuacion_provincial'))}× | {rec}"
    r = rat[ID[z]]
    # el csv trae 3 decimales (1 en «reconocido»): se admite la diferencia de redondeo
    ok_csv = (abs(float(r["veces_la_base_tabla_municipal"]) - v(z, "tierra_veces_boulogne_tabla_municipal")) <= 0.0051 and
              abs(float(r["veces_la_base_valuacion_provincial"]) - v(z, "tierra_veces_boulogne_valuacion_provincial")) <= 0.0051 and
              (z == "boulogne" or abs(float(r["reconocido_pct"]) - ct["tierra_reconocido"]["valor"]) <= 0.51))
    chk(f"Cuadro 17, fila {z}", fila in FT and ok_csv, fila)
esc = {r["localidad"]: r for r in leer(G + "/src/valuacion_escenarios_localidad.csv")}
for z in ID:
    r = esc[ID[z]]
    ok = (float(r["carga_hoy_pct"]) == v(z, "tierra_parte_del_total_hoy") and float(r["Bc_carga_pct"]) == v(z, "tierra_parte_del_total_con_tabla_nueva")
          and abs(float(r["Bc_dif_pct"]) - v(z, "tierra_variacion_de_lo_que_paga")) < 0.051)
    chk(f"3.5: parte de la tierra y variación, {z}", ok, f'{r["carga_hoy_pct"]}->{r["Bc_carga_pct"]}, {r["Bc_dif_pct"]}%')
r = esc["Todo el partido"]
chk("3.5: parcelas que bajan y suben", int(r["Bc_parcelas_bajan"]) == 34998 and int(r["Bc_parcelas_suben"]) == 33619)

# graficos: los mismos numeros, en el mismo orden de zonas, que doc/charts.py
def lista(nombre):
    m = re.search(nombre + r"\s*=\s*\[([^\]]+)\]", CH)
    return [float(x) for x in m.group(1).split(",")]
orden = ["boulogne", "beccar", "villa_adelina", "san_isidro", "martinez", "acassuso"]
for nom, k in (("nbi", "pct_hogares_nbi"), ("clo", "pct_hogares_sin_cloaca"), ("gas", "pct_hogares_sin_gas_de_red"),
               ("hac", "pct_hogares_con_hacinamiento"), ("pob", "poblacion")):
    chk(f"Gráfico 2 (charts.py, {nom})", lista(nom) == [v(z, k) for z in orden])
u = lista("v")      # primer "v=[...]": g_universitario
chk("Gráfico 3 (charts.py)", [float(f"{x:.1f}") for x in u] == [v(z, "pct_personas_con_universidad_terminada") for z in orden], u)
m = re.search(r'def g_reparto\(\):.*?v=\[([^\]]+)\].*?monto=\[([^\]]+)\]', CH, re.S)
orden_r = ["beccar", "boulogne", "villa_adelina", "san_isidro", "acassuso", "martinez"]
chk("Gráfico 23 (charts.py)", [int(x) for x in m.group(1).split(",")] == [v(z, "obra_vecinal_anio4_por_habitante") for z in orden_r]
    and [int(x) for x in m.group(2).split(",")] == [v(z, "obra_vecinal_anio4_monto") for z in orden_r])

# geojson
ps = {f["properties"]["tipo"] for f in GJ["features"]}
chk("zonas.geojson: seis localidades, partido y costa", ps == {"localidad", "partido", "costa"} and
    sum(f["properties"]["tipo"] == "localidad" for f in GJ["features"]) == 6)
import os
chk("zonas.geojson pesa menos de 150 KB", os.path.getsize(GEO) < 150 * 1024, os.path.getsize(GEO))

print("controles:", len(res), "bien:", sum(r["bien"] for r in res))
for r in res:
    if not r["bien"]:
        print("  MAL", r["control"], r["detalle"])
json.dump(res, open(SAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
