# -*- coding: utf-8 -*-
from content_a import RH, fig

CIERRE = dict(id="cierre", runhead=RH, html="""
<h1>Para cerrar</h1>
<div class="stand">La propuesta tiene dos partes. En cuatro a&ntilde;os, los vecinos deciden la mitad de la obra p&uacute;blica. Adem&aacute;s, el gasto en empleo y vivienda se multiplica por quince. Se paga actualizando la tabla de 2008 con la que se cobra la tasa, y lo que falta, con el gasto flexible. Sin subir el porcentaje de la tasa, sin tomar deuda y sin pedirle permiso a la Provincia.</div>
<div class="cols">
<p>La pregunta del principio era sobre el plan de gobierno 2024&ndash;2025. &iquest;A qui&eacute;n se escuch&oacute;, y c&oacute;mo, para que el empleo y la vivienda no aparecieran nunca? La respuesta no est&aacute; en el tama&ntilde;o del presupuesto. Hay que cambiar <span class="sg">qui&eacute;n decide</span>, y decir con qu&eacute; dinero y para cu&aacute;ndo. Por eso este programa promete poco, y lo promete con fecha: veinti&uacute;n compromisos en cien d&iacute;as, y veinte metas con el n&uacute;mero de hoy al lado.</p>
<p>Hay una pieza que sostiene a todas las dem&aacute;s: <b>la inteligencia artificial del Municipio</b>. Para cada vecino, es como tener a mano a alguien que sabe todo del Municipio. Porque para decidir bien hay que leer, y nadie tiene las horas. <span class="sg">Lo que nadie puede leer no controla nada.</span> Si los vecinos deciden sin eso, el mecanismo se apaga solo. As&iacute; pas&oacute; en todos los lugares donde se intent&oacute; sin resolverlo.</p>
<p>Adem&aacute;s, el punto de partida ya cambi&oacute;. En agosto de 2026, el Municipio tom&oacute; deuda con un bono por 30.000 millones. <span class="sg">Siete de sus ocho cuotas de capital las paga el gobierno que asuma en diciembre de 2027.</span></p>
</div>
<div class="pull"><div class="plabel">Por d&oacute;nde empieza</div>
<p>El 10 de diciembre de 2027 asume el intendente. El 19 de marzo de 2028, a los cien d&iacute;as, la primera asamblea de cada
zona ya fue convocada.</p></div>
""" + fig("f_calle", "San Isidro, a primera hora. Ilustraci&oacute;n."))
# Correccion 132: la firma de Casares sale hasta que el candidato apruebe el
# documento. Para reponerla, despues del pull de "Por donde empieza" va:
# <p style="margin-top:14pt;font-style:italic;color:var(--taupe);font-size:9pt">Jos&eacute; Luis Casares,
# candidato a intendente de San Isidro.</p>
