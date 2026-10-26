import json, re, copy, shutil
from pathlib import Path
S = '/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad'
P = Path('/home/claude/proyecto/web/data/programa.json'); A = Path('/home/claude/proyecto/despliegue/acciones.json')
shutil.copy(A, S + '/acciones_antes_d19.json')
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
log = []
# 1 · recuadro de la tasa, punto 3
e = by['5.11-r3']; o = 'Lo que el comerciante declare al Municipio no cambia su tope.'; n = 'Su tope no cambia por lo que declare al Municipio.'
ps = e['texto'].split('\n\n'); hit = [i for i, p in enumerate(ps) if o in p]; assert len(hit) == 1
i = hit[0]; pos = ps[i].index(o)
for m in e['marcas'].get(str(i), []): assert m[1] <= pos
ps[i] = ps[i].replace(o, n); e['texto'] = '\n\n'.join(ps); log.append(('5.11-r3', o, n))
# 2 · cuadro 42: la Ordenanza 18 con las demás y una fila para la 17
c = [c for c in by['6.4']['cuadros'] if c['titulo'].startswith('Cuadro 42')][0]; t = c['texto']
o1 = 'Se presentan al Concejo las nueve ordenanzas del anexo que todavía faltan:'; n1 = 'Se presentan al Concejo las diez ordenanzas del anexo que todavía faltan:'
assert t.count(o1) == 1; t = t.replace(o1, n1); log.append(('6.4 · Cuadro 42', o1, n1))
o2 = 'y el 75% de los lugares para instructores de San Isidro | Expedientes y Boletín Oficial Municipal'
n2 = 'y el 75% de los lugares para instructores de San Isidro 10) la de compras al comercio de San Isidro y de donación de alimentos | Expedientes y Boletín Oficial Municipal'
assert t.count(o2) == 1; t = t.replace(o2, n2); log.append(('6.4 · Cuadro 42', o2, n2))
anchor = [l for l in t.split('\n') if l.startswith('Meses 4–6 | Se presentan dos ordenanzas más.')]; assert len(anchor) == 1
fila = ('Meses 4–6 | Se presenta la Ordenanza 17, el tope de la tasa de seguridad e higiene para el comercio chico, pagado con una suba de alrededor de 4% a los comercios grandes (5.11). '
        'El Concejo la aprueba como ordenanza preparatoria y después la vota la Asamblea de Concejales y Mayores Contribuyentes | Expedientes y Boletín Oficial Municipal')
t = t.replace(anchor[0], anchor[0] + '\n' + fila); log.append(('6.4 · Cuadro 42', '(fila nueva, después de la de las dos ordenanzas más)', fila))
c['texto'] = t
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
# 3 · plan de despliegue
a = json.loads(A.read_text()); ab = {x['code']: x for x in a}
assert 'C61' not in ab
o3 = ab['C24']['task']; ab['C24']['task'] = 'Revisión legal de las once ordenanzas que faltan: la 2, la 4, la 6, la 8, la 10, la 11, la 12, la 13, la 14, la 17 y la 18'
log.append(('plan C24', o3, ab['C24']['task']))
NOTA_CAL = ab['C49']['note']; NOTA_TRAT = ab['C50']['note']
def acc(code, task, owner, team, dur, start, finish, flt, ms, decision, steps, sne, needs, note, fuente):
    return {'code': code, 'task': task, 'stream': '2 Concejo y ordenanzas', 'owner': owner, 'team': team, 'dur': dur, 'start': start, 'finish': finish,
            'float': flt, 'critical': False, 'milestone': ms, 'decision': decision, 'steps': steps, 'moves': '', 'sne': sne,
            'needs': [{'code': n, 'type': 'FS', 'lag': 0} for n in needs], 'note': note, 'fuente': fuente}
VOTO = 'Aprobarla o no. Hacen falta trece votos de veinticuatro, y ningún bloque llega solo (4.7).'
nuevas = [
 acc('C61', 'Entra la Ordenanza 18, de compras al comercio de San Isidro y de donación de alimentos', 'Intendente', 'Intendencia', 0, '2028-03-10', '2028-03-10', 65, True, '',
     'Prioridad de hasta 5% para el comercio de San Isidro, compras por renglón y por zona, puntaje para el comercio que dona alimentos y el registro de donantes. Cómo se comprueba: «Expedientes y Boletín Oficial Municipal.»',
     '2028-03-10', ['C24'], NOTA_CAL, 'anexo.18'),
 acc('C62', 'Tratamiento de la Ordenanza 18 en el Concejo', 'Concejo Deliberante', 'Concejo', 22, '2028-03-10', '2028-04-11', 946, False, '',
     'El proyecto pasa por las comisiones del Concejo y se vota en sesión.', '', ['C61'], NOTA_TRAT, 'anexo.18'),
 acc('C63', 'El Concejo aprueba la Ordenanza 18', 'Concejo Deliberante', 'Concejo', 0, '2028-04-11', '2028-04-11', 946, True, VOTO,
     'Votación en sesión. Después, el intendente la promulga y se publica en el Boletín Oficial.', '', ['C62'], '', 'anexo.18'),
 acc('C64', 'Entra la Ordenanza 17, del tope de la tasa de seguridad e higiene para el comercio chico', 'Intendente', 'Intendencia', 0, '2028-03-10', '2028-03-10', 65, True, '',
     'Tope para el comercio monotributista según su categoría, pagado con una suba de alrededor de 4% a los comercios grandes (5.11). Cómo se comprueba: «Expedientes y Boletín Oficial Municipal.»',
     '2028-03-10', ['C24'], NOTA_CAL, 'anexo.17'),
 acc('C65', 'Tratamiento de la Ordenanza 17 en el Concejo, como ordenanza preparatoria', 'Concejo Deliberante', 'Concejo', 22, '2028-03-10', '2028-04-11', 935, False, '',
     'El proyecto pasa por las comisiones del Concejo, que lo aprueba como ordenanza preparatoria para la Asamblea.', '', ['C64'], NOTA_TRAT, 'anexo.17'),
 acc('C66', 'El Concejo aprueba la Ordenanza 17 como ordenanza preparatoria', 'Concejo Deliberante', 'Concejo', 0, '2028-04-11', '2028-04-11', 935, True,
     'Aprobarla o no como ordenanza preparatoria: alcanza la mayoría simple (Ley Orgánica de las Municipalidades, artículo 29).',
     'Después, el presidente del Concejo cita a la Asamblea de Concejales y Mayores Contribuyentes.', '', ['C65'], '', 'anexo.17'),
 acc('C67', 'Asamblea de Concejales y Mayores Contribuyentes por la Ordenanza 17', 'Concejo Deliberante', 'Concejo', 11, '2028-04-11', '2028-04-26', 935, False, '',
     'Se cita a todos los concejales y mayores contribuyentes con ocho días de anticipación, dentro de los quince días de aprobada la ordenanza preparatoria.', '', ['C66'],
     'Ley Orgánica de las Municipalidades, artículos 29 y 98. La lista de mayores contribuyentes vigente vence el 30 de abril (artículo 94).', 'anexo.17'),
 acc('C68', 'La Asamblea aprueba la Ordenanza 17: rige el tope de la tasa para el comercio chico', 'Concejo Deliberante', 'Concejo', 0, '2028-04-26', '2028-04-26', 935, True,
     'Aprobarla o no, con la mayoría que pide la Constitución de la Provincia (artículo 193, inciso 2).',
     'Después, el intendente la promulga y se publica en el Boletín Oficial.', '', ['C67'], '', 'anexo.17'),
]
def ins_after(code, items):
    i = [k for k, x in enumerate(a) if x['code'] == code][0]
    a[i + 1:i + 1] = items
ins_after('C56', [nuevas[0], nuevas[3]]); ins_after('C57', [nuevas[1], nuevas[4]]); ins_after('C58', [nuevas[2], nuevas[5], nuevas[6], nuevas[7]])
for x in nuevas: log.append(('plan ' + x['code'], '', x['task']))
A.write_text(json.dumps(a, ensure_ascii=False, indent=1) if A.read_text().startswith('[\n') else json.dumps(a, ensure_ascii=False))
codes = {x['code'] for x in a}; assert all(n['code'] in codes for x in a for n in x['needs'])
print(len(a), 'acciones'); [print(l) for l in log]
