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
# Spectral, de Production Type para Google, e Inter, de Rasmus Andersson.
# Las dos bajo SIL Open Font License 1.1 (05_tipografia/OFL-Spectral.txt y
# OFL-Inter.txt). Los archivos estan versionados en el repo y el CSS los carga
# con @font-face apuntando a la RUTA, no al nombre de una fuente instalada. La
# diferencia importa en un documento con indice: si el armado dependiera de que
# la fuente este en la maquina, en una sin ella WeasyPrint caeria a otra,
# cambiaria el ancho de cada linea, y el indice imprimiria numeros que no son.
#
# POR QUE ESTAS DOS: porque son las de la referencia. Medido con pdfplumber
# sobre las treinta paginas del Extra Time, el PDF trae exactamente estos dos
# nombres —Spectral en Regular, Italic, MediumItalic, SemiBold y Bold, e Inter
# Regular— y ninguno mas. Estaba vendorizada Source Serif 4, que es una serif
# excelente y no es la de la referencia. Copiar el sistema incluye copiar la
# letra: el color de la mancha a cuerpo 9,7 en columna de 85 mm es la mitad de
# lo que hace que dos paginas se parezcan.
#
# Spectral es la serif de TEXTO y de TITULO. Inter es la sans, y aparece solo
# donde la referencia la usa: cornisa, rotulo de exhibit, cabecera de tabla,
# cuerpo de tabla, rotulos dentro de los graficos y pie de pagina. Nunca en
# prosa.
#
# Los cortes son ESTATICOS, no variables: Spectral no tiene eje de tamaño
# optico, asi que no hay nada que instanciar y cada peso es su archivo.
TIPOS = os.path.join(RAIZ, "05_tipografia")
SERIF = "Spectral"
SANS = "Inter"
# Los seis cortes de Spectral que usa la referencia, con el peso y el estilo
# con que el CSS los va a pedir.
CORTES_SERIF = [("Spectral-Regular.ttf", 400, "normal"),
                ("Spectral-Italic.ttf", 400, "italic"),
                ("Spectral-Medium.ttf", 500, "normal"),
                ("Spectral-MediumItalic.ttf", 500, "italic"),
                ("Spectral-SemiBold.ttf", 600, "normal"),
                ("Spectral-Bold.ttf", 700, "normal")]

# --------------------------------------------------------------------------
# LOS HUECOS DE LAS IMAGENES GENERADAS
# --------------------------------------------------------------------------
# La tapa y la apertura de cada capitulo llevan una imagen generada. NO se
# generan aca ni las genera este armador: llegan como archivos a 08_imagenes/ y
# el armador solo las coloca. Si no estan, el documento se arma igual — la tapa
# vuelve al mapa y los capitulos abren sin banda — asi que el hueco vacio nunca
# rompe el build.
#
# QUE TIENE QUE LLEGAR, Y CON QUE MEDIDA:
#
#   08_imagenes/tapa.png            2480 x 3508 px   vertical, 1:1,414 (A4)
#                                   sangra la pagina entera, con el titulo
#                                   encima; la mitad de arriba tiene que quedar
#                                   tranquila para que el titulo se lea.
#
#   08_imagenes/apertura_cap1.png   2100 x 700 px    apaisada, 3:1
#   … hasta apertura_cap6.png       banda al ancho de la caja de texto, arriba
#                                   del titulo de capitulo.
#
# Las dos a 300 dpi. ABSTRACTAS O CONCEPTUALES: ninguna imagen puede parecer
# una fotografia de un lugar o de una persona de San Isidro. Si alguien
# descubriera que una imagen de La Cava o de Beccar es sintetica, el documento
# pierde lo unico que tiene, que es que se le pueden revisar las cuentas.
# Por eso ademas cada una lleva su linea al pie diciendo que es una ilustracion.
IMAGENES = os.path.join(RAIZ, "08_imagenes")
PIE_ILUSTRACION = ("Ilustración generada. No es una fotografía de San Isidro "
                   "ni de ninguno de sus barrios.")


def imagen(nombre):
    """La ruta de una imagen generada, o None si todavia no llego."""
    ruta = os.path.join(IMAGENES, nombre)
    return ruta if os.path.exists(ruta) else None


MARCADOR = "# NO VA AL PDF"
MARGEN_PIE = 15          # mm: el margen de abajo de @page, que mide el hueco
# WeasyPrint mide TODO en pixeles CSS, que son 96 por pulgada, no en puntos.
# El acomodador convertia con 72 y ademas restaba el margen del pie en puntos:
# los huecos salian inflados un tercio y el umbral de 26 mm era en realidad de
# 19,5. Nada se rompia —la medida es comparativa y el orden se mantiene— pero el
# numero que el armador imprime es un numero que alguien va a leer.
PX_POR_MM = 96 / 25.4
# Las piezas llevan prefijo propio en el id: los h1 y los h2 tambien dejan
# ancla y el acomodador tiene que poder distinguirlas.
PREFIJO_PIEZA = "pz-"
# Las dos lineas del encabezado que son metadato del taller y no del programa.
RE_VERSION = re.compile(
    r'^\*\s*(?:Borrador\b|Reemplaza al borrador\b).*\*\s*$', re.M)

# --------------------------------------------------------------------------
# LA PALETA — la del informe de referencia, y nada mas
# --------------------------------------------------------------------------
# Muestreada de su PDF pixel por pixel: son los seis colores mas frecuentes de
# sus paginas descontando los grises del antialias. Se usa tal cual, y es la
# misma que estilo.py le da a los veinte exhibits, asi que el documento y sus
# graficos son una sola cosa.
#
# EL ACENTO ES UN ROJO LADRILLO. La regla anterior prohibia el rojo porque en
# la Argentina se lee como color politico. Queda sin efecto por decision
# tomada. Lo que verificar_pdf() sigue buscando es el rojo PURO, que es otra
# cosa y nunca es una eleccion de diseño sino un valor por defecto que se colo.
CREMA = "#F5F0E8"        # el fondo de toda la pagina
TINTA = "#2A211C"        # el texto, negro calido
ACENTO = "#7C2E23"       # ladrillo: eyebrow, numeros de seccion, titulos
DATO = "#5E7157"         # verde salvia: la serie principal
DATO_CLARO = "#7E9070"   # salvia clara: la cuarta serie
ARENA = "#EAE0CF"        # bandas de encabezado y cajas laterales
FILA = "#E8E4D9"         # filas alternadas

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


# ==========================================================================
# EL RENUMERADO
# ==========================================================================
# Los exhibits se numeraron por capitulo mientras se hacian, asi que el lector
# encontraba el 15 en la pagina 7 y el 1 en la pagina 11. Un numero que no
# sigue el orden de lectura no sirve para nada: no ayuda a buscar y hace pensar
# que faltan.
#
# Se renumeran POR ORDEN DE APARICION, del 1 al 20 y sin saltos. Se hace ACA, al
# armar, y no en los .md ni en los nombres de archivo: el nombre del PNG y el
# `[EXHIBIT 15 — ...]` del capitulo siguen siendo el identificador estable con
# el que se hizo el grafico y con el que se lo vuelve a encontrar. Lo que cambia
# es como se lo llama en la pagina.

# La misma expresion, pero para buscarla LINEA POR LINEA adentro del texto
# entero de un capitulo. RE_EXHIBIT va anclada con ^...$ y sin MULTILINE solo
# matchea si el capitulo empieza con un exhibit: sin esto el mapa de numeros
# salia vacio y todos los exhibits conservaban su numero viejo, en silencio.
RE_EXHIBIT_TEXTO = re.compile(RE_EXHIBIT.pattern, re.M)


def numeros_por_aparicion():
    """{numero viejo: numero nuevo}, recorriendo los capitulos en orden."""
    vistos = []
    for nombre, _ in ORDEN:
        for m in RE_EXHIBIT_TEXTO.finditer(leer_publicable(nombre)):
            n = m.group(1).zfill(2)
            if n not in vistos:
                vistos.append(n)
    return {viejo: i for i, viejo in enumerate(vistos, 1)}


NUMEROS = {}
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
    clase = "exh" if proporcion >= 1.45 else "exh alto"

    cab = ['<p class="exh-rot">Exhibit %d</p>' % NUMEROS.get(num, int(num))]
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


def _apertura(slug):
    """La banda ilustrada que abre un capitulo, si llego su archivo."""
    m = re.match(r"^cap(\d+)_", slug)
    if not m:
        return ""
    ruta = imagen("apertura_cap%s.png" % m.group(1))
    if not ruta:
        return ""
    return ('<figure class="apertura"><img src="file://%s" alt=""/>'
            '<figcaption>%s</figcaption></figure>'
            % (ruta, html.escape(PIE_ILUSTRACION)))


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
    # LA ENTRADA. En la referencia el primer parrafo de cada capitulo va a
    # TODO EL ANCHO y un punto mas grande que el cuerpo, y recien despues
    # empiezan las columnas. Es lo que le da a la pagina de apertura una
    # entrada de lectura en vez de tirar al lector directo a una columna de
    # 85 mm. Se marca el parrafo que sigue a la bajada del capitulo.
    toca_entrada = [False]

    def add(ancho, htm):
        # Cualquier pieza que no sea la entrada misma cancela la espera: la
        # entrada es el parrafo que viene PEGADO a la bajada, no el primer
        # parrafo que aparezca tres titulos mas abajo.
        if out and 'class="entrada"' not in htm and 'class="bajada"' not in htm:
            toca_entrada[0] = toca_entrada[0] and htm.startswith("<p>")
        out.append((ancho, htm))

    while i < n:
        l = lineas[i]

        m = RE_EXHIBIT.match(l.strip())
        if m:
            add(True, _exhibit(m.group(1).zfill(2), m.group(2).strip()))
            i += 1
            continue

        # LOS BLOQUES CERCADOS SON LISTADOS, Y VAN AL ANCHO DE LA CAJA.
        # No habia rama para ellos: cada linea de adentro caia como un parrafo
        # suelto, en serif, justificada y partida por la columna de 85 mm. Las
        # cuatro ultimas paginas del anexo —la salida del verificador
        # geografico, la lista de comandos para reproducir los numeros— eran
        # por eso un muro ilegible. Al ancho de la caja y en monoespaciada, la
        # linea mas larga de todas mide 68 caracteres y entran holgadas.
        if l.strip().startswith("```"):
            j = i + 1
            crudas = []
            while j < n and not lineas[j].strip().startswith("```"):
                crudas.append(lineas[j])
                j += 1
            if crudas:
                add(True, '<pre class="listado">%s</pre>'
                    % "\n".join(_escapar(x) for x in crudas))
            i = j + 1
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
                toca_entrada[0] = True
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
            banda = _apertura(slug)
            if banda:
                add(True, banda)
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
            elif toca_entrada[0]:
                add(True, '<p class="entrada">%s</p>' % _inline(txt))
                toca_entrada[0] = False
            else:
                add(False, "<p>%s</p>" % _inline(txt))
        i += 1
    return out, subsecciones


def _escapar(t):
    """El texto de un listado va tal cual: sin negritas, sin cursivas, y con
    los tres caracteres que el HTML se comeria puestos como entidad."""
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


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


# Cuanto texto tiene que juntar el cierre de capitulo, en caracteres. Mil
# seiscientos son unas veinte lineas a dos columnas: media pagina, que es lo
# que una pagina de cierre necesita para no parecer un error.
CIERRE_MINIMO = 1600


def cerrar_capitulo(piezas_de_seccion):
    """La nota de cierre viaja con el ultimo parrafo del capitulo.

    Un capitulo termina con su nota de lectura. Si la pagina anterior quedo
    llena, la nota —treinta milimetros— se va sola a una pagina nueva y la
    ultima pagina del capitulo queda al 7%: dieciocho milimetros de texto y el
    resto papel. Eso no se lee como un cierre, se lee como un error de armado.

    Se juntan la nota, el separador y el ultimo bloque de prosa en una sola
    pieza indivisible. Cuando no entra al pie, se van los tres juntos y la
    ultima pagina recibe un bloque que se sostiene solo. La pagina anterior
    pierde ese bloque, si; pero dos paginas a media altura se leen mucho mejor
    que una llena y una vacia.

    Si el bloque resultante fuera mas alto que una pagina, WeasyPrint lo parte
    igual y no pasa nada: el break-inside es una preferencia, no una promesa.
    """
    if len(piezas_de_seccion) < 2:
        return piezas_de_seccion
    if "nota-envoltorio" not in piezas_de_seccion[-1]["html"]:
        return piezas_de_seccion
    # Hacia atras, juntando prosa y separadores hasta que el bloque tenga con
    # que sostener una pagina. Con una sola banda no alcanzaba: el capitulo 2
    # cierra con un parrafo de dos lineas y la pagina seguia al 15%.
    #
    # SE FRENA EN LO PRIMERO QUE NO SEA PROSA. Tragarse un exhibit haria un
    # bloque indivisible de media pagina, que es el problema del otro lado.
    corte = len(piezas_de_seccion) - 1
    texto = len(_texto_plano(piezas_de_seccion[-1]["html"]))
    while corte > 0:
        previa = piezas_de_seccion[corte - 1]
        # Prosa es todo menos una figura y menos un titulo: un remate o una
        # cifra destacada son quince milimetros y viajan sin problema. Una
        # figura haria un bloque indivisible de media pagina —el problema del
        # otro lado— y un titulo tiene que poder abrir pagina.
        es_prosa = previa["tipo"] not in ("figura", "titulo")
        if not es_prosa or texto >= CIERRE_MINIMO:
            break
        texto += len(_texto_plano(previa["html"]))
        corte -= 1
    if corte == len(piezas_de_seccion) - 1:
        return piezas_de_seccion
    cola = piezas_de_seccion[corte:]
    junta = {"id": cola[0]["id"], "tipo": "ancho",
             "html": '<div class="cierre">%s</div>'
                     % "".join(x["html"] for x in cola)}
    return piezas_de_seccion[:corte] + [junta]


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

HUECO_MINIMO = 22.0     # mm: menos que esto no es un hueco, es el aire del pie
PASADAS_MAXIMAS = 8     # cada pasada rearma el PDF entero; ocho alcanzan
SALTOS_MAXIMOS = 2      # cuantas veces se puede bajar una misma figura


def _huecos(doc, fin_px):
    """Por pagina: el hueco al pie en mm, y la pieza que la abre.

    Las paginas sin ninguna pieza —la tapa y el indice— quedan en (None, None):
    no tienen hueco que medir porque no las arma el flujo del cuerpo.
    """
    fuera = []
    for pag in doc.pages:
        if not pag.anchors:
            fuera.append((None, None))
            continue
        fondo = min(max(caja[3] for caja in pag.anchors.values()), fin_px)
        # Los h1 y los h2 tambien dejan ancla —las usa el indice para su numero
        # de pagina— y no son piezas. Si se las toma por piezas, el acomodador
        # cree que la pagina la abre un titulo, no encuentra esa clave entre las
        # piezas y se saltea la pagina. Por eso la pieza que abre se busca solo
        # entre las anclas con el prefijo de pieza.
        propias = {k: v for k, v in pag.anchors.items()
                   if k.startswith(PREFIJO_PIEZA)}
        abre = (min(propias.items(), key=lambda kv: (kv[1][1], kv[1][0]))[0]
                if propias else None)
        fuera.append(((fin_px - fondo) / PX_POR_MM, abre))
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
        fin_px = doc.pages[0].height - MARGEN_PIE * PX_POR_MM
        huecos = _huecos(doc, fin_px)
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
    """La imagen de tapa, con el titulo encima.

    Si todavia no llego la imagen generada, la tapa la hace el mapa de zonas,
    que es lo que habia. Las dos ocupan la pagina entera; el titulo va arriba a
    la izquierda, sobre el aire.

    Sin nombre ni foto del candidato. Decision cerrada en la identidad.
    """
    ilustracion = imagen("tapa.png")
    if ilustracion:
        fondo = ('<img class="tapa-img cubre" src="file://%s" alt=""/>'
                 '<p class="tapa-credito">%s</p>' % (ilustracion,
                                                     PIE_ILUSTRACION))
    else:
        fondo = ('<img class="tapa-img" src="file://%s" alt=""/>'
                 % os.path.join(CHARTS, "TAPA_mapa_zonas.png"))
    return ('<section class="tapa">%s'
            '<div class="tapa-faja"></div>'
            '<div class="tapa-txt">'
            '<h1 class="t1">%s</h1><h1 class="t2">%s</h1>'
            '<p class="sub">%s</p></div>'
            '</section>' % (fondo, TITULO, ANIO, SUBTITULO))


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

# Los seis @font-face de Spectral se escriben solos desde CORTES_SERIF: son
# archivos estaticos y cada uno declara su peso y su estilo.
_FACES = "\n".join(
    '@font-face { font-family: "%s"; src: url("file://%s/%s");\n'
    '             font-weight: %d; font-style: %s; }' % (SERIF, TIPOS, f, w, e)
    for f, w, e in CORTES_SERIF)

CSS = _FACES + """
@font-face { font-family: "%(sans)s";
             src: url("file://%(tipos)s/Inter[opsz,wght].ttf");
             font-weight: 100 900; font-style: normal; }
@font-face { font-family: "%(sans)s";
             src: url("file://%(tipos)s/Inter-Italic[opsz,wght].ttf");
             font-weight: 100 900; font-style: italic; }

/* ====================================================================
   LA GEOMETRIA SALE DE 04_diseno/MEDIDAS_EXTRATIME.md

   La referencia mide 660 pt de ancho con margenes de 45 pt: la caja de
   texto se lleva el 86,4 %% del ancho y cada margen el 6,8 %%. Trasladado a
   A4 eso da margenes de 14,3 mm; se usan 16, porque esto es papel y no
   pantalla, y una hoja que se imprime necesita donde agarrarla. Caja de
   texto: 178 mm.

   El medianil de la referencia mide 24 pt sobre 570 de caja, o sea el
   4,2 %%. Sobre 178 mm da 7,5 mm, y las columnas quedan de 85,25 mm.

   NO SE COPIA EL ALTO. El original es una exportacion continua de Figma:
   sus paginas miden entre 872 y 2685 pt porque cada capitulo es un lienzo,
   no una hoja. Nosotros paginamos A4 de verdad.
   ==================================================================== */
@page {
  size: A4; margin: 15mm 16mm %(pie)dmm 16mm; background: %(crema)s;
  /* LA CORNISA. Inter en mayusculas espaciadas, como la referencia: dice en
     que seccion esta parado el lector antes de que empiece a leer. */
  @top-left     { content: string(cap); font-family: "%(sans)s";
                  font-size: 6.7pt; font-weight: 500; letter-spacing: 1pt;
                  color: %(acento)s; text-transform: uppercase;
                  margin-bottom: 5.5mm; }
  @bottom-left  { content: "%(corto)s"; font-family: "%(sans)s";
                  font-size: 6.4pt; letter-spacing: .15pt; white-space: pre;
                  color: %(tinta)s; opacity: .65; vertical-align: top; }
  @bottom-right { content: "Página " counter(page) " de " counter(pages);
                  font-family: "%(sans)s"; font-size: 6.4pt;
                  font-variant-numeric: tabular-nums lining-nums;
                  white-space: pre; color: %(tinta)s; opacity: .65;
                  vertical-align: top; }
  /* Todos los filetes de la referencia miden 0,75 pt: 567 de los 570
     rectangulos finos medidos dan exactamente ese grosor. No hay filetes
     gruesos en ninguna parte del documento, y los que habia aca —1,6 pt
     bajo el titulo de capitulo, 3,5 pt al costado de una cifra— eran
     nuestros, no suyos. */
  border-bottom: .75pt solid %(arena)s; padding-bottom: 3.5mm;
}
@page :first { margin: 0; border: 0; padding: 0;
  @top-left { content: ""; } @bottom-left { content: ""; }
  @bottom-right { content: ""; } }

html { background: %(crema)s; }
/* Cuerpo 9,7 pt con interlinea de 14,5 —los dos medidos— dan 54 caracteres
   por columna de 85 mm. La referencia tiene 60 en una columna de 95. Es la
   misma medida de lectura. Lo anterior era 8,7 sobre 1,42, que es cuerpo de
   nota al pie usado como cuerpo de texto. */
body { font-family: "%(serif)s", Georgia, serif; font-size: 9.7pt;
       line-height: 1.49; color: %(tinta)s;
       font-variant-numeric: lining-nums; }

/* --------------------------------------------------------------------
   BANDAS. La prosa a dos columnas balanceadas; todo lo demas al ancho.
   -------------------------------------------------------------------- */
.banda { columns: 2; column-gap: 7.5mm; }
.banda > *:first-child { margin-top: 0; }
.con-titulo { break-inside: avoid; }
.con-titulo .banda { margin-top: 0; }

p { margin: 0 0 .5em; text-align: justify; hyphens: auto; }
p, li { orphans: 3; widows: 3; }
/* EL COLOR ENTRA POR LA PROSA. En la referencia las negritas del cuerpo no
   son negras: las cifras y los nombres propios van en ladrillo y los
   conceptos en salvia. Es de donde sale el color de las paginas que no
   tienen ni tabla ni grafico —que aca eran veinte, y salian en gris—.
   El texto no se toca: las negritas YA ESTAN ESCRITAS en el markdown, lo
   unico que cambia es de que color se imprimen. */
strong { font-weight: 600; color: %(acento)s; }
em { font-style: italic; }
code { font-family: "DejaVu Sans Mono"; font-size: 8pt; background: %(arena)s;
       padding: .5pt 2pt; }
/* El listado: monoespaciada al ancho de la caja, sobre banda de arena y con
   filete del acento al costado, que es lo que hace la referencia con sus
   piezas de dato en bruto. */
pre.listado { font-family: "DejaVu Sans Mono"; font-size: 7.2pt;
              line-height: 1.42; margin: 7.8mm 0; padding: 3.5mm 4mm;
              background: %(arena)s; border-left: .75pt solid %(acento)s;
              color: %(tinta)s; white-space: pre; overflow: hidden;
              break-inside: avoid; }
a { color: %(acento)s; text-decoration: none; }
hr { border: 0; border-top: .75pt solid %(arena)s; margin: 7.8mm 0 6.5mm; }

/* --------------------------------------------------------------------
   JERARQUIA — los cuerpos son los medidos, uno por uno
   -------------------------------------------------------------------- */
/* Titulo de capitulo, Spectral Bold 16,5. EL NUMERO EN LADRILLO Y EL NOMBRE
   EN TINTA, que es lo que hace la referencia. Lo que se veia como un error
   era el NOMBRE partido en dos colores; el numero aparte es jerarquia. */
h1 { font-size: 16.5pt; line-height: 1.18; margin: 0 0 8.8mm;
     font-weight: 700; letter-spacing: 0; color: %(tinta)s;
     string-set: cap content(); break-before: page; break-after: avoid; }
h1 .cn { color: %(acento)s; margin-right: .28em; }

/* La bajada del capitulo: Spectral MediumItalic 10,9 en salvia. */
p.bajada { font-style: italic; font-weight: 500; font-size: 10.9pt;
           line-height: 1.38; color: %(dato)s; margin: -6mm 0 8.8mm;
           max-width: 152mm; text-align: left; hyphens: none;
           break-after: avoid; }
p.bajada strong { color: %(dato)s; font-weight: 600; }

/* La entrada: el primer parrafo del capitulo va a TODO EL ANCHO y un punto
   mas grande que el cuerpo, como en la referencia. Despues empiezan las
   columnas. */
p.entrada { font-size: 10pt; line-height: 1.6; text-align: left;
            margin: 0 0 7.8mm; hyphens: none; }

h2 { font-size: 12.2pt; line-height: 1.25; margin: 7.8mm 0 3.4mm;
     font-weight: 600; color: %(tinta)s; break-after: avoid;
     break-inside: avoid; text-indent: -0.05em; }
h2 .n { font-weight: 700; color: %(acento)s;
        font-variant-numeric: lining-nums; margin-right: .32em; }
h1 + p.bajada + .banda h2:first-child,
h1 + p.bajada + .con-titulo > h2 { margin-top: 0; }

h3 { font-size: 9.7pt; font-weight: 600; margin: 6.5mm 0 2.6mm;
     color: %(acento)s; break-after: avoid; break-inside: avoid; }
h3::before { content: ""; display: block; width: 9mm;
             border-top: .75pt solid %(acento)s; margin-bottom: 1.8mm; }

/* --------------------------------------------------------------------
   CIFRAS DESTACADAS Y REMATES
   -------------------------------------------------------------------- */
p.dato { font-size: 14pt; line-height: 1.3; color: %(acento)s;
         font-weight: 500;
         margin: 7.8mm 0; padding: 0 0 0 5mm; text-align: left;
         border-left: .75pt solid %(acento)s;
         hyphens: none; break-inside: avoid; max-width: 158mm; }
p.dato strong { color: %(acento)s; font-weight: 600; }

p.remate { font-size: 10.9pt; line-height: 1.38; color: %(tinta)s;
           font-style: italic; font-weight: 500;
           margin: 7.8mm 0; padding: 0 0 0 5mm;
           border-left: .75pt solid %(acento)s; text-align: left;
           hyphens: none; break-inside: avoid; max-width: 158mm; }
p.remate strong { font-style: normal; font-weight: 600; color: %(acento)s; }

/* --------------------------------------------------------------------
   CAJAS. Fondo arena, filete de 0,75 al costado, cintillo en Inter.
   -------------------------------------------------------------------- */
.caja { break-inside: avoid; margin: 7.8mm 0; padding: 4mm 5mm;
        background: %(arena)s; font-size: 9pt; line-height: 1.45; }
.caja h5 { font-family: "%(sans)s"; font-size: 6.4pt; font-weight: 600;
           letter-spacing: .75pt; text-transform: uppercase;
           margin: 0 0 2.4mm; color: %(acento)s; line-height: 1.3; }
.caja p { margin: 0 0 .45em; text-align: left; hyphens: none; }
.caja p:last-child { margin-bottom: 0; }
/* Las tres cajas comparten fondo arena y filete: son la misma pieza del
   sistema y distinguirlas por color inventaba una jerarquia que el texto no
   tiene. Lo que las separa es su titulo. */
.caja.metodo, .caja.hipotesis, .caja.legal {
    border-left: .75pt solid %(dato)s; }
.caja.legal { font-style: italic; }

/* Nota de lectura al pie de seccion. En la referencia es Spectral italico
   7,9 en gris calido, con la entrada en SemiBold, a todo el ancho. */
.nota-lectura { margin: 7.8mm 0 0;
                border-top: .75pt solid %(arena)s; padding-top: 3mm;
                font-size: 7.9pt; line-height: 1.46; color: %(tinta)s;
                font-style: italic; opacity: .68;
                columns: 2; column-gap: 7.5mm; }
.nota-envoltorio { break-inside: avoid; }
.cierre { break-inside: avoid; }
.nota-lectura p { margin: 0 0 .4em; text-align: left; hyphens: none; }
.nota-lectura strong { color: inherit; }
.nota-lectura .et { font-weight: 600; opacity: 1; }

/* La entrada en SemiBold de una fuente o de una nota: Spectral, no
   versalitas. La referencia no usa versalitas en ninguna parte —lo que
   parecian versalitas es Inter en mayusculas espaciadas—. */
.et { font-weight: 600; font-style: normal; color: inherit; }

ul, ol { margin: 0 0 .6em; padding: 0 0 0 4.8mm; }
li { margin-bottom: .3em; text-align: justify; hyphens: auto; }
ul li::marker { color: %(acento)s; }
ol li::marker { color: %(acento)s; font-weight: 600; }

/* --------------------------------------------------------------------
   TABLAS. Banda de cabecera en arena con Inter mayuscula en ladrillo,
   primera columna en ladrillo, filas alternadas en #E8E4D9.
   Medido: banda de cabecera 17,3 pt, fila 20,2 pt, sangria de celda 6 pt.
   -------------------------------------------------------------------- */
.tw { break-inside: avoid; margin: 7.8mm 0; }
table { width: 100%%; border-collapse: collapse;
        font-family: "%(sans)s"; font-size: 7.9pt; line-height: 1.4;
        font-variant-numeric: tabular-nums lining-nums; }
.tw:not(.ancho) table { font-size: 7.4pt; }
thead th { background: %(arena)s; color: %(acento)s; text-align: left;
           padding: 1.6mm 2.1mm; font-size: 6.4pt; font-weight: 600;
           letter-spacing: .5pt; text-transform: uppercase; line-height: 1.25;
           vertical-align: bottom; }
td { padding: 1.7mm 2.1mm; vertical-align: top; }
tbody tr:nth-child(even) { background: %(fila)s; }
tbody td:first-child { color: %(acento)s; font-weight: 600; }
/* La columna que el texto marca como la nuestra va en salvia, que es lo que
   hace la referencia con su columna "EXTRA TIME". */
tbody td.destacada { color: %(dato)s; font-weight: 600; }
thead th.destacada { color: %(dato)s; }
th:not(:first-child), td:not(:first-child) { text-align: right; }
th:first-child, td:first-child { text-align: left; }
/* Una tabla de texto no se alinea a la derecha: ahi la columna no es una
   cifra, es una oracion. */
.tw.texto th, .tw.texto td { text-align: left; }
.etq { font-style: italic; font-size: 7.9pt; font-family: "%(serif)s";
       line-height: 1.46; margin: 2.4mm 0 0; color: %(tinta)s; opacity: .68;
       text-align: left; hyphens: none; }
.etq .et { opacity: 1; }

/* --------------------------------------------------------------------
   EXHIBITS. Rotulo en Inter mayuscula, titulo que dice la conclusion,
   bajada, figura, y fuente al pie en Spectral italico.
   Ritmo medido: rotulo -> titulo 14 pt; titulo -> figura 21 pt;
   figura -> fuente 25 pt.
   -------------------------------------------------------------------- */
.exh { break-inside: avoid; margin: 7.8mm 0; }
.exh-cab { margin-bottom: 7.4mm; break-after: avoid; }
.exh-rot { font-family: "%(sans)s"; font-size: 6.7pt; font-weight: 500;
           letter-spacing: .75pt; text-transform: uppercase;
           color: %(acento)s; margin: 0 0 4.9mm; text-align: left; }
.exh-tit { font-size: 11.2pt; font-weight: 600; line-height: 1.3;
           color: %(acento)s; margin: 0; text-align: left; hyphens: none; }
.exh-baj { font-size: 7.9pt; line-height: 1.46; font-style: italic;
           color: %(tinta)s; opacity: .68; margin: 2.4mm 0 0;
           text-align: left; hyphens: none; max-width: 168mm; }
.exh img { display: block; margin: 0 auto; max-width: 100%%;
           max-height: 92mm; width: auto; height: auto; }
.exh.alto img { max-height: 108mm; }
.exh-fuente, .exh-nota { font-style: italic; font-size: 7.9pt;
                         line-height: 1.46; margin: 8.8mm 0 0;
                         text-align: left; hyphens: none;
                         color: %(tinta)s; opacity: .68; }
.exh-nota { color: %(acento)s; opacity: .9; margin-top: 3mm; }

/* --------------------------------------------------------------------
   TAPA
   -------------------------------------------------------------------- */
.tapa { position: relative; width: 210mm; height: 297mm; overflow: hidden;
        page-break-after: always; background: %(crema)s; }
/* EL MAPA LLENA LA PAGINA. Antes entraba como una estampita al pie, con dos
   tercios de papel arriba: la tapa de un programa de gobierno de un partido
   tiene que ser el partido. */
.tapa-img { position: absolute; left: 0; top: 0; width: 210mm; height: 297mm;
            object-fit: cover; }
.tapa-img.cubre { left: 0; top: 0; width: 210mm; height: 297mm;
                  object-fit: cover; }
/* La franja que sostiene el titulo: crema con un poco de transparencia, para
   que el titulo se lea sin tapar el mapa. */
.tapa-faja { position: absolute; left: 0; top: 0; width: 210mm;
             height: 118mm;
             background: linear-gradient(180deg,
                 rgba(245,240,232,.97) 0%%, rgba(245,240,232,.95) 62%%,
                 rgba(245,240,232,0) 100%%); }
.tapa-credito { position: absolute; left: 16mm; bottom: 8mm; margin: 0;
                font-family: "%(sans)s"; font-size: 6.4pt; letter-spacing: .3pt;
                color: %(tinta)s; opacity: .65; }

/* --------------------------------------------------------------------
   LA BANDA QUE ABRE CADA CAPITULO
   -------------------------------------------------------------------- */
figure.apertura { margin: 0 0 6mm; break-after: avoid; break-inside: avoid; }
figure.apertura img { display: block; width: 100%%; height: 44mm;
                      object-fit: cover; }
figure.apertura figcaption { font-family: "%(sans)s"; font-size: 6.4pt;
                             letter-spacing: .2pt; color: %(tinta)s;
                             opacity: .55; margin-top: 1.6mm;
                             text-align: right; }
figure.apertura + h1 { break-before: avoid; }
.tapa-txt { position: absolute; left: 16mm; top: 22mm; width: 178mm; }
.tapa h1 { font-size: 40pt; line-height: 1.06; margin: 0; letter-spacing: -.4pt;
           border: 0; padding: 0; break-before: avoid; font-weight: 700;
           color: %(tinta)s; }
.tapa .t2 { color: %(acento)s; margin-bottom: 7mm; }
.tapa .sub { font-size: 10.9pt; line-height: 1.45; text-align: left;
             max-width: 128mm; margin: 0; hyphens: none; font-style: italic;
             font-weight: 500; color: %(dato)s;
             border-top: .75pt solid %(acento)s; padding-top: 4mm;
             display: inline-block; }
/* --------------------------------------------------------------------
   INDICE
   -------------------------------------------------------------------- */
.indice { break-before: page; }
h1.ix-h { font-size: 16.5pt; margin-bottom: 6mm; }
ul.ix { list-style: none; margin: 0; padding: 0;
        font-variant-numeric: tabular-nums lining-nums; }
ul.ix li { margin: 0; }
ul.ix a { color: %(tinta)s; display: block; text-decoration: none;
          padding-bottom: 1.2mm; }
ul.ix a::after { content: target-counter(attr(href), page); float: right;
                 font-size: 8.6pt; color: %(tinta)s; opacity: .6;
                 padding-left: 3mm; }
li.ix-cap { margin-top: 4mm; }
li.ix-cap:first-child { margin-top: 0; }
li.ix-cap a { font-size: 11.2pt; font-weight: 600; color: %(acento)s;
              border-bottom: .75pt solid %(acento)s; padding-bottom: 1.8mm; }
li.ix-cap a::after { color: %(acento)s; opacity: 1; font-weight: 600;
                     font-size: 8.6pt; }
li.ix-sub a { font-size: 8.6pt; padding: 1mm 0;
              border-bottom: .75pt dotted rgba(124, 46, 35, .22); }
span.ix-n { display: inline-block; width: 11mm; color: %(acento)s;
            font-weight: 600; }
""" % dict(crema=CREMA, tinta=TINTA, acento=ACENTO, dato=DATO, arena=ARENA,
           fila=FILA, corto=TITULO_CORTO, pie=MARGEN_PIE, serif=SERIF,
           sans=SANS, tipos=TIPOS)


# ==========================================================================
# 6. VERIFICACION DEL PDF YA ARMADO
# ==========================================================================

# --------------------------------------------------------------------------
# DECIMO VERIFICADOR: DENSIDAD DE COLOR, PAGINA POR PAGINA
# --------------------------------------------------------------------------
# Se muestrea el PDF ya armado y se cuenta, en cada pagina, que proporcion de
# pixeles cae en un color de la paleta y que proporcion es papel. Una pagina
# que es solo tipografia negra sobre crema es una pagina que el lector saltea,
# y en la version anterior habia veinte seguidas asi.
#
# LOS UMBRALES SALEN DE LA REFERENCIA, MEDIDA. Sobre las treinta paginas del
# Extra Time (04_diseno/MEDIDAS_EXTRATIME.md, seccion 8) el color ocupa 4,00 %
# de media, con un minimo de 0,68 % y un maximo de 13,91 %; el papel ocupa
# 80,9 % de media, con un maximo de 96,8 %. Los umbrales que se habian
# propuesto —color por encima de 0,8 % y papel por debajo de 89 %— son mas
# exigentes que la propia referencia y voltearian cuatro de sus treinta
# paginas. Se toma el piso real de la referencia, 0,65 %, y su techo real,
# 96 %, redondeados hacia el lado que perdona.
#
# La tapa y el indice quedan fuera: la tapa es una imagen a sangre y el indice
# es una lista, y ninguna de las dos es una pagina de lectura.
COLOR_MINIMO = 0.65      # % de pixeles de la pagina en un color de la paleta
PAPEL_MAXIMO = 96.0      # % de pixeles de la pagina en crema


def _paginas_a_pixeles(ruta, dpi=48):
    """Cada pagina del PDF como un array de RGB. Usa pdftoppm, que ya esta."""
    import glob
    import shutil
    import tempfile
    import numpy as np
    from PIL import Image
    tmp = tempfile.mkdtemp(prefix="densidad-")
    try:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", ruta,
                        os.path.join(tmp, "p")], check=True,
                       capture_output=True)
        for f in sorted(glob.glob(os.path.join(tmp, "p-*.png"))):
            with Image.open(f) as im:
                yield np.asarray(im.convert("RGB")).astype(int)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def verificar_densidad(ruta, desde=3):
    """Denuncia cada pagina sin color o ahogada en papel. desde: 1-indexado."""
    import numpy as np
    fallas = []
    paleta = [_hex_a_rgb(c) for c in (ACENTO, DATO, DATO_CLARO, ARENA, FILA)]
    crema = np.array(_hex_a_rgb(CREMA))
    for i, a in enumerate(_paginas_a_pixeles(ruta), start=1):
        if i < desde:
            continue
        n = a.shape[0] * a.shape[1]
        color = sum(int((np.abs(a - np.array(c)).sum(axis=2) < 60).sum())
                    for c in paleta)
        papel = int((np.abs(a - crema).sum(axis=2) < 20).sum())
        pc, pp = 100.0 * color / n, 100.0 * papel / n
        if pc < COLOR_MINIMO:
            fallas.append("página %d: %.2f%% de color, hace falta %.2f%%"
                          % (i, pc, COLOR_MINIMO))
        elif pp > PAPEL_MAXIMO:
            fallas.append("página %d: %.1f%% de papel, el techo es %.1f%%"
                          % (i, pp, PAPEL_MAXIMO))
    return fallas


def _hex_a_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


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

    NUMEROS.update(numeros_por_aparicion())
    entradas, piezas = [], []
    for nombre, titulo in ORDEN:
        slug = nombre.split(".")[0].lower()
        lista, subs = bloques(leer_publicable(nombre), slug)
        entradas.append((slug, titulo, subs))
        piezas.append(cerrar_capitulo(bandas(lista, slug)))

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
    apagadas = verificar_densidad(SALIDA)
    problemas += apagadas
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
