# Mapa, cifras por zona y fotos para la web: cómo se armaron

Base: el programa final, commit `c462fcf`. Los PDF de `v21` son idénticos a los de `salida/` en ese commit (mismo hash).

## Qué hay

- `data/zonas.geojson` (22 KB): las seis localidades, el contorno del partido y la costa. Hay ocho elementos, y cada uno trae `tipo` (`localidad`, `partido` o `costa`), `id` y `nombre`.
- `data/zonas_datos.json` (53 KB): las cifras por zona del programa. Cada cifra trae `valor`, `como_figura` (el texto exacto del programa) y `fuente` (apartado y cuadro o gráfico). Los `id` son los mismos que en el geojson.
- `img/`: 27 fotos en WebP, cada una en dos tamaños (54 archivos), y `fotos.json`.

## Cómo se armaron las zonas

- Los radios salen del shapefile del Censo 2022 que está en el repo (`01_raw/censo2022/radios-censales-2022-shp.zip`), en WGS84. Los 360 radios de San Isidro son idénticos a `data/radios_censales_sanisidro.geojson`, que es el archivo que usó el documento. La diferencia de área es cero.
- El criterio es el mismo que usa el programa final. Cada radio va a la localidad de OpenStreetMap que contiene su punto representativo (nota del Gráfico 1 y Nota de método).
- Ese criterio no es el de `03_scripts/zonas.py` (semillas y crecimiento por población). El documento lo dejó de usar el 19/09, según `data/METODOLOGIA_ZONAS.md`.
- La asignación de cada radio está en `data/zonas_asignacion_radios.csv` (c462fcf). La usé tal cual: no la recalculé ni bajé nada de internet.
- `doc/charts.py` dibuja el Gráfico 1 con `data/zonas_propuestas_sanisidro.geojson`, que es la unión de esos mismos radios.
- Radios por zona: Boulogne Sur Mer 79, Béccar 73, Villa Adelina 42, San Isidro 67, Martínez 83 y Acassuso 16.
- Uní los radios de cada localidad. Quedan seis polígonos de una sola pieza, sin agujeros, iguales a `zonas_propuestas_sanisidro.geojson` (diferencia cero).
- Simplificación: cada borde que comparten dos localidades se simplificó una sola vez, con una tolerancia de 1 metro. Así, dos vecinas usan exactamente la misma línea y no quedan huecos ni solapes. Los vértices pasan de 1.481 a 544, y las coordenadas llevan 6 decimales.
- El contorno del partido es la unión de las seis localidades.
- La costa es el tramo del borde del partido que no toca ningún radio de los partidos vecinos. Mide 6,8 km, desde el límite con San Fernando (-58,5168 / -34,4470) hasta el de Vicente López (-58,4803 / -34,4900). Es el borde de los radios del censo, no una costa medida en el terreno.
- El `zonas.geojson` del intento anterior estaba bien. Lo volví a generar con el mismo script y salió idéntico, byte por byte.

## Controles

Todos dieron bien.

Forma:
- Lo más que se aleja el borde simplificado del original es 1,03 m.
- El área de cada zona cambia, como mucho, un 0,012%.
- No quedan huecos ni solapes entre localidades (0 m²).
- El punto representativo de cada uno de los 360 radios sigue dentro de su zona.
- Los polígonos son válidos y van en sentido antihorario, como pide el estándar GeoJSON.
- El archivo pesa 22.346 bytes, menos que el límite de 150 KB.

Cifras: 165 controles, que comparan los datos del censo por radio, sumados con la asignación del programa, contra el programa final:
- La población de las seis zonas suma 295.978, como dice el programa. Con las 1.304 personas de viviendas colectivas da 297.282. Los hogares del partido son 110.559.
- Los porcentajes de NBI, sin cloaca, sin gas de red y con hacinamiento de cada zona coinciden con el Gráfico 2. El NBI del partido es 3,16%.
- Los hogares con cada carencia, sus partes del total y el índice de necesidad coinciden con el Cuadro 22, fila por fila contra el texto.
- Rehice el reparto del año 4 con la fórmula del programa (mitad por población y mitad por el índice, sobre 28.907.854.675,13 pesos). Coincide con el Gráfico 23, en el monto y por habitante.
- Los lugares de formación salen del índice, con los restos mayores: 315, 307, 98, 96, 94 y 18. Suman 928.
- Chicos y personas mayores (5.13), Boulogne y Béccar juntas (1.1), la fracción 32 (9 radios y 8.749 habitantes, todos en Béccar), los radios que nombran las notas y los 16 radios de Acassuso: todo coincide.
- El Cuadro 17 y los cambios de la tasa por localidad (3.5) coinciden con los datos de valuación del repo.
- Las cifras de los Gráficos 2, 3 y 23 coinciden con `doc/charts.py`, en el mismo orden de zonas.

Además, cada `como_figura` se buscó en el texto del PDF de pantalla final o en el HTML del programa. Si faltaba uno solo, el script no escribía el archivo.

## Fotos

- En `assets/doc` hay 29 fotos. 25 están en el programa final, y lo comprobé comparando cada archivo, byte por byte, con las imágenes del PDF de pantalla y del A4.
- Quedaron afuera `f_plaza` («Plaza de barrio, un sábado») y `f_mesa` («Trabajo sobre el mapa del partido»).
- En c462fcf esas dos ya no figuran en `doc/content*.py`, así que el commit no dice qué archivo era cada una. Lo confirmé con un PDF anterior (`/home/claude/PROGRAMA_SAN_ISIDRO_2027_final46.pdf`). La imagen de la página que dice «Plaza de barrio, un sábado» es idéntica byte por byte a `f_plaza.jpg`. La de «Trabajo sobre el mapa del partido» es idéntica a `f_mesa.jpg`.
- `f_estacion` y `f_feria` están en el repo pero no en el programa final. Las convertí igual y van con `"en_programa": false` y sin epígrafe.
- Los epígrafes salen del HTML del programa y se comprobaron contra el PDF. `fotos.json` trae también el apartado, el subtítulo, la página del PDF de pantalla y la foto con la que hace par, si la hay.
- Tamaños: los originales tienen 1.493 px de ancho. Por eso la versión de 1600 px es una ampliación leve, del 7%, que no agrega detalle. Si no quieren ampliar, se rehace a 1.493 px con el mismo nombre.

## Problemas y avisos

- El programa no da el reparto del año 1 por zona. Sólo da el total del año 1, 7.227 M y 24.310 $ por habitante (Cuadro 21), y el reparto por zona del año 4 (Gráfico 23). No lo calculé. Si la web lo necesita, sería una cifra nueva y hay que aprobarla.
- El programa no da el total de hogares por zona. Da los hogares con cada carencia, el total del partido y el de Boulogne y Béccar juntas.
- El programa no da el promedio de San Isidro sin cloaca, sin gas, con hacinamiento ni con universidad. Sólo da el de NBI, 3,16%.
- Universidad (Gráfico 3): Béccar figura con 12,8% y San Isidro con 25,2%. El censo da 12,853% y 25,251%, que a un decimal serían 12,9% y 25,3%. La diferencia es porque el gráfico redondea dos veces. Dejé las cifras del programa, con una nota.
- Acassuso: la nota del Cuadro 17 dice «en vez de 2,94», pero el cuadro da 2,80× para la valuación provincial. No coinciden. Va copiado tal cual en `comparaciones`, con un aviso.
- Edades: para Béccar el 5.13 dice «menos de 14 años», pero el dato es de 0 a 14 años. El mismo apartado lo llama «hasta los 14 años».
- Los 1.810 chicos en hogares con NBI, y el 76% en Boulogne y Béccar, no se pueden comprobar con los datos por radio del repo. Van copiados del texto.
- El programa sólo da los dos porcentajes más altos de chicos (Béccar y Boulogne) y de personas mayores (Acassuso y Martínez). Las demás zonas no tienen ese dato.
- Los límites de las localidades no son oficiales: son de OpenStreetMap, aplicados a los radios del censo. La web tiene que decirlo, como lo dice el programa.
- En `img/` hay una carpeta `scrub/`, y en `web/` hay un `index.html`, que no armé yo. No los toqué.

Scripts, en la carpeta de trabajo `geo/work/`: `armar_zonas.py`, `build_datos.py`, `controles_web.py` y `build_fotos.py`.
