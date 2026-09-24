# -*- coding: utf-8 -*-
from content_a import RH, fig

CIERRE = dict(id="cierre", runhead=RH, html="""
<h1>Para cerrar</h1>
<div class="stand">Media obra p&uacute;blica decidida por los vecinos en cuatro a&ntilde;os, y el gasto en empleo y vivienda multiplicado por quince, financiado actualizando una base de valuaci&oacute;n que es de 2008. Sin subir la al&iacute;cuota, sin tomar deuda y sin pedirle permiso a la Provincia.</div>
<div class="cols">
<p>Este documento empez&oacute; con una pregunta sobre el plan de otro: a qui&eacute;n se
escuch&oacute;, y c&oacute;mo, para que el empleo y la vivienda no aparecieran nunca.</p>
<p>La respuesta no est&aacute; en el tama&ntilde;o del presupuesto: hay que cambiar
<span class="sg">qui&eacute;n decide</span>, y decir con qu&eacute; dinero y para cu&aacute;ndo.</p>
<p>Por eso este programa promete poco y lo promete con fecha: diecis&eacute;is compromisos en cien
d&iacute;as y catorce metas con l&iacute;nea de base fijada hoy.</p>
<p>Y una pieza que sostiene a todas las dem&aacute;s: <b>una inteligencia artificial nativa del
Municipio</b>, que para cada vecino es como tener a disposici&oacute;n a alguien que sabe todo del
Municipio. Porque decidir bien exige leer, y nadie tiene las horas.
<span class="sg">Lo que nadie puede leer no controla nada</span>, y un mecanismo de decisi&oacute;n
vecinal sin eso se apaga solo, como se apag&oacute; en todas partes donde se intent&oacute; sin
resolverlo.</p>
<p>Y mientras se escrib&iacute;a este documento cambi&oacute; el punto de partida. En
agosto de 2026 el Municipio coloc&oacute; un bono por 30.000 millones, y <span class="sg">siete de sus
ocho cuotas de capital las paga el gobierno que asuma en diciembre de 2027</span>.</p>
</div>
<div class="pull"><div class="plabel">Por d&oacute;nde empieza</div>
<p>El 10 de diciembre de 2027 asume el intendente. A fines de marzo de 2028 la primera asamblea de cada
zona ya fue convocada.</p></div>
""" + fig("f_calle", "San Isidro, a primera hora. Ilustraci&oacute;n."))
# Correccion 132: la firma de Casares sale hasta que el candidato apruebe el
# documento. Para reponerla, despues del pull de "Por donde empieza" va:
# <p style="margin-top:14pt;font-style:italic;color:var(--taupe);font-size:9pt">Jos&eacute; Luis Casares,
# candidato a intendente de San Isidro.</p>
