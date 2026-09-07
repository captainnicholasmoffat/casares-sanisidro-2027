# Metodología del deflactor

Todas las series fiscales del repo están en pesos corrientes y cubren 2010-2026,
un período con años de inflación superior al 200%. Sin deflactar no se pueden
comparar entre años ni proyectar. Este documento explica cómo se construyó el
índice de precios que las convierte a pesos constantes de **diciembre de 2025**.

Nada acá está estimado ni interpolado. El único ajuste es un empalme entre dos
series oficiales, y consiste en multiplicar por una constante que se publica más
abajo.

---

## 1. Qué serie cubre qué período

| Período | Serie | Organismo | Base original |
|---|---|---|---|
| **2010-01 → 2016-11** (83 meses) | IPC de la Provincia de San Luis, nivel general, mensual | Dirección Provincial de Estadística y Censos de San Luis | 2003 = 100 |
| **2016-12 → 2026-07** (116 meses) | IPC Nacional, nivel general, mensual | INDEC | diciembre 2016 = 100 |

El punto de empalme es exacto: **noviembre de 2016 → diciembre de 2016**.
Noviembre de 2016 y todo lo anterior es San Luis. Diciembre de 2016 y todo lo
posterior es INDEC.

### Por qué hay empalme

El IPC nacional del INDEC **arranca en diciembre de 2016**. Para 2010-2016 no
existe serie oficial nacional continua, por el período de intervención del
organismo. No se inventó ni se interpoló nada para tapar ese hueco: se usó otra
serie oficial que sí lo cubre.

### Por qué San Luis y no CABA

El orden de preferencia era IPC de Provincia de Buenos Aires o CABA primero, San
Luis o IPC Congreso después. Se descartaron los dos primeros:

- **Provincia de Buenos Aires no publica IPC propio.** No hay serie que bajar.
- **El IPCBA de CABA arranca en julio de 2012.** Aun usándolo, harían falta 30
  meses más (2010-01 a 2012-06) de una tercera serie: serían **dos** empalmes en
  vez de uno. Además el sitio del Instituto de Estadística y Censos de CABA
  devolvió HTTP 503 en todas sus páginas de descarga durante la construcción.
- **El IPC Congreso no tiene publicador oficial con URL estable.** Habría que
  reconstruirlo de fuentes secundarias, que es exactamente lo que no queremos.

El IPC de San Luis es oficial, provincial, mensual, continuo desde octubre de
2005, y se distribuye por el portal de datos abiertos del Estado nacional con URL
estable. Cubre todo el hueco con **un solo** empalme.

---

## 2. El coeficiente de empalme

Las dos series se solapan en **diciembre de 2016**. El coeficiente es el cociente
de los dos valores de ese mes:

```
                IPC INDEC nacional (dic-2016)        100
        k  =  ---------------------------------  =  ---------  =  0.0740477460
                IPC San Luis nivel general (dic-2016)   1350.48
```

Y para todo mes anterior a diciembre de 2016:

```
        índice_empalmado(mes)  =  IPC_San_Luis(mes)  ×  0.0740477460
```

**Cómo rehacer el cálculo.** Con las dos series públicas, sin correr nada de este
repo:

1. Bajar `serie_ipc_divisiones.csv` del INDEC y filtrar `Codigo=0`,
   `Region=Nacional`, `Periodo=201612` → **100**.
2. Bajar el CSV del IPC de San Luis y buscar `indice_tiempo=2016-12-01`,
   columna `nivel_general` → **1350.48**.
3. `100 / 1350.48 = 0.0740477460` (10 decimales, redondeo bancario a medio
   arriba).
4. Multiplicar por ese número cualquier mes de San Luis anterior a dic-2016.

Ejemplo verificable, noviembre de 2016:
`1339.02 × 0.0740477460 = 99.1514`, que es el valor de esa fila en
`data/ipc_indec_mensual.csv`.

### El empalme no inventa inflación

Multiplicar toda una serie por una constante **no cambia sus variaciones
mensuales**. La variación de diciembre de 2016 sobre noviembre de 2016 en el
índice empalmado da **0,8558%**, que es exactamente la variación que publica San
Luis para ese mes (1350,48 / 1339,02 − 1). No hay salto de nivel artificial en la
juntura. Eso lo verifica `03_scripts/test_deflactor.py` en el test dorado.

Lo que el empalme **sí** asume es que la inflación de San Luis 2010-2016 es una
aproximación razonable de la inflación nacional de esos años. Es un supuesto, y
está declarado. Ver la sección 6.

---

## 3. El deflactor

Base: **diciembre de 2025 = 100**. Convención:

```
        coeficiente(período)  =  IPC(dic-2025) / IPC(período)

        monto_constante_dic2025  =  monto_nominal  ×  coeficiente
```

Diciembre de 2025 se deflacta a sí mismo: su coeficiente es exactamente 1.

`data/deflactor.csv` trae, por año, los dos coeficientes que pide el modelo:

- **`coef_anual`** — contra el promedio del año. Es el que va para flujos:
  gasto ejecutado, recursos percibidos, cualquier cosa que se acumula a lo largo
  del año.
- **`coef_diciembre`** — contra el índice de diciembre de ese año. Es el que va
  para stocks: deuda, saldos, cualquier cosa medida a una fecha.

El promedio anual se pondera por días del mes, no por mes simple, para que un
informe acumulado de enero a diciembre y el coeficiente anual den lo mismo.

**2026 es parcial.** El IPC llega hasta julio de 2026, así que `coef_anual` de
2026 sale de 7 meses y `coef_diciembre` queda vacío. La columna `cobertura`
lo dice.

### Los coeficientes se publican redondeados y se usan redondeados

El coeficiente se redondea a 8 decimales y **es ese valor publicado el que
multiplica**. No se usa una precisión interna mayor. Así cualquiera toma el CSV,
multiplica `monto_nominal × coef_deflactor` y obtiene exactamente
`monto_constante_dic2025`, hasta el centavo, sin reconstruir la aritmética del
script. `test_deflactor.py` recalcula los 1.620 importes uno por uno.

---

## 4. Cómo se elige el coeficiente de cada fila

Esto es lo delicado, porque **los trimestres publicados por el Municipio no son
homogéneos**: los informes I y IV son acumulados desde enero, y los II y III son
el trimestre suelto. Está en la columna `periodo_tipo`.

La regla es no mirar la etiqueta del trimestre sino **el rango de fechas real del
informe** (`periodo_desde` → `periodo_hasta`), y calcular el nivel de precios
medio de ese rango ponderando cada mes por los días que aporta.

| `periodo_tipo` | Rango | Meses que entran al coeficiente |
|---|---|---|
| `trimestre` | p. ej. 1/4 → 30/6 | los 3 del trimestre |
| `acumulado_anual` | 2/1 → 30/12 | los 12 del año |
| `acumulado_parcial` | 1/1 → 4/5/2026 | ene a abr completos + 4 días de mayo |

Así un acumulado anual nunca se deflacta con el índice de un solo trimestre.

Cada rango distinto que aparece en los datasets está listado con su coeficiente,
su promedio de IPC y el detalle de días por mes en
**`data/deflactor_periodos.csv`**. Son 11 rangos.

Para el stock de deuda no se usa promedio de período sino el índice del mes de la
`fecha_corte`, porque es un stock a una fecha, no un flujo.

Para datos anuales (rendiciones, fallos del Tribunal de Cuentas) se usa
`coef_anual`.

---

## 5. Qué columnas se agregaron

Ninguna columna nominal se pisó. A cada dataset se le agregaron:

| Columna | Qué es |
|---|---|
| `coef_deflactor` | El multiplicador usado en esa fila. |
| `base_coef` | De qué período salió, en texto, con el detalle de días por mes. |
| `monto_constante_dic2025` | La cifra principal del dataset, ya deflactada. |
| `<columna>_const_dic2025` | Lo mismo para cada otra columna de importes. |

Cuál es la "cifra principal" de cada dataset:

| Dataset | Columna principal |
|---|---|
| `data/ejecucion_gastos_objeto.csv` | `devengado` |
| `data/ejecucion_recursos.csv` | `percibido` |
| `data/gastos_finalidad_funcion.csv` | `devengado` |
| `data/deuda_stock.csv` | `saldo` |
| `SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv` | `monto_pesos` |

---

## 6. Lo que hay que declarar al usar esto

**Cualquier comparación que cruce diciembre de 2016 lleva nota al pie.** No se
esconde: se declara. La nota mínima es esta:

> Las cifras anteriores a diciembre de 2016 se deflactaron con el IPC de la
> Provincia de San Luis (Dirección Provincial de Estadística y Censos), empalmado
> al IPC Nacional del INDEC en diciembre de 2016 mediante el coeficiente
> 100 / 1350,48 = 0,0740477460. El INDEC no publica IPC nacional anterior a esa
> fecha por el período de intervención del organismo.

Un economista que encuentre el empalme sin que se lo hayamos dicho nos rompe el
informe. Uno que lo lea declarado, con el coeficiente a la vista y la cuenta
reproducible, no tiene nada que decir.

Los años afectados en la serie de gastos totales son **2014, 2015 y 2016**. De
2017 en adelante es INDEC puro.

---

## 7. Qué está deflactado y qué falta

Diez datasets llevan pesos constantes:

| Dataset | Columna principal | Coeficiente |
|---|---|---|
| `data/presupuesto_historico_2010_2026.csv` | `monto` | anual |
| `data/rendiciones_2010_2021.csv` | `monto` | anual |
| `data/presupuestado_vs_ejecutado.csv` | `ejecutado` | anual |
| `data/ejecucion_gastos_objeto.csv` | `devengado` | del período del informe |
| `data/ejecucion_recursos.csv` | `percibido` | del período del informe |
| `data/gastos_finalidad_funcion.csv` | `devengado` | del período del informe |
| `data/deuda_stock.csv` | `saldo` | del mes de la fecha de corte |
| `SanIsidro_datos_fiscales/DATOS_SanIsidro_2014-2022.csv` | `monto_pesos` | anual |
| `DATOS_SanIsidro_2014-2022.csv` (copia en la raíz) | `monto_pesos` | anual |
| `02_clean/transferencias_pba_2021_2026.csv` | `monto` | del mes |

**Dos columnas que NO se deflactan y hay que dejar quietas:** `porcentaje` en
`rendiciones_2010_2021.csv` y `diferencia_pct` en `presupuestado_vs_ejecutado.csv`.
Son porcentajes, no importes. Deflactarlos no significaría nada. Están fuera de
la lista de columnas de plata en el script.

**El presupuesto 2026 es parcial.** El IPC llega a julio de 2026, así que su
coeficiente anual sale de 7 meses. La columna `base_coef` de esa fila lo dice:
*"anual 2026, promedio de 7 meses ponderado por días"*.

Las transferencias provinciales son **mensuales**, así que cada fila va con el
coeficiente de su mes, que sale del rango de fechas de la propia fila.

### Lo que falta

Nada de la lista original. Los diez datasets del repo llevan pesos constantes.

## 7 bis. La serie real de gastos totales

`data/serie_gastos_totales_real.csv` cubre **13 años entre 2010 y 2025**.
Faltan 2013, 2018 y 2023, que no tienen rendición publicada.

Hay tres fuentes y no todas cubren los mismos años. Cuando dos coinciden en un
año gana la de menor rango, y el rango queda escrito en la columna
`prioridad_fuente`:

| Rango | Fuente | Años que aporta |
|---:|---|---|
| 1 | Fallo del Tribunal de Cuentas o rendición, concepto *"Gastos con imputación al presupuesto"* | 2014-2017, 2022 |
| 2 | Rendición de cuentas parseada del PDF, fila `total_gastos` | 2010-2012, 2019-2021 |
| 3 | Informe trimestral de ejecución, acumulado anual: suma del devengado de los objetos | 2024, 2025 |

Nada se promedia ni se corrige: se elige una fila publicada y se dice cuál.
La columna `concepto` dice qué mide cada año y `brecha_anios` cuántos años hay
entre un punto y el anterior, para que nadie lea como variación interanual lo
que en realidad acumula dos o tres años.

**Ningún año varía más de 40% en términos reales contra el anterior**, así que
`data/SALTOS_REALES.csv` queda con la cabecera y sin filas. El mayor movimiento
es −21,3% en 2024 contra 2022, que son dos años.

## 8. Archivos

| Archivo | Qué es |
|---|---|
| `01_raw/indec/serie_ipc_divisiones.csv` | IPC del INDEC, crudo, como lo publica. |
| `01_raw/indec/indice-precios-consumidor-san-luis-2003-100.csv` | IPC de San Luis, crudo. |
| `01_raw/indec/DESCARGA.txt` | URL, fecha, tamaño y md5 de las dos descargas. |
| `data/ipc_indec_mensual.csv` | La serie mensual empalmada, 199 meses. Columna `serie_origen` en cada fila. |
| `data/deflactor.csv` | Coeficiente anual y a diciembre, por año. |
| `data/deflactor_periodos.csv` | Coeficiente de cada rango de fechas de los informes trimestrales. |
| `data/serie_gastos_totales_real.csv` | Gasto total por año en pesos de dic-2025. |
| `data/SALTOS_REALES.csv` | Años con variación real mayor a 40%. Para revisión humana. |
| `03_scripts/deflactor.py` | Baja, empalma, construye y aplica. |
| `03_scripts/test_deflactor.py` | Test dorado del empalme y validaciones. |

## 9. Descargas

| Archivo | URL | md5 |
|---|---|---|
| `serie_ipc_divisiones.csv` | https://www.indec.gob.ar/ftp/cuadros/economia/serie_ipc_divisiones.csv | `b7e0d9e9bf298f1e97147bcc4e56472f` |
| `indice-precios-consumidor-san-luis-2003-100.csv` | https://infra.datos.gob.ar/catalog/sspm/dataset/197/distribution/197.1/download/indice-precios-consumidor-san-luis-2003-100.csv | `0598d92a32f3a02e62794ad2cbc4a421` |

Fecha de descarga: **2026-09-05**.

## 10. Verificación

```
python3 03_scripts/deflactor.py        # reconstruye todo desde las fuentes
python3 03_scripts/test_deflactor.py   # test dorado + validaciones
```
