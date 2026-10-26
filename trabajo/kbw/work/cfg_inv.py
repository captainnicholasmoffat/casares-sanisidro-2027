# -*- coding: utf-8 -*-
"""Curacion de los informes: lo que se saca, lo que se marca y con que apartados se relaciona."""

ORDER = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
         "18", "182", "19", "20", "21", "22", "23", "23b", "23c", "23d", "23e"]

# secciones que en ningun informe son para publicar: decisiones internas, pendientes, preguntas al equipo,
# instrucciones de trabajo y detalle de como se bajaron los archivos
GENERIC_DROP_SECS = [
    r"^Preguntas abiertas",
    r"^Decisiones que necesita",
    r"^Decisiones (del cliente|de Nick|tomadas)",
    r"^Lo ya decidido",
    r"^Código y cómo reproducirlo",
    r"^Para decidir$",
    r"PISTAS DE TRABAJO DE CAMPO",
    r"FUENTES QUE SE PROBARON",
    r"Qué fotos subieron al repositorio",
    r"^Validación contra el documento",
    r"Qué hay que corregir en el documento",
]

# bloques que en ningun informe son para publicar: la leyenda de las marcas (ya pasadas a palabras), el estado del
# trabajo, las reglas internas de cada tanda y los avisos de que un borrador no esta en el programa
GENERIC_DROP_BLOCKS = [
    "**Cómo leer las marcas", "**Marcas:**", "**[V]** verificado", "**[P]** probable", "**[SC]** sin confirmar",
    "**[CP]** cálculo propio", "**[I]** inferencia", "*Según el Municipio*: lo dice su prensa", "*Según X*: lo dice",
    "*Según el Municipio*: lo dice", "**Estado: para decidir.**", "**Estado:", "**Regla de este tema.**",
    "**Reglas de este informe.**", "**BORRADOR — para discutir", "**Esto es un borrador. No está en el programa.",
    "no se tocaron: la regla es agregar sólo archivos nuevos", "no se tocó, porque la regla de esta tanda",
    "**No se pidió nada pago ni en persona y no se contactó a nadie.**",
    "[verificado]: leído", "[probable]: prensa", "[sin confirmar].", "[cálculo propio].", "[inferencia].",
    "Lo jurídico lleva además «necesita dictamen", "Lo que el Municipio comunica va «según el Municipio»",
    "**Marcas:** [verificado]", "**Lo ya decidido por el cliente:**", "**Lo que el cliente todavía no decidió**",
    "**Decisión del cliente (", "**Decisiones del cliente (", "**La idea del cliente:**",
]
# fragmentos internos que se quitan de adentro de un texto (marcas de decisiones pendientes)
GENERIC_STRIP_RE = [
    r"\.?\s*\*\*Decisi[oó]n \d+\*\*(?=\s*\|)",
    r"\s*\[a decidir[^\]]*\]",
    r"\s*\*?\[Decisi[oó]n \d+:[^\]]*\]\*?",
    r"\s*\*\*Decisi[oó]n \d+\*\*:[^|]*",
    r"\s*\*Depende de (la opinión legal )?\(?la decisión \d+[^*]*\*",
    r"\s*\*Decisi[oó]n del cliente, \d{2}/\d{2}/\d{4}\.\*",
]

# (nombre del tema, patron en minusculas, apartados del programa con los que se relaciona)
TEMAS = [
    ("costa y río", r"\bcosta\b|ribera|\bplaya|balneario|río de la plata|\bel río\b", ["5.5", "5.5-r3", "anexo-11", "anexo-12"]),
    ("calidad del agua y cloacas", r"cloaca|desag[uü]e|e\. ?coli|calidad del agua|aysa|coliformes|bañ(o|arse) en el río", ["5.5", "5.5-r1", "5.5-r3", "5.4", "anexo-11"]),
    ("basura en el agua", r"basura|flotante|\breja|barrera|\bred(es)? (en|de) (los )?desag", ["5.5", "5.5-r3"]),
    ("recolección de residuos", r"recolecci[oó]n|residuos|barrido|covelia|ceamse|higiene urbana", ["5.5", "anexo-9"]),
    ("arena y playas", r"\barena|areneras|dragad", ["5.5", "5.5-r3"]),
    ("urbanismo", r"c[oó]digo (urbano|urban[ií]stico|de ordenamiento)|excepci[oó]n|excepciones|zonificaci|\bcou\b|urban[ií]stic", ["5.5", "5.5-r7", "anexo-13"]),
    ("parques y espacios verdes", r"\bparques?\b|espacios? verdes?|\bplaza", ["5.5", "5.5-r13", "anexo-12", "anexo-14", "anexo-5"]),
    ("multas de tránsito", r"multa|fotomulta|infracci|licencia de conducir|tr[aá]nsito", ["5.11", "5.11-r1", "5.11-r2", "anexo-15", "anexo-16"]),
    ("ruido", r"ruido|decibel|\bdb\b|son[oó]metro|ac[uú]stic", ["5.5", "5.5-r5", "5.5-r6", "anexo-8"]),
    ("seguridad y cámaras", r"seguridad|videovigilancia|c[aá]maras|patrull|delito|reconocimiento facial|fiscal[ií]a", ["5.7", "5.7-r1"]),
    ("salud", r"salud|hospital|turnos?\b|tom[oó]graf|m[eé]dic|resonancia|diagn[oó]stico", ["5.6", "5.6-r1", "5.6-r4"]),
    ("inteligencia artificial", r"inteligencia artificial|\bia\b|modelo de lenguaje|chatgpt|avatar", ["4.11", "4.11-r1", "5.3", "5.8-r1"]),
    ("empleo y formación", r"empleo|pasant|tecnicatura|formaci[oó]n laboral|salari|mercado de trabajo|laboral|productividad|habilidades", ["5.3", "5.3-r2", "5.3-r3", "anexo-10"]),
    ("semillero de empresas", r"semillero|pymes?\b|subcontrat|emprend|incubad", ["5.3", "anexo-10"]),
    ("educación", r"escuela|alumn|profesor digital|apoyo escolar|docente|colegio", ["5.8", "5.8-r1", "anexo-2"]),
    ("cultura y espectáculos", r"espect[aá]culo|\bshows?\b|m[uú]sica|artista|cultura|banda", ["5.5", "5.5-r12", "5.8", "anexo-7"]),
    ("transparencia", r"transparencia|bolet[ií]n oficial|acceso a la informaci|publica(do|r)? en|datos abiertos|portal", ["5.10", "2.2", "anexo-2"]),
    ("tasa y valuación", r"\babl\b|tasa (de servicios|municipal)|valuaci[oó]n|\bvub\b|iust", ["3.5", "anexo-3"]),
    ("Concejo Deliberante", r"concejo|\bhcd\b|concejal|expediente|expte", ["4.7", "4.7-r1"]),
    ("participación vecinal", r"asamblea|presupuesto participativo|comisi[oó]n(es)? zonal|asociaci[oó]n(es)? vecinal|sociedades? de fomento|participaci[oó]n (vecinal|ciudadana)|audiencia p[uú]blica", ["4.5", "4.6", "4.3", "4.6-r2", "anexo-1"]),
    ("reclamos y aplicación municipal", r"reclamo|aplicaci[oó]n (municipal|de reclamos)|\b147\b|reseñas|san isidro digital", ["4.11", "4.11-r1", "proponemos"]),
    ("habilitaciones e inspecciones", r"habilitaci|inspector|inspecci|clausura|coima", ["5.9", "5.9-r2", "anexo-4"]),
    ("puestos de la costa", r"foodtruck|food truck|puestos? n[aá]utic|\bba[nñ]os\b|playones?|canon", ["5.5", "5.5-r11", "5.5-r8", "anexo-12"]),
    ("transporte y estacionamiento", r"colectivo|\b437\b|estacionamiento|\btren\b|transporte", ["5.11", "5.5-r9"]),
    ("género y discapacidad", r"g[eé]nero|discapacidad|violencia|\bcud\b", ["5.13", "5.13-r1", "anexo-6"]),
    ("niñez y personas mayores", r"niñez|niños|adultos mayores|personas mayores", ["5.13"]),
    ("datos personales", r"datos personales|privacidad|protecci[oó]n de datos", ["4.11", "anexo-16", "anexo-4"]),
    ("Catalejo y Barisidro", r"catalejo|barisidro", ["5.5", "5.5-r8", "5.5-r14"]),
    ("tierra pública", r"paseo del [aá]guila|arsenal|tierra p[uú]blica|hip[oó]dromo", ["5.5", "5.5-r7"]),
    ("presupuesto municipal", r"presupuesto|ejecuci[oó]n|gasto", ["3.4", "5.2"]),
    ("escuela náutica", r"n[aá]utic|vela\b|kayak|guardavidas", ["5.5", "5.5-r10", "anexo-11"]),
    ("empleados municipales", r"empleados? municipal|planta de personal|fin de semana", ["5.12", "5.12-r1"]),
]

STOP = """a al algo algunas algunos ante antes como con contra cual cuando de del desde donde dos el ella ellas ellos
en entre era es esa esas ese eso esos esta estaba estas este esto estos fue fueron ha hace hasta hay la las le les lo
los mas más me mi muy no nos o otra otras otro otros para pero por porque que qué se sea ser si sí sin sobre son su sus
también tiene tienen todo todos tres un una uno unos y ya va van ir hoy año años cada san isidro municipio millones
programa vecinos""".split()

CFG = {}

CFG["05"] = dict(
    titulo="Informe 05 · Qué dicen los vecinos, no el Municipio",
    drop_secs=[],
    drop_sents=["Los datos crudos están en", "Cómo se bajaron:", "Reproducible:",
                "Están en el CSV con su texto completo",
                "Se deja anotada porque el dato del patrullero reetiquetado es chequeable y vale la pena chequearlo",
                "Ver las tres pistas de campo en la sección 9"],
    drop_blocks=["LÍMITE A DECLARAR"],
    rel=["2.2", "5.7", "5.9", "4.11", "5.6", "5.5"],
    notas=[(r"Barisidro \(septiembre de 2025\)",
            "El programa final (5.5-r14) dice que Catalejo se demolió en junio de 2025 y Barisidro en agosto de 2025, no en septiembre.")],
)

NOTA_731 = ("El informe 08 aclaró después que la base de 731 presentaciones cubre sólo entre el 24% y el 28% de los "
            "expedientes del Concejo; rehecho el conteo sobre el registro completo, las conclusiones de fondo se sostuvieron.")

CFG["06"] = dict(
    titulo="Informe 06 · Qué propone el MDF en el Concejo, y la venta de tierra pública",
    drop_blocks=["**Conclusión operativa:**", "**Recomendación:** no usarlo"],
    drop_sents=["Conviene usar el nombre correcto según de qué se hable.",
                "Si el documento necesita hablar de esto",
                "Antes de usarlo en el documento hace falta"],
    rel=["5.5", "4.7", "5.5-r7"],
    notas=[(r"731 presentaciones|las 40 presentaciones|\b731\b", NOTA_731)],
)

CFG["07"] = dict(
    titulo="Informe 07 · Cianni, el hipódromo y el clasificador del cuadro 6",
    hide_titles=["Punto 1 · El riesgo de que nos digan que les copiamos"],
    drop_blocks=["**Lo que esto significa, sin vueltas.**",
                 "**Por lo tanto la nota al pie no puede decir",
                 "**Decisión que no tomo yo**"],
    drop_sents=["Esto es lo que hay que poder mostrar si alguien cuestiona la respuesta.",
                "ese renglón está ahí por decisión nuestra, no por el clasificador"],
    rel=["4.7", "1.3", "5.8"],
    notas=[(r"731 presentaciones|\b731\b", NOTA_731)],
)

CFG["08"] = dict(
    titulo="Informe 08 · Los textos de los antecedentes",
    drop_blocks=["**La lectura política, en una línea:**", "**Lo que esto significa para el documento:**",
                 "**Un detalle que conviene tener a mano.**"],
    drop_sents=["Lo que sí es un hecho es que **existe, es anterior a nuestro documento"],
    rel=["4.7", "4.11", "5.3-r1", "3.5"],
)

NOTA_09_ALT = ("El programa final (3.5 y anexo-3) adoptó la tabla nueva con la escala de ARBA y una facturación de la parte "
               "tierra 10,9% mayor, con un tope de suba de 25% por año; descartó la variante «a igual recaudación» y la "
               "alternativa A («nadie baja»), y calcula lo cobrado con el 74% de cobranza del ABL, no con el 89,32%.")
NOTA_09_COBRO = ("El programa final (3.5) calcula lo cobrado con el peor caso de cobranza del ABL, 74%: la tabla nueva trae "
                 "1.637, 4.851 y 5.936 millones los tres primeros años y entre 5.946 y 5.983 desde el cuarto, y los 1.242 "
                 "millones que faltan salen del gasto flexible.")
CFG["09"] = dict(
    titulo="Informe 09 · Escenario B de la base de valuación",
    drop_secs=[r"^Fuentes, todas en el repo"],
    drop_blocks=["**28 de septiembre: todas las tablas por localidad están rehechas.**",
                 "**Los porcentajes que hoy cita el documento",
                 "Lo que sigue es el informe original: las alternativas antes de la decisión."],
    drop_sents=["La elección entre esa versión de B y A es tuya.", "el documento declara el rango",
                "**No se escala el programa** (25/09)"],
    rel=["3.5", "3.5-r2", "anexo-3"],
    descartado=[(r"^(La respuesta|Qué se calculó|Resultados por localidad|La boleta típica|Lo que queda afuera)", NOTA_09_ALT),
                (r"Se cobra al 89,32%|7\.225,2 cobrados|cobra 7\.225,2|necesita \*?\*?cobrar\*?\*? 7\.225,2|necesita cobrar 7\.225,2", NOTA_09_COBRO)],
    notas=[(r"Acassuso \| 470,3", "El cuadro 17 del programa final (3.5) da 2,32× para Acassuso, no 2,31×; el resto del cuadro coincide.")],
)

NOTA_10_3 = ("El programa final (5.3 y anexo-10) reemplazó el 3% por una subcontratación del 20% de cada licitación a pymes "
             "de San Isidro, con una parte igual al 5% del contrato reservada a empresas de menos de cinco años.")
CFG["10"] = dict(
    titulo="Informe 10 · El semillero de empresas",
    strip=[" y corrección 178"],
    drop_sents=["Antes de usarlo en el documento"],
    allow=["primer cliente", "Primer cliente", "sin cliente", "tienen cliente", "el cliente y no el subsidio",
           "es el cliente: el semillero", "el cliente, no el subsidio", "clientes del exterior", "traen clientes",
           "con cliente, mentores"],
    rel=["5.3", "anexo-10", "3.4"],
    descartado=[(r"^La propuesta original", NOTA_10_3),
                (r"La propuesta original, que se reemplazó|Tres razones para el 3%|3% de cada contrato|El 3% sale del precio", NOTA_10_3)],
    notas=[(r"22,0%", "El programa final (4.11 y 5.3) dice que la plataforma de inteligencia artificial y el semillero usan juntos el 27,1% de la partida de Ciencia y Técnica."),
           (r"\| 27 \| 138 \||\b771\b", "El programa final (6.4) dice que en el mes 27 egresan los primeros 231 alumnos y que en el mandato egresan 1.286.")],
)

NOTA_CATALEJO = ("El programa final (5.5) dice, según quienes manejaban los locales, que el permiso para usar esa tierra lo "
                 "daba la Provincia y que el canon se le pagaba a la Provincia; el Municipio sólo daba la habilitación del local.")
NOTA_ARENA = ("El programa final (5.5 y 5.5-r3, punto 6) sí propone recuperar la arena: tramos piloto sobre una base de "
              "piedra, como la playa de Pacheco, con guardavidas y baño habilitado según la bandera del día.")
NOTA_COSTA = ("El programa final (5.5-r3) propone rejas en unas diez bocas, revisadas cada semana y después de cada lluvia; "
              "barreras flotantes en «J» en Perú y Alto Perú, vaciadas después de cada lluvia fuerte y de cada sudestada; "
              "una cuadrilla municipal de la costa, muestras de agua con bandera diaria, un convenio con los municipios "
              "vecinos y tramos piloto de arena. Mantener todo cuesta de 139 a 346 millones por año.")
NOTA_CAUTELAR = ("El programa final (5.5) dice que la cautelar se obtuvo en julio de 2025, que la Cámara la confirmó en "
                 "septiembre y que un juzgado la levantó el 30 de diciembre de 2025, en una resolución que todavía no está firme.")

CFG["05"]["notas"] = CFG["05"]["notas"] + [(r"cautelar|suspender\*?\*? la construcción", NOTA_CAUTELAR)]
CFG["06"]["notas"] = [(r"Amparo|amparo|suspensión de la obra", NOTA_CAUTELAR)] + CFG["06"]["notas"]

CFG["11"] = dict(
    titulo="Informe 11 · La costa de San Isidro: la basura, la arena y quién decide",
    drop_sents=["Se agotó el cupo de búsquedas.", "Cómo se contrata, sin chocar con el contrato de recolección, se define con el informe 12."],
    drop_blocks=["**Se agotó el cupo de búsquedas web**", "**El sitio del Municipio** manda su certificado",
                 "**Archivos de más de 20 MB no se guardaron**", "**Los 1.054 números de *Caras y Caretas***"],
    rel=["5.5", "5.5-r3", "5.5-r1", "anexo-11"],
    descartado=[(r"^Borrador de la propuesta", NOTA_COSTA + " " + NOTA_ARENA),
                (r"El programa no promete playa|La arena, sólo con estudio", NOTA_ARENA)],
    notas=[(r"\"Playa\" no quería decir arena|«Playa» no quería decir arena|Playa\" no quería decir arena",
            "El informe 15 corrigió esta conclusión, y el programa final (5.5) dice que hay notas y fotos de 1934 y 1937 que muestran arena en San Isidro."),
           (r"Interceptor", "El informe 16 corrigió el costo del Interceptor: los nuevos de Los Ángeles costarían de 5 a 8 millones de dólares cada uno.")],
)

NOTA_12_PASIVO = ("El programa final (5.5-r4 y anexo-9) eligió que el Municipio pague, después de auditarla, la antigüedad que cada "
                  "trabajador acumuló hasta el cambio de empresa, con un padrón que se congela el día del llamado; desde ese día, "
                  "cada empresa pone la antigüedad nueva en su precio.")
NOTA_12_ZONAS = "El programa final (5.5-r4 y anexo-9) licita el servicio en dos zonas, por separado, sin una zona testigo a cargo del Municipio."
NOTA_12_COSTA = ("El programa final (5.5-r4 y 5.5-r3) deja la costa fuera del contrato y la limpia una cuadrilla municipal; para vaciar "
                 "rejas y barreras llama a concurso a cooperativas de trabajo de San Isidro, con contrato por resultado.")
CFG["12"] = dict(
    titulo="Informe 12 · La recolección de residuos: por qué no cambia y cómo salir",
    drop_secs=[r"^Qué dice hoy el documento y qué dicen las fuentes"],
    drop_sents=["No se usa.", "No se usa en el programa."],
    rel=["5.5", "5.5-r4", "anexo-9"],
    descartado=[(r"Las dos opciones para el pasivo", NOTA_12_PASIVO),
                (r"La zona testigo municipal", NOTA_12_ZONAS),
                (r"D5 · La costa, en detalle.*Opción \| A favor|A\. Meterla en el contrato nuevo", NOTA_12_COSTA)],
    notas=[(r"^Borrador de la propuesta", "Coincide en lo central con el programa final (5.5-r4 y anexo-9): dos zonas licitadas por separado, continuidad de los trabajadores, pago por resultados medidos, reciclables fuera del contrato y la costa a cargo de una cuadrilla municipal.")],
)

NOTA_13 = ("El programa final (5.5-r7 y anexo-13) tomó la audiencia pública y el dictamen de la comisión vecinal, previos y "
           "obligatorios; el compromiso del intendente de no otorgar por decreto ni promulgar lo que la zona rechace, y una "
           "contribución del 15% de la valorización. No incluyó achicar el apartamiento del 10% ni exigir ordenanza para cada "
           "Urbanización Especial.")
CFG["13"] = dict(
    titulo="Informe 13 · El urbanismo: quién decide y cómo se frenan las excepciones que no se justifican",
    drop_blocks=["**Probado y sospechado van separados.**"],
    drop_sents=["Hay que decir las dos cosas o cambiar la frase.", "Conviene escribir \"en veintidós días hábiles"],
    strip=[" (documento, 5.5)", " (cita de vecinos que usa el documento)"],
    rel=["5.5", "5.5-r7", "anexo-13"],
    descartado=[(r"^Borrador de la propuesta", NOTA_13)],
)

NOTA_14 = ("El programa final (5.5-r13 y anexo-12) pide licitación propia para toda obra nueva en parques y costa, cualquiera "
           "sea su monto; evaluación de impacto ambiental para toda obra en la costa, y en vez de audiencia, la recomendación "
           "de un panel de vecinos sorteados; en los parques decide la comisión vecinal de la zona, con el dictamen de la "
           "asociación del parque.")
CFG["14"] = dict(
    titulo="Informe 14 · Cemento o naturaleza en parques y costa",
    drop_sents=["Es el primer dato que el programa tendría que publicar."],
    rel=["5.5", "5.5-r13", "anexo-12", "anexo-14"],
    descartado=[(r"^Borrador de la propuesta", NOTA_14),
],
    notas=[(r"Decretos 605 y 748", "El informe 17 corrigió que los Decretos 605 y 748 de 2025 son sólo de Barisidro; Catalejo salió por un convenio de devolución (Decreto 1778/2024).")],
)

CFG["15"] = dict(
    titulo="Informe 15 · ¿Había arena en las playas de San Isidro?",
    drop_secs=[r"^E2 · Cómo registrar los testimonios", r"^G · Qué se puede afirmar en el programa", r"^H · Lo que falta"],
    drop_sents=["Si el programa quiere explicar qué pasó o proponer algo", "La vía gratis que queda está en la sección H",
                "Eso deja afuera los escaneos pagos", "Lo que falta y cómo conseguirlo sin eso está en la sección H"],
    rel=["5.5", "5.5-r3"],
    notas=[(r"0% de sitios aptos", "El informe 16 corrigió que ese dato es de la red nacional de monitoreo, no de la Ciudad.")],
)

NOTA_16 = NOTA_COSTA + " " + NOTA_ARENA
CFG["16"] = dict(
    titulo="Informe 16 · Limpiar el agua y la costa, de verdad",
    drop_blocks=["**Por qué.** El cliente descartó la playa seca"],
    rel=["5.5", "5.5-r3", "5.5-r1", "5.5-r2", "anexo-11"],
    descartado=[(r"^Borrador de la propuesta", NOTA_16)],
    notas=[(r"hasta 4 veces por semana|hasta cuatro veces por semana", "El informe 17 encontró que los datos de la Intendencia de Montevideo dicen 2 muestras por semana en verano; las dos fuentes no coinciden.")],
)

NOTA_17B = ("El programa final (5.5-r9) mide con cámaras que cuentan gente en los accesos de los 21 playones, conecta la "
            "inteligencia artificial del Municipio con el Tren de la Costa y el Mitre en tiempo real, no cobra estacionamiento "
            "ni construye playones, y suma actividades fijas de lunes a jueves en cada puesto de la costa.")
CFG["17"] = dict(
    titulo="Informe 17 · La costa como lugar vivo: habilitaciones, tránsito y todo el año",
    drop_blocks=["**Para poder escribir lo que contó como un hecho**", "**La IA que propone el borrador del programa**"],
    rel=["5.5", "5.5-r8", "5.5-r9", "5.5-r14", "anexo-12"],
    descartado=[(r"^Borrador de la propuesta", NOTA_17B),
                (r"permiso municipal precario|precario y gratuito|Permiso precario|cobrará directamente los cánones|El Municipio dio en 1996 el \*?\*?permiso de uso|no pagó \"?suma alguna|Las tres cosas quedan una al lado de la otra", NOTA_CATALEJO)],
)

# oraciones de proceso que se repiten en varios informes: herramientas, pendientes y avisos al equipo
GENERIC_DROP_SENTS = [
    "WebFetch", "pdf.js", "shadow DOM", "Vía primaria pendiente", "hay que reconfirmarla", "antes de publicar hay que",
    "hay que confirmarla con el pliego", "hay que confirmarlo con la Subsecretaría", "Conviene confirmar su vigencia formal",
    "Hay que abrirlos a mano", "Hay que pedírselo a la Dirección", "Fuente pendiente e importante", "Nota técnica que vale para todo el proyecto",
    "más incómodo para un documento de gobierno municipal", "el documento **no puede apoyarse", "el documento no puede apoyarse",
    "que conviene zanjar leyendo el original", "**[PRENSA]**, pendiente", "→ **[PRENSA]**, pendiente",
    "Es contexto para el equipo", "contexto para el equipo", "No pasa al programa mientras no haya una resolución judicial",
    "Se agotó el cupo", "no se tocó `doc/`", "Sólo investigación: no se tocó",
    "el documento no los nombra", "el documento no las nombra", "del borrador del programa",
    "esto se conecta con lo que el documento ya propone", "Lo marcado \"[a decidir]\" no está decidido",
]

NOTA_SHOWS = ("El programa final (5.5-r12) calcula que los 200 shows cuestan unos 394 millones por año (532 el primer año, "
              "con la compra de los equipos), de los cuales 270,6 son para los artistas, pagados por músico con el piso del "
              "sindicato más 25%; 114 son al aire libre y 86 bajo techo, en espacios que cuestan 14,1 millones por año, y los "
              "tres grupos de producción, con ocho personas, cuestan 85,3 millones por año.")
NOTA_TEL = ("El programa final (5.9 y anexo-4) usa el teléfono propio de cada agente, que se compra en 24 cuotas sin interés por "
            "un convenio con el banco que paga los sueldos; el Municipio paga los datos, el soporte de pecho y la batería. En la "
            "primera etapa graban de 208 a 280 agentes, con un costo de 20,5 a 27,5 millones una vez y de 107,6 a 145,5 por año, "
            "y las grabaciones se guardan dos años en una nube con servidores en Bélgica.")
NOTA_PROF = ("El programa final (5.8 y 5.8-r1) da el profesor digital gratis a los 22.748 alumnos de escuelas públicas y de "
             "privadas con aporte estatal del 100%, con un costo de 151,9 a 180,5 millones por año con el uso esperado; el alumno "
             "de un colegio privado que lo usa paga lo que usa.")
NOTA_DOLAR = "El programa final pasa los dólares a pesos con el dólar de diciembre de 2025, $1.447,84 (nota de método), no con $1.520."

CFG["182"] = dict(excluir=True,
                  motivo="Es una lista interna de cambios de redacción del documento («Hoy como hoy, lo nuestro con marca»), no una investigación.")

NOTA_18_AB = ("El programa final (5.11-r1 y 5.11-r2) no fija el monto de la multa como porcentaje del ingreso ni del valor del auto: "
              "propone cuotas sin trámites con un tope del 2% del ingreso dividido por la raíz de la cantidad de personas del "
              "hogar, un tope a la deuda total según el ingreso y el valor del vehículo, y le pide a la Provincia un pago voluntario "
              "según el ingreso y una multa según el ingreso sólo para subirla a quien más gana, en faltas graves.")
CFG["18"] = dict(
    titulo="Informe 18 · Las multas de tránsito",
    hide_titles=["4 · La idea del cliente", "La prueba con los casos del cliente [cálculo propio]"],
    drop_secs=[r"^1\.6 La causa judicial"],
    drop_blocks=["Según la prensa, hay una causa federal en trámite", "**Si la UNSO está alcanzada por alguna investigación.**",
                 "**¿Aparece en la causa?**", "Sólo una nota de opinión (Agencia Comunas", "**Aparte de la causa, en Pilar:**",
                 "Con un auto de 10 millones, una multa de 1 millón es desproporcionada", "Con un ingreso de 1 millón por mes, una multa de 300.000",
                 "**Las opiniones jurídicas** (marcadas [inferencia]) necesitan dictamen"],
    strip=["**Dato para el equipo:** "],
    rel=["5.11", "5.11-r1", "5.11-r2", "anexo-15", "anexo-16"],
    descartado=[(r"^4\.[12] Opción [AB]|Opción A: que la multa no pueda superar|Opción B: un porcentaje del valor fiscal", NOTA_18_AB),
                (r"^Borrador de propuesta(?! · segunda)", NOTA_18_AB)],
)

NOTA_19_TRABAJO = ("El programa final (5.11-r1 y 5.11-r2) no incluye trabajo comunitario en lugar de la multa: propone cuotas sin "
                   "trámites con un tope según el ingreso, el juez que fija las cuotas sin que el vecino vaya, y pedidos a la Provincia.")
CFG["19"] = dict(
    titulo="Informe 19 · Multas: ¿la rebaja puede ser automática?",
    rel=["5.11-r1", "5.11-r2", "anexo-15", "anexo-16"],
    descartado=[(r"^7 · Trabajo en vez de plata|7 · Trabajo en vez de plata: NO SE SABE", NOTA_19_TRABAJO)],
)

CFG["20"] = dict(
    titulo="Informe 20 · Puestos náuticos: foodtrucks y baños, y cuánto se cobra del ABL",
    rel=["5.5-r11", "5.5-r8", "5.5-r10", "3.5", "anexo-14"],
    notas=[(r"1\.520", NOTA_DOLAR)],
)

CFG["21"] = dict(
    titulo="Informe 21 · Ruido y prueba sellada del vecino",
    rel=["5.5", "5.5-r5", "5.5-r6", "anexo-8"],
)

CFG["22"] = dict(
    titulo="Informe 22 · Profesores digitales particulares",
    rel=["5.8", "5.8-r1", "anexo-2"],
    descartado=[(r"\$29\.387 M|29\.387 millones", "El informe 23 recalculó el costo con el avatar a precio de volumen. " + NOTA_PROF)],
    notas=[(r"1\.520", NOTA_DOLAR)],
)

CFG["23"] = dict(
    titulo="Informe 23 · Costos con la opción óptima en calidad y precio, puente con los laboratorios de IA, espectáculos al aire libre, turnos médicos, y género y discapacidad",
    strip=["**Ojo:** "],
    drop_secs=[r"^Tabla A · Costos"],
    drop_sents=["Es una pregunta abierta para el cliente"],
    rel=["5.8-r1", "5.3-r3", "5.5-r12", "5.6", "5.13", "4.11"],
    descartado=[(r"Canon de los colegios privados|canon al costo|\$2\.039 a 2\.486", NOTA_PROF),
                (r"A3 · Redes en los desagües|33 a 75 M por año", NOTA_COSTA),
                (r"^C · Espectáculos|Tabla C · Espectáculos", NOTA_SHOWS),
                (r"cámaras corporales|cámara corporal", NOTA_TEL)],
    notas=[(r"1\.520", NOTA_DOLAR)],
)

CFG["23b"] = dict(
    titulo="Informe 23 bis · Redes que no tapan, teléfonos de los inspectores, escuelas parroquiales y cooperativas, espectáculos y mensajes de texto",
    drop_sents=["Si «costo completo» incluye o no el equipo de personas lo decide"],
    drop_blocks=["**El texto del documento** dice «vaciadas todos los días»"],
    rel=["5.5-r3", "5.9", "anexo-4", "5.8-r1", "5.5-r12", "5.11-r1"],
    descartado=[(r"^2 · Teléfonos|420 agentes|94 a 147 M", NOTA_TEL),
                (r"^3 · Escuelas parroquiales|136 y 166 M|escuelas parroquiales y cooperativas son gratis", NOTA_PROF),
                (r"^4 · Espectáculos|100 shows por año cuestan|93 M de compra", NOTA_SHOWS)],
)

CFG["23c"] = dict(
    titulo="Informe 23 ter · Recálculo: teléfonos, escuelas y espectáculos",
    hide_titles=["3.1 · Costo de los 200 shows con la regla de Nick", "3.6 · Definiciones de Nick y verificación de Spotify"],
    rel=["5.9", "anexo-4", "5.8-r1", "5.5-r12"],
    descartado=[(r"1\.6 · Guarda en Europa|6 meses rápida|1\.7 · Costo por etapa|19,8 a 26,5|104,4 a 141", NOTA_TEL),
                (r"^3 · Espectáculos|214,0 M|106,8 M por año|125,9 M de compra|200 shows de emergentes", NOTA_SHOWS)],
)

CFG["23d"] = dict(
    titulo="Informe 23 quáter · Lo que falta para cerrar: inspectores, grabaciones públicas, invierno y volumen",
    rel=["5.9", "anexo-4", "5.5-r12", "anexo-8"],
    descartado=[(r"3\.4 · Costo de los shows de invierno|3\.5 · Costo de los 200 shows|13,8 M por año|202,6 M|unos 326 M", NOTA_SHOWS)],
)

CFG["23e"] = dict(
    titulo="Informe 23 quinquies · Barreras de Perú y Alto Perú, y la temporada bajo techo",
    rel=["5.5-r3", "5.5-r12"],
    descartado=[(r"^2 · Temporada bajo techo|2\.2 · Cuántos clubes y cuánto cuestan|2\.3 · Costo de los 200 shows|17,8 M|201,9 M|unos 329 M", NOTA_SHOWS)],
)

NOTA_01_RECOLECCION = ("El informe 12 actualizó y corrigió este informe: fracasaron cuatro licitaciones del servicio principal "
                       "(01/2004, 17/2008, 40/2019 y 41/2022) y el mismo grupo presta el servicio desde 1998, como dice el programa final (5.5).")
CFG["01"] = dict(
    titulo="Informe 01 · El contrato de recolección de residuos y el mercado de trabajo de la inteligencia artificial",
    strip=["**ADVERTENCIA CRÍTICA PARA EL DOCUMENTO:** "],
    rel=["5.5", "5.3", "5.3-r2", "4.11"],
    notas=[(r"^TAREA A|^INFORME|recolecci[oó]n", NOTA_01_RECOLECCION)],
)
CFG["02"] = dict(
    titulo="Informe 02 · Inteligencia artificial en la salud municipal",
    rel=["5.6", "5.6-r1", "5.6-r2", "5.6-r3", "5.6-r4"],
)
CFG["03"] = dict(
    titulo="Informe 03 · Transparencia municipal, la línea 437, el ruido de los vehículos y el video municipal en investigaciones penales",
    rel=["5.10", "2.2", "5.11", "5.5-r5", "5.7"],
)
CFG["04"] = dict(
    titulo="Informe 04 · Qué tiene hoy el Municipio en niñez, personas mayores, género, discapacidad y cultura",
    rel=["5.13", "5.13-r1", "5.8", "anexo-7"],
    descartado=[(r"permisos precarios y gratuitos", NOTA_CATALEJO)],
)

# temas por defecto de cada informe, para los pasajes con menos de dos temas propios
CFG["02"]["temas"] = ['salud', 'inteligencia artificial']
CFG["03"]["temas"] = ['transparencia', 'seguridad y cámaras']
CFG["04"]["temas"] = ['género y discapacidad', 'cultura y espectáculos']
CFG["06"]["temas"] = ['Concejo Deliberante', 'tierra pública']
CFG["07"]["temas"] = ['Concejo Deliberante', 'tierra pública']
CFG["08"]["temas"] = ['Concejo Deliberante', 'participación vecinal']
CFG["09"]["temas"] = ['tasa y valuación', 'presupuesto municipal']
CFG["10"]["temas"] = ['semillero de empresas', 'empleo y formación']
CFG["11"]["temas"] = ['costa y río', 'basura en el agua']
CFG["12"]["temas"] = ['recolección de residuos', 'presupuesto municipal']
CFG["13"]["temas"] = ['urbanismo', 'participación vecinal']
CFG["14"]["temas"] = ['parques y espacios verdes', 'costa y río']
CFG["15"]["temas"] = ['arena y playas', 'costa y río']
CFG["16"]["temas"] = ['calidad del agua y cloacas', 'costa y río']
CFG["17"]["temas"] = ['costa y río', 'puestos de la costa']
CFG["18"]["temas"] = ['multas de tránsito', 'seguridad y cámaras']
CFG["19"]["temas"] = ['multas de tránsito', 'datos personales']
CFG["20"]["temas"] = ['puestos de la costa', 'costa y río']
CFG["21"]["temas"] = ['ruido', 'habilitaciones e inspecciones']
CFG["22"]["temas"] = ['educación', 'inteligencia artificial']
CFG["01"]["temas"] = ["empleo y formación", "inteligencia artificial"]
CFG["05"]["temas"] = ["reclamos y aplicación municipal", "participación vecinal"]
CFG["23"]["temas"] = ["presupuesto municipal", "inteligencia artificial"]
CFG["23b"]["temas"] = ["presupuesto municipal", "habilitaciones e inspecciones"]
CFG["23c"]["temas"] = ["presupuesto municipal", "habilitaciones e inspecciones"]
CFG["23d"]["temas"] = ["presupuesto municipal", "cultura y espectáculos"]
CFG["23e"]["temas"] = ["basura en el agua", "cultura y espectáculos"]

# ---- ajuste final: «descartado» sólo cuando el pasaje trata de la opción que el programa no tomó;
#      si el pasaje sólo menciona una cifra superada entre otras cosas válidas, va una nota sin marcarlo
NOTA_EMERGENTE = ("El programa final (5.5-r12) considera emergente al artista con menos de 50.000 oyentes por mes en Spotify "
                  "(captura con fecha, declaración jurada y acceso de lector a su cuenta), y local al que tiene al menos la mitad "
                  "de sus integrantes con domicilio en San Isidro en el DNI.")
NOTA_RESUMEN_23 = ("Varias cifras de este resumen se recalcularon después en los informes 23 bis a 23 quinquies; las que valen son "
                   "las del programa final (5.8, 5.9, 5.5-r3 y 5.5-r12).")

CFG["09"]["descartado"] = [(r"^(La respuesta|Qué se calculó|Resultados por localidad|La boleta típica|Lo que queda afuera)", NOTA_09_ALT)]
CFG["09"]["notas"] = [(r"89,32%|7\.225,2 cobrados", NOTA_09_COBRO)] + CFG["09"]["notas"]

CFG["10"]["descartado"] = [(r"^La propuesta original", NOTA_10_3),
                           (r"La propuesta original, que se reemplazó|Tres razones para el 3%", NOTA_10_3)]
CFG["10"]["notas"] = [(r"3% de cada contrato|El 3% sale del precio|el 3%", NOTA_10_3)] + CFG["10"]["notas"]

CFG["12"]["descartado"] = [(r"Las dos opciones para el pasivo", NOTA_12_PASIVO),
                           (r"D2 · Las zonas, en detalle", NOTA_12_ZONAS),
                           (r"A\. Meterla en el contrato nuevo", NOTA_12_COSTA)]

CFG["19"]["descartado"] = [(r"^Segunda parte .* › 7 · Trabajo en vez de plata: detalle", NOTA_19_TRABAJO)]
CFG["19"]["notas"] = [(r"Trabajo en vez de plata", NOTA_19_TRABAJO)]

CFG["22"]["descartado"] = []
CFG["22"]["notas"] = [(r"\$29\.387 M|29\.387 millones", "El informe 23 recalculó el costo con el avatar a precio de volumen. " + NOTA_PROF),
                      (r"1\.520", NOTA_DOLAR)]

CFG["23"]["descartado"] = [(r"Canon de los colegios privados|Los cuatro escenarios, todo incluido", NOTA_PROF),
                           (r"A3 · Redes en los desagües", NOTA_COSTA),
                           (r"^C · Espectáculos|Tabla C · Espectáculos", NOTA_SHOWS),
                           (r"A2 · Habilitaciones y analítica", NOTA_TEL)]
CFG["23"]["notas"] = [(r"^Respuestas en una línea|^Las cinco tablas", NOTA_RESUMEN_23), (r"1\.520", NOTA_DOLAR)]

CFG["23b"]["descartado"] = [(r"^2 · Teléfonos", NOTA_TEL),
                            (r"^3 · Escuelas parroquiales", NOTA_PROF),
                            (r"4\.1 · Equipo de producción municipal|4\.2 · Cuánto cobra un artista emergente", NOTA_SHOWS),
                            (r"4\.3 · Quién es «artista del partido»", NOTA_EMERGENTE)]
CFG["23b"]["notas"] = [(r"^Respuestas en una línea|^Tabla final", NOTA_RESUMEN_23)]

CFG["23c"]["descartado"] = [(r"1\.6 · Guarda en Europa|1\.7 · Costo por etapa", NOTA_TEL),
                            (r"214,0 M|202,8 a 227,0", NOTA_SHOWS)]
CFG["23c"]["notas"] = [(r"^Respuestas en una línea|^Tabla final", NOTA_RESUMEN_23),
                       (r"81 a 103|201 a 270", NOTA_TEL)]

CFG["23d"]["descartado"] = [(r"3\.4 · Costo de los shows de invierno|3\.5 · Costo de los 200 shows", NOTA_SHOWS)]
CFG["23d"]["notas"] = [(r"^Respuestas en una línea|^Tabla final", NOTA_RESUMEN_23)]

CFG["23e"]["descartado"] = [(r"^2 · Temporada bajo techo", NOTA_SHOWS)]
CFG["23e"]["notas"] = [(r"17,8 M|201,9 M|unos 329 M", NOTA_SHOWS)]
CFG["23"]["descartado"] = [(r"\A[^\n]*(Canon de los colegios privados|Los cuatro escenarios, todo incluido)", NOTA_PROF),
                           (r"\A[^\n]*A3 · Redes en los desagües", NOTA_COSTA),
                           (r"\A(C · Espectáculos|[^\n]*Tabla C · Espectáculos)", NOTA_SHOWS),
                           (r"\A[^\n]*A2 · Habilitaciones y analítica", NOTA_TEL)]
CFG["23c"]["descartado"] = [(r"\A[^\n]*(1\.6 · Guarda en Europa|1\.7 · Costo por etapa)", NOTA_TEL),
                            (r"\A3 · Espectáculos: 200 shows\n.*214,0 M", NOTA_SHOWS)]
CFG["23c"]["notas"] = CFG["23c"]["notas"] + [(r"214,0 M|6 meses rápida", NOTA_SHOWS + " " + NOTA_TEL)]
CFG["19"]["drop_blocks"] = CFG["19"].get("drop_blocks", []) + ["Ahí están la Ley 24.449, la Ley 13.927"]
CFG["19"]["notas"] = [(r"\n[\s\S]*(Trabajo en vez de plata|trabajo comunitario)", NOTA_19_TRABAJO)]
CFG["05"]["notas"] = [CFG["05"]["notas"][0], (r"suspender\*?\*? la construcción|ex Arsenal|una cautelar judicial\*?\*?: los vecinos", NOTA_CAUTELAR)]
