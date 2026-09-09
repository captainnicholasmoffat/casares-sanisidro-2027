#!/usr/bin/env python3
"""
ARMADO DEL PDF — Programa de gobierno · San Isidro 2027

    python3 03_scripts/armar_pdf.py

Lee 07_capitulos/ y produce PROGRAMA_SAN_ISIDRO_2027.pdf.

Orden: tapa · indice · introduccion · capitulos 1 a 6 · anexo de fuentes.

--------------------------------------------------------------------------
EL CORTE ES MECANICO
--------------------------------------------------------------------------
Cada capitulo termina con una seccion de pendientes precedida por la linea
exacta "# NO VA AL PDF". El corte lo hace un split, no el criterio de quien
arma:

    publicable = texto.split(MARCADOR)[0]

Si un pendiente se colara al PDF final, todo el trabajo de declarar limites
se leeria como descuido. Por eso el script ADEMAS verifica el resultado y
falla si encuentra rastro del marcador o de una seccion de pendientes.

--------------------------------------------------------------------------
LAS ETIQUETAS DE CONFIANZA
--------------------------------------------------------------------------
Un cuadro SIN etiqueta es dato verificado contra fuente primaria, y el anexo
lo dice en su primera linea. Poner "VERIFICADO" en cuarenta cuadros es ruido:
se vuelve decorativo y deja de leerse. Lo que tiene valor es la excepcion.

Llevan etiqueta solo cuatro casos, y se detectan por el encabezado de la
tabla, no por su posicion: ver ETIQUETAS.

--------------------------------------------------------------------------
IDENTIDAD
--------------------------------------------------------------------------
Paleta, titulo, subtitulo y tipografia salen de 07_IDENTIDAD_DEL_DOCUMENTO.md,
que esta cerrado. Los seis hex son los mismos que usa estilo.py para los
exhibits, asi que el PDF hereda la identidad sin trabajo extra.

ROJO PROHIBIDO: en Argentina se lee como color politico. No aparece en
ninguna parte, y verificar_pdf() falla si se cuela.
"""

import html
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CAPS = os.path.join(RAIZ, "07_capitulos")
CHARTS = os.path.join(RAIZ, "06_charts")
SALIDA = os.path.join(RAIZ, "PROGRAMA_SAN_ISIDRO_2027.pdf")

MARCADOR = "# NO VA AL PDF"

# --- Identidad, cerrada en 07_IDENTIDAD_DEL_DOCUMENTO.md -------------------
PAPEL, TINTA = "#FAF8F4", "#16293A"
RIO, BARRANCA = "#2D6E7E", "#A8763F"
CAL, AMBAR = "#EDE9E2", "#8A6A1F"

TITULO = "PROGRAMA DE GOBIERNO"
ANIO = "SAN ISIDRO 2027"
SUBTITULO = ("Con los recursos que el Municipio ya tiene,<br>"
             "y con decisión vecinal sobre la inversión pública.")
TITULO_CORTO = "Programa de gobierno · San Isidro 2027"

ORDEN = [
    ("00_INTRODUCCION.md", "Introducción"),
    ("CAP1_DIAGNOSTICO.md", "1 · Diagnóstico"),
    ("CAP2_GESTION_MEDIDA.md", "2 · La gestión, medida"),
    ("CAP3_LA_PLATA.md", "3 · La plata"),
    ("CAP4_MECANISMO.md", "4 · El mecanismo"),
    ("CAP5_SECTORIAL.md", "5 · Qué hacemos en cada área"),
    ("CAP6_CIERRE.md", "6 · Contra qué queremos que nos midan"),
    ("99_ANEXO_FUENTES.md", "Anexo de fuentes"),
]

# El primer encabezado de la tabla -> etiqueta. Se detecta por contenido, no
# por posicion: si una tabla se mueve de seccion, la etiqueta la sigue.
ETIQUETAS = [
    (("| Año | Escenario base",), "MODELADO"),
    (("| Año | Base, sin programa",), "MODELADO"),
    (("| Parámetro | Valor |",), "MODELADO"),
    (("| Municipio | Gasto devengado total",), "PROCESADO POR TERCEROS"),
    (("| Indicador | Boulogne + Béccar",), "ZONIFICACIÓN PROPIA"),
    (("| Zona | Población |",), "ZONIFICACIÓN PROPIA"),
]

LEYENDA_ETIQUETA = {
    "MODELADO": "proyección del modelo de flujo de caja, no dato observado",
    "PROCESADO POR TERCEROS": "RAFAM vía La Verdadera PBA; San Isidro validado, "
                              "los otros 105 no",
    "ZONIFICACIÓN PROPIA": "zonas construidas sobre radios censales; los límites "
                           "oficiales no están publicados",
    "SIN VERIFICAR": "no se pudo contrastar contra fuente primaria",
}


# ==========================================================================
# 1. LEER Y CORTAR
# ==========================================================================

def leer_publicable(nombre):
    """El texto de un capitulo hasta el marcador. El corte es un split."""
    with open(os.path.join(CAPS, nombre), encoding="utf-8") as f:
        texto = f.read()
    publicable = texto.split(MARCADOR)[0]
    if publicable == texto and MARCADOR in texto:        # pragma: no cover
        raise RuntimeError("el corte no se aplico en %s" % nombre)
    # El capitulo termina con los separadores que preceden al marcador. Un
    # separador suelto al final empuja una pagina casi vacia al PDF.
    publicable = re.sub(r'(\s*-{3,}\s*)+$', '', publicable)
    return publicable.rstrip()


# ==========================================================================
# 2. MARKDOWN -> HTML
# ==========================================================================

RE_EXHIBIT = re.compile(r'^`\[EXHIBIT (\d+)\s*—\s*([^\]]+)\]`\s*$')


def _inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def _exhibit(num, titulo):
    """Un exhibit: numero, titulo descriptivo y linea de fuente al pie."""
    cands = [f for f in os.listdir(CHARTS)
             if f.startswith("EXHIBIT_%s_" % num) and f.endswith(".png")]
    if not cands:
        raise RuntimeError("falta el PNG del EXHIBIT %s" % num)
    ruta = os.path.join(CHARTS, sorted(cands)[0])
    # SIN figcaption: el PNG ya trae su numero, su titulo descriptivo y su
    # linea de fuente al pie. Agregar un pie aparte los duplicaba.
    return ('<figure class="exh" title="%s">'
            '<img src="file://%s" alt="EXHIBIT %s — %s"/>'
            '</figure>' % (html.escape(titulo), ruta, num, html.escape(titulo)))


def _tabla(bloque):
    """Una tabla markdown -> HTML, con su etiqueta de confianza si le toca."""
    filas = [l for l in bloque if l.strip().startswith("|")]
    if len(filas) < 2:
        return ""
    encabezado = filas[0]
    etiqueta = None
    for claves, et in ETIQUETAS:
        if any(encabezado.startswith(c) for c in claves):
            etiqueta = et
            break

    def celdas(l):
        return [c.strip() for c in l.strip().strip("|").split("|")]

    out = ['<div class="tw">']
    if etiqueta:
        out.append('<p class="etq"><span class="etq-b">%s</span> %s</p>'
                   % (etiqueta, LEYENDA_ETIQUETA[etiqueta]))
    out.append("<table><thead><tr>")
    for c in celdas(encabezado):
        out.append("<th>%s</th>" % _inline(c))
    out.append("</tr></thead><tbody>")
    for l in filas[2:]:
        out.append("<tr>")
        for c in celdas(l):
            out.append("<td>%s</td>" % _inline(c))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def a_html(md, slug):
    lineas = md.split("\n")
    out, i, n = [], 0, len(lineas)
    while i < n:
        l = lineas[i]

        m = RE_EXHIBIT.match(l.strip())
        if m:
            out.append(_exhibit(m.group(1).zfill(2), m.group(2).strip()))
            i += 1
            continue

        if l.strip().startswith("|"):
            j = i
            while j < n and lineas[j].strip().startswith("|"):
                j += 1
            out.append(_tabla(lineas[i:j]))
            i = j
            continue

        if l.startswith("### "):
            out.append("<h3>%s</h3>" % _inline(l[4:]))
        elif l.startswith("## "):
            out.append("<h2>%s</h2>" % _inline(l[3:]))
        elif l.startswith("# "):
            out.append('<h1 id="%s">%s</h1>' % (slug, _inline(l[2:])))
        elif l.startswith("> "):
            j = i
            cita = []
            while j < n and lineas[j].startswith(">"):
                cita.append(lineas[j].lstrip("> ").rstrip())
                j += 1
            out.append("<blockquote>%s</blockquote>"
                       % "<br>".join(_inline(c) for c in cita if c))
            i = j
            continue
        elif l.strip() == "---":
            out.append('<hr>')
        elif re.match(r'^\d+\.\s', l.strip()):
            j = i
            items = []
            while j < n and re.match(r'^\d+\.\s', lineas[j].strip()):
                items.append(re.sub(r'^\d+\.\s', '', lineas[j].strip()))
                j += 1
            out.append("<ol>%s</ol>"
                       % "".join("<li>%s</li>" % _inline(x) for x in items))
            i = j
            continue
        elif l.strip().startswith("- "):
            j = i
            items = []
            while j < n and lineas[j].strip().startswith("- "):
                items.append(lineas[j].strip()[2:])
                j += 1
            out.append("<ul>%s</ul>"
                       % "".join("<li>%s</li>" % _inline(x) for x in items))
            i = j
            continue
        elif l.strip():
            out.append("<p>%s</p>" % _inline(l.strip()))
        i += 1
    return _agrupar_titulos("\n".join(out))


RE_H23 = re.compile(
    r'(<h[23]>.*?</h[23]>)\n'
    r'(<h3>.*?</h3>|<(?:p|ul|ol|blockquote)[ >].*?</(?:p|ul|ol|blockquote)>'
    r'|<div class="tw">.*?</div>)', re.S)


def _agrupar_titulos(html_txt):
    """Cada h2/h3 viaja pegado a su primer bloque, en un contenedor indivisible.

    Sin esto, "4.2 La deuda que la Provincia tiene con sus municipios" quedaba
    al pie de la pagina 25 con su primer parrafo en la 26. El lector lo lee
    como un error de armado, y con razon.
    """
    def envolver(m):
        return '<div class="keep">%s\n%s</div>' % (m.group(1), m.group(2))
    # Se aplica dos veces: un h2 seguido de un h3 seguido de un parrafo queda
    # agrupado en la segunda pasada.
    for _ in range(2):
        html_txt = RE_H23.sub(envolver, html_txt)
    return html_txt


# ==========================================================================
# 3. TAPA E INDICE
# ==========================================================================

def tapa():
    """Titulo, año, subtitulo y el mapa de zonas.

    El mapa va SIN el rotulo "EXHIBIT 15" y SIN linea de fuente: en la tapa es
    una imagen que plantea una pregunta, no un exhibit citado. Su pie de fuente
    vive en el §1.1, que es donde el dato se usa. Un lector que lo ve en la
    tapa sin entenderlo del todo y lo reencuentra explicado en el capitulo 1,
    entiende el documento.

    Sin nombre ni foto del candidato. Decision cerrada en la identidad.
    """
    mapa = os.path.join(CHARTS, "TAPA_mapa_zonas.png")
    return ('<section class="tapa">'
            '<div class="tapa-txt">'
            '<h1 class="t1">%s</h1><h1 class="t2">%s</h1>'
            '<p class="sub">%s</p></div>'
            '<img class="tapa-img" src="file://%s" alt=""/>'
            '</section>' % (TITULO, ANIO, SUBTITULO, mapa))


def indice(entradas):
    filas = "".join(
        '<li><a href="#%s">%s</a></li>' % (slug, html.escape(tit))
        for slug, tit in entradas)
    return ('<section class="indice"><h1>Índice</h1><ul class="ix">%s</ul>'
            '</section>' % filas)


# ==========================================================================
# 4. CSS
# ==========================================================================

CSS = """
@page {
  size: A4; margin: 20mm 18mm 18mm 18mm; background: %(papel)s;
  @bottom-left  { content: "%(corto)s"; font-family: "DejaVu Sans";
                  font-size: 7pt; color: %(tinta)s; opacity: .55; }
  @bottom-right { content: counter(page); font-family: "DejaVu Sans";
                  font-size: 7.5pt; color: %(tinta)s; opacity: .75; }
}
@page :first { margin: 0; @bottom-left { content: ""; } @bottom-right { content: ""; } }

html { background: %(papel)s; }
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 9.6pt;
       line-height: 1.52; color: %(tinta)s; }
p { margin: 0 0 .58em; text-align: justify; hyphens: auto; }
strong { font-weight: bold; }
code { font-family: "DejaVu Sans Mono"; font-size: 8pt; background: %(cal)s;
       padding: .5pt 2pt; }
a { color: %(rio)s; text-decoration: none; }
hr { border: 0; border-top: .5pt solid %(cal)s; margin: 1.5em 0; }

h1 { font-size: 20pt; line-height: 1.16; margin: 0 0 .5em;
     string-set: cap content(); break-before: page; }
h2 { font-size: 12.6pt; margin: 1.5em 0 .5em; color: %(tinta)s; }
h3 { font-family: "DejaVu Sans"; font-size: 9.4pt; font-weight: bold;
     margin: 1.25em 0 .4em; color: %(rio)s; }
h1 + p, h2 + p { margin-top: 0; }

/* Un titulo al pie con su primer parrafo en la pagina siguiente es un salto
   que el lector lee como error. WeasyPrint ignora break-after:avoid en los
   encabezados, asi que el armador agrupa cada titulo con su primer bloque en
   un .keep, que no se puede partir. */
.keep { break-inside: avoid; }
.keep h2, .keep h3 { margin-top: 0; }
p, li { orphans: 2; widows: 2; }

blockquote { margin: .9em 0 .9em 0; padding: .55em .9em; background: %(cal)s;
             border-left: 2.5pt solid %(rio)s; font-size: 9.2pt;
             text-align: left; }
ul, ol { margin: 0 0 .6em 1.1em; padding: 0; }
li { margin-bottom: .22em; text-align: justify; }

/* ---- tablas ---- */
.tw { break-inside: avoid; margin: .95em 0 1.15em; }
table { width: 100%%; border-collapse: collapse;
        font-family: "DejaVu Sans"; font-size: 7.9pt; }
th { text-align: left; padding: 4pt 5pt; border-bottom: 1pt solid %(tinta)s;
     font-weight: bold; }
td { padding: 3.4pt 5pt; border-bottom: .4pt solid %(cal)s;
     vertical-align: top; }
tbody tr:nth-child(even) { background: %(cal)s; }
th:not(:first-child), td:not(:first-child) { text-align: right; }
th:first-child, td:first-child { text-align: left; }

/* ---- etiqueta de confianza: solo la excepcion la lleva ---- */
.etq { font-family: "DejaVu Sans"; font-size: 6.9pt; margin: 0 0 3pt;
       color: %(ambar)s; text-align: left; }
.etq-b { font-weight: bold; letter-spacing: .3pt; }

/* ---- exhibits ---- */
.exh { break-inside: avoid; margin: 1.1em 0 1.3em; }
.exh img { width: 100%%; }
.exh figcaption { font-family: "DejaVu Sans"; font-size: 6.9pt;
                  color: %(tinta)s; opacity: .7; margin-top: 3pt; }
.exh-n { color: %(rio)s; font-weight: bold; letter-spacing: .4pt; }

/* ---- tapa ---- */
.tapa { height: 297mm; padding: 26mm 18mm 0; box-sizing: border-box; }
.tapa h1 { break-before: avoid; margin: 0; letter-spacing: 1.2pt; }
.tapa .t1 { font-size: 27pt; }
.tapa .t2 { font-size: 27pt; color: %(rio)s; margin-bottom: 8mm; }
.tapa .sub { font-size: 11.5pt; line-height: 1.5; text-align: left;
             max-width: 118mm; }
.tapa-img { width: 100%%; margin-top: 10mm; }

/* ---- indice ---- */
.indice h1 { break-before: page; }
ul.ix { list-style: none; margin: 1.4em 0 0; padding: 0;
        font-family: "DejaVu Sans"; font-size: 10pt; }
ul.ix li { margin-bottom: .72em; }
ul.ix a { color: %(tinta)s; display: block;
           border-bottom: .4pt dotted %(cal)s; padding-bottom: .3em; }
ul.ix a::after { content: target-counter(attr(href), page); float: right;
                 color: %(rio)s; font-weight: bold; }
""" % dict(papel=PAPEL, tinta=TINTA, rio=RIO, barranca=BARRANCA,
           cal=CAL, ambar=AMBAR, corto=TITULO_CORTO)


# ==========================================================================
# 5. VERIFICACION DEL PDF YA ARMADO
# ==========================================================================

def verificar_pdf(ruta):
    """Falla si un pendiente se colo, o si aparece rojo."""
    problemas = []
    txt = subprocess.run(["pdftotext", "-q", ruta, "-"],
                         capture_output=True, text=True).stdout
    for frase in (MARCADOR, "NO VA AL PDF", "Pendientes de este capítulo"):
        if frase in txt:
            problemas.append("se colo texto de pendientes: %r" % frase)
    for rojo in ("#FF0000", "#F00", "1 0 0 rg", "1 0 0 RG"):
        if rojo in open(ruta, "rb").read().decode("latin-1"):
            problemas.append("aparece rojo: %s" % rojo)
    return problemas, txt


# ==========================================================================

def main():
    from weasyprint import HTML, CSS as WCSS

    partes, entradas = [tapa()], []
    cuerpo = []
    for nombre, titulo in ORDEN:
        slug = nombre.split(".")[0].lower()
        entradas.append((slug, titulo))
        cuerpo.append(a_html(leer_publicable(nombre), slug))

    partes.append(indice(entradas))
    partes.extend(cuerpo)

    doc = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
           '<title>%s</title></head><body>%s</body></html>'
           % (TITULO_CORTO, "\n".join(partes)))

    ruta_html = os.path.join(RAIZ, "_pdf_build.html")
    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(doc)

    HTML(string=doc, base_url=RAIZ).write_pdf(
        SALIDA, stylesheets=[WCSS(string=CSS)])

    from pypdf import PdfReader
    paginas = len(PdfReader(SALIDA).pages)
    problemas, txt = verificar_pdf(SALIDA)

    print("=" * 74)
    print("PDF ARMADO — %s" % os.path.basename(SALIDA))
    print("=" * 74)
    print("  paginas            : %d" % paginas)
    print("  secciones          : %d" % len(ORDEN))
    print("  exhibits insertados: %d" % txt.count("EXHIBIT"))
    print("  etiquetas          : %s"
          % ", ".join("%s x%d" % (e, txt.count(e))
                      for e in sorted(LEYENDA_ETIQUETA) if txt.count(e)))
    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print("   ", p)
        return 1
    print("\n  corte de pendientes: limpio")
    print("  rojo               : ausente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
