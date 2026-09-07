# Series parseadas de la ejecución presupuestaria

Generado por `03_scripts/parse_ejecucion.py` desde los PDF de
`01_raw/sanisidro_transparencia/`. Validado por `03_scripts/test_parser.py`.

Ningún número está estimado, interpolado ni corregido. Toda fila lleva la
columna `fuente` con el PDF del que salió. Los importes son texto decimal con
dos decimales y sin separadores de miles; internamente se calculan como enteros
en centavos, así que no hay redondeo de punto flotante en ningún paso.

| Archivo | Filas | Qué contiene |
|---|---:|---|
| `ejecucion_gastos_objeto.csv` | 57 | Los 7 objetos del gasto por trimestre. |
| `ejecucion_recursos.csv` | 58 | Los rubros de recursos por trimestre. |
| `gastos_finalidad_funcion.csv` | 228 | Finalidades y funciones (columna `nivel`). |
| `deuda_stock.csv` | 108 | Stock de deuda del formulario Ley 12.462. |
| `presupuesto_historico_2010_2026.csv` | 110 | Serie presupuestaria por año y concepto, pesos corrientes. |
| `rendiciones_2010_2021.csv` | 122 | Ejecución real por año y concepto, pesos corrientes. |
| `presupuestado_vs_ejecutado.csv` | 10 | Presupuesto contra rendición, años con los dos. |
| `INCONSISTENCIAS.csv` | 174 | Lo que no cierra, con el motivo. No se corrigió nada. |

## Leer esto antes de sumar nada

**Los trimestres NO son homogéneos.** El período de cada informe está en las
columnas `periodo_desde`, `periodo_hasta` y `periodo_tipo`:

| Trimestre | Rango típico | Qué es |
|---|---|---|
| I | 2/1 → 31/3 | El trimestre (y a la vez el acumulado a marzo). |
| II | 1/4 → 30/6 | **Sólo** el trimestre, no acumulado. |
| III | 1/7 → 30/9 | **Sólo** el trimestre, no acumulado. |
| IV | 2/1 → 30/12 | **Acumulado anual**, no el trimestre. |

Sumar I + II + III + IV cuenta el año más de una vez. Para una serie anual usar
sólo el IV; para trimestres sueltos, I, II y III, y despejar el IV restando.

Dos rangos se salen del molde y están marcados en `periodo_tipo`:
`2026_i_gastos_por_fyf.pdf` cubre 1/1/2026 → 4/5/2026 (no es un trimestre) y
`2026_i_*` arranca el 1/1 en vez del 2/1.

## Huecos y rarezas de la fuente

- **Falta 2025 III de gastos por objeto.** El Municipio publicó por error una
  copia del PDF de finalidad y función en su lugar. El hueco queda explícito: no
  hay filas de 2025 III en `ejecucion_gastos_objeto.csv` y no se interpoló nada.
- **2024 I no tiene el objeto 6 (Activos financieros).** No hubo movimiento y la
  fila no existe en el PDF. No se inventó un cero.
- **Los informes de trimestre suelto vienen sin columnas de crédito.** Cuando el
  rango no arranca en enero, el Municipio publica `credito_aprobado`,
  `modificaciones` y `credito_vigente` vacías o parciales. De ahí salen 160 de
  las 171 inconsistencias: no son errores del parseo sino del informe publicado.
- **`stock_de_deuda_-_i_trim_2024_msi.pdf` está mal archivado.** No es un stock
  de deuda: es un estado de ejecución de gastos por fuente de financiamiento.
  Ver `NO_PARSEADOS.md`.
- **`2025_iii_gastos_por_fyf_0.pdf` es copia byte a byte** de
  `2025_iii_gastos_por_fyf.pdf` (mismo md5). Se procesa una sola vez.

## Desglose de las inconsistencias

De las 171, 160 son informes de trimestre suelto sin columna de crédito y 4 son
redondeos de ±1 peso del formulario de deuda.

7 filas quedan sin explicar y requieren revisión manual. No se interpretan en
este archivo. Están en `INCONSISTENCIAS.csv` con `periodo_tipo = acumulado_anual`.


## Pesos constantes

Todas las series están además en pesos constantes de **diciembre de 2025**. La
columna nominal nunca se pisa: al lado de cada importe hay uno deflactado.

| Archivo | Qué contiene |
|---|---|
| `ipc_indec_mensual.csv` | IPC mensual 2010-01 a 2026-07. IPC del INDEC desde dic-2016, IPC de San Luis empalmado antes. Columna `serie_origen` en cada fila. |
| `deflactor.csv` | Coeficiente anual y a diciembre, por año. Base dic-2025 = 100. |
| `deflactor_periodos.csv` | Coeficiente de cada rango de fechas de los informes trimestrales, con el detalle de días por mes. |
| `serie_gastos_totales_real.csv` | Gasto total por año en pesos de dic-2025. |
| `SALTOS_REALES.csv` | Años con variación real mayor a 40%. Para revisión humana, sin corregir. |
| `METODOLOGIA_DEFLACTOR.md` | El empalme, el coeficiente y cómo rehacer la cuenta. **Leer antes de comparar años.** |

Columnas agregadas a cada dataset: `coef_deflactor`, `base_coef`,
`monto_constante_dic2025` y `<columna>_const_dic2025` para cada importe.

**Cualquier comparación que cruce diciembre de 2016 lleva nota al pie sobre el
empalme.** La nota está escrita en `METODOLOGIA_DEFLACTOR.md`, sección 6.


## Mapa territorial (Censo 2022)

| Archivo | Qué contiene |
|---|---|
| `radios_censales_sanisidro.geojson` | Los 360 radios censales del partido, código INDEC 06756. |
| `censo2022_sanisidro_por_radio.csv` | 105 columnas por radio: población, hogares, viviendas, NBI, IPMH, hacinamiento, tenencia, agua, cloacas, gas, educación y edad. |
| `censo2022_diccionario_columnas.csv` | Qué es cada columna y de qué variable de Redatam sale. |
| `censo2022_sanisidro_otros_niveles.csv` | Lo que el Censo no publica por radio, al nivel que sí existe. |
| `zonas_propuestas_sanisidro.geojson` | Las 6 zonas vecinales con sus indicadores. |
| `zonas_indicadores.csv` | Indicadores por zona, de peor a mejor. |
| `zonas_asignacion_radios.csv` | La zona de cada radio. |
| `zonas_excepciones.csv` | Los radios movidos por la excepción de conglomerado crítico. |
| `METODOLOGIA_ZONAS.md` | La regla completa. **Leer antes de usar el mapa.** |
| `NO_DISPONIBLE.md` | Lo que no está y a qué nivel sí. |

**Los límites de las zonas son nuestros, no oficiales.** Lo único oficial es la
geometría de los radios del INDEC y los 6 puntos BAHRA de las localidades.
Cuando se publique el mapa hay que decirlo.

Los radios se identifican por código y fracción censal, nunca por nombre de
barrio: los barrios no existen como dato oficial.


## Serie de gasto comparable

**Para comparar entre años usar `serie_gastos_comparable.csv`, no la otra.**

| Archivo | Qué contiene |
|---|---|
| `serie_gastos_comparable.csv` | Un solo concepto en todos los años: gastos corrientes + de capital, sin aplicaciones financieras. 13 años entre 2010 y 2025. Los años sin dato van vacíos. |
| `conceptos_disponibles_por_anio.csv` | Todos los conceptos de gasto de cada año en todas las fuentes, ejecutado y presupuestado. |
| `COMPARACIONES_VALIDAS.md` | Qué pares de años se pueden comparar y cuáles no. **Leer antes de citar cualquier variación.** |
| `serie_gastos_totales_real.csv` | Material de trabajo. **Mezcla 6 conceptos distintos** según el año; lleva la advertencia arriba del archivo. |

El `total de gastos` de las rendiciones cambia de contenido a mitad de camino:
en 2010-2012 incluye las aplicaciones financieras y en 2019-2021 no. Es el paso
al formato Ahorro-Inversión de los informes ARSI. Por eso la serie heterogénea
no sirve para comparar.

## Orden de corrida

El parser reescribe los CSV desde los PDF, así que va primero:

```
python3 03_scripts/test_parser.py      # parsea los PDF y valida
python3 03_scripts/deflactor.py        # baja el IPC, empalma y deflacta
python3 03_scripts/test_deflactor.py   # test dorado del empalme + validaciones

python3 03_scripts/censo_radios.py     # radios y datos del Censo 2022
python3 03_scripts/zonas.py            # arma las 6 zonas
python3 03_scripts/test_censo_zonas.py # validaciones del censo y las zonas

python3 03_scripts/serie_comparable.py      # serie de un solo concepto
python3 03_scripts/test_serie_comparable.py # validaciones de la serie
```

`serie_comparable.py` va DESPUÉS del deflactor: lee los importes constantes que
el deflactor deja en cada dataset.

Al revés, el parser se lleva puestas las columnas del deflactor: reescribe
desde los PDF no sólo la ejecución trimestral sino también
`presupuesto_historico_2010_2026.csv`, `rendiciones_2010_2021.csv` y
`presupuestado_vs_ejecutado.csv`. `test_deflactor.py` lo detecta y lo dice.

## Verificación

```
python3 03_scripts/test_parser.py
```

Corre primero el test dorado (los 7 devengados de 2025 IV contra los valores
leídos a mano del PDF) y después valida cada trimestre: que las partes sumen el
total general del propio PDF, que crédito aprobado + modificaciones dé crédito
vigente, y que el devengado no supere el vigente.


# Serie presupuestaria histórica

`presupuesto_historico_2010_2026.csv`, generado por
`03_scripts/parse_presupuestos.py` desde `01_raw/presupuestos/`. **Pesos
corrientes, sin deflactar.** Son años con inflación muy distinta: no se pueden
comparar entre sí sin ajustar primero.

Columnas: `anio`, `concepto`, `subconcepto`, `monto`, `fuente`, `pagina`.
Conceptos: `total_recursos`, `total_gastos`, `recursos_por_origen` (municipal,
provincial, nacional, otros) y `gastos_por_objeto` (los rubros del clasificador).

## Qué año tiene qué

| Año | Total recursos | Total gastos | Por origen | Por objeto |
|---|:-:|:-:|:-:|:-:|
| 2011 | sí | sí | sí | sí |
| 2012 | sí | sí | sí | sí |
| 2013 | sí | sí | sí | sí |
| 2018 | sí | sí | sí | sí |
| 2019 | sí | sí | sí | sí |
| 2020 | sí | sí | sí | sí |
| 2021 | sí | sí | sí | sí |
| 2023 | sí | sí | sí | no |
| 2024 | sí | no | sí | sí |
| 2025 | sí | sí | no | sí |

Faltan 2010, 2014, 2015, 2016, 2017, 2022 y 2026: sus PDF no tienen los números
en texto. El motivo exacto de cada uno está en `NO_PARSEADOS.md`.

Los años parciales, uno por uno:

- **2023** no trae gastos por objeto en forma directa. La lámina los publica
  abierta por fuente de financiamiento (tesoro municipal, origen municipal,
  provincial, nacional) y sin total de fila. Sumar las cuatro columnas sería
  derivarlo, así que se dejó vacío.
- **2024** sale de dos documentos distintos y ninguno trae todo: la ordenanza
  sancionada (`presupuesto_2024_hcd.pdf`) tiene recursos por origen, y el
  reporte de sistema (`2024_presupuesto_de_recursos_y_gastos_por_rubro_y_objeto.pdf`)
  tiene gastos por objeto. **Los dos coinciden en el total: 155.971.165.667.**
  Cada fila lleva su `fuente`; no se promedió ni se eligió uno.
- **2025** no publica el desagregado por origen en el documento disponible.

## Validación

- **Ancla 2011.** Los cuatro orígenes de `presupuesto2011.pdf` p.4 tienen que dar
  exactamente 397.985.000 / 213.310.400 / 6.144.000 / 13.115.000. Si no, el
  parser está mal. Lo chequea `test_parser.py`.
- **Por documento:** que los orígenes sumen el total de recursos y que los
  objetos sumen el total de gastos.

Todos los años cierran menos uno: **`informe_arsi_presupuesto_2020.pdf` no cierra
consigo mismo.** Sus seis objetos del gasto suman 17.591.205.467 pero la línea
TOTALES del mismo informe dice 17.501.205.467, 90.000.000 menos. Está extraído
tal como lo publicó el Municipio y anotado en `INCONSISTENCIAS.csv`.

## Cosas que hubo que resolver para leer estos PDF

- **Dos convenciones numéricas mezcladas**, a veces en el mismo archivo:
  `1,234,567.89` en unos años y `1.234.567,89` en otros.
- **Importes partidos en dos pedazos.** En el presupuesto 2013 la fila sale como
  `Recursos Humanos$    4 69.900.000,00`: son 469.900.000,00, no un 4 seguido de
  69 millones. La reconstrucción se validó contra el total del propio PDF, que da
  exacto.
- **Porcentajes pegados al importe sin el signo `%`.** En 2018:
  `SERVICIOS NO PERSONALES$2,174,919,800.0036.25`.
- **Rótulos desacoplados de sus importes.** En la ordenanza 2024 los montos de
  "Origen Municipal" se imprimen en la línea de arriba del rótulo y los de
  "Otros Orígenes" en la de abajo.


# Rendiciones de cuentas: la ejecución real

`rendiciones_2010_2021.csv`, generado por `03_scripts/parse_rendiciones.py` desde
`01_raw/sanisidro_transparencia/rendicion_de_cuentas/`. **Pesos corrientes, sin
deflactar.**

El presupuesto dice lo proyectado; la rendición, lo que efectivamente pasó.
Columnas: `anio`, `concepto`, `subconcepto`, `monto`, `porcentaje`, `fuente`,
`pagina`. El `porcentaje` es el que publica el documento, no uno calculado.

## Qué año tiene qué

| Año | Recursos por rubro | Gastos por carácter | Por jurisdicción | Por objeto | Por origen | Resultado |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 2010 | sí | sí | sí | sí | sí | no |
| 2011 | sí | sí | sí | sí | no | no |
| 2012 | sí | sí | sí | sí | no | no |
| 2019 | sí | sí | no | no | no | sí |
| 2020 | sí | sí | no | no | no | sí |
| 2021 | sí | sí | no | no | no | sí |

Faltan 2013 a 2018 y 2022: sus PDF tienen las tablas como imagen. Motivo por
archivo en `NO_PARSEADOS.md`.

**2010 no publica un total de recursos.** La lámina de rubros no lo trae, así que
no hay contra qué validar la suma de los seis rubros.

## Una diferencia de definición, no de datos

Los informes ARSI (2019–2021) publican una **Cuenta Ahorro-Inversión-
Financiamiento**, donde las aplicaciones financieras van *debajo de la línea* y
no entran en "GASTOS TOTALES". Las rendiciones 2010–2012, en cambio, sí las
incluyen en su total de gastos por carácter económico.

Por eso la validación compara distinto según el documento: en ARSI, corrientes +
capital contra el total publicado; en 2010–2012, los tres conceptos. Sin esa
distinción aparecerían tres inconsistencias que no son de datos.

## Qué hubo que resolver

La rendición 2010 son **gráficos de torta**, no tablas. Cada etiqueta es un
bloque suelto alrededor del gráfico y el texto sale desordenado respecto del
resto de la página, así que no se puede leer por líneas. Se agrupan las palabras
en bloques por cercanía y se arma cada bloque por separado. Dos detalles:

- **Un importe se parte al medio entre dos renglones:** `$323.337.114,5` arriba y
  `1` abajo son 323.337.114,51. Se repara sólo cuando el primer pedazo quedó con
  una sola cifra decimal, que es la condición que hace segura la reconstrucción:
  `$50.574.013` (sin decimales) y `$2.577.753,19` (con las dos) no se tocan.
- **Dos etiquetas vecinas pueden caer en el mismo bloque.** Se buscan todas las
  apariciones de importe dentro de cada bloque, no una sola.

# Presupuestado contra ejecutado

`presupuestado_vs_ejecutado.csv`, para los cinco años con los dos documentos
(2011, 2012, 2019, 2020, 2021). Trae las dos cifras, la diferencia en pesos y en
porcentaje, y las dos fuentes. **No hay interpretación:** una diferencia entre
presupuestado y ejecutado puede ser subejecución, refuerzo presupuestario o
diferencia de criterio contable, y eso no se decide desde una resta.

La columna `nota` marca los años ARSI, donde las dos cifras de gasto no son
directamente comparables por lo de las aplicaciones financieras.

# Hallazgos sobre las fuentes

Tres documentos no cierran consigo mismos. Están extraídos tal como los publicó
el Municipio y anotados en `INCONSISTENCIAS.csv`:

| Documento | Qué pasa |
|---|---|
| `informe_arsi_presupuesto_2020.pdf` | Sus seis objetos del gasto suman 90.000.000 más que su propia línea TOTALES. |
| `rendicion2010.pdf` (carácter económico) | Los tres conceptos suman 1,74 pesos menos que el total del título: el gráfico redondea a pesos enteros y el título lleva centavos. |
| `rendicion2010.pdf` (origen de los recursos) | El título dice 588.384.592,29 pero los cuatro orígenes suman 558.384.592,29. Son 30.000.000 de diferencia y parece un error de tipeo en el 5 inicial. |

**El error de ARSI 2020 no es del formato.** Se verificó contra las tres
rendiciones ARSI (2019, 2020, 2021) y las tres cierran consigo mismas: rubros
contra total de recursos y gastos contra total de gastos. Es un problema puntual
del informe de presupuesto 2020. `test_parser.py` lo chequea en cada corrida.
