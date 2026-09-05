# PDF no incorporados a los CSV

Generado por `03_scripts/test_parser.py`. Cada archivo de esta lista esta fuera de los CSV, con el motivo exacto.

## Ejecucion presupuestaria: no se pudieron parsear

| Archivo | Motivo |
|---|---|
| `stock_de_deuda_-_i_trim_2024_msi.pdf` | ErrorDeParseo: no es un formulario de stock de deuda (Ley 12.462) sino ESTADO DE EJECUCION DEL PRESUPUESTO DE GASTOS; esta mal archivado en deuda_publica/ |

## Ejecucion presupuestaria: omitidos por ser copia exacta de otro

Mismo md5 que el original, asi que se procesa una sola vez. Los datos estan en los CSV bajo el nombre del original.

| Archivo omitido | Copia de | md5 |
|---|---|---|
| `2025_iii_gastos_por_fyf_0.pdf` | `2025_iii_gastos_por_fyf.pdf` | `ef7e74aaed2dcc4f18d017c416a220e7` |

## Presupuestos historicos: no se pudieron parsear

Ninguno.

## Presupuestos historicos: excluidos a proposito

| Archivo | Motivo |
|---|---|
| `ordenanza_del_presupuesto_2026_1.pdf` | Escaneo sin capa de texto (416 paginas). Excluido a proposito: son las ordenanzas completas con los anexos legales y hacer OCR sobre novecientas paginas de tablas financieras mete errores de digitos. Para 2026 ya hay ejecucion trimestral y situacion economico-financiera en texto limpio. |
| `ordenanza_presupuesto_hcd_-_msi_2.pdf` | Escaneo sin capa de texto util (493 paginas). Mismo motivo que el anterior. |
| `ordenanza_prespuesto_2024.pdf` | Tiene capa de texto pero es salida de OCR y ya viene con digitos mal: la fecha de emision sale como '12/1212023' en vez de '12/12/2023', y los encabezados como 'PROGRAMACiONDELOSRECURSOS'. Usar estos numeros meteria errores silenciosos. Para 2024 se usan los otros dos documentos, que estan en texto nativo. |
| `presupuesto_de_gastos_y_calculo_de_recursos_2010.pdf` | Las tablas estan pegadas como imagen: la capa de texto solo trae los titulos de las laminas, cero importes. Sin OCR no hay nada que extraer. |
| `presupuesto_municipal_2014_03.pdf` | Las tablas estan pegadas como imagen: la capa de texto solo trae titulos y comentarios, cero importes. |
| `msi-presupuesto-municipal-2016.pdf` | Las tablas estan pegadas como imagen, cero importes en el texto. Ademas el archivo se llama 2016 y la portada dice 'AÑO 2016', pero todas las laminas de datos dicen 2015: el anio del contenido no esta claro. |
| `_presupuesto2017.pdf.pdf` | Las tablas estan pegadas como imagen: la capa de texto solo trae titulos y comentarios, cero importes. |
| `presupuesto_municipal_2022-presentacion_en_el_honorable_concejo_deliberante-noviembre_2021_1.pdf` | Las tablas estan pegadas como imagen: la capa de texto solo trae los titulos de las laminas, cero importes. |

## Rendiciones de cuentas: no se pudieron parsear

Ninguno.

## Rendiciones de cuentas: excluidas a proposito

| Archivo | Motivo |
|---|---|
| `_rendicion2017.pdf.pdf` | Las tablas estan pegadas como imagen: 23 paginas con 836 caracteres de texto y cero importes. Sin OCR no hay nada que extraer. |
| `msi-rendicion-2015.pdf` | Las tablas estan pegadas como imagen: 26 paginas con 920 caracteres de texto y cero importes. |
| `msi-rendicion-a-o-2014.pdf` | Las tablas estan pegadas como imagen: 38 paginas con 1487 caracteres de texto y cero importes. |
| `msi_rendicion_2022_1.pdf` | Las tablas estan pegadas como imagen: 15 paginas con 183 caracteres de texto y cero importes. |
