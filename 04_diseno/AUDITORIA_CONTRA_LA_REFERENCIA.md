# Auditoría contra la referencia — extracción forense completa

Sacada con `04_diseno/medir/forense.py`, que vuelca **todas** las combinaciones
de (familia, cuerpo, color) y **todos** los rectángulos de un PDF. Existe
porque mirar un PDF y anotar lo que llama la atención deja afuera la mitad, y
uno no sabe cuál mitad: cada vez que se corrigió una pieza contra la
referencia apareció otra que nunca se había medido.

## 1. Los colores que su documento usa de verdad

| color | qué hace | ¿está en nuestra paleta? |
|---|---|---|
| `#2a211c` | el cuerpo | sí, tinta |
| `#6e625a` | fuentes, notas, pies | sí, tinta diluida |
| `#7c2e23` | títulos, cifras, primera columna | sí, ladrillo |
| `#5f7057` | bajadas, conceptos, columna destacada | sí, salvia |
| `#7e9070` | cuarta serie | sí, salvia clara |
| **`#b4863a`** | **cornisas, cintillos, micro-etiquetas** | **NO** |
| **`#db6b4b`** | **números de sección, cifras negativas** | **NO** (y es un rojo) |
| `#9b9088` / `#9a8c7e` | rótulos secundarios de gráfico | no, pero son tinta aguada |
| `#fcfaf6` | texto sobre banda oscura | no, pero es papel |

**Su riqueza visual se apoya en seis acentos; nuestra paleta da tres.** El
ocre `#b4863a` es el que lleva todas sus etiquetas y cintillos —1.833 glifos—
y no es un rojo: es un oro apagado.

## 2. Lo que sus tablas hacen y las nuestras no

Sobre las treinta páginas:

```
banda #eae0cf 17,2 pt          x51     cabecera
banda #eae0cf 16,5 / 18,0 pt   x25     cabecera
banda del color de fila                 CERO
filete 0,75 pt #282216         x364    UN PELO OSCURO BAJO CADA CELDA
```

**No tienen filas alternadas. Ninguna.** Lo que separa una fila de la
siguiente es un pelo casi negro de 0,75 pt dibujado celda por celda. Las filas
alternadas eran un invento nuestro, y encima con un filete pálido que no
separa: por eso sus tablas se leen nítidas y las nuestras lavadas.

## 3. Dispositivos suyos que no existen en nuestro documento

```
banda  82,5 pt #fbf6ec   x38                   FICHA, mas clara que el papel
banda 147,7 pt #282216   x26                   marco de foto dentro de esas fichas
banda  21,7 / 31,5 / 42 pt #66734c x29         barras oliva
filete 0,75 pt #d9cdba   x196                  filete tostado
punto de guia 0,45 pt #db6b4b x127             guias punteadas de grafico
```

**CORRECCION.** La primera version de esta auditoria decia que la referencia
tiene un *panel oscuro de media pagina, trece veces en el documento*. Es
falso, y el error es el mismo que esta auditoria existe para evitar: se leyo
el censo de rectangulos y se describio una pieza sin abrir la pagina.

Los 26 rectangulos `#282216` de 147 pt estan **todos en la pagina 11**, y son
los marcos de foto de una **grilla de fichas de producto**: cuatro columnas,
fondo `#fbf6ec` mas claro que el papel, foto arriba, titulo en ladrillo,
descripcion en tinta y URL en salvia al pie. Las fotos los tapan. El unico
otro es el marco de un grafico de posicionamiento en la pagina 17.

No hay nada que incorporar ahi: es un catalogo de equipamiento y este
documento no tiene catalogo.

## 4. Su escala tipográfica tiene el doble de escalones

4,2 · 4,5 · 4,6 · 4,8 · 4,9 · 5,2 · 5,5 · 5,6 · 5,7 · 6,0 · 6,4 · 6,6 · 6,7 ·
7,0 · 7,1 · 7,4 · 7,5 · 7,6 · 7,9 · 8,2 · 8,3 · 8,4 · 8,6 · 9,0 · 9,4 · 9,7 ·
10,0 · 10,3 · 10,5 · 10,9 · 11,0 · 11,2 · 14,7 · 16,5 · 19,0

La nuestra tiene diez. La suya baja hasta 4,2 pt para micro-etiquetas dentro
de los gráficos y sube a 19 para una cifra sola.

## 5. El interletrado de sus etiquetas llega mucho más lejos

De 0,5 pt en una cabecera de tabla a **2,89 pt** en una etiqueta de apertura,
pasando por 1,25 en la cornisa y 0,84 en las etiquetas del anexo. El nuestro
va de 0,5 a 0,75.
