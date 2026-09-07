# Gráficos que no se hicieron, y por qué

Dos de los veinte exhibits pedidos **no se generaron**. Ninguno se rellenó con
números aproximados ni con una fuente distinta de la que pedía: si el dato no
está, el gráfico no existe.

Fecha: **2026-09-07**.

---

## EXHIBIT 05 — San Isidro contra la mediana provincial

**Pedido:** % personal y % obra pública de San Isidro contra los 106 municipios
de la Provincia, con el resto de fondo en gris CAL.

**Falta:** la ejecución presupuestaria de los otros 134 municipios.

El repo tiene **transferencias** por municipio —los 13 XLSX de la Provincia, que
sí traen los 135— pero eso es lo que la Provincia les **manda**, no lo que cada
municipio **gasta**. Con transferencias no se puede calcular ni el % de personal
ni el % de obra pública de nadie.

**Qué se necesitaría:** el Registro Único de Municipios (RUM) o los estados de
ejecución presupuestaria municipal que publica el Ministerio de Hacienda de la
Provincia, con apertura por objeto del gasto para todos los partidos. No están
en `01_raw/`.

**Qué se pierde:** el argumento comparativo. Hoy podemos decir cuánto gasta San
Isidro en personal (34,4%) y en obra pública (17,8%), pero **no** si eso es mucho
o poco contra sus pares.

**Lo que sí se puede afirmar mientras tanto**, con lo que hay: la posición de San
Isidro en el reparto de transferencias contra Tigre, Vicente López y San
Fernando. Está en el **EXHIBIT 04**.

---

## EXHIBIT 19 — Las ocho medidas de transparencia

**Pedido:** las ocho medidas de transparencia, cumplidas contra pendientes.

**Falta:** el listado de las ocho medidas y el estado de cada una. **No existe
ningún archivo en el repo con ese dato.**

Esto no es un dato público que haya que ir a buscar a un organismo: es una
definición del propio programa de gobierno. Las ocho medidas hay que
**escribirlas**, no parsearlas.

**Qué se necesitaría:** un CSV con una fila por medida —nombre, estado
(cumplida / pendiente / parcial), evidencia y fecha—. Con ese archivo el gráfico
sale en minutos y se agrega al orquestador sin tocar nada más.

Sugerencia de estructura, para que quede reproducible como todo lo demás:

```
data/medidas_transparencia.csv
  medida, descripcion, estado, evidencia, fecha_verificacion, fuente
```

---

## Un tercer dato que sí se resolvió, pero conviene saber cómo

El **EXHIBIT 13** (reparto de la partida vecinal por zona) necesitaba una regla
de reparto que **tampoco estaba en el repo**. No se inventó un número: se
implementó una regla escrita y publicada, mitad por población y mitad por
hogares con NBI, en `03_scripts/graficos_cap4.py` y con la salida en
`data/reparto_vecinal_por_zona.csv`.

Esa regla reproduce **exactamente la proporción** entre Beccar y Martínez que se
pidió etiquetar (1,891 contra 1,891), pero los niveles quedan **4,8% por debajo**:

| Zona | Calculado | Pedido | Diferencia |
|---|---:|---:|---:|
| Beccar | 130.785 | 136.996 | −4,5% |
| Martínez | 69.097 | 72.446 | −4,6% |

Las dos diferencias son del mismo signo y casi del mismo tamaño, así que la
regla de reparto es la misma y lo que cambia es **la base**: el monto total a
repartir, o la población usada. El gráfico publica los números que dan los datos
del repo. **Si la base correcta es otra, hay que decir cuál y el gráfico se
regenera solo.**

---

## Cómo se completan

Los dos gráficos faltantes ya están declarados en
`03_scripts/generar_todos_los_graficos.py`, en el diccionario `SIN_DATO`.
Cuando aparezca el dato:

1. Se escribe la función del exhibit en el módulo del capítulo que corresponda.
2. Se la agrega a la lista `EXHIBITS`.
3. Se la saca de `SIN_DATO`.

El orquestador los cuenta y verifica la paleta como a los demás.
