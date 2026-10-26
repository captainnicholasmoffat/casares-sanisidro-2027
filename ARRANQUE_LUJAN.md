ARRANQUE · Inteligencia artificial del Municipio de Luján

A · Sólo para esta sesión (esto no se guarda en el repositorio de Luján)

Lo que ya existe, para leer antes de hacer nada:
1. El kit con todo lo aprendido en un programa municipal anterior (San Isidro): repositorio captainnicholasmoffat/casares-sanisidro-2027, rama kit-lujan. Agregalo a la sesión con add_repo (sólo lectura) y leé primero LEEME.md. Ahí están el código de la web con chat, el control de cifras, el plan de despliegue, los dispatches, las correcciones de Nick, sus reglas con fecha (memoria/ways-of-working.md) y el relevamiento de habilidades (proyecto/SKILLS_RELEVAMIENTO.md).
2. El programa anterior terminado, con su motor de PDF, A4 y Excel: mismo repositorio, rama claude/cool-hopper-3hdk58 (sólo leer).
3. El motor de la «web integrada»: captainnicholasmoffat/malafama-web, rama hq/panel (sólo leer). Empezá por docs/project-status.md.
4. Google Drive, unidad compartida «claude», carpeta «Proyecto San Isidro» (ID 1lfETtk5OzDOUdet-THmCldF36alzLkVl): fuentes y datos crudos. Buscá siempre con parentId.
Todo eso es consulta: el método y el código se reusan; los datos, los nombres y las propuestas de San Isidro no se copian a Luján. En los repositorios ajenos, nunca escribas ni borres nada.

B · Para guardar como CLAUDE.md en el repositorio de Luján

Quién y qué
- Coordina Nick (Cap'n Nick). El cliente es el intendente actual de Luján.
- El objetivo es la inteligencia artificial nativa del Municipio de Luján: diagnóstico, plan de gestión, modelo fiscal, ordenanzas, plan de despliegue y el sistema funcionando.
- El sistema tiene cuatro puertas: web, WhatsApp, app instalable en el celular y panel para empleados con roles.
- La base es el patrón de la «web integrada»: la inteligencia artificial lee y propone, las reglas deciden, una persona aprueba con un toque; una sola bandeja para web, WhatsApp, Instagram, Messenger y mail; registro que sólo se suma; revisión semanal de mejoras que Nick aprueba.

Paso 0
- Creá el repositorio privado captainnicholasmoffat/lujan-ia-municipal.
- Guardá esta parte B como CLAUDE.md.
- Commit y push seguido, en una rama de trabajo; main sólo recibe trabajo verificado. Nunca borres nada de Nick.

Paso 1 · Habilidades
Adoptá, desde su fuente oficial y con su licencia, estas habilidades:
- Modelo fiscal: xlsx, audit-xls (anthropics/financial-services) y model-qa-review (ya en la cuenta).
- Base de datos: supabase y supabase-postgres-best-practices (supabase/agent-skills).
- Trabajos programados: inngest-skills.
- Seguridad: owasp-security (agamm/claude-code-owasp) y security-guidance (anthropics/claude-plugins-official).
- Accesibilidad: accessibility (addyosmani/web-quality-skills, WCAG 2.2).
- Pruebas: webapp-testing.
- Chat: promptfoo evals o las evals de Inngest, una sola.
- WhatsApp: whatsapp-webhooks (hookdeck/webhook-skills).
- Datos: tabular-review (anthropics/claude-for-legal), duckdb-skills, pdf, explore-data y validate-data.
- Escritura y fuentes: house-copy-desk y trace-to-source (ya en la cuenta).
- Para crear las propias: skill-creator.
- Ya en malafama-web, mantener: ponytail, code-review, design-critique y ux-copy.
Mirá como molde whitegloveai/claude-skills-gov (68 habilidades para gobiernos locales de Texas) y adaptá lo que sirva.
Escribí con skill-creator, probadas, estas habilidades propias, en este orden:
1) castellano rioplatense llano con las reglas de abajo y un control automático;
2) fuentes públicas de un municipio bonaerense: presupuesto, ejecución, ordenanzas fiscal e impositiva, boletín oficial, censo por radio;
3) control del texto contra el modelo, con formato 1.234,5 y fuente por cifra;
4) ordenanzas con técnica legislativa bonaerense;
5) datos personales según la Ley 25.326;
6) panel «la inteligencia artificial propone, las reglas deciden, una persona aprueba», sobre la base de malafama-web.
Cuando estén, proponéselas a Nick para guardarlas.

Paso 2 · Diagnóstico (sin construir nada todavía)
- Lista de fuentes públicas de Luján: presupuesto, ejecución, ordenanzas, boletín, censo, deuda, coparticipación.
- Lista de datos internos para pedirle al Municipio: presupuesto detallado, reclamos, padrones de tasas, personal, expedientes, sistemas que usan.
- Entregale a Nick un informe corto. Esperá su OK antes de construir.
- Preguntale una sola vez: quién es el contacto en el Municipio para los datos y para cuándo lo necesitan.

Cómo hablarle a Nick
- Castellano rioplatense, corto, una línea por punto. No escribas de más.
- Cada opción, con «lo malo» y tu recomendación. Nunca decidas sin avisarle en una línea.
- Verificá con fuentes primarias; nunca supongas.
- Dispatches para otros chats: un solo bloque completo por chat, listo para copiar, sin adjuntos; preguntá antes de escribirlos.
- Cambiá sólo lo que pidió. Mostrá un anticipo antes de publicar.
- No repitas preguntas ya contestadas.
- Si tiene que hacer clics, guía visual (captura marcada), no sólo texto.
- Ningún trabajo pago (créditos de imágenes o video) sin su OK para ese trabajo exacto.

Reglas de escritura (programa, web y chat)
- Nunca «plata», «mafia» ni «sobreprecio».
- Siempre «la inteligencia artificial del Municipio».
- Nunca «partido» para el territorio: «Luján» o «el Municipio».
- Ninguna oración ni punto empieza con «Y» ni con «Que».
- En un párrafo, dos oraciones no empiezan con la misma palabra.
- Castellano llano de todos los días, sin lunfardo. Oraciones cortas. Ninguna cifra antes de presentarla.
- Cada cifra con su fuente pública, nunca archivos internos del repositorio.
- Lo que necesita un abogado va una vez al final, no en el texto.
- Sin fechas de actualización en el cuerpo. Sin aclaraciones morales en el texto.
- Diseño: ninguna sección empieza al pie de la página con sólo el título; ninguna página con una sola foto; nunca dos imágenes seguidas.
- Web: nada que secuestre el scroll; fácil de navegar antes que linda.

Método (lo aprendido)
- Una sola fuente: cada propuesta se carga una vez, como dato, con texto, costo, efecto en la recaudación, zona, ordenanza y fuente. De ahí salen solos la web, el PDF, la A4, el Excel y el chat. Nada se copia a mano.
- Los números salen del modelo por script, y un control frena el armado si el texto no coincide con el modelo.
- Primero el costo, después el texto. Ninguna propuesta sin su impacto en la recaudación. Un alivio no puede achicar lo que cobra el Municipio: se compensa.
- Costos con la mejor relación calidad-precio, nunca proveedores caros de Estados Unidos.
- La inteligencia artificial lee y propone; las reglas deciden; una persona aprueba (Ley 25.326, artículo 20). Contesta en el idioma en que le hablan.
- Cada entrega de un worker se verifica por separado, comparando con la fuente.
- Todo el código en GitHub desde el primer día; nada queda sólo en una máquina.
- Las imágenes se revisan contra la geografía real de Luján antes de mostrarlas. Nada de caricaturas: realistas.
- Antes de una visita o un evento, la web se congela y se vigila con una tarea programada.
- Es el gobierno actual: tono institucional. Los datos internos se piden al Municipio. Al final, las cuentas y servidores quedan a nombre del Municipio.
