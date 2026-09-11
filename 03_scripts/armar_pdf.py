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
import shutil
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
# LAS ILUSTRACIONES
# --------------------------------------------------------------------------
# Once ilustraciones, cada una en el lugar donde el texto habla de eso. NO se
# generan aca: llegan como archivos a 09_imagenes/ y el armador solo las
# coloca. Si falta alguna el documento se arma igual, sin ella.
#
# CADA UNA LLEVA SU PIE. Ninguna representa a una persona identificable ni
# documenta un hecho concreto, y el documento tiene que decirlo: si alguien
# descubriera que una imagen se ofrece como fotografia de un lugar o de un
# vecino de San Isidro, el documento pierde lo unico que tiene, que es que se
# le pueden revisar las cuentas.
IMAGENES = os.path.join(RAIZ, "09_imagenes")
PIE_ILUSTRACION = "Ilustración."

# La tapa, a sangre, con el titulo encima.
TAPA_ILUSTRACION = "01_costanera_juncos_a"

# La banda que abre cada capitulo, al ancho de la caja y arriba del titulo.
APERTURAS = {
    "cap1_diagnostico": "02_catedral_a",
    "cap3_la_plata": "07_barranca_escalinata_a",
    "cap4_mecanismo": "11_asamblea_vecinal_a",
    "cap5_sectorial": "08_puerto_nautica_a",
}

# Las de adentro, al final de la subseccion que nombra la clave. Una lista de
# dos imagenes se compone como un PAR ENFRENTADO, mitad y mitad.
#
# El par de la 1.1 es el argumento del capitulo en dos fotos: Boulogne con sus
# cables y su poda a muñon contra Martinez con la copa cerrada. Por eso van
# juntas y no una en cada pagina.
DENTRO = {
    "cap1_diagnostico": {
        # La variante _a de Martinez estaba mal: las casas pegadas una a otra,
        # la calle demasiado angosta y el asfalto sin textura. Se leia
        # inventada, y una imagen que se lee inventada en un documento que se
        # ofrece para que le revisen las cuentas cuesta mas de lo que aporta.
        # La _b tiene el ancho de calzada real, la vereda con su baldosa, las
        # casas retiradas detras de su reja y la copa cerrada de verdad.
        "1.1": (["04_boulogne_obra_b", "05_martinez_calle_b"],
                "Boulogne Sur Mer y Martínez. La misma distancia al río, "
                "la misma tasa municipal."),
        "1.5": (["06_villa_adelina_comercial_b"], None),
        "1.6": (["03_plaza_mitre_b"], None),
        "*": (["12_barranca_desde_arriba"], None),
    },
    # La clave "*" no es una subseccion: es el FINAL del capitulo. Ahi va la
    # imagen que cierra, en las paginas que terminaban a media altura.
    "00_introduccion": {
        "*": (["01b_costanera_paseo_a"], None),
    },
    "cap2_gestion_medida": {
        "2.5": (["13_vecinos_parada"], None),
    },
    "cap4_mecanismo": {
        "*": (["14_comision_plano"], None),
    },
    "cap6_cierre": {
        "*": (["16_calle_amanecer"], None),
    },
    "cap5_sectorial": {
        "5.3": (["10_taller_formacion_a"], None),
        "5.9": (["15_expedientes"], None),
        # La variante _b es un recorte de techos: la caja de 181 x 76 corta
        # por el medio de una foto vertical y en la _b ese medio es el
        # tejado. La _a tiene la estacion entera, el anden y la gente.
        "5.6": (["09_tren_costa_a"], None),
    },
}


def imagen(nombre):
    """La ruta de una ilustracion, o None si todavia no llego."""
    for ext in (".jpg", ".png"):
        ruta = os.path.join(IMAGENES, nombre + ext)
        if os.path.exists(ruta):
            return ruta
    return None


def _figura_ilustracion(nombres, pie, clase=""):
    """Una ilustracion, o dos enfrentadas, con su pie."""
    rutas = [imagen(n) for n in nombres]
    if any(r is None for r in rutas):
        return None
    imgs = "".join('<img src="file://%s" alt=""/>' % r for r in rutas)
    if len(rutas) > 1:
        imgs = '<div class="par">%s</div>' % imgs
    texto = ("%s %s" % (html.escape(pie), PIE_ILUSTRACION) if pie
             else PIE_ILUSTRACION)
    return ('<figure class="ilu %s">%s<figcaption>%s</figcaption></figure>'
            % (clase, imgs, texto))


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
DATO = "#5F7057"         # verde salvia: la serie principal
DATO_CLARO = "#7E9070"   # salvia clara: la cuarta serie
ARENA = "#EAE0CF"        # bandas de encabezado y cajas laterales
FILA = "#E8E4D9"         # filas alternadas
TAN = "#EFE7DA"          # el fondo de la caja al margen
# EL OCRE. Sexta voz de la paleta, sumada despues de medir la referencia
# entera: lleva TODAS sus cornisas, sus rotulos de exhibit y sus
# micro-etiquetas —1.833 glifos, la sexta familia de color mas usada del
# documento— y no es un rojo, es un oro apagado. Sin el, esa voz habia que
# hacerla con ladrillo o con salvia, que ya estan ocupados en otra cosa, y por
# eso nuestros rotulos se confundian con nuestros titulos.
OCRE = "#B4863A"         # rotulos, cintillos, micro-etiquetas
# EL CORAL. Septima voz, y la unica que hace un solo trabajo: LA CIFRA QUE
# NUMERA. En la referencia lleva los 26 numeros de seccion del titulo, los 26
# del indice y nada mas del cuerpo. Es un rojo anaranjado y por eso habia
# quedado afuera; entra por decision tomada, con el mismo criterio que el
# ladrillo: lo que verificar_pdf() prohibe es el rojo PURO.
CORAL = "#DB6B4B"        # la cifra que numera: titulo de seccion e indice
# EL GRIS CALIDO. Octava voz, y la que mas falta hacia: en la referencia
# lleva EL 18,9 % DE TODOS LOS GLIFOS —uno de cada cinco— y nosotros no la
# usabamos en ninguna parte. Sola, en Spectral cursiva de 7,9, lleva 13.912
# glifos: todo el aparato del documento —las fuentes, las notas, las bajadas
# de exhibit, los limites de cada dato—. Nosotros poniamos ese aparato en
# ladrillo y en tinta aguada, y por eso nuestro ladrillo estaba al doble que
# el suyo (19,4 % contra 9,0 %): usado para todo, no significaba nada.
# La tinta al 68 % no es lo mismo: da un gris frio y sin cuerpo.
GRIS = "#6E625A"         # el aparato: fuentes, notas, limites, remisiones

TITULO = "PROGRAMA DE GOBIERNO"
ANIO = "SAN ISIDRO 2027"
SUBTITULO = ("Con los recursos que el Municipio ya tiene,<br>"
             "y con decisión vecinal sobre la inversión pública.")
TITULO_CORTO = "Programa de gobierno · San Isidro 2027"
# El capitulo que el indice levanta del resto, como ellos levantan THE MODEL.
GRUPO_PROPUESTA = "El mecanismo"

# EL ANEXO DE FUENTES NO SE PUBLICA. El archivo sigue en 07_capitulos/ —es el
# registro de como se hizo el documento y ahi tiene que estar— pero no entra al
# PDF: un programa de gobierno no lleva adentro la linea de comandos con la que
# se arma. Ese material es el README del repositorio, que es donde cualquiera
# que quiera correr los numeros va a buscarlo.
ORDEN = [
    ("00_INTRODUCCION.md", "Introducción"),
    ("CAP1_DIAGNOSTICO.md", "1 Diagnóstico"),
    ("CAP2_GESTION_MEDIDA.md", "2 La gestión, medida"),
    ("CAP3_LA_PLATA.md", "3 La plata"),
    ("CAP4_MECANISMO.md", "4 El mecanismo"),
    ("CAP5_SECTORIAL.md", "5 Qué hacemos en cada área"),
    ("CAP6_CIERRE.md", "6 Contra qué queremos que nos midan"),
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
# EL ROTULO DE LA CAJA. Catorce de las veintiseis cajas de la referencia lo
# llevan: Inter mayuscula espaciada en salvia, sobre el texto, adentro de la
# caja. Es lo que convierte una cita en una pieza: dice de que es la caja
# antes de que se lea una palabra. Nosotros no teniamos ninguno.
# Cada rotulo es el nucleo de SU PROPIA frase puesto en mayuscula —no se
# inventa nada y no se agrega una idea que el remate no diga ya—.
ROTULOS_REMATE = json.load(
    open(os.path.join(AQUI, "rotulos_remate.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(AQUI, "rotulos_remate.json")) else {}
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
# El titulo de una seccion, en el formato de la referencia: el numero solo y
# el nombre en minuscula —"3 Why the category's economics break"—. El anexo
# lleva letra, como el suyo: "A Methodology, sources & verification".
RE_H1CAP = re.compile(r'^(\d+|[A-Z])\s+(.+)$')


# LAS NEGRITAS DE LA PROSA VAN EN DOS COLORES, COMO EN LA REFERENCIA.
# En sus paginas el color no entra solo por las tablas y los graficos: entra
# por el texto. Las CIFRAS y los importes van en ladrillo —"$0.83-1.9M",
# "$15-40K a month"— y los CONCEPTOS en salvia —"memberships cover the fixed
# costs", "First, curated third-party"—. Dos acentos corriendo por el cuerpo,
# no uno.
#
# El reparto se hace solo, y por una regla que no opina: si el tramo en
# negrita tiene un digito, es una cifra y va en ladrillo; si no lo tiene, es
# un concepto y va en salvia. Sobre los 464 tramos que ya estan escritos en el
# markdown da 183 cifras y 281 conceptos. EL TEXTO NO SE TOCA: las negritas ya
# estaban puestas por quien escribio, lo unico que decide esto es de que color
# se imprimen.
RE_CIFRA = re.compile(r'\d')

# CUANTO TEXTO HACE FALTA PARA CRUZAR LAS DOS COLUMNAS.
# Un parrafo a todo el ancho es una ENTRADA de lectura: el lector arranca la
# seccion con una linea larga y recien despues se mete en la columna. Pero eso
# solo funciona si hay texto para llenarla. Una sola linea cruzando los 181 mm,
# con la columna de al lado vacia debajo, no se lee como una entrada: se lee
# como un error de armado.
#
# LA REGLA: minimo CUATRO LINEAS. A cuerpo 8,75 en una caja de 181,4 mm entran
# 130 caracteres por linea, asi que hacen falta 520. Un parrafo mas corto que
# eso se queda en la columna, donde 520 caracteres son ocho lineas y llenan.
#
# Si el primer parrafo no llega solo, se le suman los que siguen —hasta tres—
# y se decide sobre el total: la entrada de la referencia es una REGION de
# lectura, no necesariamente un parrafo. Si ni asi llega, no hay entrada y la
# seccion arranca directamente a dos columnas.
#
# Medido sobre nuestro texto: los parrafos de apertura tienen una mediana de
# 131 caracteres —una linea— y solo cuatro secciones de cuarenta y seis llegan
# a las cuatro lineas. O sea que la entrada ancha aparece poco, y esta bien que
# asi sea: la referencia tambien la usaria poco si sus parrafos midieran esto.
CARACTERES_POR_LINEA_ANCHA = 130
CARACTERES_POR_LINEA_COLUMNA = 62
# UNA CORRIDA CORTA NO VA A DOS COLUMNAS.
# `orphans: 4` y `widows: 4` impiden partir un parrafo si a algun lado le
# quedan menos de cuatro lineas. Un parrafo de siete —el largo normal de un
# parrafo nuestro— no se puede partir 4+3, asi que WeasyPrint lo deja ENTERO
# en la columna izquierda y la derecha queda vacia de arriba abajo. Ese es el
# escalon en blanco que aparecia en media docena de paginas.
# A todo el ancho no hay nada que partir y el problema no existe. Ademas es lo
# que hace la referencia: sus dos primeras paginas de texto son enteras a una
# sola columna, y las dos columnas aparecen recien cuando hay con que llenarlas.
CORRIDA_MINIMA_COLUMNAS = 10 * CARACTERES_POR_LINEA_COLUMNA


def _corta(corrida):
    """True si la corrida no da para llenar las dos columnas."""
    if not all(x.startswith("<p") for x in corrida):
        return False          # una figura o una tabla ya ocupa alto propio
    return sum(len(_texto_plano(x)) for x in corrida) < CORRIDA_MINIMA_COLUMNAS


def _envolver(corrida):
    """La corrida como banda a dos columnas, o suelta si es corta."""
    if _corta(corrida):
        return "".join(corrida)
    return '<div class="banda">%s</div>' % "".join(corrida)
LINEAS_MINIMAS_ENTRADA = 4
ENTRADA_MINIMA = CARACTERES_POR_LINEA_ANCHA * LINEAS_MINIMAS_ENTRADA
PARRAFOS_MAXIMOS_ENTRADA = 3


def _fuerte(m):
    dentro = m.group(1)
    clase = "" if RE_CIFRA.search(dentro) else ' class="idea"'
    return "<strong%s>%s</strong>" % (clase, dentro)


def _inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', _fuerte, t)
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
    # TODAS LAS TABLAS VAN AL ANCHO DE LA CAJA. En la referencia no hay una
    # sola tabla metida adentro de una columna, y hay un motivo mecanico
    # ademas del estetico: una tabla dentro de una banda a dos columnas se
    # parte por la mitad y la columna de al lado arranca con una fila suelta
    # —"324.304 34,4 17,8"— o peor, con la cabecera. break-inside: avoid no
    # alcanza para impedirlo.
    ancha = True

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
    """La banda ilustrada que abre un capitulo, si le toca una."""
    nombre = APERTURAS.get(slug)
    if not nombre:
        return ""
    ruta = imagen(nombre)
    if not ruta:
        return ""
    return ('<figure class="apertura"><img src="file://%s" alt=""/>'
            '<figcaption>%s</figcaption></figure>'
            % (ruta, html.escape(PIE_ILUSTRACION)))


def _h1(texto, slug):
    """El titulo de capitulo. Las palabras, todas; el peso, repartido.

    "2 La gestión, medida" se compone con el numero en ladrillo y el nombre en
    tinta, que es como la referencia introduce sus veinticinco secciones sin
    una sola excepcion: numero solo, nombre en minuscula, sin la palabra
    "capitulo" y sin raya.
    """
    m = RE_H1CAP.match(texto.strip())
    if m:
        # OJO: el espacio entre el numero y el nombre tiene que estar en el
        # TEXTO, no solo en el margen del CSS. La cornisa se compone con
        # string-set: cap content(), que copia el texto y no ve los margenes:
        # sin ese espacio imprimia "5QUÉ HACEMOS EN CADA ÁREA".
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
    # Solo los capitulos NUMERADOS llevan bajada: el h2 sin numero que sigue
    # al titulo. En la introduccion y en el anexo ese h2 es una seccion de
    # verdad, y tomarlo por bajada lo borraria del indice.
    es_capitulo = bool(re.search(r'^#\s+\d+\s', md, re.M))
    subsecciones = []
    # LA ENTRADA. En la referencia el primer parrafo de cada capitulo va a
    # TODO EL ANCHO y un punto mas grande que el cuerpo, y recien despues
    # empiezan las columnas. Es lo que le da a la pagina de apertura una
    # entrada de lectura en vez de tirar al lector directo a una columna de
    # 85 mm. Se marca el parrafo que sigue a la bajada del capitulo.
    toca_entrada = [False]
    # LAS ILUSTRACIONES DE ADENTRO VAN AL FINAL DE SU SUBSECCION, no al
    # principio: la seccion desarrolla su argumento y la imagen lo cierra.
    # Se guarda cual esta pendiente y se suelta al llegar al titulo siguiente
    # o al terminar el capitulo.
    dentro = dict(DENTRO.get(slug, {}))
    pendiente = [None]

    def soltar_ilustracion(cierre=False):
        if pendiente[0] is None:
            return
        nombres, pie = pendiente[0]
        pendiente[0] = None
        # La que cierra un capitulo va mas alta: es la ultima pagina y hay
        # lugar, y una imagen de cierre a media altura se lee como relleno.
        clase = ("par" if len(nombres) > 1
                 else ("sola cierre" if cierre else "sola"))
        fig = _figura_ilustracion(nombres, pie, clase)
        if fig:
            add(True, fig)

    def add(ancho, htm):
        # La entrada es el parrafo que viene PEGADO al titulo o a la bajada, no
        # el primer parrafo que aparezca tres bloques mas abajo. Cualquier otra
        # cosa que se meta en el medio cancela la espera.
        if (out and not htm.startswith("<h2")
                and 'class="entrada"' not in htm
                and 'class="bajada"' not in htm):
            toca_entrada[0] = toca_entrada[0] and htm.startswith("<p>")
        out.append((ancho, htm))

    while i < n:
        l = lineas[i]

        # LA BAJADA, DECLARADA. Antes se adivinaba: "el h2 sin numero que
        # sigue al titulo, si el capitulo esta numerado". Esa regla ya habia
        # fallado una vez —ningun capitulo tenia bajada— y ademas no servia
        # para la introduccion, donde el primer h2 es una seccion de verdad.
        # Declararla saca la adivinanza del medio y permite que la bajada sea
        # de dos a cuatro lineas, como las 26 de la referencia, en vez de una.
        # EL TABLERO DE CIFRAS. Medido sobre su pagina 22, el exhibit 28:
        #   filete de 0,7 pt en arena #C6AE8E, a todo el ancho
        #   rotulo   Inter 6,4 MAYUSCULA en gris calido
        #   cifra    Spectral Bold 19 en ladrillo
        #   nota     Spectral cursiva 7,5 en gris calido, dos lineas
        #   filete de cierre, igual al de arriba
        # Cuatro columnas de 142,5 pt en los 570 de la caja. SIN FONDO: son
        # dos filetes y aire. Nosotros no teniamos ninguna pieza asi y es la
        # unica que pone una cifra a cuerpo de titulo.
        if l.startswith("TABLERO:"):
            celdas = []
            for tro in l[8:].split(";;"):
                partes = [x.strip() for x in tro.split("|")]
                if len(partes) != 3:
                    continue
                celdas.append(
                    '<div class="tb-c"><p class="tb-r">%s</p>'
                    '<p class="tb-n">%s</p><p class="tb-p">%s</p></div>'
                    % (html.escape(partes[0]), _inline(partes[1]),
                       _inline(partes[2])))
            if celdas:
                add(True, '<div class="tablero">%s</div>' % "".join(celdas))
            i += 1
            continue

        if l.startswith("BAJADA:"):
            add(True, '<p class="bajada">%s</p>' % _inline(l[7:].strip()))
            hay_bajada = True
            toca_entrada[0] = True
            i += 1
            continue

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
                # DONDE VA LA CAJA. En la referencia estan las dos
                # formas y no es capricho: en su pagina 8 la caja va a TODO EL
                # ANCHO, entre dos exhibits; en su pagina 13 va en la COLUMNA
                # DE LA DERECHA, con la prosa corriendo por la izquierda a su
                # lado. Lo que decide es el contexto: una caja que interrumpe
                # prosa corriente se pone al costado y deja seguir leyendo;
                # una que separa dos piezas anchas se pone al ancho.
                add(not _entre_prosa(out),
                    '<aside class="caja %s"><h5>%s</h5>%s</aside>'
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
                soltar_ilustracion()
                if m2.group(1) in dentro:
                    pendiente[0] = dentro.pop(m2.group(1))
                toca_entrada[0] = True
                add(True, '<h2 id="%s"><span class="n">%s</span>%s</h2>'
                    % (sid, m2.group(1), _inline(m2.group(2))))
            else:
                subsecciones.append((sid, None, crudo))
                toca_entrada[0] = True
                add(True, '<h2 id="%s">%s</h2>' % (sid, _inline(crudo)))

        elif l.startswith("# "):
            vistos_h1 += 1
            # LA BANDA Y EL TITULO SON UNA SOLA PIEZA. Emitidas por separado,
            # la banda se quedaba al pie de la pagina anterior y el titulo
            # saltaba solo a la siguiente: el capitulo abria con una foto
            # cerrando el capitulo de antes.
            add(True, _apertura(slug) + _h1(l[2:], slug))

        elif l.startswith("> "):
            j, cita = i, []
            while j < n and lineas[j].startswith(">"):
                cita.append(lineas[j].lstrip("> ").rstrip())
                j += 1
            add(not _entre_prosa(out),
                '<aside class="caja legal">%s</aside>'
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
            add(True, "<ol>%s</ol>"
                % "".join("<li>%s</li>" % _inline(x) for x in items))
            i = j
            continue

        elif l.strip().startswith("- "):
            j, items = i, []
            while j < n and lineas[j].strip().startswith("- "):
                items.append(lineas[j].strip()[2:])
                j += 1
            add(True, "<ul>%s</ul>"
                % "".join("<li>%s</li>" % _inline(x) for x in items))
            i = j
            continue

        elif l.strip():
            txt = l.strip()
            if txt in _lista(DATOS, slug):
                add(True, '<p class="dato">%s</p>' % _inline(txt))
            elif txt in _lista(REMATES, slug):
                rot = ROTULOS_REMATE.get(txt)
                add(True, '<aside class="caja remate">%s<p>%s</p></aside>'
                    % ('<h5>%s</h5>' % html.escape(rot) if rot else "",
                       _inline(txt)))
            elif toca_entrada[0]:
                # Se miran los parrafos que siguen, hasta tres, y se decide
                # sobre el total: o cruzan las dos columnas todos juntos, o no
                # cruza ninguno.
                j, corrida, largo = i, [], 0
                while (j < n and len(corrida) < PARRAFOS_MAXIMOS_ENTRADA):
                    c = lineas[j].strip()
                    if not c:
                        j += 1
                        continue
                    if not _es_parrafo(c):
                        break
                    corrida.append(c)
                    largo += len(c)
                    j += 1
                    if largo >= ENTRADA_MINIMA:
                        break
                if largo >= ENTRADA_MINIMA:
                    add(True, "".join('<p class="entrada">%s</p>' % _inline(c)
                                      for c in corrida))
                    toca_entrada[0] = False
                    i = j
                    continue
                toca_entrada[0] = False
                add(False, "<p>%s</p>" % _inline(txt))
            else:
                add(False, "<p>%s</p>" % _inline(txt))
        i += 1
    soltar_ilustracion()
    if "*" in dentro:
        pendiente[0] = dentro.pop("*")
        soltar_ilustracion(cierre=True)
    return out, subsecciones


def _es_parrafo(t):
    """True si la linea de markdown es prosa corriente y no otra cosa."""
    return (bool(t) and not t.startswith(("|", "- ", "#", "> ", "```", "**["))
            and not re.match(r'^\d+\.\s', t)
            and not RE_EXHIBIT.match(t))


def _entre_prosa(emitidos):
    """True si lo ultimo que se emitio es un parrafo de prosa corriente."""
    for ancho, htm in reversed(emitidos):
        if htm.strip():
            return htm.startswith("<p>")
    return False


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
            # UN h2 CON SU ENTRADA. La entrada es ancha —va cruzando las dos
            # columnas, como en la referencia—, asi que no la agarra la regla
            # de abajo, que junta el titulo con la banda. Sin esto el titulo
            # quedaria suelto y podria caer al pie de una pagina con su
            # entrada en la siguiente.
            if (htm.startswith("<h2") and i + 1 < n and lista[i + 1][0]
                    and 'class="entrada"' in lista[i + 1][1]):
                grupo = htm + lista[i + 1][1]
                j = i + 2
                # Y si despues de la entrada empieza prosa a dos columnas, las
                # primeras lineas entran al grupo: es el mismo motivo.
                if j < n and not lista[j][0]:
                    corrida = []
                    while j < n and not lista[j][0]:
                        corrida.append(lista[j][1])
                        j += 1
                    grupo += ('<div class="banda">%s</div>'
                              % "".join(corrida[:1]))
                    resto = corrida[1:]
                else:
                    resto = []
                pieza('<div class="con-titulo">%s</div>' % grupo, "titulo")
                if resto:
                    pieza(_envolver(resto), "banda")
                i = j
                continue
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
                    pieza(_envolver(corrida), "banda")
                    i = j
                    continue
                # LA UNICA EXCEPCION: una entrada que TERMINA EN DOS PUNTOS no
                # es un parrafo, es el pie de una tabla —"Millones de pesos
                # constantes de diciembre de 2025:"—. Separarla de su tabla deja
                # el titulo al pie de la pagina anunciando algo que no esta. Si
                # esa tabla es chica, entra al grupo con ella.
                # EL GRUPO TIENE QUE LLENAR LAS DOS COLUMNAS, NO UNA.
                # Con un solo parrafo de tres lineas, la banda del grupo
                # balanceaba tres lineas en la columna izquierda y dejaba la
                # derecha vacia justo debajo del titulo: un escalon en blanco
                # arriba de la pagina. Se toman parrafos hasta juntar cuatro
                # lineas de columna —dos por lado, 62 caracteres cada una— con
                # un tope de tres, que es lo que evita que el grupo se vuelva
                # un ladrillo que no entra en ningun pie.
                corte, junta = 0, 0
                while (corte < len(corrida) and corte < 3
                       and junta < 4 * CARACTERES_POR_LINEA_COLUMNA):
                    if not corrida[corte].startswith("<p"):
                        break
                    junta += len(_texto_plano(corrida[corte]))
                    corte += 1
                corte = max(corte, 1)
                if (len(corrida) > 1
                        and _texto_plano(corrida[0]).endswith(":")
                        and corrida[1].startswith('<div class="tw')
                        and corrida[1].count("<tr>") <= 11
                        and len(_texto_plano(corrida[1])) <= 400):
                    corte = 2
                cabeza, resto = corrida[:corte], corrida[corte:]
                grupo = [_envolver(cabeza)]
                pieza('<div class="con-titulo">%s%s</div>'
                      % (htm, "".join(grupo)), "titulo")
                if resto:
                    pieza(_envolver(resto), "banda")
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
        pieza(_envolver(corrida), "banda")
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
    # LA NOTA NO SIEMPRE ES LA ULTIMA PIEZA. La ilustracion de cierre del
    # capitulo —la del "*" en DENTRO— se suelta DESPUES de la nota, asi que
    # mirar solo la ultima pieza daba siempre que no, y el cierre no se
    # agrupaba nunca. Resultado: la ilustracion se iba sola a una pagina y
    # quedaba una hoja con una foto arriba y dos tercios de papel. Se busca la
    # nota entre las ultimas piezas y el grupo se estira HASTA EL FINAL, de
    # modo que la ilustracion viaja adentro.
    pos = next((k for k in range(len(piezas_de_seccion) - 1, -1, -1)
                if "nota-envoltorio" in piezas_de_seccion[k]["html"]), None)
    if pos is None or pos < len(piezas_de_seccion) - 3:
        return piezas_de_seccion
    # Hacia atras, juntando prosa y separadores hasta que el bloque tenga con
    # que sostener una pagina. Con una sola banda no alcanzaba: el capitulo 2
    # cierra con un parrafo de dos lineas y la pagina seguia al 15%.
    #
    # SE FRENA EN LO PRIMERO QUE NO SEA PROSA. Tragarse un exhibit haria un
    # bloque indivisible de media pagina, que es el problema del otro lado.
    # EL RECORRIDO HACIA ATRAS, hasta juntar con que sostener una pagina.
    # Con una sola banda no alcanzaba: el capitulo 2 cierra con un parrafo de
    # dos lineas y la pagina seguia al 15 %. Y frenando en lo primero que no
    # es prosa tampoco: en los capitulos 3 y 5 lo que hay detras de la nota es
    # un titulo, el bloque quedaba en setecientos caracteres, se iba solo a
    # una pagina nueva y esa pagina salia al 2 %.
    #
    # Asi que se cruza lo que haga falta, CON UN SOLO LIMITE: una figura. Un
    # exhibit mide media pagina; dos, mas que una pagina entera, y ahi el
    # bloque indivisible se vuelve el problema del otro lado.
    corte = pos
    texto = sum(len(_texto_plano(x["html"])) for x in piezas_de_seccion[pos:])
    figuras = sum(1 for x in piezas_de_seccion[pos:] if x["tipo"] == "figura")
    while corte > 0 and texto < CIERRE_MINIMO:
        previa = piezas_de_seccion[corte - 1]
        if previa["tipo"] == "figura":
            if figuras:
                break
            figuras += 1
        texto += len(_texto_plano(previa["html"]))
        corte -= 1
    if texto < CIERRE_MINIMO:
        # Ni asi alcanza: entonces se parte la nota, que se lee mucho mejor
        # que una pagina en blanco con una nota arriba.
        piezas_de_seccion[pos]["html"] = piezas_de_seccion[pos]["html"].replace(
            'class="nota-envoltorio"', 'class="nota-envoltorio parte"', 1)
        return piezas_de_seccion
    if corte == pos and pos == len(piezas_de_seccion) - 1:
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

HUECO_MINIMO = 16.0     # mm: menos que esto no es un hueco, es el aire del pie
PASADAS_MAXIMAS = 14    # cada pasada rearma el PDF entero
SALTOS_MAXIMOS = 4      # cuantas veces se puede bajar una misma figura


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
            # Se bajan las FIGURAS y las piezas ANCHAS —tablas, listados,
            # cifras destacadas—: las dos son bloques indivisibles que cuando
            # no entran en el pie se van enteras a la pagina siguiente y dejan
            # el hueco. Antes solo se bajaban las figuras, y la mitad de los
            # huecos grandes los abria una tabla.
            if (orden[k]["tipo"] not in ("figura", "ancho")
                    or orden[k + 1]["tipo"] != "banda"):
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
    ilustracion = imagen(TAPA_ILUSTRACION)
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
    """El indice, con la anatomia de su pagina de contenidos.

    Medida linea por linea sobre su pagina 2. Su indice tiene DOS NIVELES y
    ninguno de los dos es el que teniamos:

      - un CINTILLO DE GRUPO en Inter mayuscula espaciada, pegado al margen,
        sin numero de pagina y sin filete: "THE THESIS", "THE BUILD";
      - una ENTRADA por seccion, con el numero colgando en el margen a 22 pt
        del titulo, el titulo alineado con todos los demas, una guia de
        puntos que llega hasta el borde derecho y el numero de pagina
        alineado a la derecha.

    Nuestros capitulos ocupan el lugar de sus cintillos y nuestras
    subsecciones el de sus entradas: es la misma estructura de dos niveles
    con el mismo tratamiento, aplicada a lo que nuestro documento tiene.

    NO HAY UNA SOLA REGLA HORIZONTAL en su indice. Ni bajo el titulo de la
    pagina, ni entre entradas, ni bajo los capitulos. Las teniamos las tres.
    """
    # EL GRUPO RESALTADO. En su indice las seis entradas de THE MODEL —el
    # grupo donde esta lo que vienen a vender— van en Spectral SemiBold
    # ladrillo y el resto en Spectral Regular tinta: 35 palabras de las 108.
    # Un solo grupo levantado del resto, y es el de la propuesta. El nuestro
    # es EL MECANISMO: las comisiones vecinales con presupuesto propio.
    filas = []
    for slug, titulo, subs in entradas:
        # SIN NUMERO. Sus cintillos de grupo son "THE THESIS", "THE BUILD":
        # una etiqueta, no una numeracion. El numero del capitulo ya viaja en
        # el de cada entrada —1.1, 1.2— asi que repetirlo arriba es ruido.
        m = RE_H1CAP.match(titulo)
        nombre = m.group(2) if m else titulo
        propuesta = GRUPO_PROPUESTA.lower() in nombre.lower()
        filas.append('<li class="ix-cap"><a href="#%s">%s</a></li>'
                     % (slug, html.escape(nombre)))
        for sid, n, tit in subs:
            filas.append(
                '<li class="ix-sub%s"><a href="#%s">'
                '<span class="ix-n">%s</span>'
                '<span class="ix-t">%s</span></a></li>'
                % (" propuesta" if propuesta else "",
                   sid, html.escape(n or ""), html.escape(tit)))
    return ('<section class="indice"><h1 class="ix-h">Índice</h1>'
            '<ul class="ix">%s</ul></section>' % "".join(filas))


# ==========================================================================
# 5. CSS
# ==========================================================================

# ==========================================================================
# LA ESCALA: A4 ES UNA REDUCCION DE LA REFERENCIA, NO UNA COPIA A TAMAÑO REAL
# ==========================================================================
# La pagina del Extra Time mide 660 pt de ancho —232,8 mm— y la nuestra 210.
# Copiar sus cuerpos TAL CUAL en una pagina un 10 % mas angosta agranda la
# letra: el mismo 9,7 pt en una columna de 86 mm en vez de una de 96 da menos
# caracteres por linea, o sea una mancha mas gruesa y menos densa. Eso fue
# exactamente lo que paso, y se ve al lado de la referencia.
#
# ASI QUE TODO SE MULTIPLICA POR EL MISMO NUMERO. Margenes, medianil, cuerpos,
# interlineas, filetes, bandas de tabla, sangrias y separaciones entre bloques
# salen de las medidas de 04_diseno/MEDIDAS_EXTRATIME.md multiplicadas por
# 210/232,8. La pagina resultante es la de ellos reducida al 90,2 %: misma
# cantidad de caracteres por linea, mismo gris de la mancha, misma proporcion
# entre cada pieza y la de al lado. No hay ni un numero elegido a ojo.
ESCALA = 210.0 / 232.8


def e(pt, dec=2):
    """Un valor medido en la referencia, llevado a nuestra pagina."""
    return round(pt * ESCALA, dec)


def emm(pt, dec=2):
    """Lo mismo, pero expresado en milimetros."""
    return round(pt * ESCALA / 72 * 25.4, dec)


# Las medidas de la referencia, en puntos, tal como salieron de medirla.
# El margen de CSS de una separacion es su distancia MENOS el alto de linea
# del bloque de arriba: las distancias estan medidas de linea a linea.
REF = dict(
    pagina=660.0, margen=45.0, caja=570.0, medianil=24.0, columna=271.0,
    cuerpo=9.7, cuerpo_int=14.5,          # el cuerpo a dos columnas
    entrada=10.0, entrada_int=16.0,       # el primer parrafo, a todo el ancho
    h1=16.5, h1_int=19.5,
    bajada=10.875, bajada_int=15.0,
    h2=11.2, h3=9.7,
    exh_rot=6.7, exh_tit=11.2, exh_tit_int=14.6,
    tabla_cab=6.375, tabla=7.875, tabla_int=11.1,
    banda_cab=17.3, banda_fila=20.2, celda=6.0,
    fuente=7.875, fuente_int=11.5,
    cornisa=6.7, pie=6.4,
    filete=0.75,
    caja_cuerpo=9.0, caja_int=13.0, caja_rot=6.375,
    caja_filete=2.25, caja_sangria=12.0, caja_alto=12.0,
    sep_bloque=22.0 - 14.5,               # 7,5 pt de margen real
    sep_rot_tit=14.0 - 8.7,               # 5,3
    sep_tit_fig=21.0 - 14.6,              # 6,4
    sep_fig_fuente=25.0 - 20.2,           # 4,8
    sep_fuente_cuerpo=22.0 - 11.5,        # 10,5
    sep_h1_bajada=25.0 - 19.5,            # 5,5
    sep_bajada_entrada=25.0 - 15.0,       # 10,0
    sep_cornisa_h1=37.0 - 8.7,            # 28,3
)

def instalar_tipografias():
    """Pone las tipografias del repo donde WeasyPrint las va a encontrar.

    ESTO ES EL ARREGLO DE UN BUG QUE SE COMIO TODO EL DISEÑO. El CSS declaraba
    sus @font-face apuntando al archivo por ruta absoluta —que es lo correcto y
    lo que dice el README—, y WeasyPrint 70 los ignoraba en silencio: no avisa,
    no falla, simplemente cae a DejaVu. El documento entero venia compuesto en
    DejaVu Serif desde el primer dia.

    Y DejaVu no es un reemplazo neutro: tiene la altura de x mucho mas grande y
    los glifos mucho mas anchos que Spectral, asi que la misma medida en puntos
    se ve varios cuerpos mas grande y entran 51 caracteres por linea donde la
    referencia mete 61. Todo el trabajo de ajustar la escala corregia un sintoma
    —"la letra se ve mas grande"— cuya causa era esta.

    En esta version de WeasyPrint el unico camino que carga de verdad es
    fontconfig, asi que el armador copia los archivos versionados a la carpeta
    de fuentes del usuario y refresca el cache antes de componer. Las fuentes
    siguen viniendo del repo —no se depende de que esten instaladas en la
    maquina—, y el armado sigue siendo reproducible: lo que cambia es que ahora
    de verdad se usan.
    """
    destino = os.path.expanduser("~/.local/share/fonts")
    os.makedirs(destino, exist_ok=True)
    copiadas = 0
    for f in sorted(os.listdir(TIPOS)):
        if not f.endswith(".ttf"):
            continue
        origen, final = os.path.join(TIPOS, f), os.path.join(destino, f)
        if (not os.path.exists(final)
                or os.path.getmtime(final) < os.path.getmtime(origen)):
            shutil.copy2(origen, final)
            copiadas += 1
    if copiadas:
        subprocess.run(["fc-cache", "-f", destino], capture_output=True)
    # Y se comprueba: un fallback silencioso es justamente lo que paso.
    hay = subprocess.run(["fc-list", "--format", "%{family}\n"],
                         capture_output=True, text=True).stdout
    faltan = [n for n in (SERIF, SANS) if n.lower() not in hay.lower()]
    if faltan:                                            # pragma: no cover
        raise RuntimeError(
            "fontconfig no encuentra %s despues de instalarlas desde %s: el "
            "documento saldria compuesto en otra letra" % (", ".join(faltan),
                                                           TIPOS))
    return copiadas


# Los seis @font-face de Spectral se escriben solos desde CORTES_SERIF: son
# archivos estaticos y cada uno declara su peso y su estilo.
_FACES = "\n".join(
    '@font-face { font-family: "%s"; src: url("file://%s/%s");\n'
    '             font-weight: %d; font-style: %s; }' % (SERIF, TIPOS, f, w, e_)
    for f, w, e_ in CORTES_SERIF)

CSS = _FACES + """
@font-face { font-family: "%(sans)s";
             src: url("file://%(tipos)s/Inter[opsz,wght].ttf");
             font-weight: 100 900; font-style: normal; }
@font-face { font-family: "%(sans)s";
             src: url("file://%(tipos)s/Inter-Italic[opsz,wght].ttf");
             font-weight: 100 900; font-style: italic; }

/* ====================================================================
   GEOMETRIA — 04_diseno/MEDIDAS_EXTRATIME.md por 210/232,8

   Margen 45 pt -> %(mg).1f mm.  Caja 570 pt -> %(cj).1f mm.
   Medianil 24 pt -> %(md).1f mm.  Columna 271 pt -> %(col).1f mm, que son los
   mismos caracteres por linea que su columna de 95,6.

   Del ALTO de la referencia no se copia nada: el original es una exportacion
   continua de Figma con paginas de entre 872 y 2685 pt porque cada capitulo
   es un lienzo. Nosotros paginamos A4 de verdad.
   ==================================================================== */
@page {
  size: A4; margin: %(mgsup).1fmm %(mg).1fmm %(pie)dmm %(mg).1fmm;
  /* SIN CORNISA. Repetia el nombre de la seccion en cada pagina, y en el
     indice eso imprimia "ÍNDICE" arriba y "Índice" debajo: la misma palabra
     dos veces. La referencia no pone ahi el nombre de la seccion. */
  @bottom-left  { content: "%(corto)s"; font-family: "%(sans)s";
                  font-size: %(pie_pt).1fpt; letter-spacing: %(tr_pie).2fpt;
                  white-space: pre;
                  color: %(gris)s; vertical-align: top; }
  @bottom-right { content: "Página " counter(page) " de " counter(pages);
                  font-family: "%(sans)s"; font-size: %(pie_pt).1fpt;
                  font-variant-numeric: tabular-nums lining-nums;
                  white-space: pre; color: %(tinta)s; opacity: .65;
                  vertical-align: top; }
  /* Todos los filetes de la referencia miden 0,75 pt: 567 de los 570
     rectangulos finos medidos dan ese grosor. El unico grueso del documento
     es el que lleva la caja al costado, y mide 3.

     EL FILETE DE PIE. Estaba escrito como `border-bottom` del @page y no
     dibujaba nada: en las 44 paginas no hay un solo rectangulo debajo de
     700 pt. Se pinta como fondo del @page, que si funciona y ademas se
     puede apagar en la tapa. Va a ras del borde de abajo de la caja de
     texto —45 pt del borde de la hoja en la referencia, que es su mismo
     margen— y el texto del pie queda por debajo. Sus paginas 3 a 21 lo
     llevan; la tapa y el indice no. */
  border: 0;
  background: %(crema)s;
}
@page :first { margin: 0; border: 0; padding: 0;
  background-image: none;
  @bottom-left { content: ""; }
  @bottom-right { content: ""; } }

html { background: %(crema)s; }

/* --------------------------------------------------------------------
   EL FILETE DEL PIE

   Lo llevan sus paginas 3 a 21, en tinta, de 0,75 pt, a todo el ancho de
   la caja y justo sobre la linea del margen de abajo; el texto del pie va
   por debajo. Nosotros no teniamos ninguno.

   Dos intentos que NO sirven, anotados para no repetirlos:
     - `border-bottom` en el @page no dibuja nada. En las 44 paginas no
       habia un solo rectangulo por debajo de los 700 pt.
     - `border-top` en @bottom-left y @bottom-right dibuja dos filetes
       cortos, uno bajo cada texto, con un hueco en el medio: las cajas de
       margen se achican a su contenido.
     - Como fondo del @page tampoco: WeasyPrint 70 ignora el
       `background-size` de un `linear-gradient` en @page y el degradado
       llena la hoja entera. Da una pagina en tinta con un recuadro crema.
   Queda el elemento fijo, que se estira de margen a margen y da el filete
   entero. Se dibuja tambien en la tapa —no hay forma de apagarlo por
   pagina— asi que va con `z-index: -1` y la ilustracion a sangre, que se
   pinta encima, lo tapa. En las paginas de texto no hay nada que lo tape.
   -------------------------------------------------------------------- */
.filete-pie { position: fixed; left: 0; right: 0; bottom: 0; height: 0;
              z-index: -1;
              border-top: %(filete).2fpt solid %(tinta)s; }

/* EL MARGEN DE BODY VA EN CERO, Y ESTO NO ES UN DETALLE.
   El estilo por defecto le da a body 8 px de margen, que son 6 pt: todo el
   documento venia 2,1 mm metido hacia adentro por los cuatro lados respecto
   del margen que declara @page. La caja de texto media 173,8 mm en vez de
   181,4, y cada medida tomada de la referencia caia sobre una caja que no
   era la que se habia calculado. Se nota al medir la pagina: la cornisa, que
   vive en una caja de margen, arrancaba en 40,5 pt y el texto en 46,5. */
body { margin: 0; font-family: "%(serif)s", Georgia, serif; font-size: %(cuerpo).2fpt;
       line-height: %(cuerpo_int).3f; color: %(tinta)s;
       font-variant-numeric: lining-nums; }

/* --------------------------------------------------------------------
   BANDAS. La prosa a dos columnas balanceadas; todo lo demas al ancho.
   -------------------------------------------------------------------- */
.banda { columns: 2; column-gap: %(md).1fmm; }
.banda > *:first-child { margin-top: 0; }
.con-titulo { break-inside: avoid; }
.con-titulo .banda { margin-top: 0; }

p { margin: 0 0 .5em; text-align: justify; hyphens: auto; }
/* Cuatro lineas: con tres, una columna todavia podia arrancar con el resto
   de una oracion —"lo demuestra."— y eso se lee como un renglon perdido. */
p, li { orphans: 4; widows: 4; }
/* EL COLOR ENTRA POR LA PROSA, como en la referencia: las negritas del cuerpo
   no son negras. El texto no se toca —las negritas ya estaban escritas—, lo
   unico que cambia es de que color salen. */
/* Medido: la cifra va en Spectral BOLD ladrillo y el concepto en Spectral
   SEMIBOLD salvia. No es el mismo peso: la cifra pesa mas. */
strong { font-weight: 700; color: %(acento)s; }
strong.idea { font-weight: 600; color: %(dato)s; }
em { font-style: italic; }
code { font-family: "DejaVu Sans Mono"; font-size: %(mono).1fpt;
       background: %(arena)s; padding: .5pt 2pt; }
a { color: %(acento)s; text-decoration: none; }
/* EL SEPARADOR NO DIBUJA LINEA. Son 60 filetes de arena a todo el ancho
   repartidos por el documento, uno entre cada dos subsecciones. En sus 30
   paginas no hay NI UNO: sus unicos filetes largos son el del pie (uno por
   pagina, en tinta) y los de las tablas. El corte del original se respeta
   —sigue siendo un corte— pero se dice con aire, que es como lo dice ella. */
hr { border: 0; margin: %(sep).1fmm 0; height: 0; }

/* --------------------------------------------------------------------
   JERARQUIA
   -------------------------------------------------------------------- */
/* El numero en ladrillo y el nombre en tinta, que es lo que hace ella. */
/* EL AIRE QUE DEJABA LA CORNISA. En su pagina la linea de marca esta a
   38,3 pt del borde y el titulo a 72,1: hay 30 pt de aire entre una y otro.
   Sacada la cornisa, ese aire tiene que ponerlo el titulo, o el capitulo
   arranca pegado al borde de arriba y la composicion no es la suya. */
/* EL TITULO VA EN LADRILLO. Los 174 glifos de titulo de seccion de la
   referencia estan TODOS en ladrillo y su cifra en coral; los nuestros
   estaban en tinta —20 en tinta contra 7 en ladrillo— y por eso la pagina
   abria en gris. */
h1 { font-size: %(h1).1fpt; line-height: %(h1_int).3f;
     margin: %(aire_arriba).1fmm 0 %(sep_h1_bajada).1fmm;
     font-weight: 700; letter-spacing: 0; color: %(acento)s;
     break-before: page; break-after: avoid; }
/* En su titulo el numero y el nombre estan separados por algo mas que un
   espacio de palabra: el espacio va en el texto —lo necesita la cornisa— y el
   margen lo completa hasta el medio cuadratin. */
h1 .cn { color: %(coral)s; margin-right: .12em; }

p.bajada { font-style: italic; font-weight: 500; font-size: %(bajada).1fpt;
           line-height: %(bajada_int).3f; color: %(dato)s;
           margin: 0 0 %(sep_bajada).1fmm;
           max-width: 152mm; text-align: left; hyphens: none;
           break-after: avoid; }
p.bajada strong { color: %(dato)s; font-weight: 600; }

/* La entrada: el primer parrafo del capitulo va a TODO EL ANCHO y un punto
   mas que el cuerpo, y recien despues empiezan las columnas. */
p.entrada { font-size: %(entrada).1fpt; line-height: %(entrada_int).3f;
            text-align: left; margin: 0 0 %(sep).1fmm; hyphens: none; }

/* EL SUBTITULO: 11,2 EN LADRILLO. En las 30 paginas de la referencia NO HAY
   UN SOLO GLIFO A 12,2 pt —el 12,2 que teniamos salio de una medicion que
   nunca estuvo ahi—. Su nivel de subtitulo son las 410 palabras en Spectral
   SemiBold 11,2 ladrillo contra el margen, las mismas que rotulan sus
   exhibits. Un solo nivel, un solo color. El nuestro iba a 12,2 en tinta:
   mas grande que el suyo y sin color, que es la peor de las dos. */
h2 { font-size: %(h2).1fpt; line-height: 1.25;
     margin: %(sep_h2).1fmm 0 %(sep_h2b).1fmm;
     font-weight: 600; color: %(acento)s; break-after: avoid;
     break-inside: avoid; text-indent: -0.05em; }
h2 .n { font-weight: 700; color: %(coral)s;
        font-variant-numeric: lining-nums; margin-right: .32em; }
h1 + p.bajada + .banda h2:first-child,
h1 + p.bajada + .con-titulo > h2 { margin-top: 0; }

h3 { font-size: %(h3).1fpt; font-weight: 600;
     margin: %(sep_h3).1fmm 0 %(sep_h3b).1fmm;
     color: %(acento)s; break-after: avoid; break-inside: avoid; }
/* Sin filete encima. Era un invento nuestro: la referencia no pone una
   reglita arriba de cada subtitulo, y tres seguidos en una columna de 86 mm
   se leen como un formulario. */

/* --------------------------------------------------------------------
   CIFRAS DESTACADAS Y REMATES
   -------------------------------------------------------------------- */
p.dato { font-size: %(dato_pt).1fpt; line-height: 1.3; color: %(acento)s;
         font-weight: 500; margin: %(sep_caja).1fmm 0;
         padding: 0 0 0 %(caja_sangria).1fmm; text-align: left;
         border-left: %(filete).2fpt solid %(acento)s;
         hyphens: none; break-inside: avoid; }
p.dato strong { color: %(acento)s; font-weight: 600; }

/* EL REMATE ES UNA CAJA, NO UN FILETE. Es la frase con que cierra cada
   seccion, y la referencia cierra las suyas con la caja: fondo tan, filete
   de 3 pt al costado y el texto adentro. Nosotros lo teniamos como una
   reglita de 0,68 pt en ladrillo con cursiva al lado —un subrayado lateral,
   no una pieza—. Mismo fondo y mismo filete que la caja legal: son la misma
   familia y ahora se leen como tal. */
aside.caja.remate > p { font-size: %(bajada).1fpt;
           line-height: %(bajada_int).3f;
           color: %(tinta)s; font-style: italic; font-weight: 500;
           text-align: left;
           hyphens: none; break-inside: avoid; }
aside.caja.remate > p strong { font-style: normal; font-weight: 600;
                              color: %(acento)s; }

/* --------------------------------------------------------------------
   LA CAJA — medida pixel por pixel sobre la pagina 8 de la referencia
   --------------------------------------------------------------------
   Fondo #EFE7DA. Filete izquierdo de 3 pt en SALVIA, no de tres cuartos de
   punto: es el unico trazo grueso del documento y es lo que hace que la caja
   se lea como una caja y no como un parrafo sombreado. Cintillo en Inter
   mayuscula espaciada y en SALVIA —no en ladrillo—. Cuerpo Spectral 9,0, que
   es MENOS que el cuerpo de la pagina: la caja es un aparte, y se nota en que
   habla mas bajo. Sangria de 12,4 pt desde el borde. Y va a TODO EL ANCHO de
   la caja de texto: metida adentro de una columna de 86 mm no es esta pieza,
   es otra.
   -------------------------------------------------------------------- */
/* LA CAJA, con los valores de su hoja de estilos:
       background: var(--panel)  #EFE7DA
       border-left: 2.25pt solid var(--sage)   <- 2,25, no 3
       padding: 10.75pt 12pt 11pt
       .clabel: Inter 600 6.375 sage, letter-spacing .765pt, line-height 9pt
   El filete al costado lo teniamos en 3 pt y el rotulo en peso 500. */
.caja { break-inside: avoid; margin: %(sep_caja).1fmm 0;
        padding: %(caja_arriba).2fmm %(caja_sangria).2fmm %(caja_abajo).2fmm;
        background: %(tan)s; font-size: %(caja_cuerpo).1fpt;
        line-height: %(caja_int).3f;
        border-left: %(caja_filete).2fpt solid %(dato)s; }
.caja h5 { font-family: "%(sans)s"; font-size: %(caja_rot).3fpt;
           font-weight: 600; letter-spacing: %(tr_caja).2fpt;
           text-transform: uppercase;
           margin: 0 0 %(sep_caja_rot).1fmm; color: %(dato)s;
           line-height: %(caja_rot_int).2fpt; }
.caja p { margin: 0 0 .5em; text-align: left; hyphens: none; }
.caja p:last-child { margin-bottom: 0; }
.caja.legal { font-style: italic; }
/* LA CAJA AL COSTADO. Metida adentro de una banda a dos columnas ocupa una
   columna sola y la prosa sigue corriendo por la otra, que es lo que hace la
   referencia en su pagina 13. Misma pieza, mismo fondo, mismo filete: lo
   unico que cambia es que no interrumpe la lectura, la acompaña. */
.banda .caja { margin: 0 0 %(sep).1fmm; }
.con-titulo p.entrada { margin-top: 0; }

/* Nota de lectura al pie de seccion: Spectral italico en gris calido, con la
   entrada en SemiBold, a todo el ancho. */
.nota-lectura { margin: %(sep_fuente).1fmm 0 0;
                border-top: %(filete).2fpt solid %(arena)s;
                padding-top: %(sep).1fmm;
                font-size: %(fuente).1fpt; line-height: %(fuente_int).3f;
                color: %(gris)s; font-style: italic;
                columns: 2; column-gap: %(md).1fmm; }
/* La nota no se parte... salvo cuando partirla es lo unico que evita una
   pagina en blanco con una nota arriba. Lo decide cerrar_capitulo(). */
.nota-envoltorio { break-inside: avoid; }
.nota-envoltorio.parte { break-inside: auto; }
.cierre { break-inside: avoid; }
.nota-lectura p { margin: 0 0 .4em; text-align: left; hyphens: none; }
.nota-lectura strong { color: inherit; }
.nota-lectura .et { font-weight: 600; opacity: 1; }
/* La entrada en SemiBold de una fuente o de una nota: Spectral, no
   versalitas. La referencia no usa versalitas en ninguna parte — lo que
   parecian versalitas es Inter en mayusculas espaciadas. */
/* "Fuente:" va en tinta PLENA y el resto en gris calido: en la referencia
   son dos colores distintos, no el mismo aguado. */
.et { font-weight: 600; font-style: normal; color: %(tinta)s; opacity: 1; }

/* --------------------------------------------------------------------
   EL TABLERO DE CIFRAS — medido sobre su pagina 22

   Es la unica pieza de la referencia que pone una cifra a cuerpo de titulo,
   y no lleva fondo: dos filetes de arena y aire. Cuatro columnas iguales en
   los 570 pt de la caja, el texto a 10 pt del arranque de cada una.
   -------------------------------------------------------------------- */
.tablero { display: table; width: 100%%; table-layout: fixed;
           border-top: %(tb_filete).2fpt solid %(ix_punto)s;
           border-bottom: %(tb_filete).2fpt solid %(ix_punto)s;
           margin: %(sep_caja).1fmm 0;
           padding: %(tb_aire).1fmm 0 %(tb_pie).1fmm;
           break-inside: avoid; }
.tb-c { display: table-cell; vertical-align: top; padding-right: 6mm; }
.tb-r { font-family: "%(sans)s"; font-size: %(tb_rot).2fpt; font-weight: 400;
        letter-spacing: %(tb_track).2fpt; text-transform: uppercase;
        color: %(gris)s; margin: 0 0 %(tb_sep1).1fmm; line-height: 1.25;
        text-align: left; hyphens: none; }
.tb-n { font-size: %(tb_cifra).2fpt; font-weight: 700; color: %(acento)s;
        line-height: 1.05; margin: 0 0 %(tb_sep2).1fmm;
        font-variant-numeric: tabular-nums lining-nums;
        text-align: left; hyphens: none; }
.tb-p { font-size: %(tb_nota).2fpt; font-style: italic; color: %(gris)s;
        line-height: 1.32; margin: 0; text-align: left; hyphens: none; }

/* --------------------------------------------------------------------
   LA LISTA — medida sobre su pagina 3, que es toda ella una lista

   Es la pieza mas fuerte de su resumen ejecutivo y la teniamos como una
   vinneta de tres puntos metida en media columna. La suya:

     marca        Spectral Bold 10,5 en OCRE, colgada en el margen (x=45)
     texto        a 23,2 pt del margen (x=68,2)
     entrada      Spectral Bold 9,45 en LADRILLO, en la misma linea
     cuerpo       Spectral Regular 9,45 en tinta, interlinea 13,5
     remision     Spectral Italic 9,45 en gris calido — "(Section 3)"
     entre items  11,2 pt de aire de mas
     ancho        TODO el ancho de la caja, nunca en columna

   La marca es mas grande que el texto que encabeza, va en un color que no
   usa ninguna otra cosa del cuerpo, y cuelga afuera: se lee la lista antes
   de leer una palabra.
   -------------------------------------------------------------------- */
/* OJO CON EL INDICE. Esta regla se escribio como `ul, ol` y `li` a secas, y
   el indice ES un ul: cada entrada se llevo su bolo en ocre colgado en el
   margen, su sangria de 7,4 mm y su aire de 3,5 mm. La guia de puntos empezo
   a cruzar desde el borde y el numero de seccion quedo debajo del bolo. El
   indice tiene su propia anatomia, medida sobre la pagina 2 de la
   referencia, y no comparte NADA con la lista del cuerpo. */
ul:not(.ix), ol { list-style: none; margin: 0 0 %(sep).1fmm; padding: 0;
                  counter-reset: item; }
ul:not(.ix) > li, ol > li {
     position: relative; padding-left: %(li_sangria).2fmm;
     margin-bottom: %(li_aire).2fmm;
     text-align: justify; hyphens: auto; }
ul:not(.ix) > li:last-child, ol > li:last-child { margin-bottom: 0; }
/* LA MARCA SIN NUMERO. En sus 30 paginas NO HAY UNA SOLA lista sin
   numerar: las diecisiete marcas colgadas del margen son todas cifras. O
   sea que para una lista de guiones no hay referencia que copiar, y
   numerar la nuestra seria agregarle al texto una enumeracion que no
   tiene. Queda un bolo en ocre con la masa de una cifra —no el punto
   medio de 9 pt, que al lado del ladrillo no se veia— alineado a la base
   de la primera linea. */
ol > li::before { counter-increment: item; content: counter(item);
                  font-size: %(li_marca).2fpt; }
ul:not(.ix) > li::before { content: "•"; font-size: %(li_bolo).2fpt; }
ul:not(.ix) > li::before, ol > li::before {
             position: absolute; left: 0; top: 0;
             color: %(ocre)s; font-weight: 700;
             line-height: %(li_linea).2fpt; }
/* La entrada de cada item va en ladrillo, como en la suya. _fuerte() ya
   manda a ladrillo lo que lleva cifras y a salvia lo que no; dentro de una
   lista manda siempre el ladrillo, que es lo que ella hace en las ocho. */
li > strong:first-child, li > strong.idea:first-child {
     color: %(acento)s; font-weight: 700; }

/* --------------------------------------------------------------------
   TABLAS. Banda de cabecera 17,3 pt en arena con Inter mayuscula en
   ladrillo, fila de 20,2 pt, alternadas en #E8E4D9, sangria de celda 6 pt.
   -------------------------------------------------------------------- */
.tw { break-inside: avoid; margin: %(sep).1fmm 0; }
table { width: 100%%; border-collapse: collapse;
        font-family: "%(sans)s"; font-size: %(tabla).1fpt;
        line-height: %(tabla_int).3f;
        font-variant-numeric: tabular-nums lining-nums; }
.tw:not(.ancho) table { font-size: %(tabla_chica).1fpt; }
thead th { background: %(arena)s; color: %(acento)s; text-align: left;
           padding: %(cab_arriba).2fmm %(celda).1fmm 0;
           height: %(cab_alto).2fmm;
           font-size: %(tabla_cab).2fpt; font-weight: 600;
           letter-spacing: %(tr_tabla).2fpt; text-transform: uppercase;
           line-height: 1; vertical-align: top;
           border-bottom: %(filete).2fpt solid rgba(40, 34, 22, .24); }
/* EL FILETE DE FILA VA AL 13 %%, NO AL 100 %%. Esto es lo que hacia que
   nuestras tablas se leyeran como una planilla de calculo.
   Conte bien los filetes —364, uno bajo cada celda— pero no la opacidad:
   pdfplumber informa el COLOR del trazo, no su alfa, asi que un pelo de
   tinta al 13 %% y uno al 100 %% se leen iguales al medir el PDF. En su hoja
   de estilos, que ahora tengo, dice:
       td { border-bottom: .75pt solid rgba(40,34,22,.13) }   <- 13 %%
       th { border-bottom: .75pt solid rgba(40,34,22,.24) }   <- 24 %%
   Nosotros dibujabamos las 364 en tinta plena. Una reja negra debajo de cada
   fila es exactamente el aspecto de una planilla, y era mio, no de la
   referencia. Tampoco tienen filas alternadas: eso ya estaba bien sacado.
   El cuerpo de la celda es INTER de 7,875 con interlinea de 11,25. */
td { padding: %(celda_arriba).2fmm %(celda).1fmm 0; vertical-align: top;
     font-size: %(tabla).3fpt; line-height: %(celda_int).3f;
     border-bottom: %(filete).2fpt solid rgba(40, 34, 22, .13); }
tbody td:first-child { color: %(acento)s; font-weight: 600; }
tbody td.destacada { color: %(dato)s; font-weight: 600; }
thead th.destacada { color: %(dato)s; }
th:not(:first-child), td:not(:first-child) { text-align: right; }
th:first-child, td:first-child { text-align: left; }
.tw.texto th, .tw.texto td { text-align: left; }
.etq { font-style: italic; font-size: %(fuente).1fpt;
       font-family: "%(serif)s"; line-height: %(fuente_int).3f;
       margin: %(sep_fig).1fmm 0 0; color: %(tinta)s; opacity: .68;
       text-align: left; hyphens: none; }
.etq .et { opacity: 1; }

/* --------------------------------------------------------------------
   EXHIBITS. Rotulo Inter mayuscula, titulo que dice la conclusion, bajada,
   figura, y fuente al pie en Spectral italico.
   -------------------------------------------------------------------- */
.exh { break-inside: avoid; margin: %(sep).1fmm 0; }
.exh-cab { margin-bottom: %(sep_tit).1fmm; break-after: avoid; }
/* EL ROTULO EN OCRE, no en ladrillo: medido sobre sus paginas 5, 8 y 13, los
   tres dicen #b4863a. En ladrillo competia con el titulo del exhibit, que va
   justo debajo y tambien es ladrillo. */
.exh-rot { font-family: "%(sans)s"; font-size: %(exh_rot).1fpt;
           font-weight: 500; letter-spacing: %(tr_rot).2fpt;
           text-transform: uppercase; color: %(ocre)s;
           margin: 0 0 %(sep_rot).1fmm; text-align: left; }
.exh-tit { font-size: %(exh_tit).1fpt; font-weight: 600;
           line-height: %(exh_tit_int).3f; color: %(acento)s; margin: 0;
           text-align: left; hyphens: none; }
.exh-baj { font-size: %(fuente).1fpt; line-height: %(fuente_int).3f;
           font-style: italic; color: %(gris)s;
           margin: %(sep_fig).1fmm 0 0; text-align: left; hyphens: none; }
/* El PNG ya viene dibujado a los 181,4 mm de la caja, asi que se imprime a
   escala 1: un punto pedido adentro del grafico es un punto en el papel. El
   tope de alto solo esta para que ningun exhibit se coma una pagina entera. */
.exh img { display: block; margin: 0 auto; max-width: 100%%;
           max-height: 122mm; width: auto; height: auto; }
.exh.alto img { max-height: 134mm; }
.exh-fuente, .exh-nota { font-style: italic; font-size: %(fuente).1fpt;
                         line-height: %(fuente_int).3f;
                         margin: %(sep_fig).1fmm 0 0;
                         text-align: left; hyphens: none;
                         color: %(gris)s; }
.exh-nota { color: %(gris)s; margin-top: %(sep_rot).1fmm; }

/* El listado: monoespaciada al ancho de la caja, sobre banda de arena y con
   filete del acento al costado. */
pre.listado { font-family: "DejaVu Sans Mono"; font-size: %(mono).1fpt;
              line-height: 1.42; margin: %(sep).1fmm 0;
              padding: 3mm %(caja_sangria).1fmm;
              background: %(arena)s;
              border-left: %(caja_filete).1fpt solid %(acento)s;
              color: %(tinta)s; white-space: pre; overflow: hidden;
              break-inside: avoid; }

/* --------------------------------------------------------------------
   TAPA
   -------------------------------------------------------------------- */
.tapa { position: relative; width: 210mm; height: 297mm; overflow: hidden;
        page-break-after: always; background: %(crema)s; }
.tapa-img { position: absolute; left: 0; top: 0; width: 210mm; height: 297mm;
            object-fit: cover; }
.tapa-img.cubre { left: 0; top: 0; width: 210mm; height: 297mm;
                  object-fit: cover; }
.tapa-faja { position: absolute; left: 0; top: 0; width: 210mm;
             height: 118mm;
             background: linear-gradient(180deg,
                 rgba(245,240,232,.97) 0%%, rgba(245,240,232,.95) 62%%,
                 rgba(245,240,232,0) 100%%); }
.tapa-credito { position: absolute; left: %(mg).1fmm; bottom: 8mm; margin: 0;
                font-family: "%(sans)s"; font-size: %(pie_pt).1fpt;
                letter-spacing: .3pt; color: %(tinta)s; opacity: .65; }

/* --------------------------------------------------------------------
   LAS ILUSTRACIONES
   --------------------------------------------------------------------
   Las once son verticales, de 3:4. Recortadas a una banda de 4:1 no queda
   nada de la imagen, asi que la apertura de capitulo es una banda ALTA —2,3
   a 1— y las de adentro se recortan a apaisado suave. El pie va en Spectral
   italico gris, el mismo que la fuente de un exhibit: es una nota al pie de
   una pieza, no un rotulo.
   -------------------------------------------------------------------- */
figure.apertura { margin: 0 0 %(sep_caja).1fmm; break-before: page;
                  break-after: avoid; break-inside: avoid; }
/* Con la banda delante, el salto de pagina lo lleva ella y el titulo va
   pegado detras. */
figure.apertura + h1 { break-before: avoid; margin-top: 0; }
figure.apertura img { display: block; width: 100%%; height: 78mm;
                      object-fit: cover; }
figure.apertura figcaption, figure.ilu figcaption {
    font-style: italic; font-size: %(fuente).1fpt;
    line-height: %(fuente_int).3f; color: %(tinta)s; opacity: .68;
    margin-top: %(sep_fig).1fmm; text-align: left; }
figure.apertura + h1 { break-before: avoid; margin-top: 0; }

figure.ilu { margin: %(sep).1fmm 0; break-inside: avoid; }
figure.ilu.sola img { display: block; width: 100%%; height: 76mm;
                      object-fit: cover; }
figure.ilu.cierre img { height: 128mm; }
/* EL PAR ENFRENTADO. Mitad y mitad, separadas por el mismo medianil que las
   columnas: las dos fotos se leen como una sola pieza de comparacion. */
figure.ilu .par { display: flex; gap: %(md).1fmm; }
figure.ilu .par img { display: block; width: 50%%; height: 66mm;
                      object-fit: cover; }
.tapa-txt { position: absolute; left: %(mg).1fmm; top: 22mm;
            width: %(cj).1fmm; }
.tapa h1 { font-size: %(tapa_h1).1fpt; line-height: 1.06; margin: 0;
           letter-spacing: -.4pt; border: 0; padding: 0;
           break-before: avoid; font-weight: 700; color: %(tinta)s; }
.tapa .t2 { color: %(acento)s; margin-bottom: 6mm; }
.tapa .sub { font-size: %(bajada).1fpt; line-height: 1.45; text-align: left;
             max-width: 122mm; margin: 0; hyphens: none; font-style: italic;
             font-weight: 500; color: %(dato)s;
             border-top: %(filete).2fpt solid %(acento)s; padding-top: 3.5mm;
             display: inline-block; }
/* --------------------------------------------------------------------
   INDICE — la anatomia de su pagina de contenidos, medida
   --------------------------------------------------------------------
   Su pagina 2, linea por linea, escalada por 210/232,8:

     titulo de la pagina   Spectral Bold 16,5  EN LADRILLO, no en tinta
     cintillo de grupo     Inter 6,7 mayuscula espaciada, pegado al margen
     numero de seccion     Spectral Regular 8,6, colgando en el margen
     titulo de seccion     Spectral Regular 9,7, a 22 pt del margen
     numero de pagina      Spectral Regular 8,6, alineado a la derecha
     guia                  puntos de 0,75 pt con paso de 1,5
     fila a fila           21,0 pt de alto
     cintillo              6,2 pt mas de aire encima

   Y NINGUNA REGLA HORIZONTAL. Ni bajo el titulo, ni entre entradas, ni
   bajo los capitulos. El indice anterior tenia las tres.
   -------------------------------------------------------------------- */
.indice { break-before: page; }
h1.ix-h { font-size: %(h1).1fpt; color: %(acento)s;
          margin: %(aire_arriba).1fmm 0 %(ix_tit).1fmm; border: 0; }
ul.ix { list-style: none; margin: 0; padding: 0;
        font-variant-numeric: tabular-nums lining-nums; }
ul.ix li { margin: 0; }
ul.ix a { text-decoration: none; color: %(tinta)s; }

/* El capitulo hace de cintillo de grupo: Inter mayuscula espaciada, contra
   el margen, sin numero de pagina y sin filete. */
li.ix-cap { margin-top: %(ix_grupo).1fmm; }
li.ix-cap:first-child { margin-top: 0; }
/* EL CINTILLO VA EN SALVIA, NO EN LADRILLO. Su indice usa CINCO colores en
   una sola pagina: ocre en la cornisa y en los cintillos de grupo, ladrillo
   en el titulo de la pagina, coral en el numero de seccion, tinta en el
   titulo y gris calido en el numero de pagina. Cinco voces distintas, cada
   una para una cosa. El nuestro tenia dos, y el ladrillo hacia tres trabajos
   a la vez. El ocre y el coral no estan en nuestra paleta —y el coral ademas
   es un rojo—, asi que el cintillo toma la otra voz que la paleta si tiene y
   que el documento ya usa para las bajadas: la salvia. */
li.ix-cap a { display: block; font-family: "%(sans)s";
              font-size: %(ix_cintillo).2fpt; font-weight: 400;
              letter-spacing: %(ix_track).2fpt; text-transform: uppercase;
              color: %(ocre)s; line-height: %(ix_fila).3f; }

/* La entrada: numero colgado, titulo, guia de puntos, numero de pagina.
   SIN FLEXBOX. Con la ancla en display:flex, WeasyPrint resuelve
   target-counter antes de colocar los items y todos los numeros de pagina
   salian 0. La guia se dibuja como una linea punteada absoluta que cruza la
   fila entera, y el titulo y el numero de pagina la tapan con un fondo del
   color del papel: es la tecnica de siempre y aca es ademas la unica que
   funciona. */
li.ix-sub { position: relative; }
li.ix-sub a { display: block; padding-left: %(sangria_ix).1fmm;
              font-size: %(ix_entrada).2fpt; line-height: %(ix_alto).3f; }
/* LA GUIA VA POR EL MEDIO DE LA FILA, NO POR ABAJO. Medida sobre su
   pagina 2: los puntos estan en top=126,75 y la caja del titulo va de
   122,29 a 131,99 —o sea el centro exacto de la caja, no la linea de base.
   Puesta en `bottom`, la guia salia por debajo del titulo, el fondo crema
   del titulo no la tapaba, y cada entrada del indice quedaba subrayada.
   Con `top: 50%%` sobre una caja vacia, el borde inferior cae justo en el
   medio de la fila y el titulo y el numero de pagina la cortan. */
li.ix-sub a::before { content: ""; position: absolute;
                      left: %(sangria_ix).1fmm; right: 0; top: 50%%;
                      border-bottom: %(ix_guia).2fpt dotted %(ix_punto)s; }
/* CAJA DE LINEA EXPLICITA. Un elemento absoluto sin `top` se cuelga de su
   posicion estatica POR EL BORDE DE ARRIBA, no por la base; con un cuerpo
   mas chico que el de la entrada, su caja es mas baja y la cifra quedaba
   1,86 pt por encima del titulo. En su indice el numero de seccion, el
   titulo y el numero de pagina comparten base. Fijando la misma altura de
   linea en puntos, las tres bases coinciden salvo 0,35 pt de ascendente. */
span.ix-n { position: absolute; left: 0; color: %(coral)s;
            font-size: %(ix_num).2fpt; line-height: %(ix_caja).2fpt; }
span.ix-t { position: relative; color: %(tinta)s; background: %(crema)s;
            padding-right: 1.6mm; }
li.ix-sub.propuesta span.ix-t { font-weight: 600; color: %(acento)s; }
/* ABSOLUTO, NO FLOTADO. Flotando, el numero de pagina se apoya en el borde
   de arriba de la caja de linea y queda medio punto por encima del titulo;
   en su indice los dos comparten la linea de base. Absoluto a la derecha
   conserva la posicion estatica de la linea, o sea la misma base. */
li.ix-sub a::after { content: target-counter(attr(href), page);
                     position: absolute; right: 0; background: %(crema)s;
                     padding-left: 1.6mm; font-size: %(ix_num).2fpt;
                     line-height: %(ix_caja).2fpt;
                     color: %(gris)s; }

""" % dict(
    crema=CREMA, tinta=TINTA, acento=ACENTO, dato=DATO, arena=ARENA,
    coral=CORAL, gris=GRIS,
    # TABLA Y CAJA, de su hoja de estilos y no ya del PDF medido
    cab_alto=emm(17.25, 2), cab_arriba=emm(4.25, 2),
    celda_arriba=emm(3.5, 2), celda_int=11.25 / 7.875,
    caja_arriba=emm(10.75, 2), caja_abajo=emm(11.0, 2),
    caja_rot_int=e(9.0),
    # el tablero, todo medido sobre su pagina 22
    tb_filete=e(0.7), tb_rot=e(6.4), tb_cifra=e(19.0), tb_nota=e(7.5),
    tb_track=e(6.4) * 0.083,
    tb_aire=emm(7.9, 1), tb_pie=emm(16.0, 1),
    tb_sep1=emm(25.4 - 6.4 * 1.25, 1), tb_sep2=emm(21.2 - 19.0 * 1.05, 1),
    fila=FILA, tan=TAN, ocre=OCRE, corto=TITULO_CORTO, pie=MARGEN_PIE, serif=SERIF,
    sans=SANS, tipos=TIPOS,
    # geometria
    mg=emm(REF["margen"], 1), mgsup=emm(REF["margen"] - 5, 1),
    cj=emm(REF["caja"], 1), md=emm(REF["medianil"], 1),
    col=emm(REF["columna"], 1),
    # cuerpos
    cuerpo=e(REF["cuerpo"]), cuerpo_int=REF["cuerpo_int"] / REF["cuerpo"],
    entrada=e(REF["entrada"]), entrada_int=REF["entrada_int"] / REF["entrada"],
    h1=e(REF["h1"]), h1_int=REF["h1_int"] / REF["h1"],
    bajada=e(REF["bajada"]), bajada_int=REF["bajada_int"] / REF["bajada"],
    h2=e(REF["h2"]), h3=e(REF["h3"]),
    exh_rot=e(REF["exh_rot"]), exh_tit=e(REF["exh_tit"]),
    exh_tit_int=REF["exh_tit_int"] / REF["exh_tit"],
    tabla_cab=e(REF["tabla_cab"]), tabla=e(REF["tabla"]),
    tabla_chica=e(REF["tabla"] - 0.5),
    tabla_int=REF["tabla_int"] / REF["tabla"],
    fuente=e(REF["fuente"]), fuente_int=REF["fuente_int"] / REF["fuente"],
    cornisa=e(REF["cornisa"]), pie_pt=e(REF["pie"]),
    mono=e(REF["tabla"]), dato_pt=e(REF["exh_tit"]), tapa_h1=e(44.0),
    caja_cuerpo=e(REF["caja_cuerpo"]),
    caja_int=REF["caja_int"] / REF["caja_cuerpo"],
    caja_rot=e(REF["caja_rot"]), caja_filete=e(REF["caja_filete"]),
    filete=e(REF["filete"]),
    # INTERLETRADO, DESPEJADO CONTRA EL ARCHIVO DE LA FUENTE.
    # Restarle "el lateral natural" al hueco entre glifos era una cuenta
    # inventada y daba la mitad. Lo correcto es medir el ancho impreso de
    # cada palabra, calcular con Inter[wght=400] el ancho que esa palabra
    # tendria sin interletrado, y despejar:  ls = (impreso - natural)/(n-1).
    # Sobre las 30 paginas, por oficio de cada rotulo (en em, o sea que no
    # hay que escalarlo: es proporcion, no medida):
    #     cornisa fija        0,218 em   (145 palabras)
    #     cintillo de indice  0,174 em   ( 15)
    #     rotulo de exhibit   0,153 em   ( 80)
    #     rotulo de caja      0,134 em   ( 84)
    #     cabecera de tabla   0,075 em   (151)
    #     pie de pagina       0,039 em   (164)
    # La cabecera de tabla casi no lleva y la cornisa lleva el triple: no es
    # un valor unico repartido, es una escala de enfasis.
    tr_rot=e(REF["exh_rot"]) * 0.153,
    tr_tabla=e(REF["tabla_cab"]) * 0.050,
    tr_caja=e(REF["caja_rot"]) * 0.120,
    tr_pie=e(REF["pie"]) * 0.039,
    # separaciones
    sep=emm(REF["sep_bloque"], 1),
    sep_rot=emm(REF["sep_rot_tit"], 1),
    sep_tit=emm(REF["sep_tit_fig"], 1),
    sep_fig=emm(REF["sep_fig_fuente"], 1),
    sep_fuente=emm(REF["sep_fuente_cuerpo"], 1),
    sep_h1_bajada=emm(REF["sep_h1_bajada"], 1),
    sep_bajada=emm(REF["sep_bajada_entrada"], 1),
    sep_cornisa=emm(REF["sep_cornisa_h1"] - 12, 1),
    sep_h2=emm(REF["sep_bloque"] * 1.6, 1),
    sep_h2b=emm(REF["sep_bloque"] * 0.5, 1),
    sep_h3=emm(REF["sep_bloque"] * 1.2, 1),
    sep_h3b=emm(REF["sep_bloque"] * 0.45, 1),
    sep_caja=emm(REF["sep_bloque"] * 1.3, 1),
    sep_caja_rot=emm(17.0 - 8.3, 1),
    caja_sangria=emm(REF["caja_sangria"], 1),
    caja_alto=emm(REF["caja_alto"], 1),
    # En su pagina de contenidos el numero va en x=45 y el nombre en x=67.
    # 72,1 - 38,3 - la caja de linea de la cornisa (8,7) = 25,1 pt
    aire_arriba=emm(25.1, 1),
    sangria_ix=emm(22.0, 1),
    # Medido sobre sus veinticinco entradas, no sobre dos: el paso entre
    # entradas es 21,70 pt —no 21,0—, el cintillo se lleva 27,65 desde la
    # entrada anterior y devuelve 21,70 a la siguiente, y del titulo de la
    # pagina al primer cintillo hay 28,5. Estaba en 18,90 de paso cuando le
    # corresponden 19,57: un 3,4 % apretado, que en cuarenta filas se ve.
    ix_tit=emm(28.5, 1) - e(16.5) * 1.18 / 72 * 25.4,   # menos su caja de linea
    ix_grupo=emm(27.65 - 21.7, 1),     # aire de mas encima de un cintillo
    ix_cintillo=e(6.7), ix_entrada=e(9.7), ix_num=e(8.6),
    ix_track=e(6.7) * 0.174,
    li_sangria=emm(23.2, 2), li_aire=emm(11.2, 2), li_marca=e(10.5),
    li_bolo=e(9.6),
    li_linea=e(REF['cuerpo']) * (REF['cuerpo_int'] / REF['cuerpo']),
    ix_caja=e(21.7),                   # la fila entera, en puntos
    ix_guia=e(0.75),                   # punto de 0,75 con paso de 1,5
    ix_punto='rgba(180, 134, 58, .62)',  # ocre al 62 %% = #CDAE7C
    ix_fila=21.7 / 6.7,                # el cintillo ocupa una fila entera
    ix_alto=21.7 / 9.7,                # 21,7 pt de fila, como los suyos
    celda=emm(REF["celda"], 1),
    celda_v=emm((17.2 - REF["tabla_cab"] * 1.25) / 2, 1),
    celda_v2=emm((REF["banda_fila"] - REF["tabla_int"]) / 2, 1),
)


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
    paleta = [_hex_a_rgb(c) for c in (ACENTO, DATO, DATO_CLARO, OCRE, ARENA, FILA)]
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

    instalar_tipografias()
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
                '<title>%s</title></head><body>'
                '<div class="filete-pie"></div>%s</body></html>'
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
