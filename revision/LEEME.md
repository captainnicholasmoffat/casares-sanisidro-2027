# Revisión mensual de la web de San Isidro (autocorrección con Nick en el circuito)

Rama `web-sanisidro`. Es la copia de trabajo de la web publicada en https://sanisidro2027.pages.dev.

## Qué hace

El día 1 de cada mes, a las 8:48 (hora de Buenos Aires), una tarea programada abre una sesión nueva y sigue `revision/INSTRUCCIONES_CORRIDA.md`. La tarea es «Revisión mensual de la web de San Isidro» (`trig_01R81X8evAzB59m9k8xSk4p7`) y su primera corrida es el 1 de diciembre de 2026. Pasos:

1. Baja de la base D1 (`sanisidro2027`) las preguntas, los «¿Le faltó algo?» y los mensajes de «Escribinos» desde la corrida anterior, con `revision/extraer.py`. Las pruebas automáticas se excluyen.
2. Revisa que la web ande: cada página y una pregunta real al chat.
3. Lee cada pregunta con su respuesta y la clasifica según las reglas de abajo.
4. Corrige sola lo evidente y lo publica con `revision/publicar.sh`. El orden es fijo: armado con el control de cifras, anticipo, pruebas, link principal y pruebas otra vez. Si algo falla, no publica.
5. Anota la corrida en `revision/REGISTRO.md` y le manda el informe a Nick por mail.

## Reglas acordadas con Nick (11 de noviembre de 2026)

**Se corrige solo** (sólo cómo contesta el chat y piezas rotas de la web; nunca el programa):
1. Algo de la web no anda: un botón, un enlace, una página, el micrófono o cómo se ve en el celular.
2. El chat contesta algo sin sentido, cortado, en otro idioma o con una palabra prohibida.
3. El chat dice «el programa no habla de esto» cuando el programa sí lo dice.
4. El chat da una cifra distinta de la del modelo fiscal.

**Le llega a Nick** (decide él con sí o no):
5. Lo que el programa no cubre.
6. Lo contradictorio y las críticas.
7. Cualquier cambio al texto, las cifras o las propuestas del programa.
8. Los mensajes de «Escribinos».

**Se descarta** (sólo se cuenta): lo ofensivo, los intentos de hacerle trampa al chat y las pruebas.

La frase de la web «Cada cambio lo revisa una persona antes de publicarse» queda como está (Nick, 11/11): habla de los cambios importantes.

## Dónde está cada cosa

- `proyecto/web/ajustes_chat.json`: lo único que cambian las correcciones del chat.
  - **Sinónimos:** se suman a la pregunta y a los pasajes. Sólo para palabras con un único sentido.
  - **Frases:** se suman sólo a la pregunta. Sirven para palabras con dos sentidos, como «el bajo»: el barrio, no el adjetivo.
  - **Reglas extra:** se suman a las del chat.
  - `build_site.py` los mete en la página y en el servidor.
- `revision/contexto.mjs`: muestra qué pasajes encuentra la búsqueda para una pregunta, sin llamar a la IA y sin costo. Sirve para probar una corrección antes de publicarla.
- `revision/extraer.py`: baja los datos de la base y prueba la web.
- `revision/probar.py` y `revision/pruebas.json`: preguntas de prueba. Cada corrección suma la pregunta que falló, con lo que tiene que decir.
- `revision/publicar.sh`: arma, publica en el anticipo, prueba y recién entonces publica en el link principal.
- `revision/REGISTRO.md`: el historial de corridas. Lleva temas y números, nunca el texto de las preguntas de la gente.
- `revision/INSTRUCCIONES_CORRIDA.md`: lo que sigue la sesión de cada mes.

## Privacidad

Las preguntas de la gente se quedan en la base D1, que las borra a los seis meses, como dice la nota de privacidad de la web. No se copian al repositorio. Sólo van en el mail a Nick.

## Costo

Cada pregunta de prueba cuesta unos 3 centavos de dólar. Una corrida hace unas 10 preguntas de prueba.
