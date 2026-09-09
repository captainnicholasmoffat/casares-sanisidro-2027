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
import json
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
    (("| Zona | Población |",), "LÍMITES DE OPENSTREETMAP"),
]

# Las frases de remate de cada seccion. NO SE INVENTA NINGUNA: son las que ya
# estan escritas en los capitulos, y el armador solo les da peso tipografico.
# Sembrar remates para que todas las secciones tengan uno es lo que hace que un
# documento suene a folleto: si una seccion no tiene, se queda sin.
REMATES = json.load(open(os.path.join(AQUI, "remates.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(AQUI, "remates.json")) else {}

# Las CAJAS DESTACADAS son para cuatro cosas y ninguna mas. Si se empieza a
# encajonar lo que parece importante, dejan de significar algo.
#   metodo   advertencias metodologicas y limites declarados
#   legal    citas textuales de una norma
#   hipotesis las cuatro que se cayeron al contrastarlas
CAJAS = [
    ("metodo", ("Conviene ser exacto", "Conviene decir de entrada",
                "El límite de este dato", "La advertencia sobre este cuadro",
                "Sobre la línea de base", "Por qué esta tabla tiene sólo")),
    ("hipotesis", ("Cuatro de las críticas", "Cuatro hipótesis contra")),
]

LEYENDA_ETIQUETA = {
    "MODELADO": "proyección del modelo de flujo de caja, no dato observado",
    "PROCESADO POR TERCEROS": "RAFAM vía La Verdadera PBA; San Isidro validado, "
                              "los otros 105 no",
    "LÍMITES DE OPENSTREETMAP": "los límites de localidad son de OSM, que no es "
                                "fuente oficial, proyectados sobre los radios "
                                "censales del INDEC",
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
    # Los tres primeros bloques de un capitulo tienen roles distintos y hasta
    # ahora compartian estilo: el h1 es el titulo, el h2 SIN numero que le sigue
    # es la bajada —una linea que dice de que va la seccion— y los parrafos en
    # italica que vienen despues son la nota de version, que no es contenido.
    vistos_h1 = 0
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
            tipo = next((t for t, claves in CAJAS
                         if any(l[4:].startswith(c) for c in claves)), None)
            if tipo:
                j = i + 1
                cuerpo = []
                while j < n and not lineas[j].startswith(("#", "---", "|")):
                    if lineas[j].strip():
                        cuerpo.append(lineas[j].strip())
                    elif cuerpo:
                        break
                    j += 1
                out.append('<aside class="caja %s"><h4>%s</h4>%s</aside>'
                           % (tipo, _inline(l[4:]),
                              "".join("<p>%s</p>" % _inline(c) for c in cuerpo)))
                i = j
                continue
            out.append("<h3>%s</h3>" % _inline(l[4:]))
        elif l.startswith("## "):
            m2 = re.match(r"^(\d+(?:\.\d+)?)\s+(.*)$", l[3:].strip())
            # El h2 sin numero que sigue al titulo del capitulo es la bajada.
            if not m2 and vistos_h1 == 1 and not any(
                    "<h2" in o or "bajada" in o for o in out):
                out.append('<p class="bajada">%s</p>' % _inline(l[3:]))
                i += 1
                continue
            # El numero de seccion se separa para poder darle otro peso.
            if m2:
                out.append('<h2><span class="num">%s</span>%s</h2>'
                           % (m2.group(1), _inline(m2.group(2))))
            else:
                out.append("<h2>%s</h2>" % _inline(l[3:]))
        elif l.startswith("# "):
            vistos_h1 += 1
            out.append('<h1 id="%s">%s</h1>' % (slug, _inline(l[2:])))
        elif l.startswith("> "):
            j = i
            cita = []
            while j < n and lineas[j].startswith(">"):
                cita.append(lineas[j].lstrip("> ").rstrip())
                j += 1
            out.append('<aside class="caja legal">%s</aside>'
                       % "".join("<p>%s</p>" % _inline(c) for c in cita if c))
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
            # La nota de version: parrafo entero en italica, antes de la
            # primera seccion numerada. No es contenido y no lleva su peso.
            if (re.fullmatch(r"\*[^*].*\*", l.strip())
                    and not any('class="num"' in o for o in out)):
                out.append('<p class="version">%s</p>' % _inline(l.strip()[1:-1]))
                i += 1
                continue
            clase = ' class="remate"' if l.strip() in _remates_de(slug) else ""
            out.append("<p%s>%s</p>" % (clase, _inline(l.strip())))
        i += 1
    return _agrupar_titulos("\n".join(out))


def _remates_de(slug):
    """Las frases de remate del capitulo, tal como estan escritas en el .md."""
    for nombre, _ in ORDEN:
        if nombre.split(".")[0].lower() == slug:
            return set(REMATES.get(nombre, []))
    return set()


BLOQUE = (r'<(?:p|ul|ol|blockquote|aside)[ >].*?</(?:p|ul|ol|blockquote|aside)>'
          r'|<div class="tw">.*?</div>')

# Un h2 arrastra, si lo hay, el h3 que le sigue, y el primer bloque de contenido.
RE_H2 = re.compile(r'(<h2>.*?</h2>)\n(?:(<h3>.*?</h3>)\n)?(' + BLOQUE + ')', re.S)
RE_H3 = re.compile(r'(<h3>.*?</h3>)\n(' + BLOQUE + ')', re.S)


def _agrupar_titulos(html_txt):
    """Cada titulo viaja pegado a su primer bloque, en un contenedor indivisible.

    Sin esto, "4.2 La deuda que la Provincia tiene con sus municipios" quedaba
    al pie de una pagina con su primer parrafo en la siguiente. El lector lo lee
    como un error de armado, y con razon. WeasyPrint ignora break-after:avoid en
    los encabezados, asi que el agrupamiento se hace aca.

    UNA SOLA PASADA por regla. Antes se pasaba dos veces para atrapar el caso
    h2-h3-parrafo, y la segunda envolvia lo que la primera ya habia envuelto:
    salia <div class="keep"><div class="keep"><h2> con el cierre en el lugar
    equivocado, y el HTML mal anidado hacia que el navegador de impresion
    ignorara el break-inside. Ahora el h3 se captura en la misma regla del h2.
    """
    def envolver(m):
        partes = [g for g in m.groups() if g]
        return '<div class="keep">%s</div>' % "\n".join(partes)

    html_txt = RE_H2.sub(envolver, html_txt)
    # Los h3 sueltos, los que no venian pegados a un h2.
    html_txt = RE_H3.sub(
        lambda m: '<div class="keep">%s\n%s</div>' % (m.group(1), m.group(2)),
        html_txt)
    # Cuando el primer bloque es un parrafo corto —una linea de entrada—, el
    # titulo y esa linea entran al pie y lo que viene despues se va solo a la
    # pagina siguiente. Paso con "4.5 Quien decide y quien ejecuta", cuya
    # entrada tiene once palabras. El grupo se extiende al bloque siguiente.
    #
    # Va DESPUES de envolver los h3: si corre antes, el bloque siguiente
    # todavia es un <h3> pelado y no hay nada que agarrar.
    html_txt = re.sub(
        r'<div class="keep">((?:(?!</div>).)*?<p>[^<]{0,190}</p>)</div>\n'
        r'(<div class="keep">(?:(?!<div class="keep">).)*?</div>|' + BLOQUE + ')',
        lambda m: '<div class="keep">%s\n%s</div>' % (m.group(1), m.group(2)),
        html_txt, flags=re.S)
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

/* JERARQUIA. El numero de seccion grande y en Rio, el titulo en serif y la
   bajada en italica: de un vistazo se sabe donde esta uno en el documento. */
h1 { font-size: 21pt; line-height: 1.14; margin: 0 0 .35em;
     string-set: cap content(); break-before: page; }
/* La bajada: una linea que dice de que va la seccion, en Rio y en italica. */
p.bajada { font-family: "DejaVu Serif"; font-style: italic; font-size: 11.4pt;
           line-height: 1.34; color: %(rio)s; margin: .1em 0 .9em;
           max-width: 138mm; text-align: left; }
/* La nota de version no es contenido: chica y apagada. */
p.version { font-family: "DejaVu Sans"; font-size: 6.9pt; line-height: 1.35;
            color: %(tinta)s; opacity: .55; margin: 0 0 .3em;
            text-align: left; max-width: 138mm; }
p.version + p.version { margin-bottom: 1.4em; }
h2 { font-size: 13.4pt; line-height: 1.2; margin: 1.6em 0 .45em;
     color: %(tinta)s; }
h2 .num { color: %(rio)s; font-size: 17pt; font-weight: bold;
          margin-right: .28em; }
h3 { font-family: "DejaVu Sans"; font-size: 9.2pt; font-weight: bold;
     margin: 1.2em 0 .35em; color: %(rio)s;
     letter-spacing: .2pt; }

/* REMATE. Una por seccion, y solo las que ya estaban escritas. */
p.remate { font-size: 11.4pt; line-height: 1.38; color: %(tinta)s;
           margin: 1em 0 1.1em; padding: 0 0 0 9pt;
           border-left: 2.5pt solid %(rio)s; text-align: left;
           break-inside: avoid; }
p.remate strong { font-weight: bold; }

/* CAJAS. Cuatro usos y ninguno mas: advertencia metodologica, cita legal
   textual, limite declarado, hipotesis descartada. */
.caja { break-inside: avoid; margin: 1em 0 1.15em; padding: .62em .8em;
        background: %(cal)s; font-size: 8.9pt; }
.caja h4 { font-family: "DejaVu Sans"; font-size: 7.4pt; font-weight: bold;
           letter-spacing: .5pt; text-transform: uppercase;
           margin: 0 0 .35em; color: %(ambar)s; }
.caja p { margin: 0 0 .4em; text-align: left; }
.caja p:last-child { margin-bottom: 0; }
.caja.metodo { border-left: 2.5pt solid %(ambar)s; }
.caja.hipotesis { border-left: 2.5pt solid %(barranca)s; }
.caja.legal { border-left: 2.5pt solid %(rio)s; font-family: "DejaVu Serif";
              font-style: italic; }
.caja.legal h4 { color: %(rio)s; }
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
/* Un exhibit mas alto que media pagina no entra casi nunca junto al texto que
   lo introduce, y al irse entero deja la pagina anterior a medio llenar. El
   tope hace que quepan; el ancho manda y la altura se ajusta. */
.exh img { max-width: 100%%; max-height: 104mm; width: auto; height: auto;
           display: block; margin: 0 auto; }
.exh figcaption { font-family: "DejaVu Sans"; font-size: 6.9pt;
                  color: %(tinta)s; opacity: .7; margin-top: 3pt; }
.exh-n { color: %(rio)s; font-weight: bold; letter-spacing: .4pt; }

/* ---- tapa ---- */
/* La tapa ES el mapa, con el titulo encima. Antes el mapa flotaba en el medio
   y el tercio inferior quedaba vacio: no era respiracion, era hueco, y en la
   primera pagina que alguien ve eso se lee como que no supimos que poner. */
.tapa { height: 297mm; padding: 22mm 16mm 14mm; box-sizing: border-box;
        display: flex; flex-direction: column; }
.tapa h1 { break-before: avoid; margin: 0; letter-spacing: 1.2pt; }
.tapa .t1 { font-size: 27pt; }
.tapa .t2 { font-size: 27pt; color: %(rio)s; margin-bottom: 7mm; }
.tapa .sub { font-size: 11.5pt; line-height: 1.5; text-align: left;
             max-width: 118mm; margin: 0; }
.tapa-txt { flex: 0 0 auto; }
.tapa-img { flex: 1 1 auto; width: 100%%; height: 100%%;
            object-fit: contain; object-position: center bottom;
            margin-top: 6mm; }

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
