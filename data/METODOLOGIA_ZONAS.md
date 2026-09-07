# Metodología de las zonas vecinales

Cómo se agruparon los 360 radios censales del partido de San Isidro en 6 zonas,
y cómo volver a llegar exactamente al mismo mapa.

```
python3 03_scripts/censo_radios.py   # geometría y datos por radio
python3 03_scripts/zonas.py          # las zonas
python3 03_scripts/test_censo_zonas.py
```

---

## 0. Los límites son nuestros, no oficiales

**Esto primero, porque condiciona todo lo demás.**

Lo único oficial en este mapa es:

| Qué | Organismo | Qué es |
|---|---|---|
| La geometría de los 360 radios censales | INDEC, Censo 2022 (vía catálogo de datos de la Provincia) | polígonos |
| Los 6 puntos de las localidades del partido | IGN e INDEC, base BAHRA, capa `sublocalidad_entidad_bahra` | **puntos**, no polígonos |

**El límite de cada zona lo construimos nosotros.** No existe publicado ningún
polígono de las localidades de San Isidro: el Censo devuelve una sola localidad
censal para los 360 radios, y BAHRA y el servicio georef del Estado nacional dan
las 6 entidades como puntos. Los sitios del Municipio no responden. Está
documentado en `data/NO_DISPONIBLE.md`.

Esto no es una debilidad frente al anexo de zonas de la Ordenanza 6045/1984: ese
anexo tampoco está publicado. La diferencia es que acá la regla está escrita y
cualquiera puede correrla y llegar al mismo mapa.

**Cuando se publique el mapa hay que decir esto.** No se esconde: los límites son
una construcción propia sobre geografía oficial.

---

## 1. Las semillas: las 6 localidades del partido

Una semilla por localidad oficial, en el punto que publica BAHRA. Cada punto cae
dentro de un único radio censal, y los seis radios son distintos:

| Código INDEC | Localidad | lat, lon | Radio semilla |
|---|---|---|---|
| 0675601005 | San Isidro | -34,469883 / -58,511294 | `067560302` |
| 0675601002 | Béccar | -34,460196 / -58,531361 | `067562807` |
| 0675601004 | Martínez | -34,489010 / -58,499380 | `067560610` |
| 0675601001 | Acassuso | -34,478229 / -58,502680 | `067560406` |
| 0675601003 | Boulogne Sur Mer | -34,509480 / -58,566911 | `067562606` |
| 0675601006 | Villa Adelina | -34,518856 / -58,547356 | `067562407` |

Los seis puntos están en el script (`SEMILLAS`), y la descarga cruda de la capa
en `01_raw/censo2022/`.

---

## 2. Criterio de vecindad

**Dos radios son vecinos si comparten al menos 1 metro de borde.**

- La medición es sobre la geometría proyectada a metros (UTM 21S, EPSG:32721).
- Se calcula la intersección de los dos polígonos y su longitud.
- **Un contacto de punta no cuenta.** Dos radios que se tocan sólo en un vértice
  no son vecinos: el umbral de 1 metro los filtra.

Con esta definición, los 360 radios del partido forman **una sola pieza conexa**.
No hay radios aislados. El grado de vecindad va de 1 a 13, con media 5,2.

---

## 3. Orden de asignación

Las seis zonas crecen **a la vez**, radio por radio, desde su semilla.

En cada paso:

1. Se miran las zonas que todavía tienen algún radio libre pegado a su frontera.
2. **Avanza la que menos población acumulada tiene.**
3. Esa zona se queda con el radio libre de su frontera **cuyo centroide está más
   cerca del centroide de su propia semilla**, medido en metros.
4. Se repite hasta que no queda ningún radio libre.

Por qué así:

- **Crecer siempre la zona más chica** es lo que empareja los tamaños sin que
  nadie elija nada. El equilibrio de población sale del procedimiento, no de un
  ajuste posterior.
- **Tomar sólo radios de la frontera** es lo que garantiza la contigüidad: una
  zona crecida por adyacencia desde una semilla no puede quedar en dos pedazos.

---

## 4. Cómo se resuelven los empates

Los empates se resuelven en este orden, y siempre dan el mismo resultado:

1. **Entre zonas empatadas en población acumulada**, avanza la de nombre
   alfabético menor.
2. **Entre radios de la frontera a igual distancia** de la semilla —comparada
   redondeando al milímetro— entra el de `radio_id` menor.

Los `radio_id` son únicos, así que ningún empate queda sin resolver y dos
corridas dan siempre el mismo mapa. **No hay ningún paso manual.**

---

## 5. La excepción: los conglomerados críticos no se parten

> **Los conglomerados contiguos con NBI muy superior a la media del partido no se
> parten entre zonas: se asignan enteros a la zona que los contiene
> geográficamente.**

Es una regla, no un acomodo caso por caso. Se aplica sola, a todos los
conglomerados que cumplen la condición.

### Por qué existe

El crecimiento por población es ciego a la pobreza. Puede cortar al medio un
grupo contiguo de radios pobres y repartirlo entre dos zonas. Si eso pasa, los
dos promedios de zona se diluyen y **nuestro propio mapa termina escondiendo lo
que el programa quiere mostrar**.

### Cómo se define, exactamente

1. **Radio crítico:** está en el decil superior del partido por porcentaje de
   hogares con NBI. Son los 36 peores de 360. El umbral sale de los propios datos
   (**NBI ≥ 8,7%**), no de un número elegido a mano. El NBI del partido entero es
   **3,16%**.
2. **Conglomerado crítico:** 2 o más radios críticos contiguos entre sí, según el
   criterio de vecindad del punto 2.
3. Si un conglomerado quedó repartido entre dos zonas, **va entero a la zona que
   ya tiene la mayor parte de su población**. Esa es la zona que lo contiene
   geográficamente, porque el crecimiento avanza por contigüidad desde la semilla
   más cercana.
4. Empates: gana la zona con menos población total; si siguen empatadas, la de
   nombre alfabético menor.

Después de aplicar la excepción se **vuelven a correr las tres validaciones**,
porque ceder radios puede romper la contigüidad de la zona que los entrega.

### Qué movió, en esta corrida

6 radios, en 3 conglomerados. Está todo en `data/zonas_excepciones.csv`.

| Radio | Fracción | NBI % | Habitantes | De | A |
|---|---|---|---|---|---|
| `067563207` | 32 | 12,7 | 1.135 | San Isidro | **Beccar** |
| `067563208` | 32 | 10,8 | 1.097 | San Isidro | **Beccar** |
| `067563209` | 32 | 12,9 | 1.271 | San Isidro | **Beccar** |
| `067562503` | 25 | 9,6 | 1.243 | Villa Adelina | **Boulogne Sur Mer** |
| `067562504` | 25 | 11,4 | 1.123 | Villa Adelina | **Boulogne Sur Mer** |
| `067563402` | 34 | 10,1 | 919 | Boulogne Sur Mer | **Villa Adelina** |

**El conglomerado de la fracción censal 32** es el que más importa: 9 radios
contiguos, 8.749 habitantes, el peor NBI del partido. Sus nueve radios son
`067563202`, `067563203`, `067563204`, `067563205`, `067563206`,
`067563207`, `067563208`, `067563209` y `067563211`. El peor de todos,
`067563204`, tiene **26,6% de hogares con NBI** —ocho veces la media del
partido— y 52,3% sin cloaca. Los tres que estaban del lado de San Isidro
(`067563207`, `067563208`, `067563209`) tienen entre 64% y 79% de hogares sin
cloaca: son los peores del partido en ese indicador. **Los nueve quedan enteros
en Beccar.**

> Estos radios se identifican por su código y por su fracción censal. No se les
> pone nombre de barrio: la correspondencia con cualquier barrio conocido es
> probable pero no está verificada contra la geografía real, y hasta que se
> verifique no se afirma.

---

## 6. Cuántas zonas

**Seis**, una por localidad oficial.

La regla para pasar de seis sería que alguna quede desproporcionada en población.
No pasa: la zona más grande tiene **1,34 veces** la población de la más chica
(55.157 contra 41.213). El test corta si esa relación pasa de 2,0.

---

## 7. El resultado

Población total de las seis zonas: **295.978** habitantes en viviendas
particulares. Más 1.304 en viviendas colectivas —que el Censo no publica por
radio— dan los **297.282** del partido. Diferencia contra el Censo 2022:
**0,0000%**.

| # | Zona | Radios | Población | Hogares | NBI % | Sin cloaca % | Sin gas de red % | Hacinam. % | Univ. completa % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Boulogne Sur Mer | 58 | 55.157 | 18.567 | **5,77** | 9,94 | 29,33 | 13,83 | 6,39 |
| 2 | Beccar | 57 | 50.522 | 17.632 | **5,68** | 11,29 | 41,46 | 14,69 | 9,94 |
| 3 | Villa Adelina | 62 | 52.954 | 19.067 | 2,75 | 5,99 | 17,20 | 7,33 | 11,37 |
| 4 | San Isidro | 63 | 41.213 | 17.466 | 1,88 | 3,52 | 16,83 | 4,47 | 24,22 |
| 5 | Acassuso | 65 | 54.779 | 20.795 | 1,77 | 3,04 | 18,23 | 3,79 | 26,22 |
| 6 | Martínez | 55 | 41.353 | 17.032 | **1,19** | 1,69 | 14,09 | 2,61 | 24,95 |

Ordenadas de peor a mejor por porcentaje de hogares con NBI, que es el indicador
sintético que publica el propio Censo.

Cada indicador se calcula **sumando los radios de la zona y recién después
dividiendo**. No es el promedio de los porcentajes de los radios: eso le daría el
mismo peso a un radio de 300 habitantes que a uno de 1.500.

---

## 8. Archivos

| Archivo | Qué es |
|---|---|
| `data/radios_censales_sanisidro.geojson` | Los 360 radios con su geometría. |
| `data/censo2022_sanisidro_por_radio.csv` | 105 columnas de datos censales por radio. |
| `data/censo2022_diccionario_columnas.csv` | Qué es cada columna. |
| `data/censo2022_sanisidro_otros_niveles.csv` | Lo que no hay por radio, al nivel que sí existe. |
| `data/zonas_propuestas_sanisidro.geojson` | Las 6 zonas, con sus indicadores. |
| `data/zonas_asignacion_radios.csv` | La zona de cada radio, para rehacer cualquier cuenta. |
| `data/zonas_resumen.csv` | Resumen por zona. |
| `data/zonas_indicadores.csv` | Los indicadores, de peor a mejor. |
| `data/zonas_indicadores_diccionario.csv` | Numerador y denominador de cada indicador. |
| `data/zonas_excepciones.csv` | Los radios movidos por la excepción, con el motivo. |
| `data/NO_DISPONIBLE.md` | Lo que no está y a qué nivel sí. |
| `03_scripts/censo_radios.py` | Baja geometría y datos. |
| `03_scripts/zonas.py` | Arma las zonas. |
| `03_scripts/test_censo_zonas.py` | Las validaciones. |

## 9. Fuentes

| Qué | Fuente | Fecha |
|---|---|---|
| Radios censales 2022 | `catalogo.datos.gba.gob.ar`, dataset *Radios censales* | 2026-09-06 |
| Datos del Censo 2022 | INDEC, Censo Nacional de Población, Hogares y Viviendas 2022, procesado con Redatam 7 (`redatam.indec.gob.ar`) | 2026-09-06 |
| Puntos de las localidades | IGN e INDEC, BAHRA, capa `sublocalidad_entidad_bahra`, departamento 06756 | 2026-09-06 |
| Población del partido (297.282) | INDEC, Censo 2022, resultados definitivos | — |
