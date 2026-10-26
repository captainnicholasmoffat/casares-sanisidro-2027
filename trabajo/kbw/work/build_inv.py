# -*- coding: utf-8 -*-
"""Arma investigaciones.json: pasajes curados de los informes.
Uso: python3 build_inv.py <dir_informes> <programa.json> <salida.json> [--review CODE]"""
import json, re, sys, pathlib, importlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import inv_lib as L
import cfg_inv as C

IND = pathlib.Path(sys.argv[1])
PROG = json.load(open(sys.argv[2], encoding="utf-8"))
OUT = pathlib.Path(sys.argv[3])
REVIEW = sys.argv[sys.argv.index("--review") + 1] if "--review" in sys.argv else None
DUMP = "--dump" in sys.argv

MIN_W, MAX_W = 150, 400

log = {}          # code -> lista de (motivo, texto) de lo que se saco


def code_of(fn):
    m = re.match(r"INFORME_(\d+)_", fn)
    if m:
        return m.group(1)
    return fn.split("_")[0]


def clean_head(t):
    t = re.sub(r"\s*\((lo más importante|importantes) para el documento[^)]*\)", "", t)
    t = re.sub(r";? ?fuentes en `[^`]*`( y `[^`]*`)?", "", t)
    t = re.sub(r"\s*`[^`]*/`", "", t)
    t = re.sub(r"\s*\[\s*\]", "", t)
    return t.strip()


def match_any(pats, s):
    return any(re.search(p, s) for p in pats)


def curate(code, text, cfg):
    h1, blocks = L.parse(text)
    drops = log.setdefault(code, [])
    dsec = C.GENERIC_DROP_SECS + cfg.get("drop_secs", [])
    allow = cfg.get("allow", [])
    out = []
    dropped_li_indent = None
    drop_list_after = False
    gblocks = C.GENERIC_DROP_BLOCKS + cfg.get("drop_blocks", [])
    for b in blocks:
        # la lista que sigue a un rotulo que se saco («Lo ya decidido por el cliente:»), tambien se va
        if b["kind"] == "li" and drop_list_after:
            drops.append(("lista de un rótulo sacado", b["text"][:300]))
            continue
        if b["kind"] != "li":
            drop_list_after = False
        # los subitems de un item que se saco, tambien se van
        if b["kind"] == "li" and dropped_li_indent is not None and b.get("indent", 0) > dropped_li_indent:
            drops.append(("subitem de un item sacado", b["text"][:300]))
            continue
        if b["kind"] != "li" or (dropped_li_indent is not None and b.get("indent", 0) <= dropped_li_indent):
            dropped_li_indent = None
        for pat in C.GENERIC_STRIP_RE + cfg.get("strip_re", []):
            if b["kind"] != "h":
                b = dict(b, text=re.sub(pat, "", b["text"]))
                if b["kind"] == "table":
                    b["rows"] = [re.sub(pat, "", r) for r in b["rows"]]
        titles = [t for _, t in b["path"]]
        hit = [t for t in titles if match_any(dsec, t)]
        if hit:
            if b["kind"] == "h" and b["text"] == hit[0]:
                drops.append(("sección interna o de proceso", b["text"]))
            continue
        raw = b["text"]
        if b["kind"] != "h" and match_any([re.escape(x) for x in gblocks], raw):
            drops.append(("bloque", raw[:300]))
            if b["kind"] == "li":
                dropped_li_indent = b.get("indent", 0)
            elif re.search(r":\**\s*$", raw.strip()):
                drop_list_after = True
            continue
        if b["kind"] == "h":
            out.append(dict(b, text=L.inline_clean(clean_head(raw))))
            continue
        if b["kind"] == "table":
            rows = [r for r in b["rows"] if not re.match(r"^\|?\s*:?-{2,}", r.replace(" ", ""))]
            keep = []
            for k, r in enumerate(rows):
                why = L.internal_reasons(r, allow)
                if match_any([re.escape(x) for x in cfg.get("drop_rows", [])], r):
                    why.append("fila de proceso")
                if why and k > 0:
                    drops.append(("fila: " + ",".join(why), r[:300]))
                    continue
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                keep.append(" | ".join(L.inline_clean(c) for c in cells))
            if len(keep) > 1:
                out.append(dict(b, rows=keep, text="\n".join(keep)))
            continue
        sents = L.split_sentences(raw)
        kept = []
        for s in sents:
            why = L.internal_reasons(s, allow)
            if match_any([re.escape(x) for x in C.GENERIC_DROP_SENTS + cfg.get("drop_sents", [])], s):
                why.append("oración de proceso")
            if why:
                drops.append(("oración: " + ",".join(why), s[:300]))
                continue
            kept.append(s)
        if not kept:
            if b["kind"] == "li":
                dropped_li_indent = b.get("indent", 0)
            elif re.search(r":\**\s*$", raw.strip()):
                drop_list_after = True
            continue
        t = " ".join(kept)
        for x in cfg.get("strip", []):
            t = t.replace(x, "")
        t = L.inline_clean(t)
        if not t or re.fullmatch(r"[\W\d]*", t):
            continue
        if b["kind"] == "li":
            ind = "  " * (b.get("indent", 0) // 2)
            mk = b["marker"] if re.match(r"\d", b["marker"]) else "-"
            t = f"{ind}{mk} {t}"
        out.append(dict(b, text=t))
    clean = []
    for k, b in enumerate(out):
        nxt = out[k + 1] if k + 1 < len(out) else None
        if b["kind"] == "p" and b["text"].rstrip().endswith(":") and (nxt is None or nxt["kind"] not in ("li", "table")):
            drops.append(("rótulo sin contenido", b["text"][:200]))
            continue
        clean.append(b)
    return h1, clean


def section_key(b):
    return tuple(b["path"])


def top_of(path):
    """los niveles 1 y el primer nivel 2: el «apartado» dentro del cual se pueden juntar piezas"""
    out = []
    for lv, t in path:
        out.append((lv, t))
        if lv >= 2:
            break
    return tuple(out)


def btext(bl):
    parts, prev = [], None
    for b in bl:
        k = b["kind"]
        sep = "\n" if (prev == k and k in ("li", "row")) else "\n\n"
        parts.append((sep if parts else "") + b["text"])
        prev = k
    return "".join(parts)


def atoms_of(b):
    """un bloque en piezas minimas: filas de tabla (con su encabezado), oraciones de un parrafo largo"""
    if b["kind"] == "table":
        hdr, rows = b["rows"][0], b["rows"][1:]
        return [dict(kind="row", text=r, hdr=hdr, tid=id(b)) for r in rows]
    if L.words(b["text"]) > MAX_W:
        ss = L.split_sentences(b["text"])
        out, grp = [], []
        for x in ss:
            if grp and L.words(" ".join(grp + [x])) > MAX_W // 2:
                out.append(dict(kind=b["kind"], text=" ".join(grp)))
                grp = []
            grp.append(x)
        if grp:
            out.append(dict(kind=b["kind"], text=" ".join(grp)))
        return out
    return [dict(kind=b["kind"], text=b["text"])]


def pack(atoms):
    """reparte las piezas en grupos parejos de hasta MAX_W; en cada grupo una tabla lleva su encabezado"""
    total = sum(L.words(a["text"]) for a in atoms)
    k = max(1, -(-total // MAX_W))
    target = total / k
    groups, cur, cw = [], [], 0
    for a in atoms:
        w = L.words(a["text"])
        if a["kind"] == "row" and not any(x.get("tid") == a["tid"] for x in cur):
            w += L.words(a["hdr"])
        if cur and (cw + w > MAX_W or (cw >= target and len(groups) < k - 1)):
            groups.append(cur)
            cur, cw = [], 0
        cur.append(a)
        cw += w
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        bl, seen = [], set()
        for a in g:
            if a["kind"] == "row" and a["tid"] not in seen:
                seen.add(a["tid"])
                bl.append(dict(kind="row", text=a["hdr"]))
            bl.append(a)
        out.append(bl)
    return out


def chunk(blocks):
    """Junta los bloques en pasajes de 150 a 400 palabras, sin mezclar apartados distintos."""
    units = []
    for b in blocks:
        if b["kind"] == "h":
            units.append(dict(path=section_key(b), blocks=[]))
        else:
            if not units or units[-1]["path"] != section_key(b):
                units.append(dict(path=section_key(b), blocks=[]))
            units[-1]["blocks"].append(b)
    units = [u for u in units if u["blocks"]]
    pieces = []
    for u in units:
        atoms = [a for b in u["blocks"] for a in atoms_of(b)]
        for g in pack(atoms):
            pieces.append(dict(path=u["path"], blocks=g))
    # juntar piezas chicas con la anterior del mismo apartado (o de cualquiera, si es muy chica)
    passages = []
    for p in pieces:
        w = L.words(btext(p["blocks"]))
        if passages:
            last = passages[-1]
            lw = L.words(btext(last["blocks"]))
            same = top_of(last["paths"][0]) == top_of(p["path"])
            same_h1 = last["paths"][0][:1] == p["path"][:1]
            tiny = min(lw, w) < 70
            cap = MAX_W + 40 if min(lw, w) < 60 else MAX_W
            if ((same and min(lw, w) < MIN_W) or (same_h1 and tiny) or (lw < 70)) and lw + w <= cap:
                if p["path"] != last["paths"][-1]:
                    common = [x for x, y in zip(last["paths"][0], p["path"]) if x == y]
                    extra = p["path"][len(common):]
                    for lv, t in extra:
                        last["blocks"].append(dict(kind="h", text=L.inline_clean(t)))
                last["blocks"] += p["blocks"]
                last["paths"].append(p["path"])
                continue
        passages.append(dict(paths=[p["path"]], blocks=list(p["blocks"])))
    merged = []
    k = 0
    while k < len(passages):
        p = passages[k]
        if k + 1 < len(passages):
            q = passages[k + 1]
            pw, qw = L.words(btext(p["blocks"])), L.words(btext(q["blocks"]))
            if pw < MIN_W and pw + qw <= MAX_W + 40 and top_of(p["paths"][-1]) == top_of(q["paths"][0]):
                qp = q["paths"][0]
                if qp != p["paths"][-1]:
                    common = [x for x, y in zip(p["paths"][-1], qp) if x == y]
                    for lv, t in qp[len(common):]:
                        p["blocks"].append(dict(kind="h", text=L.inline_clean(t)))
                p["blocks"] += q["blocks"]
                p["paths"] += q["paths"]
                merged.append(p)
                k += 2
                continue
        merged.append(p)
        k += 1
    passages = merged
    out = []
    for p in passages:
        paths = p["paths"]
        common = []
        for parts in zip(*paths):
            if all(x == parts[0] for x in parts):
                common.append(parts[0])
            else:
                break
        first = paths[0]
        bl = p["blocks"]
        if len(first) > len(common):
            bl = [dict(kind="h", text=L.inline_clean(t)) for lv, t in first[len(common):]] + bl
        if not common:
            common = list(first[:1])
        sec = " › ".join(L.inline_clean(t) for lv, t in common) or "Inicio del informe"
        sec = " › ".join(L.inline_clean(clean_head(t)) for lv, t in common) or "Inicio del informe"
        out.append(dict(seccion=sec, text=btext(bl)))
    return out


# ---------------------------------------------------------------- temas y relacion
def temas_de(text):
    t = text.lower()
    sc = []
    for name, pat, _ in C.TEMAS:
        n = len(re.findall(pat, t))
        if n:
            sc.append((n, name))
    sc.sort(reverse=True)
    return [n for c, n in sc[:6] if c >= 2] or [n for c, n in sc[:2]]


TEMA_REL = {name: rel for name, _, rel in C.TEMAS}

# similitud con los apartados del programa: cada entrada se parte en sus subtitulos y se toma la mejor parte
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cand = [e for e in PROG if re.match(r"^(\d+\.\d+|anexo-\d+|proponemos|cierre|anexo-no-dicen|anexo-metas)(-r\d+)?$", e["id"])]
SUB_IDS, SUB_DOCS = [], []
for e in cand:
    paras = e["texto"].split("\n\n")
    subs = {s["titulo"] for s in e.get("subtitulos", [])}
    cur = [e["titulo"]]
    for ptxt in paras:
        if ptxt in subs and len(cur) > 1:
            SUB_IDS.append(e["id"]); SUB_DOCS.append(" ".join(cur))
            cur = [e["titulo"]]
        cur.append(ptxt)
    for c in e["cuadros"]:
        cur.append(c["titulo"] + " " + c["texto"])
    SUB_IDS.append(e["id"]); SUB_DOCS.append(" ".join(cur))
vec = TfidfVectorizer(lowercase=True, strip_accents="unicode", stop_words=C.STOP, min_df=1, max_df=0.3,
                      sublinear_tf=True)
M = vec.fit_transform(SUB_DOCS)


def base_id(i):
    return re.sub(r"-r\d+$", "", i)


def relacion_de(text, temas, rep_rel):
    v = vec.transform([text])
    sims = cosine_similarity(v, M)[0]
    best = {}
    for k, i in enumerate(SUB_IDS):
        best[i] = max(best.get(i, 0), sims[k])
    allowed = set(rep_rel)
    for t in temas[:2]:
        allowed |= set(TEMA_REL.get(t, []))
    score = {i: s + (0.03 if i in rep_rel else 0) + (0.02 if i in allowed else 0) for i, s in best.items()}
    ranked = sorted(score, key=lambda i: -score[i])
    picks = []
    for i in ranked:
        if best[i] < 0.07:
            break
        if i in allowed or base_id(i) in {base_id(a) for a in allowed}:
            picks.append(i)
        if len(picks) == 3:
            break
    if not picks:
        al = [i for i in ranked if i in allowed]
        picks = al[:2] or [i for i in ranked[:2] if best[i] >= 0.12] or list(rep_rel[:1])
    return picks


# ---------------------------------------------------------------- principal
files = sorted(IND.glob("*.md"), key=lambda f: C.ORDER.index(code_of(f.name)))
result = []
stats = []
for f in files:
    code = code_of(f.name)
    cfg = C.CFG.get(code, {})
    if cfg.get("excluir"):
        log.setdefault(code, []).append(("informe excluido", cfg.get("motivo", "")))
        stats.append((code, 0))
        continue
    if REVIEW and REVIEW != code and REVIEW != "all":
        continue
    h1, blocks = curate(code, f.read_text(encoding="utf-8"), cfg)
    hide = set(cfg.get("hide_titles", []))
    if hide:
        blocks = [dict(b, path=[x for x in b["path"] if x[1] not in hide]) for b in blocks
                  if not (b["kind"] == "h" and b["text"] in {L.inline_clean(h) for h in hide})]
    blocks = [dict(b, path=[(lv, clean_head(t)) for lv, t in b["path"]]) for b in blocks]
    ps = chunk(blocks)
    n = 0
    for p in ps:
        txt = p["text"].strip()
        if L.words(txt) < 25 and not re.search(r"\d", txt):
            log[code].append(("pasaje demasiado corto, sin dato", txt[:200]))
            continue
        n += 1
        tm = temas_de(txt + " " + p["seccion"])
        if len(tm) < 2:
            tm = tm + [t for t in cfg.get("temas", []) if t not in tm][:2 - len(tm)]
        rel = relacion_de(txt + " " + p["seccion"], tm, cfg.get("rel", []))
        d = dict(id=f"inv-{code}-{n:02d}", informe=cfg.get("titulo", h1), seccion=p["seccion"], texto=txt,
                 temas=tm, relacion=rel, descartado=False, nota="")
        for pat, nota in cfg.get("descartado", []):
            if re.search(pat, p["seccion"] + "\n" + txt, re.S):
                d["descartado"] = True
                d["nota"] = nota
                break
        if not d["descartado"]:
            ns = []
            for pat, nota in cfg.get("notas", []):
                if re.search(pat, p["seccion"] + "\n" + txt, re.S) and nota not in ns:
                    ns.append(nota)
            d["nota"] = " ".join(ns)
        result.append(d)
    stats.append((code, n))

if REVIEW:
    for code, items in log.items():
        if REVIEW not in (code, "all"):
            continue
        print(f"===== {code}: {len(items)} cosas sacadas")
        for why, t in items:
            print(f"  [{why}] {t[:260]}")
    for d in result:
        if DUMP:
            print(f"\n----- {d['id']} | {d['seccion']} | {L.words(d['texto'])} palabras | {d['temas']} | {d['relacion']} | desc={d['descartado']} {d['nota']}")
            print(d["texto"])
        else:
            print(f"{d['id']:<14} {L.words(d['texto']):>4}w desc={int(d['descartado'])} {d['seccion'][:60]} | {d['temas'][:3]} | {d['relacion']}")
else:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)
    with open(OUT.with_suffix(".log.json"), "w", encoding="utf-8") as fh:
        json.dump(log, fh, ensure_ascii=False, indent=1)
    print(len(result), "pasajes", OUT.stat().st_size, "bytes")
    for c, n in stats:
        print(c, n)
