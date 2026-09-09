# 08_imagenes — las ilustraciones generadas

Acá van las imágenes generadas que el armador coloca. **No las genera este
repositorio**: llegan como archivos y `03_scripts/armar_pdf.py` sólo las
coloca. Si un archivo no está, el documento se arma igual —la tapa vuelve al
mapa de zonas y el capítulo abre sin banda—, así que un hueco vacío nunca
rompe el build.

## Qué hace falta, y con qué medida

| Archivo | Píxeles | Proporción | Dónde va |
|---|---|---|---|
| `tapa.png` | 2480 × 3508 | vertical 1 : 1,414 (A4) | sangra la página entera de tapa, con el título encima |
| `apertura_cap1.png` … `apertura_cap6.png` | 2100 × 700 | apaisada 3 : 1 | banda al ancho de la caja de texto, arriba del título de capítulo |

Todas a 300 dpi, en PNG.

La tapa sangra los cuatro lados y se recorta al centro, así que lo que importa
tiene que estar en el centro y **la mitad de arriba tiene que quedar tranquila**:
ahí van el título y la bajada, en Tinta sobre la imagen.

## Las dos reglas que no se negocian

**Abstractas o conceptuales.** Ninguna imagen puede parecer una fotografía de un
lugar o de una persona de San Isidro. Si alguien descubriera que una imagen de
La Cava o de Béccar es sintética, el documento pierde lo único que tiene, que es
que se le pueden revisar las cuentas. Nada de calles reconocibles, fachadas,
carteles, caras ni multitudes.

**Cada una lleva su línea al pie.** El armador la pone solo, y dice:
*Ilustración generada. No es una fotografía de San Isidro ni de ninguno de sus
barrios.*

## La paleta

La misma del documento, y nada más:

| | |
|---|---|
| Crema | `#F5F0E8` |
| Tinta | `#2A211C` |
| Acento | `#7C2E23` |
| Dato | `#5E7157` |
| Arena | `#EAE0CF` |
| Filas | `#E8E4D9` |
