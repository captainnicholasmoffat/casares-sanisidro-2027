# -*- coding: utf-8 -*-
from content_a import RH, fig

CIERRE = dict(id="cierre", runhead=RH, html="""
<h1>Para cerrar</h1>
<div class="stand">Nuestra propuesta tiene dos partes. Primero, en cuatro a&ntilde;os, los vecinos van a decidir la mitad de la obra p&uacute;blica. Segundo, el gasto en empleo y vivienda se va a multiplicar por quince. Todo esto se va a pagar actualizando la tabla de valores de 2008 con la que hoy se cobra la tasa de servicios generales. El dinero que falta sale del gasto flexible, la parte del presupuesto que no est&aacute; atada a sueldos, deudas ni contratos firmados. No hace falta subir el porcentaje de la tasa, ni tomar deuda, ni pedirle permiso a la Provincia.</div>
<div class="cols">
<p>La pregunta del principio era sobre el plan de gobierno 2024&ndash;2025. &iquest;A qui&eacute;n se escuch&oacute;, y c&oacute;mo, para que el empleo y la vivienda no aparecieran nunca? Tener un presupuesto m&aacute;s grande no es la soluci&oacute;n. Hay que cambiar <span class="sg">qui&eacute;n decide</span>. Tambi&eacute;n hay que decir con qu&eacute; dinero se va a hacer cada cosa y para cu&aacute;ndo. Por eso este programa promete poco, y le pone fecha a todo. Son veinti&uacute;n compromisos para los primeros cien d&iacute;as, y veinte metas. Al lado de cada meta est&aacute; el dato de hoy, para poder comparar.</p>
<p>Hay una pieza que sostiene a todas las dem&aacute;s: <b>la inteligencia artificial del Municipio</b>. Va a ser, para cada vecino, como tener a mano a alguien que sabe todo del Municipio. Para decidir bien hay que leer mucho, y nadie tiene tanto tiempo. <span class="sg">La informaci&oacute;n que nadie puede leer no sirve para controlar al Municipio.</span> Si los vecinos tienen que decidir sin la inteligencia artificial del Municipio, la participaci&oacute;n se apaga sola. As&iacute; pas&oacute; en todos los lugares que lo intentaron sin resolver este problema.</p>
<p>Adem&aacute;s, el pr&oacute;ximo gobierno ya no va a empezar desde el mismo lugar. En agosto de 2026, el Municipio se endeud&oacute; con un bono por 30.000 millones de pesos. Ese bono se devuelve en ocho cuotas, sin contar los intereses. <span class="sg">Siete de esas cuotas las va a pagar el gobierno que asuma en diciembre de 2027.</span></p>
</div>
<div class="pull"><div class="plabel">Por d&oacute;nde empieza</div>
<p>El 10 de diciembre de 2027 asume el intendente. Para el 19 de marzo de 2028, a los cien d&iacute;as, la primera asamblea de cada
zona ya va a estar convocada.</p></div>
""" + fig("f_calle", "San Isidro, a primera hora. Ilustraci&oacute;n."))
# Correccion 132: la firma de Casares sale hasta que el candidato apruebe el
# documento. Para reponerla, despues del pull de "Por donde empieza" va:
# <p style="margin-top:14pt;font-style:italic;color:var(--taupe);font-size:9pt">Jos&eacute; Luis Casares,
# candidato a intendente de San Isidro.</p>
