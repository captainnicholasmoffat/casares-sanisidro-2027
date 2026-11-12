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
