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

def ex(kind, title, sub=None, img=None, src=None, note=None, cls=""):
    """Bloque de exhibit: etiqueta numerada, titulo-conclusion, grafico y fuente."""
    k = exn()
    lbl = "GR&Aacute;FICO" if kind == "g" else "CUADRO"
    h = [f'<div class="ex"><div class="exlabel">{lbl}&nbsp;{k}</div>',
         f'<div class="extitle">{title}</div>']
    if sub:  h.append(f'<div class="exsub">{sub}</div>')
    if img:  h.append(f'<div class="chart {cls}"><img src="asset:{img}" alt=""></div>')
    if src:  h.append(f'<p class="cap"><b>Fuente:</b> {src}</p>')
    if note: h.append(f'<p class="cap"><b>Nota:</b> {note}</p>')
    h.append('</div>')
    return "".join(h)

def exhead(kind, title, sub=None):
    k = exn()
    lbl = "GR&Aacute;FICO" if kind == "g" else "CUADRO"
    s = f'<div class="exsub">{sub}</div>' if sub else ""
    return (f'<div class="ex"><div class="exlabel">{lbl}&nbsp;{k}</div>'
            f'<div class="extitle">{title}</div>{s}</div>')

def fig(img, cap):
    if "." not in img: img += ".jpg"
    return f'<figure><img src="asset:{img}" alt=""><figcaption>{cap}</figcaption></figure>'

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
 ("i", "Ocho puntos, y los primeros cien d&iacute;as", "sintesis"),
 ("g", "1 &middot; Diagn&oacute;stico", None),
 ("i", "1.1 &nbsp;Dos partidos dentro del mismo partido", "cap1a"),
 ("i", "1.2 &nbsp;El municipio invierte m&aacute;s que casi todos. Y no llega.", "cap1a2"),
 ("i", "1.3 &nbsp;D&oacute;nde no va el dinero", "cap1a2"),
 ("i", "1.4 &nbsp;Por qu&eacute; pasa esto: est&aacute; escrito", "cap1b"),
 ("i", "1.5 &nbsp;San Isidro se financia solo. Eso cambia todo.", "cap1b"),
 ("i", "1.6 &nbsp;Lo que dice este cap&iacute;tulo, en cuatro l&iacute;neas", "cap1b"),
 ("g", "2 &middot; La gesti&oacute;n, medida", None),
 ("i", "2.1 &nbsp;Ejecutar el presupuesto no es prestar el servicio", "cap2"),
 ("i", "2.2 &nbsp;Lo que s&iacute; se puede probar: la cobranza se deterior&oacute;", "cap2"),
 ("i", "2.3 &nbsp;Lo que se prometi&oacute; publicar y no est&aacute; publicado", "cap2b"),
 ("i", "2.4 &nbsp;El hallazgo central: el plan no nombra el empleo, la vivienda ni la salud", "cap2b"),
 ("i", "2.5 &nbsp;Lo que dice este cap&iacute;tulo, en cuatro l&iacute;neas", "cap2b"),
 ("g", "3 &middot; Los fondos", None),
 ("i", "3.1 &nbsp;La trampa contable que casi nos hace decir lo contrario", "cap3a"),
 ("i", "3.2 &nbsp;Los cuatro n&uacute;meros que gobiernan el futuro fiscal", "cap3a"),
 ("i", "3.3 &nbsp;C&oacute;mo quedan las cuentas si nadie cambia nada", "cap3a"),
 ("i", "3.4 &nbsp;Cu&aacute;nto cuesta este programa", "cap3b"),
 ("i", "3.5 &nbsp;De d&oacute;nde salen los fondos", "cap3b2"),
 ("i", "3.6 &nbsp;Qu&eacute; habr&iacute;a que vigilar", "cap3b3"),
 ("i", "3.7 &nbsp;Lo que dice este cap&iacute;tulo, en cinco l&iacute;neas", "cap3b3"),
 ("g", "4 &middot; El mecanismo", None),
 ("i", "4.1 &nbsp;El l&iacute;mite legal: lo que un intendente no puede delegar", "cap4a"),
 ("i", "4.2 &nbsp;La deuda que la Provincia tiene con sus municipios", "cap4a"),
 ("i", "4.3 &nbsp;Cu&aacute;nto dinero: el n&uacute;mero", "cap4a"),
 ("i", "4.4 &nbsp;C&oacute;mo se reparte: por poblaci&oacute;n y por necesidad contada", "cap4a2"),
 ("i", "4.5 &nbsp;Qui&eacute;n decide y qui&eacute;n ejecuta: dos capas", "cap4b"),
 ("i", "4.6 &nbsp;C&oacute;mo se constituye una comisi&oacute;n, y c&oacute;mo rinde", "cap4b"),
 ("i", "4.7 &nbsp;El Concejo Deliberante: diez bloques y ninguna mayor&iacute;a", "cap4bb2"),
 ("i", "4.8 &nbsp;Por qu&eacute; las dos capas juntas cambian todo", "cap4bb2"),
 ("i", "4.9 &nbsp;Las otras dos facultades", "cap4b2"),
 ("i", "4.10 &nbsp;El primer acto de gobierno: derogar tres art&iacute;culos", "cap4b2"),
 ("i", "4.11 &nbsp;La aplicaci&oacute;n: el sistema de informaci&oacute;n del Municipio", "cap4b2"),
 ("i", "4.12 &nbsp;A qui&eacute;n le molesta esto", "cap4bc"),
 ("i", "4.13 &nbsp;Lo que dice este cap&iacute;tulo, en seis l&iacute;neas", "cap4bc"),
 ("g", "5 &middot; Qu&eacute; hacemos en cada &aacute;rea", None),
 ("i", "5.1 &nbsp;C&oacute;mo leer este cap&iacute;tulo", "cap5a"),
 ("i", "5.2 &nbsp;D&oacute;nde va hoy cada peso", "cap5a"),
 ("i", "5.3 &nbsp;Empleo", "cap5a2"),
 ("i", "5.4 &nbsp;Vivienda y servicios b&aacute;sicos", "cap5a3"),
 ("i", "5.5 &nbsp;Ambiente", "cap5b"),
 ("i", "5.6 &nbsp;Salud", "cap5bb"),
 ("i", "5.7 &nbsp;Seguridad", "cap5bc"),
 ("i", "5.8 &nbsp;Educaci&oacute;n y cultura", "cap5b2"),
 ("i", "5.9 &nbsp;Digitalizaci&oacute;n: que el tr&aacute;mite tarde diez segundos", "cap5b2a2"),
 ("i", "5.10 &nbsp;Transparencia", "cap5b2b"),
 ("i", "5.11 &nbsp;Transporte y comercio", "cap5b2b"),
 ("i", "5.12 &nbsp;Los que tienen que ejecutar todo esto", "cap5b2b"),
 ("i", "5.13 &nbsp;Ni&ntilde;ez, personas mayores, g&eacute;nero y discapacidad", "cap5b3"),
 ("i", "5.14 &nbsp;Lo que no est&aacute; en este cap&iacute;tulo, y por qu&eacute;", "cap5b3"),
 ("i", "5.15 &nbsp;Lo que dice este cap&iacute;tulo, en siete l&iacute;neas", "cap5b3"),
 ("g", "6 &middot; El plan, con fechas", None),
 ("i", "6.1 &nbsp;Los primeros cien d&iacute;as", "cap6"),
 ("i", "6.2 &nbsp;La rampa de la obra vecinal, a&ntilde;o por a&ntilde;o", "cap6"),
 ("i", "6.3 &nbsp;Las metas verificables del mandato", "cap6b"),
 ("i", "6.4 &nbsp;El calendario del mandato, mes por mes", "cap6b"),
 ("i", "6.5 &nbsp;Qu&eacute; no prometemos, y de qui&eacute;n depende", "cap6b"),
 ("i", "6.6 &nbsp;Qu&eacute; puede salir mal", "cap6c"),
 ("i", "6.7 &nbsp;Lo que dice este cap&iacute;tulo, en cinco l&iacute;neas", "cap6c"),
 ("g", "Cierre", None),
 ("i", "Para cerrar", "cierre"),
 ("g", "Nota de m&eacute;todo", None),
 ("i", "C&oacute;mo est&aacute; construido, y qu&eacute; l&iacute;mites tiene", "metodo"),
 ("g", "Anexo &middot; El articulado", None),
 ("i", "La partida vecinal, el sistema de informaci&oacute;n, la base de valuaci&oacute;n y la fiscalizaci&oacute;n", "ordenanza"),
 ("i", "Las cinco ordenanzas restantes, y las metas que no llevan ninguna", "ordenanza2"),
 ("g", "Glosario", None),
 ("i", "Dieciocho palabras, explicadas", "glosario"),
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
    return style + '<h1>&Iacute;ndice</h1>' + "".join(rows)


INDICE = dict(id="indice", runhead=RH, html=_indice())


# =====================================================================
# INTRODUCCION
# =====================================================================
INTRO = dict(id="introduccion", runhead=RH, html="""
<h1>Introducci&oacute;n</h1>
<p class="lead">En San Isidro hay <b>25.165 hogares que cocinan con garrafa</b> y 6.488 que no tienen
cloaca. La mayor&iacute;a est&aacute; en Boulogne y en B&eacute;ccar: seis de cada diez sin gas, siete
de cada diez sin cloaca.</p>

<h2>La pregunta</h2>
<p>En el pr&oacute;logo de su plan de gobierno, &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo;,
el intendente escribe: &laquo;Estas prioridades de gesti&oacute;n no las fijamos nosotros, sino que
responden a haber escuchado sus principales problemas y necesidades&raquo;. <b>&iquest;A qui&eacute;n se
escuch&oacute;, y c&oacute;mo, para que el empleo y la vivienda no aparecieran nunca?</b></p>
<div class="pull"><p>Las palabras empleo, vivienda, salud, pobreza, agua y cloaca no aparecen en ninguna
parte del programa actual de gobierno.</p></div>

<h2>Por qu&eacute; el dinero va a lo que se ve</h2>
<p class="lead">Hay dos maneras de gobernar pensando en la pr&oacute;xima elecci&oacute;n, y ninguna de
las dos es gobernar.</p>
<div class="cols">
<p><b>La primera es administrar para la foto.</b> Se elige la obra que se ve, la que se termina adentro
del mandato, la que se inaugura con cinta. No hace falta que nadie decida de mala fe: alcanza con que el
criterio sea &eacute;se. <span class="sg">Alumbrado p&uacute;blico recibe 10.313 millones al a&ntilde;o y
agua y alcantarillado 3.320.</span> Una cloaca no se inaugura con cinta.</p>
<p><b>La segunda es repartir.</b> Es la de los gobiernos populistas: se sostiene un voto entregando, y
el que entrega necesita que el otro siga necesitando. <b>Este programa no reparte un peso.</b> Los
7.730,9 millones de empleo y vivienda pagan formaci&oacute;n, contrataci&oacute;n e infraestructura, y
ninguno es una transferencia a una persona.</p>
<p><b>Hay una tercera, y es la de este programa: administrar para que crezca.</b> Que San Isidro
funcione mejor cuando termine el mandato que cuando empez&oacute;: <b>menos hogares sin cloaca y sin gas
de red</b>, <b>m&aacute;s gente formada y con trabajo</b>, y <b>los vecinos decidiendo en qu&eacute; se
gasta la obra de su barrio</b>. Ninguna de las tres da una foto el d&iacute;a que se hace.</p>
<p><b>Somos una propuesta de gobierno que gestiona.</b> Que administra para que el partido crezca, y
<span class="sg">ese crecimiento econ&oacute;mico es de todos</span>. Por eso el cap&iacute;tulo 4 no pide
un peso nuevo: mueve <span class="sg">qui&eacute;n decide</span> sobre la mitad de la obra p&uacute;blica
que el Municipio ya hace.</p>
</div>
<p style="margin-top:14pt;font-style:italic;color:var(--taupe);font-size:9pt">Jos&eacute; Luis Casares,
candidato a intendente de San Isidro.</p>
""" + fig("f_costanera", "La costanera de San Isidro. Ilustraci&oacute;n."))


# =====================================================================
# CAPITULO 1 — parte A
# =====================================================================
C1A = dict(id="cap1a", runhead=RH, html=fig("f_catedral",
    "El casco hist&oacute;rico. Ilustraci&oacute;n.") + """
<h1><span class="n">1</span>Diagn&oacute;stico</h1>
<div class="stand">San Isidro invierte en obra p&uacute;blica m&aacute;s que el 96% de los municipios bonaerenses y destina el 0,05% de su presupuesto a empleo.</div>

<h2><span class="n">1.1</span>Dos partidos dentro del mismo partido</h2>
<div class="cols">
<p>San Isidro tiene 297.282 habitantes y 110.559 hogares (Censo 2022). Repartidos entre esos hogares, el
municipio gast&oacute; en 2025 el equivalente a <b>1.090.897 pesos por habitante</b>.</p>
<p>No es poco dinero. Y sin embargo el partido est&aacute; partido en dos, y la l&iacute;nea es
geogr&aacute;fica: las localidades del oeste y del norte contra las de la costa sur.</p>
</div>
""" + exhead("c", "Seis localidades, dos realidades: el oeste y el norte contra la costa sur",
             "Los cuatro primeros indicadores est&aacute;n medidos sobre hogares; el &uacute;ltimo, sobre poblaci&oacute;n.") + """
<table>
<colgroup><col style="width:126pt"><col><col><col><col><col><col></colgroup>
<tr class="hd"><th>Zona</th><th class="r">Poblaci&oacute;n</th><th class="r">NBI</th>
<th class="r">Sin cloaca</th><th class="r">Sin gas de red</th><th class="r">Hacinamiento</th>
<th class="r">Universitario</th></tr>
<tr class="hi"><td class="l">Boulogne Sur Mer</td><td class="n">74.832</td><td class="n"><b>5,09%</b></td><td class="n">9,16%</td><td class="n">27,64%</td><td class="n">12,42%</td><td class="n">9,00%</td></tr>
<tr class="hi"><td class="l">B&eacute;ccar</td><td class="n">63.719</td><td class="n"><b>4,93%</b></td><td class="n">10,59%</td><td class="n">37,27%</td><td class="n">12,67%</td><td class="n">12,85%</td></tr>
<tr><td class="l">Villa Adelina</td><td class="n">35.542</td><td class="n">2,73%</td><td class="n">5,54%</td><td class="n">15,59%</td><td class="n">7,28%</td><td class="n">9,32%</td></tr>
<tr><td class="l">San Isidro</td><td class="n">45.872</td><td class="n">1,83%</td><td class="n">2,97%</td><td class="n">16,64%</td><td class="n">4,18%</td><td class="n">25,25%</td></tr>
<tr><td class="l">Mart&iacute;nez</td><td class="n">64.978</td><td class="n">1,43%</td><td class="n">1,81%</td><td class="n">14,55%</td><td class="n">2,96%</td><td class="n">24,39%</td></tr>
<tr><td class="l">Acassuso</td><td class="n">11.035</td><td class="n">0,94%</td><td class="n">2,12%</td><td class="n">19,48%</td><td class="n">2,50%</td><td class="n">32,28%</td></tr>
</table>
<p class="cap"><b>Fuente:</b> INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022,
procesado con Redatam 7.</p>
<p class="cap"><b>Nota:</b> los l&iacute;mites de localidad son de OpenStreetMap, que no es fuente
oficial, proyectados sobre los radios censales del INDEC.</p>

<p>Un hogar de Boulogne o B&eacute;ccar tiene <span class="sg">tres veces y media m&aacute;s
probabilidad</span> de tener necesidades b&aacute;sicas insatisfechas que uno de Mart&iacute;nez.
<span class="sg">Cinco veces y media</span> de no tener cloacas. <span class="sg">Cuatro veces</span> de
vivir en condiciones de hacinamiento. Y <span class="sg">menos de la mitad de probabilidad</span> de que
alguien en la casa haya terminado la universidad.</p>
""" + ex("g", "El partido se parte en dos: el oeste y el norte contra la costa sur",
        "Coloreadas por porcentaje de hogares con necesidades b&aacute;sicas insatisfechas. El partido entero promedia 3,16%.",
        "ex01.png",
        "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7; l&iacute;mites de localidad de OpenStreetMap.",
        "OpenStreetMap no es fuente oficial. Cada radio censal va a la localidad que contiene su punto representativo; los 360 caen dentro de exactamente una.")
+ ex("g", "Boulogne y B&eacute;ccar concentran el 67% de la carencia del partido",
     "Cuatro indicadores por zona, ordenadas de peor a mejor por NBI. El NBI del partido es 3,16%.",
     "ex02.png",
     "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7.")
+ ex("g", "El mismo orden, dado vuelta: donde falta todo, tampoco hay t&iacute;tulo universitario",
     "Poblaci&oacute;n con universidad completa o m&aacute;s, por zona. Mismo orden que el gr&aacute;fico anterior.",
     "ex03.png",
     "INDEC, Censo Nacional de Poblaci&oacute;n, Hogares y Viviendas 2022, procesado con Redatam 7.") + """
<h3>El dato que resume todo</h3>
<p class="tight">En Boulogne Sur Mer y B&eacute;ccar viven <b>138.551 personas en 47.193 hogares: el
46,8% del partido.</b></p>
<div class="pull"><p>Casi la mitad de San Isidro vive donde est&aacute; el 60% de los 25.165 hogares sin
gas de red y el 71% de los 6.488 que no tienen cloaca.</p></div>
""" + duo("f_boulogne", "f_martinez",
          "Boulogne Sur Mer y Mart&iacute;nez. La misma distancia al r&iacute;o, la misma tasa municipal. Ilustraci&oacute;n.") + """

<h2><span class="n">1.2</span>El municipio invierte m&aacute;s que casi todos. Y no llega.</h2>
<div class="cols">
<p><b>El dato.</b> Sobre 106 municipios bonaerenses con datos de ejecuci&oacute;n 2025, San Isidro
est&aacute; <b>cuarto en inversi&oacute;n en obra p&uacute;blica</b>: destina el <b>17,8%</b> de su gasto,
contra una mediana provincial de <b>5,4%</b>. Invierte m&aacute;s del triple que el municipio
bonaerense t&iacute;pico.</p>
<p><b>Y ah&iacute; est&aacute; la pregunta.</b> Si invierte tanto y todav&iacute;a hay 6.488 hogares sin
cloaca, no es porque no haya con qu&eacute;: es porque <span class="sg">el dinero va a lo que se
ve</span>.</p>
</div>
""" + exhead("c", "San Isidro contra sus vecinos y contra la mediana de la Provincia",
             "Ejecuci&oacute;n 2025, gasto devengado.") + """
<table>
<colgroup><col style="width:190pt"><col><col></colgroup>
<tr class="hd"><th>Municipio</th><th class="r">Gasto devengado total 2025 (M$)</th>
<th class="r">Obra p&uacute;blica %</th></tr>
<tr class="hi"><td class="l">San Isidro</td><td class="n">324.304</td><td class="n"><b>17,8</b></td></tr>
<tr><td class="l">Vicente L&oacute;pez</td><td class="n">318.824</td><td class="n">7,4</td></tr>
<tr><td class="l">Tigre</td><td class="n">400.156</td><td class="n">11,4</td></tr>
<tr><td class="l">San Fernando</td><td class="n">148.932</td><td class="n">6,9</td></tr>
<tr><td class="l">San Mart&iacute;n</td><td class="n">276.003</td><td class="n">1,5</td></tr>
<tr><td class="m">Mediana provincial</td><td class="n m">&mdash;</td><td class="n m">5,4</td></tr>
</table>
<p class="cap"><b>Fuente:</b> RAFAM 2025, v&iacute;a La Verdadera PBA. San Isidro validado contra la
ejecuci&oacute;n del propio Municipio; los otros 105, no.</p>

<div class="cols">
<p><b>Y esa proporci&oacute;n alta se aplica sobre un total que viene cayendo.</b> Medido desde su
m&aacute;ximo de 2017, <b>el gasto real del Municipio cay&oacute; 24,4%</b>; medido desde 2010
est&aacute; 13,1% por encima.</p>
<p><b>La ca&iacute;da atraviesa el per&iacute;odo entero.</b> Entre 2017 y 2022 el gasto real
cay&oacute; 17,2%, y entre 2022 y 2025 otro 8,8%. Los a&ntilde;os peores fueron 2019, 2020 y 2021, con
&minus;9,1%, &minus;10,4% y &minus;1,7%. <b>En quince a&ntilde;os ninguna gesti&oacute;n ampli&oacute; la
capacidad de hacer del Municipio</b>, y &eacute;sa es la restricci&oacute;n real sobre la que hay que
trabajar.</p>
</div>

<h3>En qu&eacute; se invierte: la pregunta que falta hacer</h3>
""" + exhead("c", "Alumbrado p&uacute;blico recibe el triple que el agua y las cloacas",
             "Gasto devengado 2025 dentro de la finalidad Servicios Sociales: Urbanismo abierto en sus cinco subfunciones, y la funci&oacute;n Agua potable y alcantarillado.") + """
<table>
<colgroup><col style="width:300pt"><col></colgroup>
<tr class="hd"><th>Funci&oacute;n</th><th class="r">Devengado 2025</th></tr>
<tr><td class="l">Recolecci&oacute;n de residuos, barrido y limpieza</td><td class="n">49.270 M</td></tr>
<tr class="hi"><td class="l">Alumbrado p&uacute;blico</td><td class="n"><b>10.313 M</b></td></tr>
<tr><td class="l">Otros servicios urbanos</td><td class="n">5.829 M</td></tr>
<tr><td class="l">Planeamiento y desarrollo urbano</td><td class="n">4.054 M</td></tr>
<tr><td class="l">Cementerios</td><td class="n">845 M</td></tr>
<tr class="hi"><td class="l">Agua potable y alcantarillado</td><td class="n"><b>3.320 M</b></td></tr>
</table>
<p class="cap"><b>Fuente:</b> Municipio de San Isidro, Estado de Ejecuci&oacute;n de Gastos por Finalidad
y Funci&oacute;n, ejercicio 2025. Subfunciones 3.9.1 a 3.9.9 y funci&oacute;n 3.8.</p>
<p class="cap"><b>Nota:</b> son gastos por destino, no por objeto: dentro de cada funci&oacute;n hay
sueldos, contratos de servicio y obra. Los 49.270 millones de residuos son sobre todo el contrato de
recolecci&oacute;n, que es un servicio diario y no una inversi&oacute;n. El agrupamiento es el del
clasificador provincial (RAFAM), no una elecci&oacute;n de este programa.</p>
<h3>La mitad de la obra se adjudicaba a empresas de afuera del partido</h3>
<div class="cols">
<p>Hay un dato que el Municipio public&oacute; durante quince a&ntilde;os y hoy ya no publica: el
domicilio de la empresa a la que se le adjudica cada obra.</p>
<p><b>Entre 2002 y 2017, de los 3.054 actos de adjudicaci&oacute;n con domicilio publicado, el 49,6% fue
a empresas con domicilio en San Isidro y el 50,4% a empresas de afuera.</b> Y la proporci&oacute;n local
ven&iacute;a cayendo a&ntilde;o a a&ntilde;o: 53,1% en 2013, 46,5% en 2015, <b>39,4% en 2017</b>.</p>
<p>Entre 2011 y 2017 el domicilio figuraba en el 62% al 82% de los actos. <b>La pr&aacute;ctica se abandon&oacute; en 2018,
bajo la gesti&oacute;n anterior, y la actual no la retom&oacute;.</b> De los 573 decretos de
adjudicaci&oacute;n publicados desde diciembre de 2023, <span class="sg">ninguno dice d&oacute;nde
est&aacute; el que cobra</span>.</p>
</div>

<h3>En cu&aacute;ntas manos queda la obra</h3>
<div class="cols">
<p>En los 407 decretos que nombran a cada empresa con su importe &mdash;116.343 millones de pesos
corrientes, 236 adjudicatarios&mdash;, <b>los diez primeros se llevan el 54,5% y los veinticinco
primeros el 78,6%</b>.</p>
<p><b>Y cuatro de esos diez entraron con una sola adjudicaci&oacute;n.</b> La mayor de todas, un contrato
de seguridad y vigilancia, representa por s&iacute; sola el <b>11,6% de todo lo adjudicado</b> en dos
a&ntilde;os y medio. Otro decreto &mdash;red vial y aceras, septiembre de 2024&mdash; compromete 20.916
millones en un solo acto.</p>
<p><b>Lo que el dato muestra es la escala de la decisi&oacute;n:</b> <span class="sg">un solo acto del Ejecutivo puede
comprometer m&aacute;s de la d&eacute;cima parte de lo adjudicado en dos a&ntilde;os y medio.</span></p>
</div>


""" + ex("g", "San Isidro invierte en obra m&aacute;s del triple que el municipio bonaerense t&iacute;pico",
     "Cada marca es un municipio, ordenados por valor. Ejecuci&oacute;n 2025, gasto devengado.",
     "ex04.png",
     "RAFAM 2025, v&iacute;a La Verdadera PBA (la-verdadera-pba.pages.dev), capturado el 3 de septiembre de 2026.",
     "Son 106 de los 135 municipios: los otros 29 no est&aacute;n en la planilla. No se estim&oacute; ninguno.") + """
<h2><span class="n">1.3</span>D&oacute;nde no va el dinero</h2>
<p class="tight">Ejecuci&oacute;n presupuestaria 2025, sobre un gasto devengado total de 324.304 millones
de pesos:</p>
""" + exhead("c", "Las dos partidas que este programa se propone cambiar") + """
<table>
<colgroup><col style="width:200pt"><col><col><col></colgroup>
<tr class="hd"><th>Programa</th><th class="r">Devengado</th><th class="r">% del gasto total</th>
<th class="r">Por habitante</th></tr>
<tr><td class="l">Apoyo y Promoci&oacute;n al Empleo</td><td class="n">170 M$</td><td class="n"><b>0,05%</b></td><td class="n"><b>572 $/a&ntilde;o</b></td></tr>
<tr><td class="l">Infraestructura Habitacional</td><td class="n">335 M$</td><td class="n"><b>0,10%</b></td><td class="n"><b>1.127 $/a&ntilde;o</b></td></tr>
</table>
<p class="cap"><b>Fuente:</b> Estado de Situaci&oacute;n Econ&oacute;mico-Financiera 2025, gastos por
programa.</p>
<div class="cols">
<p>Quinientos setenta y dos pesos por habitante por a&ntilde;o. Eso es toda la pol&iacute;tica de empleo
del Municipio de San Isidro.</p>
<p>Mil ciento veintisiete pesos por habitante por a&ntilde;o en infraestructura habitacional.</p>
</div>
""")


# =====================================================================
# CAPITULO 1 — parte B
# =====================================================================
C1B = dict(id="cap1b", runhead=RH, html="""
<h2><span class="n">1.4</span>Por qu&eacute; pasa esto: est&aacute; escrito</h2>
<div class="cols">
<p>El plan de gobierno vigente, &laquo;Prioridades Estrat&eacute;gicas 2024&ndash;2025&raquo;, fija tres
prioridades: Seguridad Ciudadana, Espacio P&uacute;blico y Ambiente, e Innovaci&oacute;n.</p>
<p>Seguridad interna, la primera, subi&oacute; <b>34,8% real en un a&ntilde;o</b>: ninguna otra
funci&oacute;n creci&oacute; tanto, salvo los servicios de la deuda. Promoci&oacute;n y asistencia social,
que no figura entre las tres, <b>cay&oacute; 32,5%</b>.</p>
</div>

<h2><span class="n">1.5</span>San Isidro se financia solo. Eso cambia todo.</h2>
<div class="cols">
<p>En 2025 el Municipio recibi&oacute; 82.268 millones de pesos de la Provincia de Buenos Aires, contra
324.304 millones de gasto devengado total.</p>
<p><b>Y esa proporci&oacute;n viene creciendo.</b> Desde 2010 los recursos de origen municipal
aumentaron <b>33,6% en t&eacute;rminos reales</b> &mdash;el 1,95% anual que el cap&iacute;tulo 3 usa como
par&aacute;metro del modelo&mdash;, mientras las transferencias provinciales ca&iacute;an. San Isidro
depende hoy menos de la Provincia que hace quince a&ntilde;os, y no por decisi&oacute;n de nadie: por
aritm&eacute;tica.</p>
<p>Esto tiene una consecuencia pol&iacute;tica directa: <span class="sg">un intendente de San Isidro no
depende de La Plata.</span> La mayor parte del presupuesto se define localmente, se aprueba por ordenanza
del Concejo Deliberante y se puede reasignar por decisi&oacute;n local. Todo lo que este programa propone
puede financiarse sin pedirle permiso a nadie.</p>
</div>
<div class="pull"><p>La Provincia financia aproximadamente el 25% de San Isidro. El municipio recauda el
75% restante.</p></div>
<p>Hay una salvedad, y es estructural: la participaci&oacute;n de San Isidro en las transferencias
provinciales cay&oacute; de 1,938% en 2021 a 1,773% en 2025, un 8,5%, y se compone a&ntilde;o a
a&ntilde;o. <b>El cap&iacute;tulo 3 lo descompone fondo por fondo y lo incorpora al modelo.</b></p>
""" + ex("g", "Tigre pasa a San Isidro en 2025: el reparto provincial se dio vuelta",
     "Participaci&oacute;n de cada municipio en el total transferido por la Provincia a los 135 municipios. A&ntilde;os completos.",
     "ex06.png",
     "Ministerio de Hacienda y Finanzas de la Provincia de Buenos Aires, transferencias a municipios 2021&ndash;2025.",
     "2026 va con seis meses y queda fuera del gr&aacute;fico. San Isidro cae a 1,6811% y Tigre sube a 1,8370%.") + """

<h2><span class="n">1.6</span>Lo que dice este cap&iacute;tulo, en cuatro l&iacute;neas</h2>
<ol class="n">
<li>San Isidro es un municipio rico que invierte m&aacute;s en obra p&uacute;blica que el 96% de los
municipios bonaerenses.</li>
<li>Casi la mitad de su poblaci&oacute;n &mdash;el 46,8%, en Boulogne Sur Mer y B&eacute;ccar&mdash; vive
donde est&aacute; el 60% de los hogares sin gas de red y el 71% de los que no tienen cloaca.</li>
<li>El municipio destina el 0,05% de su presupuesto a empleo y el 0,10% a vivienda.</li>
<li>San Isidro tiene los fondos y la autonom&iacute;a para cambiarlo. Lo que falta es que decida quien vive
donde est&aacute; el problema.</li>
</ol>
<p><b>Los cap&iacute;tulos siguientes proponen ese mecanismo.</b></p>
<div class="hairline"></div>
<div class="note">
<p><b>Nota metodol&oacute;gica.</b> Las series fiscales provienen de los informes de ejecuci&oacute;n
presupuestaria y rendiciones de cuentas publicados por la Municipalidad de San Isidro, de los fallos del
Honorable Tribunal de Cuentas de la Provincia de Buenos Aires y del sistema SIMCo provincial, validadas de
forma cruzada entre s&iacute;. Los datos territoriales provienen del Censo Nacional de Poblaci&oacute;n,
Hogares y Viviendas 2022 (INDEC), a nivel de radio censal. Los importes est&aacute;n expresados en pesos
constantes de diciembre de 2025 salvo indicaci&oacute;n expresa.</p>
<p>Las seis zonas de 1.1 son los l&iacute;mites de las localidades del partido seg&uacute;n OpenStreetMap,
proyectados sobre los 360 radios censales del INDEC: cada radio se asigna a la localidad que contiene su
punto representativo. Los 360 caen dentro de exactamente una, sin hu&eacute;rfanos y sin dobles.</p>
<p>El domicilio de los adjudicatarios sale de 3.670 decretos de adjudicaci&oacute;n del Bolet&iacute;n
Oficial municipal. La proporci&oacute;n es de actos y no de montos, porque los importes est&aacute;n en
pesos corrientes de cada a&ntilde;o. La concentraci&oacute;n usa los 407 decretos que nombran a cada
empresa con su importe; sumando los 144 que informan s&oacute;lo un total, baja al 42,1%.</p>
<p>Los datos de los otros 105 municipios bonaerenses usados en 1.2 provienen de informes de
ejecuci&oacute;n RAFAM procesados por La Verdadera PBA, un sitio de terceros que republica datos oficiales
de la Provincia. Las cifras de San Isidro fueron validadas contra el estado de ejecuci&oacute;n del propio
Municipio y coinciden en las siete categor&iacute;as del gasto por objeto. Las de los otros municipios no
fueron validadas individualmente: se usan para calcular la mediana provincial y la posici&oacute;n relativa
de San Isidro.</p>
</div>
""")


# =====================================================================
# NOTA DE METODO - va al final, antes del anexo
# =====================================================================
METODO = dict(id="metodo", runhead=RH, html="""
<h1>Nota de m&eacute;todo</h1>
<div class="stand">C&oacute;mo est&aacute; construido este documento, de d&oacute;nde sale cada cifra y qu&eacute; l&iacute;mites tiene.</div>
<p class="lead">Cada cifra de este documento proviene de un documento p&uacute;blico, y est&aacute;
indicada la fuente donde aparece.</p>
<div class="cols">
<p>Las series fiscales salen de los informes de ejecuci&oacute;n presupuestaria y las rendiciones de
cuentas que publica la propia Municipalidad de San Isidro, de los fallos del Tribunal de Cuentas de la
Provincia y del sistema SIMCo provincial. Los indicadores territoriales salen del Censo Nacional 2022,
a nivel de radio censal. El modelo fiscal reproduce la ejecuci&oacute;n 2025 del Municipio con
diferencia cero.</p>
<p><span class="sg">El modelo, los datos, las series y los diecinueve gr&aacute;ficos son p&uacute;blicos y
reproducibles.</span> Se publican en un repositorio abierto al presentarse este programa, con las pruebas autom&aacute;ticas que los
verifican. Cualquiera puede correrlos y llegar a los mismos n&uacute;meros, o encontrar que no llega.</p>
</div>

<div class="callout a">
<div class="clabel">Los l&iacute;mites</div>
<p>Los datos de los otros 105 municipios provienen de un procesador de terceros y no fueron verificados
uno por uno. Los l&iacute;mites de las localidades son de OpenStreetMap, porque la Municipalidad no
publica los suyos. El Municipio cambi&oacute; su nomenclador de funciones en 2025, lo que vuelve
incomparable buena parte de las series interanuales.</p>
</div>
""")
