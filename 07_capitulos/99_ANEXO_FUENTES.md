# ANEXO DE FUENTES

Este anexo existe para que cualquiera pueda rehacer las cuentas de este documento, o encontrar que no cierran.

Contiene todas las fuentes que el documento cita, y ninguna más. También contiene lo que no se pudo consultar, y por qué: **un vacío declarado no se puede usar en contra; uno escondido, sí.**

---

## 1. Las fuentes, una por una

### 1.1 Municipalidad de San Isidro

| Fuente | Qué aporta | Capítulos | Estado |
|---|---|---|---|
| Ejecución presupuestaria trimestral, 2024–2026 (19 PDF) | Recursos devengados y percibidos, gastos por objeto | 1, 2, 3, 5 | **VERIFICADA** contra fuente primaria |
| Situación económico-financiera, 2010–2026 (13 PDF) | Cuenta Ahorro-Inversión-Financiamiento, gastos por programa | 1, 3, 5 | **VERIFICADA** |
| Gasto por finalidad y función, 2024–2026 (11 PDF) | Las funciones del presupuesto y su variación | 5 | **VERIFICADA** |
| Rendición de cuentas anual (10 PDF: 2010–2012, 2014, 2015, 2017, 2019–2022) | Serie de gasto real de dieciséis años | 1 | **VERIFICADA** |
| Stock de deuda trimestral, 2024–2026 (11 PDF) | Deuda y amortizaciones del modelo | 3 | **VERIFICADA** |
| Presupuestos municipales, 2010–2026 (19 PDF, falta 2015) | Presupuestado contra ejecutado | 3 | **VERIFICADA** |
| Ordenanzas Fiscal e Impositiva, 2022–2024 (5 PDF) | Tasas y alícuotas vigentes | 2 | **VERIFICADA** |
| "Prioridades Estratégicas 2024–2025" | Las tres prioridades, 19 objetivos y 77 metas del plan vigente | Intro, 1, 2 | **VERIFICADA** |
| Portal de transparencia, relevado en septiembre de 2026 | Qué está publicado y qué no | 2, 5, 6 | **VERIFICADA**, con la evidencia de cada 404 registrada |

*Todos en `01_raw/sanisidro_transparencia/` y `01_raw/presupuestos/`, con su URL de origen y su tamaño en bytes en `01_raw/INVENTARIO.txt`.*

### 1.2 Provincia de Buenos Aires

| Fuente | Qué aporta | Capítulos | Estado |
|---|---|---|---|
| Transferencias y descentralización a municipios, 2021–2026 (13 XLSX) | Participación de San Isidro en el reparto provincial | 1, 3 | **VERIFICADA** |
| Fallos del Tribunal de Cuentas | Validación cruzada de las rendiciones | 1, 3 | **VERIFICADA** |
| Sistema SIMCo | Validación cruzada de las series fiscales | 1, 3 | **VERIFICADA** |
| Ejecución RAFAM 2025, 106 municipios | Mediana provincial y posición de San Isidro | 1, 2 | **PROCESADA POR TERCEROS** — ver 2.1 |
| Sistema de Boletines Oficiales Municipales (SIBOM) | Ordenanza 7124/2025 y Decreto 2099/2025 de Pinamar | 4, 6 | **VERIFICADA** |

### 1.3 Nacionales

| Fuente | Qué aporta | Capítulos | Estado |
|---|---|---|---|
| Censo Nacional 2022 (INDEC), por radio censal | Los seis indicadores territoriales, las seis zonas | 1, 4, 5, 6 | **VERIFICADA** |
| IPC INDEC, 2016–2026 | Deflactor de todas las series | 1, 3, 5 | **VERIFICADA** |
| IPC San Luis, 2010–2016 | Empalme del deflactor anterior a diciembre de 2016 | 1, 3 | **VERIFICADA**, con el empalme declarado |

### 1.4 Normativa

| Fuente | Qué aporta | Capítulos | Estado |
|---|---|---|---|
| Constitución de la Provincia de Buenos Aires (1994) | Arts. 190, 192, 193, 211 | 4, 6 | **VERIFICADA** contra el texto oficial |
| Decreto-Ley 6769/58, Ley Orgánica de las Municipalidades | Arts. 24, 60, 119, 132 | 4, 6 | **VERIFICADA** contra el texto oficial provincial |
| Ordenanza 6045/1984 de San Isidro, y su modificatoria 7164/1993 | Régimen de asociaciones vecinales, arts. 5 y 8 a 10 | 4, 6 | **VERIFICADA** contra el Digesto municipal |

**URLs de la normativa**

- Constitución PBA (texto oficial): `https://normas.gba.gob.ar/constitucion-de-la-provincia-de-buenos-aires-1994`
- LOM, Decreto-Ley 6769/58 (texto oficial): `https://normas.gba.gob.ar/documentos/OVG48SW0.html`
- Pinamar, Ordenanza 7124/2025: `https://sibom.slyt.gba.gob.ar/bulletins/14382/contents/2343293`
- Pinamar, Decreto 2099/2025 (el veto): `https://sibom.slyt.gba.gob.ar/bulletins/14388/contents/2344255`

*Capturas de septiembre de 2026.*

---

## 2. Los tres límites de este documento

La introducción los enuncia. Acá están desarrollados.

### 2.1 Los otros 105 municipios no están validados uno por uno

El archivo `rafam_2025_106_municipios.csv` proviene de **La Verdadera PBA** (`https://la-verdadera-pba.pages.dev`), capturado el 3 de septiembre de 2026. Es un sitio de terceros que procesa datos oficiales del RAFAM provincial. **No es la fuente oficial.**

- **San Isidro sí está validado:** coincide al millón con el estado de ejecución 2025 del propio Municipio, en las siete categorías del gasto por objeto.
- **Los otros 105, no.** Lo único que se verificó de ellos es su consistencia interna: `03_scripts/parse_rafam.py` recalcula los dos porcentajes desde los importes devengados de cada planilla y falla si alguno difiere más de 0,05 puntos del declarado. Los 106 coinciden. Eso dice que cada planilla es consistente consigo misma, no que sea la cifra oficial.

**Qué se apoya en ellos:** la mediana provincial (50,7% en personal, 5,4% en obra pública) y la posición de San Isidro (puesto 20 y puesto 4 de 106). Si alguno de los 105 estuviera mal, lo que se mueve es la mediana o el puesto, **no el valor de San Isidro**.

### 2.2 El Municipio cambió su nomenclador de funciones en 2025

En 2024 San Isidro clasificó su gasto en **catorce funciones**; en 2025, en **veinte**. Aparecieron siete que antes no existían —entre ellas Vivienda y urbanismo con 13.917 millones constantes, y Ciencia y técnica con 9.200— y desaparecieron dos.

**Qué se apoya en esto:** toda comparación interanual por función. El documento usa **cuatro** —Seguridad interna, Ecología, Salud y Educación—, que existen en los dos ejercicios y cuya finalidad no incorporó funciones nuevas. La de Seguridad es la más firme: Seguridad interna es la única función de su finalidad en los dos años, así que no hay dónde esconder un desdoblamiento.

**Lo que quedó afuera por esto:** tres variaciones superiores al 100% —Transporte, Comercio y Agua potable—, que son reclasificaciones puras. Y la caída del 32,5% en Promoción y asistencia social, que el documento **no usa** porque no puede distinguirse un recorte de un desdoblamiento hacia las funciones nuevas de la misma finalidad.

### 2.3 No existe dato público del costo de financiamiento del Municipio

El Municipio publica su stock de deuda y sus amortizaciones, pero no la tasa a la que se financia.

**Qué se apoya en esto:** nada. Es la razón por la que este programa **no propone endeudarse**. El capítulo 3 modela la opción con tres tasas reales alternativas y la declara como un vacío, no como un cálculo. Sin el dato, cualquier número sería inventado.

---

## 3. Lo que no se pudo consultar

| Qué falta | Por qué | Qué habría aportado |
|---|---|---|
| **Portal de Datos Abiertos municipal** (`datos.sanisidro.gob.ar`) | Devuelve **error 504**. Confirmado desde dos entornos distintos en septiembre de 2026. | Series municipales que hoy no están en ningún otro lado. Es, además, una de las medidas de transparencia del capítulo 6. |
| **Transferencias provinciales 2003–2020** (12 archivos XLSX) | El host `www.ec.gba.gov.ar` no acepta conexiones desde el entorno de descarga. Las series 2003–2015 agregadas y los cortes a diciembre de 2016 a 2020. | Extendería la serie de coparticipación de cinco a veintitrés años. El parámetro de caída del coeficiente se calculó sobre 2021–2025. |
| **Anexo de zonas de la Ordenanza 6045/1984** | No está publicado en el Digesto municipal. El art. 5 lo menciona; el anexo no aparece. | Los límites oficiales de las zonas vecinales. Por eso la zonificación de este documento se construyó desde los 360 radios censales y se declara como propuesta, no como límite oficial. |
| **Rendiciones de cuentas 2013, 2016, 2018 y 2023–2026** | El Municipio no las publicó. La última publicada es la de 2022. | Cerrarían la serie de gasto real. Los huecos quedan a la vista en el cuadro del capítulo 1: no se interpolaron. |
| **Gastos por objeto del III trimestre de 2025** | El Municipio subió por error el PDF de "gastos por finalidad y función" duplicado. El archivo correcto no existe en el sitio. | Un trimestre de la serie por objeto. |
| **Los decretos de Pilar que contratan cooperativas bajo el art. 132 inc. c)** | No se localizaron en el Boletín Oficial Municipal. El capítulo 4 cita el precedente; los expedientes concretos no están en este repositorio. | El circuito administrativo completo: quién inicia el expediente, cómo se acredita el 60% de adhesión, qué dictámenes intervienen, cómo se certifica el avance de obra y cómo se paga. **Es el vacío más importante de este anexo** y está señalado como tal en los pendientes del capítulo 4. |
| **Organigrama, planta de personal, DDJJ de funcionarios, compras y licitaciones** | No existen esas secciones en el portal de transparencia. Probadas las URL, devuelven 404. El enlace de "Declaraciones Juradas" lleva a declaraciones de **contribuyentes**. | Son exactamente las medidas que el capítulo 6 se compromete a publicar. Su ausencia **es** el dato. |

---

## 4. Los cuatro artículos que sostienen el capítulo 4

Transcripción literal del texto oficial provincial.

### Ley Orgánica de las Municipalidades, artículo 60
*(Texto según Decreto-Ley 8613/76)*

> Las obras públicas municipales se realizarán por: a) Administración. b) Contratación con terceros. **c) Cooperativas o asociaciones de vecinos.** d) Acogimiento a leyes de la Provincia o de la Nación.

### Ley Orgánica de las Municipalidades, artículo 132
*(Texto según Ley 10706)*

> La ejecución de las obras públicas corresponde al Departamento Ejecutivo. […] Las obras públicas que se realicen por contrato con terceros […] sólo podrán ser adjudicadas cumplido el requisito previo de la licitación. Sin embargo podrán contratarse directamente, sin tal requisito, cuando: […] **c) Se trate de obras de infraestructura realizadas por cooperativas o asociaciones de vecinos.**
>
> […] **Las excepciones que determinan los incisos c) y g) precedentes sólo podrán ser autorizadas siempre que los vecinos lo peticionen en forma expresa y se cuente con la adhesión del sesenta (60) por ciento, como mínimo, de los beneficiarios de las obras.**

### Ley Orgánica de las Municipalidades, artículo 119
*(Texto según Ley 14062, último párrafo)*

> El Departamento Ejecutivo podrá practicar directamente las ampliaciones o creaciones de partidas **que se financien con recursos afectados** que correspondan según el monto de los recursos efectivamente autorizados o realizados y acordes con la finalidad a que deban ser aplicados los aludidos recursos afectados.

### Constitución de la Provincia de Buenos Aires, artículo 211
*(Disposición transitoria)*

> La Ley Orgánica de las Municipalidades deberá contemplar la posibilidad que los municipios accedan a los institutos de democracia semidirecta.

*El artículo 210, también transitorio, fijó para eso un plazo que no debía exceder el período legislativo siguiente a 1994. La Sección VII de la Constitución, del Régimen Municipal (arts. 190 a 197), no menciona consulta popular, referéndum, plebiscito ni iniciativa popular. El Decreto-Ley 6769/58 tampoco.*

---

## 5. Las cuatro hipótesis que se cayeron

El capítulo 2 las desarrolla. Acá van con la fuente que las mató.

| Hipótesis | El dato | Fuente |
|---|---|---|
| "Lanús administra mal el municipio" | Puesto 20 de 106 en menor peso de la planta (34,4% contra una mediana de 50,7%) y puesto 4 en inversión en obra pública (17,8% contra 5,4%) | Ejecución RAFAM 2025 de 106 municipios, con el límite del punto 2.1 |
| "La Provincia castiga a San Isidro por no ser peronista" | Los fondos discrecionales no se movieron un punto básico en cinco años: 1,599% todos los años, hasta el cuarto decimal. Toda la caída está dentro del coeficiente automático de la Ley 10.559 | Planillas de transferencias de la Dirección Provincial de Coordinación Municipal, 2021–2025 |
| "El déficit es culpa de esta gestión" | 2025 cerró con un déficit equivalente al 2,0% de los ingresos. En 2010 fue del 2,9% | Estado de Situación Económico-Financiera, 2010 y 2025 |
| "Esta gestión destruyó el presupuesto municipal" | El gasto real cayó 24,4% entre 2017 y 2025, pero los peores años son anteriores a diciembre de 2023: 2019 (−9,1%), 2020 (−10,4%) y 2021 (−1,7%). Gestión anterior 2017→2022: −17,2%. Gestión actual 2022→2025: −8,8% | Rendiciones de cuentas 2010–2022 y ejecución 2024–2025, deflactadas por IPC |

---

## 6. Cómo reproducir los números

Todo el material de este documento —datos crudos, parsers, modelo fiscal, gráficos y pruebas— está en un repositorio abierto:

**`https://github.com/captainnicholasmoffat/casares-sanisidro-2027`**

```
pip install -r requirements.txt --break-system-packages
```

Las versiones están fijas a propósito: matplotlib decide el ancho de cada glifo, así que con otra versión los veinte gráficos salen distintos aunque el dato sea el mismo.

El orden importa, porque el test del parser reescribe los CSV desde los PDF:

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

**Los cinco tests pasan.** Verifican, entre otras cosas, que el año cero del modelo reproduzca la ejecución 2025 oficial con diferencia cero —un resultado financiero de −6.051.064.048 pesos—, que las identidades contables se cumplan en los treinta y nueve años-escenario proyectados, que las series deflactadas sean consistentes y que los 360 radios censales caigan cada uno en exactamente una zona.

**Los cinco verificadores de gráficos pasan.** Comprueban que ningún gráfico use un color fuera de la paleta, que ningún carácter quede fuera del lienzo, que ningún texto pise a otro, que ninguna palabra pierda su tilde, y que **ningún número esté escrito a mano**: todo lo que un gráfico muestra sale del CSV.

El generador sale con código distinto de cero si cualquiera de los cinco salta.

---

## 7. Nota metodológica: cómo se hizo este documento

Este documento lo produjo un equipo chico. Auditar dieciséis años de ejecución presupuestaria municipal, procesar 360 radios censales y construir un modelo fiscal a diez años no es trabajo que un equipo chico pueda hacer a mano.

Lo que lo hizo posible fue automatizar el procesamiento: **121 archivos de fuentes públicas —89 PDF, 15 respuestas del motor censal, 13 planillas y 3 CSV— parseados con herramientas de software**, y cada cifra resultante sujeta a una prueba automática que la verifica contra el dato de origen.

Eso tiene una consecuencia que conviene decir con todas las letras: **los errores existieron y quedaron registrados.** Una mediana calculada sobre el valor 54 de una lista par en vez del promedio de los dos centrales. Una cantidad de hogares derivada de un porcentaje ya redondeado en lugar de contada. Una tasa de percepción redondeada a dos decimales antes de restarla de la meta. El subtítulo de un gráfico con un número escrito a mano que habría sobrevivido a la siguiente corrida diciendo lo que ya no era cierto.

Los cuatro se encontraron **porque el código está escrito y se puede volver a correr**, no porque alguien los notara leyendo. Están documentados con su cálculo y su corrección en `CORRECCIONES_NUMERICAS.md`, en el mismo repositorio.

De ahí sale la regla que gobierna todos los datos de este documento: **cuando existe el conteo, se usa el conteo.** Los porcentajes son para mostrar, nunca para calcular otra cosa encima.

Esto no se cuenta como alarde. Se cuenta por dos razones.

La primera es que explica por qué un equipo sin estructura pudo hacer una auditoría de este tamaño, y por lo tanto que **cualquier otro equipo también puede**. El método no es propiedad de nadie: son fuentes públicas, herramientas comunes y código abierto.

La segunda es que es la única forma de que la afirmación central de este documento signifique algo. Un programa de gobierno que dice "los números están bien" pide confianza. Éste dice dónde están los números, con qué se los verificó y cómo volver a correrlos.

**La invitación es literal: correlo, y si algo no cierra, decilo.**
