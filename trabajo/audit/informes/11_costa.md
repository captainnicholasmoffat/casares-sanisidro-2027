# 11 · La costa de San Isidro: la basura, la arena y quién decide

Investigación. 29 de septiembre de 2026. Rama `claude/cool-hopper-3hdk58`. **El documento no se toca.**

**Estado: para decidir.** Nada de esto está en el programa todavía. Al final va un borrador de propuesta, marcado como
tal.

**Cómo leer las marcas.** **[V]** verificado: se leyó en la fuente primaria. **[P]** probable: fuente secundaria seria,
o varias que coinciden. **[SC]** sin confirmar. **[CP]** cálculo propio, con la cuenta a la vista. Lo que dice el
Municipio en su prensa va como *según el Municipio*: no es un dato verificado.

**Montos.** En pesos de diciembre de 2025, como el resto del programa, salvo que se diga otra cosa. Los montos viejos se
llevaron a diciembre de 2025 con el IPC de `data/ipc_indec_mensual.csv`; los dólares, con el tipo de cambio de
referencia del BCRA (Comunicación "A" 3500), promedio de diciembre de 2025: **$1.447,84 por dólar**; los euros, con la
referencia del Banco Central Europeo para ese mes: **1,1709 dólares por euro**. Los dos archivos están en
`01_raw/costa/tipo_cambio/`. Pasar un contrato viejo a pesos de hoy con el IPC da un orden de magnitud, no un precio.

Todas las fuentes se consultaron el 29/09/2026. Las descargadas están en `01_raw/costa/`, con su URL en
`01_raw/costa/FUENTES.txt`.

---

## Resumen

### Lo que es cierto

- **La costa está sucia y el agua no es apta para bañarse.** En las cuatro estaciones oficiales de San Isidro se
  midieron 35 muestras de *E. coli* entre 2021 y 2025. **Ninguna** quedó por debajo del valor guía para contacto directo
  (126 por 100 ml). La mediana fue 4.400, y la desembocadura de la calle Perú llegó a 2.000.000 en abril de 2025. **[V]**
  Bañarse en el río está prohibido en San Isidro desde la Ordenanza 5304 de 1978. **[P]**
- **Hubo playas y balnearios.** Hay notas y fotos de época en *Caras y Caretas* desde 1916. Hubo balnearios en el Bajo
  entre 1910 y 1940: El Mar Dulce, El Tropezón, El Águila y Las Toscas, este último de 1935. **[V]** para las notas;
  **[P]** para los nombres de los balnearios, que vienen de un estudio académico que cita un libro municipal.
- **"Playa" no quería decir arena.** La foto de 1917 muestra una "frondosa playa" de tierra y árboles. La única fuente
  de época que habla de arena en San Isidro es una nota de 1937 sobre el Club Balneario San Isidro. **[V]**
- **El Municipio ya limpia la costa, pero no mide qué junta.** En 2025 se fijó una meta de 60 "limpiezas de la costa" y
  registró 61. No dice qué cuenta como una limpieza. **[V]** *Según el Municipio*, en 2025 hubo 65 jornadas con más de
  3.500 voluntarios y unas 20 toneladas retiradas.
- **Ya se pagó por limpiar una desembocadura.** Entre 2014 y 2017 el Municipio contrató la "limpieza de residuos del
  sobrenadante y costas del desagüe pluvial de la calle Perú": primero una cooperativa y después una empresa. **[V]**
  Después de 2017 no aparece ningún contrato así.
- **Las 50 hectáreas no son del Municipio.** La Ordenanza 9430 aprobó un convenio que le da al Municipio la
  **tenencia y administración** de 15 parcelas costeras. El dominio sigue siendo de la Provincia. **[V]** Por ley, esa
  tenencia obliga al "cuidado y conservación del bien incluyendo las cargas consiguientes" (Decreto-Ley 9533/80,
  art. 38). **[V]**
- **Casi todo permiso pasa por la Autoridad del Agua.** Instalar una barrera flotante, poner una estructura en el río,
  reponer arena o dragar requiere aprobación de la Autoridad del Agua (Código de Aguas, Ley 12.257), evaluación de
  impacto ambiental (Ley 11.723) y consulta a la Provincia por ser ribera cedida (Decreto 8282/87). **[V]**

### Lo que no es cierto, o no se puede escribir

- **El "70% es plástico" no es un dato de San Isidro.** La nota municipal del 24/09/2020 copia palabra por palabra un
  comunicado de enero de 2020 del colectivo Más Río Menos Basura de **Rosario**, sobre el **río Paraná**. Es un
  porcentaje en peso, de una limpieza en Rosario. **[V]** **No lo usamos.**
- **Que la arena se sacó para construir el Hipódromo: no hay prueba.** El Hipódromo se inauguró en 1935, está en la
  parte alta del partido, a más de diez cuadras de la costa, y su página dice que la pista es de "arena de cava" y que
  dos pistas de entrenamiento son de "arena de río", sin decir de dónde vino. **[V]** Se revisaron 1.038 números de
  *Caras y Caretas* de la época y ninguno lo menciona. **No lo escribimos.**
- **Que la basura "viene de todos lados": no hay estudio que lo mida.** Lo dijo el intendente Posse en 2019. **[V]**
  Pero ninguna fuente mide qué parte es de San Isidro y qué parte llega del Reconquista, del Luján o de la Ciudad. El
  propio Municipio dice, en las mismas notas, que la basura de la calle "a través de los sistemas pluviales" termina en
  el río. **[V]**
- **Una barrera no resuelve el problema.** La mejor barrera flotante probada en la Argentina retuvo el 37% de los
  plásticos, y en diagonal menos del 10%. **[V]** Las barreras del Riachuelo se rompen con las crecidas. **[V]**

### Lo que no se pudo verificar

- El texto del convenio de las 50 hectáreas: **no está publicado**. Lo que se sabe de sus cláusulas sale de lo que
  dijeron los concejales en la sesión del 15/04/2026. El plazo es dudoso: un concejal dijo diez años y otro, que es
  revocable sin plazo.
- **Cuánta basura hay en la costa, de qué tipo y de dónde viene.** No existe ningún estudio de basura en la costa de
  San Isidro.
- Si hoy funcionan las redes que en 2015 retenían basura en el desagüe de la calle Perú.
- **Cuánto cuesta reponer arena, y si se quedaría.** No se encontró ningún estudio para San Isidro.
- El rol exacto de Prefectura y de la autoridad nacional de vías navegables en una obra en el río.

---

## La tabla de opciones

Para qué sirve cada cosa, con resultados medidos donde se usa. "Cuánto saca" es basura total en peso húmedo, salvo
aclaración: casi ningún operador informa sólo plástico.

| Opción | Qué es | Cuánto saca | Cuánto cuesta | Dónde funciona | ¿Sirve acá? |
|---|---|---|---|---|---|
| **Cuadrilla de costa** | Personas con rastrillos, ganchos y bolsas, con apoyo de bote | 28 kg por persona y hora en una costa de roca y vegetación (Aldabra, 2019) **[V]**. San Isidro sacó 50 t después de una sudestada en 2015, *según el funcionario* **[V]** | San Isidro pagó $524.062,50 por trimestre en 2015 por la limpieza del desagüe de Perú: unos **323 M por año** en pesos de hoy **[CP]** | Cualquier costa: juncal, piedra, escombro | **Sí.** Es lo único que llega al juncal y a la piedra |
| **Red o reja en la boca del desagüe** | Bolsa o reja al final del caño | Kwinana (Australia): 5 redes, 3,66 t en 6 años **[V]** | Unos US$27.300 por red y año de mantenimiento (Marin County, 2022): **39,5 M** **[V]** / **[CP]**. La instalación se presupuesta por caudal: US$2.500 por pie cúbico por segundo **[V]** | Caños pluviales | **Sí**, en desagües chicos y medianos. San Isidro ya las usó en Perú. En las bocas grandes hay que diseñarlas para la tormenta y para cuando el río entra por la sudestada |
| **Barrera flotante en boca o dársena** | Flotadores con pollera, vaciados desde tierra o bote | ACUMAR, arroyos críticos: 7.636 t en 11 meses (2021-22) **[V]**. Porto Alegre: 65 a 217 t por año **[V]** | ACUMAR pagó $428,5 M por 48 meses en 2021 (4 puntos fijos más un equipo móvil): unos **2.124 M por año** hoy **[CP]** | Arroyos y ríos urbanos | **Sí, como complemento**, con vaciado diario. Retiene 37% en el mejor caso y se rompe con crecidas |
| **Embarcación recolectora** | Barco con brazos o pala | DC Water, 2 barcos: 300 a 500 t por año **[V]** | US$484.000 por barco (2017): **701 M** **[CP]** | Agua con calado | **En parte.** No entra al juncal ni con bajante |
| **Rueda de basura** (Baltimore) | Rueda con corriente y paneles solares que rastrilla la basura hacia un contenedor | 137 a 310 t cortas por año **[V]** | US$704.000 de capital; las cuatro ruedas cuestan US$400.000 por año **[V]**. Una rueda, en pesos: **1.019 M** **[CP]** | Bocas de arroyo dentro de un puerto abrigado | **Condicional.** No hay un solo caso en costa abierta |
| **Interceptor** (The Ocean Cleanup) | Catamarán solar amarrado en el cauce | 50 a 150 t por año según el sitio **[V/P]** | €700.000 por unidad, *según la ONG*: **1.187 M** **[CP]**. Los Ángeles gasta US$550.000 por año en operarlo **[V]** | Ríos con corriente | **No.** Los desagües de San Isidro no tienen corriente constante. El de Santo Domingo se retiró en 2025 **[V]** |
| **Barrera de burbujas** (Ámsterdam) | Cortina de burbujas desde el fondo | Westerdok: 1 t de plástico por año **[V]** | €480.000 por sistema, más €52.000 a €61.000 por año **[V]**. Cuesta €76.453 por tonelada **[V]** | Canales con caudal constante | **No.** "Tiene que haber siempre un caudal neto", dice la evaluación independiente **[V]** |
| **Cámara con IA en la boca** | Cuenta la basura que flota | No saca: mide | No publicado | Ríos (madurez 8 de 9, Japón) **[V]** | **Sí, para medir** dónde conviene actuar |
| **Dron con IA sobre la costa** | Relevamiento fotográfico con clasificación automática | No saca: mide | €36.600 por año en el Báltico (2021): **62 M** **[V]** / **[CP]** | Costas despejadas | **En parte.** La vegetación le baja la precisión y en el Báltico no reemplazó al conteo a ojo **[V]** |
| **Satélite** | Imágenes Sentinel-2 | — | — | Investigación | **No.** Madurez 2 a 3 de 9 en ríos **[V]** |

**Lo que sirve en San Isidro, en una línea:** una cuadrilla de costa con protocolo para juncales, redes en los
desagües, barreras en las bocas grandes con vaciado después de cada lluvia, y cámaras para medir. Ningún equipo
documentado funciona en una costa abierta sobre un río de decenas de kilómetros de ancho: todos los casos están en
cauces, canales o bahías abrigadas. **[V]**

---

## A · El diagnóstico

### A1 · Qué desemboca en el río

No hay un plano oficial publicado de las bocas de los desagües. Lo que se sabe:

| Desembocadura | Dónde | Qué es | Confianza |
|---|---|---|---|
| **Aliviador Alto Perú** | Dársena Gauto y Pavón, Bajo de Beccar | Túnel entubado de 2.300 m, de 4,40 m de diámetro, *según el Municipio*. La ficha nacional le da un costo de $7.018 M, un avance de 78,2% y lo muestra en ejecución. | **[V]** ficha nacional; traza *según el Municipio* |
| **Desagüe de la calle Perú** | Acassuso, "a la altura del puente de madera" | Aliviador del arroyo Pavón superior, con "una gran cuenca de aporte" de San Martín, Vicente López y San Isidro, *según el Municipio*. Es el punto con la peor calidad de agua de la costa. | **[P]** La Nación, 2017, citando al Municipio |
| **Estaciones de bombeo del Bajo** | España y Mitre, Chile, Leloir, Martín y Omar, Roque Sáenz Peña y Los Álamos | Bombean sobre el albardón costero, de 4.300 m. Con el río alto se cierran las compuertas. | *Según el Municipio* |
| **Conducto de la calle Paraná** | Límite con Vicente López | Cuenca Bermúdez. No se encontró la boca exacta. | **[P]** |
| **Bocas menores sin nombre** | Juan Díaz de Solís, Sebastián Elcano, San Isidro, Beccar | Mapeadas en OpenStreetMap. | **[SC]** |

**Al Reconquista, no al Río de la Plata:** el Aliviador del Arroyo Pavón, la subcuenca de la calle Uruguay y los
arroyos Bancalari y Matorras, de Boulogne. Eso ubica a San Isidro dentro del Comité de Cuenca del Reconquista, en la
"Cuenca Baja". **[V]**

**Caudales y superficies de cuenca: no se encontró ninguno.** Sólo hay capacidades de bombeo, *según el Municipio*.
Sin ese dato no se pueden dimensionar redes ni barreras.

### A2 · Cuánta basura llega, dónde y cuándo

**No hay ningún estudio de basura en la costa de San Isidro:** ni cuánta hay por metro, ni de qué está hecha. **[V]**,
como ausencia, después de revisar la literatura del Río de la Plata. Lo que hay:

| Fuente | Qué dice | Confianza |
|---|---|---|
| Campaña "Sí al Río Limpio", 2019 | Lanzamiento el 23/03/2019 en Pacheco y el río, Martínez: 2.700 kg de reciclables. En todo 2019, "9 jornadas, y en cada una se recolectó alrededor de 3.000 kg de basura". | *Según el Municipio* |
| Campaña, 2020 | "Al finalizar cada jornada, se juntan unos 1.000 kg de residuos reciclables". | *Según el Municipio* |
| Municipio, 2025 | 65 jornadas, más de 3.500 voluntarios, unas 20 t. | *Según el Municipio* |
| Hermanos Lange, Club Náutico San Isidro, 16/12/2018 | Más de 3.000 kg en 2 horas, con gomones para entrar al juncal. | **[P]** La Nación, 17/12/2018 |
| Versova, oct-2020 a oct-2021 | 21 t en un año, unos 905 voluntarios. "El 18% de lo reunido era reciclable". | **[P]** *según Versova* (Carbono News, 2023) |
| Subsecretario de Espacio Público, 2015 | "En la última sudestada sacamos 50 toneladas de basura de la costa. Al día siguiente de una lluvia normal se recolectan unas 20 toneladas." | **[V]** que lo dijo (La Nación, 20/09/2015) |
| Microplásticos, 2016-17 | 139 partículas por m³ de agua en promedio entre San Isidro y Punta Indio. San Isidro, con hábitat "muy malo". | **[V]** Pazos, Bauer y Gómez, 2018 |

**Los números de la campaña municipal no cierran entre sí.** Se mezclan kilos de reciclables, kilos de basura y
bolsas, y ninguno trae método. Por eso no sirven como línea de base.

**La corrección de una nota:** la de La Nación del 14/01/2021 ("El río sin basura") no es sobre los hermanos Lange sino
sobre Versova. Los Lange aparecen en otra nota, del 17/12/2018. **[V]**

**Dónde se acumula.** Entre Pacheco y la calle Paraná (Martínez), en el juncal del Club Náutico, en la Reserva Ribera
Norte, en la boca de la calle Perú y en las desembocaduras pluviales. **[V]** que lo dicen las notas; no hay mapeo
sistemático. No se encontró nada específico sobre el Paseo del Águila, las Barrancas, el Puerto ni el playón de Beccar.

**Cuándo se acumula.** Después de las sudestadas y de las lluvias. **[V]** que lo dicen el Municipio y los voluntarios.
Hay dos o tres sudestadas fuertes por año, más frecuentes entre marzo y octubre. **[V]** (Moreira y Simionato, 2019).

### A3 · De dónde viene

- **La frase de Posse** está en la nota municipal del 25/03/2019: "Muchas veces vienen sudestadas y traen basura de
  todos lados". **[V]**
- **Las corrientes.** Frente a la costa argentina corre el agua del Paraná de las Palmas y del Luján. Una sudestada la
  frena y la hace retroceder; después el flujo se rearma rápido. **[V]** (INA, 2004). El mismo informe concluye que "la
  calidad del agua en cada una de las dos costas… es responsabilidad directa del manejo de las descargas antrópicas
  efectuadas por cada país". **[V]** **Ningún modelo sigue la basura que flota.**
- **Lo que retiran los vecinos de cuenca.** El Riachuelo, 2.800 a 4.750 t por año entre 2015 y 2025. **[V]**, con
  reparos por errores en la planilla de ACUMAR. El Reconquista, unas 150 t por mes en 2020, *según CEAMSE* **[SC]**.
  Los arroyos de la Ciudad, 134 t por mes en 2015, *según la Ciudad* **[P]**. Del Luján no se encontraron datos.
- **Riachuelo y Ciudad desembocan aguas abajo de San Isidro; el Luján y el Reconquista, aguas arriba.** **[V]**,
  geografía. No hay estudio que muestre que la basura de alguno de ellos llega a San Isidro.

**Conclusión honesta:** la basura de la costa es en parte de San Isidro y en parte de afuera, y **nadie midió la
proporción.** Lo que sí se puede medir es la que sale por los desagües propios.

### A4 · De quién es la costa y quién autoriza qué

**El marco.**

- El río, sus playas y su lecho son del dominio público, hasta la línea de ribera (Código Civil y Comercial, art. 235).
  **[P]**, en texto no oficial.
- La Autoridad del Agua fija esa línea (Ley 12.257, art. 18). **[V]**
- La Provincia le cedió a San Isidro la administración de playas y riberas en 1977 (Decreto 1980/77), pero se reservó
  "la fiscalización y facultades reglamentarias". **[V]**
- En 2026 le delegó además la tenencia de 15 parcelas (Decreto-Ley 9533/80, art. 38; Ordenanza 9430). **[V]**
- La franja de 2 millas marinas frente a la costa es jurisdicción exclusiva argentina (Tratado del Río de la Plata,
  art. 2). **[V]**

| Acción | Quién autoriza, y por qué norma |
|---|---|
| **Limpiar a mano** | El Municipio, como tenedor y administrador (Decreto-Ley 9533/80, art. 38; Decreto 1980/77). No se encontró ninguna norma que exija permiso de la Autoridad del Agua para juntar basura. En predios concesionados o privados, como los clubes, el Puerto o la Reserva, hay que acordar con el titular **[SC]**. |
| **Barrera flotante en la boca de un desagüe** | Autoridad del Agua: Ley 12.257, art. 102 e) ("aparatos o mecanismos flotantes, anclados o amarrados a tierra firme"), art. 44 (permiso precario para ocupar el cauce) y Resolución 2222/19 (aptitud hidráulica de la obra). **[V]** Además, evaluación de impacto ambiental (Ley 11.723) y consulta a la Provincia por ser ribera cedida (Decreto 8282/87: si no contesta en 45 días, se da por conforme). **[V]** Si la boca da al Reconquista, también el Comité de Cuenca. Prefectura **[SC]**. |
| **Estructura fija en el río** | Todo lo anterior, más: permiso de obra de defensa de la Autoridad del Agua (art. 138), opinión del gobierno nacional (art. 8) y comunicación a la Comisión Administradora del Río de la Plata (Tratado, art. 17). **[V]** Si el art. 17 rige dentro de la franja de 2 millas no está claro (art. 12). |
| **Reponer arena** | Autoridad del Agua: art. 102 a) si se saca del lecho; arts. 76 y 77 (sacar áridos de playas es un uso minero indirecto, con conformidad de la autoridad minera); art. 21 (nueva línea de ribera si cambia la costa). **[V]** Además, evaluación de impacto ambiental, Decreto 8282/87 y Tratado, arts. 17 y 41. Para arena traída de cantera no se encontró norma específica. |
| **Dragar** | Autoridad del Agua (arts. 102 a) y 44), evaluación de impacto ambiental, Tratado (art. 17), Ley 12.257 (art. 8). Prefectura y autoridad nacional de vías navegables **[SC]**. |

**Las 50 hectáreas de la Ordenanza 9430.**

- **Normas.** El convenio se firmó el 20/03/2026 (CONVE-2026-19-SI-DELE) y lo registró el Decreto 330/2026. Lo aprobó
  la Ordenanza 9430 del 15/04/2026 y lo promulgó el Decreto 465/2026. **[V]** El Decreto 330 dice que el convenio va
  "como Anexo", **pero el anexo no se publicó**.
- **Ubicación.** *Según el Municipio*: 15 parcelas, unos 500.000 m², "desde Paraná hasta Del Barco Centenera". Son
  unos 3,6 km de costa **[CP]**, medidos en OpenStreetMap. **No se encontró la nomenclatura catastral de las
  parcelas.**
- **Lo que dijeron los concejales en la sesión** **[SC]**, a falta del texto:
  - La cláusula 6ª permite usos gastronómicos, náuticos y deportivos "compatibles con el aprovechamiento del espacio
    público, libre y gratuito", y la Provincia se queda con el 40% del canon.
  - La 7ª dice que las mejoras quedan para la Provincia sin indemnización y prohíbe obras que "limiten la libre
    circulación y el acceso público".
  - Un concejal dijo que "son 43 hectáreas… no 55", y que 27 de las 55 "están en poder de privados o de entidades no
    municipales".
- **Obligación de limpiar: no aparece en lo citado.** La base es el art. 38 del Decreto-Ley 9533/80, que obliga al
  "cuidado y conservación del bien incluyendo las cargas consiguientes". **[V]**

### A5 · Qué se hace hoy, además del voluntariado

| Qué | Dato | Confianza |
|---|---|---|
| Programa 19, Servicio de Limpieza del Municipio | Devengado 2025: $49.270 M. Recolección: 185.057 t en el año. | **[V]** Situación económico-financiera 2025 |
| Programa 22, Política Ambiental y Espacio Público | Devengado 2025: $1.410 M. Meta 526, "Limpieza de la costa (cantidad)": 60 programadas y 61 ejecutadas. El monto no es sólo de la costa. | **[V]** |
| Programa 50, Desagües Pluviales y Defensa Costera | Devengado 2025: $164,7 M. | **[V]** |
| El contrato de recolección (LP 17/2008, Roggio–Cliba) | **No se encontró ninguna mención a la costa ni a la ribera** en los decretos del contrato. Los pliegos no están publicados. Ver el informe 12. | **[V]**, como ausencia |
| La limpieza del desagüe de la calle Perú, 2014-2017 | Cooperativa de Trabajo Córdoba (Decreto 4017/2014) y Líneas Marítimas Riccitelli (Decreto 1802/2015 y Licitación Privada 121/2017). $524.062,50 por trimestre en 2015. | **[V]** |
| Cooperativas en barrios del Bajo | Licitación Privada 36/2025, renglón 5 (barrios Roque Sáenz Peña y Martín y Omar): Cooperativa Lara, $4.368.000. | **[V]** Decreto 334/2026 |
| Programa provincial o de la Autoridad del Agua de limpieza de desembocaduras al Río de la Plata | **No se encontró.** Sí hay un convenio de 2019 con Hidráulica de la Provincia para los cuencos del lado del Reconquista. | **[V]** |

---

## B · La tecnología y los precedentes

### B1 · Lo que se usa afuera, con resultados medidos

La tabla de opciones resume lo esencial. Lo que conviene saber para decidir:

- **The Ocean Cleanup anuncia "hasta 50 toneladas por día" por equipo** (*según la ONG*, 2020). En los sitios con datos
  públicos saca **50 a 150 t por año.**
  - Ballona Creek (Los Ángeles) es el más documentado: 124 t cortas en el piloto de dos temporadas, US$550.000 por año
    de operación y barreras que se soltaron con las tormentas de 2023, 2024 y 2025. **[V]**
  - Santo Domingo: pescadores y una ONG hablan de "engaño". Unas 270 t en 4 años contra una promesa de 2.300 t por año.
    **[V]**, como nota de prensa.
  - Kingston (Jamaica) es el caso más parecido a San Isidro, porque trabaja en cañadas pluviales. Nueve barreras
    retuvieron 7.253 t en cuatro años y medio. Los costos no son públicos. **[V]**
- **Mr. Trash Wheel**, en Baltimore: 137 a 310 t cortas por año por rueda **[V]**, en peso húmedo con restos
  orgánicos. La norma del puerto de Baltimore dice que esos pesos "incluyen restos orgánicos mezclados… y el material
  está muy mojado". **[V]**
- **La barrera de burbujas** de Ámsterdam necesita caudal neto constante, y en Katwijk la apagaron en 2022 por falta de
  corriente. **[V]** / **[P]**
- **Barreras flotantes simples.** El ensayo argentino del INALI (UNL-CONICET) dio 37% de retención con la barrera en
  forma de C, menos de 10% en diagonal, y **0%** para platos, cubiertos, sorbetes y bolsas finas. **[V]** El INA mostró
  que las barreras del Riachuelo pueden colapsar con lluvias fuertes, y "a mayor caudal mayor es la probabilidad de
  rotura". **[V]**
- **En juncales**, el protocolo de NOAA (2014): trabajar a mano desde el agua o desde el borde, no desde adentro del
  humedal, y pisar lo menos posible. **[V]**
- **Inteligencia artificial.** Lo que funciona en operación son las cámaras fijas en puentes o bocas y los drones sobre
  costas despejadas: madurez 8 de 9, según el Ministerio de Ambiente de Japón. El satélite, en ríos, está en 2 a 3.
  **[V]**
  - Las cámaras de Yakarta tuvieron 68,7% de precisión. **[V]**
  - En el Báltico, el dron con clasificación automática costó más que el conteo a ojo y "no se puede recomendar como
    reemplazo". **[V]**
  - Ballona tiene cámaras en el puente, en uso real. **[V]**

### B2 · Precedentes argentinos

| Quién | Qué hace | Cuánto saca | Cuánto cuesta | Norma | Confianza |
|---|---|---|---|---|---|
| **ACUMAR**, Riachuelo | 16 barreras y lanchas, desde la Ruta 4 hasta la desembocadura | 2.801 t en 2024; 3.190 t en 2025 | Devengado 2024: $1.409 M (**2.257 M** hoy **[CP]**), unos 800.000 pesos por tonelada **[CP]** | Contrato con COESA, 48 meses desde 2021 | **[V]** |
| **ACUMAR**, arroyos críticos | 4 puntos fijos con barreras vaciadas desde tierra con retroexcavadora, más un equipo móvil | 7.636 t entre jul-2021 y may-2022 | $428,5 M por 48 meses (EMISER, 2021) | Licitación 318-0005-LPU21; hay una nueva en trámite, la 318-0001-LPU26 | **[V]** |
| **Ciudad de Buenos Aires**, costa del Río de la Plata | Limpieza de la faja de 35 m sobre 16 km, desde 2012 | "Unas 300 t" sin período, *según la Ciudad* | $99,9 M adjudicados en 2015; el plazo no se leyó | Licitación 1216/14. La limpieza de las márgenes está dentro del servicio de higiene urbana por ley (Ley 4120, art. 12) | **[V]** |
| **Ciudad**, margen del Riachuelo | 18 km, lancha recolectora | Unas 700 t en 2021, *según la Ciudad* | $28,6 M por 6 meses en 2024 (**89 M por año** hoy **[CP]**) | Disposición 192/DGLIM/24 | **[V]** |
| **Ciudad**, desembocaduras de arroyos | Catamaranes, camiones aspiradores y barreras en seis arroyos | Incluido en las 300 t | $38,5 M por 24 meses desde 2017 | Licitación 8503-1008-LPU16 | **[P]** |
| **Rosario**, arroyo Ludueña | Cinta transportadora con dos barreras | Casi no se usó; retirado en 2024 por bajante, pandemia y vandalismo | US$35.000 aportados por empresas | — | *Según el municipio* |
| **Escobar**, arroyo Escobar | Barrera artesanal de 25 m, con Vida Silvestre | 5.200 kg en unos 2 meses | — | — | **[SC]** |

**Lo que enseña ACUMAR para controlar.** En 2019 su propia auditoría interna **no encontró 7 de las 15 barreras** que
exigía el pliego, y la Auditoría General de la Nación observó cambios de método "sin haberse obtenido parámetros
consistentes" para evaluar los resultados. **[V]** Una barrera que no se inspecciona desaparece.

**Vicente López, Tigre y San Fernando:** no se encontraron barreras ni contratos de limpieza de costa con cifras.

---

## C · La arena

### C1 · La historia

Hay pruebas de que hubo playas y balnearios, y de que la gente se bañaba:

- **1916-1917.** Picnics "en las hermosas playas de San Isidro", con foto de la "frondosa playa que baña el Río de la
  Plata" (*Caras y Caretas* N° 958 y N° 1000). **[V]**
- **1929.** Foto de *La Prensa* del 17/01/1929, "Balneario próximo a Estación Juan Anchorena", conservada en el Museo,
  Biblioteca y Archivo Histórico Municipal Dr. Horacio Beccar Varela. **[V]** que la figura existe (Ríos, 2023).
- **1932.** Aviso del ferrocarril, "La Riviera del Plata": "pase sus horas de libertad en estas playas". **[V]**
- **1935.** Se inaugura el balneario Las Toscas, "el más lujoso de su tipo". **[P]**
- **1937.** "Vida de playa en el Club Balneario San Isidro": "Un poco de 'footing' sobre la arena…". **[V]**

Además, según Ríos (2023), que cita un libro municipal:

- Las costas del Bajo tenían bañistas a fines del siglo XIX, y la Municipalidad había construido casillas de madera
  como vestuarios. **[V]** que lo dice.
- Entre 1910 y 1920 hubo balnearios privados con concesión municipal: El Mar Dulce, El Tropezón y El Águila. **[P]**
- La sudestada del 15/04/1940 llegó a 4,40 m, el máximo registrado desde 1905, y destruyó parte del Tren del Bajo.
  **[V]** que lo dice.
- En 1944 se demolieron las más de 600 casillas de la costa. **[P]**

Hacia 1940 "la ribera sanisidrense había perdido gran parte de su atractivo como lugar turístico". **[V]** que lo dice.

**El final de los baños.** La Ordenanza 5304 del 19/01/1978 declaró "zona de emergencia sanitaria a las playas" de San
Isidro y prohibió "tomar baños en las aguas del Río de la Plata". **[P]**: es una cita textual en un artículo
académico; el texto de la ordenanza no se vio. La Ciudad había hecho lo mismo, con una redacción casi idéntica, con la
Ordenanza 32.716. La prensa la ubica en 1975. **[V]** el texto; **[P]** la fecha.

### C2 · Por qué se perdió

- **Rellenos.** En la planicie costera de Tigre, San Fernando y San Isidro, juntos, el 87% de la superficie natural
  estaba modificada por relleno y urbanización en 2010. La línea de costa pasó de 13 km a 40,6 km por las obras
  náuticas. **[V]** (Melo, Carol y Kruse, 2012). No está desagregado por partido.
  - El Club Náutico San Isidro creció en los años 20 y 30 sobre "terrenos rellenados por draga". **[V]** que lo dice
    Ríos, 2023.
  - El terraplén contra inundaciones es de 1993, con el Tren de la Costa. **[V]** en la cita.
  - En 2005, talleres vecinales todavía denunciaban "rellenos clandestinos sobre todo en los clubes". **[V]** que lo
    dicen.
- **Sedimentación.** El Paraná trae 160 millones de toneladas de sedimento por año: 56% limo, 28% arcilla y 16% arena,
  y **la arena se deposita en gran parte en el frente del Delta.** **[V]** (INA, 2006). El frente del Paraná de las
  Palmas avanza 50 a 100 m por año. **[V]** Hacia San Isidro llega, sobre todo, material fino. **[CP]**, lectura
  propia: ninguna fuente lo dice para San Isidro.
- **Extracción de arena en la costa de San Isidro: no se encontró ninguna fuente.** Lo que sí hay es arena que se
  descargaba: el Puerto de San Isidro fue "un importante embarcadero arenero (y de pedregullo)" desde fines de los años
  40. **[P]**
- **Erosión:** no se encontraron mediciones para San Isidro.

**El hipódromo, otra vez:** no se encontró ninguna prueba. Ver el resumen.

### C3 · ¿Es viable reponerla?

- **Ningún estudio lo evaluó para San Isidro.**
- **El fondo del río no es de arena.** Frente a la costa argentina del estuario superior es "limo arenoso", con poca
  arena muy fina. **[V]** (Moreira y Simionato, INA, 2016).
- **Qué pasaría con la arena.** Las sudestadas mueven sedimento hacia el noroeste, y los recintos con boca al norte
  atrapan limo y arcilla del Delta y se llenan rápido. **[V]** (Marcomini y López, 2004). Una arena puesta en San
  Isidro podría taparse de barro en las zonas quietas o irse con las sudestadas. **[CP]**, como inferencia: hace falta
  un estudio de cómo se mueve el sedimento en esa costa.
- **Costos: no se encontró ningún costo de refulado de playas por metro cúbico.**
- **Permisos:** los de la sección A4.
- **Uruguay: no se llegó a investigar.** Se agotó el cupo de búsquedas.
- **Y, sobre todo, el agua.** Una playa donde no se puede entrar al agua es un solárium. En la costa de San Isidro,
  **ninguna** de las 35 muestras de 2021 a 2025 fue apta. **[V]** Y en 2023, 2024 y 2025, 0% de los sitios de toda la
  costa monitoreada entró en la categoría "Apta". **[V]**

### C4 · La calidad del agua

| Estación | Qué muestra |
|---|---|
| SI023, Perú Puente | Siempre la peor. *E. coli*: 48.000 (abril de 2024), 96.000 (noviembre de 2024), 2.000.000 (abril de 2025) y 55.000 (noviembre de 2025). El CSV de 2025 no trae unidades en el encabezado; los anteriores dicen UFC por 100 ml. |
| SI022, Reserva Ecológica | Entre 300 y 6.000. |
| SI024, Playa Espigón de Pacheco | Entre 300 y 7.000. |
| SI021, Espigón La Farola | Casi sin medición: "en obra" en 2023. |

Fuente: la red de monitoreo de la Subsecretaría de Ambiente de la Nación con los municipios costeros, publicada en
CSV. **[V]** Las estadísticas se recalcularon para este informe desde los CSV.

- **Valor guía.** 126 *E. coli* por 100 ml, según la Resolución 42/2006 de la Autoridad del Agua para la franja
  argentina del río, y 126 *E. coli* o 33 enterococos, según las directrices del Ministerio de Salud de 2017. **[V]**
- **Cloacas.** La Planta Depuradora Norte de AySA, en San Fernando, recibe los efluentes de Tigre, San Fernando y San
  Isidro. Llegó a su capacidad de 1,8 m³ por segundo en 2018-2019 y vuelca al Reconquista. Una ampliación la llevaría a
  2,8. **[V]**, en la evaluación de impacto ambiental de 2021. **No se encontró el estado de la obra ni una fecha para
  que mejore el agua.**

---

## D · Lo regional

| Organismo | Norma | Qué tiene que ver con la costa de San Isidro |
|---|---|---|
| **ACUMAR** | Ley 26.168 | **Nada.** San Isidro no está en la cuenca. **[V]** |
| **Comité de Cuenca del Reconquista** | Ley 12.653 | San Isidro está en la Cuenca Baja: los desagües de Boulogne van al Reconquista. Con CEAMSE opera barreras en Tigre. No abarca la costa del Río de la Plata. **[V]** |
| **Comité de Cuenca del Luján** | Ley 14.710 | No se verificó si San Isidro integra la cuenca. **[SC]** |
| **Comisión Administradora del Río de la Plata** | Tratado de 1973 | Hace estudios de contaminación y recibe la comunicación de obras (art. 17). No limpia. **[V]** |
| **FREPLATA** | Programa de Acción Estratégico, 2007 | Su acción 5 es "disminuir los aportes de residuos sólidos urbanos" con una "red de municipios costeros". Prioridad muy alta. No se encontró ninguna evaluación de lo hecho. **[V]** |
| **CEAMSE** | Decretos-Leyes 8782/77 y 9111/78 | Recibe por ley lo que recoge San Isidro. Ese costo va en cualquier presupuesto. **[V]** |

**Convenios de San Isidro con los vecinos sobre la costa o la basura: no se encontró ninguno.** **[V]**, como ausencia
en el Boletín 2002-2026.

Sí hay un modelo que funcionó: el convenio de 2016 con Vicente López por la calle Paraná. Vicente López armó el pliego y
licitó, y se creó un "Comité de Coordinación" entre los dos. Lo convalidó la Ordenanza 8935. **[V]**

**El camino para un convenio con los vecinos:**

1. **Convenio entre municipios** (San Isidro, Vicente López, San Fernando, Tigre): lo firman los intendentes y cada
   Concejo lo autoriza por ordenanza (Ley Orgánica de las Municipalidades, art. 41). **[V]**
2. **Si se quiere un ente propio**, un consorcio de la Ley 13.580, con estatuto y ordenanza de cada municipio. **[V]**
   Si sirve para un objeto ambiental es una interpretación: hay que consultar a la Asesoría General de Gobierno.
3. **Con la Provincia** (Ambiente, Infraestructura o el Comité de Cuenca) **no hace falta autorización del Concejo**
   (art. 41). **[V]** San Isidro igual llevó al Concejo el convenio de la costa.
4. **Con la Nación** hace falta autorización previa de la Provincia (art. 42). **[V]**
5. **Con la Ciudad**, por el texto del art. 41, hace falta el Concejo **[P]**; del lado de la Ciudad, la Legislatura
   **[SC]**.
6. **Para un esquema de toda la región**, un acuerdo entre la Provincia y la Ciudad, aprobado por la Legislatura
   bonaerense (Constitución provincial, art. 144). **[V]** El precedente es el CEAMSE de 1977.

---

## E · Los costos

**Advertencia.** No hay un solo presupuesto de referencia para San Isidro. Lo que sigue son órdenes de magnitud armados
con contratos reales, llevados a pesos de diciembre de 2025. **Todo es [CP].**

| Componente | Precedente | Instalación | Funcionamiento por año |
|---|---|---|---|
| **1. Medir.** Conteo de basura en tramos fijos, dos veces por año y después de cada sudestada, y pesaje de todo lo que se retira | No hay precedente de costo en San Isidro | Casi nada: balanza y protocolo | Bajo, si lo hace la cuadrilla. **Sin fuente** |
| **2. Cámaras con IA** en 2 o 3 bocas | Ballona las usa, sin costo publicado | **Sin dato** | **Sin dato** |
| **3. Redes en los desagües chicos y medianos** (unas 10 bocas) | Marin County: US$27.300 por red y año | Depende del caudal, que no se conoce | 10 × 39,5 M = **unos 395 M** |
| **4. Servicio de limpieza de desembocaduras y costa** | San Isidro, desagüe de Perú, 2015: $2,1 M por año de entonces | — | **Unos 323 M** por cada boca atendida como en 2015 |
| **5. Barreras con vaciado en las bocas grandes** (Perú, Alto Perú) | ACUMAR, arroyos críticos: 4 puntos más un equipo móvil | Incluido en el contrato | **Unos 2.124 M** por los 4 puntos; unos 530 M por punto, si se reparte parejo |
| **6. Cuadrilla de costa** con protocolo para juncales | La Ciudad, margen del Riachuelo (18 km): 89 M por año | Bote, herramientas | **89 a 323 M**, entre el precedente de la Ciudad y el de Perú |
| **7. Relevamiento con dron** después de sudestadas | Báltico: €36.600 por año | — | **Unos 62 M** |
| **8. Estudio de cómo se mueve el sedimento**, antes de hablar de arena | No se encontró precedente de costo | **Sin dato** | — |
| **9. Disposición final en CEAMSE** | La tarifa por tonelada está en el informe 12 | — | Poca: 50 a 100 t por año son menos del 0,1% de las 185.057 t que ya se recogen **[CP]** |

**¿Entra en los 3.455 M más por año para ambiente?** **Sí, pero se come una parte grande.**

| Paquete | Qué incluye | Cuánto cuesta por año | Parte de los 3.455 M |
|---|---|---|---|
| **Mínimo** | Medición, cuadrilla y un servicio de limpieza en la boca de Perú, como el de 2015 | Unos 400 M (89 + 323 M, más medir) | **~12%** |
| **Completo** | El mínimo, más barreras con vaciado en las dos bocas grandes y drones | Unos 1.900 M (89 + 395 + 323 + 1.060 + 62 M) | **~55%** |
| **La arena** | No se puede costear | **Sin dato** | — |

La arena no se puede costear: no hay estudio ni precio de referencia.

**El dato que falta para cerrar la cuenta:** el caudal de cada desagüe y cuánto entra el río en ellos con una
sudestada. Sin eso, las redes y las barreras no se pueden dimensionar.

---

## Preguntas abiertas

1. **El texto del convenio de las 50 hectáreas** (CONVE-2026-19-SI-DELE) y el plano de las 15 parcelas. Cuál es el
   plazo real y si dice algo sobre la limpieza. Se puede pedir por un concejal o por acceso a la información.
2. **Qué cuenta la meta "Limpieza de la costa (cantidad)"**, quién hace esas limpiezas y cuánto se pesa. En 2015 se
   pesaba: 50 t después de una sudestada.
3. **Si siguen las redes del desagüe de la calle Perú**, y por qué se dejó de contratar esa limpieza después de 2017.
4. **El caudal de diseño de cada desagüe y el plano oficial de las bocas.** Hay un "Mapa de obras hidráulicas del
   Partido" que cita una evaluación de impacto ambiental de 2020.
5. **Qué descarga en la calle Perú**, que es siempre el peor punto: 2.000.000 *E. coli* en abril de 2025.
6. **El estado de la ampliación de la Planta Depuradora Norte**, y qué parte de San Isidro vuelca en otras cuencas.
7. **El rol de Prefectura** y de la autoridad nacional de vías navegables en una obra en el río, y si el art. 17 del
   Tratado alcanza obras dentro de la franja de 2 millas.
8. **La historia**, en el Museo Beccar Varela: las Memorias del Jockey Club de 1926 a 1935 y el libro de Kröpfl de
   2005, sobre los balnearios. Es donde podría aparecer, o no, algo sobre la arena del hipódromo.
9. **Los precedentes uruguayos de reposición de arena** (Montevideo, Canelones): no se llegó a investigar.
10. **De qué es hoy la "Playa Espigón de Pacheco".** Una muestra del material de la orilla sería barata.

---

## Borrador de la propuesta

> **BORRADOR — para discutir, no para el documento todavía.** Todo lo que sigue sale de este informe. Las cifras son
> órdenes de magnitud [CP].

**La costa se limpia en la boca del caño, no sólo en la orilla.**

**Hoy:** el Municipio organiza jornadas con voluntarios y se fija una meta de sesenta limpiezas por año, pero no mide
qué junta. No hay un solo estudio de cuánta basura llega a la costa de San Isidro ni de dónde viene. Y el agua no es
apta para bañarse en ningún punto: ninguna de las 35 muestras oficiales de los últimos cinco años.

**Propuesta:**

1. **Medir primero, y publicarlo.**
   - Conteo de basura en tramos fijos de costa, con el mismo método dos veces por año y después de cada sudestada.
   - Pesaje de todo lo que se retira.
   - Cámaras en las dos o tres bocas más grandes.
   - Sin eso, cualquier número es un anuncio.
2. **Cortar la basura en la boca de los desagües.**
   - Redes o rejas en las bocas chicas.
   - Barreras con vaciado después de cada lluvia en las dos grandes, Perú y Alto Perú.
   - El Municipio ya lo hizo en la calle Perú entre 2014 y 2017, y lo dejó de hacer.
3. **Una cuadrilla de costa permanente**, con un operativo después de cada sudestada y un protocolo para no destruir
   el juncal. Cómo se contrata, sin chocar con el contrato de recolección, se define con el informe 12.
4. **Un acuerdo con los vecinos del río.**
   - Convenio con Vicente López, San Fernando y Tigre, como el de la calle Paraná de 2016: un Comité de Coordinación y
     un método común de medición.
   - La costa es una sola, y lo que no se mide de los dos lados de la calle Paraná no se puede discutir.
5. **La arena, sólo con estudio.**
   - El programa no promete playa.
   - Promete el estudio de cómo se mueve el sedimento frente a San Isidro y el seguimiento público de la calidad del
     agua.
   - Hasta que el agua no sea apta, una playa de arena sería un solárium con carteles de prohibido bañarse.

**Cuánto cuesta:** entre 400 y 1.900 millones por año según el alcance, dentro de los 3.455 millones más por año que el
programa suma a ambiente.

**Qué no dice este borrador, a propósito:** que el 70% de la basura es plástico, porque ese dato es de Rosario; que la
arena se llevó al hipódromo, porque no hay prueba; y que la basura viene de afuera, porque nadie lo midió.

---

## Método y límites

- **Cinco investigaciones en paralelo:**
  1. diagnóstico institucional e hidrológico;
  2. basura: datos y origen;
  3. tecnología;
  4. precedentes argentinos y organismos regionales;
  5. arena, historia y calidad del agua.
- **Lo verificado por segunda vez para este informe**, en la fuente descargada:
  - la frase del 70% en las dos notas;
  - la cita de Posse;
  - las 50 t de 2015;
  - la meta de limpieza de la costa y las 185.057 t en la Situación económico-financiera 2025;
  - el contrato de 2015 del desagüe de Perú;
  - las citas clave de la evaluación de la barrera de burbujas, del informe del INA sobre el Riachuelo y del documento
    de Ballona;
  - la página del Hipódromo;
  - el artículo de Ríos (2023);
  - las estadísticas de *E. coli*, recalculadas desde los CSV.
- **El sitio del Municipio** manda su certificado sin la cadena intermedia. Se completó con el certificado intermedio
  público de Sectigo; la verificación siguió activa.
- **Se agotó el cupo de búsquedas web** de cada investigación antes de terminar. Quedaron sin buscar:
  - los precedentes uruguayos de arena;
  - los costos de refulado;
  - Tijuana, Newport Beach y otros sitios de barreras;
  - parte de la prensa local.
- **Archivos de más de 20 MB no se guardaron**; su URL está en `FUENTES.txt`:
  - el Informe al Congreso de ACUMAR 2024;
  - el diagnóstico de FREPLATA;
  - la evaluación de impacto ambiental de la Planta Norte;
  - los informes de COMIREC 2021 y 2022.
- **Los 1.054 números de *Caras y Caretas*** que se revisaron (unos 330 MB) tampoco se subieron. Están en archive.org, y
  en `01_raw/costa/c_arena/caras_y_caretas_ocr/` quedaron los textos de los números citados.
