# Análisis del Boletín Oficial — informes del corpus

Estos seis archivos los produjo otra sesión que bajó y procesó el corpus
completo del Boletín Oficial de San Isidro. Se copiaron acá desde Google
Drive (unidad compartida "claude" › Proyecto San Isidro › 09_corpus_boletin)
el 15/09/2026, byte por byte, para que dejen de existir en un solo lugar.

| Archivo | Qué es |
|---|---|
| `LEEME_CORPUS.md` | Qué hay en el corpus, cortes de fecha, trampas |
| `INFORME.md` | Informe principal: los 573 sin domicilio, tasas, urbanismo, Concejo |
| `ADENDA.md` | Urbanismo por localidad y montos por año y por mes |
| `ADENDA_2.md` | Concentración con atribución exacta, zonas de la obra vial, vetos, residuos |
| `11_montos_por_mes.csv` | Monto adjudicado mes a mes, feb 2024 – jul 2026 |
| `13_ranking_estricto_407_decretos.csv` | Ranking de 236 adjudicatarios, sólo atribución exacta |

## Verificación independiente

Bajé por mi cuenta las 516 páginas de TESI (`03_scripts/bajar_tesi.py`) y
crucé mi descarga contra estos archivos. Reconcilia:

- **15.464 actos** en total, el mismo número.
- **573 decretos de adjudicación**, el mismo número, y **los 30 meses
  coinciden uno por uno**: ni un mes de diferencia en el conteo.
- **$167.005.967.431** adjudicados, y los porcentajes mensuales suman 100,00.
- **$116.343.600.736** en el universo estricto, exacto al peso.
- Top 5 / 10 / 25 = **35,5% / 54,5% / 78,6%**, recalculados desde el CSV.
- 7.376 resoluciones de firma conjunta y 1.878 tags distintos, ambos iguales.

**Una aclaración de lectura, no un error.** La columna `decretos` del
ranking estricto suma 486, no 407. Es correcto: 407 es el número de
*decretos*, y un decreto puede nombrar a varias empresas, así que sumar
los conteos por empresa cuenta dos veces los decretos compartidos. El
DECRE-2024-1258, por ejemplo, adjudica tres zonas a tres adjudicatarios
distintos.

## Lo que corregí de estos informes

Contrastando contra el listado, dos cosas hay que citar con cuidado:

1. **Son cuatro vetos y dos observaciones, no ocho.** De los ocho actos que
   lista `ADENDA_2.md`, el `DECRE-2025-721` es una anulación de decreto, no
   un veto, y el `DECRE-2026-217` figura en el listado sólo como
   "Promulgación de la Ordenanza N° 9419", sin mención de observaciones.
   Si se afirma que fue con observaciones, hay que citar el PDF.
2. **Pedidos de informes: `INFORME.md` dice 2 menciones y `ADENDA_2.md`
   dice 3.** Vale la segunda, que es posterior y trae las tres citas
   textuales. La conclusión no cambia: ninguna es un pedido de informes
   del Concejo.

## Lo que falta

El corpus crudo — `archivo_rows.jsonl` con los 37.132 actos históricos,
`tesi_full.json`, los 6.201 textos de TESI y los 1.735 boletines
históricos — sigue existiendo en un solo contenedor efímero. Son 70 MB
comprimidos, en tres partes de 24 MB que tiene Cap'n Nick.
MD5 del archivo rearmado: `8253670726a96fe2c99147d08d6a56e1`.
El instructivo para unirlos está en `LEEME_CORPUS.md`.

`boletines.sanisidro.gob.ar`, de donde salen los históricos, no es
alcanzable desde este entorno por ninguna vía.
