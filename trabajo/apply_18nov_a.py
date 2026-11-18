"""Actualización del 18/11/2026, parte A: las decisiones de Nick sobre la revisión completa (DECISIONES_NOVIEMBRE.md,
«Decisiones de la revisión completa (18/11/2026)»): 1, 3, 4, 5, 5b, 6, 6b, 7, 8, 9, 11 y Seguridad, más la nota del
gráfico 13 de la decisión 10 (sólo texto). Las cifras que calcula otro encargado quedan marcadas ⟦NUM:nombre⟧.
Fuentes abiertas el 18/11/2026: normas.gba.gob.ar (Decreto-Ley 8912/77, Ley 13.406), Ordenanza Impositiva 2026 de
Bahía Blanca, argentina.gob.ar/sid (RENAPER) y el relevamiento de seguridad del mismo día (sanisidro.gob.ar y leyes).
Re-ejecutable sólo una vez: si ya se aplicó, se detiene sin tocar nada.
Uso: python3 trabajo/apply_18nov_a.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if 'Registro Nacional de las Personas' in by['4.6']['texto']:
    raise SystemExit('ya aplicado: no se toca nada')


def _ps(e): return e['texto'].split('\n\n')


def rep(eid, old, new, dentro=False):
    """Cambia old por new en el único párrafo que lo tiene. Corre las marcas que siguen; si el cambio toca una marca,
    se niega, salvo con dentro=True y el cambio entero adentro de esa marca (entonces se corre sólo su final)."""
    e = by[eid]; ps = _ps(e)
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta:
            if dentro and m[0] <= pos and end <= m[1]: m[1] += delta
            else: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


def rep_span(eid, old, new, negritas=()):
    """Como rep, pero el cambio puede pisar marcas: las que toca se borran y se ponen las de negritas, dadas como
    (inicio, fin) relativos al principio de new."""
    e = by[eid]; ps = _ps(e)
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    ms = []
    for m in e.get('marcas', {}).get(str(i), []):
        if m[1] <= pos: ms.append(m)
        elif m[0] >= end: ms.append([m[0] + delta, m[1] + delta, m[2]])
    ms += [[pos + a, pos + b, 'b'] for a, b in negritas]
    if ms or str(i) in e.get('marcas', {}): e.setdefault('marcas', {})[str(i)] = sorted(ms)
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


def ins(eid, ancla, texto):
    """Inserta texto justo después de ancla; corre las marcas que empiezan después."""
    e = by[eid]; ps = _ps(e); hits = [i for i, p in enumerate(ps) if p.count(ancla) == 1]
    assert len(hits) == 1 and sum(p.count(ancla) for p in ps) == 1, (eid, ancla[:60])
    i = hits[0]; k = ps[i].index(ancla) + len(ancla)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= k: m[0] += len(texto); m[1] += len(texto)
        elif m[1] > k: raise SystemExit(f'marca {eid} p{i} {m}')
    ps[i] = ps[i][:k] + texto + ps[i][k:]; e['texto'] = '\n\n'.join(ps)


def nuevos(eid, ancla, textos, negrita=None):
    """Agrega párrafos después del único párrafo que tiene ancla; corre las claves de las marcas de los que siguen.
    negrita: para cada párrafo nuevo, cuántos caracteres del principio van en negrita (o None), o una lista de marcas."""
    e = by[eid]; ps = _ps(e); hits = [i for i, p in enumerate(ps) if ancla in p]; assert len(hits) == 1, (eid, ancla[:60])
    i = hits[0]; n = len(textos); mk = e.get('marcas', {})
    mk = {str(int(k) + n if int(k) > i else int(k)): v for k, v in mk.items()}
    for j, b in enumerate(negrita or []):
        if b: mk[str(i + 1 + j)] = [[0, b, 'b']] if isinstance(b, int) else b
    if mk: e['marcas'] = mk
    e['texto'] = '\n\n'.join(ps[:i + 1] + textos + ps[i + 1:])


def reemplazar_parrafos(eid, desde, viejos_inicio, textos, negrita):
    """Reemplaza los párrafos desde «desde» hasta el final del apartado; comprueba que empiecen como se espera."""
    e = by[eid]; ps = _ps(e)
    assert [p[:len(v)] for p, v in zip(ps[desde:], viejos_inicio)] == list(viejos_inicio) and len(ps) - desde == len(viejos_inicio), eid
    mk = {k: v for k, v in e.get('marcas', {}).items() if int(k) < desde}
    for j, b in enumerate(negrita):
        if b: mk[str(desde + j)] = [[0, b, 'b']]
    e['marcas'] = mk; e['texto'] = '\n\n'.join(ps[:desde] + textos)


def cuadro(eid, old, new, campo='texto'):
    cs = by[eid]['cuadros']; idx = [k for k, c in enumerate(cs) if old in c[campo]]
    assert len(idx) == 1 and cs[idx[0]][campo].count(old) == 1, (eid, old[:60], idx)
    cs[idx[0]][campo] = cs[idx[0]][campo].replace(old, new, 1)


def cuadro_mover(eid, empieza, ancla, nueva):
    """Saca la fila que empieza con «empieza» y pone «nueva» después de la fila que empieza con «ancla»."""
    c = by[eid]['cuadros'][0]; ls = c['texto'].split('\n')
    a = [k for k, l in enumerate(ls) if l.startswith(empieza)]; assert len(a) == 1, (eid, empieza)
    ls.pop(a[0])
    b = [k for k, l in enumerate(ls) if l.startswith(ancla)]; assert len(b) == 1, (eid, ancla)
    ls.insert(b[0] + 1, nueva); c['texto'] = '\n'.join(ls)


def fuente(eid, old, new):
    e = by[eid]; assert e['fuentes'].count(old) == 1, (eid, old[:60]); e['fuentes'] = e['fuentes'].replace(old, new, 1)


def fuente_mas(eid, texto):
    e = by[eid]; e['fuentes'] = (e['fuentes'] + '\n\n' + texto) if e.get('fuentes') else texto


def titulo_parrafo(eid, old, new):
    """Cambia un párrafo entero que es un título de artículo (sin marcas)."""
    e = by[eid]; ps = _ps(e); i = [k for k, p in enumerate(ps) if p == old]; assert len(i) == 1, (eid, old)
    assert str(i[0]) not in e.get('marcas', {}); ps[i[0]] = new; e['texto'] = '\n\n'.join(ps)


HOY = 'consultado el 18 de noviembre de 2026'

# ============ 1 · La primera ronda (mes 3) se vota con la inteligencia artificial del Municipio =====================
nuevos('4.6', 'Si en una zona hay más de una asociación, van a actuar como una sola comisión', [
    'El primer año es distinto, porque las obras se eligen en la primera ronda de asambleas, en el mes 3, antes de que'
    ' se reconozca a cada comisión. Esa ronda la convoca el Municipio en cada zona, abierta y con las mismas reglas de'
    ' voto, y las obras que elige las hace el Ejecutivo (6.1). Si la votación por celular no está lista a tiempo, esa'
    ' ronda se vota sólo en las tablets de la asamblea. Desde el año 2, convoca la comisión de cada zona.'])
ins('4.6', 'Se va a votar en una asamblea abierta o por internet, con la identidad verificada.',
    ' La votación es una parte de la inteligencia artificial del Municipio desde la primera ronda, en el mes 3: se vota'
    ' con el celular, y la identidad se comprueba con el Registro Nacional de las Personas (RENAPER), que confirma el DNI'
    ' y la foto de la cara. El Municipio firma con el RENAPER el convenio que lo permite. Quien no tenga celular, o'
    ' prefiera votar con ayuda, vota en una tablet con personal del Municipio, en la asamblea o en la delegación'
    ' municipal de su zona.')
fuente_mas('4.6', '4.6 · la identidad con el RENAPER: Registro Nacional de las Personas, Sistema de Identidad Digital,'
           ' «Organizaciones»: servicio de validación de datos del DNI y servicio de validación por fotografía de rostro;'
           ' la entidad «deberá tramitar el Convenio Único de Confronte de Datos con el Renaper a través TAD» (Trámites a'
           ' Distancia), y el RENAPER dictamina si hay interés legítimo. https://www.argentina.gob.ar/sid/modalidades-y-productos,'
           f' {HOY}.')
cuadro('4.5', '1. Los vecinos votan en la asamblea de la asociación vecinal de su zona en qué se usa ese dinero.',
       '1. Los vecinos votan en la asamblea abierta de su zona en qué se usa ese dinero. El primer año la convoca el Municipio.')
rep('4.13', 'Los vecinos eligen las obras en la asamblea de su asociación vecinal,',
    'Los vecinos eligen las obras en la asamblea abierta de su zona,')
ins('4.11', 'La primera es la votación de la partida vecinal y el orden de las obras.',
    ' Funciona desde la primera ronda de asambleas, en el mes 3 (4.6).')
rep('proponemos', 'ya se le podrá preguntar, sacar un turno médico y hacerle llegar un reclamo.',
    'ya se le podrá preguntar, sacar un turno médico, hacerle llegar un reclamo y votar las obras de la primera ronda.')
rep('6.1', 'El primer año, como las comisiones todavía se están formando, las obras elegidas las hace el Ejecutivo.',
    'El primer año, como las comisiones todavía se están formando, la ronda la convoca el Municipio y las obras elegidas'
    ' las hace el Ejecutivo. Desde el año 2, la convoca la comisión de cada zona.')
cuadro('6.1', '11 · La primera ronda de asambleas, en las seis zonas. Va a servir',
       '11 · La primera ronda de asambleas, en las seis zonas, convocada por el Municipio. Se vota con el celular, con la'
       ' identidad verificada, o en las tablets de cada asamblea (4.6). Va a servir')
cuadro('6.1', '14 · Tres partes de la inteligencia artificial del Municipio van a estar funcionando.',
       '14 · Cuatro partes de la inteligencia artificial del Municipio van a estar funcionando.')
cuadro('6.1', 'La tercera escucha a los vecinos, sigue cada caso y les responde (4.11) |',
       'La tercera escucha a los vecinos, sigue cada caso y les responde (4.11). Con la cuarta se votan las obras de la'
       ' primera ronda (4.6) |')
cuadro('6.4', 'Mes 3 | Primera ronda de asambleas en las seis zonas: los vecinos eligen las obras del año 1, que hace el Ejecutivo.',
       'Mes 3 | Primera ronda de asambleas en las seis zonas, convocada por el Municipio: los vecinos eligen las obras del'
       ' año 1, que hace el Ejecutivo, y votan con el celular o en las tablets de cada asamblea y de la delegación (4.6).')
cuadro('6.4', 'empiezan a funcionar tres partes: la que responde consultas, la que saca el turno médico mientras uno conversa'
       ' y la que recibe lo que plantean los vecinos y sigue cada caso.',
       'empiezan a funcionar cuatro partes: la que responde consultas, la que saca el turno médico mientras uno conversa,'
       ' la que recibe lo que plantean los vecinos y sigue cada caso, y la votación de la partida vecinal.')
cuadro('6.4', 'suma tres partes a las que ya funcionan desde el mes 3: la partida vecinal,',
       'suma tres partes a las que ya funcionan desde el mes 3: el resto de la partida vecinal,')
cuadro('6.6', 'Primero, en el mes 3, la consulta, el turno médico y la parte que recibe lo que plantean los vecinos. Después,'
       ' en los meses 6 a 9, la partida vecinal, el seguimiento de obra y el espacio de las asociaciones. Así, el primer'
       ' ciclo de asambleas no depende de que esté completa.',
       'Primero, en el mes 3, la consulta, el turno médico, la parte que recibe lo que plantean los vecinos y la votación'
       ' de la partida vecinal. Después, en los meses 6 a 9, el resto de la partida vecinal, el seguimiento de obra y el'
       ' espacio de las asociaciones. Si la votación no está lista en el mes 3, esa ronda se vota sólo en las tablets de'
       ' la asamblea, con personal del Municipio.')
cuadro('6.6', 'El voto digital, con identidad verificada, se suma para quien no puede ir, y no reemplaza a la asamblea.',
       'El voto digital, con identidad verificada, se suma para quien no puede ir, y no reemplaza a la asamblea. En cada'
       ' asamblea y en la delegación de la zona hay tablets con personal del Municipio, para votar con ayuda (4.6).')
# Ordenanza 1: la identidad, las tablets y el primer ejercicio
ins('anexo-1', 'Se vota en la asamblea o en forma digital, con identidad verificada, en el Sistema de Información Municipal,'
    ' y nadie vota dos veces.',
    ' Los datos de identidad se verifican con el Registro Nacional de las Personas. En cada asamblea y en la delegación'
    ' municipal de la zona, el Departamento Ejecutivo pone a disposición dispositivos y personal para votar en forma digital.')
e = by['anexo-1']; assert _ps(e)[-2] == 'Artículo 13 — Comisión zonal y alcance'
e['texto'] += ('\n\nArtículo 14 — Primer ejercicio\n\nEn el primer ejercicio, mientras se forman las comisiones, el'
               ' Departamento Ejecutivo convoca en cada zona la asamblea abierta del artículo 3, que prioriza las obras de'
               ' ese año, y las ejecuta en esa misma zona. Si el voto digital no está disponible para esa asamblea, se vota'
               ' en ella, en los dispositivos del artículo 3. Desde el segundo ejercicio, convoca la comisión zonal.')
nuevos('metodo-abogado', '• 3.6. El fallo de la Corte Suprema', [
    '• 4.6. Votar con la identidad verificada contra el Registro Nacional de las Personas: el convenio del Municipio con'
    ' el RENAPER, que decide si hay interés legítimo, y el uso de esos datos sólo para votar (Ley 25.326).'], [[[2, 6, 'b']]])

# ============ 3 · La auditoría externa, en dos contratos ============================================================
cuadro('4.11', 'Auditoría externa |  |  |  |  | 135,4 M', 'Auditoría externa de la plataforma |  |  |  |  | 135,4 M')
nuevos('4.11', 'Nada se cuenta dos veces. Estos 2.000,7 millones', [
    'La auditoría externa del cuadro 28 revisa la plataforma. Certificar cada escalón de la partida vecinal (6.2), y'
    ' recibir las denuncias sobre esa obra, es otro trabajo, con otro contrato. Ese contrato cuesta'
    ' ⟦NUM:certificacion_por_año⟧ por año y se paga con lo que sobra del 1,5% de funcionamiento de la partida (4.6). Si no'
    ' alcanza, lo que falta sale del gasto flexible (3.4).'])
rep('6.2', 'cada escalón se comprueba antes con la auditoría externa (cuadro 28).',
    'cada escalón se comprueba antes con una auditoría externa de la obra (4.11).')
rep('6.2', 'ese dinero se libera recién cuando la auditoría externa certifica',
    'ese dinero se libera recién cuando la auditoría externa de la obra certifica')
cuadro('6.4', 'y la auditoría externa lo certifica hacia marzo (6.2)', 'y la auditoría externa de la obra lo certifica hacia marzo (6.2)')
ins('4.6', 'Al cuarto año son 433,6 millones.',
    ' Lo que sobra paga la auditoría externa que certifica cada escalón de la obra (4.11).')
ins('metodo-notas-4', 'Así, el 1,5% alcanza en los dos casos.',
    ' Lo que sobra del 1,5% paga la auditoría externa que certifica cada escalón (4.11): ⟦NUM:certificacion_por_año⟧ por'
    ' año. Cuando no alcanza, lo que falta sale del gasto flexible.')
rep('metodo-notas-4', 'El costo de la auditoría externa es el 10%', 'El costo de la auditoría externa de la plataforma es el 10%')
ins('anexo-1', 'y la administración de las obras que ejecute la asociación vecinal, comprendidos sus registros contables,'
    ' seguros y la justificación del gasto.',
    ' El remanente se aplica a la auditoría externa que certifica el cumplimiento de cada escalón conforme el artículo 1;'
    ' si no alcanza, el Departamento Ejecutivo completa su costo con recursos de libre disponibilidad.')

# ============ 4 · Garantía de alquiler: las ya dadas, sólo con el fondo ===========================================
ins('anexo-20', 'no se otorgan garantías nuevas hasta que se recupere.',
    ' Las garantías ya otorgadas se pagan sólo con el fondo, en el orden en que se reclaman, a medida que el fondo se repone.')
ins('5.4-r1', 'también va a reforzar el fondo.',
    ' Las garantías ya dadas se siguen pagando sólo con el fondo, nunca con otro dinero del Municipio: si un mes no'
    ' alcanza, se pagan en el orden en que se reclamaron, a medida que entra dinero.')
rep('5.4-r1', '5 · No le cuesta al Municipio ni compite con los bancos.',
    '5 · No usa dinero del presupuesto de hoy ni compite con los bancos.', dentro=True)

# ============ 5 y 5b · Terrenos sin uso: las cuatro trabas, sin expropiación =======================================
reemplazar_parrafos('5.4-r3', 3, ['3 · Si no cumple, paga un recargo', '4 · Venderlo no sirve', '5 · Primero hay que saber'], [
    '3 · Si no cumple, paga más, y cada año más. La ordenanza de tasas va a fijar para los terrenos baldíos y las obras'
    ' paradas una tasa de servicios generales más alta que la de un terreno con casa, como ya hace Bahía Blanca. Sobre'
    ' esa tasa corre el recargo de la ley: sube cada año durante cinco años, hasta el 50% de la tasa, el máximo que permite, y'
    ' después sigue en el máximo hasta que el dueño cumpla. Como sube una tasa, la aprueba también la asamblea de'
    ' concejales y mayores contribuyentes (Constitución de la Provincia, artículo 193, inciso 2). Lo que se cobre por el'
    ' recargo va a ir a la garantía de alquiler. Estas cuentas no suman lo que se cobre de más, porque todavía no se sabe'
    ' cuántos terrenos sin uso hay: se cuentan en la primera ronda (punto 6).',
    '4 · Sin planes de pago ni perdones. La ley prohíbe dar exenciones o perdonar la deuda de ese recargo (Decreto-Ley'
    ' 8912/77, artículo 86), y el Municipio tampoco va a dar planes de pago. Quien no paga, pierde el terreno: el'
    ' Municipio cobra la deuda por juicio de apremio, con embargo y remate (Ley 13.406).',
    '5 · Venderlo no sirve para esquivar la regla. Según la misma ley, el plazo sigue corriendo aunque el terreno se'
    ' venda, y la obligación queda anotada en la escritura y en el Registro de la Propiedad. El que compra hereda el'
    ' tiempo que quedaba. Comprarse el propio terreno en el remate tampoco sirve: lo que paga cancela la deuda, pero la'
    ' obligación de construir sigue anotada, con los mismos plazos (artículo 85). Además, el remate tiene una base del'
    ' 80% de la tasación, y del 60% si en el primero nadie ofrece (Ley 13.406, artículo 16).',
    '6 · Primero hay que saber cuántos son. Durante la primera ronda de asambleas se van a contar los baldíos, las ruinas'
    ' y las obras paradas, y la inteligencia artificial del Municipio va a mostrar cuántos hay en cada zona. A cada dueño'
    ' se le va a explicar el daño que hace un terreno vacío y qué puede hacer con él.'],
    [len('3 · Si no cumple, paga más, y cada año más.'), len('4 · Sin planes de pago ni perdones.'),
     len('5 · Venderlo no sirve para esquivar la regla.'), len('6 · Primero hay que saber cuántos son.')])
e = by['5.4-r3']; assert e['fuentes'].startswith('5.4 · los terrenos sin uso: Ley 14.449, artículo 64') and '\n\n' not in e['fuentes']
e['fuentes'] = (
    '5.4 · los terrenos sin uso: Decreto-Ley 8912/77, artículos 84 a 88, según la Ley 14.449, artículo 64 (texto'
    f' actualizado, https://normas.gba.gob.ar/documentos/5B3DztjV.html, {HOY}): plazo para edificar de tres a cinco años;'
    ' los plazos no cambian aunque el terreno se venda, y eso se anota en la escritura y en el Registro de la Propiedad'
    ' Inmueble (artículo 85, inciso d); gravamen progresivo durante cinco años, fijado en la Ordenanza Impositiva, con'
    ' tope del 50% de la tasa de alumbrado, barrido y limpieza, que después sigue en el máximo hasta que se cumpla, y'
    ' «Queda prohibido conceder exenciones o condonaciones de deudas relativas al gravamen progresivo» (artículo 86).'
    ' El cobro: Ley 13.406, artículos 1 y 16 (texto actualizado, https://normas.gba.gob.ar/documentos/xAzPYioB.html,'
    f' {HOY}): apremio para los tributos de las municipalidades, y subasta del inmueble embargado con base del 80% de la'
    ' tasación y, si fracasa por falta de postores, del 60%. La tasa más alta: Bahía Blanca, Ordenanza Impositiva 2026,'
    ' capítulo XXI, artículo 59, «Tasa especial para los inmuebles baldíos, edificaciones derruidas y paralizadas»: la'
    ' tasa de servicios urbanos multiplicada por el factor de ocupación total de la zona, con un adicional del 10% al 50%'
    f' en cinco años (https://www.bahia.gob.ar/wp-content/uploads/2026/01/Ordenanza-Impositiva-2026.pdf, {HOY}).'
    ' Asamblea de concejales y mayores contribuyentes: Constitución de la Provincia, artículo 193, inciso 2.')
rep('anexo-21', 'Los plazos no cambian aunque el inmueble se venda, y la obligación se hace constar en la escritura.',
    'Los plazos no cambian aunque el inmueble se venda, y la obligación se hace constar en la escritura y se inscribe en'
    ' el Registro de la Propiedad Inmueble.')
titulo_parrafo('anexo-21', 'Artículo 4 — Gravamen y expropiación', 'Artículo 4 — Gravamen')
rep('anexo-21', 'Cumplidos cinco años de gravamen, el inmueble queda sujeto a expropiación (artículo 87).',
    'Cumplidos cinco años de gravamen, se sigue aplicando la alícuota máxima hasta que se cumpla la obligación (artículo 86).')
e = by['anexo-21']; assert _ps(e)[-2] == 'Artículo 4 — Gravamen'
e['texto'] += (
    '\n\nArtículo 5 — Tasa de los inmuebles sin uso\n\nLa Ordenanza Impositiva fija para los inmuebles del artículo 3 una'
    ' Tasa por Alumbrado, Limpieza y Servicios Generales mayor que la de los inmuebles edificados de la misma zona. El'
    ' gravamen del artículo 4 se calcula sobre esa tasa.'
    '\n\nArtículo 6 — Cobro\n\nNo se conceden exenciones, condonaciones ni planes de pago sobre el gravamen (artículo 86'
    ' del Decreto-Ley 8912/77). La deuda impaga se cobra por apremio, conforme la Ley 13.406, con embargo y subasta del'
    ' inmueble. Lo pagado en la subasta cancela la deuda, y la obligación de edificar subsiste con los mismos plazos,'
    ' conforme el artículo 85, inciso d), del Decreto-Ley 8912/77.')
nuevos('metodo-abogado', '• 5.4. La edificación obligatoria y la segunda y tercera vivienda en el lote', [
    '• 5.4. La tasa más alta para los terrenos sin uso en la Ordenanza Impositiva, y que la venta en remate por apremio'
    ' no cambia los plazos de la obligación de construir (Decreto-Ley 8912/77, artículos 85 y 86; Ley 13.406, artículo 16).'],
    [[[2, 6, 'b']]])

# ============ 6 y 6b · Acompañantes de salud mental: una opción entre varias, desde el mes 27 =======================
rep('5.6-r5', 'Empleados del Municipio cuyo trabajo ahora hace la inteligencia artificial del Municipio van a poder formarse'
    ' como acompañantes, con la formación que fija la Provincia (Resolución 592/2022).',
    'Desde el mes 27, cuando la automatización empieza a liberar tareas (5.3), los empleados del Municipio que quieran'
    ' van a poder formarse como acompañantes, con la formación que fija la Provincia (Resolución 592/2022). Es una opción'
    ' entre varias: también pueden sumarse al programa de empleo tecnológico (5.3), a los equipos de las plazas y los'
    ' parques, a deportes, a arte o a otras áreas de este programa.')
ins('5.3', 'y 6 que atienden, uno en cada zona, a quien no puede usar solo la inteligencia artificial del Municipio.',
    ' Quien prefiera otra tarea va a poder elegir entre varias: formarse como acompañante terapéutico (5.6), o sumarse a'
    ' los equipos de las plazas y los parques, a deportes, a arte o a otras áreas de este programa.')
cuadro_mover('6.4', 'Meses 7–12 | Salud mental: empieza la formación de los primeros acompañantes terapéuticos',
             'Mes 27 | Egresan los primeros 231',
             'Mes 27 | Salud mental: cuando la automatización empieza a liberar tareas, los empleados del Municipio que'
             ' eligen esta opción empiezan a formarse como acompañantes terapéuticos (5.3 y 5.6) | Cuántos se forman y'
             ' cuántos vecinos acompañan: se le pregunta a la inteligencia artificial del Municipio')

# ============ 7 y 8 · Power users: la tercera fórmula y las multas =================================================
rep('4.11-r5', 'Cobran sólo una parte de lo que su aviso le hace cobrar o ahorrar al Municipio, así que el sistema no puede'
    ' costar más de lo que genera.',
    'Todo se les paga de un mismo fondo, que se llena sólo con una parte de lo que sus mejoras le hacen cobrar o ahorrar'
    ' al Municipio, así que el sistema no puede costar más de lo que genera. Las reglas de detalle todavía se están estudiando.')
rep('4.11-r5', 'Cuando la mejora no tiene un monto, se usa una tabla según cuánto vale y a cuántos vecinos les sirve.',
    'Cuando la mejora no trae un cobro ni un ahorro directo, la inteligencia artificial del Municipio calcula cuánta'
    ' productividad suma, con las horas de trabajo que ahorra y los vecinos que la usan, y una persona lo confirma. En'
    ' ese caso cuenta sólo una propuesta bien armada, presentada y argumentada, no una idea suelta. Las multas también'
    ' cuentan: el vecino cobra un porcentaje sólo de lo que efectivamente se cobra de esa multa, no de lo que se impone.'
    ' Ningún proveedor ni empleado del Municipio cobra por una multa, y las multas siguen siendo acordes al ingreso de'
    ' cada uno (5.11).')
rep('5.11-r1', '10 · Nadie cobra por cada multa.', '10 · Ningún proveedor ni empleado cobra por cada multa.', dentro=True)
rep('5.11-r1', 'Ese fondo no se podrá usar para otra cosa. Va a pagar calles, cruces, reductores y educación vial,',
    'Ese fondo no se podrá usar para otra cosa, salvo la parte del vecino que avisó la falta, que se calcula sólo sobre lo'
    ' que efectivamente se cobra de esa multa (4.11). Va a pagar cámaras, calles, cruces y educación vial,')
cuadro('6.3', 'Nadie va a ganar dinero por cada multa que se pone. El dinero de las multas va a ir a un fondo de seguridad'
       ' vial, que no se puede usar para otra cosa |',
       'Ningún proveedor ni empleado va a ganar dinero por cada multa que se pone. El dinero de las multas va a ir a un'
       ' fondo de seguridad vial, que no se puede usar para otra cosa, salvo la parte del vecino que avisó la falta (4.11) |')
cuadro('6.6', 'Qué lo reduce: nadie va a cobrar por cada multa.',
       'Qué lo reduce: ningún proveedor ni empleado va a cobrar por cada multa.')
cuadro('6.6', 'Todo lo que se cobra por multas va a un fondo de seguridad vial, que no se puede usar para otra cosa.',
       'Todo lo que se cobra por multas va a un fondo de seguridad vial, que no se puede usar para otra cosa, salvo la'
       ' parte del vecino que avisó la falta, sólo sobre lo que se cobra de verdad (4.11).')
cuadro('6.4', 'el dinero de las multas va a un fondo de seguridad vial, que no se puede usar para otra cosa (5.11)',
       'el dinero de las multas va a un fondo de seguridad vial, que no se puede usar para otra cosa, salvo la parte del'
       ' vecino que avisó la falta (4.11 y 5.11)')
rep('anexo-metas', 'el contrato nuevo va a decir que nadie cobra por multa (5.11).',
    'el contrato nuevo va a decir que ningún proveedor cobra por multa (5.11).')

# ============ 9 · La inteligencia artificial del Municipio, siempre neutral ========================================
nuevos('4.11', 'Mostrará lo que no cierra, pero sin acusar.', [
    'Va a ser siempre neutral: muestra los pros y los contras, resumidos y claros, y acompaña las preguntas del vecino'
    ' sin tomar decisiones de criterio.'], [len('Va a ser siempre neutral: muestra los pros y los contras, resumidos y claros, y acompaña las preguntas del vecino sin tomar decisiones de criterio.')])
_n16 = ('Si el vecino le pregunta qué conviene votar, le muestra los pros y los contras de cada opción, resumidos y claros,'
        ' con los datos en la mano, sin recomendar ninguna.')
rep_span('4.11', 'Si el vecino le pregunta qué conviene votar, le da su punto de vista y le explica por qué, con los datos'
         ' en la mano. Siempre le aclara que es sólo un punto de vista, que puede estar equivocada y que la decisión es del vecino.',
         _n16 + ' Cuando le pide una recomendación, le cuenta qué dicen las mejores prácticas, nunca una conclusión propia,'
         ' porque la decisión es siempre del vecino.', [(0, len(_n16))])
rep('4.11-r4', '7 · Para votar, le va a explicar cada tema con sus datos, sin decirle qué votar.',
    '7 · Para votar, le va a explicar cada tema con sus datos y con los pros y los contras, sin decirle qué votar.', dentro=True)
cuadro('4.5', 'Antes de votar, le explica a cada vecino cada tema, con su historia y su contexto.',
       'Antes de votar, le explica a cada vecino cada tema, con su historia, su contexto y los pros y los contras, sin'
       ' decirle qué votar.')
rep('proponemos', 'también podrá consultarle por cada tema que se va a votar, con su historia y su contexto.',
    'también podrá consultarle por cada tema que se va a votar, con su historia, su contexto y los pros y los contras,'
    ' sin que ella le diga qué votar.')
nuevos('metodo-no-hace', '• Alertas. Cuando la inteligencia artificial del Municipio avise', [
    '• Neutralidad. La inteligencia artificial del Municipio es siempre neutral: muestra los pros y los contras,'
    ' resumidos y claros, y no toma decisiones de criterio. Si el vecino le pide una recomendación, le cuenta qué dicen'
    ' las mejores prácticas, nunca una conclusión propia (4.11).'], [[[2, 14, 'b']]])

# ============ 11 · El reductor lo paga la obra de la zona; la cámara, el fondo de seguridad vial ===================
rep('5.11-r1', 'Primero va la calle, y el reductor se paga con el dinero de obra de la zona.',
    'Primero va la calle. El reductor es obra, y se paga con el dinero de obra de la zona; la cámara, con el fondo de'
    ' seguridad vial (punto 11).')
cuadro('6.4', 'En cada lugar, la comisión de la zona elige entre una cámara o un reductor de velocidad. Después,',
       'En cada lugar, la comisión de la zona elige entre una cámara o un reductor de velocidad. El reductor se paga con'
       ' el dinero de obra de la zona, y la cámara, con el fondo. Después,')

# ============ Seguridad: la patrulla, sólo para el delito; tránsito, para ordenar ==================================
nuevos('5.7', 'Además, cuesta poco. En un experimento', [
    'La patrulla, sólo para prevenir y buscar el delito. Hoy hace también otra cosa: participa de operativos con la Policía'
    ' de la Provincia que en noviembre de 2025 hicieron 37.348 identificaciones, a 25.731 personas y a 11.617 vehículos,'
    ' y sus agentes se forman para labrar actas de tránsito. Proponemos que deje los controles de tránsito y que no pare a'
    ' nadie para pedirle papeles. Esa patrulla no es una policía: la seguridad pública le toca a la Provincia (Ley 12.154,'
    ' artículo 2), y demorar a alguien para identificarlo es una facultad de la policía (Ley 13.482, artículo 15). Como'
    ' cualquier persona, un agente de la patrulla sí puede detener a quien encuentra cometiendo un delito, y lo entrega'
    ' enseguida a la policía o al fiscal (Código Procesal Penal de la Provincia, artículo 156).',
    'Agentes de tránsito para ordenar el tránsito, no para multar. San Isidro tiene 120 agentes de tránsito, que hoy'
    ' también controlan licencias y papeles del vehículo. Van a quedar sólo los necesarios para ordenar el tránsito: la'
    ' entrada y la salida de las escuelas, los choques y los cortes de calle. Ninguno va a parar a nadie para multarlo.'
    ' El resto pasa a la patrulla, con la formación que ya reciben quienes entran a ella en el Centro de Formación Santa'
    ' Rita. La ley de empleo municipal permite ese pase cuando lo pide el servicio, siempre que no perjudique al'
    ' trabajador ni se use como castigo (Ley 14.656, artículo 8).',
    'Ningún vehículo retenido por una falta menor. Si la patente está floja, se ajusta en el lugar y el vehículo sigue:'
    ' la ley pide que no circule hasta que se arregle (Decreto 532/09, anexo III, artículo 14), pero no lo manda al'
    ' depósito. El vehículo se retiene sólo en los casos que manda la ley (Ley 13.927, artículo 37).',
    'Esto no es perdonar la ley. Un municipio no puede crear un régimen de multas más benigno que la ley nacional de'
    ' tránsito (Ley 24.449, artículo 2). Lo que cambia es la tarea de cada agente, que organiza el Ejecutivo (Ley Orgánica'
    ' de las Municipalidades, artículo 107), y queda escrita como una definición de funciones. Cuando un agente ve una'
    ' falta que la ley obliga a atender, actúa. Las cámaras de tránsito quedan, con tolerancia y aviso previo, y se suman'
    ' donde hay choques (5.11). La Policía de la Provincia sigue siendo autoridad de control del tránsito (Ley 13.927,'
    ' artículo 2).',
    'Cuánto cuesta. No suma sueldos, porque los agentes que pasan a la patrulla ya son empleados del Municipio. Formarlos'
    ' cuesta ⟦NUM:formacion_agentes_patrulla⟧. Hoy no se puede calcular cuánto se deja de cobrar en multas por los'
    ' controles que ya no se hacen, porque el Municipio no publica cuántas multas pone (5.11). Las multas no son para recaudar.'],
    [len('La patrulla, sólo para prevenir y buscar el delito.'), len('Agentes de tránsito para ordenar el tránsito, no para multar.'),
     len('Ningún vehículo retenido por una falta menor.'), len('Esto no es perdonar la ley.'), len('Cuánto cuesta.')])
ins('5.7', 'Este programa mantiene la cantidad de agentes que haya al asumir.',
    ' La patrulla va a crecer con los agentes de tránsito que pasan a ella, sin sumar empleados al Municipio (punto 1).')
fuente_mas('5.7', '5.7 · la patrulla y los agentes de tránsito: los 120 agentes de tránsito y sus tareas, Municipio de San'
           ' Isidro, 3 de agosto de 2026 (https://www.sanisidro.gob.ar/novedades/para-mejorar-la-seguridad-vial-san-isidro-ya-cuenta-con-120-agentes-de-tr%C3%A1nsito);'
           ' las 37.348 identificaciones de noviembre de 2025, Municipio de San Isidro, 3 de diciembre de 2025'
           ' (https://www.sanisidro.gob.ar/novedades/se-realizaron-3-mil-operativos-de-seguridad-y-m%C3%A1s-de-37-mil-identificaciones-en-noviembre);'
           ' la formación de la patrulla en actas de tránsito, 30 de octubre de 2025'
           ' (https://www.sanisidro.gob.ar/novedades/san-isidro-suma-nuevos-agentes-su-patrulla-municipal-y-alcanza-120-en-2025),'
           ' y el Centro de Formación Santa Rita (https://www.sanisidro.gob.ar/san-isidro-seguro). Ley 12.154, artículo 2'
           ' (https://normas.gba.gob.ar/documentos/BLmG9IQV.html); Ley 13.482, artículo 15'
           ' (https://normas.gba.gob.ar/documentos/xapPdi40.html); Código Procesal Penal de la Provincia, Ley 11.922,'
           ' artículos 153, 154 y 156 (https://normas.gba.gob.ar/documentos/V9OGJUPx.html); Ley 14.656, artículo 8'
           ' (https://normas.gba.gob.ar/documentos/xqq2dtpx.html); Ley 13.927, artículos 2 y 37'
           ' (https://normas.gba.gob.ar/documentos/0YqDnfd0.html); Decreto 532/09, anexo III, artículo 14'
           ' (https://normas.gba.gob.ar/documentos/B3yPzhj0.html); Ley 24.449, artículos 2 y 3'
           ' (https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/818/texact.htm); Ley Orgánica de las'
           ' Municipalidades, artículo 107 (https://normas.gba.gob.ar/documentos/OVG48SW0.html). Consultados el 18 de'
           ' noviembre de 2026.')
rep('proponemos', 'sólo le queda tomar la denuncia.',
    'sólo le queda tomar la denuncia. La patrulla municipal se va a dedicar sólo a prevenir y buscar el delito, sin'
    ' controles de tránsito ni pedir papeles.')
cuadro('2.3', 'También va a haber una oficina de ciberdelito.',
       'También va a haber una oficina de ciberdelito. La patrulla municipal va a dedicarse sólo a prevenir y buscar el'
       ' delito, sin controles de tránsito.')
rep('5.15', '7. Seguridad y multas: patrullar donde está el delito con los agentes que haya al asumir,',
    '7. Seguridad y multas: una patrulla que sólo previene y busca el delito, donde está el delito, con los agentes que'
    ' haya al asumir y los agentes de tránsito que pasan a ella;')
nuevos('metodo-no-hace', '• Cámaras. Proponemos que las cámaras analicen hechos', [
    '• Seguridad. La patrulla municipal no hace controles de tránsito ni para a nadie para pedirle papeles, y ningún'
    ' vehículo se retiene por una falta menor. Tampoco se perdona la ley: cambia la tarea de cada agente, no lo que la ley'
    ' manda (5.7).'], [[[2, 12, 'b']]])
nuevos('metodo-abogado', '• 5.6. El acompañamiento de la inteligencia artificial del Municipio', [
    '• 5.7. El pase de agentes de tránsito a la patrulla municipal (Ley 14.656, artículo 8), el decreto que define las'
    ' tareas de cada uno, y si la adhesión de la Provincia a la ley nacional de tránsito incluye el texto actual de su'
    ' artículo 2 (Ley 13.927, artículo 1; Ley 24.449, artículo 2).'], [[[2, 6, 'b']]])

# ============ 10 · Nota del gráfico 13 (sólo el texto; los datos del gráfico los rehace otro encargado) ============
cuadro('3.3', 'Desde 2028 cuentan también los 60 agentes que se sumaron a la patrulla en 2026 (5.7).',
       'Desde 2026 cuentan también los 60 agentes que se sumaron a la patrulla ese año (5.7).')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
