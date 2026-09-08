# Correcciones numéricas — ocho cifras que se contradecían entre capítulos

No se editó ningún capítulo. Este archivo devuelve, para cada cifra, **el valor
correcto, el archivo fuente, la cuenta y en qué capítulos hay que cambiarla.**

Todo se recalcula con `03_scripts/correcciones_numericas.py`, que lee `data/` y
no escribe nada. Ningún número de este archivo está escrito a mano:

```
python3 03_scripts/correcciones_numericas.py
```

Fecha: **2026-09-08**. El punto 8 se agregó el mismo día. Los importes van en millones de pesos **nominales de
2025**, salvo donde diga otra cosa.

---

## Tabla resumen

| # | Concepto | Valor correcto | Qué circulaba | Capítulos a corregir |
|---|---|---:|---|---|
| 1 | Percepción de recursos corrientes 2025 | **89,32%** (337.148,8 dev / 301.154,7 perc) | la base B, que suma recursos de capital | 2, 3 |
| 2 | Volver a cobrar como en 2024 | **14.115,3 M** | 13.984 M (cap. 2) y 13.981 M (cap. 3) | 2, 3 |
| 3 | Llevar la percepción al 92% | **9.022,2 M** | 8.860 M (v2) y 9.036 M (v1) | 3 |
| 4 | Empleo y vivienda en régimen | **7.225,2 M de plata nueva** sobre un programa de **7.730,9 M** | "multiplicar por quince" aplicado a 7.225 M | 3 §3.8, y donde se enuncie la meta |
| 5 | Hacinamiento por zona | seis valores, ver abajo | 14,7% y 2,6% sin decir de qué zonas | 1 |
| 6 | Boulogne + Beccar combinadas | cinco valores, ver abajo | cuatro de las cinco filas eran Beccar sola | 1, cuadro de apertura |
| 7 | Gasto total 2025 | dos conceptos distintos, ver abajo | 324.304 M y 348.876 M sin aclarar | 1 §1.2 y §1.5 |
| 8 | Percepción 2024 en base A | **229.946 / 215.023 / 93,51%** | 215.024 M en el percibido | 2, 3 (tablas 2024–2025) |

---

## 1. Percepción 2025: la base correcta es la A

**Valor a usar en todo el documento: 89,32%.**

| | Devengado | Percibido | Tasa |
|---|---:|---:|---:|
| **A — recursos corrientes** (rubro 1) | 337.148,8 M | 301.154,7 M | **89,3240%** |
| B — recursos totales (rubros 1+2+3) | 339.178,9 M | 303.184,8 M | 89,3879% |

**La diferencia es el rubro 2.1, RECURSOS PROPIOS DE CAPITAL: 2.030,1 M.** Se
cobra entero —devengado igual a percibido— y por eso las dos bases dan el mismo
"sin cobrar" de **35.994,1 M**. Esa coincidencia es lo que hacía parecer que las
dos cuentas eran la misma.

La base B no es una percepción de recursos corrientes: es la de los recursos
totales, con la venta de activos adentro.

El propio SEF lo separa en dos líneas de la cuenta Ahorro-Inversión:

- línea **I, Ingresos corrientes (percibido) = 301.154,7 M** → base A
- línea **VI, Ingresos totales = 303.184,8 M** → base B

**Fuente:** `01_raw/sanisidro_transparencia/ejecucion_presupuestaria/2025_iv_recursos.pdf`,
parseado a `data/ejecucion_recursos.csv` (filas `periodo_tipo = acumulado_anual`,
año 2025). Contrastado con
`01_raw/sanisidro_transparencia/situacion_economico_financiera/situacion_economico_financiera_2025_anual.pdf`
→ `data/sef_anual.csv` y `data/baseline_2025.csv`.

`data/parametros_modelo.csv` ya trae `percepcion_recursos_corrientes = 89.32` y
`03_scripts/parametros_modelo.py` ya filtra por `rubro_codigo.startswith("1.")`:
**el modelo estaba bien, el que se desvió fue el texto.**

---

## 2. Volver a cobrar como en 2024: **14.115,3 M**

```
tasa 2024 = 215.023,5 / 229.945,5           = 93,5106%
93,5106% x 337.148,8 M devengados de 2025   = 315.270,0 M
menos el percibido real                     - 301.154,7 M
                                            = 14.115,3 M
```

**Fuente:** `data/ejecucion_recursos.csv`, años 2024 y 2025, `acumulado_anual`,
rubro 1.

**De dónde salían las otras dos.** Las dos usan la base B:

| | Cuenta | Da |
|---|---|---:|
| cap. 2 — 13.984 M | tasa 2024 exacta sobre recursos **totales** | 13.983,6 M |
| cap. 3 — 13.981 M | tasa 2024 **redondeada a 93,51%** sobre recursos totales | 13.981,4 M |

No eran dos cuentas distintas: era la misma cuenta mal basada, una con la tasa
exacta y otra con la tasa redondeada.

---

## 3. Llevar la percepción al 92%: **9.022,2 M**

```
0,92 x 337.148,8 M       = 310.176,9 M
menos el percibido real  - 301.154,7 M
                         =   9.022,2 M
```

**Fuente:** `data/ejecucion_recursos.csv`, 2025, `acumulado_anual`, rubro 1.

**De dónde salían las otras dos:**

| | Cuenta | Da |
|---|---|---:|
| v2 — 8.860 M | `0,92 x 339.178,9 − 303.184,8`, o sea la base B | 8.859,8 M |
| v1 — 9.036 M | `(0,92 − 0,8932) x 337.148,8`, base A pero con la tasa redondeada | 9.035,6 M |

El v1 estaba en la base correcta y falla por otra cosa: **redondea la tasa a
89,32% antes de restar.** La tasa real es 89,323958%. Ese redondeo vale
**13,3 M**.

> **Ojo, esto toca el modelo.** `03_scripts/modelo.py` toma
> `perc_base = parametros["percepcion_pct"] / 100`, y ese parámetro viene
> redondeado a dos decimales desde `parametros_modelo.py`. Por eso
> `data/financiamiento_opciones.csv` publica hoy **9.035.588.223,32** como
> aporte en régimen de la opción `ii_percepcion_92`.
>
> Si se adopta 9.022,2 M en el texto hay que **regenerar el modelo** con la tasa
> sin redondear —una línea en `modelo.py`— o el documento vuelve a
> contradecirse consigo mismo. **No lo cambié: mueve el capítulo 3 entero y esa
> decisión es tuya.** El efecto es del 0,15% y no da vuelta ninguna conclusión:
> la opción sigue cubriendo el programa con holgura.

---

## 4. Empleo y vivienda: los 7.225 M no son un múltiplo de la base

**La sospecha era correcta en el diagnóstico y equivocada en la causa.** No es
el 8,27% del gasto flexible: eso es una **consecuencia**, no el origen.

El modelo fija la meta como **2,5% del gasto total**, no como un múltiplo de lo
que se gasta hoy. Está en `03_scripts/modelo.py`, `OBJETIVO_MEDIO = 0.025`:

```
gasto total 2025 (corrientes + capital)      309.235,8 M
x 2,5%  = PROGRAMA COMPLETO en régimen         7.730,9 M
empleo 170,3 M + vivienda 335,4 M   =            505,7 M   (lo de hoy)
PLATA NUEVA = completo − lo de hoy             7.225,2 M
```

Reproduce al centavo el `costo_del_programa` del año 4 que publica
`data/financiamiento_opciones.csv`: **7.225.194.059,57**.

**El error de redacción es de qué mide el número:**

| | Valor | Contra la base de 505,7 M |
|---|---:|---:|
| Programa completo en régimen | 7.730,9 M | **15,29 x** |
| Plata nueva (los 7.225 M citados) | 7.225,2 M | 14,29 x |

**"Multiplicar por quince" es correcto** —y es 15,29×— pero se refiere al
programa **completo**, 7.730,9 M. La cifra que el capítulo cita al lado, 7.225 M,
es la **plata nueva**. Por eso `505 × 15 = 7.575` no cerraba: se estaba
multiplicando la base y comparándola con el incremento.

**Cómo redactar la meta para que sea cierta.** Cualquiera de estas dos:

> Llevar empleo y vivienda al **2,5% del gasto municipal**: de los 506 millones
> de hoy a **7.731 millones anuales**, quince veces más. Son **7.225 millones de
> plata nueva** por año en régimen.

o, si se quiere una sola cifra:

> **7.225 millones anuales de plata nueva** para empleo y vivienda, el
> **8,3% del gasto flexible** del Municipio.

**Sobre el §3.8.** El 8,3% del gasto flexible es correcto **para la plata
nueva**: 7.225,2 / 87.325,6 = **8,27%**. El programa completo es el **8,85%** del
flexible. Si en el mismo párrafo se cita el 8,3% y los 7.731 M, se contradicen.

---

## 5. Hacinamiento por zona

Hogares con **2 o más personas por cuarto**, Censo 2022 por radio censal.

| Zona | Hogares | Con hacinamiento | % |
|---|---:|---:|---:|
| Boulogne Sur Mer | 18.567 | 2.567 | **13,83%** |
| Beccar | 17.632 | 2.590 | **14,69%** |
| Villa Adelina | 19.067 | 1.398 | **7,33%** |
| San Isidro | 17.466 | 781 | **4,47%** |
| Acassuso | 20.795 | 788 | **3,79%** |
| Martínez | 17.032 | 445 | **2,61%** |

**Fuente:** `data/censo2022_sanisidro_por_radio.csv` cruzado con
`data/zonas_asignacion_radios.csv`. Numerador
`hogares_hacinamiento__2_00_3_00_personas_por_cuarto` +
`hogares_hacinamiento__mas_de_3_00_personas_por_cuarto`, denominador
`hogares_hacinamiento__total`. Coincide con `data/zonas_indicadores.csv`.

**Los dos números del capítulo 1 son correctos y están mal atribuidos.** El
14,7% es **Beccar** y el 2,6% es **Martínez**. Boulogne es 13,83%, no 14,7%. Ver
el punto 6.

---

## 6. Boulogne + Beccar, las dos zonas juntas

Se combinan **sumando numerador y denominador radio por radio**, no promediando
los dos porcentajes: cada indicador tiene su propio universo en el Censo y los
universos no son iguales entre zonas.

| Indicador | Boulogne | Beccar | **JUNTAS** | Universo combinado |
|---|---:|---:|---:|---:|
| NBI | 5,77% | 5,68% | **5,73%** | 36.199 hogares |
| Sin cloaca | 9,94% | 11,29% | **10,60%** | 36.012 hogares |
| Sin gas de red | 29,33% | 41,46% | **35,24%** | 36.199 hogares |
| Hacinamiento | 13,83% | 14,69% | **14,25%** | 36.199 hogares |
| Universidad completa o más | 6,39% | 9,94% | **8,08%** | 105.679 personas |

Los cuatro primeros van ponderados por **hogares**; el de educación, por
**personas**. Su universo, `educacion_mni__total`, coincide exactamente con
`poblacion_sexo__total` en los 360 radios: son las 295.978 personas en viviendas
particulares del partido, las mismas que usa el reparto vecinal del capítulo 4.

**Hogares sin gas de red, en número absoluto:**

| | Hogares |
|---|---:|
| Boulogne Sur Mer | 5.445 |
| Beccar | 7.311 |
| **Las dos juntas** | **12.756** |

Sobre los **25.165** hogares sin gas de red de todo el partido, las dos zonas
concentran el **50,7%**.

> **Corrección de yapa, no pedida.** El EXHIBIT 20 titula "25.166 hogares". Sale
> de multiplicar los hogares de cada zona por su porcentaje publicado a dos
> decimales y sumar. Contando hogar por hogar en los 360 radios da **25.165**.
> Es un hogar de diferencia y sale del redondeo del porcentaje, no de un error
> de dato, pero el número que se cita en el documento conviene que sea el
> contado. Es una línea en `03_scripts/graficos_cap5.py`, `ex20`: contar los
> hogares en vez de derivarlos del porcentaje. **No la toqué.**

**Qué cambia en el cuadro de apertura del capítulo 1.** Hoy dice "Boulogne /
Béccar" y cuatro de sus cinco filas son Beccar sola. Con las cifras combinadas
el cuadro cambia poco pero deja de mentir en el rótulo. Si se quiere el número
más fuerte, el que se sostiene es el de gas: **12.756 hogares**, la mitad del
partido, en dos zonas.

---

## 7. Los dos totales de gasto 2025

**No se contradicen: miden cosas distintas y difieren en dos ejes a la vez**, el
concepto y la unidad.

```
Los 7 objetos del gasto devengado 2025, nominales:
  1  GASTOS EN PERSONAL                                111.589,5 M
  2  BIENES DE CONSUMO                                  22.096,3 M
  3  SERVICIOS NO PERSONALES                           110.490,8 M
  4  BIENES DE USO                                      57.815,7 M
  5  TRANSFERENCIAS                                      7.243,5 M
  6  ACTIVOS FINANCIEROS                                   170,1 M
  7  SERVICIO DE LA DEUDA Y DISM. DE OTROS PASIVOS      14.898,0 M
                                                      -------------
                                                      324.304,0 M   <- §1.2
  menos activos financieros + servicio de la deuda    - 15.068,1 M
                                                      -------------
                                                      309.235,8 M   nominal
  x 1,12817252  (coeficiente anual del deflactor 2025)
                                                      -------------
                                                      348.875,9 M   <- §1.5
```

| | Qué mide | Unidad |
|---|---|---|
| **324.304 M** | los **siete** objetos del gasto devengado, con los financieros | pesos **nominales** de 2025 |
| **348.876 M** | los **cinco** objetos no financieros —gasto corriente + de capital— | pesos **constantes de diciembre de 2025** |

El mismo gasto corriente + de capital, en pesos nominales, es **309.235,8 M**
(línea VII de la cuenta Ahorro-Inversión del SEF). El coeficiente 1,128 no es
un ajuste raro: los importes anuales están al nivel de precios **promedio** de
2025 y el deflactor los lleva a **diciembre** de 2025.

**Cómo nombrarlos para que no se contradigan:**

- §1.2 → **"gasto devengado total 2025: 324.304 millones corrientes"**, y aclarar
  que incluye el servicio de la deuda. Es el total que usa el EXHIBIT 05 como
  denominador del % de personal y del % de obra, así que tiene que quedar con
  ese nombre.
- §1.5 → **"gasto corriente y de capital 2025: 348.876 millones de diciembre de
  2025"**, o su equivalente nominal, 309.236 millones. Es el concepto de la
  serie comparable 2010–2025 y el que usa el modelo.

**Regla para el resto del documento:** cada vez que aparezca un total de gasto,
decir las dos cosas —**con o sin financieros**, y **nominal o constante**—. Son
los dos ejes que se cruzaron.

**Fuente:** `data/ejecucion_gastos_objeto.csv`, `data/serie_gastos_comparable.csv`
(fila 2025), `data/deflactor.csv` (`coef_anual` 2025) y `data/baseline_2025.csv`.

---

## 8. La fila de 2024 en base A

**Las tres cifras pedidas, base A —recursos corrientes, rubro 1, sin el 2.1:**

| | Devengado | Percibido | Tasa |
|---|---:|---:|---:|
| **2024, base A** | **229.945.522.987,77** | **215.023.499.681,17** | **93,510627%** |

Sin cobrar: **14.922.023.306,60**.

**Como va en la tabla, al lado de 2025 y en la misma base:**

| Año | Devengado | Percibido | Percepción | Sin cobrar |
|---|---:|---:|---:|---:|
| 2024 | 229.946 M | **215.023 M** | 93,51% | 14.922 M |
| 2025 | 337.149 M | 301.155 M | 89,32% | 35.994 M |

**Cambia un dígito, y no es el que se esperaba.** En 2024 el rubro 2.1
RECURSOS PROPIOS DE CAPITAL fueron **178.900,89 pesos**. En 2025 fueron
**2.030,1 millones**. La corrección de base, que en 2025 mueve la tasa de
89,3879% a 89,3240%, en 2024 mueve la sexta cifra decimal:

| 2024 | Devengado | Percibido | Tasa |
|---|---:|---:|---:|
| base A | 229.945.522.987,77 | 215.023.499.681,17 | 93,510627% |
| base B | 229.945.701.888,66 | 215.023.678.582,06 | 93,510632% |

Redondeado a millones, **lo único que cambia es el percibido: 215.024 → 215.023.**
El devengado y la tasa se escriben igual en las dos bases.

**Qué hacer con esto.** Cambiar el 215.024 por 215.023 y listo. Pero lo que
importa no es el millón: es que la fila de 2024 quede **declarada** en la misma
base que la de 2025. Hoy las dos filas comparan bien por casualidad —porque en
2024 casi no hubo venta de activos—, no por construcción. El año que el
Municipio venda algo, la tabla se rompe sola y nadie se entera.

Poner al pie de las dos tablas: **"recursos corrientes, rubro 1 de la ejecución
presupuestaria; no incluye recursos de capital"**.

**Fuente:** `data/ejecucion_recursos.csv`, año 2024, `periodo_tipo =
acumulado_anual`, rubros 1.1, 1.2, 1.6 y 1.7. Viene de
`01_raw/sanisidro_transparencia/ejecucion_presupuestaria/2024_iv_recursos_-_anual.pdf`.

**Ojo con el punto 2.** La tasa de 2024 no cambia a la precisión que se usa,
así que **los 14.115,3 M de "volver a cobrar como 2024" siguen valiendo**: ya
estaban calculados con la tasa de base A. Lo que estaba mal basado ahí era el
**2025**, no el 2024.

---

## Lo que queda abierto y no decidí yo

1. **El redondeo del modelo (punto 3).** Adoptar 9.022,2 M obliga a regenerar
   `data/financiamiento_opciones.csv` y `data/modelo_flujo_caja.csv` con la tasa
   sin redondear. Es una línea de `modelo.py`. No la toqué.
2. **El EXHIBIT 20 (punto 6).** Titula 25.166 hogares sin gas de red y el
   conteo exacto da 25.165. Una línea en `graficos_cap5.py`.
3. **El cuadro de apertura del capítulo 1 (punto 6).** Con las cifras combinadas
   el titular deja de ser "Boulogne y Beccar" sostenido por números de Beccar
   sola. Hay que decidir si el cuadro pasa a ser de las dos zonas combinadas o
   si se separa en dos columnas. Las dos versiones están calculadas arriba.
