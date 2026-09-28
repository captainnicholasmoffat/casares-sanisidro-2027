# 09 · Escenario B de la base de valuación

25 de septiembre de 2026. Rama `claude/cool-hopper-3hdk58`. Todo sale de
`03_scripts/escenario_b_valuacion.py`, con los datos crudos guardados en el repo.

**28 de septiembre: todas las tablas por localidad están rehechas.** La primera versión asignó cada
parcela a las zonas que había construido `zonas.py` (semillas y crecimiento por población), que no son las
localidades del documento. Ahora las localidades son las de los capítulos 1 y 4: los 360 radios censales
asignados a su localidad de OpenStreetMap (`data/zonas_asignacion_radios.csv`), disueltos en
`data/zonas_propuestas_sanisidro.geojson`, que se regeneró con `03_scripts/zonas_osm_geojson.py`. **Los
totales del partido no cambian**: 8.089,1 millones emitidos, 7.225,2 cobrados, 34.998 parcelas que bajan y
33.619 que suben, los 789 millones del mínimo y el camino con tope año por año.

## Lo decidido: escenario B, con suba pareja de 10,9% y un tope de 25% por año

El programa necesita **cobrar** 7.225,2 millones. Con la percepción de hoy, del 89,32%, eso
exige **emitir 8.089,1 millones más por la parte tierra**. La escala de ARBA se fija entonces un
**10,9%** por encima del nivel que dejaría la recaudación igual (10,88% exacto).

**Quién paga más y quién menos (en régimen):**

| Localidad | Tierra hoy (M) | Con B (M) | Diferencia (M) | % | Parcelas que suben | Parcelas que bajan | Suba mediana de las que suben | Duplican o más |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Acassuso | 5.433,1 | 6.283,0 | +849,9 | +15,6% | 2.253 | 511 | +20,5% | 40 |
| Martínez | 19.081,1 | 22.485,1 | +3.404,0 | +17,8% | 15.863 | 2.785 | +22,5% | 62 |
| San Isidro | 21.380,3 | 27.363,9 | +5.983,5 | +28,0% | 6.843 | 3.945 | +26,3% | 1 |
| Béccar | 11.246,9 | 11.252,4 | +5,5 | 0,0% | 4.426 | 6.400 | +24,9% | 44 |
| Villa Adelina | 4.711,1 | 3.118,5 | −1.592,6 | −33,8% | 307 | 9.047 | +14,4% | 0 |
| Boulogne | 12.515,0 | 11.953,8 | −561,2 | −4,5% | 3.927 | 12.310 | +23,2% | 0 |
| **Todo el partido** | 74.367,6 | 82.456,7 | **+8.089,1** | **+10,9%** | **33.619** | **34.998** | +23,5% | 147 |

**Bajan más parcelas de las que suben: 34.998 contra 33.619.** Las otras 27 quedan igual.

**El tope.** Ninguna boleta sube por esta actualización más de **25% por año**, por encima de la
actualización anual del multiplicador, que es pareja para todos. Las que tienen que subir más llegan
por escalones. **Las bajas se aplican completas desde el primer año.** La suba más grande es de
+122,8%, y con el tope llega en cuatro años.

| Año del programa | Se emite (M) | Se cobra al 89,32% (M) | Lo que pide la rampa del programa (M) | Parcelas todavía topeadas |
|---:|---:|---:|---:|---:|
| 1 | 2.212,5 | 1.976,2 | 1.806,3 | 15.884 |
| 2 | 6.558,2 | 5.857,8 | 3.612,6 | 2.892 |
| 3 | 8.025,6 | 7.168,5 | 5.418,9 | 215 |
| 4 en adelante | 8.089,1 | **7.225,2** | 7.225,2 | 0 |

**Por qué 25%.** Es el tope más bajo que, cada año, cobra al menos lo que pide la rampa del
programa (25%, 50%, 75% y 100% de 7.225,2 millones). Con 24% el primer año se cobran 1.753 millones y
la rampa pide 1.806. Con 25%, **el rendimiento final queda en pie: 7.225,2 millones cobrados por año
desde el cuarto**, y no hace falta achicar el programa.

**Cuántos años tarda cada parcela en llegar:**

| Localidad | Llegan el año 1 | En 2 años | En 3 años | En 4 años |
|---|---:|---:|---:|---:|
| Acassuso | 1.288 | 742 | 183 | 40 |
| Martínez | 8.660 | 5.632 | 1.443 | 128 |
| San Isidro | 3.147 | 3.396 | 297 | 3 |
| Béccar | 2.247 | 1.661 | 474 | 44 |
| Villa Adelina | 218 | 89 | 0 | 0 |
| Boulogne | 2.175 | 1.472 | 280 | 0 |

**La boleta típica, parte tierra, pesos por año** (mediana de cada grupo, antes y después):

| Localidad | Parcela mediana hoy | Las que suben | Las que bajan |
|---|---:|---:|---:|
| Acassuso | 1.245.118 | 1.296.619 → 1.607.053 | 594.520 → 368.876 |
| Martínez | 593.566 | 595.428 → 764.908 | 582.761 → 487.744 |
| San Isidro | 670.641 | 777.733 → 994.387 | 517.328 → 418.246 |
| Béccar | 437.506 | 616.566 → 751.387 | 358.397 → 264.306 |
| Villa Adelina | 384.771 | 460.959 → 494.639 | 382.414 → 228.295 |
| Boulogne | 335.066 | 660.530 → 815.667 | 302.497 → 195.510 |

**El mínimo, con este escenario.** De las bajas, 789 millones de emisión caen por debajo del mínimo
de $234.000 (vivienda, Impositiva 2026): 410 en Boulogne, 241 en Villa Adelina y 124 en Béccar, en
16.097 parcelas. Si esas casas tienen poca superficie construida, siguen pagando el mínimo y esa parte
de la baja no les llega. Del otro lado, el mínimo tapa hasta 49,8 millones de subas de lotes que hoy
están debajo del piso. Mirado sólo con la tierra, el neto emitido queda entre 8.039 y 8.878 millones
(8.089 − 50 y 8.089 + 789). Es un cálculo parcela por parcela: no ve lo construido ni los
departamentos, y en los edificios cada unidad funcional paga su propio mínimo (Impositiva 2026, art. 1).

**Lo decidido sobre el mínimo (25/09): se ajusta.** La baja que produce la tabla nueva se aplica
aunque la boleta quede debajo del mínimo (anexo III, artículo 4). El mínimo se fijó con la tabla vieja, y
con la nueva cobraría de más a las parcelas más chicas de las zonas con menos servicios: las 16.097
parcelas cuya baja frenaría tienen 226 m² de mediana, contra 298 del partido, y el 98% de esos 789
millones está en Boulogne, Villa Adelina y Béccar. **Contra el plan no cuesta nada**: los 8.089 millones emitidos y los
7.225,2 cobrados ya cuentan esas bajas completas. Contra aplicar la tabla con el mínimo como está, el
Municipio resigna hasta 789 millones emitidos por año, 705 cobrados, que no estaban en el plan. Lo único
que queda es la suba tapada por el mínimo: hasta 49,8 millones emitidos, 44,5 cobrados, con lo que lo
cobrado podría quedar en 7.180,7 millones, un 0,6% debajo de 7.225,2. Está en `data/valuacion_resumen.json`
(bloque `minimo_propuesta`). **No se escala el programa** (25/09): el documento declara el rango,
entre 7.180,7 y 7.225,2 millones cobrados, y que el cálculo es sobre la parte tierra.

| Año del programa | Cobrado (M) | Si el mínimo frena todas las subas de lotes chicos (M) | Lo que pide la rampa (M) |
|---:|---:|---:|---:|
| 1 | 1.976,2 | 1.946,4 | 1.806,3 |
| 2 | 5.857,8 | 5.814,7 | 3.612,6 |
| 3 | 7.168,5 | 7.124,0 | 5.418,9 |
| 4 en adelante | 7.225,2 | 7.180,7 | 7.225,2 |

Columna `cobrado_si_el_minimo_frena_subas` de `data/valuacion_rendimiento_por_anio.csv`.

Todo esto está en `data/valuacion_escenarios_localidad.csv` (columnas `Bc_`), en
`data/valuacion_rendimiento_por_anio.csv`, que lee el modelo fiscal, y en `data/valuacion_resumen.json`
(bloque `adoptado`).

## El cuadro de la tabla municipal, por localidad (3.5)

Valor de la tierra de cada localidad en veces el de Boulogne Sur Mer, promedio ponderado por superficie
de parcela, con las mismas 68.644 parcelas. «Reconocido» es la tabla municipal dividida por la valuación
provincial.

| Localidad | IUST por m² | VUB por m² | Tabla municipal | Valuación provincial | Reconocido |
|---|---:|---:|---:|---:|---:|
| Acassuso | 470,3 | 10.912,3 | 2,31× | 2,80× | 83% |
| Martínez | 356,3 | 8.423,7 | 1,75× | 2,16× | 81% |
| San Isidro | 327,8 | 8.418,0 | 1,61× | 2,16× | 75% |
| Béccar | 245,6 | 4.930,3 | 1,21× | 1,27× | 95% |
| Boulogne Sur Mer | 203,1 | 3.892,7 | 1× | 1× | — |
| Villa Adelina | 195,1 | 2.591,8 | 0,96× | 0,67× | 144% |

- Las seis quedan en el mismo orden en las dos escalas: Acassuso, Martínez, San Isidro, Béccar,
  Boulogne y Villa Adelina.
- La tabla municipal achata la distancia entre las localidades de valor alto y Boulogne, pero menos de lo
  que decía la primera versión: Acassuso reconoce el 83%, no el 64%.
- Villa Adelina es el caso contrario: la tabla vieja la pone casi a la par de Boulogne
  (0,96×) y la valuación provincial, un tercio por debajo
  (0,67×): la tabla le cobra de más, el 144% de lo que le toca.
- Las localidades son las de los capítulos 1 y 4, armadas con radios censales; sus límites no siguen el
  catastro. Cada parcela va a la localidad donde cae su punto interior. El cruce sección por sección está
  en `data/valuacion_secciones_localidad.csv`: 2.012 parcelas
  (2,9%) caen en una sección cuya mayoría es de otra localidad.
- Con cada sección entera asignada a su localidad mayoritaria, el cuadro casi no cambia: Acassuso
  2,37× contra 2,94× (80%), Martínez 80%, San Isidro 74%, Béccar 95%, Villa Adelina 145%.
- La correlación entre las dos escalas, sección por sección (50 secciones), es 0,916.

Sale de `ratios_por_localidad()` y `secciones_por_localidad()` en el script, y está en
`data/valuacion_ratios_localidad.csv`.


---

Lo que sigue es el informe original: las alternativas antes de la decisión.

## La respuesta

1. **B, tal como lo cuenta hoy el documento, recauda cero.** La carga se corre de unas zonas a otras
   y el total queda igual, por definición. Lo que mueve son **9.402 millones**: los pagan de más
   San Isidro, Martínez y Acassuso, y los pagan de menos Villa Adelina, Boulogne y Béccar.
2. **Para juntar los 7.225,2 millones con la escala de ARBA, hay que subir el nivel de toda la
   escala un 9,7%.** Un 10,9% si se quiere *cobrar* esa cifra con la percepción actual, del 89,32%.
   Con esa suba alcanza. Y aun así **Villa Adelina paga 34,5% menos por tierra, Boulogne 5,5% menos
   y Béccar 1,0% menos**. San Isidro sube 26,6%, Martínez 16,6% y Acassuso 14,4%.
3. **A (nadie baja, las subvaluadas suben hasta el promedio) junta 9.402 millones**: sobran 2.177.
   Pero Boulogne, Villa Adelina y Béccar también suben: 6,0%, 0,2% y 8,2%.
4. **El mínimo de la tasa recorta la baja de B.** En 2026 el mínimo de vivienda es de $234.000 por
   año, y un cuarto de las parcelas de Boulogne (26,3%) ya paga por tierra menos que eso. Unos
   424 millones de las bajas de Boulogne no le llegarían a nadie si esas casas tienen poca
   superficie construida. Lo que el Municipio deja de cobrar sería menor, y el neto de B, mayor.
5. **Los porcentajes que hoy cita el documento (32→38%, 10→6% y 14→13%) no son de las
   localidades.** Son de las circunscripciones III, V y VI. Con las seis localidades del documento,
   las cifras son otras (tabla 1).

**¿B alcanza los 7.225,2 millones?** B a igual recaudación, no: da cero. B con la escala subida un
9,7%, sí, y con Boulogne, Béccar y Villa Adelina pagando menos. La elección entre esa versión de B y
A es tuya.

## Qué se calculó

La tasa usa esta fórmula (Ordenanza Impositiva 2026, Nº 9415, artículo 1):

`Val. Fiscal = [(ST × IUST × CMS × CPH) + (SC × IUSC × CA)] × 575,9141`

- ST es la superficie del lote.
- IUST es el índice de la manzana, fijado por la Ordenanza 8373/2008 (Anexo I).
- CMS es el coeficiente de mayor superficie; CPH, el de propiedad horizontal.
- La segunda mitad de la fórmula es la construcción.
- A la valuación se le aplica la alícuota: 12 por mil para vivienda.

El cálculo toma **sólo la parte tierra**: ST × IUST × 575,9141 × 12‰, parcela por parcela. En los
dos escenarios cambia únicamente el IUST, y todo lo demás queda como está, alícuota incluida.

- **Hoy:** el IUST de la tabla municipal.
- **B a igual recaudación:** el IUST pasa a ser proporcional al valor de ARBA de su macizo,
  `IUST nuevo = R × VUB`. R es el cociente promedio del partido, ponderado por superficie, así que el
  total no cambia.
- **B con la escala subida:** `IUST nuevo = s × R × VUB`, con `s` elegido para que el total suba
  exactamente 7.225,2 millones. Da s = 1,097: una suba pareja de 9,7%.
- **A:** `IUST nuevo = máximo(IUST de hoy, R × VUB)`. Es la definición del documento: ninguna manzana
  baja y las que están por debajo del promedio suben hasta él.

**Unidad.** Los montos salen del multiplicador 2026, que se fijó en la ordenanza del 17 de diciembre
de 2025. Son pesos de diciembre de 2025, la misma unidad del resto del documento y de los 7.225,2
millones. Son **emisión**, lo que se factura. Lo cobrado depende de la percepción.

## Fuentes, todas en el repo

| Qué | Archivo en el repo | De dónde |
|---|---|---|
| 69.258 parcelas, con superficie y partida | `01_raw/arba/parcelas_097_wfs/p_*.json.gz` (70 archivos, 1.000 parcelas cada uno) | ARBA, WFS IDERA, capa `idera:Parcela`, filtro `cca LIKE '097%'`, `https://geo.arba.gov.ar/geoserver/idera/wfs`, bajado el 25/09/2026 |
| Valores unitarios básicos (VUB) por macizo | `01_raw/arba/VUBxMacizo_paginas_6516-6650_san_isidro.pdf` | ARBA, "Consulta de Valores por Macizos (Decreto 790/16)", `https://www.arba.gov.ar/archivos/Publicaciones/VUBxMacizo.pdf`. Es el revalúo del Decreto 760/16, vigente desde 2018. El PDF provincial tiene 8.994 páginas; San Isidro (partido 97) va de la 6.516 a la 6.650 |
| IUST por manzana (Ordenanza 8373) | `01_raw/arsi/ORDENANZA_IMPOSITIVA_2016.pdf`, páginas 7 a 34 | ARSI, `https://arsi.gob.ar/pdf/ordenanzas/ORDENANZA_IMPOSITIVA_2016.pdf`. Es la última versión publicada con texto; la de 2026 es un escaneo |
| Página 28 de esa tabla, que es una imagen | `data/valuacion_iust_2016_pagina28_transcripta.csv` | Transcripta a mano: 142 filas de las secciones 7B, 7C y el comienzo de 7D. La continuidad se verificó: la página 27 termina en 7B-0001 y la 29 empieza en 7D-0010 |
| Multiplicador, alícuotas y mínimos 2026 | `01_raw/arsi/Ordenanza_Impositiva_2026-Nro_9415-2025_paginas_1-3.pdf` | ARSI, Ordenanza 9415. Multiplicador 575,9141; vivienda 12‰, comercio 16‰, industria 20‰, baldío 26‰; mínimo anual $234.000 para las categorías 2, 3, 4, 5, 10 y 12 |
| Las seis localidades | `data/zonas_propuestas_sanisidro.geojson` | Las de los capítulos 1 y 4: radios censales del INDEC asignados a su localidad de OpenStreetMap (`data/zonas_asignacion_radios.csv`); el archivo se regeneró el 28/09 con `03_scripts/zonas_osm_geojson.py` |

## Método

1. **Cruce.** Cada parcela se identifica por su código catastral: circunscripción, sección, y
   fracción o manzana. La misma clave cruza las tres fuentes.
2. **Un IUST por manzana.** En 11.006 parcelas (16%) la tabla municipal lista más de un valor
   para la misma manzana: el Ejecutivo asigna cada lote y esa asignación no es pública. Se usa el
   promedio, con el mínimo y el máximo como sensibilidad.
3. **Un VUB por macizo.** ARBA da un valor por cada lado de la manzana. Se usa el promedio
   ponderado por cantidad de lados.
4. **Localidad.** Se asigna por el punto interior de cada parcela dentro de los seis polígonos. Si
   cae afuera, por borde o costa, va a la localidad más cercana.
5. **Cobertura.** Cruzan **68.644 de 69.258 parcelas (99,1%)** y 3.789 de 3.881 hectáreas
   (97,6%). Quedan afuera 614:
   - 394 en Béccar, casi todas de la sección VIII-A, donde ARBA no publica valor para
     varias manzanas.
   - 162 en Boulogne, sobre todo de las secciones VI-E y VI-F, y 58 en el resto.

## Validación contra el documento

Sin la página 28, que el cálculo de septiembre no tenía, esta corrida **reproduce exactamente los
números del documento**:

- la circunscripción III pasa de 32,2% a 37,9% de la carga;
- la V, de 10,0% a 6,3%;
- la VI, de 14,3% a 12,7%;
- A da 12,5% de la parte tierra.

Con la página 28 incorporada, esos números quedan en 30,7→36,4%, 9,6→6,1%, 13,6→12,2% y
**A = 12,6%, 9.402 millones**. El documento dice "unos 8.600": es el mismo 12,5% sobre una base
más chica, sin las secciones 7B y 7C.

**El documento llamaba "Acassuso y Martínez" a la circunscripción III, "Villa Adelina" a la V y
"Boulogne" a la VI.** Con las localidades de los capítulos 1 y 4, la VI coincide con Boulogne (100% de
sus parcelas); la III es sobre todo Martínez (83%, y 16% Acassuso); la V es dos tercios Villa Adelina y un
tercio Boulogne.

## Resultados por localidad

**Tabla 1 · Qué parte de la carga de tierra paga cada localidad**

| Localidad | Parcelas | Tierra hoy (M) | Carga hoy | Carga con escala ARBA |
|---|---:|---:|---:|---:|
| Acassuso | 2.764 | 5.433,1 | 7,3% | 7,6% |
| Martínez | 18.648 | 19.081,1 | 25,7% | 27,3% |
| San Isidro | 10.788 | 21.380,3 | 28,7% | 33,2% |
| Béccar | 10.853 | 11.246,9 | 15,1% | 13,6% |
| Villa Adelina | 9.354 | 4.711,1 | 6,3% | 3,8% |
| Boulogne | 16.237 | 12.515,0 | 16,8% | 14,5% |
| **Todo el partido** | 68.644 | 74.367,6 | 100,0% | 100,0% |

**Tabla 2 · Cuánto sube o baja cada localidad, parte tierra, millones por año**

| Localidad | B a igual recaudación | | B con la escala 9,7% más alta | | A: nadie baja | |
|---|---:|---:|---:|---:|---:|---:|
| | millones | % | millones | % | millones | % |
| Acassuso | +233,6 | +4,3% | +784,1 | +14,4% | +556,1 | +10,2% |
| Martínez | +1.198,2 | +6,3% | +3.168,4 | +16,6% | +2.121,5 | +11,1% |
| San Isidro | +3.299,1 | +15,4% | +5.696,8 | +26,6% | +5.043,0 | +23,6% |
| Béccar | −1.098,4 | −9,8% | −112,4 | −1,0% | +923,6 | +8,2% |
| Villa Adelina | −1.898,5 | −40,3% | −1.625,3 | −34,5% | +9,3 | +0,2% |
| Boulogne | −1.733,9 | −13,9% | −686,5 | −5,5% | +748,3 | +6,0% |
| **Todo el partido** | 0,0 | 0,0% | **+7.225,2** | +9,7% | **+9.401,9** | +12,6% |

En B con la escala subida, las subas suman 14.453,7 millones y las bajas 7.228,5; el neto es
7.225,2.

**Tabla 3 · Cuántas parcelas pagan más y cuántas menos**

| Localidad | B igual recaudación: suben / bajan | B + 9,7%: suben / bajan | Suba mediana de las que suben (B + 9,7%) | Parcelas que duplican la parte tierra (B + 9,7%) | A: suben | Suba mediana (A) |
|---|---:|---:|---:|---:|---:|---:|
| Acassuso | 1.568 / 1.196 | 2.253 / 511 | +19,2% | 40 | 1.568 | +20,8% |
| Martínez | 13.449 / 5.199 | 15.619 / 3.025 | +21,3% | 62 | 13.449 | +14,0% |
| San Isidro | 5.997 / 4.791 | 6.801 / 3.987 | +25,1% | 1 | 5.997 | +16,2% |
| Béccar | 3.576 / 7.277 | 4.278 / 6.575 | +24,1% | 44 | 3.576 | +15,5% |
| Villa Adelina | 224 / 9.130 | 295 / 9.047 | +13,2% | 0 | 224 | +10,2% |
| Boulogne | 3.340 / 12.897 | 3.910 / 12.327 | +21,9% | 0 | 3.340 | +14,0% |
| **Todo el partido** | 28.154 / 40.490 | 33.156 / 35.472 | +22,4% | 147 | 28.154 | +15,2% |

**Cuánta gente.** La unidad es la parcela, es decir, el lote. Un edificio es una sola parcela
aunque tenga cien departamentos, y todos se mueven en la misma dirección. Para dar escala, el Censo
2022 cuenta estos hogares: Acassuso 4.805, Martínez 26.155, San Isidro 19.358, Béccar 22.055,
Villa Adelina 13.048 y Boulogne 25.138.

## La boleta típica

Parte tierra en pesos por año, B con la escala subida un 9,7%. Cada cifra es la mediana de su grupo
antes y después.

| Localidad | Parcela mediana hoy | Las que suben: antes → después | Las que bajan: antes → después | En A, las que suben: antes → después |
|---|---:|---:|---:|---:|
| Acassuso | 1.245.118 | 1.296.619 → 1.590.215 | 594.520 → 365.011 | 1.332.220 → 1.547.888 |
| Martínez | 593.566 | 597.087 → 762.923 | 567.368 → 480.043 | 609.900 → 729.602 |
| San Isidro | 670.641 | 775.846 → 981.649 | 520.479 → 416.415 | 794.495 → 939.705 |
| Béccar | 437.506 | 611.037 → 742.272 | 362.743 → 265.033 | 629.152 → 729.246 |
| Villa Adelina | 384.771 | 460.959 → 489.457 | 382.414 → 225.903 | 408.185 → 421.179 |
| Boulogne | 335.066 | 665.236 → 809.704 | 302.877 → 193.527 | 656.425 → 743.320 |

- **Duplicar.** En B con la escala subida, **147 parcelas duplican o más su parte tierra**: 62 en
  Martínez, 44 en Béccar, 40 en Acassuso y 1 en San Isidro. La mayor suba es de +120%. En A, 40 parcelas llegan
  a duplicar, con un máximo de +101%. La mediana de las subas es +22,4% en B y +15,2% en A.
- **La boleta entera sube menos.** Estos porcentajes son de la parte tierra. La boleta suma además
  la construcción, que no cambia, así que en pesos la suba es la misma, pero como porcentaje de la
  boleta total es menor.
- **Boulogne y Villa Adelina.** La parcela mediana que baja queda por tierra debajo del mínimo:
  193.527 y 225.903 contra 234.000. Esa parte de la baja sólo le llega a quien tiene construcción
  suficiente para estar por encima del mínimo.

## Lo que queda afuera, y cuánto puede mover

**Tabla 4 · El mínimo de $234.000 por año**

| Localidad | Parcelas | Pagan hoy por tierra menos que el mínimo | Baja de B que cae debajo del mínimo (M) |
|---|---:|---:|---:|
| Acassuso | 2.764 | 41 (1,5%) | 5,7 |
| Martínez | 18.648 | 425 (2,3%) | 1,0 |
| San Isidro | 10.788 | 288 (2,7%) | 8,3 |
| Béccar | 10.853 | 1.413 (13,0%) | 128,9 |
| Villa Adelina | 9.354 | 1.036 (11,1%) | 249,7 |
| Boulogne | 16.237 | 4.275 (26,3%) | 423,9 |
| **Todo el partido** | 68.644 | 7.478 (10,9%) | 817,4 |

- **Mínimos.** Hasta 817 millones de las bajas de B podrían no ocurrir, porque esas parcelas
  seguirían pagando el mínimo. El neto de B quedaría entonces **entre 7.225 y unos 8.000 millones**.
  La contracara: esa parte de la baja no llega a los vecinos de Boulogne y Villa Adelina.
- **Superficie construida.** No es pública parcela por parcela. En los dos escenarios esa parte de
  la fórmula no cambia, así que no mueve el neto en pesos; sólo achica el porcentaje de cambio de la
  boleta entera.
- **Propiedad horizontal (CPH).** En los edificios la fórmula multiplica la tierra por un coeficiente
  mayor que 1, que depende de la superficie construida. Este cálculo usa 1, así que subestima la
  parte tierra donde hay edificios: el centro de San Isidro, Martínez y las torres de Acassuso. La
  suba pareja necesaria sería algo menor y las subas en pesos de esas zonas, algo mayores.
- **Exenciones.** Jubilados hasta tres haberes mínimos, personas con discapacidad, escasos recursos y
  entidades. Una parcela exenta no paga ni antes ni después, así que achican las subas y las bajas.
  No hay dato público por zona.
- **Alícuota por categoría.** Se usó 12‰ para todas las parcelas. Comercio paga 16‰, industria 20‰
  y baldío 26‰: donde hay comercios y baldíos, la parte tierra es algo mayor que la calculada.
- **Coeficiente de mayor superficie (CMS).** Baja hasta 0,65 en los lotes grandes. Se usó 1 porque
  el lote mínimo de cada zona está en el Código de Ordenamiento Urbano. Con un lote mínimo de 300 o
  600 m², la suba pareja necesaria pasa a 11,4–11,7% y el sentido por localidad no cambia (tabla 5).
- **Cobranza.** Para *cobrar* 7.225,2 millones al 89,32% de percepción hay que emitir 8.089,1
  millones: la suba pareja pasa de 9,7% a 10,9%.
- **Valores de ARBA.** Son del revalúo vigente desde 2018 y no son el mercado de hoy. Lo que se usa
  es cómo ordenan las zonas, no su nivel.
- **Parcelas sin cruzar.** 614 parcelas, el 0,9% del total y 92 hectáreas.

**Tabla 5 · Sensibilidad**

| Variante | Tierra hoy (M) | A (M) | A (%) | Suba pareja para B + 7.225,2 M | Acassuso | Martínez | San Isidro | Béccar | Villa Adelina | Boulogne |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base: IUST promedio de la manzana, CMS = 1 | 74.367,6 | 9.401,9 | 12,6% | 9,7% | +14,4% | +16,6% | +26,6% | −1,0% | −34,5% | −5,5% |
| IUST mínimo de la manzana | 68.845,4 | 8.377,5 | 12,2% | 10,5% | +15,3% | +16,2% | +27,1% | +3,3% | −36,9% | −4,1% |
| IUST máximo de la manzana | 80.264,2 | 12.373,9 | 15,4% | 9,0% | +14,0% | +17,4% | +26,7% | −5,9% | −31,9% | −6,9% |
| CMS con lote mínimo de 300 m² | 61.601,8 | 7.681,2 | 12,5% | 11,7% | +17,9% | +20,4% | +27,9% | +2,2% | −33,2% | −4,0% |
| CMS con lote mínimo de 600 m² | 63.431,3 | 7.863,7 | 12,4% | 11,4% | +17,6% | +20,0% | +27,3% | +2,1% | −33,5% | −4,2% |

En todas las variantes Villa Adelina y Boulogne bajan con B, y San Isidro, Martínez y Acassuso suben.
Béccar queda cerca de cero: entre −5,9% y +3,3%.

## Código y cómo reproducirlo

`python3 03_scripts/escenario_b_valuacion.py`. Necesita `pymupdf` y `shapely` y tarda unos diez
segundos. Escribe:

- `data/valuacion_iust_manzanas.csv`: el IUST de cada manzana, con todos los valores listados.
- `data/valuacion_vub_macizos.csv`: el VUB de cada macizo, con sus lados.
- `data/valuacion_parcelas.csv`: parcela por parcela, la parte tierra hoy y en cada escenario.
- `data/valuacion_escenarios_localidad.csv`: las tablas 1 a 3.
- `data/valuacion_resumen.json`: los totales, la sensibilidad y el efecto del mínimo.

## Para decidir

1. **Qué B va.** B a igual recaudación no junta nada. B con la escala subida un 9,7% junta los
   7.225,2 millones y baja Boulogne, Villa Adelina y Béccar. A junta 9.402 millones y no baja a
   nadie.
2. **Los porcentajes del 3.5.** El 32→38%, el 10→6% y el 14→13% son de las circunscripciones III, V
   y VI, no de localidades. Con localidades, y con la tabla completa, son los de la tabla 1.
3. **Los 8.600 millones del 3.5.** Con la tabla completa, A da 9.402 millones: sigue siendo 12,6%.
4. **"Esto no es subir una tasa".** Con A o con B + 9,7% la alícuota no cambia, pero la recaudación
   total de la parte tierra sí sube: 12,6% en A y 9,7% en B.
