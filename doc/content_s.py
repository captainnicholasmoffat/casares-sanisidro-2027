# -*- coding: utf-8 -*-
from content_a import RH, exhead

# Pagina 4. La lista va ordenada como cadena: los vecinos deciden la obra, el
# Municipio la contrata en San Isidro, para eso se forma a la gente aca, esa
# gente construye la inteligencia artificial del Municipio y esa herramienta es
# la que le permite al vecino informarse y decidir (correcciones 125 y 126).
SINTESIS = dict(id="sintesis", runhead=RH, html="""
<h1>Qu&eacute; proponemos hacer</h1>
<div class="stand">Proponemos una democracia semidirecta asistida por inteligencia artificial: los vecinos de cada zona
van a decidir la mitad de la obra p&uacute;blica y a controlar c&oacute;mo se usa el dinero de todos. Hoy se puede hacer: la
inteligencia artificial del Municipio le va a dar a cada vecino la informaci&oacute;n para decidir, y va a poder escuchar a
miles de vecinos a la vez.</div>

<ol class="n">
<li><b>Los vecinos van a decidir la mitad de la obra p&uacute;blica, en cuatro a&ntilde;os.</b> Hoy no deciden ninguna obra p&uacute;blica. Van a decidir el 12,5% el primer a&ntilde;o y la mitad al cuarto a&ntilde;o, que son
28.908 millones por a&ntilde;o. Una f&oacute;rmula escrita, y no el intendente, va a repartir el dinero entre las zonas, seg&uacute;n la
poblaci&oacute;n y la necesidad de cada una. Por eso la mayor parte va a ir a Boulogne Sur Mer y a B&eacute;ccar. <b>El dinero de cada
zona va a quedar reservado por ordenanza</b>, para que no se pueda usar en otra cosa. <i>(Cap&iacute;tulo 4)</i></li>

<li><b>La obra y los servicios que paga el Municipio se van a contratar con empresas y cooperativas de San
Isidro.</b> Puede pasar que, al licitar un trabajo, no se presente ninguna empresa de San Isidro capaz de hacerlo. En ese
caso, el Municipio va a intentar formar a vecinos para que aprendan ese trabajo, armen su propia empresa o cooperativa y
den ellos el servicio. Las universidades de San Isidro los van a acompa&ntilde;ar en ese camino. Adem&aacute;s, en cada
licitaci&oacute;n p&uacute;blica, <span class="sg">una parte del trabajo va a quedar para las pymes de San Isidro</span>.
<i>(Cap&iacute;tulo 5)</i></li>

<li><b>Vamos a formar a la gente ac&aacute;, en lo que mejor paga: inteligencia artificial y tecnolog&iacute;a.</b>
La formaci&oacute;n ser&aacute; una tecnicatura de la universidad nacional que tiene sede en San Isidro, para que lo aprendido sirva
tambi&eacute;n fuera del Municipio. Cuando la formaci&oacute;n funcione completa, van a entrar <b>928 personas</b> por a&ntilde;o. Los alumnos van a estudiar el primer a&ntilde;o, y el segundo
van a trabajar como pasantes, seis meses en el Municipio y seis en una empresa de San Isidro. <span class="sg">El presupuesto
de empleo y vivienda se va a multiplicar por quince.</span> Tambi&eacute;n proponemos <b>un centro de apoyo escolar en cada localidad</b>.
Hoy hay apenas cinco espacios peque&ntilde;os de apoyo escolar, todos en B&eacute;ccar y Boulogne. A ellos van unos cien alumnos. En las
otras cuatro localidades no hay ninguno. <i>(Cap&iacute;tulo 5)</i></li>

<li><b>Las personas que se forman en la tecnicatura van a construir la inteligencia artificial del Municipio.</b> Va a ser
una inteligencia artificial propia, y cualquier vecino le va a poder preguntar lo que necesita. No va a ser una
aplicaci&oacute;n m&aacute;s. La van a hacer docentes y t&eacute;cnicos de San Isidro, junto con los pasantes y egresados de la formaci&oacute;n.
Se va a pagar con el dinero que el presupuesto municipal ya reserva para Ciencia y T&eacute;cnica, que son 8.155 millones por
a&ntilde;o: no hacen falta fondos nuevos. <i>(Cap&iacute;tulo 4)</i></li>

<li><b>La inteligencia artificial del Municipio le va a permitir al vecino informarse y decidir.</b> El vecino le va a
poder preguntar lo que necesite sobre el Municipio, y ella siempre le va a mostrar de d&oacute;nde sac&oacute; cada dato. Antes de la
asamblea de su zona, tambi&eacute;n podr&aacute; consultarle por cada tema que se va a votar, con su historia y su contexto. As&iacute;
llegar&aacute; a la reuni&oacute;n entendiendo de qu&eacute; se trata. <span class="sg">Hoy el Municipio tiene una
aplicaci&oacute;n de reclamos muy mal puntuada: sus propios usuarios le ponen 1,84 sobre 5. Nuestra propuesta es la
respuesta a esas quejas.</span> <i>(Cap&iacute;tulo 4)</i></li>

<li><b>Las c&aacute;maras van a detectar y avisar, y no s&oacute;lo grabar.</b> Si una c&aacute;mara ve un hecho violento
mientras est&aacute; pasando, va a avisar en el momento al patrullero que est&aacute; a tres cuadras, para que llegue a tiempo.
Cuando alguien denuncie un robo, con las c&aacute;maras se va a poder seguir hacia d&oacute;nde se fue el que lo cometi&oacute;, y
la polic&iacute;a ir&aacute; directo a buscarlo. <span class="sg">Se gana tiempo</span>: el caso se resuelve en horas y no
en d&iacute;as, y el patrullero llega cuando todav&iacute;a puede hacer algo, no cuando ya pas&oacute; todo y s&oacute;lo le
queda tomar la denuncia. En el tr&aacute;nsito, proponemos que cada persona pague las multas seg&uacute;n lo que gana, para que
ninguna sea imposible de pagar. Tambi&eacute;n proponemos un l&iacute;mite: la suma de las multas de una persona nunca puede
superar lo que puede pagar con su ingreso, ni el valor de su auto o su moto. El Municipio le va a pedir a la Provincia
los cambios en las multas que no pueda hacer por su cuenta. Mientras tanto, va a avisar antes de multar y va a dejar pagar en cuotas. <i>(Cap&iacute;tulo 5)</i></li>

<li><b>Las inspecciones de comercios van a quedar grabadas.</b> Los inspectores van a grabar con su tel&eacute;fono cada
inspecci&oacute;n, y despu&eacute;s cualquier vecino podr&aacute; ver c&oacute;mo fue. Si la inspecci&oacute;n no queda grabada y sellada, no van a valer el acta, la clausura ni la habilitaci&oacute;n que salgan de esa inspecci&oacute;n. El comerciante tambi&eacute;n va a tener derecho a grabar la
inspecci&oacute;n, y ese video va a quedar guardado en la inteligencia artificial del Municipio, igual que el del inspector.
As&iacute;, el comerciante podr&aacute; protegerse si el inspector no hace las cosas como corresponde. Nuestro objetivo es <span class="sg">bajar la
corrupci&oacute;n en las inspecciones y habilitaciones</span> de los comercios de San Isidro. <i>(Cap&iacute;tulo 5)</i></li>

<li><b>Va a haber muchos m&aacute;s shows y espect&aacute;culos al aire libre: 200 por a&ntilde;o, en plazas y espacios p&uacute;blicos de
todo San Isidro.</b> Van a tocar artistas nuevos de San Isidro, y las bandas van a tener prioridad, para que haya trabajo para m&aacute;s m&uacute;sicos. Tambi&eacute;n queremos que la costa funcione como una riviera, con actividades y gente todos los d&iacute;as
de la semana, no s&oacute;lo el fin de semana. <i>(Cap&iacute;tulo 5)</i></li>

<li><b>Todo esto se paga sin subir el porcentaje de la tasa de servicios generales y sin tomar deuda.</b> El dinero nuevo
que necesita este programa es de 7.225,2 millones por a&ntilde;o, para empleo y vivienda. La mayor parte va a salir de actualizar la tabla de valores de 2008
con la que hoy se cobra esa tasa, y el resto, de reordenar gastos del Municipio. Lo dem&aacute;s ya se gasta hoy. Con la obra
p&uacute;blica que van a elegir los vecinos, por ejemplo, no cambia cu&aacute;nto se gasta: s&oacute;lo cambia qui&eacute;n decide qu&eacute; obra se hace. <i>(Cap&iacute;tulo 3)</i></li>
</ol>
<p><b>Los primeros cien d&iacute;as.</b> El nuevo gobierno asume el <b>10 de diciembre de 2027</b>. Ese mismo mes, el
intendente va a mandar al Concejo Deliberante las primeras ordenanzas. Una va a apartar el dinero de obra que le toca a
cada zona, para que no se pueda usar en otra cosa. Otra va a actualizar los valores de 2008 con los que hoy se cobra la
tasa de servicios generales. Durante los meses siguientes empezar&aacute; a funcionar la inteligencia artificial del Municipio:
ya se le podr&aacute; preguntar, sacar un turno m&eacute;dico y hacerle llegar un reclamo. Al mismo tiempo abrir&aacute; el primer centro de
apoyo escolar y empezar&aacute; el primer grupo de la formaci&oacute;n laboral. Para el <b>19 de marzo de 2028</b>, a los cien d&iacute;as,
todos los vecinos ya van a estar convocados a la primera asamblea de su zona. <span class="sg">En total son veinti&uacute;n
compromisos con fecha. Todos est&aacute;n explicados, uno por uno, en el cap&iacute;tulo 6.</span></p>

""")
