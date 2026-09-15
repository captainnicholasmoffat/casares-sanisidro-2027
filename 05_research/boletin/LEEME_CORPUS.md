# Corpus Boletín Oficial de San Isidro — paquete completo

Armado el 14 de septiembre de 2026. Fuente: Boletín Oficial del Municipio de San Isidro.

## Qué hay adentro

| Carpeta / archivo | Qué es | Tamaño sin comprimir |
|---|---|---|
| `ttxt/` | 6.201 textos completos de actos de TESI (feb 2024 – sep 2026) | 61 MB |
| `txt/` | 1.735 boletines históricos completos en texto (2002 – mar 2024) | 266 MB |
| `tesi_rows.json` | 15.464 actos de TESI, metadatos crudos del buscador | 8,8 MB |
| `tesi_full.json` | Los mismos 15.464 enriquecidos con el texto de los PDF | 9,3 MB |
| `archivo_rows.jsonl` | 37.132 actos históricos segmentados | 29 MB |
| `adj_rows.json` / `adj_montos.json` | Los 573 decretos de adjudicación y sus montos | 0,5 MB |
| `meta.json` | Índice de los 1.750 boletines históricos con fecha y URL | 0,35 MB |
| `tpdf_index.json` | Índice de los PDF de TESI descargados | 1,3 MB |
| `cuit_dom_map.json` | CUIT con dirección hallada en actos municipales | 0,06 MB |
| `01` a `13` .csv | Las 13 tablas de salida | 31 MB |
| `INFORME.md`, `ADENDA.md`, `ADENDA_2.md` | Los tres informes | |
| `*.py` | Los scripts que generaron todo, para reproducirlo | |

## Qué NO hay

Los PDF originales: 6.201 de TESI y 1.741 históricos, 5,6 GB en total.
Se dejaron afuera a propósito. **Cada renglón de cada CSV trae la URL del PDF fuente**,
así que se rebajan cuando hagan falta.

## Cómo rearmar el paquete

Los tres trozos se unen así.

En Mac o Linux, en la carpeta donde estén los tres archivos:

    cat corpus_sanisidro.tar.gz.part00 corpus_sanisidro.tar.gz.part01 corpus_sanisidro.tar.gz.part02 > corpus_sanisidro.tar.gz
    tar xzf corpus_sanisidro.tar.gz

En Windows, en PowerShell:

    cmd /c copy /b corpus_sanisidro.tar.gz.part00+corpus_sanisidro.tar.gz.part01+corpus_sanisidro.tar.gz.part02 corpus_sanisidro.tar.gz
    tar -xzf corpus_sanisidro.tar.gz

Para verificar que se unió bien, el MD5 del archivo rearmado tiene que dar:

    8253670726a96fe2c99147d08d6a56e1

## Aviso técnico para quien vuelva a bajar del Municipio

Los dominios `boletines.sanisidro.gob.ar` y `www.sanisidro.gob.ar` sirven su certificado
sin la cadena intermedia de Sectigo. Cualquier cliente que verifique bien da error y
parece un 403. No es un bloqueo. Se resuelve completando la cadena con el certificado
intermedio que sí publica `tesi.sanisidro.gob.ar`.

## Fuentes exactas

- Listado estructurado 2024–2026: `https://tesi.sanisidro.gob.ar/boletin?page=N` (516 páginas)
- Archivo histórico 2002–2024: `https://boletines.sanisidro.gob.ar/index.php/boletin`
