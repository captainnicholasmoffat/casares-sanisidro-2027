"""Agrega a data/programa.json el orden de los bloques (párrafos, recuadros, fotos, cuadros) y el gráfico de cada cuadro.
Uso: python3 -I merge_orden.py <programa_orden.json>   (sale de build_orden.py sobre el texto final c462fcf)"""
import json, sys
from pathlib import Path
P = Path(__file__).resolve().parent / "data" / "programa.json"
web = json.loads(P.read_text()); new = {e["id"]: e for e in json.load(open(sys.argv[1]))}
fotos = json.loads((P.parent.parent / "img" / "fotos.json").read_text())["fotos"]
cap2 = {}
for f in fotos:
    if f.get("en_programa"):
        cap2.setdefault(f["epigrafe"], []).append(f["archivo"])
n = 0
for e in web:
    m = new[e["id"]]
    assert m["texto"] == e["texto"] and len(m["cuadros"]) == len(e["cuadros"]), e["id"]
    if m.get("orden"):
        o = []
        for x in m["orden"]:
            if x[0] == "foto":
                arch = cap2.get(x[1])
                assert arch, x[1]
                o.append(["foto", arch, x[1]])
            else:
                o.append(x)
        e["orden"] = o; n += 1
    for c, mc in zip(e["cuadros"], m["cuadros"]):
        assert c["titulo"] == mc["titulo"]
        if mc.get("grafico"): c["grafico"] = mc["grafico"]
        else: c.pop("grafico", None)
P.write_text(json.dumps(web, ensure_ascii=False, indent=1))
print("orden en", n, "entradas;", sum(1 for e in web for c in e["cuadros"] if c.get("grafico")), "gráficos")
