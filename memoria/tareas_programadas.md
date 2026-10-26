# Tareas programadas de San Isidro (copia de las instrucciones)

## «Vigilar la web sanisidro2027» (cada 2 horas, del 16 al 17 de octubre de 2026; ya apagada)

Control automático de la web https://sanisidro2027.pages.dev (programa de gobierno para San Isidro). Nick pidió que no se caiga hasta el sábado 17 de octubre de 2026 a la noche. Hacé sólo esto, sin cambiar nada de la web:

0. Mirá la hora actual (zona America/Buenos_Aires). Si ya es el 18 de octubre de 2026 o después: buscá esta tarea programada («Vigilar la web sanisidro2027») con list_triggers, desactivala con update_trigger (enabled=false) y terminá con una sola línea: «Vigilancia de la web terminada».

1. Páginas. Con curl, pedí cada una de estas y anotá el código HTTP: https://sanisidro2027.pages.dev/ , https://sanisidro2027.pages.dev/cuentas/ , https://sanisidro2027.pages.dev/despliegue/ , https://sanisidro2027.pages.dev/contacto/ , https://sanisidro2027.pages.dev/data/programa.json . Todas tienen que dar 200. Si alguna falla, probala una vez más antes de darla por caída.

2. Chat. Mandá una sola pregunta de prueba:
curl -s -m 120 -X POST https://sanisidro2027.pages.dev/api/ask -H 'content-type: application/json' -H 'origin: https://sanisidro2027.pages.dev' -d '{"question":"[PRUEBA AUTOMATICA] ¿Qué propone el programa para el comercio chico? Respondé en una línea."}'
Está bien si el código es 200 y la respuesta contiene «text_delta» y «message_stop». Si falla, probá una vez más. Si la respuesta trae un código como «daily_limit», «rate_limited», «upstream_error» o un error de saldo o crédito, anotalo tal cual.

3. Resultado.
- Si todo está bien, terminá con una sola línea: «Sin novedades: la web anda bien (HH:MM)». Nada más.
- Si algo falló, terminá con un aviso corto en castellano simple, una línea por problema, por ejemplo: «La web falló a las HH:MM: el chat no contesta (upstream_error)». Agregá una última línea: «Avisale a la sesión del programa de San Isidro para volver a la versión anterior.» Si el error es de saldo o crédito, decí: «Se quedó sin saldo la cuenta de la inteligencia artificial: hay que cargar saldo en la consola de Anthropic.»

No publiques, no despliegues, no borres ni cambies nada; sólo mirá y avisá.

## «Cerrar la vigilancia de la web» (una vez, 18 de octubre de 2026)

Terminó el plazo de vigilancia de la web (hasta el sábado 17 a la noche). Confirmá con list_triggers que la tarea «Vigilar la web sanisidro2027» quedó desactivada; si sigue activa, desactivala con update_trigger y avisale a Nick en una línea.

## Lección
- Antes de una visita o un evento: la web se congela (nada se publica) y una tarea programada la vigila cada 2 horas, con prueba real del chat. Otra tarea la apaga sola al terminar el plazo.
