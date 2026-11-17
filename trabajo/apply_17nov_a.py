"""Actualización del 17/11/2026, parte A: recuadros nuevos (vivienda, denuncias, power users, historias,
salud mental, consulta de lugares), Miami, ordenanzas nuevas del anexo y lo que tiene que ver un abogado."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}

def primera(p):
    m = re.search(r'\.(\s|$)', p)
    return m.end() - (1 if m.group(1) else 0) if m else len(p)

def caja(eid, padre, titulo, parrafos, fuentes, tono='g', despues=None):
    assert eid not in by, eid
    texto = '\n\n'.join(parrafos)
    marcas = {str(i): [[0, primera(p), 'b']] for i, p in enumerate(parrafos)}
    e = {'id': eid, 'capitulo': by[padre]['capitulo'], 'titulo': titulo, 'hoja_a4': by[padre]['hoja_a4_fin'],
         'hoja_a4_fin': by[padre]['hoja_a4_fin'], 'texto': texto, 'cuadros': [], 'fuentes': fuentes,
         'recuadro_de': padre, 'marcas': marcas, 'tono': tono}
    i = max(k for k, x in enumerate(d) if x['id'] == padre or x.get('recuadro_de') == padre)
    d.insert(i + 1, e); by[eid] = e
    o = by[padre]['orden']
    if despues:
        j = next(k for k, x in enumerate(o) if x == ['box', despues]); o.insert(j + 1, ['box', eid])
    else:
        o.append(['box', eid])

def anexo(eid, titulo, arts):
    assert eid not in by, eid
    ps = []
    for t, cuerpo in arts:
        ps += [t, cuerpo]
    i = max(k for k, x in enumerate(d) if re.fullmatch(r'anexo-\d+', x['id']))
    e = {'id': eid, 'capitulo': by['anexo-18']['capitulo'], 'titulo': titulo, 'hoja_a4': by['anexo-18']['hoja_a4_fin'],
         'hoja_a4_fin': by['anexo-18']['hoja_a4_fin'], 'texto': '\n\n'.join(ps), 'cuadros': [], 'fuentes': '',
         'marcas': {}, 'orden': [['h3' if k % 2 == 0 else 'p', k] for k in range(len(ps))]}
    if 'orden' not in by['anexo-18']: e.pop('orden')
    d.insert(i + 1, e); by[eid] = e

def rep(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]; assert len(hits) == 1, (eid, old[:50], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and m[1] <= end and m[0] < pos: m[1] = max(m[0] + 1, min(m[1], pos + len(new)))
        elif m[1] > pos: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)

def agregar_parrafo(eid, texto, marca=None):
    e = by[eid]; ps = e['texto'].split('\n\n'); ps.append(texto); e['texto'] = '\n\n'.join(ps)
    k = len(ps) - 1
    if 'orden' in e: e['orden'].append(['p', k])
    if marca: e.setdefault('marcas', {})[str(k)] = [[0, primera(texto), 'b']]

# ---------- 5.4 Vivienda ----------
caja('5.4-r1', '5.4', 'Nuestra propuesta: una garantía del Municipio para alquilar', [
 'Hoy, para alquilar hace falta una garantía: un familiar con una casa a su nombre o un seguro de caución, que cuesta del 4% al 7% del contrato y pide recibo de sueldo. Muchos jóvenes de San Isidro no tienen ninguna de las dos cosas. Según una encuesta nacional, el 44% de los jóvenes vive con sus padres, y el 7% dice que lo que lo frena es no conseguir garantía. Llevado a San Isidro, son unas 840 personas que quieren mudarse y no pueden.',
 '1 · El Municipio va a dar la garantía, como hace Uruguay desde 1936. Allá hay unas 35.000 garantías del Estado, casi una de cada cuatro casas alquiladas. Es para quien no consigue un seguro de caución: jóvenes, trabajadores sin recibo de sueldo y quienes trabajan o estudian en los programas del Municipio.',
 '2 · La paga el propio sistema, no el Municipio. Cada mes, el inquilino paga el 3% del alquiler, y el dueño, otro 3%. Al entrar, el inquilino deja un depósito del 12% de un mes. En un contrato de dos años, eso suma menos de un mes de alquiler, contra uno o dos meses de un seguro de caución. Con ese dinero se forma un fondo que le paga al dueño si el inquilino deja de pagar.',
 '3 · Está pensada para que no suba los alquileres. El alquiler garantizado no puede pasar del 40% del ingreso de quien alquila, como en Uruguay. Quien tiene ingresos sin recibo los declara bajo juramento ante la inteligencia artificial del Municipio, y una persona del Municipio lo aprueba. A quien cobra del Municipio, el alquiler se le descuenta del sueldo.',
 '4 · Tiene un freno. Si muchos dejan de pagar, se dejan de dar garantías nuevas hasta que el fondo se recupere, porque eso quiere decir que el sistema no se sostiene. En la cuenta de este programa, el fondo no queda en rojo aunque deje de pagar uno de cada diez, el doble de lo que calculaba Uruguay. Lo que el Municipio cobra por la suba de valor de un terreno cuando da una excepción para construir más (Ordenanza 13 del anexo) también va a reforzar el fondo.',
 '5 · No le cuesta al Municipio ni compite con los bancos. La garantía no presta dinero: sólo respalda el pago del alquiler. Funciona también para alquilar una habitación o una parte de una casa (recuadro siguiente).'],
 '5.4 · la garantía de Uruguay: Ministerio de Vivienda y Ordenamiento Territorial de Uruguay, «Garantía de alquiler para jóvenes» (gub.uy, 13 de marzo de 2024), y «El alquiler como alternativa de acceso a la vivienda» (2010): unas 35.000 garantías de la Contaduría General de la Nación, el 23% de los alquileres del país, y un fondo con el 0,8% de quebranto en diciembre de 2009.\n\n5.4 · los jóvenes: UADE, Centro de Investigaciones Sociales, informe de situación habitacional (1.040 encuestados de todo el país; Ámbito, 28 de julio de 2026). Censo 2022 (INDEC): 46.815 personas de 18 a 29 años en San Isidro. Las 840 salen de aplicarles el 44% que vive con sus padres, el 58% de ellos que quiere mudarse y el 7% que no consigue garantía.\n\n5.4 · el seguro de caución: iProfesional, 12 de mayo de 2026.\n\n5.4 · el fondo: cuenta de este programa con el alquiler de un departamento de dos ambientes en el GBA Norte (826.916 pesos por mes, Zonaprop, septiembre de 2026), mil garantías que entran a lo largo del primer año y seis meses de alquiler perdidos por cada caso que deja de pagar.')

caja('5.4-r2', '5.4', 'Nuestra propuesta: más lugares para alquilar, con las casas que ya existen', [
 'La forma más rápida y barata de que haya más lugares para alquilar no es construir. Es que las casas que ya existen puedan alquilar una parte. En San Isidro hay muchas personas mayores que viven solas en casas grandes. Con un ingreso fácil y seguro, muchas van a querer alquilarle una habitación o una parte de la casa a un joven.',
 '1 · Se va a poder tener una segunda y una tercera vivienda en el mismo lote, por ejemplo un departamento chico al fondo. California lo permitió por ley en 2016: los permisos pasaron de algo más de mil por año a más de 24.000 en 2022, casi una de cada cinco viviendas nuevas. En San Isidro va a ir por ordenanza (Ordenanza 21 del anexo).',
 '2 · Alquilar una habitación o una parte de la casa va a ser fácil, legal y sin castigo. Vale el alquiler de siempre y el de aplicaciones como Airbnb. Quien hoy alquila sin papeles va a poder ponerse en regla sin multa. El Municipio no va a pedir habilitación ni va a mandar inspecciones para esto, y lo va a promocionar. La tasa de cada casa sigue igual.',
 '3 · La inteligencia artificial del Municipio va a juntar al dueño con el inquilino. Les va a armar el contrato y les va a explicar sus derechos a los dos. Además, con el permiso de cada uno, va a verificar la identidad y el historial de pagos. Así, el dueño corre menos riesgo, y la garantía del Municipio también sirve para una habitación.',
 '4 · Ya funciona en otros lugares. Desde 2001, València junta a personas mayores que viven solas con estudiantes que no pueden pagar un alquiler, con el apoyo del Ayuntamiento y de tres universidades. La inteligencia artificial del Municipio va a poder hacer lo mismo en San Isidro, para quien quiera.',
 '5 · Si una norma de la Provincia pide inscribir un alquiler temporario, la inteligencia artificial del Municipio va a hacer la inscripción junto con el dueño.'],
 '5.4 · California: Bipartisan Policy Center, «Accessory Dwelling Units (ADUs) in California», 12 de septiembre de 2023.\n\n5.4 · València: El Periòdic, 4 de mayo de 2025 (programa ValènciaConviu, que empezó en 2001 como «Viure i Conviure»).\n\n5.4 · la Provincia: Ley 14.209 de turismo y su Decreto 13/2014, que crean el Registro Provincial de Prestadores Turísticos.')

caja('5.4-r3', '5.4', 'Nuestra propuesta: los terrenos que nadie usa, a construir o a vender', [
 'Un terreno vacío en un lugar donde falta dónde vivir le hace daño a todos. Sube el precio de lo que queda, y los jóvenes, que son el futuro de la economía, no pueden progresar. Comprar para especular y dejar el lugar sin uso va contra el bien común. Todas las generaciones tienen que tener las mismas oportunidades.',
 '1 · El Municipio va a usar la ley provincial que ya existe. La Ley 14.449 permite obligar a construir en los terrenos baldíos, en los edificios en ruinas y en las obras paradas hace más de cinco años. Hace falta una ordenanza del Concejo, una sola vez (Ordenanza 21 del anexo).',
 '2 · El dueño va a tener tres años para empezar a construir o vender, el plazo más corto que permite la ley. Construir quiere decir empezar la obra. Para terminarla, el plazo lo va a calcular la inteligencia artificial del Municipio según el tamaño de la obra, con una regla publicada, y no un funcionario.',
 '3 · Si no cumple, paga un recargo que sube cada año durante cinco años, hasta el 50% de la tasa, el máximo que permite la ley, sin rebajas. Pasados esos cinco años, el terreno se puede expropiar, pagándole al dueño su valor, como manda la Constitución. Lo que se cobre por el recargo va a ir a la garantía de alquiler.',
 '4 · Venderlo no sirve para esquivar la regla. Según la misma ley, el plazo sigue corriendo aunque el terreno se venda, y la obligación queda anotada en la escritura. El que compra hereda el tiempo que quedaba.',
 '5 · Primero hay que saber cuántos son. Durante la primera ronda de asambleas se van a contar los baldíos, las ruinas y las obras paradas, y la inteligencia artificial del Municipio va a mostrar cuántos hay en cada zona. A cada dueño se le va a explicar el daño que hace un terreno vacío y qué puede hacer con él.'],
 '5.4 · los terrenos sin uso: Ley 14.449, artículo 64, que reemplaza los artículos 84 a 88 del Decreto-Ley 8912/77 (texto actualizado en normas.gba.gob.ar): plazo para edificar de tres a cinco años, gravamen progresivo durante cinco años con tope del 50% de la tasa de alumbrado, barrido y limpieza, plazos que no cambian con la venta y expropiación después de cinco años de gravamen. Constitución Nacional, artículo 17.')

agregar_parrafo('5.4', 'Cuando la Provincia abra un plan de vivienda, la inteligencia artificial del Municipio le va a avisar a cada joven que puede anotarse, y el Municipio se va a anotar para que llegue a San Isidro.')

# ---------- 4.11 ----------
caja('4.11-r4', '4.11', 'Nuestra propuesta: la inteligencia artificial del Municipio, del lado del vecino cuando necesita reclamar o denunciar', [
 'Muchas veces, el vecino no sabe si lo que le pasó es una falta, un delito o nada, ni dónde se denuncia. Con la inteligencia artificial del Municipio va a alcanzar con contarlo. Vale para lo que le pasó a él y para lo que ve en la calle.',
 '1 · Le va a explicar qué dice la ley. Por ejemplo, si un cuidacoches insulta o amenaza a quien ya le dijo que no, eso es una falta del Código de Faltas de la Provincia, y si lo intimida para cobrar, es un delito.',
 '2 · Lo va a ayudar a juntar la prueba: fotos, videos y cómo fue. Las grabaciones que hace el vecino se sellan en el momento, como las de las inspecciones (5.9).',
 '3 · Le va a preguntar si quiere que haga la denuncia, y la va a redactar. Cuando el hecho entra en el sistema de denuncias en línea de la Provincia, la manda por ahí. Si no, la deja lista para que el vecino la firme y la presente en la fiscalía. No hace falta abogado, porque el que denuncia es el vecino. Sólo si quiere ser parte del juicio, el Municipio le va a ofrecer uno de sus abogados.',
 '4 · Lo mismo con una carta documento: la inteligencia artificial del Municipio la escribe y el vecino la manda él mismo, por el servicio electrónico del Correo Argentino.',
 '5 · La denuncia llega también al Municipio y a cada lugar que corresponda, y queda registrada. El vecino puede preguntar en qué está cuando quiera.',
 '6 · También va a servir para anotarse en la asociación vecinal, en línea. Para inscribirse en el Municipio y tener su espacio propio en la inteligencia artificial del Municipio, cada asociación va a aceptar a los vecinos que se anotan así.',
 '7 · Para votar, le va a explicar cada tema con sus datos, sin decirle qué votar. En una elección, va a mostrar lo que propone cada lista, con el mismo espacio para todas. Antes de cada elección, en los días que fija el Código Electoral Nacional, deja de hacerlo.'],
 '4.11 · la denuncia: Código Procesal Penal de la Provincia (Ley 11.922), artículos 285 a 287. Ministerio Público de la Provincia de Buenos Aires, «Denuncias» (mpba.gov.ar/denuncia): oficinas de denuncias y sistema de denuncias en línea «Mi Seguridad».\n\n4.11 · cuidacoches: Código de Faltas de la Provincia (Decreto-Ley 8031/73), artículos 67 b y 74 a; Código Penal, artículos 149 bis y 168.\n\n4.11 · carta documento: Correo Argentino, servicio electrónico con validación de identidad (Disposición 1197/23).\n\n4.11 · elecciones: Código Electoral Nacional, artículo 64 quater.')

caja('4.11-r5', '4.11', 'Nuestra propuesta: los power users de la inteligencia artificial del Municipio', [
 'Los vecinos y los empleados que usan la inteligencia artificial del Municipio para mejorarlo van a cobrar por lo que logran: son sus power users. Cobran sólo una parte de lo que su aviso le hace cobrar o ahorrar al Municipio, así que el sistema no puede costar más de lo que genera.',
 '1 · Hay tres fórmulas, publicadas. Para lo que se cobra gracias al aviso, se paga un porcentaje de lo cobrado. Si el aviso ahorra dinero, se paga un porcentaje del ahorro del primer año. Cuando la mejora no tiene un monto, se usa una tabla según cuánto vale y a cuántos vecinos les sirve.',
 '2 · La cuenta la hace la inteligencia artificial del Municipio, y se respeta. Una persona confirma cada pago, y cada power user ve cómo se calculó lo suyo, para entender por qué cobra lo que cobra y hacer más de eso.',
 '3 · Pueden cobrar todos, también los empleados del Municipio, porque dejar a alguien afuera invita a hacer trampa. No hay tope por persona: si genera mejoras, no hay por qué limitarlo. Cobra el primero que avisa, sin esperas.',
 '4 · Está protegido contra el engaño. Hacer una denuncia falsa es un delito, y no cobra quien armó o dirigió lo que denuncia. Ningún pago sale por decisión de la inteligencia artificial sola: lo aprueba una persona, y queda registrado quién hizo qué. Si la inteligencia artificial sospecha un acuerdo para cobrar, avisa. Sigue las guías internacionales para estos sistemas, que piden tratar al programa como una pieza en la que no se confía a ciegas.'],
 '4.11 · premios por ahorro: Estados Unidos, 5 U.S.C. § 4503 (premios a empleados públicos por mejoras de eficiencia), y la escala de sugerencias del gobierno federal (10% del beneficio del primer año). Comisión de Bolsa y Valores de Estados Unidos, 17 CFR 240.21F-16 (no cobra quien dirigió la conducta). Nota Fiscal Paulista: Naritomi, American Economic Review 109(9), 2019.\n\n4.11 · seguridad: OWASP, Top 10 para aplicaciones con modelos de lenguaje (2026); NIST AI 100-2 E2025. Código Penal, artículo 245 (falsa denuncia).')

caja('4.11-r6', '4.11', 'Nuestra propuesta: historias cortas para aprender a usarla', [
 'La inteligencia artificial del Municipio sólo sirve si la gente sabe todo lo que puede hacer. Por eso va a mostrar historias cortas, como las de las redes, con cosas que ya hace: sacar un turno, ver si un local se puede habilitar, denunciar o mostrarle un lugar. También van a salir en las redes del Municipio.',
 'Cada vecino va a ver primero las que le sirven a él, según lo que usa. Ese uso para el propio vecino tiene un aviso y un botón para apagarlo. Lo que el Municipio usa para mejorar el servicio va sin nombre.'], '')

# ---------- 5.6 Salud mental ----------
caja('5.6-r5', '5.6', 'Nuestra propuesta: salud mental, con acompañantes y alguien con quien hablar', [
 'San Isidro ya tiene una sala municipal de internación en salud mental en el Hospital Central, abierta en abril de 2025. Proponemos sumar acompañamiento cerca de la casa, con lo que ya existe.',
 '1 · Acompañantes terapéuticos. Empleados del Municipio cuyo trabajo ahora hace la inteligencia artificial van a poder formarse como acompañantes, con la formación que fija la Provincia (Resolución 592/2022). Van a trabajar asesorados y controlados por profesionales. No suma sueldos, porque ya son empleados del Municipio.',
 '2 · Vecinos que acompañan a vecinos, en los casos leves, como una depresión leve o un autismo leve. En Zimbabue, mujeres de la comunidad formadas y supervisadas lo hacen: a los seis meses seguía con depresión el 14% de los atendidos, contra el 50% con la atención común. Los casos graves van siempre a profesionales, en una institución.',
 '3 · Receta social. El acompañante puede llevar al vecino a las clases gratis del Municipio en la costa y los parques (5.5), o a un espectáculo de la agenda cultural. En Inglaterra, los médicos de cabecera hicieron 1,3 millones de derivaciones así en 2023.',
 '4 · Alguien con quien hablar, a cualquier hora. El vecino que quiera le va a poder contar a la inteligencia artificial del Municipio cómo se siente. Con su permiso, ella le pasa un resumen a su acompañante y al profesional. Si escucha una emergencia, avisa a quien corresponda y le da la Línea Nacional de Salud Mental, 0800-999-0091.',
 '5 · Con reglas claras. La inteligencia artificial no hace terapia ni diagnostica: acompaña y avisa, bajo un profesional responsable. Le recuerda al vecino, cada tanto, que no está hablando con una persona. Nadie está obligado a contar nada, y lo que cuenta es un dato de salud protegido por la ley.'],
 '5.6 · la sala del Hospital Central: El Economista, 14 de abril de 2025.\n\n5.6 · vecinos que acompañan: Chibanda y otros, Friendship Bench, JAMA, 2016.\n\n5.6 · receta social: The Lancet Public Health, septiembre de 2025.\n\n5.6 · la inteligencia artificial: Asociación Estadounidense de Psicología, aviso de salud de noviembre de 2025; ensayo de Therabot, NEJM AI, 27 de marzo de 2025.\n\n5.6 · reglas: Resolución 592/2022 del Ministerio de Salud de la Provincia; Ley 25.326, artículos 2, 7 y 8; Línea Nacional de Salud Mental.')

# ---------- 5.9 ----------
caja('5.9-r3', '5.9', 'Nuestra propuesta: le mostrás un lugar y te dice qué se puede hacer', [
 'Hoy, para saber qué se puede hacer en un terreno, una casa o un local, hay que pagarle a un profesional o recorrer oficinas. Con la inteligencia artificial del Municipio va a alcanzar con mostrarle el lugar con la cámara del teléfono y decirle qué le gustaría hacer. Vale también para un pedazo de plaza.',
 '1 · Primero, las reglas. La inteligencia artificial del Municipio lee el Código de Ordenamiento Urbano y los datos del catastro, y calcula lo que permite cada lote: metros, pisos y retiros. Las medidas salen del catastro, no de la foto.',
 '2 · Después, la imagen. Sobre el video del vecino dibuja cómo quedaría, marcado como ilustración, y le muestra ejemplos parecidos. No encontramos ningún municipio que lo haga sobre el video del propio vecino: San Isidro sería el primero.',
 '3 · Si el vecino no sabe qué quiere, la inteligencia artificial lo ayuda a definirlo. Le hace preguntas abiertas, una por vez, sobre lo que necesita y para qué, sin empujarlo hacia una respuesta.',
 '4 · En una plaza o un parque, le muestra lo que permite la Ordenanza 14 del anexo: nada que cierre, cobre o se quede con una parte del espacio. Sí puede dar clases con el registro gratuito de instructores, o proponerle una obra para la plaza a la comisión de su zona.',
 '5 · Lo que se presenta para una obra lo firma un profesional matriculado, que responde por el proyecto. La inteligencia artificial acelera, pero no aprueba sola.'],
 '5.9 · revisión previa con inteligencia artificial: Seattle (CivCheck, Daily Journal of Commerce, 7 de julio de 2026), Honolulu, Singapur (CORENET X) y Chile (REVI): en todos decide una persona. Imágenes guiadas por las reglas del lugar: He y otros, arXiv 2505.24260 (2025). Fotomontajes: Landscape Institute, nota técnica 06/19 (Reino Unido).')

# Miami (5.9-r1)
rep('5.9-r1', 'Preguntó por qué ese trámite tarda meses.', 'Preguntó por qué ese trámite tarda meses y meses.')
rep('5.9-r1', 'En marzo de 2026, la Ciudad de Miami empezó a usar una plataforma de permisos y licencias. Junta ocho aplicaciones en una, y hace sola buena parte de la revisión. Antes, en Miami-Dade, aprobar un permiso tardaba unos noventa días en promedio.',
    'En marzo de 2026, la Ciudad de Miami eligió una plataforma de permisos y licencias que junta ocho aplicaciones en una. Ese mismo mes empezó a revisar en el día las obras simples, y en julio el condado de Miami-Dade lo hizo permanente, con un 10% menos de tasa por cada día hábil de demora.')
by['5.9-r1']['fuentes'] = '5.9 · Miami: Refresh Miami, 7 de noviembre de 2025 (Jeff Bezos en el America Business Forum, 6 de noviembre de 2025). Ciudad de Miami, elección de Oracle Permitting and Licensing, 12 de marzo de 2026. Revisión en el día: Ciudad de Miami, 9 de marzo de 2026; Miami-Dade, 21 de julio de 2026 (Diario Las Américas, 22 de julio de 2026). El análisis crítico: Independent Institute, 23 de marzo de 2026.'

# ---------- Anexo ----------
anexo('anexo-19', '19 · Ordenanza de los foodtrucks y del Bosque Alegre', [
 ('Artículo 1 — Dónde', 'Los foodtrucks funcionan en la calle o en playones pavimentados o de ripio, al borde de cada puesto náutico de la costa y en el Bosque Alegre, nunca sobre el pasto (Ordenanza 14). La inteligencia artificial del Municipio asigna cada lugar y muestra qué foodtrucks hay cada día.'),
 ('Artículo 2 — Canon', 'Cada foodtruck paga un canon mensual por vehículo, que fija la Ordenanza Impositiva y reemplaza el derecho por ocupación del espacio público. En la costa de tenencia provincial se aplica el reparto del convenio aprobado por la Ordenanza 9430. La parte del Municipio se usa en la costa.'),
 ('Artículo 3 — Empleo local y ofertas', 'Rige el setenta y cinco por ciento (75%) de empleo local de la Ordenanza 10. Cada foodtruck ofrece descuentos de lunes a jueves.'),
 ('Artículo 4 — Bosque Alegre', 'Modifícase el artículo 9 de la Ordenanza 5824: en el Bosque Alegre se admite la venta de comidas y bebidas en foodtrucks sobre la calle y en el lote de ripio del Centro de Exposiciones, sin entrar al bosque.')])

anexo('anexo-20', '20 · Ordenanza de la garantía de alquiler', [
 ('Artículo 1 — Garantía del Municipio', 'Créase la garantía de alquiler del Municipio para quien alquila en San Isidro una vivienda, una parte de una vivienda o una habitación, y no consigue otra garantía. Tienen prioridad las personas de 18 a 29 años y quienes trabajan o estudian en los programas del Municipio.'),
 ('Artículo 2 — Fondo', 'La garantía se paga con un fondo propio, separado del resto del presupuesto. Lo forman una comisión mensual del tres por ciento (3%) del alquiler a cargo del inquilino, otra igual a cargo del propietario, un depósito único del doce por ciento (12%) de un mes de alquiler a cargo del inquilino, lo que se cobre por el gravamen de la Ordenanza 21 y lo que asigne el Departamento Ejecutivo de la contribución por valorización de la Ordenanza 13. El fondo no recibe otros recursos del Municipio.'),
 ('Artículo 3 — Límite', 'El alquiler garantizado no supera el cuarenta por ciento (40%) del ingreso del inquilino o del grupo que alquila. El ingreso sin recibo se declara bajo juramento ante la inteligencia artificial del Municipio, y lo aprueba un agente municipal. A quien cobra del Municipio, el alquiler se le descuenta del sueldo, con su conformidad.'),
 ('Artículo 4 — Freno', 'Si el fondo baja del piso que fija la reglamentación, no se otorgan garantías nuevas hasta que se recupere. El estado del fondo se consulta en el Sistema de Información Municipal.'),
 ('Artículo 5 — Recupero', 'Cuando el fondo le paga al propietario por un inquilino, el Municipio le reclama al inquilino lo pagado.')])

anexo('anexo-21', '21 · Ordenanza de las viviendas en el lote y de los terrenos sin uso', [
 ('Artículo 1 — Segunda y tercera vivienda', 'En toda parcela con destino residencial se admiten una segunda y una tercera unidad de vivienda, dentro de la ocupación y la altura que fija el Código de Ordenamiento Urbano para esa parcela. La reglamentación fija la superficie mínima de cada unidad y su conexión a los servicios.'),
 ('Artículo 2 — Alquilar una parte de la casa', 'Alquilar una habitación o una parte de la vivienda, por plazo largo o temporario, no requiere habilitación municipal ni cambia la tasa del inmueble. Quien hoy alquila sin registrar se puede regularizar sin multa.'),
 ('Artículo 3 — Edificación obligatoria', 'Conforme a los artículos 84 a 88 del Decreto-Ley 8912/77, según la Ley 14.449, se declara la edificación obligatoria de los terrenos baldíos, de los inmuebles declarados inhabitables y de las obras paralizadas hace más de cinco (5) años. El propietario tiene tres (3) años desde la notificación para empezar la obra, y un (1) año como máximo desde la aprobación del proyecto. El plazo para terminarla lo calcula la inteligencia artificial del Municipio según la superficie, con la regla que publica la reglamentación. Los plazos no cambian aunque el inmueble se venda, y la obligación se hace constar en la escritura.'),
 ('Artículo 4 — Gravamen y expropiación', 'Vencido el plazo, se aplica el gravamen especial progresivo del artículo 86 del Decreto-Ley 8912/77: sube cada año durante cinco (5) años hasta el cincuenta por ciento (50%) de la tasa de alumbrado, barrido y limpieza, sin exenciones. Lo recaudado va al fondo de la Ordenanza 20. Cumplidos cinco años de gravamen, el inmueble queda sujeto a expropiación (artículo 87).')])

rep('anexo', 'y diecisiete cortas.', 'y veinte cortas.')
rep('anexo', ' Faltan dos cambios menores, que se redactan en los meses 4 a 6 (cuadro 42): la ordenanza de los foodtrucks y el cambio del artículo 9 de la Ordenanza 5824.', '')

# ---------- Lo que tiene que ver un abogado ----------
for t in [
 '• 4.11. Pagarles a vecinos y a empleados del Municipio una parte de lo que su aviso hace cobrar o ahorrar: la base legal, cómo se paga y cómo se declara.',
 '• 4.11. Presentar con firma digital, sin ir en persona, la denuncia que deja lista la inteligencia artificial del Municipio, en las fiscalías de San Isidro.',
 '• 4.11. Mostrarle a cada vecino historias según lo que usa, con aviso y botón para apagarlo, sin un permiso aparte (Ley 25.326, artículo 5).',
 '• 5.4. El descuento del alquiler garantizado del sueldo de quien cobra del Municipio, y el fondo de la garantía (Ordenanza 20 del anexo).',
 '• 5.4. La edificación obligatoria y la segunda y tercera vivienda en el lote (Ordenanza 21 del anexo; Ley 14.449).',
 '• 5.6. Que la inteligencia artificial del Municipio acompañe a un vecino en salud mental bajo un profesional responsable, y el resumen que le pasa al acompañante.']:
    agregar_parrafo('metodo-abogado', t)

P.write_text(json.dumps(d, ensure_ascii=False, indent=1))

# ---------- controles ----------
nuevos = ['5.4-r1', '5.4-r2', '5.4-r3', '4.11-r4', '4.11-r5', '4.11-r6', '5.6-r5', '5.9-r3', '5.9-r1', 'anexo-19', 'anexo-20', 'anexo-21']
prohib = re.compile(r'\b(plata|mafia|sobreprecio|candidat\w*|ángel de la guarda)\b', re.I)
bad = 0
for i in nuevos:
    for p in by[i]['texto'].split('\n\n'):
        if prohib.search(p): bad += 1; print('PALABRA', i, prohib.search(p).group(0))
        body = re.sub(r'^\d+ · ', '', p)
        s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', body) if x]
        f = [x.split()[0].lower().strip('«') for x in s]
        if any(f.count(w) > 1 for w in f) or any(re.match(r'^(Y|Que)\b', x) for x in s): bad += 1; print('FALLA', i, p[:70], f)
print('fallas:', bad)
for e in d:
    for k, ms in e.get('marcas', {}).items():
        ps = e['texto'].split('\n\n')
        for a, z, _ in ms: assert 0 <= a < z <= len(ps[int(k)]), (e['id'], k)
