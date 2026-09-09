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
| SIBOM — tres decretos de Pilar bajo el art. 132 inc. c) | El precedente de contratación directa a cooperativas de vecinos, y la acreditación de la adhesión | 4 | **VERIFICADA** |

### 1.3 Nacionales

| Fuente | Qué aporta | Capítulos | Estado |
|---|---|---|---|
| Censo Nacional 2022 (INDEC), por radio censal | Los seis indicadores territoriales | 1, 4, 5, 6 | **VERIFICADA** |
| OpenStreetMap, relaciones administrativas de localidad | Los límites de las seis zonas | 1, 4, 5, 6 | **PROCESADA POR TERCEROS** — ver 2.4 |
| IPC INDEC, 2016–2026 | Deflactor de todas las series | 1, 3, 5 | **VERIFICADA** |
| IPC San Luis, 2010–2016 | Empalme del deflactor anterior a diciembre de 2016 | 1, 3 | **VERIFICADA**, con el empalme declarado |

### 1.4 Normativa

| Fuente | Qué aporta | Capítulos | Estado |
|---|---|---|---|
| Constitución de la Provincia de Buenos Aires (1994) | Arts. 190, 192, 193, 211 | 4, 6 | **VERIFICADA** contra el texto oficial |
| Decreto-Ley 6769/58, Ley Orgánica de las Municipalidades | Arts. 24, 60, 119, 132 | 4, 6 | **VERIFICADA** contra el texto oficial provincial |
| Ordenanza 6045/1984 de San Isidro, y su modificatoria 7164/1993 | Régimen de asociaciones vecinales, arts. 5 y 8 a 10 | 4, 6 | **VERIFICADA** contra el Digesto municipal |

**Las seis localidades en OpenStreetMap.** Cualquiera puede abrirlas en `openstreetmap.org/relation/<id>`:

| Localidad | Relación |
|---|---|
| San Isidro | 1877221 |
| Béccar | 1770851 |
| Martínez | 1770849 |
| Acassuso | 1877206 |
| Boulogne Sur Mer | 1770848 |
| Villa Adelina | 1770850 |

*Capturadas en septiembre de 2026 vía Nominatim. Los cuatro partidos vecinos —San Fernando 2443418, Tigre 2411762, General San Martín 1719022, Vicente López 2752665— se usan sólo para definir la línea de costa por descarte, en el verificador geográfico.*

**URLs de la normativa**

- Constitución PBA (texto oficial): `https://normas.gba.gob.ar/constitucion-de-la-provincia-de-buenos-aires-1994`
- LOM, Decreto-Ley 6769/58 (texto oficial): `https://normas.gba.gob.ar/documentos/OVG48SW0.html`
- Pinamar, Ordenanza 7124/2025: `https://sibom.slyt.gba.gob.ar/bulletins/14382/contents/2343293`
- Pinamar, Decreto 2099/2025 (el veto): `https://sibom.slyt.gba.gob.ar/bulletins/14388/contents/2344255`

**Pilar — contratación directa a cooperativas de vecinos bajo el art. 132 inc. c)**

- Expediente municipal Nº 144/2019, Cooperativa de Trabajo Nueva Unión Ltda., Barrio Los Cachorros, Manuel Alberti: `https://sibom.slyt.gba.gob.ar/bulletins/2049/contents/1312293`
  **Es el que documenta el requisito de adhesión.** Consta textualmente que *"se cumplimentó con lo establecido por el artículo mencionado en el párrafo anterior, acreditándose la adhesión de los vecinos beneficiarios de las obras."*
- Ente Coordinador de Cooperativas, 600 m² de veredas, Barrio Río Luján: `https://sibom.slyt.gba.gob.ar/bulletins/269/contents/1155763`
  Encomienda directa a cooperativa *"en concordancia con lo previsto en el artículo 132 inc. c) de la Ley Orgánica Municipal"*.
- Secretaría de Obras Públicas, Cooperativa de Trabajo Unión y Progreso Limitada, fresado y reconstitución de pavimento: `https://sibom.slyt.gba.gov.ar/bulletins/234/contents/1148249`
  Mismo encuadre. *(El SIBOM publica bajo dos dominios, `.gob.ar` y `.gov.ar`. Esta URL usa el segundo; no es un error de transcripción.)*

*Capturas de septiembre de 2026.*

---

## 2. Los límites de este documento

La introducción enuncia tres. Acá están desarrollados, y va un cuarto que la introducción no alcanza a nombrar.

### 2.1 Los otros 105 municipios no están validados uno por uno

El archivo `rafam_2025_106_municipios.csv` proviene de **La Verdadera PBA** (`https://la-verdadera-pba.pages.dev`), capturado el 3 de septiembre de 2026. Es un sitio de terceros que procesa datos oficiales del RAFAM provincial. **No es la fuente oficial.**

- **San Isidro sí está validado:** coincide al millón con el estado de ejecución 2025 del propio Municipio, en las siete categorías del gasto por objeto.
- **Los otros 105, no.** Lo único que se verificó de ellos es su consistencia interna: `03_scripts/parse_rafam.py` recalcula los dos porcentajes desde los importes devengados de cada planilla y falla si alguno difiere más de 0,05 puntos del declarado. Los 106 coinciden. Eso dice que cada planilla es consistente consigo misma, no que sea la cifra oficial.

**Qué se apoya en ellos:** la mediana provincial (50,7% en personal, 5,4% en obra pública) y la posición de San Isidro (puesto 20 y puesto 4 de 106). Si alguno de los 105 estuviera mal, lo que se mueve es la mediana o el puesto, **no el valor de San Isidro**.

### 2.2 El Municipio cambió su nomenclador de funciones en 2025

En 2024 San Isidro clasificó su gasto en **catorce funciones**; en 2025, en **veinte**. Aparecieron siete que antes no existían —entre ellas Vivienda y urbanismo con 13.917 millones constantes, y Ciencia y técnica con 9.200— y desaparecieron dos.

**Qué se apoya en esto:** toda comparación interanual por función. El documento usa **cuatro** —Seguridad interna, Ecología, Salud y Educación—, que existen en los dos ejercicios y cuya finalidad no incorporó funciones nuevas. La de Seguridad es la más firme: Seguridad interna es la única función de su finalidad en los dos años, así que no hay dónde esconder un desdoblamiento.

**Lo que quedó afuera por esto:** tres variaciones superiores al 100% —Transporte, Comercio y Agua potable—, que son reclasificaciones puras. Y la caída del 32,5% en Promoción y asistencia social, que el documento **no usa** porque no puede distinguirse un recorte de un desdoblamiento hacia las funciones nuevas de la misma finalidad.

### 2.3 Los límites de las localidades son de OpenStreetMap, no de un organismo

La Municipalidad de San Isidro **no publica los límites de sus localidades**. El Censo devuelve una sola localidad censal para los 360 radios; BAHRA y el servicio georef nacional dan las seis entidades como puntos, no como polígonos; y el anexo de zonas del artículo 5 de la Ordenanza 6045/1984, que los definiría, tampoco está publicado.

OpenStreetMap sí las tiene, como relaciones administrativas con polígono, y eso es lo que usa este documento. **No es fuente oficial**, y por eso la etiqueta de los cuadros por zona dice OpenStreetMap y no otra cosa.

Lo que sí se puede afirmar de la capa: cubre el 99,63% del partido, las seis no se solapan entre sí, y **los 360 radios censales caen cada uno dentro de exactamente una localidad**, sin huérfanos y sin dobles.

**La regla de asignación, y su desempate.** Cada radio va a la localidad que contiene su punto representativo —el punto representativo y no el centroide, porque en un polígono con forma de L el centroide puede caer afuera—. Si un radio no cayera dentro de ninguna, va a la localidad más cercana desde ese mismo punto. **Ese desempate hoy no se usa: los 360 caen adentro.** Se documenta igual, porque una regla decidida sobre la marcha el día que haga falta no es una regla.

**Qué se apoya en esto:** todos los indicadores por zona del capítulo 1, el reparto del capítulo 4 y los conteos por zona del capítulo 5. Los totales del partido —297.282 habitantes, 25.165 hogares sin gas de red, 6.488 sin cloaca— no dependen de la zonificación y no cambian con ella.

### 2.4 No existe dato público del costo de financiamiento del Municipio

El Municipio publica su stock de deuda y sus amortizaciones, pero no la tasa a la que se financia.

**Qué se apoya en esto:** nada. Es la razón por la que este programa **no propone endeudarse**. El capítulo 3 modela la opción con tres tasas reales alternativas y la declara como un vacío, no como un cálculo. Sin el dato, cualquier número sería inventado.

---

## 3. Lo que no se pudo consultar

| Qué falta | Por qué | Qué habría aportado |
|---|---|---|
| **Portal de Datos Abiertos municipal** (`datos.sanisidro.gob.ar`) | Devuelve **error 504**. Confirmado desde dos entornos distintos en septiembre de 2026. | Series municipales que hoy no están en ningún otro lado. Es, además, una de las medidas de transparencia del capítulo 6. |
| **Transferencias provinciales 2003–2020** (12 archivos XLSX) | El host `www.ec.gba.gov.ar` no acepta conexiones desde el entorno de descarga. Las series 2003–2015 agregadas y los cortes a diciembre de 2016 a 2020. | Extendería la serie de coparticipación de cinco a veintitrés años. El parámetro de caída del coeficiente se calculó sobre 2021–2025. |
| **Rendiciones de cuentas 2013, 2016, 2018 y 2023–2026** | El Municipio no las publicó. La última publicada es la de 2022. | Cerrarían la serie de gasto real. Los huecos quedan a la vista en el cuadro del capítulo 1: no se interpolaron. |
| **Gastos por objeto del III trimestre de 2025** | El Municipio subió por error el PDF de "gastos por finalidad y función" duplicado. El archivo correcto no existe en el sitio. | Un trimestre de la serie por objeto. |
| **El anexo de zonas de la Ordenanza 6045/1984** | No está publicado en el Digesto municipal. El art. 5 lo menciona; el anexo no aparece. | Los límites oficiales de las zonas vecinales. **Dejó de ser una carencia de este documento**: los límites ya no se construyen, se toman de OpenStreetMap, que cualquiera puede verificar. Queda como contexto: el Municipio no publica ni sus localidades ni sus zonas vecinales. |
| **El circuito administrativo del art. 132 inc. c)** | Los tres decretos de Pilar muestran el encuadre y el resultado, no el trámite paso a paso. | Quién inicia el expediente, cómo se acredita la adhesión, qué dictámenes intervienen, cómo se certifica el avance de obra y cómo se paga. **Es el vacío más importante de este anexo.** El precedente está verificado; el procedimiento no está reconstruido. |
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

## 6. El mapa que se descartó, y por qué

Este documento tuvo un mapa anterior. Está contado acá porque **la forma en que se encontró dice más sobre el método que el resultado final**.

### Qué tenía el primero

Las seis zonas se generaban haciendo crecer seis semillas —los puntos que BAHRA publica para cada localidad— por radios censales vecinos, hasta **equilibrar población**. El algoritmo cumplió lo que se le pidió: seis zonas de entre 41.213 y 55.157 habitantes.

Para lograrlo tuvo que estirar las zonas costeras hacia el interior, porque la densidad del partido es desigual. El resultado no era un mapa de San Isidro:

- **Acassuso**, una localidad costera chica entre Martínez y San Isidro, medía el **87% del ancho del partido** y llegaba al límite oeste, a diez kilómetros del río.
- **San Isidro y Béccar quedaban sin costa**, teniéndola las dos.
- El punto **más al norte del partido**, el que limita con San Fernando, caía en San Isidro y no en Béccar.

Nadie lo había verificado nunca contra un mapa base. Se detectó superponiendo el geojson sobre un callejero real.

### El cambio de método, y qué se puede discutir de él

**El equilibrio poblacional nunca fue necesario.** La fórmula del capítulo 4 ya pondera por población y por necesidad: zonas desparejas no rompen nada, porque la fórmula les da montos distintos y eso es exactamente lo que hace.

Así que la restricción se dio vuelta: **la geografía manda y la población es un resultado que se reporta, no una meta que se persigue.** Las seis zonas actuales van de 11.035 a 74.832 habitantes.

Es una decisión metodológica y se puede discutir. Quien prefiera zonas parejas tiene que aceptar que dejen de coincidir con las localidades que los vecinos nombran, y el capítulo 4 depende de que un vecino reconozca su barrio.

### El índice, de tasas a hogares

El mismo cambio de mapa dejó al descubierto un segundo problema, en la fórmula de reparto.

El índice de necesidad **promediaba tasas**. Un porcentaje no sabe cuánta gente hay detrás: Acassuso, con 936 hogares sin gas de red, entraba a la fórmula por una escala parecida a Béccar, que tiene 8.221. Con el índice en tasas, **Acassuso quedaba primera en pesos por habitante teniendo el NBI más bajo del partido**.

Con el índice en hogares queda quinta. **Es el caso donde el conteo contra la tasa no corrigió una cifra impresa sino una decisión**: reparte los 28.908 millones de la partida vecinal de otra manera.

### El control que ahora lo impediría

De ese episodio salió un séptimo verificador que corre cinco referencias geográficas que no se discuten, y falla si alguna no se cumple. La línea de costa se define **por descarte**: se restan del contorno del partido los cuatro partidos vecinos, y lo que no comparte con ninguno es el río.

Corrido sobre el mapa descartado, da esto:

```
COSTA (borde del partido que no comparte con ningun vecino)
  Acassuso           costa       3703 m de ribera  esperado costa     OK
  Beccar             sin costa      0 m de ribera  esperado costa     FALLA
  Boulogne Sur Mer   sin costa      0 m de ribera  esperado sin costa OK
  Martinez           sin costa    353 m de ribera  esperado costa     FALLA
  San Isidro         costa       3378 m de ribera  esperado costa     OK
  Villa Adelina      sin costa      0 m de ribera  esperado sin costa OK

MAS AL NORTE (limita con San Fernando)
  San Isidro         esperado Beccar             FALLA

COMPACIDAD (ancho de cada zona sobre el ancho del partido)
  Acassuso            87%  FALLA

FALLA: 4 referencias geograficas no se cumplen.
```

**Cuatro fallas**, incluida una que a ojo no se veía: Martínez tenía 353 metros de ribera, apenas rozando el río.

Sobre el mapa actual el verificador da cero, y corre con los otros seis cada vez que se regeneran los gráficos.

---

## 7. Cómo reproducir los números

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

## 8. Nota metodológica: cómo se hizo este documento

Este documento lo produjo un equipo chico. Auditar dieciséis años de ejecución presupuestaria municipal, procesar 360 radios censales y construir un modelo fiscal a diez años no es trabajo que un equipo chico pueda hacer a mano.

Lo que lo hizo posible fue automatizar el procesamiento: **121 archivos de fuentes públicas —89 PDF, 15 respuestas del motor censal, 13 planillas y 3 CSV— parseados con herramientas de software**, y cada cifra resultante sujeta a una prueba automática que la verifica contra el dato de origen.

Eso tiene una consecuencia que conviene decir con todas las letras: **los errores existieron y están contados.** Son siete, y están en `CORRECCIONES_NUMERICAS.md` con su cálculo y su corrección.

**Los cuatro primeros son de cálculo.** Una mediana tomada del valor 54 de una lista par en vez del promedio de los dos centrales. Una cantidad de hogares derivada de un porcentaje ya redondeado en lugar de contada. Una tasa de percepción redondeada a dos decimales antes de restarla de la meta. El subtítulo de un gráfico con un número escrito a mano que habría sobrevivido a la siguiente corrida diciendo lo que ya no era cierto.

Los cuatro se encontraron **porque el código está escrito y se puede volver a correr**, no porque alguien los notara leyendo. De ellos sale la regla que gobierna todos los datos de este documento: **cuando existe el conteo, se usa el conteo.** Los porcentajes son para mostrar, nunca para calcular otra cosa encima.

**El quinto es de otra clase, y es el más caro.** El mapa de zonas estaba mal: seis zonas construidas por un algoritmo que equilibraba población y deformaba el territorio para lograrlo. Está contado en la sección 6.

Lo que importa acá es por qué ninguno de los controles lo vio. Había seis verificadores de gráficos corriendo, y los seis pasaban. **Controlaban cómo se dibuja un gráfico, ninguno si lo que dibuja es cierto.** Se puede tener un gráfico perfectamente formado que miente: paleta correcta, sin texto fuera del lienzo, sin colisiones, con todas las tildes, sin números escritos a mano — y las zonas en el lugar equivocado. Lo detectó un lector mirando el mapa, no la máquina. De ahí salió el séptimo verificador.

**El sexto es de una clase que tampoco teníamos, y ningún verificador puede atraparlo.** Cuando las zonas pasaron a ser de OpenStreetMap, la etiqueta de confianza de los cuadros por zona siguió diciendo "ZONIFICACIÓN PROPIA". No había nada malformado: el rótulo era correcto el día que se escribió y dejó de serlo cuando cambió lo que describía. **Cambia la fuente y queda un rótulo describiendo la anterior.** Se detectó leyendo, no corriendo código, y por eso está en la lista.

Del mismo tipo, un nivel más abajo, apareció otro que se arregló por analogía: el colocador de etiquetas de los mapas comprobaba que una etiqueta no chocara con otro texto, pero no que entrara en su propio polígono. La de Acassuso, que tiene 16 radios, terminaba flotando fuera del contorno del partido sin nada que la atara. **El control existía y medía la cosa equivocada.**

**El séptimo es el que dice algo sobre el límite de todo este aparato, y por eso va último.**

Uno de los siete verificadores busca números escritos a mano en los textos de los gráficos, porque un número fijo en un título sobrevive a la siguiente corrida diciendo lo que ya no es cierto. Funciona: encontró doce.

Pero **busca dígitos**. Dos títulos de exhibit decían *"Boulogne y Béccar concentran toda la carencia del partido"* y *"la partida vecinal reparte casi el doble por vecino en Béccar que en Martínez"*. Las dos son cuantificaciones —dicen 100% y aproximadamente el doble— y las dos dejaron de ser ciertas cuando cambiaron las zonas: la concentración es del 67% y el reparto es 1,71 veces. Ninguna tenía un dígito, así que el verificador las dejó pasar.

**Un número escrito a mano se detecta. Una afirmación escrita a mano, no.**

Y la conclusión honesta es que **no sabemos automatizarlo.** Detectar que "toda" dejó de ser cierto exige entender la frase, no parsearla. Lo único que se puede hacer es lo que se hizo acá: que la frase se construya del dato, de modo que el título diga 67% porque lo calculó y no porque alguien lo escribió. Pero eso depende de que quien escriba el título lo escriba así, y ningún control lo obliga.

Queda declarado como el límite conocido del método, no como algo resuelto.

Esto no se cuenta como alarde. Se cuenta por dos razones.

La primera es que explica por qué un equipo sin estructura pudo hacer una auditoría de este tamaño, y por lo tanto que **cualquier otro equipo también puede**. El método no es propiedad de nadie: son fuentes públicas, herramientas comunes y código abierto.

La segunda es que es la única forma de que la afirmación central de este documento signifique algo. Un programa de gobierno que dice "los números están bien" pide confianza. Éste dice dónde están los números, con qué se los verificó, cuáles estuvieron mal y cómo volver a correrlos.

**Siete errores contados es una cifra rara en un documento como éste, y es a propósito.** Un anexo que declara cero está diciendo que nadie revisó, o que revisó y no lo cuenta. Y son siete y no seis porque el séptimo apareció después de dar la lista por cerrada: parar en un número redondo habría sido otra forma de no contarlos.

Hay además un límite que se conoce y no se intenta resolver. El verificador de acentos tiene una lista de palabras que en español siempre llevan tilde, y falla si alguna aparece sin ella. "Está" no puede estar en esa lista, porque "esta" también es una palabra correcta: un verificador que no distingue *esta zona* de *está concentrada* daría falsos positivos en todo el documento, y un verificador ruidoso enseña a ignorar la suite entera. El título del EXHIBIT 16 tuvo esa falta de tilde y la encontró un lector.

**La invitación es literal: correlo, y si algo no cierra, decilo.**
