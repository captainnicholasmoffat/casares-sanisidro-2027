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

## Un tercer dato que faltaba y ya no falta

El **EXHIBIT 13** (reparto de la partida vecinal por zona) necesitaba una regla
de reparto que no estaba en el repo. Ya está, escrita y publicada en
`03_scripts/graficos_cap4.py`, con la salida en
`data/reparto_vecinal_por_zona.csv`:

```
POOL = bienes de uso devengados 2025 x 0,50 = 28.907.854.675,13

indicadores = [pct_nbi, pct_sin_cloaca, pct_sin_gas_red, pct_hacinamiento]
para cada indicador k:  max_k = el mayor valor entre las seis zonas
need_zona = promedio( valor_zona[k] / max_k )  sobre los cuatro

peso_zona = 0,5 x (poblacion_zona / 295.978)
          + 0,5 x (need_zona / suma_need)
monto     = POOL x peso_zona
```

**Por qué se normaliza cada indicador por su propio máximo:** sin eso, "sin gas
de red" —que llega al 41,5%— aplastaría a "NBI" —que llega al 5,8%— y el índice
sería en los hechos un solo indicador disfrazado de cuatro.

**Por qué la población suma 295.978 y no 297.282:** son las personas en
viviendas **particulares**. Los 1.304 restantes viven en viviendas colectivas,
que el Censo no publica por radio y por lo tanto no se pueden asignar a ninguna
zona.

Reproduce los dos valores a etiquetar al centavo: **Beccar 136.996,14** y
**Martínez 72.446,13**.

> Antes de tener esta fórmula se había implementado una aproximación con un solo
> indicador de necesidad (cantidad de hogares con NBI). Daba la proporción
> correcta entre las zonas pero los niveles quedaban 4,8% abajo. Queda anotado
> porque explica por qué un método puede ordenar bien y aun así estar mal: el
> orden lo daba cualquiera de los dos, los niveles sólo la fórmula completa.

---

## Cómo se completan

Los dos gráficos faltantes ya están declarados en
`03_scripts/generar_todos_los_graficos.py`, en el diccionario `SIN_DATO`.
Cuando aparezca el dato:

1. Se escribe la función del exhibit en el módulo del capítulo que corresponda.
2. Se la agrega a la lista `EXHIBITS`.
3. Se la saca de `SIN_DATO`.

El orquestador los cuenta y verifica la paleta como a los demás.
