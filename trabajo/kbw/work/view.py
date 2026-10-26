import sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import inv_lib as L
f = pathlib.Path(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 150
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
KW = re.compile(r"document|decid|decisi|borrador|correg|correcci|informe \d|informes? \d|pendiente|conviene|habría que|hay que|sugier|recomiend|equipo|nuestr|campaña|Casares|SADOP|escribir|afirmar|citar|para el texto|capítulo|apartado|cuadro \d|opción|alternativa|descart|cliente|Nick|repo|worker|programa (dice|usa|propone|pone)|en el programa|del programa|al programa", re.I)
h1, blocks = L.parse(f.read_text(encoding="utf-8"))
print("H1:", h1)
for b in blocks:
    if not (lo <= b["line"] <= hi):
        continue
    if b["kind"] == "h":
        print(f"\n{b['line']:>4} {'#'*b['level']} {b['text']}")
        continue
    t = b["text"]
    if b["kind"] == "table":
        rows = b["rows"]
        print(f"{b['line']:>4} [tabla {len(rows)-2} filas] {rows[0][:W]}")
        for r in rows[2:]:
            hit = KW.findall(r) or L.internal_reasons(r)
            if hit:
                print(f"       | {r[:W]}  <<" + ",".join(map(str, hit[:4])))
        continue
    pre = {"p": "", "li": "- ", "quote": "> "}.get(b["kind"], "")
    flag = L.internal_reasons(t)
    print(f"{b['line']:>4} {pre}{t[:W]}{'…' if len(t) > W else ''}" + (f"  <<{flag}" if flag else ""))
    if len(t) > W:
        for s in L.split_sentences(t):
            if (KW.search(s) or L.internal_reasons(s)) and s not in t[:W]:
                print(f"       ~ {s[:300]}")
