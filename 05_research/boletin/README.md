# Boletín Oficial de San Isidro — el corpus, ya en el repo

El corpus completo dejó de vivir en un contenedor efímero. Está acá.

Lo produjo otra sesión que bajó y procesó las dos fuentes del Boletín. Se
trajo el 15/09/2026 desde un artifact publicado, byte por byte. Lo único
que quedó afuera son los PDF originales (5,6 GB) y los textos completos
(327 MB): cada renglón de cada CSV trae la URL de su PDF fuente.

## Dónde está cada cosa

**`01_raw/boletin_oficial/`** — las capturas crudas, comprimidas.

| Archivo | Qué es |
|---|---|
| `archivo_rows.jsonl.gz` | **37.132 actos históricos, 2002 – mar 2024** |
| `tesi_full.json.gz` | 15.464 actos de TESI con el texto de los PDF |
| `tesi_rows.json.gz` | los mismos, metadatos crudos del buscador |
| `adj_rows.json.gz` | los 573 decretos de adjudicación con CUIT |
| `adj_montos.json.gz` | monto por decreto y método de cálculo |
| `meta.json.gz` | índice de los 1.750 boletines históricos |
| `tesi_listado.jsonl.gz` | mi propia descarga de TESI, para contrastar |

**`02_clean/boletin/`** — las tablas. Los `01` a `13` son del otro chat,
UTF-8 con BOM, abren en Excel sin romper acentos. Los `tesi_*` son míos.

**`05_research/boletin/`** — `INFORME.md`, `ADENDA.md`, `ADENDA_2.md` y
`LEEME_CORPUS.md`.

Falta el `08_archivo_historico_2002-2024.csv` a propósito: pesaba 21 MB y
sale entero de `archivo_rows.jsonl.gz`.

## Verificación

Bajé por mi cuenta las 516 páginas de TESI (`03_scripts/bajar_tesi.py`) y
contrasté todo contra estos archivos. Reconcilia sin una sola diferencia:

**El histórico, reconstruido de tres partes**
- 29.351.413 bytes y **37.132 líneas exactas**, cero JSON roto.
- Publicaciones de **2002 a 2024**, 1.082 boletines distintos, 14 campos.

**La gestión actual**
- **15.464 actos**, el mismo número que mi descarga independiente.
- **573 adjudicaciones**, y **los 30 meses coinciden uno por uno**.
- **$167.005.967.431** adjudicados; los porcentajes mensuales suman 100,00.
- **$116.343.600.736** en el universo estricto, exacto al peso.
- Top 5 / 10 / 25 = **35,5% / 54,5% / 78,6%**, recalculados desde el CSV.

**Los domicilios históricos**
- 3.670 filas. Clasificados 3.293, sin clasificar 377.
- **1.663 dentro del partido y 1.630 fuera: 50,5% / 49,5% exacto.**

**Las nueve tablas restantes** dan la fila exacta que declara el informe:
15.464, 2.712, 956, 1.235, 2.117, 350, 573, 95 y 332.

## Tres cosas para citar con cuidado

1. **Son cuatro vetos y dos observaciones, no ocho.** De los ocho actos que
   lista `ADENDA_2.md`, el `DECRE-2025-721` es una anulación de decreto y
   el `DECRE-2026-217` figura en el listado sólo como "Promulgación de la
   Ordenanza N° 9419", sin mención de observaciones. Para afirmar que fue
   con observaciones hay que citar el PDF.
2. **Pedidos de informes: `INFORME.md` dice 2 menciones y `ADENDA_2.md`
   dice 3.** Vale la segunda, que es posterior y trae las tres citas
   textuales. La conclusión no cambia: ninguna es un pedido del Concejo.
3. **La columna `decretos` del ranking estricto suma 486, no 407.** No es
   un error: 407 son decretos y un decreto puede nombrar varias empresas.
   El `DECRE-2024-1258` adjudica tres zonas a tres adjudicatarios.

## Dos versiones de los informes, y cuál quedó

El artifact y la copia de Drive no eran iguales. Quedaron las de Drive para
los tres informes, que son posteriores:

- `INFORME.md` de Drive trae tres autocorrecciones que la del artifact no
  tiene, entre ellas que el conteo de 97 Permisos y 84 Factibilidades
  mezclaba habilitaciones comerciales con decretos de obra.
- `ADENDA_2.md` de Drive trae dos secciones enteras que faltan en la del
  artifact: los vetos y el contrato de residuos.
- `LEEME_CORPUS.md` quedó la del artifact, que documenta el corpus en vez
  de la carpeta de Drive.
- Los CSV quedaron los del artifact: son idénticos en contenido y
  conservan el BOM.

## Un hallazgo del listado que no está en los informes

`DECRE-2025-721` anula el Decreto 719/2025, del mismo día y del mismo
expediente que el veto a la Ordenanza 9399 (288-HCD-2025).
**El Decreto 719/2025 no aparece publicado en el Boletín.**

Y un tercer expediente de Roggio/CLIBA que los informes no mencionan:
**9835/2023**, alcances 6 a 12, corriendo en paralelo al 5229/2008 y al
12653/2014.
