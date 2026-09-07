# Índice de gráficos

**Los 20 exhibits pedidos.** No falta ninguno. Cómo se cerraron los tres que
faltaban está en `06_charts/FALTAN_DATOS.md`.

Todos se regeneran de cero con:

```
python3 03_scripts/generar_todos_los_graficos.py        # los 20
python3 03_scripts/generar_todos_los_graficos.py 15     # uno solo
```

Cada uno sale en **PNG a 300 dpi y en SVG**, 1600 px de ancho, fondo PAPEL,
nunca transparente. **Ningún número está escrito a mano**: todos salen de
`data/`.

---

## Capítulo 1 — Diagnóstico

| # | Título | Datos de origen | Script |
|---|---|---|---|
| 01 | El gasto municipal real cae 34,9% entre 2017 y 2024 | `data/serie_gastos_comparable.csv` | `graficos_cap1.py` → `ex01` |
| 02 | Boulogne y Beccar concentran toda la carencia del partido | `data/zonas_indicadores.csv` | `graficos_cap1.py` → `ex02` |
| 03 | El mismo orden, dado vuelta: donde falta todo, tampoco hay título | `data/zonas_indicadores.csv` | `graficos_cap1.py` → `ex03` |
| 04 | Tigre pasa a San Isidro en 2025: el reparto provincial se dio vuelta | `data/coparticipacion_comparada.csv` | `graficos_cap1.py` → `ex04` |
| 05 | San Isidro gasta menos en sueldos y mucho más en obra que la mediana bonaerense | `data/rafam_2025_municipios.csv` (generado por `parse_rafam.py` desde `01_raw/rafam_2025_106_municipios.csv`) | `graficos_cap1.py` → `ex05` |

## Capítulo 2 — La gestión

| # | Título | Datos de origen | Script |
|---|---|---|---|
| 06 | En 2025 quedaron 35.994 millones sin cobrar de lo ya facturado | `data/ejecucion_recursos.csv` | `graficos_cap2.py` → `ex06` |
| 07 | Qué subió y qué bajó en términos reales entre 2024 y 2025 | `data/gastos_finalidad_funcion.csv`, `data/deflactor.csv` | `graficos_cap2.py` → `ex07` |

## Capítulo 3 — La plata

| # | Título | Datos de origen | Script |
|---|---|---|---|
| 08 | Sin cambios, San Isidro vuelve al azul en 2028. En el adverso, nunca | `data/modelo_flujo_caja.csv` | `graficos_cap3.py` → `ex08` |
| 09 | Pagar el programa cobrando mejor deja al Municipio mejor que no hacerlo | `data/modelo_flujo_caja.csv` | `graficos_cap3.py` → `ex09` |
| 10 | Lo que manda es cuánto crecen los recursos propios | `data/sensibilidad.csv`, `data/modelo_flujo_caja.csv` | `graficos_cap3.py` → `ex10` |
| 11 | El 73,1% del presupuesto no se puede tocar dentro del ejercicio | `data/ejecucion_gastos_objeto.csv`, `data/modelo_flujo_caja.csv`, `data/baseline_2025.csv` | `graficos_cap3.py` → `ex11` |
| 12 | El déficit de 2025 no viene del gasto corriente: viene de la obra | `data/baseline_2025.csv` | `graficos_cap3.py` → `ex12` |

## Capítulo 4 — El mecanismo

| # | Título | Datos de origen | Script |
|---|---|---|---|
| 13 | La partida vecinal reparte casi el doble por vecino en Beccar que en Martínez. Regla: mitad por población, mitad por un índice de cuatro indicadores normalizados | `data/reparto_vecinal_por_zona.csv` (generado), `data/baseline_2025.csv`, `data/zonas_indicadores.csv` | `graficos_cap4.py` → `ex13` |
| 14 | En el año 4, la mitad de la obra pública la deciden las comisiones vecinales | `data/baseline_2025.csv` | `graficos_cap4.py` → `ex14` |
| **15** | **Las seis zonas vecinales de San Isidro** | `data/zonas_propuestas_sanisidro.geojson` | `graficos_cap4.py` → `ex15` |
| 16 | La carencia no está repartida: está concentrada en nueve radios | `data/radios_censales_sanisidro.geojson`, `data/censo2022_sanisidro_por_radio.csv`, `data/zonas_asignacion_radios.csv` | `graficos_cap4.py` → `ex16` |

## Capítulo 5 — Sectorial

| # | Título | Datos de origen | Script |
|---|---|---|---|
| 17 | Ecología y agua potable juntas no llegan al 1,5% del presupuesto | `data/gastos_finalidad_funcion.csv` | `graficos_cap5.py` → `ex17` |
| 18 | Empleo y vivienda son 5 de cada 3.000 pesos que gasta el Municipio | `data/baseline_2025.csv` | `graficos_cap5.py` → `ex18` |
| 19 | Las ocho medidas de transparencia: hoy no hay ninguna cumplida | `data/transparencia_medidas.csv` | `graficos_cap5.py` → `ex19` |
| 20 | 25.166 hogares de San Isidro cocinan sin gas de red | `data/zonas_indicadores.csv` | `graficos_cap5.py` → `ex20` |

---

## El sistema visual

`03_scripts/estilo.py`. Lo importan todos y **nadie define un color a mano**.

| Token | Hex | Uso |
|---|---|---|
| PAPEL | `#FAF8F4` | fondo de todos los gráficos |
| TINTA | `#16293A` | texto, ejes, titulares |
| RIO | `#2D6E7E` | serie primaria |
| BARRANCA | `#A8763F` | serie secundaria y contraste |
| CAL | `#EDE9E2` | fondos, bandas, grillas |
| AMBAR | `#8A6A1F` | sólo advertencias y notas |

**Nada de rojo ni de verde**, y ninguna paleta por defecto de matplotlib:
`estilo.aplicar()` las desarma al importar el módulo.

`estilo.verificar_paleta()` abre cada SVG generado, lee sólo los atributos que
pintan (`fill`, `stroke`, `stop-color`) y falla si aparece un color que no
sea de la paleta, un gris de antialias o un tono de la rampa de los mapas. El
orquestador lo corre sobre los 18 y sale distinto de cero si alguno falla.

`estilo.verificar_desborde()` recorre todos los objetos de texto de la figura,
le pide a cada uno su caja al renderer ya dibujado y la compara contra el
lienzo. Si algún carácter queda afuera, el orquestador falla. Corre solo, dentro
de `guardar()`, así que no hay forma de publicar un gráfico con el título
cortado. `titular()` y `pie()` además envuelven el texto midiendo el ancho real
de la figura, no asumiéndolo.

**Acentos.** `estilo.verificar_acentos()` recorre el texto que la figura va a
**dibujar** y falla si encuentra una palabra de su lista que en español lleva
tilde escrita sin ella. Se mira lo que se dibuja y no el código fuente: un
nombre de variable sin acento no importa porque no se ve.

Encontró seis casos que una revisión del código no alcanzaba: tres armados con
`%` dentro de un `annotate()`, y tres que venían sin tilde **del propio CSV del
Municipio**. Al ampliar la lista y hacerla sensible también a la mayúscula
inicial aparecieron trece más, todos en títulos y pies escritos a mano —entre
ellos `El deficit de 2025`, `Qué subio y que bajo en terminos reales` y, en el
título del EXHIBIT 14, `En el ano 4`, que sin tilde dice otra cosa.

Las rutas y los nombres de archivo quedan afuera a propósito: el archivo se
llama `ejecucion_gastos_objeto.csv` y escribirlo con tilde en el pie de un
gráfico manda al lector a un archivo que no existe. Es la misma regla de
siempre —los identificadores en snake_case nunca llevan tilde— ahora hecha
mecánica.

**Colisiones.** `estilo.verificar_colisiones()` compara **las cajas de todos
los textos entre sí** y falla si dos se solapan más del 10% del más chico. El
verificador de desborde controlaba el borde del lienzo pero no que dos textos
se pisaran entre ellos.

Encontró colisiones en **9 de los 18** gráficos, y la causa de fondo era una
sola: `subplots_adjust` coloca la caja de los ejes, pero los números del eje y
los rótulos cuelgan **afuera** de esa caja. Se cambió por
`tight_layout(rect=...)`, que encaja los ejes **con** sus decoraciones, y
`marco()` pasó a **medir** cada bloque de la cabecera en vez de apoyarlo en una
altura fija. Lo que quedó después se arregló uno por uno.

Dos detalles que costaron encontrar y que valen para cualquier gráfico nuevo:

- La caja de una `Annotation` incluye **la flecha**, no sólo el texto. Una
  etiqueta con línea guía larga reportaba una caja del tamaño de media figura y
  el verificador la acusaba de pisar todo lo que la línea cruzaba.
  `estilo.caja_de_texto()` mide sólo lo escrito.
- Una `Annotation` no sabe dónde cae su texto hasta que se le actualizan las
  posiciones. Medirla antes devuelve la caja apoyada en el destino de la flecha
  y no en el del texto, así que el colocador de etiquetas de los mapas daba por
  buenas posiciones que después se pisaban.

En los dos mapas los nombres de zona se colocan **midiendo**: de mayor a menor
área, cada etiqueta se prueba en su lugar y, si choca, en ocho direcciones a
cuatro distancias, y la que se mueve se lleva una línea guía. Si después de las
32 pruebas no hay lugar, se dibuja igual: un nombre de zona que falta es peor
que un nombre de zona apretado, y el verificador lo denuncia.

Los datos nunca se tocan. Lo que la fuente escribe sin tilde se corrige **al
mostrarlo**, con dos tablas de nombres: `estilo.zona_bonita()` para las zonas
(`Martinez` → `Martínez`) y `estilo.nombre_funcion()` para las funciones
(`CONTROL DE LA GESTION PUBLICA` → `Control de la gestión pública`). Cambiar el
CSV rompería las claves y además falsearía la fuente.

El EXHIBIT 19 usa la misma técnica sobre un CSV que escribimos nosotros:
`data/transparencia_medidas.csv` va en ASCII y `estilo.nombre_medida()`,
`nombre_estado()` y `nombre_evidencia()` le ponen las tildes al dibujarlo. Si
una clave del CSV no está en esas tablas se devuelve tal cual y el verificador
de acentos la denuncia, así que no hay forma de que un texto sin tilde pase sin
que alguien se entere.

Cada script lleva `# -*- coding: utf-8 -*-`.

**Números a la castellana** con `numero()`, `pct()` y `millones()`: miles
con punto y decimales con coma. 324.304 y 89,32%. Nunca a mano.
