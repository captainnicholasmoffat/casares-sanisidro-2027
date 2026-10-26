# Arma acciones.json: duraciones, fechas, camino crítico (CPM) y validaciones.
import json
import re
import sys
from collections import defaultdict, deque

from cal import (D, ONE, pos_on_or_after, pos_on_or_before, date_of, wd_span, fecha_larga)
import acciones_def as AD
from pruebas import PRUEBA
from pasos_extra import STEPS

OUT = sys.argv[1] if len(sys.argv) > 1 else "acciones.json"
A = AD.A
BY = {a["code"]: a for a in A}
errors, warns = [], []

# ---------- normalizar
for a in A:
    a["stream"] = AD.STREAMS[a["code"][0]]
    if a["owner"] not in AD.TEAM:
        errors.append(f"{a['code']}: responsable sin equipo: {a['owner']}")
    a["team"] = AD.TEAM.get(a["owner"], "?")
    a["ms"] = a.get("ms", False)
    if a["ms"]:
        a["dur"] = 0
    elif "span" in a:
        s0, s1 = a["span"]
        a["dur"] = wd_span(s0, s1) - (1 if a.get("cierre") else 0)
    if "dur" not in a:
        errors.append(f"{a['code']}: sin duración")
    nd = []
    for n in a.get("needs", []):
        if isinstance(n, str):
            nd.append((n, "FS", 0))
        else:
            nd.append(tuple(n))
    a["_needs"] = nd
    for c, t, l in nd:
        if c not in BY:
            errors.append(f"{a['code']}: necesita {c}, que no existe")
    if not nd and "sne" not in a and "win" not in a and "fixed" not in a:
        errors.append(f"{a['code']}: no tiene antecesor ni fecha")

for k in list(PRUEBA) + list(STEPS):
    if k not in BY:
        errors.append(f"prueba para un código que no existe: {k}")
if len({a["code"] for a in A}) != len(A):
    errors.append("códigos repetidos")

# ---------- orden topológico (detecta ciclos)
succ = defaultdict(list)
indeg = {a["code"]: 0 for a in A}
for a in A:
    for c, t, l in a["_needs"]:
        if c in BY:
            succ[c].append((a["code"], t, l))
            indeg[a["code"]] += 1
q = deque(sorted(c for c, d in indeg.items() if d == 0))
order = []
while q:
    c = q.popleft()
    order.append(c)
    for s, t, l in succ[c]:
        indeg[s] -= 1
        if indeg[s] == 0:
            q.append(s)
if len(order) != len(A):
    errors.append("hay un ciclo: " + ", ".join(sorted(set(BY) - set(order))))
    print("\n".join(errors))
    sys.exit(1)

# ---------- límites de cada acción
for a in A:
    a["_sne"] = None
    a["_dl"] = None
    if "win" in a:
        a["_sne"] = a["win"][0]
        a["_dl"] = a["win"][1]
    if "sne" in a:
        a["_sne"] = max(a["_sne"], a["sne"]) if a["_sne"] else a["sne"]

# ---------- pasada hacia adelante
ES, EF = {}, {}
for c in order:
    a = BY[c]
    es = 0
    if a["_sne"]:
        es = max(es, pos_on_or_after(a["_sne"]))
    for p, t, l in a["_needs"]:
        es = max(es, (EF[p] if t == "FS" else ES[p]) + l)
    if "fixed" in a:
        fin = pos_on_or_before(a["fixed"])
        fout = pos_on_or_after(a["fixed"])
        latest_pred = max([EF[p] for p, t, l in a["_needs"] if t == "FS"] + [0])
        if latest_pred > fin and a["_needs"]:
            errors.append(f"{c}: lo anterior no llega a la fecha fija {a['fixed']}")
        es = fout
    ES[c], EF[c] = es, es + a["dur"]

# ---------- pasada hacia atrás (contra el fin del mandato y los plazos del programa)
PEND = pos_on_or_after(D(2031, 12, 10))
LS, LF, LSP = {}, {}, {}
for c in reversed(order):
    a = BY[c]
    lf = PEND + 0
    for s, t, l in succ[c]:
        bound_s = LSP[s]
        if t == "FS":
            lf = min(lf, bound_s - l)
        else:
            lf = min(lf, bound_s - l + a["dur"])
    if a["_dl"]:
        if a["ms"]:
            lf = min(lf, pos_on_or_before(a["_dl"]))
        else:
            lf = min(lf, pos_on_or_after(a["_dl"] + ONE))
    if "fixed" in a:
        LS[c] = LF[c] = ES[c]
        LSP[c] = pos_on_or_before(a["fixed"])
    else:
        LF[c] = lf
        LS[c] = lf - a["dur"]
        LSP[c] = LS[c]

FLOAT = {c: (0 if "fixed" in BY[c] else LS[c] - ES[c]) for c in BY}
for c, f in FLOAT.items():
    if f < 0:
        errors.append(f"{c}: holgura negativa ({f}): no entra en las fechas del programa")


# ---------- textos de nota
def win_sentence(a):
    if "win" not in a:
        return ""
    ws, we, label = a["win"]
    if a.get("win_est"):
        return f"Fecha estimada: {label}, entre el {fecha_larga(ws)} y el {fecha_larga(we)}."
    if ws == we:
        return f"Calendario del programa: {label}."
    return f"Calendario del programa: {label}, del {fecha_larga(ws)} al {fecha_larga(we)}."


def note_of(a):
    parts = []
    ws = win_sentence(a)
    if ws:
        parts.append(ws)
    if a.get("durnote"):
        parts.append(a["durnote"])
    elif a.get("est"):
        parts.append("Duración estimada.")
    if a.get("note"):
        n = a["note"]
        if a.get("est") and n.startswith("Duración estimada"):
            parts = [p for p in parts if p != "Duración estimada."]
        parts.append(n)
    return " ".join(parts)


def iso(d):
    return d.isoformat()


out = []
for a in A:
    c = a["code"]
    if "fixed" in a:
        start = finish = a["fixed"]
    else:
        start = date_of(ES[c])
        finish = date_of(EF[c]) if not a["ms"] else start
    sne = ""
    if "fixed" in a:
        sne = iso(a["fixed"])
    elif a["_sne"]:
        sne = iso(a["_sne"])
    needs = [{"code": p, "type": t, "lag": l} for p, t, l in a["_needs"]]
    out.append({
        "code": c, "task": a["task"], "stream": a["stream"], "owner": a["owner"], "team": a["team"],
        "dur": a["dur"], "start": iso(start), "finish": iso(finish), "float": FLOAT[c],
        "critical": FLOAT[c] == 0, "milestone": a["ms"], "decision": a.get("decision", ""),
        "steps": " ".join(x for x in [a.get("steps", "") or STEPS.get(c, ""), ("Cómo se comprueba: «" + PRUEBA[c] + "»") if c in PRUEBA else ""] if x), "moves": "", "sne": sne, "needs": needs, "note": note_of(a),
        "fuente": a.get("fuente", ""),
    })

# ---------- validaciones sobre la salida
OD = {o["code"]: o for o in out}
for o in out:
    a = BY[o["code"]]
    st = D.fromisoformat(o["start"])
    fi = D.fromisoformat(o["finish"])
    if o["milestone"] and o["dur"] != 0:
        errors.append(f"{o['code']}: hito con duración")
    if not o["milestone"]:
        n = pos_on_or_after(fi) - pos_on_or_after(st)
        if n != o["dur"]:
            errors.append(f"{o['code']}: inicio y fin no cuadran con la duración")
    # ninguna acción empieza antes de lo que necesita
    for nd in o["needs"]:
        p = OD[nd["code"]]
        if nd["type"] == "FS":
            ref = D.fromisoformat(p["finish"])
        else:
            ref = D.fromisoformat(p["start"])
        if nd["lag"]:
            ref = date_of(pos_on_or_after(ref) + nd["lag"])
        if st < ref:
            errors.append(f"{o['code']} empieza {st} antes de {nd['code']} ({nd['type']}) {ref}")
    # dentro de la ventana del programa
    if "win" in a:
        ws, we, _ = a["win"]
        last = st if o["milestone"] else date_of(pos_on_or_after(fi) - 1)
        if st < ws or last > we:
            errors.append(f"{o['code']}: fuera de su ventana ({ws}–{we}): {st}–{last}")
    if "reldl" in a:
        ref, days = a["reldl"]
        lim = D.fromisoformat(OD[ref]["start"]) + days * ONE
        last = date_of(pos_on_or_after(fi) - 1)
        if last > lim:
            errors.append(f"{o['code']}: pasa el plazo de {days} días desde {ref}")
    if "fixed" in a and o["start"] != iso(a["fixed"]):
        errors.append(f"{o['code']}: no quedó en su fecha fija")
    # textos
    for f in ("task", "decision", "steps", "note"):
        txt = o[f]
        for sent in re.split(r"(?<=[.!?])\s+", txt):
            w = sent.strip().split(" ")[0] if sent.strip() else ""
            if w in ("Y", "Que", "y", "que"):
                errors.append(f"{o['code']}.{f}: oración que empieza con «{w}»: {sent[:60]}")
    if not o["fuente"]:
        errors.append(f"{o['code']}: sin fuente")
    if o["dur"] and not (a.get("est") or a.get("durnote")):
        errors.append(f"{o['code']}: duración sin marcar si es estimada o del programa")

streams = sorted({o["stream"] for o in out}, key=lambda s: int(s.split()[0]))
if len(streams) != 13:
    errors.append(f"líneas de trabajo: {len(streams)}")

# orden de salida: por línea, inicio y código
out.sort(key=lambda o: (int(o["stream"].split()[0]), o["start"], o["code"]))

json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)

# ---------- resumen
crit = [o for o in out if o["critical"]]
ms = [o for o in out if o["milestone"]]
est = [o for o in out if (not o["milestone"]) and "Duración estimada" in o["note"]]
print("acciones", len(out), "hitos", len(ms), "críticas", len(crit), "duraciones estimadas", len(est))
print("inicio", min(o["start"] for o in out), "fin", max(o["finish"] for o in out))
print("errores", len(errors))
for e in errors:
    print("  ", e)
json.dump({"crit": [o["code"] for o in crit]}, open("_crit.json", "w"))
