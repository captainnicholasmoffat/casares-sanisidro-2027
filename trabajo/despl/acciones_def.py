# Definición de las acciones del plan de despliegue «San Isidro 2027».
# Cada acción sale del texto final del programa (commit c462fcf).
from cal import D, M, E, fecha_larga

STREAMS = {
    "T": "0 Transición",
    "M": "1 Mecanismo vecinal y obra pública",
    "C": "2 Concejo y ordenanzas",
    "P": "3 Presupuesto y tasas",
    "I": "4 Inteligencia artificial del Municipio",
    "E": "5 Empleo y formación",
    "V": "6 Vivienda",
    "S": "7 Salud",
    "G": "8 Seguridad",
    "K": "9 Costa y espacio público",
    "U": "10 Cultura y espectáculos",
    "H": "11 Habilitaciones e inspecciones",
    "X": "12 Transparencia",
}

TEAM = {
    "Intendente electo": "Intendencia",
    "Intendente": "Intendencia",
    "Intendente con la UNSO": "Intendencia",
    "Intendente con cada área": "Intendencia",
    "Intendente con el CFL 404 y la Provincia": "Intendencia",
    "Intendente con los trabajadores municipales": "Intendencia",
    "Intendente con Tránsito y el Juzgado de Faltas": "Intendencia",
    "Concejo Deliberante": "Concejo",
    "Asamblea de Concejales y Mayores Contribuyentes": "Concejo",
    "Secretaría de Hacienda": "Secretarías",
    "Secretaría de Hacienda con la Secretaría de Obras": "Secretarías",
    "Secretaría de Hacienda con el banco que paga los sueldos": "Secretarías",
    "Secretaría de Obras": "Secretarías",
    "Secretaría de Obras con Salud": "Secretarías",
    "Secretaría de Obras con Deportes y Ambiente": "Secretarías",
    "Secretaría de Salud": "Secretarías",
    "Secretaría de Salud con el equipo de la inteligencia artificial": "Secretarías",
    "Desarrollo Social": "Secretarías",
    "Educación (área municipal)": "Secretarías",
    "Cultura": "Secretarías",
    "Deportes": "Secretarías",
    "Ambiente": "Secretarías",
    "Tránsito y Juzgado de Faltas": "Secretarías",
    "Seguridad (Centro de Operaciones Municipal)": "Secretarías",
    "Habilitaciones y Agencia de Control": "Secretarías",
    "Habilitaciones con el equipo de la inteligencia artificial": "Secretarías",
    "Dirección de género": "Secretarías",
    "Gobierno y Legal y Técnica": "Secretarías",
    "Áreas del Municipio": "Secretarías",
    "Ciencia y Técnica": "Equipo de la IA",
    "Equipo de la inteligencia artificial del Municipio": "Equipo de la IA",
    "Comisiones vecinales": "Vecinos",
    "Comisiones vecinales con la Secretaría de Obras": "Vecinos",
    "Secretaría de Obras con las comisiones vecinales": "Secretarías",
    "Asociaciones de parque": "Vecinos",
    "Panel de vecinos sorteados": "Vecinos",
    "Organización independiente que sortea el panel": "Externos",
    "Junta Electoral de la Provincia": "Externos",
    "Abogado especialista en municipios": "Externos",
    "UNSO y CFL 404": "Externos",
    "Empresas de San Isidro": "Externos",
    "Ministerio de Educación de la Nación": "Externos",
    "Nación": "Externos",
    "Provincia de Buenos Aires": "Externos",
    "AySA": "Externos",
    "Tribunal de Cuentas de la Provincia": "Externos",
    "Universidades de San Isidro": "Externos",
}

LIC = "Duración del programa: cada licitación se adjudica tres meses después del llamado (nota del cuadro 42)."
TREINTA = "Duración del programa: treinta días corridos, unos 22 días hábiles."
TRAT = ("Duración estimada: 22 días hábiles, lo que tardó la única reforma de las reglas de urbanismo "
        "que pasó por el Concejo, la Ordenanza 9432 (5.5).")
RECESO = ("Supuesto: se cuenta desde el 1 de marzo, cuando abren las sesiones ordinarias (6.6). "
          "El programa no dice si se aprueba en diciembre.")
TRECE = "Aprobarla o no. Hacen falta trece votos de veinticuatro, y ningún bloque llega solo (4.7)."


def W(a, b=None, label=None):
    b = a if b is None else b
    if label is None:
        label = f"mes {a}" if a == b else f"meses {a} a {b}"
    return (M(a), E(b), label)


DIC = (D(2027, 12, 10), D(2027, 12, 31), "sesión extraordinaria de diciembre de 2027, en el mes 1")
MAR1 = (D(2028, 3, 1), D(2028, 3, 1), "1 de marzo de 2028, cuando abren las sesiones ordinarias (mes 3)")
AÑO1 = W(1, 12, "año 1 (meses 1 a 12)")
FIN = W(48, 48, "mes 48, al final del mandato")

A = []


def act(code, task, owner, **kw):
    a = dict(code=code, task=task, owner=owner)
    a.update(kw)
    A.append(a)


# ---------------------------------------------------------------- 0 Transición
act("T01", "Elección general de intendente y concejales", "Junta Electoral de la Provincia",
    ms=True, fixed=D(2027, 10, 24), fuente="6.1",
    steps="Votan los vecinos de San Isidro.",
    note=("Fecha estimada. El programa no da la fecha de la elección. La regla nacional es el cuarto domingo de octubre "
          "(Código Electoral Nacional, artículo 53): el 24 de octubre de 2027. A agosto de 2026, la Provincia todavía "
          "no había fijado su fecha. Se supone que vota el mismo día que la Nación."))
act("T02", "Revisión legal de las cinco ordenanzas del anexo que entran en diciembre: la 1, la 3, la 5, la 7 y la 9",
    "Abogado especialista en municipios", dur=20, est=True, needs=["T01"], fuente="anexo",
    decision="Dar por buena la redacción final de cada ordenanza.",
    steps="Redacción final. Fundamentos. Cómo encaja cada una con el Digesto de San Isidro.",
    note="El anexo es un borrador. Antes de entrar al Concejo, lo tiene que revisar un abogado especialista en municipios.")
act("T03", "Redactar el proyecto que deroga los artículos 8, 9 y 10 de la Ordenanza 6045", "Intendente electo",
    dur=5, est=True, needs=["T01"], fuente="4.10",
    steps="Se deroga sólo el poder del intendente de disolver una asociación vecinal. Las sociedades de fomento siguen existiendo.")
act("T04", "Explicar el mecanismo a los bloques del Concejo, también a los concejales que asumen en diciembre",
    "Intendente electo", dur=30, est=True, needs=["T01"], fuente="4.7",
    decision="Buscar el acuerdo de cuatro bloques: hacen falta trece votos.",
    steps="La fórmula de reparto y la subida de la partida, por escrito. El primer proyecto es la derogación, que no le cuesta nada a ningún bloque.",
    note="Riesgo crítico del 6.6: el Concejo no acompaña.")
act("T05", "Dictamen del abogado sobre las propuestas que lo necesitan antes de aplicarse",
    "Abogado especialista en municipios", dur=20, est=True, needs=["T01"], fuente="nota de método",
    steps=("El convenio con el banco de los sueldos. La compensación del teléfono propio. Quién ve cada grabación. "
           "El registro de instructores y artistas. Los shows que no cuentan como ruido molesto. Los datos de los chicos "
           "en el profesor digital. Las cuotas de las multas."),
    note="La nota de método lista estas propuestas en «Lo que tiene que confirmar un abogado».")
act("T06", "Preparar la convocatoria a la sesión extraordinaria de diciembre, con la ordenanza preparatoria de la tabla en primer lugar",
    "Intendente electo", dur=3, est=True, needs=["T02"], fuente="6.6",
    note="Riesgo del 6.6: la tabla nueva no sale en diciembre.")
act("T07", "Asume el intendente", "Intendente", ms=True, fixed=D(2027, 12, 10),
    needs=["T02", "T03", "T04", "T06"], fuente="6.1",
    note="Fecha del programa: el mandato empieza el 10 de diciembre de 2027.")

# ---------------------------------------------------------------- 2 Concejo y ordenanzas
act("C01", "Entra al Concejo el proyecto que deroga los artículos 8 a 10 de la Ordenanza 6045 (compromiso 1)",
    "Intendente", ms=True, needs=[("P01", "FS", 2), "T03"], win=DIC, fuente="6.1",
    steps="Es el primer proyecto en entrar al Concejo (4.10).",
    note="Supuesto: la sesión se hace dos días hábiles después de la convocatoria.")
act("C02", "Tratamiento de la derogación en el Concejo", "Concejo Deliberante", dur=22, est=True,
    sne=D(2028, 3, 1), needs=["C01"], fuente="4.10", note=TRAT + " " + RECESO)
act("C03", "El Concejo aprueba la derogación", "Concejo Deliberante", ms=True, needs=["C02"], fuente="4.10",
    decision=TRECE, note="Es la prueba de si hay acuerdo en el Concejo (4.7).")
act("C04", "Entra la Ordenanza 1, de la partida de obra vecinal (compromiso 2)", "Intendente", ms=True,
    needs=["C01", "T02"], win=DIC, fuente="anexo.1",
    steps=("Escala de 12,5% a 50%. Fórmula de reparto entre las zonas. Voto desde los 16 años. Respuesta escrita en 30 días. "
           "Comité de vigilancia de cada obra. Intervención sin disolución. Los saldos quedan en la misma zona."))
act("C05", "Tratamiento de la Ordenanza 1 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    sne=D(2028, 3, 1), needs=["C04"], fuente="anexo.1", note=TRAT + " " + RECESO)
act("C06", "El Concejo aprueba la Ordenanza 1", "Concejo Deliberante", ms=True, needs=["C05"], fuente="anexo.1",
    decision=TRECE + " Sin acuerdo, la partida no arranca, y no hay plan por decreto.")
act("C07", "Entra la Ordenanza 3, que actualiza la tabla de valores de 2008 (compromiso 3)", "Intendente", ms=True,
    needs=["C01", "T02"], win=DIC, fuente="anexo.3",
    steps=("La alícuota no sube. Ninguna boleta sube más de 25% por año. Las bajas se aplican completas. "
           "El 10% de las propiedades de mayor valuación pierde el descuento por pago anual."))
act("C08", "Entra la Ordenanza 5, de las asociaciones de parque (compromiso 4)", "Intendente", ms=True,
    needs=["C01", "T02"], win=DIC, fuente="anexo.5",
    steps="Se empieza por las asociaciones del Parque del Águila y el Bosque Alegre.")
act("C09", "Tratamiento de la Ordenanza 5 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    sne=D(2028, 3, 1), needs=["C08"], fuente="anexo.5", note=TRAT + " " + RECESO)
act("C10", "El Concejo aprueba la Ordenanza 5", "Concejo Deliberante", ms=True, needs=["C09"], fuente="anexo.5",
    decision=TRECE)
act("C11", "Entra la Ordenanza 7, la adhesión a la Ley provincial 15.302 de espacios culturales (compromiso 5)",
    "Intendente", ms=True, needs=["C01", "T02"], win=DIC, fuente="anexo.7")
act("C12", "Tratamiento de la Ordenanza 7 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    sne=D(2028, 3, 1), needs=["C11"], fuente="anexo.7", note=TRAT + " " + RECESO)
act("C13", "El Concejo aprueba la Ordenanza 7", "Concejo Deliberante", ms=True, needs=["C12"], fuente="anexo.7",
    decision=TRECE)
act("C14", "Entra la Ordenanza 9, del pliego de la recolección de residuos (compromiso 6)", "Intendente", ms=True,
    needs=["C01", "T02"], win=DIC, fuente="anexo.9",
    steps=("Frecuencias, horarios, zonas, qué se separa, indicadores y penalidades. Dos zonas, cada una con su precio. "
           "Todos los trabajadores siguen, con su antigüedad."))
act("C15", "Tratamiento de la Ordenanza 9 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    sne=D(2028, 3, 1), needs=["C14"], fuente="anexo.9", note=TRAT + " " + RECESO)
act("C16", "El Concejo aprueba la Ordenanza 9: el pliego queda aprobado antes del llamado", "Concejo Deliberante",
    ms=True, needs=["C15"], fuente="anexo.9", decision=TRECE)
act("C17", "Revisión legal de las ordenanzas 15 y 16", "Abogado especialista en municipios", dur=10, est=True,
    needs=["T02"], fuente="anexo")
act("C18", "Entra la Ordenanza 15, de las cuotas de las multas de tránsito (compromiso 19)", "Intendente", ms=True,
    needs=["C17"], win=MAR1, fuente="anexo.15",
    steps="Anotarse una sola vez, por internet, para pagar en cuotas. Plan de pagos sin interés para las multas que ya se deben. Como la de Bragado.")
act("C19", "Tratamiento de la Ordenanza 15 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    needs=["C18"], fuente="anexo.15", note=TRAT)
act("C20", "El Concejo aprueba la Ordenanza 15", "Concejo Deliberante", ms=True, needs=["C19"], fuente="anexo.15",
    decision=TRECE)
act("C21", "Entra la Ordenanza 16, de la base de datos de las cuotas (compromiso 20)", "Intendente", ms=True,
    needs=["C17", ("C18", "SS", 0)], win=MAR1, fuente="anexo.16",
    steps="Guarda el ingreso y cuántas personas viven en el hogar. Se usa sólo para las multas. Se presenta junto con la Ordenanza 15.")
act("C22", "Tratamiento de la Ordenanza 16 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    needs=["C21"], fuente="anexo.16", note=TRAT)
act("C23", "El Concejo aprueba la Ordenanza 16", "Concejo Deliberante", ms=True, needs=["C22"], fuente="anexo.16",
    decision=TRECE)
act("C24", "Revisión legal de las nueve ordenanzas que faltan: la 2, la 4, la 6, la 8, la 10, la 11, la 12, la 13 y la 14",
    "Abogado especialista en municipios", dur=30, est=True, needs=["C17"], fuente="anexo")

NUEVE = [
    ("C25", 2, "del Sistema de Información Municipal, que crea también la base de datos del profesor digital",
     "Todo dato se registra el día en que se genera. Sólo lo gastado del presupuesto se muestra cada tres meses."),
    ("C28", 6, "de la partida propia de género",
     "Un programa propio en el presupuesto, separado del que hoy comparte con niñez, juventud y personas mayores. No fija monto."),
    ("C31", 4, "de la grabación de las inspecciones",
     "Defiende al comerciante que denuncia. Sin grabación sellada no valen el acta, la clausura ni la habilitación."),
    ("C34", 8, "del ruido",
     "Sonómetro clase 1 o 2. Estaciones móviles. Aviso antes de multar. Prueba sellada del vecino. Mediación voluntaria."),
    ("C37", 10, "de empleo local y del semillero de empresas",
     "75% de personal de San Isidro en cada contrato. Pasantías con la UNSO. Subcontratación del 20% a pymes de San Isidro. Pago a quince días. Semillero de empresas."),
    ("C40", 11, "de la costa: el baño y la calidad del agua",
     "Baño habilitado sólo con guardavidas. Muestras dos veces por semana y bandera de cada día. Deroga la Ordenanza 5304 de 1978."),
    ("C43", 12, "de la obra en parques y costa, con el panel de vecinos sorteados",
     "Licitación propia para cada obra. Estudio de impacto ambiental. La obra en la costa pasa por un panel sorteado."),
    ("C46", 13, "de las excepciones urbanísticas",
     "Audiencia pública y dictamen de la comisión de la zona antes de cada excepción. Contribución del 15% de la valorización."),
    ("C49", 14, "de los parques y espacios verdes, con el registro gratis de instructores y artistas",
     "Los parques no se venden, no se edifican y no se achican. El 75% de los lugares del registro de instructores, para vecinos de San Isidro."),
]
for code, n, que, pasos in NUEVE:
    k = int(code[1:])
    act(code, f"Entra la Ordenanza {n}, {que}", "Intendente", ms=True, needs=["C24"], win=W(4, 6),
        fuente=f"anexo.{n}", steps=pasos)
    act(f"C{k+1:02d}", f"Tratamiento de la Ordenanza {n} en el Concejo", "Concejo Deliberante", dur=22, est=True,
        needs=[code], fuente=f"anexo.{n}", note=TRAT)
    act(f"C{k+2:02d}", f"El Concejo aprueba la Ordenanza {n}", "Concejo Deliberante", ms=True,
        needs=[f"C{k+1:02d}"], fuente=f"anexo.{n}", decision=TRECE)

act("C52", "Redactar la ordenanza de foodtrucks y el cambio del artículo 9 de la Ordenanza 5824", "Intendente",
    dur=15, est=True, needs=["T07"], fuente="5.5",
    note="Estas dos ordenanzas no están en el anexo.")
act("C53", "Entra la ordenanza de foodtrucks: canon por mes y 75% de empleo local", "Intendente", ms=True,
    needs=["C52"], win=W(4, 6), fuente="6.4",
    steps="Canon como el de Tigre: 201.350 pesos por mes por vehículo (5.5).")
act("C54", "Tratamiento de la ordenanza de foodtrucks en el Concejo", "Concejo Deliberante", dur=22, est=True,
    needs=["C53"], fuente="5.5", note=TRAT)
act("C55", "El Concejo aprueba la ordenanza de foodtrucks", "Concejo Deliberante", ms=True, needs=["C54"],
    fuente="5.5", decision=TRECE)
act("C56", "Entra el cambio del artículo 9 de la Ordenanza 5824, que hoy sólo permite vender bebidas en kioscos en el Bosque Alegre",
    "Intendente", ms=True, needs=["C52"], win=W(4, 6), fuente="6.4")
act("C57", "Tratamiento del cambio de la Ordenanza 5824 en el Concejo", "Concejo Deliberante", dur=22, est=True,
    needs=["C56"], fuente="5.5", note=TRAT)
act("C58", "El Concejo aprueba el cambio de la Ordenanza 5824", "Concejo Deliberante", ms=True, needs=["C57"],
    fuente="5.5", decision=TRECE)
act("C59", "Cambia la mitad del Concejo", "Concejo Deliberante", ms=True, sne=D(2027, 12, 10), needs=["T01"],
    fuente="4.7",
    note="Fecha estimada. El programa dice que la composición del Concejo cambia en diciembre de 2027 (cuadro 26).")
act("C60", "Cambia la otra mitad del Concejo", "Concejo Deliberante", ms=True, sne=D(2029, 12, 10), needs=["C59"],
    fuente="4.7",
    note="Fecha estimada. El programa dice que el Concejo renueva la mitad de sus bancas cada dos años (cuadro 26).")

# ---------------------------------------------------------------- 3 Presupuesto y tasas
act("P01", "Convocar al Concejo a sesión extraordinaria (Ley Orgánica, artículo 68, inciso 5)", "Intendente",
    dur=1, est=True, needs=["T07"], win=DIC, fuente="3.5",
    steps="Decreto de convocatoria. La ordenanza preparatoria de la tabla va primera.")
act("P02", "Tratamiento de la ordenanza preparatoria de la tabla, primera en la convocatoria", "Concejo Deliberante",
    dur=3, est=True, needs=["C07"], win=DIC, fuente="6.6")
act("P03", "El Concejo vota la ordenanza preparatoria de la tabla", "Concejo Deliberante", ms=True,
    needs=["P02"], win=(D(2027, 12, 10), D(2027, 12, 21), "antes del 22 de diciembre de 2027 (mes 1)"),
    fuente="6.4", decision="Votar la ordenanza preparatoria. Así la asamblea se puede reunir antes de fin de año.")
act("P04", "Ajustar la lista de mayores contribuyentes al Concejo nuevo, como pide el Tribunal de Cuentas",
    "Concejo Deliberante", dur=5, est=True, needs=["C59"], win=DIC, fuente="6.6")
act("P05", "Aviso de la convocatoria a la asamblea, con los ocho días que pide la Ley Orgánica (artículo 98)",
    "Concejo Deliberante", dur=6, needs=["P03", "P04"], win=DIC, fuente="6.6",
    durnote="Duración del programa: ocho días corridos, unos seis días hábiles.")
act("P06", "La Asamblea de Concejales y Mayores Contribuyentes aprueba la tabla nueva",
    "Asamblea de Concejales y Mayores Contribuyentes", ms=True, needs=["P05"],
    win=(D(2027, 12, 10), D(2027, 12, 31), "antes de fin de 2027 (mes 1)"), fuente="6.4",
    decision=("Aprobar la tabla. Si no se aprueba en diciembre, pasa a las sesiones ordinarias del 1 de marzo y se cobra desde abril. "
              "En ese caso faltan 616 millones, que salen del gasto flexible (6.6)."),
    note="En 2025, la asamblea se reunió el 17 de diciembre (6.6).")
act("P07", "Publicar la tabla nueva en el Boletín Oficial y emitir las boletas", "Secretaría de Hacienda",
    dur=2, est=True, needs=["P06"], fuente="anexo.3",
    steps="Con la emisión se publica la valuación desde la que no rige el descuento por pago anual (Ordenanza 3, artículo 5).")
act("P08", "La tabla nueva se cobra desde enero de 2028", "Secretaría de Hacienda", ms=True, needs=["P07"],
    win=(D(2028, 1, 3), D(2028, 1, 31), "enero de 2028"), fuente="3.5",
    note="El primer año, la tabla aporta 1.637 millones y el programa necesita 1.806. Faltan 170, que salen del gasto flexible (3.5).")
act("P09", "Reservar la partida de obra vecinal del primer año, unos 7.227 millones, con recursos afectados (Ley Orgánica, artículo 119)",
    "Secretaría de Hacienda", dur=10, est=True, needs=["C06"], fuente="4.9",
    note=("El programa no dice cómo entra el 12,5% en el presupuesto de 2028. "
          "El 4.9 dice que con recursos afectados el Ejecutivo puede crear la partida sin volver al Concejo."))
act("P10", "Adelantar unos 335 millones para empezar por la costa, de lo que ceden otros programas", "Secretaría de Hacienda",
    dur=10, est=True, needs=["T07"], win=AÑO1, fuente="6.4",
    steps="Pagan el diagnóstico de Perú, el tramo de arena, las muestras y la primera temporada de guardavidas (5.5).")
act("P11", "El gasto en ambiente empieza a subir hacia el 1,5% del presupuesto", "Secretaría de Hacienda", ms=True,
    needs=["P10"], win=W(12), fuente="6.4",
    steps="El dinero sale de otros gastos de Servicios Económicos y Urbanismo.")
act("P12", "Educación recupera lo que perdió en 2025: 2.064 millones, que salen del programa de mantenimiento y embellecimiento",
    "Secretaría de Hacienda", ms=True, needs=["T07"], win=W(12), fuente="6.4")

CICLOS = [
    (2029, "P13", "año 2", "25%", "P08", "M11",
     "Partida de obra vecinal al 25%. Fondo de seguridad vial con renglón propio. Ambiente, empleo y vivienda, y centros de apoyo escolar."),
    (2030, "P17", "año 3", "37,5%", "P16", "M17",
     "Partida de obra vecinal al 37,5%. Ambiente al 1,5%. Empleo y vivienda, y centros de apoyo escolar."),
    (2031, "P21", "año 4", "50%", "P20", "M19",
     "Partida de obra vecinal al 50%. Empleo y vivienda a 7.730,9 millones por año."),
]
for y, c, año, pct, prev, gate, pasos in CICLOS:
    k = int(c[1:])
    act(c, f"El Ejecutivo presenta al Concejo el presupuesto {y} y la ordenanza fiscal e impositiva {y}",
        "Secretaría de Hacienda", ms=True, needs=[prev],
        win=(D(y - 1, 10, 1), D(y - 1, 10, 31), f"octubre de {y - 1}"), win_est=True, fuente="3.5", steps=pasos,
        note="El programa dice que el Concejo vota el presupuesto cada año, pero no da el calendario.")
    act(f"P{k+1}", f"Tratamiento del presupuesto {y} en el Concejo", "Concejo Deliberante", dur=30, est=True,
        needs=[c], fuente="3.5")
    act(f"P{k+2}", f"El Concejo vota el presupuesto {y}", "Concejo Deliberante", ms=True,
        needs=[f"P{k+1}", gate], win=(D(y - 1, 11, 1), D(y - 1, 12, 31), f"antes de que empiece {y}"), win_est=True, fuente="anexo",
        decision=f"Subir la partida de obra vecinal al {pct} sólo si el escalón anterior se ejecutó y justificó entero (Ordenanza 1, artículo 1).",
        note="El presupuesto es anual: rige de enero a diciembre.")
    act(f"P{k+3}", f"La Asamblea de Concejales y Mayores Contribuyentes aprueba la ordenanza impositiva {y}",
        "Asamblea de Concejales y Mayores Contribuyentes", ms=True, needs=[f"P{k+1}"],
        win=(D(y - 1, 11, 1), D(y - 1, 12, 31), f"antes de que empiece {y}"), win_est=True, fuente="anexo.3",
        steps="Sigue la tabla nueva, con el tope de 25% por boleta. Con la emisión se publica la valuación desde la que no rige el descuento por pago anual.",
        note="En 2025, la asamblea se reunió el 17 de diciembre (6.6).")

act("P25", "El gasto en empleo y vivienda llega a la mitad del camino hacia 7.730,9 millones por año", "Secretaría de Hacienda",
    ms=True, needs=["P15"], win=W(24), fuente="6.4")
act("P26", "Gasto en ambiente al 1,5% del presupuesto (meta 3)", "Secretaría de Hacienda", ms=True,
    needs=["P19", "P11"], win=W(36), fuente="6.4")
act("P27", "El presupuesto 2031 lleva el gasto en empleo y vivienda a 7.730,9 millones por año (meta 2)", "Secretaría de Hacienda",
    ms=True, needs=["P23"], win=W(37, 48, "año 4 (meses 37 a 48)"), fuente="6.3",
    note="Hoy son 505,7 millones (cuadro 41).")
act("P28", "La tabla nueva llega a su valor completo: desde el cuarto año se cobran unos 5.983 millones por año", "Secretaría de Hacienda",
    ms=True, needs=["P24"], win=(D(2031, 1, 2), D(2031, 12, 31), "2031, el cuarto año"), fuente="3.5",
    note="Con el tope de 25% por año, la actualización se completa en cuatro años (3.5).")
act("P29", "Abrir el programa propio de género en el presupuesto, separado del que comparte con niñez, juventud y personas mayores",
    "Secretaría de Hacienda", dur=10, est=True, needs=["C30"], fuente="anexo.6",
    note="La ordenanza no fija monto. Fija que el monto exista por separado y se pueda ver.")

# ---------------------------------------------------------------- 1 Mecanismo vecinal y obra pública
act("M01", "Rige desde el primer día la regla de la costa: ningún contrato ni demolición sin consultar a todo San Isidro",
    "Intendente", ms=True, needs=["T07"], fuente="6.4",
    steps="Vale para los terrenos que son de todo San Isidro, como la costa. El resto del Municipio sigue funcionando como siempre (4.6).",
    note="Vale hasta que funcione el primer panel sorteado.")
act("M02", "Convocar a la primera ronda de asambleas en las seis zonas", "Intendente", dur=10, est=True,
    needs=["T07"], win=W(1, 3), fuente="6.1",
    steps="Fuera del horario de trabajo. En el propio barrio. Con un espacio para cuidar a los chicos (4.6).")
act("M03", "Primera ronda de asambleas en las seis zonas: informar y anotar qué necesita cada zona (compromiso 11)",
    "Intendente", dur=15, est=True, needs=["M02"], win=W(3), fuente="6.4",
    steps="Se informa a los vecinos y se completa el diagnóstico de cada zona. Las actas y los asistentes se pueden consultar.",
    note="La primera ronda informa. Las obras se eligen en la segunda (6.1).")
act("M04", "Reconocer como comisión de su zona a cada asociación vecinal en condiciones", "Intendente",
    dur=20, est=True, needs=["C06", "C03", "M03"], win=W(4, 6), fuente="6.4",
    steps="Si en una zona hay más de una asociación, actúan como una sola comisión, con una sola partida (4.6).",
    note="Los compromisos 1 y 2 van juntos porque todo lo demás depende de ellos (nota del cuadro 40).")
act("M05", "Volver a armar el registro de asociaciones vecinales, consultable por cualquiera", "Gobierno y Legal y Técnica",
    dur=20, est=True, needs=["C06"], win=W(4, 6), fuente="6.4",
    steps="Con su zona, sus autoridades y su domicilio (Ordenanza 1, artículo 11).")
act("M06", "En las zonas sin una asociación en condiciones: asamblea abierta y ayuda para formar una", "Intendente",
    dur=90, est=True, needs=[("M04", "SS", 0)], win=W(4, 12), fuente="6.4",
    note="Mientras tanto, el Municipio hace la obra de esa zona, en esa zona. Los vecinos eligen igual (6.6).")
act("M07", "Comisiones formadas en las seis zonas", "Intendente", ms=True, needs=["M04", "M06"], win=W(4, 12),
    fuente="6.4", note="A más tardar en el mes 12 donde hay que formar una nueva (nota del cuadro 42).")
act("M08", "Segunda ronda de asambleas: los vecinos eligen las obras de su zona", "Comisiones vecinales",
    dur=40, est=True, needs=["M04"], win=W(6, 9), fuente="6.4",
    steps=("Un voto por persona desde los 16 años, en la asamblea o por internet con identidad verificada. "
           "Cada proyecto se revisa antes de votar. Cada comisión decide si el tendido de internet de su barrio entra en el dinero de su zona (5.4)."),
    note="Duración estimada: dos meses, como el ciclo de la Ciudad de Buenos Aires que cita el 6.1.")
act("M09", "El Ejecutivo responde por escrito a cada decisión de las zonas, con sus razones", "Intendente",
    dur=22, needs=["M08"], win=W(6, 9), fuente="anexo.1", durnote=TREINTA,
    steps="Toda persona puede ver cada respuesta desde el día en que sale. Ningún silencio reemplaza la respuesta.")
act("M10", "Contratar y hacer las obras elegidas del año 1: el 12,5% de la obra pública, unos 7.227 millones",
    "Secretaría de Obras con las comisiones vecinales", dur=70, est=True, needs=["M09", "P09"],
    win=(M(6), E(12), "dentro del año 1, hasta el mes 12"), fuente="6.2",
    steps=("Tres vecinos que elige la asamblea reciben cada obra y la firman. Nadie que eligió una obra cobra por ella. "
           "El 1,5% de la partida paga el cuidado de los chicos, los honorarios y la administración."),
    note="El año 1 sirve para probar que las seis comisiones pueden formarse, elegir obras y justificar cada peso (6.2).")
act("M11", "Año 1 de la rampa, cumplido", "Intendente", ms=True, needs=["M10", "M07"], win=W(12), fuente="6.4",
    decision=("¿Se ejecutó y justificó todo? Si no, la rampa no sube y el saldo queda para la misma zona (Ordenanza 1, artículos 1 y 9). "
              "Si una comisión falla, el Ejecutivo la interviene y llama a una nueva asamblea en treinta días (6.6)."))
act("M12", "Sortear el primer panel de vecinos, apenas se aprueba la Ordenanza 12", "Organización independiente que sortea el panel",
    dur=15, est=True, needs=["C45"], win=W(7, 12), fuente="6.4",
    steps=("Invitación por correo a varios cientos de personas al azar. Unos cuarenta vecinos que se parezcan a San Isidro por localidad, edad, "
           "género y estudios. Entra también quien usa la costa aunque viva en otro lado."),
    note="El sorteo no lo hace el Municipio (4.6).")
act("M13", "El primer panel se reúne y da su recomendación, con razones, sobre la obra en la costa", "Panel de vecinos sorteados",
    dur=20, est=True, needs=["M12"], win=W(7, 12), fuente="6.4",
    steps="Escucha a técnicos y a quien quiera opinar. Cada vecino del panel cobra un honorario al final, si fue a todas las reuniones. Todo es público.",
    note="Duración estimada: cuatro reuniones, una por semana.")
act("M14", "El Ejecutivo responde al panel en público, por escrito y con sus razones", "Intendente",
    dur=22, needs=["M13"], win=W(7, 12), fuente="anexo.12", durnote=TREINTA)
act("M15", "Año 2 de la rampa (25%): las asociaciones hacen ellas mismas la obra, por contrato directo",
    "Comisiones vecinales con la Secretaría de Obras", span=(M(13), E(24)), cierre=True, needs=["M11", "P15"], win=W(13, 24), fuente="6.2",
    steps="Contrato directo con la firma del 60% de los vecinos beneficiados (Ley Orgánica, artículo 132). Unos 14.454 millones.",
    durnote="Duración del programa: un año.")
act("M16", "Revisión del Tribunal de Cuentas sobre la obra que hicieron las asociaciones", "Tribunal de Cuentas de la Provincia",
    dur=60, est=True, needs=["M15"], fuente="6.2",
    note="El programa pide que no haya objeciones en el año 2, pero no dice cuándo se conoce ese resultado.")
act("M17", "Año 2 de la rampa, cumplido", "Intendente", ms=True, needs=["M15"], win=W(24), fuente="6.4",
    decision="¿Las asociaciones hicieron la obra y justificaron cada peso, sin objeciones del Tribunal de Cuentas? Si no, la rampa se queda en 25% (6.2).")
act("M18", "Año 3 de la rampa (37,5%), con el registro de asociaciones vecinales ya renovado",
    "Comisiones vecinales con la Secretaría de Obras", span=(M(25), E(36)), cierre=True, needs=["M17", "M05", "P19"], win=W(25, 36),
    fuente="6.2", steps="Unos 21.681 millones.", durnote="Duración del programa: un año.")
act("M19", "Año 3 de la rampa, cumplido", "Intendente", ms=True, needs=["M18"], win=W(36), fuente="6.4",
    decision="¿Se ejecutó y justificó todo? Si no, la rampa se queda en 37,5% (Ordenanza 1, artículo 1).")
act("M20", "Año 4 de la rampa: los vecinos deciden la mitad de la obra pública", "Comisiones vecinales con la Secretaría de Obras",
    span=(M(37), E(48)), cierre=True, needs=["M19", "P23"], win=W(37, 48), fuente="6.2",
    steps="Unos 28.908 millones por año. La otra mitad, la obra que sirve a varias zonas, sigue en manos del Ejecutivo y del Concejo.",
    durnote="Duración del programa: un año.")
act("M21", "Los vecinos deciden la mitad de la obra pública (meta 4)", "Intendente", ms=True, needs=["M20"], win=W(48),
    fuente="6.4", note="Hoy deciden el 0% (cuadro 41).")
act("M22", "Cien días: los veintiún compromisos, a la vista", "Intendente", ms=True, fixed=D(2028, 3, 19),
    needs=["C01", "C04", "C07", "P06", "C08", "C11", "C14", "S01", "S02", "S03", "G02", "G03", "X02", "M02", "M03",
           "E04", "E05", "E36", "I07", "I04", "G05", "H01", "H07", "G14", "G15", "C18", "C21", "U02"],
    fuente="6.1",
    steps="Cada compromiso se prueba con un documento público o se le pregunta a la inteligencia artificial del Municipio (cuadro 40).",
    note="Fecha del programa: los cien días se cumplen el 19 de marzo de 2028. Es domingo: todo lo anterior termina el viernes 17.")
act("M23", "Termina el mandato", "Intendente", ms=True, fixed=D(2031, 12, 10),
    needs=["M21", "V03", "P27", "I16", "G13", "G23", "G27", "U10", "H13", "X09", "E34"], fuente="6.1",
    note="El mandato es de cuatro años, desde el 10 de diciembre de 2027.")

# ---------------------------------------------------------------- 4 Inteligencia artificial del Municipio
act("I01", "Armar el equipo que construye la inteligencia artificial del Municipio, con gente de San Isidro", "Ciencia y Técnica",
    dur=20, est=True, needs=["T07"], win=W(1, 3), fuente="4.11",
    steps="Docentes y técnicos de San Isidro, con mucha experiencia, con experiencia media y principiantes. Se paga con la partida de Ciencia y Técnica (cuadro 28).")
act("I02", "Construir las tres primeras partes: la que responde consultas, la que saca el turno médico conversando y la que escucha a los vecinos",
    "Equipo de la inteligencia artificial del Municipio", dur=35, est=True, needs=["I01"], win=W(1, 3), fuente="6.4",
    steps=("Contesta sólo sobre lo que el Municipio registró y muestra el documento de cada dato. Es el primer contacto, a toda hora, de una víctima "
           "de violencia, con un modo discreto. Cada tema tiene un plazo; si el responsable no contesta, pasa a su jefe. Una cuenta por persona, con identidad verificada."),
    note="Riesgo crítico del 6.6: la inteligencia artificial del Municipio no se construye o llega tarde. Por eso se entrega por partes.")
act("I03", "Revisión de seguridad por las universidades de San Isidro antes de abrir al público", "Universidades de San Isidro",
    dur=5, est=True, needs=["I02"], win=W(1, 3), fuente="6.6",
    note="Riesgo del 6.6: la inteligencia artificial del Municipio contesta mal.")
act("I04", "Empiezan a funcionar las tres primeras partes de la inteligencia artificial del Municipio (compromiso 14)",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I03", "S01"], win=W(3), fuente="6.4")
act("I05", "Pedir gratis a la Nación el certificado de firma digital para programas", "Gobierno y Legal y Técnica",
    dur=5, est=True, needs=["T07"], win=W(1, 3), fuente="6.4",
    steps="Con ese certificado se sellan las grabaciones de las inspecciones y las de los vecinos que denuncian (5.5 y 5.9).")
act("I06", "Recibir de la Nación el certificado de firma digital", "Nación", dur=30, est=True, needs=["I05"], fuente="5.5",
    note="El programa no dice cuánto tarda la Nación. Sin el certificado no se pueden sellar las grabaciones.")
act("I07", "Prueba a ciegas de un mes de las caras del profesor digital, antes de pagar nada", "Educación (área municipal)",
    span=(M(3), E(3)), needs=["I01"], win=W(3), fuente="6.4",
    steps="Quienes evalúan no saben de qué empresa es cada cara. Se comparan la calidad y el precio.",
    durnote="Duración del programa: un mes.")
act("I08", "Contratar la cara del profesor digital aparte del resto: por minuto, con la calidad mínima de la prueba y con un plan B",
    "Educación (área municipal)", dur=10, est=True, needs=["I07", "T05"], fuente="6.6",
    note="Riesgo del 6.6: quiebra la empresa de la cara del profesor digital.")
act("I09", "Construir las tres partes siguientes: la partida vecinal, el seguimiento de cada obra y el espacio de cada asociación",
    "Equipo de la inteligencia artificial del Municipio", dur=60, est=True, needs=["I04"], fuente="6.4",
    steps=("Votación con el padrón de la zona y acta el mismo día. Aviso cuando una obra se atrasa. "
           "El Municipio no lee ni filtra el espacio de cada asociación."))
act("I10", "Suman tres partes: la partida vecinal, el seguimiento de cada obra y el espacio propio de cada asociación inscripta (meta 19)",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I09", "C06", "C10", "M05"], win=W(6, 9), fuente="6.4")
act("I11", "Empieza la prueba de seis meses del profesor digital en los primeros centros de apoyo escolar", "Educación (área municipal)",
    ms=True, needs=["C27", "I08", "E38"], win=W(7, 12), fuente="6.4",
    steps="La familia da dos permisos por separado. No se guardan diagnósticos, ni datos de salud, ni emociones (Ordenanza 2).")
act("I12", "Prueba del profesor digital, medida con exámenes hechos sin inteligencia artificial", "Educación (área municipal)",
    span=(M(7), E(12)), needs=["I11"], fuente="5.8", durnote="Duración del programa: seis meses.")
act("I13", "Publicar el resultado de la prueba del profesor digital (meta 14)", "Educación (área municipal)", ms=True,
    needs=["I12"], fuente="6.3", decision="Extender el profesor digital sólo con el resultado publicado.")
act("I14", "El profesor digital llega a todos los chicos de primaria y secundaria, desde el año escolar siguiente",
    "Educación (área municipal)", ms=True, needs=["I13"], sne=D(2029, 3, 1), fuente="6.4",
    steps="Gratis en las escuelas públicas, en los colegios que el Estado paga por completo y en el apoyo escolar del Municipio (5.8).",
    note="Fecha estimada. El programa dice «desde el año escolar siguiente». Se supone que el año escolar empieza en marzo.")
act("I15", "Transmitir y pasar a texto las asambleas, para buscarlas y consultarlas", "Equipo de la inteligencia artificial del Municipio",
    dur=60, est=True, needs=["I04"], fuente="4.11",
    note="El calendario no le pone fecha. Es parte de la meta 6 del cuadro 41.")
act("I16", "La inteligencia artificial del Municipio funcionando, con la partida vecinal, las asambleas pasadas a texto y cada dato cargado el mismo día (meta 6)",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I10", "I15", "X03"], win=FIN, fuente="6.3",
    note="Hoy no existe: el Municipio publica en PDF y su portal de datos abiertos devuelve error (cuadro 41).")
act("I17", "Licitar y contratar la auditoría externa de la inteligencia artificial del Municipio", "Ciencia y Técnica",
    dur=66, needs=["I01"], fuente="6.6", durnote=LIC,
    note="Riesgo del 6.6: la inteligencia artificial del Municipio contesta mal. La auditoría externa está en el cuadro 28.")
act("I18", "Centros con computadoras y mesa de ayuda en cada zona, para quien no tiene teléfono o conexión",
    "Equipo de la inteligencia artificial del Municipio", dur=40, est=True, needs=["V01", "I04"], fuente="6.6",
    note="Riesgo del 6.6: queda afuera el que no tiene teléfono o conexión. El programa no le pone fecha.")

# ---------------------------------------------------------------- 5 Empleo y formación
act("E01", "Firmar el convenio con la UNSO para la tecnicatura", "Intendente con la UNSO", dur=20, est=True,
    needs=["T07"], win=W(1, 3), fuente="6.4",
    steps="Tecnicatura universitaria de dos años en inteligencia artificial aplicada y datos. Nace en el CFL 404 de La Cava, en Béccar.")
act("E02", "Pedir al Ministerio de Educación que el título valga en todo el país", "Intendente con la UNSO", dur=5, est=True,
    needs=[("E01", "SS", 0)], win=W(1, 3), fuente="6.4")
act("E03", "Pedir a la Provincia que permita la pasantía dentro de la formación profesional", "Intendente", dur=5, est=True,
    needs=[("E01", "SS", 0)], win=W(1, 3), fuente="6.4")
act("E04", "Abrir la inscripción a la formación laboral en las seis zonas (compromiso 12)", "Intendente", dur=10, est=True,
    needs=["E01"], win=W(3), fuente="6.4",
    steps="Los lugares se reparten por zona con el índice de necesidad del capítulo 4 (5.3).")
act("E05", "El primer grupo empieza a cursar en los lugares que ya existen", "UNSO y CFL 404", ms=True, needs=["E04"],
    win=W(3), fuente="6.4",
    note="El primer grupo se paga con lo que sube el gasto en empleo el primer año (cuadro 40).")
act("E06", "Primer grupo: un año de cursada", "UNSO y CFL 404", span=(M(3), E(14)), needs=["E05"], fuente="5.3",
    durnote="Duración del programa: un año.")
act("E07", "Firmar el convenio de pasantías con la UNSO (Ley 26.427)", "Intendente con la UNSO", dur=20, est=True,
    needs=["E01"], win=W(1, 15, "a más tardar en el mes 15"), fuente="6.4")
act("E08", "Trámite de validez nacional del título en el Ministerio de Educación", "Ministerio de Educación de la Nación",
    dur=120, est=True, needs=["E02"], fuente="6.6", note="Hoy la UNSO no tiene esta tecnicatura (6.6).")
act("E09", "El título de la tecnicatura vale en todo el país", "Ministerio de Educación de la Nación", ms=True, needs=["E08"],
    win=W(1, 15, "a más tardar en el mes 15"), fuente="6.6",
    decision="Si no llega antes del mes 15, el primer grupo hace igual su práctica, con una beca municipal de 240.000 $ por mes (6.6).")
act("E10", "Preparar los lugares de pasantía en las áreas: equipos de diez pasantes con un supervisor", "Intendente con cada área",
    dur=40, est=True, needs=["E07"], fuente="5.3",
    steps="El supervisor es un empleado que cambia de tarea y no pierde su sueldo. Sólo proyectos nuevos, nunca puestos de trabajo.")
act("E11", "El primer grupo termina de cursar y empieza su primera pasantía, en el Municipio", "Áreas del Municipio", ms=True,
    needs=["E06", "E07", "E09", "E10"], win=W(15), fuente="6.4")
act("E12", "Primer grupo: primera pasantía, seis meses en proyectos de las áreas del Municipio", "Áreas del Municipio",
    span=(M(15), E(20)), needs=["E11"], fuente="5.3",
    steps="240.000 $ por mes por 20 horas semanales, con ART y obra social. Paga el área.",
    durnote="Duración del programa: seis meses.")
act("E13", "Firmar el convenio marco con la Cámara del Comercio e Industria de San Isidro y con las cámaras de Boulogne y Béccar",
    "Intendente", dur=30, est=True, needs=["E07"], fuente="5.3")
act("E14", "El primer grupo pasa a su segunda pasantía, en empresas de San Isidro", "Empresas de San Isidro", ms=True,
    needs=["E12", "E13"], win=W(21), fuente="6.4")
act("E15", "Primer grupo: segunda pasantía, seis meses en una empresa de San Isidro", "Empresas de San Isidro",
    span=(M(21), E(26)), needs=["E14"], fuente="5.3",
    steps="Paga la empresa. Quien no consiga lugar hace la práctica en el centro de formación, con beca municipal (Ordenanza 10, artículo 6).",
    durnote="Duración del programa: seis meses.")
act("E16", "Egresan los primeros 231, con el título de la UNSO y un año de trabajo real", "UNSO y CFL 404", ms=True,
    needs=["E15"], win=W(27), fuente="6.4")
act("E17", "Primera convocatoria del semillero de empresas", "Intendente", ms=True, needs=["E16", "C39"], win=W(27),
    fuente="6.4",
    steps="Un año de incubación en las sedes, con mentores. Préstamo a tasa cero: un peso por cada peso de capital que consiga la empresa (Ordenanza 10, artículo 9).")
act("E18", "Los egresados pasan a hacer el trabajo de todos los días en las áreas, y la oficina de delitos por internet suma egresados",
    "Áreas del Municipio", ms=True, needs=["E16"], win=W(27), fuente="5.3",
    note="Hasta el mes 27, el trabajo de todos los días lo sigue haciendo el personal actual (5.3).")
act("E19", "Entra el segundo grupo de alumnos", "UNSO y CFL 404", ms=True, needs=["E04"], win=W(9), fuente="6.4",
    steps="La inscripción se abre cada seis meses (5.3).")
act("E20", "Segundo grupo: un año de cursada", "UNSO y CFL 404", span=(M(9), E(20)), needs=["E19"], fuente="5.3",
    durnote="Duración del programa: un año.")
act("E21", "Segundo grupo: primera pasantía en el Municipio y segunda en empresas de San Isidro", "Áreas del Municipio",
    span=(M(21), E(32)), needs=["E20"], win=W(21, 33), fuente="6.4",
    durnote="Duración del programa: dos pasantías de seis meses.")
act("E22", "Egresa el segundo grupo", "UNSO y CFL 404", ms=True, needs=["E21"], win=W(33), fuente="6.4",
    note="Desde el mes 27 egresa un grupo cada seis meses (cuadro 42).")
act("E23", "Segunda convocatoria del semillero de empresas", "Intendente", ms=True, needs=["E22", "E17"], win=W(33),
    fuente="5.3", note="Las convocatorias se abren después de cada egreso (5.3).")
act("E24", "Tercer grupo: entra en el mes 15, cursa un año y hace sus dos pasantías", "UNSO y CFL 404",
    span=(M(15), E(38)), needs=["E04"], win=W(15, 39), fuente="5.3", durnote="Duración del programa: dos años.",
    note="Inferido del 5.3: la inscripción se abre cada seis meses y egresa un grupo cada seis meses.")
act("E25", "Egresa el tercer grupo", "UNSO y CFL 404", ms=True, needs=["E24"], win=W(39), fuente="6.4")
act("E26", "Tercera convocatoria del semillero de empresas", "Intendente", ms=True, needs=["E25", "E23"], win=W(39), fuente="5.3")
act("E27", "Cuarto grupo: entra en el mes 21, cursa un año y hace sus dos pasantías", "UNSO y CFL 404",
    span=(M(21), E(44)), needs=["E04"], win=W(21, 45), fuente="5.3", durnote="Duración del programa: dos años.",
    note="Inferido del 5.3: la inscripción se abre cada seis meses y egresa un grupo cada seis meses.")
act("E28", "Egresa el cuarto grupo: 1.286 egresados en el mandato", "UNSO y CFL 404", ms=True,
    needs=["E27", "E25", "E22", "E16"], win=W(45), fuente="6.4")
act("E29", "Cuarta convocatoria del semillero de empresas", "Intendente", ms=True, needs=["E28", "E26"], win=W(45), fuente="5.3",
    note="En el mandato nacen dieciséis empresas (5.3).")
act("E30", "Empiezan a funcionar las cinco sedes fijas de formación laboral y la sede móvil de Acassuso",
    "Intendente con el CFL 404 y la Provincia", dur=60, est=True, needs=["E01"], win=W(6, 12), fuente="6.4",
    steps=("El Municipio pone el edificio, los permisos, el seguro y el equipamiento. La Provincia paga los cargos docentes; "
           "si no los cubre, los paga el Municipio. Los cursos se revisan según lo que hoy piden las empresas."))
act("E31", "Empieza el registro de inserción laboral: cuántas personas consiguen trabajo, cargado el mismo día",
    "Educación (área municipal)", ms=True, needs=["I04"], win=W(6), fuente="6.4")
act("E32", "Puente con las empresas de inteligencia artificial: el Municipio y la UNSO empiezan a buscar convenios",
    "Intendente con la UNSO", ms=True, needs=["E01"], win=W(12), fuente="6.4",
    steps="Firman el rector de la UNSO y el intendente, con permiso del Concejo (Ley Orgánica, artículo 41). Lo coordina una persona del equipo de la plataforma.",
    note="El puente no promete trabajos: las empresas eligen a quién toman (6.5).")
act("E33", "Las ofertas de trabajo se pueden consultar en la inteligencia artificial del Municipio",
    "Equipo de la inteligencia artificial del Municipio", dur=20, est=True, needs=["I04", "E31"], win=W(18, 24), fuente="6.4")
act("E34", "Entre 250 y 300 egresados por año consiguen empleo pago (meta 13)", "Intendente", ms=True,
    needs=["E28", "E31", "E30", "E40"], win=FIN, fuente="6.3",
    note="El número sale del registro de inserción laboral. El primer registro da el punto de partida (cuadro 41).")
act("E35", "Elegir con el índice de necesidad el lugar del primer centro de apoyo escolar y contratar a sus docentes",
    "Educación (área municipal)", dur=30, est=True, needs=["T07"], win=W(1, 3), fuente="5.8",
    steps="No se construye nada: se abre a la tarde un lugar que ya existe y se pagan docentes.")
act("E36", "Abre el primer centro de apoyo escolar (compromiso 13)", "Educación (área municipal)", ms=True,
    needs=["E35"], win=W(3), fuente="6.4",
    note="Hoy hay cinco espacios pequeños, sólo en Béccar y Boulogne, con unos cien alumnos (cuadro 40).")
act("E37", "Preparar el segundo centro de apoyo escolar", "Educación (área municipal)", dur=30, est=True, needs=["E36"],
    fuente="6.4")
act("E38", "Abre el segundo centro de apoyo escolar", "Educación (área municipal)", ms=True, needs=["E37"], win=AÑO1,
    fuente="6.4",
    note="Supuesto: abre antes de la prueba del profesor digital, que se hace «en los primeros centros» (mes 7).")
act("E39", "Abrir el tercer y el cuarto centro de apoyo escolar", "Educación (área municipal)", dur=60, est=True,
    needs=["E38"], win=W(13, 24, "año 2 (meses 13 a 24)"), fuente="6.4", note="Abren de a dos por año (cuadro 42).")
act("E41", "Preparar el quinto y el sexto centro de apoyo escolar", "Educación (área municipal)", dur=40, est=True,
    needs=["E39"], sne=M(23), fuente="6.4",
    note="Fecha estimada. Supuesto: abren al empezar el año 3, para que abran de a dos por año y estén los seis en el mes 25.")
act("E40", "Los seis centros de apoyo escolar abiertos, uno por localidad (meta 12)", "Educación (área municipal)", ms=True,
    needs=["E39", "E41"], win=W(25), fuente="6.4")

# ---------------------------------------------------------------- 6 Vivienda
act("V01", "Medir la conexión a internet en cada zona durante la primera ronda de asambleas, primero en La Cava y en Boulogne",
    "Secretaría de Obras", dur=15, est=True, needs=[("M03", "SS", 0)], win=W(3), fuente="5.4",
    steps="Cualquier vecino puede preguntar cómo está la conexión en su zona.")
act("V02", "Pagar la conexión de cada casa al agua, la cloaca y el gas, donde la obra vecinal hizo la red", "Secretaría de Obras",
    dur=760, est=True, needs=["P15", "M10"], win=(M(1), E(48), "dentro del mandato, hasta el mes 48"), fuente="5.4",
    steps="La partida de vivienda llega a 3.092,4 millones por año cuando el programa funciona completo (cuadro 35).",
    note="Duración estimada: unos tres años. El calendario no dice desde cuándo. Se ubica después de la primera obra vecinal y del presupuesto 2029.")
act("V03", "En Boulogne y Béccar, los hogares sin cloaca se reducen a la mitad (meta 1)", "Secretaría de Obras", ms=True,
    needs=["V02", "M20"], win=W(48), fuente="6.4", note="Hoy son 4.616 hogares (Censo 2022, cuadro 41).")
act("V04", "Aplicar la Ordenanza 13: audiencia pública y dictamen de la comisión de la zona antes de cada excepción urbanística",
    "Intendente", ms=True, needs=["C48", "M07"], fuente="anexo.13",
    steps="Respuesta escrita a cada observación. El Ejecutivo no otorga por decreto la excepción que la zona rechaza.")
act("V05", "Pedir a la Provincia la aprobación para cobrar el 15% de la valorización que genera cada excepción (Ley 14.449)",
    "Intendente", dur=10, est=True, needs=["C48"], fuente="anexo.13",
    steps="El dinero va a vivienda y a obra en las zonas donde falta.")

# ---------------------------------------------------------------- 7 Salud
act("S01", "Turno médico por internet en los primeros hospitales y centros de salud, en la plataforma que ya da turnos para otros trámites (compromiso 7)",
    "Secretaría de Salud", dur=30, est=True, needs=["T07"], win=W(1, 3), fuente="6.4",
    steps="Hoy el único turno de salud por internet es el de castración de mascotas (cuadro 41).")
act("S02", "Pedir sumarse a Mi Salud Digital, el sistema de la Provincia", "Secretaría de Salud", dur=5, est=True,
    needs=[("S01", "SS", 0)], win=W(1, 3), fuente="6.4")
act("S03", "Publicar el precio por unidad de cada compra de insumos de los tres hospitales, con sus comparaciones (compromiso 8)",
    "Secretaría de Salud", dur=30, est=True, needs=["T07"], win=W(1, 3), fuente="6.4",
    steps=("Al lado, lo que se pagó la vez anterior y lo que pagan los otros dos hospitales. También lo que cobran los laboratorios y pagan "
           "los sanatorios y las obras sociales. Si esos precios no son públicos, el Municipio los pide."))
act("S04", "Estudiar el contrato actual de la tomografía y cómo termina", "Secretaría de Salud", dur=30, est=True,
    needs=["T07"], win=W(1, 3), fuente="6.4")
act("S05", "Licitar los dos tomógrafos, o tomarlos con el leasing de la Provincia, mientras sigue el contrato actual",
    "Secretaría de Salud", dur=66, needs=["S04"], win=W(4, 9), fuente="6.4", durnote=LIC,
    steps="El leasing es un alquiler en 48 cuotas con opción de compra, pagado con la partida que hoy paga el servicio (5.6).")
act("S06", "Hacer las obras en las salas de los tomógrafos del Central y de Boulogne", "Secretaría de Obras con Salud",
    dur=60, est=True, needs=[("S05", "SS", 22)], win=W(4, 9), fuente="6.4")
act("S07", "Instalar los dos tomógrafos", "Secretaría de Salud", dur=20, est=True, needs=["S05", "S06"], win=W(4, 12),
    fuente="5.6")
act("S08", "Funcionan los dos tomógrafos del Municipio, en el Central y en Boulogne", "Secretaría de Salud", ms=True,
    needs=["S07"], win=W(12), fuente="6.4",
    decision="Salir del contrato actual sin un solo día sin tomógrafo.")
act("S09", "Extender el turno por internet a los trece centros de salud, con recordatorio y lista de espera",
    "Secretaría de Salud con el equipo de la inteligencia artificial", dur=120, est=True, needs=["S01", "I04"],
    win=AÑO1, fuente="6.4")
act("S10", "Turno médico por internet en los tres hospitales, el odontológico y los nueve centros de atención primaria (meta 7)",
    "Secretaría de Salud", ms=True, needs=["S09"], win=W(12), fuente="6.4")
act("S11", "En la inteligencia artificial del Municipio: turnos, gente en las guardias, insumos que hay y faltan, y comparación de cada compra (meta 8)",
    "Secretaría de Salud con el equipo de la inteligencia artificial", dur=60, est=True, needs=["S10", "S03"],
    win=W(12, 18), fuente="6.4",
    steps="La espera de la guardia se muestra como un número, por gravedad, nunca como imagen. La comparación avisa cuando algo se sale de lo normal.")
act("S12", "Contratar a cien cuidadores a domicilio, formados en el curso de operador de cuidados del CFL 404",
    "Desarrollo Social", dur=40, est=True, needs=["T07"], fuente="5.13",
    steps="Curso gratuito de 380 horas, distinto de la tecnicatura.")
act("S13", "Empiezan los cien cuidadores a domicilio: unas 240 personas mayores y personas con discapacidad que no pueden salir",
    "Desarrollo Social", ms=True, needs=["S12"], win=W(4, 6), fuente="6.4",
    steps="Cuatro horas por día para cada persona. Cuesta 667,8 millones por año, con cargas sociales (5.13).")

# ---------------------------------------------------------------- 8 Seguridad
act("G01", "Cargar los datos de seguridad que ya produce el Municipio: patrullaje, cámaras que funcionan y tiempo del 911 municipal",
    "Seguridad (Centro de Operaciones Municipal)", dur=20, est=True, needs=["T07"], win=W(1, 3), fuente="6.4")
act("G02", "Cualquier vecino puede preguntar por el patrullaje, las cámaras y el 911 municipal (compromiso 9)",
    "Seguridad (Centro de Operaciones Municipal)", ms=True, needs=["G01", "I04"], win=W(1, 3), fuente="6.4")
act("G03", "Pedir formalmente a la Provincia los datos de delitos por zona", "Intendente", dur=5, est=True,
    needs=["T07"], win=W(1, 3), fuente="6.4",
    note="El mapa del delito por zona depende de la Provincia (6.5).")
act("G04", "Poner las 110 cámaras con inteligencia artificial a detectar hechos violentos y avisar al patrullero más cercano",
    "Seguridad (Centro de Operaciones Municipal)", dur=20, est=True, needs=["T07"], win=W(1, 3), fuente="5.7",
    steps="No hace falta comprar cámaras ni licencias: ya se compraron.")
act("G05", "Decreto: las 110 cámaras empiezan a detectar en el momento y a avisar al patrullero (compromiso 15)", "Intendente",
    ms=True, needs=["G04"], win=W(3), fuente="6.4")
act("G06", "Armar el mapa de los hechos que registra el Municipio", "Seguridad (Centro de Operaciones Municipal)",
    dur=30, est=True, needs=["G01"], win=W(4, 6), fuente="6.4")
act("G07", "La patrulla municipal empieza a recorrer los pocos lugares donde se concentra el delito, a la hora en que pasa",
    "Seguridad (Centro de Operaciones Municipal)", ms=True, needs=["G06"], win=W(4, 6), fuente="6.4",
    steps="Es la misma patrulla, en otro lugar y a otra hora (5.7).")
act("G08", "Preparar la constancia para quien es acusado en público sin una causa judicial", "Gobierno y Legal y Técnica",
    dur=20, est=True, needs=["I04"], fuente="5.7",
    steps="Dice qué registros se consultaron, en qué fecha, qué consta y qué no. Sin adjetivos ni conclusiones.")
act("G09", "Empieza la constancia: la pide sólo la persona acusada y la inteligencia artificial la resuelve en horas",
    "Gobierno y Legal y Técnica", ms=True, needs=["G08"], win=W(6, 9), fuente="6.4")
act("G10", "Los datos de seguridad pasan a estar al día, con las órdenes de juez recibidas y cumplidas",
    "Seguridad (Centro de Operaciones Municipal)", dur=40, est=True, needs=["G02", "C27"], win=W(12, 18), fuente="6.4")
act("G11", "Preparar la oficina de delitos por internet, junto al equipo técnico de las cámaras",
    "Seguridad (Centro de Operaciones Municipal)", dur=30, est=True, needs=["G05"], fuente="5.7")
act("G12", "Abre la oficina de delitos por internet, con pasantes de la tecnicatura como personal técnico",
    "Seguridad (Centro de Operaciones Municipal)", ms=True, needs=["G11", "E11"], win=W(15), fuente="6.4",
    note="Desde el mes 27, el personal técnico son egresados (cuadro 42).")
act("G13", "Las cámaras detectan en el momento, ayudan a reconstruir el recorrido después de una denuncia y se puede preguntar por las órdenes de juez (meta 10)",
    "Seguridad (Centro de Operaciones Municipal)", ms=True, needs=["G05", "G10"], win=FIN, fuente="6.3",
    note="Hoy no hay registro público de que funcionen. Las alertas no se publican (cuadro 41).")
act("G14", "Firmar el decreto de cuotas sin trámites para el pago voluntario de las multas, según el ingreso (compromiso 17)",
    "Intendente con Tránsito y el Juzgado de Faltas", dur=15, est=True, needs=["T07", "T05"], win=W(1, 3), fuente="6.4",
    steps="Como el de Balcarce. La cuota del mes no pasa del 2% del ingreso, dividido por la raíz cuadrada de las personas del hogar (5.11).")
act("G15", "Pedir a la Provincia seis cambios en las multas, y a la Legislatura la licencia por puntos (compromiso 18)",
    "Intendente", dur=10, est=True, needs=["T07"], win=W(1, 3), fuente="6.4",
    steps=("Pago voluntario según el ingreso. Un agregado al convenio de multas de 2020. Deuda congelada en pesos. "
           "Una sola multa por las pasadas antes del aviso. Permiso para trabajar durante la suspensión. Tope a la deuda por multas."))
act("G16", "Inscripción en línea para pagar en cuotas y plan sin interés para la deuda vieja (lo destraba la Ordenanza 15)",
    "Tránsito y Juzgado de Faltas", dur=20, est=True, needs=["C20", "I04"], fuente="anexo.15",
    steps="Se depuran las multas prescriptas. La inteligencia artificial avisa a cada vecino cuánto debe y hasta cuándo.")
act("G17", "Inscribir la base de datos de las cuotas ante la autoridad de datos personales (lo destraba la Ordenanza 16)",
    "Gobierno y Legal y Técnica", dur=10, est=True, needs=["C23"], fuente="anexo.16",
    steps="Una persona fija cada cuota, y el vecino puede pedir que se revise.")
act("G18", "La inteligencia artificial propone dónde poner cámaras de multas, sólo donde se supera un mínimo publicado de choques",
    "Tránsito y Juzgado de Faltas", dur=30, est=True, needs=["I04"], win=W(6, 12), fuente="6.4")
act("G19", "Cada comisión de zona elige entre una cámara o un reductor de velocidad", "Comisiones vecinales", dur=30, est=True,
    needs=["G18", "M04"], win=W(6, 12), fuente="6.4",
    steps="No puede elegir no hacer nada. El reductor se paga con el dinero de obra de la zona. En las avenidas que cruzan varias zonas opina el panel (5.11).")
act("G20", "La Provincia autoriza cada cámara (Disposiciones 14/2020 y 43/2021)", "Provincia de Buenos Aires", dur=40, est=True,
    needs=["G19"], fuente="6.4", note="El calendario dice «después»: no da fecha.")
act("G21", "Desde el presupuesto del año 2, el dinero de las multas va a un fondo de seguridad vial", "Secretaría de Hacienda",
    ms=True, needs=["P15"], sne=D(2029, 1, 2), fuente="6.4",
    steps="Renglón propio en el presupuesto. No se puede usar para otra cosa (Ley 24.449, artículo 85).",
    note="Fecha estimada: el presupuesto del año 2 rige desde enero de 2029.")
act("G22", "Revisar cada cámara de multas una vez por año, con sus datos a la vista", "Tránsito y Juzgado de Faltas",
    dur=10, est=True, needs=[("G20", "FS", 250)], fuente="6.6",
    note="Riesgo del 6.6: las cámaras se ponen para recaudar. Supuesto: la primera revisión es un año después de la autorización.")
act("G23", "Nadie gana dinero por cada multa: los proveedores cobran sólo los equipos y su mantenimiento, a precio fijo (meta 20)",
    "Tránsito y Juzgado de Faltas", ms=True, needs=["G21", "G22"], win=FIN, fuente="6.3",
    note="Rige cuando vence cada contrato actual (5.11). El programa no da esas fechas.")
act("G24", "Organizar los días fijos de la dirección de género en lugares que ya existen en cada zona", "Dirección de género",
    dur=20, est=True, needs=["T07"], fuente="5.13",
    steps="Delegaciones, centros de salud y centros de apoyo escolar. Sin sedes nuevas.")
act("G25", "La dirección de género empieza a atender días fijos en cada zona, empezando por Boulogne y Béccar", "Dirección de género",
    ms=True, needs=["G24"], win=W(4, 6), fuente="6.4")
act("G26", "Pedir lugar en la red provincial de hogares y firmar los convenios de patrocinio jurídico gratuito (lo destraba la Ordenanza 6)",
    "Dirección de género", dur=30, est=True, needs=["C30"], fuente="anexo.6",
    note="El refugio propio no es una promesa: va por convenio con la Provincia (6.5).")
act("G27", "Género con partida propia y atención en cada zona (meta 11)", "Dirección de género", ms=True,
    needs=["G25", "P29", "G26"], win=FIN, fuente="6.3",
    note="Hoy género no tiene partida propia y tiene una sola sede (cuadro 41).")

# ---------------------------------------------------------------- 9 Costa y espacio público
act("K01", "Pedir a AySA que diga si se pueden conectar a la cloaca los baños de los seis lugares de la costa", "Ambiente",
    dur=5, est=True, needs=["T07"], win=W(1, 3), fuente="6.4")
act("K02", "AySA confirma qué baños se pueden hacer", "AySA", dur=60, est=True, needs=["K01"], fuente="6.4",
    note="Depende de AySA.")
act("K03", "Reconocer las primeras asociaciones de parque: Parque del Águila y Bosque Alegre", "Gobierno y Legal y Técnica",
    dur=15, est=True, needs=["C10"], fuente="anexo.5",
    steps="Cada asociación opina antes de cualquier obra en su parque, participa del diseño y firma la recepción de la obra.")
act("K04", "Diagnóstico del desagüe de la calle Perú: marcador de ADN humano y unos veinte sensores caño arriba", "Ambiente",
    dur=60, est=True, needs=["P10"], win=AÑO1, fuente="6.4",
    steps="Abarca los tres municipios por donde pasa el desagüe. Si es la red de AySA, se le exige el arreglo. Si son casas, orden formal y ayuda para pagar el arreglo (5.5).")
act("K05", "Empezar las muestras de agua en cada tramo, dos veces por semana, y la bandera sanitaria de cada día", "Ambiente",
    dur=20, est=True, needs=["P10"], win=AÑO1, fuente="6.4")
act("K06", "Proyecto de los puestos náuticos, los baños y el tramo de arena, con su costo y sus planos",
    "Secretaría de Obras con Deportes y Ambiente", dur=30, est=True, needs=["T07"], fuente="5.5",
    note="El Ejecutivo se lo manda a la asociación del parque antes que a nadie (Ordenanza 5, artículo 2).")
act("K07", "Estudio de impacto ambiental de las obras de la costa del año 1", "Ambiente", dur=40, est=True,
    needs=["K06", "C45"], fuente="anexo.12", steps="Toda persona lo puede consultar completo.")
act("K08", "Dictamen de la asociación del Parque del Águila sobre las obras en su parque", "Asociaciones de parque",
    dur=22, needs=["K03", "K06"], fuente="anexo.5", durnote=TREINTA,
    note="Vencido el plazo, quien decide la obra decide sin el dictamen.")
act("K09", "Concurso abierto de profesores de la Escuela Náutica, con prueba técnica y de rescate", "Deportes",
    dur=40, est=True, needs=["T07"], fuente="5.5", steps="Profesores del Municipio. No se subcontrata a escuelas ni a empresas privadas.")
act("K10", "Licitación propia de los dos primeros puestos náuticos: módulo de madera, bajada al río y bote", "Secretaría de Obras",
    dur=66, needs=["K07", "K05"], fuente="anexo.12", durnote=LIC)
act("K11", "Adjudicar los puestos náuticos, con el dictamen de la asociación y la recomendación del panel", "Secretaría de Obras",
    ms=True, needs=["K10", "K08", "M13"], fuente="6.4")
act("K12", "Armar los dos primeros puestos náuticos", "Secretaría de Obras", dur=20, est=True, needs=["K11"], fuente="5.5")
act("K13", "Abren los dos primeros puestos de la Escuela Náutica: el Parque del Águila y el siguiente con mejor agua", "Deportes",
    ms=True, needs=["K12", "K09"], win=W(7, 12), fuente="6.4",
    steps="Kayak y stand up paddle. La clase en el agua, sólo si la bandera lo permite. Si no, en tierra.")
act("K14", "Licitación propia de los dos primeros baños con cloaca y sus plataformas para las clases", "Secretaría de Obras",
    dur=66, needs=["K07", "K02"], fuente="anexo.12", durnote=LIC)
act("K15", "Adjudicar los baños, con el dictamen de la asociación y la recomendación del panel", "Secretaría de Obras",
    ms=True, needs=["K14", "K08", "M13"], fuente="6.4")
act("K16", "Construir los dos primeros baños y sus plataformas", "Secretaría de Obras", dur=25, est=True, needs=["K15"],
    fuente="5.5")
act("K17", "Abren los dos primeros baños, conectados a la cloaca, con su plataforma para las clases", "Ambiente", ms=True,
    needs=["K16"], win=W(7, 12), fuente="6.4", steps="Gratis. Abiertos de día, con un encargado fijo. Nunca químicos ni secos.")
act("K18", "Licitación propia del primer tramo de prueba con arena", "Secretaría de Obras", dur=66, needs=["K07"],
    fuente="anexo.12", durnote=LIC)
act("K19", "Adjudicar el tramo de arena, con la recomendación del panel", "Secretaría de Obras", ms=True,
    needs=["K18", "M13"], fuente="5.5")
act("K20", "Construir el tramo de prueba: 100 por 20 metros, sobre base de piedra", "Secretaría de Obras", dur=25, est=True,
    needs=["K19"], fuente="5.5")
act("K21", "Contratar los guardavidas del tramo: uno cada 80 metros, mínimo dos, y un bote", "Ambiente", dur=20, est=True,
    needs=["P10"], fuente="5.5", steps="Hoy el Municipio ya contrata guardavidas para sus natatorios (5.5).")
act("K22", "Primer tramo de prueba con arena, con sus guardavidas y el baño habilitado", "Ambiente", ms=True,
    needs=["K20", "K21", "C42", "K05"], win=AÑO1, fuente="6.4")
act("K23", "Año 2: abren el tercer y el cuarto puesto náutico y dos baños más", "Deportes", dur=120, est=True,
    needs=["K13", "K17"], win=W(13, 24, "año 2 (meses 13 a 24)"), fuente="6.4")
act("K24", "Año 3: abren los dos últimos puestos náuticos y los dos últimos baños", "Deportes", dur=120, est=True,
    needs=["K23"], win=W(25, 36, "año 3 (meses 25 a 36)"), fuente="6.4")
act("K25", "Foodtrucks al borde de cada puesto, con canon y 75% de empleo local (lo destraba la ordenanza de foodtrucks)",
    "Habilitaciones y Agencia de Control", dur=20, est=True, needs=["C55", "K13"], fuente="5.5",
    steps="En la calle o en playones, nunca sobre el pasto. Ofertas de lunes a jueves.")
act("K26", "Centro de foodtrucks y actividades en el Bosque Alegre (lo destraba el cambio de la Ordenanza 5824)",
    "Habilitaciones y Agencia de Control", dur=20, est=True, needs=["C58", "K25"], fuente="5.5",
    steps="Sobre la calle ancha y el lote de ripio del Centro de Exposiciones, sin entrar al bosque.")
act("K27", "Preparar las clases gratis del Municipio en las plazas donde ya dan clase los instructores registrados", "Deportes",
    dur=20, est=True, needs=["U02"], fuente="5.5")
act("K28", "Empiezan las clases gratis del Municipio en plazas y parques", "Deportes", ms=True, needs=["K27"],
    win=W(4, 6), fuente="6.4")
act("K29", "Pedir a la Provincia la ley que protege la ribera y los parques principales", "Intendente", dur=10, est=True,
    needs=["C51"], fuente="anexo.14", reldl=("C51", 180),
    note="La Ordenanza 14 da 180 días para pedirla.")
act("K30", "Congelar y revisar la lista de trabajadores de la recolección al llamar a licitación", "Ambiente",
    dur=20, est=True, needs=[("K31", "SS", 0)], fuente="6.6",
    note="Riesgo del 6.6: cada año sin licitar, la antigüedad que reconoce el Municipio crece unos 650 millones.")
act("K31", "Llamado a licitación de la recolección, en dos zonas, con el pliego aprobado por ordenanza", "Ambiente", ms=True,
    needs=["C16"], win=W(6), fuente="6.4")
act("K32", "Licitación de la recolección: ofertas y evaluación", "Ambiente", dur=66, needs=["K31"], fuente="6.4", durnote=LIC,
    steps="Presupuesto oficial con precios de mercado. Pago según lo que se mide (5.5).")
act("K33", "Se adjudica la recolección por licitación pública (meta 9)", "Intendente", ms=True, needs=["K32", "K30"],
    win=W(9), fuente="6.4", note="Desde 2004 se llamó a cuatro licitaciones, y ninguna terminó en un contrato (cuadro 41).")
act("K34", "Pedir por convenio a Trenes Argentinos dónde está cada tren del Mitre y del Tren de la Costa", "Intendente",
    dur=30, est=True, needs=["T07"], fuente="5.5")
act("K35", "La inteligencia artificial dice dónde está cada tren y cuánto falta, y se ponen carteles de cada estación al río",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["K34", "I04"], win=W(6, 9), fuente="6.4")
act("K36", "Licitar las cámaras que cuentan gente en los accesos de los 21 playones de la costa", "Ambiente", dur=66,
    needs=["P11"], win=W(12, 18), fuente="6.4", durnote=LIC, steps="Se pagan con el aumento del gasto en ambiente.")
act("K37", "Instalar una cámara que cuenta gente en cada acceso de los 21 playones", "Ambiente", dur=20, est=True,
    needs=["K36"], win=W(12, 18), fuente="6.4")
act("K38", "Las estaciones móviles miden el ruido de motos y colectivos donde marca el mapa del ruido (meta 18)", "Ambiente",
    dur=20, est=True, needs=["C36", "I04"], win=W(12, 18), fuente="6.4",
    steps="Primero un aviso. Un inspector revisa con un instrumento aprobado antes de multar. Cualquiera puede preguntar qué se midió en su zona.")

# ---------------------------------------------------------------- 10 Cultura y espectáculos
act("U01", "Preparar el decreto de prueba de los espectáculos al aire libre de lunes a jueves", "Cultura", dur=15, est=True,
    needs=["T07", "T05"], win=W(1, 3), fuente="5.5",
    steps=("Lugares señalizados. Cien metros entre puntos con sonido. Turnos de una hora. Volumen máximo medido. Hora de fin. "
           "Zonas tranquilas: la Reserva Ribera Norte, el Bosque Alegre y los frentes de las casas."))
act("U02", "Empieza la prueba por decreto y abre el registro gratis de instructores y artistas (compromiso 21)", "Cultura",
    ms=True, needs=["U01", "I04"], win=W(1, 3), fuente="6.4", note="Riesgo del 6.6: espectáculos que saturan una plaza.")
act("U03", "Licitación pública de los equipos de sonido propios", "Cultura", dur=66, needs=["T07"], win=AÑO1, fuente="5.5",
    durnote=LIC, steps="Dos equipos para bandas y dos chicos para artistas callejeros, con requisitos de calidad publicados.",
    note="El primer año los shows cuestan 532 millones, con la compra de los equipos (5.5).")
act("U04", "Armar los tres grupos de producción y el control de los equipos", "Cultura", dur=20, est=True, needs=["U03"],
    win=AÑO1, fuente="5.5",
    steps="Ocho personas nuevas. Patrimonio hace un control sorpresa cada mes. Remitos con código QR, rastreador GPS y seguro.")
act("U05", "Los vecinos proponen en la inteligencia artificial a qué artistas nuevos de San Isidro quieren ver", "Cultura",
    dur=20, est=True, needs=["I04"], fuente="5.5",
    steps="Artistas con menos de 50.000 oyentes por mes. Al menos un 30% de mujeres (Ley 27.539).")
act("U06", "Convenio con cuatro clubes o centros culturales para los shows bajo techo", "Cultura", dur=30, est=True,
    needs=["T07", "T05"], fuente="5.5",
    note="Supuesto: hace falta antes de los primeros shows, porque al aire libre se toca del 20 de septiembre al 15 de abril (5.5).")
act("U07", "Primeros espectáculos que paga el Municipio, con artistas nuevos de San Isidro y prioridad para las bandas", "Cultura",
    ms=True, needs=["U05", "U06"], win=W(4, 6), fuente="6.4",
    steps="Se paga directo al artista, por músico, con el piso del sindicato más un 25%. Cada pago, publicado.")
act("U08", "Sumar al cuadro de usos la categoría de la Ley 15.302: hasta 300 personas y 500 metros cuadrados (lo destraba la Ordenanza 7)",
    "Habilitaciones y Agencia de Control", dur=20, est=True, needs=["C13"], fuente="anexo.7",
    steps="La comisión de la zona opina sobre horarios y lugar.")
act("U09", "El registro de instructores y artistas pasa a ser permanente (lo destraba la Ordenanza 14)", "Cultura", ms=True,
    needs=["C51", "U02"], fuente="anexo.14", steps="El 75% de los lugares de instructores, para vecinos de San Isidro con un año de domicilio.")
act("U10", "Doscientos shows por año de artistas nuevos de San Isidro, y espectáculos al aire libre todas las semanas, de lunes a jueves (meta 17)",
    "Cultura", ms=True, needs=["U07", "U04", "U09"], win=FIN, fuente="6.3",
    note="En 2026 hubo un solo espectáculo en un día hábil en la costa, según el Municipio (cuadro 41).")

# ---------------------------------------------------------------- 11 Habilitaciones e inspecciones
act("H01", "Firmar el decreto que ordena grabar cada inspección con el teléfono del agente (compromiso 16)", "Intendente",
    dur=10, est=True, needs=["T07"], win=W(1, 3), fuente="6.4")
act("H02", "Llamar a la compra de los soportes de pecho y las baterías", "Habilitaciones y Agencia de Control", dur=5,
    est=True, needs=["H01"], win=W(1, 3), fuente="6.4")
act("H03", "Compra de soportes y baterías: adjudicación y entrega", "Habilitaciones y Agencia de Control", dur=66,
    needs=["H02"], fuente="6.4", durnote=LIC)
act("H04", "Convenio con el banco que paga los sueldos: teléfonos aptos en 24 cuotas sin interés",
    "Secretaría de Hacienda con el banco que paga los sueldos", dur=20, est=True, needs=["T07", "T05"], win=W(1, 3),
    fuente="6.4", steps="El Municipio no adelanta dinero. El riesgo de cobro lo toma el banco.")
act("H05", "Acordar con los trabajadores municipales la compensación por usar el teléfono propio (Ley 14.656, artículo 75)",
    "Intendente con los trabajadores municipales", dur=40, est=True, needs=["H01", "T05"], fuente="5.9")
act("H06", "Construir la grabación sellada del turno: huella al grabar, corte por inspección y base por comercio o domicilio",
    "Equipo de la inteligencia artificial del Municipio", dur=60, est=True, needs=["I04", "I06"], fuente="5.9",
    steps="Avisa si una grabación sellada no se sube. Difumina las caras de quienes no son parte del acto antes de mostrarlo.")
act("H07", "El comerciante ya puede denunciar coimas, presiones y amenazas ante la inteligencia artificial, con grabación sellada (compromiso 16)",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "I06", "H01"], win=W(1, 3), fuente="6.4",
    steps=("La denuncia va a la Comisión de Obras y Servicios Públicos del Concejo, a la auditoría externa y, si hay delito, a la fiscalía. "
           "Nunca sólo al jefe del denunciado. Con la misma prueba sellada se puede denunciar un ruido."),
    note="Riesgo del 6.6: represalias contra el comerciante que denuncia.")
act("H08", "Los inspectores y los agentes de tránsito graban todo su turno con su teléfono", "Habilitaciones y Agencia de Control",
    ms=True, needs=["H03", "H04", "H05", "H06"], win=W(9), fuente="6.4",
    steps="Comercio, Agencia de Control, Habilitaciones, obra y tránsito: de 208 a 280 agentes. La patrulla municipal, en una segunda etapa (5.9).")
act("H09", "Rige la Ordenanza 4: sin grabación sellada y subida, no valen el acta, la clausura ni la habilitación", "Intendente",
    ms=True, needs=["C33", "H08"], fuente="anexo.4",
    note="Supuesto: la consecuencia rige desde que empiezan las grabaciones. El programa no dice desde cuándo rige.")
act("H10", "Organizar la atención del sábado con el personal que elige ese horario", "Intendente con los trabajadores municipales",
    dur=20, est=True, needs=["T07"], fuente="5.12",
    steps="Trabaja las mismas horas en otros días y descansa otro día de la semana. Es optativo.")
act("H11", "Atención los siete días: las delegaciones, el Juzgado de Faltas y los turnos de salud por teléfono abren el sábado a la mañana",
    "Intendente", ms=True, needs=["H10"], win=W(4, 6), fuente="6.4", steps="Las delegaciones abren rotando por zona.")
act("H12", "Habilitaciones en la inteligencia artificial: consulta previa con la cámara del teléfono, inspección con fecha fija y aviso de inspecciones fuera de lo normal",
    "Habilitaciones con el equipo de la inteligencia artificial", dur=60, est=True, needs=["I10", "H08"], win=W(18, 24),
    fuente="6.4", steps="Empieza por la habilitación comercial. Después siguen las obras particulares (5.9).")
act("H13", "Cada denuncia de un comerciante tiene respuesta, y la que es delito llega a la fiscalía (meta 16)", "Intendente",
    ms=True, needs=["H07", "H09"], win=FIN, fuente="6.3",
    note="Una condena no es una promesa: la decide un juez (6.5).")

# ---------------------------------------------------------------- 12 Transparencia
act("X01", "Registrar cada pedido de informes del Concejo y su respuesta, el día en que entra y el día en que sale",
    "Gobierno y Legal y Técnica", dur=15, est=True, needs=["T07"], win=W(1, 3), fuente="4.7",
    note="Hoy ese intercambio no deja ningún registro público (cuadro 40).")
act("X02", "Cualquier vecino puede preguntar por cada pedido de informes del Concejo y su respuesta (compromiso 10)",
    "Gobierno y Legal y Técnica", ms=True, needs=["X01", "I04"], win=W(1, 3), fuente="6.4")
act("X03", "Cualquier vecino puede preguntar qué se hizo en su zona, y cada contrato queda registrado el día en que se firma",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I10"], win=W(9), fuente="6.4",
    note="Sólo lo gastado del presupuesto se muestra cada tres meses (cuadro 42).")
act("X04", "Cargar en qué se gastó el Fondo Educativo, obra por obra", "Educación (área municipal)", dur=30, est=True,
    needs=["I04"], win=AÑO1, fuente="6.4")
act("X05", "Cualquiera puede preguntar en qué se gastó el Fondo Educativo, obra por obra", "Educación (área municipal)",
    ms=True, needs=["X04"], win=W(12), fuente="6.4")
act("X06", "Anotar cada gasto del Municipio con la zona donde se hace", "Secretaría de Hacienda con la Secretaría de Obras",
    dur=260, est=True, needs=["C06", ("E12", "SS", 0)], fuente="5.12",
    steps="Hacienda y Obras suman esta tarea. Lo carga también un equipo de pasantes de Hacienda (cuadro 33).",
    note="Ningún municipio del conurbano norte lo hace. Riesgo del 6.6: cuesta más de lo previsto; por eso es meta de los cuatro años.")
act("X07", "Cualquier vecino puede preguntar cuánto se gastó en su zona (meta 5)", "Secretaría de Hacienda", ms=True,
    needs=["X06"], win=W(36, 42), fuente="6.4",
    note="La Ordenanza 1 pide que funcione antes del fin del mandato (artículo 9).")
act("X08", "Rige el Sistema de Información Municipal: cada dato se registra el día en que se genera (lo destraba la Ordenanza 2)",
    "Gobierno y Legal y Técnica", ms=True, needs=["C27"], fuente="anexo.2",
    steps="Entran la espera por especialidad, la matrícula por sede, las órdenes de juez y la inserción laboral (artículo 2).")
act("X09", "Cada funcionario contesta, dentro del plazo, lo que los vecinos le plantean a la inteligencia artificial (meta 15)",
    "Intendente", ms=True, needs=["I04", "X08"], win=FIN, fuente="6.3",
    note="Hoy no hay forma pública de saber cuánto tarda el Municipio en responder un reclamo (cuadro 41).")
