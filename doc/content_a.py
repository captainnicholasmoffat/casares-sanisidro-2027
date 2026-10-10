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
 ("i", "1.1 &nbsp;San Isidro, dividido en dos", "cap1a"),
 ("i", "1.2 &nbsp;El Municipio invierte m&aacute;s que casi todos. Pero el dinero no llega adonde hace falta.", "cap1a2"),
 ("i", "1.3 &nbsp;D&oacute;nde no va el dinero", "cap1a2"),
 ("i", "1.4 &nbsp;Por qu&eacute; pasa esto: lo dice el plan de gobierno", "cap1b"),
 ("i", "1.5 &nbsp;San Isidro se financia solo. Eso cambia todo.", "cap1b"),
 ("i", "1.6 &nbsp;Lo que dice este cap&iacute;tulo, en cinco puntos", "cap1b"),
 ("g", "2 &middot; El gobierno actual, medido", None),
 ("i", "2.1 &nbsp;Gastar el presupuesto no es prestar el servicio", "cap2"),
 ("i", "2.2 &nbsp;Lo que se prometi&oacute; publicar y no est&aacute; publicado", "cap2b"),
 ("i", "2.3 &nbsp;El hallazgo central: el plan no nombra el empleo, la vivienda ni la salud", "cap2b"),
 ("i", "2.4 &nbsp;Lo que dice este cap&iacute;tulo, en cinco puntos", "cap2b"),
 ("g", "3 &middot; Los fondos", None),
 ("i", "3.1 &nbsp;En 2025 hubo d&eacute;ficit, si se cuenta lo que de verdad se cobr&oacute;", "cap3a"),
 ("i", "3.2 &nbsp;Los cuatro n&uacute;meros que deciden el futuro de las cuentas de San Isidro", "cap3a"),
 ("i", "3.3 &nbsp;C&oacute;mo quedan las cuentas si nadie cambia nada", "cap3a"),
 ("i", "3.4 &nbsp;Cu&aacute;nto cuesta este programa", "cap3b"),
 ("i", "3.5 &nbsp;De d&oacute;nde salen los fondos", "cap3b2"),
 ("i", "3.6 &nbsp;Qu&eacute; habr&iacute;a que vigilar", "cap3b3"),
 ("i", "3.7 &nbsp;Lo que dice este cap&iacute;tulo, en ocho puntos", "cap3b3"),
 ("g", "4 &middot; El mecanismo", None),
 ("i", "4.1 &nbsp;El l&iacute;mite legal: lo que un intendente bonaerense no puede delegar", "cap4a"),
 ("i", "4.2 &nbsp;La Legislatura todav&iacute;a no habilit&oacute; el refer&eacute;ndum ni la consulta popular en los municipios", "cap4a"),
 ("i", "4.3 &nbsp;Cu&aacute;nto dinero van a decidir los vecinos", "cap4a"),
 ("i", "4.4 &nbsp;C&oacute;mo se reparte el dinero entre las zonas: por poblaci&oacute;n y por necesidad", "cap4a2"),
 ("i", "4.5 &nbsp;Qui&eacute;n decide y qui&eacute;n ejecuta: dos capas", "cap4b"),
 ("i", "4.6 &nbsp;C&oacute;mo se forma una comisi&oacute;n, y c&oacute;mo rinde cuentas", "cap4b"),
 ("i", "4.7 &nbsp;El Concejo Deliberante: diez bloques y ninguna mayor&iacute;a", "cap4bb2"),
 ("i", "4.8 &nbsp;Qu&eacute; cambia cuando el barrio tambi&eacute;n hace la obra", "cap4bb2"),
 ("i", "4.9 &nbsp;Dos piezas m&aacute;s: el gasto de cada zona a la vista y la partida protegida", "cap4b2"),
 ("i", "4.10 &nbsp;El primer acto de gobierno: derogar tres art&iacute;culos", "cap4b2"),
 ("i", "4.11 &nbsp;La inteligencia artificial del Municipio", "cap4b2"),
 ("i", "4.12 &nbsp;A qui&eacute;n le molesta esto", "cap4bc"),
 ("i", "4.13 &nbsp;Lo que dice este cap&iacute;tulo, en nueve puntos", "cap4bc"),
 ("g", "5 &middot; Qu&eacute; hacemos en cada &aacute;rea", None),
 ("i", "5.1 &nbsp;C&oacute;mo leer este cap&iacute;tulo", "cap5a"),
 ("i", "5.2 &nbsp;D&oacute;nde va hoy cada peso", "cap5a"),
 ("i", "5.3 &nbsp;Empleo", "cap5a2"),
 ("i", "5.4 &nbsp;Vivienda y servicios b&aacute;sicos", "cap5a4"),
 ("i", "5.5 &nbsp;Ambiente", "cap5b"),
 ("i", "5.6 &nbsp;Salud", "cap5bb"),
 ("i", "5.7 &nbsp;Seguridad", "cap5bc"),
 ("i", "5.8 &nbsp;Educaci&oacute;n y cultura", "cap5b2"),
 ("i", "5.9 &nbsp;Digitalizaci&oacute;n: tr&aacute;mites r&aacute;pidos e inspecciones grabadas", "cap5b2a2"),
 ("i", "5.10 &nbsp;Transparencia", "cap5b2b"),
 ("i", "5.11 &nbsp;Transporte y comercio", "cap5b2b"),
 ("i", "5.12 &nbsp;Los empleados del Municipio", "cap5b2c"),
 ("i", "5.13 &nbsp;Ni&ntilde;ez, personas mayores, g&eacute;nero y discapacidad", "cap5b3"),
 ("i", "5.14 &nbsp;Las &aacute;reas sin un apartado propio, y d&oacute;nde se tratan", "cap5b3b"),
 ("i", "5.15 &nbsp;Lo que dice este cap&iacute;tulo, en ocho puntos", "cap5b3b"),
 ("g", "6 &middot; El plan, con fechas", None),
 ("i", "6.1 &nbsp;Los primeros cien d&iacute;as", "cap6"),
 ("i", "6.2 &nbsp;Cu&aacute;nta obra deciden los vecinos, a&ntilde;o por a&ntilde;o", "cap6"),
 ("i", "6.3 &nbsp;Las metas de los cuatro a&ntilde;os, y c&oacute;mo se comprueban", "cap6b"),
 ("i", "6.4 &nbsp;El calendario del mandato, mes por mes", "cap6b2"),
 ("i", "6.5 &nbsp;Qu&eacute; no prometemos, y de qui&eacute;n depende", "cap6c"),
 ("i", "6.6 &nbsp;Qu&eacute; puede salir mal", "cap6c"),
 ("i", "6.7 &nbsp;Lo que dice este cap&iacute;tulo, en seis puntos", "cap6d"),
 ("g", "Cierre", None),
 ("i", "Para cerrar", "cierre"),
 ("g", "Anexo &middot; Las ordenanzas que proponemos", None),
 ("i", "La partida vecinal, el sistema de informaci&oacute;n y la base de valuaci&oacute;n", "ordenanza"),
 ("i", "La fiscalizaci&oacute;n, las asociaciones de parque, g&eacute;nero y los espacios culturales", "ordenanza2"),
 ("i", "El ruido, la higiene urbana y el empleo local", "ordenanza3"),
 ("i", "La costa, la obra en parques y costa, las excepciones urban&iacute;sticas, los parques y las cuotas de las multas", "ordenanza4"),
 ("i", "Lo que estas ordenanzas no dicen, y por qu&eacute;", "ordenanza4"),
 ("i", "Las metas que no llevan ordenanza, y por qu&eacute;", "ordenanza4"),
 ("g", "Glosario", None),
 ("i", "Cuarenta palabras, explicadas", "glosario"),
 ("g", "Nota de m&eacute;todo", None),
 ("i", "C&oacute;mo est&aacute; construido, y qu&eacute; l&iacute;mites tiene", "metodo"),
 ("i", "Las notas de cada cap&iacute;tulo", "metodo"),
 ("i", "Las fuentes de lo que afirma el texto", "fuentes"),
 ("i", "Lo que este programa no hace", "fuentes3"),
 ("i", "Lo que tiene que confirmar un abogado", "fuentes3"),
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
<p class="lead">Seg&uacute;n el Censo 2022, en San Isidro hay <b>25.165 hogares sin gas de red</b> y 6.488 que no tienen
cloaca. La mayor&iacute;a est&aacute; en Boulogne y en B&eacute;ccar. Ah&iacute; est&aacute;n seis de cada diez hogares sin gas y siete de cada diez sin cloaca.</p>

<h2>La pregunta</h2>
<p>El plan de gobierno del intendente se llama &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo;. En el pr&oacute;logo, el intendente escribe: &laquo;Estas prioridades de gesti&oacute;n no las fijamos nosotros, sino que
responden a haber escuchado sus principales problemas y necesidades&raquo;. <b>&iquest;A qui&eacute;n escucharon, y c&oacute;mo, si el empleo y la vivienda no aparecen nunca en el plan?</b></p>
<div class="pull"><p>Las palabras empleo, vivienda, salud, pobreza, agua y cloaca no aparecen en ninguna
parte del plan de gobierno 2024&ndash;2025.</p></div>

<h2>Por qu&eacute; el dinero va a lo que se ve</h2>
<p class="lead">Hay dos maneras de manejar un municipio pensando en la pr&oacute;xima elecci&oacute;n. Ninguna de las dos es gobernar.</p>
<div class="cols">
<p><b>La primera es administrar para la foto.</b> Se elige la obra que se ve: la que se termina antes del fin del mandato y se inaugura cortando una cinta. Nadie tiene que actuar de mala fe para que esto pase. Alcanza con que se elija con ese criterio. <span class="sg">En 2025, el alumbrado p&uacute;blico recibi&oacute; 10.313 millones de pesos, y el agua y las cloacas, 3.320 millones.</span> Una cloaca no se inaugura con una cinta.</p>
<p><b>La segunda es repartir.</b> Es la manera de los gobiernos populistas. Mantienen los votos repartiendo cosas. El que reparte necesita que quien recibe siga dependiendo de lo que le dan. <b>Este programa no va a dar un peso sin trabajo a cambio. Su &uacute;nica beca va a pagar una pr&aacute;ctica de trabajo.</b> Todo el dinero que este programa destina a empleo y vivienda va a pagar formaci&oacute;n, contrataci&oacute;n de personas y obras.</p>
<p><b>Hay una tercera manera, que es la de este programa: administrar para que San Isidro crezca.</b> Queremos que San Isidro funcione mejor al final del mandato que al principio. Eso quiere decir <b>menos hogares sin cloaca y sin gas de red</b>. Quiere decir <b>m&aacute;s gente formada y con trabajo</b>. Tambi&eacute;n quiere decir <b>que los vecinos decidan qu&eacute; obras se hacen en su barrio</b>. Ninguna de esas tres cosas da una foto el d&iacute;a en que se hace.</p>
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

<h2><span class="n">1.1</span>San Isidro, dividido en dos</h2>
<div class="cols">
<p>San Isidro tiene 297.282 habitantes y 110.559 hogares, seg&uacute;n el Censo 2022. En 2025, el Municipio gast&oacute; el equivalente a <b>1.090.897 pesos por habitante</b>. No es poco dinero.</p>
<p>San Isidro est&aacute; dividido en dos, y la divisi&oacute;n es geogr&aacute;fica. De un lado quedan las localidades del oeste y del norte: Boulogne Sur Mer, B&eacute;ccar y Villa Adelina. Del otro, las de la costa sur: la localidad de San Isidro, Mart&iacute;nez y Acassuso.</p>
<p>Un hogar de Boulogne o de B&eacute;ccar tiene <span class="sg">tres veces y media m&aacute;s probabilidad</span> de tener necesidades b&aacute;sicas insatisfechas que uno de Mart&iacute;nez. As&iacute; llama el censo a los hogares a los que les falta algo b&aacute;sico. Por ejemplo, no tienen ba&ntilde;o, o tienen un chico en edad de primaria que no va a la escuela. Ese mismo hogar tiene <span class="sg">cinco veces y media</span> m&aacute;s probabilidad de no tener cloaca, y <span class="sg">cuatro veces</span> m&aacute;s probabilidad de vivir hacinado, con demasiada gente por cuarto. En Boulogne y B&eacute;ccar, tomadas juntas, la proporci&oacute;n de gente con la universidad terminada es <span class="sg">menos de la mitad</span> que en Mart&iacute;nez.</p>
</div>
""" + ex("g", "San Isidro est&aacute; dividido en dos: de un lado el oeste y el norte, del otro la costa sur",
        "Cada localidad tiene el color de su porcentaje de hogares con necesidades b&aacute;sicas insatisfechas. En todo San Isidro, el promedio es 3,16%.",
        "ex01.png",
        "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7; l&iacute;mites de localidad de OpenStreetMap.",
        "OpenStreetMap no es una fuente oficial. El censo divide San Isidro en 360 radios censales, que son las zonas m&aacute;s chicas para las que publica datos. Cada radio se asign&oacute; a una localidad seg&uacute;n d&oacute;nde cae un punto que siempre est&aacute; dentro de &eacute;l. As&iacute;, cada radio qued&oacute; en una sola localidad.")
+ ex("g", "En Boulogne y B&eacute;ccar est&aacute;n cerca de dos tercios de los hogares de San Isidro que tienen estas carencias",
     "Porcentaje de hogares de cada zona con cada una de las cuatro carencias de la leyenda. Debajo de cada zona, cu&aacute;ntos habitantes tiene. En todo San Isidro, el 3,16% de los hogares tiene necesidades b&aacute;sicas insatisfechas (NBI).",
     "ex02.png",
     "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7.")
+ ex("g", "Donde m&aacute;s faltan servicios, menos gente termin&oacute; la universidad: 9% en Boulogne, 32% en Acassuso",
     "Porcentaje de personas con la universidad terminada en cada zona. Las zonas est&aacute;n ordenadas seg&uacute;n cu&aacute;ntos hogares tienen necesidades b&aacute;sicas insatisfechas: primero la que m&aacute;s tiene, al final la que menos.",
     "ex03.png",
     "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7.") + """
<h3>Cu&aacute;nta gente vive en Boulogne Sur Mer y en B&eacute;ccar</h3>
<p class="tight">En Boulogne Sur Mer y en B&eacute;ccar viven <b>138.551 personas, en 47.193 hogares. Son el 46,8% de la gente de San Isidro.</b></p>
<p class="cap"><b>Nota:</b> el 46,8% se calcula sobre las 295.978 personas que viven en viviendas particulares, como casas o departamentos. Esa es la base de todos los datos por zona. Las otras 1.304 personas viven en viviendas colectivas, como los geri&aacute;tricos. Si se cuentan los 297.282 habitantes, es el 46,6%.</p>
<div class="pull"><p>Casi la mitad de la gente de San Isidro vive en esas dos localidades. Ah&iacute; est&aacute; el 60% de los 25.165 hogares sin gas de red, y el 71% de los 6.488 hogares que no tienen cloaca.</p></div>
""" + duo("f_boulogne", "f_martinez",
          "Boulogne Sur Mer y Mart&iacute;nez pagan la misma tasa municipal, pero no tienen los mismos servicios. Ilustraci&oacute;n.") + """

<h2><span class="n">1.2</span>El Municipio invierte m&aacute;s que casi todos. Pero el dinero no llega adonde hace falta.</h2>
<div class="cols">
<p><b>El dato.</b> Hay 106 municipios de la provincia con datos de lo que gastaron en 2025. Entre ellos, San Isidro es <b>el cuarto que m&aacute;s invierte en obra p&uacute;blica</b>. Pone en obra el <b>17,8%</b> de su gasto. En cambio, el municipio t&iacute;pico de la provincia, el que queda en el medio de la lista, pone el <b>5,4%</b>. San Isidro invierte m&aacute;s del triple.</p>
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
<p class="cap"><b>Fuente:</b> RAFAM 2025 (el sistema de cuentas de los municipios de la provincia), v&iacute;a La Verdadera PBA. El dato de San Isidro se compar&oacute; con lo que publica el propio Municipio. Los de los otros 105 municipios, no.</p>

<div class="cols">
<p><b>Adem&aacute;s, ese porcentaje alto se aplica sobre un gasto total que viene bajando.</b> El gasto real del Municipio, es decir, descontada la inflaci&oacute;n, tuvo su m&aacute;ximo en 2017. <b>Desde ese a&ntilde;o cay&oacute; 24,4%.</b> Comparado con 2010, igual est&aacute; 13,1% m&aacute;s alto.</p>
<p><b>La ca&iacute;da empez&oacute; despu&eacute;s de 2017.</b> Entre 2010 y 2017, el gasto real subi&oacute; 49,6%. De 2017 a 2022 baj&oacute; 17,2%, y de 2022 a 2025, otro 8,8%. El peor momento fue de 2022 a 2024, cuando cay&oacute; 21,4%. En 2025 recuper&oacute; una parte: subi&oacute; 16,0%. <b>Desde 2017, ning&uacute;n gobierno volvi&oacute; a ese nivel de gasto.</b> Ese es el l&iacute;mite con el que hay que trabajar.</p>
</div>

<h3>En qu&eacute; servicios urbanos gasta el Municipio</h3>
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
<p class="cap"><b>Nota:</b> los gastos est&aacute;n agrupados seg&uacute;n para qu&eacute; se usan, no seg&uacute;n qu&eacute; se compra. Por eso, dentro de cada rengl&oacute;n hay sueldos, contratos de servicio y obras. Los 49.270 millones de residuos son, sobre todo, el contrato de recolecci&oacute;n. Es un servicio de todos los d&iacute;as, no una inversi&oacute;n. La Provincia usa estos mismos renglones para clasificar el gasto de los municipios (RAFAM).</p>
<h3>La mitad de lo adjudicado iba a empresas de afuera de San Isidro</h3>
<div class="cols">
<p>Durante quince a&ntilde;os, el Municipio public&oacute; un dato que hoy ya no publica. Es el domicilio de la empresa que gana una obra, un servicio o una compra. Elegir a esa empresa se llama adjudicar. Entre 2002 y 2017 hubo 3.013 adjudicaciones con el domicilio publicado. <b>El 49,8% fue a empresas con domicilio en San Isidro, y el 50,2%, a empresas de afuera.</b> La parte de las empresas de San Isidro ven&iacute;a bajando. Fue el 52,6% en 2013, el 46,6% en 2015 y <b>el 40,4% en 2017</b>.</p>
<p>Entre 2011 y 2017, el domicilio aparec&iacute;a en el 62% al 82% de las adjudicaciones. <b>Se dej&oacute; de publicar en 2018, durante el gobierno anterior. El gobierno actual no volvi&oacute; a publicar ese dato.</b> Desde diciembre de 2023 se publicaron 573 decretos de adjudicaci&oacute;n. <span class="sg">Ninguno dice d&oacute;nde est&aacute; la empresa que cobra</span>.</p>
</div>

<h3>En cu&aacute;ntas manos queda lo adjudicado</h3>
<div class="cols">
<p>De esos 573 decretos, 407 dicen qu&eacute; empresa gana y cu&aacute;nto cobra. Suman 116.343 millones de pesos, sin ajustar por inflaci&oacute;n, repartidos entre 236 proveedores. <b>Los diez que m&aacute;s recibieron se llevan el 54,5%, y los veinticinco que m&aacute;s recibieron, el 78,6%</b>.</p>
<p><b>A cuatro de esas empresas les alcanz&oacute; con una sola adjudicaci&oacute;n para estar entre las diez que m&aacute;s recibieron.</b> La m&aacute;s grande de todas es un contrato de seguridad y vigilancia. Ese contrato, por s&iacute; solo, es el <b>11,6% de esos 116.343 millones</b>. Otro decreto, de septiembre de 2024, es para calles y veredas. Con ese &uacute;nico decreto, el Municipio se comprometi&oacute; a pagar 20.916 millones.</p>
</div>


""" + ex("g", "San Isidro invierte en obra m&aacute;s del triple que el municipio t&iacute;pico de la provincia",
     "Qu&eacute; parte de su gasto de 2025 puso en obra p&uacute;blica cada municipio de la provincia. Cada marca es un municipio.",
     "ex04.png",
     "RAFAM 2025, v&iacute;a La Verdadera PBA (la-verdadera-pba.pages.dev), capturado el 3 de septiembre de 2026.",
     "Son 106 de los 135 municipios de la provincia. Los otros 29 no aparecen en esa fuente. Tampoco se calcul&oacute; para ellos ning&uacute;n n&uacute;mero aproximado.") + """
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
<p>El plan de gobierno 2024&ndash;2025 se llama &laquo;Prioridades Estrat&eacute;gicas&raquo;. Fija tres prioridades, en este orden: Seguridad Ciudadana, Espacio P&uacute;blico y Ambiente, e Innovaci&oacute;n. Entre 2024 y 2025, el gasto en seguridad interna, que corresponde a la primera prioridad, <b>subi&oacute; 34,8%, descontada la inflaci&oacute;n</b>. Ning&uacute;n otro gasto creci&oacute; tanto, salvo los pagos de la deuda. La promoci&oacute;n y asistencia social no est&aacute; entre las tres prioridades. En el mismo per&iacute;odo, su gasto <b>cay&oacute; 32,5%</b>.</p>

<h2><span class="n">1.5</span>San Isidro se financia solo. Eso cambia todo.</h2>
<div class="cols">
<p>En 2025, el Municipio recibi&oacute; 82.268 millones de pesos de la Provincia de Buenos Aires. Ese a&ntilde;o gast&oacute; 324.304 millones en total.</p>
<p><b>Hoy, el 64% de lo que gasta el Municipio sale de lo que recauda &eacute;l mismo, y esa parte viene creciendo.</b> Desde 2010, lo que recauda el propio Municipio <b>aument&oacute; 33,6%, descontada la inflaci&oacute;n</b>. Es un 1,95% por a&ntilde;o. Los c&aacute;lculos del cap&iacute;tulo 3 usan ese mismo n&uacute;mero. Mientras tanto, lo que manda la Provincia bajaba. San Isidro depende hoy menos de la Provincia que hace quince a&ntilde;os. No fue una decisi&oacute;n de nadie: sali&oacute; as&iacute; por los n&uacute;meros.</p>
<p>Esto tiene una consecuencia pol&iacute;tica directa: <span class="sg">un intendente de San Isidro no depende del gobierno de la Provincia, en La Plata.</span> La mayor parte del presupuesto se decide ac&aacute;. El Concejo Deliberante aprueba el presupuesto por ordenanza. Adem&aacute;s, el propio Municipio puede pasar dinero de un gasto a otro.</p>
<p>Todo lo que este programa propone puede financiarse sin pedirle permiso a nadie.</p>
</div>
<div class="pull"><p>La Provincia paga el 25% del gasto de San Isidro. El propio Municipio
paga el 64% con lo que recauda.</p></div>
<p>Hay una salvedad, y es de fondo. La Provincia reparte entre los municipios una parte de lo que recauda. A San Isidro le tocaba el 1,938% de ese reparto en 2021, y en 2025 le toc&oacute; el 1,773%. Eso quiere decir que en 2025 le lleg&oacute; un 8,5% menos de lo que habr&iacute;a recibido con la parte de 2021. Esa p&eacute;rdida se repite y se suma a&ntilde;o tras a&ntilde;o. <b>El cap&iacute;tulo 3 muestra que toda la ca&iacute;da viene del coeficiente autom&aacute;tico: la parte del reparto que sale de una f&oacute;rmula fijada por ley. Los c&aacute;lculos de este programa ya tienen en cuenta esa ca&iacute;da.</b></p>
""" + ex("g", "Desde 2025 Tigre recibe de la Provincia una parte mayor que San Isidro",
     "Qu&eacute; parte de lo que la Provincia reparte entre sus 135 municipios le toca a cada uno, a&ntilde;o por a&ntilde;o.",
     "ex06.png",
     "Ministerio de Hacienda y Finanzas de la Provincia de Buenos Aires, transferencias a municipios 2021&ndash;2025.",
     "De 2026 s&oacute;lo hay seis meses de datos, y por eso no est&aacute; en el gr&aacute;fico. En esos meses, San Isidro baja a 1,6811% y Tigre sube a 1,8370%.") + """

<h2><span class="n">1.6</span>Lo que dice este cap&iacute;tulo, en cinco puntos</h2>
<ol class="n">
<li>San Isidro est&aacute; dividido en dos. Casi la mitad de la gente vive en Boulogne Sur Mer y en B&eacute;ccar. Ah&iacute; est&aacute;n la mayor&iacute;a de los hogares sin gas de red y sin cloaca, y hay menos gente con la universidad terminada.</li>
<li>El Municipio invierte en obra p&uacute;blica m&aacute;s que casi todos los municipios de la provincia. Pero el dinero va a lo que se ve: el alumbrado recibe el triple que el agua y las cloacas. Diez empresas se llevan m&aacute;s de la mitad de lo adjudicado. Desde 2018 no se publica d&oacute;nde est&aacute;n las empresas que cobran.</li>
<li>A empleo va el 0,05% del gasto y a vivienda, el 0,10%. Es casi nada.</li>
<li>El plan de gobierno 2024&ndash;2025 muestra por qu&eacute; pasa esto. Su primera prioridad es la seguridad, y ese gasto subi&oacute; 34,8% entre 2024 y 2025, descontada la inflaci&oacute;n. La asistencia social no est&aacute; entre sus prioridades, y en el mismo per&iacute;odo su gasto baj&oacute; 32,5%.</li>
<li>San Isidro se financia solo. El propio Municipio paga el 64% de su gasto con lo que recauda. Por eso tiene el dinero y la libertad para cambiar en qu&eacute; se gasta. Falta que decidan los vecinos que viven donde est&aacute;n los problemas.</li>
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
<p class="lead">Cada cifra de este documento sale de un documento p&uacute;blico. Debajo de cada cuadro y de cada gr&aacute;fico con datos va su fuente. Las fuentes de lo que dice el texto van en las p&aacute;ginas que siguen a esta nota.</p>
<div class="cols">
<p><b>Fecha de corte.</b> Los datos est&aacute;n actualizados al 20 de septiembre de 2026. Donde el texto dice &laquo;hoy&raquo;, se refiere a esa fecha. Hay cuatro excepciones. Las cuentas de este programa usan datos hasta el 31 de diciembre de 2025. El portal de transparencia se revis&oacute; en septiembre de 2026. Para la valuaci&oacute;n de la tierra del 3.5 se usan las parcelas de ARBA, la agencia de impuestos de la Provincia. Se bajaron el 25 de septiembre de 2026. Por &uacute;ltimo, en la lista de fuentes, cada dato posterior al corte lleva su fecha al lado.</p>
<p>Las cifras de las cuentas salen de tres lugares. Uno son los informes de ejecuci&oacute;n presupuestaria y las rendiciones de cuentas que publica la propia Municipalidad de San Isidro. Otro, los fallos del Tribunal de Cuentas de la Provincia. El tercero, el sistema SIMCo de la Provincia. Los datos de cada zona salen del Censo Nacional 2022, por radio censal, que es la zona m&aacute;s chica para la que el Censo publica datos. Para 2025, las cuentas de este programa reproducen exactamente lo que gast&oacute; y cobr&oacute; el Municipio, sin ninguna diferencia.</p>
<p><b>Las investigaciones de esta edici&oacute;n.</b> Se hicieron en octubre de 2026, s&oacute;lo con fuentes p&uacute;blicas, y cada una est&aacute; en la lista de fuentes que sigue a esta nota. Cada dato dice si se ley&oacute; en la fuente o si es c&aacute;lculo propio. Tratan el ruido y la prueba sellada, los profesores digitales, los costos con la mejor opci&oacute;n en calidad y precio, el puente con las empresas de inteligencia artificial, los espect&aacute;culos, los turnos, g&eacute;nero y discapacidad, las rejas y las barreras de la costa, los tel&eacute;fonos de los inspectores, qui&eacute;n tiene gratis el profesor digital y los mensajes de texto. Los montos en d&oacute;lares se pasan a pesos con el d&oacute;lar de diciembre de 2025, $1.447,84, seg&uacute;n el Banco Central (BCRA).</p>
<p><span class="sg">El modelo, los datos, las series y los catorce gr&aacute;ficos son p&uacute;blicos, y cualquiera puede rehacerlos.</span> Desde que se presenta este programa, se pueden bajar de un repositorio abierto, con las pruebas autom&aacute;ticas que los controlan. Cualquiera puede correrlos y llegar a los mismos n&uacute;meros, o encontrar que no llega.</p>
</div>

<div class="callout a">
<div class="clabel">Los l&iacute;mites</div>
<p>Los datos de los otros 105 municipios vienen de un sitio de terceros, y no se comprobaron uno por uno. Para los l&iacute;mites de las localidades se us&oacute; OpenStreetMap, porque la Municipalidad no publica los suyos. En 2025, el Municipio cambi&oacute; la forma de clasificar su gasto por funci&oacute;n. Por eso, buena parte de las series no se puede comparar de un a&ntilde;o al otro.</p>
</div>

<div class="hairline"></div>
<h2>Las notas de cada cap&iacute;tulo</h2>
<h3>Cap&iacute;tulo 1 &middot; Diagn&oacute;stico</h3>
<div class="note">
<p>Las cifras de las cuentas salen de los informes de ejecuci&oacute;n presupuestaria y de las rendiciones de cuentas que publica la Municipalidad de San Isidro. Tambi&eacute;n salen de los fallos del Honorable Tribunal de Cuentas de la Provincia de Buenos Aires y del sistema SIMCo de la Provincia. Esas tres fuentes se compararon entre s&iacute;. Los datos de cada zona salen del Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022 (INDEC, el instituto nacional de estad&iacute;stica), por radio censal. Salvo que se diga otra cosa, los montos est&aacute;n en pesos constantes de diciembre de 2025, es decir, ajustados por la inflaci&oacute;n hasta esa fecha.</p>
<p>Las seis zonas del 1.1 son las localidades de San Isidro, con los l&iacute;mites de OpenStreetMap, aplicados a los 360 radios censales del INDEC. Cada radio va a la localidad que contiene su punto representativo, que siempre cae dentro del radio. Ninguno de los 360 radios queda afuera, y ninguno est&aacute; en dos localidades.</p>
<p>El domicilio de las empresas que ganaron contratos sale de 3.670 decretos del Bolet&iacute;n Oficial municipal que lo publican. Para calcular la proporci&oacute;n de 2002 a 2017 se dejaron afuera 41 designaciones de inspector t&eacute;cnico. No son contratos con terceros, y el domicilio que publican es el del inspector. Esa proporci&oacute;n cuenta decretos, no montos, porque los montos est&aacute;n en pesos de cada a&ntilde;o, sin ajustar por inflaci&oacute;n. La concentraci&oacute;n usa los 407 decretos que nombran a cada empresa con su monto. Si se suman los 144 que informan s&oacute;lo un total, la concentraci&oacute;n baja al 42,1%.</p>
<p>Los datos de los otros 105 municipios bonaerenses del 1.2 salen de informes de ejecuci&oacute;n RAFAM, procesados por La Verdadera PBA. RAFAM es el sistema contable que la Provincia exige a todos sus municipios. La Verdadera PBA es un sitio de terceros que vuelve a publicar datos oficiales de la Provincia. Para San Isidro, las cifras se compararon con el estado de ejecuci&oacute;n del propio Municipio, y coinciden en las siete categor&iacute;as del gasto por objeto. Las de los otros municipios no se compararon una por una. Se usan para calcular la mediana de la Provincia y el lugar de San Isidro entre los dem&aacute;s.</p>
<p>El gasto devengado total de 2025, 324.304 millones, es el del estado de ejecuci&oacute;n del Municipio por objeto y por programa. Es tambi&eacute;n el que publica RAFAM. En cambio, el estado por finalidad y funci&oacute;n suma 324.133,9 millones, porque deja afuera 170,1 millones de activos financieros.</p>
</div>
<h3>Cap&iacute;tulo 2 &middot; El gobierno actual, medido</h3>
<div class="note">
<p>Todas las cifras salen de documentos publicados por la Municipalidad de San Isidro. Son los estados de ejecuci&oacute;n presupuestaria, la situaci&oacute;n econ&oacute;mico-financiera y el documento &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo;. Tambi&eacute;n salen de los informes de ejecuci&oacute;n RAFAM de los 106 municipios bonaerenses con datos comparables para 2025. La nota del cap&iacute;tulo 1 dice de d&oacute;nde vienen esos datos y qu&eacute; l&iacute;mites tienen. El portal de transparencia se revis&oacute; en septiembre de 2026, y cualquiera puede repetir esa revisi&oacute;n. Alcanza con abrir el portal del Municipio y mirar c&oacute;mo est&aacute; cada una de las siete secciones que enumera el cap&iacute;tulo 5.</p>
<p><b>Cuadro [[n:accion]].</b> El plan &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo; tiene tres prioridades, diecinueve objetivos y setenta y siete metas numeradas, contadas una por una. En el cuadro, las metas est&aacute;n agrupadas por tema, y no se recort&oacute; ninguna. Las cuatro primeras filas cubren las tres prioridades completas del plan.</p>
</div>
<h3>Cap&iacute;tulo 3 &middot; Los fondos</h3>
<div class="note">
<p>Las cuentas de este programa usan cuatro fuentes. Una es la ejecuci&oacute;n presupuestaria 2010&ndash;2025 del Municipio. Otra, los fallos del Tribunal de Cuentas de la Provincia. Adem&aacute;s, usan el Estado de Situaci&oacute;n Econ&oacute;mico-Financiera del Municipio y las planillas de transferencias de la Direcci&oacute;n Provincial de Coordinaci&oacute;n Municipal. A todas las series se les descont&oacute; la inflaci&oacute;n con el &iacute;ndice de precios al consumidor, el IPC (INDEC 2016&ndash;2026; IPC San Luis 2010&ndash;2016, con la forma de unir las dos series explicada).</p>
<p>Los cuatro par&aacute;metros se calcularon con la serie hist&oacute;rica, y no se supusieron. El a&ntilde;o cero reproduce exactamente la ejecuci&oacute;n oficial de 2025. En los treinta y nueve a&ntilde;os-escenario de las cuentas de este programa, un control autom&aacute;tico revisa que los n&uacute;meros cierren. Las cuentas de este programa, los datos y las pruebas son p&uacute;blicos, y cualquiera puede rehacerlos.</p>
<p>El escenario base congela el gasto, descontada la inflaci&oacute;n, en el nivel de 2025. Durante doce a&ntilde;os no hay aumento real de sueldos ni m&aacute;s servicios. La deuda entra con su saldo al 31 de diciembre de 2025: 8.960 millones, la cifra del informe oficial de ese trimestre. No se incluye el informe de junio de 2026, que es posterior. Para comparar la tabla municipal con ARBA, se cruzaron las dos escalas en 69.258 parcelas, y cada parcela pesa seg&uacute;n su superficie. Los metros construidos no son p&uacute;blicos. Por eso, las cuentas de este programa calculan s&oacute;lo sobre la tierra lo que aporta actualizar la tabla de valuaci&oacute;n.</p>
<p><b>Gr&aacute;fico [[n:sinada]].</b> El gasto de este programa tambi&eacute;n entra en las cuentas. En 2029 y 2030, la tabla nueva cobra m&aacute;s que ese gasto. Cobra menos en 2028 y desde 2031 (cuadro [[n:programa_base]]).</p>
<p><b>Cuadro [[n:programa]].</b> Las cifras marcadas son c&aacute;lculos del equipo de este programa, no cifras oficiales. Antes de comprometer cada uno de esos gastos, el Municipio lo va a presupuestar o licitar. Son las cifras de apoyo escolar, las inspecciones grabadas, la plataforma, las pasant&iacute;as, el semillero, los cuidadores y la Escuela N&aacute;utica. Tambi&eacute;n las de los ba&ntilde;os y las clases de la costa, los espect&aacute;culos, lo que se deja de cobrar en multas y los equipos. El resto sale de la ejecuci&oacute;n 2025 publicada y de las cuentas de este programa, que explica el cap&iacute;tulo 3.</p>
<p><b>Los equipos van cada uno en el rengl&oacute;n de su &aacute;rea, y dentro de su monto.</b> Ambiente: seis estaciones que miden el ruido, 313,5 M una sola vez. Formaci&oacute;n: sesenta puestos en seis centros de acceso, 137,1 M una sola vez y 39,5 M por a&ntilde;o de conexi&oacute;n. Salud: trece pantallas que muestran la gente en la guardia, 8,3 M una sola vez. En Ciencia y T&eacute;cnica quedan s&oacute;lo las personas que los instalan (cuadro [[n:equipo]]). Esos precios salen de compras p&uacute;blicas de la Ciudad y de la Naci&oacute;n, llevados a diciembre de 2025 con el IPC. De la Ciudad salen la estaci&oacute;n de ruido, de diciembre de 2024, y la mini PC y el enlace de fibra, de 2026. Las compras de la Naci&oacute;n dan los precios de la notebook, de noviembre de 2025, y del televisor, el escritorio y la silla, de 2026. Como las inspecciones se van a grabar con el tel&eacute;fono del agente, no se compran c&aacute;maras corporales. El an&aacute;lisis de video de seguridad usa las 110 licencias que el Municipio ya compr&oacute; (Licitaci&oacute;n P&uacute;blica 45/2025, Decretos 1372/2025 y 682/2026). Para pasar a pesos lo que est&aacute; en d&oacute;lares, se usa el d&oacute;lar de diciembre de 2025, $1.447,84 (BCRA). Cada cuidador cobra 427.806,54 $ por mes, en la categor&iacute;a asistencia y cuidado de personas, a diciembre de 2025 (Comisi&oacute;n Nacional de Trabajo en Casas Particulares, Resoluci&oacute;n 3/2025). Se suman las cargas del cuadro [[n:equipo]], y se cuentan trece sueldos por a&ntilde;o.</p>
<p><b>Cuadro [[n:tabla2008]].</b> Las parcelas salen del servicio de mapas de ARBA, y &laquo;reconocido&raquo; usa los valores sin redondear. Los valores de ARBA son los de su consulta de valores por macizo (Decreto 790/16), y los municipales, los de la Ordenanza 8373, publicada en la Ordenanza Impositiva 2016. Como en los cap&iacute;tulos 1 y 4, las localidades est&aacute;n armadas con radios censales, y sus l&iacute;mites no siguen el catastro. Cada parcela va a la localidad donde cae. Estas son las circunscripciones y secciones del catastro donde est&aacute; la mayor parte de cada localidad. Acassuso: III-A y III-C. Mart&iacute;nez: III-B, III-D a III-J y IV-A a IV-D. Localidad de San Isidro: I-A, I-B, II-A a II-C, III-K, IV-E, VII-C, VII-D y VII-H. B&eacute;ccar: VII-A, VII-B, VII-E a VII-G y VIII-A a VIII-E. Villa Adelina: V-B, V-D, V-F y V-G. Boulogne Sur Mer: V-A, V-C, V-E y VI-A a VI-J. El 2,9% de las parcelas cae en una secci&oacute;n donde la mayor&iacute;a es de otra localidad. Si se toman las secciones enteras, Acassuso da 2,37 veces Boulogne Sur Mer, en vez de 2,94. Son c&aacute;lculo propio la asignaci&oacute;n parcela por parcela y el cruce por secci&oacute;n, sobre esas fuentes y los radios del Censo 2022. <b>L&iacute;mites.</b> Se comparan proporciones, no pesos, porque las dos escalas usan unidades distintas. De las 69.258 parcelas de la valuaci&oacute;n provincial, 68.644 cruzan con la tabla municipal: el 99,1%. Es s&oacute;lo tierra, sin lo construido. Adem&aacute;s, la valuaci&oacute;n provincial es de un reval&uacute;o de 2016, as&iacute; que no es el precio de mercado de hoy. La comparaci&oacute;n muestra c&oacute;mo ordena cada escala, no cu&aacute;nto vale un inmueble.</p>
<p><b>Cuadro [[n:deuda]].</b> La deuda flotante son pagos de corto plazo, y cambia mucho de un trimestre a otro. En cambio, la deuda consolidada muestra la tendencia. Creci&oacute; de 1.408 a 5.927 millones. Descontada la inflaci&oacute;n, creci&oacute; de 2.660 a 5.072 millones de pesos de diciembre de 2025: casi el doble. El bono de 30.000 millones no est&aacute; en el cuadro, porque se emiti&oacute; el 13 de agosto de 2026 y el &uacute;ltimo informe publicado cierra en junio.</p>
<p><b>Cuadro [[n:programa_base]].</b> Los dos escenarios suponen lo mismo sobre lo que recauda el Municipio y sobre la coparticipaci&oacute;n, el dinero que la Provincia le gira a cada municipio seg&uacute;n una f&oacute;rmula de ley. S&oacute;lo cambian el gasto de este programa y lo que cobra la tabla nueva. Este programa va a empezar en 2028, el primer a&ntilde;o completo del mandato. La &uacute;ltima fila supone que el m&iacute;nimo de la tasa frena todas las subas de los lotes chicos (3.5). Las diferencias se calculan sin redondear.</p>
</div>
<h3>Cap&iacute;tulo 4 &middot; El mecanismo</h3>
<div class="note">
<p>Los art&iacute;culos 60, 132 y 119 de la Ley Org&aacute;nica de las Municipalidades se comprobaron en tres fuentes oficiales distintas. Son la copia de la ley del Ministerio del Interior de la Naci&oacute;n y las recopilaciones de normas, o digestos, del Concejo Deliberante de La Plata y del Municipio de Tigre. El art&iacute;culo 211 de la Constituci&oacute;n provincial se comprob&oacute; en el texto oficial. Para el Decreto 2099/2025 de Pinamar se us&oacute; el Sistema de Boletines Oficiales Municipales de la Provincia. La Ordenanza 6045/1984 de San Isidro se comprob&oacute; en el Digesto del Municipio. Su &uacute;nico cambio posterior es la Ordenanza 7164/1993, que no toca los art&iacute;culos 5, 8, 9 ni 10.</p>
<p>Las cifras de obra p&uacute;blica y su reparto por zona salen de la ejecuci&oacute;n presupuestaria 2025 del Municipio y del Censo 2022 (INDEC), por radio censal. El reparto se calcula sobre 295.978 habitantes, que es la gente que vive en viviendas particulares, como casas o departamentos, seg&uacute;n el Censo 2022. Otras 1.304 personas viven en viviendas colectivas, como los geri&aacute;tricos. Como el Censo no publica esos datos por radio censal, esas personas no se pueden asignar a una zona.</p>
<p>El 1,5% que paga el funcionamiento de las comisiones sale de estos supuestos. Se calcula sobre el sueldo de la categor&iacute;a de ingreso del Municipio: categor&iacute;a 6, 35 horas. Son 432.624 pesos por mes en la Ordenanza 9422 de presupuesto 2026, y 420.507 en pesos de diciembre de 2025. Hay cuatro asambleas por zona y por a&ntilde;o, 24 en total, como el ciclo m&iacute;nimo de la Ciudad de Buenos Aires. Cada una tiene dos cuidadoras, cuatro horas cada una: medio mill&oacute;n por a&ntilde;o. Una obra promedio es de 100 millones, lo que da 289 obras el a&ntilde;o 4. Por cada obra cobran tres vecinos, cada uno un cuarto de ese sueldo: 91 millones. Tambi&eacute;n hay un 3% de administraci&oacute;n sobre lo que hacen las propias comisiones. Si hacen un cuarto de la partida vecinal, el dinero que el presupuesto reserva para la obra que deciden los vecinos, son 217 millones. En total, son 308 millones, el 1,1%. Con obras promedio de 50 millones son 400 millones, el 1,4%. As&iacute;, el 1,5% alcanza en los dos casos. Para el panel sorteado se cuentan 40 personas y cuatro sesiones, y cada persona cobra un d&iacute;a de ese sueldo por sesi&oacute;n.</p>
<p>Las carencias de la franja baja de la costa se cuentan en la zona San Isidro. Hay tres radios vecinos de la fracci&oacute;n 02 (un grupo de radios censales), los terminados en 03, 04 y 05. Tienen entre 4,3% y 11,8% de hogares con necesidades b&aacute;sicas insatisfechas (NBI), y entre 24,8% y 63,1% sin gas de red. Para toda la zona, los promedios son 1,83% y 16,64%. En Acassuso no hay un bols&oacute;n de pobreza. Sus diecis&eacute;is radios tienen NBI de 0,0% a 2,4%, y el 19,48% sin gas de red est&aacute; repartido parejo. El &uacute;nico radio donde la falta de cloaca pesa es el 067560403, con 17,4% sobre 316 hogares, y tiene 0,6% de NBI.</p>
<p>Los casos de panel sorteado son experiencias en marcha o documentadas. Son Ostbelgien, Winterthur, Darebin, Melbourne, Bolonia, Barcelona, Par&iacute;s, Se&uacute;l, Reikiavik, Nueva York, Chicago, C&oacute;rdoba y la Ciudad de Buenos Aires. De los estudios acad&eacute;micos sobre sorteo y control popular sale la idea de hacer una pregunta concreta, y de evitar que un grupo se quede con el panel. Ning&uacute;n caso se puede copiar sin adaptarlo. Barcelona y Par&iacute;s no tienen los l&iacute;mites de la Ley Org&aacute;nica bonaerense. La Ciudad de Buenos Aires tiene comunas con autoridades electas, que San Isidro no tiene.</p>
<p><b>Cuadro [[n:equipo]].</b> Los sueldos son brutos y de mercado, seg&uacute;n la mediana de la encuesta de Sysarmy 2026.1. Una persona con mucha experiencia cobra 3,40 M por mes, una con experiencia media 2,43 M y una principiante 1,50 M. Se cuentan trece sueldos por a&ntilde;o, m&aacute;s las cargas del empleador. Son el 16,8% de contribuciones y la ART. Las contribuciones son el 12% para el IPS, la caja de jubilaciones de la Provincia (Decreto-Ley 9650/80), y el 4,8% para el IOMA, la obra social de la Provincia (Decreto 2655/04). La ART es el seguro de riesgos del trabajo que contrat&oacute; el Municipio: 3,275% m&aacute;s una suma fija por persona (Decreto 1587/2025). Cada pasante cobra 240.000 $ por mes, con ART y salud. Para las 10 personas nuevas y las 8 de las &aacute;reas, el c&aacute;lculo es propio, tarea por tarea, con esos mismos sueldos. Infraestructura y licencias van con los precios que publica cada proveedor, consultados en octubre de 2026, y el d&oacute;lar de diciembre de 2025, $1.447,84 (BCRA). Incluyen lo que usan los vecinos, las 160 asociaciones inscriptas al 40% de su cupo, los alumnos, el semillero y las herramientas del equipo. Ning&uacute;n aviso va a ir por WhatsApp, sino por la propia inteligencia artificial del Municipio. El costo de la auditor&iacute;a externa es el 10% del equipo de las primeras 49 personas, sin cargas. Empleados que ya cobran su sueldo van a cambiar de tarea para dar la ayuda en cada una de las seis zonas.</p>
</div>
<h3>Cap&iacute;tulo 5 &middot; Qu&eacute; hacemos en cada &aacute;rea</h3>
<div class="note">
<p>El gasto por funci&oacute;n sale del estado de ejecuci&oacute;n presupuestaria acumulado de todo 2025 del Municipio de San Isidro. Para los cambios entre 2024 y 2025 se usan pesos constantes de diciembre de 2025, descontada la inflaci&oacute;n con el IPC. Los datos de cada zona salen del Censo 2022 (INDEC), por radio censal. Cu&aacute;nto cuesta cada propuesta est&aacute; en el cap&iacute;tulo 3.</p>
<p>En 2025 el Municipio dividi&oacute; su gasto en veinte funciones, y en 2024 en catorce. El cap&iacute;tulo 5 s&oacute;lo usa los cambios de un a&ntilde;o al otro de las funciones que est&aacute;n en los dos a&ntilde;os, y cuyo grupo no sum&oacute; funciones nuevas. Las dem&aacute;s se marcan como no comparables.</p>
<p>La historia de la recolecci&oacute;n se arm&oacute; leyendo el texto de 527 boletines quincenales y 324 ediciones extra, de 2002 a 2024. Tambi&eacute;n se ley&oacute; el visor nuevo del Bolet&iacute;n Oficial, de 2024 a 2026. En la plataforma vieja, que publica hasta marzo de 2024, s&oacute;lo se puede buscar por el t&iacute;tulo del bolet&iacute;n, y no por el texto de los decretos. El Decreto 29/2003 cita el contrato de 1998.</p>
<p>Las pruebas sobre seguridad son de otros pa&iacute;ses. La revisi&oacute;n de 65 estudios es de la Campbell Collaboration, actualizada por Braga y otros. En Dallas, la evaluaci&oacute;n mide el primer a&ntilde;o del plan de la ciudad. Usa el m&eacute;todo de diferencias en diferencias, que compara lo que cambi&oacute; donde se aplic&oacute; el plan con lo que cambi&oacute; donde no se aplic&oacute;. Los 35,5 minutos por turno salen de un experimento controlado en la calle. Son estudios sobre polic&iacute;as, no sobre patrullas municipales argentinas. Concentrar el patrullaje es una idea que se puede aplicar ac&aacute;. No est&aacute; demostrado cu&aacute;nto bajar&iacute;a el delito en este caso. Para Tigre, los datos son comunicados del propio Municipio de Tigre.</p>
<p>Bezos hizo su propuesta en el America Business Forum de Miami, en noviembre de 2025. La Ciudad de Miami anunci&oacute; que adoptaba la plataforma en marzo de 2026. El caso de Miami sirve como referencia, pero todav&iacute;a no tiene resultados medidos.</p>
<p><b>Cuadro [[n:piramide]].</b> En el mandato entran 231 y 231 el primer a&ntilde;o, 412 y 412 el segundo, 355 y 356 el tercero, y 464 y 464 el cuarto. Cada uno pasa seis meses por el Municipio y seis por las empresas. El equipo de la plataforma (cuadro [[n:equipo]]) es parte de los pasantes y principiantes del Municipio (cuadro [[n:proyectos]]), y ellos son parte de esta pir&aacute;mide.</p>
<p><b>Cuadro [[n:reparto_empleo]].</b> Los 3 millones por persona pagan los dos a&ntilde;os de formaci&oacute;n. Quien recibe al pasante paga su pasant&iacute;a. Durante los dos primeros a&ntilde;os, la formaci&oacute;n usa toda la partida de empleo, porque todav&iacute;a no hay egresados para contratar. Entran 462 y 824, en vez de 277 y 494, y egresan 1.286 en el mandato. El tercer a&ntilde;o vuelve este reparto. La parte de salud de los meses 12 a 18 se pagaba con la contrataci&oacute;n de desarrollos. Esos dos a&ntilde;os, esa parte sale del gasto flexible libre (el gasto flexible es la parte del presupuesto que no est&aacute; atada a sueldos, deudas ni contratos firmados).</p>
<p><b>Cuadro [[n:hoy_propuesta]].</b> Mi Primer Empleo da talleres de curr&iacute;culum y contacto con empresas, y tiene el portal de empleo: 131 empresas y unos 600 puestos, seg&uacute;n el Municipio. Las pr&aacute;cticas de Medicina se hacen en hospitales y centros de salud. Participan la Barcel&oacute; (Decreto 374/2025, sin gasto del Municipio), la Universidad Cat&oacute;lica Argentina (UCA, Decreto 498/2026) y, de 2026 a 2028, la Favaloro, seg&uacute;n una nota del Municipio que public&oacute; InfoBAN. En Veterinaria, las pr&aacute;cticas son en Zoonosis, con la Universidad de Buenos Aires (UBA), por hasta dos meses (Decreto 775/2026). Ni las de la Barcel&oacute; ni las de Veterinaria se pagan, y los convenios de la Favaloro y de la UCA no est&aacute;n publicados. El Municipio paga a los 15 pasantes de las fiscal&iacute;as, por un convenio de 2003 con el Ministerio P&uacute;blico. Cobran 747.500 $ por mes desde marzo de 2026. Son becas dadas por decreto (Decreto 298/2026), fuera del r&eacute;gimen de pasant&iacute;as. No se publican sus horas, y no se encontr&oacute; qu&eacute; cobertura tienen. La UNSO, la universidad nacional con sede en San Isidro, tiene pasant&iacute;as pagas con pymes, sin un convenio vigente con el Municipio. Su convenio de 2021 con el Municipio no tiene movimientos desde 2022 (Zona Norte Visi&oacute;n, 16 de junio de 2025). Un comunicado del Municipio, citado por Zona Norte Visi&oacute;n el 11 de agosto de 2026, da el dato de los m&aacute;s de 300 vecinos con trabajo. Desde 2018 ya no se publica d&oacute;nde est&aacute;n las empresas que cobran del Municipio (1.2).</p>
</div>
<h3>Cap&iacute;tulo 6 &middot; El plan, con fechas</h3>
<div class="note">
<p>El cap&iacute;tulo 6 no trae datos nuevos, salvo el caso de Los &Aacute;ngeles del cuadro de riesgos, que sale del LA School Report (23 de julio de 2024). Para el plan B de la cara y del programa del profesor digital se usan los precios, las licencias y los t&eacute;rminos de uso para menores que publica cada proveedor, consultados el 5 de octubre de 2026. Cada cifra sale del cap&iacute;tulo que la explica. Los datos de cada zona salen del cap&iacute;tulo 1. La revisi&oacute;n del plan de gobierno 2024&ndash;2025 sale del cap&iacute;tulo 2. Las cuentas de este programa y los n&uacute;meros de hoy del presupuesto est&aacute;n en el cap&iacute;tulo 3. En el cap&iacute;tulo 4 est&aacute;n la rampa, es decir, c&oacute;mo crece la partida vecinal a&ntilde;o a a&ntilde;o, y la f&oacute;rmula de reparto. Por &uacute;ltimo, el estado del portal de transparencia sale del cap&iacute;tulo 5.</p>
<p>Los 4.616 hogares sin cloaca de Boulogne y B&eacute;ccar est&aacute;n contados hogar por hogar en los 360 radios censales del Censo 2022, y no calculados con un porcentaje. Las dos zonas son las localidades, con los l&iacute;mites de OpenStreetMap, aplicados a esos radios. El cap&iacute;tulo 4 explica por qu&eacute; se cuentan hogares y no porcentajes.</p>
<p><b>Cuadro [[n:compromisos]].</b> Los dos primeros compromisos van a ir juntos a la sesi&oacute;n extraordinaria. Sin partida, no hay asamblea que decida. Si no se derogan los art&iacute;culos 8 a 10 de la Ordenanza 6045, la asociaci&oacute;n que decide puede ser disuelta por el Departamento Ejecutivo (el intendente y sus secretar&iacute;as, que gobiernan el Municipio), que es el mismo al que le dijo que no. Tres compromisos, el 15, el 16 y el 21, dependen s&oacute;lo del Ejecutivo. Para la detecci&oacute;n en el momento se van a usar las 110 licencias de an&aacute;lisis de video que el Municipio ya compr&oacute;. No hay nada que licitar, y va a funcionar a los cien d&iacute;as. Las inspecciones se van a grabar con el tel&eacute;fono del agente. El decreto va a salir a los cien d&iacute;as, con el convenio de 24 cuotas sin inter&eacute;s con el banco que paga los sueldos. Desde el mes 9, la grabaci&oacute;n va a funcionar primero con los inspectores y los agentes de tr&aacute;nsito. En una segunda etapa va a entrar la patrulla. La ordenanza que anula el acta hecha sin grabaci&oacute;n sellada y subida, y la clausura o la habilitaci&oacute;n que salgan de esa inspecci&oacute;n, va a ir m&aacute;s tarde. Su texto est&aacute; en el anexo. Por decreto van a empezar la denuncia del comerciante y el registro de instructores y artistas. Despu&eacute;s, las Ordenanzas 4 y 14 los van a dejar fijos.</p>
</div>
""")
