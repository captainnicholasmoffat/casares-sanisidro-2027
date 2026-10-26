# Plan de despliegue (rollout plan) · pedido de Nick, 10 de octubre de 2026

## Lo que pidió Nick (05:03)
- Un plan de despliegue como los que usan las grandes industrias y los gerentes de proyectos de software para proyectos muy grandes.
- Tiene que mostrar qué desencadena qué, para que suceda qué, y todos los pasos.
- Objetivo: mostrar que estamos organizados y que lo tenemos pensado; que el día uno sabemos a quién pedirle qué y qué hacer.
- Ejemplo de Nick: una página HTML que hizo para otro proyecto (130 acciones, 11 líneas de trabajo, 67 en el camino crítico, 13 hitos). Vistas: línea de tiempo, «esta semana», por línea de trabajo y lista. Filtros: línea, responsable, «sólo camino crítico». Al tocar una acción se ve qué necesita antes y qué destraba. Cada acción tiene: código, tarea, línea, responsable, equipo, duración en días hábiles, inicio, fin, holgura, si es crítica, si es hito, la decisión que pide, los pasos, y de qué otras acciones depende (fin-inicio o inicio-inicio, con días de espera).
- Para el programa hace falta algo mucho más serio que el ejemplo.

## Propuesta del coordinador · APROBADA (Nick, 10 de octubre, 05:10, «si»)
- Se arma cuando el programa esté terminado, junto con la web, porque sale del texto final: los primeros cien días, el calendario por meses, las ordenanzas del anexo y cada propuesta de los capítulos 4 a 6.
- Arranca en la elección de 2027 (transición) y llega hasta el fin del mandato; los primeros 18 meses, en detalle.
- Una línea de trabajo por área: mecanismo vecinal y obra pública; Concejo y ordenanzas; presupuesto y tasas; inteligencia artificial del Municipio; empleo y formación; vivienda; salud; seguridad; costa y espacio público; cultura y espectáculos; habilitaciones e inspecciones; transparencia.
- Responsables por cargo (secretarías, Concejo, Provincia), sin nombres de personas.
- Página aparte, con un enlace desde la web.

## Página del plan · anticipo (11 de octubre, 21:45)
- Página propia dentro del sitio: /despliegue/ (plantilla web/despliegue.tpl.html, datos despliegue/acciones.json). Link «Plan de despliegue» en el menú de arriba y en el pie.
- Arriba: 293 acciones, 13 líneas de trabajo, 133 hitos, 14 en el camino crítico, 48 meses; la lista del camino crítico con fecha; cómo leer (días hábiles, meses del programa, fechas estimadas).
- Vistas: línea de tiempo (todo el mandato o los primeros 18 meses; cada línea se abre), los primeros cien días mes por mes, por línea de trabajo, lista ordenable. Filtros: línea, responsable, búsqueda, sólo camino crítico, sólo hitos.
- Ficha de cada acción: cuándo, mes del programa, responsable, equipo, duración, margen, decisión que pide, qué se hace, qué necesita antes, qué destraba, nota con supuestos, link al apartado del programa (abre el lector en ese apartado).
- Publicado sólo en https://anticipo.sanisidro2027.pages.dev/despliegue/ — el link principal no lo tiene hasta que Nick apruebe.
- Pendiente de Nick: los 30 huecos de REVISION.md (recomendado: corregir el programa antes de publicar el plan).

## Ajustes de Nick (12 de octubre, 02:00) · en el anticipo
- Línea de tiempo: botones «Todo el mandato», «Año 1» a «Año 4»; cada año muestra sólo sus acciones, grande y con desplazamiento al costado (reemplaza «Primeros 18 meses»).
- Ficha: botón «← Volver a [código]» (vuelve un paso por toque); el gesto de atrás del celular hace lo mismo.
- «Lo que no se puede atrasar ni un día»: recuadro con pestañas por período (Antes de asumir · 1, Año 1 · 5, Año 2 · 2, Año 3 · 2, Año 4 · 4); hito = punto, tramo = barra. Opción D, elegida por Nick.
- Retirada la propuesta de unir metas y riesgos a cada acción (sería interpretación, no texto del programa).

## Control contra el modelo fiscal (Excel del commit 917c9fe), 12 de octubre
- El Excel reparte cada monto anual en doce meses iguales: sirve para comparar montos por año y el año en que empieza cada cosa, no fechas exactas.
- Coinciden: rampa vecinal 12,5/25/37,5/50% (7.227 M el primer año); empleo y vivienda 7.730,9 M en 2031 y mitad del camino en 2029; ambiente 335 M adelantados y 1,5% en el mes 36; educación 2.064 M desde el mes 12; centros de apoyo escolar 2, 4 y 6; formación (entra en febrero–marzo de 2028, pasantías en 2029, egresos desde marzo de 2030); la tabla, 5.983 M.
- Falta en el plan: «contratación de desarrollos» con la partida de empleo desde el año 3 (Excel: desde enero de 2030, 1.421,9 M; texto 4.11 y 5.3).
- Agregada (Nick, 02:26, «si»): E42, hito del 1 de enero de 2030, necesita P19 (presupuesto 2030 votado), fuente 5.3. El plan pasa a 294 acciones. En el anticipo.
- Salud de la plataforma: el Excel la paga en 2028 y 2029 enteros (554,9 y 988,4 M). Coincide con el texto (4.11 y 3.4: «los dos primeros años»); el turno médico conversando se construye en enero–febrero de 2028 (I02). No es error.
- Fuente de verdad (respuesta a Nick, 02:25): el programa; dentro de él, el Excel manda en la plata y en el año de presupuesto (ejercicio, Ordenanza 1 art. 1), y el calendario (cuadro 42) en las fechas. En las dos diferencias reales, el que está bien es el Excel.
- Ya en la lista de huecos: el Excel cuenta por ejercicio (enero a diciembre) y el plan por año de mandato (10 de diciembre a 9 de diciembre) — huecos 1 y 2 de REVISION.md.
