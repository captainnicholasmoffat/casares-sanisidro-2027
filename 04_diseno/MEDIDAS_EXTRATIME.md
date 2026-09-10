# MEDIDAS DE LA REFERENCIA — Extra Time / Investor Report

Medido, no estimado. Fuente: `Extra_Time___Investor_Report_Final_3.pdf`, 30 páginas.
Herramientas: `pdfplumber` para tipografía y geometría, `pdftoppm` a 100 dpi + PIL
para colores de fondo y proporciones. El CSS del armador se construye contra estos
números; si alguno cambia, se cambia acá primero y después en el CSS.

Los scripts de medición están en `04_diseno/medir/`.

---

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

## 6. FILETES Y CAJAS

- **Todos los filetes del documento miden 0,75 pt.** 567 de 570 rectángulos finos
  medidos dan exactamente ese grosor. No hay filetes gruesos.
- Caja destacada: fondo `#EFE7DA`, filete vertical izquierdo en verde, cintillo
  en Inter versalita espaciada arriba, cuerpo Spectral 9,7.

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

