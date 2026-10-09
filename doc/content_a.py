# -*- coding: utf-8 -*-
"""Contenido del programa. El texto es el del PDF anterior, sin cambios de
fondo; lo que cambia es como esta puesto en pagina."""

DOC_TITLE = "Programa de gobierno &middot; San Isidro 2027"
RH = "PROGRAMA DE GOBIERNO &middot; PARTIDO DE SAN ISIDRO"

# numeros de pagina del indice; se completan despues de la primera pasada
PAGES = {}
def pg(k):
    return PAGES.get(k, "&mdash;")

_n = [0]
def exn():
    _n[0] += 1
    return _n[0]

# referencias a exhibits por clave: el texto escribe [[n:clave]] y el armado
# pone el numero que le toco al exhibit, asi una renumeracion no rompe nada
_REFS = {}

def resolver_refs(html):
    import re
    return re.sub(r"\[\[n:([a-z0-9_]+)\]\]", lambda m: str(_REFS[m.group(1)]), html)

def ex(kind, title, sub=None, img=None, src=None, note=None, cls="", key=None):
    """Bloque de exhibit: etiqueta numerada, titulo-conclusion, grafico y fuente."""
    k = exn()
    if key: _REFS[key] = k
    lbl = "GR&Aacute;FICO" if kind == "g" else "CUADRO"
    h = [f'<div class="ex"><div class="exlabel">{lbl}&nbsp;{k}</div>',
         f'<div class="extitle">{title}</div>']
    if sub:  h.append(f'<div class="exsub">{sub}</div>')
    if img:  h.append(f'<div class="chart {cls}"><img src="asset:{img}" alt=""></div>')
    if src:  h.append(f'<p class="cap"><b>Fuente:</b> {src}</p>')
    if note: h.append(f'<p class="cap"><b>Nota:</b> {note}</p>')
    h.append('</div>')
    return "".join(h)

def exhead(kind, title, sub=None, key=None):
    k = exn()
    if key: _REFS[key] = k
    lbl = "GR&Aacute;FICO" if kind == "g" else "CUADRO"
    s = f'<div class="exsub">{sub}</div>' if sub else ""
    return (f'<div class="ex"><div class="exlabel">{lbl}&nbsp;{k}</div>'
            f'<div class="extitle">{title}</div>{s}</div>')

def fig(img, cap, pos=None):
    if "." not in img: img += ".jpg"
    st = f' style="object-position:center {pos}"' if pos else ""
    return f'<figure><img src="asset:{img}" alt=""{st}><figcaption>{cap}</figcaption></figure>'

def duo(a, b, cap):
    a = a if "." in a else a+".jpg"
    b = b if "." in b else b+".jpg"
    return (f'<div class="duo"><figure><img src="asset:{a}" alt=""></figure>'
            f'<figure><img src="asset:{b}" alt=""></figure></div>'
            f'<figcaption style="margin-top:4.6pt">{cap}</figcaption>')


# =====================================================================
# INDICE
# =====================================================================
_IDX = [
 ("g", "Introducci&oacute;n", None),
 ("i", "La pregunta", "introduccion"),
 ("i", "Por qu&eacute; el dinero va a lo que se ve", "introduccion"),
 ("g", "Qu&eacute; proponemos hacer", None),
 ("i", "Nueve puntos, y los primeros cien d&iacute;as", "sintesis"),
 ("g", "1 &middot; Diagn&oacute;stico", None),
 ("i", "1.1 &nbsp;Un partido dividido en dos", "cap1a"),
 ("i", "1.2 &nbsp;El Municipio invierte m&aacute;s que casi todos. Pero el dinero no llega adonde hace falta.", "cap1a2"),
 ("i", "1.3 &nbsp;D&oacute;nde no va el dinero", "cap1a2"),
 ("i", "1.4 &nbsp;Por qu&eacute; pasa esto: lo dice el plan de gobierno", "cap1b"),
 ("i", "1.5 &nbsp;San Isidro se financia solo. Eso cambia todo.", "cap1b"),
 ("i", "1.6 &nbsp;Lo que dice este cap&iacute;tulo, en cinco puntos", "cap1b"),
 ("g", "2 &middot; La gesti&oacute;n, medida", None),
 ("i", "2.1 &nbsp;Gastar el presupuesto no es prestar el servicio", "cap2"),
 ("i", "2.2 &nbsp;Lo que se prometi&oacute; publicar y no est&aacute; publicado", "cap2b"),
 ("i", "2.3 &nbsp;El hallazgo central: el plan no nombra el empleo, la vivienda ni la salud", "cap2b"),
 ("i", "2.4 &nbsp;Lo que dice este cap&iacute;tulo, en cinco puntos", "cap2b"),
 ("g", "3 &middot; Los fondos", None),
 ("i", "3.1 &nbsp;La trampa contable que casi nos hace decir lo contrario", "cap3a"),
 ("i", "3.2 &nbsp;Los cuatro n&uacute;meros que deciden el futuro de las cuentas de San Isidro", "cap3a"),
 ("i", "3.3 &nbsp;C&oacute;mo quedan las cuentas si nadie cambia nada", "cap3a"),
 ("i", "3.4 &nbsp;Cu&aacute;nto cuesta este programa", "cap3b"),
 ("i", "3.5 &nbsp;De d&oacute;nde salen los fondos", "cap3b2"),
 ("i", "3.6 &nbsp;Qu&eacute; habr&iacute;a que vigilar", "cap3b3"),
 ("i", "3.7 &nbsp;Lo que dice este cap&iacute;tulo, en ocho puntos", "cap3b3"),
 ("g", "4 &middot; El mecanismo", None),
 ("i", "4.1 &nbsp;El l&iacute;mite legal: lo que un intendente bonaerense no puede delegar", "cap4a"),
 ("i", "4.2 &nbsp;La deuda que la Provincia tiene con sus municipios", "cap4a"),
 ("i", "4.3 &nbsp;Cu&aacute;nto dinero: el n&uacute;mero", "cap4a"),
 ("i", "4.4 &nbsp;C&oacute;mo se reparte: por poblaci&oacute;n y por necesidad contada", "cap4a2"),
 ("i", "4.5 &nbsp;Qui&eacute;n decide y qui&eacute;n ejecuta: dos capas", "cap4b"),
 ("i", "4.6 &nbsp;C&oacute;mo se forma una comisi&oacute;n, y c&oacute;mo rinde cuentas", "cap4b"),
 ("i", "4.7 &nbsp;El Concejo Deliberante: diez bloques y ninguna mayor&iacute;a", "cap4bb2"),
 ("i", "4.8 &nbsp;Por qu&eacute; las dos capas juntas cambian todo", "cap4bb2"),
 ("i", "4.9 &nbsp;Las otras dos piezas del mecanismo", "cap4b2"),
 ("i", "4.10 &nbsp;El primer acto de gobierno: derogar tres art&iacute;culos", "cap4b2"),
 ("i", "4.11 &nbsp;La inteligencia artificial del Municipio", "cap4b2"),
 ("i", "4.12 &nbsp;A qui&eacute;n le molesta esto", "cap4bc"),
 ("i", "4.13 &nbsp;Lo que dice este cap&iacute;tulo, en doce puntos", "cap4bc"),
 ("g", "5 &middot; Qu&eacute; hacemos en cada &aacute;rea", None),
 ("i", "5.1 &nbsp;C&oacute;mo leer este cap&iacute;tulo", "cap5a"),
 ("i", "5.2 &nbsp;D&oacute;nde va hoy cada peso", "cap5a"),
 ("i", "5.3 &nbsp;Empleo", "cap5a2"),
 ("i", "5.4 &nbsp;Vivienda y servicios b&aacute;sicos", "cap5a4"),
 ("i", "5.5 &nbsp;Ambiente", "cap5b"),
 ("i", "5.6 &nbsp;Salud", "cap5bb"),
 ("i", "5.7 &nbsp;Seguridad", "cap5bc"),
 ("i", "5.8 &nbsp;Educaci&oacute;n y cultura", "cap5b2"),
 ("i", "5.9 &nbsp;Digitalizaci&oacute;n: que el tr&aacute;mite tarde diez segundos", "cap5b2a2"),
 ("i", "5.10 &nbsp;Transparencia", "cap5b2b"),
 ("i", "5.11 &nbsp;Transporte y comercio", "cap5b2b"),
 ("i", "5.12 &nbsp;Los que tienen que ejecutar todo esto", "cap5b2c"),
 ("i", "5.13 &nbsp;Ni&ntilde;ez, personas mayores, g&eacute;nero y discapacidad", "cap5b3"),
 ("i", "5.14 &nbsp;Lo que no est&aacute; en este cap&iacute;tulo, y por qu&eacute;", "cap5b3b"),
 ("i", "5.15 &nbsp;Lo que dice este cap&iacute;tulo, en veinte puntos", "cap5b3b"),
 ("g", "6 &middot; El plan, con fechas", None),
 ("i", "6.1 &nbsp;Los primeros cien d&iacute;as", "cap6"),
 ("i", "6.2 &nbsp;La rampa de la obra vecinal, a&ntilde;o por a&ntilde;o", "cap6"),
 ("i", "6.3 &nbsp;Las metas verificables del mandato", "cap6b"),
 ("i", "6.4 &nbsp;El calendario del mandato, mes por mes", "cap6b2"),
 ("i", "6.5 &nbsp;Qu&eacute; no prometemos, y de qui&eacute;n depende", "cap6b2"),
 ("i", "6.6 &nbsp;Qu&eacute; puede salir mal", "cap6c"),
 ("i", "6.7 &nbsp;Lo que dice este cap&iacute;tulo, en seis puntos", "cap6c"),
 ("g", "Cierre", None),
 ("i", "Para cerrar", "cierre"),
 ("g", "Anexo &middot; El articulado", None),
 ("i", "La partida vecinal, el sistema de informaci&oacute;n y la base de valuaci&oacute;n", "ordenanza"),
 ("i", "La fiscalizaci&oacute;n, las asociaciones de parque, g&eacute;nero y los espacios culturales", "ordenanza2"),
 ("i", "El ruido, la higiene urbana y el empleo local", "ordenanza3"),
 ("i", "La costa, la obra en parques y costa, las excepciones urban&iacute;sticas, los parques y las cuotas de las multas; y las metas que no llevan ordenanza", "ordenanza4"),
 ("g", "Glosario", None),
 ("i", "Treinta y dos palabras, explicadas", "glosario"),
 ("g", "Nota de m&eacute;todo", None),
 ("i", "C&oacute;mo est&aacute; construido, y qu&eacute; l&iacute;mites tiene", "metodo"),
 ("i", "Las notas de cada cap&iacute;tulo", "metodo"),
 ("i", "Las fuentes de lo que afirma el texto", "fuentes"),
]

def _indice():
    rows = []
    for kind, txt, key in _IDX:
        if kind == "g":
            rows.append(f'<div class="igrp">{txt}</div>')
        else:
            rows.append('<div class="irow"><span class="it">%s</span>'
                        '<span class="ilead"></span>'
                        '<span class="ipg">%s</span></div>' % (txt, pg(key)))
    style = """<style>
      .igrp{margin-top:17pt;font-family:'Inter',sans-serif;font-weight:600;font-size:6.7pt;
        letter-spacing:1.02pt;text-transform:uppercase;color:var(--amber)}
      .irow{display:flex;align-items:baseline;margin-top:6.6pt}
      .irow .it{font-family:'Spectral',serif;font-size:9.7pt;color:var(--ink)}
      .irow .ilead{flex:1 1 auto;border-bottom:.75pt dotted var(--rule);margin:0 6pt}
      .irow .ipg{font-family:'Spectral',serif;font-size:8.6pt;color:var(--taupe)}
    </style>"""
    # Dispatch 11, punto 1: la fecha de actualizacion sale del indice; queda en la nota de metodo.
    return style + '<h1>&Iacute;ndice</h1>' + "".join(rows)


INDICE = dict(id="indice", runhead=RH, html=_indice())


# =====================================================================
# INTRODUCCION
# =====================================================================
INTRO = dict(id="introduccion", runhead=RH, html="""
<h1>Introducci&oacute;n</h1>
<p class="lead">En San Isidro hay <b>25.165 hogares sin gas de red</b> y 6.488 que no tienen
cloaca. La mayor&iacute;a est&aacute; en Boulogne y en B&eacute;ccar. Ah&iacute; est&aacute;n seis de cada diez hogares sin gas y siete de cada diez sin cloaca.</p>

<h2>La pregunta</h2>
<p>El plan de gobierno del intendente se llama &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo;. En el pr&oacute;logo, escribe: &laquo;Estas prioridades de gesti&oacute;n no las fijamos nosotros, sino que
responden a haber escuchado sus principales problemas y necesidades&raquo;. <b>&iquest;A qui&eacute;n escucharon, y c&oacute;mo, si el empleo y la vivienda no aparecen nunca en el plan?</b></p>
<div class="pull"><p>Las palabras empleo, vivienda, salud, pobreza, agua y cloaca no aparecen en ninguna
parte del plan de gobierno 2024&ndash;2025.</p></div>

<h2>Por qu&eacute; el dinero va a lo que se ve</h2>
<p class="lead">Hay dos maneras de manejar un municipio pensando en la pr&oacute;xima elecci&oacute;n. Ninguna de las dos es gobernar.</p>
<div class="cols">
<p><b>La primera es administrar para la foto.</b> Se elige la obra que se ve: la que se termina antes del fin del mandato y se inaugura cortando una cinta. Nadie tiene que actuar de mala fe para que esto pase. Alcanza con que se elija con ese criterio. <span class="sg">El alumbrado p&uacute;blico recibe 10.313 millones de pesos por a&ntilde;o. El agua y las cloacas reciben 3.320 millones.</span> Una cloaca no se inaugura con una cinta.</p>
<p><b>La segunda es repartir.</b> Es la manera de los gobiernos populistas. Mantienen los votos repartiendo cosas. El que reparte necesita que el otro siga necesitando. <b>Este programa no da un peso sin trabajo a cambio. La &uacute;nica beca que tiene paga una pr&aacute;ctica de trabajo.</b> Los 7.730,9 millones de pesos para empleo y vivienda pagan formaci&oacute;n, contrataci&oacute;n de personas y obras.</p>
<p><b>Hay una tercera manera, que es la de este programa: administrar para que el partido crezca.</b> Queremos que San Isidro funcione mejor al final del mandato que al principio. Eso quiere decir <b>menos hogares sin cloaca y sin gas de red</b>. Quiere decir <b>m&aacute;s gente formada y con trabajo</b>. Tambi&eacute;n quiere decir <b>que los vecinos decidan en qu&eacute; se gasta la obra de su barrio</b>. Ninguna de esas tres cosas da una foto el d&iacute;a en que se hace.</p>
<p><b>Somos una propuesta de gobierno que gestiona.</b> Queremos administrar para que San Isidro crezca, y <span class="sg">ese crecimiento econ&oacute;mico es de todos</span>. Por eso el cap&iacute;tulo 4 no pide
un peso nuevo. La mitad de la obra p&uacute;blica que hoy hace el Municipio
<span class="sg">la van a decidir los vecinos de cada barrio</span>.</p>
</div>
""" + fig("f_costanera", "La costanera de San Isidro. Ilustraci&oacute;n."))
# Correccion 132: la firma de Casares (nombre y cargo) sale hasta que el
# candidato lea y apruebe el documento. Para reponerla, despues del </div> de
# las columnas va:
# <p style="margin-top:14pt;font-style:italic;color:var(--taupe);font-size:9pt">Jos&eacute; Luis Casares,
# candidato a intendente de San Isidro.</p>


# =====================================================================
# CAPITULO 1 — parte A
# =====================================================================
C1A = dict(id="cap1a", runhead=RH, html=fig("f_catedral",
    "El casco hist&oacute;rico. Ilustraci&oacute;n.") + """
<h1><span class="n">1</span>Diagn&oacute;stico</h1>
<div class="stand">San Isidro invierte en obra p&uacute;blica m&aacute;s que el 96% de los municipios de la provincia de Buenos Aires. Pero a empleo destina s&oacute;lo el 0,05% de su presupuesto.</div>

<h2><span class="n">1.1</span>Un partido dividido en dos</h2>
<div class="cols">
<p>San Isidro tiene 297.282 habitantes y 110.559 hogares, seg&uacute;n el Censo 2022. En 2025, el Municipio gast&oacute; el equivalente a <b>1.090.897 pesos por habitante</b>. No es poco dinero.</p>
<p>Sin embargo, el partido est&aacute; dividido en dos, y la divisi&oacute;n es geogr&aacute;fica. De un lado quedan las localidades del oeste y del norte. Del otro, las de la costa sur.</p>
<p>Un hogar de Boulogne o de B&eacute;ccar tiene <span class="sg">tres veces y media m&aacute;s probabilidad</span> de tener necesidades b&aacute;sicas insatisfechas que uno de Mart&iacute;nez. Tiene <span class="sg">cinco veces y media</span> m&aacute;s probabilidad de no tener cloaca. Tiene <span class="sg">cuatro veces</span> m&aacute;s probabilidad de vivir hacinado, con demasiada gente por cuarto. La gente con la universidad terminada es <span class="sg">menos de la mitad</span> que en Mart&iacute;nez.</p>
</div>
""" + ex("g", "San Isidro est&aacute; dividido en dos: de un lado el oeste y el norte, del otro la costa sur",
        "Cada localidad tiene el color de su porcentaje de hogares con necesidades b&aacute;sicas insatisfechas. En todo el partido, el promedio es 3,16%.",
        "ex01.png",
        "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7; l&iacute;mites de localidad de OpenStreetMap.",
        "OpenStreetMap no es una fuente oficial. Cada radio censal se cont&oacute; en la localidad donde est&aacute; su punto representativo, un punto que siempre cae dentro del radio. Cada uno de los 360 radios cae dentro de una sola localidad.")
+ ex("g", "Boulogne y B&eacute;ccar re&uacute;nen dos tercios de las carencias del partido",
     "Porcentaje de hogares de cada zona con cada una de las cuatro carencias de la leyenda. Debajo de cada zona, cu&aacute;ntos habitantes tiene. En todo el partido, el 3,16% de los hogares tiene necesidades b&aacute;sicas insatisfechas (NBI).",
     "ex02.png",
     "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7.")
+ ex("g", "Donde m&aacute;s faltan servicios, menos gente termin&oacute; la universidad: 9% en Boulogne, 32% en Acassuso",
     "Porcentaje de personas con la universidad terminada en cada zona. Las zonas est&aacute;n ordenadas seg&uacute;n cu&aacute;ntos hogares tienen necesidades b&aacute;sicas insatisfechas: primero la que m&aacute;s tiene, al final la que menos.",
     "ex03.png",
     "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7.") + """
<h3>El dato que resume todo</h3>
<p class="tight">En Boulogne Sur Mer y en B&eacute;ccar viven <b>138.551 personas, en 47.193 hogares. Son el 46,8% de la gente del partido.</b></p>
<p class="cap"><b>Nota:</b> el 46,8% se calcula sobre las 295.978 personas que viven en viviendas particulares. Esa es la base de todos los datos por zona. Las otras 1.304 personas viven en viviendas colectivas. Si se cuentan los 297.282 habitantes, es el 46,6%.</p>
<div class="pull"><p>Casi la mitad de la gente de San Isidro vive en esas dos localidades. Ah&iacute; est&aacute; el 60% de los 25.165 hogares sin gas de red, y el 71% de los 6.488 hogares que no tienen cloaca.</p></div>
""" + duo("f_boulogne", "f_martinez",
          "Boulogne Sur Mer y Mart&iacute;nez pagan la misma tasa municipal, pero no tienen los mismos servicios. Ilustraci&oacute;n.") + """

<h2><span class="n">1.2</span>El Municipio invierte m&aacute;s que casi todos. Pero el dinero no llega adonde hace falta.</h2>
<div class="cols">
<p><b>El dato.</b> Hay 106 municipios de la provincia con datos de lo que gastaron en 2025. Entre ellos, San Isidro es <b>el cuarto que m&aacute;s invierte en obra p&uacute;blica</b>. Pone en obra el <b>17,8%</b> de su gasto. El municipio t&iacute;pico de la provincia, el que queda en el medio de la lista, pone el <b>5,4%</b>. San Isidro invierte m&aacute;s del triple.</p>
<p><b>Ah&iacute; aparece la pregunta.</b> Si invierte tanto, &iquest;por qu&eacute; todav&iacute;a hay 6.488 hogares sin cloaca? No es porque falte dinero. Es porque <span class="sg">el dinero va a lo que se ve</span>.</p>
</div>
""" + exhead("c", "San Isidro pone en obra p&uacute;blica el 17,8% de su gasto, m&aacute;s que los municipios vecinos",
             "Lo que gast&oacute; cada municipio en 2025 y qu&eacute; parte fue a obra p&uacute;blica. Est&aacute;n San Isidro, los cuatro municipios que lo rodean y el municipio t&iacute;pico de la provincia.") + """
<table>
<colgroup><col style="width:190pt"><col><col></colgroup>
<tr class="hd"><th>Municipio</th><th class="r">Total gastado en 2025 (millones de pesos)</th>
<th class="r">Parte que fue a obra p&uacute;blica (%)</th></tr>
<tr class="hi"><td class="l">San Isidro</td><td class="n">324.304</td><td class="n"><b>17,8</b></td></tr>
<tr><td class="l">Vicente L&oacute;pez</td><td class="n">318.824</td><td class="n">7,4</td></tr>
<tr><td class="l">Tigre</td><td class="n">400.156</td><td class="n">11,4</td></tr>
<tr><td class="l">San Fernando</td><td class="n">148.932</td><td class="n">6,9</td></tr>
<tr><td class="l">San Mart&iacute;n</td><td class="n">276.003</td><td class="n">1,5</td></tr>
<tr><td class="m">Municipio t&iacute;pico de la provincia (mediana)</td><td class="n m">&mdash;</td><td class="n m">5,4</td></tr>
</table>
<p class="cap"><b>Fuente:</b> RAFAM 2025, v&iacute;a La Verdadera PBA. El dato de San Isidro se compar&oacute; con lo que publica el propio Municipio. Los de los otros 105 municipios, no.</p>

<div class="cols">
<p><b>Adem&aacute;s, ese porcentaje alto se aplica sobre un gasto total que viene bajando.</b> El gasto real del Municipio, es decir, descontada la inflaci&oacute;n, tuvo su m&aacute;ximo en 2017. <b>Desde ese a&ntilde;o cay&oacute; 24,4%.</b> Comparado con 2010, igual est&aacute; 13,1% m&aacute;s alto.</p>
<p><b>La ca&iacute;da empez&oacute; despu&eacute;s de 2017.</b> Entre 2010 y 2017, el gasto real subi&oacute; 49,6%. Entre 2017 y 2022 baj&oacute; 17,2%. Entre 2022 y 2025 baj&oacute; otro 8,8%. El peor momento fue de 2022 a 2024, cuando cay&oacute; 21,4%. En 2025 recuper&oacute; una parte: subi&oacute; 16,0%. <b>Desde 2017, ninguna gesti&oacute;n volvi&oacute; a ese nivel de gasto.</b> Ese es el l&iacute;mite con el que hay que trabajar.</p>
</div>

<h3>En qu&eacute; se invierte: la pregunta que falta hacer</h3>
""" + exhead("c", "El alumbrado p&uacute;blico recibe el triple que el agua y las cloacas",
             "Lo que gast&oacute; el Municipio en 2025 en cada servicio urbano, y en agua y cloacas.") + """
<table>
<colgroup><col style="width:300pt"><col></colgroup>
<tr class="hd"><th>En qu&eacute; se gast&oacute;</th><th class="r">Gastado en 2025</th></tr>
<tr><td class="l">Recolecci&oacute;n de residuos, barrido y limpieza</td><td class="n">49.270 M</td></tr>
<tr class="hi"><td class="l">Alumbrado p&uacute;blico</td><td class="n"><b>10.313 M</b></td></tr>
<tr><td class="l">Otros servicios urbanos</td><td class="n">5.829 M</td></tr>
<tr><td class="l">Planeamiento y desarrollo urbano</td><td class="n">4.054 M</td></tr>
<tr><td class="l">Cementerios</td><td class="n">845 M</td></tr>
<tr class="hi"><td class="l">Agua potable y alcantarillado</td><td class="n"><b>3.320 M</b></td></tr>
</table>
<p class="cap"><b>Fuente:</b> Municipio de San Isidro, Estado de Ejecuci&oacute;n de Gastos por Finalidad
y Funci&oacute;n, ejercicio 2025. Subfunciones 3.9.1 a 3.9.9 y funci&oacute;n 3.8.</p>
<p class="cap"><b>Nota:</b> los gastos est&aacute;n agrupados seg&uacute;n para qu&eacute; se usan, no seg&uacute;n qu&eacute; se compra. Por eso, dentro de cada rengl&oacute;n hay sueldos, contratos de servicio y obras. Los 49.270 millones de residuos son, sobre todo, el contrato de recolecci&oacute;n. Es un servicio de todos los d&iacute;as, no una inversi&oacute;n. Los renglones son los que usa la Provincia para clasificar el gasto de los municipios (RAFAM).</p>
<h3>La mitad de lo adjudicado iba a empresas de afuera del partido</h3>
<div class="cols">
<p>Durante quince a&ntilde;os, el Municipio public&oacute; un dato que hoy ya no publica. Es el domicilio de la empresa que gana una obra, un servicio o una compra. Entre 2002 y 2017 hubo 3.013 adjudicaciones con el domicilio publicado. <b>El 49,8% fue a empresas con domicilio en San Isidro. El 50,2% fue a empresas de afuera.</b> La parte de las empresas del partido ven&iacute;a bajando. Fue el 52,6% en 2013, el 46,6% en 2015 y <b>el 40,4% en 2017</b>.</p>
<p>Entre 2011 y 2017, el domicilio aparec&iacute;a en el 62% al 82% de las adjudicaciones. <b>Se dej&oacute; de publicar en 2018, durante la gesti&oacute;n anterior. La gesti&oacute;n actual no lo volvi&oacute; a publicar.</b> Desde diciembre de 2023 se publicaron 573 decretos de adjudicaci&oacute;n. <span class="sg">Ninguno dice d&oacute;nde est&aacute; la empresa que cobra</span>.</p>
</div>

<h3>En cu&aacute;ntas manos queda lo adjudicado</h3>
<div class="cols">
<p>Hay 407 decretos que nombran a cada empresa y lo que cobra. Suman 116.343 millones de pesos, sin ajustar por inflaci&oacute;n, repartidos entre 236 proveedores. <b>Los diez que m&aacute;s recibieron se llevan el 54,5%. Los veinticinco que m&aacute;s recibieron se llevan el 78,6%</b>.</p>
<p><b>Cuatro de esos diez est&aacute;n en la lista por una sola adjudicaci&oacute;n.</b> La m&aacute;s grande de todas es un contrato de seguridad y vigilancia. Ese contrato, por s&iacute; solo, es el <b>11,6% de todo lo adjudicado</b> en dos a&ntilde;os y medio. Otro decreto, de septiembre de 2024, es para calles y veredas. Compromete 20.916 millones en un solo acto.</p>
</div>


""" + ex("g", "San Isidro invierte en obra m&aacute;s del triple que el municipio t&iacute;pico de la provincia",
     "Qu&eacute; parte de su gasto de 2025 puso en obra p&uacute;blica cada municipio de la provincia. Cada marca es un municipio.",
     "ex04.png",
     "RAFAM 2025, v&iacute;a La Verdadera PBA (la-verdadera-pba.pages.dev), capturado el 3 de septiembre de 2026.",
     "Son 106 de los 135 municipios de la provincia. Los otros 29 no est&aacute;n en la planilla, y no se estim&oacute; ninguno.") + """
<h2><span class="n">1.3</span>D&oacute;nde no va el dinero</h2>
<p class="tight">Esto es lo que se gast&oacute; en 2025 en empleo y en vivienda. El gasto total del Municipio ese a&ntilde;o fue de 324.304 millones de pesos.</p>
""" + exhead("c", "Empleo y vivienda: 0,05% y 0,10% del gasto del Municipio",
             "Lo que se gast&oacute; en 2025 en los dos programas, en total y por habitante.", key="dos_partidas") + """
<table>
<colgroup><col style="width:200pt"><col><col><col></colgroup>
<tr class="hd"><th>Programa</th><th class="r">Gastado</th><th class="r">% del gasto total</th>
<th class="r">Por habitante</th></tr>
<tr><td class="l">Apoyo y Promoci&oacute;n al Empleo</td><td class="n">170 M$</td><td class="n"><b>0,05%</b></td><td class="n"><b>572 $/a&ntilde;o</b></td></tr>
<tr><td class="l">Infraestructura Habitacional</td><td class="n">335 M$</td><td class="n"><b>0,10%</b></td><td class="n"><b>1.127 $/a&ntilde;o</b></td></tr>
</table>
<p class="cap"><b>Fuente:</b> Estado de Situaci&oacute;n Econ&oacute;mico-Financiera 2025, gastos por
programa.</p>
""")


# =====================================================================
# CAPITULO 1 — parte B
# =====================================================================
C1B = dict(id="cap1b", runhead=RH, html="""
<h2><span class="n">1.4</span>Por qu&eacute; pasa esto: lo dice el plan de gobierno</h2>
<p>El plan de gobierno 2024&ndash;2025 se llama &laquo;Prioridades Estrat&eacute;gicas&raquo;. Fija tres prioridades. La primera es Seguridad Ciudadana. La segunda, Espacio P&uacute;blico y Ambiente. La tercera, Innovaci&oacute;n. El gasto en seguridad interna, que corresponde a la primera prioridad, <b>subi&oacute; 34,8% en un a&ntilde;o, descontada la inflaci&oacute;n</b>. Ning&uacute;n otro gasto creci&oacute; tanto, salvo los pagos de la deuda. El gasto en promoci&oacute;n y asistencia social no est&aacute; entre las tres prioridades. Ese gasto <b>cay&oacute; 32,5%</b>.</p>

<h2><span class="n">1.5</span>San Isidro se financia solo. Eso cambia todo.</h2>
<div class="cols">
<p>En 2025, el Municipio recibi&oacute; 82.268 millones de pesos de la Provincia de Buenos Aires. Ese a&ntilde;o gast&oacute; 324.304 millones en total.</p>
<p><b>Hoy, el 64% de lo que gasta el Municipio sale de lo que recauda &eacute;l mismo, y esa parte viene creciendo.</b> Desde 2010, lo que recauda el propio Municipio <b>aument&oacute; 33,6%, descontada la inflaci&oacute;n</b>. Es un 1,95% por a&ntilde;o, el mismo n&uacute;mero que usa el modelo del cap&iacute;tulo 3. Mientras tanto, lo que manda la Provincia bajaba. Hoy San Isidro depende menos de la Provincia que hace quince a&ntilde;os. No fue una decisi&oacute;n de nadie: sali&oacute; as&iacute; por los n&uacute;meros.</p>
<p>Esto tiene una consecuencia pol&iacute;tica directa: <span class="sg">un intendente de San Isidro no depende del gobierno de la Provincia, en La Plata.</span> La mayor parte del presupuesto se decide ac&aacute;. La aprueba el Concejo Deliberante, por ordenanza. Adem&aacute;s, el propio Municipio puede pasar dinero de un gasto a otro.</p>
<p>Todo lo que este programa propone puede financiarse sin pedirle permiso a nadie.</p>
</div>
<div class="pull"><p>La Provincia paga el 25% del gasto de San Isidro. Lo que recauda el propio Municipio
paga el 64%.</p></div>
<p>Hay una salvedad, y es de fondo. La Provincia reparte entre los municipios una parte de lo que recauda. La parte que le toca a San Isidro baj&oacute; de 1,938% en 2021 a 1,773% en 2025. Es una ca&iacute;da de 8,5%, y se acumula a&ntilde;o tras a&ntilde;o. <b>El cap&iacute;tulo 3 muestra que toda la ca&iacute;da viene del coeficiente autom&aacute;tico: la parte del reparto que sale de una f&oacute;rmula fijada por ley. El modelo la tiene en cuenta.</b></p>
""" + ex("g", "Desde 2025 Tigre recibe de la Provincia una parte mayor que San Isidro",
     "Qu&eacute; parte de lo que la Provincia reparte entre sus 135 municipios le toca a cada uno, a&ntilde;o por a&ntilde;o.",
     "ex06.png",
     "Ministerio de Hacienda y Finanzas de la Provincia de Buenos Aires, transferencias a municipios 2021&ndash;2025.",
     "De 2026 s&oacute;lo hay seis meses de datos, y por eso no est&aacute; en el gr&aacute;fico. En esos meses, San Isidro baja a 1,6811% y Tigre sube a 1,8370%.") + """

<h2><span class="n">1.6</span>Lo que dice este cap&iacute;tulo, en cinco puntos</h2>
<ol class="n">
<li>San Isidro est&aacute; dividido en dos. Casi la mitad de la gente vive en Boulogne Sur Mer y en B&eacute;ccar. Ah&iacute; est&aacute;n la mayor&iacute;a de los hogares sin gas de red y sin cloaca. Ah&iacute; hay menos gente con la universidad terminada.</li>
<li>El Municipio invierte en obra p&uacute;blica m&aacute;s que casi todos los municipios de la provincia. Pero el dinero va a lo que se ve: el alumbrado recibe el triple que el agua y las cloacas. Diez empresas se llevan m&aacute;s de la mitad de lo adjudicado. Desde 2018 no se publica d&oacute;nde est&aacute;n las empresas que cobran.</li>
<li>A empleo va el 0,05% del gasto y a vivienda, el 0,10%. Es casi nada.</li>
<li>As&iacute; lo dice el plan de gobierno 2024&ndash;2025. Su primera prioridad es la seguridad, y ese gasto subi&oacute; 34,8% en un a&ntilde;o, descontada la inflaci&oacute;n. La asistencia social no est&aacute; entre sus prioridades, y su gasto baj&oacute; 32,5%.</li>
<li>San Isidro se financia solo. Lo que recauda el propio Municipio paga el 64% de su gasto. Por eso tiene el dinero y la libertad para cambiar en qu&eacute; se gasta. Lo que falta es que decidan los vecinos que viven donde est&aacute;n los problemas.</li>
</ol>
<p><b>Los cap&iacute;tulos que siguen proponen c&oacute;mo hacerlo: que los vecinos de cada zona decidan la mitad de la obra p&uacute;blica.</b></p>
""")


# =====================================================================
# NOTA DE METODO - va al final del documento, con las notas de cada capitulo
# y las fuentes del texto (content_f.py)
# =====================================================================
METODO = dict(id="metodo", runhead=RH, html="""
<h1>Nota de m&eacute;todo</h1>
<div class="stand">C&oacute;mo est&aacute; construido este documento, de d&oacute;nde sale cada cifra y qu&eacute; l&iacute;mites tiene.</div>
<p class="lead">Cada cifra de este documento sale de un documento p&uacute;blico. La fuente de cada cuadro y de cada gr&aacute;fico con datos va debajo de &eacute;l. La de lo que dice el texto va en las p&aacute;ginas que siguen a esta nota.</p>
<div class="cols">
<p><b>Fecha de corte.</b> Los datos est&aacute;n actualizados al 20 de septiembre de 2026. Donde el texto dice &laquo;hoy&raquo;, se refiere a esa fecha. Hay cuatro excepciones. El modelo fiscal est&aacute; cerrado al 31 de diciembre de 2025. El portal de transparencia se revis&oacute; en septiembre de 2026. La valuaci&oacute;n de la tierra del 3.5 usa las parcelas de ARBA descargadas el 25 de septiembre de 2026. Lo que la lista de fuentes fecha despu&eacute;s del corte lleva su fecha al lado.</p>
<p>Las cifras de las cuentas salen de tres lugares. Uno son los informes de ejecuci&oacute;n presupuestaria y las rendiciones de cuentas que publica la propia Municipalidad de San Isidro. Otro, los fallos del Tribunal de Cuentas de la Provincia. El tercero, el sistema SIMCo de la Provincia. Los datos de cada zona salen del Censo Nacional 2022, por radio censal. El modelo fiscal reproduce exactamente lo que gast&oacute; y cobr&oacute; el Municipio en 2025, sin ninguna diferencia.</p>
<p><b>Las investigaciones de esta edici&oacute;n.</b> Son siete informes. Se hicieron en octubre de 2026, s&oacute;lo con fuentes p&uacute;blicas que quedan guardadas en el repositorio. Cada uno marca qu&eacute; se ley&oacute; en la fuente y qu&eacute; es c&aacute;lculo propio. El 21 trata el ruido y la prueba sellada. El 22, los profesores digitales. El 23, los costos con la mejor opci&oacute;n en calidad y precio, el puente con los laboratorios, los espect&aacute;culos, los turnos, y g&eacute;nero y discapacidad. El 23 bis, las rejas en los desag&uuml;es, los tel&eacute;fonos de los inspectores, qui&eacute;n tiene gratis el profesor digital, los espect&aacute;culos y los mensajes de texto. El 23 ter, los tel&eacute;fonos sin transmisi&oacute;n, los colegios con aporte del 100% y los doscientos shows. El 23 qu&aacute;ter, los inspectores de Habilitaciones y de obra, el banco de los sueldos, las grabaciones a la vista, el invierno bajo techo y el volumen. El 23 quinquies, las barreras de Per&uacute; y Alto Per&uacute;, y la temporada bajo techo. Lo que est&aacute; en d&oacute;lares se pasa a pesos con el d&oacute;lar de diciembre de 2025, $1.447,84 (BCRA).</p>
<p><span class="sg">El modelo, los datos, las series y los catorce gr&aacute;ficos son p&uacute;blicos, y cualquiera puede rehacerlos.</span> Desde que se presenta este programa, se pueden bajar de un repositorio abierto, con las pruebas autom&aacute;ticas que los controlan. Cualquiera puede correrlos y llegar a los mismos n&uacute;meros, o encontrar que no llega.</p>
</div>

<div class="callout a">
<div class="clabel">Los l&iacute;mites</div>
<p>Los datos de los otros 105 municipios vienen de un sitio de terceros, y no se comprobaron uno por uno. Los l&iacute;mites de las localidades son de OpenStreetMap, porque la Municipalidad no publica los suyos. En 2025, el Municipio cambi&oacute; la forma de clasificar su gasto por funci&oacute;n. Por eso, buena parte de las series no se puede comparar de un a&ntilde;o al otro.</p>
</div>

<div class="hairline"></div>
<h2>Las notas de cada cap&iacute;tulo</h2>
<h3>Cap&iacute;tulo 1 &middot; Diagn&oacute;stico</h3>
<div class="note">
<p>Las cifras de las cuentas salen de los informes de ejecuci&oacute;n presupuestaria y de las rendiciones de cuentas que publica la Municipalidad de San Isidro. Tambi&eacute;n salen de los fallos del Honorable Tribunal de Cuentas de la Provincia de Buenos Aires y del sistema SIMCo de la Provincia. Las tres fuentes se compararon entre s&iacute;. Los datos de cada zona salen del Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022 (INDEC), por radio censal. Salvo que se diga otra cosa, los montos est&aacute;n en pesos constantes de diciembre de 2025, es decir, ajustados por la inflaci&oacute;n hasta esa fecha.</p>
<p>Las seis zonas del 1.1 son las localidades del partido, con los l&iacute;mites de OpenStreetMap, aplicados a los 360 radios censales del INDEC. Cada radio va a la localidad que contiene su punto representativo, que siempre cae dentro del radio. Los 360 caen en una sola localidad: ninguno queda afuera y ninguno est&aacute; en dos.</p>
<p>El domicilio de las empresas que ganaron contratos sale de 3.670 decretos del Bolet&iacute;n Oficial municipal que lo publican. La proporci&oacute;n de 2002 a 2017 deja afuera 41 designaciones de inspector t&eacute;cnico. No son contratos con terceros, y el domicilio que publican es el del inspector. La proporci&oacute;n cuenta decretos, no montos, porque los montos est&aacute;n en pesos de cada a&ntilde;o, sin ajustar por inflaci&oacute;n. La concentraci&oacute;n usa los 407 decretos que nombran a cada empresa con su monto. Si se suman los 144 que informan s&oacute;lo un total, baja al 42,1%.</p>
<p>Los datos de los otros 105 municipios bonaerenses del 1.2 salen de informes de ejecuci&oacute;n RAFAM, procesados por La Verdadera PBA. Es un sitio de terceros que vuelve a publicar datos oficiales de la Provincia. Las cifras de San Isidro se compararon con el estado de ejecuci&oacute;n del propio Municipio, y coinciden en las siete categor&iacute;as del gasto por objeto. Las de los otros municipios no se compararon una por una. Se usan para calcular la mediana de la Provincia y el lugar de San Isidro entre los dem&aacute;s.</p>
<p>El gasto devengado total de 2025, 324.304 millones, es el del estado de ejecuci&oacute;n del Municipio por objeto y por programa. Es tambi&eacute;n el que publica RAFAM. El estado por finalidad y funci&oacute;n suma 324.133,9 millones, porque deja afuera 170,1 millones de activos financieros.</p>
</div>
<h3>Cap&iacute;tulo 2 &middot; La gesti&oacute;n, medida</h3>
<div class="note">
<p>Todas las cifras salen de documentos publicados por la Municipalidad de San Isidro. Son los estados de ejecuci&oacute;n presupuestaria, la situaci&oacute;n econ&oacute;mico-financiera y el documento &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo;. Tambi&eacute;n salen de los informes de ejecuci&oacute;n RAFAM de los 106 municipios bonaerenses con datos comparables para 2025. De d&oacute;nde vienen esos datos, y qu&eacute; l&iacute;mites tienen, lo dice la nota del cap&iacute;tulo 1. La revisi&oacute;n del portal de transparencia se hizo en septiembre de 2026, y cualquiera la puede repetir. Alcanza con abrir el portal del Municipio y mirar c&oacute;mo est&aacute; cada una de las siete secciones que enumera el cap&iacute;tulo 5.</p>
<p><b>Cuadro [[n:accion]].</b> El plan &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo; tiene tres prioridades, diecinueve objetivos y setenta y siete metas numeradas, contadas una por una. Las metas est&aacute;n agrupadas por tema, y no se recort&oacute; ninguna. Las cuatro primeras filas del cuadro cubren las tres prioridades completas del plan.</p>
</div>
<h3>Cap&iacute;tulo 3 &middot; Los fondos</h3>
<div class="note">
<p>El modelo usa cuatro fuentes. La ejecuci&oacute;n presupuestaria 2010&ndash;2025 del Municipio. Los fallos del Tribunal de Cuentas de la Provincia. El Estado de Situaci&oacute;n Econ&oacute;mico-Financiera del Municipio. Las planillas de transferencias de la Direcci&oacute;n Provincial de Coordinaci&oacute;n Municipal. A todas las series se les descont&oacute; la inflaci&oacute;n con el IPC (INDEC 2016&ndash;2026; IPC San Luis 2010&ndash;2016, con la forma de unir las dos series explicada).</p>
<p>Los cuatro par&aacute;metros se calcularon con la serie hist&oacute;rica, y no se supusieron. El a&ntilde;o cero reproduce exactamente la ejecuci&oacute;n oficial de 2025. En los treinta y nueve a&ntilde;os-escenario del modelo, un control autom&aacute;tico revisa que las cuentas cierren. El modelo, los datos y las pruebas son p&uacute;blicos, y cualquiera puede rehacerlos.</p>
<p>El escenario base congela el gasto, descontada la inflaci&oacute;n, en el nivel de 2025. Durante doce a&ntilde;os no hay aumento real de sueldos ni m&aacute;s servicios. La deuda entra con su saldo al 31 de diciembre de 2025: 8.960 millones, la cifra del informe oficial de ese trimestre. El informe de junio de 2026 es posterior, y no est&aacute; incluido. La comparaci&oacute;n de la tabla municipal con ARBA cruza las dos escalas en 69.258 parcelas, y cada parcela pesa seg&uacute;n su superficie. Los metros construidos no son p&uacute;blicos. Por eso, lo que aporta actualizar la tabla de valuaci&oacute;n se calcula en el modelo s&oacute;lo sobre la tierra.</p>
<p><b>Gr&aacute;fico [[n:sinada]].</b> El programa tambi&eacute;n est&aacute; en el modelo. En 2029 y 2030, la tabla nueva cobra m&aacute;s de lo que el programa gasta. En 2028, y desde 2031, cobra menos (cuadro [[n:programa_base]]).</p>
<p><b>Cuadro [[n:programa]].</b> Las cifras marcadas son c&aacute;lculos del equipo de este programa, no cifras oficiales. Antes de comprometerse, se presupuestan o se licitan. Son las de apoyo escolar, las inspecciones grabadas, la plataforma, las pasant&iacute;as, el semillero, los cuidadores y la Escuela N&aacute;utica. Tambi&eacute;n las de los ba&ntilde;os y las clases de la costa, los espect&aacute;culos, lo que se deja de cobrar en multas y los equipos. Las dem&aacute;s salen de la ejecuci&oacute;n 2025 publicada y del modelo del cap&iacute;tulo.</p>
<p><b>Los equipos van cada uno en el rengl&oacute;n de su &aacute;rea, y dentro de su monto.</b> Ambiente: seis estaciones que miden el ruido, 313,5 M una sola vez. Formaci&oacute;n: sesenta puestos en seis centros de acceso, 137,1 M una sola vez y 39,5 M por a&ntilde;o de conexi&oacute;n. Salud: trece pantallas que muestran la gente en la guardia, 8,3 M una sola vez. En Ciencia y T&eacute;cnica quedan s&oacute;lo las personas que los instalan (cuadro [[n:equipo]]). Los precios salen de compras p&uacute;blicas de la Ciudad y de la Naci&oacute;n, llevados a diciembre de 2025 con el IPC. De la Ciudad: la estaci&oacute;n de ruido, de diciembre de 2024, y la mini PC y el enlace de fibra, de 2026. De la Naci&oacute;n: la notebook, de noviembre de 2025, y el televisor, el escritorio y la silla, de 2026. Las inspecciones se graban con el tel&eacute;fono del agente, as&iacute; que no hay c&aacute;maras corporales. El an&aacute;lisis de video de seguridad usa las 110 licencias que el Municipio ya compr&oacute; (informe 23). Lo que est&aacute; en d&oacute;lares se pasa con el d&oacute;lar de diciembre de 2025, $1.447,84 (BCRA). Los cuidadores cobran 427.806,54 $ por mes, en la categor&iacute;a asistencia y cuidado de personas, a diciembre de 2025 (Comisi&oacute;n Nacional de Trabajo en Casas Particulares, Resoluci&oacute;n 3/2025). Se suman las cargas del cuadro [[n:equipo]], y se cuentan trece sueldos por a&ntilde;o.</p>
<p><b>Cuadro [[n:tabla2008]].</b> Las parcelas salen del servicio de mapas de ARBA, y &laquo;reconocido&raquo; usa los valores sin redondear. El detalle est&aacute; en el informe 09. Las localidades son las de los cap&iacute;tulos 1 y 4, armadas con radios censales, y sus l&iacute;mites no siguen el catastro. Cada parcela va a la localidad donde cae. La mayor parte de cada una est&aacute; en estas circunscripciones y secciones. En Acassuso, III-A y III-C. En Mart&iacute;nez, III-B, III-D a III-J y IV-A a IV-D. En la localidad de San Isidro, I-A, I-B, II-A a II-C, III-K, IV-E, VII-C, VII-D y VII-H. En B&eacute;ccar, VII-A, VII-B, VII-E a VII-G y VIII-A a VIII-E. En Villa Adelina, V-B, V-D, V-F y V-G. En Boulogne Sur Mer, V-A, V-C, V-E y VI-A a VI-J. El 2,9% de las parcelas cae en una secci&oacute;n donde la mayor&iacute;a es de otra localidad. Si se toman las secciones enteras, Acassuso da 2,37 veces Boulogne Sur Mer, en vez de 2,94. La lista parcela por parcela est&aacute; en data/valuacion_parcelas.csv, y el cruce por secci&oacute;n, en data/valuacion_secciones_localidad.csv. <b>L&iacute;mites.</b> La comparaci&oacute;n es de proporciones, no de pesos, porque las dos escalas usan unidades distintas. De las 69.258 parcelas de la valuaci&oacute;n provincial, 68.644 cruzan con la tabla municipal: el 99,1%. Es s&oacute;lo tierra, sin lo construido. Adem&aacute;s, la valuaci&oacute;n provincial es de un reval&uacute;o de 2016, as&iacute; que no es el precio de mercado de hoy. Lo que se compara es c&oacute;mo ordena cada escala, no cu&aacute;nto vale un inmueble.</p>
<p><b>Cuadro [[n:deuda]].</b> La deuda flotante son pagos de corto plazo, y cambia mucho de un trimestre a otro. La que muestra la tendencia es la consolidada. Creci&oacute; de 1.408 a 5.927 millones. Descontada la inflaci&oacute;n, creci&oacute; de 2.660 a 5.072 millones de pesos de diciembre de 2025: casi el doble. El bono de 30.000 millones no est&aacute; en el cuadro, porque se emiti&oacute; el 13 de agosto de 2026 y el &uacute;ltimo informe publicado cierra en junio.</p>
<p><b>Cuadro [[n:programa_base]].</b> Los dos escenarios suponen lo mismo sobre lo que recauda el Municipio y sobre la coparticipaci&oacute;n. Lo &uacute;nico que cambia es el programa, y lo que cobra la tabla nueva. El programa empieza en 2028, el primer a&ntilde;o completo del mandato. La &uacute;ltima fila supone que el m&iacute;nimo de la tasa frena todas las subas de los lotes chicos (3.5). Las diferencias se calculan sin redondear.</p>
</div>
<h3>Cap&iacute;tulo 4 &middot; El mecanismo</h3>
<div class="note">
<p>Los art&iacute;culos 60, 132 y 119 de la Ley Org&aacute;nica de las Municipalidades se comprobaron en tres fuentes oficiales distintas. Son la copia de la ley del Ministerio del Interior de la Naci&oacute;n, el digesto del Concejo Deliberante de La Plata y el digesto del Municipio de Tigre. El art&iacute;culo 211 de la Constituci&oacute;n provincial se comprob&oacute; en el texto oficial. El Decreto 2099/2025 de Pinamar se comprob&oacute; en el Sistema de Boletines Oficiales Municipales de la Provincia. La Ordenanza 6045/1984 de San Isidro se comprob&oacute; en el Digesto del Municipio. Su &uacute;nico cambio posterior es la Ordenanza 7164/1993, que no toca los art&iacute;culos 5, 8, 9 ni 10.</p>
<p>Las cifras de obra p&uacute;blica y su reparto por zona salen de la ejecuci&oacute;n presupuestaria 2025 del Municipio y del Censo 2022 (INDEC), por radio censal. El reparto se calcula sobre 295.978 habitantes, que es la gente que vive en viviendas particulares seg&uacute;n el Censo 2022. Las otras 1.304 personas viven en viviendas colectivas. El Censo no las publica por radio censal, as&iacute; que no se pueden asignar a una zona.</p>
<p>El 1,5% que paga el funcionamiento de las comisiones sale de estos supuestos. Se calcula sobre el sueldo de la categor&iacute;a de ingreso del Municipio: categor&iacute;a 6, 35 horas. Son 432.624 pesos por mes en la Ordenanza 9422 de presupuesto 2026, y 420.507 en pesos de diciembre de 2025. Hay cuatro asambleas por zona y por a&ntilde;o, 24 en total, como el ciclo m&iacute;nimo de la Ciudad de Buenos Aires. Cada una tiene dos cuidadoras, cuatro horas cada una: medio mill&oacute;n por a&ntilde;o. Una obra promedio es de 100 millones, lo que da 289 obras el a&ntilde;o 4. Hay tres vecinos por obra, y cada uno cobra un cuarto de ese sueldo: 91 millones. Tambi&eacute;n hay un 3% de administraci&oacute;n sobre lo que hacen las propias comisiones, si hacen un cuarto de la partida: 217 millones. En total, son 308 millones, el 1,1%. Con obras promedio de 50 millones son 400, el 1,4%. En los dos casos, el 1,5% alcanza. El panel sorteado tiene 40 personas y cuatro sesiones, y cobra un d&iacute;a de ese sueldo por sesi&oacute;n.</p>
<p>Lo que falta en la franja baja de la costa se cuenta en la zona San Isidro. Hay tres radios vecinos de la fracci&oacute;n 02, los terminados en 03, 04 y 05. Tienen entre 4,3% y 11,8% de hogares con NBI, y entre 24,8% y 63,1% sin gas de red. El promedio de la zona es 1,83% y 16,64%. En Acassuso no hay un bols&oacute;n de pobreza. Sus diecis&eacute;is radios tienen NBI de 0,0% a 2,4%, y el 19,48% sin gas de red est&aacute; repartido parejo. El &uacute;nico radio donde la falta de cloaca pesa es el 067560403, con 17,4% sobre 316 hogares, y tiene 0,6% de NBI.</p>
<p>Los casos de panel sorteado son experiencias en marcha o documentadas. Son Ostbelgien, Winterthur, Darebin, Melbourne, Bolonia, Barcelona, Par&iacute;s, Se&uacute;l, Reikiavik, Nueva York, Chicago, C&oacute;rdoba y la Ciudad de Buenos Aires. La idea de hacer una pregunta concreta, y de evitar que un grupo se quede con el panel, sale de los estudios acad&eacute;micos sobre sorteo y control popular. Ning&uacute;n caso se puede copiar sin adaptarlo. Barcelona y Par&iacute;s no tienen los l&iacute;mites de la Ley Org&aacute;nica bonaerense. La Ciudad de Buenos Aires tiene comunas con autoridades electas, que San Isidro no tiene.</p>
<p><b>Cuadro [[n:equipo]].</b> Los sueldos son brutos y de mercado, seg&uacute;n la mediana de la encuesta de Sysarmy 2026.1. Un senior cobra 3,40 M por mes, un semi-senior 2,43 M y un junior 1,50 M. Se cuentan trece sueldos por a&ntilde;o, m&aacute;s las cargas del empleador. Son el 16,8% de contribuciones (IPS 12%, Decreto-Ley 9650/80, e IOMA 4,8%, Decreto 2655/04) y la ART que contrat&oacute; el Municipio: 3,275% m&aacute;s una suma fija por persona (Decreto 1587/2025). Los pasantes cobran 240.000 $ por mes, con ART y salud. Las 10 personas nuevas y las 8 de las &aacute;reas salen del informe 23. La infraestructura y las licencias van con precios publicados y el d&oacute;lar de diciembre de 2025, $1.447,84 (informe 23). Incluyen lo que usan los vecinos, las 160 asociaciones inscriptas al 40% de su cupo, los alumnos, el semillero y las herramientas del equipo. Los avisos van por la propia inteligencia artificial del Municipio, sin WhatsApp. La auditor&iacute;a externa es el 10% del equipo de las primeras 49 personas, sin cargas. La ayuda en cada una de las seis zonas la dan empleados que ya cobran su sueldo y cambian de tarea.</p>
</div>
<h3>Cap&iacute;tulo 5 &middot; Qu&eacute; hacemos en cada &aacute;rea</h3>
<div class="note">
<p>El gasto por funci&oacute;n sale del estado de ejecuci&oacute;n presupuestaria acumulado de todo 2025 del Municipio de San Isidro. Los cambios entre 2024 y 2025 est&aacute;n calculados en pesos constantes de diciembre de 2025, descontada la inflaci&oacute;n con el IPC. Los datos de cada zona salen del Censo 2022 (INDEC), por radio censal. Cu&aacute;nto cuesta cada propuesta est&aacute; en el cap&iacute;tulo 3.</p>
<p>En 2025 el Municipio dividi&oacute; su gasto en veinte funciones, y en 2024 en catorce. En este cap&iacute;tulo s&oacute;lo se usan los cambios de un a&ntilde;o al otro de las funciones que est&aacute;n en los dos a&ntilde;os, y cuyo grupo no sum&oacute; funciones nuevas. Las dem&aacute;s se marcan como no comparables.</p>
<p>La historia de la recolecci&oacute;n se arm&oacute; leyendo el texto de 527 boletines quincenales y 324 ediciones extra, de 2002 a 2024. Tambi&eacute;n se ley&oacute; el visor nuevo del Bolet&iacute;n Oficial, de 2024 a 2026. La plataforma vieja, que publica hasta marzo de 2024, s&oacute;lo permite buscar por el t&iacute;tulo del bolet&iacute;n, y no por el texto de los decretos. El contrato de 1998 lo cita el Decreto 29/2003.</p>
<p>Las pruebas sobre seguridad son de otros pa&iacute;ses. La revisi&oacute;n de 65 estudios es de la Campbell Collaboration, actualizada por Braga y otros. La evaluaci&oacute;n de Dallas mide el primer a&ntilde;o del plan de la ciudad, con el m&eacute;todo de diferencias en diferencias. Los 35,5 minutos por turno salen de un experimento controlado en la calle. Son estudios sobre polic&iacute;as, no sobre patrullas municipales argentinas. La idea de concentrar el patrullaje se puede aplicar ac&aacute;. Cu&aacute;nto baja el delito no est&aacute; demostrado para este caso. Los datos de Tigre son comunicados del propio Municipio de Tigre.</p>
<p>Bezos hizo su propuesta en el America Business Forum de Miami, en noviembre de 2025. La Ciudad de Miami anunci&oacute; que adoptaba la plataforma en marzo de 2026. Sirve para ver d&oacute;nde est&aacute; la vara, pero todav&iacute;a no tiene resultados medidos.</p>
<p><b>Cuadro [[n:piramide]].</b> En el mandato entran 231 y 231 el primer a&ntilde;o, 412 y 412 el segundo, 355 y 356 el tercero, y 464 y 464 el cuarto. Cada uno pasa seis meses por el Municipio y seis por las empresas. El equipo de la plataforma (cuadro [[n:equipo]]) es parte de los pasantes y juniors del Municipio (cuadro [[n:proyectos]]), y ellos son parte de esta pir&aacute;mide.</p>
<p><b>Cuadro [[n:reparto_empleo]].</b> Los 3 millones por persona pagan los dos a&ntilde;os de formaci&oacute;n. La pasant&iacute;a la paga quien la recibe. Los dos primeros a&ntilde;os, la formaci&oacute;n usa toda la partida de empleo, porque todav&iacute;a no hay egresados para contratar. Entran 462 y 824, en vez de 277 y 494, y egresan 1.286 en el mandato. El tercer a&ntilde;o vuelve este reparto. La parte de salud de los meses 12 a 18 se pagaba con la contrataci&oacute;n de desarrollos. Esos dos a&ntilde;os sale del gasto flexible libre.</p>
<p><b>Cuadro [[n:hoy_propuesta]].</b> Mi Primer Empleo da talleres de curr&iacute;culum y contacto con empresas, y tiene el portal de empleo: 131 empresas y unos 600 puestos, seg&uacute;n el Municipio. Las pr&aacute;cticas de Medicina se hacen en hospitales y centros de salud. Son con la Barcel&oacute; (Decreto 374/2025, sin gasto del Municipio), con la UCA (Decreto 498/2026) y, de 2026 a 2028, con la Favaloro, seg&uacute;n una nota del Municipio que public&oacute; InfoBAN. Las de Veterinaria son en Zoonosis, con la UBA, por hasta dos meses (Decreto 775/2026). Las de la Barcel&oacute; y las de Veterinaria no se pagan, y los convenios de la Favaloro y de la UCA no est&aacute;n publicados. Los 15 pasantes de las fiscal&iacute;as los paga el Municipio, por un convenio de 2003 con el Ministerio P&uacute;blico. Cobran 747.500 $ por mes desde marzo de 2026. Son becas dadas por decreto (Decreto 298/2026), fuera del r&eacute;gimen de pasant&iacute;as. No se publican sus horas, y no se encontr&oacute; qu&eacute; cobertura tienen. La UNSO tiene pasant&iacute;as pagas con pymes, sin un convenio vigente con el Municipio. El de 2021 no tiene movimientos desde 2022 (Zona Norte Visi&oacute;n, 16 de junio de 2025). Lo de los m&aacute;s de 300 vecinos con trabajo sale de un comunicado del Municipio, citado por Zona Norte Visi&oacute;n el 11 de agosto de 2026. D&oacute;nde est&aacute;n las empresas que cobran del Municipio se dej&oacute; de publicar en 2018 (1.2).</p>
</div>
<h3>Cap&iacute;tulo 6 &middot; El plan, con fechas</h3>
<div class="note">
<p>Este cap&iacute;tulo no trae datos nuevos, salvo el caso de Los &Aacute;ngeles del cuadro de riesgos, que sale del LA School Report (23 de julio de 2024). El plan B de la cara y del programa del profesor digital sale del informe 23. Cada cifra sale del cap&iacute;tulo que la explica. Los datos de cada zona, del cap&iacute;tulo 1. La revisi&oacute;n del plan de gobierno 2024&ndash;2025, del cap&iacute;tulo 2. El modelo fiscal y los n&uacute;meros de hoy del presupuesto, del cap&iacute;tulo 3. La rampa y la f&oacute;rmula de reparto, del cap&iacute;tulo 4. El estado del portal de transparencia, del cap&iacute;tulo 5.</p>
<p>Los 4.616 hogares sin cloaca de Boulogne y B&eacute;ccar est&aacute;n contados hogar por hogar en los 360 radios censales del Censo 2022, y no calculados con un porcentaje. Las dos zonas son las localidades, con los l&iacute;mites de OpenStreetMap, aplicados a esos radios. El cap&iacute;tulo 4 lo explica.</p>
<p><b>Cuadro [[n:compromisos]].</b> Los dos primeros van juntos a la sesi&oacute;n extraordinaria. Sin partida, no hay asamblea que decida. Sin derogar los art&iacute;culos 8 a 10 de la Ordenanza 6045, la asociaci&oacute;n que decide puede ser disuelta por el mismo al que le dijo que no. Los compromisos 15, 16 y 21 dependen s&oacute;lo del Ejecutivo. La detecci&oacute;n en el momento usa las 110 licencias de an&aacute;lisis de video que el Municipio ya compr&oacute;. No hay nada que licitar, y funciona a los cien d&iacute;as. Las inspecciones se graban con el tel&eacute;fono del agente. El decreto sale a los cien d&iacute;as, con el convenio de 24 cuotas sin inter&eacute;s con el banco que paga los sueldos. Funciona en el mes 9, primero con los inspectores y los agentes de tr&aacute;nsito. La patrulla entra en una segunda etapa. La ordenanza que anula el acta hecha sin grabaci&oacute;n sellada y subida va despu&eacute;s, y est&aacute; escrita en el anexo. La denuncia del comerciante y el registro de instructores y artistas empiezan por decreto, y las Ordenanzas IV y XIV los dejan fijos despu&eacute;s.</p>
</div>
""")
