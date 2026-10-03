# 19 · Multas: ¿la rebaja puede ser automática?

Programa San Isidro 2027 · Investigación al 03/10/2026.

**Fuentes:**
- **Normas ya guardadas en la octava parte:** `01_raw/multas/1_ley_y_montos/` y `01_raw/multas/4_idea_del_cliente/`. Ahí están la Ley 24.449, la Ley 13.927, el Decreto 532/09, el Decreto-Ley 8751/77, la Ley Orgánica de las Municipalidades (LOM), el Código Penal, la Ley 25.326 y las ordenanzas de Baradero y Chivilcoy.
- **Lo nuevo:** en `01_raw/multas_automaticas/`.

**Marcas:** [verificado] = lo leí en la norma. [inferencia] = interpretación mía. Lo que es opinión jurídica dice además «necesita dictamen de un abogado».

**Lo ya decidido por el cliente:**
- **Las multas no pueden ser regresivas.** Si la rebaja depende de que el vecino vaya al juzgado a pedirla, no sirve: quien no tiene tiempo no va.
- **El diseño:**
  1. Una ordenanza fija el criterio.
  2. El vecino le dice una sola vez a la inteligencia artificial del Municipio su ingreso y cuántos viven en su hogar.
  3. Cuando sale una multa, la IA calcula el monto rebajado y la cuota.
  4. El Juez de Faltas lo revisa y lo firma.
- **Cuota máxima por mes:** 2% del ingreso dividido por la raíz de la cantidad de personas del hogar, sumando todas sus multas. Sin plazo máximo.

---

## Respuestas en una línea

1. **SÍ, en la sentencia y dentro del rango.**
   - El juez resuelve sin que la persona se presente (Ley 13.927, art. 35 g).
   - Puede mirar la situación económica y fijar cuotas (Ley 24.449, arts. 85 c y 90; Código Penal, art. 21).
   - [verificado el texto; que valga de oficio con datos declarados antes: inferencia, necesita dictamen de un abogado]
2. **NO.** El pago voluntario es fijo: el mínimo menos 50%. Las cuotas generales las da sólo la Provincia (Decreto 532/09, Anexo I, art. 33 b; Anexo III, art. 40). [verificado]
   - **Qué tendría que cambiar la Provincia:** un decreto del Gobernador que reforme esos dos artículos para un pago voluntario rebajado según el ingreso, y una disposición de la Dirección Provincial de Política y Seguridad Vial con cuotas a este tope. No hace falta una ley. [inferencia]
3. **NO en multas: todos los precedentes que encontré son a pedido** (Castelli 2026, Rauch 2020, Balcarce 2022 y 2025, Pinamar 2022, Luján de Cuyo 2025). **SÍ de oficio en tasas y servicios:** Quilmes (exención de tasa a jubilados, Decreto 762/2020) y la tarifa social de energía por cruce de datos (2016-2019). [verificado]
4. **Velocidad:**
   - Va de 150 a 1.000 UF ($342.150 a $2.281.000), y el pago voluntario es $171.075 (Decreto 532/09, Anexo V, art. 28). [verificado; pesos: cálculo propio]
   - **Hoy no se puede bajar del pago voluntario.** Con un decreto provincial podría bajar hasta $57.025 (25 UF), y por debajo hace falta ley nacional (Ley 24.449, art. 84). [inferencia]
5. **NO SE SABE.**
   - Las cuotas las fija el juez (Ley 24.449, art. 85 c).
   - Baradero fue para deuda vieja y a pedido. Chivilcoy fue una rebaja automática, pero transitoria y no según el ingreso.
   - Sirven como antecedente de que un Concejo regule el pago de multas, no de un plan permanente para multas nuevas. [verificado los textos; el alcance: inferencia, necesita dictamen de un abogado]
6. **SÍ, con condiciones** (Ley 25.326). [verificado las normas; la aplicación: inferencia, necesita dictamen de un abogado]
   - El ingreso y el hogar no son datos sensibles (art. 2).
   - Hace falta consentimiento libre, expreso e informado (arts. 5 y 6).
   - Los datos se usan sólo para las multas (art. 4.3).
   - La base se crea por ordenanza publicada y se inscribe (arts. 21 y 22).
   - Hace falta un contrato con el proveedor de la IA (art. 25).
   - Una persona decide, porque un acto no puede fundarse sólo en un tratamiento automatizado (art. 20).

---

## Las seis respuestas

**1 · ¿Puede el juez bajar la multa hacia el mínimo y dar cuotas de oficio, sin que la persona se presente? — SÍ, en la sentencia, dentro del rango. Necesita dictamen de un abogado.**
- **El juez resuelve sin la persona:** si el infractor no paga ni presenta descargo, "el Órgano de Juzgamiento resolverá" igual, sin otra sustanciación (Ley 13.927, art. 35 g; Decreto 532/09, Anexo I, art. 35). [verificado]
- **Puede mirar la situación económica:** la Ley 24.449 (art. 90) aplica en subsidio la parte general del Código Penal. El art. 21 de ese Código manda fijar la multa "teniendo en cuenta… la situación económica" y dice que "el tribunal fijará el monto y la fecha de los pagos, según la condición económica". [verificado el texto]
- **Las cuotas para "infractores de escasos recursos"** las fija "la autoridad de juzgamiento" (Ley 24.449, art. 85 c). Ninguna de esas normas exige que la persona las pida. [verificado el texto; que valga de oficio y con datos declarados antes: inferencia]
- **La ordenanza no puede darle órdenes al juez:** sólo puede fijar el criterio como guía y crear el registro de declaraciones. El juez es independiente (Decreto-Ley 8751, arts. 21 y 22). [verificado el texto; el alcance: inferencia]

**2 · ¿El pago voluntario se puede ofrecer ya rebajado y en cuotas? — NO, hoy no.**
- **El monto:** es el mínimo de la infracción menos 50%, por decreto provincial (Decreto 532/09, Anexo I, art. 33 b, y Anexo III, art. 40). [verificado]
- **Las cuotas:** sólo puede disponerlas "con alcance general" la Dirección Provincial de Política y Seguridad Vial (mismo art. 33 b). [verificado]
- **Qué tendría que cambiar la Provincia, en una línea:** un decreto del Gobernador que reforme esos dos artículos para permitir un pago voluntario rebajado según el ingreso, y una disposición de la Dirección Provincial que habilite cuotas con este tope. No hace falta una ley. [inferencia]

**3 · ¿Hay precedentes argentinos de rebajas o cuotas de oficio según el ingreso? — En multas, NO: todos los que encontré son a pedido.** Ver la sección 3.

**4 · Exceso de velocidad** [verificado el rango; pesos con la UF de $2.281: cálculo propio]
- **El rango:** de 150 a 1.000 UF, es decir, de $342.150 a $2.281.000 (Decreto 532/09, Anexo V, art. 28).
- **El pago voluntario:** 75 UF, $171.075.
- **Hasta cuánto se puede bajar:**
  - **Hoy, en el pago voluntario:** nada por debajo de $171.075.
  - **Hoy, por sentencia:** el mínimo, $342.150, que es el doble del pago voluntario. Con el atenuante por falta intrascendente (Ley 24.449, art. 79: un tercio menos) quedan $228.100. [inferencia]
  - **Con un decreto del Gobernador que cambie el Anexo V:** el mínimo puede bajar hasta 50 UF ($114.050), y el pago voluntario hasta 25 UF ($57.025).
  - **Por debajo de 50 UF:** hace falta una ley nacional (Ley 24.449, art. 84).

**5 · ¿Puede una ordenanza fijar un plan de pagos para multas nuevas con ese tope? — NO SE SABE. Necesita dictamen de un abogado.**
- **Las cuotas de una multa ya sentenciada las fija el juez,** no el Concejo (art. 85 c). [verificado]
- **Baradero (Ordenanza 5651/2018):**
  - Fue "de modo excepcional", por 6 meses, para multas ya sentenciadas.
  - Daba 50% de quita y 6 cuotas, sólo a quien se adhería.
  - **Sirve como antecedente de que un Concejo regule el pago de multas de su juzgado; no sirve para multas nuevas ni para cuotas automáticas.** [verificado el texto; el alcance: inferencia]
- **Chivilcoy (Ordenanza 9806/2020):**
  - Redujo al 30% todas las multas de tránsito de su juzgado, **sin que nadie lo pidiera**, incluidas las que estaban en pago voluntario.
  - Fue temporal (hasta diciembre de 2020) y se perdía si el infractor presentaba descargo.
  - **Es el antecedente más cercano a "automático", pero no se basó en el ingreso.** No encontré que un juez lo haya revisado. [verificado el texto]
- **Para multas nuevas y para siempre,** lo más seguro es que la ordenanza cree el registro y el criterio, y que el juez aplique las cuotas en cada sentencia (punto 1). [inferencia]

**6 · ¿Qué permite la Ley 25.326? — SÍ, con condiciones.** Ver la sección 6.

---

## Cómo quedaría el circuito, con lo que se puede hoy

1. **El vecino se anota una vez** (ingreso y personas del hogar) y acepta que el dato se use sólo para sus multas.
2. **Llega la multa** con la notificación de siempre, que ofrece el pago voluntario de $171.075. La IA le muestra cuál sería su cuota si no paga en ese momento.
3. **Si no paga en 30 días,** el juez dicta sentencia sin que el vecino vaya:
   - aplica el mínimo ($342.150);
   - fija las cuotas con el tope del 2% dividido por la raíz del hogar;
   - la IA lo preparó y el juez lo firma.
4. **El problema que queda:** por sentencia el monto mínimo es el doble del pago voluntario. Quien menos tiene termina debiendo más, aunque en cuotas chicas. **Para que la rebaja llegue al pago voluntario hace falta el cambio provincial del punto 2.**

### Ejemplos con la cuota máxima [cálculo propio]

| Caso | Cuota máxima por mes | Pago voluntario ($171.075) | Mínimo por sentencia ($342.150) | 10 multas al mínimo |
|---|---|---|---|---|
| Ingreso de $1 millón, vive solo | $20.000 | 9 cuotas | 18 cuotas | 172 cuotas |
| Ingreso de $1 millón, hogar de 4 | $10.000 | 18 cuotas | 35 cuotas | 343 cuotas |
| Salario mínimo ($391.200), solo | $7.824 | 22 cuotas | 44 cuotas | 438 cuotas |
| Jubilación mínima ($435.749), hogar de 2 | $6.162 | 28 cuotas | 56 cuotas | 556 cuotas |
| Ingreso de $10 millones, solo | $200.000 | 1 cuota | 2 cuotas | 18 cuotas |

**Dos avisos sobre "sin plazo máximo":**
- **Prescripción:** la sanción prescribe a los 5 años (Ley 24.449, art. 89). Entre las causas que interrumpen ese plazo no figura el pago de cuotas. Un plan de más de 60 cuotas podría quedar con saldo prescripto. [verificado el texto; el efecto: inferencia, necesita dictamen de un abogado]
- **La deuda sube con la nafta:** la multa se paga al valor de la unidad de multa del día de pago (Ley 24.449, art. 84). Si la cuota queda fija en pesos y la unidad de multa sube, el plan se alarga. Congelar la deuda en pesos lo puede hacer la Provincia, como en 2020 (Disposición 69/2020). [verificado]

---

## Qué multas alcanza

- **Sólo las que juzga el Juez de Faltas de San Isidro,** es decir, las de calles municipales.
- **Las de rutas provinciales y nacionales** (Panamericana, y según fuentes no oficiales también Márquez, Rolón y Libertador) las juzga el juzgado administrativo provincial, salvo delegación (Ley 13.927, arts. 32 y 33). [verificado el texto; qué avenidas son rutas: probable]
- **El cobro:** las multas se cobran por el sistema provincial y el Banco Provincia. Para cobrar en cuotas, ese sistema tiene que poder hacerlo. [inferencia]

---

## 3 · Precedentes

**En multas: ninguno de oficio según el ingreso.** Todos los que encontré son a pedido. No encontrarlo no prueba que no exista. [verificado en cada fuente]

| Dónde | Qué hace | ¿De oficio? |
|---|---|---|
| **Castelli, Ord. 19/2026** | El Juzgado de Faltas, "previo informe socioeconómico", puede "eximir total o parcialmente", dar cuotas o cambiar la multa por tareas comunitarias, ponderando "la composición de su grupo familiar". Sólo para vehículos abandonados y puestos gastronómicos móviles | No, a pedido |
| **Rauch, Ord. 1419/2020** | Trabajo comunitario en lugar de multa para grupos familiares con ingresos de hasta "dos veces el salario mínimo" | No, con documentos o informe social |
| **Balcarce, Decreto 26/2022 y Ord. 14/2025** | Hasta 8 cuotas; jubilados y personas con discapacidad, 50% menos de intereses | No, con comprobante |
| **Pinamar, Ord. 6148/2022** | Trabajo comunitario o curso para quien acredite que no puede pagar | No, a pedido |
| **Luján de Cuyo (Mendoza), 2025** | Jubilados: multas viales en 10 cuotas sin interés | No, a pedido (noticia oficial; no leí la ordenanza) |
| **Ciudad de Buenos Aires, Ley 451, art. 31** | El juez considera "la situación social y económica del infractor/a y de su grupo familiar" | Caso por caso |
| **Chivilcoy, Ord. 9806/2020** | Todas las multas al 30%, incluido el pago voluntario | **Sí**, pero transitoria y para todos, no según el ingreso |

**De oficio, en tasas y servicios** (para comparar) [verificado salvo indicación]:
- **Quilmes, Decreto 762/2020:**
  - "OTÓRGASE el reconocimiento de oficio de la exención" de la tasa a los jubilados que ya la tenían.
  - Escala según el haber: 100% de exención hasta 1,5 haberes mínimos, 75% hasta 1,75, 50% hasta 2 y 25% hasta 2,25.
  - El jubilado tiene que avisar si cambia su situación.
- **Tarifa social eléctrica 2016:** en la Provincia, el ente regulador eléctrico (OCEBA) mandaba la lista de usuarios al SINTyS, el sistema nacional que cruza datos sociales y tributarios, y éste devolvía quiénes tenían el beneficio, sin que nadie lo pidiera (Res. OCEBA 51/2016). En gas fue automática de 2017 a 2019 y después pasó a ser a pedido.
- **Subsidios a la energía (Decreto 332/2022 y Decreto 943/2025):** es lo más parecido al diseño del cliente.
  - El vecino hace una declaración jurada única de ingresos y convivientes, que no hay que repetir.
  - El Estado la cruza con el SINTyS "de acuerdo con la autorización brindada por cada solicitante".
  - Hay un reclamo gratuito, y la base está inscripta ante la Agencia de Acceso a la Información Pública (AAIP).
- **San Isidro hoy:** la exención de la tasa a jubilados se pide en persona y se renueva presentando papeles. [verificado, página de ARSI]

---

## 6 · Datos personales

**Qué rige:**
- La **Ley 25.326 está vigente.** No encontré una ley nueva aprobada; hay proyectos en el Congreso. [verificado]
- Sus capítulos I a IV rigen en todo el país (art. 44). [verificado]
- En la Provincia rigen además el art. 20 de la Constitución provincial ("Ningún dato podrá registrarse con fines discriminatorios"), la Ley 14.214 (hábeas data) y el Decreto 961/2026, que invita a los municipios a adherir a su marco de datos. [verificado]

**Qué exige, para este diseño** [normas verificadas; aplicación: inferencia, necesita dictamen de un abogado]:

| Tema | Qué dice | Qué implica |
|---|---|---|
| ¿Es dato sensible? | La lista del art. 2 no incluye ingreso ni composición del hogar. Sí incluye salud | No pedir salud ni discapacidad. Si se piden, el dato pasa a ser sensible (art. 7) |
| Consentimiento | "Libre, expreso e informado" (arts. 5 y 6). La AAIP exige comprobar que quien consiente es el titular (Res. 4/2019, criterio 5) | Formulario claro sobre para qué se usa, quién lo ve y qué pasa si no se declara. Validar la identidad, por ejemplo con Mi Argentina. El vecino puede retirarlo |
| Finalidad | Los datos no pueden usarse "para finalidades distintas o incompatibles", y se destruyen cuando dejan de servir (art. 4) | Sólo para multas. No para tasas ni controles fiscales, salvo que se avise antes |
| Crear la base | "Disposición general publicada en el Boletín Oficial… o diario oficial", con finalidad, responsable y oficina de reclamos (art. 22). Inscripción (art. 21) | La ordenanza crea la base. Inscribirla también ante la AAIP es lo prudente |
| Proveedor de la IA | Contrato; actúa "sólo… siguiendo instrucciones" (art. 25). Para sacar datos del país hay reglas (art. 12) | Contrato con el proveedor. Cuidado si los datos se procesan fuera del país: Estados Unidos no figura entre los países "adecuados" de la AAIP |
| Decisión automatizada | Un acto que valore conductas no puede tener "como único fundamento" un tratamiento informatizado; si lo tiene, es "insanablemente nulo" (art. 20). El vecino tiene derecho a que le expliquen la lógica (Res. AAIP 4/2019, criterio 2) | La fórmula, pública y simple. **El juez revisa de verdad y firma.** El vecino puede opinar e impugnar. La IA atiende y prepara; no decide |

**Cómo verificar lo que declara el vecino** [verificado]:
- **SINTyS:** un municipio puede firmar convenio. Necesita una norma propia "autosuficiente" (Res. 312/2018 del Consejo Nacional de Coordinación de Políticas Sociales). La Provincia adhirió en 2002.
- **ARBA:** le debe informar al Municipio (Código Fiscal, art. 163), pero no tiene los sueldos.
- **Certificación negativa de ANSES:** el vecino la baja gratis y prueba que no tiene ingresos registrados. No prueba los ingresos en negro, que son el 44,2% del trabajo según INDEC.
- **Ley provincial 15.430 ("una sola vez"):**
  - Presume autorizada la consulta de datos entre reparticiones, salvo que el vecino se oponga (art. 6).
  - Invita a los municipios a adherir (art. 11). Quilmes adhirió; no encontré que San Isidro lo haya hecho.

---

## Lo que tendría que hacer cada uno

| Quién | Qué | Norma |
|---|---|---|
| Concejo de San Isidro | Ordenanza que crea el registro voluntario, el criterio y la IA como apoyo, con una persona que decide | LOM, art. 27; Ley 25.326 |
| Juez de Faltas | Sentencias en el mínimo con cuotas según el criterio, sin comparecencia | Ley 13.927, art. 35 g; Ley 24.449, arts. 85 c y 90; Código Penal, art. 21 |
| Gobernador | Decreto que permita un pago voluntario rebajado según el ingreso, y que baje mínimos del Anexo V si se quiere | Decreto 532/09, Anexo I, art. 33 b; Anexo III, art. 40; Anexo V |
| Dirección Provincial de Política y Seguridad Vial | Disposición de cuotas con el tope, y deuda congelada en pesos | Decreto 532/09, Anexo I, art. 33 b; antecedente: Disposición 69/2020 |
| Congreso | Sólo si se quiere bajar de 50 UF ($114.050) | Ley 24.449, art. 84 |

---

## Método y límites

- **Respuestas 1, 2, 4 y 5:** las armé leyendo yo los textos ya guardados.
- **Respuestas 3 y 6:** las investigó un agente, y verifiqué en la fuente:
  - el art. 20 y el art. 22 de la Ley 25.326;
  - Castelli, Rauch y Quilmes;
  - la Ley 15.430;
  - el Decreto 332/2022.
- **No encontré:**
  - una rebaja de multas de oficio según el ingreso en ningún municipio;
  - un dictamen de la AAIP sobre si las bases municipales deben inscribirse en el registro nacional;
  - una adhesión de San Isidro al SINTyS o a la Ley 15.430.
- **Todo lo marcado [inferencia] es opinión jurídica** y necesita dictamen de un abogado antes de pasar al programa.


---
---

# Segunda parte · Trabajo en vez de plata, convenio con la Provincia, tribunal en línea y cantidad de multas

Investigación al 03/10/2026.

**Fuentes nuevas:**
- `01_raw/multas_automaticas/s_trabajo_convenio_cantidad/` para los puntos 7, 8 y 10.
- `01_raw/multas_automaticas/r_tribunal_en_linea/` para el punto 9 y la corrección.

Las normas base siguen en `01_raw/multas/1_ley_y_montos/`.

**El cliente descartó que el Municipio adelante las multas.** Por eso no se responden las preguntas del adelanto. Lo que se investigó sobre eso quedó en la carpeta `r_tribunal_en_linea/` y no se usa.

*Donde esta segunda parte corrige a la primera, vale lo de esta segunda parte.*

---

## Corrección a la respuesta 2 de la primera parte

- **La respuesta 2 decía que las cuotas del pago voluntario las da sólo la Provincia. No es así:** Balcarce las da por decreto municipal. [verificado]
  - **Decreto 26/2022:** hasta 8 cuotas.
  - **Decreto 21/2026:** hasta 6 cuotas, que se piden en persona dentro de los 15 días del acta. Se firma un convenio de reconocimiento, y si no se pagan dos cuotas seguidas se pierde el beneficio.
- **La base que usan:** el Código de Faltas (Decreto-Ley 8751/77, art. 16 e) deja las «modalidades» del pago voluntario a «las Ordenanzas, Decretos y Reglamentos Municipales». [verificado]
- **No sé si vale para tránsito,** que tiene un régimen provincial (Decreto 532/09, Anexo I, art. 33 b), ni si el sistema provincial de cobro lo permite. [inferencia, necesita dictamen de un abogado]
- **Lo que cambia:** las cuotas del pago voluntario podrían no necesitar a la Provincia. **El monto rebajado según el ingreso sí la necesita** (ver punto 8).

---

## Respuestas en una línea

**7 · Trabajo en vez de plata: NO SE SABE. Lo más defendible es que lo autorice el juez después de la condena, a pedido del vecino y con una ordenanza que organice el programa. Ofrecerlo «de entrada» no tiene base clara.** [inferencia, necesita dictamen de un abogado]
- **El art. 21 del Código Penal exige condena:** habla de «el condenado» y del «término que fije la sentencia», y llega a tránsito por la Ley 24.449, art. 90, y por el Código de Faltas, art. 3. [verificado]
- **Ese artículo es para antes de convertir la multa en prisión, y en tránsito la multa impaga no se convierte en arresto:** se cobra por vía ejecutiva (Ley 24.449, art. 85 b; Ley 13.927, art. 35 bis). Por eso su aplicación «en lo pertinente» es dudosa. [verificado los textos; el efecto: inferencia]
- **La Provincia ya lo tuvo y lo sacó:** la Ley 11.768 (1996) dejaba al juez «disponer el cumplimiento de tareas comunitarias» si el infractor no pagaba; en 2006 el Gobernador vetó el trabajo comunitario como «única sanción» por los «altos índices de lesiones y mortalidad»; la Ley 13.927 (2008) no lo incluye. [verificado]
- **El pago voluntario es dinero:** el mínimo de la falta menos 50% (Decreto 532/09, Anexo I, art. 33 b). No encontré ninguna norma provincial que deje cambiarlo por trabajo. [verificado; búsqueda en el sistema de normas de la Provincia]
- **Lo que la IA sí puede hacer:** informar la opción y tomar el pedido apenas llega la multa. La decisión tiene que ser una resolución del juez. [inferencia]
- **Pinamar (Ord. 6148/2022) lo hace antes de la sentencia:** el vecino reconoce la falta dentro del plazo de descargo y acredita que no puede pagar. Una jornada de 4 horas vale 50 UF ($114.050, 12,5 UF por hora). Si no cumple, debe la multa sin la rebaja; el seguro lo paga el infractor. [verificado; pesos: cálculo propio]
- **Con la regla de Pinamar:** el pago voluntario por velocidad (75 UF) son 6 horas; el mínimo por sentencia (150 UF), 12 horas. [cálculo propio]
- **Otros precedentes bonaerenses:** Baradero (2019), La Plata (2019), Junín (2019, después de la sentencia), Rauch (2020), Gonzales Chaves (2018, con seguro del Municipio), Capitán Sarmiento (2022), San Andrés de Giles (2023) y Coronel Rosales (2024). Todos por ordenanza. [verificado; Junín: probable, prensa]
- **Uso real:** en Junín, sobre unas 500 sentencias por mes, en dos meses lo pidió una sola persona. De Pinamar no hay datos. [probable, prensa]
- **Riesgos:**
  - **seguro**, para cubrir accidentes durante la tarea;
  - **relación laboral**: la Ley de Contrato de Trabajo, art. 23, presume contrato si hay dependencia;
  - **trabajo forzoso**: el Convenio 29 de la OIT admite el trabajo exigido por «sentencia judicial», y el juez de faltas no es Poder Judicial.
  - Por eso conviene que sea voluntario, sin paga, con tope de horas y nunca para una empresa privada. [verificado los textos; la conclusión: inferencia, necesita dictamen de un abogado]

**8 · Convenio con la Provincia como prueba piloto. Las cuotas: SÍ. El monto según el ingreso: NO por convenio ni por disposición.** [inferencia, necesita dictamen de un abogado]
- **Cuotas.** Hay tres vías:
  - la del juez, caso por caso (Ley 24.449, art. 85 c);
  - la del Municipio, como Balcarce (ver la corrección de arriba);
  - la de la Dirección Provincial de Política y Seguridad Vial, por disposición «con alcance general» (Decreto 532/09, Anexo I, art. 33 b). [verificado]
- **«Alcance general»:** se opone a una medida para una persona determinada, no necesariamente a toda la Provincia. Un plan para todos los infractores de un partido podría entrar. [inferencia, necesita dictamen de un abogado]
- **Precedentes de planes provinciales:** la Disposición 69/2020 (6 o 12 cuotas sin interés por 90 días) y la 26/2021 (prórroga). No encontré ninguna posterior. [verificado; búsqueda en el sistema de normas de la Provincia]
- **Monto según el ingreso.** La ley de tránsito sólo deja que un convenio cambie el **reparto** de la plata, no los montos: «pudiendo modificar la distribución de los ingresos provinciales» (Ley 13.927, art. 42). [verificado]
- **Hace falta al menos un decreto del Gobernador** que cambie el Decreto 532/09. Para cobrar distinto la misma falta según el ingreso, o bajar de la rebaja del 50% que fija la ley nacional (art. 85 a), probablemente haga falta una ley. [inferencia, necesita dictamen de un abogado]
- **El canal para un piloto existe:** la Res. 601/2021, que aprobó el convenio de 2020, prevé «protocolos adicionales» que pasan por la Asesoría General de Gobierno, la Contaduría General y la Fiscalía de Estado. El Municipio no necesita autorización del Concejo para firmar con la Provincia (LOM, art. 41). [verificado]
- **El convenio de 2020 no trae nada sobre cuotas ni ingreso;** el anterior, de 2014, sí listaba entre las sentencias del sistema el «plan de facilidades de pago» y las «tareas comunitarias». [verificado]
- **Precedentes de un trato distinto por municipio:** sólo en el reparto. San Nicolás deja el 10% a la Provincia (Res. 566/2019) y San Isidro el 20% (convenio de 2020). No encontré ninguna prueba piloto de tránsito en un solo municipio. [verificado; búsqueda en el sistema de normas de la Provincia]
- **Igualdad ante la ley** (Constitución Nacional, art. 16; Constitución bonaerense, art. 11):
  - las cuotas, que son una facilidad de pago, tienen riesgo bajo;
  - cobrar distinto la misma falta según el lugar donde se cometió tiene riesgo más alto;
  - lo baja que el piloto sea temporal, con un criterio objetivo como el ingreso y con evaluación;
  - no encontré ningún fallo sobre este punto.
  - [inferencia, necesita dictamen de un abogado]

**9 · ¿El Tribunal de Faltas de San Isidro recibe trámites en línea? SÍ, en parte, por correo electrónico, sin norma que lo regule. Para ampliarlo, lo más seguro es una ordenanza.** [verificado; la norma: inferencia, necesita dictamen de un abogado]
- **Hoy:** la página municipal publica un correo para los pedidos de pago voluntario al 50% y otro para los descargos de fotomultas. Los turnos en línea son para ir en persona. [verificado]
- **Lo que no encontré:**
  - una norma de San Isidro sobre trámites a distancia del Tribunal (revisé los decretos del Boletín de febrero de 2024 a septiembre de 2026);
  - el Reglamento Interno que el Decreto 154/2024 le mandó dictar al Tribunal.
  - [no encontrado]
- **Expediente electrónico municipal:** rige desde 2024 (Ord. 8897 y 9321), pero no tiene trámites del Tribunal, y el uso obligatorio se prorrogó al 01/03/2027. [verificado]
- **Modelos:**
  - **Bragado, Ord. 5398/2021:** domicilio electrónico optativo, descargo por correo en PDF firmado y audiencia virtual, también para tránsito. Es el mejor modelo.
  - **Vicente López, Ord. 36.929:** audiencia por videoconferencia.
  - Castelli y Avellaneda: notificaciones y descargos por medios electrónicos.
  - [verificado]
- **La Provincia** tiene descargo web desde 2019 para sus juzgados (InfraccionesBA). [verificado]
- **Un límite a resolver:** en las faltas que no son de tránsito, el Código de Faltas dice que en la audiencia «no se aceptará la presentación de escritos» (art. 47). La ordenanza tendría que resolverlo con audiencia virtual. [verificado el texto; la salida: inferencia]
- **Para tránsito,** el descargo va «en el lugar y con las formas que establezca la reglamentación» (Ley 13.927, art. 35 g), que es provincial; por eso también podría habilitarse dentro del sistema provincial. [verificado el texto; la vía: inferencia]

**10 · ¿Cuántas multas de tránsito se labran por año en San Isidro? NO HAY DATO PÚBLICO, ni total ni por cámara.** [no encontrado]
- **Lo más cercano son las «infracciones tratadas» del Juzgado de Faltas,** que mezclan tránsito con otras faltas: 146.732 en 2022 y 218.720 en 2024. [verificado, presupuesto 2024 y situación económico-financiera 2024]
- **Desde 2025 el presupuesto mide otra cosa:** «intervenciones» (72.897 en 2025). No sirve para contar multas. [verificado]
- **Las de Panamericana y rutas provinciales** las juzga el juzgado provincial con asiento en General Pacheco; no hay cifras públicas. [verificado el juzgado; cifras: no encontrado]
- **Por cámara:** sólo se sabe, según el Municipio, que tres radares concentraban la mayor cantidad de infracciones (Cuyo 3405, Elcano 1540 y Juan Díaz de Solís 2490) y que fueron reemplazados por reductores de velocidad. [según el Municipio, en La Nación, 20/01/2026]
- **Estimación para 2024: unas 81.000 multas pagadas,** y unas 244.000 labradas si se paga una de cada tres, como calculó la Provincia para sus actas de 2016-2019. El rango posible es enorme: de 13.000 a 456.000. [cálculo propio; supuestos abajo]
- **Lo que costaría la rebaja:** cada 10% de rebaja media cuesta unos $323 M por año a pesos de diciembre de 2025, si todas las «otras multas en vía pública» son de tránsito y la gente paga igual que antes. [cálculo propio]
- **2025 no sirve para calcular:** las cámaras están suspendidas desde el 23/04/2025. [verificado]

---

## 7 · Trabajo en vez de plata: detalle

**Los textos** [verificado]:
- **Código Penal, art. 21:** «Podrá autorizarse al condenado a amortizar la pena pecuniaria, mediante el trabajo libre, siempre que se presente ocasión para ello. También se podrá autorizar al condenado a pagar la multa por cuotas. El tribunal fijará el monto y la fecha de los pagos, según la condición económica del condenado.» Va después de «antes de transformar la multa en la prisión correspondiente, procurará la satisfacción de la primera».
- **Ley 24.449, art. 90:** «es de aplicación supletoria, en lo pertinente, la parte general del Código Penal».
- **Ley 24.449, art. 87 d:** el **arresto** puede ser «reemplazado por la realización de trabajo comunitario». La multa no.
- **Ley 24.449, art. 83, y Ley 13.927, art. 39 bis:** las sanciones son «de cumplimiento efectivo» y no pueden aplicarse «en suspenso». La lista no incluye el trabajo comunitario.
- **Código de Faltas (Decreto-Ley 8751/77), art. 3:** «Las disposiciones de la parte general del Código Penal serán de aplicación para el juzgamiento de las faltas, siempre que no sean expresa o tácitamente excluidas por esta Ley.»
- **Qué procedimiento rige en San Isidro:** el presupuesto 2024 dice que el Juzgado juzga el tránsito «con la aplicación del Código de Faltas… (Ley 8751)». El Código Penal llega entonces por dos vías: la Ley 24.449, art. 90, y el Código de Faltas, art. 3. [verificado el texto; la conclusión: inferencia]

**La historia provincial** [verificado]:

| Año | Norma | Qué decía |
|---|---|---|
| 1996 | Ley 11.768 (modificó el Código de Tránsito, Ley 11.430, art. 137) | «En caso de no verificarse el pago el Juez podrá disponer el cumplimiento de tareas comunitarias a realizar por el infractor.» Después de la sentencia firme |
| 2006 | Ley 13.581 y su veto parcial (Decreto 3200/2006) | Se vetó el trabajo comunitario «como única sanción» porque «adolece de una flexibilidad… que no condice con los altos índices de lesiones y mortalidad» |
| 2007 | Decreto 40/2007 | Tareas comunitarias «en concurrencia» con otras sanciones |
| 2008 | Ley 13.927, vigente | No las incluye |

Esa omisión puede leerse como una exclusión «tácita» en el sentido del art. 3 del Código de Faltas. [inferencia, necesita dictamen de un abogado]

**Precedentes** [verificado salvo indicación]:

| Dónde | Norma | Cuándo se ofrece | Equivalencia | Si no cumple / seguro |
|---|---|---|---|---|
| Pinamar | Ord. 6148/2022 | Antes de la sentencia, con reconocimiento y prueba de que no puede pagar | 50 UF por jornada de 4 horas | Debe la multa sin rebaja. Seguro a cargo del infractor |
| Baradero | Ord. 5901/2019 | Dentro del plazo de la notificación, con reconocimiento | La fija un protocolo del Ejecutivo | Pierde la rebaja |
| La Plata | Ord. 11.883/2019 | La decide el juez | Horas que fija el juez; curso de 10 horas | Agravamiento de la multa |
| Junín | Ord. 7602/2019 | Después de la sentencia (5 días hábiles) | Según el juez | Si cumple, se archiva [probable, prensa] |
| Rauch | Ord. 1419/2020 y Decreto 901/2020 | En la sentencia | Hasta 36 horas | Doble de la multa. El Municipio no responde por accidentes (validez dudosa) |
| Gonzales Chaves | Ord. 3345/2018 | A pedido del juez | Hora = 1,5% del sueldo municipal de la categoría 5 | Seguro a cargo del Municipio |
| Coronel Rosales | Ord. 4302/2024 | El juez convierte la multa (todas las faltas) | Hasta 5 horas por día | El Ejecutivo gestiona el seguro |
| Capitán Sarmiento y San Andrés de Giles | Ord. 2816/2022; Ord. 2617/2023 | El juez convierte la multa | Horas que fija el juez | – |
| Ciudad de Buenos Aires | Ley 451, arts. 32 y 33 | A pedido | Hasta 160 horas, 2 por día | Aumenta la multa |
| Santa Fe | Ley 13.169 | A pedido, sin reincidencia | – | Si no cumple, 1 día = 10 UF |

- **Fallos:** no encontré ninguno de juzgados de faltas o cámaras que aplique el art. 21 (trabajo libre) a multas de tránsito. [no encontrado]
- **La evidencia de afuera:** está en la primera parte del informe 18. En Ciudad de México, cambiar multas por cursos y trabajo comunitario se asoció con más mortalidad vial.

**Para el diseño del cliente** [inferencia, necesita dictamen de un abogado]:
- La IA avisa la opción con la multa y toma el pedido; el juez la autoriza por resolución.
- Hace falta una ordenanza (LOM, arts. 24 y 26) que diga:
  - qué tareas, dónde y con qué supervisión;
  - la equivalencia en horas;
  - quién paga el seguro;
  - qué pasa si no cumple.
- Las tareas no pueden ser para empresas privadas.

---

## 8 · Convenio con la Provincia: detalle

**Los textos** [verificado]:
- **Decreto 532/09, Anexo I, art. 33 b** (texto del Decreto 1350/18): «se aplicará el monto mínimo de UF's correspondiente a la infracción notificada y se le aplicará un descuento del cincuenta por ciento (50%). Queda autorizada la Dirección Provincial de Política y Seguridad Vial para disponer, con alcance general, facilidades de pago en cuotas del monto de las multas e intereses adeudados».
- **Anexo III, art. 40:** la rebaja del 50% «se aplica sobre el valor mínimo de la multa».
- **Ley 13.927, art. 42:** «El Poder Ejecutivo podrá celebrar Convenios de colaboración y asistencia en materia de tránsito… cobro y control de infracciones… pudiendo modificar la distribución de los ingresos provinciales».
- **Decreto 1350/18, art. 3:** faculta a hacer convenios «a fin de procurar la unidad de criterios».
- **Ley 15.078 (Presupuesto 2019), art. 94:** la misma autorización de cuotas «con alcance general», con interés mínimo salvo en planes de hasta 5 cuotas.
- **Disposición 69/2020:** dio 6 o 12 cuotas sin interés por 90 días. En sus considerandos dice que de las actas provinciales de 2016 a 2019 «tan solo un tercio» se pagó.

**Lo que tendría que hacer cada uno para un piloto en San Isidro** [inferencia, necesita dictamen de un abogado]:

| Qué | Quién | Con qué |
|---|---|---|
| Cuotas del pago voluntario con el tope del 2%/√hogar | El Municipio, por decreto o mejor por ordenanza, como Balcarce; o la Dirección Provincial, por disposición | Código de Faltas, art. 16 e; Decreto 532/09, Anexo I, art. 33 b |
| Que el sistema provincial de cobro emita cuotas para San Isidro | La Dirección Provincial y el Municipio | Protocolo adicional al convenio de 2020 (Res. 601/2021, art. 2) |
| Pago voluntario más bajo según el ingreso | El Gobernador, por decreto, y probablemente una ley | Decreto 532/09; Ley 24.449, art. 85 a, por la adhesión de la Ley 13.927, art. 1 |

---

## 10 · Cantidad de multas: detalle

**Metas del Juzgado de Faltas en los presupuestos de San Isidro** [verificado]:

| Año | Qué mide | Programado | Ejecutado |
|---|---|---|---|
| 2022 | Infracciones tratadas | – | 146.732 |
| 2023 | Infracciones tratadas | 120.000 | no publicado |
| 2024 | «Resolución de contravenciones (cantidad infracciones tratadas)» | 154.198 al inicio; 230.809 ajustado | 218.720 (y 76.834 audiencias) |
| 2025 | «Intervenciones» (otra unidad) | 150.000 | 72.897 |
| 2026 | «Intervenciones» | 14.977 | sin dato |

No separan tránsito de las otras faltas y no se sabe si incluyen los pagos voluntarios. De 2019 a 2021 no hay dato.

**La estimación** [cálculo propio]:
- **Fórmula:** multas pagadas = recaudación ÷ (valor medio de la UF × UF por multa × parte que cobra el Municipio).
- **Datos de 2024:**
  - recaudación del subrubro «otras multas en vía pública», $2.207,9 M [verificado];
  - valor medio de la UF, $1.130,5;
  - 75 UF por multa (el pago voluntario por velocidad);
  - 32% para el Municipio, por los convenios con las universidades desde agosto de 2022.
- **Resultado:** unas 81.000 multas pagadas. Si se paga una de cada tres, unas 244.000 labradas, del mismo orden que las 218.720 «infracciones tratadas».
- **Rango:** de 13.000 (150 UF por multa, el Municipio registra el total) a 456.000 (25 UF por multa, 32% para el Municipio y todo el rubro de multas).
- **Supuesto clave:** que todo ese subrubro sea de tránsito. Ningún rubro lo dice.

**Lo que haría falta para un número firme:** las multas de tránsito por año y por equipo del sistema provincial de cobro, o del propio Juzgado. No están publicadas y no se hizo ningún pedido.

---

## Método y límites de la segunda parte

- **Los puntos 7, 8 y 10 los investigó un agente.** Verifiqué en la fuente:
  - el art. 21 del Código Penal y el art. 3 del Código de Faltas;
  - la Ley 11.768 y el veto de 2006;
  - el art. 42 de la Ley 13.927 y el art. 2 de la Res. 601/2021;
  - el art. 41 de la LOM y el art. 94 de la Ley 15.078;
  - el convenio de 2014;
  - la Ordenanza de Pinamar;
  - la Disposición 69/2020;
  - las 218.720 infracciones de 2024;
  - la cifra de la recaudación.
- **El punto 9 y la corrección de Balcarce** los investigó otro agente. Verifiqué la página del Juzgado, el art. 47 del Código de Faltas, la Ordenanza de Bragado y los dos decretos de Balcarce.
- **Corregí al agente:** el artículo de la Ley 11.768 sobre tareas comunitarias es el 137, no el 136.
- **No se nombran personas.** Una nota de prensa sobre un caso en La Plata que nombra a un particular no se subió.
