import json, collections, os, re, sys
D = sys.argv[1]; LOG = sys.argv[2]
P = json.load(open(os.path.join(D, "programa.json"), encoding="utf-8"))
I = json.load(open(os.path.join(D, "investigaciones.json"), encoding="utf-8"))
L = json.load(open(LOG, encoding="utf-8"))

cat = collections.Counter()
for code, items in L.items():
    for why, t in items:
        k = why.split(":")[0]
        cat[k] += 1
n_secc = cat["sección interna o de proceso"]
n_bloq = cat["bloque"] + cat["subitem de un item sacado"] + cat["lista de un rótulo sacado"] + cat["rótulo sin contenido"]
n_orac = cat["oración"]
n_fila = cat["fila"]

desc = collections.OrderedDict()
for d in I:
    if d["descartado"]:
        desc.setdefault(d["nota"], []).append(d["id"])
notas = collections.OrderedDict()
for d in I:
    if d["nota"] and not d["descartado"]:
        notas.setdefault(d["nota"], []).append(d["id"])

w = [len(d["texto"].split()) for d in I]
size_p = os.path.getsize(os.path.join(D, "programa.json"))
size_i = os.path.getsize(os.path.join(D, "investigaciones.json"))
tipos = collections.Counter()
for e in P:
    i = e["id"]
    if re.match(r"^\d+\.\d+$", i): tipos["apartados de los capítulos 1 a 6"] += 1
    elif re.match(r"^\d+(\.\d+)?-r\d+$", i): tipos["recuadros de los capítulos"] += 1
    elif re.match(r"^\d$", i): tipos["aperturas de capítulo"] += 1
    elif i.startswith("glosario-"): tipos["términos del glosario"] += 1
    elif re.match(r"^anexo-\d+$", i): tipos["ordenanzas del anexo"] += 1
    elif i.startswith("metodo"): tipos["nota de método (incluye las notas de cada capítulo, lo que el programa no hace y lo que confirma un abogado)"] += 1
    else: tipos["otras (introducción, «Qué proponemos hacer», «Para cerrar», apertura y cierre del anexo, glosario)"] += 1

out = []
A = out.append
A("# Curación de la base de conocimiento del chatbot\n")
A("Este archivo explica qué se hizo con el programa final y con las investigaciones para armar `programa.json` e `investigaciones.json`, qué se sacó y por qué, qué pasajes quedaron marcados como descartados y qué contradicciones aparecieron.\n")

A("## 1. El programa (`programa.json`)\n")
A("- Sale del texto final del programa, el commit c462fcf: el HTML de cada sección que arma `doc/content*.py`. No se reescribió nada. Se sacaron sólo el encabezado y el pie de cada página.")
A("- Hay una entrada por cada apartado de los capítulos 1 a 6, por cada recuadro (id del tipo `5.5-r3`), por la introducción, «Qué proponemos hacer», «Para cerrar», cada ordenanza del anexo, cada término del glosario y cada parte de la nota de método.")
A("- Se comprobó contra la A4 final: los 52 apartados del índice de la A4 están todos, con el mismo título y en la misma hoja. También se comprobó al revés: todo el texto de las hojas 5 a 140 de la A4 está en el JSON, salvo los números sueltos de adentro de los gráficos y los rótulos con letras separadas, que el PDF desordena.")
A("- `hoja_a4` es la hoja donde empieza la entrada; se agregó `hoja_a4_fin` (dónde termina) y, en los apartados largos, `subtitulos` con la hoja de cada subtítulo, para que el chatbot pueda citar la hoja exacta.")
A("- Las fuentes de la lista final («Las fuentes de lo que afirma el texto») se repartieron en el campo `fuentes` de cada apartado, con `fuentes_hojas_a4` (hojas 132 a 137). Las fuentes que van debajo de cada cuadro o gráfico quedaron dentro del cuadro.")
A("- En los gráficos, además del título, la bajada, la fuente y la nota, va `texto_del_grafico` con los rótulos y valores del gráfico, en el orden en que están dibujados. Los pies de foto («Ilustración») van aparte, en `pies_de_foto`, y las etiquetas de los apartados («Reasignación», «Gestión») en `etiquetas`.\n")

A("## 2. Las investigaciones (`investigaciones.json`)\n")
A("- La carpeta `informes/` tiene 32 archivos: 28 informes en Markdown y 4 planillas CSV (reseñas de la aplicación y asuntos del Concejo). Se usaron los 28 informes; las planillas son datos sueltos, sin secciones ni texto que citar.")
A("- Uno de los 28, el «182 · Hoy como hoy, lo nuestro con marca: la lista», no se publicó: es una lista interna de cambios de redacción del documento, no una investigación. Quedan 27 informes.")
A("- Cada pasaje es el texto del informe, cortado por sección, en trozos de 150 a 400 palabras. Las secciones chicas se juntaron con la de al lado; en ese caso el subtítulo va dentro del texto. Las tablas largas se cortaron por filas, repitiendo el encabezado.")
A("- El título del informe se escribió legible (por ejemplo, «Informe 02 · Inteligencia artificial en la salud municipal» en vez de «INFORME 02 — Worker Chrome»).")
A("- `temas` sale de una lista fija de temas, contando las palabras de cada uno en el pasaje. `relacion` son los apartados del programa más parecidos en el texto, entre los que corresponden a esos temas y al informe.\n")

A("## 3. Qué se sacó, y por qué\n")
A(f"En total se sacaron {n_secc} secciones enteras, {n_bloq} párrafos, ítems o rótulos, {n_orac} oraciones sueltas y {n_fila} filas de tablas. Todo lo que se sacó es de estos tipos:\n")
A("- **Notas internas y decisiones del equipo.** Las secciones «Decisiones del cliente», «Decisiones de Nick», «Lo ya decidido por el cliente», «Decisiones que necesita el cliente», «Preguntas abiertas (decide el cliente / decide Nick)» y «Para decidir». También frases como «La elección entre esa versión de B y A es tuya», «Si Nick quiere, se le agrega una nota que remita acá», «Las aplica el worker del documento» o «Es una pregunta abierta para el cliente».")
A("- **Pendientes y tareas.** «Las tres pistas de trabajo de campo» (informe 05), «Lo que falta, y cómo conseguirlo sin gastar y sin ir en persona» y «Cómo registrar los testimonios del cliente» (informe 15), y frases como «Vía primaria pendiente», «hay que reconfirmarla» o «antes de publicar hay que descargar el PDF».")
A("- **Comentarios sobre el borrador del documento.** «Qué hay que corregir en el documento» (07), «Qué dice hoy el documento y qué dicen las fuentes» (12), «Validación contra el documento» (09), «Qué se puede afirmar en el programa y qué no» (15), los avisos «BORRADOR — para discutir, no para el documento todavía», «El documento no se toca», «Estado: para decidir», y frases como «Antes de usarlo en el documento hace falta…» o «Conviene escribir “en veintidós días hábiles”».")
A("- **Comentarios de proceso y de herramientas.** «Fuentes que se probaron y cuáles no respondieron» (05), cómo se bajaron las reseñas («google-play-scraper»), los errores de conexión («WebFetch falla…», «devolvió 403», «rechaza la conexión desde este entorno»), «Se agotó el cupo de búsquedas», y las reglas internas de cada tanda («No se pidió nada pago ni en persona»).")
A("- **Rutas de archivos y el repositorio.** Toda oración, fila o ítem con rutas (`01_raw/…`, `data/…`, `informes/…`, `doc/…`), nombres de archivos (`.py`, `.csv`, `.json`, `FUENTES.txt`, `NO_SUBIDOS.txt`), la rama de trabajo, y las secciones «Fuentes, todas en el repo» (09), «Qué fotos subieron al repositorio» (15) y «Código y cómo reproducirlo» (09). Los enlaces públicos (https://…) se dejaron.")
A("- **Las marcas.** [V], [P], [CP], [SC] e [I] se pasaron a palabras entre paréntesis: «(verificado en la fuente)», «(probable, según fuentes secundarias)», «(cálculo propio)», «(sin confirmar)» e «(inferencia propia)». Ojo: en los informes, [P] no quiere decir «según la prensa» sino «probable: fuente secundaria seria» (y a veces una fecha de foto que no se pudo confirmar); por eso se escribió «probable, según fuentes secundarias» y no «según la prensa», para no afirmar algo falso. Las leyendas que explicaban las marcas se sacaron. Las marcas que ya eran palabras («[verificado]», «[cálculo propio]») se dejaron.")
A("- **Una sección que el propio informe marcaba como contexto interno.** En el informe 18 se sacó «1.6 La causa judicial: contexto, no argumento» y las frases que la retoman: el informe decía que «no pasa al programa mientras no haya una resolución judicial» y que era «contexto para el equipo». No se sacó por los nombres, sino porque el equipo decidió no usarla.")
A("- **Frases de estrategia de campaña.** Por ejemplo «La lectura política, en una línea» y «Lo que esto significa para el documento» (08), «Lo que esto significa, sin vueltas» (07) y «Conclusión operativa» (06).\n")
A("No se sacaron nombres de personas ni de empresas. No se reescribió ni se resumió nada: lo que quedó es el texto del informe, sin el marcado de Markdown.\n")

A("### Democracia directa\n")
A("Se buscó en todos los informes cualquier pasaje que planteara la democracia directa como una etapa futura o un plan posterior del programa («democracia directa», «referéndum», «plebiscito», «consulta popular», «vinculante», «segunda fase», «más adelante»). **No apareció ninguno.** Las únicas menciones son otras cosas y se dejaron: el informe 07 cuenta que en el Concejo hubo cero proyectos de consulta popular o plebiscito; el 08 dice que el proyecto de presupuesto participativo 626-HCD-2024 «no es un referéndum ni una consulta popular»; y el 13 dice que el voto vecinal no puede obligar al Concejo y que la democracia semidirecta del artículo 211 de la Constitución provincial nunca se reglamentó.\n")

A("## 4. Pasajes marcados como descartados\n")
A(f"Son {sum(len(v) for v in desc.values())} pasajes. Cada uno describe una opción que el programa final no tomó o decidió distinto; la nota dice qué decidió el programa.\n")
for nota, ids in desc.items():
    A(f"- **{', '.join(ids)}.** {nota}")
A("")
A(f"Además, {sum(len(v) for v in notas.values())} pasajes no están descartados pero llevan una nota, porque mencionan una cifra o un dato que después se corrigió, en otro informe o en el programa:\n")
for nota, ids in notas.items():
    A(f"- **{', '.join(ids)}.** {nota}")
A("")

A("## 5. Contradicciones entre las investigaciones y el programa final\n")
A("- **Los permisos de Catalejo y Barisidro.** El informe 17 (y una fila del 04) dice, con decretos, que los dos locales tenían un permiso municipal precario y gratuito de 1996, y que el convenio de 1977 dice que los cánones los cobra el Municipio. El programa final (5.5) dice, según quienes manejaban los locales, que el permiso para usar la tierra lo daba la Provincia y que el canon se le pagaba a la Provincia. Esos pasajes están marcados como descartados.")
A("- **La fecha de la demolición de Barisidro.** El informe 05 dice septiembre de 2025; el programa (5.5 y 5.5-r14) dice agosto de 2025, como corrigió el informe 17.")
A("- **La cautelar del ex Arsenal de Boulogne.** Los informes 05 y 06 la cuentan como vigente (05 la fecha el 13/08/2025). El programa (5.5) dice que se obtuvo en julio de 2025, que la Cámara la confirmó en septiembre y que un juzgado la levantó el 30 de diciembre, en una resolución que todavía no está firme, como encontró el informe 13.")
A("- **La recolección.** El informe 01 habla de una sola licitación fracasada desde 2009; el 12 y el programa (5.5) dicen que fracasaron cuatro y que el mismo grupo presta el servicio desde 1998.")
A("- **Cuánto se cobra de la tasa.** El informe 09 calcula lo cobrado con el 89,32% (todos los ingresos); el programa (3.5) usa el peor caso del ABL, 74%, y por eso la tabla nueva trae entre 5.946 y 5.983 millones por año y faltan 1.242 que salen del gasto flexible. Además, el 09 da 2,31× para Acassuso y el cuadro 17 del programa, 2,32×.")
A("- **El semillero.** El informe 10 dice que Ciencia y Técnica queda ocupada en 22,0%, que en el mes 27 egresan 138 y que en el mandato egresan 771; el programa dice 27,1% (con la plataforma), 231 en el mes 27 y 1.286 en el mandato. La subcontratación del 3% de la propuesta original se cambió por 20% para pymes, con 5% para empresas de menos de cinco años.")
A("- **La arena.** El informe 11 concluyó que «playa» no quería decir arena y su borrador decía «el programa no promete playa»; el 16 dice que se descartó la playa seca. El programa final dice que hubo arena (notas y fotos de 1934 y 1937, como encontró el 15) y propone tramos piloto de arena con baño habilitado.")
A("- **Las rejas y barreras de la costa.** Los informes 11 y 16 hablan de vaciado diario y de costos de 400 a 1.900 millones por año; el programa propone rejas revisadas cada semana y después de cada lluvia, barreras en «J» vaciadas después de cada lluvia fuerte y sudestada, y un mantenimiento de 139 a 346 millones por año.")
A("- **Los espectáculos.** Los informes 23 a 23 quinquies calculan los cachets de los 200 shows en unos 202 a 214 millones por año y el programa completo de espectáculos en unos 326 a 329; el programa final (5.5-r12) dice unos 394 millones (532 el primer año), con 270,6 para los artistas, 14,1 millones por los espacios bajo techo y 85,3 por los grupos de producción. Ningún informe tiene esas cifras finales. También cambió cómo se define al artista emergente (el 23 bis usaba el registro del INAMU; el programa usa menos de 50.000 oyentes por mes en Spotify).")
A("- **Los teléfonos de los inspectores.** El 23 bis calcula 420 agentes y el 23 ter de 201 a 270, con guarda rápida de 6 meses; el programa dice de 208 a 280 agentes y guarda de dos años en una nube con servidores en Bélgica.")
A("- **El profesor digital.** El 23 bis lo daba gratis a escuelas parroquiales y cooperativas; el programa lo da gratis a los 22.748 alumnos de escuelas públicas y de privadas con aporte estatal del 100%. La idea inicial que cuenta el informe 22 (se sacó por ser una nota interna) era que el avatar les avisara a los profesores si el alumno hace trampa; el programa dice que el profesor digital no va a acusar ni a sancionar a un chico.")
A("- **El dólar.** Los informes 20, 22 y 23 pasan los dólares a pesos con $1.520; el programa usa $1.447,84 (diciembre de 2025, BCRA).")
A("- **Las multas.** El informe 18 estudió poner un tope a la multa como porcentaje del ingreso o del valor del auto, y el 19, trabajo comunitario en lugar de la multa; el programa no hace ninguna de las dos cosas: propone cuotas sin trámites con tope, un tope a la deuda total y pedidos a la Provincia.")
A("- **Urbanismo y obra en parques.** El borrador del 13 proponía achicar el apartamiento del 10% del Código y exigir ordenanza para cada Urbanización Especial; el programa no lo incluye y fija la contribución por valorización en 15%. El borrador del 14 pedía licitación propia por encima de un monto y audiencia; el programa pide licitación propia para cualquier monto y, en la costa, la recomendación de un panel sorteado.")
A("- **Entre informes** (no con el programa): el 08 corrigió que la base de 731 presentaciones del Concejo usada en el 06 y el 07 era parcial; el 16 corrigió el costo del Interceptor del 11 y el origen del dato de monitoreo del 15; el 17 corrigió que los Decretos 605 y 748 de 2025 son sólo de Barisidro (14 y 16) y que Montevideo muestrea 2 veces por semana, no 4 (16). Esos pasajes llevan una nota.\n")

A("## 6. Tamaños y cantidades\n")
def num(n):
    return f"{n:,}".replace(",", ".")
A(f"- `programa.json`: {num(size_p)} bytes ({str(round(size_p/1e6, 2)).replace('.', ',')} MB), {len(P)} entradas.")
for k, v in tipos.most_common():
    A(f"  - {v} {k}")
A(f"- `investigaciones.json`: {num(size_i)} bytes ({size_i/1e6:.2f} MB), {len(I)} pasajes de 27 informes. Tienen entre {min(w)} y {max(w)} palabras. "
  f"{sum(x<150 for x in w)} quedaron por debajo de 150: son comienzos de informe o secciones cortas que no se podían juntar con la vecina sin pasar de 400. "
  f"{sum(x>400 for x in w)} quedaron un poco por encima de 400 (el máximo es {max(w)}). "
  f"{sum(d['descartado'] for d in I)} están marcados como descartados y {sum(1 for d in I if d['nota'] and not d['descartado'])} llevan sólo una nota.".replace("1.3", "1,3", 1) if False else
  f"- `investigaciones.json`: {num(size_i)} bytes ({str(round(size_i/1e6, 2)).replace('.', ',')} MB), {len(I)} pasajes de 27 informes. Tienen entre {min(w)} y {max(w)} palabras. "
  f"{sum(x<150 for x in w)} quedaron por debajo de 150: son comienzos de informe o secciones cortas que no se podían juntar con la vecina sin pasar de 400. "
  f"{sum(x>400 for x in w)} quedaron un poco por encima de 400 (el máximo es {max(w)}). "
  f"{sum(d['descartado'] for d in I)} están marcados como descartados y {sum(1 for d in I if d['nota'] and not d['descartado'])} llevan sólo una nota.")
A("- Los dos archivos se leyeron sin errores con `json.load` de Python.")
open(os.path.join(D, "CURACION.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("ok", len(out))
