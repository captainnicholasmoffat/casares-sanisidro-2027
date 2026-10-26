# Kit: todo lo aprendido en San Isidro, para Luján y los próximos municipios

Rama `kit-lujan` del repositorio `captainnicholasmoffat/casares-sanisidro-2027`. Armado el 26 de octubre de 2026 por la sesión coordinadora del programa de San Isidro.

Es material de consulta: el método, el código y las lecciones. No se copian a Luján los datos, los nombres ni las propuestas de San Isidro. Esta rama no tiene claves (se revisó archivo por archivo contra las claves reales).

## Dónde está cada cosa

### 1. El programa de San Isidro, terminado
- Rama del worker `claude/cool-hopper-3hdk58` de este mismo repositorio. Último commit verificado: 621a1ef (Dispatch 19). Sigue el Dispatch 20 (`trabajo/DISPATCH_20_DOCUMENTO.txt`).
- Ahí está el motor del documento: PDF de pantalla, A4 de 143 hojas, Excel del modelo fiscal (`doc/build.py`, `doc/content*.py`, `doc/charts.py`), los datos (`data/`), las fuentes bajadas (`01_raw/`) y los informes de investigación (`informes/`).
- Las metodologías: `data/METODOLOGIA_MODELO.md`, `METODOLOGIA_DEFLACTOR.md`, `METODOLOGIA_ZONAS.md`, `COMPARACIONES_VALIDAS.md`, `NO_DISPONIBLE.md`.

### 2. La web con chat (`proyecto/`)
- Publicada en Cloudflare Pages, proyecto `sanisidro2027`, ramas `main` (pública) y `anticipo` (para mostrarle a Nick antes de publicar). Dirección: https://sanisidro2027.pages.dev
- `proyecto/web/data/programa.json`: **la fuente única del programa**. Cada sección: `id`, `texto` (párrafos separados por línea en blanco), `marcas` (negritas y resaltados por párrafo), `orden`, `cuadros`, `fuentes`, `hoja_a4`/`hoja_a4_fin`, `subtitulos`, `recuadro_de`, `tono`.
- `proyecto/web/data/investigaciones.json`: las investigaciones que el chat usa para explicar de dónde sale cada propuesta.
- `proyecto/web/build_site.py`: arma el sitio. Uso: `python3 -I build_site.py ../../trabajo/nueve.json`. Corre antes `cuentas/check.py`.
- `proyecto/web/cuentas/check.py`: cruza cada número del Excel (`cuentas.json`, sale de `modelo_fiscal.xlsx` con `extract.py`) con el texto. Si un número no coincide, el armado se detiene. **Es la lección más importante: ningún número se copia a mano.**
- `proyecto/sitio/functions/api/ask.js` y `proyecto/sitio/lib/claude.js`, `context.js`, `rules.js`: el chat «Preguntale al programa». La clave de Claude vive como secreto en Cloudflare (`ANTHROPIC_API_KEY`), nunca en el navegador. Topes por persona y por día. Responde en el idioma en que le hablan.
- `proyecto/sitio/functions/api/panel/`, `lib/access.js`: el panel interno, cerrado con Cloudflare Access (código por mail).
- `proyecto/sitio/LEEME.md`: cómo subirlo a Cloudflare paso a paso.
- Publicar: `wrangler pages deploy ./public --project-name sanisidro2027 --branch main` (o `--branch anticipo`), con `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID` en el entorno. Después de publicar: probar cada página (200) y una pregunta real al chat (`POST /api/ask`, tiene que traer `text_delta` y `message_stop`).
- `proyecto/despliegue/acciones.json` y `REVISION.md`: el plan de despliegue (302 acciones con camino crítico, holguras, responsables y «cómo se comprueba»).

### 3. Los documentos de trabajo (`proyecto/*.md`)
- `CONTEXTO_PROYECTO_SAN_ISIDRO_v3.md`: el contexto del programa.
- `SKILLS_RELEVAMIENTO.md`: **qué habilidades (skills) adoptar y cuáles escribir**, con fuentes y licencias.
- `WEB_DEMO_PROGRAMA.md`, `WEB_INVESTIGACION.md`, `PLAN_DESPLIEGUE.md`: cómo se diseñó la web, qué se investigó y el plan.
- `CORRECCIONES_LECTURA_NICK.md`, `CORRECCIONES_LECTURA_A4_8_OCTUBRE.md`, `BARRIDO_COMPRENSION_c693a25.md`: las correcciones de Nick, una por una. **Leerlas antes de escribir nada: muestran lo que no quiere.**
- `DISPATCHES_5_OCTUBRE.md`, `PENDIENTE_DISPATCH_DOCUMENTO.md`, `PENDIENTE_D_E.md`: cómo se le escribe a un worker.
- `CAMBIOS_WEB_COMERCIO.md`, `CAMBIOS_WEB_V1_1.md`, `TASA_SEGURIDAD_HIGIENE.md`: cambios grandes, con su verificación.
- `INFORME_IMAGENES.md`: cómo se auditaron las imágenes contra la geografía real.
- `ESQUEMA_MECANISMO_aprobado.html` y `.png`: el esquema aprobado del mecanismo.

### 4. Las herramientas de la sesión coordinadora (`trabajo/`)
- `DISPATCH_18_DOCUMENTO.txt` a `DISPATCH_20_DOCUMENTO.txt`, `box_d*.txt`, `18.md` a `23b.md`: dispatches enviados al worker, en orden.
- `apply_*.py`: cada cambio al programa se hace con un script que deja copia de antes y un registro (`log_*.json`). Las copias: `programa_antes_*.json`.
- `hojas_a4.py`: recalcula en qué hoja de la A4 está cada sección, leyendo el PDF del worker. Uso: `python3 -I hojas_a4.py <a4.txt> [--aplicar]`.
- `chk_*.py`, `tools/`, `filt*/`: controles (enlaces, mapas, cambios de cada dispatch).
- `llano/`, `compr/`: controles de castellano llano y de comprensión.
- `shot_*.py`, `mob*.py`: capturas para revisar la web en computadora y celular.
- `pdfjl/`: cómo se arma un PDF A4 lindo desde HTML (`topdf.py`, con Playwright). Ejemplo: la visita a la panadería.
- `audit/`, `tish/`, `tish_scripts/`, `compras_local/`, `r/`: investigaciones (auditoría, tasa de seguridad e higiene, compras al comercio local, boletín oficial).
- `ocr_*/`, `dl3/`, `*.txt` de ordenanzas, `lom.txt`, `ley15558*.txt`, `leyes/`: textos de las ordenanzas Fiscal e Impositiva, de la Ley Orgánica de las Municipalidades y de otras leyes, con su OCR.
- `geo/`, `kb/`, `kbw/`, `design/`, `esquema/`: mapas (radios censales, zonas), base de conocimiento del chat y diseño.
- `out/`, `xlsx/`, `xl17/`: versiones del modelo fiscal en Excel.
- `*pricing*.html`, `ali_*`, `akool_*`, `deepseek.html` y otros: precios de proveedores de inteligencia artificial (avatares, voz, modelos), usados para costear con la mejor relación calidad-precio.

### 5. Memoria y reglas (`memoria/`)
- `ways-of-working.md`: **todas las reglas que dio Nick** para el programa, el diseño y el trabajo, con fecha.
- `otras_notas.md`: diseño, cuentas, Luján y la «web integrada».
- `tareas_programadas.md`: cómo se vigiló la web antes de la visita.

### 6. Lo que está en otros lugares (no se copió acá)
- Google Drive, unidad compartida «claude», carpeta «Proyecto San Isidro» (ID `1lfETtk5OzDOUdet-THmCldF36alzLkVl`): `01_raw`, `02_clean`, `05_research`, `09_corpus_boletin` y un PDF del programa. Buscar siempre con `parentId`, porque la búsqueda común no la encuentra.
- Proyecto de claude.ai «Campaña Politica Intendencia San Isidro…»: borradores viejos de los capítulos (`CAP1` a `CAP6`, `00_INTRODUCCION`, `99_ANEXO_FUENTES`) y `San_Isidro.pdf`. Ya están superados por `programa.json`.
- Motor de la «web integrada»: `captainnicholasmoffat/malafama-web`, rama `hq/panel` (sólo leer). Ver su `docs/project-status.md` y `docs/hq-system-architecture.md`.

## Lecciones (lo que hay que hacer mejor en Luján)
1. Una sola fuente de datos desde el día uno. En San Isidro, el PDF (worker) y la web (`programa.json`) son dos copias del mismo texto y cada cambio se manda dos veces. En Luján, un solo repositorio y una sola fuente de la que salen la web, el PDF, la A4, el Excel y el chat.
2. Los números salen del modelo por script y se controlan solos (`check.py`). Nunca a mano.
3. Primero el costo y el efecto en la recaudación, después el texto.
4. Cada entrega de un worker se verifica por separado, contra la fuente, antes de decirle a Nick que está bien.
5. Todo el código en GitHub desde el principio. En San Isidro la web vivió semanas sólo en la máquina de una sesión.
6. Los números de hoja de la A4 se recalculan después de cada entrega del worker.
7. Antes de un evento, la web se congela y se vigila.
8. Las imágenes se auditan contra la geografía real antes de mostrarlas.
