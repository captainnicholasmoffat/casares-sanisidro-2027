# Adenda — urbanismo por localidad y montos por año

---

## 1. Dónde cae el urbanismo

Primero una corrección al informe anterior. Los 97 «Permisos de Localización» y 84 «Factibilidades» que conté antes mezclaban dos cosas distintas:

- **Disposiciones de la Dirección General de Permisos y Habilitaciones**: son habilitaciones comerciales de locales. 1.167 en el período. No son excepciones al plan urbano.
- **Decretos del Intendente**: son las autorizaciones de obra, factibilidades y permisos de localización que sí tocan el plan. **95 en el período.**

De esos 95, **73 identifican un inmueble concreto** y 22 son decretos generales sin inmueble (delegación de facultades, reglamentaciones, vetos, presupuesto).

### Los 73 con inmueble, por localidad

| Localidad | Decretos | % |
|---|---:|---:|
| Martínez | 21 | 28,8% |
| San Isidro (ciudad) | 20 | 27,4% |
| Boulogne | 14 | 19,2% |
| Beccar | 9 | 12,3% |
| Acassuso | 6 | 8,2% |
| Villa Adelina | 3 | 4,1% |

**Sí se concentra.** Martínez y San Isidro ciudad juntos son el 56%. Sumando Boulogne, tres localidades explican tres de cada cuatro decretos.

Por año, Martínez lidera 2024 (10) y 2026 (4); San Isidro ciudad lidera 2025 (13). Boulogne crece de 6 a 7 entre 2024 y 2025 y prácticamente desaparece en 2026.

El CSV trae además **circunscripción y sección catastral** de cada uno, más la dirección cuando el decreto la dice. Con eso el cruce con el mapa del capítulo 1 se hace a nivel de parcela, no sólo de localidad. Las circunscripciones más cargadas son la III (15), la VII (13) y la IV (11).

**Cómo se determinó la localidad.** Tomé la que el decreto nombra explícitamente como «Ciudad de X» o «localidad de X». No usé la mención «Partido de San Isidro», que aparece en todos los decretos y habría inflado San Isidro artificialmente. Los 22 sin inmueble quedan marcados como «general / sin inmueble», no imputados a ninguna localidad.

**Un decreto para mirar aparte.** El DECRE-2025-614 veta la Ordenanza Municipal N° 9395, de Paisaje Protegido Municipal, sancionada por el Concejo. Si el capítulo toca el rechazo vecinal al plan urbano, ese veto es material directo.

---

## 2. Los $167.005 millones: no se reparten parejo

### Por año

| Año | Decretos | Monto | % del total |
|---|---:|---:|---:|
| 2024 (desde febrero) | 246 | $65.274.008.894 | 39,1% |
| 2025 (año completo) | 250 | $72.411.395.844 | 43,4% |
| 2026 (hasta julio) | 77 | $29.320.562.693 | 17,6% |

Son pesos corrientes sin ajustar por inflación, así que la comparación entre años no dice nada sobre volumen real de obra. Lo que sí dice algo es la distribución dentro de cada año.

### Dos meses explican casi un tercio de todo

| Mes | Monto | % del total |
|---|---:|---:|
| Septiembre 2024 | $31.969.192.761 | 19,1% |
| Abril 2025 | $25.047.884.552 | 15,0% |

Todos los demás meses están por debajo de los $11.000 millones y la mayoría por debajo de $6.000 millones.

**Y dentro de esos dos meses, dos decretos:**

- **DECRE-2024-1258**, de septiembre de 2024: Licitación Pública N° 38/2024, «Puesta en valor y mantenimiento de la red vial y aceras en el Partido de San Isidro». **$26.933.887.263**, dividido en tres zonas: Zona 1 a VIAL TEC S.A. – TECNOVÍAS S.R.L. U.T.E. ($7.161.649.393,91), Zona 2 a CONSTRUMEX S.A. ($6.658.961.115,45) y Zona 3 a ALTOTE S.A. ($7.095.611.905,90). **Un solo decreto = 16,1% de todo lo adjudicado en dos años y medio.**
- **DECRE-2025-398**, de abril de 2025: Licitación Pública N° 69/2024, servicio de seguridad y vigilancia, a SEGURIDAD GRUPO MAIPÚ S.A., **$13.448.373.748,32**. Un solo decreto = 8,1% del total.

Los dos los verifiqué leyendo el PDF completo, no por índice.

### Concentración por adjudicatario

Sobre 332 adjudicatarios con monto atribuible:

- **Los 10 primeros se llevan el 42,1%.**
- **Los 25 primeros se llevan el 64,6%.**

| # | Adjudicatario | Decretos | Monto |
|---:|---|---:|---:|
| 1 | SEGURIDAD GRUPO MAIPÚ S.A. | 4 | $13.875.725.428 |
| 2 | ALTOTE S.A. | 2 | $8.544.192.688 |
| 3 | CONSTRUMEX S.A. | 2 | $8.107.541.897 |
| 4 | DATCO S.A. | 3 | $5.792.235.814 |
| 5 | TECNOVÍAS S.R.L. | 3 | $5.717.143.127 |
| 6 | EXANET S.A. | 3 | $5.524.541.374 |
| 7 | INTERNATIONAL HEALTH SERVICES ARGENTINA S.A. | 3 | $4.947.831.867 |
| 8 | MANTELECTRIC I.C.I.S.A. | 3 | $4.811.892.216 |
| 9 | VERDE INTEGRAL S.A. | 1 | $4.729.401.373 |
| 10 | SILICA NETWORKS S.A. | 1 | $3.804.111.306 |

**Ojo con leer esto como ranking de facturación.** Es monto adjudicado por decreto, no pagado. En 407 de los 552 decretos con monto cada empresa tiene su cifra propia en el artículo y la atribución es exacta. En los 144 restantes el decreto da un total sin abrirlo por empresa y repartí en partes iguales entre los adjudicatarios del acto: ahí la cifra individual es aproximada. Ver la ADENDA_2 para el ranking estricto, que es el que hay que citar.

El contraste que importa no es el ranking sino el otro: **sabemos exactamente cuánto cobró cada uno y no sabemos dónde tiene domicilio ninguno.**

---

## 3. Archivos de esta adenda

| Archivo | Qué trae | Filas |
|---|---|---|
| `10_urbanismo_por_localidad.csv` | Los 95 decretos urbanos con localidad, dirección y catastro | 95 |
| `11_montos_por_mes.csv` | Monto adjudicado mes a mes | 30 |
| `12_ranking_adjudicatarios_por_monto.csv` | Ranking completo con % acumulado | 332 |
