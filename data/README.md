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
| `INCONSISTENCIAS.csv` | 171 | Lo que no cierra, con el motivo. No se corrigió nada. |

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

## Las inconsistencias que sí importan

De las 171, 160 son informes de trimestre suelto sin columna de crédito y 4 son
redondeos de ±1 peso del formulario de deuda. Quedan 7 sobre informes anuales,
que son hallazgos reales sobre la gestión y no defectos de los datos:

- **Recursos percibidos por encima de lo calculado** en Ingresos no tributarios y
  Rentas de la propiedad (2024 y 2025), y en Transferencias corrientes (2025).
- **Gasto devengado por encima del crédito vigente** en Promoción y asistencia
  social y en Educación y cultural (2025 anual).


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

## Orden de corrida

El parser reescribe los CSV desde los PDF, así que va primero:

```
python3 03_scripts/test_parser.py      # parsea los PDF y valida
python3 03_scripts/deflactor.py        # baja el IPC, empalma y deflacta
python3 03_scripts/test_deflactor.py   # test dorado del empalme + validaciones
```

Al revés, el parser se lleva puestas las columnas del deflactor.
`test_deflactor.py` lo detecta y lo dice.

## Verificación

```
python3 03_scripts/test_parser.py
```

Corre primero el test dorado (los 7 devengados de 2025 IV contra los valores
leídos a mano del PDF) y después valida cada trimestre: que las partes sumen el
total general del propio PDF, que crédito aprobado + modificaciones dé crédito
vigente, y que el devengado no supere el vigente.
