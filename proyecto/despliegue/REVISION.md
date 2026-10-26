# Plan de despliegue «San Isidro 2027» · Revisión

Datos del plan de despliegue del programa de gobierno, sacados del texto final (commit c462fcf). La página todavía no está armada. Este archivo explica cómo se armaron los datos de `acciones.json`, qué supuestos se tomaron, cuál es el camino crítico y qué huecos o contradicciones aparecieron en el programa.

## 1. Qué hay en acciones.json

- 293 acciones, de las cuales 133 son hitos (duración 0).
- 14 acciones críticas y 20 casi críticas (holgura de 1 a 5 días hábiles).
- Desde el 24 de octubre de 2027 (elección, fecha estimada) hasta el 10 de diciembre de 2031 (fin del mandato).
- Trece líneas de trabajo: «0 Transición» y las doce del pedido.
- Los mismos campos del ejemplo (code, task, stream, owner, team, dur, start, finish, float, critical, milestone, decision, steps, moves, sne, needs, note), más «fuente». El campo «moves» va vacío.
- En «steps» van los pasos o lo que hace falta. Cuando el programa lo dice, termina con «Cómo se comprueba», copiado de los cuadros 40, 41 y 42.
- En «sne» va la fecha desde la que la acción puede empezar: el primer día de su mes en el calendario, o una fecha fija.

| Línea de trabajo | Acciones |
|---|---|
| 0 Transición | 7 |
| 1 Mecanismo vecinal y obra pública | 23 |
| 2 Concejo y ordenanzas | 60 |
| 3 Presupuesto y tasas | 29 |
| 4 Inteligencia artificial del Municipio | 18 |
| 5 Empleo y formación | 41 |
| 6 Vivienda | 5 |
| 7 Salud | 13 |
| 8 Seguridad | 27 |
| 9 Costa y espacio público | 38 |
| 10 Cultura y espectáculos | 10 |
| 11 Habilitaciones e inspecciones | 13 |
| 12 Transparencia | 9 |

## 2. Reglas del plan

**Los meses del programa.** El mes n empieza el día 10 y termina el día 9 del mes siguiente. El mes 1 va del 10 de diciembre de 2027 al 9 de enero de 2028. El mes 3 va del 10 de febrero al 9 de marzo de 2028. El mes 12 va del 10 de noviembre al 9 de diciembre de 2028. El mes 48 va del 10 de noviembre al 9 de diciembre de 2031. Es la única regla que deja el 1 de marzo dentro del mes 3, como dice el calendario (cuadro 42). Con meses de calendario, el 1 de marzo caería en el mes 4. Se aplica igual a todo el plan.

**Días hábiles.** Se cuentan de lunes a viernes. No se descuentan feriados nacionales, provinciales ni municipales. Tampoco se descuenta el receso del Concejo, salvo donde el programa lo nombra: las sesiones ordinarias abren el 1 de marzo (6.6). Por eso las ordenanzas que entran en diciembre se tratan desde el 1 de marzo.

**Inicio y fin.** «start» es el primer día de trabajo. «finish» es el primer día hábil después del último día de trabajo, como en el ejemplo. Un hito tiene el mismo inicio y fin.

**Dependencias.** «FS» quiere decir que la acción empieza cuando termina la anterior. «SS» quiere decir que empieza cuando empieza la otra. «lag» son días hábiles de espera.

**Holgura y camino crítico.** La holgura («float») son los días hábiles que una acción se puede atrasar sin romper tres cosas: lo que destraba, el último día de su mes en el calendario del programa y el fin del mandato. Es el método del camino crítico, con los plazos del programa como fecha límite. Una acción es crítica si su holgura es cero. Las cuatro fechas fijas (elección, asunción, cien días y fin del mandato) tienen holgura cero.

**La asunción.** El texto lo confirma: «El mandato empieza el 10 de diciembre de 2027» (6.1). Lo repiten «Qué proponemos hacer» y «Para cerrar».

**Los cien días.** El texto dice que se cumplen el 19 de marzo de 2028 (6.1). Es domingo. En el plan, todo lo que exige ese hito termina a más tardar el viernes 17. Todo lo que el calendario pone en los meses 1 a 3 termina el 9 de marzo, diez días antes.

**La elección.** El programa no da la fecha. La regla nacional es el cuarto domingo de octubre anterior al fin de los mandatos (Código Electoral Nacional, artículo 53): el 24 de octubre de 2027. A agosto de 2026, la Provincia todavía no había fijado su fecha ni decidido si separa su elección de la nacional. El plan supone que vota el mismo día que la Nación, y lo marca como fecha estimada. Fuentes consultadas:

- Decreto 335/2025, que cita el artículo 53 del Código Electoral Nacional: https://www.argentina.gob.ar/normativa/nacional/norma-412945/texto
- Letra P, 22 de agosto de 2026, «Buenos Aires 2027: hola PASO, chau desdoblamiento»: https://www.letrap.com.ar/politica/buenos-aires-2027-hola-paso-chau-desdoblamiento-n5426002
- Aire de Santa Fe, 1 de agosto de 2026, «Elecciones 2027: qué provincias desdoblan y cuáles tienen fecha confirmada»: https://www.airedesantafe.com.ar/politica/elecciones-2027-que-provincias-desdoblan-y-cuales-tienen-fecha-confirmada-n665155

**Nivel de detalle.** Los primeros 18 meses van acción por acción. Después, el plan usa bloques de seis meses o de un año: los años de la rampa, los grupos de la formación, los presupuestos anuales y las aperturas de la costa.

**Responsables.** Siempre por cargo o por organismo, nunca por persona. En la transición, el responsable es el «Intendente electo». El anexo pide que un abogado especialista en municipios revise cada ordenanza antes de que entre al Concejo, y la nota de método lista lo que necesita su dictamen: por eso aparece como responsable de tres revisiones y un dictamen. Los equipos («team») son seis: Intendencia, Secretarías, Concejo, Vecinos, Equipo de la IA y Externos.

**Áreas sin línea propia.** El pedido fija doce líneas. Estas áreas del programa se ubicaron así:

- Niñez (centros de apoyo escolar) y la tecnicatura: 5 Empleo y formación. El profesor digital: 4 Inteligencia artificial del Municipio.
- Personas mayores y discapacidad (los cien cuidadores a domicilio): 7 Salud.
- Género (atención en cada zona, hogares y patrocinio): 8 Seguridad. Su partida propia: 3 Presupuesto y tasas.
- Multas de tránsito: 8 Seguridad, como seguridad vial.
- Empleados del Municipio (atención los siete días y teléfono propio): 11 Habilitaciones e inspecciones.
- Recolección de residuos, ruido y ambiente: 9 Costa y espacio público.
- Excepciones urbanísticas: 6 Vivienda, porque el 15% de la valorización va a vivienda.
- Fondo Educativo, pedidos de informes y gasto por zona: 12 Transparencia.
- El hito de los cien días y el fin del mandato: 1 Mecanismo vecinal y obra pública.

**Fuente.** El campo «fuente» lleva el apartado del programa: «6.4», «5.5», «4.11». Para el anexo usa «anexo.N» (N es el número de la ordenanza) o «anexo» para las reglas generales. «nota de método» es la lista de lo que tiene que confirmar un abogado.

**Metas sin fecha.** Las veinte metas del cuadro 41 están todas en el plan. Las que el calendario fecha van en su mes. Las demás van en el mes 48, porque son metas de los cuatro años.

**Riesgos.** Del 6.6 entran los riesgos que tienen una acción que los reduce. Cada una lo dice en su nota («Riesgo del 6.6: …»). Los riesgos sin acción propia (la recaudación, la coparticipación, la tasa del bono, la reforma de la Ley Orgánica) no generan acciones.

## 3. Supuestos de duración

Toda duración que el programa no da es un supuesto. Cada una dice «Duración estimada» en su nota. Las que el programa sí da dicen «Duración del programa». Para el tratamiento de cada ordenanza se usaron 22 días hábiles: es lo que tardó la única reforma de las reglas de urbanismo que pasó por el Concejo (Ordenanza 9432, citada en el 5.5).

### 3.1 Duraciones que da el programa (25)

| Código | Acción | Días hábiles | Base |
|---|---|---|---|
| E06 | Primer grupo: un año de cursada | 262 | un año |
| E12 | Primer grupo: primera pasantía, seis meses en proyectos de las áreas del Municipio | 129 | seis meses |
| E15 | Primer grupo: segunda pasantía, seis meses en una empresa de San Isidro | 131 | seis meses |
| E20 | Segundo grupo: un año de cursada | 261 | un año |
| E21 | Segundo grupo: primera pasantía en el Municipio y segunda en empresas de San Isidro | 261 | dos pasantías de seis meses |
| E24 | Tercer grupo: entra en el mes 15, cursa un año y hace sus dos pasantías | 520 | dos años |
| E27 | Cuarto grupo: entra en el mes 21, cursa un año y hace sus dos pasantías | 521 | dos años |
| H03 | Compra de soportes y baterías: adjudicación y entrega | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| I07 | Prueba a ciegas de un mes de las caras del profesor digital, antes de pagar nada | 21 | un mes |
| I12 | Prueba del profesor digital, medida con exámenes hechos sin inteligencia artificial | 130 | seis meses |
| I17 | Licitar y contratar la auditoría externa de la inteligencia artificial del Municipio | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| K08 | Dictamen de la asociación del Parque del Águila sobre las obras en su parque | 22 | treinta días corridos, unos 22 días hábiles |
| K10 | Licitación propia de los dos primeros puestos náuticos: módulo de madera, bajada al río y bote | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| K14 | Licitación propia de los dos primeros baños con cloaca y sus plataformas para las clases | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| K18 | Licitación propia del primer tramo de prueba con arena | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| K32 | Licitación de la recolección: ofertas y evaluación | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| K36 | Licitar las cámaras que cuentan gente en los accesos de los 21 playones de la costa | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| M09 | El Ejecutivo responde por escrito a cada decisión de las zonas, con sus razones | 22 | treinta días corridos, unos 22 días hábiles |
| M14 | El Ejecutivo responde al panel en público, por escrito y con sus razones | 22 | treinta días corridos, unos 22 días hábiles |
| M15 | Año 2 de la rampa (25%): las asociaciones hacen ellas mismas la obra, por contrato directo | 259 | un año |
| M18 | Año 3 de la rampa (37,5%), con el registro de asociaciones vecinales ya renovado | 260 | un año |
| M20 | Año 4 de la rampa: los vecinos deciden la mitad de la obra pública | 260 | un año |
| P05 | Aviso de la convocatoria a la asamblea, con los ocho días que pide la Ley Orgánica (artículo 98) | 6 | ocho días corridos, unos seis días hábiles |
| S05 | Licitar los dos tomógrafos, o tomarlos con el leasing de la Provincia, mientras sigue el contrato actual | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |
| U03 | Licitación pública de los equipos de sonido propios | 66 | cada licitación se adjudica tres meses después del llamado (nota del cuadro 42) |

### 3.2 Duraciones estimadas (135)

| Código | Acción | Días hábiles | Base |
|---|---|---|---|
| C02 | Tratamiento de la derogación en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C05 | Tratamiento de la Ordenanza 1 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C09 | Tratamiento de la Ordenanza 5 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C12 | Tratamiento de la Ordenanza 7 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C15 | Tratamiento de la Ordenanza 9 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C17 | Revisión legal de las ordenanzas 15 y 16 | 10 | estimación propia |
| C19 | Tratamiento de la Ordenanza 15 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C22 | Tratamiento de la Ordenanza 16 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C24 | Revisión legal de las nueve ordenanzas que faltan: la 2, la 4, la 6, la 8, la 10, la 11, la 12, la 13 y la 14 | 30 | estimación propia |
| C26 | Tratamiento de la Ordenanza 2 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C29 | Tratamiento de la Ordenanza 6 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C32 | Tratamiento de la Ordenanza 4 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C35 | Tratamiento de la Ordenanza 8 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C38 | Tratamiento de la Ordenanza 10 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C41 | Tratamiento de la Ordenanza 11 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C44 | Tratamiento de la Ordenanza 12 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C47 | Tratamiento de la Ordenanza 13 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C50 | Tratamiento de la Ordenanza 14 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C52 | Redactar la ordenanza de foodtrucks y el cambio del artículo 9 de la Ordenanza 5824 | 15 | estimación propia |
| C54 | Tratamiento de la ordenanza de foodtrucks en el Concejo | 22 | precedente de la Ordenanza 9432 |
| C57 | Tratamiento del cambio de la Ordenanza 5824 en el Concejo | 22 | precedente de la Ordenanza 9432 |
| E01 | Firmar el convenio con la UNSO para la tecnicatura | 20 | estimación propia |
| E02 | Pedir al Ministerio de Educación que el título valga en todo el país | 5 | estimación propia |
| E03 | Pedir a la Provincia que permita la pasantía dentro de la formación profesional | 5 | estimación propia |
| E04 | Abrir la inscripción a la formación laboral en las seis zonas (compromiso 12) | 10 | estimación propia |
| E07 | Firmar el convenio de pasantías con la UNSO (Ley 26.427) | 20 | estimación propia |
| E08 | Trámite de validez nacional del título en el Ministerio de Educación | 120 | estimación propia |
| E10 | Preparar los lugares de pasantía en las áreas: equipos de diez pasantes con un supervisor | 40 | estimación propia |
| E13 | Firmar el convenio marco con la Cámara del Comercio e Industria de San Isidro y con las cámaras de Boulogne y Béccar | 30 | estimación propia |
| E30 | Empiezan a funcionar las cinco sedes fijas de formación laboral y la sede móvil de Acassuso | 60 | estimación propia |
| E33 | Las ofertas de trabajo se pueden consultar en la inteligencia artificial del Municipio | 20 | estimación propia |
| E35 | Elegir con el índice de necesidad el lugar del primer centro de apoyo escolar y contratar a sus docentes | 30 | estimación propia |
| E37 | Preparar el segundo centro de apoyo escolar | 30 | estimación propia |
| E39 | Abrir el tercer y el cuarto centro de apoyo escolar | 60 | estimación propia |
| E41 | Preparar el quinto y el sexto centro de apoyo escolar | 40 | estimación propia |
| G01 | Cargar los datos de seguridad que ya produce el Municipio: patrullaje, cámaras que funcionan y tiempo del 911 municipal | 20 | estimación propia |
| G03 | Pedir formalmente a la Provincia los datos de delitos por zona | 5 | estimación propia |
| G04 | Poner las 110 cámaras con inteligencia artificial a detectar hechos violentos y avisar al patrullero más cercano | 20 | estimación propia |
| G06 | Armar el mapa de los hechos que registra el Municipio | 30 | estimación propia |
| G08 | Preparar la constancia para quien es acusado en público sin una causa judicial | 20 | estimación propia |
| G10 | Los datos de seguridad pasan a estar al día, con las órdenes de juez recibidas y cumplidas | 40 | estimación propia |
| G11 | Preparar la oficina de delitos por internet, junto al equipo técnico de las cámaras | 30 | estimación propia |
| G14 | Firmar el decreto de cuotas sin trámites para el pago voluntario de las multas, según el ingreso (compromiso 17) | 15 | estimación propia |
| G15 | Pedir a la Provincia seis cambios en las multas, y a la Legislatura la licencia por puntos (compromiso 18) | 10 | estimación propia |
| G16 | Inscripción en línea para pagar en cuotas y plan sin interés para la deuda vieja (lo destraba la Ordenanza 15) | 20 | estimación propia |
| G17 | Inscribir la base de datos de las cuotas ante la autoridad de datos personales (lo destraba la Ordenanza 16) | 10 | estimación propia |
| G18 | La inteligencia artificial propone dónde poner cámaras de multas, sólo donde se supera un mínimo publicado de choques | 30 | estimación propia |
| G19 | Cada comisión de zona elige entre una cámara o un reductor de velocidad | 30 | estimación propia |
| G20 | La Provincia autoriza cada cámara (Disposiciones 14/2020 y 43/2021) | 40 | estimación propia |
| G22 | Revisar cada cámara de multas una vez por año, con sus datos a la vista | 10 | estimación propia |
| G24 | Organizar los días fijos de la dirección de género en lugares que ya existen en cada zona | 20 | estimación propia |
| G26 | Pedir lugar en la red provincial de hogares y firmar los convenios de patrocinio jurídico gratuito (lo destraba la Ordenanza 6) | 30 | estimación propia |
| H01 | Firmar el decreto que ordena grabar cada inspección con el teléfono del agente (compromiso 16) | 10 | estimación propia |
| H02 | Llamar a la compra de los soportes de pecho y las baterías | 5 | estimación propia |
| H04 | Convenio con el banco que paga los sueldos: teléfonos aptos en 24 cuotas sin interés | 20 | estimación propia |
| H05 | Acordar con los trabajadores municipales la compensación por usar el teléfono propio (Ley 14.656, artículo 75) | 40 | estimación propia |
| H06 | Construir la grabación sellada del turno: huella al grabar, corte por inspección y base por comercio o domicilio | 60 | estimación propia |
| H10 | Organizar la atención del sábado con el personal que elige ese horario | 20 | estimación propia |
| H12 | Habilitaciones en la inteligencia artificial: consulta previa con la cámara del teléfono, inspección con fecha fija y aviso de inspecciones fuera de lo normal | 60 | estimación propia |
| I01 | Armar el equipo que construye la inteligencia artificial del Municipio, con gente de San Isidro | 20 | estimación propia |
| I02 | Construir las tres primeras partes: la que responde consultas, la que saca el turno médico conversando y la que escucha a los vecinos | 35 | estimación propia |
| I03 | Revisión de seguridad por las universidades de San Isidro antes de abrir al público | 5 | estimación propia |
| I05 | Pedir gratis a la Nación el certificado de firma digital para programas | 5 | estimación propia |
| I06 | Recibir de la Nación el certificado de firma digital | 30 | estimación propia |
| I08 | Contratar la cara del profesor digital aparte del resto: por minuto, con la calidad mínima de la prueba y con un plan B | 10 | estimación propia |
| I09 | Construir las tres partes siguientes: la partida vecinal, el seguimiento de cada obra y el espacio de cada asociación | 60 | estimación propia |
| I15 | Transmitir y pasar a texto las asambleas, para buscarlas y consultarlas | 60 | estimación propia |
| I18 | Centros con computadoras y mesa de ayuda en cada zona, para quien no tiene teléfono o conexión | 40 | estimación propia |
| K01 | Pedir a AySA que diga si se pueden conectar a la cloaca los baños de los seis lugares de la costa | 5 | estimación propia |
| K02 | AySA confirma qué baños se pueden hacer | 60 | estimación propia |
| K03 | Reconocer las primeras asociaciones de parque: Parque del Águila y Bosque Alegre | 15 | estimación propia |
| K04 | Diagnóstico del desagüe de la calle Perú: marcador de ADN humano y unos veinte sensores caño arriba | 60 | estimación propia |
| K05 | Empezar las muestras de agua en cada tramo, dos veces por semana, y la bandera sanitaria de cada día | 20 | estimación propia |
| K06 | Proyecto de los puestos náuticos, los baños y el tramo de arena, con su costo y sus planos | 30 | estimación propia |
| K07 | Estudio de impacto ambiental de las obras de la costa del año 1 | 40 | estimación propia |
| K09 | Concurso abierto de profesores de la Escuela Náutica, con prueba técnica y de rescate | 40 | estimación propia |
| K12 | Armar los dos primeros puestos náuticos | 20 | estimación propia |
| K16 | Construir los dos primeros baños y sus plataformas | 25 | estimación propia |
| K20 | Construir el tramo de prueba: 100 por 20 metros, sobre base de piedra | 25 | estimación propia |
| K21 | Contratar los guardavidas del tramo: uno cada 80 metros, mínimo dos, y un bote | 20 | estimación propia |
| K23 | Año 2: abren el tercer y el cuarto puesto náutico y dos baños más | 120 | estimación propia |
| K24 | Año 3: abren los dos últimos puestos náuticos y los dos últimos baños | 120 | estimación propia |
| K25 | Foodtrucks al borde de cada puesto, con canon y 75% de empleo local (lo destraba la ordenanza de foodtrucks) | 20 | estimación propia |
| K26 | Centro de foodtrucks y actividades en el Bosque Alegre (lo destraba el cambio de la Ordenanza 5824) | 20 | estimación propia |
| K27 | Preparar las clases gratis del Municipio en las plazas donde ya dan clase los instructores registrados | 20 | estimación propia |
| K29 | Pedir a la Provincia la ley que protege la ribera y los parques principales | 10 | estimación propia |
| K30 | Congelar y revisar la lista de trabajadores de la recolección al llamar a licitación | 20 | estimación propia |
| K34 | Pedir por convenio a Trenes Argentinos dónde está cada tren del Mitre y del Tren de la Costa | 30 | estimación propia |
| K37 | Instalar una cámara que cuenta gente en cada acceso de los 21 playones | 20 | estimación propia |
| K38 | Las estaciones móviles miden el ruido de motos y colectivos donde marca el mapa del ruido (meta 18) | 20 | estimación propia |
| M02 | Convocar a la primera ronda de asambleas en las seis zonas | 10 | estimación propia |
| M03 | Primera ronda de asambleas en las seis zonas: informar y anotar qué necesita cada zona (compromiso 11) | 15 | estimación propia |
| M04 | Reconocer como comisión de su zona a cada asociación vecinal en condiciones | 20 | estimación propia |
| M05 | Volver a armar el registro de asociaciones vecinales, consultable por cualquiera | 20 | estimación propia |
| M06 | En las zonas sin una asociación en condiciones: asamblea abierta y ayuda para formar una | 90 | estimación propia |
| M08 | Segunda ronda de asambleas: los vecinos eligen las obras de su zona | 40 | dos meses, como el ciclo de la Ciudad de Buenos Aires que cita el 6 |
| M10 | Contratar y hacer las obras elegidas del año 1: el 12,5% de la obra pública, unos 7.227 millones | 70 | estimación propia |
| M12 | Sortear el primer panel de vecinos, apenas se aprueba la Ordenanza 12 | 15 | estimación propia |
| M13 | El primer panel se reúne y da su recomendación, con razones, sobre la obra en la costa | 20 | cuatro reuniones, una por semana |
| M16 | Revisión del Tribunal de Cuentas sobre la obra que hicieron las asociaciones | 60 | estimación propia |
| P01 | Convocar al Concejo a sesión extraordinaria (Ley Orgánica, artículo 68, inciso 5) | 1 | estimación propia |
| P02 | Tratamiento de la ordenanza preparatoria de la tabla, primera en la convocatoria | 3 | estimación propia |
| P04 | Ajustar la lista de mayores contribuyentes al Concejo nuevo, como pide el Tribunal de Cuentas | 5 | estimación propia |
| P07 | Publicar la tabla nueva en el Boletín Oficial y emitir las boletas | 2 | estimación propia |
| P09 | Reservar la partida de obra vecinal del primer año, unos 7.227 millones, con recursos afectados (Ley Orgánica, artículo 119) | 10 | estimación propia |
| P10 | Adelantar unos 335 millones para empezar por la costa, de lo que ceden otros programas | 10 | estimación propia |
| P14 | Tratamiento del presupuesto 2029 en el Concejo | 30 | estimación propia |
| P18 | Tratamiento del presupuesto 2030 en el Concejo | 30 | estimación propia |
| P22 | Tratamiento del presupuesto 2031 en el Concejo | 30 | estimación propia |
| P29 | Abrir el programa propio de género en el presupuesto, separado del que comparte con niñez, juventud y personas mayores | 10 | estimación propia |
| S01 | Turno médico por internet en los primeros hospitales y centros de salud, en la plataforma que ya da turnos para otros trámites (compromiso 7) | 30 | estimación propia |
| S02 | Pedir sumarse a Mi Salud Digital, el sistema de la Provincia | 5 | estimación propia |
| S03 | Publicar el precio por unidad de cada compra de insumos de los tres hospitales, con sus comparaciones (compromiso 8) | 30 | estimación propia |
| S04 | Estudiar el contrato actual de la tomografía y cómo termina | 30 | estimación propia |
| S06 | Hacer las obras en las salas de los tomógrafos del Central y de Boulogne | 60 | estimación propia |
| S07 | Instalar los dos tomógrafos | 20 | estimación propia |
| S09 | Extender el turno por internet a los trece centros de salud, con recordatorio y lista de espera | 120 | estimación propia |
| S11 | En la inteligencia artificial del Municipio: turnos, gente en las guardias, insumos que hay y faltan, y comparación de cada compra (meta 8) | 60 | estimación propia |
| S12 | Contratar a cien cuidadores a domicilio, formados en el curso de operador de cuidados del CFL 404 | 40 | estimación propia |
| T02 | Revisión legal de las cinco ordenanzas del anexo que entran en diciembre: la 1, la 3, la 5, la 7 y la 9 | 20 | estimación propia |
| T03 | Redactar el proyecto que deroga los artículos 8, 9 y 10 de la Ordenanza 6045 | 5 | estimación propia |
| T04 | Explicar el mecanismo a los bloques del Concejo, también a los concejales que asumen en diciembre | 30 | estimación propia |
| T05 | Dictamen del abogado sobre las propuestas que lo necesitan antes de aplicarse | 20 | estimación propia |
| T06 | Preparar la convocatoria a la sesión extraordinaria de diciembre, con la ordenanza preparatoria de la tabla en primer lugar | 3 | estimación propia |
| U01 | Preparar el decreto de prueba de los espectáculos al aire libre de lunes a jueves | 15 | estimación propia |
| U04 | Armar los tres grupos de producción y el control de los equipos | 20 | estimación propia |
| U05 | Los vecinos proponen en la inteligencia artificial a qué artistas nuevos de San Isidro quieren ver | 20 | estimación propia |
| U06 | Convenio con cuatro clubes o centros culturales para los shows bajo techo | 30 | estimación propia |
| U08 | Sumar al cuadro de usos la categoría de la Ley 15.302: hasta 300 personas y 500 metros cuadrados (lo destraba la Ordenanza 7) | 20 | estimación propia |
| V01 | Medir la conexión a internet en cada zona durante la primera ronda de asambleas, primero en La Cava y en Boulogne | 15 | estimación propia |
| V02 | Pagar la conexión de cada casa al agua, la cloaca y el gas, donde la obra vecinal hizo la red | 760 | unos tres años |
| V05 | Pedir a la Provincia la aprobación para cobrar el 15% de la valorización que genera cada excepción (Ley 14.449) | 10 | estimación propia |
| X01 | Registrar cada pedido de informes del Concejo y su respuesta, el día en que entra y el día en que sale | 15 | estimación propia |
| X04 | Cargar en qué se gastó el Fondo Educativo, obra por obra | 30 | estimación propia |
| X06 | Anotar cada gasto del Municipio con la zona donde se hace | 260 | estimación propia |

### 3.3 Fechas estimadas y otros supuestos (25)

Acciones cuya fecha o cuyo orden no sale del texto. El motivo está en la nota de cada una.

| Código | Acción | Fecha en el plan |
|---|---|---|
| C01 | Entra al Concejo el proyecto que deroga los artículos 8 a 10 de la Ordenanza 6045 (compromiso 1) | 15/12/2027 |
| C02 | Tratamiento de la derogación en el Concejo | 01/03/2028 |
| C05 | Tratamiento de la Ordenanza 1 en el Concejo | 01/03/2028 |
| C09 | Tratamiento de la Ordenanza 5 en el Concejo | 01/03/2028 |
| C12 | Tratamiento de la Ordenanza 7 en el Concejo | 01/03/2028 |
| C15 | Tratamiento de la Ordenanza 9 en el Concejo | 01/03/2028 |
| C59 | Cambia la mitad del Concejo | 10/12/2027 |
| C60 | Cambia la otra mitad del Concejo | 10/12/2029 |
| E38 | Abre el segundo centro de apoyo escolar | 23/03/2028 |
| E41 | Preparar el quinto y el sexto centro de apoyo escolar | 10/10/2029 |
| G21 | Desde el presupuesto del año 2, el dinero de las multas va a un fondo de seguridad vial | 02/01/2029 |
| G22 | Revisar cada cámara de multas una vez por año, con sus datos a la vista | 12/09/2029 |
| H09 | Rige la Ordenanza 4: sin grabación sellada y subida, no valen el acta, la clausura ni la habilitación | 10/08/2028 |
| I14 | El profesor digital llega a todos los chicos de primaria y secundaria, desde el año escolar siguiente | 01/03/2029 |
| P13 | El Ejecutivo presenta al Concejo el presupuesto 2029 y la ordenanza fiscal e impositiva 2029 | 02/10/2028 |
| P15 | El Concejo vota el presupuesto 2029 | 13/11/2028 |
| P16 | La Asamblea de Concejales y Mayores Contribuyentes aprueba la ordenanza impositiva 2029 | 13/11/2028 |
| P17 | El Ejecutivo presenta al Concejo el presupuesto 2030 y la ordenanza fiscal e impositiva 2030 | 01/10/2029 |
| P19 | El Concejo vota el presupuesto 2030 | 07/12/2029 |
| P20 | La Asamblea de Concejales y Mayores Contribuyentes aprueba la ordenanza impositiva 2030 | 12/11/2029 |
| P21 | El Ejecutivo presenta al Concejo el presupuesto 2031 y la ordenanza fiscal e impositiva 2031 | 01/10/2030 |
| P23 | El Concejo vota el presupuesto 2031 | 09/12/2030 |
| P24 | La Asamblea de Concejales y Mayores Contribuyentes aprueba la ordenanza impositiva 2031 | 12/11/2030 |
| T01 | Elección general de intendente y concejales | 24/10/2027 |
| U06 | Convenio con cuatro clubes o centros culturales para los shows bajo techo | 10/12/2027 |

## 4. Camino crítico

Las acciones críticas no se pueden atrasar ni un día hábil sin romper una fecha del programa.

| Código | Acción | Inicio | Fin |
|---|---|---|---|
| T01 | Elección general de intendente y concejales | 24/10/2027 | 24/10/2027 |
| T07 | Asume el intendente | 10/12/2027 | 10/12/2027 |
| I07 | Prueba a ciegas de un mes de las caras del profesor digital, antes de pagar nada | 10/02/2028 | 10/03/2028 |
| C18 | Entra la Ordenanza 15, de las cuotas de las multas de tránsito (compromiso 19) | 01/03/2028 | 01/03/2028 |
| C21 | Entra la Ordenanza 16, de la base de datos de las cuotas (compromiso 20) | 01/03/2028 | 01/03/2028 |
| M22 | Cien días: los veintiún compromisos, a la vista | 19/03/2028 | 19/03/2028 |
| M15 | Año 2 de la rampa (25%): las asociaciones hacen ellas mismas la obra, por contrato directo | 11/12/2028 | 07/12/2029 |
| M17 | Año 2 de la rampa, cumplido | 07/12/2029 | 07/12/2029 |
| M18 | Año 3 de la rampa (37,5%), con el registro de asociaciones vecinales ya renovado | 10/12/2029 | 09/12/2030 |
| M19 | Año 3 de la rampa, cumplido | 09/12/2030 | 09/12/2030 |
| M20 | Año 4 de la rampa: los vecinos deciden la mitad de la obra pública | 10/12/2030 | 09/12/2031 |
| M21 | Los vecinos deciden la mitad de la obra pública (meta 4) | 09/12/2031 | 09/12/2031 |
| V03 | En Boulogne y Béccar, los hogares sin cloaca se reducen a la mitad (meta 1) | 09/12/2031 | 09/12/2031 |
| M23 | Termina el mandato | 10/12/2031 | 10/12/2031 |

Cómo se lee:

- La columna vertebral es la rampa de la obra vecinal desde el año 2: M15, M17, M18, M19, M20 y M21, hasta el fin del mandato (M23). Cada año de la rampa dura lo que dice el programa, un año, y el siguiente empieza el día después. Si un año se atrasa, el 50% no llega al mes 48. Con la rampa también queda crítica la meta de las cloacas en Boulogne y Béccar (V03).
- Antes del año 2 no hay acciones críticas en la rampa. El año 1 (M11) tiene unos 20 días hábiles de margen antes del mes 13.
- La prueba a ciegas del profesor digital (I07) es crítica porque dura un mes y el calendario le da exactamente el mes 3.
- Las dos ordenanzas de las multas (C18 y C21) son críticas porque el programa las fija el 1 de marzo de 2028.
- La elección (T01), la asunción (T07), los cien días (M22) y el fin del mandato (M23) son fechas fijas.

Casi críticas (holgura de 1 a 5 días hábiles). Casi todas caen en los primeros cien días:

| Código | Acción | Holgura | Inicio |
|---|---|---|---|
| P01 | Convocar al Concejo a sesión extraordinaria (Ley Orgánica, artículo 68, inciso 5) | 1 | 10/12/2027 |
| C01 | Entra al Concejo el proyecto que deroga los artículos 8 a 10 de la Ordenanza 6045 (compromiso 1) | 1 | 15/12/2027 |
| C07 | Entra la Ordenanza 3, que actualiza la tabla de valores de 2008 (compromiso 3) | 1 | 15/12/2027 |
| P02 | Tratamiento de la ordenanza preparatoria de la tabla, primera en la convocatoria | 1 | 15/12/2027 |
| P03 | El Concejo vota la ordenanza preparatoria de la tabla | 1 | 20/12/2027 |
| P19 | El Concejo vota el presupuesto 2030 | 1 | 07/12/2029 |
| P23 | El Concejo vota el presupuesto 2031 | 1 | 09/12/2030 |
| P05 | Aviso de la convocatoria a la asamblea, con los ocho días que pide la Ley Orgánica (artículo 98) | 3 | 20/12/2027 |
| P06 | La Asamblea de Concejales y Mayores Contribuyentes aprueba la tabla nueva | 3 | 28/12/2027 |
| T04 | Explicar el mecanismo a los bloques del Concejo, también a los concejales que asumen en diciembre | 4 | 25/10/2027 |
| C59 | Cambia la mitad del Concejo | 4 | 10/12/2027 |
| P04 | Ajustar la lista de mayores contribuyentes al Concejo nuevo, como pide el Tribunal de Cuentas | 4 | 10/12/2027 |
| I01 | Armar el equipo que construye la inteligencia artificial del Municipio, con gente de San Isidro | 4 | 10/12/2027 |
| I02 | Construir las tres primeras partes: la que responde consultas, la que saca el turno médico conversando y la que escucha a los vecinos | 4 | 07/01/2028 |
| I03 | Revisión de seguridad por las universidades de San Isidro antes de abrir al público | 4 | 25/02/2028 |
| I04 | Empiezan a funcionar las tres primeras partes de la inteligencia artificial del Municipio (compromiso 14) | 4 | 03/03/2028 |
| G02 | Cualquier vecino puede preguntar por el patrullaje, las cámaras y el 911 municipal (compromiso 9) | 4 | 03/03/2028 |
| U02 | Empieza la prueba por decreto y abre el registro gratis de instructores y artistas (compromiso 21) | 4 | 03/03/2028 |
| H07 | El comerciante ya puede denunciar coimas, presiones y amenazas ante la inteligencia artificial, con grabación sellada (compromiso 16) | 4 | 03/03/2028 |
| X02 | Cualquier vecino puede preguntar por cada pedido de informes del Concejo y su respuesta (compromiso 10) | 4 | 03/03/2028 |

- La sesión extraordinaria de diciembre tiene un día de margen: convocatoria, entrada de los proyectos y voto de la ordenanza preparatoria antes del 22 de diciembre. Si el aviso de la asamblea se cuenta en días hábiles y no corridos, el margen de la asamblea baja de tres días a uno.
- La inteligencia artificial del Municipio tiene cuatro días de margen para estar en el mes 3. De ella dependen, además del compromiso 14, otros cuatro compromisos de los cien días: G02, U02, H07 y X02.
- Los presupuestos 2030 y 2031 tienen un día de margen, porque se votan entre el cierre de un año de la rampa y el inicio del siguiente.

## 5. Huecos y contradicciones

No se resuelven acá: se listan para decidir. Entre paréntesis, dónde está cada cosa en el programa y qué acción del plan toca.

### 5.1 Dentro del capítulo 6

1. **El año de la rampa no es el año del presupuesto.** La Ordenanza 1 cuenta la partida por ejercicio, de enero a diciembre (artículo 1). El calendario da cada escalón por cumplido en los meses 12, 24, 36 y 48, que terminan el 9 de diciembre. A esa altura el ejercicio todavía no cerró. (Cuadro 42 y anexo, Ordenanza 1. Acciones M11, M17, M19 y M21.)
2. **La regla de la rampa choca con el calendario del presupuesto.** La partida sólo sube si el escalón anterior se ejecutó y justificó entero (Ordenanza 1, artículo 1). El presupuesto del año siguiente se vota antes de que cierre el año. El programa no dice cómo se comprueba el escalón a tiempo para votar el siguiente. (P15, P19 y P23.)
3. **La condición del Tribunal de Cuentas no tiene fecha.** Para que la rampa siga después del año 2, el Tribunal de Cuentas no tiene que hacer objeciones (6.2). El Tribunal revisa las cuentas después del cierre de cada año. El programa no dice cuándo se conoce ese resultado. (M16 y M17.)
4. **Dos «primeros» en la sesión de diciembre.** La derogación de los artículos 8 a 10 es «el primer proyecto en entrar al Concejo» (6.1 y 4.10). La ordenanza preparatoria de la tabla «va a ir primera en la convocatoria de diciembre» (6.6). Puede ser compatible, porque una cosa es el orden de entrada y otra el orden del día. El programa no lo aclara. El plan las pone el mismo día, con la derogación primero. (C01 y C07.)
5. **Primera asamblea: convocada o hecha.** El 6.1, la introducción y el cierre dicen que a los cien días cada vecino va a estar «convocado» a la primera asamblea. El cuadro 40 (compromiso 11) y el calendario dicen que la primera ronda se hace en el mes 3, que termina el 9 de marzo. Son dos compromisos distintos. El plan cumple los dos. (M02 y M03.)
6. **Compromisos 4 y 5: entrada o aprobación.** El cuadro 40 los pone entre lo que va «al Concejo Deliberante, en la sesión extraordinaria de diciembre». Pero los comprueba con «Ordenanza» y, en el 4, con el registro de las asociaciones de parque. Eso supone las ordenanzas aprobadas antes del 19 de marzo. El programa sólo fecha su entrada, y en enero y febrero no hay sesiones ordinarias. El plan estima su aprobación a fines de marzo. (C08 a C13 y K03.)
7. **Centros de apoyo escolar: «de a dos por año» y «los seis en el mes 25».** Con dos por año, el quinto y el sexto abren en el año 3. El mes 25 es el primer mes del año 3. Para cumplir las dos cosas tienen que abrir justo al empezar el año 3. El plan lo supone así. (Cuadro 42, mes 25. E39, E41 y E40.)
8. **Profesor digital: «los primeros centros».** La prueba de seis meses es «en los primeros centros de apoyo escolar», en plural (meses 7 a 12). El calendario sólo fecha el primer centro (mes 3). El plan supone que el segundo abre antes del mes 7. (E38 e I11.)
9. **Panel sorteado: «apenas» y «meses 7 a 12».** El calendario dice que el panel se sortea apenas el Concejo aprueba la Ordenanza 12, y lo pone en los meses 7 a 12. La Ordenanza 12 entra en los meses 4 a 6. Si se aprueba antes del mes 7 (el plan estima abril de 2028), «apenas» y la ventana no coinciden. El plan respeta la ventana. (C45 y M12.)
10. **La obra del año 1 tiene poco tiempo.** Las obras se eligen en la segunda ronda (meses 6 a 9), y el Ejecutivo responde en treinta días corridos. El año 1 se cumple en el mes 12. La nota del cuadro 42 dice que cada licitación se adjudica tres meses después del llamado. Una obra que se licita después de la segunda ronda se adjudica cerca del mes 12 y no se hace ese año. El programa no dice si el año 1 se cumple con la obra adjudicada o terminada. El plan le da 70 días hábiles a la obra, sin una licitación de tres meses. (M08 a M11.)
11. **El argumento de los cien días.** El 6.1 dice que si la primera asamblea se pasara a mitad de año, las obras llegarían tarde para el presupuesto de ese año. La ronda que elige las obras cae justamente a mitad de año (meses 6 a 9). Es el mismo problema del punto 10.
12. **El título de la tecnicatura.** El calendario (mes 15) da por hecho que el Ministerio de Educación ya reconoció el título. El 6.6 lo trata como riesgo, con una beca municipal si no llega. No es una contradicción. El calendario no menciona ese plan B. (E09 y E11.)

### 5.2 Entre el capítulo 6 y los capítulos 4 y 5

13. **Pasantes como personal técnico.** El calendario (mes 15) dice que el personal técnico de la oficina de delitos por internet sale primero de los pasantes. El 5.3 y la Ordenanza 10 (artículo 4) dicen que los pasantes trabajan sólo en proyectos nuevos, y nunca en tareas de la planta ni en vacantes. Una oficina que atiende casos todos los días se parece a una tarea de la planta. (G12.)
14. **La inteligencia artificial en el mes 3 y la regla de licitar.** El 4.11 y el cuadro 28 dicen que cada contrato se licita antes de comprometer el dinero. La nota del cuadro 42 dice que una licitación tarda tres meses. Desde el 10 de diciembre, ninguna licitación se adjudica antes de mediados de marzo, después del mes 3. El programa no dice con qué infraestructura y con qué licencias funcionan las tres primeras partes. (I01 a I04.)
15. **Denuncias de coimas desde los cien días.** El canal manda cada denuncia a la auditoría externa (5.9 y Ordenanza 4, artículo 6). La auditoría externa se contrata (cuadro 28), y por la regla del punto anterior no estaría lista en el mes 3. Además, la grabación sellada necesita el certificado de firma digital de la Nación, que se pide en los meses 1 a 3 sin un plazo de respuesta. (H07, I06 e I17.)
16. **La Ordenanza 4 y el mes 9.** La Ordenanza 4 entra en los meses 4 a 6. Anula el acta, la clausura y la habilitación que salgan de una inspección sin grabación sellada. Las grabaciones empiezan en el mes 9. El programa no dice desde cuándo rige esa consecuencia. Si rigiera al aprobarse, toda inspección entre la aprobación y el mes 9 sería nula. El plan supone que rige desde el mes 9. (C33, H08 y H09.)
17. **Recolección y empleo local.** El 5.3 cuenta el contrato de recolección entre los que subcontratan el 20% a pymes de San Isidro y el 5% a empresas nuevas, con prioridad para el semillero. Esas reglas están en la Ordenanza 10, que entra en los meses 4 a 6. El pliego de la recolección es la Ordenanza 9, que se aprueba antes del llamado del mes 6, y su texto no las incluye. Además, las empresas del semillero existen recién desde el mes 27, y la recolección se adjudica en el mes 9. (C16, C39, K31 y K33.)
18. **Dos ordenanzas sin texto en el anexo.** El calendario (meses 4 a 6) presenta la ordenanza de foodtrucks y el cambio del artículo 9 de la Ordenanza 5824. El anexo dice que las promesas del programa necesitan normas «y acá están escritas», pero estas dos no están. (C52 a C58.)
19. **Espectáculos todas las semanas.** La meta 17 pide espectáculos al aire libre todas las semanas, de lunes a jueves. El 5.5 pone los 114 shows al aire libre que paga el Municipio entre el 20 de septiembre y el 15 de abril. El programa no dice si entre abril y septiembre las semanas se cubren sólo con artistas a la gorra. Los primeros shows pagos (meses 4 a 6) caen justo sobre el final de esa temporada. (U07 y U10.)
20. **Sonido para la prueba de los espectáculos.** La prueba por decreto (meses 1 a 3) promete que un equipo de producción del Municipio lleva y arma el sonido (5.5). Los equipos se compran por licitación pública, y los tres grupos de producción son personal nuevo. Con la regla de tres meses, no llegan a la prueba. El programa no dice qué sonido se usa mientras tanto. (U02, U03 y U04.)
21. **Tramo de arena en el año 1.** El calendario lo pone en el año 1 (mes 12). Antes necesita estudio de impacto ambiental (Ordenanza 12), la recomendación del panel (meses 7 a 12) y una licitación propia de tres meses. En el plan entra con unos 40 días hábiles de margen, pero el programa no ordena esos pasos. Tampoco dice si «el primer verano» del 5.5 es el de 2028 a 2029. (K07, K18 a K22.)
22. **Escuela Náutica y Ordenanza 11.** Las clases en el agua usan el límite de 630 E. coli de la Ordenanza 11, que entra en los meses 4 a 6. El calendario abre los primeros puestos en los meses 7 a 12 sin atarlos a esa aprobación. El tramo de arena con baño habilitado sí la necesita, porque la Ordenanza 11 deroga la prohibición de bañarse de 1978. (K13, K22 y C42.)
23. **Semillero: dieciséis o cuarenta.** El 5.3 dice que, con el programa completo, nacen diez empresas por convocatoria, y que en el mandato son dieciséis. El calendario y el 5.3 dan cuatro convocatorias dentro del mandato (meses 27, 33, 39 y 45). Diez por cuatro son cuarenta. El programa no explica la diferencia. (E17, E23, E26 y E29.)

### 5.3 Lo que el programa no fecha

24. **La elección.** No está en el programa. El plan usa el 24 de octubre de 2027 como fecha estimada (ver la sección 2). (T01.)
25. **El presupuesto de cada año.** El programa dice que el Concejo vota el presupuesto cada año, pero no da fechas para presentarlo ni para votarlo. Tampoco las da para la ordenanza fiscal e impositiva. No dice quién vota el presupuesto 2028 ni la impositiva 2028, ni si la asamblea de diciembre de 2027 trata la impositiva junto con la tabla. Tampoco dice cómo entra en 2028 la partida del año 1. El plan usa el artículo 119 de la Ley Orgánica, como dice el 4.9. (P09 y P13 a P24.)
26. **La aprobación de cada ordenanza.** Sólo la tabla tiene fecha de aprobación (diciembre). Las demás tienen fecha de entrada. El plan estima 22 días hábiles de tratamiento para cada una.
27. **Los plazos de otros.** No tienen plazo en el programa: la respuesta de AySA sobre los baños, el certificado de firma digital de la Nación, la validez nacional del título, la autorización de la Provincia para cada cámara de multas, los datos de delitos por zona, los lugares en la red provincial de hogares y la revisión del Tribunal de Cuentas. (K02, I06, E08, G20, G03, G26 y M16.)
28. **Cosas sin fecha.** La patrulla municipal que graba (segunda etapa). La transmisión y el paso a texto de las asambleas (meta 6). El registro público de órdenes de juez. El fin del cobro por multa, que llega cuando vence cada contrato actual. La partida propia de género en el presupuesto. El pago de la conexión de cada casa. Ordenar la información publicada del cuadro 37 (5.10). El plan ubica las que tienen una acción después de lo que las destraba, con fecha estimada. La patrulla que graba y el cuadro 37 no tienen acción, porque no tienen fecha.
29. **Las asambleas de los años 2 a 4.** El calendario sólo fecha las dos rondas del año 1. El plan pone las asambleas de cada año dentro del bloque de ese año de la rampa. (M15, M18 y M20.)
30. **Los grupos 3 y 4 de la formación.** El calendario no fecha su entrada. El plan la deduce de dos datos del 5.3: la inscripción se abre cada seis meses y egresa un grupo cada seis meses. (E24 y E27.)

## 6. Validaciones hechas

- Sin ciclos: el orden de las dependencias se recorre de punta a punta.
- Cada código de «needs» existe.
- Ninguna acción empieza antes de lo que necesita (fin de la anterior para «FS», inicio para «SS», más los días de espera).
- Cada acción con mes en el calendario cae dentro de su mes: empieza el primer día del mes o después, y su último día de trabajo cae el último día del mes o antes.
- La holgura no es negativa en ninguna acción: todo entra en las fechas del programa con las duraciones supuestas.
- Los hitos tienen duración 0. Inicio, fin y duración cuadran en días hábiles.
- Hay trece líneas de trabajo con los nombres del pedido.
- Ninguna oración de los textos empieza con «Y» ni con «Que».
- Toda duración dice si es del programa o estimada.
- El pedido a la Provincia de la Ordenanza 14 (K29) cae dentro de los 180 días de su aprobación.

