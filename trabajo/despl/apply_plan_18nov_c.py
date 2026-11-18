"""Plan de despliegue, 18/11/2026, parte C: arreglos de la segunda revisión (scratchpad rev/r6 y rev/r7, HALLAZGOS.md) y
decisiones del coordinador:
1. La segunda ronda del año 1 (M08) la convoca el Municipio, como la primera (Ordenanza 1, artículo 14).
2. Supuestos nuevos, a la vista en REVISION.md §3.3: la derogación (C02) y la Ordenanza 1 (C05) se tratan en la sesión
   extraordinaria; la votación del mes 3 entra en los 35 días de I02 porque la arquitectura y el esqueleto se preparan
   antes de asumir. §2 de REVISION.md (gen_revision.py) ya no dice que todo lo de diciembre se trata desde el 1 de marzo.
3. Salud mental (I27): el resumen va al profesional y, desde el mes 37 (S15), también al acompañante.
4. Denuncias de la obra vecinal: hasta que se contrata su auditoría (M29), a la de la plataforma (I17, I22).
5. Votar: validación del DNI y prueba de vida (no «la foto»); plan B en las tablets de la asamblea y de la delegación, con
   dos personas del Municipio por asamblea; la delegación de la zona o la más cercana (M03); el convenio con el RENAPER
   (I20) ya no frena el arranque (I04): sin él se vota en las tablets.
6. Inspecciones grabadas (H08): de 108 a 193 agentes, porque de 40 a 100 de tránsito pasan a la patrulla.
7. Garantía de alquiler (V08): lo ya garantizado se paga sólo con el fondo (decisión 4 del 18/11).
8. Tablets (I21): una por asamblea y una en la delegación de cada zona.
Requiere apply_plan_18nov_b.py ya aplicado. Si ya se corrió, se detiene."""
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()
assert 'act("S16"' in s, 'falta apply_plan_18nov_b.py'
if 'sólo con el fondo, en el orden en que se reclaman' in s:
    print('ya aplicado'); raise SystemExit
G = H / 'gen_revision.py'; g = G.read_text()


def rep(old, new, cuantas=1):
    global s
    assert s.count(old) == cuantas, (old[:70], s.count(old)); s = s.replace(old, new)


# ---------------------------------------------------------------- 1. M08: el primer año convoca el Municipio
rep('''act("M08", "Segunda ronda de asambleas: los vecinos siguen las obras del año y preparan las del año siguiente", "Comisiones vecinales",''',
    '''act("M08", "Segunda ronda de asambleas: los vecinos siguen las obras del año y preparan las del año siguiente", "Intendente",''')
rep('''    steps=("Un voto por persona desde los 16 años, en la asamblea, en las tablets o por celular con el DNI y la foto verificados contra el RENAPER. "
           "Cada proyecto se revisa antes de votar, y cada comisión decide si el tendido de internet de su barrio entra en el dinero de su zona (5.4)."),''',
    '''    steps=("Un voto por persona desde los 16 años, en la asamblea, en las tablets o por celular, con la validación del DNI y la prueba de vida del RENAPER. "
           "Cada proyecto se revisa antes de votar, y cada comisión decide si el tendido de internet de su barrio entra en el dinero de su zona (5.4). "
           "El primer año la convoca el Municipio en cada zona; desde el año 2, la comisión de cada zona (decisión del 18/11/2026; Ordenanza 1, artículo 14)."),''')

# ---------------------------------------------------------------- 2. supuestos nuevos: sesión extraordinaria e I02
rep('''    note=TRAT + " El intendente pide tratarla en la sesión extraordinaria, junto con la Ordenanza 1 (Ley Orgánica, artículo 68, inciso 5).")''',
    '''    note=TRAT + " El intendente pide tratarla en la sesión extraordinaria, junto con la Ordenanza 1 (Ley Orgánica, artículo 68, inciso 5). "
                "Supuesto del 18/11/2026: se trata en esa sesión, y no desde el 1 de marzo.")''')
rep('''    note=TRAT + " Para que la primera ronda elija las obras con la partida ya creada, el intendente pide tratarla en la sesión "
                "extraordinaria (Ley Orgánica, artículo 68, inciso 5).")''',
    '''    note=TRAT + " Para que la primera ronda elija las obras con la partida ya creada, el intendente pide tratarla en la sesión "
                "extraordinaria (Ley Orgánica, artículo 68, inciso 5). Supuesto del 18/11/2026: se trata en esa sesión, y no desde el 1 de marzo.")''')
rep('''          "ni cómo la recibe el Municipio. Decisión del 18/11/2026."))''',
    '''          "ni cómo la recibe el Municipio. Decisión del 18/11/2026. Supuesto: la votación entra en los mismos 35 días hábiles que las "
          "otras tres partes, porque la arquitectura y el esqueleto preparados antes acortan la construcción; así llega al mes 3."))''')
rep('''           "La votación de la primera ronda funciona por celular, con el DNI y la foto verificados contra el RENAPER, y en tablets que lleva el personal del Municipio."),''',
    '''           "La votación de la primera ronda funciona por celular, con la validación del DNI y la prueba de vida del RENAPER, y en tablets que lleva el personal del Municipio."),''')

# ---------------------------------------------------------------- 3. I27: el resumen
rep('''Con permiso del vecino, le pasa un resumen "
           "a su acompañante y al profesional.''',
    '''Con permiso del vecino, le pasa un resumen "
           "al profesional y, desde que hay acompañantes formados (S15, mes 37), también a su acompañante.''')

# ---------------------------------------------------------------- 4. denuncias de la obra antes de M29
rep('''" Las denuncias sobre la obra vecinal van a la auditoría de la obra (M29); las demás, a la de la plataforma (I17)."),''',
    '''" Las denuncias sobre la obra vecinal van a la auditoría de la obra (M29) y, hasta que se contrata, a la de la plataforma (I17); "
           "las demás, a la de la plataforma."),''')
rep('''Recibe las denuncias graves, salvo las de la obra vecinal."))''',
    '''Recibe las denuncias graves; las de la obra vecinal, sólo hasta que se contrata la auditoría de la obra (M29)."))''')

# ---------------------------------------------------------------- 5. votar
rep('''un voto por persona desde los 16 años, por celular con el DNI y la foto "
           "verificados contra el RENAPER, o en las tablets que lleva el personal del Municipio a cada asamblea y a la delegación de la zona. "
           "Si la votación por celular se atrasa, esa ronda se vota sólo en las tablets de la asamblea. "''',
    '''un voto por persona desde los 16 años, por celular, con la validación del DNI "
           "y la prueba de vida del RENAPER, o en las tablets que lleva el personal del Municipio a cada asamblea y a la delegación de la zona o la más cercana. "
           "Si la votación por celular se atrasa, esa ronda se vota en las tablets de la asamblea y de la delegación, con dos personas del Municipio por asamblea. "''')
rep('''    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I03", "S01", "I20", "I21"], win=W(3), fuente="6.4",
    note="Si la votación por celular se atrasa, la primera ronda se vota sólo en las tablets de la asamblea (decisión del 18/11/2026).")''',
    '''    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I03", "S01", "I21"], win=W(3), fuente="6.4",
    note=("Si la votación por celular se atrasa, también porque el convenio con el RENAPER (I20) no llegó, la primera ronda se vota "
          "en las tablets de la asamblea y de la delegación, donde el personal del Municipio mira el DNI contra el padrón "
          "(decisión del 18/11/2026). Por eso el convenio no frena el arranque."))''')
rep('''act("I20", "Firmar con el RENAPER el Convenio Único de Confronte de Datos, por TAD, para verificar el DNI y la foto de quien vota",''',
    '''act("I20", "Firmar con el RENAPER el Convenio Único de Confronte de Datos, por TAD, para validar el DNI de quien vota y hacerle la prueba de vida",''')
rep('''sus servicios de validación de identidad: datos del DNI y foto. "''',
    '''sus servicios de validación de identidad: los datos del DNI y la prueba de vida. "''')
rep('''Si el convenio se atrasa, esa ronda se vota sólo en las tablets (I04). "''',
    '''Si el convenio se atrasa, esa ronda se vota en las tablets de la asamblea y de la delegación (I04). "''')

# ---------------------------------------------------------------- 6. H08: los agentes de la primera etapa
rep('''    steps="Comercio, Agencia de Control, Habilitaciones, obra y tránsito: de 208 a 280 agentes. La patrulla municipal, en una segunda etapa (5.9).")''',
    '''    steps=("Comercio, Agencia de Control, Habilitaciones, obra y los agentes que quedan en tránsito: de 108 a 193 agentes. "
           "Con los agentes de tránsito que pasan a ella en los meses 4 a 6 (G30), la patrulla municipal entra en una segunda etapa (5.9)."))''')

# ---------------------------------------------------------------- 7. V08: la garantía ya dada, sólo con el fondo
rep('''    steps="Comisión del 3% por mes de cada lado, depósito del 12% de un mes, alquiler hasta el 40% del ingreso, freno si la mora es alta.")''',
    '''    steps=("Comisión del 3% por mes de cada lado, depósito del 12% de un mes, alquiler hasta el 40% del ingreso, freno si la mora es alta. "
           "Las garantías ya dadas se pagan sólo con el fondo, en el orden en que se reclaman, a medida que se repone; nunca con "
           "otro dinero del Municipio (decisión del 18/11/2026)."))''')

# ---------------------------------------------------------------- 8. I21: las 12 tablets
rep('''con una por asamblea y una por delegación, 12, cuestan''',
    '''con una por asamblea y una en la delegación de cada zona, 12, cuestan''')

P.write_text(s)

# ---------------------------------------------------------------- REVISION.md §2: la sesión extraordinaria
OLD = '''  "Por eso las ordenanzas que entran en diciembre se tratan desde el 1 de marzo.")'''
NEW = ('''  "Por eso las ordenanzas que entran en diciembre se tratan desde el 1 de marzo, salvo la derogación y la Ordenanza 1: el intendente "\n'''
       '''  "las incluye en la sesión extraordinaria, para que la primera ronda vote con la partida ya creada (C02 y C05, supuesto del 18/11/2026).")''')
assert g.count(OLD) == 1; G.write_text(g.replace(OLD, NEW))
print('ok')
