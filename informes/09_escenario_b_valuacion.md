# 09 · Escenario B de la base de valuación

25 de septiembre de 2026. Rama `claude/cool-hopper-3hdk58`. Todo sale de
`03_scripts/escenario_b_valuacion.py`, con los datos crudos guardados en el repo.
**Este informe no toca el documento.**

## La respuesta

1. **B, tal como lo cuenta hoy el documento, recauda cero.** La carga se corre de unas zonas a otras
   y el total queda igual, por definición. Lo que mueve son **9.402 millones**: los pagan de más
   Acassuso y Martínez y los pagan de menos San Isidro, Béccar, Villa Adelina y Boulogne.
2. **Para juntar los 7.225,2 millones con la escala de ARBA, hay que subir el nivel de toda la
   escala un 9,7%.** Un 10,9% si se quiere *cobrar* esa cifra con la percepción actual, del 89,32%.
   Con esa suba alcanza. Y aun así **Boulogne paga 18,9% menos por tierra, Villa Adelina 12,7% menos
   y Béccar 9,3% menos**. San Isidro sube 2,7%, Martínez 17,8% y Acassuso 26,8%.
3. **A (nadie baja, las subvaluadas suben hasta el promedio) junta 9.402 millones**: sobran 2.177.
   Pero Boulogne, Villa Adelina y Béccar también suben: 2,8%, 5,0% y 6,0%.
4. **El mínimo de la tasa recorta la baja de B.** En 2026 el mínimo de vivienda es de $234.000 por
   año, y un tercio de las parcelas de Boulogne ya paga por tierra menos que eso. Unos 400 de los
   1.246 millones de baja de Boulogne no le llegarían a nadie si esas casas tienen poca superficie
   construida. Lo que el Municipio deja de cobrar sería menor, y el neto de B, mayor.
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
| Las seis localidades | `data/zonas_propuestas_sanisidro.geojson` | Las mismas del resto del documento |

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
   - 404 en San Isidro, casi todas de la sección 8A, donde ARBA no publica valor para varias
     manzanas.
   - 146 en Villa Adelina y 64 en el resto.

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

**El documento llama "Acassuso y Martínez" a la circunscripción III, "Villa Adelina" a la V y
"Boulogne" a la VI, y no coinciden.** La III es 65% Acassuso y 35% Martínez. La V es 68% Villa
Adelina y 32% Boulogne. La VI es 56% Boulogne y 36% Villa Adelina.

## Resultados por localidad

**Tabla 1 · Qué parte de la carga de tierra paga cada localidad**

| Localidad | Parcelas | Tierra hoy (M) | Carga hoy | Carga con escala ARBA |
|---|---:|---:|---:|---:|
| Acassuso | 16.204 | 30.506,6 | 41,0% | 47,4% |
| Martínez | 11.469 | 10.322,9 | 13,9% | 14,9% |
| San Isidro | 8.743 | 10.624,7 | 14,3% | 13,4% |
| Béccar | 7.562 | 6.596,7 | 8,9% | 7,3% |
| Villa Adelina | 12.644 | 9.733,7 | 13,1% | 10,4% |
| Boulogne | 12.022 | 6.583,0 | 8,9% | 6,5% |
| **Todo el partido** | 68.644 | 74.367,6 | 100,0% | 100,0% |

**Tabla 2 · Cuánto sube o baja cada localidad, parte tierra, millones por año**

| Localidad | B a igual recaudación | | B con la escala 9,7% más alta | | A: nadie baja | |
|---|---:|---:|---:|---:|---:|---:|
| | millones | % | millones | % | millones | % |
| Acassuso | +4.762,5 | +15,6% | +8.189,1 | +26,8% | +6.326,3 | +20,7% |
| Martínez | +764,1 | +7,4% | +1.841,3 | +17,8% | +1.156,3 | +11,2% |
| San Isidro | −675,5 | −6,4% | +291,1 | +2,7% | +851,6 | +8,0% |
| Béccar | −1.142,4 | −17,3% | −612,5 | −9,3% | +393,0 | +6,0% |
| Villa Adelina | −1.989,9 | −20,4% | −1.237,5 | −12,7% | +487,6 | +5,0% |
| Boulogne | −1.718,9 | −26,1% | −1.246,3 | −18,9% | +187,2 | +2,8% |
| **Todo el partido** | 0,0 | 0,0% | **+7.225,2** | +9,7% | **+9.401,9** | +12,6% |

En B con la escala subida, las subas suman 14.453,7 millones y las bajas 7.228,5; el neto es
7.225,2.

**Tabla 3 · Cuántas parcelas pagan más y cuántas menos**

| Localidad | B igual recaudación: suben / bajan | B + 9,7%: suben / bajan | Suba mediana de las que suben (B + 9,7%) | Parcelas que duplican la parte tierra (B + 9,7%) | A: suben | Suba mediana (A) |
|---|---:|---:|---:|---:|---:|---:|
| Acassuso | 11.017 / 5.187 | 12.780 / 3.424 | +22,9% | 66 | 11.017 | +15,4% |
| Martínez | 8.669 / 2.800 | 10.235 / 1.230 | +20,5% | 37 | 8.669 | +14,0% |
| San Isidro | 4.088 / 4.655 | 4.909 / 3.834 | +24,0% | 44 | 4.088 | +15,9% |
| Béccar | 1.399 / 6.163 | 1.735 / 5.827 | +24,3% | 0 | 1.399 | +18,9% |
| Villa Adelina | 1.994 / 10.650 | 2.303 / 10.329 | +20,9% | 0 | 1.994 | +11,1% |
| Boulogne | 987 / 11.035 | 1.194 / 10.828 | +33,1% | 0 | 987 | +25,6% |
| **Todo el partido** | 28.154 / 40.490 | 33.156 / 35.472 | +22,4% | 147 | 28.154 | +15,2% |

**Cuánta gente.** La unidad es la parcela, es decir, el lote. Un edificio es una sola parcela
aunque tenga cien departamentos, y todos se mueven en la misma dirección. Para dar escala, el Censo
2022 cuenta estos hogares: Acassuso 20.795, Martínez 17.032, San Isidro 17.466, Béccar 17.632,
Villa Adelina 19.067 y Boulogne 18.567.

## La boleta típica

Parte tierra en pesos por año, B con la escala subida un 9,7%. Cada cifra es la mediana de su grupo
antes y después.

| Localidad | Parcela mediana hoy | Las que suben: antes → después | Las que bajan: antes → después | En A, las que suben: antes → después |
|---|---:|---:|---:|---:|
| Acassuso | 733.530 | 779.671 → 1.017.520 | 572.062 → 465.074 | 749.702 → 914.514 |
| Martínez | 562.090 | 559.258 → 705.462 | 594.868 → 553.914 | 595.884 → 698.050 |
| San Isidro | 586.484 | 694.362 → 867.772 | 500.754 → 403.907 | 725.010 → 857.582 |
| Béccar | 385.784 | 598.974 → 724.919 | 351.973 → 259.970 | 549.754 → 643.079 |
| Villa Adelina | 408.740 | 758.032 → 885.383 | 385.955 → 231.081 | 787.363 → 864.691 |
| Boulogne | 289.271 | 399.330 → 559.036 | 283.772 → 184.160 | 382.199 → 486.335 |

- **Duplicar.** En B con la escala subida, **147 parcelas duplican o más su parte tierra**: 66 en
  Acassuso, 44 en San Isidro y 37 en Martínez. La mayor suba es de +120%. En A, 40 parcelas llegan
  a duplicar, con un máximo de +101%. La mediana de las subas es +22,4% en B y +15,2% en A.
- **La boleta entera sube menos.** Estos porcentajes son de la parte tierra. La boleta suma además
  la construcción, que no cambia, así que en pesos la suba es la misma, pero como porcentaje de la
  boleta total es menor.
- **Boulogne y Villa Adelina.** La parcela mediana que baja queda por tierra debajo del mínimo:
  184.160 y 231.081 contra 234.000. Esa parte de la baja sólo le llega a quien tiene construcción
  suficiente para estar por encima del mínimo.

## Lo que queda afuera, y cuánto puede mover

**Tabla 4 · El mínimo de $234.000 por año**

| Localidad | Parcelas | Pagan hoy por tierra menos que el mínimo | Baja de B que cae debajo del mínimo (M) |
|---|---:|---:|---:|
| Acassuso | 16.204 | 291 (1,8%) | 12,0 |
| Martínez | 11.469 | 296 (2,6%) | 0,2 |
| San Isidro | 8.743 | 374 (4,3%) | 34,5 |
| Béccar | 7.562 | 1.255 (16,6%) | 101,1 |
| Villa Adelina | 12.644 | 1.232 (9,7%) | 270,4 |
| Boulogne | 12.022 | 4.031 (33,5%) | 399,2 |
| **Todo el partido** | 68.644 | 7.479 (10,9%) | 817,4 |

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
| Base: IUST promedio de la manzana, CMS = 1 | 74.367,6 | 9.401,9 | 12,6% | 9,7% | +26,8% | +17,8% | +2,7% | −9,3% | −12,7% | −18,9% |
| IUST mínimo de la manzana | 68.845,4 | 8.377,5 | 12,2% | 10,5% | +28,1% | +14,6% | +3,4% | −3,5% | −11,5% | −19,9% |
| IUST máximo de la manzana | 80.264,2 | 12.373,9 | 15,4% | 9,0% | +25,9% | +21,2% | +2,4% | −15,2% | −14,0% | −17,9% |
| CMS con lote mínimo de 300 m² | 61.601,8 | 7.681,2 | 12,5% | 11,7% | +28,6% | +21,8% | +6,9% | −6,5% | −12,0% | −18,1% |
| CMS con lote mínimo de 600 m² | 63.431,3 | 7.863,7 | 12,4% | 11,4% | +28,0% | +21,4% | +6,8% | −6,6% | −12,2% | −18,3% |

En todas las variantes, Boulogne, Villa Adelina y Béccar bajan con B, y Acassuso y Martínez suben.

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
