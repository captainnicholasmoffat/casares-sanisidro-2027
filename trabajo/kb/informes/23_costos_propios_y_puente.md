# Informe 23 · Costos con la opción óptima en calidad y precio, puente con los laboratorios de IA, espectáculos al aire libre, turnos médicos, y género y discapacidad

**Fecha:** 05/10/2026. Sólo investigación: no se tocó `doc/` ni `salida/`.

**Fuentes:**
- `01_raw/costos_propios/`, con seis subcarpetas:
  - `1_avatar`
  - `2_modelo_voz_fijos`
  - `3_canon_privados_y_cefa`
  - `4_seguridad_y_barrido`
  - `5_redes_desagues`
  - `6_plataforma_y_personas`
- `01_raw/puente_laboratorios/`
- `01_raw/espectaculos/`
- `01_raw/turnos/`
- `01_raw/genero_discapacidad/`

Cada carpeta tiene su `FUENTES.txt` (archivo, bytes, URL, fecha y qué es) y su `NO_SUBIDOS.txt`.

**Plata:**
- Va en pesos de diciembre de 2025, con el IPC del repositorio (`data/ipc_indec_mensual.csv`, dic-2025 = 10.121,3715). El último mes del IPC es julio de 2026, así que los precios posteriores se deflactan con julio.
- El dólar va a $1.520, como en el informe 22.
- **Ojo:** $1.520 es el dólar de octubre de 2026 y los pesos son de diciembre de 2025. Si también se deflacta el dólar, quedaría en unos $1.274, y todo lo que se calcula en dólares bajaría un 16%. Es una pregunta abierta para el cliente; acá se usa $1.520.

**Marcas:**
- [verificado]: leído en la fuente primaria.
- [probable]: prensa o fuente secundaria.
- [sin confirmar].
- [cálculo propio].
- [inferencia].
- Lo jurídico lleva además «necesita dictamen de un abogado».
- Lo que el Municipio comunica va «según el Municipio».
- «No lo encontré» no quiere decir que no exista.

**Nombres:**
- En este informe se nombran empresas y productos para poder verificar; el documento no los nombra.
- No se nombra a ninguna persona.

**Criterio, regla fija del programa:**
- Para cada herramienta se busca la opción óptima en calidad y precio: servicio pago, código abierto o propio.
- Lo que ya existe y está bien hecho no se fabrica.
- No se paga precio de lista donde hay volumen.
- Se recomienda la opción óptima, no la más barata.

---

## Respuestas en una línea

**A · Costos propios**
- **A1 · Profesor digital:** con la cara realista a precio de volumen, todo incluido cuesta US$26 a 32 por alumno por año con uso pleno ($2.039 a 2.486 M por año). El informe 22 daba $29.387 M con el avatar a 50 centavos por minuto. [cálculo propio]
- **A1 · Avatar:** a precio de volumen cuesta de 1 a 2 centavos por minuto, contra los 50 del informe 22; a precio de lista sería unas 8 veces más caro. Ningún servicio publica su calidad: antes de elegir hace falta una prueba a ciegas de un mes. [verificado los precios; inferencia la elección]
- **A1 · Modelo para menores:** gpt-6-luna, con los datos procesados en la UE, por US$0,57 por alumno por año. El plan B es Claude Haiku 4.5. Gemini queda afuera por sus términos sobre menores. [verificado; necesita dictamen de un abogado]
- **A1 · Canon de los colegios privados:**
  - el 63% de los alumnos de primaria y secundaria va a colegios privados, y casi la mitad de ellos a colegios sin aporte estatal [verificado];
  - la propuesta que no cobra de más es atar el canon al costo, de $0 a $6.840 por mes según el tramo [cálculo propio; decide el cliente].
- **A2 · Habilitaciones y analítica:** el Municipio ya compró las cámaras con IA, el sistema de video y 110 licencias de análisis de video [verificado]. La inversión baja de 1.200 M a entre 246 y 450 M, y el mantenimiento, de 264 M a entre 34 y 56 M por año. [cálculo propio]
- **A3 · Redes en los desagües:** con reja-canasto y la cuadrilla municipal, cuestan de 33 a 75 M por año, no 395 M. [cálculo propio]
- **A4 · Plataforma:**
  - lo que sirve a los vecinos cuesta 139,6 M por año, menos que los 193,2 M de «infraestructura y licencias»;
  - con las licencias del equipo, las asociaciones, los alumnos y el semillero llega a 268,7 M.
  - [cálculo propio]
- **A4 bis · Personas:** hacen falta 10 personas nuevas en la plataforma (336,7 M) y 8 en las áreas (202,0 M). [cálculo propio con los sueldos del cuadro 27]
- **A5 · Otros precios caros:**
  - licencia de las cámaras corporales, −3,8 M por año;
  - sensores de Perú mal leídos, −13,8 M una vez;
  - WhatsApp en el informe 17, hasta −47,4 M por año.
  - [verificado la regla; cálculo propio el monto]
- **A6 · CEFAyP:** sigue funcionando, ahora como CEFA, con dos sedes. No hay un número actualizado de chicos. [verificado]

**B · Puente con los laboratorios:** ningún laboratorio tiene un programa abierto que sirva a un técnico argentino que no viva en EE. UU., el Reino Unido o Canadá, salvo Cohere Labs Scholars (a distancia, hoy cerrado) y Google Summer of Code [verificado]. La vía legal más realista a EE. UU. es la visa J-1 de pasante. [verificado; necesita dictamen de un abogado]

**C · Espectáculos:** San Isidro no tiene un régimen de permisos para artistas callejeros. Sólo existe la Ordenanza 9120/2019, que reconoce la gorra, y un proyecto de registro gratuito está en comisión desde 2025 [verificado]. Las reglas que se repiten afuera son puntos señalizados, 100 m entre artistas, turnos de 1 hora y de 65 a 72 dB.

**D · Turnos médicos:** San Isidro no publica sus faltazos. El recordatorio con respuesta («confirmo / cancelo») baja los faltazos de 21% a 15% [verificado]. La IA rindió sólo cuando ordenó a quién llamar primero, y en un hospital no rindió nada. [verificado]

**E · Género y discapacidad:**
- Hay patrocinio jurídico gratuito cerca, pero no es municipal: CASI, Defensa Oficial y la UBA [verificado].
- San Isidro no tiene hogar propio; pide vacantes a la Red Provincial [verificado].
- La junta del CUD funciona en el Hospital Central [verificado].

---

## A · Costos propios

### A1 · Profesor digital

**Lo decidido por el cliente:**
- Cara realista con video.
- Seis centros municipales y además en la casa, para los 50.833 alumnos de primaria y secundaria.
- Gratis para los de escuelas estatales y del apoyo escolar.
- Los de colegios privados pagan un canon según la cuota de su colegio.
- Los colegios privados pagan otro canon para que sus docentes reciban los informes.
- Primero, una prueba de 6 meses.

**El documento hoy (después del commit 888e8b1):**
- `doc/content_c.py` L2243 a L2280: el profesor digital, puntos 1 a 8. No tiene costo.
- L2260, punto 4, «Quién paga»: «los de cuota baja… pagan poco o nada, y los de cuota alta, más».
- El Excel no tiene ninguna línea del profesor digital. [verificado]

**Uso supuesto, el del informe 22:** 2 sesiones de 20 minutos por semana, 36 semanas. Son 1.440 minutos de sesión por alumno por año, 576 de ellos con el tutor hablando.

#### Avatar (cara realista con video)

**Precios publicados por minuto de sesión** [verificado; cálculo propio el costo por alumno]:

| Servicio | Centavos de US$ por minuto | US$ por alumno por año (1.440 min) | Lo importante |
|---|---|---|---|
| LiveAvatar LITE (HeyGen), plan Business | 7,92 | 114 | Cobra el minuto entero de sesión, no sólo cuando habla. Menos de 300 ms. «No pensado para menores de 18»; puede entrenar con lo que recibe salvo que se lo excluya |
| LiveAvatar Enterprise | «desde 1» | 14,4 | No dice a qué volumen |
| Spatius, plan anual | 0,60 | 8,6 | Hasta 40 sesiones a la vez; con más, contrato Enterprise. Datos y región sin revisar |
| Simli | alrededor de 1 | 14,4 | [probable] |
| Beyond Presence | 9,85 (anuncio a escala: 3,38) | 142 | — |
| Anam Enterprise | 4 | 57,6 | Datos en la UE; retención cero sólo en Enterprise |
| Alibaba China, 3D | 8,95 | 129 | Exige identidad china; los datos quedan en China. **Afuera** |
| Tavus / D-ID / Azure | 32 a 50 | 457 a 720 | **Afuera** por precio |

**Código abierto en placas** [verificado las licencias]:
- **MuseTalk 1.5** (MIT) sirve. Falta revisar la licencia de los pesos de face-alignment (necesita dictamen de un abogado).
- **SoulX-FlashHead Lite** tiene un riesgo escondido: usa el VAE de LTX-Video, que es «sólo investigación» o pide licencia paga. Necesita dictamen de un abogado.
- **Ditto** queda afuera por los detectores de InsightFace.
- **Placas GeForce:** el driver «no está licenciado para despliegue en centro de datos». Si eso le aplica al Municipio, necesita dictamen de un abogado.
- **MuseTalk sobre una L40S alquilada** (RunPod) cuesta unos US$10 por alumno por año. Pero los datos van a EE. UU., que no es país «adecuado» para la Ley 25.326 (Disposición 60/2016). Necesita dictamen de un abogado. [cálculo propio]
- **Placas propias:** con pocas horas de uso por día salen más caras que alquilar. Sólo convienen si se comparten con otras cargas de la inteligencia artificial del Municipio. [cálculo propio]

**Calidad:**
- Ningún servicio pago publica métricas.
- Los papers abiertos usan protocolos distintos y no prueban en castellano. [verificado]
- Por eso hace falta una **prueba a ciegas de un mes**, antes de pagar nada:
  - 30 frases rioplatenses: voseo, labiales, sheísmo y matemática hablada;
  - una sesión de 20 minutos seguidos;
  - demora de punta a punta medida con un teléfono a 240 cuadros por segundo;
  - un panel de 24 adultos y, después, 12 alumnos con permiso de sus familias;
  - peso en la decisión: calidad 50%, precio 30%, datos y legal 20%.
  - El protocolo completo está en `01_raw/costos_propios/1_avatar/` y en el reporte de origen. [inferencia]
- **Diseño que protege a los chicos:** el avatar recibe sólo la voz sintética del tutor, nunca la voz ni la cara del chico. [inferencia]

**Recomendación** [inferencia sobre cálculo propio]:
- **Prueba de 6 meses:** LiveAvatar LITE como referencia, unos US$12.600, más un brazo paralelo con el finalista barato, unos US$1.000 a 1.500.
- **Los 6 centros:** el ganador; si es LiveAvatar, negociar Enterprise a 3 centavos o menos.
- **En la casa:** licitar «sólo avatar» por minuto, con un techo de 1 a 2 centavos y los umbrales de calidad de la prueba. El plan B es MuseTalk en placas alquiladas.
- **Nunca a precio de lista:** con uso pleno en la casa serían US$6,6 M por año.
- **Para el 9,1% sin internet en la casa:** una cara dibujada en el propio equipo (LiteAvatar corre sin placa).

#### Modelo de lenguaje, voz y reconocimiento de voz

**Precio:**
- Con el uso del informe 22, todos los modelos chicos cuestan menos de US$2 por alumno por año. [cálculo propio]
- Por eso no decide el precio: deciden los términos para menores y dónde quedan los datos.

| Pieza | Opción óptima | Por alumno por año | Por qué | Marca |
|---|---|---|---|---|
| Modelo para el tutor | gpt-6-luna (OpenAI), datos procesados en la UE | US$0,57 | No entrena con los datos. Admite menores con salvaguardas; para menores de 13 exige «retención cero», que OpenAI tiene que aprobar | [verificado]; necesita dictamen de un abogado |
| Plan B | Claude Haiku 4.5 (Anthropic) | US$5,19 | No entrena; admite menores con salvaguardas | [verificado] |
| Afuera para menores | Gemini (Google) | — | Sus términos prohíben servicios dirigidos a menores de 18 o que puedan usar | [verificado] |
| No para menores | DeepSeek V4.1 Flash y GLM-5.3-Flash | US$0,65 y 0,76 | La API de DeepSeek guarda los datos en China y «no apunta a chicos»; Z.ai dice «no dirigido a menores de 18». Sirven para la plataforma de los adultos (A4) | [verificado] |
| Voz | Azure Neural, voces es-AR (Elena y Tomás) | US$7,78 a lista; US$3,89 a 5,05 con compromiso | Es el único servicio grande con voces argentinas | [verificado] |
| Reconocimiento de voz | Azure, tiempo real | US$7,20 a lista; US$3,60 a 5,76 con compromiso | Menor error en castellano del ranking abierto (1,75% en FLEURS), medido con adultos | [verificado] |
| Casi igual y más barato | ElevenLabs Scribe v2 Realtime | US$2,81 | 1,85% de error; conviene probarlo en el piloto con voces de chicos | [verificado] |

**Dónde quedan los datos:**
- La aplicación, la base de datos y los informes pueden quedar en Buenos Aires: Amazon tiene una Local Zone con precios publicados [verificado].
- El modelo y la voz van como servicios con contrato de no entrenamiento, retención cero y las cláusulas de la Disposición 60-E/2016. [inferencia; necesita dictamen de un abogado]

**Servidor propio para el modelo:** no conviene. Alquilar 8 H100 en San Pablo cuesta US$99.865 por año, contra US$29.005 del servicio con uso pleno. [cálculo propio]

#### Lo fijo

| Concepto | Opción óptima | Marca |
|---|---|---|
| Equipo | 6 a 8 personas si se compran los servicios, no 11 | [inferencia] |
| Computadoras | El celular de la familia alcanza para texto y voz. Sólo el 3,84% no tiene ni computadora ni celular con internet. Una netbook escolar cuesta unos US$217 (compra por UNOPS de 2026) | [verificado] el Censo; [probable] el precio |
| Internet | Un pase prepago de 50 MB por día cuesta $585 y alcanza para una sesión de voz: $35.301 por alumno por año, sólo para el 3,13% sin conexión. La tarifa social fue derogada | [verificado] el precio; [probable] la derogación |
| Capacitación | Cursos gratuitos de IA para docentes en Educ.ar 2026, en lugar de 20 horas pagas | [verificado] |

#### Los cuatro escenarios, todo incluido

Las dos primeras columnas salen de dos reportes separados: «sin avatar» del de modelo, voz y fijos; «avatar» del de avatar. La tercera es la suma [cálculo propio].

| Escenario | Sin avatar (modelo, voz, reconocimiento y fijos) | Avatar a precio de volumen | Total | Por alumno |
|---|---|---|---|---|
| **a) Prueba de 6 meses en 2 centros, 200 chicos** | US$64.432 | US$13.570 a 14.070 | **US$78.000 a 78.500 ($118,6 a 119,3 M)** | US$390 en 6 meses |
| **b) Los 6 centros, 600 chicos por año** | US$179.865 | US$5.000 a 26.000 | **US$184.865 a 205.865 ($281,0 a 312,9 M)** | US$308 a 343 |
| **c) En casa, uso realista (15%)** | US$367.724 | US$65.600 a 109.799 | **US$433.324 a 477.523 ($658,7 a 725,8 M)** | US$8,5 a 9,4 por inscripto; US$57 a 63 por alumno que lo usa |
| **d) En casa, uso pleno (50.833)** | US$903.729 | US$437.500 a 731.995 | **US$1.341.229 a 1.635.724 ($2.038,7 a 2.486,3 M)** | **US$26,4 a 32,2** |

- **Qué incluye «sin avatar»:** gpt-6-luna con datos en la UE, voz y reconocimiento de Azure (a precio de lista en a y b, con compromiso en c y d), equipo, netbooks para el 3,84%, datos para el 3,13%, capacitación y servidores en Buenos Aires.
- **Con los sueldos del cuadro 27:** el reporte de personas (A4 bis) arma el equipo del tutor con 9 personas por 269,7 M, en lugar de 482,1 M. Con eso, el (d) baja a $1.826 a 2.274 M (US$23,6 a 29,4 por alumno). [cálculo propio]
- **Si se informa al docente** (versión B), capacitar a 4.726 docentes de escuela 4 horas cada uno cuesta $369 M una vez. [cálculo propio]
- **IVA:** un municipio paga IVA como consumidor final. Los servicios digitales del exterior podrían sumar 21%. Necesita dictamen de un abogado. [verificado el texto]
- **Contra el informe 22:**
  - informe 22: $29.387 M por año con el avatar a 50 centavos por minuto, para los 50.833 alumnos (cobertura B);
  - ahora: $2.039 a 2.486 M;
  - diferencia: **−26.901 a −27.348 M por año**. [cálculo propio]
- **Por qué baja tanto:**
  - avatar por volumen, de 1 a 2 centavos por minuto, en lugar de 50;
  - cursos gratuitos;
  - netbooks para el 3,8% y no para el 21,9%;
  - pases de datos en lugar de internet fijo;
  - menos personas.

#### Canon de los colegios privados

**Topes de cuota de la Provincia para los colegios con aporte** [verificado]:
- Para agosto de 2026, con 100% de aporte: $37.150 en inicial y primaria y $40.960 en secundaria. Para septiembre, $38.070 y $41.980.
- Los fija la providencia PV-2026-26081548-GDEBA-DLHRYAEPDGCYE (24/07/2026), de la Dirección de Liquidaciones de la DGCyE, sobre la base de la Res. DGCyE 34/2017.
- La copia es la que circuló por la Jefatura Regional; no la encontré en abc.gob.ar ni en normas.gba.gob.ar.
- La cifra de la prensa coincide.

| Septiembre 2026, por mes | 100% | 80% | 70% | 60% | 50% | 40% |
|---|---|---|---|---|---|---|
| Inicial y primaria | 38.070 | 70.260 | 89.880 | 134.600 | 156.620 | 172.180 |
| Secundaria | 41.980 | 79.550 | 110.360 | 162.260 | 179.010 | 223.740 |

- En pesos de diciembre de 2025, el tramo de 100% en primaria son $31.907. [cálculo propio]
- **Colegios sin aporte:** tienen cuota libre y la informan a la Provincia «a modo informativo» (Res. 34/17, art. 19). La Nación derogó el Decreto 2417/93 con el Decreto 787/2025. [verificado]
- **Cuotas sin aporte en San Isidro:** sólo 3 colegios publican la suya, de $1,16 a $1,87 millones por mes. No hay dato público de las cuotas bajas o medias. [verificado]

**Alumnos de colegios privados de San Isidro por tramo de aporte**

Padrón oficial de establecimientos de la Provincia, corte al 28/09/2026, con la matrícula del Relevamiento Inicial 2026. Recalculé los totales sobre el CSV y coinciden con los de la DGCyE. [verificado]

| Tramo de aporte | Primaria | Secundaria (con técnica) | Total | % |
|---|---|---|---|---|
| 100% | 1.905 | 2.130 | 4.035 | 12,9% |
| 80% | 1.233 | 5.189 | 6.422 | 20,6% |
| 70% | 1.252 | 645 | 1.897 | 6,1% |
| 60% | 2.689 | 1.005 | 3.694 | 11,8% |
| 50% | 0 | 0 | 0 | 0% |
| 40% | 334 | 0 | 334 | 1,1% |
| Sin aporte | 7.070 | 7.782 | 14.852 | 47,6% |
| **Total privados** | 14.483 | 16.751 | **31.234** | 100% |

- Los privados son unos 32.100 de los 50.833 alumnos de 2025: el **63%**. [cálculo propio]
- Secciones por tramo, para el canon de cada colegio:
  - 100%: 148;
  - 80%: 237;
  - 70%: 80;
  - 60%: 144;
  - 40%: 12;
  - sin aporte: 655.

**Dos formas de armar el canon** [cálculo propio; es propuesta, decide el cliente]:

| Tramo | Quiénes | Opción 1: monto fijo por alumno por mes (10 meses) | Opción 2: atado al costo (US$30 por alumno por año) | Canon del colegio por sección por año (las dos opciones) |
|---|---|---|---|---|
| A | 100% de aporte | $0 | $0 (0%) | $0 |
| B | 80% y 70% | $1.000 | $912 (20%) | $50.000 |
| C | 60%, 50% y 40% | $2.500 | $2.280 (50%) | $120.000 |
| D | Sin aporte, cuota de hasta $600.000 | $10.000 | $4.560 (100%) | $300.000 |
| E | Sin aporte, cuota de más de $600.000 | $25.000 | $6.840 (150%) | $600.000 |

**Cuánto cubre cada opción:**
- **Opción 1:** cubre entre 84% y 191% del costo total con US$30 por alumno. Puede cobrar más de lo que cuesta. Si el canon se arma como tasa, tiene que guardar relación con el costo del servicio: necesita dictamen de un abogado.
- **Opción 2:** cubre entre 47% y 71% del costo total. Depende de cuántos colegios sin aporte caigan en E.
- Con la mitad de los colegios adheridos, la cobertura se reduce a la mitad.

**Recomendación:**
- La Opción 2: sigue al costo real, que en (d) da US$26 a 32 por alumno. [inferencia]
- El corte de $600.000 entre D y E se parece al umbral de 0% de descuento de Ceibal: unos $562.000 por mes.

**Reglas que importan** [verificado; necesita dictamen de un abogado]:
- Los colegios con aporte pueden cobrar «equipamiento didáctico… medios… tecnológicos» hasta el 10% del arancel (RESFC 2381/18, art. 3). Es la vía si el canon se cobra en el recibo del colegio.
- «En ningún caso se exigirá al alumno menor de edad pago alguno»: el canon se cobra a los padres.
- Los colegios con aporte becan al 100% entre el 7% y el 10% de su matrícula. Conviene eximir a esos becados.

**Precedentes** [verificado]:
- **Ceibal (Uruguay):** cobra a los colegios privados con un descuento según la cuota anual promedio. Va del 100% de descuento con cuota cero al 0% desde UYU 149.273 por año. Es el más parecido. No ubiqué la resolución de su directorio.
- **Chile, prueba de acceso a la universidad (PAES):** gratis para colegios municipales y subvencionados; CLP 46.500 para los particulares pagados.
- **Provincia de Buenos Aires, boleto educativo:** sólo para escuelas estatales y privadas con aporte.
- **Ciudad de Buenos Aires, Sarmiento BA:** sólo estatales y privadas con cuota cero.

### A2 · Habilitaciones y analítica de seguridad

**Hoy** [verificado]:
- **Excel, Supuestos:**
  - fila 54: 1.200 M una vez, «ESTIMACIÓN PROPIA, NO VERIFICADA»;
  - fila 57: 22% de mantenimiento, con la nota «10.450 USD sobre una licencia de 47.500 USD (lista de precios de Oracle, 2026)»;
  - fila 233: 80 cámaras corporales, 168,7 M;
  - fila 234: licencia de monitoreo, 3,8 M por año.
- **Documento:**
  - `content_b.py` L276 (cuadro 14), L293 y L299;
  - L342 (cuadro 15, 6.863 M);
  - `content_c.py` L2425 a L2427 (5.9);
  - `content_o.py` L486.
- **Lo identificado de los 1.200 M:** sólo las cámaras corporales. Los otros 1.031,3 M no tienen desglose.
- **El 22%:** sale del soporte de una base de datos Oracle y se aplica también a cámaras, que son equipo.

**Lo que el Municipio ya compró y opera** [verificado; lo que comunica, según el Municipio]:
- **2.650 cámaras** (LP 76/2024, ampliada por el Decreto 416/2026). Las 2.379 nuevas, Hanwha, traen en la propia cámara:
  - detección de persona, cara, vehículo y patente;
  - merodeo e intrusión;
  - sonidos de grito, disparo, explosión y vidrio que se rompe.
- **Sistema de video:** Milestone XProtect, con 2.650 licencias (LP 25/2025).
- **110 licencias de IA de video con 3 años de soporte** (LP 45/2025):
  - adjudicadas por $188.179.200 a EXANET S.A. (Decreto 1372/2025);
  - una ampliación de 10 por $18.817.920 (Decreto 682/2026);
  - reglas en vivo (persona caída, agrupación, objeto abandonado, contramano) y búsqueda forense;
  - el pliego dice «No se debería requerir una GPU».
- **Despacho con GPS de los móviles** (LP 9/2024).

**Opción óptima** [cálculo propio e inferencia]:
- Usar lo que ya hay.
- Sumar, si una auditoría lo justifica, hasta 40 licencias a precio de contrato: 77,4 M. Ampliar en 2028 un contrato de 2025 necesita dictamen de un abogado.
- Sumar las 80 cámaras corporales con transmisión por protocolo abierto: 168,7 M. Llave en mano, hasta 336 a 372 M.

| | Hoy | Óptima | Diferencia |
|---|---|---|---|
| Inversión | 1.200 M | 246 M de piso, más accesorios sin precio; 450 M de techo | **−750 a −954 M una vez** |
| Por año | 264 M | 34 a 56 M (reposición de cámaras y baterías), más los datos móviles, que no tienen precio | **−208 a −230 M por año** |
| Cuadro 15 y Supuestos fila 176 | 6.863 M, el 28% | 6.632 a 6.655 M, el 26,8% a 26,9% | baja 1 punto |

- **Afuera:** YOLO de Ultralytics es AGPL-3.0, con la misma regla con la que el programa descartó Decidim.
- **Afuera:** la nube cuesta 78,8 M por cámara y por año si analiza todo el día.
- **Hikvision, Dahua y Hytera:** las compras federales de EE. UU. las prohíben (FAR 52.204-25). En la Argentina no encontré prohibición.

### A3 · Redes en los desagües de la costa

**Hoy** [verificado]:
- **Documento:**
  - `content_c.py` L1334: «Redes y barreras en las bocas de los desagües, vaciadas todos los días»;
  - L1363 y L1364: lo que funciona todo el año suma 790 a 1.140 M.
- **Informe 11:**
  - L87 y L406: 39,5 M por red y 395 M las diez;
  - L420: el paquete «Completo».
- **El origen es Marin County (EE. UU.):** tres limpiezas por año con camión grúa a US$5.000 el medio día, US$27.300 por red.
- **El Excel** no tiene una línea de redes.

**Opción óptima** [cálculo propio e inferencia]:
- Una reja-canasto de acero galvanizado en la boca, vaciada a mano por la cuadrilla de la costa.
- La barrera flotante corta va sólo donde la boca descarga en agua abierta.
- No encontré precio argentino de una bolsa de red.

**Precios locales** [verificado]:
- Reja perimetral provista y colocada: $223.955 por m². Reja tipo Techno: $373.588 por m². Jornal de herrería: $294.705. Son de San Isidro, LP 62/2024, Decreto 1077/2025.
- Camión volcador con chofer: $33.114 por hora con IVA (Decreto 1238/2024).
- Escala de los obreros municipales: Decreto 782/2026.
- Barrera flotante de OSSE Mar del Plata: $36.960.000 (Res. 609/2026), largo no publicado.

| | Hoy | Óptima | Diferencia |
|---|---|---|---|
| Por boca, por año | 39,5 M | 3,3 a 7,5 M, vaciando 104 veces por año (cada semana y después de cada lluvia) | −32 a −36 M |
| Diez bocas, por año | 395 M | 33 a 75 M | **−320 a −362 M por año** |
| Si se vacían todos los días hábiles, como dice el texto | 395 M | 75 a 161 M | −234 a −320 M |
| Instalación, una vez | No se presupuesta | 52 a 85 M las diez, sin el proyecto hidráulico | +52 a 85 M |

- **Efecto en el 5.5:** el total de 790 a 1.140 M bajaría a unos 430 a 820 M. Es una inferencia sobre cómo se armó ese total, que no está escrito.
- **Lo que pesa es el camión, no el sueldo:**
  - un obrero cuesta unos $4.300 a $4.900 por hora;
  - el camión con chofer, unos $48.700.
- **Precedente propio:** en 2014-2017 San Isidro contrató «redes» y limpieza del «sobrenadante» en el desagüe de Perú (Decretos 4017/2014, 1802/2015 y 1014/2017). No se sabe si siguen. [verificado]
- **La Plata, arroyo El Gato:** hay una nota de prensa sobre una causa judicial: [Infobae, 11/03/2026](https://www.infobae.com/politica/2026/03/11/la-justicia-embargo-por-mas-de-157000-millones-al-gobierno-bonaerense-por-un-caso-de-contaminacion-aberrante/).

### A4 · Plataforma: «infraestructura y licencias» del cuadro 27

**Hoy** [verificado]:
- `content_c.py` L774: 193,2 M.
- Supuestos E161.
- Son el 18% de los sueldos sin cargas (0,18 × 1.073,6 M): una regla, no un precio.

**Uso esperado** [cálculo propio]:
- Los precedentes van de 0,4 conversaciones por habitante por año (Córdoba) a 10,4 (Boti, Ciudad de Buenos Aires) [verificado / probable].
- El medio, 3 por habitante, da unas 2,2 millones de preguntas por año.

**Modelo para los vecinos adultos** [verificado el índice y los precios; inferencia la elección]:
- **GLM-5.3-Flash** (Z.ai, licencia MIT): índice 41,8 y 28% de respuestas inventadas.
- DeepSeek V4.1 Flash: índice 39,5 y 96% de respuestas inventadas. Queda para las fotos y como respaldo.
- Cuesta unos US$0,005 por pregunta.

| Rubro, por año | Bajo | Medio | Alto |
|---|---|---|---|
| Lo que sirve a los vecinos: modelo, audios, WhatsApp, servidores en la UE, Cloudflare e imprevistos | 80,9 M | **139,6 M** | 274,4 M |
| Más las licencias de IA para programar del equipo (49 personas) | 148,4 M | 207,1 M | 341,9 M |
| Más los espacios de 70 asociaciones, los alumnos y el semillero | 210,0 M | **268,7 M** | 403,5 M |
| Contra 193,2 M | +16,8 M | +75,5 M | +210,3 M |

- **Lo que más pesa no es la IA:** son los avisos por WhatsApp (49,9 M en el escenario medio) y las licencias del equipo (67,5 M). [cálculo propio]
- **Responder dentro de las 24 horas de que escribió el vecino es gratis;** un aviso fuera de esa ventana cuesta US$0,026 [verificado].
- **Si los avisos van por la app y el correo:** el total medio baja a unos 211 M. [cálculo propio]
- **Herramientas de las asociaciones** [verificado los rankings y precios]:
  - textos con GLM-5.3-Flash;
  - imágenes y renders con MAI-Image-2.6, a US$0,039 por imagen, en «vista previa»;
  - piezas finales con GPT Image 2.5, a US$0,21, con un cupo chico;
  - análisis de datos con GLM-5.3 en un entorno propio.
- **Cupo por espacio:** usado entero cuesta US$40 por mes.
- **Cuántas asociaciones hay:** no hay un número oficial.
  - El registro nacional tiene 895 entidades sin fines de lucro con domicilio en el partido; 34 se llaman vecinales o de fomento [cálculo propio].
  - Según el Municipio, se inscribieron 160 en su registro hasta julio de 2025 [probable, prensa].
- **Abuso:** se controla sin leer el contenido [verificado los precedentes]:
  - identidad por WhatsApp y Mi Argentina;
  - topes por usuario y por minuto;
  - Turnstile (gratis);
  - tope de largo por pregunta.
- **Sin límites:** un solo robot a 1 pregunta por segundo costaría 237 M por año. [cálculo propio]
- **Dónde quedan los datos:** ni China ni EE. UU. son países «adecuados». Hace falta un proveedor en la UE, el Reino Unido o Uruguay, o las cláusulas de la AAIP. Necesita dictamen de un abogado.

### A4 bis · Personas

Con los sueldos que salen del cuadro 27 [cálculo propio]:
- senior, 53,10 M por año;
- semi-senior, 37,96 M;
- junior, 23,44 M;
- pasante, 3,17 M.

| Tarea | ¿Entra en lo que ya existe? | Gente nueva | Costo por año |
|---|---|---|---|
| Profesor digital | En parte: operación, seguridad y diseño se comparten | 1 Sr, 2 SSr y 2 Jr en la plataforma; 4 docentes revisores en Educación | 175,9 + 93,8 = **269,7 M** |
| Prueba sellada (informe 21) | Sí, en Servicios | 1 SSr de firma digital y cadena de custodia | 38,0 M |
| Mapa del ruido | Sí, entero | 0 | 0 |
| Multas: la IA aliada del vecino | Sí, en Servicios | 1 Jr | 23,4 M |
| Multas: operación pública | No: es Tránsito o Juzgado de Faltas | 1 SSr y 3 Jr que validan unas 244.000 actas por año | 108,3 M |
| Analítica de seguridad | Conviene comprarla, no hacerla (A2) | 1 SSr que audite, opcional | 38,0 M |
| Puente con los laboratorios | No | 1 SSr de vinculación, sin viajes ni becas | 38,0 M |
| La IA que escucha a los vecinos | En parte | 1 SSr y 1 Jr | 61,4 M |

**Total nuevo:**
- 10 personas en la plataforma por **336,7 M**;
- 8 en las áreas por **202,0 M**;
- 18,2 M de licencias para las 10 nuevas de la plataforma.

**Con eso:**
- la plataforma pasa de 49 a 59 personas;
- el equipo, de 1.285,1 M a 1.621,8 M.

### A5 · Barrido de otros precios de lista o de EE. UU.

| # | Dónde | Hoy | Opción mejor | Diferencia | Marca |
|---|---|---|---|---|---|
| 1 | Supuestos fila 57; `content_b.py` L276 y L299; `content_c.py` L2425; Programas fila 13 | 264 M por año (22% de Oracle) | Lo de A2 | −208 a −230 M por año | [verificado] |
| 2 | Supuestos fila 234; `content_b.py` L293 | 3,8 M por año de licencia de las cámaras corporales, «lista de proveedor», sin nombre | MediaMTX (MIT) y el equipo de transmisión del cuadro 27, ya pagado. La licitación debe pedir cámaras con protocolo abierto | −3,8 M por año (dentro de A2) | [verificado] la licencia |
| 3 | `content_c.py` L1328; Supuestos E238 («diagnóstico de Perú 22-36 M») | «veinte sensores de 500 dólares» | El informe 16 dice unos US$25 por sensor: 20 sensores cuestan unos US$500 en total | −13,8 M una vez | [verificado] la lectura; [cálculo propio] el monto |
| 4 | `content_f.py` L30; Supuestos E238 («muestras 42-75 M») | Precio de lista de un laboratorio privado | Convenio con los laboratorios de la Autoridad del Agua y de ABSA | Sin precio | [sin confirmar] |
| 5 | Informe 17, L339 y L340 (no está en el documento ni en el Excel) | US$2.600 por mes en WhatsApp | Los mensajes dentro de las 24 horas son gratis | Hasta −47,4 M por año | [verificado] la regla |
| 6 | Informe 14, L306 a L310 (no está en el documento) | Imagen satelital a precio de lista, US$2.000 a 2.550 | Ortofotos de ARBA o del Municipio, si existen | Hasta −3,9 M una vez | [sin confirmar] |

**Además:**
- El 10% de «auditoría externa» del cuadro 27 (107,3 M) tampoco tiene fuente. [verificado]
- El Municipio ya tiene licencias Oracle Database Standard Edition (Concurso de Precios 66/2025). [verificado]

### A6 · CEFAyP, hoy CEFA

- **Nombre:** desde 2018 se llama Centro Educativo Facilitador de Aprendizajes (CEFA). [verificado]
- **Sigue funcionando** [verificado]:
  - el Presupuesto 2026 (Programa 36) habla de «dos sedes»;
  - según el Municipio, atiende a niños de 4 a 12 años, de 8 a 17 horas, en Beccar (Tomkinson 2130) y en Bajo Boulogne (Junín y Comodoro Rivadavia).
- **Cuántos chicos:** no hay dato de 2024 a 2026. La última cifra publicada es «más de 300» (2017).
- **Apoyo escolar municipal:** según el Municipio, «un centenar» de alumnos en 5 espacios. [verificado, página sin fecha]
- **Para el profesor digital:** son los lugares naturales de la prueba de 6 meses. [inferencia]

---

## B · Puente con los laboratorios de IA

- **B1 · Programas** [verificado]:
  - casi todos piden estar cursando grado o doctorado, o tener permiso de trabajo en EE. UU., el Reino Unido o Canadá;
  - sirven: Cohere Labs Scholars (a distancia y pago; reabre en el otoño boreal de 2026) y Google Summer of Code (a distancia; US$750 a 3.000 para la Argentina).
- **B2 · Acuerdos de los laboratorios** [verificado]:
  - son con gobiernos nacionales: Anthropic con Islandia, Ruanda y el Reino Unido; Google DeepMind con cinco países;
  - ninguno es con un municipio ni con una universidad pública latinoamericana;
  - el único que habla de mover personas es el de Google DeepMind con Corea.
- **B3 · Qué funcionó** [verificado / probable]:
  - el puente que termina en un empleo o que incluye escuela;
  - el modelo a copiar es Mistral–Corea: 6 meses en París o Londres con visa y después un puesto en Seúl.
- **B4 · Visas** [verificado; necesita dictamen de un abogado]:
  - **H-1B:** casi imposible sin título.
  - **La tasa de 100.000 dólares:** hoy no se cobra, porque dos tribunales anularon las políticas que la aplican, pero puede volver.
  - **J-1:** como pasante, dentro de los 12 meses de recibido, o como *trainee*.
  - **Unión Europea:** prácticas por la Directiva 2016/801, o Tarjeta Azul con 3 años de experiencia.
  - **Alemania:** admite 2 años de experiencia en informática.
- **B5 · Inglés** [verificado]:
  - piden de IELTS 4,5 (Australia) a B2 (Reino Unido);
  - la UNSO no tiene hoy una tecnicatura de IA, y sólo su tecnicatura en Videojuegos tiene «Inglés técnico».
- **B6 · Quién firma** [verificado; necesita dictamen de un abogado]:
  - en la UNSO, el Rector *ad referéndum* del Consejo Superior;
  - en el Municipio, el Intendente, con autorización del Concejo (LOM, art. 41) y «fijando a las partes la jurisdicción provincial» (art. 108 inc. 14), lo que choca con las cláusulas habituales de estas empresas [inferencia].
- **Persona de vinculación:** 1 SSr, 38,0 M por año (A4 bis). [cálculo propio]

---

## C · Espectáculos al aire libre

- **C1 · Qué rige hoy** [verificado]:
  - la Ordenanza 9120/2019 declara de interés cultural el arte callejero y reconoce la gorra, pero no crea permiso ni reglas, y no figura en el digesto en línea;
  - el proyecto de registro gratuito (Expte. 527-HCD-2025) está en comisión desde el 03/09/2025.
- **Lo que se aplica por la vía general** [verificado]:
  - permiso y tasa de $246 por m² y por día (Impositiva 2026, art. 17 d.1);
  - el Código Contravencional (Ord. 5182, arts. 81, 123, 137 y 145);
  - la Ord. 7198 para concurrencias masivas.
  - Si eso alcanza a un artista a la gorra, necesita dictamen de un abogado.
- **C2 · Antecedentes:** Rosario, Barcelona, Córdoba (España), Melbourne, Westminster y Sydney traen números claros. La Ciudad de Buenos Aires y Mar del Plata tienen registro gratis.
- **C3 · Qué hace el Municipio en la costa** [verificado; según el Municipio]:
  - casi todo es los fines de semana y con artistas que elige el Municipio: DJ Sunset (5 domingos), Nochecitas en el río (2 viernes);
  - hubo un solo show en día hábil en la costa en 2026;
  - no publica cuánta gente fue.
- **C4 · Propuesta** [inferencia; necesita dictamen de un abogado]:
  - **Por decreto:** un piloto de lunes a jueves en la costa con puntos señalizados, turnos de 1 hora, 100 m entre puntos con sonido, acústico o amplificación chica a batería, y zonas tranquilas (Ribera Norte, Bosque Alegre, frentes de vivienda).
  - **Por ordenanza:** el registro gratuito, la exención de la tasa, la excepción contravencional para los registrados y la prohibición de secuestrar instrumentos.
  - **La inteligencia artificial del Municipio** publica puntos y turnos, toma reservas y deriva quejas.

---

## D · Turnos médicos

- **D1 · Faltazos:** San Isidro no publica su cifra.
  - Hospitales municipales bonaerenses: 15% a 17% [probable, prensa].
  - Hospital Italiano (privado): 28% [verificado].
  - Chile, sistema público: 19% a 20% [verificado].
- **D2 · Recordatorios** [verificado]:
  - el mensaje baja los faltazos de 21% a 15% (BMJ Open 2016, 21 ensayos);
  - reasignar el turno liberado funciona sólo si alguien o algo lo vuelve a ocupar: en Inglaterra se reocuparon 20 de 35.
- **D3 · IA** [verificado]:
  - rindió en hospitales públicos sólo cuando ordenó a quién llamar primero: Chile, de 21% a 10,7%; Badalona, −39% a −51%; Singapur, de 19,3% a 15,9%;
  - en Zúrich no rindió nada;
  - el sobreturno decidido por IA tiene efecto incierto y puede perjudicar a los grupos con más faltazos.
- **Para San Isidro** [inferencia]:
  - hoy los turnos se dan sólo por teléfono o en persona, sin cancelación por mensaje (informe 02);
  - el primer paso es el recordatorio con respuesta y alguien que reasigne;
  - después, la inteligencia artificial del Municipio puede ordenar a quién llamar, midiendo antes y después.
- **Costo de los recordatorios:** unos 4 M por cada 100.000 turnos, del presupuesto de salud (A4). [cálculo propio]

---

## E · Género y discapacidad

- **E1 · Patrocinio jurídico gratuito:** existe cerca, pero no es municipal [verificado; necesita dictamen de un abogado]:
  - Consultorio Jurídico Gratuito del Colegio de Abogados de San Isidro;
  - Defensa Oficial del Fuero de Familia;
  - comisiones del Práctico de la UBA.
- **E2 · Refugios:** San Isidro no tiene hogar propio [verificado].
  - En 2021-22 no pidió fondos provinciales para hogares.
  - El equipo municipal puede pedir una vacante en la Red Provincial.
- **E3 · Línea 144:** la de la Provincia atiende las 24 horas y deriva al área municipal [verificado]. La Mesa Local se creó por el Decreto 2493/2012; si funciona en 2026 está [sin confirmar].
- **E4 · Área de género:** según el Municipio, la Dirección de Acompañamiento a la Mujer atiende en O'Higgins 380, de lunes a viernes de 8 a 14, con guardia por WhatsApp. Tiene una sola sede [verificado].
- **E5 · Junta del CUD** [verificado]:
  - funciona en el Hospital Central, Av. Santa Fe 431;
  - el trámite empieza en argentina.gob.ar/cud, sigue con una pre-junta y termina con la junta;
  - la web no dice por qué canal se pide el turno de la pre-junta.
- **Programa provincial de 2026 para la salida de las violencias:** si San Isidro adhirió está [sin confirmar].

---

## Las cinco tablas

### Tabla A · Costos: hoy, opción óptima con calidad, diferencia por año, y dónde cambia

Pesos de diciembre de 2025, dólar a $1.520. [cálculo propio salvo donde se indica]

| Rubro | Costo hoy | Opción óptima con calidad | Diferencia | Dónde cambia en el documento y en el Excel |
|---|---|---|---|---|
| Profesor digital, todo incluido, 50.833 alumnos con uso pleno | Sin cifra en el documento ni en el Excel. Informe 22: $29.387 M por año (avatar a US$0,50 por minuto) | $2.039 a 2.486 M por año (US$26 a 32 por alumno): gpt-6-luna en la UE, voz y reconocimiento de Azure es-AR, avatar por volumen a 1-2 centavos, celular de la familia y cursos gratuitos | −26.901 a −27.348 M por año contra el informe 22 | `content_c.py` L2243 a L2280 (no tiene costo); el Excel necesitaría una línea nueva |
| Profesor digital, uso realista (15%) | Ídem | $659 a 726 M por año | — | Ídem |
| Prueba de 6 meses, 2 centros | Sin cifra | $118,6 a 119,3 M | — | `content_c.py` L2277, punto 8 |
| Canon de los colegios privados | «Pagan poco o nada… y los de cuota alta, más», sin montos | Opción 2: $0, $912, $2.280, $4.560 y $6.840 por alumno por mes, más $50.000 a 600.000 por sección por año para el colegio | Cubre 47% a 71% del costo total | `content_c.py` L2260, punto 4 |
| Habilitaciones y analítica, inversión | 1.200 M una vez | 246 a 450 M | **−750 a −954 M una vez** | Supuestos fila 54; Programas fila 13; `content_b.py` L276; `content_c.py` L2425; `content_o.py` L486 |
| Habilitaciones y analítica, mantenimiento | 264 M por año (22% de Oracle) | 34 a 56 M, más datos móviles | **−208 a −230 M por año** | Supuestos filas 57 y 176; Programas fila 13; `content_b.py` L276, L299 y L342 (6.863 M → 6.632 a 6.655 M); `content_c.py` L2426 |
| Licencia de las cámaras corporales | 3,8 M por año | 0, con código abierto | −3,8 M por año (dentro de la fila anterior) | Supuestos fila 234; `content_b.py` L293 |
| Redes en los desagües (10 bocas) | 395 M por año (informe 11) | 33 a 75 M por año, más 52 a 85 M una vez | **−320 a −362 M por año** | `content_c.py` L1334 («todos los días») y L1363 y L1364 (790 a 1.140 M → unos 430 a 820 M); informe 11 L87, L406 y L420; el Excel no tiene línea |
| Plataforma, infraestructura y licencias | 193,2 M por año (18% de los sueldos) | 139,6 M sólo vecinos; 268,7 M con todo; unos 211 M con los avisos por la app | −53,6 a +75,5 M por año | `content_c.py` L774 (cuadro 27); Supuestos E161 |
| Personas nuevas | No están | 10 en la plataforma (336,7 M) y 8 en las áreas (202,0 M) | +538,7 M por año | Cuadro 27, `content_c.py` L774; Supuestos E161 |
| Sensores del diagnóstico de Perú | 20 × US$500 dentro de 22 a 36 M | 20 × US$25 | −13,8 M una vez | `content_c.py` L1328; Supuestos E238 |
| Muestras de agua | 42 a 75 M, precio de lista privado | Convenio con laboratorios públicos | Sin precio | `content_f.py` L30; Supuestos E238 |
| WhatsApp del informe 17 | US$2.600 por mes | Respuestas gratis dentro de las 24 h | Hasta −47,4 M por año | Sólo el informe 17, L339 y L340 |
| Imagen satelital del informe 14 | US$2.000 a 2.550 una vez | Ortofotos de ARBA o del Municipio | Hasta −3,9 M una vez [sin confirmar] | Sólo el informe 14, L306 a L310 |

### Tabla B · Puente con los laboratorios

| Programa | Requisitos | Visa | ¿A distancia? | ¿Sirve para nuestros egresados? |
|---|---|---|---|---|
| Cohere Labs Scholars | Tiempo completo y curiosidad por la IA; no pide investigación previa. Pago | No hace falta | Sí, desde cualquier país | **Sí, el mejor candidato.** Hoy cerrado; reabre en el otoño boreal de 2026 |
| Google Summer of Code | 18 años o más; estudiante o principiante en código abierto; 90 a 350 horas; US$750 a 3.000 | No hace falta | Sí | **Sí**, desde la cursada |
| J-1 Intern o Trainee (22 CFR 62.22) | Intern: hasta 12 meses después de recibido. Trainee: título y 1 año de experiencia | J-1 con patrocinador | No | **Sí: la vía legal más realista a EE. UU.** |
| Residencia de OpenAI | Sin título formal; la vara técnica de un empleado de planta; 6 meses | Sí | No | Sólo un perfil excepcional; la convocatoria 2026 está cerrada |
| Fellows de Anthropic | Python fluido; 4 meses; cierra el 18/10/2026 | No | Sólo desde EE. UU., el Reino Unido o Canadá | No, salvo que ya vivan allá |
| Claude Corps (Anthropic) | Sin requisito de estudios; 1 año en ONG de EE. UU. | No lo dice | No | No; sirve de modelo para la pasantía en el Municipio |
| Mistral, vía Corea | 6 meses en París o Londres y después un puesto en Seúl; pide estar radicado en Corea | Sí | No | Directamente no. **Es el modelo a copiar** |
| Student Researcher de Google DeepMind, pasantías de Microsoft, NVIDIA y Cohere | Estar cursando grado o posgrado | No lo dicen | No | No |
| ByteDance, Baidu, Tencent, Alibaba y DeepSeek | Doctorado, maestría o grado de universidades top | — | No | No |
| Vacaciones y trabajo: Australia (18 a 30 años) y Nueva Zelanda (18 a 35) | Diploma terciario o 2 años de facultad; inglés funcional (Australia) | Sí | No | Sí, como experiencia, no como puente |

Marcas: [verificado], salvo OpenAI (extracto del buscador) y las empresas chinas ([probable] en parte).

### Tabla C · Espectáculos al aire libre

| Regla | Quién la usa | Número | ¿Sirve para San Isidro? |
|---|---|---|---|
| Registro gratis con credencial | Ciudad de Buenos Aires; Mar del Plata (Ord. 24950/2020); Córdoba AR (Ord. 10093/1999); proyecto 527-HCD-2025 | $0 | Sí, por ordenanza |
| Puntos fijos señalizados | Westminster; parques de Nueva York; Barcelona | Westminster: 26 puntos, 1 actuación por punto | Sí, por decreto (la Ord. 6610 ya habla de espacios «señalizados») |
| Distancia entre artistas | Rosario; Melbourne; Córdoba ES; Sydney | 50 m, 30 m y 100 m | Sí: 100 m entre puntos con sonido |
| Tiempo por punto | Barcelona; Westminster; Ciudad de Buenos Aires; Melbourne; Sydney | 30 min a 2 h | Sí: turnos de 1 h y tope de 2 h por punto y por día |
| Tope de volumen | Rosario; Barcelona; Melbourne; Ciudad de Buenos Aires; Córdoba ES | 60, 65, 72 y 75 dB | Sí: un tope medido a 3 o 5 m |
| Amplificación | Córdoba ES; Melbourne; Westminster; Ciudad de Buenos Aires | Hasta 20 W a batería; nada enchufado | Sí: acústico por defecto |
| Horarios | Ciudad de Buenos Aires; Barcelona; Westminster; Rosario | 10 a 21 o 22 | Sí: de lunes a jueves, con hora de corte |
| Zonas sin sonido | Mar del Plata; Rosario; Melbourne; San Isidro, Ord. 8461 art. 11 o) | — | Sí: Ribera Norte, Bosque Alegre y frentes de vivienda |
| Permisos que rotan | Rosario; Barcelona; Córdoba ES | 30 días a 4 semanas | Sí: turnos mensuales por sorteo o por la app |
| Costo | Ciudad de Buenos Aires y Mar del Plata, gratis; Melbourne AUD 30 por año; Westminster £10 por mes; San Isidro hoy $246 por m² y por día | — | Gratis para independientes registrados (por ordenanza) |
| No secuestrar instrumentos | Mar del Plata, Ord. 24950 art. 8 | — | Sí, por ordenanza |
| Pase a permiso de evento | San Isidro, Agencia de Control y Ord. 7198 | 1 persona cada 3 m² | Sí |

Marcas: [verificado], salvo Camden, Mendoza y las tarifas actuales de Melbourne [sin confirmar]. Todo lo jurídico necesita dictamen de un abogado.

### Tabla D · Turnos médicos

| Dato | Fuente | ¿Sirve para San Isidro? |
|---|---|---|
| Hospital Italiano: 27,84% de faltazos sobre 2,5 millones de turnos; la causa principal es el olvido (44%) | Int J Health Plann Manage 2019 [verificado] | Como referencia; es privado |
| Hospital Elizalde: 11,35% de teleconsultas perdidas | Arch Argent Pediatr 2026 [verificado] | En parte: sólo teleconsulta |
| Hospitales municipales de Olavarría y Trenque Lauquen: 15% a 17% | Prensa local [probable] | Sí, como orden de magnitud |
| Mensajes: asistencia de 67,8% a 78,6% (Cochrane, 7 ensayos); faltazos de 21% a 15% (BMJ Open, 21 ensayos) | Cochrane 2013; BMJ Open 2016 [verificado] | Sí |
| Población pobre o sin seguro en EE. UU.: el mensaje solo no tuvo efecto | J Eval Clin Pract 2021 [verificado] | Advertencia: en La Cava o el Bajo hace falta mensaje y llamada |
| Ensayo argentino (privado): de 30% a 10% con mensaje | CAIS 2016, SEDICI [verificado; con sesgo] | Sí, con sesgo |
| Inglaterra 2026: se liberaron 35 turnos y se reocuparon 20 | BMJ Open Quality 2026 [verificado] | Sí: hace falta cancelar en dos vías y alguien que reasigne |
| Chile, hospital público pediátrico: la IA eligió a quién llamar, de 21,0% a 10,7% | Health Care Manag Sci 2023 [verificado] | Sí, el caso más parecido |
| Badalona: −39% a −51% llamando a los de alto riesgo | BMC Health Serv Res 2022 [verificado] | Sí |
| Singapur: de 19,3% a 15,9% | AJR 2020 [verificado] | Sí |
| Zúrich: sin efecto (21,9% contra 22,0%) | JAMIA Open 2026 [verificado] | Sí, como advertencia |
| Sobreturno por IA: efecto incierto; puede perjudicar a los grupos con más faltazos | JAMIA 2023; MSOM 2022 [verificado] | Con cuidado |

### Tabla E · Género y discapacidad

| Qué existe | Dónde | Cómo se accede | Fuente |
|---|---|---|---|
| Dirección de Acompañamiento a la Mujer (municipal), con «asesoramiento legal» | O'Higgins 380, San Isidro | Lunes a viernes de 8 a 14; 4512-3136; guardia por WhatsApp 11-3163-8969 | sanisidro.gob.ar/mujeres [verificado, según el Municipio] |
| Consultorio Jurídico Gratuito del Colegio de Abogados de San Isidro | Acassuso 426 (otras fuentes dicen 424 o 442) | Martes a viernes desde las 8, 6 números por día; hay que demostrar falta de recursos | casi.com.ar [verificado]; necesita dictamen de un abogado |
| Defensa Oficial del Fuero de Familia (Ministerio Público bonaerense) | Rivadavia 468, San Isidro | (011) 4747-6698/6705; acreditar falta de recursos o vulnerabilidad | Folleto del Ministerio Público, 13/03/2026 [verificado] |
| Práctico de la UBA | Martín y Omar 339 | Lunes, martes, jueves y viernes de 8 a 10; declaración jurada | derecho.uba.ar [verificado] |
| Red Provincial de Dispositivos de Protección Integral (hogares) | Cualquier municipio | El equipo municipal manda la ficha de riesgo; no se entra en forma directa | Guía provincial de 2020 [verificado]; vigencia 2026 [probable] |
| Hogar propio en San Isidro | No existe | — | Informe provincial 2022 [verificado] |
| Línea 144 de la Provincia | Remota | 144, las 24 horas; WhatsApp 221 508 5988 | gba.gob.ar/mujeres/linea144 [verificado] |
| Mesa Local Intersectorial | Municipio | Decreto 2493/2012; conformada en 2023 | Boletín municipal; informe provincial 2020-23 [verificado]; 2026 [sin confirmar] |
| Comisaría de la Mujer | Juncal 46, Martínez | (011) 4512-2345 | Folleto del Ministerio Público 2026 [verificado] |
| Junta evaluadora del CUD | Hospital Central, Av. Santa Fe 431 | argentina.gob.ar/cud, pre-junta y junta; consultas lunes, martes y jueves de 8 a 12 | sanisidro.gob.ar [verificado] |
| Dirección de Discapacidad | 25 de Mayo 574; y La Cava, Newbery 1450 (lunes) | 4512-3313/3378 | sanisidro.gob.ar [verificado] |

---

## Dónde busqué y no encontré

**A · Costos propios**
- **Avatar:**
  - la fuente primaria de los «72 cuadros por segundo de MuseTalk en una RTX 4090»;
  - precios de tiempo real de Akool, Volcengine, iFlytek y SenseTime;
  - planes de educación o de gobierno;
  - proveedores de placas en la Argentina;
  - el número «Resolución ENRE 534/2026», que no figura en el cuadro tarifario.
- **Modelo, voz y fijos:**
  - mediciones de tutoría o de reconocimiento con voces de chicos en castellano;
  - los términos sobre menores de Azure Speech y ElevenLabs;
  - el precio unitario de tablets en licitaciones argentinas.
- **Canon:**
  - las providencias de topes 2026 en una fuente oficial en línea;
  - las cuotas bajas o medias de los colegios sin aporte;
  - si la evaluación META cobra a los colegios.
- **Seguridad:**
  - el original del precio de la cámara corporal (SRT, enero de 2026);
  - el proveedor de la licencia de 55.878 $;
  - precios de BriefCam, Genetec y Avigilon;
  - tarifas de datos 4G.
- **Redes:**
  - precio argentino de una bolsa de red;
  - días de lluvia del SMN, que bloqueó la descarga;
  - si siguen las redes de Perú.
- **Plataforma:**
  - un número oficial de asociaciones;
  - la tarifa de marketing de WhatsApp en dólares;
  - el precio de GitHub Copilot Business.

**B · Puente:** openai.com y uscis.gov respondieron 403. No encontré convenios de vacaciones y trabajo vigentes según la Cancillería.

**C · Espectáculos:**
- el digesto de San Isidro (índice con error 403);
- la reglamentación de la 9120;
- el público de DJ Sunset y de Nochecitas;
- una ley provincial sobre artistas.

**D · Turnos:**
- el ausentismo de San Isidro;
- cifras oficiales de la Ciudad y de la Provincia;
- un hospital público argentino con IA en la turnera y resultado medido.

**E · Género y discapacidad:**
- el estado 2026 del Cuerpo de Abogadas de Nación;
- consultorios de género en universidades de zona norte;
- el canal para pedir la pre-junta del CUD.

**Método:** varios investigadores agotaron el cupo de 200 búsquedas web y siguieron con direcciones conocidas. Por eso algunas búsquedas quedaron incompletas.

---

## Preguntas abiertas (decide el cliente)

1. **El dólar:** ¿se sigue con $1.520 o se deflacta a diciembre de 2025 (unos $1.274, un 16% menos en todo lo que se calcula en dólares)?
2. **Profesor digital:**
   - ¿se cargan en el documento el escenario (d) de uso pleno o el (c) de uso realista?
   - ¿el equipo se paga con los sueldos del cuadro 27 (A4 bis) o con los del informe 22?
3. **Canon:**
   - ¿Opción 1 (montos fijos) u Opción 2 (atada al costo)?
   - ¿lo cobra el Municipio o el colegio en su recibo?
   - ¿adhesión obligatoria o voluntaria?
   - ¿se exime a los becados?
   - Necesita dictamen de un abogado.
4. **Avatar:**
   - ¿se acepta que la cara se genere en EE. UU. o en la UE con cláusulas tipo?
   - ¿cara propia, de un actor o docente con consentimiento, o de catálogo?
   - ¿cómo se paga el IVA de servicios digitales del exterior?
   - Necesita dictamen de un abogado.
5. **Seguridad:**
   - ¿cuántas cámaras con IA de servidor (hoy 110; el contrato llega a 150)?
   - ¿80 cámaras corporales o las 331 que daría «todo agente con facultad de fiscalización»?
   - ¿cuánto tiempo se guarda la grabación pública (57 a 114 TB por año)?
6. **Redes:** ¿vaciado semanal y después de cada lluvia (33 a 75 M), o todos los días hábiles como dice hoy el texto (75 a 161 M)?
7. **Plataforma:**
   - ¿los avisos van por WhatsApp (50 M por año) o por la app y el correo (gratis)?
   - ¿«licencias» incluye las herramientas para programar del equipo (67,5 M)?
   - ¿espacios para 70 asociaciones o para las 895 entidades?
8. **Puente:** ¿la tecnicatura nueva tendrá validez nacional y qué nivel (CINE 5 o 6)? De eso depende que encaje en la J-1 y en las prácticas de la UE.
9. **Espectáculos:** ¿se arranca con el piloto por decreto y se retoma el proyecto 527-HCD-2025 para la ordenanza?
10. **Turnos:** ¿quién reasigna los turnos liberados y con qué personal?

---

## Método

- **Investigadores:** nueve, uno por tema. Ninguno contactó a nadie, se registró en ningún servicio ni pagó nada.
- **Verificación en la fuente guardada:**
  - las cifras clave de cada reporte, entre ellas:
    - los topes de la providencia PV-2026-26081548;
    - los totales del padrón por tramo (recalculados sobre el CSV);
    - el texto de Marin County;
    - los precios de LP 62/2024 y del Decreto 1238/2024;
    - la Resolución 609/2026 de OSSE;
    - el Decreto 682/2026 y el pliego de LP 45/2025;
    - la lista de Oracle;
  - las filas del Excel y las líneas del documento después del commit 888e8b1.
- **Cuentas propias:** están en las carpetas `_tools/` de cada subcarpeta.
- **Copia de las fuentes:**
  - no se duplican los archivos que ya están en el repositorio (se listan en `NO_SUBIDOS.txt`);
  - se reemplazaron números de DNI y claves de terceros;
  - el padrón de establecimientos se sube sin las columnas de correo y teléfono.
- **Navegación:** sanisidro.gob.ar se leyó con el certificado intermedio público, sin desactivar la verificación.
