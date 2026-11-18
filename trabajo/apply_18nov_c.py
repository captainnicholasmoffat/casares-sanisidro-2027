"""Actualización del 18/11/2026, parte C: las cifras de NUMEROS (scratchpad rev/aplicar_numeros/NUMEROS.md y su
PENDIENTES.md §8) y lo que decidió el coordinador sobre los pendientes de TEXTOS.
- Llena las marcas ⟦NUM⟧: la certificación de cada escalón (de 15,7 a 62,7 millones por año) y la formación de los
  agentes que pasan a la patrulla (de 9,2 a 55,0 millones por grupo de hasta 60, una vez, con el presupuesto de Seguridad).
- Decisión 2: las funciones nuevas de la inteligencia artificial del Municipio con su costo (70,7 millones por año en el
  escenario medio; 210,1 en el alto) y su fecha; la votación (RENAPER y 12 tablets, 4,5 millones por año) dentro del
  cuadro 28; la arquitectura y el esqueleto se preparan antes de asumir. Cifras que se mueven: cuadro 28, 4.11, cuadro 14,
  5.3 y notas del capítulo 4.
- Coordinador: votar cuesta (sale «no cuesta dinero» del 4.6); si falla el RENAPER, el personal mira el DNI contra el
  padrón; denuncias de la obra a la auditoría de la obra y todas las demás a la de la plataforma; la patrulla deja los
  controles en el mes 1 y el pase con formación va en los meses 4 a 6 (fila nueva en el cuadro 42); quien pasa no cobra
  menos; lo que se deja de cobrar en multas, de la parte libre del gasto flexible; lo que se cobre de más a los terrenos
  sin uso, al fondo de la garantía.
Fuentes: las que abrió NUMEROS el 18/11/2026 (Z.ai, Cloudflare, Azure, Dartmouth, RENAPER, Samsung, Ministerio de
Infraestructura de la Provincia, Ordenanza 9422 y el Municipio de San Isidro).
Re-ejecutable sólo una vez: si ya se aplicó, se detiene sin tocar nada.
Uso: python3 trabajo/apply_18nov_c.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if '⟦NUM:' not in json.dumps(d, ensure_ascii=False):
    raise SystemExit('ya aplicado (no quedan marcas ⟦NUM⟧): no se toca nada')


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

# ============ 1 · Las marcas ⟦NUM⟧ ===================================================================================
rep('4.11', 'La auditoría externa del cuadro 28 revisa la plataforma.',
    'La auditoría externa del cuadro 28 revisa la plataforma y recibe las denuncias graves que no son de la obra'
    ' vecinal: las coimas de inspectores, las de los comerciantes y los casos graves que escucha la inteligencia'
    ' artificial del Municipio.')
rep('4.11', 'Ese contrato cuesta ⟦NUM:certificacion_por_año⟧ por año y se paga con lo que sobra del 1,5% de funcionamiento'
    ' de la partida (4.6). Si no alcanza, lo que falta sale del gasto flexible (3.4).',
    'Ese contrato cuesta de 15,7 millones por año el año 1 a 62,7 millones el año 4, y se paga con lo que sobra del 1,5%'
    ' de funcionamiento de la partida (4.6). Si las obras son de 50 millones en promedio, no alcanza: faltan de 7,6 a 28,7'
    ' millones por año, que salen del gasto flexible (3.4).')
rep('metodo-notas-4', 'Así, el 1,5% alcanza en los dos casos. Lo que sobra del 1,5% paga la auditoría externa que certifica'
    ' cada escalón (4.11): ⟦NUM:certificacion_por_año⟧ por año. Cuando no alcanza, lo que falta sale del gasto flexible.',
    'Así, el 1,5% alcanza en los dos casos para que funcionen las comisiones. Lo que sobra del 1,5% paga la auditoría'
    ' externa que certifica cada escalón (4.11): de 15,7 millones el año 1 a 62,7 millones el año 4, el 0,22% de la'
    ' partida vecinal, la parte que un programa de obras de la Provincia con el BID reserva para su auditoría'
    ' independiente y sus evaluaciones. Cuando las obras son de 100 millones, lo que sobra alcanza; cuando son de 50'
    ' millones, faltan de 7,6 a 28,7 millones por año, que salen del gasto flexible.')
rep('5.7', 'No suma sueldos, porque los agentes que pasan a la patrulla ya son empleados del Municipio. Formarlos cuesta'
    ' ⟦NUM:formacion_agentes_patrulla⟧. Hoy no se puede calcular cuánto se deja de cobrar en multas por los controles que'
    ' ya no se hacen, porque el Municipio no publica cuántas multas pone (5.11).',
    'No suma sueldos, porque los agentes que pasan a la patrulla ya son empleados del Municipio. Formarlos cuesta, una'
    ' sola vez, de 9,2 a 55,0 millones por cada grupo de hasta 60 agentes, es decir, de 0,15 a 0,92 millones por agente,'
    ' y se paga con el presupuesto de Seguridad, que ya forma a quienes entran a la patrulla. Hoy no se puede calcular'
    ' cuánto se deja de cobrar en multas por los controles que ya no se hacen, porque el Municipio no publica cuántas'
    ' multas pone; lo cubre la parte libre del gasto flexible, como las rebajas de las multas (5.11).')

# ============ 2 · Decisión 2: funciones nuevas, su costo y su fecha ==================================================
nuevos('4.11', 'Nada se cuenta dos veces. Estos 2.000,7 millones', [
    'Las funciones más nuevas las construye el mismo equipo, a medida que llegan sus fechas (cuadro 42): las denuncias,'
    ' los power users, las historias cortas, la consulta de lugares con imágenes, la conversación de salud mental y los'
    ' contratos de alquiler. Lo que usan del modelo y de los servicios de imágenes y video suma 70,7 millones por año a'
    ' infraestructura y licencias cuando funcionan todas, desde 2030: 14,7 millones en 2028 y 65,4 millones en 2029. Con'
    ' un uso alto, serían 210,1 millones por año. La conversación de salud mental es la que más usa: 43,1 millones. Votar'
    ' con la identidad verificada suma 4,5 millones por año: 3,1 millones de la validación del RENAPER y 1,4 millones de'
    ' 12 tablets, que se compran por 4,3 millones y se reponen cada tres años.'])
for old, new in [('el costo es de 2.091,7 millones: el 25,6% de esa partida', 'el costo es de 2.166,9 millones: el 26,6% de esa partida'),
                 ('llega al 27,1%.', 'llega al 28,1%.'),
                 ('la plataforma cuesta 2.000,7 millones.', 'la plataforma cuesta 2.075,9 millones.'),
                 ('Estos 2.000,7 millones pagan la plataforma', 'Estos 2.075,9 millones pagan la plataforma')]:
    rep('4.11', old, new, dentro=True)
cuadro('4.11', 'Infraestructura y licencias |  |  |  |  | 243,5 M', 'Infraestructura y licencias |  |  |  |  | 318,7 M')
cuadro('4.11', 'Plataforma |  |  |  |  | 2.000,7 M', 'Plataforma |  |  |  |  | 2.075,9 M')
cuadro('4.11', 'Ciencia y Técnica, en total |  |  |  |  | 2.091,7 M', 'Ciencia y Técnica, en total |  |  |  |  | 2.166,9 M')
cuadro('4.11', 'salvo las compras chicas de los primeros meses (6.4). El detalle está en las notas del capítulo 4.',
       'salvo las compras chicas de los primeros meses (6.4). Infraestructura y licencias incluye las funciones nuevas,'
       ' con un uso medio (con un uso alto, 458,1 M), y la votación: la validación del RENAPER y 12 tablets, 4,5 M. El'
       ' detalle está en las notas del capítulo 4.')
cuadro('3.4', 'Plataforma de inteligencia artificial y dispositivos (4.11) | 2.091,7 M*', 'Plataforma de inteligencia artificial y dispositivos (4.11) | 2.166,9 M*')
cuadro('3.4', 'Junto con la plataforma, usa el 27,1% de ese presupuesto.', 'Junto con la plataforma, usa el 28,1% de ese presupuesto.')
rep('5.3', 'se va a usar el 27,1% de ese dinero.', 'se va a usar el 28,1% de ese dinero.', dentro=True)
nuevos('3.4', 'El detalle de cada parte está en el cuadro 14.', [
    'Las propuestas nuevas de vivienda, de reclamos y denuncias, de los power users y de salud mental casi no suman'
    ' gasto. La garantía de alquiler se paga con lo que aportan inquilinos y dueños, y se frena si muchos dejan de pagar'
    ' (5.4). Lo que se cobre de más a los terrenos sin uso va a esa garantía, y estas cuentas no lo suman. A los power'
    ' users se les paga de un fondo que se llena sólo con una parte de lo que las mejoras hacen cobrar o ahorrar (4.11).'
    ' Los acompañantes de salud mental son empleados que ya cobran su sueldo (5.6). El uso del modelo, de las imágenes y'
    ' del video de las funciones nuevas suma 70,7 millones por año, y votar con la identidad verificada, 4,5 millones:'
    ' los dos están en el cuadro 28, dentro de Ciencia y Técnica.'])
rep('metodo-notas-4', 'y el dólar de diciembre de 2025, $1.447,84 (BCRA).',
    'y el dólar de diciembre de 2025, $1.447,84 (BCRA). Con precios consultados el 18 de noviembre de 2026 van las'
    ' funciones nuevas y la votación: Z.ai, Cloudflare, Azure, el RENAPER y Samsung. Sus volúmenes de uso son una'
    ' estimación de este programa, en un escenario medio, que es el del cuadro, y uno alto.')
# Las fechas, en el cuadro 42
def fila_despues(eid, ancla, nueva):
    c = by[eid]['cuadros'][0]; ls = c['texto'].split('\n')
    b = [k for k, l in enumerate(ls) if l.startswith(ancla)]; assert len(b) == 1, (eid, ancla)
    ls.insert(b[0] + 1, nueva); c['texto'] = '\n'.join(ls)
fila_despues('6.4', 'Meses 6–9 | La inteligencia artificial del Municipio suma tres partes',
             'Meses 6–9 | La inteligencia artificial del Municipio suma la denuncia y la carta documento que le redacta al'
             ' vecino, con el dictamen del abogado (4.11), y las historias cortas para aprender a usarla, también en video'
             ' (4.11) | La propia inteligencia artificial del Municipio')
fila_despues('6.4', 'Meses 7–12 | Vivienda: una vez aprobada la Ordenanza 20',
             'Meses 7–12 | La inteligencia artificial del Municipio suma el pago a sus power users, con el dictamen del'
             ' abogado (4.11), y el encuentro entre dueños e inquilinos, con el contrato armado (5.4) | Cada pago y cómo se'
             ' calculó: se le pregunta a la inteligencia artificial del Municipio')
fila_despues('6.4', 'Meses 12–18 | Salud: en la inteligencia artificial del Municipio',
             'Meses 12–18 | Salud mental: la inteligencia artificial del Municipio suma la conversación a cualquier hora con'
             ' quien quiera contarle cómo se siente, bajo un profesional responsable (5.6) | La propia inteligencia'
             ' artificial del Municipio')
fila_despues('6.4', 'Meses 18–24 | Habilitaciones:',
             'Meses 18–24 | La inteligencia artificial del Municipio suma la consulta de lugares: el vecino le muestra un'
             ' terreno, una casa, un local o un pedazo de plaza con la cámara del teléfono, y ella le dice qué se puede hacer'
             ' ahí (5.9) | La propia inteligencia artificial del Municipio')
cuadro('6.5', ' Después de las cuatro primeras partes, la inteligencia artificial del Municipio suma sus funciones nuevas a'
       ' medida que se construyen, con el dictamen del abogado donde la Nota de método lo pide: las denuncias de los'
       ' vecinos, los power users, las historias cortas, la consulta de lugares, la conversación sobre salud mental y el'
       ' encuentro entre dueños e inquilinos.', '')
cuadro('6.6', 'esa ronda se vota sólo en las tablets de la asamblea, con personal del Municipio.',
       'esa ronda se vota sólo en las tablets de la asamblea, con personal del Municipio. La arquitectura y el esqueleto'
       ' se preparan antes de asumir: no cambia quién la construye ni cómo la recibe el Municipio, pero baja el riesgo de'
       ' que las fechas se atrasen.')
fuente_mas('4.11', '4.11 · las funciones nuevas: precios de Z.ai (https://docs.z.ai/guides/overview/pricing y'
           ' https://docs.z.ai/guides/video/cogvideox-3), Cloudflare Stream (https://developers.cloudflare.com/stream/pricing/)'
           ' y la API de precios de Azure (prices.azure.com), con el dólar de diciembre de 2025, $1.447,84, y un 15% de'
           ' contingencia; las horas de conversación, el ensayo de Therabot (Dartmouth,'
           ' https://tto.dartmouth.edu/news/2025/03/first-therapy-chatbot-trial-yields-mental-health-benefits). Los'
           f' volúmenes de uso son una estimación de este programa. Todo {HOY}.')
fuente_mas('4.11', '4.11 · la votación: RENAPER, cuadro tarifario (Anexo IF-2026-20279196-APN-RENAPER#MI, 26 de febrero de'
           ' 2026), validación de datos del DNI, 60 pesos, y prueba de vida pasiva, 70 pesos, con la tarifa entera'
           ' (https://servicios.infoleg.gob.ar/infolegInternet/anexos/420000-424999/423589/res19.pdf); la tablet, Samsung'
           f' Argentina, tienda oficial (https://www.samsung.com/ar/tablets/galaxy-tab-a/). Todo {HOY}.')
fuente_mas('4.11', '4.11 · la certificación de cada escalón: Ministerio de Infraestructura de la Provincia de Buenos Aires,'
           ' Reglamento Operativo del Programa de Saneamiento Ambiental de la Cuenca del Río Reconquista (Préstamo BID'
           ' 3256/OC-AR): auditoría, monitoreo y evaluación, 500 mil dólares sobre 230.600 mil de obras, el 0,22%'
           f' (https://www.minfra.gba.gob.ar/web/Compartida/Reglamento_OPrograma.pdf, {HOY}).')
fuente_mas('metodo-notas-4', 'Notas del capítulo 4 · las funciones nuevas, la votación y la certificación: las fuentes'
           ' del 4.11 (Z.ai, Cloudflare, Azure, Dartmouth, RENAPER, Samsung y el Reglamento Operativo del préstamo BID'
           f' 3256/OC-AR, https://www.minfra.gba.gob.ar/web/Compartida/Reglamento_OPrograma.pdf), {HOY}.')

# ============ 3 · Lo que decidió el coordinador =====================================================================
# Votar cuesta; si falla el RENAPER, el personal mira el DNI
rep('4.6', 'Ninguna de esas tres cosas cuesta dinero.',
    'Cambiar el horario y el lugar no cuesta dinero. Votar con la identidad verificada cuesta 4,5 millones por año: la'
    ' validación del RENAPER, con su tarifa entera, y 12 tablets. Se paga con la inteligencia artificial del Municipio'
    ' (cuadro 28).')
rep('4.6', 'El Municipio firma con el RENAPER el convenio que lo permite.',
    'El Municipio firma con el RENAPER el convenio que lo permite, y en él pide la tarifa de un organismo público.')
ins('4.6', 'vota en una tablet con personal del Municipio, en la asamblea o en la delegación municipal de su zona.',
    ' Si la validación falla, el personal del Municipio mira el DNI contra el padrón de la zona.')
ins('anexo-1', 'pone a disposición dispositivos y personal para votar en forma digital.',
    ' Si la verificación no es posible, el personal municipal coteja el documento con el padrón de la zona.')
fuente_mas('4.6', '4.6 · lo que cuesta votar: RENAPER, cuadro tarifario del 26 de febrero de 2026, 60 pesos la validación'
           ' de datos del DNI y 70 la prueba de vida pasiva, por persona'
           ' (https://servicios.infoleg.gob.ar/infolegInternet/anexos/420000-424999/423589/res19.pdf); 12 tablets de la'
           f' tienda oficial de Samsung Argentina (https://www.samsung.com/ar/tablets/galaxy-tab-a/). {HOY[0].upper() + HOY[1:]}.')
# Denuncias: las de la obra, a la auditoría de la obra; todas las demás, a la de la plataforma
rep('4.11-r1', 'También va a ir a un control independiente: la auditoría externa, el Concejo y la asociación de la zona.',
    'También va a ir a un control independiente: el Concejo, la asociación de la zona y la auditoría externa de la'
    ' plataforma (cuadro 28), o la de la obra si se trata de la obra vecinal (4.11).')
rep('5.9', 'Sólo los auditores del Municipio y la auditoría externa van a ver',
    'Sólo los auditores del Municipio y la auditoría externa de la plataforma (4.11) van a ver')
rep('5.9-r2', 'También le llegará a la auditoría externa y, si hay delito, a la fiscalía. Mientras no se contrate la'
    ' auditoría externa,',
    'También le llegará a la auditoría externa de la plataforma (4.11) y, si hay delito, a la fiscalía. Mientras no se'
    ' contrate esa auditoría,')
rep('5.9-r2', 'como la comisión del Concejo y la auditoría externa.', 'como la comisión del Concejo y la auditoría externa de la plataforma.')
rep('4.9', 'Cada escalón nuevo se libera cuando la auditoría externa certifica', 'Cada escalón nuevo se libera cuando la auditoría externa de la obra certifica')
rep('proponemos', 'el dinero del siguiente se libera recién cuando la auditoría externa certifica',
    'el dinero del siguiente se libera recién cuando la auditoría externa de la obra certifica')
cuadro('6.5', 'la beca municipal, la auditoría externa y el mapa', 'la beca municipal, la auditoría externa de la obra y el mapa')
cuadro('6.6', 'y hay una auditoría externa (cuadro 28).', 'y hay una auditoría externa de la plataforma (cuadro 28).')
rep('anexo-1', 'y se libera cuando la auditoría externa certifica que el anterior se cumplió.',
    'y se libera cuando la auditoría externa de la obra certifica que el anterior se cumplió.')
rep('anexo-4', 'sólo lo ven los auditores del Municipio y la auditoría externa.',
    'sólo lo ven los auditores del Municipio y la auditoría externa de la plataforma.')
rep('anexo-4', 'a la auditoría externa y, si hay delito, a la fiscalía, y nunca sólo al superior del denunciado.',
    'a la auditoría externa de la plataforma y, si hay delito, a la fiscalía, y nunca sólo al superior del denunciado.')
rep('anexo-4', 'Hasta que se contrata la auditoría externa, la denuncia', 'Hasta que se contrata esa auditoría, la denuncia')
# Seguridad: controles fuera desde el mes 1; el pase con formación, en los meses 4 a 6; nadie cobra menos
rep('5.7', 'Proponemos que deje los controles de tránsito y que no pare a nadie para pedirle papeles.',
    'Proponemos que, desde el primer mes, deje los controles de tránsito y no pare a nadie para pedirle papeles: alcanza'
    ' con una instrucción del intendente, sin formación.')
rep('5.7', 'El resto pasa a la patrulla, con la formación que ya reciben quienes entran a ella en el Centro de Formación'
    ' Santa Rita.',
    'El resto pasa a la patrulla en los meses 4 a 6, con la formación que ya reciben quienes entran a ella en el Centro de'
    ' Formación Santa Rita. Cuántos pasan lo fija un relevamiento de lo que hace falta: entre 40 y 100.')
ins('5.7', 'siempre que no perjudique al trabajador ni se use como castigo (Ley 14.656, artículo 8).',
    ' Por eso, quien pasa no cobra menos que hoy.')
fila_despues('6.4', 'Meses 4–6 | Seguridad: se arma el mapa de los hechos',
             'Meses 4–6 | Seguridad: los agentes de tránsito que no hacen falta para ordenar el tránsito pasan a la'
             ' patrulla, con la formación que ya da el Municipio, y ninguno cobra menos. Cuántos, lo fija un relevamiento:'
             ' entre 40 y 100. La patrulla ya dejó los controles de tránsito en el primer mes, por una instrucción del'
             ' intendente (5.7) | Cuántos pasan y cuántos se forman: se le pregunta a la inteligencia artificial del Municipio')
fuente_mas('5.7', '5.7 · lo que cuesta el pase: Ordenanza 9422, presupuesto 2026, programa 47.01, «Formación y capacitación'
           ' de agentes de seguridad» (formularios F6 y F7), y artículo 17, compensaciones del inspector de tránsito y'
           ' de la Patrulla Municipal'
           ' (https://www.sanisidro.gob.ar/sites/default/files/img/ordenanza_del_presupuesto_2026_1.pdf); el curso de dos'
           ' meses, Municipio de San Isidro, «Capacitan 60 nuevos agentes…», 3 de marzo de 2026'
           ' (https://www.sanisidro.gob.ar/novedades/capacitan-60-nuevos-agentes-para-reforzar-la-patrulla-municipal-y-el-sistema-de-prevenci%C3%B3n).'
           f' Cálculo propio, {HOY}.')
# Terrenos: lo que se cobra de más por la tasa, al fondo de la garantía
rep('5.4-r3', 'Lo que se cobre por el recargo va a ir a la garantía de alquiler.',
    'Lo que se cobre de más por esa tasa y por el recargo va a ir a la garantía de alquiler.')
rep('anexo-20', 'lo que se cobre por el gravamen de la Ordenanza 21',
    'lo que se cobre por el gravamen y por la diferencia de tasa de los artículos 4 y 5 de la Ordenanza 21')
rep('anexo-21', 'El gravamen del artículo 4 se calcula sobre esa tasa.',
    'El gravamen del artículo 4 se calcula sobre esa tasa. Lo que se recauda por encima de la tasa de los inmuebles'
    ' edificados de la misma zona va al fondo de la Ordenanza 20.')

assert '⟦NUM:' not in json.dumps(d, ensure_ascii=False)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
