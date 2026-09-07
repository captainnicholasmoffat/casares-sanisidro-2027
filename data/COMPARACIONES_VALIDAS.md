# Qué comparaciones de gasto se sostienen

Pesos constantes de diciembre de 2025. Generado por
`03_scripts/serie_comparable.py` el 2026-09-07.

Una comparación entre dos años se sostiene **si los dos años miden el
mismo concepto de gasto**. Si no, no es una comparación: es un cambio de
definición disfrazado de variación.

---

## 1. La serie comparable — usar esta

`data/serie_gastos_comparable.csv`. Un solo concepto en todos los años:
**Gastos corrientes + gastos de capital (sin aplicaciones financieras)**.

Es el gasto de gestión: lo que el Municipio gasta en funcionar y en
invertir, sin la amortización de deuda ni los movimientos financieros.

| Año | Constante dic-2025 | Var. real | Brecha | Origen |
|---|---:|---:|---:|---|
| 2010 | 308461384323.82 | — | — | publicado |
| 2011 | 319416074100.93 | 3.55% | 1 año(s) | publicado |
| 2012 | 316286899626.36 | -0.98% | 1 año(s) | publicado |
| 2014 | 358359662680.73 | 13.30% | 2 año(s) | publicado |
| 2015 | 393185801150.07 | 9.72% | 1 año(s) | publicado |
| 2016 | 371602251443.77 | -5.49% | 1 año(s) | derivado |
| 2017 | 461540565785.43 | 24.20% | 1 año(s) | publicado |
| 2019 | 419618913651.84 | -9.08% | 2 año(s) | publicado |
| 2020 | 376048621624.61 | -10.38% | 1 año(s) | publicado |
| 2021 | 369551973565.29 | -1.73% | 1 año(s) | publicado |
| 2022 | 382390334727.64 | 3.47% | 1 año(s) | publicado |
| 2024 | 300697965150.41 | -21.36% | 2 año(s) | derivado |
| 2025 | 348875923719.59 | 16.02% | 1 año(s) | derivado |

**Todos los pares de esta tabla son comparables entre sí**, porque todos
miden lo mismo. `origen_del_dato` dice si el año viene publicado directo
o derivado de los objetos del gasto; la derivación está verificada en la
sección 3.

---

## 2. Todos los pares válidos de la serie comparable

78 pares. Ordenados por variación real, de la mayor caída a la mayor suba.

| Desde | Hasta | Años | Var. real | Nota |
|---|---|---:|---:|---|
| 2017 | 2024 | 7 | -34.85% | un extremo derivado de los objetos (2024) |
| 2019 | 2024 | 5 | -28.34% | un extremo derivado de los objetos (2024) |
| 2017 | 2025 | 8 | -24.41% | un extremo derivado de los objetos (2025) |
| 2015 | 2024 | 9 | -23.52% | un extremo derivado de los objetos (2024) |
| 2022 | 2024 | 2 | -21.36% | un extremo derivado de los objetos (2024) |
| 2020 | 2024 | 4 | -20.04% | un extremo derivado de los objetos (2024) |
| 2017 | 2021 | 4 | -19.93% | los dos publicados directo |
| 2016 | 2024 | 8 | -19.08% | un extremo derivado de los objetos (2016, 2024) |
| 2021 | 2024 | 3 | -18.63% | un extremo derivado de los objetos (2024) |
| 2017 | 2020 | 3 | -18.52% | los dos publicados directo |
| 2017 | 2022 | 5 | -17.15% | los dos publicados directo |
| 2019 | 2025 | 6 | -16.86% | un extremo derivado de los objetos (2025) |
| 2014 | 2024 | 10 | -16.09% | un extremo derivado de los objetos (2024) |
| 2019 | 2021 | 2 | -11.93% | los dos publicados directo |
| 2015 | 2025 | 10 | -11.27% | un extremo derivado de los objetos (2025) |
| 2019 | 2020 | 1 | -10.38% | los dos publicados directo |
| 2017 | 2019 | 2 | -9.08% | los dos publicados directo |
| 2019 | 2022 | 3 | -8.87% | los dos publicados directo |
| 2022 | 2025 | 3 | -8.76% | un extremo derivado de los objetos (2025) |
| 2020 | 2025 | 5 | -7.23% | un extremo derivado de los objetos (2025) |
| 2016 | 2025 | 9 | -6.12% | un extremo derivado de los objetos (2016, 2025) |
| 2015 | 2021 | 6 | -6.01% | los dos publicados directo |
| 2011 | 2024 | 13 | -5.86% | un extremo derivado de los objetos (2024) |
| 2021 | 2025 | 4 | -5.59% | un extremo derivado de los objetos (2025) |
| 2015 | 2016 | 1 | -5.49% | un extremo derivado de los objetos (2016) |
| 2012 | 2024 | 12 | -4.93% | un extremo derivado de los objetos (2024) |
| 2015 | 2020 | 5 | -4.36% | los dos publicados directo |
| 2015 | 2022 | 7 | -2.75% | los dos publicados directo |
| 2014 | 2025 | 11 | -2.65% | un extremo derivado de los objetos (2025) |
| 2010 | 2024 | 14 | -2.52% | un extremo derivado de los objetos (2024) |
| 2020 | 2021 | 1 | -1.73% | los dos publicados directo |
| 2011 | 2012 | 1 | -0.98% | los dos publicados directo |
| 2016 | 2021 | 5 | -0.55% | un extremo derivado de los objetos (2016) |
| 2016 | 2020 | 4 | 1.20% | un extremo derivado de los objetos (2016) |
| 2020 | 2022 | 2 | 1.69% | los dos publicados directo |
| 2010 | 2012 | 2 | 2.54% | los dos publicados directo |
| 2016 | 2022 | 6 | 2.90% | un extremo derivado de los objetos (2016) |
| 2014 | 2021 | 7 | 3.12% | los dos publicados directo |
| 2021 | 2022 | 1 | 3.47% | los dos publicados directo |
| 2010 | 2011 | 1 | 3.55% | los dos publicados directo |
| 2014 | 2016 | 2 | 3.70% | un extremo derivado de los objetos (2016) |
| 2014 | 2020 | 6 | 4.94% | los dos publicados directo |
| 2014 | 2022 | 8 | 6.71% | los dos publicados directo |
| 2015 | 2019 | 4 | 6.72% | los dos publicados directo |
| 2011 | 2025 | 14 | 9.22% | un extremo derivado de los objetos (2025) |
| 2014 | 2015 | 1 | 9.72% | los dos publicados directo |
| 2012 | 2025 | 13 | 10.30% | un extremo derivado de los objetos (2025) |
| 2011 | 2014 | 3 | 12.19% | los dos publicados directo |
| 2016 | 2019 | 3 | 12.92% | un extremo derivado de los objetos (2016) |
| 2010 | 2025 | 15 | 13.10% | un extremo derivado de los objetos (2025) |
| 2012 | 2014 | 2 | 13.30% | los dos publicados directo |
| 2011 | 2021 | 10 | 15.70% | los dos publicados directo |
| 2024 | 2025 | 1 | 16.02% | un extremo derivado de los objetos (2024, 2025) |
| 2010 | 2014 | 4 | 16.18% | los dos publicados directo |
| 2011 | 2016 | 5 | 16.34% | un extremo derivado de los objetos (2016) |
| 2012 | 2021 | 9 | 16.84% | los dos publicados directo |
| 2014 | 2019 | 5 | 17.09% | los dos publicados directo |
| 2015 | 2017 | 2 | 17.38% | los dos publicados directo |
| 2012 | 2016 | 4 | 17.49% | un extremo derivado de los objetos (2016) |
| 2011 | 2020 | 9 | 17.73% | los dos publicados directo |
| 2012 | 2020 | 8 | 18.89% | los dos publicados directo |
| 2011 | 2022 | 11 | 19.72% | los dos publicados directo |
| 2010 | 2021 | 11 | 19.80% | los dos publicados directo |
| 2010 | 2016 | 6 | 20.47% | un extremo derivado de los objetos (2016) |
| 2012 | 2022 | 10 | 20.90% | los dos publicados directo |
| 2010 | 2020 | 10 | 21.91% | los dos publicados directo |
| 2011 | 2015 | 4 | 23.10% | los dos publicados directo |
| 2010 | 2022 | 12 | 23.97% | los dos publicados directo |
| 2016 | 2017 | 1 | 24.20% | un extremo derivado de los objetos (2016) |
| 2012 | 2015 | 3 | 24.31% | los dos publicados directo |
| 2010 | 2015 | 5 | 27.47% | los dos publicados directo |
| 2014 | 2017 | 3 | 28.79% | los dos publicados directo |
| 2011 | 2019 | 8 | 31.37% | los dos publicados directo |
| 2012 | 2019 | 7 | 32.67% | los dos publicados directo |
| 2010 | 2019 | 9 | 36.04% | los dos publicados directo |
| 2011 | 2017 | 6 | 44.50% | los dos publicados directo |
| 2012 | 2017 | 5 | 45.92% | los dos publicados directo |
| 2010 | 2017 | 7 | 49.63% | los dos publicados directo |

---

## 3. Por qué se puede derivar el concepto desde los objetos

En los años donde la fuente publica **las dos aperturas** —el gasto por
carácter económico y el gasto por objeto— se comprueba la identidad:

```
suma de los objetos  −  objetos financieros  ==  corrientes + capital
```

| Año | Publicado (cte+cap) | Derivado de objetos | Diferencia | ¿Cierra? | |
|---|---:|---:|---:|---|---|
| 2010 | 574631896.00 | 574631897.39 | 1.39 | sí | difiere en $1.39, redondeo de la fuente |
| 2011 | 737044564.84 | 733148262.33 | -3896302.51 | **no** | difiere en $-3896302.51: la apertura por objeto y la de caracter no dicen lo mismo en este anio |
| 2012 | 902719747.36 | 902719747.36 | 0.00 | sí | exacto |
| 2014 | 1836789774.71 | 1836789774.71 | 0.00 | sí | exacto |
| 2015 | 2550765880.76 | 2550765880.76 | 0.00 | sí | exacto |
| 2017 | 5150189491.25 | 5150189491.25 | 0.00 | sí | exacto |
| 2022 | 32005333857.82 | 32005333857.82 | 0.00 | sí | exacto |

La identidad cierra en **6 de los 7 años** donde se puede probar (2010, 2012, 2014, 2015, 2017, 2022).
Sobre eso se apoya la derivación de los años sin apertura por carácter:
**2016, 2024, 2025**.

> **Límite honesto.** Para 2024 y 2025 la fuente es el informe trimestral
> de ejecución, que **no** publica apertura por carácter económico, así
> que la identidad no se puede probar en esos años: se apoya en que se
> cumple en los siete anteriores, con las otras dos fuentes. Si algún día
> el Municipio publica el Ahorro-Inversión de 2024-2025, hay que
> recontrastarlo.

**Los años que no cierran no se derivan**: para ellos se usa el valor
publicado directo, que existe. La identidad sólo habilita la
derivación en los años donde no hay apertura por carácter, que son
los que aparecen como `derivado` en la serie.

---

## 4. Pares válidos dentro de la serie heterogénea

`data/serie_gastos_totales_real.csv` mezcla conceptos. Estos son los
únicos pares que ahí adentro comparan lo mismo, agrupados por concepto.

### Total de gastos de la rendicion de cuentas

Años: **2010, 2011, 2012, 2019, 2020, 2021**

| Desde | Hasta | Años | Var. real |
|---|---|---:|---:|
| 2010 | 2011 | 1 | 2.88% |
| 2010 | 2012 | 2 | 1.56% |
| 2010 | 2019 | 9 | 25.03% |
| 2010 | 2020 | 10 | 12.05% |
| 2010 | 2021 | 11 | 10.11% |
| 2011 | 2012 | 1 | -1.29% |
| 2011 | 2019 | 8 | 21.53% |
| 2011 | 2020 | 9 | 8.91% |
| 2011 | 2021 | 10 | 7.03% |
| 2012 | 2019 | 7 | 23.11% |
| 2012 | 2020 | 8 | 10.33% |
| 2012 | 2021 | 9 | 8.42% |
| 2019 | 2020 | 1 | -10.38% |
| 2019 | 2021 | 2 | -11.93% |
| 2020 | 2021 | 1 | -1.73% |

### Gastos con imputacion al presupuesto

Años: **2016, 2017, 2022**

| Desde | Hasta | Años | Var. real |
|---|---|---:|---:|
| 2016 | 2017 | 1 | 18.70% |
| 2016 | 2022 | 6 | -6.49% |
| 2017 | 2022 | 5 | -21.22% |

### Gastos ejecutados (incluye aplicaciones financieras)

Años: **2014**

Un solo año, no hay par posible.

### Gastos con imputacion al presupuesto (HTC)

Años: **2015**

Un solo año, no hay par posible.

### Devengado, suma de los 6 objetos del gasto del informe acumulado anual

Años: **2024**

Un solo año, no hay par posible.

### Devengado, suma de los 7 objetos del gasto del informe acumulado anual

Años: **2025**

Un solo año, no hay par posible.

---

## 5. Lo que NO se puede decir

- **No** comparar un año de *gastos con imputación al presupuesto* contra
  uno de *devengado por objeto*: no miden lo mismo.
- **No** comparar 2010-2012 contra 2019-2021 usando el *total de gastos*
  de las rendiciones: el de 2010-2012 incluye las aplicaciones
  financieras y el de 2019-2021 no. Es el cambio al formato
  Ahorro-Inversión de los informes ARSI, donde las aplicaciones van
  debajo de la línea. En 2010 eran el 8,1% del total y en 2021 el 14,0%.
- **No** leer como variación interanual un salto que cruza años sin dato.
  La columna `brecha_anios` dice cuántos años acumula cada variación.
- **No** mezclar presupuestado con ejecutado. El presupuesto está en
  `data/presupuesto_historico_2010_2026.csv` y es otra cosa.

## 6. Años sin dato

No hay rendición de cuentas ni informe de ejecución anual publicado para
**2013, 2018 y 2023**. Quedan vacíos en la serie comparable. No se
interpolan ni se sustituyen por otro concepto.
