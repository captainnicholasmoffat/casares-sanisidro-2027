# Lo que no está disponible, y a qué nivel sí

Censo 2022, partido de San Isidro. Nada de lo que falta se estimó ni se
completó. Acá está qué falta, por qué, y con qué se trabajó en su lugar.

Fecha de consulta: **2026-09-06**.

---

## 1. Población en viviendas colectivas: no hay por radio

El formulario de Redatam del ítem `FREQPOBCOL` (personas en viviendas
colectivas) ofrece desagregación hasta **departamento**. No ofrece fracción ni
radio. El script lo comprueba contra el propio desplegable del formulario antes
de pedir nada, así que esto no es una suposición.

| Qué | Nivel disponible | Valor |
|---|---|---|
| Población en viviendas colectivas | departamento | 1.304 personas |

Va en `data/censo2022_sanisidro_otros_niveles.csv` con su columna
`nivel_geografico`, no en la tabla por radio. **No se repartió entre radios.**

La tabla por radio cuenta, entonces, **población en viviendas particulares**:
295.978 personas. Los 1.304 de viviendas colectivas se suman aparte para llegar
al total del partido.

## 2. Límites de las localidades: no existen publicados

El Censo no los da y ningún organismo los publica como polígono:

- **Redatam, `VIVIENDA.CODLOC`** devuelve una sola categoría para los 360
  radios: "San Isidro". Es la localidad censal compuesta del Gran Buenos Aires.
  No distingue Martínez, Beccar, Boulogne, Acassuso ni Villa Adelina.
- **BAHRA (IGN/INDEC), capa `sublocalidad_entidad_bahra`** sí trae las 6
  entidades del partido, pero como **puntos** (MultiPoint), no como polígonos.
- **API georef del Estado nacional** devuelve las mismas 6 entidades, también
  como puntos con centroide.
- **Sitios del Municipio de San Isidro** (`datos.sanisidro.gob.ar`,
  `gis.sanisidro.gob.ar`) no responden desde este entorno.

Las 6 entidades oficiales, con su código INDEC y su punto:

| Código | Nombre | lat | lon |
|---|---|---|---|
| 0675601001 | Acasusso | -34,478229 | -58,502680 |
| 0675601002 | Béccar | -34,460196 | -58,531361 |
| 0675601003 | Boulogne Sur Mer | -34,509480 | -58,566911 |
| 0675601004 | Martínez | -34,489010 | -58,499380 |
| 0675601005 | San Isidro | -34,469883 | -58,511294 |
| 0675601006 | Villa Adelina | -34,518856 | -58,547356 |

**Consecuencia para el paso 3:** los límites de las zonas los construimos
nosotros. Lo único oficial es la geometría de los 360 radios y estos 6 puntos.
Está explicado en `data/METODOLOGIA_ZONAS.md`.

## 3. Los barrios no existen como dato

Las seis entidades de la sección anterior son las únicas unidades por debajo del
partido que tienen código INDEC. **Los barrios no son localidades censales ni
entidades BAHRA**: no tienen código, ni geometría oficial de ningún organismo.
Aparecen en el habla y en la gestión, no en los datos.

Por eso, en todos los archivos de este repo, los radios se identifican por su
**código de radio** y su **fracción censal**, nunca por nombre de barrio.
Cualquier correspondencia entre un grupo de radios y un barrio conocido es una
hipótesis que hay que verificar contra la geografía real antes de escribirla. No
se afirma ninguna.

## 4. Un defecto de la fuente que sí se corrigió

En la salida de Redatam la letra "ñ" viene doblemente codificada ("aÃ±os" en vez
de "años"), mientras que el resto de los acentos vienen bien. Se repara solo
cuando la vuelta latin-1 → utf-8 da un texto válido. **Ningún número se toca**:
la reparación es sobre las etiquetas de categoría, no sobre los datos.

## 5. Lo que sí se consiguió por radio

Todo lo demás que pedía la tarea está a nivel radio, los 360:

| Pedido | Variable Redatam | Nivel |
|---|---|---|
| Población total | `PERSONA.SEXO` | radio |
| Hogares | `HOGAR.*` (total) | radio |
| Viviendas | `VIVIENDA.TIPOVIV` (total) | radio |
| NBI | `HOGAR.NBI_TOT` | radio |
| Privación material | `HOGAR.IPMH` | radio |
| Hacinamiento | `HOGAR.HACINA` | radio |
| Tipo de vivienda | `VIVIENDA.TIPOVIV` | radio |
| Régimen de tenencia | `HOGAR.REGTEN` | radio |
| Agua de red | `HOGAR.AGUAORIG` + `HOGAR.AGUADIST` | radio |
| Cloacas | `HOGAR.DESAGUE` | radio |
| Gas de red | `HOGAR.COMBUS` | radio |
| Nivel educativo | `PERSONA.MNI` | radio |
| Grupos de edad | `PERSONA.EDADGRU` y `PERSONA.EDADQUI` | radio |

La columna `nivel_geografico` de `censo2022_sanisidro_por_radio.csv` dice
`radio` en las 360 filas. No hay mezcla de niveles en esa tabla.
