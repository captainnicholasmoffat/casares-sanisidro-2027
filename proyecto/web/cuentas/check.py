"""Cruza los números del modelo fiscal (cuentas.json, que sale del Excel) con el texto del programa (programa.json).
Si algún número del Excel no aparece donde el programa lo dice, el armado del sitio se detiene.
Uso: python3 -I check.py <cuentas.json> <programa.json>"""
import json, sys
d = json.load(open(sys.argv[1]))
docs = {}
for e in json.load(open(sys.argv[2])):
    docs[e["id"]] = e.get("texto", "") + "\n" + "\n".join(str(c.get("titulo", "")) + " " + str(c.get("texto", "")) for c in (e.get("cuadros") or []) if isinstance(c, dict))
from decimal import Decimal, ROUND_HALF_UP
def f(v, dec):
    q = Decimal(str(abs(v))).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP)
    return f"{q:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
I, G, PR, R, Es = d["ingresos"], d["gastos"], d["programas"], d["resultado"], d["escenarios"]
z = {x["zona"]: x for x in d["zonas"]}
pide = d["empleo_vivienda"][3] - 505.7
F = [
 ("Lo que pide el programa en régimen", f(pide, 1), "3.5"),
 ("Empleo y vivienda en 2031", f(d["empleo_vivienda"][3], 1), "6.3"),
 ("La tabla en régimen", f(I["tabla"][3], 0), "3.5"),
 ("Lo que sale del gasto flexible", f(-PR["flex_tabla"][3], 0), "3.5"),
 ("La tabla en 2028", f(I["tabla"][0], 0), "3.5"),
 ("La tabla en 2029", f(I["tabla"][1], 0), "3.5"),
 ("La tabla en 2030", f(I["tabla"][2], 0), "3.5"),
 ("Reasignación en régimen", f(-PR["contrapartida"][3], 0), "3.4"),
 ("Educación", f(PR["educacion"][3], 0), "3.4"),
 ("Resultado 2025", f(d["base2025"]["resultado"], 0), "3.1"),
 ("Cuadro 20 · 2028", f(Es["nada"][0], 0), "3.6"),
 ("Cuadro 20 · 2029 si nada cambia", f(Es["nada"][1], 0), "3.6"),
 ("Cuadro 20 · 2030 si nada cambia", f(Es["nada"][2], 0), "3.6"),
 ("Cuadro 20 · 2031", f(Es["nada"][3], 0), "3.6"),
 ("Cuadro 20 · 2029 con el programa", f(Es["programa"][1], 0), "3.6"),
 ("Cuadro 20 · 2030 con el programa", f(Es["programa"][2], 0), "3.6"),
 ("Mejora 2029", f(Es["dif"][1], 0), "3.6"),
 ("Mejora 2030", f(Es["dif"][2], 0), "3.6"),
 ("Obra pública", f(G["obra"][3], 0), "4.3"),
 ("Obra vecinal año 1", f(G["vecinos"][0], 0), "4.3"),
 ("Obra vecinal año 2", f(G["vecinos"][1], 0), "4.3"),
 ("Obra vecinal año 3", f(G["vecinos"][2], 0), "4.3"),
 ("Obra vecinal año 4", f(G["vecinos"][3], 0), "4.3"),
 ("Índice Boulogne", f(z["Boulogne Sur Mer"]["indice"] * 100, 1) + "%", "4.4"),
 ("Índice Béccar", f(z["Béccar"]["indice"] * 100, 1) + "%", "4.4"),
 ("Índice Martínez", f(z["Martínez"]["indice"] * 100, 1) + "%", "4.4"),
 ("Cupos: Boulogne", f"{z['Boulogne Sur Mer']['cupos']} en Boulogne", "5.3"),
 ("Cupos: Béccar", f"{z['Béccar']['cupos']} en Béccar", "5.3"),
 ("Cupos: Martínez", f"{z['Martínez']['cupos']} en Martínez", "5.3"),
 ("Cupos: San Isidro", f"{z['San Isidro']['cupos']} en San Isidro", "5.3"),
 ("Cupos: Villa Adelina", f"{z['Villa Adelina']['cupos']} en Villa Adelina", "5.3"),
 ("Cupos: Acassuso", f"{z['Acassuso']['cupos']} en Acassuso", "5.3"),
 ("Egresados en el mandato", f(d["egresados"][2] + d["egresados"][3], 0), "5.3"),
 ("Sensibilidad: coparticipación −3,5%", f(d["sensibilidad"][1]["v"][2]["res"], 0), "3.2-r2"),
 ("Sensibilidad: percepción −3 puntos", f(d["sensibilidad"][2]["v"][0]["res"], 0), "3.6"),
]
bad = [(n, v, a) for n, v, a in F if v not in docs.get(a, "")]
for n, v, a in F: print(("OK  " if (n, v, a) not in bad else "MAL ") + f"{n}: {v} en {a}")
if bad:
    print(f"\n{len(bad)} números del Excel no coinciden con el programa. No se arma el sitio."); sys.exit(1)
print(f"\nLos {len(F)} números coinciden con el programa.")
