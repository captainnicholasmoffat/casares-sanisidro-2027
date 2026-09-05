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
| `INCONSISTENCIAS.csv` | 172 | Lo que no cierra, con el motivo. No se corrigió nada. |

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
