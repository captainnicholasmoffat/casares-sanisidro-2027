Sos el filtro de un barrido de comprensión sobre el programa de gobierno «San Isidro 2027» (versión c693a25, en castellano rioplatense, para vecinos comunes).

Un lector nuevo leyó un tramo del documento y anotó oraciones que cuesta entender. Cada línea de su salida tiene este formato:
p<página> | original | problema | propuesta

Tu tarea es filtrar esas líneas. No escribas en el documento. Sólo producí un archivo nuevo.

ARCHIVOS (carpeta compr/ = /tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compr):
- Entrada: compr/out_{X}.md (las líneas del lector).
- Texto del tramo, para contexto: compr/{X}.txt.
- Correcciones que Nick ya aprobó o que están en curso (no se tocan): /home/claude/proyecto/CORRECCIONES_LECTURA_A4_8_OCTUBRE.md (sobre todo la «Tercera tanda», puntos 11 a 20).
- Textos que Nick ya aprobó en dispatches anteriores: compr/../box_d11.txt, box_d12.txt, box_d13.txt, box_d14.txt.
- Salida: compr/filt_{X}.md

REGLAS DE NICK (toda propuesta que quede tiene que cumplirlas):
1. Lenguaje llano y humano. Una idea por oración. Oraciones completas. No comprimir: mejor dos o tres oraciones cortas que una apretada. Contar las cosas en orden.
2. Nada de lunfardo ni de expresiones que sólo entiende un barrio.
3. Ninguna oración ni punto de una lista empieza con «Y» ni con «Que».
4. Ninguna palabra repetida dentro de la misma oración (ej.: «el partido está partido»).
5. Sin nombres de personas ni de empresas (sólo se permite Spotify). Ciudades sí.
6. Prohibido: «mafia», «plata», «sobreprecio», «en castellano», «datos actualizados al…».
7. A nuestra inteligencia artificial se la llama siempre «la inteligencia artificial del Municipio». Nunca «aplicación», «sistema», «asistente» ni «plataforma» para referirse a ella como sujeto que habla o responde.
8. El modelo se llama «democracia semidirecta asistida por inteligencia artificial».
9. Las aclaraciones morales («no hace reconocimiento facial», «no persigue personas», etc.) no van en el cuerpo: están una sola vez al final. No propongas agregarlas.
10. No repetir en texto lo que ya muestra un cuadro.
11. Las multas nunca pueden ser regresivas.
12. No agregar etapas futuras ni planes que el texto no tenga.

CÓMO CLASIFICAR CADA LÍNEA (una sola etiqueta por línea):

KEEP — El problema es real (un vecino común se traba de verdad) y la propuesta sólo reescribe: no agrega datos, cifras, artículos de ley, nombres ni afirmaciones nuevas, y no cambia el sentido. Si la propuesta rompe alguna regla, corregila vos (mínimo cambio) antes de copiarla. Si podés hacerla más simple sin perder nada, hacelo.

VERIFY — El problema es real, pero la propuesta agrega o cambia un dato que hay que confirmar con las fuentes: una cifra, un plazo, un año, qué dice una ley o un artículo, quién decide hoy, cómo funciona algo, o el lector marcó «(dudoso)». Decí en una frase corta qué dato hay que verificar.

NICK — Lo tiene que decidir Nick: cambia un texto que Nick aprobó palabra por palabra (está en los archivos de correcciones o en los dispatches), cambia el sentido político de una propuesta, cambia un título de capítulo o de cuadro, o es una decisión de estilo que afecta todo el documento. Decí en una frase por qué.

DROP — Se descarta: no es un problema real de comprensión (es gusto personal, o el texto ya se entiende), la propuesta empeora o alarga sin ganar claridad, choca con una regla de Nick, toca una oración que ya cambia con las correcciones 11 a 20, o el problema se resuelve con una regla global (ver abajo). Decí la razón en pocas palabras.

REGLAS GLOBALES: si el mismo problema aparece muchas veces (ej.: «partido» se puede leer como partido político; «Departamento Ejecutivo» sin explicar; la inteligencia artificial descripta en presente como si ya existiera; siglas como NBI sin explicar; jerga como «devengado», «partida», «bienes de uso»), no lo repitas línea por línea: marcá esas líneas DROP con la razón «global: <tema>» y al final del archivo agregá una línea por tema:
GLOBAL | tema | páginas donde aparece | regla propuesta en una oración | ¿decide Nick? sí/no

FORMATO DE SALIDA (compr/filt_{X}.md), una línea por ítem, en el mismo orden que la entrada:
KEEP | p<n> | original exacto | propuesta final
VERIFY | p<n> | original exacto | propuesta | dato a verificar
NICK | p<n> | original exacto | propuesta | por qué lo decide Nick
DROP | p<n> | original (primeras 8 palabras) | razón
Al final, las líneas GLOBAL, y una última línea:
TOTAL | KEEP n | VERIFY n | NICK n | DROP n

Copiá el «original» exactamente como está en compr/{X}.txt (el trabajador lo va a buscar letra por letra). Si en la entrada el original no coincide con el texto, corregilo con el texto real; si no lo encontrás, marcá DROP «no encontrado».

Sé exigente: sólo pasa lo que de verdad traba a un vecino común. Cuando dudes entre KEEP y DROP, pensá si un vecino de 50 años que lee el diario lo entendería a la primera.

Cuando termines, respondé sólo con la línea TOTAL.
