# Corpus Boletín Oficial de San Isidro — qué hay y dónde

Armado el 14 de septiembre de 2026. Fuente: Boletín Oficial del Municipio de San Isidro.

## Qué está en esta carpeta de Drive

Los informes y las tablas de análisis. Es la capa que se lee.

| Archivo | Qué contesta |
|---|---|
| `INFORME.md` | Informe principal: qué se bajó, el hallazgo de los 573 decretos sin domicilio, tasas y vigencias, urbanismo, control del Concejo, qué no se pudo |
| `ADENDA.md` | Urbanismo por localidad y montos adjudicados por año y por mes |
| `ADENDA_2.md` | Concentración con atribución exacta y las tres zonas de la obra vial delimitadas calle por calle |
| `06_adjudicatarios_por_cuit.csv` | Los 350 adjudicatarios únicos con su CUIT y cuántos decretos ganó cada uno |
| `10_urbanismo_por_localidad.csv` | Los 95 decretos urbanos con localidad, dirección y catastro |
| `11_montos_por_mes.csv` | Monto adjudicado mes a mes, febrero 2024 a julio 2026 |
| `12_ranking_adjudicatarios_por_monto.csv` | Ranking completo de 332 adjudicatarios, método mixto |
| `13_ranking_estricto_407_decretos.csv` | Ranking de 236 adjudicatarios, sólo con atribución exacta. **Es el que hay que citar.** |

## Qué NO está acá y dónde conseguirlo

El corpus crudo: 6.201 textos completos de actos de TESI, 1.735 boletines
históricos en texto, los JSON estructurados y los CSV grandes (el completo de
15.464 actos y el histórico de 37.132). Son 70 MB comprimidos.

Cap'n Nick los tiene en tres archivos de 24 MB
(`corpus_sanisidro.tar.gz.part00`, `part01`, `part02`). Pedíselos y los sube acá.
El MD5 del archivo rearmado es `8253670726a96fe2c99147d08d6a56e1`.

Para unirlos, en Mac o Linux:

    cat corpus_sanisidro.tar.gz.part00 corpus_sanisidro.tar.gz.part01 corpus_sanisidro.tar.gz.part02 > corpus_sanisidro.tar.gz
    tar xzf corpus_sanisidro.tar.gz

En Windows, PowerShell:

    cmd /c copy /b corpus_sanisidro.tar.gz.part00+corpus_sanisidro.tar.gz.part01+corpus_sanisidro.tar.gz.part02 corpus_sanisidro.tar.gz
    tar -xzf corpus_sanisidro.tar.gz

Los PDF originales (5,6 GB, 6.201 de TESI y 1.741 históricos) se dejaron afuera
a propósito: **cada renglón de cada CSV trae la URL de su PDF fuente**, así que
se rebajan cuando hagan falta.

## Aviso técnico para quien vuelva a bajar del Municipio

Los dominios `boletines.sanisidro.gob.ar` y `www.sanisidro.gob.ar` sirven su
certificado sin la cadena intermedia de Sectigo. Cualquier cliente que verifique
bien da error y parece un 403. No es un bloqueo. Se resuelve completando la
cadena con el certificado intermedio que sí publica `tesi.sanisidro.gob.ar`.

## Fuentes exactas

- Listado estructurado 2024–2026: `https://tesi.sanisidro.gob.ar/boletin?page=N` (516 páginas, 30 por página)
- Archivo histórico 2002–2024: `https://boletines.sanisidro.gob.ar/index.php/boletin` (1.750 ids)

## Cortes de fecha, para no equivocarse

- TESI: firmas del 04/01/2024 al 01/09/2026; publicaciones del 20/02/2024 al 08/09/2026.
- Archivo histórico: hasta el boletín extra 1278, del 21/03/2024.
- El corte entre las dos fuentes es de fuente, no político. Para un corte por
  gestión hay que filtrar `fecha_firma >= 2023-12-10` y decirlo.
- En el histórico hay outliers de parseo en `fecha_firma` (se vieron 1971 y 2915).
  Filtrar por rango antes de usar esa columna.
