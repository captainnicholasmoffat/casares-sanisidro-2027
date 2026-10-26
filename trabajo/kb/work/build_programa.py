# -*- coding: utf-8 -*-
"""Arma programa.json desde el HTML final de las secciones (c462fcf) y ubica cada entrada en la A4."""
import json, re, sys, unicodedata, pathlib
from bs4 import BeautifulSoup, NavigableString, Tag

WORK = pathlib.Path(__file__).parent
SEC = json.load(open(WORK / "sections.json"))
A4DIR = pathlib.Path(sys.argv[1])          # v21/t
OUT = pathlib.Path(sys.argv[2])            # programa.json

BR = ""


def norm_ws(s):
    s = re.sub(r"\s+", " ", s)
    s = s.replace(" " + BR, BR).replace(BR + " ", BR)
    return s.replace(BR, "\n").strip()


def prep(el):
    """<br> -> salto; etiquetas en linea -> [Etiqueta]."""
    for br in el.find_all("br"):
        br.replace_with(NavigableString(BR))
    for sp in el.find_all("span", class_="tag"):
        sp.replace_with(NavigableString(" [" + sp.get_text().strip() + "]"))


def T(el):
    if isinstance(el, NavigableString):
        return norm_ws(str(el))
    return norm_ws(el.get_text())


def heading(el):
    """titulo de un h1/h2 sin el numero; devuelve (numero, titulo, etiquetas)."""
    n = el.find("span", class_="n")
    num = n.get_text().strip() if n else None
    if n:
        n.extract()
    t = T(el)
    m = re.match(r"^(.*?)((?:\s*\[[^\]]+\])*)$", t)
    tags = re.findall(r"\[([^\]]+)\]", m.group(2))
    return num, m.group(1).strip(), tags


def table_rows(tb):
    rows = []
    for tr in tb.find_all("tr"):
        cells = [T(c) for c in tr.find_all(["th", "td"])]
        rows.append(cells)
    return rows


def rows_text(rows):
    return "\n\n".join(" | ".join(r) for r in rows)


def svg_text(svg):
    """textos del diagrama: los <text> seguidos con la misma x y renglones contiguos forman una frase."""
    parts, cur, cx, cy = [], [], None, None
    for t in svg.find_all("text"):
        x, y = t.get("x"), float(t.get("y"))
        s = norm_ws(t.get_text())
        if cur and x == cx and 0 < y - cy <= 17:
            cur.append(s)
        else:
            if cur:
                parts.append(" ".join(cur))
            cur = [s]
        cx, cy = x, y
    if cur:
        parts.append(" ".join(cur))
    return parts


def mec_text(mec):
    out = []
    for el in mec.descendants:
        if not isinstance(el, Tag):
            continue
        cls = el.get("class", [])
        if "mec-lab" in cls or "mec-sub" in cls:
            out.append(T(el))
        elif el.name == "p":
            out.append(T(el))
        elif "mec-pills" in cls:
            out.append(" · ".join(T(s) for s in el.find_all("span", recursive=False)))
        elif el.name == "ol":
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                out.append(f"{i}. {T(li)}")
        elif "mec-cards" in cls:
            for d in el.find_all("div", recursive=False):
                out.append(T(d))
    return out


CAPS = {
    "introduccion": ("intro", "Introducción"),
    "sintesis": ("proponemos", "Qué proponemos hacer"),
    "cierre": ("cierre", "Para cerrar"),
    "ordenanza": ("anexo", "Anexo · Las ordenanzas que proponemos"),
    "glosario": ("glosario", "Glosario"),
    "metodo": ("metodo", "Nota de método"),
}

entries = []
cur = None
capitulo = None
chap_key = None
pending_paras = []         # pies de foto antes de un h1
open_cuadro = None         # cuadro que todavia puede recibir filas o Fuente/Nota
rec_n = {}
intro_n = [0]
mode_notas = [False]


def new_entry(id_, titulo, parent=None):
    global cur, open_cuadro
    e = {"id": id_, "capitulo": capitulo, "titulo": titulo, "hoja_a4": None,
         "texto": [], "cuadros": [], "fuentes": ""}
    entries.append(e)
    open_cuadro = None
    if parent is None:
        cur = e
    return e


def para(s, e=None):
    global open_cuadro
    e = e or cur
    if s:
        e["texto"].append(s)
    open_cuadro = None


def recuadro(titulo, paras):
    base = cur["id"]
    rec_n[base] = rec_n.get(base, 0) + 1
    e = {"id": f"{base}-r{rec_n[base]}", "capitulo": capitulo, "titulo": titulo, "hoja_a4": None,
         "texto": [p for p in paras if p], "cuadros": [], "fuentes": "", "_parent": base}
    entries.append(e)


def list_items(el):
    out = []
    numbered = el.name == "ol"
    for i, li in enumerate(el.find_all("li", recursive=False), 1):
        out.append((f"{i}. " if numbered else "• ") + T(li))
    return out


ORD_SPECIAL = {"Lo que estas ordenanzas no dicen, y por qué": "anexo-no-dicen",
               "Las metas que no llevan ordenanza, y por qué": "anexo-metas"}
MET_SPECIAL = {"Las notas de cada capítulo": "metodo-notas",
               "Las fuentes de lo que afirma el texto": "metodo-fuentes",
               "Lo que este programa no hace": "metodo-no-hace",
               "Lo que tiene que confirmar un abogado": "metodo-abogado"}

fuentes_rows = []
glos_rows = []

for sec in SEC[1:]:                     # sin el indice
    sid = sec["id"]
    soup = BeautifulSoup(sec["html"], "html.parser")
    prep(soup)
    for el in soup.contents:
        if not isinstance(el, Tag):
            continue
        name, cls = el.name, el.get("class", [])
        if name == "h1":
            num, tit, _ = heading(el)
            if num:
                capitulo = f"{num} · {tit}"
                chap_key = num
                new_entry(num, tit)
            else:
                key, cap = CAPS[sid]
                capitulo = cap
                chap_key = key
                new_entry(key, tit)
            mode_notas[0] = False
            for p in pending_paras:
                para(p)
            pending_paras.clear()
        elif name == "h2":
            num, tit, tags = heading(el)
            if num:
                new_entry(num, tit)
                if tags:
                    para(" ".join(f"[{t}]" for t in tags))
            elif chap_key == "intro":
                intro_n[0] += 1
                new_entry(f"intro-{intro_n[0]}", tit)
            elif chap_key == "anexo":
                m = re.match(r"(\d+) · (.*)", tit)
                if m:
                    new_entry(f"anexo-{m.group(1)}", tit)
                else:
                    new_entry(ORD_SPECIAL[tit], tit)
            elif chap_key == "metodo":
                new_entry(MET_SPECIAL[tit], tit)
                mode_notas[0] = tit == "Las notas de cada capítulo"
            else:
                raise SystemExit(f"h2 sin numero inesperado: {tit} en {sid}")
        elif name == "h3":
            h = T(el)
            if mode_notas[0]:
                m = re.match(r"Capítulo (\d+) · (.*)", h)
                new_entry(f"metodo-notas-{m.group(1)}", "Las notas de cada capítulo · " + h)
            else:
                para(h)
        elif name == "figure":
            cap = el.find("figcaption")
            if cap:
                s = T(cap)
                nxt = el.find_next_sibling()
                if nxt is not None and nxt.name == "h1":
                    pending_paras.append(s)
                else:
                    para(s)
        elif name == "figcaption":
            para(T(el))
        elif name == "div" and "duo" in cls:
            pass
        elif name == "div" and "hairline" in cls:
            pass
        elif name == "div" and ("cols" in cls or "note" in cls):
            for k in el.children:
                if not isinstance(k, Tag):
                    continue
                if k.name in ("ol", "ul"):
                    for s in list_items(k):
                        para(s)
                else:
                    para(T(k))
        elif name == "div" and "stand" in cls:
            para(T(el))
        elif name == "p":
            s = T(el)
            if "cap" in cls and open_cuadro is not None and re.match(r"(Fuente|Nota)s?:", s):
                open_cuadro["texto"] += "\n\n" + s
            else:
                para(s)
        elif name in ("ol", "ul"):
            for s in list_items(el):
                para(s)
        elif name == "div" and "callout" in cls:
            lab = el.find("div", class_="clabel")
            tit = T(lab) if lab else ""
            ps = []
            for k in el.children:
                if not isinstance(k, Tag) or k is lab:
                    continue
                if k.name in ("ol", "ul"):
                    ps += list_items(k)
                else:
                    ps.append(T(k))
            recuadro(tit, ps)
            open_cuadro = None
        elif name == "div" and "pull" in cls:
            lab = el.find("div", class_="plabel")
            ps = [T(k) for k in el.children if isinstance(k, Tag) and k is not lab]
            if lab:
                recuadro(T(lab), ps)
                open_cuadro = None
            else:
                for s in ps:
                    para(s)
        elif name == "div" and "ex" in cls:
            lab = T(el.find("div", class_="exlabel"))
            tit = T(el.find("div", class_="extitle"))
            sub = el.find("div", class_="exsub")
            kind, n = lab.split(" ", 1) if " " in lab else (lab, "")
            kind = kind.capitalize().replace("GRÁFICO".capitalize(), "Gráfico")
            c = {"titulo": f"{kind} {n} · {tit}", "texto": T(sub) if sub else ""}
            for p in el.find_all("p", class_="cap"):
                c["texto"] = (c["texto"] + "\n\n" + T(p)).strip()
            cur["cuadros"].append(c)
            open_cuadro = c
            c["_kind"] = "chart" if el.find("div", class_="chart") else "head"
        elif name == "table":
            rows = table_rows(el)
            if chap_key == "glosario":
                glos_rows.extend(rows)
                continue
            if cur["id"] == "metodo-fuentes":
                fuentes_rows.extend(rows)
            oc = open_cuadro
            if oc is not None and oc.get("_kind") == "head" and not oc.get("_rows"):
                oc["_rows"] = rows
                oc["texto"] = ((oc["texto"] + "\n\n") if oc["texto"] else "") + rows_text(rows)
            elif cur["cuadros"] and cur["cuadros"][-1].get("_rows") and cur["cuadros"][-1]["_rows"][0] == rows[0]:
                # continuacion de un cuadro partido entre paginas: el encabezado se repite, no se copia
                c = cur["cuadros"][-1]
                c["_rows"] += rows[1:]
                c["texto"] += "\n\n" + rows_text(rows[1:])
                open_cuadro = c
            else:
                c = {"titulo": cur["texto"][-1] if cur["texto"] else cur["titulo"], "texto": rows_text(rows), "_rows": rows}
                cur["cuadros"].append(c)
                open_cuadro = c
        elif name == "div" and "mec" in cls:
            oc = open_cuadro
            oc["texto"] = (oc["texto"] + "\n\n" + "\n\n".join(mec_text(el))).strip()
        elif name == "div" and "diag" in cls:
            oc = open_cuadro
            oc["texto"] = (oc["texto"] + "\n\n" + "\n\n".join(svg_text(el.find("svg")))).strip()
        else:
            raise SystemExit(f"elemento sin tratar: {name} {cls} en {sid}")

# ---- glosario: una entrada por termino
glos = [e for e in entries if e["id"] == "glosario"][0]
gi = entries.index(glos)
hdr, body = glos_rows[0], glos_rows[1:]
new = []
used = set()
for term, defin in body:
    slug = unicodedata.normalize("NFKD", term).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    while slug in used:
        slug += "-2"
    used.add(slug)
    new.append({"id": f"glosario-{slug}", "capitulo": "Glosario", "titulo": term, "hoja_a4": None,
                "texto": [defin], "cuadros": [], "fuentes": ""})
entries[gi + 1:gi + 1] = new

# ---- fuentes del texto, repartidas por apartado
by_id = {e["id"]: e for e in entries}
fu_hdr = fuentes_rows[0]
asignadas = {}
for r in fuentes_rows[1:]:
    if r == fu_hdr:
        continue
    donde, fuente = r
    m = re.match(r"(\d+\.\d+) · ", donde)
    if m:
        k = m.group(1)
    elif donde.startswith("Qué proponemos hacer"):
        k = "proponemos"
    else:
        raise SystemExit("fuente sin destino: " + donde)
    asignadas.setdefault(k, []).append(f"{donde}: {fuente}")
for k, v in asignadas.items():
    by_id[k]["fuentes"] = "\n\n".join(v)

# ---- recuadros despues de su apartado (orden del documento por apartado)
ordered = []
pend = {}
for e in entries:
    if "_parent" in e:
        pend.setdefault(e["_parent"], []).append(e)
seen_parent = []
for e in entries:
    if "_parent" in e:
        continue
    ordered.append(e)
    ordered.extend(pend.get(e["id"], []))
assert len(ordered) == len(entries)
entries = ordered

# ---- ubicar cada entrada en la A4
HEAD = re.compile(r"^P R O G R A M A D E G O B I E R N O · PA R T I D O D E S A N I S I D R O\s*$", re.M)
FOOT = re.compile(r"^(Programa de gobierno · San Isidro 2027|Página \d+ de \d+)\s*$", re.M)


def squash(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", s)


pages = {}
for f in A4DIR.glob("*.txt"):
    t = f.read_text(encoding="utf-8")
    t = HEAD.sub("", t)
    t = FOOT.sub("", t)
    pages[int(f.stem)] = squash(t)
NP = max(pages)


def find_page(s, frm, tail=False):
    q = squash(s)
    if len(q) < 18:
        return None
    keys = [q[-45:]] if tail else [q[:45]]
    keys += [q[len(q) // 2: len(q) // 2 + 40]]
    for key in keys:
        hits = [p for p in range(5, NP + 1) if key in pages[p]]
        if hits:
            ok = [p for p in hits if p >= frm]
            return ok[0] if ok else hits[0]
    return None


prev = 5
for e in entries:
    blocks = list(e["texto"]) + [c["texto"] for c in e["cuadros"]]
    start = None
    if re.match(r"^\d+\.\d+$", e["id"]):
        start = find_page(e["id"] + " " + e["titulo"], max(5, prev - 1))
    for b in ([] if start else blocks):
        start = find_page(b, max(1, prev - 1))
        if start:
            break
    if start is None:
        start = find_page(e["titulo"], max(1, prev - 1))
    end = None
    for b in reversed(blocks):
        end = find_page(b, start or prev, tail=True)
        if end:
            break
    e["hoja_a4"] = start
    e["hoja_a4_fin"] = end if end and start and end >= start else start
    if start:
        prev = start

# ---- salida
out = []
entries = [e for e in entries if e["texto"] or e["cuadros"]]
for e in entries:
    cu = [{"titulo": c["titulo"], "texto": c["texto"]} for c in e["cuadros"]]
    out.append({"id": e["id"], "capitulo": e["capitulo"], "titulo": e["titulo"],
                "hoja_a4": e["hoja_a4"], "hoja_a4_fin": e["hoja_a4_fin"],
                "texto": "\n\n".join(e["texto"]), "cuadros": cu, "fuentes": e["fuentes"]})
OUT.parent.mkdir(parents=True, exist_ok=True)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "entradas")
for e in out:
    print(f'{e["id"]:<28} h{e["hoja_a4"]}-{e["hoja_a4_fin"]}  t{len(e["texto"]):>6} c{len(e["cuadros"])} f{len(e["fuentes"])}  {e["titulo"][:60]}')
