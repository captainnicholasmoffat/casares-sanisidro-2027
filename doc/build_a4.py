#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Version A4 para imprimir (dispatch 3, D). Sale del mismo texto que la de pantalla
(content.SECTIONS), pero corre en paginas A4 verticales (595 x 842 pt):

- margenes espejados para abrochar o anillar: 24 mm del lado del lomo y 16 mm del otro;
- cuerpo de 10,5 pt; nada por debajo de 8 pt (notas, fuentes, rotulos de cuadros);
- cada capitulo empieza en pagina nueva, y los pedazos que la version de pantalla parte
  solo por el alto de pagina vuelven a correr juntos;
- los cuadros no se parten, salvo que no entren en una pagina: entonces repiten el
  encabezado; ninguna fila se corta;
- las dos columnas pasan a una, para que la letra grande se lea de corrido;
- el indice lleva las paginas de esta version: se arma, se mide y se vuelve a armar;
- la tapa es la misma, llevada a A4 (tiene la misma proporcion).

Sale a /mnt/user-data/outputs/PROGRAMA_SAN_ISIDRO_2027_A4.pdf."""
import html as H
import os, pathlib, re, sys, unicodedata
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import build as B          # CSS, fuentes embebidas, graficos en SVG, control de fuentes
import content             # el mismo texto que la version de pantalla
import content_a as A      # el indice se rehace con las paginas de esta version

A4_W, A4_H = 595.2756, 841.8898
SALIDA = pathlib.Path("/mnt/user-data/outputs") / "PROGRAMA_SAN_ISIDRO_2027_A4.pdf"
# paginas que en la de pantalla no tienen <h1> pero en papel empiezan pagina
NUEVA_PAGINA = {"indice", "introduccion", "sintesis", "cierre", "ordenanza", "glosario", "metodo"}

PRINT_CSS = r"""
@page{size:210mm 297mm;margin:20mm 16mm 20mm 24mm;
  @top-left{content:"PROGRAMA DE GOBIERNO \00B7  PARTIDO DE SAN ISIDRO";font-family:'Inter',sans-serif;
    font-weight:600;font-size:8pt;letter-spacing:.9pt;color:#B4863A;vertical-align:bottom;padding-bottom:5mm}
  @bottom-left{content:"Programa de gobierno \00B7  San Isidro 2027";font-family:'Inter',sans-serif;
    font-size:8pt;color:#6E625A;vertical-align:top;padding-top:5mm}
  @bottom-right{content:"P\00E1 gina " counter(page) " de " counter(pages);font-family:'Inter',sans-serif;
    font-size:8pt;color:#6E625A;vertical-align:top;padding-top:5mm}}
@page :right{margin-left:24mm;margin-right:16mm}
@page :left{margin-left:16mm;margin-right:24mm}
@page portada{margin:0;@top-left{content:none}@bottom-left{content:none}@bottom-right{content:none}}
.portada{page:portada;height:20mm;break-after:page}

html,body{background:#fff}
.page{width:auto;min-height:0;padding:0;overflow:visible;display:block;background:transparent}
.runhead,.runfoot{display:none}
.trozo{break-before:page}

/* letra para leer en papel */
p,.cols>p,ul.b>li,ol.n>li{font-size:10.5pt;line-height:1.45}
ol.n>li:before{font-size:10.5pt}
p.lead{font-size:11pt;line-height:1.45}
.callout p{font-size:10.5pt;line-height:1.42}
.pull p{font-size:11pt;line-height:1.4}
.stand{font-size:11.5pt;line-height:1.4;max-width:none}
h1{font-size:18pt;line-height:1.2}
h2{font-size:13pt}
h3,.cols>h3{font-size:12pt}
td,.kv td{font-size:9.5pt;line-height:1.32}
th,.exlabel,.clabel,.plabel,.kv td:first-child,.tag{font-size:8pt;line-height:1.2}
th{height:auto;padding-bottom:4pt}
.exlabel{line-height:10pt}
.extitle{font-size:12pt;line-height:1.3}
.exsub,.cap,.note p,figcaption{font-size:8.5pt;line-height:1.4}
.irow .it{font-size:10.5pt}
.irow .ipg{font-size:10pt}
.igrp{font-size:8pt !important}

/* una sola columna: con letra grande, dos columnas en A4 quedan angostas */
.cols,.note{column-count:1 !important;height:auto !important;padding-bottom:0 !important}
.cols>p{margin-bottom:6pt}

/* cuadros: al ancho de la caja; no se parten; si no entran, repiten el encabezado */
table,.kv{width:100%}
.kv td:first-child{width:24%}
table{break-inside:avoid}
thead{display:table-header-group}
tr{break-inside:avoid}
.ex{break-inside:avoid;break-after:avoid}
.exw{break-inside:avoid}
.cap{break-before:avoid}
h1,h2,h3,.stand,.clabel,.plabel{break-after:avoid;break-inside:avoid}
p,li{orphans:3;widows:3}
.chart,figure,.duo,.pull,.diag{break-inside:avoid}
.diag svg{width:100% !important;height:auto !important}
figure img{height:62mm}
figure.tall img{height:80mm}
figure.band img{height:46mm}
.duo figure img{height:52mm}
"""


def a_imprenta(html):
    """La fila de encabezado de cada cuadro (la de <th>) pasa a <thead>, para que se
    repita si el cuadro no entra en una pagina; los anchos fijos de columna pasan a
    proporciones de la caja de pantalla (570 pt), para que entren en la de A4."""
    html = re.sub(r'(<table[^>]*>\s*(?:<colgroup>.*?</colgroup>\s*)?)(<tr class="hd">\s*<th.*?</tr>)',
                  r"\1<thead>\2</thead>", html, flags=re.S)
    html = re.sub(r'<col style="width:([0-9.]+)pt">',
                  lambda m: f'<col style="width:{float(m.group(1)) / 570 * 100:.3f}%">', html)
    # el titulo de un cuadro o grafico va pegado a su cuadro o grafico y a su fuente
    html = re.sub(r'(<div class="ex"><div class="exlabel">[^<]*</div><div class="extitle">.*?</div>'
                  r'(?:<div class="exsub">.*?</div>)?</div>\s*'
                  r'(?:<table.*?</table>|<div class="chart[^"]*">.*?</div>)'
                  r'(?:\s*<p class="cap">.*?</p>)*)',
                  r'<div class="exw">\1</div>', html, flags=re.S)
    return html


SVG_A4 = B.ROOT / "assets" / "svg_a4"
CAJA_PT = 210 / 25.4 * 72 - (24 + 16) / 25.4 * 72      # ancho de la caja de texto en A4


def inline_svgs_a4(html):
    """Los graficos de imprenta (charts_a4.py); si alguno no esta, el de pantalla con la
    letra llevada a 8 pt impresos, segun cuanto se estira para llenar la caja."""
    for k, v in B.SVG_MAP.items():
        tag = f'<img src="asset:{k}" alt="">'
        if tag not in html:
            continue
        f = SVG_A4 / f"{v}.svg"
        svg = (f if f.exists() else B.SVGDIR / f"{v}.svg").read_text(encoding="utf-8")
        svg = svg[svg.index("<svg"):]
        if not f.exists():
            ancho = float(re.search(r'viewBox="[0-9.]+ [0-9.]+ ([0-9.]+)', svg).group(1))
            minimo = 8.05 * ancho / CAJA_PT
            svg = re.sub(r"font-size: ([0-9.]+)px",
                         lambda m: f"font-size: {max(float(m.group(1)), minimo):.2f}px", svg)
        svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)
        html = html.replace(tag, svg)
    return html


def trozos(sections):
    out = []
    for s in sections:
        if not out or s["id"] in NUEVA_PAGINA or "<h1" in s["html"]:
            out.append([s])
        else:
            out[-1].append(s)
    return out


def norm(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = unicodedata.normalize("NFKC", H.unescape(t))
    return re.sub(r"\s+", "", t).lower()


def titulos(html):
    return [m.group(2) for m in re.finditer(r"<h([1-3])[^>]*>(.*?)</h\1>", html, re.S)]


def armar_html(sections, solo_indice=False):
    partes = ['<div class="portada"></div>']
    for tr in trozos(sections)[:1] if solo_indice else trozos(sections):
        cuerpo = "".join(f'<div class="page">{s["html"]}</div>' for s in tr)
        partes.append(f'<div class="trozo">{cuerpo}</div>')
    body = a_imprenta("".join(partes))
    return B.SHELL % {"css": B.CSS + PRINT_CSS, "body": B.inline_images(inline_svgs_a4(body))}


def imprimir(pg, html, pdf):
    f = B.OUT / "a4.html"
    f.write_text(html, encoding="utf-8")
    pg.goto(f.as_uri())
    pg.wait_for_timeout(800)
    try:
        pg.evaluate("document.fonts.ready")
    except Exception:
        pass
    pg.wait_for_timeout(400)
    pg.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
    return len(PdfReader(str(pdf)).pages)


def titulo_de_entrada(txt, key, por_id, todo):
    """El titulo que el indice nombra: el h2 numerado (4.4, 5.13...), o el titulo de la
    seccion con ese mismo texto, o el primero de la seccion."""
    plano = H.unescape(re.sub(r"<[^>]+>", "", txt)).replace("\xa0", " ").strip()
    m = re.match(r"(\d+\.\d+)\s", plano)
    if m:
        mm = re.search(r'<h2><span class="n">%s</span>(.*?)</h2>' % re.escape(m.group(1)), todo, re.S)
        if mm:
            return norm(m.group(1) + mm.group(1))
    s = por_id.get(key)
    if s:
        ts = titulos(s["html"])
        for t in ts:
            if norm(t) == norm(txt):
                return norm(t)
        if ts:
            return norm(ts[0])
    return None


def paginas_por_entrada(sections, pdf, n_indice):
    """Cada entrada del indice, con la pagina de A4 donde esta su titulo. Se busca en el
    texto de cada pagina, en orden, despues de la tapa y del indice."""
    paginas = [norm(p.extract_text() or "") for p in PdfReader(str(pdf)).pages]
    por_id = {s["id"]: s for s in sections}
    todo = "".join(s["html"] for s in sections)
    out, faltan, desde = [], [], 1 + n_indice
    for kind, txt, key in A._IDX:
        if kind != "i":
            continue
        t = titulo_de_entrada(txt, key, por_id, todo)
        n = next((i for i in range(desde, len(paginas)) if t and t in paginas[i]), None)
        if n is None:
            faltan.append(re.sub(r"<[^>]+>", "", H.unescape(txt)))
            out.append("&mdash;")
        else:
            desde = n
            out.append(n + 1)
    return out, faltan


def indice_a4(paginas):
    base = A._indice()
    cab = base[:base.index('<div class="igrp">')]
    filas, it = [], iter(paginas)
    for kind, txt, key in A._IDX:
        if kind == "g":
            filas.append(f'<div class="igrp">{txt}</div>')
        else:
            filas.append('<div class="irow"><span class="it">%s</span><span class="ilead"></span>'
                         '<span class="ipg">%s</span></div>' % (txt, next(it)))
    return cab + "".join(filas)


def main():
    B.write_font_css()
    secs = list(content.SECTIONS)
    exe = os.environ.get("PW_CHROMIUM")
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        pg = br.new_page()
        # cuantas paginas ocupa el indice (la tapa es la 1)
        n_indice = imprimir(pg, armar_html(secs, solo_indice=True), B.OUT / "a4_indice.pdf") - 1
        # primera pasada: donde cae cada titulo del indice
        p1 = B.OUT / "a4_pasada1.pdf"
        imprimir(pg, armar_html(secs), p1)
        pags, faltan = paginas_por_entrada(secs, p1, n_indice)
        secs[0] = dict(secs[0], html=indice_a4(pags))
        # segunda pasada: el indice con las paginas de A4, y se comprueba que no se movio nada
        p2 = B.OUT / "a4_pasada2.pdf"
        imprimir(pg, armar_html(secs), p2)
        pags2, _ = paginas_por_entrada(secs, p2, n_indice)
        br.close()
    if pags2 != pags:
        sys.exit("  !! el indice movio las paginas entre pasadas: revisar")
    # la tapa: la misma, llevada a A4 (660 x 934 pt es la proporcion de A4)
    wr = PdfWriter()
    tapa_pdf = B.ROOT / "tapa_vector.pdf"
    rd = PdfReader(str(p2))
    if tapa_pdf.exists():
        tapa = PdfReader(str(tapa_pdf)).pages[0]
        tapa.scale_by(A4_W / float(tapa.mediabox.width))
        tapa.mediabox = RectangleObject([0, 0, A4_W, A4_H])
        tapa.cropbox = RectangleObject([0, 0, A4_W, A4_H])
        wr.add_page(tapa)
    else:
        print("  !! falta la tapa: queda la pagina en blanco")
        wr.add_page(rd.pages[0])
    for p in rd.pages[1:]:
        wr.add_page(p)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA, "wb") as fh:
        wr.write(fh)
    total = len(PdfReader(str(SALIDA)).pages)
    print(f"\n-> {SALIDA} {SALIDA.stat().st_size / 1e6:.1f} MB | {total} paginas | indice en {n_indice}")
    if faltan:
        print("  !! entradas del indice sin pagina:", "; ".join(faltan))
    print("  indice A4:", ", ".join(str(x) for x in pags))
    B.check_fonts(SALIDA)
    malas = [i + 1 for i, p in enumerate(PdfReader(str(SALIDA)).pages)
             if abs(float(p.mediabox.width) - A4_W) > 0.6 or abs(float(p.mediabox.height) - A4_H) > 0.6]
    print("  OK: todas las paginas en A4." if not malas else f"  !! paginas que no son A4: {malas}")


if __name__ == "__main__":
    main()
