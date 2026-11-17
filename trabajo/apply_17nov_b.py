"""Actualización del 17/11/2026, parte B: los 30 huecos del plan de despliegue (REVISION.md §5) y las decisiones
de Nick del 16/11 sobre la rampa, los cien días, la obra del año 1, la inteligencia artificial antes de la primera
licitación y las denuncias antes de la auditoría externa; filas nuevas del calendario para vivienda y salud mental."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}

def rep(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]; assert len(hits) == 1, (eid, old[:50], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)

def cuadro(eid, old, new, ci=0):
    c = by[eid]['cuadros'][ci]; assert c['texto'].count(old) == 1, (eid, old[:60], c['texto'].count(old))
    c['texto'] = c['texto'].replace(old, new, 1)

def fila_despues(eid, ancla, fila, ci=0):
    c = by[eid]['cuadros'][ci]; rs = c['texto'].split('\n')
    k = [i for i, r in enumerate(rs) if r.startswith(ancla)]; assert len(k) == 1, (ancla, k)
    rs.insert(k[0] + 1, fila); c['texto'] = '\n'.join(rs)

def agregar_parrafo(eid, texto, marca_hasta=None):
    e = by[eid]; ps = e['texto'].split('\n\n'); ps.append(texto); e['texto'] = '\n\n'.join(ps)
    k = len(ps) - 1
    if 'orden' in e: e['orden'].append(['p', k])
    if marca_hasta: e.setdefault('marcas', {})[str(k)] = [[0, marca_hasta, 'b']]

# Arreglos de la parte A (dos párrafos con oraciones que empezaban igual)
rep('anexo-20', 'El ingreso sin recibo se declara bajo juramento', 'Si el ingreso no tiene recibo, se declara bajo juramento')
rep('anexo-21', 'El plazo para terminarla lo calcula la inteligencia artificial del Municipio', 'Para terminarla, el plazo lo calcula la inteligencia artificial del Municipio')

CAL = '6.4'
# 1 · El año de la rampa es el ejercicio
cuadro(CAL, 'Mes 12 | Año 1 de la rampa, cumplido (cuadro 21) | Ejecución presupuestaria del ejercicio',
       'Mes 12 | Termina el año 1 de la rampa (cuadro 21). Cada escalón se cuenta por ejercicio, que cierra el 31 de diciembre | Ejecución presupuestaria del ejercicio')
cuadro(CAL, 'Mes 24 | Se cumple el año 2 de la rampa (cuadro 21).', 'Mes 24 | Termina el año 2 de la rampa (cuadro 21).')
cuadro(CAL, 'Mes 36 | Año 3 de la rampa (cuadro 21).', 'Mes 36 | Termina el año 3 de la rampa (cuadro 21).')
# 2 y 3 · Cómo se comprueba cada escalón (Nick, 16/11: opción A)
rep('6.2', 'no les tiene que hacer objeciones.', 'no les tiene que hacer objeciones. Como el Tribunal se pronuncia más de un año después, cada escalón se comprueba antes con la auditoría externa (cuadro 28).')
agregar_parrafo('6.2', 'Cómo se comprueba cada escalón a tiempo. El presupuesto de cada año se vota antes de que cierre el anterior. Por eso, el presupuesto incluye el escalón siguiente, pero ese dinero se libera recién cuando la auditoría externa certifica que el anterior se cumplió, hacia marzo. Si después el Tribunal de Cuentas objeta un año, se congela el escalón que sigue. Como las obras se eligen en marzo, esa espera casi no las demora.', 40)
agregar_parrafo('6.2', 'Las fechas del presupuesto. Cada año, el intendente presenta el presupuesto al Concejo antes del 31 de octubre (Ley Orgánica de las Municipalidades, artículo 109), y el Concejo lo vota. El de 2028 lo presenta el gobierno que termina, y la partida del año 1 se crea con el artículo 119 de la misma ley (4.9).', 27)
rep('anexo-1', 'La progresión no avanzará al escalón siguiente si el inmediato anterior no fue ejecutado y justificado en su totalidad.',
    'La progresión no avanzará al escalón siguiente si el inmediato anterior no fue ejecutado y justificado en su totalidad. El crédito del escalón siguiente se incluye en el presupuesto, y se libera cuando la auditoría externa certifica que el anterior se cumplió. Si el Honorable Tribunal de Cuentas formula observaciones sobre un ejercicio, no se libera el escalón que sigue hasta que se resuelvan.')
# 4 · Los dos «primeros»
cuadro('6.6', 'la ordenanza preparatoria va a ir primera en la convocatoria de diciembre', 'la ordenanza preparatoria va a ir primera en el orden del día de la sesión de diciembre')
# 5 y 10/11 · La primera ronda ya se hizo a los cien días y elige las obras del año (Nick, 16/11: opción A)
rep('6.1', 'Para esa fecha, cualquier vecino de San Isidro va a estar convocado a la primera asamblea de su zona.',
    'Para esa fecha, la primera asamblea de cada zona ya se va a haber hecho, y los vecinos ya van a haber elegido las obras del primer año.')
by['6.1']['marcas'].pop('2', None)
rep('6.1', 'La primera ronda de asambleas va a servir para informar. Las obras se eligen en la segunda. Así empezaba cada ciclo del presupuesto participativo de la Ciudad de Buenos Aires, según su reglamento de mayo de 2004. En la Ciudad, primero había una reunión en cada barrio, para informar a los vecinos y completar el diagnóstico de lo que hacía falta. Al final, dos meses después, se votaban las prioridades. Con nuestra propuesta, la segunda ronda, en la que se eligen las obras, va a ser entre los meses 6 y 9 (6.4).',
    'En la primera ronda de asambleas, los vecinos se van a informar y van a elegir las obras del año. Así, cada obra tiene tiempo de licitarse y terminarse dentro del mismo año, que es lo que pide la rampa para subir. La segunda ronda, entre los meses 6 y 9, sigue las obras en marcha y prepara las del año siguiente (6.4). El primer año, como las comisiones todavía se están formando, las obras elegidas las hace el Ejecutivo.')
by['6.1']['marcas']['2'] = [[0, len('En la primera ronda de asambleas, los vecinos se van a informar y van a elegir las obras del año.'), 'b']]
rep('proponemos', 'todos los vecinos ya van a estar convocados a la primera asamblea de su zona.', 'la primera asamblea de cada zona ya se va a haber hecho.')
rep('cierre-r1', 'la primera asamblea de cada zona ya va a estar convocada.', 'la primera asamblea de cada zona ya se va a haber hecho.')
cuadro('6.1', '11 · La primera ronda de asambleas, en las seis zonas. Va a servir para informar a los vecinos y para anotar qué necesita cada zona',
       '11 · La primera ronda de asambleas, en las seis zonas. Va a servir para informar a los vecinos y para elegir las obras del primer año, que hace el Ejecutivo')
cuadro(CAL, 'Mes 3 | Primera ronda de asambleas en las seis zonas.', 'Mes 3 | Primera ronda de asambleas en las seis zonas: los vecinos eligen las obras del año 1, que hace el Ejecutivo. También se cuentan los baldíos, las ruinas y las obras paradas de cada zona (5.4).')
cuadro(CAL, 'Meses 6–9 | Segunda ronda de asambleas, en la que los vecinos ya eligen las obras. El Ejecutivo responde por escrito a cada decisión, con sus razones y dentro del plazo fijado',
       'Meses 6–9 | Segunda ronda de asambleas: los vecinos siguen las obras del año y preparan las del año siguiente. El Ejecutivo responde por escrito a cada pedido, con sus razones y dentro del plazo fijado')
# 29 · Las asambleas de los años 2 a 4
fila_despues(CAL, 'Mes 12 | Termina el año 1 de la rampa', 'Cada año | Las dos rondas de asambleas se repiten en los mismos meses: en el mes 3 de cada año se eligen las obras de ese año, y entre los meses 6 y 9 se siguen y se preparan las del año siguiente | Actas y asistentes: se le preguntan a la inteligencia artificial del Municipio')
# 6 · Compromisos 4 y 5: la promesa queda, con la aclaración (Nick, 16/11)
cuadro('6.1', 'tener su espacio propio en la inteligencia artificial del Municipio desde los meses 6 a 9 (6.4) | Ordenanza;',
       'tener su espacio propio en la inteligencia artificial del Municipio desde los meses 6 a 9 (6.4). Depende de que el Concejo apruebe la ordenanza antes de los cien días | Ordenanza;')
cuadro('6.1', '5 · La adhesión a la Ley provincial 15.302 de espacios culturales | Ordenanza de adhesión',
       '5 · La adhesión a la Ley provincial 15.302 de espacios culturales. Depende de que el Concejo la apruebe antes de los cien días | Ordenanza de adhesión')
# 7 y 8 · Centros de apoyo escolar
cuadro(CAL, 'Mes 25 | Los seis centros de apoyo escolar abiertos, uno por localidad: abren de a dos por año, los dos primeros en el año 1',
       'Mes 25 | Al empezar el año 3 abren el quinto y el sexto centro de apoyo escolar, y quedan los seis abiertos, uno por localidad. Abren de a dos por año, los dos primeros en el año 1')
fila_despues(CAL, 'Meses 4–6 | Donde ya hay una asociación vecinal', 'Mes 6 | Abre el segundo centro de apoyo escolar, antes de que empiece la prueba del profesor digital | La matrícula por sede se le pregunta a la inteligencia artificial del Municipio')
# 9 · El panel
cuadro(CAL, 'Meses 7–12 | Apenas el Concejo aprueba la Ordenanza 12, se sortea', 'Meses 7–12 | Una vez aprobada la Ordenanza 12, se sortea')
# 12 · El título de la tecnicatura
cuadro(CAL, 'Para entonces, el Ministerio de Educación ya reconoció la tecnicatura, y el título vale en todo el país.',
       'Si para entonces el Ministerio de Educación todavía no reconoció el título, el grupo hace igual su práctica, con una beca municipal (6.6).')
# 14 · La inteligencia artificial antes de la primera licitación (Nick, 16/11: opción A)
cuadro(CAL, 'la que recibe lo que plantean los vecinos y sigue cada caso | Actas, matrícula',
       'la que recibe lo que plantean los vecinos y sigue cada caso. Mientras corre la primera licitación, su uso se paga con las compras chicas que la ley permite hacer sin licitación pública (Ley Orgánica de las Municipalidades, artículo 151) | Actas, matrícula')
# 15 · Denuncias antes de la auditoría externa y del certificado
rep('anexo-4', 'Quien denuncie en falso recibe una sanción.', 'Quien denuncie en falso recibe una sanción. Hasta que se contrata la auditoría externa, la denuncia se remite a la Comisión y, si hay delito, a la fiscalía; al empezar, la auditoría recibe todas las anteriores.')
cuadro(CAL, 'Con él se sellan las grabaciones de las inspecciones y las que hacen los vecinos para denunciar (5.5 y 5.9) | El expediente del pedido',
       'Con él se sellan las grabaciones de las inspecciones y las que hacen los vecinos para denunciar (5.5 y 5.9). Mientras llega, cada grabación se guarda con su fecha, su hora y su huella, que muestra si alguien la cambió | El expediente del pedido')
# 17 · Recolección y empleo local
agregar_parrafo('anexo-9', 'Artículo 4 — Empleo local')
agregar_parrafo('anexo-9', 'El pliego exige subcontratar al menos el veinte por ciento (20%) del servicio con pymes con domicilio en el Partido de San Isidro y, dentro de esa parte, el cinco por ciento (5%) del valor total con empresas de San Isidro de menos de cinco (5) años, conforme a la Ordenanza 10. Desde que existen empresas del semillero, las subcontrataciones nuevas les dan prioridad.')
if 'orden' in by['anexo-9']:
    o = by['anexo-9']['orden']; o[-2] = ['h3', o[-2][1]]
# 18 · Foodtrucks y Ordenanza 5824 (Ordenanza 19 del anexo)
cuadro(CAL, 'Meses 4–6 | Se presentan dos ordenanzas más. Una regula los foodtrucks: fija el canon, que es lo que cada uno le paga por mes al Municipio, y exige que el 75% del empleo sea local. La otra cambia el artículo 9 de la Ordenanza 5824',
       'Meses 4–6 | Se presentan tres ordenanzas más. La 19 del anexo regula los foodtrucks: fija el canon, que es lo que cada uno le paga por mes al Municipio, y exige que el 75% del empleo sea local. También cambia el artículo 9 de la Ordenanza 5824')
cuadro(CAL, 'que hoy sólo permite vender bebidas en kioscos en el Bosque Alegre (5.5) | Expedientes y Boletín Oficial Municipal',
       'que hoy sólo permite vender bebidas en kioscos en el Bosque Alegre (5.5). La 20 crea la garantía de alquiler del Municipio, y la 21 permite una segunda y una tercera vivienda en el lote y obliga a construir en los terrenos sin uso (5.4) | Expedientes y Boletín Oficial Municipal')
rep('metodo-abogado', 'El cambio del artículo 9 de la Ordenanza 5824, para el lugar del Bosque Alegre.', 'El cambio del artículo 9 de la Ordenanza 5824, para el lugar del Bosque Alegre (Ordenanza 19 del anexo).')
# 19 · Espectáculos todas las semanas
cuadro('6.3', 'Además, espectáculos al aire libre todas las semanas, de lunes a jueves, en los parques y plazas de San Isidro',
       'Además, espectáculos todas las semanas, de lunes a jueves: al aire libre en los parques y plazas de San Isidro de septiembre a abril, y bajo techo el resto del año')
# 20 · Sonido de la prueba
rep('5.5-r12', 'Un equipo de producción del Municipio les va a llevar y armar el sonido, los micrófonos y un escenario chico, y los va a ayudar durante el show.',
    'Un equipo de producción del Municipio les va a llevar y armar el sonido, los micrófonos y un escenario chico, y los va a ayudar durante el show. Durante la prueba de los primeros meses, se usa el sonido que ya tiene el Municipio, o se alquila.')
# 21 · Tramo de arena
rep('5.5-r3', 'para que funcionen desde el primer verano.', 'para que funcionen desde el primer verano, el de 2028 a 2029.')
cuadro(CAL, 'Además, se arma el primer tramo de prueba con arena, con sus guardavidas | Gastos por finalidad y función',
       'Además, se arma el primer tramo de prueba con arena, con sus guardavidas, después del estudio de impacto ambiental de la Ordenanza 12, de la recomendación del panel y de su licitación, para el verano de 2028 a 2029 | Gastos por finalidad y función')
# 22 · Escuela Náutica y Ordenanza 11
cuadro(CAL, 'Antes se mide el agua, y dan su opinión la asociación del parque y el panel.',
       'Abren una vez aprobada la Ordenanza 11, que fija la calidad del agua para las clases. Antes se mide el agua, y dan su opinión la asociación del parque y el panel.')
# 26 · Fecha de aprobación de cada ordenanza
cuadro(CAL, 'Nota: la comisión se forma en los meses 4 a 6', 'Nota: las fechas de este cuadro son las de entrada de cada ordenanza; cuándo se aprueba cada una lo decide el Concejo. La comisión se forma en los meses 4 a 6')
# 30 · Los grupos 3 y 4 de la formación
cuadro(CAL, 'El segundo grupo de alumnos entra en el mes 9.', 'El segundo grupo de alumnos entra en el mes 9. La inscripción se abre cada seis meses: el tercer grupo entra en el mes 15, y el cuarto, en el mes 21.')
# 27 y 28 · Plazos de otros y cosas sin fecha (cuadro 43)
c43 = by['6.5']['cuadros'][0]
c43['texto'] += '\n' + '\n'.join([
 'Una fecha para cada respuesta de otro organismo | No tienen plazo: la respuesta de AySA sobre cada baño de la costa, el certificado de firma digital de la Nación, la validez nacional del título, la autorización de la Provincia para cada cámara de multas, sus datos de delitos por zona, los lugares en su red de hogares y la revisión del Tribunal de Cuentas. Para cada una hay un plan mientras tanto: la grabación con su huella, la beca municipal, la auditoría externa (6.2, 6.4 y 6.6).',
 'Una fecha para lo que depende de otra cosa | La patrulla que graba llega en una segunda etapa, después de las inspecciones. El fin del cobro por multa llega cuando vence cada contrato actual. La partida propia de género entra en el presupuesto siguiente a su ordenanza. La conexión de cada casa se paga a medida que la obra vecinal hace las redes de la calle. La transmisión de las asambleas empieza con la inteligencia artificial del Municipio.'])

# Calendario: vivienda y salud mental
fila_despues(CAL, 'Meses 7–12 | Profesor digital', 'Meses 7–12 | Vivienda: una vez aprobada la Ordenanza 20, el Municipio empieza a dar la garantía de alquiler con su fondo propio. Una vez aprobada la 21, se notifica a los dueños de los terrenos sin uso contados en la primera ronda, y desde ahí corren sus tres años (5.4) | Cuántas garantías hay y el estado del fondo: se le pregunta a la inteligencia artificial del Municipio')
fila_despues(CAL, 'Meses 7–12 | Vivienda:', 'Meses 7–12 | Salud mental: empieza la formación de los primeros acompañantes terapéuticos, entre empleados cuyo trabajo ya hace la inteligencia artificial del Municipio (5.6) | Cuántos se forman y cuántos vecinos acompañan: se le pregunta a la inteligencia artificial del Municipio')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1))

# ---------- controles ----------
prohib = re.compile(r'\b(plata|mafia|sobreprecio|candidat\w*|ángel de la guarda)\b', re.I)
ids = ['6.1', '6.2', 'anexo-1', 'anexo-4', 'anexo-9', 'anexo-20', 'anexo-21', 'proponemos', 'cierre-r1', '5.5-r12', '5.5-r3']
bad = 0
for i in ids:
    for p in by[i]['texto'].split('\n\n'):
        if prohib.search(p): bad += 1; print('PALABRA', i)
        body = re.sub(r'^\d+ · ', '', p)
        s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', body) if x]
        f = [x.split()[0].lower() for x in s]
        if any(f.count(w) > 1 for w in f) or any(re.match(r'^(Y|Que)\b', x) for x in s): bad += 1; print('FALLA', i, p[:80], f)
for i in ['6.1', '6.3', '6.4', '6.5', '6.6']:
    for r in by[i]['cuadros'][0]['texto'].split('\n'):
        for cel in r.split(' | '):
            if prohib.search(cel): bad += 1; print('PALABRA cuadro', i)
            s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', re.sub(r'^\d+ · ', '', cel)) if x]
            f = [x.split()[0].lower() for x in s if x.split()]
            if any(f.count(w) > 1 for w in f) or any(re.match(r'^(Y|Que)\b', x) for x in s): print('aviso cuadro', i, cel[:70], f)
print('fallas:', bad)
for e in d:
    for k, ms in e.get('marcas', {}).items():
        ps = e['texto'].split('\n\n')
        for a, z, _ in ms: assert 0 <= a < z <= len(ps[int(k)]), (e['id'], k)
