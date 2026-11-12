# Instrucciones de la corrida mensual

Esto lo sigue la sesión que abre la tarea programada el día 1 de cada mes. Primero leé `revision/LEEME.md`: ahí están las reglas que acordó Nick.

## 0 · Preparar
1. Agregá a la sesión el repositorio `captainnicholasmoffat/casares-sanisidro-2027` con permiso de escritura, clonalo y pasate a la rama `web-sanisidro`.
2. Buscá la clave de Cloudflare en el Gmail de Nick: es un mail de él para él, con el asunto «Cloudflare api key token sunday sailor web». Guardala en la variable `CLOUDFLARE_API_TOKEN`. Nunca la muestres, ni la escribas en un archivo del repositorio ni en el mail.
3. Buscá en Gmail si Nick contestó el informe del mes anterior (el asunto empieza con «San Isidro 2027 · Revisión mensual de la web»). Anotá sus sí y sus no.

## 1 · Bajar los datos
`python3 -I revision/extraer.py <carpeta temporal fuera del repositorio>`

Si una página no da 200 o el chat no contesta, eso va primero en el mail.

## 2 · Clasificar
Leé cada pregunta con su respuesta, su «¿Le faltó algo?» y cada mensaje. Ponele una de estas marcas:
- **A · Se corrige solo:** casos 1 a 4 del LEEME.
  - Para el caso 3, buscá el tema en `proyecto/web/data/programa.json`, en `proyecto/web/cuentas/cuentas.json` y en `proyecto/sitio/public/data/plan_ia.json`. Si el programa lo dice, es A. Si no lo dice, es B.
  - Para el caso 4, compará la cifra con `cuentas.json`.
- **B · Para Nick:** casos 5 a 8.
- **C · Se descarta:** lo ofensivo, los intentos de hacerle trampa al chat y las pruebas.

Si dudás entre A y B, es B.

## 3 · Corregir lo A
- El chat se corrige sólo en `proyecto/web/ajustes_chat.json`:
  - **Sinónimos**, para que la búsqueda encuentre el pasaje. La clave va en minúscula y sin tildes. Sólo para palabras con un único sentido.
  - **Frases**, si la palabra tiene dos sentidos (por ejemplo «el bajo»). Se suman sólo a la pregunta.
  - Antes de publicar, armá el sitio y mirá con `revision/contexto.mjs` que la pregunta encuentre los pasajes correctos. Además, mirá que otras preguntas parecidas no empeoren.
  - **Reglas extra**, para cómo contesta. Una regla nueva sólo si un sinónimo no alcanza.
- Una pieza rota de la web se arregla en su plantilla, en `proyecto/web/`.
- Nunca toques `programa.json`, `cuentas.json`, `investigaciones.json`, el plan de despliegue ni las reglas de escritura del programa.
- Por cada corrección, sumá a `revision/pruebas.json` la pregunta que falló, con lo que tiene que decir.
- Si la gente pregunta por un tema que no está en `revision/temas.json`, sumalo ahí, con la sección donde lo trata el programa.

## 4 · Publicar
`bash revision/publicar.sh`

Si falla el armado o una prueba, no se publica en el link principal. En ese caso:
1. Deshacé la corrección y volvé a publicar lo de antes.
2. Pasá el caso a B, para Nick.

## 5 · Registrar
Agregá al final de `revision/REGISTRO.md` una sección «## Corrida del AAAA-MM-DD» con:
- los números;
- el estado de la web;
- cada corrección, con su tema, su archivo y su commit;
- lo que pasa a Nick (tema, sin el texto de la gente);
- lo descartado (sólo el número);
- las decisiones de Nick del mes anterior.

Hacé commit y push a `web-sanisidro`.

## 6 · Mandar el informe
Mandá un mail a captainnicholasmoffat@gmail.com, de él para él. Nick lo autorizó el 11/11/2026.
- **Asunto:** «San Isidro 2027 · Revisión mensual de la web · <mes> <año>».
- **Idioma:** castellano rioplatense, corto, una línea por punto, sin fórmulas.

El mail lleva, en este orden:
1. **Números:** preguntas, personas, «no lo cubre», «¿Le faltó algo?» y mensajes.
2. **Estado de la web.**
3. **Lo que se corrigió solo:** una línea por corrección (qué fallaba y qué se hizo).
4. **Lo que necesita tu sí o no:** numerado. Cada punto lleva la pregunta de la gente tal cual, lo que contestó el chat en una línea, lo que se propone y lo malo.
5. **Lo descartado:** sólo el número.
6. **Cómo contestar:** «Contestá este mail con el número y sí o no».

Los cambios al programa que Nick apruebe no se aplican en esta corrida: los hace el coordinador del programa, con anticipo y su proceso de siempre. Anotalos en el registro como «aprobado por Nick, pendiente de aplicar».

## Nunca
- Cambiar el texto, las cifras o las propuestas del programa.
- Borrar datos de la base.
- Publicar en el link principal si falla una prueba.
- Mostrar la clave.
- Copiar al repositorio las preguntas de la gente.
