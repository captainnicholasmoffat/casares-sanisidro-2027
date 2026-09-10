# MEDIDAS DE LA REFERENCIA — Extra Time / Investor Report

Medido, no estimado. Fuente: `Extra_Time___Investor_Report_Final_3.pdf`, 30 páginas.
Herramientas: `pdfplumber` para tipografía y geometría, `pdftoppm` a 100 dpi + PIL
para colores de fondo y proporciones. El CSS del armador se construye contra estos
números; si alguno cambia, se cambia acá primero y después en el CSS.

Los scripts de medición están en `04_diseno/medir/`.

---

## 0. LA ESCALA — todo se multiplica por 210/232,8

Su página mide **660 pt de ancho = 232,8 mm**; la nuestra, 210. Copiar sus
cuerpos tal cual en una página un 10 % más angosta **agranda la letra**: el
mismo 9,7 pt en una columna de 86 mm en vez de una de 96 da menos caracteres
por línea, o sea una mancha más gruesa y menos densa.

Así que **cada número de este archivo se multiplica por 0,9021** antes de
llegar al CSS. Márgenes, medianil, cuerpos, interlíneas, filetes, bandas de
tabla, sangrías y separaciones. La página resultante es la de ellos reducida
al 90,2 %: misma cantidad de caracteres por línea, mismo gris de la mancha,
misma proporción entre cada pieza y la de al lado. Está implementado en
`03_scripts/armar_pdf.py` como `ESCALA`, `e()` y `emm()` sobre el diccionario
`REF`: no hay ni un número elegido a ojo.

**Lo mismo vale para los gráficos.** Se dibujaban en 5,33 pulgadas y la página
los estiraba hasta los 181,4 mm de la caja de texto: un factor de 1,34 que
agrandaba cada rótulo. Un "7,5 pt" pedido en el código salía impreso a 10. Se
dibujan al ancho de la caja, así que un punto pedido es un punto impreso.

## 1. PÁGINA

| qué | pt | mm |
|---|---|---|
| ancho | 660 | 232,8 |
| alto | variable (872 a 2685) | — |
| margen izquierdo | 45 | 15,9 |
| margen derecho | 45 | 15,9 |
| margen superior (al ojo de la cornisa) | 40 | 14,1 |
| caja de texto | 570 | 201,3 |
| pie (línea de pie a 1051 en una página de 1090) | ~39 al borde | ~13,8 |

El alto es variable porque el original es una exportación continua de Figma:
no es una página de imprenta, es un lienzo por capítulo. **Eso no se copia.**
Nosotros paginamos A4 (210 × 297 mm) y adaptamos los márgenes a esa proporción.

**Márgenes proporcionales:** 15,9 / 232,8 = **6,8 % del ancho**. En A4 eso da
**14,3 mm**. Se usa 16 mm izquierda y derecha por ser papel real y no pantalla.

## 2. COLUMNAS

| qué | pt | mm |
|---|---|---|
| columna | 271 | 95,6 |
| medianil | 24 | 8,5 |
| columna derecha | 275 | 97,0 |

Medido sobre el hueco real de la banda a dos columnas de la página 8:
tinta de 44,6 a 606,7 pt con un único hueco de **316 a 340 pt = 23,8 pt**.

**Medianil proporcional:** 24 / 570 = **4,2 % de la caja**. En A4 con caja de
178 mm eso da **7,5 mm**, columnas de **85,2 mm**.

## 3. TIPOGRAFÍAS

**Spectral** (serif, Production Type, OFL) y **Inter** (sans, Rasmus Andersson, OFL).
Cortes presentes en el PDF: Spectral Regular, Italic, MediumItalic, SemiBold, Bold;
Inter Regular.

> El documento nuestro tiene vendorizada **Source Serif 4**, no Spectral.

| pieza | familia y corte | cuerpo pt | interlínea pt | color |
|---|---|---|---|---|
| cornisa (running head) | Inter Regular, versalita espaciada | 6,7 | — | ocre `#B48639` |
| número de capítulo | Spectral Bold | 16,5 | — | acento `#7C2E23` |
| título de capítulo | Spectral Bold | 16,5 | 22 | tinta `#2A211C` |
| bajada del capítulo | Spectral MediumItalic | 10,9 | 15,0 | dato `#5F7057` |
| entrada a todo el ancho | Spectral Regular | 10,0 | 16,0 | tinta |
| cuerpo a dos columnas | Spectral Regular | 9,7 | 14,5 (×1,50) | tinta |
| rótulo del exhibit | Inter Regular, versalita espaciada | 6,7 | — | ocre `#B48639` |
| título del exhibit | Spectral SemiBold | 11,2 | 15 | acento `#7C2E23` |
| cabecera de tabla | Inter Regular, versalita espaciada | 6,4 | — | acento `#7C2E23` |
| cuerpo de tabla | Inter Regular | 7,9 | 12 | tinta |
| primera columna de tabla | Inter Regular | 7,9 | 12 | acento `#7C2E23` |
| columna destacada de tabla | Inter Regular | 7,9 | 12 | dato `#5F7057` |
| fuente / pie de exhibit | Spectral SemiBold + Spectral Italic | 7,9 | 12 | gris cálido `#6E625A` |
| nota de lectura | Spectral SemiBold + Spectral Italic | 7,9 | 11,5 | gris cálido `#6E625A` |
| rótulo dentro del gráfico | Inter Regular | 7,9 | — | tinta o crema |
| pie de página | Inter Regular | 6,4 | — | gris cálido `#6E625A` |

Cuerpo 9,7 pt sobre 570 pt de caja son **~95 caracteres por línea a todo el ancho**
y **~45 por columna**. Es una medida de lectura, no de folleto.

## 4. RITMO VERTICAL

Medido de línea a línea sobre la página 5.

| de → a | pt | mm |
|---|---|---|
| cornisa → título de capítulo | 37 | 13,1 |
| título → bajada | 25 | 8,8 |
| bajada → entrada | 25 | 8,8 |
| entrada → rótulo de exhibit | 22 | 7,8 |
| rótulo → título del exhibit | 14 | 4,9 |
| título del exhibit → tabla | 21 | 7,4 |
| última fila → fuente | 25 | 8,8 |
| fuente → cuerpo | 22 | 7,8 |
| cuerpo → siguiente exhibit | 22 | 7,8 |
| nota de lectura → pie | 47 | 16,6 |

**Ojo: esto NO es el margen de CSS.** Las distancias están medidas de alto de
línea a alto de línea, y adentro de los 22 pt entre bloque y bloque está el alto
de la línea del bloque de arriba. El margen es la diferencia:

| de → a | medido | alto de línea | **margen real** |
|---|---|---|---|
| bloque → bloque | 22 pt | 14,5 pt | **2,6 mm** |
| rótulo → título del exhibit | 14 pt | 8,7 pt | **1,9 mm** |
| título del exhibit → figura | 21 pt | 14,6 pt | **2,3 mm** |
| última fila → fuente | 25 pt | 20,2 pt | **1,7 mm** |
| fuente → cuerpo | 22 pt | 11,5 pt | **3,7 mm** |
| título de capítulo → bajada | 25 pt | 19,5 pt | **1,9 mm** |
| bajada → entrada | 25 pt | 15,0 pt | **3,5 mm** |

Puestos los 22 pt directamente como margen, el documento lleva **tres veces** el
aire de la referencia, y las páginas terminan a media altura.

## 5. TABLAS

| qué | valor |
|---|---|
| banda de cabecera | `#EAE0CF` (arena), alto **17,3 pt** |
| fila alterna | `#E8E4D9` (filas), alto **20,2 pt** |
| fila impar | crema, sin banda |
| sangría de celda | 6 pt desde el borde de la banda (x=51 con banda desde x=45) |
| ancho | siempre a los 570 pt completos, nunca a una columna |
| filete | 0,75 pt |

## 6. FILETES Y LA CAJA

- **Todos los filetes del documento miden 0,75 pt.** 567 de 570 rectángulos finos
  medidos dan exactamente ese grosor. El **único trazo grueso de todo el
  documento** es el que lleva la caja al costado, y mide 3 pt.

### La caja, medida píxel por píxel sobre la página 8

| qué | valor |
|---|---|
| fondo | `#EFE7DA` — un tercer tan, ni arena ni fila |
| filete izquierdo | **3,0 pt** en salvia `#5F7057` |
| cintillo | Inter 6,4 pt mayúscula, tracking 0,55 pt, **en salvia** — no en ladrillo |
| cuerpo | Spectral Regular **9,0 pt** / 13,0 — *menos* que el cuerpo de la página |
| sangría | 12,4 pt desde el borde de la caja |
| aire arriba y abajo | 12 pt |
| ancho | **toda la caja de texto**, nunca dentro de una columna |

Es la pieza que más la distingue y la que faltaba: metida adentro de una
columna de 86 mm no es esta pieza, es otra.

## 7. PALETA MEDIDA — proporción real de píxeles sobre las 30 páginas

| color | hex | % del total |
|---|---|---|
| crema | `#F5F0E8` | 78,41 |
| tan de caja | `#EFE7DA` | 4,74 |
| arena | `#EAE0CF` | 0,81 |
| filas | `#E8E4D9` | 0,57 |
| acento (ladrillo) | `#7C2E23` | 0,46 |
| oliva de gráfico | `#66734C` | 0,43 |
| tinta | `#2A211C` | 0,19 |
| coral de gráfico | `#DB6B4B` | 0,17 |
| dato (salvia) | `#5F7057` | 0,15 |
| salvia clara | `#7E9070` | 0,12 |

La paleta que fijó Nick es exactamente ésta menos el coral (rojo, prohibido) y
el oliva. El tan de caja `#EFE7DA` y el ocre de cornisa `#B48639` son dos colores
que la referencia usa y la paleta fijada no tiene.

## 8. DENSIDAD DE COLOR POR PÁGINA — el umbral del décimo verificador

Muestreo a 100 dpi, tolerancia de suma de canales < 60 para color y < 20 para fondo.

| medida | media | mínimo | máximo |
|---|---|---|---|
| color (acento + dato + salvia) | **4,00 %** | **0,68 %** | 13,91 % |
| fondo crema | **80,9 %** | 59,3 % | **96,8 %** |

Ninguna página de la referencia es sólo tipografía negra sobre crema.
La página más pobre en color tiene 0,68 %; la más rica, 13,91 %.

---

# LAS REGLAS DE COMPOSICIÓN

Medidas sobre las páginas 5, 8, 11 y 13 clasificando **cada línea** por dónde
cae respecto del medianil. No son opiniones sobre el diseño: son lo que hace
la referencia, contado.

## 1. La anatomía de una sección, en orden

```
cornisa                       Inter mayúscula espaciada, arriba a la izquierda
título                        número + nombre, A TODO EL ANCHO
bajada                        Spectral MediumItalic, A TODO EL ANCHO, 2 a 6 líneas
entrada                       Spectral 10 pt, A TODO EL ANCHO, 2 a 5 líneas
exhibit / tabla + fuente      A TODO EL ANCHO
prosa                         A DOS COLUMNAS
caja                          al ancho, o en UNA columna con la prosa al lado
exhibit / tabla + fuente      A TODO EL ANCHO
nota de lectura               A TODO EL ANCHO
```

## 2. Cuándo algo cruza las dos columnas

**Sólo si hay al menos cuatro líneas para llenarlo.** Una línea sola cruzando
los 181 mm, con la columna de al lado vacía debajo, no se lee como una entrada:
se lee como un error de armado.

A cuerpo 8,75 en una caja de 181,4 mm entran **130 caracteres por línea**, así
que hacen falta **520**. Si el primer párrafo no llega solo, se le suman los que
siguen —hasta tres— y se decide sobre el total: la entrada es una *región* de
lectura, no necesariamente un párrafo. Si ni así llega, **no hay entrada** y la
sección arranca directamente a dos columnas.

Los exhibits, las tablas, los listados, las fuentes y las notas cruzan siempre,
sin importar su largo: no son prosa, son piezas.

## 3. La caja tiene dos posiciones y el contexto decide

| dónde estaba | qué la rodea | cómo va |
|---|---|---|
| su página 8 | entre dos exhibits | **a todo el ancho** |
| su página 13 | entre prosa corriente | **en una columna**, con la prosa al lado |

Una caja que interrumpe prosa se pone al costado y deja seguir leyendo; una que
separa dos piezas anchas se pone al ancho.

## 4. Cómo se introduce una sección

Sus 25 secciones se introducen igual, sin una sola excepción:

```
3 Why the category's economics break
```

**Número solo, y el título en minúscula.** Nunca escriben la palabra
"chapter", nunca usan raya, nunca van en mayúsculas. El número en ladrillo, el
nombre en tinta.

## 5. El color entra por el texto

Las negritas del cuerpo no son negras. **Las cifras van en ladrillo y los
conceptos en salvia**: dos acentos corriendo por la prosa, no uno. Es de donde
sale el color de las páginas que no tienen ni tabla ni gráfico.

## 6. Lo que la referencia NO hace

- No pone un filete arriba de cada subtítulo.
- No usa versalitas en ninguna parte: lo que parecen versalitas es Inter en
  mayúsculas espaciadas.
- No tiene filetes gruesos, salvo uno: los 3 pt al costado de la caja.
- No deja una página que sea sólo tipografía negra sobre crema.
