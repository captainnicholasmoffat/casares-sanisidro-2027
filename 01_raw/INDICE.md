# Índice de datos crudos — `01_raw/`

Fuentes oficiales descargadas para el proyecto San Isidro 2027. **Los nombres de
archivo son los originales de la fuente y no se renombran**: son la trazabilidad
contra la URL de origen registrada en `INVENTARIO.txt`.

Totales: **121 archivos** — 89 PDF, 15 HTML.GZ, 13 XLSX, 3 CSV y 1 ZIP. Los 89
PDF los bajó el worker de Chrome; el resto se bajó a mano o con un script del
repo. **Todos** están registrados en `INVENTARIO.txt` con su tamaño y su origen,
y `03_scripts/verificar_inventario.py` sale en 0 cuando el disco coincide con el
inventario.

Los años de la tabla se derivan del nombre de archivo, que es lo único
verificable sin abrir los PDFs. Ningún PDF fue parseado todavía.

## Tabla

| Carpeta | Archivos | Años cubiertos | Qué contiene |
|---|---:|---|---|
| `sanisidro_transparencia/ejecucion_presupuestaria/` | 19 PDF | 2024–2026 | Ejecución trimestral: recursos y gastos por objeto. 2024 completo (I–IV), 2025 sin gastos por objeto del III trim. (el Municipio nunca lo publicó), 2026 hasta el II trim. |
| `sanisidro_transparencia/situacion_economico_financiera/` | 13 PDF | 2010, 2012, 2013, 2024–2026 | Estado de situación económico-financiera (SEF). Serie vieja suelta (2010, 2012, 2013) y serie trimestral moderna 2024–2026. |
| `sanisidro_transparencia/deuda_publica/` | 11 PDF | 2024–2026 | Stock de deuda trimestral. 2024 y 2025 completos (I–IV), 2026 hasta el II trim. Hay dos PDF distintos del I trim. 2024, con URL propia cada uno. |
| `sanisidro_transparencia/gastos_por_finalidad_y_funcion/` | 11 PDF | 2024–2026 | Gasto clasificado por finalidad y función, trimestral. Dos de los 11 son el mismo archivo del III trim. 2025 (ver notas), así que cubre 10 trimestres distintos. |
| `sanisidro_transparencia/rendicion_de_cuentas/` | 10 PDF | 2010–2012, 2014, 2015, 2017, 2019–2022 | Rendición de cuentas anual del Municipio. Faltan 2013, 2016, 2018, 2023–2026. |
| `sanisidro_transparencia/ordenanza_fiscal_impositiva/` | 5 PDF | 2022–2024 | Ordenanzas fiscal e impositiva (alícuotas y tasas). Incluye la exposición de motivos 2022 ante el HCD. |
| `sanisidro_transparencia/otros/` | 1 PDF | 2024–2025 | Documento de prioridades estratégicas del Municipio. |
| `presupuestos/` | 19 PDF | 2010–2014, 2016–2026 (falta 2015) | Presupuestos municipales: ordenanzas, presentaciones ante el HCD e informes ARSI. Un archivo (`ordenanza_presupuesto_hcd_-_msi_2.pdf`) no lleva año en el nombre. |
| `transferencias_pba/` | 13 XLSX | 2021–2026 (cortes a diciembre; 2026 a junio) | Transferencias y descentralización de la Provincia de Buenos Aires a los municipios. Descarga manual del usuario (ver abajo). |
| `rafam_2025_106_municipios.csv` | 1 CSV | 2025 | Ejecución presupuestaria 2025 de **106 de los 135** municipios bonaerenses, del RAFAM provincial. Capturado el 2026-09-03 de `la-verdadera-pba.pages.dev`, un sitio de **terceros** que procesa datos oficiales de RAFAM. **No es la fuente oficial**: ver la advertencia en `NO_DESCARGADOS.txt`. Es la fuente del EXHIBIT 05. |
| `censo2022/` | 1 ZIP + 15 HTML.GZ | 2022 | Geometría de los radios censales (catálogo de datos de la Provincia) y las respuestas crudas del motor Redatam del INDEC. Las baja `03_scripts/censo_radios.py`, no el worker. |
| `indec/` | 2 CSV | 2003–2026 | Serie IPC por divisiones del INDEC y el IPC de San Luis usado para el empalme anterior a dic-2016. Detalle con md5 en `indec/DESCARGA.txt`. |

## Archivos de control

| Archivo | Qué es |
|---|---|
| `INVENTARIO.txt` | Lista de los 89 PDF descargados por el worker de Chrome, con tamaño en bytes y URL de origen. Verificable con `03_scripts/verificar_inventario.py`. |
| `NO_DESCARGADOS.txt` | Lo que no se pudo bajar, en tres bloques: 25 XLSX de la Provincia (`www.ec.gba.gov.ar`, el host no acepta conexiones desde el entorno del worker); el portal `datos.sanisidro.gob.ar` caído con 504; y las secciones que el sitio de Transparencia directamente no publica (organigrama, planta de personal, DDJJ de funcionarios, compras y licitaciones). |

## Notas de trazabilidad

- **Los 13 XLSX no figuran en `INVENTARIO.txt`.** Se bajaron a mano desde el
  navegador del usuario porque el host de la Provincia bloquea al worker. El
  script de verificación los cuenta aparte y no los marca como sobrantes.
- **De los 25 XLSX provinciales pendientes se recuperaron exactamente 13.** Los
  13 archivos en disco cruzan uno a uno contra 13 de las 25 URLs de
  `NO_DESCARGADOS.txt`; no sobra ninguno. Siguen faltando 12:
  las dos series agregadas 2003–2015 y los cortes a diciembre de 2016, 2017,
  2018, 2019 y 2020 (transferencias y descentralización de cada año).
- **Un XLSX lleva sufijo del navegador:** `12-25 - Transferencias Diciembre 2025
  (2).xlsx`. En la fuente es `... Diciembre 2025.xlsx`; el `(2)` lo agregó
  Chrome al descargar. No se renombró para no romper la trazabilidad.
- **La ruta de `presupuestos/` cambió al reordenar el repo.** `INVENTARIO.txt` la
  registra como `sanisidro_transparencia/presupuestos/`; ahora cuelga de
  `01_raw/presupuestos/`. El script de verificación normaliza esa ruta.
- **Un duplicado real, verificado por md5:** `2025_iii_gastos_por_fyf.pdf` y
  `2025_iii_gastos_por_fyf_0.pdf` son byte-idénticos
  (`ef7e74aaed2dcc4f18d017c416a220e7`). No es un error de descarga: según
  `NO_DESCARGADOS.txt`, el Municipio subió ese PDF dos veces y por eso **no
  existe** el "gastos por objeto" del III trim. 2025. Se conservan los dos porque
  cada uno tiene su URL de origen en el inventario.
- **`stock_de_deuda_-_i_trim_2024_msi.pdf` está mal archivado.** Al parsearlo
  (tarea 2) resultó que no es un stock de deuda sino un *estado de ejecución del
  presupuesto de gastos por fuente de financiamiento* del I trim. 2024. El nombre
  del archivo engaña. Se deja donde está para no romper la trazabilidad, pero no
  es comparable con los otros diez PDF de `deuda_publica/`.
- **`sef_-_i_trim_2024_msi.pdf` y `sef_msi_-_2024.pdf` NO son duplicados**
  (md5 distinto): uno es el I trimestre y el otro el anual.
- **Los PDF no fueron abiertos.** Todo lo de arriba sale de nombres de archivo,
  tamaños, md5 y de los dos archivos de control. El contenido se valida en la
  siguiente tarea.

## Verificación

```
python3 03_scripts/verificar_inventario.py
```

Compara `01_raw/` contra `INVENTARIO.txt` y reporta presentes, faltantes,
sobrantes y diferencias de tamaño. Sale con código 0 si está todo bien.
