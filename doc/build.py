#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arma el PDF. Cada seccion se renderiza a SU PROPIA pagina, con el alto que
pide su contenido: por eso no hay huerfanos, ni exhibits separados de su
argumento, ni paginas a medio llenar. Al final se pega la tapa."""
import base64, os, pathlib, re, sys
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
CSS  = (HERE / "design.css").read_text(encoding="utf-8")
ASSETS = ROOT / "assets" / "doc"
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)

PT = 96 / 72.0            # 1 pt en px CSS
PAGE_W_PT = 660.0
PAGE_W_PX = PAGE_W_PT * PT     # 880

_cache = {}
_missing = set()
# 1x1 transparente: si la ilustracion no esta en el paquete el <img> igual
# ocupa el alto que le fija design.css, asi que la pagina mide lo mismo.
BLANK = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAA"
         "AC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
def data_uri(name):
    if name in _cache: return _cache[name]
    p = ASSETS / name
    if not p.exists():
        _missing.add(name)
        _cache[name] = BLANK
        return BLANK
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    u = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
    _cache[name] = u
    return u

def inline_images(html):
    def rep(m):
        return f'src="{data_uri(m.group(1))}"'
    return re.sub(r'src="asset:([^"]+)"', rep, html)


SVG_MAP = {
 "ex02.png":"g_indicadores","ex03.png":"g_universitario","ex04.png":"g_dots",
 "ex05.png":"g_gasto_real","ex06.png":"g_copa","ex07.png":"g_percepcion",
 "ex08.png":"g_cascada","ex09.png":"g_escenarios","ex10.png":"g_rigidez",
 "ex11.png":"g_reformista","ex12.png":"g_tornado","ex13.png":"g_obra",
 "ex14.png":"g_reparto","ex01.png":"g_mapa_zonas","ex15.png":"g_mapa_radios","ex16.png":"g_funcion","ex17.png":"g_variacion",
 "ex18.png":"g_empleo","ex19.png":"g_gas",
}
SVGDIR = ROOT / "assets" / "svg"

def inline_svgs(html):
    """Los graficos van como SVG dentro del HTML: vectorial, y con la Inter
    de la propia pagina en vez de trazos."""
    for k, v in SVG_MAP.items():
        tag = f'<img src="asset:{k}" alt="">'
        if tag in html:
            svg = (SVGDIR / f"{v}.svg").read_text(encoding="utf-8")
            svg = svg[svg.index("<svg"):]
            svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)
            html = html.replace(tag, svg)
    return html

SHELL = """<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>%(css)s</style></head><body>%(body)s</body></html>"""


def build(sections, doc_title, cover_pdf=None, out_name="documento.pdf"):
    # la tapa cuenta como pagina 1 aunque el PDF vectorial no este en el
    # paquete: si no, la numeracion del pie y la del indice se corren una.
    total = len(sections) + 1
    if cover_pdf and not pathlib.Path(cover_pdf).exists():
        print(f"  !! falta la tapa {cover_pdf}: se arma sin ella")
        cover_pdf = None
    pages = []
    with sync_playwright() as pw:
        # PW_CHROMIUM permite apuntar a un Chromium ya instalado en la maquina
        _exe = os.environ.get("PW_CHROMIUM")
        br = pw.chromium.launch(executable_path=_exe) if _exe else pw.chromium.launch()
        pg = br.new_page(viewport={"width": int(PAGE_W_PX), "height": 1200})
        for i, s in enumerate(sections):
            n = i + 2
            foot = (f'<div class="runfoot"><span>{doc_title}</span>'
                    f'<span>P&aacute;gina {n} de {total}</span></div>')
            head = (f'<div class="runhead">{s["runhead"]}</div>'
                    if s.get("runhead") else "")
            body = f'<div class="page" id="pg">{head}{s["html"]}{foot}</div>'
            html = SHELL % {"css": CSS, "body": inline_images(inline_svgs(body))}
            f = OUT / f"s{i:02d}.html"
            f.write_text(html, encoding="utf-8")
            pg.goto(f.as_uri())
            pg.wait_for_timeout(450)
            try: pg.evaluate("document.fonts.ready")
            except Exception: pass
            pg.wait_for_timeout(250)
            h_px = pg.evaluate("document.getElementById('pg').getBoundingClientRect().height")
            # ninguna pagina puede ser mas baja que A4
            MIN_PX = 841.89 * PT
            nat_pt = h_px / PT
            if h_px < MIN_PX:
                h_px = MIN_PX
            h_pt = h_px / PT
            pdf = OUT / f"s{i:02d}.pdf"
            # Chrome redondea hacia abajo y a veces derrama una segunda pagina
            # casi vacia: se agranda el alto hasta que entra en UNA sola.
            extra = 2
            for _ in range(8):
                pg.pdf(path=str(pdf), print_background=True,
                       width=f"{PAGE_W_PX:.0f}px", height=f"{h_px + extra:.0f}px",
                       margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
                if len(PdfReader(str(pdf)).pages) == 1:
                    break
                extra += 6
            pages.append(pdf)
            aviso = ""
            if nat_pt < 841.89: aviso = f"  <- rellena desde {nat_pt:.0f}"
            elif h_pt > 2700:   aviso = "  <- PASA DE 2.700"
            print(f"  p{n:>2}  {s['id']:<26} {h_pt:7.1f} pt{aviso}")
        br.close()

    wr = PdfWriter()
    if cover_pdf:
        wr.append(PdfReader(str(cover_pdf)))
    for p in pages:
        wr.append(PdfReader(str(p)))
    dest = pathlib.Path("/mnt/user-data/outputs") / out_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as fh:
        wr.write(fh)
    if _missing:
        print(f"\n  !! {len(_missing)} ilustraciones ausentes, reemplazadas por un"
              f" pixel transparente (el alto de pagina no cambia):")
        for m in sorted(_missing): print("     -", m)
    print("\n->", dest, f"{dest.stat().st_size/1e6:.1f} MB", f"| {total} paginas")
    return dest


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    import content
    build(content.SECTIONS, content.DOC_TITLE,
          cover_pdf=ROOT / "tapa_vector.pdf", out_name="PROGRAMA_SAN_ISIDRO_2027.pdf")
