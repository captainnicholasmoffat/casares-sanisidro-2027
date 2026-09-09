# 07_capitulos

**Los capítulos viven acá y sólo acá.** No hay copia en Drive.

Antes estaban en la carpeta de Drive "Proyecto San Isidro". Se movieron al repo
porque son la fuente del PDF, igual que los exhibits y los CSV: tenerlos en otro
lado significa que el armado lee de dos orígenes que se pueden desincronizar, y
ése es exactamente el error que este proyecto viene corrigiendo. Acá además
quedan con historial.

En Drive queda lo que no es entregable: contexto, hallazgos, decisiones, marco
legal, modelo.

## El marcador de corte

Cada capítulo termina con una sección de pendientes precedida por esta línea
exacta:

```
# NO VA AL PDF
```

**El script de armado corta ahí, de forma mecánica, no por criterio.** Es una
restricción, no una intención, igual que los cinco verificadores de gráficos:

```python
publicable = texto.split("# NO VA AL PDF")[0]
```

Los pendientes viven pegados al capítulo que los genera. En un archivo aparte se
leen como lista de tareas y nadie los cruza con el texto.

## Los exhibits

Cada capítulo llama sus gráficos con este formato:

```
`[EXHIBIT 07 — Qué subió y qué bajó en términos reales entre 2024 y 2025]`
```

Los veinte están llamados exactamente una vez. El armado los reemplaza por el
PNG correspondiente de `06_charts/`.

| Capítulo | Exhibits |
|---|---|
| 1 — Diagnóstico | 01, 02, 03, 04, 05, 15 |
| 2 — La gestión, medida | 06 |
| 3 — La plata | 08, 09, 10, 11, 12 |
| 4 — El mecanismo | 13, 14, 16 |
| 5 — Qué hacemos en cada área | 07, 17, 18, 19, 20 |
| 6 — Contra qué queremos que nos midan | — |

La introducción (`00_INTRODUCCION.md`) no llama ningún exhibit a propósito: plantea
la pregunta y explica cómo se contesta, no resume el documento.

## Orden de armado

```
00_INTRODUCCION.md
CAP1_DIAGNOSTICO.md
CAP2_GESTION_MEDIDA.md
CAP3_LA_PLATA.md
CAP4_MECANISMO.md
CAP5_SECTORIAL.md
CAP6_CIERRE.md
```

La introducción va sin firma en el cuerpo y cierra con una línea al pie:
*José Luis Casares, candidato a intendente de San Isidro.* El documento tiene que
sostenerse solo; la línea deja asentado quién responde por él, que es distinto de
encabezarlo. La tapa no lleva el nombre.

## El PDF

```
python3 03_scripts/armar_pdf.py
```

Produce `PROGRAMA_SAN_ISIDRO_2027.pdf`: 53 páginas, tapa · índice · introducción
· capítulos 1 a 6 · anexo.

El corte por `# NO VA AL PDF` es un `split`, y el script **relee el PDF armado y
falla** si encuentra rastro de un pendiente o del color rojo. No alcanza con
cortar bien: hay que comprobar que se cortó.

## Trabajo futuro

Esto no son limitaciones del documento: son cosas que, si aparecen, lo mejoran.
Cada una está declarada en el anexo de fuentes o en los pendientes del capítulo
que la genera.

| Qué | Qué cambiaría | Dónde toca |
|---|---|---|
| **Las tres reclasificaciones del cap 5** — Transporte, Comercio y Agua potable, con variaciones de más del 100% | Si se rastrean contra el detalle por programa, vuelven a ser comparables y el cuadro de variación real puede crecer de cuatro filas | cap 5 §5.2 |
| **El −32,5% de Promoción y asistencia social** | Hoy no se usa porque no se distingue un recorte de un desdoblamiento hacia las funciones nuevas de 2025. Si el detalle por programa muestra los mismos programas con menos plata, **vuelve probado, y vuelve más fuerte** | cap 5 §5.2 |
| **El circuito administrativo del art. 132 inc. c)** | Es el vacío más grande que queda. Los tres decretos de Pilar muestran el encuadre y el resultado, no el trámite: quién inicia el expediente, cómo se acredita la adhesión, qué dictámenes intervienen, cómo se certifica y se paga | cap 4 §4.5, anexo §3 |
| **La percepción anual de 2026** | Se publica a principios de 2027, antes de la elección. Es el dato del que depende la crítica más concreta del documento: **si 2026 cierra cerca del 93,5%, la sección 2.3 hay que reescribirla** | cap 2 §2.3 |

Las dos primeras son trabajo de un research worker sobre los estados de
ejecución por programa. La tercera, sobre el Boletín Oficial Municipal. La
cuarta es esperar y volver a mirar.
