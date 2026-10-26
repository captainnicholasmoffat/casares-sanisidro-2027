# -*- coding: utf-8 -*-
"""Arma programa.json desde el HTML final de las secciones (commit c462fcf) y ubica
cada entrada en las hojas de la A4 final (texto extraido hoja por hoja)."""
import json, re, sys, unicodedata, pathlib
from bs4 import BeautifulSoup, NavigableString, Tag

SEC = json.load(open(sys.argv[1], encoding="utf-8"))   # sections.json
A4DIR = pathlib.Path(sys.argv[2])                       # v21/t
OUT = pathlib.Path(sys.argv[3])                         # programa.json

BR = "\u2028"     # marca temporal de <br>


def norm_ws(s):
    s = s.replace("\xa0", " ")
    s = re.sub(r"[ \t\r\n\f\v]+", " ", s)
    s = re.sub(r" ?\u2028 ?", BR, s)
    return s.strip()


def prep(el):
    for br in el.find_all("br"):
        br.replace_with(NavigableString(BR))
    for sp in el.find_all("span", class_="tag"):
        if sp.find_parent("h2") is None:      # las del titulo de apartado van a «etiquetas»
            sp.replace_with(NavigableString(" [" + sp.get_text().strip() + "]"))


def T(el, br="\n\n"):
    s = norm_ws(str(el) if isinstance(el, NavigableString) else el.get_text())
    return s.replace(BR, br).strip()


def heading(el):
    n = el.find("span", class_="n")
    num = n.get_text().strip() if n else None
    tags = [t.get_text().strip() for t in el.find_all("span", class_="tag")]
    for t in el.find_all("span", class_="tag"):
        t.extract()
    if n:
        n.extract()
    return num, T(el, " "), tags


def table_rows(tb):
    rows = []
    for tr in tb.find_all("tr"):
        rows.append([T(c, " ") for c in tr.find_all(["th", "td"])])
    return rows


def rows_text(rows):
    return "\n".join(" | ".join(c for c in r) for r in rows)


def svg_text(svg):
    """textos de un diagrama: los <text> seguidos con la misma x y renglones contiguos forman una frase."""
    parts, cur, cx, cy = [], [], None, None
    for t in svg.find_all("text"):
        x, y = t.get("x"), float(t.get("y"))
        s = T(t, " ")
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
            out.append(T(el, " "))
        elif el.name == "p":
            out.append(T(el, " "))
        elif "mec-pills" in cls:
            out.append(" · ".join(T(s, " ") for s in el.find_all("span", recursive=False)))
        elif el.name == "ol":
            for i, li in enumerate(el.find_all("li", recursive=False), 1):
                out.append(f"{i}. {T(li, ' ')}")
        elif "mec-cards" in cls:
            for d in el.find_all("div", recursive=False):
                out.append(T(d, " "))
    return out


def list_items(el):
    out = []
    numbered = el.name == "ol"
    for i, li in enumerate(el.find_all("li", recursive=False), 1):
        out.append((f"{i}. " if numbered else "• ") + T(li, " "))
    return out


SVG_MAP = {
 "ex02.png":"g_indicadores","ex03.png":"g_universitario","ex04.png":"g_dots",
 "ex05.png":"g_gasto_real","ex06.png":"g_copa","ex07.png":"g_percepcion",
 "ex08.png":"g_cascada","ex09.png":"g_escenarios","ex10.png":"g_rigidez",
 "ex11.png":"g_reformista","ex12.png":"g_tornado","ex13.png":"g_obra",
 "ex14.png":"g_reparto","ex01.png":"g_mapa_zonas","ex15.png":"g_mapa_radios","ex16.png":"g_funcion","ex17.png":"g_variacion",
 "ex18.png":"g_empleo","ex19.png":"g_gas",
}   # igual que doc/build.py: cada grafico del PDF es este SVG
SVGDIR = pathlib.Path(__file__).parent.parent / "svg"


def chart_labels(img_src):
    name = img_src.split("asset:")[-1]
    if name not in SVG_MAP:
        return ""
    svg = BeautifulSoup((SVGDIR / (SVG_MAP[name] + ".svg")).read_text(encoding="utf-8"), "html.parser")
    ts = [norm_ws(t.get_text(" ")) for t in svg.find_all("text")]
    return " · ".join(t for t in ts if t)


CAPS = {
    "introduccion": ("intro", "Introducción"),
    "sintesis": ("proponemos", "Qué proponemos hacer"),
    "cierre": ("cierre", "Para cerrar"),
    "ordenanza": ("anexo", "Anexo · Las ordenanzas que proponemos"),
    "glosario": ("glosario", "Glosario"),
    "metodo": ("metodo", "Nota de método"),
}
ORD_SPECIAL = {"Lo que estas ordenanzas no dicen, y por qué": "anexo-no-dicen",
               "Las metas que no llevan ordenanza, y por qué": "anexo-metas"}
MET_SPECIAL = {"Las notas de cada capítulo": "metodo-notas",
               "Las fuentes de lo que afirma el texto": "metodo-fuentes",
               "Lo que este programa no hace": "metodo-no-hace",
               "Lo que tiene que confirmar un abogado": "metodo-abogado"}

entries = []
stream = []            # (entry, tipo, texto) en el orden del documento, para ubicar en la A4
cur = None
capitulo = None
chap_key = None
pending_fotos = []
open_cuadro = None
rec_n = {}
intro_n = [0]
mode = {"notas": False}
fuentes_rows = []
glos_rows = []


def new_entry(id_, titulo, parent=None, tags=None):
    global cur, open_cuadro
    e = {"id": id_, "capitulo": capitulo, "titulo": titulo, "texto": [], "cuadros": [],
         "fuentes": [], "etiquetas": tags or [], "fotos": [], "subtitulos": []}
    if parent:
        e["_parent"] = parent
    entries.append(e)
    open_cuadro = None
    if parent is None:
        cur = e
    stream.append((e, "titulo", (id_ + " " + titulo) if re.match(r"^\d+(\.\d+)?$", id_) else titulo))
    return e


def para(s, e=None, kind="p"):
    global open_cuadro
    e = e or cur
    if s:
        e["texto"].append(s)
        stream.append((e, kind, s))
        if kind == "h3":
            e["subtitulos"].append({"titulo": s})
    open_cuadro = None


def recuadro(titulo, paras):
    base = cur["id"]
    rec_n[base] = rec_n.get(base, 0) + 1
    e = {"id": f"{base}-r{rec_n[base]}", "capitulo": capitulo, "titulo": titulo, "texto": [],
         "cuadros": [], "fuentes": [], "etiquetas": [], "fotos": [], "subtitulos": [], "_parent": base}
    entries.append(e)
    stream.append((e, "titulo", titulo))
    for p in paras:
        if p:
            e["texto"].append(p)
            stream.append((e, "p", p))


def add_cuadro(c, e=None):
    e = e or cur
    e["cuadros"].append(c)
    stream.append((e, "cuadro", c["titulo"]))
    return c


def foto(s, e=None):
    e = e or cur
    e["fotos"].append(s)
    stream.append((e, "foto", s))


for sec in SEC[1:]:                     # sin el indice
    sid = sec["id"]
    soup = BeautifulSoup(sec["html"], "html.parser")
    prep(soup)
    for el in soup.contents:
        if not isinstance(el, Tag):
            if str(el).strip():
                raise SystemExit(f"texto suelto en {sid}: {str(el)[:80]}")
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
            mode["notas"] = False
            for f in pending_fotos:
                foto(f)
            pending_fotos.clear()
        elif name == "h2":
            num, tit, tags = heading(el)
            if num:
                new_entry(num, tit, tags=tags)
            elif chap_key == "intro":
                intro_n[0] += 1
                new_entry(f"intro-{intro_n[0]}", tit)
            elif chap_key == "anexo":
                m = re.match(r"(\d+) · (.*)", tit)
                new_entry(f"anexo-{m.group(1)}" if m else ORD_SPECIAL[tit], tit)
            elif chap_key == "metodo":
                new_entry(MET_SPECIAL[tit], tit)
                mode["notas"] = tit == "Las notas de cada capítulo"
            else:
                raise SystemExit(f"h2 sin numero inesperado: {tit} en {sid}")
        elif name == "h3":
            h = T(el, " ")
            if mode["notas"]:
                m = re.match(r"Capítulo (\d+) · (.*)", h)
                new_entry(f"metodo-notas-{m.group(1)}", "Las notas de cada capítulo · " + h)
                stream[-1] = (cur, "titulo", h)
            else:
                para(h, kind="h3")
        elif name == "figure":
            cap = el.find("figcaption")
            if cap:
                s = T(cap, " ")
                nxt = el.find_next_sibling()
                if nxt is not None and nxt.name == "h1":
                    pending_fotos.append(s)      # foto de apertura: va con el capitulo que sigue
                else:
                    foto(s)
        elif name == "figcaption":
            foto(T(el, " "))
        elif name == "div" and ("duo" in cls or "hairline" in cls):
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
                stream.append((cur, "cuadro-cap", s))
            else:
                para(s)
        elif name in ("ol", "ul"):
            for s in list_items(el):
                para(s)
        elif name == "div" and "callout" in cls:
            lab = el.find("div", class_="clabel")
            tit = T(lab, " ") if lab else ""
            ps = []
            for k in el.children:
                if not isinstance(k, Tag) or k is lab:
                    continue
                ps += list_items(k) if k.name in ("ol", "ul") else [T(k)]
            recuadro(tit, ps)
            open_cuadro = None
        elif name == "div" and "pull" in cls:
            lab = el.find("div", class_="plabel")
            ps = [T(k) for k in el.children if isinstance(k, Tag) and k is not lab]
            if lab:
                recuadro(T(lab, " "), ps)
                open_cuadro = None
            else:
                for s in ps:
                    para(s)
        elif name == "div" and "ex" in cls:
            lab = T(el.find("div", class_="exlabel"), " ")
            tit = T(el.find("div", class_="extitle"), " ")
            sub = el.find("div", class_="exsub")
            kind, n = lab.split(" ", 1)
            kind = {"GRÁFICO": "Gráfico", "CUADRO": "Cuadro"}.get(kind, kind.capitalize())
            c = {"titulo": f"{kind} {n} · {tit}", "texto": T(sub) if sub else "",
                 "_kind": "chart" if el.find("div", class_="chart") else "head"}
            for p in el.find_all("p", class_="cap"):
                c["texto"] = (c["texto"] + "\n\n" + T(p)).strip()
            img = el.find("img")
            if img is not None and el.find("div", class_="chart"):
                lab = chart_labels(img.get("src", ""))
                if lab:
                    c["texto_del_grafico"] = lab
            add_cuadro(c)
            open_cuadro = c
        elif name == "table":
            rows = table_rows(el)
            if chap_key == "glosario":
                glos_rows.extend(rows)
                stream.append((None, "GLOS", ""))
                continue
            if cur["id"] == "metodo-fuentes":
                fuentes_rows.extend(rows)
                continue
            oc = open_cuadro
            if oc is not None and oc.get("_kind") == "head" and not oc.get("_rows"):
                oc["_rows"] = rows
                oc["texto"] = ((oc["texto"] + "\n\n") if oc["texto"] else "") + rows_text(rows)
            elif cur["cuadros"] and cur["cuadros"][-1].get("_rows") and cur["cuadros"][-1]["_rows"][0] == rows[0]:
                # continuacion de un cuadro partido entre paginas de pantalla: el encabezado repetido no se copia
                c = cur["cuadros"][-1]
                c["_rows"] += rows[1:]
                c["texto"] += "\n" + rows_text(rows[1:])
                open_cuadro = c
            else:
                raise SystemExit(f"cuadro sin rotulo en {sid}: {rows[0]}")
            for r in rows[1:]:
                stream.append((cur, "fila", " ".join(r)))
        elif name == "div" and "mec" in cls:
            open_cuadro["texto"] = (open_cuadro["texto"] + "\n\n" + "\n\n".join(mec_text(el))).strip()
        elif name == "div" and "diag" in cls:
            open_cuadro["texto"] = (open_cuadro["texto"] + "\n\n" + "\n\n".join(svg_text(el.find("svg")))).strip()
        else:
            raise SystemExit(f"elemento sin tratar: {name} {cls} en {sid}")

# ---- glosario: una entrada por termino
glos = next(e for e in entries if e["id"] == "glosario")
gi = entries.index(glos)
assert glos_rows[0] == ["Palabra", "Qué quiere decir"], glos_rows[0]
new, used = [], set()
for term, defin in glos_rows[1:]:
    slug = unicodedata.normalize("NFKD", term).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    assert slug not in used, slug
    used.add(slug)
    g = {"id": f"glosario-{slug}", "capitulo": "Glosario", "titulo": term, "texto": [defin], "cuadros": [],
         "fuentes": [], "etiquetas": [], "fotos": [], "subtitulos": []}
    new.append(g)
entries[gi + 1:gi + 1] = new
k = next(i for i, x in enumerate(stream) if x[1] == "GLOS")
stream[k:k + 1] = [(g, "glos", g["titulo"] + " " + g["texto"][0]) for g in new]

# ---- fuentes del texto, repartidas por apartado
by_id = {e["id"]: e for e in entries}
fu_hdr = fuentes_rows[0]
assert fu_hdr == ["Dónde", "Fuente"], fu_hdr
n_fuentes = 0
fuente_items = []
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
    item = {"texto": f"{donde}: {fuente}", "_key": donde + " " + fuente}
    by_id[k]["fuentes"].append(item)
    fuente_items.append(item)
    n_fuentes += 1

# ---- recuadros inmediatamente despues de su apartado
pend = {}
for e in entries:
    if "_parent" in e:
        pend.setdefault(e["_parent"], []).append(e)
ordered = []
for e in entries:
    if "_parent" in e:
        continue
    ordered.append(e)
    ordered.extend(pend.get(e["id"], []))
assert len(ordered) == len(entries)
entries = ordered

# ---- ubicar en la A4
HEAD = re.compile(r"^P R O G R A M A D E G O B I E R N O · PA R T I D O D E S A N I S I D R O\s*$", re.M)
FOOT = re.compile(r"^(Programa de gobierno · San Isidro 2027|Página \d+ de \d+)\s*$", re.M)


def squash(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", s)


NP = len(list(A4DIR.glob("*.txt")))
offs, big = [], []
pos = 0
for p in range(1, NP + 1):
    t = (A4DIR / f"{p}.txt").read_text(encoding="utf-8")
    t = FOOT.sub("", HEAD.sub("", t))
    q = squash(t)
    offs.append((pos, pos + len(q), p))
    big.append(q)
    pos += len(q)
BIG = "".join(big)
FIRST_BODY = next(o[0] for o in offs if o[2] == 5)    # despues del indice


def sheet_at(i):
    for a, b, p in offs:
        if a <= i < b:
            return p
    return None


def locate(s, ptr, slack=6000, minlen=8):
    q = squash(s)
    if len(q) < minlen:
        return None
    keys = [q[:50]] if len(q) <= 50 else [q[:50], q[len(q) // 2:len(q) // 2 + 40], q[-40:]]
    for k in keys:
        i = BIG.find(k, max(FIRST_BODY, ptr - slack))
        if i >= 0 and i - ptr < 400000:
            j = i - (q.find(k) if k != q[:50] else 0)
            return max(j, FIRST_BODY)
    return None


# el stream ya esta en el orden del documento (los recuadros, donde aparecen; el glosario, en su lugar)
ptr = FIRST_BODY
miss = []
loc = {}
for e, kind, s in stream:
    if kind == "foto":
        # las fotos pueden cambiar de lugar en la A4 (subir una foto, la de apertura al final del capitulo anterior)
        i = locate(s, ptr, slack=30000)
        if i is None or abs(i - ptr) > 60000:
            miss.append((e["id"], kind, s[:80]))
            continue
    else:
        i = locate(s, ptr, minlen=5 if kind in ("titulo", "h3") else 8)
        if i is None:
            miss.append((e["id"], kind, s[:80]))
            continue
        if i < ptr - 6000:
            miss.append((e["id"], kind + "-atras", s[:80]))
            continue
        ptr = max(ptr, i)
    sh = sheet_at(i)
    if kind != "foto":
        loc.setdefault(id(e), []).append(sh)
    if kind == "h3":
        for st in e["subtitulos"]:
            if st["titulo"] == s and "hoja_a4" not in st:
                st["hoja_a4"] = sh
                break
# fuentes: aparte, en las hojas de las fuentes
ptrf = next(o[0] for o in offs if o[2] == 132)
for it in fuente_items:
    i = locate(it["_key"], ptrf, slack=20000)
    if i is None:
        miss.append(("fuente", "fuente", it["_key"][:80]))
        continue
    ptrf = max(ptrf, i)
    it["hoja"] = sheet_at(i)

for e in entries:
    hs = loc.get(id(e), [])
    e["hoja_a4"] = hs[0] if hs else None
    e["hoja_a4_fin"] = max(hs) if hs else None

# ---- orden de los bloques dentro de cada entrada (para la web)
ORDEN = {}
PC = {}
CC = {}
for e, kind, s_ in stream:
    if e is None:
        continue
    if "_parent" in e:
        if kind == "titulo":
            ORDEN.setdefault(e["_parent"], []).append(["box", e["id"]])
        continue
    k = e["id"]
    if kind in ("p", "h3"):
        ORDEN.setdefault(k, []).append([kind, PC.get(k, 0)]); PC[k] = PC.get(k, 0) + 1
    elif kind == "foto":
        ORDEN.setdefault(k, []).append(["foto", s_])
    elif kind == "cuadro":
        ORDEN.setdefault(k, []).append(["cuadro", CC.get(k, 0)]); CC[k] = CC.get(k, 0) + 1
# ---- salida
out = []
for e in entries:
    if not (e["texto"] or e["cuadros"]):
        if e["id"] == "metodo-notas":      # solo el titulo: cada capitulo es su propia entrada
            continue
        raise SystemExit("entrada vacia " + e["id"])
    d = {"id": e["id"], "capitulo": e["capitulo"], "titulo": e["titulo"],
         "hoja_a4": e["hoja_a4"], "hoja_a4_fin": e["hoja_a4_fin"],
         "texto": "\n\n".join(e["texto"]),
         "cuadros": [dict({"titulo": c["titulo"], "texto": c["texto"]},
                          **({"texto_del_grafico": c["texto_del_grafico"]} if c.get("texto_del_grafico") else {}))
                     for c in e["cuadros"]],
         "fuentes": "\n\n".join(f["texto"] for f in e["fuentes"])}
    if e["fuentes"]:
        d["fuentes_hojas_a4"] = sorted({f.get("hoja") for f in e["fuentes"] if f.get("hoja")})
    if e["etiquetas"]:
        d["etiquetas"] = e["etiquetas"]
    if e["subtitulos"]:
        d["subtitulos"] = e["subtitulos"]
    if e["fotos"]:
        d["pies_de_foto"] = e["fotos"]
    if "_parent" in e:
        d["recuadro_de"] = e["_parent"]
    if e["id"] in ORDEN:
        d["orden"] = ORDEN[e["id"]]
    out.append(d)
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(len(out), "entradas;", n_fuentes, "filas de fuentes;", len(new), "terminos del glosario")
print("bloques sin ubicar en la A4:", len(miss))
for m in miss:
    print("   ", m)
for d in out:
    print(f'{d["id"]:<30} h{d["hoja_a4"]}-{d["hoja_a4_fin"]} t{len(d["texto"]):>6} c{len(d["cuadros"])} f{len(d["fuentes"]):>5}  {d["titulo"][:55]}')
