#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Version A4: la version de pantalla tal cual, achicada en forma pareja (660 -> 595,28 pt de ancho, un 90%)
y cortada en hojas A4. No rehace nada: toma cada pagina del PDF de pantalla y la reparte en hojas, cortando
solo entre bloques (parrafo, bloque de dos columnas, recuadro, cuadro, grafico, foto). Un titulo nunca queda
separado de lo que sigue, ni un cuadro o grafico de su rotulo y de su fuente. Un grafico nunca se corta.

Lo que no entra en una hoja se parte (aprobado por Nick el 07/10): un cuadro, entre filas, repitiendo arriba la
fila del encabezado; un recuadro, entre sus puntos; una lista, entre sus items.

Cada hoja lleva el encabezado y el pie de la pagina de pantalla; el pie dice el numero de hoja de la A4. El
indice es el mismo, con los numeros de hoja de la A4.

Uso:  python3 doc/corte_a4.py              (la A4 entera, a salida/PROGRAMA_SAN_ISIDRO_2027_A4.pdf)
      python3 doc/corte_a4.py --muestras   (cuatro hojas de muestra, al lado de la version de pantalla)
Lee salida/PROGRAMA_SAN_ISIDRO_2027.pdf y out/sNN.html, que deja doc/build.py: correr antes build.py."""
import collections, html as H, os, pathlib, re, sys, unicodedata
import pymupdf as fitz
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build as B          # solo se lee: el HTML, el CSS y el script de columnas de la version de pantalla
import content             # solo se lee: las secciones, para el indice
import content_a as CA

ROOT = HERE.parent
PANTALLA = ROOT / "salida" / "PROGRAMA_SAN_ISIDRO_2027.pdf"
SALIDA = ROOT / "salida" / "PROGRAMA_SAN_ISIDRO_2027_A4.pdf"
A4_W, A4_H = 595.2756, 841.8898
ESC = A4_W / B.PAGE_W_PT                  # 0,9019: todo se achica igual
HOJA = A4_H / ESC                         # alto de una hoja A4, en pt de la pagina de pantalla (933,4)
# los margenes de la pagina de pantalla (design.css): encabezado arriba, pie abajo
ARRIBA_CONT = 40.5 + 6.75 + 16.5          # en una hoja que sigue: el encabezado y el aire de un titulo h2
ABAJO = 28.1 + 7 + 0.75 + 6.4 + 30        # aire antes del pie, el pie y el margen de abajo
LIM = HOJA - ABAJO                        # hasta donde puede llegar el contenido de una hoja
FONDO = None                              # el beige de la pagina de pantalla, tal como lo dibujo Chrome (--ground)
GRIS = (0x6E / 255, 0x62 / 255, 0x5A / 255)       # --taupe, el color del pie
INTER = HERE / "_fonts" / "Inter-Regular.ttf"

JS_MEDIR = r"""() => {
  const pg = document.getElementById('pg');
  const r0 = pg.getBoundingClientRect();
  const pt = v => v * 0.75;
  const caja = e => { const r = e.getBoundingClientRect(); return [pt(r.top - r0.top), pt(r.bottom - r0.top)]; };
  const out = {alto: pt(r0.height), bloques: [], titulos: []};
  for (const e of pg.children) {
    const [top, bottom] = caja(e);
    const b = {tag: e.tagName.toLowerCase(), cls: e.className || '', top, bottom,
               txt: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90),
               tabla: e.tagName === 'TABLE' || !!e.querySelector('table'),
               dibujo: !!e.querySelector('svg, img') || ['FIGURE', 'IMG', 'SVG'].includes(e.tagName)};
    // una lista larga se parte entre sus puntos; un cuadro, entre sus filas; un recuadro, entre sus parrafos
    if (e.tagName === 'OL' || e.tagName === 'UL') b.items = [...e.children].map(caja);
    const t = e.tagName === 'TABLE' ? e : e.querySelector('table');
    if (t) b.filas = [...t.rows].map(r => { const [a, z] = caja(r);
      return {top: a, bottom: z, th: !!r.querySelector('th'), sub: r.classList.contains('hd') && !r.querySelector('th')}; });
    if (/^callout/.test(b.cls)) b.hijos = [...e.children].map(caja);
    out.bloques.push(b);
  }
  for (const h of pg.querySelectorAll('h1, h2, h3')) {
    const [top] = caja(h);
    out.titulos.push([h.textContent.trim().replace(/\s+/g, ' '), top]);
  }
  return out;
}"""


def _abrir(pw):
    exe = os.environ.get("PW_CHROMIUM")
    br = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
    return br, br.new_page(viewport={"width": int(B.PAGE_W_PX), "height": 1200})


def _medir_archivo(pg, f):
    pg.goto(f.as_uri())
    pg.wait_for_timeout(450)
    try:
        pg.evaluate("document.fonts.ready")
    except Exception:
        pass
    pg.wait_for_timeout(250)
    pg.evaluate(B.JS_COLFILL)
    m = pg.evaluate(JS_MEDIR)
    m["archivo"] = f.name
    return m


def medir():
    """Los bloques de primer nivel de cada pagina de pantalla, como los dibujo build.py (con las columnas
    llenadas por su mismo script)."""
    archivos = sorted(B.OUT.glob("s[0-9][0-9].html"))
    with sync_playwright() as pw:
        br, pg = _abrir(pw)
        res = [_medir_archivo(pg, f) for f in archivos]
        br.close()
    return res


# ---------------------------------------------------------------------------------------------- el corte
def grupos(m):
    """Bloques que van juntos: un titulo con lo que sigue; el rotulo de un cuadro o grafico con el cuadro o
    grafico; un cuadro o grafico con su fuente y sus notas."""
    bl = [b for b in m["bloques"] if b["cls"] not in ("runhead", "runfoot") and b["tag"] != "style"
          and b["bottom"] - b["top"] > 0.1]
    out = []
    pegar_al_siguiente = False
    for b in bl:
        previo = out[-1]["partes"][-1] if out else None
        de_cuadro = previo is not None and (previo["tabla"] or previo["dibujo"] or previo["tag"] == "table"
                                            or (previo["tag"] == "p" and previo["cls"].startswith("cap")))
        es_cola = ((b["tag"] == "p" and b["cls"].startswith("cap")) or b["tag"] == "figcaption"
                   or (b["cls"] == "note" and de_cuadro))
        if out and (pegar_al_siguiente or es_cola):
            g = out[-1]
            g["bottom"] = max(g["bottom"], b["bottom"])
            g["partes"].append(b)
        else:
            out.append({"top": b["top"], "bottom": b["bottom"], "partes": [b]})
        titulo = b["tag"] in ("h1", "h2", "h3", "h4") or b["cls"] in ("stand", "igrp", "hairline")
        rotulo = b["cls"].split(" ")[0] == "ex" and not (b["tabla"] or b["dibujo"])
        pegar_al_siguiente = titulo or rotulo
    return out


def _pieza(top, bottom, pt=2.0, pb=2.0, repetir=None, parte=None):
    return dict(top=top, bottom=bottom, pt=pt, pb=pb, repetir=repetir, parte=parte)


def piezas(m):
    """Los pedazos entre los que se puede cortar. Lo que no entra en una hoja se parte: un cuadro entre filas
    (con su encabezado repetido), un recuadro entre sus parrafos y una lista entre sus items."""
    entra = LIM - ARRIBA_CONT
    out, partidos, no_entran = [], [], []
    for g in grupos(m):
        if g["bottom"] - g["top"] <= entra:
            out.append(_pieza(g["top"], g["bottom"]))
            continue
        tabla = next((p for p in g["partes"] if p.get("filas")), None)
        recuadro = next((p for p in g["partes"] if p.get("hijos")), None)
        lista = next((p for p in g["partes"] if p.get("items")), None)
        if tabla:
            filas = tabla["filas"]
            enc = [f for f in filas[:2] if f["th"]]
            datos = filas[len(enc):]
            rep = (enc[0]["top"], enc[-1]["bottom"]) if enc else None
            # la primera fila de datos va con el rotulo, el titulo y el encabezado; una fila de subtitulo, con la
            # que la sigue; la ultima, con la fuente y las notas
            trozos, actual = [], [g["top"], datos[0]["bottom"]]
            pegada = datos[0]["sub"]
            for f in datos[1:]:
                if pegada:
                    actual[1] = f["bottom"]
                else:
                    trozos.append(actual)
                    actual = [f["top"], f["bottom"]]
                pegada = f["sub"]
            actual[1] = g["bottom"]
            trozos.append(actual)
            ult = len(trozos) - 1
            for k, (a, z) in enumerate(trozos):
                out.append(_pieza(a, z, pt=2.0 if k == 0 else 0.0, pb=2.0 if k == ult else 0.0,
                                  repetir=rep if k else None, parte="cuadro"))
            partidos.append(("cuadro", g))
        elif recuadro:
            hijos = recuadro["hijos"]
            cortes = [hijos[1][1]] + [h[1] for h in hijos[2:-1]]      # el rotulo va con el primer punto
            a = g["top"]
            for c in cortes:
                out.append(_pieza(a, c, parte="recuadro"))
                a = c
            out.append(_pieza(a, g["bottom"], parte="recuadro"))
            partidos.append(("recuadro", g))
        elif lista:
            a = g["top"]
            for (t, z) in lista["items"][:-1]:
                out.append(_pieza(a, z, parte="lista"))
                a = z
            out.append(_pieza(a, g["bottom"], parte="lista"))
            partidos.append(("lista", g))
        else:
            out.append(_pieza(g["top"], g["bottom"]))
            no_entran.append(g)
    return out, partidos, no_entran


def cortar(m):
    """Reparte los pedazos de una pagina en hojas. Cada hoja es una lista de tramos [desde, hasta, aire arriba,
    aire abajo, encabezado repetido] de la pagina de pantalla, que se ponen uno abajo del otro; la primera hoja
    de cada pagina empieza en 0, con su encabezado de pagina."""
    ps, partidos, no_entran = piezas(m)
    hojas = []
    tramos, usado, primera = [], 0.0, True
    for p in ps:
        for intento in (0, 1):
            nuevo, alto = [list(t) for t in tramos], usado
            if primera and not nuevo:
                nuevo, alto = [[0.0, p["bottom"], 0.0, p["pb"], False]], p["bottom"]
            elif not nuevo:
                if p["repetir"]:
                    a, z = p["repetir"]
                    nuevo.append([a, z, 0.0, 0.0, True])
                    alto += z - a
                nuevo.append([p["top"], p["bottom"], p["pt"], p["pb"], False])
                alto += p["bottom"] - p["top"]
            else:
                alto += p["bottom"] - nuevo[-1][1]
                nuevo[-1][1], nuevo[-1][3] = p["bottom"], p["pb"]
            if alto <= LIM or not tramos:
                tramos, usado = nuevo, alto
                break
            hojas.append({"tramos": tramos, "primera": primera})
            tramos, usado, primera = [], ARRIBA_CONT, False
    if tramos:
        hojas.append({"tramos": tramos, "primera": primera})
    return hojas, partidos, no_entran


# ---------------------------------------------------------------------------------------------- la hoja
def fondo(src):
    """El color del fondo, leido de una pagina de pantalla (Chrome lo dibuja apenas distinto del CSS)."""
    global FONDO
    if FONDO is None:
        px = src[1].get_pixmap(clip=fitz.Rect(2, 2, 6, 6)).pixel(1, 1)
        FONDO = tuple(v / 255 for v in px[:3])
    return FONDO


def pie_original(src_pg, m):
    """Donde esta el pie en la pagina de pantalla: la raya de arriba, y desde donde empieza el numero."""
    pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
    num = [s for b in src_pg.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]
           if s["text"].strip().startswith("Página") and s["bbox"][1] > pie["top"] - 2]
    x_num = num[0]["bbox"][0] if num else 520.0
    base = num[0]["origin"][1] if num else pie["bottom"] - 2
    return pie, x_num, base


def escribir(pg, x_der, base, texto, tam, espaciado):
    """Texto alineado a la derecha, con la letra y el espaciado del pie de pantalla."""
    f = fitz.Font(fontfile=str(INTER))
    ancho = sum(f.text_length(c, fontsize=tam) for c in texto) + espaciado * (len(texto) - 1)
    tw = fitz.TextWriter(pg.rect, color=GRIS)
    x = x_der - ancho
    for c in texto:
        tw.append((x, base), c, font=f, fontsize=tam)
        x += f.text_length(c, fontsize=tam) + espaciado
    tw.write_text(pg)


def componer(dst, src, pno, m, hoja, n_hoja, total):
    """Una hoja A4: fondo, encabezado, los tramos de la pagina de pantalla y el pie con el numero de hoja."""
    pg = dst.new_page(width=A4_W, height=A4_H)
    pg.draw_rect(pg.rect, color=None, fill=fondo(src), overlay=False)
    E = ESC
    pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
    tope = pie["top"] - 0.1                    # ningun tramo se lleva la raya del pie
    y = 0.0
    if not hoja["primera"]:
        cab = next(b for b in m["bloques"] if b["cls"] == "runhead")
        pg.show_pdf_page(fitz.Rect(0, 0, A4_W, (cab["bottom"] + 2) * E), src, pno,
                         clip=fitz.Rect(0, 0, 660, cab["bottom"] + 2))
        y = ARRIBA_CONT
    for (a, z, pa, pz, _) in hoja["tramos"]:
        a0 = max(0.0, a - pa)
        z1 = min(z + pz, tope)
        y0 = y - (a - a0)
        pg.show_pdf_page(fitz.Rect(0, y0 * E, A4_W, (y0 + z1 - a0) * E), src, pno, clip=fitz.Rect(0, a0, 660, z1))
        y += z - a
    # el pie: la raya y el titulo, tal cual; el numero, el de la hoja
    _, x_num, base = pie_original(src[pno], m)
    alto = max(m["alto"], 841.89)
    dy = HOJA - alto                           # el pie va al fondo de la hoja, como en pantalla
    raya = fitz.Rect(0, pie["top"] + 0.1, 660, pie["top"] + 0.85)     # solo la raya (0,75 pt), nada de arriba
    izq = fitz.Rect(0, pie["top"] + 0.85, x_num - 2, alto)
    for r in (raya, izq):
        pg.show_pdf_page(fitz.Rect(r.x0 * E, (r.y0 + dy) * E, r.x1 * E, (r.y1 + dy) * E), src, pno, clip=r)
    escribir(pg, (660 - 45) * E, (base + dy) * E, f"Página {n_hoja} de {total}", 6.4 * E, 0.25 * E)
    return pg


def portada(dst, src):
    pg = dst.new_page(width=A4_W, height=A4_H)
    pg.draw_rect(pg.rect, color=None, fill=fondo(src), overlay=False)
    pg.show_pdf_page(pg.rect, src, 0)
    return pg


# ---------------------------------------------------------------------------------------------- el indice
def _plano(t):
    t = unicodedata.normalize("NFKC", H.unescape(re.sub(r"<[^>]+>", "", t))).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip().lower()


def hoja_de_titulo(m, hojas, n_primera, txt):
    """La hoja de la A4 donde cae el titulo de una entrada del indice."""
    plano = _plano(txt)
    num = re.match(r"(\d+\.\d+)\s", plano)
    y = None
    for t, top in m["titulos"]:
        tp = _plano(t)
        if (num and re.match(re.escape(num.group(1)) + r"(?!\d)", tp)) or (not num and tp.startswith(plano[:24])):
            y = top
            break
    if y is None:
        return n_primera
    for k, h in enumerate(hojas):
        if any(a - 3 <= y <= z + 3 for a, z, _, _, rep in h["tramos"] if not rep):
            return n_primera + k
    return n_primera


def indice_html(numeros):
    """El mismo indice de la version de pantalla (content_a), con los numeros de hoja de la A4."""
    base = CA._indice()
    cab = base[:base.index('<div class="igrp">')]
    filas, it = [], iter(numeros)
    for kind, txt, key in CA._IDX:
        if kind == "g":
            filas.append(f'<div class="igrp">{txt}</div>')
        else:
            filas.append('<div class="irow"><span class="it">%s</span><span class="ilead"></span>'
                         '<span class="ipg">%s</span></div>' % (txt, next(it)))
    return cab + "".join(filas)


def render_indice(numeros, total):
    """Dibuja la pagina del indice con los numeros de la A4, con el mismo HTML y CSS de build.py."""
    s = content.SECTIONS[0]
    assert s["id"] == "indice"
    head = f'<div class="runhead">{s["runhead"]}</div>' if s.get("runhead") else ""
    foot = (f'<div class="runfoot"><span>Programa de gobierno &middot; San Isidro 2027</span>'
            f'<span>P&aacute;gina 2 de {total}</span></div>')
    body = f'<div class="page" id="pg">{head}{indice_html(numeros)}{foot}</div>'
    f = B.OUT / "a4_indice.html"
    f.write_text(B.SHELL % {"css": B.CSS, "body": B.inline_images(B.inline_svgs(body))}, encoding="utf-8")
    pdf = B.OUT / "a4_indice.pdf"
    with sync_playwright() as pw:
        br, pg = _abrir(pw)
        m = _medir_archivo(pg, f)
        h_px = max(m["alto"], 841.89) * B.PT
        extra = 2
        for _ in range(8):
            pg.pdf(path=str(pdf), print_background=True, width=f"{B.PAGE_W_PX:.0f}px", height=f"{h_px + extra:.0f}px",
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            if len(fitz.open(str(pdf))) == 1:
                break
            extra += 6
        br.close()
    return fitz.open(str(pdf)), m


# ---------------------------------------------------------------------------------------------- todo
def plan_completo():
    """Mide, corta y numera: [(pagina de pantalla, hoja, numero de hoja)], el total, lo que se parte y lo que no
    entra en una hoja, y la primera hoja y las hojas de cada pagina."""
    med = medir()
    src = fitz.open(str(PANTALLA))
    assert len(src) == len(med) + 1, (len(src), len(med))
    for i, m in enumerate(med):
        h_pdf = src[i + 1].rect.height
        assert abs(max(m["alto"], 841.89) - h_pdf) < 9, (i + 2, m["alto"], h_pdf)
    plan, partidos, no_entran, por_pagina, n = [], [], [], [], 1
    for i, m in enumerate(med):
        hs, pt, ne = cortar(m)
        por_pagina.append((n + 1, hs))
        for h in hs:
            n += 1
            plan.append((i + 1, h, n))
        partidos += [(i + 2, k, g) for k, g in pt]
        no_entran += [(i + 2, g) for g in ne]
    return med, src, plan, n, partidos, no_entran, por_pagina


def numeros_indice(med, por_pagina):
    """Para cada entrada del indice, la hoja de la A4 donde cae su titulo."""
    ids = [s["id"] for s in content.SECTIONS]
    out = []
    for kind, txt, key in CA._IDX:
        if kind != "i":
            continue
        k = ids.index(key)
        n_primera, hojas = por_pagina[k]
        out.append(hoja_de_titulo(med[k], hojas, n_primera, txt))
    return out


def comparar(fuentes, dst, plan):
    """Hoja por hoja contra la version de pantalla: las palabras de cada pagina de pantalla tienen que estar,
    todas y una sola vez, en sus hojas de la A4 (sin contar el encabezado y el pie de pagina, y descontando el
    encabezado repetido de los cuadros partidos)."""
    def palabras(pg, clip):
        return collections.Counter(w[4] for w in pg.get_text("words", clip=clip))
    malas = []
    por_pag = collections.defaultdict(list)
    for (pno, h, n) in plan:
        por_pag[pno].append((h, n))
    for pno, hs in sorted(por_pag.items()):
        sp, m = fuentes[pno]
        cab = next(b for b in m["bloques"] if b["cls"] == "runhead")
        pie = next(b for b in m["bloques"] if b["cls"] == "runfoot")
        esperado = palabras(sp, fitz.Rect(0, cab["bottom"] + 1, 660, pie["top"] - 0.5))
        visto = collections.Counter()
        alto = max(m["alto"], 841.89)
        for h, n in hs:
            hp = dst[n - 1]
            ws = palabras(hp, fitz.Rect(0, (cab["bottom"] + 1) * ESC, A4_W, (HOJA - (alto - pie["top"]) - 0.5) * ESC))
            for (a, z, _, _, rep) in h["tramos"]:
                if rep:
                    ws -= palabras(sp, fitz.Rect(0, a, 660, z))
            visto += ws
        if esperado != visto:
            falta, sobra = esperado - visto, visto - esperado
            malas.append((pno + 1, sum(falta.values()), sum(sobra.values()), list(falta)[:6], list(sobra)[:6]))
    return malas


def armar():
    med, src, plan, total, partidos, no_entran, por_pagina = plan_completo()
    print(f"A4: {total} hojas (con la portada)")
    for p, k, g in partidos:
        print(f"  partido ({k}): pag. {p}, {g['bottom'] - g['top']:.0f} pt: {g['partes'][0]['txt'][:60]}")
    for p, g in no_entran:
        print(f"  !! pag. {p}: un bloque de {g['bottom'] - g['top']:.0f} pt no entra en una hoja y no se puede partir: "
              f"{g['partes'][0]['txt'][:60]}")
    # el indice, con los numeros de hoja de la A4 (su largo no cambia: se comprueba)
    nums = numeros_indice(med, por_pagina)
    ind_doc, ind_m = render_indice(nums, total)
    ind_hojas, _, _ = cortar(ind_m)
    assert len(ind_hojas) == len(por_pagina[0][1]), (len(ind_hojas), len(por_pagina[0][1]))
    dst = fitz.open()
    portada(dst, src)
    k_ind, plan_final = 0, []
    for (pno, h, n) in plan:
        if pno == 1:
            h = ind_hojas[k_ind]
            k_ind += 1
            componer(dst, ind_doc, 0, ind_m, h, n, total)
        else:
            componer(dst, src, pno, med[pno - 1], h, n, total)
        plan_final.append((pno, h, n))
    dst.save(str(SALIDA), garbage=3, deflate=True)
    dst = fitz.open(str(SALIDA))
    print(f"-> {SALIDA} | {len(dst)} hojas | {SALIDA.stat().st_size / 1e6:.1f} MB")
    fuentes = {pno: (src[pno], med[pno - 1]) for pno in range(2, len(src))}
    fuentes[1] = (ind_doc[0], ind_m)
    return dst, plan_final, fuentes, nums, total


def lado_a_lado(src, dst, pno_src, desde, hasta, pno_dst, rotulo_izq, rotulo_der, salida, dpi=110):
    """La misma parte de la version de pantalla (izquierda) y la hoja A4 (derecha), a la misma escala."""
    from PIL import Image, ImageDraw, ImageFont
    clip = fitz.Rect(0, max(0, desde - 24), 660, hasta + 24)
    izq = src[pno_src].get_pixmap(dpi=dpi, clip=clip)
    der = dst[pno_dst].get_pixmap(dpi=dpi)
    a = Image.frombytes("RGB", (izq.width, izq.height), izq.samples)
    b = Image.frombytes("RGB", (der.width, der.height), der.samples)
    f = ImageFont.truetype(str(HERE / "_fonts" / "Inter-SemiBold.ttf"), 22)
    m, cab = 40, 60
    lienzo = Image.new("RGB", (a.width + b.width + 3 * m, max(a.height, b.height) + cab + m), "white")
    lienzo.paste(a, (m, cab))
    lienzo.paste(b, (2 * m + a.width, cab))
    d = ImageDraw.Draw(lienzo)
    d.text((m, 18), rotulo_izq, font=f, fill=(124, 46, 35))
    d.text((2 * m + a.width, 18), rotulo_der, font=f, fill=(124, 46, 35))
    lienzo.save(salida)


def muestras(elegidas):
    med, src, plan, total, _, _, _ = plan_completo()
    dst = fitz.open()
    portada(dst, src)
    detalle = []
    for n_hoja in elegidas:
        pno, h, n = next(x for x in plan if x[2] == n_hoja)
        componer(dst, src, pno, med[pno - 1], h, n, total)
        detalle.append((pno, h, n))
    carpeta = ROOT / "salida" / "muestras_a4"
    carpeta.mkdir(parents=True, exist_ok=True)
    pdf = carpeta / "MUESTRAS_A4.pdf"
    dst.save(str(pdf), garbage=3, deflate=True)
    dst = fitz.open(str(pdf))
    lado_a_lado(src, dst, 0, 0, src[0].rect.height - 24, 0, "PANTALLA · tapa", "A4 · hoja 1 (al 90%)",
                carpeta / "muestra_1_portada.png")
    nombres = ["muestra_2_texto_y_recuadro", "muestra_3_cuadro", "muestra_4_grafico"]
    for k, (pno, h, n) in enumerate(detalle):
        a, z = h["tramos"][0][0], h["tramos"][-1][1]
        lado_a_lado(src, dst, pno, a, z, k + 1, f"PANTALLA · pág. {pno + 1} (la misma parte)",
                    f"A4 · hoja {n} de {total} (al 90%)", carpeta / f"{nombres[k]}.png")
    print("muestras:", pdf, [d[2] for d in detalle])


if __name__ == "__main__":
    if "--muestras" in sys.argv:
        muestras([int(x) for x in sys.argv[sys.argv.index("--muestras") + 1:]] or [78, 26, 57])
        sys.exit(0)
    dst, plan, fuentes, nums, total = armar()
    malas = comparar(fuentes, dst, plan)
    if malas:
        print("  !! paginas cuyas palabras no coinciden con las de sus hojas A4:")
        for p in malas:
            print("     pag. %d: faltan %d, sobran %d · %s · %s" % p)
    else:
        print("  OK: cada pagina de pantalla esta entera en sus hojas A4, palabra por palabra")
    print("  indice A4:", ", ".join(map(str, nums)))
