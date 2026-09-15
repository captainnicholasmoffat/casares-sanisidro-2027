# Boletín Oficial de San Isidro — procesamiento masivo

Fecha del trabajo: 14 de septiembre de 2026. Todo sale del Boletín Oficial del Municipio, sin fuentes externas.

---

## 1. Lo que se bajó

- **TESI (buscador online), feb 2024 – sep 2026**: 15.464 actos individuales, las 516 páginas del listado, con tipo, número, objeto, fecha de firma, fecha de publicación, tags y link al PDF.
- **PDF de esos actos**: 4.466 descargados y convertidos a texto en la primera pasada; con las habilitaciones sumadas, 6.201 en total.
- **Archivo histórico, 2002 – marzo 2024**: 1.741 boletines en PDF de 1.748 listados, convertidos a texto, y segmentados en 37.132 actos que contienen alguno de los términos buscados.
- No hubo rate limit, bloqueo ni captcha en ninguna de las dos fuentes. No hizo falta el worker de Chrome.

**El 403 del iframe.** No era un bloqueo del Municipio. Los dominios `boletines.sanisidro.gob.ar` y `www.sanisidro.gob.ar` publican su certificado sin la cadena intermedia de Sectigo, así que cualquier cliente que verifique bien los rechaza. `tesi.sanisidro.gob.ar` sí la publica. Completé la cadena con el intermedio que sirve tesi y los tres bajan normalmente, con verificación activa. Es un defecto de configuración del Municipio, no una restricción de acceso.

---

## 2. El hallazgo principal

**573 decretos de adjudicación revisados en la gestión Lanús. Cero publican el domicilio del adjudicatario.**

- 573 actos de adjudicación entre febrero de 2024 y julio de 2026.
- 0 con domicilio del adjudicatario. 100% sin el dato.
- 350 CUIT distintos identificados: 309 personas jurídicas y 41 personas físicas.
- 572 de los 573 decretos sí traen el CUIT, así que la empresa queda identificada aunque el domicilio falte.
- **Monto total adjudicado en el período: $167.005.967.431** en pesos corrientes, sin ajustar por inflación. De ese total, $150.508.755.256 salen de decretos donde el monto está explícito o es la suma de los renglones adjudicados; los $16.497.212.175 restantes corresponden a 29 decretos donde tomé la cifra mayor del texto y son menos firmes. 21 decretos no declaran monto.

### La salvedad sobre las habilitaciones

Ninguno de los 350 CUIT aparece en el registro de habilitaciones de San Isidro del mismo período. **Eso no prueba que ninguno sea local.** Una constructora, un proveedor de insumos o una empresa de servicios puede tener domicilio en el partido sin necesitar habilitación comercial, que es para locales al público. El dato es sugerente y hay que presentarlo así, no como conclusión.

### El cruce San Isidro / afuera para el período actual

No se puede hacer con el Boletín. El Municipio no produce el dato. Llegar al número exige el padrón de ARCA, que hoy pide clave fiscal o certificado. Queda **SIN DATO** y así figura en el CSV.

---

## 3. El dato que sí se pudo calcular: el Municipio antes publicaba el domicilio

Al procesar el archivo histórico apareció algo que no buscábamos. Hasta 2017 los decretos de adjudicación decían dónde tenía domicilio el que cobraba, con la fórmula «Adjudícase a X, con domicilio en Y». Después dejaron de decirlo.

| Años | Adjudicaciones | Con domicilio publicado |
|---|---|---|
| 2002–2010 | 2.409 | 41% a 53% según el año |
| 2011–2017 | 3.514 | 62% a 82% según el año |
| 2018 | 361 | 8,0% |
| 2019–2022 | 1.259 | entre 0,7% y 5,4% |
| 2023–2026 | 1.026 | 0% |

**El corte es 2018, no 2023.** La práctica se abandonó bajo la gestión anterior. La gestión actual no la retomó. Conviene decirlo así: el documento queda a prueba de la réplica obvia.

Con los 3.670 decretos históricos que sí traen domicilio se puede calcular el número que nadie publicó, para esa época:

- **50,5% de los adjudicatarios tenía domicilio en el partido de San Isidro** (1.663 de 3.293 clasificados).
- **49,5% tenía domicilio fuera** (1.630).
- Los de afuera se concentran en CABA, San Fernando, Tigre, Vicente López y Olivos.
- 377 casos no se pudieron clasificar por cómo quedó el texto en el PDF.

La proporción local bajaba con los años: 72% en 2004, 53% en 2013, 39% en 2017.

---

## 4. Tasas, aumentos y la denuncia de cobro retroactivo

Busqué los decretos de actualización general de tasas y leí el artículo de vigencia de cada uno en el PDF original.

| Decreto | Firmado | Publicado | Vigencia declarada |
|---|---|---|---|
| DECRE-2024-160 | 22/02/2024 | 26/02/2024 | devengados desde el 1° de marzo de 2024 |
| DECRE-2024-473 | 25/04/2024 | 30/04/2024 | devengados desde el 1° de mayo de 2024 |
| DECRE-2024-706 | 19/06/2024 | 28/06/2024 | devengados desde el 1° de julio de 2024 |

**En los tres casos el decreto se firmó y se publicó antes de la fecha desde la que rige.** Sobre el texto del Boletín, el aumento del 1° de mayo de 2024 no es retroactivo: el DECRE-2024-473 se firmó el 25 de abril y salió publicado el 30, un día antes de entrar en vigencia. El aumento fue del 12% sobre Alumbrado, Limpieza y Servicios Generales y sobre Inspección de Comercios, invocando el artículo 48 de la Ordenanza Impositiva N° 9324.

**Un límite que hay que decir.** La fecha de publicación que uso es la que declara el propio Boletín. No pude verificar cuándo estuvo efectivamente disponible el boletín en el sitio. En el archivo histórico los boletines se imprimían con semanas de demora — el N° 1138, primera quincena de enero de 2024, dice «Publicado, el día 20 de febrero de 2024». Si la denuncia se apoya en que el vecino no pudo conocer el decreto a tiempo, ese es el punto a probar, y no se prueba desde el Boletín. Sería otra pieza de trabajo.

Hay además un DECRE-2024-696 del 18/06/2024 que dispone **una limitación a la actualización** — vale leerlo entero antes de escribir sobre el tema.

---

## 5. Urbanismo

- **«Convenio urbanístico» no aparece ni una sola vez** en los 15.464 actos del período. El instrumento no se usa con ese nombre en San Isidro.
- Lo que sí hay son autorizaciones individuales por decreto: **97 Permisos de Localización** y **84 Factibilidades**, aunque ese conteo mezcla habilitaciones comerciales con decretos de obra; ver la ADENDA para la separación correcta.
- **202 actos** mencionan mayor altura, altura máxima, FOT, FOS o densidad.
- **85 actos** tocan zonificación o el Código de Ordenamiento Urbano.
- Una sola Ordenanza modifica el C.O.U. en todo el período: la **N° 9432**, del 6 de mayo de 2026.
- El patrón a mirar: el plan urbano no se cambia por ordenanza sino caso por caso, por decreto del Ejecutivo.

---

## 6. Control del Concejo

- **Interpelación: 5 menciones** en 15.464 actos del período actual. En el archivo histórico, 118.
- **Pedido de informes: 2 menciones** en el período actual. En el archivo histórico, 22.
- **Rendición de cuentas: 258** en el período actual, 5.413 en el histórico.

Los números son bajos, pero hay que tener cuidado: el Boletín publica lo que el Ejecutivo promulga, no la actividad interna del Concejo. Una interpelación que no termina en ordenanza puede no aparecer nunca. No sirve para medir control parlamentario sin otra fuente.

---

## 7. Qué no se pudo

- **El domicilio actual de los adjudicatarios.** No existe publicado. Requiere padrón de ARCA con clave fiscal.
- **7 boletines históricos** figuran en el índice pero el link está roto del lado del Municipio: Ediciones Extras 251, 561, 782 y 1099, el boletín 834 de 2011, el N° 893 de 2013 y el 1257. De 1.748, faltan 7.
- **40 PDF históricos** son imágenes escaneadas sin texto. Se pueden pasar por OCR si hace falta.
- **La fecha real de publicación** de cada boletín en el sitio, que es lo que haría falta para la denuncia de retroactividad.
- **Una rareza para avisar, no para tocar.** La URL del boletín 834 de 2011 (`/uploads/boletin/Boletines-Oficiales-1a-quincena-834-2011-05-01.pdf`) devuelve código PHP en lugar de un PDF. No lo descargué ni lo ejecuté. Puede ser un archivo mal subido o algo peor; corresponde avisarle al Municipio, no investigarlo desde acá.

---

## 8. Los archivos

| Archivo | Qué trae | Filas |
|---|---|---|
| `01_tesi_completo_2024-2026.csv` | Todo el período actual, acto por acto | 15.464 |
| `02_tesi_con_terminos.csv` | Sólo los que tocan alguno de los términos | 2.712 |
| `03_adjudicaciones.csv` | Adjudicaciones del período actual | 956 |
| `04_tasas_aumentos.csv` | Tasas, aumentos y Ordenanza Impositiva | 1.235 |
| `05_urbanismo.csv` | Localización, factibilidad, altura, zonificación, excepción | 2.117 |
| `06_adjudicatarios_por_cuit.csv` | Un renglón por CUIT, con cuántos decretos ganó | 350 |
| `07_adjudicaciones_montos.csv` | Monto por decreto y con qué método se obtuvo | 573 |
| `08_archivo_historico_2002-2024.csv` | Actos históricos con alguno de los términos | 37.132 |
| `09_domicilios_historicos.csv` | Adjudicaciones históricas con domicilio, clasificadas | 3.670 |

Todos en UTF-8 con BOM, abren en Excel sin romper los acentos. Cada renglón lleva el link al PDF original.

---

## 9. Verificación

- Los tres métodos de cálculo de montos los contrasté a mano contra el PDF original, uno por método, y los tres dan bien.
- La clasificación de domicilios la revisé sobre una muestra al azar de 10 casos: todos correctos.
- Los tres decretos de tasas los leí completos en el PDF, no por índice.
- Lo que queda sin verificar a mano es el resto del volumen, que salió por reglas automáticas sobre el texto de los PDF oficiales.
