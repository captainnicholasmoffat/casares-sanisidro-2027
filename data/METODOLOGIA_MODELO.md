# Metodología del modelo de flujo de caja

Proyección financiera del Municipio de San Isidro, **2026-2037**, con corte en
2031 (fin del mandato 2028-2031) y en 2037 (diez años).

```
python3 03_scripts/parse_sef.py          # el estado económico-financiero a CSV
python3 03_scripts/parametros_modelo.py  # los parámetros, desde las series
python3 03_scripts/modelo.py             # escenarios, financiamiento, sensibilidad
python3 03_scripts/test_modelo.py        # las validaciones
```

---

## 0. Dos decisiones que condicionan todo

### Pesos constantes de diciembre de 2025, sin supuesto de inflación

El modelo **no lleva sendero de inflación**. No hace falta: lo que se proyecta
son cantidades reales. Y ponerlo sería colgar todo el modelo del número más
frágil que existe — nadie proyecta la inflación argentina a diez años y sobrevive
a la auditoría.

Todo está deflactado con el índice de `data/deflactor.csv` (IPC del INDEC
empalmado con el de San Luis; ver `data/METODOLOGIA_DEFLACTOR.md`).

### El año 0 es la ejecución real, no una estimación

2025 sale de la cuenta **Ahorro-Inversión-Financiamiento** del Estado de
Situación Económico-Financiera 2025, parseado por `03_scripts/parse_sef.py`:

| | Millones de pesos |
|---|---:|
| I. Ingresos corrientes (percibido) | 301.155 |
| II. Gastos corrientes (devengado) | 251.404 |
| **III. Ahorro corriente** | **49.751** |
| IV. Recursos de capital | 2.030 |
| V. Gastos de capital | 57.832 |
| VI. Ingresos totales | 303.185 |
| VII. Gastos totales | 309.236 |
| **VIII. Resultado financiero** | **−6.051** |

**Ojo con la asimetría:** los ingresos van por lo **percibido** y los gastos por
lo **devengado**. No es un descuido: es la convención del formato oficial.
Comparar devengado contra devengado da +14.875 millones de superávit, que no es
el resultado financiero de nada. Esta distinción es la diferencia entre decir que
San Isidro cerró 2025 con déficit o con superávit.

Las cuatro identidades internas de la cuenta cierran al centavo en 2024 y 2025.

---

## 1. Los tres parámetros

Ninguno está escrito a mano. `03_scripts/test_modelo.py` los recalcula desde
las series y falla si no coinciden con `data/parametros_modelo.csv`.

### a) Crecimiento real de los recursos propios: **+1,95% anual**

"Recursos propios" = recursos de **origen municipal**. Serie en
`data/recursos_propios_serie.csv`, siete puntos entre 2010 y 2025, en pesos
constantes:

| Año | Millones dic-2025 | Var. real anual |
|---|---:|---:|
| 2010 | 175.559 | — |
| 2014 | 205.700 | +4,04% |
| 2015 | 242.311 | +17,80% |
| 2017 | 266.272 | +4,83% |
| 2022 | 267.589 | +0,10% |
| 2024 | 232.199 | −6,80% |
| 2025 | 234.625 | +1,04% |

Punta a punta 2010-2025: **+1,95% anual**. La media de los seis tramos da +3,49%
con un desvío de **8,14 puntos**, que es enorme: esta serie es volátil y el
modelo lo trata en la sensibilidad, no lo esconde.

> **Trampa que hay que evitar.** No se puede usar la apertura por rubro como
> sustituto. La coparticipación provincial está contabilizada **dentro de
> "ingresos no tributarios"**, así que sumar tributarios + no tributarios +
> rentas daría 291.319 millones de "recursos propios" en 2025 en vez de 207.969:
> un 40% de más, contando como propio lo que manda la Provincia.

### b) Caída del coeficiente de coparticipación: **−2,196% anual**

Participación de San Isidro en el total transferido por la Provincia a los 135
municipios, calculada de los XLSX crudos. Serie en
`data/coparticipacion_serie.csv`:

| Año | San Isidro (mill.) | Total 135 municipios (mill.) | Participación |
|---|---:|---:|---:|
| 2021 | 5.070 | 261.654 | **1,9378%** |
| 2022 | 9.541 | 481.511 | 1,9814% |
| 2023 | 20.191 | 1.049.342 | 1,9242% |
| 2024 | 62.713 | 3.337.288 | 1,8792% |
| 2025 | 82.268 | 4.639.756 | **1,7731%** |
| 2026 (6 meses) | 46.719 | 2.778.995 | 1,6811% |

Compuesto 2021-2025: **−2,196% anual**. El dato preliminar de 2026 muestra la
caída acelerándose.

> **Un error que costó un factor de 2.** La planilla trae una fila
> **"CONSOLIDADO 135 MUNICIPIOS"** que es el total provincial, no un municipio.
> Sumarla como si lo fuera duplica el denominador y da una participación de
> 0,8866% en vez de 1,7731% — exactamente la mitad. Está resuelto en el código y
> queda anotado acá porque es fácil de repetir.

**Esto se arrastra en todos los escenarios.** El 82,4% de lo que San Isidro
recibe de la Provincia es coparticipación bruta y se mueve con este coeficiente;
el 17,6% restante son fondos específicos que no dependen de él. Es viento fiscal
en contra estructural, no una hipótesis.

### c) Rigidez del gasto: **39,0% núcleo duro, 73,1% con contratos**

Sobre el devengado por objeto de 2025:

| | Millones | % del gasto | Qué es |
|---|---:|---:|---|
| Personal | 111.590 | 34,4% | núcleo duro |
| Servicio de la deuda | 14.898 | 4,6% | núcleo duro |
| **Núcleo duro** | **126.488** | **39,0%** | no se toca sin romper un contrato |
| Servicios no personales | 110.491 | 34,1% | contratos plurianuales |
| **Con contratos** | **236.978** | **73,1%** | no se toca dentro del ejercicio |
| Bienes de consumo | 22.096 | 6,8% | flexible |
| Bienes de uso | 57.816 | 17,8% | flexible |
| Transferencias | 7.243 | 2,2% | flexible |
| Activos financieros | 170 | 0,1% | flexible |
| **Flexible** | **87.326** | **26,9%** | el único margen del ejercicio |

### d) Percepción de recursos corrientes: **89,32%**

De 337.149 millones devengados en 2025 se percibieron 301.155. Quedaron
**35.994 millones sin cobrar**. Es una palanca de financiamiento que no requiere
subir una sola tasa.

---

## 2. Qué crece y qué no

| Componente | 2025 | Regla | Por qué |
|---|---:|---|---|
| Origen municipal | 206.577 | +1,95% anual real | la tasa histórica |
| Origen provincial | 87.107 | 82,4% cae −2,196% anual; 17,6% constante | el coeficiente |
| Origen nacional | 190 | constante real | es el 0,06% |
| Otros orígenes | 7.281 | constante real | es el 2,4% |
| Recursos de capital | 2.030 | constante real | es el 0,67% |
| Gastos corrientes | 251.404 | constante real | "sin cambios de política" |
| Gastos de capital | 57.832 | constante real | ídem |

### Los supuestos que hay que declarar

1. **La masa provincial a repartir se mantiene constante en términos reales.** No
   hay dato para proyectarla. Suponer que crece sería regalarle al modelo un
   ingreso que nadie garantizó.
2. **El gasto real constante es un supuesto, no un pronóstico.** Implica que no
   hay recomposición salarial real ni ampliación de servicios. Es la lectura
   literal de "sin cambios de política" y es lo que produce el superávit del
   escenario base: si el gasto acompañara a los recursos, el resultado se quedaría
   cerca de cero. **El superávit del base mide el margen disponible, no una
   predicción de que el Municipio vaya a ahorrarlo.**
3. **Amortización de la deuda existente.** El formulario de la Ley 12.462 publica
   el vencimiento del ejercicio 1 (3.388 millones) y nada más. De 2027 en adelante
   se supone que el remanente consolidado se amortiza en tres partes iguales. El
   stock es el 2,9% del gasto anual, así que mueve poco.
4. **El costo del crédito no existe en el repo.** No hay ningún dato sobre a qué
   tasa se financia el Municipio. Por eso la opción de endeudamiento se corre con
   tres tasas reales (0%, 5% y 10%) y no se elige ninguna. Lo que se pierde:
   no se puede decir cuál es el costo verdadero, sólo acotarlo.

---

## 3. Los tres escenarios

| Escenario | Recursos propios | Coparticipación | Programa |
|---|---|---|---|
| **base** | +1,95% anual | −2,196% anual | no |
| **adverso** | −0,05% anual (2 puntos menos) | −3,5% anual | no |
| **reformista** | +1,95% anual | −2,196% anual | sí, al 2,5% del gasto en 4 años |

Resultado financiero, en millones de pesos de diciembre de 2025:

| Escenario | 2025 | 2028 | 2031 | 2034 | 2037 |
|---|---:|---:|---:|---:|---:|
| base | −6.051 | +1.645 | +10.375 | +20.162 | +31.035 |
| adverso | −6.051 | −13.637 | −20.484 | −26.668 | −32.257 |
| reformista | −6.051 | +1.645 | +10.375 | +20.162 | +31.035 |

El reformista da igual que el base **por construcción**: el programa se financia
reasignando, así que el gasto total no cambia — cambia su composición.

---

## 4. El programa: empleo y vivienda

Hoy, del Estado de Situación Económico-Financiera 2025, por programa:

| Programa | Devengado 2025 | % del gasto |
|---|---:|---:|
| Apoyo y promoción al empleo | 170.314.501 | 0,055% |
| Infraestructura habitacional | 335.387.189 | 0,108% |
| **Total** | **505.701.690** | **0,164%** |

Llevarlo al **2,5% del gasto total** en cuatro años cuesta **7.225 millones por
año** en régimen. Las dos puntas del rango pedido: al 2% son 5.680 millones; al
3% son 8.771 millones.

Ese costo equivale al **8,3% del gasto flexible** de 2025 (87.326 millones). No
toca personal, deuda ni contratos de servicios.

### De dónde sale la plata: las tres opciones, sin elegir

En `data/financiamiento_opciones.csv`, cuantificadas contra el mismo costo.
En régimen (2029 en adelante), para el objetivo del 2,5%:

| Opción | Aporte anual | Cubre | Efecto en el resultado financiero |
|---|---:|---:|---:|
| **i. Reasignación** | 7.225 mill. | 100% | 0 — el gasto total no cambia |
| **ii. Percepción al 92%** | 9.036 mill. | 125% | +9.036 mill. |
| **ii. Percepción al 95%** | 19.150 mill. | 265% | +19.150 mill. |
| **ii. Percepción al 97%** | 25.893 mill. | 358% | +25.893 mill. |
| **iii. Crédito, 0% real** | 7.225 mill. | 100% | +2.529 mill. |
| **iii. Crédito, 5% real** | 7.225 mill. | 100% | +1.626 mill. |
| **iii. Crédito, 10% real** | 7.225 mill. | 100% | +723 mill. |

La opción (i) sale del gasto flexible: bienes de consumo, bienes de uso,
transferencias. Cuáles exactamente es una decisión política, y el detalle por
finalidad y función está en `data/gastos_finalidad_funcion.csv`.

La opción (ii) sola alcanza y sobra: subir la cobranza tres puntos —de 89,3% a
92,3%— ya cubre el programa entero. Es la más barata políticamente y la que no
requiere sacarle nada a nadie.

---

## 5. Sensibilidad

`data/sensibilidad.csv`. Cada dimensión se mueve sola, con las otras dos en su
valor del escenario base. Resultado financiero en millones de pesos dic-2025:

| Dimensión | Variante | 2031 | 2037 |
|---|---|---:|---:|
| Recursos propios | +0,95% anual | −2.946 | +1.980 |
| | **+1,95% anual (base)** | **+10.375** | **+31.035** |
| | +2,95% anual | +24.365 | +63.401 |
| Coparticipación | −1,5% anual | +13.105 | +35.919 |
| | **−2,196% anual (base)** | **+10.375** | **+31.035** |
| | −2,5% anual | +9.212 | +29.019 |
| | −3,5% anual | +5.514 | +22.855 |
| Percepción | 86,32% (−3 puntos) | −292 | +19.675 |
| | **89,32% (base)** | **+10.375** | **+31.035** |
| | 92,32% (+3 puntos) | +21.041 | +42.396 |

**Lo que manda es el crecimiento de los recursos propios.** Un punto menos por
año da vuelta el resultado del mandato: de +10.375 a −2.946 millones en 2031. La
coparticipación mueve menos porque afecta al 29% de los ingresos, no al 68%. Y
tres puntos de cobranza valen casi lo mismo que un punto de crecimiento.

---

## 6. Qué NO hace este modelo

- **No proyecta la inflación**, a propósito.
- **No proyecta la masa coparticipable provincial**: no hay dato.
- **No sabe a qué tasa se endeuda el Municipio**: no hay dato, por eso hay tres.
- **No modela cambios de alícuotas ni nuevas tasas.** Todo el crecimiento de
  recursos propios es el histórico, sin reforma tributaria.
- **No modela el gasto por finalidad hacia adelante.** La reasignación se
  cuantifica contra el agregado flexible; cuáles partidas exactamente es una
  decisión política que el modelo no toma.
- **Los años 2013, 2018 y 2023 no tienen rendición publicada** y no aparecen en la
  serie histórica de recursos propios.

## 7. Archivos

| Archivo | Qué es |
|---|---|
| `data/baseline_2025.csv` | La ejecución real 2025, estructura completa. |
| `data/modelo_flujo_caja.csv` | Los tres escenarios, 2025-2037. |
| `data/financiamiento_opciones.csv` | Las tres formas de pagar el programa. |
| `data/sensibilidad.csv` | Qué pasa si se mueve cada parámetro. |
| `data/parametros_modelo.csv` | Los parámetros y de dónde salen. |
| `data/recursos_propios_serie.csv` | La serie que da el parámetro (a). |
| `data/coparticipacion_serie.csv` | La serie que da el parámetro (b). |
| `data/sef_anual.csv` | El estado económico-financiero 2024 y 2025. |
| `data/RESUMEN_MODELO.md` | Tres párrafos: qué pasa, qué cuesta, de dónde sale. |

Fecha: **2026-09-07**.
