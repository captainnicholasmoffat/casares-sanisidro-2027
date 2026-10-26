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
