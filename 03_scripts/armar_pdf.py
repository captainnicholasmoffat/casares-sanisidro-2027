#!/usr/bin/env python3
"""
ARMADO DEL PDF — Programa de gobierno · San Isidro 2027

    python3 03_scripts/armar_pdf.py

Lee 07_capitulos/ y produce PROGRAMA_SAN_ISIDRO_2027.pdf.

Orden: tapa · indice · introduccion · capitulos 1 a 6 · anexo de fuentes.

--------------------------------------------------------------------------
LO QUE SE CORTA, Y SE CORTA MECANICAMENTE
--------------------------------------------------------------------------
Dos cosas del .md no van al PDF, y las dos las corta un split o un regex, no el
criterio de quien arma:

  1. TODO LO QUE SIGUE AL MARCADOR "# NO VA AL PDF" — los pendientes de cada
     capitulo.  publicable = texto.split(MARCADOR)[0]

  2. LA NOTA DE VERSION del encabezado de cada capitulo: las dos lineas en
     italica "*Borrador N · mes año*" y "*Reemplaza al borrador N. Cambios: …*".
     Son metadato interno del taller. Estaban impresas en el PDF, debajo de la
     bajada de cada capitulo, y le decian al lector de un programa de gobierno
     cuantas veces se reescribio.

Las dos palabras que las delatan —"Borrador" y "Reemplaza"— no aparecen en
ninguna otra parte del texto publicable, asi que verificar_pdf() relee el PDF
armado y falla si sobrevive cualquiera de las dos, o el marcador.

--------------------------------------------------------------------------
LA MAQUETA: BANDAS, NO COLUMNAS CON SALTADORES
--------------------------------------------------------------------------
La prosa va a dos columnas y los exhibits, las tablas anchas y los titulos
cruzan las dos. Hay dos maneras de conseguirlo y solo una funciona.

  NO: una sola caja `columns: 2` con `column-span: all` en lo que cruza.
      Cada saltador abre una fila de columnas nueva, y con `column-fill: auto`
      —que es lo que habia— la primera columna se llena hasta el pie de la
      pagina antes de empezar la segunda. El resultado eran paginas con el
      tercio de abajo vacio, que es lo que hay que arreglar.

  SI: BANDAS. El armador agrupa los bloques: cada corrida de prosa entra en su
      propia caja `<div class="banda">` de dos columnas balanceadas, y lo que
      cruza —exhibit, tabla ancha, titulo, remate, dato— queda afuera, como
      bloque de ancho completo entre dos bandas.

      Una banda balanceada no desperdicia nada: si tiene veinte lineas hace dos
      columnas de diez y lo que sigue empieza abajo. El unico hueco posible es
      el de un exhibit que no entra al pie de pagina, y para eso esta el tope de
      altura de la figura.

--------------------------------------------------------------------------
LA CABECERA DE LOS EXHIBITS SE RECOMPONE
--------------------------------------------------------------------------
Los PNG traen el rotulo, el titulo y la bajada dibujados adentro por matplotlib.
Adentro del PDF ese texto sale al cuerpo que le toque por el tamaño de la
imagen, no por la jerarquia del documento, y ademas no se puede buscar.

recorte_exhibits.py le saca la cabecera al PNG y el armador la vuelve a componer
con las fuentes del documento, leyendo 06_charts/pies.json — que es de donde
salio el texto que matplotlib dibujaba. Mismas palabras, otra tipografia.

--------------------------------------------------------------------------
IDENTIDAD
--------------------------------------------------------------------------
Paleta, titulo, subtitulo y tipografia salen de 07_IDENTIDAD_DEL_DOCUMENTO.md,
que esta cerrado. Los seis hex son los mismos que usa estilo.py para los
exhibits, asi que el PDF hereda la identidad sin trabajo extra.

ROJO PROHIBIDO: en Argentina se lee como color politico. No aparece en ninguna
parte, y verificar_pdf() falla si se cuela.

--------------------------------------------------------------------------
LAS PASADAS DEL ARMADOR, EN ORDEN
--------------------------------------------------------------------------
  1. leer_publicable()   corta por el marcador y saca la nota de version.
                         VA PRIMERO: nada de lo que sigue debe ver un pendiente.

  2. bloques()           el .md a una lista de bloques tipados. Cada bloque sabe
                         si cruza las dos columnas (ancho) o vive adentro de una
                         (flujo). Ese unico dato es el que arma la maqueta.

  3. bandas()            agrupa las corridas de bloques de flujo en cajas de dos
                         columnas y deja los anchos afuera. VA DESPUES de 2:
                         necesita el tipo de cada bloque ya decidido.

  4. tapa() e indice()   se anteponen al cuerpo ya armado. El indice usa
                         target-counter, asi que necesita los id ya puestos.

  5. WeasyPrint          aplica el CSS.

  6. verificar_pdf()     relee el PDF: marcador, nota de version, rojo. No
                         alcanza con cortar bien; hay que comprobar que se corto.

SI ALGUIEN INSERTA UNA PASADA NUEVA:
  - si toca texto, que corra DESPUES del corte (1) o vera pendientes;
  - si agrupa bloques, que respete el ancho: meter un bloque ancho adentro de
    una banda lo encierra en una columna de 84 mm;
  - correr 03_scripts/verificar_maqueta.py sobre el PDF resultante y MIRAR las
    paginas renderizadas. El armador anterior fallo exactamente por no mirar.
"""

import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recorte_exhibits import recortar                       # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CAPS = os.path.join(RAIZ, "07_capitulos")
CHARTS = os.path.join(RAIZ, "06_charts")
SALIDA = os.path.join(RAIZ, "PROGRAMA_SAN_ISIDRO_2027.pdf")

# --------------------------------------------------------------------------
# LA TIPOGRAFIA VIVE EN EL REPO Y SE CARGA POR RUTA
# --------------------------------------------------------------------------
# Source Serif 4, de Frank Grießhammer para Adobe, bajo SIL Open Font License
# 1.1 (05_tipografia/OFL.txt). Los dos archivos estan versionados en el repo y
# el CSS los carga con @font-face apuntando al archivo, NO por nombre de fuente
# instalada en el sistema. La diferencia importa en un documento con indice: si
# el armado dependiera de que la fuente este instalada, en una maquina sin ella
# WeasyPrint caeria a otra, cambiaria el ancho de cada linea, y el indice
# imprimiria numeros de pagina que no son.
#
# POR QUE ESTA Y NO OTRA, en las dos condiciones que importaban:
#   - color a cuerpo chico en columna angosta: altura de x 0,475 em contra
#     0,400 de EB Garamond; y ancho de la 'n' 0,606 em contra 0,662 de
#     Literata, o sea mas caracteres por linea en una columna de 85 mm, que es
#     menos guiones y menos rios de blanco.
#   - numeros para tablas: trae tabulares y de caja alta (tnum + lnum), que es
#     lo que alinea una columna de cifras.
#   - y versalitas de verdad (smcp), que son las de los rotulos de exhibit y
#     los encabezados de tabla. Simuladas por el motor salen como mayusculas
#     achicadas, con el trazo mas fino que el del texto de al lado.
# Ademas tiene eje de TAMAÑO OPTICO: el dibujo a cuerpo 9 no es el mismo
# reducido, es otro, con mas altura de x y mas espacio entre letras.
TIPOS = os.path.join(RAIZ, "05_tipografia")
SERIF = "Source Serif 4"
OPSZ_TEXTO = 9        # el dibujo para cuerpo de texto
OPSZ_TITULO = 24      # el dibujo para titulo: mas contraste y menos espaciado

MARCADOR = "# NO VA AL PDF"
MARGEN_PIE = 15          # mm: el margen de abajo de @page, que mide el hueco
# Las piezas llevan prefijo propio en el id: los h1 y los h2 tambien dejan
# ancla y el acomodador tiene que poder distinguirlas.
PREFIJO_PIEZA = "pz-"
# Las dos lineas del encabezado que son metadato del taller y no del programa.
RE_VERSION = re.compile(
    r'^\*\s*(?:Borrador\b|Reemplaza al borrador\b).*\*\s*$', re.M)

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

LEYENDA_ETIQUETA = {
    "MODELADO": "proyección del modelo de flujo de caja, no dato observado",
    "PROCESADO POR TERCEROS": "RAFAM vía La Verdadera PBA; San Isidro validado, "
                              "los otros 105 no",
    "LÍMITES DE OPENSTREETMAP": "los límites de localidad son de OSM, que no es "
                                "fuente oficial, proyectados sobre los radios "
                                "censales del INDEC",
    "SIN VERIFICAR": "no se pudo contrastar contra fuente primaria",
}

# Las frases de remate de cada seccion. NO SE INVENTA NINGUNA: son las que ya
# estan escritas en los capitulos, y el armador solo les da peso tipografico.
# Sembrar remates para que todas las secciones tengan uno es lo que hace que un
# documento suene a folleto: si una seccion no tiene, se queda sin.
REMATES = json.load(open(os.path.join(AQUI, "remates.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(AQUI, "remates.json")) else {}
DATOS = json.load(open(os.path.join(AQUI, "datos.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(AQUI, "datos.json")) else {}

# Las CAJAS DESTACADAS son para tres cosas y ninguna mas. Si se empieza a
# encajonar lo que parece importante, dejan de significar algo.
#   metodo     advertencias metodologicas y limites declarados
#   hipotesis  las cuatro que se cayeron al contrastarlas
#   legal      citas textuales de una norma (las abre un blockquote)
CAJAS = [
    ("metodo", ("Conviene ser exacto", "Conviene decir de entrada",
                "El límite de este dato", "La advertencia sobre este cuadro",
                "Sobre la línea de base", "Por qué esta tabla tiene sólo")),
    ("hipotesis", ("Cuatro de las críticas", "Cuatro hipótesis contra")),
]

# Un h3 que empieza asi no es una subseccion: es la nota de lectura al pie de la
# seccion. Va al ancho de la caja, en cuerpo chico, con el titulo de entrada en
# negrita corrido con el primer parrafo.
NOTAS_AL_PIE = ("Nota metodológica", "Nota sobre las fuentes")

PIES = json.load(open(os.path.join(CHARTS, "pies.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(CHARTS, "pies.json")) else {}


# ==========================================================================
# 1. LEER Y CORTAR
# ==========================================================================

def leer_publicable(nombre):
    """El texto de un capitulo, sin pendientes y sin nota de version."""
    with open(os.path.join(CAPS, nombre), encoding="utf-8") as f:
        texto = f.read()
    publicable = texto.split(MARCADOR)[0]
    if publicable == texto and MARCADOR in texto:        # pragma: no cover
        raise RuntimeError("el corte no se aplico en %s" % nombre)
    publicable = RE_VERSION.sub("", publicable)
    # El capitulo termina con los separadores que preceden al marcador. Un
    # separador suelto al final empuja una pagina casi vacia al PDF.
    publicable = re.sub(r'(\s*-{3,}\s*)+$', '', publicable)
    return publicable.rstrip()


# ==========================================================================
# 2. MARKDOWN -> BLOQUES
# ==========================================================================
# Un bloque es (ancho, html). `ancho` True significa que cruza las dos columnas
# y por lo tanto NO puede entrar en una banda. Es el unico dato que decide la
# maqueta, y por eso se calcula aca y en un solo lugar.

RE_EXHIBIT = re.compile(r'^`\[EXHIBIT (\d+)\s*—\s*([^\]]+)\]`\s*$')
RE_H2NUM = re.compile(r'^(\d+(?:\.\d+)?)\s+(.*)$')
RE_H1CAP = re.compile(r'^(CAPÍTULO\s+\d+\s*—)\s*(.*)$')


def _inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def _exhibit(num, titulo):
    """Un exhibit al ancho de la caja: rotulo, titulo, bajada, figura y fuente.

    El rotulo y el titulo NO salen del PNG —ahi ya no estan, los recorto
    recorte_exhibits— sino de pies.json, compuestos con la tipografia del
    documento. El titulo dice la conclusion; para eso esta escrito asi.
    """
    cands = [f for f in os.listdir(CHARTS)
             if f.startswith("EXHIBIT_%s_" % num) and f.endswith(".png")]
    if not cands:                                        # pragma: no cover
        raise RuntimeError("falta el PNG del EXHIBIT %s" % num)
    archivo = sorted(cands)[0]
    nombre = archivo[:-4]
    ruta, proporcion = recortar(archivo)
    pie = PIES.get(nombre, {})
    # Sin entrada en pies.json el exhibit sale con el texto del marcador del
    # capitulo en vez de su titulo, que es mas corto y no dice la conclusion.
    # Es una perdida que no rompe nada y por eso hay que denunciarla: paso de
    # verdad cuando la fabrica corrio con un solo exhibit y reescribio el json.
    if not pie.get("titulo"):
        raise RuntimeError(
            "el EXHIBIT %s no tiene título en 06_charts/pies.json: correr "
            "03_scripts/generar_todos_los_graficos.py entero" % num)

    # Un exhibit apaisado se lee bien al ancho de la caja. Uno casi cuadrado
    # —los dos mapas y la lista larga de funciones— llega a 180 mm de alto si se
    # lo deja crecer, se come una pagina entera y deja hueco en la anterior. El
    # tope lo decide la proporcion.
    clase = "exh" if proporcion >= 1.55 else "exh alto"

    cab = ['<p class="exh-rot">%s</p>'
           % html.escape(pie.get("exhibit", "EXHIBIT %s" % num))]
    cab.append('<h4 class="exh-tit">%s</h4>'
               % _inline(pie.get("titulo") or titulo))
    if pie.get("bajada"):
        cab.append('<p class="exh-baj">%s</p>' % _inline(pie["bajada"]))

    pies = []
    if pie.get("fuente"):
        pies.append('<p class="exh-fuente"><span class="et">Fuente:</span> %s</p>'
                    % _inline(pie["fuente"]))
    if pie.get("nota"):
        pies.append('<p class="exh-nota"><span class="et">Nota:</span> %s</p>'
                    % _inline(pie["nota"]))

    return ('<figure class="%s"><div class="exh-cab">%s</div>'
            '<img src="file://%s" alt="%s"/>%s</figure>'
            % (clase, "".join(cab), ruta,
               html.escape(pie.get("titulo") or titulo), "".join(pies)))


RE_ETIQUETAS_HTML = re.compile(r'<[^>]+>')


def _texto_plano(htm):
    """El texto de un bloque HTML, para medir su largo."""
    return html.unescape(RE_ETIQUETAS_HTML.sub("", htm)).strip()


def _celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


def _tabla(bloque):
    """Una tabla markdown -> HTML, con su etiqueta de confianza si le toca.

    La etiqueta va DEBAJO, como la linea de fuente de un exhibit: arriba se leia
    como el titulo de la tabla, que es lo que no es.
    """
    filas = [l for l in bloque if l.strip().startswith("|")]
    if len(filas) < 2:
        return None
    encabezado = filas[0]
    etiqueta = next((et for claves, et in ETIQUETAS
                     if any(encabezado.startswith(c) for c in claves)), None)

    cols = _celdas(encabezado)
    cuerpo = [_celdas(l) for l in filas[2:]]
    largo = max([len(c) for fila in cuerpo for c in fila] + [0])
    # Una tabla de dos columnas cortas entra comoda adentro de una columna de
    # 84 mm y ahi hace su trabajo. Una de cuatro columnas, o una de dos con
    # celdas de parrafo —las del anexo—, necesita el ancho de la caja.
    ancha = len(cols) >= 4 or largo > 58

    out = ['<div class="tw%s">' % (" ancho" if ancha else "")]
    out.append("<table><thead><tr>")
    for c in cols:
        out.append("<th>%s</th>" % _inline(c))
    out.append("</tr></thead><tbody>")
    for fila in cuerpo:
        out.append("<tr>%s</tr>"
                   % "".join("<td>%s</td>" % _inline(c) for c in fila))
    out.append("</tbody></table>")
    if etiqueta:
        out.append('<p class="etq"><span class="et">%s</span> %s</p>'
                   % (etiqueta, LEYENDA_ETIQUETA[etiqueta]))
    out.append("</div>")
    return ancha, "".join(out)


def _h1(texto, slug):
    """El titulo de capitulo. Las palabras, todas; el peso, repartido.

    "CAPÍTULO 1 — DIAGNÓSTICO" se compone en una linea con la numeracion en
    Barranca y el nombre en Tinta. No se reescribe ni se reordena: el numero de
    seccion grande y en color de acento pegado al titulo es exactamente eso.
    """
    m = RE_H1CAP.match(texto.strip())
    if m:
        return ('<h1 id="%s"><span class="cn">%s</span> %s</h1>'
                % (slug, _inline(m.group(1)), _inline(m.group(2))))
    return '<h1 id="%s">%s</h1>' % (slug, _inline(texto))


def bloques(md, slug):
    """El markdown de un capitulo a una lista de (ancho, html)."""
    lineas = md.split("\n")
    out, i, n = [], 0, len(lineas)
    vistos_h1 = 0
    hay_bajada = False
    # Solo los capitulos tienen bajada: el h2 sin numero que sigue al titulo.
    # En la introduccion ese h2 —"La pregunta"— es una seccion de verdad, y
    # tomarla por bajada la borraba del indice.
    #
    # OJO CON EL ANCLA: la linea del .md es "# CAPÍTULO 1 — …", con la
    # almohadilla adelante. Buscar "^CAPÍTULO" contra el texto crudo no matchea
    # nunca, y entonces NINGUN capitulo tenia bajada: la suya se maquetaba como
    # un titulo de seccion mas, en negrita y en el indice.
    es_capitulo = bool(re.search(r'^#\s+CAPÍTULO\s+\d+', md, re.M))
    subsecciones = []

    def add(ancho, htm):
        out.append((ancho, htm))

    while i < n:
        l = lineas[i]

        m = RE_EXHIBIT.match(l.strip())
        if m:
            add(True, _exhibit(m.group(1).zfill(2), m.group(2).strip()))
            i += 1
            continue

        if l.strip().startswith("|"):
            j = i
            while j < n and lineas[j].strip().startswith("|"):
                j += 1
            t = _tabla(lineas[i:j])
            if t:
                add(*t)
            i = j
            continue

        if l.startswith("### "):
            titulo = l[4:]
            # Nota de lectura al pie de seccion: entrada en negrita corrida con
            # el texto, cuerpo chico, al ancho de la caja.
            if titulo.startswith(NOTAS_AL_PIE):
                j = i + 1
                cuerpo = []
                while j < n and not lineas[j].startswith(("#", "---", "|", "`")):
                    if lineas[j].strip():
                        cuerpo.append(lineas[j].strip())
                    j += 1
                add(True, '<div class="nota-envoltorio">'
                          '<div class="nota-lectura"><p><span class="et">%s.</span> '
                          '%s</p>%s</div>'
                    % (_inline(titulo), _inline(cuerpo[0]) if cuerpo else "",
                       "".join("<p>%s</p>" % _inline(c) for c in cuerpo[1:])
                       + "</div>"))
                i = j
                continue
            tipo = next((t for t, claves in CAJAS
                         if any(titulo.startswith(c) for c in claves)), None)
            if tipo:
                j = i + 1
                cuerpo = []
                while j < n and not lineas[j].startswith(("#", "---", "|", "`")):
                    if lineas[j].strip():
                        cuerpo.append(lineas[j].strip())
                    elif cuerpo:
                        break
                    j += 1
                add(False, '<aside class="caja %s"><h5>%s</h5>%s</aside>'
                    % (tipo, _inline(titulo),
                       "".join("<p>%s</p>" % _inline(c) for c in cuerpo)))
                i = j
                continue
            add(False, "<h3>%s</h3>" % _inline(titulo))

        elif l.startswith("## "):
            crudo = l[3:].strip()
            m2 = RE_H2NUM.match(crudo)
            # El h2 SIN numero que sigue al titulo del capitulo es la bajada.
            if not m2 and es_capitulo and vistos_h1 == 1 and not hay_bajada:
                add(True, '<p class="bajada">%s</p>' % _inline(crudo))
                hay_bajada = True
                i += 1
                continue
            sid = "%s-%s" % (slug, len(subsecciones))
            if m2:
                subsecciones.append((sid, m2.group(1), m2.group(2)))
                add(True, '<h2 id="%s"><span class="n">%s</span>%s</h2>'
                    % (sid, m2.group(1), _inline(m2.group(2))))
            else:
                subsecciones.append((sid, None, crudo))
                add(True, '<h2 id="%s">%s</h2>' % (sid, _inline(crudo)))

        elif l.startswith("# "):
            vistos_h1 += 1
            add(True, _h1(l[2:], slug))

        elif l.startswith("> "):
            j, cita = i, []
            while j < n and lineas[j].startswith(">"):
                cita.append(lineas[j].lstrip("> ").rstrip())
                j += 1
            add(False, '<aside class="caja legal">%s</aside>'
                % "".join("<p>%s</p>" % _inline(c) for c in cita if c))
            i = j
            continue

        elif l.strip() == "---":
            add(True, '<hr>')

        elif re.match(r'^\d+\.\s', l.strip()):
            j, items = i, []
            while j < n and re.match(r'^\d+\.\s', lineas[j].strip()):
                items.append(re.sub(r'^\d+\.\s', '', lineas[j].strip()))
                j += 1
            add(False, "<ol>%s</ol>"
                % "".join("<li>%s</li>" % _inline(x) for x in items))
            i = j
            continue

        elif l.strip().startswith("- "):
            j, items = i, []
            while j < n and lineas[j].strip().startswith("- "):
                items.append(lineas[j].strip()[2:])
                j += 1
            add(False, "<ul>%s</ul>"
                % "".join("<li>%s</li>" % _inline(x) for x in items))
            i = j
            continue

        elif l.strip():
            txt = l.strip()
            if txt in _lista(DATOS, slug):
                add(True, '<p class="dato">%s</p>' % _inline(txt))
            elif txt in _lista(REMATES, slug):
                add(True, '<p class="remate">%s</p>' % _inline(txt))
            else:
                add(False, "<p>%s</p>" % _inline(txt))
        i += 1
    return out, subsecciones


def _lista(mapa, slug):
    """Las frases marcadas de un capitulo, tal como estan escritas en el .md."""
    for nombre, _ in ORDEN:
        if nombre.split(".")[0].lower() == slug:
            return set(mapa.get(nombre, []))
    return set()


# ==========================================================================
# 3. BANDAS
# ==========================================================================

def bandas(lista, seccion):
    """Las corridas de bloques de flujo, cada una en su caja de dos columnas.

    Devuelve una lista de PIEZAS —los bloques de primer nivel de la seccion—,
    cada una con su id, si cruza las dos columnas, y si el acomodador puede
    moverla. El id es lo que despues permite preguntarle a WeasyPrint en que
    pagina cayo cada pieza y cuanto mide.

    Un titulo al pie de la banda con su texto en la siguiente es un salto que el
    lector lee como error. Como el h2 es ancho y la prosa que le sigue es una
    banda aparte, el CSS no puede mantenerlos juntos con break-after: hay que
    envolverlos. El envoltorio agarra el h2 y las PRIMERAS LINEAS de la banda,
    no la banda entera: si agarrara la banda entera, una banda de pagina y media
    con break-inside:avoid se iria completa a la pagina siguiente y dejaria la
    anterior vacia — que es el mismo bug, del otro lado.
    """
    out, i, n = [], 0, len(lista)

    def pieza(htm, tipo):
        # El id va en un envoltorio propio y no en el bloque, para que la caja
        # que devuelve page.anchors sea la de la pieza entera —banda incluida—
        # y no la de su primer elemento.
        pid = "%s%s-%d" % (PREFIJO_PIEZA, seccion, len(out))
        out.append({"id": pid, "tipo": tipo,
                    "html": '<div id="%s" class="pz">%s</div>' % (pid, htm)})

    while i < n:
        ancho, htm = lista[i]
        if ancho:
            # Un h2 arrastra el arranque de la banda que le sigue.
            if htm.startswith("<h2") and i + 1 < n and not lista[i + 1][0]:
                j = i + 1
                corrida = []
                while j < n and not lista[j][0]:
                    corrida.append(lista[j][1])
                    j += 1
                # EL GRUPO ES EL TITULO Y SU PRIMER PARRAFO, Y NADA MAS.
                # Estirarlo —a dos bloques, o a la tabla que sigue— parece que
                # deberia ayudar y hace lo contrario: el grupo se vuelve un
                # ladrillo indivisible de 120 a 157 mm que no entra en el pie de
                # ninguna pagina, se va entero a la siguiente, y deja atras el
                # hueco que se queria evitar. Medido: el hueco total pasa de 678
                # a 1.277 mm.
                #
                # Por eso una tabla NUNCA entra al grupo, ni siquiera si es el
                # primer bloque: una tabla de nueve filas ya pesa mas que el
                # aire que suele quedar al pie.
                if corrida[0].startswith('<div class="tw'):
                    pieza(htm, "ancho")
                    pieza('<div class="banda">%s</div>' % "".join(corrida),
                          "banda")
                    i = j
                    continue
                # LA UNICA EXCEPCION: una entrada que TERMINA EN DOS PUNTOS no
                # es un parrafo, es el pie de una tabla —"Millones de pesos
                # constantes de diciembre de 2025:"—. Separarla de su tabla deja
                # el titulo al pie de la pagina anunciando algo que no esta. Si
                # esa tabla es chica, entra al grupo con ella.
                corte = 1
                if (len(corrida) > 1
                        and _texto_plano(corrida[0]).endswith(":")
                        and corrida[1].startswith('<div class="tw')
                        and corrida[1].count("<tr>") <= 11
                        and len(_texto_plano(corrida[1])) <= 400):
                    corte = 2
                cabeza, resto = corrida[:corte], corrida[corte:]
                grupo = ['<div class="banda">%s</div>' % "".join(cabeza)]
                pieza('<div class="con-titulo">%s%s</div>'
                      % (htm, "".join(grupo)), "titulo")
                if resto:
                    pieza('<div class="banda">%s</div>' % "".join(resto),
                          "banda")
                i = j
                continue
            tipo = ("figura" if htm.startswith(("<figure", '<div class="tw'))
                    else "ancho")
            pieza(htm, tipo)
            i += 1
            continue
        j = i
        corrida = []
        while j < n and not lista[j][0]:
            corrida.append(lista[j][1])
            j += 1
        pieza('<div class="banda">%s</div>' % "".join(corrida), "banda")
        i = j
    return out


# ==========================================================================
# 3bis. EL ACOMODADOR
# ==========================================================================
# UN EXHIBIT QUE NO ENTRA AL PIE DE LA PAGINA SE VA ENTERO A LA SIGUIENTE Y
# DEJA UN HUECO. Ese es el unico hueco que la maqueta por bandas no resuelve
# sola, y es exactamente "paginas a medio llenar".
#
# Lo que hace un armador a mano en ese caso es bajar la figura un parrafo: el
# texto que la sigue sube y llena el pie, y la figura entra al principio de la
# pagina siguiente. Eso es todo lo que hace el acomodador, y no hace nada mas:
#
#   - solo mueve figuras y tablas anchas, nunca titulos ni prosa;
#   - solo las intercambia con la banda de prosa que viene INMEDIATAMENTE
#     despues, asi que la figura nunca se separa de su seccion ni se cruza con
#     un titulo. Se aleja un parrafo del texto que la llama, no mas;
#   - como maximo dos saltos por figura;
#   - y cada cambio se MIDE sobre el PDF rearmado: si el hueco total no baja,
#     se deshace. El acomodador no propone, comprueba.
#
# La medida sale de WeasyPrint, no de mirar el PNG: cada pieza lleva un id y
# page.anchors devuelve su caja. El hueco de una pagina es la distancia entre el
# fondo de la ultima pieza que cayo en ella y el fin de la caja de texto.

HUECO_MINIMO = 26.0     # mm: menos que esto no es un hueco, es el aire del pie
PASADAS_MAXIMAS = 8     # cada pasada rearma el PDF entero; ocho alcanzan
SALTOS_MAXIMOS = 2      # cuantas veces se puede bajar una misma figura


def _huecos(doc, fin_pt):
    """Por pagina: el hueco al pie en mm, y la pieza que la abre.

    Las paginas sin ninguna pieza —la tapa y el indice— quedan en (None, None):
    no tienen hueco que medir porque no las arma el flujo del cuerpo.
    """
    fuera = []
    for pag in doc.pages:
        if not pag.anchors:
            fuera.append((None, None))
            continue
        fondo = min(max(caja[3] for caja in pag.anchors.values()), fin_pt)
        # Los h1 y los h2 tambien dejan ancla —las usa el indice para su numero
        # de pagina— y no son piezas. Si se las toma por piezas, el acomodador
        # cree que la pagina la abre un titulo, no encuentra esa clave entre las
        # piezas y se saltea la pagina. Por eso la pieza que abre se busca solo
        # entre las anclas con el prefijo de pieza.
        propias = {k: v for k, v in pag.anchors.items()
                   if k.startswith(PREFIJO_PIEZA)}
        abre = (min(propias.items(), key=lambda kv: (kv[1][1], kv[1][0]))[0]
                if propias else None)
        fuera.append(((fin_pt - fondo) * 25.4 / 72.0, abre))
    return fuera


def _hueco_evitable(huecos, cierres, doc):
    """El hueco total que SE PUEDE arreglar moviendo algo.

    La ultima pagina de cada capitulo termina donde se le acaba el texto, y el
    capitulo siguiente empieza en pagina nueva: ese hueco no es un defecto de
    armado y no hay nada que moverle. Meterlo en la cuenta ademas ARRUINA la
    medida, porque vale doscientos milimetros y tapa por completo las mejoras de
    veinte que si son reales — con esa cuenta el acomodador se frenaba en la
    primera pasada creyendo que no habia mejorado.
    """
    finales = set()
    for i, pag in enumerate(doc.pages):
        if pag.anchors and cierres & set(pag.anchors):
            finales.add(i)
    return sum(h for i, (h, _) in enumerate(huecos)
               if h and h > HUECO_MINIMO and i not in finales)


def acomodar(piezas, css_txt, envolver, cierres):
    """Baja las figuras que dejan la pagina a medio llenar. Y lo comprueba."""
    from weasyprint import HTML, CSS as WCSS
    hoja = [WCSS(string=css_txt)]
    cache = {}

    def medir(orden):
        doc = HTML(string=envolver(orden), base_url=RAIZ).render(
            stylesheets=hoja, cache=cache)
        fin_pt = doc.pages[0].height - MARGEN_PIE * 72 / 25.4
        huecos = _huecos(doc, fin_pt)
        return huecos, _hueco_evitable(huecos, cierres, doc)

    orden = list(piezas)
    huecos, mejor = medir(orden)
    saltos, movidos = {}, 0

    for _ in range(PASADAS_MAXIMAS):
        indice = {p["id"]: k for k, p in enumerate(orden)}
        # LO QUE NO ENTRO EN LA PAGINA CON HUECO ES LO QUE ABRE LA SIGUIENTE.
        # Esa es la pieza que hay que bajar, no la que abre la pagina del hueco:
        # bajandola, la prosa que la seguia sube y llena el pie.
        saltar = []
        for i, (hueco, _) in enumerate(huecos):
            if not hueco or hueco <= HUECO_MINIMO or i + 1 >= len(huecos):
                continue
            abre = huecos[i + 1][1]
            k = indice.get(abre)
            if k is None or k + 1 >= len(orden):
                continue
            if orden[k]["tipo"] != "figura" or orden[k + 1]["tipo"] != "banda":
                continue
            if saltos.get(abre, 0) >= SALTOS_MAXIMOS:
                continue          # una figura no se aleja mas de dos parrafos
            saltar.append((k, abre))
        # Dos saltos contiguos se pisarian: se toma uno de cada par.
        saltar = [x for j, x in enumerate(saltar)
                  if j == 0 or x[0] > saltar[j - 1][0] + 1]
        if not saltar:
            break

        def probar(lote):
            prueba = list(orden)
            for k, _ in lote:
                prueba[k], prueba[k + 1] = prueba[k + 1], prueba[k]
            return (prueba,) + medir(prueba)

        prueba, h2, total2 = probar(saltar)
        # Bajar todas las figuras de una es rapido pero grosero: un solo salto
        # que empeora tapa a los otros cinco que mejoran. Si el lote entero no
        # mejora, se prueba solo el de la pagina con MAS hueco, que es el que
        # mas tiene para ganar. Recien si ese tampoco mejora se corta.
        if total2 >= mejor - 1.0 and len(saltar) > 1:
            solo = max(saltar, key=lambda x: huecos[
                next(i for i, (h, _) in enumerate(huecos)
                     if h and h > HUECO_MINIMO)][0] if False else 0)
            solo = saltar[0]
            mejor_hueco, elegido = -1, None
            for k, abre in saltar:
                for i, (h, _) in enumerate(huecos):
                    if h and i + 1 < len(huecos) and huecos[i + 1][1] == abre:
                        if h > mejor_hueco:
                            mejor_hueco, elegido = h, (k, abre)
            solo = elegido or solo
            prueba, h2, total2 = probar([solo])
            saltar = [solo]
        if total2 >= mejor - 1.0:
            break                      # no mejoro: se deshace y se corta
        for _, abre in saltar:
            saltos[abre] = saltos.get(abre, 0) + 1
        orden, huecos, mejor = prueba, h2, total2
        movidos += len(saltar)
    return orden, movidos, mejor


# ==========================================================================
# 4. TAPA E INDICE
# ==========================================================================

def tapa():
    """El mapa ocupa la pagina y el titulo va encima.

    El PNG del mapa tiene el fondo en PAPEL, el mismo del documento, asi que
    sangrarlo a los cuatro lados no deja borde: la mancha del partido queda
    flotando en la pagina y el titulo se apoya en el aire que el mapa deja
    arriba a la izquierda. Antes el mapa era una figura chica en el medio con
    dos margenes blancos, y el tercio de abajo quedaba vacio.

    Sin nombre ni foto del candidato. Decision cerrada en la identidad.
    """
    mapa = os.path.join(CHARTS, "TAPA_mapa_zonas.png")
    return ('<section class="tapa">'
            '<img class="tapa-img" src="file://%s" alt=""/>'
            '<div class="tapa-txt">'
            '<h1 class="t1">%s</h1><h1 class="t2">%s</h1>'
            '<p class="sub">%s</p></div>'
            '</section>' % (mapa, TITULO, ANIO, SUBTITULO))


def indice(entradas):
    """Indice con la pagina real de cada seccion y de cada subseccion."""
    filas = []
    for slug, titulo, subs in entradas:
        filas.append('<li class="ix-cap"><a href="#%s">'
                     '<span class="ix-t">%s</span></a></li>'
                     % (slug, html.escape(titulo)))
        for sid, num, tit in subs:
            filas.append('<li class="ix-sub"><a href="#%s">'
                         '<span class="ix-n">%s</span>'
                         '<span class="ix-t">%s</span></a></li>'
                         % (sid, html.escape(num or ""), html.escape(tit)))
    return ('<section class="indice"><h1 class="ix-h">Índice</h1>'
            '<ul class="ix">%s</ul></section>' % "".join(filas))


# ==========================================================================
# 5. CSS
# ==========================================================================

CSS = """
@font-face { font-family: "%(serif)s";
             src: url("file://%(tipos)s/SourceSerif4[opsz,wght].ttf");
             font-weight: 200 900; font-style: normal; }
@font-face { font-family: "%(serif)s";
             src: url("file://%(tipos)s/SourceSerif4-Italic[opsz,wght].ttf");
             font-weight: 200 900; font-style: italic; }

@page {
  size: A4; margin: 17mm 17mm %(pie)dmm 17mm; background: %(papel)s;
  @top-left     { content: string(cap); font-family: "%(serif)s";
                  font-size: 7.4pt; font-weight: 600; letter-spacing: .9pt;
                  color: %(ambar)s; text-transform: lowercase;
                  font-variant-caps: small-caps; margin-bottom: 6mm; }
  @bottom-left  { content: "%(corto)s"; font-family: "%(serif)s";
                  font-size: 7pt; letter-spacing: .1pt; white-space: pre;
                  color: %(tinta)s; opacity: .55; vertical-align: top; }
  @bottom-right { content: "Página " counter(page) " de " counter(pages);
                  font-family: "%(serif)s"; font-size: 7pt;
                  font-variant-numeric: tabular-nums lining-nums;
                  white-space: pre; color: %(tinta)s; opacity: .55;
                  vertical-align: top; }
  /* La regla del pie es el borde de abajo de la caja de pagina: cae justo
     entre el final de la caja de texto y la linea del pie, y no le come ancho
     a ninguna de las dos cajas de margen. Poner la regla como border-top de
     @bottom-left obligaba a fijarle un ancho, y ese ancho aplastaba el numero
     de pagina hasta partirlo en tres lineas. */
  border-bottom: .4pt solid %(cal)s; padding-bottom: 3.5mm;
}
@page :first { margin: 0; border: 0; padding: 0;
  @top-left { content: ""; } @bottom-left { content: ""; }
  @bottom-right { content: ""; } }

html { background: %(papel)s; }
body { font-family: "%(serif)s", Georgia, serif; font-size: 8.7pt;
       line-height: 1.42; color: %(tinta)s;
       font-variation-settings: "opsz" %(opsz)d;
       font-variant-numeric: lining-nums; }

/* --------------------------------------------------------------------
   BANDAS. La prosa a dos columnas balanceadas; todo lo demas al ancho.
   column-fill: balance (el que viene por defecto) es lo que evita que la
   primera columna se estire hasta el pie de la pagina.
   -------------------------------------------------------------------- */
.banda { columns: 2; column-gap: 6.5mm; }
.banda > *:first-child { margin-top: 0; }
.con-titulo { break-inside: avoid; }
.con-titulo .banda { margin-top: 0; }

p { margin: 0 0 .55em; text-align: justify; hyphens: auto; }
p, li { orphans: 3; widows: 3; }
strong { font-weight: bold; }
em { font-style: italic; }
code { font-family: "DejaVu Sans Mono"; font-size: 7.4pt; background: %(cal)s;
       padding: .5pt 2pt; }
a { color: %(rio)s; text-decoration: none; }
hr { border: 0; border-top: .5pt solid %(cal)s; margin: 1.1em 0 .95em; }

/* --------------------------------------------------------------------
   JERARQUIA
   -------------------------------------------------------------------- */
/* Titulo de capitulo: la numeracion en Barranca, el nombre en Tinta, una
   regla gruesa encima. Empieza pagina. */
h1 { font-size: 17.5pt; line-height: 1.16; margin: 0 0 .24em;
     font-weight: 700; font-variation-settings: "opsz" %(opszt)d;
     letter-spacing: .2pt; string-set: cap content();
     break-before: page; break-after: avoid;
     border-top: 1.6pt solid %(barranca)s; padding-top: 2.6mm; }
h1 .cn { color: %(barranca)s; }

/* La bajada: una linea que dice de que va la seccion, en italica. */
p.bajada { font-style: italic; font-size: 11pt;
           font-variation-settings: "opsz" 14; line-height: 1.32;
           color: %(rio)s; margin: .12em 0 .85em; max-width: 150mm;
           text-align: left; hyphens: none; break-after: avoid; }

/* NUMERO DE SECCION GRANDE, EN SERIF, EN ACENTO, PEGADO AL TITULO. */
h2 { font-size: 12.8pt; line-height: 1.18; margin: 1.25em 0 .5em;
     font-weight: 600; font-variation-settings: "opsz" 16;
     color: %(tinta)s; break-after: avoid; break-inside: avoid;
     text-indent: -0.05em; }
h2 .n { font-size: 17pt; font-weight: 700; color: %(barranca)s;
        font-variant-numeric: lining-nums;
        margin-right: .3em; letter-spacing: -.2pt; }
h1 + p.bajada + .banda h2:first-child,
h1 + p.bajada + .con-titulo > h2 { margin-top: .2em; }

h3 { font-size: 9.6pt; font-weight: 700;
     margin: 1.35em 0 .4em; color: %(tinta)s;
     break-after: avoid; break-inside: avoid; }
h3::before { content: ""; display: block; width: 9mm;
             border-top: 1.4pt solid %(barranca)s; margin-bottom: 1.6mm; }

/* --------------------------------------------------------------------
   CIFRAS DESTACADAS Y REMATES
   -------------------------------------------------------------------- */
/* Un dato que merece verse sin leer. Son parrafos que YA estan escritos como
   una cifra sola; solo se les da el peso que tienen. */
p.dato { font-size: 15pt; line-height: 1.24; color: %(barranca)s;
         font-variation-settings: "opsz" 16;
         margin: 1.1em 0 1.15em; padding: 3.5mm 0 3.5mm 5mm;
         border-left: 3.5pt solid %(barranca)s; text-align: left;
         hyphens: none; break-inside: avoid; max-width: 158mm; }
p.dato strong { color: %(tinta)s; font-weight: bold; }

/* Una por seccion, y solo las que ya estaban escritas. */
p.remate { font-size: 11.2pt; line-height: 1.34; color: %(tinta)s;
           font-variation-settings: "opsz" 14;
           font-style: italic; margin: 1.1em 0 1.2em; padding: 0 0 0 5mm;
           border-left: 2.5pt solid %(rio)s; text-align: left;
           hyphens: none; break-inside: avoid; max-width: 158mm; }
p.remate strong { font-style: normal; font-weight: bold; }

/* --------------------------------------------------------------------
   CAJAS. Tres usos y ninguno mas.
   -------------------------------------------------------------------- */
.caja { break-inside: avoid; margin: .9em 0 1.05em; padding: 2.4mm 3mm;
        background: %(cal)s; font-size: 8.2pt; line-height: 1.42; }
.caja h5 { font-size: 7.6pt; font-weight: 700; letter-spacing: .55pt;
           text-transform: lowercase; font-variant-caps: small-caps;
           margin: 0 0 1.6mm; color: %(ambar)s; line-height: 1.32; }
.caja p { margin: 0 0 .45em; text-align: left; hyphens: none; }
.caja p:last-child { margin-bottom: 0; }
.caja.metodo { border-left: 2.5pt solid %(ambar)s; }
.caja.hipotesis { border-left: 2.5pt solid %(barranca)s; }
.caja.legal { border-left: 2.5pt solid %(rio)s; font-style: italic; }

/* Nota de lectura al pie de seccion: cuerpo chico, entrada en negrita. */
.nota-lectura { margin: 1.1em 0 1.15em;
                border-top: .5pt solid %(cal)s; padding-top: 2.4mm;
                font-size: 7.9pt; line-height: 1.4; color: %(tinta)s;
                opacity: .82; columns: 2; column-gap: 6.5mm; }
/* LA NOTA NO SE PARTE. Se probaron las dos: dejandola partir, el resto caia
   arriba de la pagina siguiente en una, cuatro u ocho lineas sueltas, que se
   leen como un error de armado. Sin partir, cuando no entra al pie se va
   entera y la ultima pagina del capitulo queda con la nota sola. Eso segundo
   se lee como un colofon, que es lo que la nota es. */
/* El que lleva el break-inside es el ENVOLTORIO y no la caja de dos columnas:
   WeasyPrint parte igual una caja multicolumna aunque le pidas que no. */
.nota-envoltorio { break-inside: avoid; }
.nota-lectura p { margin: 0 0 .4em; text-align: left; hyphens: none; }
.nota-lectura .et { font-weight: bold; opacity: 1; }

.et { font-size: 7.4pt; font-weight: 700; letter-spacing: .5pt;
      text-transform: lowercase; font-variant-caps: small-caps;
      font-style: normal; color: %(ambar)s; }

ul, ol { margin: 0 0 .65em; padding: 0 0 0 4.6mm; }
li { margin-bottom: .3em; text-align: justify; hyphens: auto; }
ul li::marker { color: %(barranca)s; }
ol li::marker { color: %(barranca)s; font-weight: bold; }

/* --------------------------------------------------------------------
   TABLAS. Banda de encabezado oscura, versalitas claras, filas alternadas,
   primera columna en color.
   -------------------------------------------------------------------- */
.tw { break-inside: avoid; margin: .85em 0 1em; }
.tw.ancho { margin: 1em 0 1.1em; }
table { width: 100%%; border-collapse: collapse; font-size: 7.5pt;
        line-height: 1.3;
        font-variant-numeric: tabular-nums lining-nums; }
.tw:not(.ancho) table { font-size: 7.1pt; }
/* VERSALITAS DE VERDAD en la banda de encabezado: el texto se pasa a
   minuscula y la fuente devuelve sus versalitas dibujadas. Puestas como
   mayusculas achicadas, el trazo sale mas fino que el de la fila de abajo y la
   banda se ve descolorida. */
thead th { background: %(tinta)s; color: %(papel)s; text-align: left;
           padding: 2.1mm 2.2mm; font-size: 7.3pt; font-weight: 600;
           letter-spacing: .5pt; text-transform: lowercase;
           font-variant-caps: small-caps; line-height: 1.22;
           vertical-align: bottom; }
td { padding: 1.5mm 2.2mm; border-bottom: .4pt solid %(cal)s;
     vertical-align: top; }
tbody tr:nth-child(odd) { background: rgba(237, 233, 226, .55); }
tbody td:first-child { color: %(rio)s; font-weight: bold; }
th:not(:first-child), td:not(:first-child) { text-align: right; }
th:first-child, td:first-child { text-align: left; }
/* Una tabla de texto no se alinea a la derecha: ahi la columna no es una
   cifra, es una oracion. */
.tw.texto th, .tw.texto td { text-align: left; }
.etq { font-style: italic; font-size: 7pt;
       line-height: 1.34; margin: 1.6mm 0 0; color: %(tinta)s; opacity: .62;
       text-align: left; hyphens: none; }
.etq .et { opacity: 1; }

/* --------------------------------------------------------------------
   EXHIBITS. Rotulo en versalitas, titulo que dice la conclusion, bajada,
   figura, y fuente al pie en cuerpo 6-7 italico gris.
   -------------------------------------------------------------------- */
.exh { break-inside: avoid; margin: 1em 0 1.15em; }
.exh-cab { margin-bottom: 1.8mm; break-after: avoid; }
.exh-rot { font-size: 7.6pt; font-weight: 700; letter-spacing: .8pt;
           text-transform: lowercase; font-variant-caps: small-caps;
           color: %(ambar)s; margin: 0 0 1.1mm; text-align: left; }
.exh-tit { font-size: 11.2pt; font-weight: 600; line-height: 1.2;
           color: %(barranca)s; margin: 0; text-align: left; hyphens: none;
           font-variation-settings: "opsz" 14; }
.exh-baj { font-size: 7.6pt; line-height: 1.34;
           color: %(tinta)s; opacity: .68; margin: 1.3mm 0 0; text-align: left;
           hyphens: none; max-width: 168mm; }
.exh img { display: block; margin: 0 auto; max-width: 100%%;
           max-height: 58mm; width: auto; height: auto; }
/* Los dos mapas y las listas largas. A 78 mm el mapa entraba en la mitad del
   ancho de la caja y la otra mitad quedaba en papel: el partido es una franja
   en diagonal y su lienzo es casi cuadrado, asi que lo que manda es el alto.
   El acomodador se encarga del hueco que deje al pie de pagina. */
.exh.alto img { max-height: 84mm; }
.exh-fuente, .exh-nota { font-style: italic;
                         font-size: 7pt; line-height: 1.34; margin: 1.8mm 0 0;
                         text-align: left; hyphens: none; opacity: .66; }
.exh-nota { color: %(ambar)s; opacity: .95; margin-top: 1.2mm; }

/* --------------------------------------------------------------------
   TAPA
   -------------------------------------------------------------------- */
.tapa { position: relative; width: 210mm; height: 297mm; overflow: hidden;
        page-break-after: always; }
.tapa-img { position: absolute; left: -11mm; bottom: 4mm; width: 232mm;
            height: auto; }
.tapa-txt { position: absolute; left: 17mm; top: 30mm; width: 165mm; }
.tapa h1 { font-size: 27pt; line-height: 1.15; margin: 0; letter-spacing: .4pt;
           border: 0; padding: 0; break-before: avoid; font-weight: 700;
           font-variation-settings: "opsz" 40; }
.tapa .t2 { color: %(rio)s; margin-bottom: 6mm; }
.tapa .sub { font-size: 11pt; line-height: 1.5; text-align: left;
             max-width: 118mm; margin: 0; hyphens: none;
             border-top: 1.6pt solid %(barranca)s; padding-top: 4mm;
             display: inline-block; }
/* --------------------------------------------------------------------
   INDICE
   -------------------------------------------------------------------- */
.indice { break-before: page; }
h1.ix-h { font-size: 17.5pt; margin-bottom: 5mm; }
ul.ix { list-style: none; margin: 0; padding: 0;
        font-variant-numeric: tabular-nums lining-nums; }
ul.ix li { margin: 0; }
ul.ix a { color: %(tinta)s; display: block; text-decoration: none;
          padding-bottom: 1.1mm; }
ul.ix a::after { content: target-counter(attr(href), page); float: right;
                 font-size: 8.2pt; color: %(tinta)s; opacity: .6;
                 padding-left: 3mm; }
li.ix-cap { margin-top: 3.6mm; }
li.ix-cap:first-child { margin-top: 0; }
li.ix-cap a { font-size: 10.8pt; color: %(barranca)s;
              border-bottom: .6pt solid %(barranca)s; padding-bottom: 1.6mm; }
li.ix-cap a::after { color: %(barranca)s; opacity: 1; font-weight: bold;
                     font-size: 8.4pt; }
li.ix-sub a { font-size: 8.1pt; padding: .85mm 0 .85mm;
              border-bottom: .4pt dotted rgba(22, 41, 58, .22); }
span.ix-n { display: inline-block; width: 11mm; color: %(rio)s;
            font-weight: bold; }
""" % dict(papel=PAPEL, tinta=TINTA, rio=RIO, barranca=BARRANCA,
           cal=CAL, ambar=AMBAR, corto=TITULO_CORTO, pie=MARGEN_PIE,
           serif=SERIF, tipos=TIPOS, opsz=OPSZ_TEXTO, opszt=OPSZ_TITULO)


# ==========================================================================
# 6. VERIFICACION DEL PDF YA ARMADO
# ==========================================================================

def verificar_pdf(ruta):
    """Falla si sobrevive un pendiente, una nota de version, o aparece rojo."""
    problemas = []
    txt = subprocess.run(["pdftotext", "-q", "-layout", ruta, "-"],
                         capture_output=True, text=True).stdout
    for frase in (MARCADOR, "NO VA AL PDF", "Pendientes de este capítulo"):
        if frase in txt:
            problemas.append("se coló texto de pendientes: %r" % frase)
    # Las dos palabras de la nota de version no aparecen en ninguna otra parte
    # del texto publicable, asi que encontrarlas es encontrar la nota.
    for frase in ("Borrador", "Reemplaza al borrador"):
        if frase in txt:
            problemas.append("sobrevivió la nota de versión: %r" % frase)
    crudo = open(ruta, "rb").read().decode("latin-1")
    for rojo in ("#FF0000", "#F00", "1 0 0 rg", "1 0 0 RG"):
        if rojo in crudo:
            problemas.append("aparece rojo: %s" % rojo)
    return problemas, txt


# ==========================================================================

def main():
    from weasyprint import HTML, CSS as WCSS

    entradas, piezas = [], []
    for nombre, titulo in ORDEN:
        slug = nombre.split(".")[0].lower()
        lista, subs = bloques(leer_publicable(nombre), slug)
        entradas.append((slug, titulo, subs))
        piezas.append(bandas(lista, slug))

    def envolver(orden_de_piezas, secciones=None):
        """Las piezas ya acomodadas, adentro del documento completo."""
        cuerpo = "\n".join(p["html"] for p in orden_de_piezas)
        partes = [tapa(), indice(secciones if secciones is not None else entradas),
                  '<section class="cap">%s</section>' % cuerpo]
        return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
                '<title>%s</title></head><body>%s</body></html>'
                % (TITULO_CORTO, "\n".join(partes)))

    # La ultima pieza de cada capitulo: su pagina no cuenta como hueco.
    cierres = {seccion[-1]["id"] for seccion in piezas if seccion}
    planas = [p for seccion in piezas for p in seccion]
    planas, movidos, hueco = acomodar(planas, CSS, envolver, cierres)

    doc = envolver(planas)
    with open(os.path.join(RAIZ, "_pdf_build.html"), "w", encoding="utf-8") as f:
        f.write(doc)

    HTML(string=doc, base_url=RAIZ).write_pdf(
        SALIDA, stylesheets=[WCSS(string=CSS)])

    from pypdf import PdfReader
    paginas = len(PdfReader(SALIDA).pages)
    problemas, txt = verificar_pdf(SALIDA)
    # Los rotulos van en VERSALITAS: el texto real es minuscula y la fuente
    # dibuja las versalitas. pdftotext devuelve la minuscula, y ademas le mete
    # un espacio a cada letra interletrada. Por eso se cuenta sobre el texto sin
    # espacios y sin distinguir mayusculas.

    plano = re.sub(r'\s+', '', txt).lower()
    print("=" * 74)
    print("PDF ARMADO — %s" % os.path.basename(SALIDA))
    print("=" * 74)
    print("  páginas            : %d" % paginas)
    print("  secciones          : %d" % len(ORDEN))
    print("  subsecciones       : %d" % sum(len(s) for _, _, s in entradas))
    print("  exhibits insertados: %d" % plano.count("exhibit"))
    print("  figuras acomodadas : %d" % movidos)
    print("  hueco evitable     : %.0f mm en total" % hueco)
    print("  etiquetas          : %s"
          % (", ".join("%s x%d" % (e, plano.count(e.replace(" ", "").lower()))
                       for e in sorted(LEYENDA_ETIQUETA)
                       if plano.count(e.replace(" ", "").lower())) or "ninguna"))
    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print("   ", p)
        return 1
    print("\n  corte de pendientes: limpio")
    print("  nota de versión    : ausente")
    print("  rojo               : ausente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
