# 16 · Limpiar el agua y la costa, de verdad

Investigación. 1 de octubre de 2026. Rama `claude/cool-hopper-3hdk58`. **El documento no se toca.** Completa los informes
11, 14 y 15, y corrige tres puntos de ellos (ver "Correcciones").

**Estado: para decidir.** Al final va un **borrador** de propuesta, marcado como tal.

**Por qué.** El cliente descartó la playa seca: es cara y se arruina. El eje es otro: que deje de entrar mugre y cloaca
al río, que la costa esté limpia y linda, y que la gente la siga usando. El agua contaminada no puede ser excusa para
cerrar el río: hay que recuperarlo.

**Marcas:**

- **[V]** verificado: se leyó en la fuente primaria.
- **[P]** probable: fuente secundaria seria.
- **[SC]** sin confirmar.
- **[CP]** cálculo propio, con la cuenta a la vista.
- **[I]** inferencia: razonamiento de este informe, no de una fuente.
- *Según X*: lo dice el propio organismo, empresa o club; no es un dato verificado.

**Montos.** En la moneda original, con su año. Entre paréntesis, un orden de magnitud en pesos, con el tipo de cambio
que usa el programa: **$1.447,84 por dólar** y **1,1709 dólares por euro** (diciembre de 2025). Esa conversión no corrige
la inflación de otros países: sirve para comparar tamaños, no como precio.

**Regla de este tema.** No se pidió nada que cueste plata ni que haya que ir a buscar en persona. No se contactó a nadie.
Las fuentes se consultaron el 01/10/2026 y están en `01_raw/agua/`, con `FUENTES.txt`.

---

## Resumen

### Lo que es cierto

**La cloaca**

- **El desagüe de la calle Perú es el peor punto de toda la costa norte.** Las 31 muestras de *E. coli* tomadas entre
  2016 y 2025 superan el valor guía para bañarse (126 por 100 ml). La mediana es 19.000; entre 2021 y 2025, 37.000; el
  máximo, 2.000.000, del 09/04/2025. **[V]** / **[CP]**, recalculado desde los CSV oficiales.
  - Además tiene poco oxígeno y mucho amonio, que es lo que se espera de un aporte cloacal. **[CP]** / **[I]**
- **Es un conducto pluvial grande, de tres partidos.** Mide 5,50 m de diámetro, empieza en Villa Adelina, sigue por
  Dardo Rocha y Perú y sale al río con dos bocas de 3,20 × 3,20 m (*La Nación*, 08/01/2007). **[V]** que lo dice
  - *Según el Municipio*, trae agua "pluvial y/o servida" de San Martín, Vicente López y San Isidro.
- **La ley ya obliga a AySA a eliminar las conexiones cloacales clandestinas a los pluviales.** El Marco Regulatorio,
  hoy ordenado por el Decreto 805/2025, dice tres cosas **[V]**:
  - AySA "incluirá en el Plan de Acción… un programa que permita eliminar las conexiones clandestinas cloacales a
    conductos pluviales" (art. 16 d);
  - las sobrecargas de la cloaca "no deberán generar vertidos a la red pluvial" (art. 16);
  - el usuario debe "mantener el funcionamiento independiente de las instalaciones cloacales internas respecto de las
    pluviales" (art. 61 j).
  - **Ese programa no se encontró.**
- **El Municipio tiene poder para actuar.** La Ley provincial 5965 dice que las municipalidades "ejercerán la
  inspección", ejecutarán "de oficio y por cuenta de los propietarios" los trabajos necesarios, podrán clausurar
  (art. 7) y cobrar multas (arts. 8 y 9). **[V]**
- **Los pluviales no son de AySA.** Su contrato de concesión de 2026 los deja afuera, salvo el radio antiguo de la
  Ciudad, y también deja afuera "el control de la contaminación". **[V]**
- **La Planta Depuradora Norte de AySA, adonde va parte de la cloaca de San Isidro, ya está al límite.** Se diseñó para
  1,8 m³ por segundo y trata unos 2 *según AySA*. Su tercer módulo, financiado por el Banco Mundial, estaba "mayormente
  paralizado" en diciembre de 2024. **[V]**
- **Cobertura de cloaca en San Isidro:** 94,1% de los hogares (Censo 2022) **[CP]**; 94,47% de la población *según
  AySA* (2023). Lo que falta se concentra en La Cava. **[CP]**

**La basura**

- **El sargazo del Caribe dejó un precedente de barreras en costa abierta, pero funcionan a medias.**
  - Aun con barrera, "around 30–60% of the algae may still reach the beach" (Chávez y otros, 2020). **[V]**
  - En Guadalupe, una barrera desvió el 60% hasta que una tormenta con olas de más de 2,5 m la destruyó (2023). **[V]**
  - La evaluación oficial francesa de 2025 dice que juntar en tierra "apparaît plus efficiente" que juntar en el mar.
    Juntar en la playa costó **104 a 133 € por tonelada**; en el mar, de **1.035 € bajó a 296 €**. **[V]**
- **Los robots recolectores no tienen evaluaciones independientes.** Su ficha los limita a agua calma: el WasteShark
  soporta olas de 0,5 m como máximo, *según la empresa*. **[V]** que lo dice
- **Las cámaras con IA en ríos ya funcionan para medir.** Un estudio de 2026 en 11 sitios dio **74%** de precisión
  para plásticos, de día y con marea. **[V]**
- **El Plan de Manejo de Ribera Norte (2012) ya pedía una barrera en la boca de Perú**: "Esto debe ser una de las
  prioridades para el Municipio". **[V]**

**El agua y el río**

- **La Ordenanza 5304 de 1978 prohíbe "tomar baños" en todo el río del partido.** Se leyó el texto. No menciona los
  deportes náuticos. Figura en el Digesto vigente. **[V]**
- **El Municipio enseña kite, windsurf, SUP, kayak y vela en el río**, en el Campo Municipal de Deportes N° 9. **[V]**
  *según el Municipio*
- **En lo sanitario, el windsurf cuenta como nadar.** Las directrices del Ministerio de Salud (Res. 125/2016) ponen
  "Surfeo a vela" en exposición **alta**, junto a natación y surf. Remo, canotaje, vela y kayak van en **moderada**.
  **[V]**
- **Los sistemas de aviso que funcionan tienen tres cosas:** muchos años de datos por sitio, lluvia medida en tiempo
  real y un aviso simple. Sídney acierta el **93%** de los días (2025-26). **[V]**
- **Hoy en San Isidro un aviso diría "no apto" casi siempre:** las 35 muestras de 2021-2025 superan el valor guía.
  Además, se toman sólo 2 a 4 muestras por año, y desde noviembre de 2024 sólo en Perú. **[V]** / **[CP]**

**Los parques**

- **Bosque Alegre tiene protección legal y una historia de rellenos con basura documentada en actos oficiales.**
  - El Decreto 910/2012 dice que el predio vecino "era un bañado rellenado con residuos domiciliarios". **[V]**
  - El mismo decreto declaró **Paisaje Protegido** a Bosque Alegre (lo convalidó la Ordenanza 8651). **[V]**
  - No se encontró ningún estudio de suelo ni de contaminación.
- **La tierra de la costa es de la Provincia y la administra el Municipio.** Las parcelas del Campo de Deportes N° 6 y de
  Roque Sáenz Peña y el río tienen como "titular registral la Provincia de Buenos Aires". **[V]**
- **Con los precios del propio contrato municipal, un sendero de tosca cuesta un quinto que uno de hormigón.** **[CP]**

**El plan con la Provincia**

- **No existe ningún plan ni mesa sobre la calidad del agua en la costa norte.** Lo único es una red nacional de
  monitoreo (RIIGLO, Res. 520/2014) que mide desde 2004, sin metas ni obras. **[V]**
- **La Autoridad del Agua puede crear por resolución, sin ley, un comité de cuenca para la costa.** Ya lo hizo para
  Berazategui, Quilmes y Florencio Varela (Res. ADA 541/2018). **[V]**
- **San Isidro ya tiene un asiento en la comisión asesora que planifica las obras de AySA** (APLA, art. 37 del marco).
  **[V]**

### Lo que no es cierto, o hay que corregir

- **"El Aliviador Alto Perú tiene que ver con el desagüe de Perú": no.** El Alto Perú desagua el centro de Beccar y
  sale a la Dársena Gauto y Pavón, a unos 3,3 km. **[V]** (Decreto 491/2026) / **[CP]**
- **"Ningún equipo funciona en una costa abierta" (informe 11): hay que matizarlo.** Las barreras de sargazo están en
  costa abierta, pero dejan pasar del 30 al 60% y se rompen con temporales. **[V]**
- **"El Interceptor cuesta €700.000" (informe 11, *según la ONG*): los nuevos de Los Ángeles costarían US$5 a 8 M cada
  uno, más US$3 a 4 M por año de operación**, según funcionarios citados por el *Los Angeles Times*. **[P]**
- **"El monitoreo de la Ciudad dio 0% de sitios aptos" (informe 15, F4): el dato es de la red nacional**, no de la
  Ciudad. El CIAM es el centro de información de la Subsecretaría de Ambiente de la Nación. **[V]**
- **La Ordenanza 5304 pasa de [P] a [V]** (informes 11 y 15): se leyó el texto.
- **El "humedal en la boca" no alcanza para Perú.** Para pasar de 2.000.000 a 126 hay que dividir por 15.873. Los
  humedales medidos sacan entre 0,2 logaritmos y 75%, y la luz ultravioleta en un canal de California sacó entre 63% y
  78%; la playa siguió cerrada igual. **[V]** / **[CP]**

### Lo que no está verificado

- **Por qué hay cloaca en el desagüe de Perú.** Ningún estudio lo dice: puede ser conexiones de casas, pérdidas de la
  red de AySA o desbordes. **[SC]**
- **Quién construyó el conducto de Perú y de quién es.** No hay norma ni acto que lo diga. Que lo opera el Municipio es
  **[I]**: pagó la limpieza de la boca entre 2014 y 2017.
- **Si la muestra de 2.000.000 se tomó con o sin lluvia.** Los datos no lo dicen, y las coordenadas publicadas de la
  estación están mal. **[V]** el problema
- **Quién tiene el poder de policía sobre una conexión clandestina en el área de AySA**: la Nación (art. 122 del
  marco) o el Municipio y la Autoridad del Agua (Ley 5965 y Código de Aguas). Hace falta una opinión legal.
- **Qué pasó con la ampliación de la Planta Norte después de mayo de 2026.**
- **Cuánta gente usa el río.** Ningún club ni escuela publica socios o alumnos. *Según el Municipio*, más de 400
  navegantes en el campeonato de clubes de 2026.
- **Cuánto cuesta una cámara con IA instalada.** No se publica.
- **La lista de las 15 parcelas del convenio de 2026.** No se publicó.

---

## La tabla de tecnologías

Ordenadas por los cinco ejes del borrador. "Resultado" es lo medido por un tercero, salvo que diga *según la empresa*.

| Tecnología | Qué hace | Dónde y cuándo | Resultado medido | Cuánto cuesta | ¿Sirve en San Isidro? | Marca |
|---|---|---|---|---|---|---|
| **Cortar la cloaca** | | | | | | |
| Recorrido de bocas en tiempo seco + indicadores simples (amonio, potasio, detergentes, conductividad) | Encuentra qué bocas traen agua cuando no llueve y si es cloaca | Manual de la EPA de EE.UU., 2004 | Toronto: 59% de las bocas con caudal seco, 14% "muy contaminadas" | US$2 a 35 por parámetro en laboratorio; US$5.700 a 12.800 por campaña (2004) | **Sí. Es el primer paso** | **[V]** |
| Marcador de cloaca humana (HF183, por ADN) | Confirma que la materia fecal es humana | California, Países Bajos, Sídney | Países Bajos: tras reparar conexiones, la *E. coli* no bajó pero el HF183 sí (2023) | US$100 a 300 por muestra (2013). 40 muestras: US$4.000 a 12.000 ($5,8 a 17,4 M) | **Sí**, para el diagnóstico de Perú | **[V]** |
| Sensores baratos en cámaras (nivel, temperatura, conductividad) | Registran cuándo hay descarga en tiempo seco | Melbourne, 2021 | 22 sensores durante un año detectaron descargas de minutos a horas | ~US$25 por sensor | **Sí**, para acotar el tramo | **[V]** |
| Cámara dentro del caño (CCTV) | Ve los caños que entran y las descargas | Ciudad de Buenos Aires con ACUMAR, 2015 | 520 operativos, **233 conexiones industriales clandestinas** detectadas | US$6,6 a 16,4 por metro (Michigan, 2023) | **Sí**, para confirmar | **[V]** |
| Colorante y humo | Prueban qué inodoro o pileta va al pluvial | Wayne County (EE.UU.), 1987-2009 | 2.496 conexiones ilícitas en 611 de 8.858 establecimientos; 552 corregidos | US$900 por establecimiento (2003) | **Sí**, al final, casa por casa | **[V]** |
| Programa completo con subsidio | Detectar, intimar y subsidiar la corrección | París, 2019-2024 | 4.500 conexiones corregidas a dic-2022, de 23.000 estimadas; a jul-2024, 30.000 a 40.000 habitantes dejaron de volcar al río | Hasta €6.000 por vivienda ($10,2 M), después el 100% | **Sí, como modelo** | **[V]** *según la Prefectura* |
| Desviador de tiempo seco | Manda a la cloaca el agua del pluvial cuando no llueve | Marquez, Los Ángeles, 2006 | Casi sin excedencias de bacterias en la temporada seca de 2007 | US$1,4 M por boca ($2.027 M) | **Condicional**: necesita que AySA acepte el caudal y que la Planta Norte tenga lugar | **[V]** |
| Colector costero | Intercepta los desagües a lo largo de la costa y los lleva a tratamiento | Montevideo, Plan de Saneamiento Urbano I (1981-1991) | Recuperó las playas de Carrasco a Punta Carretas *según la Intendencia*; 2023-24: todas las habilitadas en "Muy buena" | Plan IV: US$220 M del BID más US$40 M locales | **Escala AySA**, no municipal | **[V]** |
| Colector Margen Izquierdo (AySA) | Intercepta el caudal de tiempo seco de los pluviales de la Ciudad que van al Riachuelo | Ciudad de Buenos Aires, 2015-2022 | No se encontró la mejora medida en el agua | Lote 1: $42.571 M (sin año base) | **Muestra que AySA ya lo hizo** | **[V]** |
| Humedal en la boca | Sedimentación y sol | Revisiones de EE.UU. | Entre 0,2 log y 75% de remoción; a veces **aporta** bacterias | No se encontró por hectárea | **No como solución principal** | **[V]** |
| Luz ultravioleta en el canal | Desinfecta | Poche Beach, California, 2004 | Sacó 63 a 78%; la playa siguió cerrada igual | ~US$130.000 ($188 M) | **No** | **[V]** |
| **Frenar la basura** | | | | | | |
| Cuadrilla de costa con bote | Junta a mano, entra al juncal | San Isidro, Ciudad, ACUMAR | Ver informe 11 | Ver informe 11 | **Sí. Es lo único que llega al juncal y a la piedra** | **[V]** |
| Red o reja en la boca del desagüe | Retiene lo que sale del caño | San Isidro (Perú, 2014-2017), Australia | Ver informe 11 | Ver informe 11 | **Sí** | **[V]** |
| Barrera flotante simple | Encierra la basura en una dársena o boca | ACUMAR, arroyos de todo el mundo | 0% de retención de bolsas finas (ensayo INALI) | US$697 a 1.052 por 3 a 6 m de barrera (2021) | **Sí, como complemento**, con vaciado diario | **[V]** |
| Barrera de sargazo en costa abierta | Desvía o retiene el alga antes de la playa | Quintana Roo, Guadalupe, Martinica | Pasa igual del 30 al 60%; una se destruyó con olas de 2,5 m | Guadalupe: €200.000 por 350 m (~$1 M por metro) | **Sólo el método** (estudiar corrientes, vaciar siempre, retirar antes del temporal) | **[V]** |
| Recolección en tierra (sargazo) | Palas, camiones y cuadrillas | Saint-Martin, Saint-Barthélemy, 2023-2025 | 10.630 t en 2024 en Saint-Martin | **104 a 133 € por tonelada** ($176.000 a 225.000) | **Como referencia de costo** de la cuadrilla | **[V]** |
| WasteShark (robot flotante) | Junta basura en agua calma | Puertos y canales | "500 kg por jornada", *según la empresa*. Sin evaluación independiente | €23.500 por unidad ($39,8 M), *según la empresa* | **Sólo en dársenas**: olas de 0,5 m como máximo | **[V]** la ficha; **[SC]** el rendimiento |
| Interceptor (The Ocean Cleanup) | Catamarán en el cauce de un río | Los Ángeles, Kingston, Guatemala, Asia | Ballona: 193,5 t cortas entre oct-2022 y may-2026, *según la ONG* | US$5 a 8 M por unidad y US$3 a 4 M por año (Los Ángeles, 2026) | **No**: los desagües no tienen corriente constante | **[P]** |
| Rueda de basura (familia Mr. Trash Wheel) | Rueda que lleva la basura a un contenedor | Baltimore, Newport Bay (2025) | Newport: ~80% de lo que junta es material vegetal | Newport: US$5,5 M ($7.963 M) | **Condicional**: sólo en una boca con caudal y agua abrigada | **[V]** / **[P]** |
| Barrera de burbujas | Cortina de burbujas que desvía la basura | Ámsterdam y otros 4 sitios | Westerdok: ~1 t de plástico por año | €76.453 por tonelada (informe 11) | **No**: necesita caudal constante | **[V]** |
| Seabin, BeBot, Clearbot | Tacho flotante en marinas; robot de arena; bote autónomo | Marinas, playas de arena, puertos | Sólo cifras de las empresas | Seabin AUD 37.000 por unidad y año; BeBot ~US$80.000 | **No** | **[SC]** |
| Cámara con IA en la boca | Cuenta la basura que pasa | 11 sitios en ríos con marea, 2026 | 74% de precisión para plásticos; bolsas 51%; botellas 33% | **No se publica** | **Sí, para medir** dónde y cuándo entra | **[V]** |
| Satélite | Ve manchas de algas o basura desde el espacio | Sargazo; camalotes en el Río de la Plata (2016) | Sólo acumulaciones de más de ~100 m² | Imágenes gratis | **Sólo para llegadas grandes de camalote** | **[V]** |
| **Informar la calidad del agua** | | | | | | |
| Pronóstico por lluvia (Beachwatch, Sídney) | Modelo por sitio entre bacterias y lluvia; pronóstico 2 veces por día | 160 sitios, 2025-26 | **93%** de días correctos | AUD 18,5 M en 10 años **[P]** | **Más adelante**: exige ~100 muestras por sitio | **[V]** |
| Análisis rápido por ADN (Chicago) | Resultado en 3-4 horas, en el día | 22 playas, 2025 | El modelo anterior detectaba sólo el 7 al 12% de los días malos (2015-16) | 2 a 5 veces un análisis común | **Posible**, con una universidad | **[V]** |
| Sensores rápidos aguas arriba + banderas (París) | Alerta en 15-20 minutos y cierre preventivo tras lluvia | Sena, 2025-2026 | Abrió 2/3 de los días en 2025; clasificación europea "insuficiente" | Plan de obras: ~€1.300 M desde 2016 | **El método sí; la escala no** | **[V]** |
| Bandera sanitaria y monitoreo frecuente (Montevideo) | Muestras hasta 4 veces por semana en verano | 19 playas | La regla "24 h después de lluvia" acierta 82%, pero detecta 40% de los excesos | No publicado | **Sí, como primer paso** | **[V]** |

---

## 1 · La cloaca que entra al río

### 1.1 El desagüe de la calle Perú

| Tema | Lo que se sabe | Marca |
|---|---|---|
| Nombre | "Canal aliviador del arroyo Pavón superior" *según el Municipio* (2017). En OpenStreetMap, "Desagüe Dardo Rocha" | **[P]** / **[SC]** |
| Recorrido | Empieza en Mazza y Moreno, Villa Adelina; sigue por Dardo Rocha y Perú hasta el río | **[V]** que lo dice *La Nación* (2007) |
| Tamaño | 5,50 m de diámetro; dos bocas de 3,20 × 3,20 m | **[V]** que lo dice *La Nación* (2007) |
| Boca | Perú y el río, junto a Perú Beach, "a la altura del puente de madera" | *Según el Municipio* |
| Cuenca | Partes de San Martín, Vicente López y San Isidro. Superficie y caudal: **no encontrados** | *Según el Municipio* |
| Quién lo hizo y de quién es | **No encontrado.** La Ley Orgánica de las Municipalidades (art. 52) pone los pluviales a cargo del Municipio "siempre que su ejecución no se encuentre a cargo de la Provincia o de la Nación" | **[V]** la ley |
| Qué paga hoy el Municipio | Limpió la boca entre 2014 y 2017 (Decretos 4017/2014 y 1802/2015; LP 121/2017). En 2026 dice limpiar "más de 540 metros de desembocaduras" | **[V]** / *según el Municipio* |
| Cobertura de cloaca cerca del recorrido | 97,2% de los hogares en los radios a menos de 300 m. En el radio de la boca, 82,6% (55 de 316 hogares sin red) | **[CP]**, Censo 2022 |
| Por qué hay cloaca | **No hay estudio.** El dueño de un club dijo en 2017: "se suman las cloacas clandestinas de miles de personas" | **[SC]** |
| Qué obra haría falta según alguna fuente | **Ninguna fuente lo dice.** El Plan de Manejo de 2012 pidió una barrera de basura en la boca (proyecto 17), no una obra para la cloaca | **[V]** |

**Calidad del agua en Perú (estación SI023).** 31 muestras de *E. coli*, 2016-2025: mediana 19.000, media geométrica
19.977, máximo 2.000.000 (09/04/2025); las 31 superan 126. Enterococos: mediana 4.600 (21 muestras). Oxígeno disuelto,
mediana 2021-2025: 3,3 mg/l, contra 6,4 en la Reserva. Amonio: 2,9 mg/l, contra 0,75. **[CP]**, recalculado desde los CSV
de la red nacional; la serie de *E. coli* se recalculó dos veces, por separado, con el mismo resultado.

### 1.2 Las demás desembocaduras con datos

*E. coli* por 100 ml. Recalculado desde los CSV de la red nacional (RIIGLO). El conteo es por muestra; la norma usa la
media geométrica. **[CP]**

| Estación | Sitio | Muestras | Años | Mediana | Máximo | Sobre 126 |
|---|---|---|---|---|---|---|
| **SI023** | **Perú Puente** | 31 | 2016-25 | **19.000** | **2.000.000** | **31/31** |
| SI024 | Playa Espigón de Pacheco | 28 | 2016-24 | 3.750 | 32.500 | 27/28 |
| SI022 | Reserva Ecológica | 30 | 2004-24 | 1.000 | 17.200 | 28/30 |
| SI021 | Espigón La Farola | 15 | 2004-24 | 500 | 1.300 | 14/15 |
| VL031 | Vicente López, Costa y Melo | 34 | 2004-25 | 7.450 | 180.000 | 32/34 |
| VL032 | Puerto de Olivos | 31 | 2004-24 | 4.000 | 28.100 | 30/31 |
| VL033 | Reserva Barrio El Ceibo | 30 | 2016-24 | 3.300 | 25.000 | 28/30 |
| SF015 | San Fernando, Del Arca | 26 | 2016-25 | 3.000 | 410.000 | 23/26 |
| TI005 | Río Tigre antes del Luján | 31 | 2004-24 | 7.700 | 48.000 | 30/31 |
| CA041 | Ciudad, Parque de los Niños | 26 | 2004-23 | 6.200 | 140.000 | 25/26 |

- **En 2025 sólo se midió Perú.** SI021, SI022 y SI024 figuran "sin medición" desde noviembre de 2024. **[V]**
- **Sólo Perú tiene un conducto identificado en una fuente.** Las demás estaciones no.
- Tabla completa (20 estaciones, con Tigre y enterococos): `01_raw/agua/1_cloaca_local/estaciones_calidad_costa_norte.csv`.

### 1.3 Cloacas y la Planta Norte

| Dato | Valor | Marca |
|---|---|---|
| Hogares de San Isidro con cloaca (Censo 2022) | 94,1% (103.777 de 110.265) | **[CP]** |
| Población con cloaca (AySA, 2023) | San Isidro 94,47%; Vicente López 98,69%; San Martín 82,10%; San Fernando 85,58%; Tigre 34,47% | *Según AySA* |
| A dónde va la cloaca de San Isidro | 28,58 km² al "Sistema Río de la Plata"; 18,83 km² al "Sistema Reconquista" (Planta Norte) | *Según AySA* |
| Dónde falta | 5 radios con menos del 50%, todos en La Cava (Beccar). La Cava drena probablemente al Alto Perú, no a Perú | **[CP]** / **[I]** |
| Planta Norte (San Fernando) | Diseño 1,8 m³/s; trata ~2 m³/s; vuelca al Reconquista | **[V]** / *según AySA* |
| Ampliación (tercer módulo, +1 m³/s) | Contrato de ~US$97,5 M "en proceso de adjudicación" (dic-2023). Préstamo BIRF 9207, US$300 M, "mayormente paralizado" (dic-2024), cierre previsto el 26/05/2026 | **[V]** |
| Lo que obliga el contrato de AySA de 2026 | Terminar la optimización de los módulos 1 y 2 de la Planta Norte en el primer ciclo tarifario. El tercer módulo **no aparece nombrado** | **[V]** |
| Desbordes cloacales en San Isidro | **No hay datos por partido.** AySA informa 14.443 desbordes en 2023 en toda su área | *Según AySA* |

### 1.4 Cómo se encuentran y se cortan las conexiones

**El orden que propone el manual de la EPA de EE.UU. (2004)** **[V]**:

1. Recorrer las bocas cuando no llueve y ver cuáles traen agua.
2. Medir indicadores simples (amonio, potasio, detergentes, conductividad).
3. Subir de cámara en cámara para acotar el tramo.
4. Recién al final, colorante, humo o cámara, casa por casa.

**Encontrar cuesta más que corregir.** En Inglaterra y Gales se estimó £450 M para investigar todas las malas
conexiones y unos £50 M para corregirlas. **[P]** En EE.UU., corregir una conexión costaba en promedio US$2.500 (~2002).
**[V]**

**Quién paga.** Casi en todas partes, el dueño paga lo que está dentro de su terreno y el Estado subsidia para acelerar
**[V]**:

- **París**: hasta €6.000 por vivienda, después el 100% si la obra la hace el municipio. Desde 2022, la ley obliga a
  revisar la conexión al vender.
- **Uruguay** (Ley 18.840): plazo de 1 o 2 años para conectarse; multa mensual igual al consumo de agua; créditos y
  subsidios para hogares vulnerables.
- **Área de AySA**: el dueño instala "a su cargo" (Decreto 805/2025, art. 10). "Las jurisdicciones deberán establecer
  mecanismos que permitan asegurar la conexión". **No se encontraron subsidios.**

**En San Isidro no se encontró ninguna ordenanza ni programa sobre conexiones clandestinas al pluvial.** **[V]**, como
ausencia en el Boletín 2002-2026. Sí hay un convenio marco con AySA (Ordenanza 8894, 2016, cláusula octava) en el que el
Municipio se compromete a colaborar, "incluso por medio de sus facultades jurisdiccionales", para que los **nuevos**
usuarios de la red se conecten, cieguen sus pozos y no conecten sus pluviales internos a la nueva red cloacal. Las dos
partes dicen además que buscarán financiamiento para adecuar las instalaciones "en especial para los usuarios de menores
recursos". **[V]**

### 1.5 Obras en la boca

| Obra | Qué hace | Cuándo sirve | Costo | Marca |
|---|---|---|---|---|
| Desviador de tiempo seco | Manda a la cloaca el agua que baja sin lluvia | Sólo sin lluvia, y si la cloaca tiene lugar. Tiene que cerrarse con sudestada para que el río no entre a la cloaca **[I]** | US$1 a 1,4 M por boca (California); R$2,3 M por punto (Río de Janeiro) | **[V]** / **[P]** |
| Colector costero | Junta todas las bocas a lo largo de la costa | Es la solución de fondo de Montevideo | Cientos de millones de dólares | **[V]** |
| Humedal o UV en la boca | Trata el agua que sale | Como complemento, después de cortar la fuente | Ver tabla de tecnologías | **[V]** |

**Para Perú, en orden** **[I]**:

1. **Medir antes de cualquier obra.** Muestrear con tres días sin lluvia y después de llover: *E. coli*, HF183, amonio,
   potasio, detergentes, conductividad. Cruzar con la lluvia de cada día. Unos US$5.000 a 15.000 de laboratorio, más
   personal. **[CP]**
2. **Acotar aguas arriba**, cámara por cámara, con unos 20 sensores baratos (~US$500). Así se separa una conexión de una
   pérdida o un desborde de AySA. La cuenca es de tres partidos: hace falta Vicente López y San Martín.
3. **Si es la red de AySA**, la obligación está en el art. 16 del marco: se pide por el ente regulador (ERAS).
4. **Si son casas**, intimar y subsidiar, como París.
5. **Recién después, decidir si hace falta un desviador** en la boca, de acuerdo con AySA.

### 1.6 Quién es responsable de qué

| Acción | Responsable | Norma |
|---|---|---|
| Pluviales locales | Municipio, salvo que estén a cargo de la Provincia o la Nación | Ley Orgánica de las Municipalidades, art. 52 |
| Obras hidráulicas provinciales | Ministerio de Infraestructura de la Provincia | Ley 15.477, art. 27 |
| Red cloacal, tratamiento y desbordes | AySA, controlada por el ERAS | Decreto 805/2025, arts. 1, 3 y 16 |
| Programa para eliminar conexiones cloacales clandestinas a pluviales | AySA, dentro de su Plan de Acción | Decreto 805/2025, art. 16 d |
| Mantener separadas cloaca y pluvial en la casa, y conectarse | El vecino | Decreto 805/2025, art. 61 j y k |
| Poder de policía sobre las instalaciones de las casas | **No es AySA** | Decreto 805/2025, art. 2 |
| Permiso de vuelco y límite de coliformes (2.000 por 100 ml a un pluvial o río) | Autoridad del Agua | Ley 12.257, arts. 103 y 104; Res. ADA 336/2003 |
| Comprobar infracciones y recibir denuncias | Municipio, junto con la Autoridad del Agua | Ley 12.257, art. 166 ter |
| Inspeccionar, hacer la obra a cargo del dueño, clausurar y multar | **Municipio** | Ley 5965, arts. 7 a 9 |
| Control de la contaminación en el área de AySA | Subsecretaría de Ambiente de la Nación | Decreto 805/2025, art. 122 |

Todo **[V]** en el texto de cada norma. **Superposición sin resolver:** en el área de AySA hay a la vez autoridad
nacional (art. 122) y provincial y municipal (Ley 5965 y Código de Aguas). Antes de proponer multas municipales hace
falta una opinión legal.

---

## 2 · Lo más nuevo para sacar basura del agua

La tabla de tecnologías tiene los números. Lo que conviene saber para decidir:

- **El sargazo enseña el método, no el equipo.** Lo transferible es **[I]**:
  - estudiar las corrientes antes de poner una barrera (mal ubicada, "contre-productif", dice la evaluación francesa
    **[V]**);
  - pensar la cadena completa: barrera, vaciado, transporte, disposición y pesaje;
  - vaciar siempre (lo retenido se pudre en 24 a 48 h **[V]**) y poder retirar la barrera antes de un temporal.
- **Lo que no sirve en la costa abierta de San Isidro**: ningún robot, ninguna rueda, ningún Interceptor, ninguna
  barrera de burbujas. Todos necesitan agua calma o corriente constante. **[I]**, con base en las fichas y los casos
  **[V]**.
- **Las bolsas finas no las retiene ninguna barrera** (0% en el ensayo argentino del INALI) y las cámaras las detectan
  con 51% de precisión. **[V]**
- **El mejillón dorado** incrusta cualquier barrera fija en el Río de la Plata y obliga a limpiarla, como las ostras en
  Guadalupe. **[I]**
- **Un aviso propio sí es copiable**: pronóstico de sudestada del Servicio de Hidrografía Naval, lluvia y cámaras en las
  bocas, para mandar la cuadrilla a tiempo. **[I]**
- **Satélite:** en el Río de la Plata sólo se detectaron camalotes (2016). Que una llegada masiva de camalotes sirva como
  aviso de basura es una hipótesis que nadie midió. **[I]**

---

## 3 · Cuándo se puede entrar al agua

### 3.1 Cómo funcionan los sistemas de aviso

| Lugar | Cómo funciona | Cómo avisa | Precisión | Qué hizo falta |
|---|---|---|---|---|
| **Sídney (Beachwatch)** | Modelo por sitio entre enterococos y lluvia, con pluviómetros en tiempo real | Web, correo, redes; "contaminación improbable / posible / probable" | 93% de días correctos (2025-26) | Los últimos 100 resultados por sitio en 5 años o menos |
| **Chicago** | Antes, modelo; desde 2015, análisis por ADN con resultado en 3-4 h | Banderas verde, amarilla y roja | El modelo detectaba sólo el 7 al 12% de los días malos (2015-16) | Laboratorio universitario y muestreo diario temprano |
| **Directiva europea 2006/7/CE** | Perfil de cada sitio, mínimo 4 muestras por temporada, clasificación con 4 temporadas | Cartel junto al sitio con la clasificación y los días cerrados del año anterior | — | Es el modelo normativo |
| **Berlín** | Modelo con lluvia diaria y caudal del río | Mapa actualizado cada día | >90% de verdaderos positivos en 3 ríos alemanes (estudio de 2024) | Proyecto de €2,7 M, 2015-2019 |
| **Copenhague** | Sensores de nivel en cada aliviadero cada 15 minutos y modelo | Bandera roja, SMS, pronóstico a 3 días | 2002-2011: 30 días cerrados por 20 lluvias | Sensores en cada aliviadero |
| **París** | Laboratorio diario, sensores rápidos aguas arriba, cierre de 24 a 36 h tras lluvia | Banderas y web | 2/3 de los días abiertos en 2025 | ~€1.300 M de obras |
| **Montevideo** | Muestras hasta 4 veces por semana en verano; regla de 24 h tras lluvia | Bandera sanitaria | No hay métrica oficial | Laboratorio de la Intendencia |
| **Río de la Plata argentino** | Red nacional, 2 a 4 muestras por año por sitio | Datos en CSV, **sin aviso al público** | — | — |

Todo **[V]**, salvo los costos de Sídney **[P]**.

### 3.2 Qué uso tiene hoy el río en San Isidro

| Quién | Qué hace | Dónde | Cuánta gente | Marca |
|---|---|---|---|---|
| **Municipio** (Escuela Náutica, Campo N° 9) | Kayak, vela, windsurf, SUP, kitesurf, canotaje; gratis para vecinos | Gaetán Gutiérrez 757, Bajo | No publicado | *Según el Municipio* |
| Perú Beach | Escuela de kite, windsurf y kayak | El Cano 794, Acassuso | No publicado | **[V]** que existe |
| El Molino | Escuela de kite, windsurf y SUP | Sebastián Elcano 888 | No publicado | *Según la escuela* |
| Nautiaventura (en el Club de Veleros) | Windsurf, kite, wingfoil, vela, kayak, SUP | Camino de la Escollera 1500 | "805 personas en la última temporada", en sus dos sedes | *Según la empresa* |
| Club de Veleros San Isidro | Vela; reglamento propio de kite desde 2021 | Camino de la Escollera 1500 | No publicado | **[V]** |
| CASI, sede La Ribera | Kite, SUP, kayak, windsurf, vela; avisa a Prefectura si alguien no vuelve | Junto a la escollera del Club de Veleros | No publicado | **[V]** |
| Club Náutico San Isidro (1910) | Vela y regatas; regata San Isidro Labrador | Av. Mitre 1999 | 84 embarcaciones del club para socios | *Según el club* |
| Campeonato de Clubes 2026 | 9 fechas, 10 clubes | Costa de San Isidro | "Más de 400 navegantes" | *Según el Municipio* |
| Travesías de natación | Travesía Rosa (11 km, ~30 nadadores, 2022); cruce Carmelo–San Isidro (58 km, 6 nadadores, 2026) | Del Náutico a Núñez; desde Uruguay | Decenas | **[V]** |
| Vecinos | Nado informal y kite en la ribera pública | Bajo, entre Alvear y Perú | Sin números | **[V]** que lo dice un estudio de 2024-25 |

**Riesgo para la salud del contacto secundario.** En Chicago, en 11.297 personas que hacían canoa, kayak, remo, pesca y
bote, la enfermedad gastrointestinal atribuible fue de 13,7 a 15,1 casos por 1.000. Ingieren en promedio 3 a 4 ml de
agua. **[V]** No hay estudios sobre kitesurf.

### 3.3 La norma y los valores guía

- **Ordenanza 5304 (19/01/1978)** **[V]**:
  - art. 1: "Declárase zona de emergencia sanitaria a las playas ubicadas en la ribera del Río de la Plata en
    jurisdicción del Partido";
  - art. 2: "Prohíbese tomar baños en las aguas del Río de la Plata en toda la extensión" del partido;
  - art. 3: sanción según el Código Contravencional de entonces.
  - No menciona deportes náuticos. La dictó el intendente con fuerza de ordenanza (Ley 8.613).
- **Valores guía en la Argentina**: 126 *E. coli* o 33 enterococos por 100 ml, media geométrica (Res. ADA 42/2006;
  Ministerio de Salud, Res. 125/2016). **No hay valor argentino para contacto secundario.** **[V]**
- **Afuera hay valores más altos para contacto secundario.** Por ejemplo, Texas: 630 *E. coli* por 100 ml. **[V]**
- **San Isidro 2021-2025, con el método europeo**: las tres estaciones quedarían en "insuficiente". La media geométrica
  de *E. coli* fue de 1.236 en la Reserva, 2.461 en Pacheco y 29.483 en Perú. **[CP]**

### 3.4 Qué haría falta para un aviso en San Isidro **[I]**

1. **Una línea de base intensiva**: muestras 2 a 4 veces por semana en temporada, durante 2 o 3 temporadas, donde la
   gente usa el agua (Perú Beach, Elcano, Club de Veleros y CASI, Pacheco, Puerto). Al ritmo actual, juntar 100
   muestras por sitio llevaría 25 a 50 años. **[CP]**
2. **Laboratorio** para *E. coli* y enterococos. Para decidir en el día: análisis por ADN con una universidad, o
   sensores rápidos como en París.
3. **Datos de entrada**: lluvia en tiempo real en la cuenca de Perú, sensores de nivel en las bocas grandes, altura del
   río y viento.
4. **Aviso simple**: bandera en el sitio, web y correo diario a clubes y escuelas, que ya llevan libros de entrada y
   salida.
5. **Una decisión previa**: si el aviso es para los deportes o también para bañarse. Para bañarse habría que modificar
   la Ordenanza 5304.
6. **Advertencia**: un aviso no reemplaza el saneamiento. Hoy diría "no apto" casi siempre.

---

## 4 · Los parques para empezar

### 4.1 Fichas

| Espacio | Dónde y cuánto | De quién es el suelo | Qué hay hoy | Protección | Qué está proyectado |
|---|---|---|---|---|---|
| **Bosque Alegre** | Costa, Del Barco Centenera, calle 1 y el canal de desagüe. 3,5 ha según el polígono del decreto **[CP]**; 4,5 ha *según el Municipio* | Probablemente la Provincia, como el Campo N° 6 vecino **[I]** | Juncal, matorral ribereño, alisos y sauces criollos. Vegetación densa y estable 2023-2026 por satélite **[CP]** | **Paisaje Protegido** (Decreto 910/2012, Ordenanza 8651) **[V]** | Senderos hacia el bosque y muelle (Plan Urbano Costero, etapa 2). Al lado, 2 canchas de rugby del CASI con riego e iluminación, 2026-2027 (Decreto 1154/2025) **[V]** |
| **Reserva Ecológica Ribera Norte** | Camino de la Ribera 480, Acassuso. 50 ha con el río; 14 ha de tierra (2009) | No encontrado | Lirio amarillo en el 30% de la tierra y ligustrina en el 15%; basura que entra por el desagüe de Perú (Plan de 2012) | Parque Natural Municipal (Ordenanzas 6541/1988 y 8461/2009); prohíbe remover juncales y rellenar **[V]** | El Plan de 2012 debía revisarse a los 5 años; no hay versión nueva |
| **Parque del Águila** | Cuatro piezas en Martínez: Paseo del Águila (cerrado), Águila Grande, Águila Chico y el sector que protegía la Ordenanza 9395 (~580 m de costa) | Provincia, administrado por el Municipio **[V]** | Vegetación estable 2023-2026 **[CP]** | La Ordenanza 9395 fue vetada (Decreto 614/2025) | Tramo de 907 m Águila–Alvear hecho por un privado desde julio de 2026, sin acto publicado |
| **Perú Beach** | 11.553 m² (OpenStreetMap) | No encontrado | Entre 22 y 32% sin vegetación; parte del albardón ocupado **[CP]** / Plan de 2012 | — | — |
| **Roque Sáenz Peña y el río** | 9.775 m², ex Catalejo y Barisidro, parquizado en 2025 | Parcela 14, de la Provincia **[V]** | Parque nuevo | — | Muelle, juegos y senderos (etapa 2) |
| **Puerto de San Isidro (playón)** | "Casi siete hectáreas" | Administración transferida al Municipio por acta, *según el Municipio* | Parque con césped y nativas | Zonificación de parque de la ribera | Ya se invirtieron entre 6.000 y 6.450 millones de pesos de dic-2025 desde 2017 **[CP]** |
| **Paseo del Río (Beccar)** | 1.200 m de costa, ~35.000 m² | No encontrado | Ciclovía; proyecto "de bajo impacto" *según el Municipio* (2020) | — | — |
| **Espigón de Pacheco y La Farola** | Martínez | No encontrado | Agua "muy deteriorada" en 2024 | — | — |

### 4.2 Naturaleza o cemento: lo que cuesta

Con los precios del propio contrato municipal de espacios verdes (LP 62/2024, vigentes desde marzo de 2025), suponiendo
un sendero de 2 m de ancho. En pesos de diciembre de 2025 por metro de sendero. **[CP]**

| Sendero | Pesos por metro |
|---|---|
| Tosca compactada | 33.000 a 39.000 |
| Chips de madera | 47.000 a 183.000 |
| Granza sobre tosca | 83.000 a 117.000 |
| Intertrabado | 111.000 a 114.000 |
| Hormigón peinado | 161.000 a 222.000 |
| Tablado de madera dura, sin estructura | ~537.000 |

Para comparar, el tablestacado costero de 2025 costó **5,7 a 7,9 millones por metro** (informe 14).

**Otros costos de referencia:**

- **Restauración de bosque nativo**, pilotos nacionales de 2017: unos 2,4 M por ha. No dice qué incluye. **[CP]**
- **Mantenimiento de un área natural**: el Plan de Ribera Norte de 2012 calculó $84.000 por año para 50 ha, sin
  sueldos; unos 0,59 M por ha y por año en pesos de hoy. **[CP]**
- **Control de exóticas: no hay costo por hectárea en la Argentina.** En la Reserva Costanera Sur, la ligustrina bajó
  de 82 a 9 ejemplares cada 8 m² en 12 años de manejo a mano y con herbicida. **[V]**
- **Una costa con juncal en vez de muro**: en EE.UU., sólo vegetación cuesta hasta US$3.280 por metro, y un muro
  vertical hasta US$16.400 (NOAA, 2015). **[V]**

**Dentro del mismo contrato municipal, la misma planta cuesta distinto según la zona** **[V]**. Sólo los números, con
precios de marzo de 2025:

| Ítem | Zona 1 | Zona 2 |
|---|---|---|
| Herbácea perenne chica | $3.478 | $15.222 |
| Arbusto mediano | $9.192 | $28.571 |
| Chips de madera, por m³ | $195.708 | $757.185 |

No se publicaron los análisis de precios que lo expliquen.

### 4.3 Orden que sugieren las fuentes

- **El Plan de Manejo de Ribera Norte (2012)** ordena los problemas así: basura, exóticas, avance urbano, contaminación
  del agua. Sus prioridades altas son la barrera de basura en Perú (proyecto 17), restaurar ambientes empezando por las
  especies invasoras (proyecto 45) y monitorear el avance del juncal (proyecto 51). **[V]**
- **El Decreto 280/1973** pide que la ribera de Bosque Alegre "no altere su fisonomía natural y agreste". **[V]**
- **El Decreto 910/2012** pide primero el Plan de Remediación y la reforestación con 180 nativas; después, la
  ampliación del campo de deportes. El Plan de Remediación no está publicado. **[V]**
- **Sugerencia de este informe** **[I]**: proteger y medir lo que ya está vegetado (Bosque Alegre, juncales de Ribera
  Norte, sector del Águila) antes de intervenir con obra.

---

## 5 · El plan con la Provincia

### 5.1 Quién está hoy

| Organismo | Qué hace | Qué tiene que ver con la costa de San Isidro | Marca |
|---|---|---|---|
| **AySA** | Agua y cloacas. Contrato nuevo del 07/05/2026; en venta el 90% de las acciones (ofertas abiertas el 15/09/2026) | Opera la cloaca. No los pluviales | **[V]** / **[P]** |
| **ERAS** | Controla a AySA | Vía de reclamo por el art. 16 | **[V]** |
| **APLA** | Planifica las obras de AySA. Plan Director 2027-2031 aprobado el 24/06/2026 | **San Isidro tiene un representante en su comisión asesora** (art. 37) | **[V]** |
| **Red nacional de monitoreo (RIIGLO)** | Mide la costa desde 2004 con 10 gobiernos locales; laboratorios de la Autoridad del Agua y de ABSA | Mide San Isidro. No tiene metas ni obras | **[V]** |
| **Autoridad del Agua** | Permisos, vuelcos, comités de cuenca | Puede crear un comité de cuenca de la costa norte por resolución | **[V]** |
| **Ministerio de Ambiente** (Provincia) | Evaluación de impacto ambiental | Firma convenios ambientales | **[V]** |
| **Ministerio de Infraestructura** (Provincia) | Obras hidráulicas | No se encontró ningún programa del lado del Río de la Plata | **[V]**, como ausencia |
| **COMIREC** (Reconquista) | Plan de cuenca, préstamo BID 3256 | San Isidro está en la cuenca baja; sólo figura con una obra vial | **[V]** |
| **COMILU** (Luján) | Plan de cuenca, préstamo CAF | San Isidro no está | **[V]** |
| **ENOHSA** | — | Disuelto en 2024 | **[V]** |

### 5.2 Cómo se armaría, de menor a mayor

| # | Instrumento | Quién firma | Base legal |
|---|---|---|---|
| 1 | **Usar el asiento en la APLA** para pedir obras en el Plan Director de AySA | Nadie nuevo | Decreto 805/2025, art. 37 |
| 2 | **Convenio entre municipios** (San Isidro, Vicente López, San Fernando, Tigre, y San Martín por la cuenca de Perú), con un comité de coordinación | Intendentes y cada Concejo | Ley Orgánica, art. 41; modelo: Ordenanza 8935 (calle Paraná, 2016) |
| 3 | **Convenio marco con la Provincia** (Ambiente, Infraestructura, Autoridad del Agua) | Intendentes y ministros; no necesita el Concejo | Ley Orgánica, art. 41 |
| 4 | **Convenio con AySA** para obras | Hoy no necesita el Concejo por ser empresa del Estado; después de la venta, probablemente sí **[I]** | Contrato de 2026, cláusula 4.2 |
| 5 | **Comité de Cuenca "Vertiente Río de la Plata Norte"** | Resolución del directorio de la Autoridad del Agua | Ley 12.257, arts. 121 a 125; precedente: Res. ADA 541/2018 |
| 6 | **Ente por ley**, como el COMIREC | Legislatura | Leyes 12.653 y 14.710 como modelo |

### 5.3 Qué enseñan los precedentes

| Precedente | Cómo se armó | Quién pagó | Resultado | Marca |
|---|---|---|---|---|
| **Montevideo** (Plan de Saneamiento Urbano, desde 1981) | Lo ejecuta la Intendencia | Préstamos del BID con aporte local | Playas del este recuperadas; 2023-24 todas las habilitadas en "Muy buena" | **[V]** *según la Intendencia* |
| **París** (Plan Baignade, desde 2016) | Estado, Región, Ciudad y empresa de saneamiento en un comité | ~€1.400 M; la mitad, la agencia del agua | 2/3 de los días abiertos en 2025; clasificación anual "insuficiente" | **[V]** |
| **ACUMAR** (Riachuelo) | Ley nacional, con adhesión de Provincia y Ciudad | Presupuesto nacional y Banco Mundial | Su índice de calidad no mide bacterias; en 2024-25 no se pudo calcular | **[V]** |
| **Porto Alegre** (lago Guaíba) | El servicio municipal de agua ejecuta | BID 35%, Caixa 54%, Prefeitura 11% | Tratamiento de cloacas del 30% al 80%, *según el servicio municipal* | **[V]** que lo dice |

**Lo común** **[I]**: definieron por norma qué es "apto", midieron todo el año y lo publicaron, y financiaron con
crédito multilateral o una agencia del agua más aporte local.

---

## Correcciones a informes anteriores

| Informe | Decía | Corrección |
|---|---|---|
| 11, tabla de opciones | Interceptor: €700.000 por unidad, *según la ONG* | En Los Ángeles se habla de US$5 a 8 M por unidad y US$3 a 4 M por año **[P]** |
| 11, tabla de opciones | "Ningún equipo documentado funciona en una costa abierta" | Las barreras de sargazo están en costa abierta, pero dejan pasar del 30 al 60% y se rompen con temporales **[V]** |
| 11 y 15 | Ordenanza 5304 **[P]** | Pasa a **[V]**: se leyó el texto |
| 15, F4 | "El monitoreo de la Ciudad dio 0% de sitios aptos" | El dato es de la red nacional (RIIGLO), no de la Ciudad **[V]** |

Los archivos de los informes 11 y 15 no se tocaron: la regla es agregar sólo archivos nuevos.

---

## Decisiones que necesita el cliente

1. **¿El aviso de calidad del agua es para los deportes o también para bañarse?** Para bañarse habría que modificar la
   Ordenanza 5304.
2. **¿El programa promete una obra en Perú o primero un diagnóstico?** Ninguna fuente estudió una obra para ese
   desagüe, y depende de AySA o de la Provincia.
3. **¿Se pide una opinión legal** sobre quién tiene el poder de policía en las conexiones clandestinas del área de AySA?
4. **¿Se hacen pedidos de acceso a la información** (plano del conducto de Perú, protocolo de muestreo, programa del
   art. 16 de AySA)? Son gratis, pero son pedidos a organismos públicos.
5. **¿El plan regional incluye a San Martín**, que comparte la cuenca de Perú?

---

## Borrador de la propuesta

**Esto es un borrador. No está en el programa. Cada punto marca de qué depende.**

### 1. Cortar la cloaca

- **Diagnóstico de Perú en los primeros 6 meses.** Muestreo con y sin lluvia, marcador de cloaca humana, sensores
  cámara por cámara aguas arriba, y publicación de los resultados. Orden de magnitud: decenas de millones de pesos de
  laboratorio y equipos, más personal. **[CP]**
- **Pedirle a AySA, por el ERAS, el programa del art. 16 d)** para la cuenca de Perú, y usar el asiento de San Isidro
  en la APLA para que el Plan Director lo incluya.
- **Programa municipal de conexiones**: inspección con la Ley 5965, intimación al dueño y un subsidio para hogares de
  bajos ingresos, como París. *Depende de la opinión legal (decisión 3).*
- **Convenio con Vicente López y San Martín** para rastrear la cuenca de Perú, con el modelo de la calle Paraná.
- **Una obra en la boca sólo después del diagnóstico**, y de acuerdo con AySA. *Depende de la decisión 2.*

### 2. Frenar la basura

- **Barrera de basura en la boca de Perú**, como pidió el Plan de Manejo en 2012, con vaciado diario y retiro antes de
  cada sudestada.
- **Redes en las bocas chicas** y **barreras simples en dársenas**, con vaciado diario.
- **Cuadrilla de costa con bote**, con protocolo para juncales, movilizada con el pronóstico de sudestada.
- **Cámaras con IA en las bocas grandes** para medir cuánta basura entra y cuándo.
- **Pesar y publicar todo** con un mismo método, para tener por primera vez una línea de base.

### 3. Recuperar parque por parque

- **Primero, proteger y medir lo que ya está vivo**: Bosque Alegre, juncales de Ribera Norte y el sector del Águila.
- **Pedir y publicar el Plan de Remediación de Bosque Alegre** y un estudio de suelo del relleno.
- **Actualizar el Plan de Manejo de Ribera Norte**, que debía revisarse en 2017, con control de lirio amarillo y
  ligustrina.
- **Senderos de tosca o granza, no de hormigón**: con los precios del propio contrato municipal, cuestan entre un quinto
  y la mitad. **[CP]**
- **Costa con juncal donde se pueda, en vez de muro.** Ver el informe 14.

### 4. Informar la calidad del agua

- **Muestreo 2 a 4 veces por semana en temporada** donde la gente usa el río, durante 2 o 3 temporadas, con laboratorio
  de la Autoridad del Agua o de una universidad.
- **Bandera en el sitio y aviso diario** a clubes y escuelas, con la regla de 24 a 72 horas después de lluvia mientras
  no haya modelo.
- **Publicar todos los datos** en formato abierto.
- *Depende de la decisión 1 (deportes o baño).*

### 5. El plan con la Provincia

- **Proponer a la Autoridad del Agua un Comité de Cuenca "Vertiente Río de la Plata Norte"** con Vicente López, San
  Fernando y Tigre, como el de Berazategui, Quilmes y Florencio Varela.
- **Convenio marco con la Provincia** (Ambiente, Infraestructura y Autoridad del Agua), que no necesita el Concejo.
- **Metas públicas**, con los indicadores de los precedentes: porcentaje de días aptos por sitio, conexiones
  clandestinas encontradas y corregidas, caudal tratado en la Planta Norte contra su capacidad, campañas completas por
  año.
- **Pedir la ampliación de la Planta Norte** en el Plan Director de AySA, porque sin lugar en la cloaca no hay desviador
  posible.

---

## Método y límites

- Seis investigaciones en paralelo: cloaca local, detección e intercepción, tecnología para basura, calidad del agua y
  uso del río, parques, y plan con la Provincia. Los datos clave se verificaron después contra las fuentes guardadas:
  el Decreto 805/2025, el contrato de AySA de 2026, la Ordenanza 5304, la Ley 5965, el Decreto 910/2012, la adenda del
  CASI de 2025, el Plan de Manejo de 2012, la evaluación francesa del sargazo, los informes de California y los datos de
  París y Sídney. La serie de *E. coli* de Perú se recalculó dos veces, por separado.
- **El cupo de búsquedas web de la sesión se agotó** a mitad del trabajo de cuatro de los seis investigadores. Quedaron
  sin buscar, entre otras cosas: la Defensoría del Pueblo provincial, denuncias ante la Autoridad del Agua, los
  boletines de Vicente López y San Martín sobre la cuenca de Perú, y Chile.
- El sitio de AySA no respondió; el Plan Director 2027-2031 (244 MB) no se bajó.
- No se pidió nada pago ni en persona y no se contactó a nadie.
- **Fuentes:** `01_raw/agua/`, con una carpeta por investigación y `FUENTES.txt`. Lo que no se subió y por qué, en
  `01_raw/agua/NO_SUBIDOS.txt`.
