# -*- coding: utf-8 -*-
"""Lectura, limpieza y corte en pasajes de los informes de investigacion."""
import re

# ---------------------------------------------------------------- parseo
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def parse(text):
    """Devuelve (titulo_h1, bloques). Cada bloque: dict(path, kind, text, line).
    path: lista de (nivel, titulo) de los encabezados que lo contienen (sin el primer h1)."""
    lines = text.split("\n")
    blocks = []
    path = []
    h1 = None
    i = 0
    n = len(lines)
    para = []
    para_line = None

    def flush_para():
        nonlocal para, para_line
        if para:
            blocks.append(dict(path=list(path), kind="p", text=" ".join(s.strip() for s in para), line=para_line))
        para, para_line = [], None

    while i < n:
        l = lines[i]
        m = HEAD_RE.match(l)
        if m:
            flush_para()
            lv, t = len(m.group(1)), m.group(2).strip()
            if h1 is None and lv == 1:
                h1 = t
                i += 1
                continue
            while path and path[-1][0] >= lv:
                path.pop()
            path.append((lv, t))
            blocks.append(dict(path=list(path), kind="h", text=t, line=i + 1, level=lv))
            i += 1
            continue
        if not l.strip():
            flush_para()
            i += 1
            continue
        if re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", l):
            flush_para()
            i += 1
            continue
        if l.lstrip().startswith("|"):
            flush_para()
            rows = []
            start = i
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            blocks.append(dict(path=list(path), kind="table", rows=rows, line=start + 1, text="\n".join(rows)))
            continue
        lm = LIST_RE.match(l)
        if lm:
            flush_para()
            indent = len(lm.group(1).replace("\t", "    "))
            marker = lm.group(2)
            item = [lm.group(3)]
            start = i
            i += 1
            # continuacion: renglones indentados que no son un item nuevo ni encabezado
            while i < n and lines[i].strip() and not HEAD_RE.match(lines[i]) \
                    and not LIST_RE.match(lines[i]) and not lines[i].lstrip().startswith("|") \
                    and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                item.append(lines[i].strip())
                i += 1
            blocks.append(dict(path=list(path), kind="li", text=" ".join(item), line=start + 1,
                               indent=indent, marker=marker))
            continue
        if l.lstrip().startswith(">"):
            flush_para()
            q = []
            start = i
            while i < n and lines[i].lstrip().startswith(">"):
                q.append(re.sub(r"^\s*>\s?", "", lines[i]).strip())
                i += 1
            blocks.append(dict(path=list(path), kind="quote", text=" ".join(x for x in q if x), line=start + 1))
            continue
        if para_line is None:
            para_line = i + 1
        para.append(l)
        i += 1
    flush_para()
    return h1, blocks


# ---------------------------------------------------------------- limpieza de texto
MARKS = [
    (r"\*\*\[V\]\*\*|\[V\]", "(verificado en la fuente)"),
    (r"\*\*\[CP\]\*\*|\[CP\]", "(cálculo propio)"),
    (r"\*\*\[SC\]\*\*|\[SC\]", "(sin confirmar)"),
    (r"\*\*\[P\]\*\*|\[P\]", "(probable, según fuentes secundarias)"),
    (r"\*\*\[I\]\*\*|\[I\]", "(inferencia propia)"),
]


def inline_clean(s):
    """Quita el marcado de markdown y pasa las marcas a palabras. No cambia el texto."""
    for pat, rep in MARKS:
        s = re.sub(pat, rep, s)
    # enlaces [texto](url) -> texto (url)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r"\1 (\2)", s)
    # negritas y cursivas
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"__(.+?)__", r"\1", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])", r"\1", s)
    s = s.replace("**", "")
    # codigo en linea
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"[ \t]+", " ", s).strip()
    # «(verificado en la fuente) / (cálculo propio)» queda legible; espacios antes de puntuacion
    s = re.sub(r" +([,.;:])", r"\1", s)
    return s


# señales de nota interna: si aparecen, se saca la oracion (o la fila, o el item)
URL_RE = re.compile(r"https?://\S+|\b(?:www\.)?[\w-]+(?:\.[\w-]+)*\.(?:ar|com|org|net|gov|gob|io|es|uy|br|cl|uk|eu|int|edu|fr|de|it|il|au|nz|mx|pe|co|us|ca|fi|ch|se|nl|info|ai)\b(?:/[^\s)|]*)?")
CODE_RE = re.compile(r"`([^`]*)`")
PATHLIKE = re.compile(r"(^|/)0\d[a-z]?_|_tools|_tmp|claude/|\.(py|csv|json|md|txt|pdf|geojson|xlsx|sh|ipynb)$|^[\w.-]+/$|^[\w.-]+/[\w./-]+$|^/[\w-]+$|\(\)$|^python3? ")
INTERNAL = [
    (r"\b0\d[a-z]?_[\w]+/|\b0[1-6]_(raw|clean|scripts|charts)\b", "ruta"),
    (r"(?<![\w.])(informes|data|doc|salida|assets|copias|sibom|_tools|_tmp|0_cuentas|r_t\w*|uf_actos|ocr_archive_org|\d{1,2}_[a-z_]+)/", "ruta"),
    (r"\b[\w-]+\.(py|csv|json|xlsx|md|ipynb|geojson|sh)\b|\b[A-Za-z0-9_]+_[A-Za-z0-9_]+\.(txt|pdf)\b|\b[A-Z_]{4,}\.txt\b", "archivo"),
    (r"\brepo(sitorio)?\b", "repositorio"),
    (r"\bRama\b|\bclaude/[\w-]+|\bcommit\b|\bbranch\b", "rama"),
    (r"\bNick\b", "Nick"),
    (r"\bcoordinador", "coordinador"),
    (r"\b[Ww]orkers?\b", "worker"),
    (r"\bTODO\b", "TODO"),
    (r"(?i:\b(el|del|al|lo|la) cliente\b)|\bclientes? (decid|descart|pid|defin|eligi|lo defin)|decide el cliente|del cliente\b", "cliente"),
    (r"El documento no se toca", "proceso"),
    (r"\bcontent_\w|\bL\d{3,4}\b", "archivo"),
    (r"\bcorrecci[oó]n \d{2,3}\b|\bdispatch\b", "proceso"),
    (r"\bcurl\b|pdftotext|pymupdf|PyMuPDF|scraper|[Pp]ull[Pp]ush|este servidor|este entorno|\bproxy\b|CERTIFICATE_VERIFY|tesseract|devuelve (un )?(403|404|503|429)|devolvió (un )?(403|404|503|429)|\b(HTTP|error) (403|404|503|429)\b", "herramienta"),
]
INTERNAL_RE = [(re.compile(p), why) for p, why in INTERNAL]


def internal_reasons(s, allow=()):
    for a in allow:
        if a in s:
            return []
    why = []
    for c in CODE_RE.findall(s):
        c2 = c.strip()
        if c2 and not URL_RE.fullmatch(c2) and PATHLIKE.search(c2):
            why.append("ruta")
    t = URL_RE.sub(" URL ", s)
    why += [w for r, w in INTERNAL_RE if r.search(t)]
    return sorted(set(why))


SENT_SPLIT = re.compile(r"(?:(?<=[.!?])|(?<=[.!?]\*\*)|(?<=[.!?]\*)|(?<=[.!?][»\"”)])|(?<=[.!?][»\"”)]\*\*))\s+(?=(?:\*\*|\*|_)?[«\"“(¿¡\[]?[A-ZÁÉÍÓÚÑ0-9])")


def split_sentences(s):
    return [x for x in SENT_SPLIT.split(s) if x.strip()]


def words(s):
    return len(re.findall(r"\S+", s))
