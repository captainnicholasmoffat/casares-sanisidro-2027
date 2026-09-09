# casares-sanisidro-2027

Datos, modelo fiscal y gráficos del programa de gobierno para San Isidro 2027.

## Montar el entorno

```
pip install -r requirements.txt --break-system-packages
```

Las versiones están **fijas a propósito**: matplotlib decide el ancho de cada
glifo, así que con otra versión los 20 exhibits salen distintos aunque el dato
sea el mismo, y el verificador de colisiones acusa colisiones que no existen.
Sin geopandas, `test_censo_zonas.py` no falla: no corre.

## Antes de cualquier push

Los **cinco tests** y los **cinco verificadores de gráficos** tienen que pasar.
El orden importa: `test_parser.py` reescribe los CSV desde los PDF y se lleva
puestas las columnas en pesos constantes, así que va primero y `deflactor.py`
detrás.

```
python3 03_scripts/test_parser.py
python3 03_scripts/deflactor.py
python3 03_scripts/parse_sef.py
python3 03_scripts/modelo.py
python3 03_scripts/test_deflactor.py
python3 03_scripts/test_modelo.py
python3 03_scripts/test_serie_comparable.py
python3 03_scripts/test_censo_zonas.py
python3 03_scripts/generar_todos_los_graficos.py
```

Los verificadores corren dentro del generador, que sale distinto de cero si
salta cualquiera: **paleta**, **desborde**, **colisiones**, **acentos**,
**texto tapado por el gráfico**, **texto derramado fuera de su forma**,
**geografía** y **números escritos a mano**.

El octavo —**texto derramado**— existe porque el EXHIBIT 11 salió publicado con
los rótulos de una barra apilada centrados adentro de tramos más angostos que
ellos: se derramaban sobre los tramos vecinos y ahí el texto claro caía sobre
fondo claro y el oscuro sobre fondo oscuro. Se leía "ontratos de servicio", sin
la C. Los siete anteriores dijeron OK y los siete tenían razón: colisiones mide
texto contra texto, tapado mide el punto de abajo, y desborde mide el borde del
lienzo. `test_verificadores.py` arma esa figura rota a propósito y comprueba que
el octavo la denuncia, y que se calla con la versión arreglada:

```
python3 03_scripts/test_verificadores.py
```

El año cero del modelo tiene que seguir reproduciendo la ejecución 2025 con
diferencia cero: **−6.051.064.048**.

## Armar el PDF

```
python3 03_scripts/armar_pdf.py          # -> PROGRAMA_SAN_ISIDRO_2027.pdf
python3 03_scripts/verificar_maqueta.py  # sobre el PDF ya armado
```

`armar_pdf.py` corta lo que no se publica —lo que sigue al marcador
`# NO VA AL PDF` y las notas de versión del encabezado de cada capítulo— y
vuelve a fallar si alguna de las dos cosas sobrevive al armado. **Después de
tocar la maqueta hay que MIRAR las páginas renderizadas**, no confiar en que el
CSS hizo lo que uno cree:

```
pdftoppm -png -r 80 PROGRAMA_SAN_ISIDRO_2027.pdf salida
```

## La paleta

La del informe de referencia, muestreada de su PDF pixel por pixel: son los
colores más frecuentes de sus páginas descontando los grises del antialias.
Vive en `03_scripts/estilo.py` y el CSS del armador usa los mismos seis, así que
el documento y sus veinte exhibits son una sola cosa.

| | | |
|---|---|---|
| Crema | `#F5F0E8` | el fondo de toda la página |
| Tinta | `#2A211C` | el texto, negro cálido |
| Acento | `#7C2E23` | ladrillo: eyebrow, números de sección, títulos |
| Dato | `#5E7157` | verde salvia: la serie principal |
| Arena | `#EAE0CF` | bandas de encabezado y cajas laterales |
| Filas | `#E8E4D9` | filas alternadas |
| Salvia clara | `#7E9070` | la **cuarta** serie, cuando hacen falta cuatro |

La séptima existe por una razón concreta: el exhibit 2 compara cuatro series
sobre las mismas seis categorías, y con seis colores hay tres tintas que se lean
sobre el crema. Está en las páginas de la referencia y se muestreó igual que las
otras seis. Se usa en los exhibits **2**, **4** y **10**, y en ningún otro lado.

**El acento es un rojo ladrillo.** La regla anterior del repositorio prohibía el
rojo porque en la Argentina se lee como color político. Queda sin efecto por
decisión tomada. Lo que se sigue buscando es el **rojo puro**, que nunca es una
elección de diseño sino un valor por defecto que se coló.

### La lista negra no es la paleta

`estilo.PROHIBIDOS` tiene verdes, azules y rojos —`#2ca02c`, `#1f77b4`,
`#00ff00`— que **no** son del sistema visual: son los colores por defecto de
matplotlib, escritos ahí para **buscarlos** en el SVG generado y fallar si
aparecen. Vive al lado de `verificar_paleta()` y no de la paleta, justamente
para que no se confunda. Borrarlos no saca esos colores del documento: saca el
control que los caza.

## Tipografía

**Source Serif 4**, de Frank Grießhammer para Adobe, bajo **SIL Open Font
License 1.1**. Los archivos y la licencia están versionados en `05_tipografia/`
y el CSS los carga **por ruta**, con `@font-face`, nunca por nombre de fuente
instalada en el sistema. La diferencia importa en un documento con índice: si el
armado dependiera de que la fuente esté instalada, en una máquina sin ella
WeasyPrint caería a otra, cambiaría el ancho de cada línea y el índice
imprimiría números de página que no son.

Se eligió sobre EB Garamond, Alegreya, Literata, Spectral y Vollkorn, por las
dos condiciones que importaban:

- **Color a cuerpo chico en columna angosta.** Altura de x de 0,475 em, contra
  0,400 de EB Garamond, que a 8,7 pt se ve desvaído. Y ancho de la `n` de
  0,606 em contra 0,662 de Literata: más caracteres por línea en una columna de
  85 mm, o sea menos guiones y menos ríos de blanco. La anterior, DejaVu Serif,
  medía 0,644 y es una fuente de pantalla.
- **Números para tablas.** Trae tabulares y de caja alta (`tnum` + `lnum`), que
  es lo que alinea una columna de cifras.

Además trae **versalitas dibujadas** (`smcp`), que son las de los rótulos de
exhibit, los encabezados de tabla y la cabecera de página. Simuladas por el
motor salen como mayúsculas achicadas, con el trazo más fino que el del texto de
al lado. Y tiene **eje de tamaño óptico**: el dibujo a cuerpo 9 no es el mismo
reducido, es otro, con más altura de x y más espacio entre letras.

## Reglas de datos

- **Cuando existe el conteo, se usa el conteo.** Los porcentajes son para
  mostrar, nunca para calcular otra cosa encima. Derivar de un intermedio ya
  redondeado mete error donde había un dato exacto.
- **Ningún número escrito a mano en un gráfico**, en ninguna parte: título,
  subtítulo, anotación, etiqueta o pie. Todo sale del CSV. El texto de un
  capítulo lo lee alguien; el subtítulo de un gráfico no lo vuelve a mirar
  nadie.

## Dónde está qué

| Carpeta | Qué hay |
|---|---|
| `01_raw/` | fuentes originales, sin tocar |
| `02_clean/` | fuentes parseadas |
| `03_scripts/` | parsers, modelo, gráficos, tests y verificadores |
| `data/` | series y salidas del modelo, en CSV |
| `05_tipografia/` | Source Serif 4 y su licencia OFL |
| `06_charts/` | los 20 exhibits, PNG a 300 dpi y SVG |
| `07_capitulos/` | el texto del programa, fuente del PDF |

`CORRECCIONES_NUMERICAS.md` registra cada cifra que se corrigió, con su cálculo
y su fuente.
