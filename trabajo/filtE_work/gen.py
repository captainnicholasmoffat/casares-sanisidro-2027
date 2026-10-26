import re, sys
base = sys.argv[1]
src = [l.rstrip('\n') for l in open(base + '/out_E.md', encoding='utf-8') if l.strip()]
orig = []
for l in src:
    p = [x.strip() for x in l.split(' | ')]
    orig.append((p[0], p[1]))

K, V, N, D = 'KEEP', 'VERIFY', 'NICK', 'DROP'
E = {
1: (N, "Las dos propuestas más grandes, empleo y vivienda y la obra vecinal, ya ocupan el 41,4% del gasto flexible. Todo lo que sigue entra en el 58,6% que queda, o no cuesta nada.", "Nick sacó el 41,4% del capítulo 3 (corrección 9) para no mostrar dos porcentajes; acá sigue, y el 58,6% libre choca con el 46,7% del texto aprobado."),
2: (V, "San Isidro gasta, sobre todo, en salud y en obra, que en el gráfico figura como «Urbanismo». Entre las dos funciones se llevan casi la mitad del presupuesto.", "Qué incluye la función «Urbanismo»: si incluye la recolección de residuos, no es sólo obra."),
3: (D, "Se entiende: remata la oración anterior («La que se llama Trabajo es la última»)."),
4: (K, "Propuesta: llevar el gasto en empleo y vivienda a 7.730,9 millones anuales cuando el programa funcione completo, algo que se alcanza en cuatro años. Es quince veces lo que hoy se gasta en empleo y vivienda juntos. El capítulo 3 explica cómo se paga (3.5)."),
5: (K, "El Municipio funciona como una bolsa de trabajo. Las empresas privadas crean y pagan el empleo, y el Municipio pone en contacto a las dos partes."),
6: (K, "No se encontró ninguna regla que obligue a las empresas que cobran del Municipio a contratar gente del partido."),
7: (K, "Este programa agrega lo que hoy falta: usar el presupuesto del propio Municipio para dar empleo en el partido. Las obras y los servicios que el Municipio ya paga los hacen empresas y cooperativas del partido, con gente formada acá."),
8: (D, "Se entiende: «el que paga él» se lee como el que paga el Municipio."),
9: (D, "Se entiende: el recuadro de la misma página explica La Cava 4.0."),
10: (D, "global: siglas de universidades sin desarrollar."),
11: (D, "global: leyes citadas sólo por número."),
12: (K, "Proponemos usar la obra vecinal como política de empleo. Al cuarto año, el capítulo 4 destina 28.908 millones anuales a obras que hacen cooperativas de vecinos. Esas obras dan trabajo a gente del barrio."),
13: (K, "El tutor es uno de los profesores del alumno, el que mejor lo conoce. Por eso es quien lo conecta con el empleador. Tener ese tutor es lo que diferencia a los programas que funcionan de los que entregan un certificado y dejan sola a la persona. Ese papel, junto con el sueldo, atrae a gente capaz a enseñar."),
14: (K, "Hoy, sobre los vecinos que consiguieron trabajo por el portal del Municipio, sólo hay una gacetilla, y no un registro."),
15: (V, "Hay muchos trabajos que hacen equipos contratados por el Municipio. Por ejemplo, la plataforma de la inteligencia artificial del Municipio (capítulo 4), el análisis de video de seguridad, las habilitaciones de comercios y los turnos de salud.", "Si «contratados acá» quiere decir contratados por el Municipio."),
16: (D, "global: «panel» sin decir cuál."),
17: (K, "El profesor con más alumnos que se gradúan y consiguen trabajo recibe una mención y un premio en dinero. Ese dinero sale de una parte del presupuesto reservada para incentivar a los docentes."),
18: (K, "Hay una cuarta regla, que vale para todo contrato del Municipio. Incluye obras, servicios, desarrollos tecnológicos y los trabajos de las asociaciones vecinales. Al menos el 75% del personal tiene que vivir en el partido desde hace un año o más. Para cubrir ese 75%, los egresados del programa tienen prioridad."),
19: (N, "La Corte Suprema anuló en 2010 cupos provinciales para residentes. En 2022, la justicia bonaerense anuló una preferencia local que Olavarría aplicó sin reglas previas.", "Sacar los nombres de empresas (regla 5) deja los dos fallos sin su cita; decidir si la regla alcanza a las citas judiciales."),
20: (K, "Por eso el mínimo no es el 100%, y pide un año de residencia, no cinco. También admite excepciones, que se justifican ante el panel. La regla se escribe en el pliego de cada licitación antes de llamarla. El texto está en la Ordenanza X del anexo."),
21: (D, "global: jerga censal (radio censal, fracción, NBI)."),
22: (K, "Según el mapa colaborativo OpenStreetMap, el punto central del barrio La Cava queda a 136 metros del centro de la zona que marca el capítulo 4. Esa zona mide 0,28 km²."),
23: (K, "No hace falta adivinar de qué barrio se trata. En esa zona está el Centro de Formación Laboral Nº 404 Barrio La Cava. Lleva el nombre del barrio."),
24: (N, "También dispuso un reconocimiento a su director, que es quien encabeza este programa (Resolución Nº 26, sesión del 6 de agosto de 2025). Es un antecedente nuestro.", "Es el nombre del candidato: la regla 5 prohíbe nombres de personas y sólo Nick puede exceptuarlo."),
25: (K, "Lo que proponemos. Abrir, con recursos del Municipio, centros como este donde hoy no hay ninguno. Para eso se usa la misma regla con la que la Provincia abre centros nuevos."),
26: (V, "Si la Provincia no cubre esos cargos, los paga el Municipio, por el sistema de «matrícula indirecta».", "Qué es la «matrícula indirecta», para explicarla en pocas palabras."),
27: (K, "La formación cuesta tres millones por persona si paga todo el Municipio."),
28: (D, "Se entiende con la oración siguiente; la propuesta cambia el sentido de «2015»."),
29: (D, "Se entiende: «economía del conocimiento» es de uso común en los diarios."),
30: (K, "Además, formar en inteligencia artificial cuesta muchísimo menos. Un taller de fabricación necesita máquinas, espacio, seguridad y mantenimiento. En cambio, un aula de inteligencia artificial necesita equipos livianos y conexión."),
31: (V, "Para un barrio aislado, eso no es un detalle técnico. Quiere decir que sus vecinos pueden trabajar desde ahí, para clientes de cualquier lugar.", "Qué quiere decir el contraste entre «mejorar el barrio» y «trabajar desde él»; la propuesta deja sólo la segunda idea."),
32: (D, "Se entiende; el cuadro 31 detalla qué piden esas certificaciones."),
33: (K, "Cada una apunta a uno de los puestos que más crecen según un informe de empleo de 2026 (cuadro 31). Para quien quiera fundar su propia empresa está el semillero, que se explica más abajo."),
34: (K, "Los puestos del cuadro 31 son de Estados Unidos, y la formación apunta también al trabajo a distancia. Más de un cuarto de esos puestos se hace a distancia, en tres de las cuatro orientaciones. En Estados Unidos, la mitad de los ingenieros en inteligencia artificial consigue ese puesto con más de 3,7 años de experiencia. Nuestros egresados entran como juniors, y la pasantía achica la diferencia."),
35: (N, "Programas que funcionan sobre modelos de inteligencia artificial, con herramientas de código abierto y búsqueda en documentos propios (RAG)", "Sacar los nombres de herramientas (regla 5) le quita precisión al plan de estudios; decidir si la regla alcanza al cuadro 31 y a su fuente."),
36: (K, "Sin acceso gratis, el que puede pagar una suscripción aprende, y el que no, mira. Así, adentro del aula se repetiría la desigualdad que el capítulo 1 muestra afuera. Incluso sería peor, porque el que ya está atrás terminaría la carrera sin haber usado la herramienta."),
37: (K, "El otro es un escritorio remoto en la nube: una computadora potente, ubicada lejos, que el alumno usa por internet. Así alcanza con una computadora vieja. La computadora remota hace el trabajo pesado, y en la casa sólo hacen falta una pantalla y conexión."),
38: (K, "El Municipio licita el acceso a los modelos, que son los programas de inteligencia artificial. Para elegir, primero se mira la capacidad: las universidades del partido prueban qué modelo rinde mejor."),
39: (D, "Se entiende: el resto del programa ya prefiere a las empresas del partido."),
40: (V, "Se pierden las formas de trabajar que no se adaptaron a estas herramientas, no el oficio.", "Si «lo que no se adaptó» son formas de trabajar o personas."),
41: (K, "La otra cara de este cambio es que la demanda crece, porque aparecieron trabajos que antes no convenía hacer."),
42: (V, "Por eso el egresado no sale a competir por un puesto de principiante. Sale habiendo trabajado en la plataforma de la inteligencia artificial del Municipio, que ya funciona, y con partes construidas por él que están en uso. También sale con las auditorías que hizo y con el título de la UNSO.", "Qué auditorías hace el alumno: el capítulo 5 no las nombra antes."),
43: (D, "global: leyes citadas sólo por número."),
44: (K, "Cobra 240.000 $ por mes. Es el sueldo con el que entra un empleado del Municipio, calculado para veinte horas por semana."),
45: (K, "Por qué con la UNSO. La Ley 26.427 incluye a la formación profesional (artículo 1). Pero en la Provincia la deja afuera una resolución de la Dirección General de Cultura y Educación, la 5356/24. Esa resolución sólo le permite prácticas que no se pagan. En cambio, a los alumnos de una carrera universitaria la ley los cubre sin depender de esa resolución."),
46: (D, "Se entiende: «llave» es una metáfora común."),
47: (D, "global: siglas de universidades sin desarrollar."),
48: (D, "Se entiende: sigue la serie de la oración anterior («una de la UTN», «la pagan»)."),
49: (D, "global: juniors y seniors sin explicar; el personal reasignado se explica en el mismo apartado."),
50: (D, "Se entiende: es la asociación vecinal del capítulo 4."),
51: (V, "El tope se cuenta sobre los pasantes que están trabajando en ese momento. Los supervisores se cuentan igual: hay uno cada diez de esos pasantes, presente todo el horario. Son 928 pasantes por año y cada uno pasa seis meses en el Municipio. Por eso hay 464 a la vez.", "Que el supervisor cada diez se cuenta sobre los pasantes presentes (cuadro 33: 95 supervisores)."),
52: (V, "Los segundos seis meses de la pasantía se hacen en una empresa del partido o en una contratista del Municipio. Rige la misma regla: sólo proyectos nuevos, nunca puestos de trabajo. Esa parte la paga la empresa. Para eso hay un convenio marco con la Cámara de Comercio y Servicios del Partido de San Isidro.", "Si el convenio marco con la Cámara ya existe o es una propuesta (si es propuesta, «Para eso proponemos un convenio marco…»)."),
53: (K, "¿Qué pasa si a alguien no le toca una empresa en los segundos seis meses? Primero puede ocupar uno de los hasta 92 lugares que quedan en el Municipio antes de llegar al tope de 556."),
54: (D, "global: «gasto flexible» sin explicar."),
55: (K, "Su premio lo paga el Municipio, de forma pública. Los convenios con el centro de formación y con la UNSO incluyen dinero reservado para premiar a los docentes. Cada institución le paga ese premio a su profesor con más alumnos que se gradúan y consiguen trabajo. Ese dinero es del Municipio, y la institución sólo lo entrega. Así, el tutor no tiene un cargo en el Municipio, algo que el artículo 10 de la ley le prohíbe al docente guía."),
56: (K, "Ese supervisor es, en las áreas, un empleado del Municipio que cambió de tarea. En la plataforma, es uno de sus programadores con más experiencia (los seniors)."),
57: (K, "Son 77 empleados del Municipio. Hay 45 supervisores y 26 que sostienen el trabajo de noche y los fines de semana. Los otros 6 atienden, uno en cada zona, a quien no puede usar solo la inteligencia artificial del Municipio. Siguen cobrando su sueldo, no el de un pasante."),
58: (V, "Además, el costo nuevo del programa es menor, porque esos sueldos ya se pagan. Hasta el mes 27 de la gestión, el trabajo de todos los días lo sigue haciendo el personal actual. Los juniors se hacen cargo cuando se reciben.", "Desde cuándo se cuenta el mes 27 (¿desde que asume el nuevo gobierno?)."),
59: (V, "Uno que carga la información pública que, según la sección 5.10, hoy no se puede ver o está escondida, cada dato con su documento de origen", "Qué información es y dónde se carga."),
60: (D, "Se entiende con el título del apartado y la oración siguiente."),
61: (D, "global: notas internas «(necesita dictamen de un abogado)»."),
62: (K, "4 · La puerta es el título. En los primeros tres meses de gestión, este programa pide que el título de la tecnicatura tenga validez nacional (6.4)."),
63: (K, "5 · Quién firma. Firman el rector de la UNSO y el intendente, con permiso del Concejo (Ley Orgánica, artículo 41, necesita dictamen de un abogado). El puente lo coordina una persona del equipo de la plataforma."),
64: (K, "La meta es que, cada año, entre 250 y 300 egresados consigan un empleo pago después de la pasantía. El primer escalón es trabajar uno o dos años como junior en los puestos que hacen falta para que funcione la inteligencia artificial del Municipio."),
65: (K, "Si trescientos juniors por año se quedaran, a sueldo de mercado costarían más de 28.000 millones a los cuatro años. En cambio, como los puestos rotan y se pagan con la escala de sueldos del Municipio, los juniors de las áreas cuestan 720 millones por año."),
66: (K, "[Borrar: repite cifra por cifra el cuadro 34, que está al lado (regla 10).]"),
67: (K, "Hoy el reparto es casi al revés: el 33,7% va a empleo y el 66,3% a vivienda. La razón del cambio es que, con este programa, las redes de cloaca y gas se pagan con la obra vecinal del capítulo 4."),
68: (K, "Dejar dos tercios para vivienda sería pagar dos veces lo mismo. [Borrar la segunda oración: ya la dicen el párrafo de arriba y el cuadro 34.]"),
69: (K, "El costo de tres millones por persona es una decisión de este programa. Otros programas prometen miles de egresados porque calculan el costo de los docentes con lo que se les paga hoy. Por eso su certificado no vale nada."),
70: (K, "Con esos tres millones se pagan el equipamiento, el acceso a las herramientas y los profesores. Uno de ellos es el tutor, que acompaña al alumno hasta el empleo. También se pagan el premio a los docentes, las materias y el título de la UNSO."),
71: (K, "Los 928 lugares se reparten entre las localidades con el índice de necesidad del capítulo 4. Es el mismo índice que decide cuánto dinero de la obra vecinal le toca a cada zona."),
72: (K, "Suman justo las 928 que paga el presupuesto. Al redondear, los lugares que sobran van a las localidades con los decimales más altos."),
73: (K, "Los tres millones por persona son el número que más pesa en todo el programa. Si ese costo resulta menor, se forma a más gente con el mismo dinero."),
74: (K, "Por eso la formación se lleva la mayor parte del dinero para empleo: el 60%."),
75: (K, "Los programas que sí funcionan en la región combinan capacitación con experiencia de trabajo real en empresas. Además, suman un tutor que conecta al egresado con el empleador. Es justo lo que propone este programa."),
76: (K, "El semillero ayuda a los egresados a armar su propia empresa. Es para el que no queda contratado. Se entra en equipo, con un proyecto, en una de las dos convocatorias del año, que se abren después de cada egreso."),
77: (V, "Cuando el programa funcione completo, van a nacer veinte empresas por año: diez por convocatoria, de tres egresados en promedio. En los cuatro años del mandato serían dieciséis en total, porque los primeros egresados recién salen en el mes 27.", "Por qué en el mandato son dieciséis (¿porque los primeros egresados salen en el mes 27?)."),
78: (D, "Se entiende: las oraciones siguientes dicen qué incluye."),
79: (K, "El primer cliente, por pliego. El pliego de cada licitación obliga a subcontratar el 20% a pymes del partido, de cualquier antigüedad. De ese 20%, una parte igual al 5% del valor total del contrato queda para empresas del partido con menos de cinco años. Entre esas empresas, las del semillero van primero."),
80: (K, "En los contratos más grandes, eso suma 15.635,6 millones para pymes y 3.908,9 para empresas nuevas. Esos contratos son la recolección de residuos y la mitad de la obra pública que, en el cuarto año, todavía hacen empresas privadas."),
81: (K, "Si la empresa que gana la licitación no encuentra una pyme del partido que haga ese trabajo, lo tiene que justificar ante el panel, igual que con la regla del 75%."),
82: (K, "El Municipio le paga la parte subcontratada directamente a la empresa chica. Para eso, la empresa grande le pasa su derecho a cobrar esa parte, lo que se llama «cesión del crédito». El Tribunal de Cuentas bonaerense lo admite."),
83: (K, "Además, el pliego puede prever un adelanto al firmar. A cambio, la empresa presenta una póliza de caución por el total, que es un seguro que cubre al Municipio si no cumple."),
84: (V, "También proponemos un fondo que multiplica la inversión. Por cada peso que una empresa del semillero consiga de inversores privados, de la Nación o de la Provincia, el Municipio le presta otro igual.", "Si «capital nacional o provincial» quiere decir fondos de la Nación y de la Provincia."),
85: (V, "El fondo se crea por ordenanza. Presta dinero y no compra partes de las empresas, porque el Municipio no puede ser dueño ni socio de ellas (5.7). Además, hace falta porque el fondo nacional para emprendedores de la Ley 27.349 se disolvió en 2024.", "Si este fondo viene a ocupar el lugar del fondo nacional disuelto en 2024, y que la Ley 27.349 es la de apoyo a emprendedores."),
86: (K, "El semillero cuesta 121 millones por año y se paga con el dinero de Ciencia y Técnica. Entre el semillero y la plataforma de la inteligencia artificial del Municipio, se usa el 22,0% de ese dinero."),
87: (K, "Sigue las mismas reglas que cualquier obra. En el presupuesto cuenta como obra (bienes de uso). La puede elegir una comisión vecinal. También la puede hacer una asociación vecinal, como permite el artículo 132."),
88: (D, "global: jerga censal; el resto se entiende."),
89: (K, "Este programa se compromete a medirla. La conexión se mide en cada zona, durante la primera ronda de asambleas vecinales."),
90: (D, "global: «partida» como jerga de presupuesto."),
91: (D, "global: «partida» como jerga de presupuesto; la cita del artículo 132 no traba la lectura."),
92: (K, "También es lo que se puede sumar sin tocar sueldos, deudas ni contratos firmados: 3.455 millones más, el 4,0% del gasto flexible."),
93: (D, "Se entiende lo esencial: sale de otros gastos, sin fondos nuevos."),
94: (K, "Un dato para tener en cuenta. Ambiente creció 23,1% entre 2024 y 2025, descontada la inflación."),
95: (D, "Se entiende: la comparación 19.000 contra 126 muestra qué es el valor guía."),
96: (D, "Se entiende: en el documento va justo después de «…por la Ordenanza 5304» (el texto extraído cambia el orden de las columnas)."),
97: (K, "Está en General Pacheco 1545 y el río, en Martínez. Según un diario, la arena está sobre una base de piedras en canastos de alambre."),
98: (K, "Cuando el agua está justo en el límite de lo apto, se compara a los que se metieron con los que no. Los que se metieron tienen unos cuatro casos más de malestar por cada cien personas."),
99: (K, "Los jueces condenan al municipio que habilita una playa sin cuidar a los bañistas, y protegen al que avisa del peligro con claridad."),
100: (V, "Primero, analizar el agua con un marcador de ADN humano: un estudio de laboratorio que muestra si la suciedad viene de cloacas. Cuesta unos 5.000 a 15.000 dólares.", "Que el marcador de ADN humano sirve para saber si la contaminación viene de cloacas (de personas y no de animales)."),
101: (K, "Tercero, si el problema es la red de AySA, exigirle el arreglo ante el organismo que la controla, con el artículo 16 de las normas de su servicio. Cuarto, si el problema son casas con la cloaca conectada al desagüe de lluvia, darles a los dueños una orden formal de corregirlo y ayudarlos a pagar el arreglo, como en París."),
102: (K, "El compromiso es el resultado: que deje de entrar cloaca al río. No prometemos una obra que todavía nadie diseñó."),
103: (V, "Ya las pedía para Perú, en 2012, el Plan de Manejo de la Reserva Ribera Norte.", "Qué reserva es (¿la Reserva Ribera Norte?)."),
104: (K, "Para vaciar las barreras, la cuadrilla usa el camión con grúa y pinza que el Municipio ya alquila."),
105: (V, "Para las rejas y las barreras se llama a concurso a las cooperativas de trabajo del partido, con un contrato por resultado: se paga por cada boca vaciada. Si las cooperativas cobran menos de lo que le cuesta al Municipio hacerlo con su cuadrilla, el trabajo queda en sus manos (necesita dictamen de un abogado).", "Menos que qué: ¿que el costo de la cuadrilla municipal?"),
106: (K, "El proyecto técnico de las barreras define tres cosas: dónde está exactamente la boca de Alto Perú, para qué crecida del río se diseña el anclaje y el permiso de la Autoridad del Agua. El permiso del dueño de la dársena, el lugar donde amarran las embarcaciones, necesita dictamen de un abogado. Otras soluciones, como robots y barcazas que juntan basura, no sirven en una costa abierta como esta."),
107: (K, "El baño se habilita en los tramos de prueba con arena (punto 6), con los guardavidas que pide la ley y la bandera del día."),
108: (D, "Se entiende: la misma página dice que la Ordenanza 5304 prohíbe el baño."),
109: (K, "Se empieza por el Parque del Águila y el Bosque Alegre. Las asociaciones de cada parque participan desde el diseño (más abajo)."),
110: (K, "También proponemos un comité de cuenca de la costa norte dentro de la Autoridad del Agua: una mesa donde los municipios tratan juntos los desagües que comparten. La Autoridad del Agua ya creó uno para Berazategui, Quilmes y Florencio Varela."),
111: (D, "global: «panel» sin decir cuál; el resto se entiende."),
112: (D, "Se entiende: la unidad está en la oración anterior."),
113: (V, "Ese aumento empieza a llegar en el mes 12 de la gestión. Por eso, el primer año se adelanta lo que cuesta empezar: el diagnóstico de Perú, el piloto, las muestras y la primera temporada de guardavidas. Son unos 335 millones. Salen de lo que otros programas del presupuesto ceden (cuadro 15), y no de lo que Ambiente ya tiene.", "Desde cuándo se cuenta el mes 12 (¿desde que asume el nuevo gobierno?)."),
114: (V, "Es el contrato más caro del Municipio, y cuesta casi tanto como toda la obra pública de un año.", "Que es el contrato más caro: Salud gasta 78.217 millones (gráfico 28), más que estos 49.270."),
115: (K, "La licitación 01/2004 quedó frenada treinta días por una medida cautelar de un tribunal laboral. No se encontró el documento oficial que la da por terminada."),
116: (D, "global: jerga de licitaciones."),
117: (D, "global: jerga de licitaciones."),
118: (D, "Se entiende con el título del apartado y la oración siguiente."),
119: (D, "Se entiende: la columna en blanco ya muestra que falta el decreto; sumar la conclusión agrega una afirmación."),
120: (D, "Se entiende: «agregados» se lee como lo que se fue agregando."),
121: (K, "Además, el Municipio llama «adjudicataria» a la empresa que da el servicio, como si hubiera ganado una licitación. Sin embargo, según los papeles municipales, la contrató en forma directa, después de una licitación desierta."),
122: (V, "Dos zonas, licitadas por separado. Así hay competencia y un segundo precio para comparar, algo que no se publica desde 1998. Por la misma razón, en salud proponemos publicar el precio por unidad de cada compra (5.6).", "Que publicar el precio por unidad en salud es una propuesta del 5.6 y no algo que ya se hace."),
123: (K, "El Municipio paga lo que vale la antigüedad que cada trabajador acumuló hasta el cambio de empresa, después de controlarla. Se calcula con una lista del personal que se cierra el día que se llama a licitación. Desde ese día, cada empresa incluye la antigüedad nueva en su precio. Cada año que pasa sin licitar, lo que el Municipio debe por esa antigüedad crece unos 650 millones (6.6)."),
124: (D, "Se entiende: el descuento es por no cumplir el resultado."),
125: (K, "Los residuos reciclables y los que sirven para hacer compost quedan fuera de este contrato. De ellos se ocupan cooperativas del partido, siempre que no choque con el convenio colectivo del sector."),
126: (D, "Se entiende con el título del apartado y la cita que sigue."),
127: (K, "Las normas del Municipio tampoco fijan límites en decibeles para los vehículos que circulan."),
128: (K, "Para un colectivo de un modelo aprobado después de 1997, fija 80 decibeles, u 83 si el motor es grande. A los modelos anteriores les fija 89. Cualquier vehículo en la calle, motos incluidas, no puede superar en más de tres decibeles el valor aprobado para su modelo."),
129: (K, "Pero ninguna ciudad lo aplica todavía, porque falta la aprobación oficial del aparato que mide el ruido."),
130: (K, "Para eso, el Municipio le pide gratis a la Nación un certificado de firma digital. Con ese certificado, la ley da por hecho que el archivo viene del Municipio y que no se cambió (Ley 25.506, artículo 10)."),
131: (K, "Para la moto sin silenciador, alcanza con verla y hacer el acta. Este punto necesita dictamen de un abogado, porque el artículo 81 pide avisarle antes al infractor, de manera formal."),
132: (K, "Así, las estaciones de medición (punto 5) se pueden mover sin pedirle a la Provincia un permiso para cada lugar. En la Argentina no hay aprobación oficial de sonómetros, los aparatos que miden el ruido. Por eso, la ordenanza define qué aparato vale: un sonómetro clase 1 o 2, con un certificado de laboratorio de no más de dos años."),
133: (K, "5 · Estaciones móviles. Se mueven según el mapa del ruido que arma la inteligencia artificial del Municipio, y moverlas no obliga a calibrarlas de nuevo."),
134: (K, "La inteligencia artificial del Municipio distingue un escape adulterado de una sirena o de una bocina. También une el sonido con la imagen de la cámara que lee la patente. Hoy no hay en uso ninguna cámara que haga todo esto sin que una persona revise."),
135: (K, "Hoy, cuando se autoriza a construir más de lo que permite la norma de la zona, se hace por decreto. Esas autorizaciones se llaman «factibilidades», y las firma el intendente."),
136: (K, "También hay «premios», que son metros de más para construir, a cambio de hacer cocheras, ceder terreno o demoler edificios con usos que la zona no admite."),
137: (K, "Esos decretos no se reparten de forma pareja entre las localidades."),
138: (K, "Es decir, el crecimiento de la ciudad también se concentra en algunas localidades."),
139: (K, "Además, no siempre se publica qué se autorizó. Se revisaron cien de esas decisiones desde diciembre de 2023. Catorce permitieron construir más de lo que la zona admite como base."),
140: (K, "Otros tres aceptaron dinero en lugar del terreno para una calle: 2.030 millones de pesos de 2025 por 5.890 metros cuadrados."),
141: (K, "Sólo una vez un cambio de las reglas de urbanismo pasó por el Concejo, y se aprobó en veintidós días hábiles."),
142: (V, "Fue veintidós días hábiles después de entrar al Concejo, sin audiencia pública y sin estudios de impacto ambiental ni sobre las redes de agua y cloaca.", "Qué redes no se estudiaron (expediente de la Ordenanza 9432)."),
143: (D, "Se entiende: es vocabulario judicial de los diarios."),
144: (K, "El intendente no va a aprobar lo que rechacen los vecinos de la zona."),
145: (K, "Primero: no autorizar por decreto lo que rechacen los vecinos de la zona. Segundo: vetar la ordenanza de excepción que ellos rechacen. Con el veto, el Concejo sólo puede aprobarla igual si junta 16 de sus 24 votos (anexo, Ordenanza XIII)."),
146: (K, "Quien gana con la suba del valor de su terreno va a pagar una parte."),
}

GLOBAL = [
"GLOBAL | «gasto flexible» sin explicar | p22, p24, p26 | La primera vez en cada capítulo, explicarlo con las palabras ya aprobadas en el capítulo 3: la parte del presupuesto que el Municipio decide libremente, la que no está atada a sueldos, deudas ni contratos firmados. | no",
"GLOBAL | «partida» como jerga de presupuesto | p23, p24, p25 | Cambiar «partida» por «el dinero del presupuesto para…» o «el presupuesto de…», según el caso. | no",
"GLOBAL | «panel» sin decir cuál | p23, p25, p26 | La primera vez en cada capítulo, decir qué panel es y quién lo integra (verificar si el del 5.3 es el panel sorteado del capítulo 4). | no",
"GLOBAL | juniors, semi-seniors y seniors sin explicar | p23, p24, p25 | Explicarlos una vez, la primera vez que aparecen: junior es el egresado en su primer empleo; semi-senior y senior, quienes tienen más experiencia. | no",
"GLOBAL | jerga censal (radio censal, fracción, NBI) | p23, p25 | La primera vez en cada capítulo, explicar «radio censal» (el sector más chico en que el Censo divide el territorio) y escribir completo «necesidades básicas insatisfechas». | no",
"GLOBAL | leyes citadas sólo por número | p23, p24, p27 | La primera vez que aparece cada ley, decir en pocas palabras cuál es (por ejemplo, «la ley nacional de pasantías, 26.427»). | no",
"GLOBAL | siglas de universidades sin desarrollar (UNSO, UNICEN, UTN) | p23, p24 | Desarrollar cada sigla la primera vez; el nombre completo de la UNSO lleva el de una persona (Raúl Scalabrini Ortiz), y eso choca con la regla 5. | sí",
"GLOBAL | notas internas «(necesita dictamen de un abogado)» dentro del texto | p24, p26, p27 | Cambiar el paréntesis por una oración clara («Este punto lo tiene que confirmar un abogado») o pasarlo a las notas del capítulo. | sí",
"GLOBAL | jerga de licitaciones (pliego, llamado, adjudicar, desierta, adjudicataria) | p23, p25, p26 | Explicar una vez por capítulo, la primera vez que aparecen, qué es el pliego (las condiciones de la licitación) y qué es una licitación desierta (sin ganador). | no",
"GLOBAL | propuestas escritas en presente que se leen como algo que ya existe | p24, p25, p26 | Cuando una propuesta está al lado de lo que pasa hoy, marcarla con «proponemos» o escribirla en futuro. | sí",
"GLOBAL | «Ordenanza X» del anexo se lee como un dato sin completar | p23 | Numerar las ordenanzas del anexo con cifras (Ordenanza 10) en todo el documento, o aclarar que son números romanos. | sí",
"GLOBAL | nombres de empresas en fuentes de cuadros y en citas de fallos (LinkedIn, Zona Norte Visión, Argenova, Wayro) | p23 | Decidir si la regla 5 alcanza a las fuentes y a los nombres de los fallos; en el texto corrido se sacan, como se hizo con la calificadora de riesgo. | sí",
]

assert sorted(E) == list(range(1, len(orig) + 1)), 'faltan items'
out = []
cnt = {K: 0, V: 0, N: 0, D: 0}
for i in range(1, len(orig) + 1):
    page, o = orig[i - 1]
    e = E[i]
    lab = e[0]
    cnt[lab] += 1
    if lab == K:
        out.append(f"KEEP | {page} | {o} | {e[1]}")
    elif lab == V:
        out.append(f"VERIFY | {page} | {o} | {e[1]} | {e[2]}")
    elif lab == N:
        out.append(f"NICK | {page} | {o} | {e[1]} | {e[2]}")
    else:
        first8 = ' '.join(o.split()[:8])
        out.append(f"DROP | {page} | {first8} | {e[1]}")
for row in out + GLOBAL:
    body = row.split(' | ')
    for f in body[2:]:
        assert '|' not in f
out += GLOBAL
total = f"TOTAL | KEEP {cnt[K]} | VERIFY {cnt[V]} | NICK {cnt[N]} | DROP {cnt[D]}"
out.append(total)
open(base + '/filt_E.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(total)
# checks on proposals: no sentence starts with Y / Que; forbidden words
bad = re.compile(r'(^|[.!?:]\s+)(Y|Que)\s')
forb = ['mafia', 'plata', 'sobreprecio', 'en castellano', 'datos actualizados']
for i in E:
    if E[i][0] in (K, V, N):
        p = E[i][1]
        if bad.search(p):
            print('START Y/QUE', i)
        for w in forb:
            if w in p.lower():
                print('FORB', i, w)
