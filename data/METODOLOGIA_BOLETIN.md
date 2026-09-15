# Boletín Oficial de San Isidro — listado TESI

Qué hay acá, de dónde salió y qué se puede y qué no se puede afirmar con esto.

## Fuente

`https://tesi.sanisidro.gob.ar/boletin?page=N` — el buscador oficial del
Boletín Oficial Municipal. 516 páginas, 30 actos por página.
Bajado el 15/09/2026 con `03_scripts/bajar_tesi.py`.

**Total: 15.464 actos.** 515 páginas de 30 + 14 en la última.
El conteo cierra exacto y fue reproducido de forma independiente por otra
descarga del mismo padrón.

TESI **no** es el archivo histórico. Cubre firmas desde el **04/01/2024** y
publicaciones desde el **20/02/2024**, hasta el 01/09/2026 y 08/09/2026
respectivamente. El archivo 2002 – 21/03/2024 vive en
`boletines.sanisidro.gob.ar`, que **no es alcanzable** desde este entorno:
el gateway de egreso no llega al servidor, por https, por http y sin proxy.
Ese tramo histórico no está en este repo.

## Archivos

| Archivo | Filas | Qué es |
|---|---|---|
| `01_raw/boletin_oficial/tesi_listado.jsonl.gz` | 15.464 | captura cruda, un acto por línea |
| `02_clean/boletin/tesi_listado.csv` | 15.464 | lo mismo en CSV |
| `02_clean/boletin/tesi_adjudicaciones.csv` | 573 | adjudicaciones |
| `02_clean/boletin/tesi_concejo.csv` | 163 | decretos sobre ordenanzas del Concejo |
| `02_clean/boletin/tesi_residuos.csv` | 699 | higiene urbana, recolección y barrido |

Columnas: `boletin`, `fecha_publicacion`, `fecha_firma`, `tipo`, `numero`,
`objeto`, `tags`, `pdf`. El corte del Concejo agrega `accion`.

`numero` es el identificador GDE (`DECRE-2026-814-SI-INTEN`).
`objeto` trae el número de expediente adentro, sin parsear.
`tags` son las etiquetas del **propio sistema municipal**, no nuestras:
1.878 etiquetas distintas.

## Qué sí se puede afirmar

**Las 573 adjudicaciones son todas de la gestión actual.** Filtrando
`fecha_firma >= 2023-12-10` (asunción) quedan las 573: ninguna es anterior.
Los dos números son el mismo, así que se puede escribir "573 decretos de
adjudicación, todos de la gestión actual" sin nota al pie. La coincidencia
es porque TESI arranca después del cambio de gestión, no porque hayamos
filtrado por gestión.

**Cuatro vetos y dos observaciones**, todos verificados contra la fuente:

| Firma | Decreto | Acción | Ordenanza | Expediente |
|---|---|---|---|---|
| 11/06/2025 | DECRE-2025-614 | veto | 9395 — Paisaje Protegido Municipal | 216-HCD-2025 |
| 11/06/2025 | DECRE-2025-615 | veto | 9396 | 110 y 220-HCD-2025 |
| 11/06/2025 | DECRE-2025-616 | observa artículos y promulga | 9397 | 235-HCD-2025 |
| 07/07/2025 | DECRE-2025-722 | veto | 9399 | 288-HCD-2025 |
| 26/08/2025 | DECRE-2025-999 | veto | 9405 | 445-HCD-2025 |
| 12/01/2026 | DECRE-2026-37 | promulga y suprime una frase | 9418 | EX-2025-283656 |

Los cuatro vetos lisos caen entre junio y agosto de 2025.
Ojo con el tag: 614, 615 y 722 están etiquetados `Veto` y el 999 `Vetar`.
Filtrar por un solo string pierde uno.

**Residuos: el expediente de 2008 sigue vivo.** El listado muestra tres
expedientes corriendo en paralelo para la misma UTE
(Benito Roggio e Hijos S.A. – CLIBA Ingeniería Ambiental S.A.):

- **5229/2008** — alcances 50, 51, 54, 55, 56, 57, 60, 61, 62, 64, 66 y 68
  reconocidos entre 2024 y 2025.
- **12653/2014** — alcances 33, 34, 37, 42 y 44.
- **9835/2023** — alcances 6 a 12.

`DECRE-2025-86-SI-INTEN` (24/01/2025) cita las dos licitaciones juntas:
"Licitaciones Públicas Nros. 17/2008 y 17/2014".
En los 15.464 actos **no hay ningún llamado ni adjudicación nueva del
servicio troncal de recolección**: todo lo que aparece son reconocimientos
de mayores costos y redeterminaciones de precios.

## Qué NO se puede afirmar con este archivo

1. **Pedidos de informes del Concejo: no están, y no por error.** El Boletín
   publica lo que el Ejecutivo promulga, no la actividad interna del Concejo.
   El propio `DECRE-2025-722` explica por qué: el pedido de informes se
   vehiculiza por Comunicación, y las Comunicaciones no se promulgan.
   El número de pedidos pedidos vs. respondidos **no sale de esta fuente**:
   hace falta el Digesto o las actas del HCD.

2. **Localidad de la obra adjudicada: no es un campo.** Hay que sacarla del
   texto del pliego que cita cada decreto. No está resuelto acá.

3. **Domicilio del adjudicatario: no se publica.** Cero de los 573.

4. **Montos: no están en el listado.** El `objeto` a veces los trae, casi
   siempre no. Para montos hay que ir al PDF.

5. **El texto completo no está acá.** Este repo tiene el listado, no los
   PDF. Sólo 2.518 de los 15.464 actos exponen link directo al PDF en el
   listado; el resto cuelga del PDF del boletín completo.
   Los conteos por término hechos sobre `objeto` son un **piso**, no el
   total: buscar sobre el texto completo da más.

6. **DECRE-2026-217** promulga la Ordenanza 9419 y el listado no dice que
   sea con observaciones. Si se afirma eso, hay que respaldarlo con el PDF.

## Un dato suelto que conviene mirar

`DECRE-2025-721` (07/07/2025) anula el Decreto 719/2025, del mismo día y del
mismo expediente que el veto a la Ordenanza 9399 (288-HCD-2025).
**El Decreto 719/2025 no aparece publicado en el Boletín.**
