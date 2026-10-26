"""Agrega a data/programa.json las negritas del programa (<b> bordó, <span class="sg"> verde, <i>) como rangos
de caracteres por párrafo: "marcas": {"<n de párrafo>": [[inicio, fin, "b"|"sg"|"i"], ...]}.
Uso: python3 -I merge_marcas.py <sections.json del commit c462fcf>"""
import copy, json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
BR = " "
def norm_ws(s):
    s = s.replace("\xa0", " "); s = re.sub(r"[ \t\r\n\f\v]+", " ", s); s = re.sub(r" ?  ?", BR, s); return s.strip()
SENT = {"b": ("", ""), "sg": ("", ""), "i": ("", "")}
OPEN = {v[0]: k for k, v in SENT.items()}; CLOSE = {v[1]: k for k, v in SENT.items()}
def pieces(el, br):
    c = copy.copy(el)
    for br_ in c.find_all("br"): br_.replace_with(NavigableString(BR))
    for sp in c.find_all("span", class_="tag"): sp.replace_with(NavigableString(" [" + sp.get_text().strip() + "]"))
    for tag, k in (("b", "b"), ("strong", "b"), ("i", "i"), ("em", "i")):
        for x in c.find_all(tag): x.insert_before(SENT[k][0]); x.insert_after(SENT[k][1])
    for x in c.find_all("span", class_="sg"): x.insert_before(SENT["sg"][0]); x.insert_after(SENT["sg"][1])
    s = norm_ws(c.get_text()).replace(BR, br).strip()
    out = []
    for part in s.split("\n\n"):
        plain, rng, stack = [], [], []
        for ch in part:
            if ch in OPEN: stack.append((OPEN[ch], len(plain)))
            elif ch in CLOSE:
                k = CLOSE[ch]
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j][0] == k:
                        _, a = stack.pop(j)
                        if len(plain) > a: rng.append([a, len(plain), k])
                        break
            else: plain.append(ch)
        p = "".join(plain)
        # recortar espacios que quedaron dentro de la marca
        fixed = []
        for a, b, k in rng:
            while a < b and p[a] == " ": a += 1
            while b > a and p[b - 1] == " ": b -= 1
            if b > a: fixed.append([a, b, k])
        out.append((p.strip(), fixed, len(p) - len(p.lstrip())))
    return out
SEC = json.load(open(sys.argv[1], encoding="utf-8"))
D = {}
for sec in SEC:
    soup = BeautifulSoup(sec["html"], "html.parser")
    for el in soup.find_all(["p", "li", "div", "td", "th"]):
        if not el.find(["b", "strong", "i", "em"]) and not el.find("span", class_="sg"): continue
        if el.name == "div" and el.find(["p", "li", "div"]): continue
        for plain, rng, lead in pieces(el, " " if el.name in ("li", "td", "th") else "\n\n"):
            if rng and plain not in D:
                D[plain] = [[a - lead, b - lead, k] for a, b, k in rng]
P = Path(__file__).resolve().parent / "data" / "programa.json"
web = json.loads(P.read_text())
tot = hit = 0
for e in web:
    m = {}
    if not e["texto"]: e.pop("marcas", None); continue
    for i, p in enumerate(e["texto"].split("\n\n")):
        r = D.get(p); off = 0
        if r is None:
            mm = re.match(r"^(• |\d+\. )", p)
            if mm and p[mm.end():] in D: r, off = D[p[mm.end():]], mm.end()
        if r:
            ok = [[a + off, b + off, k] for a, b, k in r if 0 <= a + off < b + off <= len(p)]
            if ok: m[str(i)] = ok; hit += len(ok)
    tot += 1
    if m: e["marcas"] = m
    else: e.pop("marcas", None)
P.write_text(json.dumps(web, ensure_ascii=False, indent=1))
print("marcas:", hit, "en", sum(1 for e in web if e.get("marcas")), "entradas; elementos con marcas en el HTML:", len(D))
