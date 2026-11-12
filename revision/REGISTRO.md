# Registro de la revisión mensual de la web de San Isidro

Cada corrida agrega una sección al final. Temas y números; nunca el texto de las preguntas de la gente.

## Corrida del 2026-11-11

Primera corrida, hecha a mano por el coordinador del programa. Cubre desde el 12/10/2026, cuando la web salió al link principal.

**Números**
- 34 preguntas guardadas, sin contar las pruebas automáticas.
  - 12 eran pruebas a mano del coordinador (12 y 16 de octubre).
  - Quedan 22 preguntas de gente, de 18 conexiones distintas.
- «No lo cubre»: 5. «¿Le faltó algo?»: 0. Mensajes de «Escribinos»: 0.
- Pruebas automáticas excluidas: 23.

**Estado de la web:** las cinco páginas dan 200 y el chat contesta.

**Se corrigió solo (A)**
- **El Bajo** (5 preguntas). El chat decía que el programa no habla del Bajo, pero el programa trata la costa y las cuencas del Bajo.
  - Causa: la búsqueda no encontraba esos pasajes, porque «bajo» también es adjetivo («bajo techo», «bajó el gasto»).
  - Arreglo: frases que se suman sólo a la pregunta («el bajo», «del bajo», «al bajo» → costa, ribera, cuenca, río), en `proyecto/web/ajustes_chat.json`, más el soporte de frases en `index_b.tpl.html` y `build_site.py`.
  - Commit 79d7ccf. Probado en el anticipo y en el link principal: 4 de 4 bien. Ahora contesta con la costa, las cuencas, el Parque del Águila y la Escuela Náutica.

**Para Nick (B)**, sólo los temas:
1. Salud mental (1 pregunta).
2. Capacitación de la patrulla municipal (2 preguntas).
3. Un resumen de qué cambia para el Bajo (5 preguntas).
4. Oficios independientes, como plomeros (1 pregunta).
5. Adultos que quieren terminar la secundaria (1 pregunta).

**Descartado (C):** 12 pruebas a mano del coordinador, con preguntas trampa.

**Ya corregido antes de esta corrida:** el 12/10, antes de las 06:30, el chat se negaba en segunda persona («sólo respondés…»). Se arregló ese mismo día.

**Decisiones de Nick del mes anterior:** no hay; es la primera corrida.

### Agregado el 2026-11-12: prueba por temas
- Prueba nueva, `revision/temas.mjs`, gratis: 48 preguntas típicas, una por tema. Mira si la sección correcta está entre los 14 pasajes que recibe la IA.
- Con el sitio del 11/11 (ya con el arreglo del Bajo) encontraban su sección 47 de 48.
  - Faltaba «los perros de la calle»: el programa no lo trata, así que no es un error del chat. Queda como tema posible para Nick.
- Mejorado «me robaron»: la búsqueda no unía «robaron» con «robo».
  - Arreglo: sinónimos robaron, roban, asaltaron, asalto, afanaron → robo, delito; inseguridad → seguridad, delito.
  - La sección de Seguridad pasó del fondo de la lista al primer lugar.
- `publicar.sh` corre esta prueba antes de publicar. Publicado y probado: 47 de 47 temas, 4 de 4 preguntas en el anticipo y en el link principal.

### Agregado el 2026-11-12: preguntas sobre «qué está mal» (pedido del coordinador de Pipinas)
- Prueba en el link principal, antes del cambio: «¿Qué problemas ves en el programa?» contestaba con los problemas del Municipio, no del programa. «¿Qué errores o debilidades tiene?» mezclaba límites sacados de las investigaciones. No habló de correcciones, versiones ni decisiones internas.
- Causa 1: los cuadros largos se cortaban a los 2.200 caracteres. Del cuadro 44 («Veinticinco cosas que pueden salir mal») la búsqueda veía sólo los tres primeros riesgos. Lo mismo pasaba con los cuadros 9, 14, 33, 40, 41, 42 y 43. Arreglo: cada cuadro largo se lee en partes, con su título y su encabezado (`cuadroPartes` en `index_b.tpl.html` y en `build_site.py`).
- Causa 2: las investigaciones mandaban a la IA trabajo interno. Arreglo: el chat ya no lee los pasajes descartados, los que el programa cambió después (su nota dice «corrigió», «recalculó» o «reemplazó»), los borradores de propuesta, lo que no se encontró, el método ni las correcciones. Tampoco lee las frases sobre el encargo o el «programa final», ni los rótulos «TAREA A/B/C» (`invParaChat` y `seccionChat`). Quedan 440 de 609 pasajes. Las páginas de las investigaciones no cambian.
- Regla nueva (Ajuste 1, `ajustes_chat.json`): ante «qué problemas, errores o debilidades tiene», «es confiable» o «qué criticaría un escéptico», contesta con los cuatro o cinco riesgos principales de 6.6, los críticos primero, cada uno con lo que lo reduce. No dice que no hay errores ni llama a nada error, pendiente o desactualizado.
- Búsqueda: 23 frases nuevas que suman «riesgos, salir mal, reduce» a esas preguntas. La prueba gratis por temas suma 4 preguntas de este tipo: 51 de 51.
- Pruebas pagas: 4 preguntas nuevas en `pruebas.json`, con lo que no tienen que decir. Dos son fijas de cada mes y dos quedan para correr con `--todas`. `probar.py` ahora busca las palabras prohibidas desde el comienzo de una palabra («pendiente» no salta con «independiente»).
- Resultado: 8 de 8 en el anticipo y 6 de 6 en el link principal. Se usaron 16 preguntas pagas, de 20 autorizadas.
