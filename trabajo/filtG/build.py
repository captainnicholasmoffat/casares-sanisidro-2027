import re, sys
D = '/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compr/'
inp = [l.rstrip('\n') for l in open(D + 'out_G.md', encoding='utf-8') if l.strip()]
rows = []
for l in inp:
    p = [x.strip() for x in l.split(' | ')]
    rows.append((p[0], p[1]))

K, V, N, X = 'KEEP', 'VERIFY', 'NICK', 'DROP'
dec = {
1: (V, "Hoy, el Municipio gasta en esta área 13.986 millones, el 4,3% del presupuesto.", "qué incluye la cifra: sólo educación, o educación y cultura juntas (el 5.8 da aparte los 1.360,4 millones de cultura)"),
2: (X, "el nombre del fondo ya dice qué es; la explicación agrega un dato"),
3: (K, "San Isidro ya tiene lugares donde poner los centros de apoyo escolar."),
4: (K, "Proponemos un centro de apoyo escolar gratuito en cada localidad. El lugar exacto lo va a definir el índice de necesidad del capítulo 4, que mide lo que le falta a cada zona."),
5: (K, "3 · El modelo del Centro de Formación Laboral 404 (CFL 404) va a llegar a las seis zonas, como propone la sección 5.3. Es el puente entre la escuela y el trabajo, que hoy no existe para tanta gente."),
6: (K, "Antes de elegir qué empresa da el servicio, se prueban las distintas opciones durante un mes. Quienes las evalúan no saben de qué empresa es cada una. Así se comparan la calidad y el precio de todas."),
7: (K, "En un estudio en Turquía, los alumnos que usaron un chatbot que les daba las respuestas mejoraron un 48% sus notas de práctica. Pero en el examen, hecho sin inteligencia artificial, su nota bajó un 17%. Con un chatbot que sólo daba pistas, esa caída no se vio."),
8: (K, "Su aprendizaje mejoró entre 0,06 y 0,36 desvíos estándar. Esa es la medida que usan estos estudios para comparar cuánto aprende un grupo de alumnos frente a otro."),
9: (K, "4 · Quién paga. Es gratis en las escuelas públicas y en los colegios privados que el Estado paga por completo. Entre todos, tienen 22.748 alumnos."),
10: (K, "Para saber si un colegio privado entra en este grupo, se mira cada nivel por separado, como primaria o secundaria. Cuenta el aporte del Estado que el colegio tiene al empezar el año."),
11: (K, "Cuesta de 10.887 a 12.146 pesos por alumno por año. Ese precio incluye el uso que se espera y una parte del costo del equipo de personas que construye la inteligencia artificial del Municipio."),
12: (K, "El Municipio paga sólo el costo de los alumnos que lo tienen gratis. Lo paga con el dinero que se le devuelve a Educación, que perdió presupuesto en 2025 (se explica más abajo)."),
13: (X, "global: «necesita dictamen de un abogado»; la ley citada no traba la lectura"),
14: (X, "se entiende: viene justo después del punto 5, «Qué informa»"),
15: (K, "El profesor digital procesa los datos en Europa, algo que la ley argentina acepta (Disposición 60/2016). El contrato le prohíbe a la empresa que da el servicio usar estos datos para entrenar su propia inteligencia artificial."),
16: (K, "Salen del programa de mantenimiento y embellecimiento, que nombra el capítulo 3. Son el 2,4% de los 87.326 millones que el Municipio puede usar libremente cada año."),
17: (K, "Dentro de esos 2.064 millones se paga el profesor digital de los 22.748 alumnos que lo tienen gratis. Con el uso que se espera, cuesta de 151,9 a 180,5 millones por año. Si lo usan todos, cuesta de 788,3 a 979,1 millones por año. La parte que les toca a estos alumnos del costo del equipo de personas, 120,7 millones, ya está contada en el cuadro 27."),
18: (K, "Cualquiera va a poder preguntar en qué obras y en qué escuelas se gastó el Fondo de Financiamiento Educativo. Es dinero que la ley destina a algo concreto. Por eso se debería poder seguir en qué se gasta, y hoy eso no es posible. Esa información sirve, además, para lo único que importa acá: saber si las obras llegan a las escuelas que están en peor estado."),
19: (K, "No es que falte dinero. Hay lugares, pero las reglas hacen muy difícil usarlos para la cultura."),
20: (K, "Las reglas de la música en vivo en San Isidro son de 1970. Siguen publicadas en el Digesto, que es la recopilación oficial de las normas del Municipio."),
21: (V, "La Ordenanza 8216/2006 agrega que hay que cerrar entre las doce de la noche y las siete de la mañana.", "que en la Ordenanza 8216/2006 el cierre es de 0 a 7 h (el «Permiso de Funcionamiento Nocturno» lo sugiere)"),
22: (K, "Esa falta de una categoría para lugares chicos tiene un costo que nadie ve. Habilitar cuesta tanto que sólo conviene hacer un evento en un lugar grande y caro. Por eso, la entrada sale demasiado cara. Las reglas tienen que cuidar al vecino que se acuesta a las nueve, pero no sólo a él."),
23: (X, "global: «la propuesta» → «nuestra propuesta»; «no inventar» se entiende con lo que sigue"),
24: (X, "global: términos del capítulo 4 («la comisión de la zona») y propuestas en presente"),
25: (K, "Además, la música va a salir a la calle. Los espectáculos al aire libre de lunes a jueves están en el 5.5. Va a haber artistas que tocan a cambio de lo que el público les quiera dar, con el sonido del Municipio. También va a haber shows elegidos por los vecinos, con artistas nuevos del partido."),
26: (N, "LO QUE SE PERDIÓ EN LA COSTA, MÁS ALLÁ DE LO ECONÓMICO", "cambia el título de un recuadro («contado entero» se entiende mal)"),
27: (V, "Los locales de la costa que se demolieron (5.5) no eran sólo trabajo y edificios. Eran un lugar adonde la gente iba. En este partido, habilitar un lugar con música depende de un decreto de 1970. Por eso es muy difícil abrir otros que los reemplacen. Cerrar dos lugares que funcionaban no es, entonces, sólo un problema económico.", "que el paso que falta es ese: por el decreto de 1970, es muy difícil abrir otros lugares con música que reemplacen a los cerrados"),
28: (V, "Cuánto trabajo le toca a cada institución se calcula con el índice de necesidad del capítulo 4, el mismo que reparte el dinero de obra entre las zonas. Con los datos de hoy, esa cuenta les da dos tercios de los encargos a las instituciones públicas.", "qué es «el peso» de cada institución, cómo lo fija el índice y de qué son los «dos tercios»"),
29: (K, "El criterio, dicho de frente. En un sector chico de Boulogne, que el censo identifica como radio 067562205, el 13,7% de los hogares tiene necesidades básicas insatisfechas. Además, el 95,8% cocina sin gas de red."),
30: (K, "La otra es una universidad privada, con sede en Béccar."),
31: (K, "Propone que la inteligencia artificial del Municipio conteste. También propone que el dinero que se gaste en construirla quede en San Isidro."),
32: (K, "Pero esas metas dejan afuera lo más importante."),
33: (N, "LA IDEA SURGIÓ EN MIAMI, Y DESPUÉS LA CIUDAD LA PUSO EN PRÁCTICA", "cambia el título de un recuadro; «la vara» y «la compró» son expresiones coloquiales (regla 2)"),
34: (K, "En noviembre de 2025, en un encuentro de negocios en Miami, un empresario muy conocido propuso una idea para la ciudad."),
35: (X, "se entiende: la diferencia entre ciudad y condado no traba la lectura"),
36: (X, "se entiende: el párrafo anterior dice de qué son las críticas"),
37: (X, "se entiende: «en cuánto tiempo» sale el trámite"),
38: (X, "se entiende con la oración anterior; la propuesta suma una aclaración del tipo que va al final (regla 9)"),
39: (X, "se entiende: la segunda mitad de la oración lo explica"),
40: (K, "Si, con nuestra propuesta, la habilitación pasa a ser automática, la inspección queda como el único momento en que alguien decide a su criterio. Por eso, esa inspección queda grabada, como proponemos para todas las del Municipio. La grabación se sella en ese mismo instante, y así nadie la puede cambiar ni borrar sin que se note."),
41: (K, "Cuánto cuesta. La parte de la inteligencia artificial del Municipio que lee los trámites la construye el equipo de la plataforma (4.11). Para las cámaras de seguridad se usan las 110 licencias de análisis de video que el Municipio ya compró (5.7)."),
42: (K, "En una primera etapa, la grabación de las inspecciones, que se explica más abajo, incluye a los inspectores, Habilitaciones, obra y tránsito. Los soportes de pecho para el teléfono, las baterías, los datos y la guarda de las grabaciones cuestan de 20,5 a 27,5 millones una sola vez. Después cuestan de 107,6 a 145,5 millones por año."),
43: (X, "global: jerga de presupuesto («ceden su gasto»)"),
44: (K, "Lo anterior sirve para que el trámite tenga una respuesta. Falta resolver otra cosa: el momento en que se puede pedir o pagar una coima."),
45: (X, "global: «la propuesta» → «nuestra propuesta»"),
46: (K, "Cada grabación se sella en el mismo instante en que se hace. En ese momento, un código único que identifica esa grabación llega a la inteligencia artificial del Municipio."),
47: (K, "La inteligencia artificial del Municipio divide el video del turno en una grabación por cada inspección. Después guarda cada una en una base de datos, ordenada por comercio o por domicilio."),
48: (K, "La Ley 14.656, del empleo municipal, dice que el Municipio tiene que dar las herramientas de trabajo. Como el teléfono es del agente, la solución es compensarle ese gasto, como prevé el artículo 75 de esa ley. Esa compensación se acuerda con los trabajadores municipales (necesita dictamen de un abogado)."),
49: (K, "No graban todos los empleados municipales. Graban sólo los agentes que pueden controlar o ejercer autoridad, y únicamente durante su turno."),
50: (K, "La regla tiene una consecuencia escrita: si no hay grabación sellada y subida, el acta no vale. Si no tuviera esa consecuencia, la regla sería sólo una recomendación."),
51: (X, "la cita no traba la lectura; explicar el artículo agrega un dato; «necesita dictamen» va por la regla global"),
52: (K, "Una persona revisa el video antes de mostrarlo. Todo esto cuesta unos 2.200 pesos por pedido. En total, son de 5 a 23 millones por año."),
53: (K, "La inteligencia artificial del Municipio sella la prueba en el momento de grabar, como hace con la del vecino que denuncia un ruido (5.5)."),
54: (K, "Si se juntan en un mismo agente, rubro o zona, les avisa a quienes controlan sin depender del denunciado, como la comisión del Concejo y la auditoría externa."),
55: (X, "la primera oración ya cambia con la corrección 18 (al aplicarla, «Antes» puede pasar a «Primero»)"),
56: (V, "Las adjudicaciones, es decir, quién ganó cada licitación, están en el Boletín Oficial. Pero su buscador funciona dentro de un recuadro fijo. Ese recuadro muestra sólo cuatro de las treinta filas de resultados, y esconde los botones para seguir viendo más. Si se intenta abrir el buscador en una página aparte, da un error de permisos.", "qué quiere decir «cuatro filas de treinta» (¿se ven 4 de 30 resultados?) en el relevamiento del 12 de septiembre"),
57: (K, "Es más un problema de diseño que de voluntad, pero para el vecino el efecto es el mismo."),
58: (V, "Los números de cada área salen del presupuesto de 2026, que separa el gasto por programa y explica cada uno. Pero son 492 y 416 páginas escaneadas como imágenes.", "qué son «los puestos de cada área» (¿cargos de personal o números de gasto?)"),
59: (K, "Publicar cada tres meses es una costumbre de cuando un empleado tenía que armar un informe a mano. Proponemos que casi todo se pueda consultar el mismo día en que pasa. Con la inteligencia artificial del Municipio (capítulo 4), cada adjudicación queda cargada el día en que se firma. Mostrarla no es una tarea aparte, porque es el mismo registro."),
60: (K, "Dar como definitivo un número que después se corrige es peor que no contestar. Por eso, lo gastado en el mes se muestra marcado como provisorio."),
61: (X, "global: jerga de presupuesto («partida», «renglón»)"),
62: (K, "El gasto en comercio, sumado al de turismo y otros servicios, es de 2.216 millones, el 0,7% del presupuesto."),
63: (K, "En los temas que decide la Provincia, como el recorrido de los colectivos, proponemos que el Municipio le pida lo que haga falta. También proponemos que cualquier vecino pueda preguntar qué contestó la Provincia."),
64: (K, "La ley nacional de tránsito no deja que una norma local sea «más benigna», es decir, más suave que ella (Ley 24.449, artículo 2)."),
65: (K, "Hoy, la multa por exceso de velocidad no distingue si uno se pasó por 5 o por 50 km/h. En los dos casos va de 342.150 a 2.281.000 pesos, o 171.075 si se paga enseguida. Para el 10% que menos gana, pagar esos 171.075 pesos equivale al 125% de su ingreso de un mes."),
66: (K, "Si la multa no se paga a tiempo, la deuda no se congela. Se calcula con el valor que tenga la unidad de multa el día en que se cancela."),
67: (K, "El Juzgado de Faltas ya recibe por correo electrónico los pedidos de pago voluntario. Es la forma de cancelar la multa enseguida, con descuento."),
68: (K, "Además, no se publica cuántas multas se hacen por año. Hasta el 23 de abril de 2025, las cámaras las manejaban dos universidades nacionales, que se quedaban con un porcentaje de lo recaudado (Decretos 704, 1542, 1543, 1588 y 1982 de 2022)."),
69: (V, "Entre 2017 y 2024 murieron 109 personas en el tránsito de San Isidro. De ellas, 53 murieron en la Panamericana, que es una ruta nacional.", "que las 53 muertes de la Panamericana están dentro de las 109"),
70: (V, "Completar la oración cortada con el texto de la fuente; si no hay más texto, borrar «También el Tribunal de».", "cómo sigue la oración en la fuente: parece texto cortado o escondido por el armado de la hoja"),
71: (K, "Además, el vecino no tiene que hacer nada para recibir la rebaja que le corresponde según su ingreso."),
72: (K, "La inteligencia artificial del Municipio propone los lugares según los datos de choques. Para poner una cámara, tiene que haber una cantidad mínima de choques, y esa cifra se publica."),
73: (X, "global: términos del capítulo 4 («el panel sorteado»)"),
74: (K, "Una vez por año, la inteligencia artificial del Municipio revisa cada cámara para decidir si sigue o se saca. En Nueva Gales del Sur, en Australia, una revisión así llevó a sacar 3 de sus 92 cámaras fijas en 2023."),
75: (K, "4 · En zona de 40, la multa empieza en 47. Primero se descuentan los 3 km/h de error que admite el equipo (Resolución 753/98). Después, sólo hay multa si lo que queda de exceso es de 4 km/h o más, como en los Países Bajos."),
76: (X, "el cuadro 36 ya muestra la fórmula aplicada; el ejemplo agrega una cifra (regla 10)"),
77: (K, "El vecino se anota una sola vez, por internet, en la inteligencia artificial del Municipio. Esto se establece como lo hizo Bragado (Ordenanza 5398/2021)."),
78: (K, "8 · Varias pasadas, una multa. Para que todas las pasadas por la misma cámara antes del aviso cuenten como una sola multa, hace falta que lo apruebe la Provincia (Ley 24.449, artículo 81). Mientras tanto, el juez une en una sola multa las pasadas de un mismo viaje. Si alguien no se anotó para recibir el aviso, sólo se unen las pasadas del primer día."),
79: (V, "Hoy, si alguien vuelve a cometer una falta grave, la ley prevé una suspensión de la licencia de hasta 9 meses la primera vez. La segunda vez que reincide, es de hasta 12 meses. Como la ley dice «hasta», el juez ya puede dar una suspensión más corta. Esa suspensión puede ser para un solo tipo de vehículo, y se le suma un curso.", "que 9 meses corresponde a la primera reincidencia y 12 a la segunda (Ley 13.927, artículo 39 ter), y qué curso es"),
80: (K, "Si la Provincia aprueba una ley, quien tenga la licencia suspendida podría recibir un permiso especial para manejar en su trabajo, con horarios y recorridos fijos."),
81: (K, "Cuatro personas, en Tránsito o en el Juzgado de Faltas, revisan las actas. Para esos puestos, primero se toma a egresados de la tecnicatura en inteligencia artificial."),
82: (K, "En Estados Unidos, Virginia y Seattle pagan un monto fijo por equipo. La guía federal de 2023 recomienda lo mismo."),
83: (V, "La regla vale también para la UNSO, que fue una de las dos universidades que manejaban las cámaras. La UNSO sigue en este programa como la universidad de la tecnicatura.", "si «sigue en el programa» es en este programa de gobierno o en el manejo de las cámaras (según las notas de Nick, la UNSO operó las fotomultas de 2022 a 2025 y es la de la tecnicatura)"),
84: (K, "El aviso, el mapa y el reclamo son parte de la inteligencia artificial del Municipio. La paga el área municipal de Ciencia y Técnica (4.11)."),
85: (K, "Los equipos y su mantenimiento se pagan con el fondo de seguridad vial. Eso no cambia las cuentas del Municipio, porque ya gasta en esto más de lo que cobra en multas. En 2025 se cobraron 3.819 millones de multas en la vía pública. Ese año, el Municipio gastó 7.199 millones en semáforos, señales y movilidad."),
86: (K, "En 2024 se pagaron entre 13.000 y 456.000 multas."),
87: (X, "global: jerga de presupuesto («gasto flexible libre»)"),
88: (K, "EL MUNICIPIO SOLO"),
89: (K, "Nota: sin la Provincia, quien más gana sigue pagando menos en proporción a su ingreso."),
90: (K, "Para quien más gana, una multa según el ingreso, como en Finlandia. Sería sólo para faltas graves, y únicamente cuando da más que la multa común."),
91: (K, "Un agregado al convenio de multas de 2020 con la Provincia, para proteger las cuotas que da San Isidro. Congelar la deuda en pesos, para que no suba con el valor de la unidad de multa, como hizo la Provincia en 2020."),
92: (K, "Las dos propuestas más grandes son empleo y vivienda, y la obra pública que deciden los vecinos. Se pagan de tres maneras. Una es actualizar los valores de 2008 con los que hoy se cobra la tasa de servicios generales. Otra es usar parte del dinero que el Municipio puede decidir libremente. La tercera es cambiar el destino de una parte de lo que ya se gasta en obra."),
93: (K, "Ninguna sale del gasto en personal. Las cuentas del capítulo 3 tratan ese gasto como fijo, justamente porque este programa no lo toca."),
94: (X, "global: jerga de presupuesto («partida de contratación»); la elipsis se entiende con la oración anterior"),
95: (K, "Cualquiera tiene que poder preguntar cuántos empleados hay en el Municipio y cuánto cobra cada categoría. La revisión de la sección 5.10 no pudo comprobar si esa información está publicada. Aunque sea información sobre los propios empleados, se contesta igual."),
96: (X, "se entiende que es una línea de teléfono"),
97: (K, "El empleado municipal que quiera puede trabajar el sábado y el domingo, y tomarse francos entre semana."),
98: (V, "Son cuatro áreas que están dentro de promoción y asistencia social, el gasto del Municipio que más cayó en 2025. Niñez, personas mayores y género comparten un solo programa del presupuesto. Discapacidad tiene un programa propio, que es el más chico.", "de qué es «el más chico» el programa de discapacidad (¿de las cuatro áreas o de todo el presupuesto?)"),
99: (X, "se entiende; la precisión no cambia la lectura"),
100: (K, "Además, el mapa de los chicos y el de las personas mayores son opuestos."),
101: (X, "global: «la propuesta» → «nuestra propuesta»"),
102: (X, "global: «necesidades básicas insatisfechas» sin explicar"),
103: (K, "De las tres, proponemos la más barata, que es también la que se necesita primero."),
104: (K, "Es un curso gratuito de 380 horas, distinto de la tecnicatura en inteligencia artificial."),
105: (V, "El relevamiento que propone la sección 5.3 va a decir cuántos cuidadores más hacen falta.", "si el relevamiento del 5.3 ya se hizo o es una propuesta"),
106: (K, "La línea de atención publicada es un número de celular de guardia para mandar mensajes, y no un teléfono oficial."),
107: (X, "se entiende: «lo» es el dato de certificados del párrafo anterior"),
108: (N, "NUESTRA PROPUESTA, SIN DINERO NI OFICINAS NUEVAS: CON LO QUE CADA ÁREA YA TIENE EN EL PRESUPUESTO", "cambia el título de un recuadro; hay que confirmar si «el programa» es el del presupuesto o este programa de gobierno"),
109: (K, "6 · Lo que los vecinos le cuentan a la inteligencia artificial del Municipio (4.11) se ordena por zona. Así, la dirección de género ve en qué zonas tiene que estar."),
110: (K, "6 · Lo que ya propusimos más arriba. Cualquiera va a poder preguntar cuántos certificados de discapacidad dio la junta municipal en su zona."),
111: (K, "Un intendente gobierna sobre más cosas que las once áreas de este capítulo."),
112: (K, "Acá sólo se marca la comparación con agua y cloacas."),
113: (K, "Policía, escuelas, justicia y salud de alta complejidad"),
114: (X, "se entiende: las etiquetas están arriba de cada área"),
115: (X, "global: siglas sin explicar («UNSO»)"),
116: (K, "Los contratistas del Municipio toman al menos el 75% de su personal entre gente del partido. Además, una parte de cada licitación queda para las pymes del partido. Al egresado que no queda contratado, un semillero de empresas le da su primer cliente."),
117: (X, "global: términos del capítulo 4 («las asambleas», «la obra vecinal»), propuestas en presente y jerga de presupuesto («partida»)"),
118: (V, "Hay que cortar, en su origen, la cloaca que llega al río. También hay que frenar la basura. Cada tramo de la costa va a tener una bandera que diga, cada día, si el agua está apta para bañarse.", "qué quiere decir «cortar la cloaca donde nace» (¿cortar en su origen las descargas cloacales que llegan al río?)"),
119: (V, "La da el mismo grupo de empresas desde 1998, con un contrato de 2009 firmado sin licitación. Proponemos licitarla dividida en dos zonas, y mantener a todos sus trabajadores. El pago va a depender de lo que se mide del servicio.", "que «contrato directo» quiere decir firmado sin licitación, y qué se mide para pagar"),
120: (X, "se entiende: son excepciones a las reglas de construcción"),
121: (K, "En cada uno de esos parques va a haber foodtrucks, baños gratis, clases y espectáculos durante la semana."),
122: (K, "También proponemos que la inteligencia artificial del Municipio saque el turno y se lo recuerde al paciente. Si alguien no va a ir, ese lugar se le da a otra persona."),
123: (K, "El sistema de inteligencia artificial que el Municipio anunció en 2023 para los hospitales va a pasar por una auditoría."),
124: (V, "También proponemos una oficina para los delitos por internet. Además, quien fue acusado sin motivo va a poder pedir una constancia que lo diga.", "qué es la «constancia para quien es acusado sin causa» (ver el 5.7)"),
125: (X, "global: propuestas en presente"),
126: (X, "global: propuestas en presente"),
}

globals_ = [
"GLOBAL | «necesita dictamen de un abogado», repetido y sin explicar | 34, 35, 37 | Cambiarlo en todo el documento por una sola fórmula llana, por ejemplo «(esto lo tiene que confirmar un abogado)». | sí",
"GLOBAL | «la propuesta» en lugar de «nuestra propuesta» | 34, 35, 38 | Extender la corrección 13 al texto corrido: «La propuesta es…» y «La propuesta:» pasan a «Nuestra propuesta…» (los títulos de recuadro van aparte). | sí",
"GLOBAL | propuestas contadas en presente, como si ya pasaran | 34, 37, 38, 39 | Lo que proponemos va en futuro («va a…»), sobre todo en el resumen del 5.15 y en los recuadros; el presente queda para lo que existe hoy. | sí",
"GLOBAL | términos del capítulo 4 sin recordar qué son («la comisión de la zona», «el panel sorteado», «las asambleas», «la obra vecinal», «el índice de necesidad») | 34, 37, 39 | La primera vez que aparecen en cada sección del capítulo 5, sumar una aclaración corta, por ejemplo «el panel de vecinos elegidos por sorteo (capítulo 4)». | no",
"GLOBAL | jerga de presupuesto («ceden su gasto», «partida», «renglón», «gasto flexible libre», «cambiar de destino», «partida de contratación», «bienes de uso») | 35, 36, 37 | Usar siempre las mismas palabras comunes: «la parte del presupuesto que el Municipio puede decidir libremente» (como en el texto aprobado del Dispatch 14), «dinero», «una cuenta propia en el presupuesto». | no",
"GLOBAL | siglas sin explicar («UNSO», «CFL») | 34, 37, 38, 39 | Explicar la sigla la primera vez en cada capítulo, sin nombres de personas: «la UNSO, la universidad nacional con sede en San Isidro»; confirmar si la «Universidad Nacional de San Isidro» del 5.8 es la UNSO y usar un solo nombre. | no",
"GLOBAL | «necesidades básicas insatisfechas» sin explicar | 34, 38 | Explicarlo una sola vez, donde aparece por primera vez en el documento: «hogares a los que, según el censo, les falta algo básico, como una vivienda adecuada o un baño». | no",
"GLOBAL | «la inteligencia artificial» suelta, sin «del Municipio» (regla 7) | 35, 37, 38 | Toda mención a nuestra inteligencia artificial dice «la inteligencia artificial del Municipio»; quedan varias en el 5.9, el 5.11 y el 5.13 que el lector no marcó. | no",
]

title_fix = {
26: "LO QUE SE PERDIÓ EN LA COSTA, CONTADO ENTERO",
33: "LA VARA LA PUSO MIAMI, Y DESPUÉS LA COMPRÓ",
88: "HOY, EL MUNICIPIO",
108: "LA PROPUESTA, SIN DINERO NUEVO NI OFICINAS NUEVAS: CON LO QUE EL PROGRAMA YA TIENE",
}

assert len(rows) == 126, len(rows)
assert set(dec) == set(range(1, 127))
out = []
cnt = {K: 0, V: 0, N: 0, X: 0}
for i, (pg, orig) in enumerate(rows, 1):
    d = dec[i]
    lab = d[0]
    cnt[lab] += 1
    o = title_fix.get(i, orig)
    if lab == K:
        out.append(f"{K} | {pg} | {o} | {d[1]}")
    elif lab in (V, N):
        out.append(f"{lab} | {pg} | {o} | {d[1]} | {d[2]}")
    else:
        w = ' '.join(o.split()[:8])
        out.append(f"{X} | {pg} | {w} | {d[1]}")
out += globals_
out.append(f"TOTAL | KEEP {cnt[K]} | VERIFY {cnt[V]} | NICK {cnt[N]} | DROP {cnt[X]}")
open(D + 'filt_G.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(out[-1])

# checks on proposals
bad = re.compile(r'\b(mafia|plata|sobreprecio|en castellano|datos actualizados)\b', re.I)
stop = set('para como sólo solo están entre sobre desde hasta donde cuando porque pero también además este esta esto estos estas otra otro otros otras cada todo todos toda todas tiene tienen puede pueden hace hacer menos mucho muchos'.split())
for i in sorted(dec):
    d = dec[i]
    if d[0] not in (K, V, N):
        continue
    prop = d[1]
    if bad.search(prop):
        print('BANNED', i, prop)
    for s in re.split(r'(?<=[.:;])\s+', prop):
        s2 = re.sub(r'^\d+\s*·\s*', '', s).strip()
        if re.match(r'^(Y|Que|E)\b', s2):
            print('START', i, s2[:60])
        words = re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', s.lower())
        seen = {}
        for w in words:
            if len(w) >= 5 and w not in stop:
                seen[w] = seen.get(w, 0) + 1
        reps = [w for w, c in seen.items() if c > 1]
        if reps:
            print('REP', i, reps, '::', s[:90])
    for m in re.finditer(r'inteligencia artificial(?! del Municipio)', prop):
        print('IA', i, prop[max(0, m.start()-40):m.end()+20])
