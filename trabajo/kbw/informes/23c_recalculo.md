# Informe 23 ter · Recálculo con las decisiones de Nick: teléfonos, escuelas y espectáculos

**Fecha:** 7 de octubre de 2026. Sólo investigación: no se tocó `doc/` ni `salida/`.

**Fuentes:** `01_raw/23c/`, con un `FUENTES.txt` (archivo, bytes, URL, fecha y qué es) y un `NO_SUBIDOS.txt`. Subcarpetas:
- `1_agentes_turnos_financiacion`
- `2_video_datos_nube`
- `3_shows_calidad_alquiler`
- `4_robos_spotify`
- `0_cuentas`: las cuentas del coordinador.

**Plata:**
- Pesos de diciembre de 2025, deflactados con el IPC del repositorio. El último mes es julio de 2026, así que los precios posteriores quedan un poco altos.
- Dólar a $1.447,84 (BCRA, Comunicación A 3500, promedio de diciembre de 2025).

**Marcas:**
- [verificado]: leído en la fuente primaria.
- [probable]: prensa o fuente secundaria.
- [sin confirmar].
- [cálculo propio].
- [inferencia].
- Lo jurídico lleva además «necesita dictamen de un abogado».
- Lo que comunica un municipio va «según el Municipio».
- «No lo encontré» no quiere decir que no exista.

**Nombres:** se nombran empresas, entidades y escuelas para poder verificar; el documento no las nombra. No se nombra a ninguna persona.

## Decisiones de Nick sobre el 23 bis (registro; las aplica el worker del documento)

- **Redes:**
  - reja con alivio, revisada cada semana y después de cada lluvia, por la cuadrilla;
  - concurso abierto a las cooperativas del partido.
- **Teléfonos:**
  - sin transmisión en vivo y con teléfono propio;
  - empiezan inspectores y tránsito.
- **Escuelas:** gratis en las públicas y en todo colegio privado que el Estado financia al 100%.
- **Privados:** cada alumno paga lo que usa, con su parte del equipo de personas.
- **Espectáculos:**
  - 200 shows;
  - si el Municipio cancela, paga el 70% y después el show entero en la nueva fecha;
  - cancela la alerta amarilla.
- **Mensajes de texto:** sólo a quien dio su celular; los paga Tránsito.

---

## Respuestas en una línea

**1 · Teléfonos:**
- **Agentes**, según el Presupuesto 2026 [verificado]:
  - hay entre 81 y 103 inspectores de comercio, industria y la Agencia de Control;
  - tránsito tiene 177 cargos; según el Municipio, 120 son agentes de tránsito.
- **Turnos:** 7 horas por 5 días para inspectores y 8 horas por 6 días para tránsito [inferencia sobre la escala municipal].
- **Video:** 1080p alcanza y pesa 2,3 GB por hora [cálculo propio].
- **Datos:** sin transmisión en vivo alcanza con 1 GB por mes, unos $82.000 por año por agente [verificado el precio].
- **Guarda:** en Google Cloud Bélgica, 6 meses con acceso rápido y 18 de archivo.
- **Costo:**
  - primera etapa (inspectores y tránsito): 20 a 27 M de compra y 104 a 141 M por año;
  - Patrulla: 30 a 35 M de compra y 136 a 162 M por año [cálculo propio].
- **Financiación:** Banco Provincia ya vende el teléfono apto en 24 cuotas sin interés, sin plata del Estado [verificado].

**2 · Escuelas:**
- 13 unidades privadas tienen aporte del 100%, con 4.035 alumnos [verificado]. Ningún colegio tiene el 100% en un nivel y menos en otro.
- Para el Municipio, los gratuitos (22.748 alumnos) cuestan 152 a 181 M por año con uso esperado, y 788 a 979 M con uso pleno [cálculo propio].
- El alumno privado que lo usa paga unos $930 a $1.040 por sesión de 20 minutos con uso esperado.
- Con eso entran 272 a 306 M por año [cálculo propio].

**3 · Espectáculos:**
- **Cachets:** los 200 shows, con las cancelaciones por alerta amarilla, cuestan unos 214 M por año [cálculo propio].
- **Equipos:** 2 no alcanzan; hacen falta 3, con 8 personas [cálculo propio].
- **Calidad:** el kit del 23 bis no alcanza para bandas ante 300 personas. Con subwoofer y monitores, el kit de show cuesta 29,5 M.
- **Costo total:** todo propio son 107 M por año, contra 146 a 683 M si se alquila [cálculo propio].
- **Control contra robos:** unos 5 M de compra y 2 a 3 M por año.
- **Spotify:** los oyentes mensuales son públicos, pero no se pueden leer con programas. Se verifican con una captura y declaración jurada, o con un acceso de «lector» del Municipio [verificado].

---

## 1 · Teléfonos de los inspectores (diseño nuevo)

**El diseño decidido:**
- el agente graba todo el turno con su teléfono, desde la inteligencia artificial del Municipio, en un soporte en el pecho;
- cada bloque se sella al grabar y su huella llega a la inteligencia artificial del Municipio en el momento;
- el video se sube por wifi en la base;
- no hay transmisión en vivo;
- el teléfono es propio y es requisito del puesto;
- el Municipio paga el plan de datos, el soporte y la batería.

### 1.1 · Cuántos agentes

**Fuente:** el Presupuesto 2026 (Ordenanza 9422), formulario F6 «Jurisdicción, Categoría Programática y Cargo». Es un PDF escaneado. Revisé las páginas 164 y 176 como imagen; las cifras coinciden [verificado].

| Grupo | Cargos 2026 | Agentes en la calle | Lo que dice el Municipio |
|---|---|---|---|
| **Fiscalización** (comercio, industria y Agencia de Control) | 120 | **81 a 103**: 32 de servicio y 49 mensualizados como piso; todos menos los 17 superiores y jerárquicos como techo [cálculo propio] | Sin cifra |
| **Tránsito** (Gestión de la Política de Movilidad, que incluye la Jefatura de Inspectores) | 177 (64 de servicio y 103 mensualizados) | **120 a 167** | 120 agentes de tránsito (03/08/2026) |
| Patrullaje municipal | 359 | **300 a 359** | 331 efectivos (2025); 300 en la calle (2026) |
| Monitoreo | 158 | No inspecciona | 145 |
| Habilitaciones y Permisos | 29 (4 técnicos) | No se sumó | — |

- **La «Jefatura de Inspectores» es el cuerpo de tránsito** [verificado]: depende de la Subsecretaría de Movilidad, y sus agentes cobran la bonificación de «Inspectores de Tránsito con Jornada Prolongada».
- **Metas 2026 de la Agencia de Fiscalización** [verificado]: 10.000 fiscalizaciones de comercios, 610 de obras y 420 habilitaciones. Son unas 100 a 130 por inspector por año [cálculo propio].

### 1.2 · Horas de turno

- **Ley 14.656, art. 71:** jornada de 6 a 8 horas diarias. El Municipio puede fijar otros regímenes [verificado].
- **Ordenanza 9422, arts. 10 y 12:** regímenes de 35, 40 (sólo enfermería) y 48 horas; la jornada prolongada de 48 h suma 30% [verificado].
- **Tránsito:**
  - categoría 8 de 35 horas más la bonificación de jornada prolongada, es decir 48 horas;
  - el Decreto 782/2026 habla de «8 horas diarias»;
  - según el Municipio, hay «turnos durante los siete días de la semana».
  - Queda en **8 horas por 6 días** [verificado las 48 h; el reparto es inferencia].
- **Inspectores de comercio:** cargos de 35 horas; la oficina atiende de lunes a viernes de 8 a 14, según el Municipio. Quedan en **7 horas por 5 días** [inferencia].
- **Patrulla:**
  - cargos de 35 horas; el servicio funciona las 24 horas los 365 días;
  - **la duración de cada turno no la encontré**;
  - se usó 7 horas por 5 días [supuesto].

### 1.3 · Calidad del video y peso

- **Guías** [verificado]:
  - EE. UU. (DHS SAVER, citado por el NIJ) y el Reino Unido (Home Office, 2018) piden como mínimo definición estándar y 25 cuadros;
  - las cámaras corporales usan sobre todo 1080p;
  - Salta (LP 14/2026) pidió Full HD con H.265.
- **Recomendación** [inferencia]:
  - 1080p a 30 cuadros, con la lente principal (no la gran angular) y H.265 a 5 Mbps;
  - con eso se ven caras y patentes a 1 a 2 metros, y llega casi justo a 3 metros;
  - los documentos se leen acercándolos o con una foto, que se sella igual.
- **Peso** [cálculo propio]:
  - **2,34 GB por hora**;
  - un turno de 7 horas son unos 16 GB, y uno de 8, unos 19 GB.
- **Bloques de 10 minutos:**
  - Android cambia de archivo sin cortar la grabación [verificado];
  - se sella cada bloque, la huella de cada uno incluye la del anterior, y si falla el equipo se pierde a lo sumo un bloque [inferencia].
- **Memoria:** el teléfono necesita unos 46 GB libres para cubrir dos turnos de 8 horas [cálculo propio].
- **Batería:** con una externa de 10.000 mAh se cubren los turnos de 6 y 8 horas; para 12 horas hace falta una de 20.000 mAh [inferencia; hay que probar el calor en un piloto].

### 1.4 · Plan de datos mínimo

- **Huellas:** una huella firmada pesa menos de 1 KB. Con el control de la app, son unos 1 MB por turno [cálculo propio].
- **Con todo lo demás** (consultas a la inteligencia artificial del Municipio, actas y fotos reducidas): unos 12 MB por turno, de 0,2 a 0,3 GB por mes [cálculo propio].
- **Plan mínimo que alcanza:** 1 GB de solo datos.
  - En el convenio de la Ciudad de Buenos Aires (623-0849-LPU25, renglón 21, abril de 2026) cuesta **$6.631 a $7.119 por mes**, unos **$82.000 por agente y por año** [verificado el precio y el renglón en el pliego].
  - Si el agente necesita voz, el plan de 5 GB con voz cuesta unos $233.000 por año.
- **Ojo:** en un teléfono personal con dos chips, Android usa uno solo para datos, así que no está garantizado que la app salga por la línea municipal [inferencia].

### 1.5 · Subida en la base

- **Tiempo:** un turno de 8 horas tarda 29 minutos en subir a 100 Mbps [cálculo propio].
- **Volumen:** si 150 agentes vuelven juntos y se van a los 30 minutos, subir directo a Europa no es posible [cálculo propio].
- **Lo que funciona:** una **estación de descarga en cada base**, que recibe por la red interna y reenvía a Europa durante 24 horas. Cuesta unos **9,5 M por base** [cálculo propio sobre precios del 23 bis; supuesto el armado].
- **Red del Municipio:** tiene fibra y centro de datos propios (LP 86/2024 y otras) [verificado]. No encontré la capacidad de su salida a internet.

### 1.6 · Guarda en Europa: 6 meses rápida y después archivo

| Proveedor y región | $ por TB de video (24 meses) | Recuperar del archivo | Marca |
|---|---|---|---|
| **Google Cloud, Bélgica** (Coldline 6 meses + Archive 18) | **74.186** | Al instante | [verificado el precio; cálculo propio el total] |
| Azure, Suecia (Cold + Archive) | 68.128 | Hasta 15 horas | Ídem |
| AWS, Estocolmo o Irlanda | 72.165 | Horas | Ídem |
| OVHcloud, Francia (empresa europea) | 85.606 | Requiere restauración | Ídem |

- **Recomendación:** Google Cloud en Bélgica, con retención bloqueada por 24 meses. Todo se ve al instante y cuesta un 9% más que Azure Suecia [inferencia].
- **Legalidad:** Bélgica es país «adecuado» para la Ley 25.326 (Disposición 60/2016) [verificado]. Que la empresa sea de EE. UU. necesita dictamen de un abogado. Si se descarta, la alternativa es OVHcloud, un 15% más cara.
- **Otros costos:**
  - escribir y cambiar de capa cuesta poco, US$1,2 a 1,5 por TB;
  - con el plan de 6 + 18 meses no hay cargo por borrar antes de tiempo [verificado].

### 1.7 · Costo por etapa

**Por agente** [cálculo propio]:
- compra: soporte de pecho y batería, **$98.327**;
- por año: guarda + datos ($82.495) + reposición del kit cada 2 años ($49.164).

| Grupo | Horas | TB por año por agente | Por agente y año, en régimen | Agentes | Compra | Por año, en régimen |
|---|---|---|---|---|---|---|
| Inspectores | 7 h × 22 turnos por mes | 4,32 | $452.463 | 81 a 103 | 8,0 a 10,1 M | 36,6 a 46,6 M |
| Tránsito | 8 h × 26 turnos por mes | 5,84 | $564.952 | 120 a 167 | 11,8 a 16,4 M | 67,8 a 94,3 M |
| **Primera etapa** | | | | **201 a 270** | **19,8 a 26,5 M** | **104,4 a 141,0 M** |
| **Segunda etapa: Patrulla** | 7 h × 22 [supuesto] | 4,32 | $452.463 | 300 a 359 | **29,5 a 35,3 M** | **135,7 a 162,4 M** |

- **Aparte:** una estación de descarga por base, unos 9,5 M cada una. Tránsito tiene 2 bases, según el Municipio.
- **El primer año** la guarda cuesta menos, porque se va acumulando: unos dos tercios del régimen.
- **No incluye** el teléfono (es propio) ni los impuestos argentinos al pago de un servicio del exterior (necesita dictamen de un abogado o contador).
- **Contra el diseño del 23 bis**, que transmitía en vivo: con 420 agentes eran 490 a 736 M por año, casi todo en datos. Sin transmisión, los datos pasan a ser lo de menos y lo que pesa es la guarda.

### 1.8 · Financiación y descuentos para el teléfono propio

| Precedente | Condiciones | ¿Puso plata el Estado? | Marca |
|---|---|---|---|
| **Banco Provincia, «Provincia Compras»** | El Galaxy A27 5G 8/256 a $925.999 (= $776.091) en 18 o 24 cuotas sin interés, con tarjeta del banco. La cuota es el 7,4% del básico de la categoría 8 | No: es promoción del banco | [verificado] |
| PC Docente (Nación, 2020) | Banco Nación: 36 cuotas al 12% anual; las empresas, 20% de descuento | Sí: Educación puso dinero para bajar la tasa | [probable] |
| General Pueyrredon, código de descuento por recibo (Decreto 557/2021) | Préstamos con retención del sueldo y tope de tasa | No: el Municipio cobra un 2% de gastos | [verificado] |
| Reino Unido («Home & Tech») | El empleador paga el equipo y lo recupera del sueldo en hasta 12 cuotas, sin interés | Sólo adelanta | [verificado] |
| Samsung EE. UU., programa para empleados públicos | Hasta 30% de descuento con correo oficial | No | [verificado] |
| Cuota Simple / Ahora 12 | **Ya no existe** (Res. SIC 12/2026) | — | [verificado] |

- **Opciones** [inferencia]: un convenio con el banco que paga los sueldos o con una marca, por cuotas sin interés o con descuento, sin plata del Municipio.
- **Pendiente:** no encontré qué banco paga los sueldos de San Isidro.

**El teléfono propio como requisito** [verificado el texto; necesita dictamen de un abogado]:
- **No encontré** una convocatoria de empleo público argentina que lo exija. Lo más cercano son los delegados de la Justicia Electoral, pero es una carga pública y tienen alternativa si no tienen teléfono.
- **Reparo:** la Ley 14.656 da derecho a «ropas y útiles de trabajo» (arts. 6 q y 17). Se puede acordar en la negociación colectiva (art. 54) y prevé compensar gastos (art. 75).
- **Riesgo:** exigir el teléfono puede dejar afuera a postulantes que no lo tengan [inferencia].
- **EE. UU.:** algunas ciudades pagan un monto mensual por usar el teléfono propio: US$45 por mes en Capitola y Prosser [verificado].

---

## 2 · Escuelas: gratis en las públicas y en los privados con aporte del 100%

**Colegios privados con aporte del 100%** (padrón provincial al 28/09/2026, Relevamiento Inicial 2026) [verificado]:

| Escuela | Primaria | Secundaria |
|---|---|---|
| Nuestra Señora de Lourdes | 353 | 359 |
| Plácido Marín | 166 | 157 |
| San Andrés Avelino | 375 | 359 |
| San José | 397 | 560 |
| San Francisco Javier | 167 | — |
| Santo Domingo Savio | 447 | 339 |
| Sagrada Familia | — | 161 |
| Santísima Trinidad | — | 195 |
| **Total** | **1.905** | **2.130** |

- **Total: 4.035 alumnos**, el 12,9% de los 31.234 de privados.

**Colegios con 100% en un nivel y menos en otro:**
- Hoy no hay ninguno. Revisé todos los niveles de cada uno en el padrón [verificado]:
  - Sagrada Familia y Santísima Trinidad sólo tienen secundaria en el padrón;
  - San Francisco Javier sólo tiene primaria;
  - el «Santa Trinidad» de Avellaneda 450 es otro colegio, sin aporte.
- **Regla propuesta:** que la gratuidad vaya por unidad educativa (cada nivel), porque el aporte se fija así [inferencia; necesita dictamen de un abogado].
  - Si un colegio tiene 100% en primaria y 80% en secundaria, la primaria es gratis y la secundaria paga.
  - Se toma el aporte vigente en el padrón al inicio de cada año lectivo.

**Costo para el Municipio de los gratuitos** (públicas 18.713 + aporte del 100% 4.035 = **22.748**), sin el equipo de personas [cálculo propio]:
- **Método:** sus usuarios cargan con su uso (inteligencia artificial, voz, avatar y servidores). Además se suman las netbooks y los datos para los chicos sin equipo, el internet de los centros y la capacitación, que van todos a las escuelas gratuitas.

| | Uso esperado (15%) | Uso pleno |
|---|---|---|
| Alumnos que lo usan | 3.412 | 22.748 |
| Costo por año, sin equipo | **151,9 a 180,5 M** | **788,3 a 979,1 M** |
| Su parte del equipo de personas (va en el cuadro 27) | 120,7 M | 120,7 M |

**Lo que paga cada alumno privado que lo usa** («paga lo que usa, con su parte del equipo de personas») [cálculo propio]:
- **Componentes:** el uso (inteligencia artificial, voz, avatar y servidores) más su parte de los 269,7 M del equipo, repartida entre todos los que lo usan.

| | Uso esperado (15%) | Uso pleno |
|---|---|---|
| Uso, por año | $31.282 a $39.674 | $24.831 a $33.219 |
| Parte del equipo, por año | $35.370 | $5.306 |
| **Total por año** | **$66.652 a $75.045** | **$30.137 a $38.525** |
| Por mes (10 meses) | $6.665 a $7.504 | $3.014 a $3.852 |
| **Por sesión de 20 minutos (72 por año)** | **$926 a $1.042** | **$419 a $535** |
| Privados que lo usan y pagan (de 27.199) | 4.080 | 27.199 |
| **Ingreso por año** | **271,9 a 306,2 M** (144,3 M de equipo) | **819,7 a 1.047,8 M** (144,3 M de equipo) |

- **Con uso esperado, la parte del equipo pesa más que el uso**, porque los 269,7 M se reparten entre pocos usuarios. Con uso pleno, el precio por sesión baja a la mitad [cálculo propio].
- **Una forma simple de cobrarlo:** un precio por sesión, de unos $1.000 con uso esperado, que la inteligencia artificial del Municipio cobra al usarse [inferencia]. Si se cobra por sesión, el ingreso sigue al uso real.
- **Recordatorio:** los alumnos de las públicas son los de 2025 (informe 22) y los de privados, de 2026 (padrón).

---

## 3 · Espectáculos: 200 shows

### 3.1 · Costo de los 200 shows con la regla de Nick

**Mezcla y precio del 23 bis:**
- 40% solistas, 30% dúos o tríos y 30% bandas;
- piso del sindicato más 25%: **$980.112 por show en promedio**;
- 200 shows sin cancelaciones = **196,0 M** [cálculo propio].

**¿Cuántos días hay alerta amarilla?** El SMN no publica cuántas alertas emite por zona [verificado: sólo hay totales del país]. Por eso se estimó con las estadísticas oficiales [verificado]:
- San Fernando: 72 días por año con lluvia de 1 mm o más y 45 con tormenta (normales 1991-2020);
- alertas en todo el país en 12 meses (2021-2022): 1.077, de las que acertaron entre el 70% y el 77%.

**Estimación para la zona de San Isidro** [inferencia]:
- unos **33 días por año** con alerta amarilla o mayor (rango de 14 a 53);
- más días entre diciembre y febrero (13% a 14% de los días) que en invierno (4%).

| Temporada | % de shows cancelados | Cancelaciones | 70% pagado | **Total de cachets por año** |
|---|---|---|---|---|
| **Octubre a abril** (escenario central) | 11,6% | 26 | 18,0 M | **214,0 M** |
| Octubre a abril (bajo / alto) | 4,7% / 18,4% | 10 / 45 | 6,8 / 31,0 M | 202,8 / 227,0 M |
| Todo el año (central) | 9,1% | 20 | 13,8 M | 209,8 M |

- La nueva fecha también puede caer en alerta; eso ya está en la cuenta.
- **Si sólo cancela la alerta que cubre el horario del show:** cerca del 7% de cancelaciones [supuesto].
- **El 70%, según la formación** [cálculo propio]:
  - solista, $274.000;
  - dúo o trío, $686.000;
  - banda, $1,24 M.
- **Riesgo ante el Tribunal de Cuentas** (informe 23 bis): pagar el 70% sin show necesita una cláusula expresa en el contrato firmado antes, y la constancia de la nueva fecha. Necesita dictamen de un abogado.

### 3.2 · ¿2 o 3 equipos de producción?

**Jornadas que hacen falta por año** [cálculo propio]:
- callejeros de lunes a jueves: 320;
- 200 shows de 9 horas: entre 605 y 646 en total, contando las cancelaciones del mismo día y un 10% de mantenimiento.

**Lo que da cada opción:**
- **2 equipos** dan 444 jornadas: alcanzan para los callejeros y unos 79 shows. **No alcanzan.**
- **3 equipos** dan 666 jornadas: **alcanzan**.
- **Semana pico:** si los shows son sólo de octubre a abril, piden 17,5 jornadas contra 15 disponibles. Hay que hacer funciones dobles o repartir los shows en el año.

| | Personas | Por año | Con 15% de reemplazos |
|---|---|---|---|
| 2 equipos | 2 técnicos, 2 asistentes y 1 chofer | 46,4 M | 53,4 M |
| **3 equipos** | **3 técnicos, 3 asistentes y 2 choferes** | **74,2 M** | **85,3 M** |

- Escala del Decreto 782/2026: técnico de categoría 9, asistente de categoría 6 y chofer de categoría 7.
- **Turnos escalonados posibles:**
  - lunes a viernes;
  - lunes a jueves más el sábado;
  - miércoles a domingo.

### 3.3 · Calidad del sonido

**Qué piden los pliegos** [verificado]:
- **Ciudad de Buenos Aires** (Usina del Arte, BAC 3190-1544-CME24): bafles autopotenciados, consola, micrófonos inalámbricos y un operador por espacio.
- **Malargüe** (aire libre): line array con subwoofers, consola Behringer XR18, 2 monitores, 5 micrófonos SM58 y cajas directas.
- **Montevideo** (bandas emergentes): hasta 20 canales, hasta 6 mezclas de monitor y 4 micrófonos de batería.
- **Ningún pliego argentino de los que encontré fija decibeles:** piden potencia, cantidad de cajas y marcas «tipo… o superior».
- **El pliego de la LP 3/2026 de San Isidro:** no lo encontré.

**¿El kit del 23 bis cumple?** [verificado las fichas; cálculo propio la presión sonora]
- **Sí cumple:** la consola XR18 (la misma que pidió Malargüe), los micrófonos SM58 y SM57, la energía y el técnico.
- **No cumple para bandas ante 300 personas:**
  - las columnas JBL EON ONE PRO dan unos 89 dB a 20 m;
  - no hay subwoofer;
  - con 2 monitores no alcanza, porque una banda necesita 4 mezclas;
  - faltan micrófonos de batería y uno inalámbrico;
  - además, la JBL EON ONE PRO figura como **discontinuada** en la página del fabricante.
- **Para solistas y dúos hasta unas 100 personas, alcanza.**

**Kit óptimo para shows** (precios de Todo Música y Hendrix, octubre de 2026) [verificado los precios]:
- 2 bafles dB Technologies B-Hype 12 (126 dB) y 1 subwoofer dB SUB 615 (131 dB);
- 4 monitores B-Hype 10;
- consola Behringer XR18;
- 7 micrófonos Shure, kit de micrófonos de batería e inalámbrico Sennheiser;
- 4 cajas directas activas y 2 estaciones de energía EcoFlow.
- **Costo:** sonido **19,4 M**; con tarima de 3 × 4 m y toldos, **29,5 M por kit**.
- Da unos 103 dB a 10 m y 97 dB a 20 m. Alcanza para una banda ante 300 personas [cálculo propio].
- Variante de más calidad: bafles dB KL 12, unos 0,55 M más por kit.
- **Kit para callejeros:** 2 columnas JBL EON ONE Compact (12 h de batería), 3 micrófonos, pies y cables: **4,9 M**. Cumple el tope de 65 a 72 dB.

### 3.4 · Robos y roturas

**Lo que más protege contra el robo interno es el procedimiento, no el aparato** [inferencia sobre los precedentes]:
- cargo patrimonial firmado por cada kit, a nombre de un responsable;
- remito de salida y entrada en cada show, con QR y la firma de 2 personas;
- arqueo sorpresa mensual hecho por Patrimonio, no por Cultura: 0,27 M por año. San Isidro tiene un Departamento de Patrimonio (Decreto 637/2026) [verificado];
- depósito con acceso registrado y cámaras;
- separar funciones: quien administra el control de acceso no custodia el equipo.

| Control | Opción | Compra | Por año | Marca |
|---|---|---|---|---|
| **GPS de la camioneta** | Con corte de corriente, conectado al sistema de seguimiento de flota (AVL) que el Municipio ya tiene. San Isidro ya compró «equipos GPS» dos veces (CP 48/2025, $12,06 M; LPriv 40/2025, $61,99 M) | 0,23 M | 0,16 M | [verificado] las compras |
| **Rastreo de las cajas** | Rastreadores Bluetooth moto tag ($41.905 cada uno) y 1 GPS 4G escondido por kit | 0,46 M por kit | 0,19 M por kit | [verificado] los precios |
| **Seguro** | Equipos electrónicos con Provincia Seguros, por contratación directa (LOM, art. 156, inc. 2), como Quilmes, Salto y Mar Chiquita. Para el robo del propio personal está la póliza de infidelidad de empleados | — | 0,48 a 1,23 M para 3 kits | [verificado] los precedentes; la tasa es [supuesto]: no hay tasa argentina publicada |
| **Marcado** | Grabado «Municipalidad de San Isidro – Patrimonio N°» con lápiz grabador, más etiqueta QR | 0,09 M el grabador; 0,015 M por kit las etiquetas | — | [verificado] el precio del grabador |
| **Depósito con cámaras** | 2 cámaras, licencia del sistema de video y control de acceso con registro | 3,47 M (compra menor) o 7,25 M (ampliando la LP 76, con 36 meses de mantenimiento) | 0,35 M | [cálculo propio] |
| **Total, 3 kits y camioneta** | | **5,2 M** (8,1 M con 4 cámaras) | **2,0 a 2,7 M** | [cálculo propio] |

- **Por qué conviene:** cuesta cerca del 5% de lo que protege una vez y el 1,7% por año [cálculo propio].
- **Inventariar ya es obligatorio** [verificado; el alcance necesita dictamen de un abogado]:
  - Ley Orgánica de las Municipalidades, arts. 167 y 168;
  - Decreto 2980/00, arts. 127 a 135, con recuento físico anual;
  - Acordada 4/84 del Tribunal de Cuentas.
- **Precedentes** [verificado, en boletines oficiales]:
  - Quilmes dio de baja bienes de Cultura «por robo» y aseguró «Robo – Fidelidad de Empleados» con Provincia Seguros;
  - en Coronel Rosales, las cámaras registraron el faltante de un parlante de Cultura; se cambiaron la cerradura y la alarma y se abrió un sumario;
  - en General Pueyrredon, el sumario por una pachera de sonido robada se cerró porque no se pudo saber ni el día ni el autor. Eso pasa sin registro de acceso;
  - Coronel Suárez obliga a tener GPS en todos los vehículos municipales (Ordenanza 8454/2025);
  - Filadelfia sólo encontró el 47% de los equipos de una muestra de su auditoría.
- **Datos personales:** rastrear vehículos que usan empleados y usar huella en el control de acceso necesitan dictamen de un abogado (Ley 25.326).

### 3.5 · Alquilar o equipo propio

**Precios de alquiler de referencia por evento** [verificado]:
- Ciudad de Buenos Aires: 0,6 M por espacio y día.
- Municipios bonaerenses: de 0,1 a 7,4 M.
- San Isidro: 5,3 a 39,0 M por evento, en concursos de 2024 y 2025.
- **La LP 3/2026 de San Isidro** (71,1 M) no publica cuántos eventos cubre: si fueran 100, serían 0,7 M cada uno.

| Opción | Por año | Compra |
|---|---|---|
| **A. Todo propio:** 3 equipos, 2 kits de show, 2 de callejeros y camioneta grande | **106,8 M** (personas, amortización y camioneta) | **125,9 M** |
| B. 2 equipos sólo para callejeros + alquilar los 200 shows | 211,5 / 381,2 / 748,2 M (alquiler bajo / central / alto) | 61,9 M |
| C. 2 equipos con kits de show: 79 shows propios y 121 alquilados | 172,8 / 275,5 / 497,5 M | — |

- **Los 200 shows con equipo propio** cuestan 41,5 M por año más que tener sólo los callejeros: unos 0,2 M por show, contra 0,7 a 3,3 M si se alquilan [cálculo propio].
- **Mejorar la calidad** sobre el kit del 23 bis suma 2,7 M por año y 18,2 M de compra.

**Programa completo** [cálculo propio]:
- cachets 214,0 M + producción 106,8 M + control contra robos 2,0 a 2,7 M = **unos 323 M por año**;
- compra: 125,9 + 5,2 = **131,1 M**;
- **el primer año, unos 454 M**.

### 3.6 · Definiciones de Nick y verificación de Spotify

- **Artista del partido:** domicilio del DNI en San Isidro de al menos el 50% de la agrupación.
  - El último domicilio del DNI es el que vale (Ley 17.671, art. 47) y dar uno falso está penado (art. 40 c) [verificado, informe 23 bis].
  - Se verifica con el DNI de cada integrante al inscribirse [inferencia].
  - Necesita dictamen de un abogado.
- **Emergente:** menos de 50.000 oyentes mensuales en Spotify.
  - **El dato es público:** Spotify dice que los oyentes mensuales son una cifra pública en la app y que se depuran de las reproducciones artificiales [verificado].
  - **No se puede leer con programas:** la API oficial no lo da, y desde febrero y marzo de 2026 tampoco da seguidores ni popularidad [verificado].
  - **Además, Spotify lo prohíbe:** sus pautas prohíben el «rastreo» o la «extracción» por medios automatizados [verificado; el alcance necesita dictamen de un abogado].
  - **Método propuesto** [inferencia; necesita dictamen de un abogado]:
    1. al inscribirse: enlace al perfil, captura fechada de Spotify for Artists y declaración jurada;
    2. verificación fuerte: el artista suma una cuenta del Municipio como «lector» (Reader) de su equipo en Spotify for Artists, que es gratis, y la quita al cierre [verificado que el lector ve las estadísticas];
    3. control cruzado: un agente mira la página pública el día del cierre. La inteligencia artificial del Municipio sólo compara datos cargados por personas; no lee Spotify.
  - **Artistas que no están en Spotify:**
    - YouTube tiene una API oficial que da suscriptores y vistas [verificado];
    - para SoundCloud y Bandcamp, captura y enlace;
    - no estar en Spotify no excluye a nadie [propuesta].

---

## Tabla final

| Tema | Opción | Costo (pesos de dic-2025) | Fuente |
|---|---|---|---|
| Teléfonos, primera etapa (inspectores 81 a 103 y tránsito 120 a 167) | Teléfono propio, soporte y batería, 1080p H.265, bloques sellados, subida por wifi, datos M2M de 1 GB, guarda en Google Cloud Bélgica | 19,8 a 26,5 M de compra; 104,4 a 141,0 M por año en régimen; más 9,5 M por base | Presupuesto 2026 (F6); convenio de telefonía de la Ciudad; precios oficiales de Google Cloud; guías del NIJ y del Home Office |
| Teléfonos, segunda etapa (Patrulla, 300 a 359) | Ídem | 29,5 a 35,3 M de compra; 135,7 a 162,4 M por año | Ídem |
| Financiación del teléfono propio | Convenio con el banco que paga los sueldos o con una marca: cuotas sin interés o descuento | 0 para el Municipio | Banco Provincia; PC Docente; Reino Unido; Samsung EE. UU. |
| Profesor digital, gratuitos (públicas y privados con aporte del 100%: 22.748) | Uso real más netbooks, datos, centros y capacitación | 151,9 a 180,5 M por año (15%); 788,3 a 979,1 M (pleno); más 120,7 M de su parte del equipo en el cuadro 27 | Padrón provincial 28/09/2026; informes 23 y 23 bis |
| Profesor digital, alumno privado que lo usa | Paga lo que usa con su parte del equipo | $926 a $1.042 por sesión (15%) o $419 a $535 (pleno); ingreso de 271,9 a 306,2 M por año (15%) | Ídem |
| 200 shows de emergentes | Piso del sindicato más 25%; 70% al cancelar y el show entero en la nueva fecha; alerta amarilla | 214,0 M por año (rango de 202,8 a 227,0) | Tarifas SADEM; normales del SMN 1991-2020; verificación de alertas del SMN |
| Equipos de producción | 3 equipos, 8 personas, 2 kits de show de 29,5 M y 2 de callejeros de 4,9 M, camioneta | 125,9 M de compra; 106,8 M por año | Decreto 782/2026; Todo Música y Hendrix; pliegos de la Ciudad, Malargüe y Montevideo |
| Control contra robos | Procedimiento más GPS, seguro, marcado y depósito con cámaras | 5,2 M de compra; 2,0 a 2,7 M por año | Decretos de San Isidro (GPS, seguros, LP 76); precedentes de Quilmes, Coronel Rosales y General Pueyrredon |
| Alquilar en vez de equipo propio | Alquilar los 200 shows | 146 a 683 M por año (central 316 M), contra 41,5 M de equipo propio extra | LP 3/2026 de San Isidro; Ciudad BAC 3190-1544-CME24; decretos de otros municipios |
| Verificar «emergente» | Captura + declaración jurada + acceso de lector a Spotify for Artists; YouTube por su API | 0 | Spotify (Web API, pautas, Spotify for Artists); YouTube Data API |

---

## Dónde busqué y no encontré

- **Teléfonos:**
  - la duración del turno de la Patrulla;
  - el convenio colectivo de San Isidro (Ordenanza 8850);
  - qué banco paga los sueldos;
  - una convocatoria argentina que pida teléfono propio;
  - un protocolo argentino de cámaras corporales con requisitos técnicos;
  - la capacidad de la salida a internet del Municipio;
  - los planes de Claro y Personal empresas con precio visible.
- **Espectáculos:**
  - cuántas alertas emite el SMN por zona (el sitio del SMN respondió 403);
  - el pliego y el alcance de la LP 3/2026;
  - pliegos argentinos con decibeles;
  - una tasa argentina publicada de seguro técnico;
  - el precio por unidad de los GPS que compró San Isidro.
- **Escuelas:** el padrón no trae 2025 por escuela, así que se mezclan los años 2025 (públicas) y 2026 (privados).

## Preguntas abiertas (decide Nick)

1. **Teléfonos:**
   - ¿la primera etapa son Fiscalización y tránsito, o entran también Habilitaciones y los inspectores de obra?
   - ¿qué mecanismo de financiación: el banco de los sueldos, una marca o un adelanto que se recupera del sueldo?
   - ¿qué pasa con quien no tiene teléfono ni puede financiarlo? Necesita dictamen de un abogado.
   - ¿Google Cloud o una empresa europea (OVHcloud, un 15% más)? Necesita dictamen de un abogado.
2. **Escuelas:** ¿la gratuidad va por nivel, tomando el aporte vigente al inicio del año?
3. **Privados:** ¿se cobra por sesión (unos $1.000 con uso esperado) o una cuota anual?
4. **Espectáculos:**
   - ¿shows de octubre a abril o todo el año?
   - ¿cancela cualquier alerta amarilla del día o sólo la que cubre el horario del show?
   - si la nueva fecha también cae en alerta, ¿se paga otro 70%?
   - ¿subwoofer y tarima grande para todos los shows o sólo para las bandas?
   - ¿personal nuevo o agentes actuales pagados por jornada?

## Método

- **Investigadores:** cuatro, uno por tema. La parte de las escuelas la hizo el coordinador con el padrón provincial. Ninguno contactó a nadie, se registró en ningún servicio ni pagó nada.
- **Verificación en la fuente guardada:**
  - los cargos del F6 del Presupuesto 2026, sobre la imagen de las páginas 164 y 176;
  - el renglón 21 del convenio de la Ciudad (1 GB, M2M) y su precio;
  - el precio de Google Cloud en Bélgica y la guía del Home Office (350 a 500 MB por 10 minutos en HD);
  - las normales del SMN y la verificación de 1.077 alertas;
  - los precios del subwoofer y de la contratación de la Ciudad, y la página de JBL (EON ONE PRO discontinuada);
  - las compras de GPS de San Isidro ($12,06 M y $61,99 M) y las primas de seguros de 2025 ($291 M);
  - la frase de Spotify sobre la cifra pública, la quita de seguidores y popularidad de la API, y la prohibición de extraer datos.
- **Cuentas del coordinador:** en `0_cuentas/` (escuelas con aporte del 100% y teléfonos por etapa).
- **Copia de las fuentes:**
  - no se duplican los archivos que ya están en el repositorio;
  - se reemplazaron números de DNI, CUIT de personas y claves de terceros;
  - no se suben las copias de trabajo (`_tmp/`).
