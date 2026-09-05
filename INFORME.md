# INFORME — Datos fiscales Municipio de San Isidro, años faltantes (2014, 2015, 2016, 2017, 2022)

Fecha de captura: 5 de septiembre de 2026.
Todos los montos en pesos corrientes de cada ejercicio.

## Resultado en una línea

Los 5 años aparecieron. Ninguno quedó sin datos.

## Qué se encontró, por año

| Año | 1. Totales | 2. Recursos por origen | 3. Gastos por carácter | 4. Gastos por objeto | 5. Resultado |
|---|---|---|---|---|---|
| 2014 | Sí | Sí | Sí | Sí | Derivado (no hay fallo HTC online) |
| 2015 | Sí | Sí | Sí | Sí | Sí |
| 2016 | Sí | Sí (por afectación, no por origen) | Parcial (no hay apertura corriente/capital) | Sí | Sí |
| 2017 | Sí | Sí | Sí | Sí | Sí |
| 2022 | Sí | Sí | Sí | Sí | Sí |

Los números están en `DATOS_SanIsidro_2014-2022.csv`, una fila por dato, con fuente y nivel de confianza.

## De dónde salió cada cosa

**Tribunal de Cuentas de la PBA (fuente más autorizada).** El buscador de fallos tiene el fallo completo en PDF de la rendición de cuentas municipal de 2015, 2016, 2017 y 2022. Los cuatro se bajaron. El de 2022 tiene capa de texto; los de 2015, 2016 y 2017 son escaneos y se les pasó OCR (páginas 1 a 4, que es donde están los Resultandos con los totales).
- 2022: https://sistemas.htc.gba.gov.ar/sistemas/summun/uploads/documents/fallohtc/34836/661e760b4f1ca.SanIsidro2022F.pdf
- 2017: https://sistemas.htc.gba.gov.ar/sistemas/summun/uploads/documents/fallohtc/30165/5cd047f06258a.sanisidro2017F.pdf
- 2016: https://sistemas.htc.gba.gov.ar/sistemas/summun/uploads/documents/fallohtc/29142/5ac4f9e26bcf7.sanisidro2016F.pdf
- 2015: https://sistemas.htc.gba.gov.ar/sistemas/summun/uploads/documents/fallohtc/28133/5936aecfcac5f.sanisidro2015F.pdf
- Buscador: https://sistemas.htc.gba.gov.ar/sistemas/summun/busqueda/fallohtc/0/buscador (campo "Entes" = San Isidro)

**SIMCo (Sistema de Información Municipal Consolidada).** La serie fiscal municipal llega hasta 2014 y arranca en 2007. Cubre justo el año que faltaba en el Tribunal de Cuentas. Se extrajeron 22 variables para San Isidro 2014, y la serie 2007-2014 completa está disponible ahí con botón XLS.
- https://www.simco.rafam.ec.gba.gov.ar/inicio/variables
- La consulta de variables es pública, no hace falta cuenta. El registro que ofrece el sitio no se usó.

**Portal de San Isidro — "Ejercicios anteriores".** Las presentaciones de rendición de cuentas de 2014, 2015, 2017 y 2022 tienen todas las tablas pegadas como imagen, sin capa de texto, tal como estaba dicho. Se les pasó OCR y de ahí salieron las aperturas que ningún otro lado tiene: recursos por origen, recursos por rubro, gastos por objeto, gastos por jurisdicción y gastos por carácter económico.
- 2022: https://www.sanisidro.gob.ar/sites/default/files/img/msi_rendicion_2022_1.pdf
- 2017: https://www.sanisidro.gob.ar/sites/default/files/img/_rendicion2017.pdf.pdf
- 2015: https://www.sanisidro.gob.ar/sites/default/files/img/msi-rendicion-2015.pdf
- 2014: https://www.sanisidro.gob.ar/sites/default/files/img/msi-rendicion-a-o-2014.pdf
- Índice: https://www.sanisidro.gob.ar/ejercicios-anteriores

## Tres hallazgos que conviene mirar

**1. El 2016 no tiene rendición publicada en el portal municipal.** Solo está el presupuesto. Pero la presentación de rendición 2017 trae, por error, la lámina "Gastos por Objeto" del ejercicio 2016 (total $3.832.062.816,94, que es exactamente el gasto ejecutado 2016 según el fallo del Tribunal de Cuentas). O sea: el desglose por objeto de 2016 existe, está dentro del PDF de 2017, en la página 19. El gráfico de la página siguiente sí muestra 2017.

**2. El fallo del ejercicio 2014 no está en la base del Tribunal de Cuentas.** Buscando por ente y por expediente 3-109.0-2014 solo aparece una resolución de tipo "Procedencia" del 18/08/2016, con la ficha vacía y sin PDF adjunto. El fallo de fondo de 2014 no está publicado online. El dato de 2014 se cubrió con SIMCo y con la rendición municipal, y ambas fuentes coinciden número por número.

**3. Hay diferencias entre el municipio y el Tribunal de Cuentas en dos años.**
- 2015: el municipio informa gastos por $2.802.807.307,81 y el Tribunal $2.802.816.043,81. Diferencia: $8.736,00.
- 2022: el municipio informa recursos por origen por $34.130.379.003,31 y el Tribunal recaudación en rubros de cálculo por $33.942.866.674,59. Diferencia: $187.512.328,72. Probablemente sean criterios distintos de clasificación, pero no lo verifiqué.

## Control de calidad hecho

Todas las tablas de gastos por objeto suman exactamente su total, y esos totales coinciden con los del fallo del Tribunal de Cuentas del mismo año (2015, 2016, 2017 y 2022). Para 2014, los cinco valores clave de SIMCo y de la rendición municipal coinciden hasta el peso. Eso quiere decir que el OCR de los números está bien, no solo que se leyó algo.

Además, en los cuatro fallos del Tribunal se cumple la identidad resultado financiero = aplicaciones financieras - fuentes financieras, al peso, en 2015, 2016, 2017 y 2022. Eso valida cruzado los cuatro resultados.

No quedó ningún dato con confianza baja. El único que revisé a ojo sobre el PDF, por dudas de OCR, fue el resultado financiero 2016 ($183.542.494,82): está correcto.

## Dónde ya no hace falta volver a mirar

**ASAP (asap.org.ar).** Los informes de transparencia fiscal municipal son rankings de cumplimiento: miden si el municipio publica la información, no publican los montos. Además arrancan en 2019. No sirve para ninguno de los 5 años.
https://asap.org.ar/informes-detalle/cumplimiento-municipios/8

**Ministerio de Economía PBA — Situación Económica Financiera.** Las publicaciones por municipio llegan hasta 2013 (libros 2008-2009, 2010-2011, y "Evolución económico financiera 2007-2013"). Nada de 2014 en adelante.
https://www.gba.gob.ar/hacienda_y_finanzas/direccion_provincial_de_coordinacion_municipal_y_programas_de_desarrollo/situacion_economica_financiera

**Ministerio de Economía PBA — "Evolución de las Finanzas Municipales 2015-2024".** Es un informe agregado de los 135 municipios, 56 páginas, no trae tablas por municipio. Desde el contenedor no se pudo descargar (el proxy bloquea ec.gba.gov.ar), sí se abrió en el navegador. Si en algún momento querés el agregado provincial, está acá: https://www.ec.gba.gov.ar/areas/Sub_Politica_Coord_Eco/CoordMunicipal/informe/INFORME%20FISCAL%20DE%20LOS%20MUNICIPIOS%20BONAERENSES%202015-2024.pdf

**Portal de San Isidro — Ejecución presupuestaria trimestral.** Solo 2024, 2025 y 2026. Nada anterior.
https://www.sanisidro.gob.ar/ejecucion-presupuestaria

**Concejo Deliberante de San Isidro.** El sitio publica sesiones desde 2018; no hay nada de 2014-2017. Y las ordenanzas de aprobación de rendición no traen cifras: aprueban y punto. Como referencia, el fallo del Tribunal dice que la rendición 2022 se aprobó por Ordenanza N° 9283 del 18/05/2023, la de 2016 por Resolución 02/2017 del 18/05/2017 y la de 2015 por Resolución 04/2016 del 19/05/2016.
https://hcd.sanisidro.gob.ar/index.php/el-concejo-2/normativas/

**Boletín Oficial municipal (boletines.sanisidro.gob.ar).** Las ediciones extra publican ordenanzas fiscales, impositivas y de presupuesto, no ejecución. No aporta.

**SIMCo para 2015 en adelante.** La serie fiscal termina en 2014. No hay que volver a intentarlo para 2015-2022.

## Qué falta todavía

- **Gastos por carácter económico de 2016** (apertura corrientes / capital / aplicaciones financieras). El fallo del Tribunal da ahorro corriente, resultado financiero, fuentes y aplicaciones financieras, pero no la apertura de gastos. La única vía sería el expediente 3-109.0-2016 completo, o pedirlo al municipio.
- **Recursos por origen de 2016 en el criterio del municipio** (municipal / provincial / nacional). Lo que hay es la apertura del Tribunal por afectación, que no es lo mismo.
- **El fallo del Tribunal de Cuentas del ejercicio 2014.** No está online. Se puede pedir por mesa de entradas: mesadeentradas@htc.gba.gov.ar, citando expediente 3-109.0-2014.

## Contenido de la entrega

- `DATOS_SanIsidro_2014-2022.csv` — todos los números, una fila por dato, con fuente y confianza.
- `archivos/` — los PDFs originales con sus nombres de origen (4 fallos del Tribunal + 5 documentos del portal municipal) y el CSV de SIMCo 2014.
- `texto_ocr/` — el texto extraído de cada PDF, para que puedas verificar cualquier número contra la fuente sin volver a hacer OCR.
