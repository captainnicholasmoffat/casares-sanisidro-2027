"""Actualización del 18/11/2026, parte D: tercera tanda del coordinador, con las fuentes de la investigación del mismo día
(scratchpad rev/investigar_18nov/HALLAZGOS.md y ACOMPANANTES.md).
- Delegaciones: Acassuso no tiene delegación propia (comparte la subdelegación de Martínez Este): donde decía «la
  delegación de la zona», ahora «la delegación de su zona o la más cercana». Fuente oficial bloqueada: dos medios del
  26/6/2024.
- Acompañantes: la formación es gratis. El curso de 640 horas del registro provincial (Resolución 592/2022) equivale al
  primer año de la Tecnicatura Superior en Acompañamiento Terapéutico (Resolución DGCyE 1221/15), que dan gratis los
  institutos superiores públicos; dura un año lectivo y mientras se cursa no se puede trabajar como acompañante: quien
  empieza después del mes 27 acompaña desde el año siguiente, cerca del mes 37 (fila nueva en el cuadro 42).
- Tercer remate: el Municipio no pide la venta sin base (Ley 13.406, art. 16): el terreno sigue embargado, la deuda y el
  recargo siguen corriendo y la obligación sigue anotada. No se promete que el Municipio se quede con el terreno.
Re-ejecutable sólo una vez: si ya se aplicó, se detiene sin tocar nada.
Uso: python3 trabajo/apply_18nov_d.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if 'no pide venderlo sin base' in by['5.4-r3']['texto']:
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


def fila_despues(eid, ancla, nueva):
    c = by[eid]['cuadros'][0]; ls = c['texto'].split('\n')
    b = [k for k, l in enumerate(ls) if l.startswith(ancla)]; assert len(b) == 1, (eid, ancla)
    ls.insert(b[0] + 1, nueva); c['texto'] = '\n'.join(ls)


# ============ 1 · Delegaciones: la de su zona o la más cercana ======================================================
rep('4.6', 'en la asamblea o en la delegación municipal de su zona.',
    'en la asamblea o en la delegación municipal de su zona o la más cercana.')
rep('anexo-1', 'En cada asamblea y en la delegación municipal de la zona, el Departamento Ejecutivo',
    'En cada asamblea y en la delegación municipal de la zona o la más cercana, el Departamento Ejecutivo')
cuadro('6.4', 'votan con el celular o en las tablets de cada asamblea y de la delegación (4.6).',
       'votan con el celular o en las tablets de cada asamblea y de la delegación de su zona o la más cercana (4.6).')
cuadro('6.6', 'En cada asamblea y en la delegación de la zona hay tablets con personal del Municipio,',
       'En cada asamblea y en la delegación de la zona o la más cercana hay tablets con personal del Municipio,')
fuente_mas('4.6', '4.6 · las delegaciones: el Municipio tiene nueve delegaciones y dos subdelegaciones; Acassuso comparte'
           ' la subdelegación de Martínez Este. Zona Norte Hoy y Conurbano Digital, 26 de junio de 2024'
           ' (https://www.zonanortehoy.com/san-isidro/san-isidro-las-delegaciones-amplian-el-horario-de-atencion-y-suman-servicios/'
           ' y https://www.conurbanodigital.com/san-isidro-las-delegaciones-municipales-amplian-el-horario-de-atencion-y-suman-servicios/),'
           f' {HOY}; la página oficial de las delegaciones no se pudo abrir.')

# ============ 2 · Acompañantes: la formación es gratis y dura un año lectivo ========================================
rep('5.6-r5', 'los empleados del Municipio que quieran van a poder formarse como acompañantes, con la formación que fija la'
    ' Provincia (Resolución 592/2022). Es una opción entre varias: también pueden sumarse al programa de empleo tecnológico'
    ' (5.3), a los equipos de las plazas y los parques, a deportes, a arte o a otras áreas de este programa. Van a trabajar'
    ' asesorados y controlados por profesionales. No suma sueldos, porque ya son empleados del Municipio.',
    'los empleados del Municipio que quieran van a poder formarse como acompañantes. Es una opción entre varias: también'
    ' pueden sumarse al programa de empleo tecnológico (5.3), a los equipos de las plazas y los parques, a deportes, a arte'
    ' o a otras áreas de este programa. La formación es gratis: el curso de 640 horas que pide la Provincia para el'
    ' registro de acompañantes (Resolución 592/2022) equivale al primer año de la Tecnicatura Superior en Acompañamiento'
    ' Terapéutico, que dan gratis los institutos superiores públicos de la Provincia. Dura un año lectivo, y mientras se'
    ' cursa no se puede trabajar como acompañante: quien empieza con el año lectivo que sigue al mes 27 acompaña desde el'
    ' año siguiente, cerca del mes 37. Van a trabajar asesorados y controlados por profesionales. No suma sueldos ni otros'
    ' gastos, porque cursan en horario de trabajo y conservan su sueldo.')
fuente_mas('5.6-r5', '5.6 · la formación de los acompañantes: Resolución 592/2022 del Ministerio de Salud de la Provincia,'
           ' artículos 2 y 4 (https://normas.gba.gob.ar/documentos/0ZdY8yfq.pdf); el curso de 640 horas (Resolución'
           ' 1014/14) da por aprobado el primer año de la Tecnicatura Superior en Acompañamiento Terapéutico (Resolución'
           ' 1221/15 de la Dirección General de Cultura y Educación, artículo 3), según la ficha de la carrera del ISFDyT'
           ' N° 5 (https://isfdyt5-bue.infd.edu.ar/sitio/wp-content/uploads/2019/02/Info-Acompa%C3%B1amiento.pdf); la'
           ' Tecnicatura es «pública y gratuita», Ministerio de Salud de la Provincia, 10 de diciembre de 2025'
           ' (https://gba.gob.ar/saludprovincia/noticias/abri%C3%B3_la_preinscripci%C3%B3n_para_carreras_y_cursos_de_formaci%C3%B3n_en_salud);'
           ' quien cursa se inscribe en el registro al terminar, Anexo de la Resolución 442/2023'
           f' (https://normas.gba.gob.ar/anexos/descargar/60nqmZVv.pdf). {HOY[0].upper() + HOY[1:]}.')
cuadro('6.4', 'empiezan a formarse como acompañantes terapéuticos (5.3 y 5.6) |',
       'empiezan a formarse como acompañantes terapéuticos, gratis, en un instituto superior público, con el año lectivo'
       ' (5.3 y 5.6) |')
fila_despues('6.4', 'Mes 36 | Terminan las obras del año 3',
             'Mes 37 | Salud mental: los primeros empleados del Municipio que se formaron como acompañantes terapéuticos'
             ' empiezan a acompañar a los vecinos, bajo un profesional (5.6) | Cuántos acompañan y a cuántos vecinos: se le'
             ' pregunta a la inteligencia artificial del Municipio')

# ============ 3 · El tercer remate: el Municipio no vende sin base =================================================
rep('5.4-r3', 'y del 60% si en el primero nadie ofrece (Ley 13.406, artículo 16).',
    'y del 60% si en el primero nadie ofrece (Ley 13.406, artículo 16). Si en el segundo tampoco hay ofertas, el Municipio'
    ' no pide venderlo sin base, aunque la ley se lo permite: el terreno sigue embargado, la deuda y el recargo siguen'
    ' corriendo, y la obligación de construir sigue anotada.')
rep('anexo-21', 'conforme el artículo 85, inciso d), del Decreto-Ley 8912/77.',
    'conforme el artículo 85, inciso d), del Decreto-Ley 8912/77. En la subasta, el Departamento Ejecutivo no solicita la'
    ' venta sin limitación de precio del artículo 16 de la Ley 13.406: si la segunda subasta fracasa, el inmueble sigue'
    ' embargado y el gravamen sigue corriendo.')
e = by['5.4-r3']; old = 'y, si fracasa por falta de postores, del 60%.'
assert e['fuentes'].count(old) == 1
e['fuentes'] = e['fuentes'].replace(old, 'y, si fracasa por falta de postores, del 60%; si tampoco hay postores, «la actora'
                                    ' podrá proponer realizar la venta sin limitación de precio».', 1)

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
