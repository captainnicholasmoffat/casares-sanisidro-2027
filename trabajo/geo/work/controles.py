# -*- coding: utf-8 -*-
"""Controles: que lo que da el censo por radio, sumado por zona con la
asignacion del programa, coincida con las cifras que publica el programa final."""
import csv, json, sys
G = sys.argv[1]
censo = {r["radio_id"]: r for r in csv.DictReader(open(G + "/src/censo2022_sanisidro_por_radio.csv"))}
asig = {r["radio_id"]: r["zona"] for r in csv.DictReader(open(G + "/src/zonas_asignacion_radios.csv"))}
I = lambda r, c: int(r[c] or 0)
CLO = ["hogares_desague__a_camara_septica_y_pozo_ciego", "hogares_desague__solo_a_pozo_ciego",
       "hogares_desague__a_hoyo_excavacion_en_la_tierra_etc"]
GAS = ["hogares_combustible__electricidad", "hogares_combustible__gas_en_garrafa",
       "hogares_combustible__gas_en_tubo_o_a_granel_zeppelin", "hogares_combustible__lena_o_carbon",
       "hogares_combustible__otro_combustible"]
HAC = ["hogares_hacinamiento__2_00_3_00_personas_por_cuarto", "hogares_hacinamiento__mas_de_3_00_personas_por_cuarto"]
UNI = ["educacion_mni__universitario_completo", "educacion_mni__posgrado_incompleto", "educacion_mni__posgrado_completo"]

def agg(radios):
    s = lambda cols: sum(I(censo[k], c) for k in radios for c in cols)
    return {"radios": len(radios), "poblacion": s(["poblacion_sexo__total"]), "hogares": s(["hogares_nbi__total"]),
            "nbi": s(["hogares_nbi__si"]), "nbi_den": s(["hogares_nbi__total"]),
            "clo": s(CLO), "clo_den": s(["hogares_desague__total"]),
            "gas": s(GAS), "gas_den": s(["hogares_combustible__total"]),
            "hac": s(HAC), "hac_den": s(["hogares_hacinamiento__total"]),
            "uni": s(UNI), "uni_den": s(["educacion_mni__total"]),
            "m14": s(["poblacion_edad__hasta_14_anos"]), "m65": s(["poblacion_edad__65_y_mas_anos"]),
            "edad_den": s(["poblacion_edad__total"])}

ZONAS = ["Boulogne Sur Mer", "Beccar", "Villa Adelina", "San Isidro", "Martinez", "Acassuso"]
A = {z: agg([k for k in asig if asig[k] == z]) for z in ZONAS}
T = agg(list(asig))

# lo que publica el programa final (c462fcf)
PROG = {
 "poblacion": dict(zip(ZONAS, [74832, 63719, 35542, 45872, 64978, 11035])),        # Grafico 2
 "pct_nbi": dict(zip(ZONAS, [5.09, 4.93, 2.73, 1.83, 1.43, 0.94])),                # Graficos 1 y 2
 "pct_clo": dict(zip(ZONAS, [9.16, 10.59, 5.54, 2.97, 1.81, 2.12])),               # Grafico 2
 "pct_gas": dict(zip(ZONAS, [27.64, 37.27, 15.59, 16.64, 14.55, 19.48])),          # Grafico 2
 "pct_hac": dict(zip(ZONAS, [12.42, 12.67, 7.28, 4.18, 2.96, 2.50])),              # Grafico 2
 "pct_uni_1dec": dict(zip(ZONAS, ["9,0", "12,8", "9,3", "25,2", "24,4", "32,3"])), # Grafico 3
 "nbi": dict(zip(ZONAS, [1280, 1088, 356, 354, 374, 45])),                         # Cuadro 22
 "clo": dict(zip(ZONAS, [2295, 2321, 722, 574, 474, 102])),
 "gas": dict(zip(ZONAS, [6947, 8221, 2034, 3221, 3806, 936])),
 "hac": dict(zip(ZONAS, [3121, 2794, 950, 809, 775, 120])),
 "indice": dict(zip(ZONAS, [34.0, 33.0, 10.1, 10.3, 10.5, 2.0])),
 "monto_m": dict(zip(ZONAS, [8569, 7887, 3198, 3729, 4697, 827])),                 # Grafico 23
 "por_hab": dict(zip(ZONAS, [114508, 123782, 89987, 81297, 72285, 74962])),
 "formacion": dict(zip(ZONAS, [315, 307, 94, 96, 98, 18])),                         # 5.3
}
res = []
def chk(nombre, ok, detalle=""):
    res.append((nombre, ok, detalle)); print(("OK  " if ok else "MAL ") + nombre, detalle)

pct = lambda n, d: round(100.0 * n / d, 2)
for z in ZONAS:
    a = A[z]
    chk(f"poblacion {z}", a["poblacion"] == PROG["poblacion"][z], f'{a["poblacion"]} vs {PROG["poblacion"][z]}')
    for k, kp in (("nbi", "pct_nbi"), ("clo", "pct_clo"), ("gas", "pct_gas"), ("hac", "pct_hac")):
        v = pct(a[k], a[k + "_den"])
        chk(f"% {k} {z}", abs(v - PROG[kp][z]) < 0.006, f"{v} vs {PROG[kp][z]}")
        chk(f"hogares {k} {z}", a[k] == PROG[k][z], f"{a[k]} vs {PROG[k][z]}")
    u = f"{100.0 * a['uni'] / a['uni_den']:.1f}".replace(".", ",")
    chk(f"% universidad {z}", u == PROG["pct_uni_1dec"][z], f"{u} vs {PROG['pct_uni_1dec'][z]}")
chk("poblacion total zonas = 295.978", T["poblacion"] == 295978, str(T["poblacion"]))
chk("295.978 + 1.304 = 297.282", T["poblacion"] + 1304 == 297282)
chk("hogares total = 110.559", T["hogares"] == 110559, str(T["hogares"]))
chk("NBI partido 3,16%", f"{100 * T['nbi'] / T['nbi_den']:.2f}" == "3.16")
for k, tot in (("nbi", 3497), ("clo", 6488), ("gas", 25165), ("hac", 8569)):
    chk(f"total {k} = {tot}", T[k] == tot, str(T[k]))
# indice de necesidad del cuadro 22
idx = {z: sum(A[z][k] / T[k] for k in ("nbi", "clo", "gas", "hac")) / 4 for z in ZONAS}
for z in ZONAS:
    chk(f"indice {z}", round(100 * idx[z], 1) == PROG["indice"][z], f"{100 * idx[z]:.2f} vs {PROG['indice'][z]}")
# reparto del ano 4 (grafico 23): mitad poblacion, mitad indice, sobre 28.907.854.675,13
OBRA4 = 28907854675.13
for z in ZONAS:
    peso = 0.5 * A[z]["poblacion"] / T["poblacion"] + 0.5 * idx[z]
    monto = OBRA4 * peso
    chk(f"monto ano 4 {z}", round(monto / 1e6) == PROG["monto_m"][z], f"{monto / 1e6:.1f} M vs {PROG['monto_m'][z]}")
    chk(f"por habitante ano 4 {z}", round(monto / A[z]["poblacion"]) == PROG["por_hab"][z],
        f"{monto / A[z]['poblacion']:.0f} vs {PROG['por_hab'][z]}")
chk("suma montos ano 4 = 28.908 M", round(sum(PROG["monto_m"].values())) in (28907, 28908), str(sum(PROG["monto_m"].values())))
chk("Beccar / Martinez por habitante = 1,71", f"{PROG['por_hab']['Beccar'] / PROG['por_hab']['Martinez']:.2f}" == "1.71")
chk("Boulogne / Martinez por habitante = 1,58", f"{PROG['por_hab']['Boulogne Sur Mer'] / PROG['por_hab']['Martinez']:.2f}" == "1.58")
# formacion: 928 lugares con el indice, restos mayores
base = {z: int(928 * idx[z]) for z in ZONAS}
falta = 928 - sum(base.values())
for z in sorted(ZONAS, key=lambda z: -(928 * idx[z] - base[z]))[:falta]:
    base[z] += 1
chk("formacion 928 por indice (restos mayores)", base == PROG["formacion"], str(base))
chk("formacion suma 928", sum(PROG["formacion"].values()) == 928)
# Boulogne + Beccar
bb = ["Boulogne Sur Mer", "Beccar"]
chk("Boulogne+Beccar poblacion 138.551", sum(A[z]["poblacion"] for z in bb) == 138551)
chk("Boulogne+Beccar hogares 47.193", sum(A[z]["hogares"] for z in bb) == 47193)
chk("Boulogne+Beccar 46,8% de 295.978", f"{100 * 138551 / 295978:.1f}" == "46.8")
chk("Boulogne+Beccar 46,6% de 297.282", f"{100 * 138551 / 297282:.1f}" == "46.6")
chk("Boulogne+Beccar sin cloaca 4.616", sum(A[z]["clo"] for z in bb) == 4616)
chk("Boulogne+Beccar 71% sin cloaca", round(100 * 4616 / 6488) == 71)
chk("Boulogne+Beccar 60% sin gas", round(100 * sum(A[z]["gas"] for z in bb) / 25165) == 60)
# edades (5.13)
for z, k, v in (("Beccar", "m14", "21,0"), ("Boulogne Sur Mer", "m14", "18,7"), ("Acassuso", "m65", "22,5"), ("Martinez", "m65", "22,4")):
    x = f"{100 * A[z][k] / A[z]['edad_den']:.1f}".replace(".", ",")
    chk(f"edad {k} {z}", x == v, f"{x} vs {v}")
chk("partido hasta 14 = 51.388 (17,4%)", T["m14"] == 51388, f"{T['m14']} {100 * T['m14'] / T['edad_den']:.1f}")
chk("partido 65+ = 52.769 (17,8%)", T["m65"] == 52769, f"{T['m65']} {100 * T['m65'] / T['edad_den']:.1f}")
# radios citados
chk("Acassuso tiene 16 radios", A["Acassuso"]["radios"] == 16)
f32 = ["067563202", "067563203", "067563204", "067563205", "067563206", "067563207", "067563208", "067563209", "067563211"]
chk("los 9 radios de la fraccion 32 estan en Beccar", all(asig[k] == "Beccar" for k in f32))
chk("los 9 radios de la fraccion 32 suman 8.749 hab", sum(I(censo[k], "poblacion_sexo__total") for k in f32) == 8749)
r = censo["067562205"]
chk("radio 067562205 en Boulogne, 13,7% NBI y 95,8% sin gas", asig["067562205"] == "Boulogne Sur Mer" and
    f"{100 * I(r, 'hogares_nbi__si') / I(r, 'hogares_nbi__total'):.1f}" == "13.7" and
    f"{100 * sum(I(r, c) for c in GAS) / I(r, 'hogares_combustible__total'):.1f}" == "95.8")
r = censo["067560403"]
chk("radio 067560403 en Acassuso: 17,4% sin cloaca sobre 316 hogares, 0,6% NBI", asig["067560403"] == "Acassuso" and
    I(r, "hogares_desague__total") == 316 and f"{100 * sum(I(r, c) for c in CLO) / 316:.1f}" == "17.4" and
    f"{100 * I(r, 'hogares_nbi__si') / I(r, 'hogares_nbi__total'):.1f}" == "0.6")
aca = [k for k in asig if asig[k] == "Acassuso"]
nbis = [100 * I(censo[k], "hogares_nbi__si") / I(censo[k], "hogares_nbi__total") for k in aca]
chk("Acassuso: NBI de sus radios entre 0,0% y 2,4%", f"{min(nbis):.1f}" == "0.0" and f"{max(nbis):.1f}" == "2.4", f"{min(nbis):.2f}-{max(nbis):.2f}")
tres = ["067560203", "067560204", "067560205"]
nb = [100 * I(censo[k], "hogares_nbi__si") / I(censo[k], "hogares_nbi__total") for k in tres]
gs = [100 * sum(I(censo[k], c) for c in GAS) / I(censo[k], "hogares_combustible__total") for k in tres]
chk("zona San Isidro, fraccion 02 (03, 04, 05): NBI 4,3-11,8%, sin gas 24,8-63,1%",
    all(asig[k] == "San Isidro" for k in tres) and f"{min(nb):.1f}" == "4.3" and f"{max(nb):.1f}" == "11.8"
    and f"{min(gs):.1f}" == "24.8" and f"{max(gs):.1f}" == "63.1", f"{min(nb):.1f}-{max(nb):.1f} / {min(gs):.1f}-{max(gs):.1f}")
print()
print("controles:", len(res), "bien:", sum(ok for _, ok, _ in res), "mal:", [n for n, ok, _ in res if not ok])
json.dump({"radios_por_zona": {z: A[z]["radios"] for z in ZONAS},
           "controles": [{"control": n, "bien": ok, "detalle": d} for n, ok, d in res]},
          open(G + "/work/controles.json", "w"), ensure_ascii=False, indent=1)
