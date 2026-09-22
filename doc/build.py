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
_viudas = []          # pedazos de parrafo de una sola linea arriba o abajo de columna
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

# ---------------------------------------------------------------------------
# LAS FUENTES VAN EMBEBIDAS, NO SE PIDEN A GOOGLE.
# Chromium no puede traer fonts.googleapis.com a traves del proxy (rechaza el
# certificado) y cae en silencio a Liberation. Por eso las TTF viven en
# doc/_fonts/ y entran como @font-face con data URI. El CSS de fuentes se
# escribe UNA vez en out/fonts.css y cada pagina lo referencia: si se inyectara
# en cada HTML serian 36 copias de 4 MB.
# ---------------------------------------------------------------------------
FONTDIR = HERE / "_fonts"
SPECTRAL = [
    (400, "normal", "Spectral-Regular.ttf"),
    (500, "normal", "Spectral-Medium.ttf"),
    (600, "normal", "Spectral-SemiBold.ttf"),
    (700, "normal", "Spectral-Bold.ttf"),
    (400, "italic", "Spectral-Italic.ttf"),
    (500, "italic", "Spectral-MediumItalic.ttf"),
    (600, "italic", "Spectral-SemiBoldItalic.ttf"),
    (700, "italic", "Spectral-BoldItalic.ttf"),
]
# Inter va en instancias estaticas, no como fuente variable: Chromium carga la
# variable en pantalla pero NO la embebe al exportar el PDF, y ahi sustituye sin
# avisar. Las cuatro salen de Inter-var.ttf con doc/fetch_fonts.py.
INTER = [
    (400, "Inter-Regular.ttf"),
    (500, "Inter-Medium.ttf"),
    (600, "Inter-SemiBold.ttf"),
    (700, "Inter-Bold.ttf"),
]

def _face(fam, weight, style, fn, fmt="truetype"):
    p = FONTDIR / fn
    if not p.exists():
        sys.exit(f"  !! falta la fuente {p}. Sin ella el PDF sale en Liberation.\n"
                 f"     Corre: python3 doc/fetch_fonts.py")
    u = "data:font/ttf;base64," + base64.b64encode(p.read_bytes()).decode()
    return (f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"src:url({u}) format('{fmt}');font-display:block}}")

def write_font_css():
    faces = [_face("Spectral", w, st, fn) for w, st, fn in SPECTRAL]
    faces += [_face("Inter", w, "normal", fn) for w, fn in INTER]
    f = OUT / "fonts.css"
    f.write_text("\n".join(faces), encoding="utf-8")
    print(f"  fuentes embebidas: {len(faces)} caras -> {f.name} "
          f"({f.stat().st_size/1e6:.1f} MB)")
    return f

# Chromium no implementa widows/orphans dentro de columnas, asi que la regla de
# design.css es break-inside. Esto lo comprueba mirando las cajas dibujadas: si un
# parrafo se parte entre columnas y de un lado queda una sola linea, avisa.
JS_VIUDAS = """() => {
  const malos = [];
  document.querySelectorAll('.cols').forEach(cols => {
    cols.querySelectorAll(':scope > p, :scope > ul, :scope > ol, :scope > h3').forEach(el => {
      const rects = [...el.getClientRects()];
      if (rects.length < 2) return;
      const bandas = {};
      rects.forEach(r => { const k = Math.round(r.left / 10) * 10;
                           (bandas[k] = bandas[k] || []).push(r); });
      const claves = Object.keys(bandas);
      if (claves.length < 2) return;
      const lh = parseFloat(getComputedStyle(el).lineHeight) || 14;
      claves.forEach(k => {
        const alto = bandas[k].reduce((s, r) => s + r.height, 0);
        if (alto < lh * 1.6) malos.push(el.textContent.trim().slice(0, 80));
      });
    });
  });
  return malos;
}"""

SHELL = """<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts.css">
<style>%(css)s</style></head><body>%(body)s</body></html>"""


def build(sections, doc_title, cover_pdf=None, out_name="documento.pdf"):
    # la tapa cuenta como pagina 1 aunque el PDF vectorial no este en el
    # paquete: si no, la numeracion del pie y la del indice se corren una.
    total = len(sections) + 1
    if cover_pdf and not pathlib.Path(cover_pdf).exists():
        print(f"  !! falta la tapa {cover_pdf}: se arma sin ella")
        cover_pdf = None
    write_font_css()
    pages = []
    _viudas.clear()
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
            for t in pg.evaluate(JS_VIUDAS):
                _viudas.append((n, t))
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
    check_fonts(dest)
    if _viudas:
        print(f"\n  !! {len(_viudas)} viudas o huerfanas en columna:")
        for n, t in _viudas: print(f"     p{n:>2}  &laquo;{t}&raquo;".replace("&laquo;","\u00ab").replace("&raquo;","\u00bb"))
    else:
        print("  OK: ninguna viuda ni huerfana en columna.")
    return dest


def check_fonts(pdf):
    """Aborta si el PDF salio con fuentes sustituidas. Paso obligatorio: cuando
    Chromium no consigue Spectral e Inter cae a Liberation sin avisar, y el
    documento no es presentable."""
    nombres = set()
    for pg in PdfReader(str(pdf)).pages:
        res = pg.get("/Resources")
        if not res: continue
        fuentes = res.get_object().get("/Font")
        if not fuentes: continue
        for f in fuentes.get_object().values():
            bf = f.get_object().get("/BaseFont")
            if bf: nombres.add(str(bf).lstrip("/").split("+")[-1])
    usadas = sorted(nombres)
    malas = [n for n in usadas if "Liberation" in n or "DejaVu" in n]
    print(f"\n  fuentes del PDF ({len(usadas)}):")
    for n in usadas: print("     -", n)
    if malas:
        sys.exit(f"\n  !! FUENTES SUSTITUIDAS: {', '.join(malas)}."
                 f" El PDF no es presentable. Revisa doc/_fonts/ y fonts.css.")
    if not any(n.startswith("Spectral") for n in usadas) or \
       not any(n.startswith("Inter") for n in usadas):
        sys.exit("\n  !! faltan Spectral o Inter en el PDF.")
    print("  OK: sin sustituciones.")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    import content
    build(content.SECTIONS, content.DOC_TITLE,
          cover_pdf=ROOT / "tapa_vector.pdf", out_name="PROGRAMA_SAN_ISIDRO_2027.pdf")
