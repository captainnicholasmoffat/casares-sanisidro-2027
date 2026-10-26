# Investigación para el sitio web demo del Programa de Gobierno San Isidro 2027

Fecha: 10 de octubre de 2026. Todo lo que sigue se verificó hoy en la fuente indicada. Cuando algo no se pudo confirmar, lo digo con las palabras **«sin confirmar»**. Las recomendaciones propias (no sacadas de una fuente) van marcadas **«recomendación propia»**.

---

## 1. Resumen en 10 líneas

1. Lo mejor hoy, para un HTML único sin compilar: módulos ES con *import map* (ya es estándar en todos los navegadores), **three.js 0.186.1 con WebGL 2**, **GSAP 3.15.0 + ScrollTrigger** (gratis desde abril de 2025, con todos sus plugins) y **Lenis 1.3.26** opcional.
2. **WebGPU todavía no sirve como base:** no es estándar en todos los navegadores, en Android depende del chip gráfico y three.js dice que su renderizador WebGPU sigue «en estado experimental». Se usa el renderizador WebGL.
3. Animación ligada al scroll: el motor es GSAP. Las animaciones por scroll hechas sólo con CSS van como extra (Firefox no las tiene activadas). Las **View Transitions** dentro de una misma página ya andan en todos los navegadores desde octubre de 2025.
4. Mapas: **MapLibre GL JS 6** (o 5.24) con teselas gratis y sin clave (**OpenFreeMap** o el **IGN Argenmap**, probada hoy sobre Acassuso), y las 6 zonas del Censo coloreadas por dato. Pero en una página privada de Claude las teselas externas probablemente queden bloqueadas, así que el plan seguro es un mapa propio en SVG o 3D, sin teselas.
5. 3D: modelos GLB livianos (de 1 a 2 MB como máximo, comprimidos) cargados con GLTFLoader. Descarto Spline (es pago y deja marca de agua), Babylon (pesa 1,1 MB) y React Three Fiber (necesita React y un paso de compilación).
6. Celulares: en Argentina el **56,5 % del tráfico es móvil y el 87 % de ese tráfico es Android**. Presupuesto: unos 250 KB de JavaScript comprimido al abrir, el 3D se carga recién cuando hace falta, y con «reducir movimiento» se ve una versión estática completa.
7. Chatbot: en la página privada de Claude cada pregunta acepta **hasta 256 KiB de texto**. El programa (unos 480.000 caracteres) no entra entero. Hace falta una búsqueda local por palabras clave (MiniSearch u Orama con raíces en español) que mande los 8 a 12 pasajes más relevantes y el índice del programa, y que muestre citas que se puedan tocar para ir a la sección.
8. La búsqueda «por significado» (embeddings) dentro del navegador no conviene: el modelo multilingüe más chico pesa **unos 118 MB**.
9. Higgsfield: su generador de sitios no sirve para el chatbot, porque en un sitio `type: "website"` prohíbe toda generación con IA, también la de texto. Lo que sí sirve son sus videos, imágenes y modelos GLB: se bajan, son nuestros, se pueden usar comercialmente y se meten en nuestro HTML. Sus documentos casi no dan costos en créditos (sólo el personaje 3D animado: 38 créditos más 8 por cada clip).
10. Propuesta: 9 secciones con un solo efecto principal (el **mapa 3D de las 6 zonas, que se arma con el scroll**, sin créditos), más relato de datos con scroll y el esquema del mecanismo animado. Lo que gasta créditos es todo opcional y necesita el OK de Nick: un film de scroll de unos 15 segundos y de 3 a 5 objetos GLB.

---

## 2. Detalle

### A. Buenas prácticas actuales (2025–2026)

#### A1. 3D en el navegador

| Opción | Estado verificado hoy | Veredicto para este sitio |
|---|---|---|
| **three.js** | Versión 0.186.1 (npm, 24 sep 2026). El manual oficial dice que `WebGPURenderer` «is still in an experimental state», que si no hay WebGPU «can automatically fall back to using a WebGL 2 backend», y que `WebGLRenderer` «is still maintained and the recommended choice for pure WebGL 2 applications». Con WebGPU no andan `ShaderMaterial`, `onBeforeCompile` ni `EffectComposer`. | **Usar three.js con `WebGLRenderer`.** |
| **React Three Fiber** | 9.8.1 (24 sep 2026). Pide React `>=19 <19.4` (según las dependencias publicadas en npm). | No para un HTML sin compilar: suma React y está pensado para compilar. |
| **model-viewer (Google)** | 4.3.1 en cdnjs (4 jun 2026). La 4.4.0 salió el 9 oct 2026 y es demasiado nueva. Tiene `poster`, `reveal` y `loading="lazy\|eager\|auto"`. Por defecto baja los decodificadores Draco y KTX2 desde `www.gstatic.com` (lo verifiqué en su código) y trae su propio three.js adentro (pide three `^0.183`). | Sólo si se quiere un visor 3D suelto con giro y zoom. Hay que cambiar los decodificadores a jsDelivr o usar Meshopt. No conviene cargarlo junto con three.js porque se bajaría dos veces. |
| **Spline** | Plan gratis: «Web exports with watermark». Hobby (USD 12 por mes con pago anual): «No watermark on web exports». Su paquete npm no declara licencia libre. Las guías de Higgsfield lo listan como fuente propietaria prohibida. | Descartado. |
| **Babylon.js** | La 9.0 se anunció el 26 mar 2026 (luces agrupadas, iluminación volumétrica, Gaussian splats, andando sobre WebGPU y WebGL 2). En npm va por 9.30.0, pero cdnjs sólo llega a la 8.54.1. `babylon.min.js` pesa unos 1,13 MB comprimido (medido hoy). | Descartado por peso. |

**WebGPU: estado de soporte** (tabla de implementación del grupo gpuweb, editada el 28 may 2026, más los datos de web-features):
- Chrome y Edge: Windows, Mac y ChromeOS desde la 113. En Android 12 o posterior desde la 121 con chips ARM, Qualcomm o Intel. Imagination recién desde Android 16 (Chrome 139). **Samsung Xclipse: «work in progress».** En Linux, parcial.
- Safari: viene activado en macOS, iOS y iPadOS 26.
- Firefox: Windows desde la 141. Mac con Apple Silicon desde la 145 (macOS 26) o la 147. **En Linux y Android todavía no está activado.**
- web-features lo marca como **no Baseline**, es decir que no está en todos los navegadores.

**Modelos GLB livianos:**
- glTF Transform: `gltf-transform optimize input.glb output.glb --compress draco --texture-compress webp` (ejemplo oficial). Para no tener que cargar un decodificador desde otro sitio, conviene `--compress meshopt`: three.js trae `meshopt_decoder.module.js`, de unos 8 KB (verificado en jsDelivr). Lo de meshopt dentro de `optimize` está **sin confirmar** en la página que leí; se confirma con `optimize -h`.
- Buenas prácticas de MDN para WebGL: dibujar en un lienzo más chico que la pantalla («reducing canvas.width and height»), usar texturas comprimidas (Basis/KTX2), evitar las llamadas que bloquean (`getError`, `getParameter`), usar mipmaps sólo en objetos 3D y llevar la cuenta de la memoria de video.
- Higgsfield avisa de dos trampas con GLB generados: el material con `alphaMode: BLEND` se ve «con normales invertidas» (hay que forzar `OPAQUE`), y un navegador sin pantalla no tiene WebGL, así que una captura en blanco no prueba que el 3D esté roto.
- Los modelos de Meshy en Higgsfield salen por defecto con 30.000 triángulos (`target_polycount` acepta de 100 a 300.000). Meshy 7 tiene `model_type: "lowpoly"`. Para la web, apuntar a entre 5.000 y 15.000 triángulos por objeto (**recomendación propia**).

#### A2. Animación ligada al scroll

- **GSAP 3.15.0** (npm, 13 abr 2026).
  - Licencia «Standard No Charge», vigente desde el 30 abr 2025 y modificada el 30 may 2025 (Webflow): «Commercial usage is covered under the standard license».
  - SplitText y MorphSVG «can be used in commercial projects at no charge».
  - Sólo se prohíbe usarlo para herramientas visuales de animación sin código que compitan con Webflow. Dice textual: «AI-generated code is not a "Prohibited Use"».
  - En npm la licencia figura como `Standard 'no charge' license`.
- **ScrollTrigger** (documentación de la versión 3.15):
  - `scrub` ata la animación a la barra de scroll; con un número, por ejemplo `scrub: 1`, la suaviza un segundo.
  - `pin` fija un elemento y `pinSpacing` agrega el espacio que ocupa; con `false` el contenido siguiente se le monta encima.
  - Para distintos tamaños de pantalla se usa `gsap.matchMedia()`. `ScrollTrigger.matchMedia()` está marcado como obsoleto.
- **Lenis 1.3.26** (5 ago 2026, licencia MIT).
  - Para integrarlo con GSAP: `lenis.on('scroll', ScrollTrigger.update)`, después `gsap.ticker.add(t => lenis.raf(t*1000))` y `gsap.ticker.lagSmoothing(0)`.
  - `respectReducedMotion` viene activado por defecto.
  - Dice que «wraps the browser's own scroll, so position: sticky, anchor links, and accessibility keep working».
  - Límites: no anda sobre iframes, en Safari queda en 60 fps y para scroll-snap hace falta `lenis/snap`.
- **Animaciones por scroll sólo con CSS** (`animation-timeline: scroll()` y `view()`):
  - Chrome y Edge desde la 115, Safari desde la 26. **No son Baseline.**
  - En Firefox la preferencia `layout.css.scroll-driven-animations.enabled` viene apagada en la versión normal y prendida sólo en Nightly (desde la 136), según MDN.
  - Se usan sólo como mejora para quien las tenga.
- **View Transitions** (web-features):
  - Dentro de una misma página son «Baseline newly available» desde el **14 oct 2025** (Chrome 111, Safari 18, Firefox 144). Sirven para abrir fichas y cambiar de capítulo con transición.
  - Entre páginas distintas: Chrome 126 y Safari 18.2, sin Firefox.
- **scrollama 3.2.0** (MIT, «Lightweight scrollytelling library using IntersectionObserver», 1,8 KB comprimido en cdnjs). Es una alternativa liviana para relatos «gráfico fijo más pasos de texto».
- **Películas de scroll** (técnica de Higgsfield, ver B2):
  - Un video de unos 15 segundos sin cortes, que avanza o retrocede según el scroll.
  - Exige un solo movimiento de cámara continuo, fondo que soporte texto encima, exposición fija y nada de texto dentro del video.
  - El video se codifica en H.264 con muchos fotogramas clave: GOP 8 en escritorio y GOP 4 con altura máxima de 720 px en celular.

#### A3. Mapas interactivos

- **MapLibre GL JS:**
  - La 6.0.0 salió el **22 jul 2026**. Su registro de cambios dice: «Switch to an ESM-only distribution (`maplibre-gl.mjs`)», «The UMD bundles … are no longer published», «WebGL2 is now required». También agrega «Auto-load worker module for CDN usage».
  - Hay que importarlo con `import * as maplibregl from 'maplibre-gl'`.
  - **En cdnjs, la versión 6 sólo tiene el CSS**; el JavaScript se baja de jsDelivr. La **5.24.0** (23 abr 2026) está completa en cdnjs, en formato de script clásico.
- **Zonas con colores y datos:** la especificación de estilos tiene capas `fill` y `fill-extrusion` («An extruded (3D) polygon»). La altura y el color aceptan expresiones (`interpolate`, `feature-state`), así que se puede pintar o levantar cada zona según su NBI o su porcentaje de hogares sin gas.
- **deck.gl 9.4.0** (5 sep 2026): según la documentación oficial, es «expected to be the final release in the v9 series». El módulo `@deck.gl/maplibre` soporta MapLibre 4, 5 y 6, y WebGPU sigue «experimental». Pesa 558 KB comprimido. **No hace falta para 6 zonas.**
- **Leaflet 1.9.4** (2023) es la versión estable; la 2.0 sigue en alfa (2.0.0-alpha.1, ago 2025). Es liviano (37 KB) pero sólo maneja teselas de imagen, sin 3D.
- **Teselas gratis y sin clave:**
  - **OpenFreeMap:** «completely free», sin límite de vistas ni pedidos, sin registro ni clave. Uso comercial permitido. Atribución obligatoria a OpenFreeMap, OpenMapTiles y OpenStreetMap. Los estilos `https://tiles.openfreemap.org/styles/positron` y `/liberty` respondieron 200 hoy.
  - **IGN Argenmap** (oficial argentino), en formato TMS:
    - `https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png`
    - `…/mapabase_gris@EPSG%3A3857@png/{z}/{x}/{-y}.png`
    - Bajé la tesela 13/2764/3259 y muestra Acassuso y la Av. Centenario.
    - En MapLibre se usa `"scheme": "tms"` con `{y}`. El IGN lo describe como «un servicio libre y gratuito».
    - **Las condiciones de uso exactas están sin confirmar**: no las encontré publicadas.
  - **tile.openstreetmap.org:** se permite para ver mapas interactivos, con atribución visible y sin descargar teselas por adelantado. No hay garantía de servicio y el acceso «may be withdrawn at any point».
  - **Protomaps:** recortes PMTiles que se alojan uno mismo, con licencia ODbL y atribución a OSM. Desaconsejan enlazar sus archivos directo desde sus servidores.
- **Límites de las zonas:** el documento de contexto del proyecto (v3, §4.8) dice que las 6 zonas son «propios, no oficiales»; lo oficial son los 360 radios del INDEC. **El mapa tiene que decirlo.**

#### A4. Rendimiento en celulares, accesibilidad y SEO

- **Quién va a entrar** (StatCounter, septiembre de 2026): en Argentina el tráfico es **56,51 % móvil**, 42,99 % escritorio y 0,5 % tablet. En celulares, **Android tiene el 87,37 %** e iOS el 12,63 %.
- **Metas de Google** (web.dev), medidas sobre el 75 % de las visitas:
  - LCP (cuánto tarda en aparecer lo principal): 2,5 s o menos.
  - INP (cuánto tarda en responder a un toque): 200 ms o menos.
  - CLS (cuánto se mueve la página mientras carga): 0,1 o menos.
- **Reglas prácticas** (recomendación propia, apoyada en MDN y en las guías de Higgsfield):
  - Al abrir: HTML, texto y GSAP, menos de 300 KB comprimidos. three.js, GLB y mapa se cargan recién cuando la sección se acerca a la pantalla.
  - En el 3D: `renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5))`, un solo lienzo WebGL, pausar el dibujo cuando no se ve y una imagen estática como portada hasta que el 3D esté listo.
  - Animar sólo `transform` y `opacity`, y nunca escuchar el evento `scroll` a mano (regla de design-taste-frontend).
- **Accesibilidad** (WCAG 2.2):
  - 2.2.2 (nivel A): todo lo que se mueve solo por más de 5 segundos necesita una forma de pausarlo.
  - 2.3.3 (nivel AAA): el movimiento que dispara una interacción, incluido el parallax, se tiene que poder apagar.
  - 1.4.3 (nivel AA): contraste de 4,5:1 para texto normal y 3:1 para texto grande (18 pt, o 14 pt en negrita).
  - `prefers-reduced-motion` funciona en todos los navegadores desde 2022.
  - En Argentina existe la Ley 26.653 de accesibilidad web (2010), que remite a WCAG 2.0 (página de políticas del W3C). A quién obliga no lo confirmé en esa fuente.
- **SEO** (Google, «JavaScript SEO basics»):
  - Google sólo ve lo que queda en el HTML ya dibujado.
  - Los enlaces tienen que ser `<a href>`.
  - Recomienda dibujar la página en el servidor o de antemano («server-side or pre-rendering is still a great idea»).
  - Para nosotros: **todo el texto del programa va escrito en el HTML**, no inyectado por JavaScript. Además, ese mismo texto alimenta el índice del chatbot.
  - Una página privada de Claude no se indexa, así que el SEO pesa recién cuando se hostee abierta.

#### A5. Ejemplos recientes destacados

- **Awwwards, Sitios del Año 2025:**
  - **Lando Norris** (estudio OFF+BRAND). Etiquetas: 3D, WebGL, GSAP, Webflow, gestos e interacción. Sitio del Día el 17 nov 2025.
  - **Messenger** (estudio abeto). Etiquetas: 3D, WebGL, WebSockets, Three.js, storytelling. Sitio del Día el 10 nov 2025.
  - **2024:** Igloo Inc (abeto), Don't Board Me y Opal Tadpole.
- **Vitrina de GSAP** (hoy): A24, Illoca (Unseen Studio), See What Eye See y otros. La página no detalla las técnicas.
- **Lista secundaria** (hontran.dev, 27 jun 2026; no es fuente primaria): By-Kin (GSAP con scroll suavizado), Iventions (escena Three.js con GSAP) y Mat Voyce (tipografía en movimiento con GSAP).
- **Periodismo de datos:**
  - Los Sigma Awards 2026 eligieron 10 ganadores entre 31 finalistas.
  - Los latinoamericanos fueron Salud con Lupa (Perú), Quinto Elemento Lab (México) y Ambiental Media (Brasil).
  - **Qué técnicas usan: sin confirmar.** Las fuentes no las describen.
- **Sitios de campañas o programas de gobierno municipales con premio:** **no encontré ninguno verificable** en 2025–2026.
- Lo que se repite en los premiados (síntesis propia de las etiquetas):
  - Un objeto 3D protagonista con WebGL.
  - Revelados con GSAP y scroll suavizado.
  - En periodismo, el patrón «gráfico fijo más pasos de texto».

#### A6. Chatbot dentro de la página

**Patrones de interfaz que funcionan** (Nielsen Norman Group):
- «10 Guidelines for Designing Your Site's AI Chatbots» (24 abr 2026). Las que aplican acá:
  - Decir al principio qué puede hacer el chatbot.
  - Preguntas sugeridas **como botones, no como texto**.
  - Detalles que se abren y cierran, para que la conversación no se alargue.
  - **No mover la vista al final** de una respuesta larga.
  - Ventana que se pueda agrandar.
  - Poder guardar o compartir la respuesta.
  - Opción de dictar por voz.
- «Prompt Suggestions» (25 abr 2025): las sugerencias de seguimiento que aparecen debajo de cada respuesta «tend to be the most relevant and useful».
- «Explainable AI in Chat Interfaces» (12 dic 2025):
  - Cada cita va pegada a la frase que respalda, enlaza **al pasaje exacto** y lleva un nombre descriptivo, no «Fuente».
  - Avisar que puede equivocarse, porque la gente «rarely click[s] citation links».
- Idioma: basta una instrucción («respondé en el idioma en que te escriben»). No hace falta detectar el idioma.

**Límites reales del canal** (contrato de las páginas de Claude, capacidad `sample`, versión 0.2.75):
- Cada llamada lleva **como máximo 256 KiB (262.144 bytes) de texto**. El programa, con unos 480.000 caracteres, ocupa casi 490 KB, así que **no entra entero**.
- Cada pregunta gasta el uso de Claude de quien pregunta, y la primera vez el navegador pide permiso.
- Las respuestas repetidas se guardan 5 minutos.
- Tiempos:
  - Nivel `"quick"`: responde en 1 o 2 segundos.
  - Nivel normal: tarda entre 5 y 60 segundos antes de empezar a escribir.
- Se le pueden dar **funciones de la propia página** como herramientas (por ejemplo `buscarEnPrograma`):
  - Cada respuesta de herramienta admite como máximo 32 KB.
  - Cada vuelta es otra consulta.
  - Una pregunta de 3 vueltas tarda de 30 a 90 segundos en el nivel normal y alrededor de un segundo por vuelta en `"quick"`.
- El mismo contrato dice que la página **«cannot fetch images from URLs (its network is blocked)»**. Ver Riesgos.

**Cómo buscar en 480.000 caracteres desde el navegador:**
- Anthropic, «Contextual Retrieval» (19 sep 2024):
  - Si la base es menor a 200.000 tokens, se puede mandar entera con caché de consulta.
  - Combinar búsqueda por significado y por palabras (BM25) redujo las fallas un 49 %, y con reordenamiento un 67 %.
  - Mandar los 20 mejores fragmentos funcionó mejor que 5 o 10.
  - Fragmentos de «unos pocos cientos de tokens».
- Los modelos actuales de Claude tienen 1 millón de tokens de contexto (página de modelos). Mandar el programa entero sólo es posible **en la versión hosteada con la API**, no en la página privada.
- **MiniSearch 7.2.0** (5 KB comprimido):
  - Búsqueda de texto en memoria, con prefijos, tolerancia a errores de tipeo, peso por campo y autocompletado.
  - «No stemming is performed, and no stop-word list is applied» por defecto: hay que agregarlo con `processTerm`.
- **Orama 3.1.18:**
  - «33 languages» y, para cada uno, «a default tokenizer, stop-words, and stemmer».
  - En jsDelivr confirmé los archivos en español `@orama/stemmers/dist/es.js` y `@orama/stopwords/dist/es.js`.
  - También trae búsqueda vectorial (`searchVector`).
- **Embeddings en el navegador** (transformers.js 4.3.0):
  - Los modelos multilingües pesan demasiado: `multilingual-e5-small` en int8, 118 MB; `embeddinggemma-300m` en q4, unos 197 MB (Hugging Face).
  - Además se bajan de huggingface.co, que en la página privada probablemente esté bloqueado.
  - **No conviene.**
- **Citas en la versión hosteada:** la API de Claude tiene «citations». Con documentos de texto cita por rangos de caracteres y con contenido propio por bloques. «All active models support citations», y el texto citado no cuenta como tokens de salida.

### B. Higgsfield (leído con `get_workflow_bundle_file`, workflow `website-builder-flow`, versión 2026-07-25)

#### B1. Qué tipos de sitio permite

- **Tres tipos.** El usuario elige uno al crear:
  - **`website`**: marca propia, sin ninguna integración con Higgsfield.
  - **`app`**: con «Sign in with Higgsfield», el SDK fnf y su diseño Quanta, de modo que «must look and feel like a Higgsfield product».
  - **`game`**: juego con salas multijugador.
- **Tecnología.** React 19 con TanStack Start, dibujado en el servidor (SSR) y desplegado como un Cloudflare Worker en `<subdominio>.higgsfield.app`.
  - Base de datos D1, almacenamiento R2 y KV sólo si se piden en `app.manifest.json`.
  - **Cada deploy queda publicado en vivo enseguida**: «Every deploy ships the live public site». No hay etapa de prueba.
- **Pasos obligatorios del armado.**
  - Primero una pregunta: «Animated (recommended)» o «Non-animated».
  - Brief de diseño.
  - Una **imagen de referencia por sección**.
  - Kit de recursos generados.
  - Construcción fiel a esas imágenes.
  - Pasada de movimiento.
  - Control mecánico con comandos de búsqueda en el código.
  - Deploy.
  - Además, cada armado exige una **portada generada** y sus metadatos.
- **Plantillas.**
  - `scroll-scrub` para el sitio animado, que trae el motor de «película de scroll» ya hecho.
  - Sin plantilla para el no animado.
  - En `app`: `studio`, `preset`, `app-detail` y `custom`.
- **Mapas.** El directorio de ingredientes no trae MapLibre ni Leaflet. Sólo globos (`cobe`, el `globe` de Magic UI) y un `map` de Eldora UI. Además, un `website` «may still use ordinary non-generation third-party APIs — payments, maps, email — with the user's own keys».

#### B2. Efectos y técnicas que trae (wow-catalog y wow-maker)

- **A, película de scroll.**
  - A1: un clip de unos 5 segundos convertido en unas 100 imágenes y dibujado en un lienzo.
  - A2: 2 a 4 clips con capítulos.
  - A3: un producto que gira con el scroll.
  - **A4: el «sitio animado», que es su opción por defecto.** Un film de unos 15 segundos que el scroll recorre de punta a punta, o de 4 a 7 «mundos» encadenados por el último fotograma real de cada uno.
- **B, profundidad.**
  - B1: recortes en capas con parallax.
  - B2: dos versiones de la misma imagen, apagada y encendida, que se cruzan con el cursor o el scroll.
  - **B3: imagen aprobada → `generate_3d` → GLB → escena 3D que gira con el scroll.**
- **C, imagen viva.** Distorsión al pasar el cursor, imagen que se deshace en partículas, máscara que se abre con el scroll.
- **D, la página se mueve.** Riel horizontal, capítulos que se apilan, tipografía en movimiento.
- **Efectos de autor.** Héroe de partículas que cambian de forma, vitrina 3D que gira manteniendo apretado, revelado tipo rayos X con el cursor, tarjetas esmeriladas sobre el film, entre otros.
- **Librerías permitidas** (todas libres):
  - motion, GSAP, Lenis, three más R3F y drei, postprocessing, shadergradient.
  - tsParticles, cobe, ogl, maath, anime.js, number-flow, split-type, swiper.
- **Fuentes prohibidas por ser propietarias:** Unicorn Studio, Cult Pro, React Bits, **Spline**, Rive, Origin UI, hover.dev, Aceternity Pro y Motion+.
- **Prohibido como efecto principal:** un video que se reproduce solo y nada más, apariciones genéricas con fundido, partículas detrás del texto, cintas de texto corrido, tarjetas que se inclinan.
- **Reglas del efecto principal.**
  - Uno solo por página.
  - Tiene que **responder a lo que hace el usuario**.
  - Tiene que verse completo en una captura.
  - Tiene que tener versión estática para «reducir movimiento».
  - Tiene que declarar cómo se simplifica en celulares.

#### B3. ¿Un sitio `type: "website"` puede tener un chatbot de IA? **No.** Regla textual (SKILL.md):

> «`type: "website"` — a standalone product with NO Higgsfield integration and **NO AI generation of any kind** (no image/video/audio/text generation — not via Higgsfield, and not via some other provider)»

y

> «**Generation is ALWAYS an app.** … NEVER offer the user an option to "bring your own image/video API" or plug in their own generation key for a website — that path does not exist.»

El tipo `app` obliga a «Sign in with Higgsfield» y al diseño Quanta. Por eso queda descartado para nuestro sitio, como ya estaba anotado en `WEB_DEMO_PROGRAMA.md`.

#### B4. Qué se puede llevar a nuestro propio HTML

- **Sí, las tres cosas:** videos, imágenes y GLB.
  - Su propio flujo genera durante el armado, **descarga los archivos al sitio** y publica un sitio «standalone … that performs no runtime generation».
  - Dicen: «Internal use of Higgsfield generation tools is invisible to visitors and always fine».
  - El GLB de `generate_3d` está pensado para cargarse en una escena three.js o R3F.
- **Propiedad.**
  - Ayuda de Higgsfield (2 ago 2026): «You own your outputs». El uso comercial no depende del plan.
  - **Los planes pagos bajan sin marca de agua.**
  - No se pueden usar las salidas para entrenar modelos.
  - Sección 5.3: no se puede subir ni usar la imagen de otra persona sin su permiso.
  - Términos vigentes desde el 27 ago 2026: «We don't claim your inputs or outputs, and you can use them commercially».
  - Sobre contenido político o electoral, las páginas que leí **no dicen nada (sin confirmar)**.
- **Detalles prácticos.**
  - Bajar cada resultado apenas termine. En la API directa de Meshy los enlaces vencen en unos 3 días. Cuánto duran los enlaces de Higgsfield está **sin confirmar**.
  - Higgsfield rechaza subir un `.glb` suelto: hay que comprimirlo en `.zip`.
  - El rigging (esqueleto para animar) funciona sólo con figuras humanas.
- **Modelos 3D disponibles** (consultado con `models_explore`):
  - Meshy: `image_to_3d`, `meshy_v7_image_to_3d` (con modo `lowpoly`), `multi_image_to_3d` y `3d_rigging`.
  - Meta: `sam_3_3d`.
  - Tripo: `tripo_h3_1_image_to_3d` y su variante multivista.
  - Tencent: `hunyuan3d_v3_image_to_3d`, que sale por defecto con 500.000 caras y es muy pesado para la web.
- **Película de scroll en un HTML propio.**
  - Codificar en H.264: escritorio con CRF ~20 y GOP 8; celular con altura máxima de 720 px, CRF ~23 y GOP 4.
  - Portada = primer fotograma del clip ya codificado.
  - Presupuesto: 32 MiB en total para escritorio y 16 MiB para celular.
  - Agregar `blob:` en la directiva `media-src` de la política de seguridad (CSP).
  - En nuestro caso hay que escribir el motor a mano, porque el de Higgsfield viene en su plantilla React.

#### B5. Cuánto cuestan en créditos

Lo único que los documentos dicen con números:
- Personaje 3D texturizado, con esqueleto y animado, hecho con la herramienta nativa: **38 créditos**, más **8 por cada clip extra** (game-3d-animation.md).
- Las cifras de «~85» y «41 créditos» se refieren a créditos **de Meshy** por su API directa, no a créditos de Higgsfield.

Lo que dicen sin números:
- El video «costs credits», y por eso la portada en video exige pedir permiso.
- Generar el video sin audio es «cheaper».
- El modo `fast` de Seedance 2.0 es «cheaper/faster» (sólo en 480p y 720p).
- Las imágenes `gpt_image_2` tienen calidad baja, media o alta y resolución 1k, 2k o 4k.
- Texturizar y ponerle esqueleto a un 3D «adds cost».

**Sin confirmar:**
- El costo de una imagen, de un video de 15 segundos o de un GLB estático. `models_explore` no muestra precios y la página de precios de Higgsfield no se pudo leer porque se arma con JavaScript.
- Hay que pedir el costo exacto antes de generar.

#### B6. Buenas prácticas de diseño que recomiendan

**design-taste-frontend:**
- Antes de diseñar, una línea de «lectura del encargo».
- Tres diales, de variación, movimiento y densidad: la base es 8/6/4 y **«servicio del sector público» es 3/2/5**. Un programa de gobierno está más cerca de lo segundo; sugiero algo como 6/5/4 (**recomendación propia**).
- **Serif** sólo con justificación editorial: Spectral la tiene, porque viene de un documento impreso.
- Una sola paleta, un solo color de acento y un solo sistema de esquinas.
- Héroe:
  - Como máximo 4 elementos de texto.
  - Título de 2 líneas como máximo y bajada de 20 palabras como máximo.
  - Altura con `min-h-[100dvh]`, nunca `h-screen`.
- Rótulos chicos en mayúscula: como mucho uno cada 3 secciones.
- Prohibido:
  - 3 tarjetas iguales en fila, o 3 o más secciones seguidas con el mismo zigzag de imagen y texto.
  - Indicaciones de «scroll».
  - Números de sección como rótulo.
  - Cifras inventadas.
  - Guiones largos.
- Movimiento «motivado» (que comunique jerarquía, relato, respuesta o cambio de estado).
- `prefers-reduced-motion` obligatorio.
- Modo claro y oscuro.
- Metas de rendimiento LCP < 2,5 s, INP < 200 ms y CLS < 0,1.

**Paleta.** Prohíben por cliché «beige/cream + brass/clay/oxblood». La paleta del documento (fondo #F5F0E8 con bordó #7C2E23) cae justo en esa familia, salvo que sea la marca del usuario, que es nuestro caso. Igual hay que distinguir el sitio por el contenido (mapa y datos), no por la paleta.

**wow-catalog, review-rubric e image-to-code:**
- Un solo efecto principal, elegido a partir de la idea central del sitio.
- **Nada puede quedar invisible esperando el scroll** (`opacity:0` hasta que entra en pantalla).
- La «trampa del espaciador»: un héroe fijado deja un hueco en blanco en la captura de página completa.
- Cada botón con su propia identidad.
- Se construye fiel a las imágenes de referencia («the board wins»).

**seo.md y security.md:**
- Títulos de 60 caracteres como máximo y descripción de 150 a 160.
- Dirección canónica, `robots` y `sitemap`.
- JSON-LD con `@graph` (WebSite, Organization y FAQPage si se muestran preguntas frecuentes).
- Para buscadores con IA: encabezados que sean preguntas reales y respuestas directas.
- Un solo `h1`, `alt` en todas las imágenes, enlaces con texto que se entienda solo y al menos 200 palabras visibles.
- Nunca meter HTML sin limpiar: aplica a la respuesta del chatbot, que pasa por DOMPurify.

### C. Librerías por CDN (todas respondieron HTTP 200 hoy; peso = bytes transferidos comprimidos)

Versiones publicadas antes del 26 sep 2026 (más de dos semanas), con la fecha de npm.

| Librería | Versión (fecha) | URL exacta | Peso | Uso |
|---|---|---|---|---|
| three.js | 0.186.1 (24 sep 2026) | `https://cdnjs.cloudflare.com/ajax/libs/three.js/0.186.1/three.module.min.js` | 74 KB | 3D (WebGL 2) |
| three.js, núcleo | 0.186.1 | `https://cdnjs.cloudflare.com/ajax/libs/three.js/0.186.1/three.core.js` (lo importa el anterior) | 209 KB | La versión `.min` pesa 84 KB, ver nota |
| three.js, complementos | 0.186.1 | `https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/loaders/GLTFLoader.js` (y `controls/OrbitControls.js`, `libs/meshopt_decoder.module.js`, `loaders/DRACOLoader.js`) | 27 / 9 / 8 / 6 KB | cdnjs no trae los complementos |
| GSAP | 3.15.0 (13 abr 2026) | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/gsap.min.js` | 26 KB | Animación |
| ScrollTrigger | 3.15.0 | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/ScrollTrigger.min.js` | 16 KB | Scroll |
| SplitText / Flip | 3.15.0 | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/SplitText.min.js` · `…/Flip.min.js` | 3 / 9 KB | Títulos y transiciones |
| Lenis | 1.3.26 (5 ago 2026) | `https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js` + `…/dist/lenis.css` | 6 KB | Scroll suave (opcional; no está en cdnjs) |
| MapLibre GL JS 6 | 6.11.2 (24 sep 2026) | `https://cdn.jsdelivr.net/npm/maplibre-gl@6.11.2/dist/maplibre-gl.mjs` + CSS `https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/6.11.2/maplibre-gl.min.css` | 153 KB + 145 KB (shared) + 6 KB (worker) | Mapa (versión hosteada) |
| MapLibre GL JS 5 (todo en cdnjs) | 5.24.0 (23 abr 2026) | `https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.min.js` + `…/maplibre-gl.min.css` | 223 KB | Alternativa en formato de script clásico |
| Leaflet | 1.9.4 (18 may 2023) | `https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js` + `…/leaflet.min.css` | 37 KB | Alternativa liviana, sin 3D |
| model-viewer | 4.3.1 (4 jun 2026) | `https://cdnjs.cloudflare.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js` (`type="module"`) | 236 KB | Sólo si se usa un visor suelto |
| D3 | 7.9.0 (12 mar 2024) | `https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js` | 78 KB | Gráficos y mapa SVG |
| scrollama | 3.2.0 (17 jun 2022) | `https://cdnjs.cloudflare.com/ajax/libs/scrollama/3.2.0/scrollama.min.js` | 2 KB | Pasos de relato (opcional) |
| MiniSearch | 7.2.0 (16 sep 2025) | `https://cdnjs.cloudflare.com/ajax/libs/minisearch/7.2.0/es/index.min.js` (o `umd/index.min.js`) | 5 KB | Buscador del chatbot |
| Orama + español | 3.1.18 (19 dic 2025) | `https://cdn.jsdelivr.net/npm/@orama/orama@3.1.18/dist/browser/index.js` · `https://cdn.jsdelivr.net/npm/@orama/stemmers@3.1.18/dist/es.js` · `https://cdn.jsdelivr.net/npm/@orama/stopwords@3.1.18/dist/es.js` | varios archivos chicos | Alternativa con raíces en español |
| marked | 18.0.14 (22 sep 2026) | `https://cdnjs.cloudflare.com/ajax/libs/marked/18.0.14/lib/marked.umd.min.js` | 13 KB | Respuesta del chatbot en formato |
| DOMPurify | 3.4.16 (23 sep 2026) | `https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.4.16/purify.min.js` | 10 KB | Limpiar el HTML de la respuesta |
| pmtiles | 4.5.0 (10 ago 2026) | `https://cdn.jsdelivr.net/npm/pmtiles@4.5.0/dist/pmtiles.js` | 8 KB | Sólo si se aloja un recorte de Protomaps |
| Tipografías | Google Fonts | `https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap` | — | Spectral e Inter |

**No recomendadas** (las anoto para comparar; también responden 200):
- Babylon.js en cdnjs, 8.54.1 (5 mar 2026): 1.129 KB.
- deck.gl 9.4.0 desde jsDelivr (`/dist.min.js`): 558 KB.
- transformers.js 4.3.0: 166 KB más un modelo de 118 MB o más.

**Notas técnicas:**
- `three.module.min.js` (tanto en cdnjs como en jsDelivr) importa `./three.core.js` sin minificar, y eso son 125 KB de más.
- Un *import map* puede redirigir esa dirección exacta a `three.core.min.js`. **Sin probar en navegador: hay que probarlo.**
- MapLibre 6 en cdnjs sólo tiene el CSS (lo verifiqué en la API de cdnjs).
- GSAP y Lenis se cargan con `<script src>` común y quedan como variables globales.

Esqueleto de *import map* (los nombres son los que exigen las librerías):

```html
<script type="importmap">
{ "imports": {
  "three": "https://cdnjs.cloudflare.com/ajax/libs/three.js/0.186.1/three.module.min.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.186.1/examples/jsm/",
  "maplibre-gl": "https://cdn.jsdelivr.net/npm/maplibre-gl@6.11.2/dist/maplibre-gl.mjs",
  "minisearch": "https://cdnjs.cloudflare.com/ajax/libs/minisearch/7.2.0/es/index.min.js"
} }
</script>
```

---

## 3. Propuesta concreta

### 3.1 Stack

- **Un HTML hecho por el coordinador.** El texto completo del programa va en HTML semántico, con un `id` por capítulo y por sección (por ejemplo `cap4-s3`).
  - Mismas tipografías y paleta del documento.
  - Colores definidos como variables, con versión oscura (lo exige el contrato de páginas de Claude).
- **Movimiento:**
  - GSAP 3.15.0, ScrollTrigger y SplitText.
  - Lenis 1.3.26 sólo en escritorio y apagado con «reducir movimiento».
  - View Transitions para abrir fichas.
  - CSS por scroll sólo como extra.
- **3D:** three.js 0.186.1 con `WebGLRenderer`, cargado recién cuando hace falta.
  - Las zonas se arman con `ExtrudeGeometry` a partir de GeoJSON proyectado.
  - Los GLB se comprimen con meshopt y texturas WebP.
- **Mapa:**
  - **En la página privada de Claude:** mapa propio, sin teselas. Va en SVG con D3 y en 3D con three.js, con las 6 zonas y una base mínima (río, avenidas principales, vías) en GeoJSON simplificado de OpenStreetMap, con atribución ODbL.
  - **En la versión hosteada:** MapLibre 6 con OpenFreeMap Positron o IGN `mapabase_gris`.
- **Chatbot** «Preguntale al programa»:
  - MiniSearch con normalización de acentos y raíces, u Orama con `es`.
  - marked y DOMPurify para mostrar la respuesta.
  - En la página privada se usa la capacidad `sample` (nivel normal; nivel `quick` para reformular la pregunta). En la versión hosteada, la API de Claude con citas.
- **Peso al abrir** (estimación propia): entre 150 y 250 KB comprimidos de JavaScript y CSS, más el texto (unos 480.000 caracteres, que comprimidos quedan en el orden de 150 KB, **sin medir**). three.js (de 160 a 285 KB) y los GLB se cargan cuando la sección se acerca.

### 3.2 Secciones

Un solo efecto principal: el mapa del héroe. Los demás son de apoyo y tienen un motivo.

| # | Sección (capítulo) | Qué se ve y qué efecto | Técnica | Hecho con | Créditos |
|---|---|---|---|---|---|
| 0 | **Portada.** «Programa de Gobierno San Isidro 2027» y su subtítulo, sin nombre ni foto del candidato. | El partido en 3D, visto en diagonal. Con el scroll, las 6 zonas suben como bloques cuya altura es «hogares sin gas de red». La cámara baja hacia Boulogne y Béccar. Primero aparece una imagen fija y después el 3D. | three.js extrusión + ScrollTrigger `scrub` | A mano (geometría de las zonas del Exhibit 15) | **No** |
| 1 | **Preguntale al programa** (entrada visible, después flotante) | Preguntas sugeridas como botones, por perfil: «Tengo una cafetería en Martínez», «Vivo en Boulogne y no tengo gas», «¿De dónde salen los recursos?», «¿Qué pasa en los primeros 100 días?» | Panel con View Transition | A mano | **No** (usa Claude de quien pregunta) |
| 2 | **Introducción** | Título que se arma palabra por palabra y 3 cifras grandes que cuentan hacia arriba (297.282 habitantes, 6 zonas, 360 radios) | SplitText + contador | A mano | **No** |
| 3 | **Cap. 1 Diagnóstico** | Mapa fijo y pasos de texto. Cada paso pinta las zonas con otro indicador (NBI, sin cloaca, sin gas, hacinamiento, universitarios) y debajo hay una tabla accesible equivalente. | Mapa SVG con `pin` + scrollama o ScrollTrigger | A mano (D3) | **No** |
| 4 | **Cap. 2 La gestión, medida** | Fila de 106 puntos (municipios) que se ordena. San Isidro se destaca en el puesto 20 de 106 en personal y en el 4 de 106 en obra. | D3 + GSAP Flip | A mano | **No** |
| 5 | **Cap. 3 Recursos** | Un número grande (35.994 M sin cobrar) y las líneas de los escenarios (base, adverso, reformista) que se dibujan con el scroll | Trazo SVG con `scrub` | A mano | **No** |
| 6 | **Cap. 4 El mecanismo** | El esquema aprobado (`ESQUEMA_MECANISMO_aprobado`) se arma paso a paso. Al lado, una «maqueta» 3D de una cuadra con 3 a 5 objetos de obra vecinal (conexión de gas, vereda, luminaria, banco de plaza) que aparecen en orden. | GSAP timeline + three.js GLTFLoader | Esquema a mano; objetos **generados con Higgsfield** (opcional) | **Sí, opcional** (imagen de cada objeto + `generate_3d`) |
| 7 | **Cap. 5 Qué hacemos en cada área** | Riel horizontal fijado con fichas por área, usando las 13 imágenes aprobadas. Al tocar una ficha se abre el detalle con View Transition. | ScrollTrigger horizontal + View Transitions | A mano con imágenes ya aprobadas | **No** |
| 8 | **Cap. 6 Primeros 100 días** | Línea de tiempo con tarjetas que se apilan | Apilado fijo (`pin`, `pinSpacing:false`) | A mano | **No** |
| 9 | **Fuentes** | Lista completa, enlazable y que se puede buscar | HTML | A mano | **No** |

**Opcional y con créditos** (todo necesita el OK explícito de Nick antes de generar):
- **Film de scroll para la portada.** Reemplazaría la sección 0 o iría justo después.
  - 1 imagen de guion (`gpt_image_2`, calidad alta).
  - 1 video (Seedance 2.0) de unos 15 segundos, 1080p, sin audio, con un solo movimiento lento (por ejemplo, un sobrevuelo desde la barranca y el río hacia el oeste del partido).
  - Respeta su «contrato de rodaje»: sin cortes, fondo que soporte texto, sin texto adentro.
  - Costo **sin confirmar**.
  - Opinión: no hace falta si el mapa 3D sale bien; las dos cosas juntas serían dos efectos principales.
- **Objetos GLB del mecanismo:** de 3 a 5 objetos estáticos (sin esqueleto). Primero una imagen de cada uno (créditos) y después `generate_3d` con unos 10.000 triángulos o Meshy 7 `lowpoly` (créditos). Costo **sin confirmar**. Si fueran personajes animados, son 38 créditos cada uno más 8 por clip.
- **Imagen para compartir** (1200 × 630): se puede generar (créditos) o armar a mano con una imagen aprobada (**sin créditos**).

**Hecho a mano sin créditos:** todo lo demás. Mapas, gráficos, esquema, textos, buscador, chatbot y las 13 imágenes ya aprobadas.

### 3.3 Cómo responde el chatbot

1. Al cargar la página, el texto se arma en fragmentos por sección (de 800 a 1.500 caracteres), cada uno con «capítulo y título de sección» al frente.
2. Se indexa con MiniSearch:
   - El título pesa 3 veces más que el texto.
   - Se toleran errores de tipeo (`fuzzy` 0,2) y se buscan prefijos.
   - Se sacan los acentos con NFD.
   - Se quitan las palabras vacías del español.
3. Se suma una lista de sinónimos de vecino: «luz» → alumbrado, «baches» → pavimento, «cafetería» → comercio y habilitación, etcétera.
4. **Opcional:** una llamada `quick` reescribe la pregunta en palabras clave.
5. A Claude se le mandan:
   - Las reglas: responder sólo con el programa, decir de qué capítulo y sección sale cada cosa, decir «el programa no habla de esto» cuando corresponda, contestar en el idioma de la pregunta, usar voseo y respetar las palabras prohibidas del documento.
   - El índice del programa con una línea por sección (unos 8 KB).
   - Los 8 a 12 fragmentos más relevantes (de 40 a 60 KB).
   - Total muy por debajo de 256 KiB.
6. Las citas se muestran como botones con el nombre de la sección. Al tocar una, la página baja a esa sección y la resalta.
7. Debajo de cada respuesta van 2 o 3 preguntas de seguimiento. No se baja la vista sola al final de la respuesta, y se puede copiar.
8. **Alternativa más «agéntica»:** darle a Claude la herramienta `buscarEnPrograma(consulta)` para que busque él mismo. Responde mejor a preguntas cruzadas, pero tarda de 30 a 90 segundos en el nivel normal.
9. **Versión hosteada:**
   - La misma búsqueda local más la API con «citations». O, si se acepta el costo, el programa entero, que con 1 millón de tokens de contexto entra.
   - Estimación con precios de lista (sin caché, sin medir tokens; unos 140.000 tokens si va entero):
     - Programa entero: con Haiku 5.5, unos USD 0,014 por pregunta; con Sonnet 5.5, unos USD 0,28.
     - Con búsqueda local (unos 15.000 tokens): aproximadamente la décima parte.

---

## 4. Riesgos y límites

- **Red bloqueada en la página privada de Claude.**
  - El contrato de esas páginas permite scripts sólo de cdnjs, jsDelivr, unpkg, cdn.tailwindcss.com y code.jquery.com, CSS sólo de Google Fonts, y «everything else inline».
  - La capacidad `sample` dice que la página no puede bajar imágenes de URLs porque «its network is blocked».
  - **Muy probablemente queden bloqueadas** las teselas de OpenFreeMap o del IGN, los modelos de Hugging Face y los decodificadores de gstatic.
  - El *worker* de MapLibre cargado desde jsDelivr también puede fallar.
  - **Probarlo con una página mínima antes de construir.** Los GLB y los MP4 van publicados como archivos junto a la página (como máximo 15 MB cada archivo binario y 16 MB la página).
- **Chatbot:**
  - Funciona sólo para quien abre la página con una cuenta de Claude, gasta el uso de esa persona y la primera vez le pide permiso.
  - Cada llamada lleva como máximo 256 KiB, así que **la búsqueda local es obligatoria**.
  - El modelo puede equivocarse. Mitigaciones: sólo pasajes del programa, citas verificables, «no está en el programa» como respuesta válida y una advertencia visible.
- **WebGPU y CSS por scroll** no están en todos los navegadores: en Android dependen del chip y Firefox no los tiene activados. Todo tiene que andar sin ellos.
- **Celulares de gama media:** el 3D y los videos son lo más caro.
  - Hace falta una imagen fija de reemplazo, cargar a demanda y limitar la densidad de píxeles.
  - Con «reducir movimiento», la historia completa tiene que poder leerse sin animación y sin bajar videos.
- **Higgsfield:**
  - Costos por imagen, video y GLB **sin confirmar**.
  - Duración de los enlaces de resultado **sin confirmar**: bajar todo enseguida.
  - El plan gratis baja con marca de agua.
  - Sección 5.3: no usar imágenes de personas reales sin permiso. La tapa ya excluye la foto del candidato.
  - Nada de esto se genera sin el OK de Nick (regla ya anotada).
- **Paleta:**
  - `CONTEXTO_PROYECTO_SAN_ISIDRO_v3.md` (8 sep) dice «PROHIBIDO EL ROJO». El esquema aprobado del 10 oct usa bordó #7C2E23 y coral #DB6B4B.
  - Además, Higgsfield considera crema con bordó un cliché.
  - **Confirmar con Nick** qué paleta va en la web.
- **Mapa:**
  - Las 6 zonas son límites propios, no oficiales. Hay que decirlo en el mapa.
  - Las condiciones de uso de las teselas del IGN están **sin confirmar**.
  - No pude abrir el repo `casares-sanisidro-2027` desde esta sesión para confirmar el archivo de geometría del Exhibit 15.
- **Versiones:**
  - model-viewer 4.4.0 y MapLibre 6.12 y 6.13 son demasiado nuevas.
  - cdnjs va atrasado en Babylon (8.54.1) y no tiene el JavaScript de MapLibre 6.
  - El truco del *import map* para `three.core.min.js` está **sin probar**.
- **No investigado:**
  - Reglas electorales argentinas sobre chatbots o IA en campañas.
  - A quién obliga exactamente la Ley 26.653.
  - Un ejemplo premiado de sitio de programa municipal (no encontré ninguno verificable).
  - Las técnicas de los ganadores Sigma 2026.

---

## Fuentes

**3D y WebGPU**
- three.js, manual de WebGPURenderer: https://threejs.org/manual/en/webgpurenderer
- Estado de WebGPU (gpuweb, 28 may 2026): https://github.com/gpuweb/gpuweb/wiki/implementation-status
- web-features (datos de Baseline, paquete npm `web-features`): https://cdn.jsdelivr.net/npm/web-features/data.json · https://github.com/web-platform-dx/web-features
- model-viewer: https://modelviewer.dev/ · https://raw.githubusercontent.com/google/model-viewer/master/packages/model-viewer/README.md · código de carga: https://cdn.jsdelivr.net/npm/@google/model-viewer@4.3.1/lib/features/loading.js
- Spline, precios: https://spline.design/pricing
- Babylon.js 9.0: https://blogs.windows.com/blog/2026/03/26/announcing-babylon-js-9-0/
- glTF Transform CLI: https://gltf-transform.dev/cli
- MDN, buenas prácticas de WebGL: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices

**Scroll y animación**
- Licencia de GSAP: https://gsap.com/standard-license/
- ScrollTrigger: https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- Lenis: https://raw.githubusercontent.com/darkroomengineering/lenis/main/README.md
- Firefox, funciones experimentales: https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features
- scrollama: https://github.com/russellgoldenberg/scrollama

**Mapas**
- MapLibre GL JS, registro de cambios: https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/CHANGELOG.md
- Especificación de estilos de MapLibre: https://maplibre.org/maplibre-style-spec/layers/
- deck.gl, novedades: https://deck.gl/docs/whats-new
- OpenFreeMap: https://openfreemap.org/ · https://openfreemap.org/quick_start/
- IGN Argenmap: https://www.ign.gob.ar/AreaServicios/Argenmap/IntroduccionV2 · https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/ServiciosOGC/Leaflet
- Política de uso de teselas de OSM: https://operations.osmfoundation.org/policies/tiles/
- Protomaps: https://docs.protomaps.com/basemaps/downloads

**Rendimiento, accesibilidad y SEO**
- StatCounter Argentina, plataformas: https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet/argentina
- StatCounter Argentina, sistemas operativos móviles: https://gs.statcounter.com/os-market-share/mobile/argentina
- Core Web Vitals: https://web.dev/articles/vitals
- Google, JavaScript SEO: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- WCAG 2.2: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html · https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html · https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Ley 26.653 (W3C, políticas): https://www.w3.org/WAI/policies/argentina/

**Ejemplos**
- Awwwards, Sitios del Año: https://www.awwwards.com/inspiration_search/sites_of_the_year/
- Lando Norris: https://www.awwwards.com/sites/lando-norris
- Messenger: https://www.awwwards.com/sites/messenger
- Vitrina de GSAP: https://gsap.com/showcase/
- Lista secundaria de sitios premiados: https://www.hontran.dev/blog/best-award-winning-websites-2026
- Sigma Awards: https://sigmaawards.org/ · https://latamjournalismreview.org/news/data-journalism-projects-from-brazil-mexico-and-peru-win-at-2026-sigma-awards/

**Chatbot y búsqueda**
- NN/g, guías para chatbots: https://www.nngroup.com/articles/ai-chatbots-design-guidelines/
- NN/g, preguntas sugeridas: https://www.nngroup.com/articles/prompt-suggestions/
- NN/g, citas en chats con IA: https://www.nngroup.com/articles/explainable-ai/
- Anthropic, Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval
- API de Claude, citas: https://platform.claude.com/docs/en/build-with-claude/citations
- API de Claude, modelos: https://platform.claude.com/docs/en/models/overview
- MiniSearch: https://raw.githubusercontent.com/lucaong/minisearch/master/README.md
- Orama, idiomas: https://docs.orama.com/docs/orama-js/supported-languages
- Modelos de embeddings: https://huggingface.co/api/models/Xenova/multilingual-e5-small/tree/main/onnx · https://huggingface.co/api/models/onnx-community/embeddinggemma-300m-ONNX/tree/main/onnx
- Contrato de páginas de Claude, capacidad `sample` 0.2.75: tipos `sample.d.ts` del skill `artifact-capabilities` (interno de esta sesión)

**Higgsfield**
- Documentos leídos (workflow `website-builder-flow`, versión 2026-07-25): `SKILL.md`, `references/website-flow.md`, `scroll-scrub.md`, `wow-catalog.md`, `wow-maker.md`, `design-taste-frontend.md`, `reference-boards.md`, `asset-system.md`, `review-rubric.md`, `runtime-and-infra.md`, `seo.md`, `security.md`, `game-3d-animation.md`, `game-meshy-api.md`, `image-to-code.md`
- Modelos consultados con `models_explore`: `list` con tipo 3d, `get` de image_to_3d, seedance_2_0 y gpt_image_2
- Propiedad de lo generado: https://higgsfield.ai/creator-hub/help-center/account-and-privacy/who-owns-my-generations-and-can-i-use-them-commercially
- Términos de uso: https://higgsfield.ai/blog/terms-of-use-privacy-policy-update
- Precios (no se pudo leer): https://higgsfield.ai/pricing

**Versiones y CDN** (consultas de hoy)
- Registro npm: https://registry.npmjs.org/
- API de cdnjs: https://api.cdnjs.com/libraries/
- API de jsDelivr: https://data.jsdelivr.com/v1/packages/npm/
- Las URLs de la tabla C, verificadas una por una con HTTP 200.
