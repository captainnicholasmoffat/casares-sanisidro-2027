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

## Falta

- El anexo de fuentes, generado desde lo que efectivamente se cite.
- El armado del PDF, con la paleta de `07_IDENTIDAD_DEL_DOCUMENTO.md` (Drive).
