# PDF no incorporados a los CSV

Generado por `03_scripts/parse_ejecucion.py`.

## No se pudieron parsear

Ningun dato de estos archivos entro a los CSV.

| Archivo | Motivo |
|---|---|
| `stock_de_deuda_-_i_trim_2024_msi.pdf` | ErrorDeParseo: no es un formulario de stock de deuda (Ley 12.462) sino ESTADO DE EJECUCION DEL PRESUPUESTO DE GASTOS; esta mal archivado en deuda_publica/ |

## Omitidos por ser copia exacta de otro

Mismo md5 que el archivo original, asi que se procesa una sola vez. Los datos estan en los CSV bajo el nombre del original.

| Archivo omitido | Copia de | md5 |
|---|---|---|
| `2025_iii_gastos_por_fyf_0.pdf` | `2025_iii_gastos_por_fyf.pdf` | `ef7e74aaed2dcc4f18d017c416a220e7` |
