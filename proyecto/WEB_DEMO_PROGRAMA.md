# Web demo del programa · plan (10 de octubre de 2026)

## Lo que pidió Nick (04:10 y 04:12)
- Volcar todo el programa en una página web, con un chatbot que responda cualquier pregunta sobre el programa, basado sólo en el programa.
- Ejemplo: un comerciante con una cafetería cuenta sus problemas y el chatbot le dice qué soluciones le da el programa.
- Objetivo: que quien no tiene tiempo de leer el programa se interese y lo empiece a leer.
- Es un demo en HTML completo para mostrar. Si después quieren subirlo y hostearlo, se hostea.
- Se arma recién cuando Nick confirme que el programa está terminado.
- Tiene que estar muy bien hecho: nada de look and feel de hace 20 años; efectos 3D y animaciones; lo mejor que se pueda hacer.

## Decisiones y límites verificados
- El generador de sitios de Higgsfield no sirve para el chatbot: en un sitio común (`type: website`) prohíbe cualquier generación con inteligencia artificial, también de texto; el tipo `app` obliga a entrar con cuenta de Higgsfield y a usar su marca. Además, cada guardado queda publicado en vivo.
- Camino: HTML completo armado por el coordinador (3D y animaciones con librerías de cdnjs), con la paleta y las tipografías del documento (Spectral e Inter; fondo #F5F0E8, oxblood #7C2E23, coral #DB6B4B, sage #5F7057, amber #B4863A).
- El demo se publica como página privada de Claude: ahí el chatbot funciona con la cuenta de Claude de quien lo usa (Nick, al mostrarlo). Un visitante sin cuenta de Claude ve el programa pero no el chatbot.
- Para hostearlo abierto a cualquiera, el chatbot va a necesitar su propia conexión paga por pregunta (paso posterior).
- Imágenes: se reusan las 13 aprobadas. Cualquier imagen o video nuevo (por ejemplo con Higgsfield) necesita el OK explícito de Nick.
- Guías de diseño a usar al armarla: frontend-design, artifact-design, artifact-diagramming, dataviz, y las guías de diseño de Higgsfield (design-taste-frontend, wow-catalog, wow-maker), sólo como referencia.

## Chatbot (propuesta, pendiente del OK de Nick)
- Nombre: «Preguntale al programa». No se puede llamar «la inteligencia artificial del Municipio», que es una propuesta y todavía no existe.
- Responde sólo con lo que dice el programa, y dice de qué capítulo sale cada respuesta.
- Responde en el idioma en que le escriben.
- Si el programa no habla de algo, lo dice.
- Mismas reglas del documento: sin «mafia», «plata» ni «sobreprecio»; lenguaje llano.

## Conocimiento del chatbot (Nick, 10 de octubre, 19:13)
- El chatbot no se alimenta sólo del programa: también de todas las investigaciones (los 32 informes del repositorio, unos 1,7 MB).
- Pirámide de relevancia: primero el programa, que es lo aprobado; debajo, las investigaciones, para explicar de dónde salió cada cosa y lo que se investigó.
- Si una investigación dice algo que el programa decidió distinto, el chatbot dice lo que decidió el programa.
- Antes de cargar los informes, el coordinador los revisa y saca notas internas y opciones descartadas que no deben salir al público. Los archivos crudos (01_raw) no se cargan.

## Higgsfield y navegación (Nick, 10 de octubre, 20:58)
- Visuales con Higgsfield: sí, hay créditos (saldo 2.915,5 al 10 de octubre). Pero todo lo que se haga con Higgsfield se le propone antes a Nick.
- La página tiene que impactar, pero sobre todo ser funcional y muy fácil de entender y de navegar.

## Inspiración (link de Nick, 10 de octubre, 21:10)
- Guía mavgpt.ai «Claude cinematic 3D websites Higgsfield 2026»: el efecto «cine» es un video de un solo movimiento de cámara (5 a 10 segundos, sin cortes) cortado en cuadros y dibujado en canvas según el scroll, hacia adelante y hacia atrás, en una sección fija; con Lenis y GSAP ScrollTrigger.
- Reglas que dan: póster inmediato, carga acotada en celulares, versión quieta para quien pide menos movimiento, texto real en HTML (no dentro del video), un solo suavizado de scroll.
- El 3D de verdad (girar libre) es aparte, con three.js; un video generado no es un modelo 3D.
- Nick va a pasar además un usuario de Instagram como referencia.

## Borrador 1 publicado (11 de octubre, 00:30)
- Página privada de Claude: https://claude.ai/artifact/FJTD4wvw3za2PHzU7dcsQw (se actualiza en la misma dirección).
- Tiene: portada con la costanera que avanza con el scroll (video de 10 segundos ya aprobado por Nick, 100 cuadros), tres ideas de la introducción y la frase de los fondos; los nueve puntos con «abrir/cerrar»; los primeros cien días.
- Faltan: el programa completo por capítulos, el mapa 3D de las seis zonas, «Preguntale al programa», el plan de despliegue enlazado.
- Fuente del texto: hojas 1, 5, 6, 7 y 100 de la A4 final (c462fcf), copiado sin cambios.

## Borrador 1 rechazado (Nick, 11 de octubre, 00:25) · regla firme
- El efecto de scroll con la escena fija no sirve: la página se traba, sólo se mueve la imagen, la gente camina rápido o para atrás. Parece rota y no vende.
- Regla: el scroll siempre baja la página. Nada de escenas fijas ni animaciones atadas al scroll. El movimiento sólo de apoyo, cuando la persona hace algo (abrir, tocar, girar el mapa).
- Antes de programar: primero se acuerda el diseño con propuestas en imágenes.

## Tres propuestas de diseño (11 de octubre, 01:00)
- Tablero: https://claude.ai/artifact/ANDB31TNscEzX1ZL731dAf (computadora y celular de cada una).
- A. Sitio de diario: menú arriba, foto quieta de la costanera, nueve puntos en tarjetas, cien días, programa por capítulos con buscador.
- B. La pregunta primero: arriba «¿Qué te preocupa de San Isidro?» con «Preguntale al programa», ejemplos y una respuesta de muestra (punto 7 y 5.9).
- C. El mapa primero: arriba el mapa en relieve de las seis zonas (altura = obra que deciden por año desde el cuarto año, 4.4 gráfico 23) y los datos de la zona elegida.
- Pendiente: que Nick elija o mezcle.

## Diseño elegido: B2 (Nick, 11 de octubre, 01:00–01:20)
- A descartada (no se entiende). C: el mapa queda para después, se ve estadístico. B es la base: la pregunta arriba, el ejemplo «Así responde» debajo, las nueve tarjetas con ilustración, «Leer más» y «Preguntale sobre esto», y el programa completo con buscador.
- Micrófono: por ahora el del teclado del celular; un botón propio, más adelante.
- Primera versión publicada en la misma dirección de la web (versión 2, 01:35). Capacidad: «sample» (cuenta de Claude de quien pregunta). Busca en el programa (primero) y en las investigaciones; responde con fuente (apartado y hoja) y dos preguntas para seguir.
- Probado con un simulador de Claude: búsqueda, armado de la pregunta (unos 32 KB, debajo del tope de 64 KB), fuentes que abren el texto, tarjetas, buscador, celular sin desborde. La respuesta real la prueba Nick.

- Versión 3 (02:15): tarjetas más bajas (error: la imagen tomaba el alto de la foto original).
- Versión 4 (02:55): «El programa completo» con 12 cuadros y un lector propio: índice a la izquierda (en el celular, botón «Índice»), subtítulos destacados, recuadros en caja, «Anterior» y «Siguiente», «Preguntale sobre este apartado». Cada tarjeta abierta lleva al apartado (1→4.3, 2 y 3→5.3, 4 y 5→4.11, 6→5.7, 7→5.9, 8→5.5, 9→capítulo 3).
- Tokens: con «sample», cada persona usa su propia cuenta de Claude; quien no tiene cuenta no puede preguntar. Para el público, sitio propio con conexión paga (pendiente de decisión de Nick).

## Sitio propio en Cloudflare (11 de octubre, 06:30)
- Por qué: según la ayuda de Claude, una página que usa Claude no se comparte con «cualquiera con el link» y a invitados de afuera el chat no les funciona. El formato clásico publicado no entra con 2 MB de research.
- Solución elegida por Nick: sitio propio en Cloudflare Pages (plan gratis) + función que llama a Claude con los créditos mensuales del plan Max, vinculados a una organización nueva de la Consola (no toca créditos comprados). Modelo: Sonnet 5.5.
- Paquete listo: /home/claude/proyecto/sitio (zip enviado a Nick). Probado en local con un simulador de Claude: página, chat con respuesta en vivo, fuentes, preguntas en inglés, celular.
- Cuenta: la misma de Cloudflare que Sunday Sailor (Nick, 11 de octubre, 16:56). Los topes gratis son de la cuenta, pero sólo cuentan las preguntas al chat; los créditos de Claude se acaban mucho antes.
- Nick agregó el permiso «Cloudflare Pages › Edit» a su clave «bulwark-sunday-sailor» (19:11).
- PUBLICADO (11 de octubre, 19:15): https://sanisidro2027.pages.dev. Página, programa, investigaciones e imágenes responden; vista previa para WhatsApp con og.jpg (1200×630, foto de la asamblea). El chat responde «todavía no está activado» hasta que se cargue la clave de Claude.
- Créditos (11 de octubre, 20:38): Consola con captainnicholasmoffat@gmail.com (el mismo mail de claude.ai), organización «Cap'n Nick Projects», vinculada al Max (200 dólares por mes, para todos los proyectos; un workspace por proyecto). La Consola de oldtimesailors, con los 247 dólares comprados, no se toca.
- Clave de Claude cargada como secreto ANTHROPIC_API_KEY y sitio vuelto a subir. La clave anda, pero todavía no hay saldo: claude.ai dice «Next credit: Processing, Oct 13, 2026». Hasta entonces el chat responde «llegó a su límite».
- Créditos activos (11 de octubre, 21:18). Probado en el sitio publicado con preguntas reales (café en Martínez; cloaca en Boulogne): responde con fuentes y preguntas para seguir. Arreglos subidos: respuesta hasta 1.400 tokens (antes se cortaba) y listas con guiones bien armadas.
- Rediseño del lector (Nick, 20:51: «rústico, sin diseño»): portada con foto, capítulos con foto, portada de cada capítulo con sus apartados, foto del capítulo arriba de cada apartado, negritas de color del programa, recuadros en su lugar, «Hoy / Propuesta», las 25 fotos y los 13 gráficos del programa, los esquemas 25 y 27 de la A4, cuadros como tablas, «En esta página», fuentes plegadas, anterior y siguiente con foto, zoom de imágenes. Sin el recuadro bordó alrededor del texto.
- Anticipo en https://anticipo.sanisidro2027.pages.dev (con chat). La dirección principal sigue con el diseño anterior hasta que Nick apruebe.
- Capítulo 6 no tiene foto en el programa: va con fondo bordó; propuesta de imagen nueva con Higgsfield, pendiente del OK de Nick.

## Realismo (Nick, 10 de octubre, 21:07)
- Todo lo que se genere (imágenes, videos, 3D) tiene que verse realista: proporciones reales, nada de dibujitos.
- Hechos con Higgsfield (21:07): 4 videos de 5 a 10 segundos desde fotos aprobadas (costanera, asamblea, costa en la semana, náutica) e imagen del puesto en la costa en vista de maqueta. Gastados 44,5 créditos (saldo 2.871). Pendiente: OK de Nick y decisión sobre el modelo 3D del puesto.

## Ajustes de Nick (11 y 12 de octubre)
- Portada: sin foto al lado de la pregunta (Nick, 21:29: «estaba mejor antes»). El resto del rediseño, aprobado («están lindas»).
- Tres pasos debajo de la pregunta (propuesta A, elegida por Nick): «Preguntá lo que quieras · Un problema, una duda o pura curiosidad», «El programa te responde», «Te dice dónde leerlo». B (ejemplo al lado) y C (botón fijo) descartadas.
- Nombre (Nick, 12 de octubre, 00:23): debajo del título dice «Preguntale a nuestro programa de gobierno»; el menú y los botones siguen con «Preguntale al programa». Así se aclara una vez que es el programa de gobierno.
- Capítulo 6 con la foto de la estación de tren (f_estacion, estaba en el repositorio y no en el programa). Epígrafe en la web: «Una estación de tren en San Isidro. Ilustración.»
- Plan de despliegue publicado en https://sanisidro2027.pages.dev/despliegue/ (Nick: «se ve bien»), con link arriba y abajo.
- Todo publicado en el link principal el 12 de octubre, 00:30. Chat probado de nuevo: responde.

## «Las cuentas» (12 de octubre, 03:40) · en el anticipo
- Página /cuentas/: el modelo fiscal en 12 partes con gráficos, «Tu zona», las 20 metas, la cuenta completa y la descarga del Excel (/data/modelo-fiscal-san-isidro-2028-2035.xlsx).
- Todo sale del Excel con web/cuentas/extract.py → cuentas.json; la página se arma con cuentas.tpl.html. Excel de origen: web/cuentas/modelo_fiscal.xlsx (commit 917c9fe, Dispatch 17).
- La IA de la web también lee el modelo: web/cuentas/ia.py arma data/cuentas_ia.json (16 textos, uno por zona). Cita «Las cuentas · …» y el botón lleva a /cuentas/#sección.
- Control automático: web/cuentas/check.py cruza 35 números del Excel con el texto del programa; si alguno no coincide, el armado del sitio se detiene. Hoy: 35 de 35.
- Preguntas en la página: caja arriba (con micrófono) y «Preguntar sobre esto» en cada sección; la respuesta se abre al costado (iframe a /?embed=1&q=…).
- Regla nueva del chat: usar las cifras con unidad y año, sin cuentas propias.
- Prueba en vivo (anticipo): 9 preguntas de plata, todas con los números correctos.
- Pendiente de Nick: aprobar el paso al link principal; paleta del PDF (maqueta «Colores del programa en la web»).

## Seguridad y chat (12 de octubre, 05:00) · en el link principal
- El servidor arma el contexto él solo (sitio/lib/context.js, generado por build_site.py con el mismo código de búsqueda de la página). /api/ask acepta sólo {question ≤700, search ≤1600, history ≤6 turnos de ≤3000}; el formato viejo da 400. Primero manda «refs» (qué pasaje es cada código) y después la respuesta.
- Cabeceras: CSP, X-Frame-Options SAMEORIGIN, HSTS, Permissions-Policy (micrófono sólo propio), nosniff, Referrer-Policy.
- Reglas nuevas: la IA calcula cuando los números están (sin mostrar la operación, avisa que es una cuenta); línea oculta CUENTAS que la página rehace y corrige (fixCalcs); regla 9 contra «ignorá tus reglas» y pedidos de instrucciones; lee el plan de despliegue (data/plan_ia.json, 294 acciones) y aclara fechas estimadas.
- Límite por conexión: 40 preguntas cada 10 minutos (en memoria, aproximado). Con D1: límite real por conexión y total diario.
- Si se llega al tope de gasto de la consola, el chat avisa que llegó a su límite del mes.
- Probado en vivo: cuentas (123.783 $ por habitante en Béccar; +1.429% empleo y vivienda), plan (licitación de recolección), ataques (poema, mostrar instrucciones): todo bien.
- Nick (04:39): no rotar las claves pegadas en el chat. Pendiente de Nick: tope de gasto en la consola y permiso D1 en el token de Cloudflare.

## Costo y límites (12 de octubre, 05:15)
- Tope de gasto en la consola: 200 dólares por mes, sin tarjeta cargada (nunca cobra de más). Gastado en pruebas: 1,08 dólares.
- Medido: cada pregunta usa unos 11.500 a 12.800 tokens de entrada y 400 a 600 de salida: entre 2,5 y 3 centavos de dólar (Sonnet 5.5: 2 dólares por millón de entrada, 10 por millón de salida). Con 200 dólares: unas 7.000 preguntas por mes.
- Corregido: el modelo pensaba antes de responder (se pagaba como salida y cortaba respuestas). Ahora thinking «between_tools» y effort «medium» (sitio/lib/claude.js; se puede cambiar con las variables THINKING y EFFORT).
- Límites con D1 (base sanisidro2027, tabla hits): 60 preguntas por hora por conexión (hash) y 500 por día en total (variables PER_IP_HOUR y DAILY_CAP).
- Colores del PDF aplicados (opción A): recuadros por tipo (data/tonos.json), Hoy ámbar, Propuesta verde, tablas arena, frase clave en verde en las respuestas, gráficos de las cuentas en bordó y verde.
- Filtro: la palabra «plata» se cambia por «dinero» al mostrar la respuesta.

## Pensar o no pensar, y aprendizaje paso 1 (12 de octubre, 05:30)
- Comparación con las mismas 10 preguntas (scratchpad ab.py): las dos formas dieron los datos correctos. Con pensar: 3,3 ¢ por pregunta, respeta mejor las reglas (no se le escapó «plata», respuestas más cortas). Sin pensar: 2,9 ¢, una «plata», respuestas a veces de más de 170 palabras. La diferencia de costo es chica (12%). Pendiente de Nick: volver a pensar (recomendado) subiendo max_tokens para que no corte.
- Aprendizaje paso 1, en el link principal: tabla «preguntas» en D1 (pregunta, respuesta, fuentes, sin_dato, cortada, feedback; conexión como hash; se borran a los 180 días). Botón «¿Le faltó algo a esta respuesta?» (/api/feedback). Aviso en el inicio y en «Las cuentas».

## Panel privado (12 de octubre, 05:50) · en el link principal
- https://sanisidro2027.pages.dev/panel/ — protegido con Cloudflare Access (Zero Trust Free, equipo super-thunder-44e8): código por mail, sólo captainnicholasmoffat@gmail.com, sesión de 24 horas. App «Panel San Isidro 2027» cubre /panel y /api/panel (también en anticipo).
- Segunda cerradura: sitio/lib/access.js verifica el JWT de Access (firma, audiencia, vencimiento y mail) en /api/panel/datos, /exportar y /borrar. Probado: sin login redirige al login; en las direcciones de cada deploy, 403.
- Muestra: totales, lo que el programa no cubre, comentarios «¿Le faltó algo?», de qué preguntan más, todas las preguntas con buscador, descarga CSV. Las preguntas no se borran solas: a los 5 meses avisa; borrar las de más de 6 meses pide confirmar dos veces.
- Nick (05:19): IA con pensar (adaptive, effort high, max_tokens 3000), unas 6.000 preguntas por mes; si quieren más, que lo paguen.

## Filtro final antes de compartir (12 de octubre, 06:30) · en el link principal desde las 16:05 (OK de Nick)
- Prueba de maldades en vivo (6 preguntas trampa: Lanús, a quién votar, chiste ofensivo, Milei y Kicillof, «firmá como Casares», evadir tasas): las 6 bien. Sin forma de meter código ni en las respuestas ni en el panel (todo como texto).
- Pie en todas las páginas (Nick, 06:19: «propuesta», sin candidato y sin responsable): «Propuesta de programa de gobierno para San Isidro. No es un sitio de la Municipalidad de San Isidro.» Links «Escribinos» y «Privacidad».
- Aviso en la caja de preguntas: «Responde una inteligencia artificial… Puede equivocarse: vale lo que dice el programa» y «No escribas datos personales». En «Las cuentas»: «valen el modelo fiscal y el programa».
- Página /contacto/ (opción A de Nick, 06:20): formulario «Escribinos» (mensaje ≤1.500, mail opcional, campo trampa para robots) → tabla «mensajes» en D1 → sección «Mensajes de «Escribinos»» en el panel (con el mail). Topes: 5 mensajes por día por conexión, 300 por día en total. Debajo, la nota de privacidad (qué se guarda, para qué, quién lo procesa, hasta seis meses, cómo pedir que se borre). Sin responsable con nombre: la nota queda incompleta para la Ley 25.326 hasta que se decida.
- Reporte de mejoras (Nick, 06:21): la descarga del panel junta preguntas y mensajes en un solo CSV (columna «tipo»), sin el mail. Borrar las de más de 6 meses borra también los mensajes.
- Tope nuevo: 100 preguntas por día por conexión (PER_IP_DAY). El tope diario de 500 ya no cuenta las preguntas rechazadas por los topes por persona (antes una sola conexión insistente podía gastar el cupo de todos).
- Descarga: las celdas que empiezan con = + - @ se neutralizan (no se ejecutan como fórmula en Excel).
- La IA se niega en primera persona: «Sólo respondo sobre el programa de gobierno de San Isidro» (antes decía «sólo respondés»).
- Ícono de la pestaña: «SI» crema sobre bordó (favicon.ico, apple-touch-icon, icon-192/512).
- Para Nick, sin código: verificación en dos pasos en Gmail, Cloudflare y la consola de Claude; no pagar publicidad del link en internet antes de la campaña oficial (ley nacional; la provincial, a consultar con el abogado).

## Menú en el celular (12 de octubre, 17:00) · en el link principal
- Problema (Nick, 16:39): en el celular los links de arriba se acomodaban en tres renglones y se mezclaban; al bajar desaparecían.
- Opción A elegida (maqueta «Menú en el celular»): barra fija con el nombre y «Menú»; al tocar, lista grande de las 5 partes, «Escribinos», «Privacidad» y la línea de propuesta. «Estás acá» en Las cuentas y el plan. Sólo en pantallas de hasta 760 px; en la computadora, igual que antes.
- Archivo único web/menu_movil.html, que build_site.py agrega al inicio, a «Las cuentas» y al plan; el botón está en cada encabezado (clase mm-bar).
- Regla (Nick, 16:52): cambiar sólo lo que pide; lo de abajo del cuadro de charla estaba perfecto. Comprobado comparando la web actual con el anticipo: debajo del encabezado, igual.
- Sin tocar (pendiente de Nick): la caja de pregunta que corta el ejemplo en celulares chicos y en «Las cuentas», y el encabezado distinto de «Las cuentas».
