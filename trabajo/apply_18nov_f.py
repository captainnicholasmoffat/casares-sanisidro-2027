"""Actualización del 18/11/2026, parte F: los arreglos de la segunda revisión (scratchpad rev/r6 y rev/r7, HALLAZGOS.md),
con lo que decidió el coordinador sobre los puntos medios:
1. 5.9 y Ordenanza 4: la patrulla no demora a nadie (Ley 13.482, art. 15, es de la policía); puede detener a quien
   encuentra cometiendo un delito, como cualquier persona (5.7).
2. Inspecciones grabadas: de 40 a 100 de los 120 agentes de tránsito pasan a la patrulla en los meses 4 a 6, antes de que
   empiece la grabación (mes 9). Primera etapa: 88 a 113 inspectores y 20 a 80 agentes que quedan en tránsito, 108 a 193
   agentes: 10,6 a 19,0 M una vez y 51,1 a 96,3 M por año. Segunda etapa: la patrulla, de 359 a unos 390 más los 40 a 100
   que pasan, de 399 a unos 490: 39,2 a 48,3 M una vez y 180,5 a 222,2 M por año. Mismos costos por agente que antes
   (98.327 pesos una vez; 452.463 por año el inspector y la patrulla, 564.952 el de tránsito). Los sueldos no cambian.
3. 3.4 y cuadro 14: la certificación de cada escalón, la formación de los agentes que pasan y lo que se deja de cobrar en
   multas. El 44,7% no se mueve: la planilla ya resta la certificación del peor caso (Supuestos C182 suma C339).
4. Plan B de la votación (Ordenanza 1, art. 14; 4.6; cuadro 44): tablets de la asamblea y de la delegación, con dos
   personas del Municipio por asamblea; si falla el RENAPER, el personal mira el DNI contra el padrón.
5. Salud mental: hasta que hay acompañantes (mes 37), el resumen va sólo al profesional.
6. La tecnicatura pide el secundario completo; el Plan FinEs lo termina gratis (argentina.gob.ar, abierta hoy).
7. Terrenos: la tasa más alta corre desde que se declara; el recargo, si no cumple (como la Ordenanza 21, art. 5).
8. El primer año el Municipio convoca las dos rondas; cuadro 42, la formación de acompañantes en el mes 28 (como S14).
9. Denuncias de la obra antes de la auditoría de la obra: a la de la plataforma.
10. RENAPER: «validación del DNI y prueba de vida», con la tarifa del cuadro tarifario.
Además, los menores de los dos revisores. Se niega a correr dos veces.
Uso: python3 trabajo/apply_18nov_f.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if 'de 108 a 193 agentes' in by['5.9']['texto']:
    raise SystemExit('ya aplicado: no se toca nada')


def _ps(e): return e['texto'].split('\n\n')


def rep(eid, old, new):
    """Cambia old por new en el único párrafo que lo tiene; corre las marcas que siguen y se niega si toca una."""
    e = by[eid]; ps = _ps(e)
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
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
    """Agrega párrafos después del único párrafo que tiene ancla; corre las claves de las marcas de los que siguen."""
    e = by[eid]; ps = _ps(e); hits = [i for i, p in enumerate(ps) if ancla in p]; assert len(hits) == 1, (eid, ancla[:60])
    i = hits[0]; n = len(textos); mk = e.get('marcas', {})
    mk = {str(int(k) + n if int(k) > i else int(k)): v for k, v in mk.items()}
    for j, b in enumerate(negrita or []):
        if b: mk[str(i + 1 + j)] = [[0, b, 'b']] if isinstance(b, int) else b
    if mk: e['marcas'] = mk
    e['texto'] = '\n\n'.join(ps[:i + 1] + textos + ps[i + 1:])


def cuadro(eid, old, new, campo='texto'):
    cs = by[eid]['cuadros']; idx = [k for k, c in enumerate(cs) if old in c[campo]]
    assert len(idx) == 1 and cs[idx[0]][campo].count(old) == 1, (eid, old[:60], idx)
    cs[idx[0]][campo] = cs[idx[0]][campo].replace(old, new, 1)


def fila_despues(eid, ancla, nueva):
    c = by[eid]['cuadros'][0]; ls = c['texto'].split('\n')
    b = [k for k, l in enumerate(ls) if l.startswith(ancla)]; assert len(b) == 1, (eid, ancla)
    ls.insert(b[0] + 1, nueva); c['texto'] = '\n'.join(ls)


def fuente(eid, old, new):
    e = by[eid]; assert e['fuentes'].count(old) == 1, (eid, old[:60]); e['fuentes'] = e['fuentes'].replace(old, new, 1)


# ============ 1 · La patrulla no demora a nadie ======================================================================
rep('5.9', 'Es decir, quienes pueden labrar un acta, clausurar, multar o demorar a alguien.',
    'Es decir, quienes pueden labrar un acta, clausurar o multar, y la patrulla, que puede detener a quien encuentra '
    'cometiendo un delito (5.7).')
rep('anexo-4', '—quien pueda labrar acta, clausurar, multar o demorar a una persona—',
    '—quien pueda labrar acta, clausurar o multar, y la patrulla municipal—')

# ============ 2 · Inspecciones grabadas, con el pase de agentes de tránsito a la patrulla =============================
rep('5.9', 'Con ellos empiezan los agentes de tránsito. En total, son de 208 a 280 agentes. La patrulla municipal va a '
    'entrar en una segunda etapa.',
    'Con ellos empiezan los agentes que quedan en tránsito, de 20 a 80 de los 120 de hoy (5.7). En total, son de 108 a 193 '
    'agentes. La patrulla municipal va a entrar en una segunda etapa, con los agentes de tránsito que pasan a ella en los '
    'meses 4 a 6.')
rep('5.9', 'cuestan de 20,5 a 27,5 millones una sola vez. Después cuestan de 107,6 a 145,5 millones por año.',
    'cuestan de 10,6 a 19,0 millones una sola vez. Después cuestan de 51,1 a 96,3 millones por año.')
rep('5.9', 'Con los agentes que haya al asumir, de 359 a unos 390 (5.7), cuesta de 35,3 a 38,4 millones una sola vez, y de '
    '162,4 a 176,9 millones por año.',
    'Con los agentes que haya al asumir, de 359 a unos 390, y los de tránsito que pasan a ella, de 40 a 100 (5.7), son de '
    '399 a unos 490: cuesta de 39,2 a 48,3 millones una sola vez, y de 180,5 a 222,2 millones por año.')
cuadro('3.4', 'Inspecciones grabadas con el teléfono del agente (5.9) | 107,6 a 145,5 M por año, y 20,5 a 27,5 M una sola vez.',
       'Inspecciones grabadas con el teléfono del agente (5.9) | 51,1 a 96,3 M por año, y 10,6 a 19,0 M una sola vez.')
cuadro('3.4', 'de Habilitaciones y de obra, y los agentes de tránsito. La patrulla municipal se suma en la segunda.',
       'de Habilitaciones y de obra, y los agentes que quedan en tránsito. La patrulla municipal, con los agentes de '
       'tránsito que pasan a ella, se suma en la segunda.')

# ============ 3 · 3.4: la certificación, la formación de los agentes y las multas que no se cobran ====================
rep('3.4', 'Estas son las quince partes del programa', 'Estas son las diecisiete partes del programa')
rep('3.7', '4. Este programa tiene quince partes con costo', '4. Este programa tiene diecisiete partes con costo')
rep('3.4', '(4.11) y los tomógrafos ahorran sólo 660 millones.',
    '(4.11), los tomógrafos ahorran sólo 660 millones y las obras vecinales son de 50 millones en promedio, así que lo '
    'que sobra del 1,5% de la partida vecinal no alcanza para certificar cada escalón de la obra: faltan de 7,6 a 28,7 '
    'millones por año (4.11).')
ins('3.4', 'se usa otro 0,4% de esa parte del presupuesto (5.11).',
    ' Lo mismo pasa con lo que se deja de cobrar porque la patrulla deja los controles de tránsito, que hoy no se puede '
    'calcular (5.7).')
ins('3.4', 'Los acompañantes de salud mental son empleados que ya cobran su sueldo (5.6).',
    ' Tampoco suma sueldos el pase de agentes de tránsito a la patrulla: formarlos cuesta, una sola vez, de 9,2 a 55,0 '
    'millones por cada grupo de hasta 60, y lo paga el presupuesto de Seguridad (5.7).')
ins('3.4', 'Son 108,4 millones el año 1 y 433,6 millones el año 4.',
    ' Lo que sobra paga la auditoría externa que certifica cada escalón de la obra, de 15,7 millones el año 1 a 62,7 '
    'millones el año 4 (4.11). Si las obras son de 50 millones en promedio, no alcanza, y lo que falta, de 7,6 a 28,7 '
    'millones por año, sale del gasto flexible.')
fila_despues('3.4', 'Obra pública vecinal, la mitad de la obra al cuarto año |',
             'Certificación de cada escalón de la obra vecinal (4.11) | De 15,7 M el año 1 a 62,7 M el año 4* | No, salvo en '
             'el peor caso: con obras de 50 M en promedio, faltan de 7,6 a 28,7 M por año. | De lo que sobra del 1,5% de '
             'funcionamiento de la partida vecinal. Lo que falta, de la parte libre del gasto flexible.')
fila_despues('3.4', 'Multas de tránsito (5.11) |',
             'Agentes de tránsito que pasan a la patrulla (5.7) | De 9,2 a 55,0 M por cada grupo de hasta 60 agentes, una '
             'sola vez* | No. Los agentes ya son empleados del Municipio y cobran lo mismo. | Del presupuesto de Seguridad, '
             'que ya forma a quienes entran a la patrulla (programa 47.01). Lo que se deje de cobrar en multas, de la parte '
             'libre del gasto flexible.')

# ============ 4 · Plan B de la votación ===============================================================================
rep('anexo-1', 'Si el voto digital no está disponible para esa asamblea, se vota en ella, en los dispositivos del artículo 3.',
    'Si el voto desde el teléfono propio no está disponible para esa asamblea, se vota en los dispositivos del artículo 3, '
    'en la asamblea y en la delegación municipal, con dos agentes municipales por asamblea; si la verificación no es '
    'posible, el personal municipal coteja el documento con el padrón de la zona.')
cuadro('6.6', 'Si la votación no está lista en el mes 3, esa ronda se vota sólo en las tablets de la asamblea, con personal '
       'del Municipio.',
       'Si la votación por celular no está lista en el mes 3, esa ronda se vota en las tablets de la asamblea y de la '
       'delegación, con dos personas del Municipio por asamblea; si falla la validación del RENAPER, el personal mira el '
       'DNI contra el padrón.')
rep('4.6', 'Esa ronda la convoca el Municipio en cada zona, abierta y con las mismas reglas de voto, y las obras que elige '
    'las hace el Ejecutivo (6.1). Si la votación por celular no está lista a tiempo, esa ronda se vota sólo en las tablets '
    'de la asamblea.',
    'Esa ronda, y la segunda de ese año, las convoca el Municipio en cada zona, abiertas y con las mismas reglas de voto, '
    'y las obras del año 1 las hace el Ejecutivo (6.1). Si la votación por celular no está lista a tiempo, esa ronda se '
    'vota en las tablets de la asamblea y de la delegación, con dos personas del Municipio por asamblea.')

# ============ 5 · Salud mental: el resumen, al profesional; al acompañante, desde el mes 37 ============================
rep('5.6-r5', 'Con su permiso, ella le pasa un resumen a su acompañante y al profesional.',
    'Con su permiso, ella le pasa un resumen al profesional y, desde que hay acompañantes formados (mes 37), también a su '
    'acompañante.')
rep('proponemos', 'También va a escuchar a quien quiera contarle cómo se siente, y le va a acercar un acompañante formado, '
    'bajo un profesional (5.6).',
    'También va a escuchar a quien quiera contarle cómo se siente, bajo un profesional, y desde el mes 37 le va a acercar '
    'un acompañante formado (5.6).')
rep('metodo-abogado', 'y el resumen que le pasa al acompañante.',
    'y el resumen que le pasa al profesional y, desde el mes 37, al acompañante.')

# ============ 6 · La tecnicatura pide el secundario completo; FinEs ===================================================
rep('5.6-r5', 'Dura un año lectivo, y mientras se cursa no se puede trabajar como acompañante:',
    'Para entrar hace falta el secundario completo; quien no lo tiene lo puede terminar gratis con el Plan FinEs, que '
    'también se cursa en la Provincia. Dura un año lectivo, y recién al aprobarlo se puede inscribir en el registro de '
    'acompañantes:')
fuente('5.6-r5', '(Resolución 1221/15 de la Dirección General de Cultura y Educación, artículo 3)',
       '(Resolución 1221/15 de la Dirección General de Cultura y Educación, artículos 3 y 4)')
fuente('5.6-r5', 'la Tecnicatura es «pública y gratuita», Ministerio de Salud de la Provincia, 10 de diciembre de 2025 '
       '(https://gba.gob.ar/saludprovincia/noticias/abri%C3%B3_la_preinscripci%C3%B3n_para_carreras_y_cursos_de_formaci%C3%B3n_en_salud);',
       'la Tecnicatura es una de las «carreras públicas y gratuitas» de formación en Salud, y las tecnicaturas superiores '
       '«requieren título secundario completo», Ministerio de Salud de la Provincia, 10 de diciembre de 2025 '
       '(https://gba.gob.ar/saludprovincia/noticias/abri%C3%B3_la_preinscripci%C3%B3n_para_carreras_y_cursos_de_formaci%C3%B3n_en_salud); '
       'el Plan FinEs permite «cursar, de manera semipresencial y gratuito, el trayecto primario y/o secundario», con '
       'contactos en cada jurisdicción, también Buenos Aires, Ministerio de Capital Humano, página actualizada el 31 de '
       'agosto de 2026 (https://www.argentina.gob.ar/terminar-la-primaria-o-la-secundaria-con-el-plan-fines);')

# ============ 7 · Terrenos: la tasa más alta, desde que se declara; el recargo, si no cumple ===========================
_t3 = '3 · Paga más desde que se declara, y si no cumple, cada año más.'
rep_span('5.4-r3', '3 · Si no cumple, paga más, y cada año más. La ordenanza de tasas va a fijar para los terrenos baldíos y '
         'las obras paradas una tasa de servicios generales más alta que la de un terreno con casa, como ya hace Bahía '
         'Blanca. Sobre esa tasa corre el recargo de la ley:',
         _t3 + ' La ordenanza de tasas va a fijar para los terrenos baldíos, los edificios en ruinas y las obras paradas '
         'una tasa de servicios generales más alta que la de un terreno con casa de la misma zona, desde que se declara la '
         'obligación de construir, como ya hace Bahía Blanca. Si el dueño no cumple el plazo, sobre esa tasa corre el '
         'recargo de la ley:', negritas=[(0, len(_t3))])
rep('5.4-r3', 'Según la misma ley, el plazo sigue corriendo aunque el terreno se venda,',
    'Según el Decreto-Ley 8912/77, el plazo sigue corriendo aunque el terreno se venda,')
rep('5.4-r3', 'sigue anotada en el Registro, con los mismos plazos (artículo 85),',
    'sigue anotada en el Registro, con los mismos plazos (Decreto-Ley 8912/77, artículo 85),')
rep('anexo-21', 'No se conceden exenciones, condonaciones ni planes de pago sobre el gravamen (artículo 86 del Decreto-Ley 8912/77).',
    'No se conceden exenciones ni condonaciones sobre el gravamen (artículo 86 del Decreto-Ley 8912/77), ni planes de pago.')
rep('metodo-abogado', 'La edificación obligatoria y la segunda y tercera vivienda en el lote, y si la Ordenanza 21 '
    'necesita antes la aprobación de la Provincia, como las normas de ordenamiento urbano (Ordenanza 21 del anexo; Ley '
    '14.449; Decreto-Ley 8912/77, artículo 83).',
    'La edificación obligatoria y la segunda y tercera vivienda en el lote; si la Ordenanza 21 necesita antes la '
    'aprobación de la Provincia, como las normas de ordenamiento urbano; y si el plazo de tres años es para empezar o '
    'para terminar la obra, y desde cuándo corre (Ordenanza 21 del anexo; Ley 14.449; Decreto-Ley 8912/77, artículos 83 '
    'y 85, incisos a y b).')

# ============ 8 · El primer año el Municipio convoca las dos rondas; la formación de acompañantes, mes 28 ==============
rep('6.1', 'El primer año, como las comisiones todavía se están formando, la ronda la convoca el Municipio y las obras '
    'elegidas las hace el Ejecutivo. Desde el año 2, la convoca la comisión de cada zona.',
    'El primer año, como las comisiones todavía se están formando, las dos rondas las convoca el Municipio y las obras '
    'elegidas las hace el Ejecutivo. Desde el año 2, las convoca la comisión de cada zona.')
cuadro('6.4', 'Mes 27 | Salud mental: cuando la automatización empieza a liberar tareas, los empleados del Municipio que '
       'eligen esta opción empiezan a formarse como acompañantes terapéuticos, gratis, en un instituto superior público, '
       'con el año lectivo (5.3 y 5.6)',
       'Mes 28 | Salud mental: con el año lectivo que sigue al mes 27, cuando la automatización empieza a liberar tareas, '
       'los empleados del Municipio que eligen esta opción empiezan a formarse como acompañantes terapéuticos, gratis, en '
       'un instituto superior público (5.3 y 5.6)')

# ============ 9 · Denuncias de la obra antes de la auditoría de la obra ===============================================
ins('4.11', 'es otro trabajo, con otro contrato.',
    ' Hasta que empieza ese contrato, las denuncias sobre la obra las recibe la auditoría de la plataforma.')
rep('anexo-1', 'El remanente se aplica a la auditoría externa que certifica el cumplimiento de cada escalón conforme el '
    'artículo 1; si no alcanza, el Departamento Ejecutivo completa su costo con recursos de libre disponibilidad.',
    'El remanente se aplica a la auditoría externa que certifica el cumplimiento de cada escalón conforme el artículo 1 y '
    'recibe las denuncias sobre las obras de la Partida; si no alcanza, el Departamento Ejecutivo completa su costo con '
    'recursos de libre disponibilidad. Hasta que esa auditoría se contrata, las denuncias sobre las obras las recibe la '
    'auditoría externa de la plataforma.')

# ============ 10 · RENAPER: validación del DNI y prueba de vida ========================================================
rep('4.6', 'y la identidad se comprueba con el Registro Nacional de las Personas (RENAPER), que confirma el DNI y la foto de '
    'la cara. El Municipio firma con el RENAPER el convenio que lo permite, y en él pide la tarifa de un organismo público.',
    'y la identidad se comprueba con el Registro Nacional de las Personas (RENAPER), con la validación del DNI y la prueba '
    'de vida. El Municipio firma con el RENAPER el convenio que lo permite, y en él pide la tarifa reducida que hoy tiene '
    'sólo la Administración Pública Nacional.')
rep('4.6', 'Si la validación falla, el personal del Municipio mira el DNI contra el padrón de la zona.',
    'Si la validación falla, el vecino vota en la asamblea o en la delegación, donde el personal del Municipio mira su DNI '
    'contra el padrón de la zona.')
rep('4.6', 'Se paga con la inteligencia artificial del Municipio (cuadro 28).',
    'Está dentro del costo de la inteligencia artificial del Municipio, en Ciencia y Técnica (cuadro 28).')
fuente('4.6', 'servicio de validación de datos del DNI y servicio de validación por fotografía de rostro; la entidad',
       'servicios de validación de identidad por API, entre ellos el de validación de datos del DNI; la entidad')
fuente('4.6', '60 pesos la validación de datos del DNI y 70 la prueba de vida pasiva, por persona '
       '(https://servicios.infoleg.gob.ar/infolegInternet/anexos/420000-424999/423589/res19.pdf);',
       '60 pesos la validación de datos del DNI (ítem 13) y 70 la prueba de vida pasiva (ítem 14), por persona; la tarifa '
       'reducida es sólo para la Administración Pública Nacional (ítems 16 a 19) '
       '(https://servicios.infoleg.gob.ar/infolegInternet/anexos/420000-424999/423589/res19.pdf);')
fuente('4.11', 'validación de datos del DNI, 60 pesos, y prueba de vida pasiva, 70 pesos, con la tarifa entera',
       'validación de datos del DNI (ítem 13), 60 pesos, y prueba de vida pasiva (ítem 14), 70 pesos, con la tarifa entera')

# ============ Menores de los dos revisores ===========================================================================
rep('3.3', 'más los 60 agentes que se sumaron a la patrulla en marzo de 2026',
    'más los 60 agentes que empezaron a formarse para la patrulla en marzo de 2026')
rep('metodo-notas-3', 'más los 60 agentes que se sumaron a la patrulla en marzo de 2026',
    'más los 60 agentes que empezaron a formarse para la patrulla en marzo de 2026')
rep('5.7', 'No hace falta más patrulla. Es la misma patrulla,', 'No hace falta contratar más agentes. Es la misma patrulla,')
rep('4.11', '(cuadro 42): las denuncias, los power users,',
    '(cuadro 42): las denuncias y cartas documento que le redacta al vecino, los power users,')
cuadro('4.11', 'Los pasantes van a cobrar 240.000 $ por mes. Son cifras de referencia.',
       'Los pasantes van a cobrar 240.000 $ por mes. Estas cifras son de referencia.')
fuente('4.11', 'y la API de precios de Azure (prices.azure.com),',
       'y la API de precios de Azure (https://prices.azure.com/api/retail/prices?$filter=serviceName%20eq%20%27Storage%27'
       '%20and%20armRegionName%20eq%20%27swedencentral%27%20and%20skuName%20eq%20%27Hot%20LRS%27),')
fuente('4.11', '500 mil dólares sobre 230.600 mil de obras, el 0,22%',
       '500 mil dólares sobre 230.600 mil de costos directos (obras y gestión ambiental y social), el 0,22%')
rep('4.11-r5', 'Cobra el primero que avisa, sin esperas.',
    'Cobra el primero que avisa. Lo de las multas se le paga a medida que se cobran.')
rep('5.11-r1', 'Los reductores ya están contratados: son 536,7 millones de la licitación de 2025.',
    'Los reductores que ya están contratados son 536,7 millones de la licitación de 2025; los que elige cada zona se '
    'pagan con su dinero de obra (punto 2).')
cuadro('3.4', 'Además, los reductores de velocidad ya están contratados (536,7 M).',
       'Además, los reductores de velocidad que ya están contratados son 536,7 M; los que elige cada zona se pagan con su '
       'dinero de obra.')
rep('anexo-4', 'y la inteligencia artificial marca toda grabación sellada que no se suba.',
    'y la inteligencia artificial del Municipio marca toda grabación sellada que no se suba.')
rep('anexo-4', 'la inteligencia artificial corta el turno en una grabación por acto',
    'la inteligencia artificial del Municipio corta el turno en una grabación por acto')
rep('anexo-4', 'la inteligencia artificial difumina las caras de quienes no son parte de él',
    'la inteligencia artificial del Municipio difumina las caras de quienes no son parte de él')
rep('metodo-abogado', 'El pase de agentes de tránsito a la patrulla municipal (Ley 14.656, artículo 8), el decreto',
    'El pase de agentes de tránsito a la patrulla municipal (Ley 14.656, artículo 8), también el del personal '
    'temporario mensualizado (artículo 111), el decreto')
nuevos('metodo-abogado', '• 5.11. Quién lleva el registro de donantes de alimentos',
       ['• 5.11. Pagarle al vecino que avisó la falta un porcentaje de lo que se cobra de esa multa con el dinero de las '
        'multas, que la ley destina a la seguridad vial (Ley 24.449, artículo 85).'], [[[2, 7, 'b']]])

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
