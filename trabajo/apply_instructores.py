import json, re, shutil
from pathlib import Path
S = '/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad'
P = Path('/home/claude/proyecto/web/data/programa.json'); shutil.copy(P, S + '/programa_antes_instructores.json')
d = json.loads(P.read_text()); by = {e['id']: e for e in d}; log = []
def rep(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n'); hit = [i for i, p in enumerate(ps) if old in p]; assert len(hit) == 1, (eid, old[:40], hit)
    i = hit[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps); log.append((eid, old, new))
# 1 · recuadro 5.5-r11, punto 5
rep('5.5-r11', 'No van a pagar canon, y van a tener reglas simples. El registro no le da a nadie un sitio ni un horario exclusivo en la plaza.',
    'No van a pagar nada por dar clases en la plaza: ni canon ni tasa. Hoy, en cambio, la Ordenanza Impositiva permite cobrar 246 pesos por metro cuadrado y por día a quien usa un espacio público (artículo 17, d.1): una clase en 200 metros cuadrados podría pagar 49.200 pesos por día. Además, cada instructor registrado va a tener su lugar y su horario garantizados, que asigna la inteligencia artificial del Municipio. Fuera de ese horario, el lugar es de todos: nadie se adueña de la plaza.')
# 2 · punto nuevo 6 y el viejo 6 pasa a 7
e = by['5.5-r11']; ps = e['texto'].split('\n\n')
k = [i for i, p in enumerate(ps) if p.startswith('6 · Espectáculos al aire libre')]; assert len(k) == 1; k = k[0]
nuevo = ('6 · El lugar de la clase, protegido. Durante la clase, nadie va a poder estacionar ni ocupar ese lugar, y quien deje ahí una moto o un auto va a recibir una multa. '
         'El instructor va a poder pedirle a la gente que se corra, mostrando en su teléfono el permiso de la inteligencia artificial del Municipio. '
         'Si alguien no se corre, el instructor saca una foto y la inteligencia artificial la sella y arma la denuncia, como con la prueba del vecino por el ruido (más arriba). '
         'La multa la pone el Municipio, nunca el instructor. Así, quien da clases se siente protegido y parte de este programa.')
ps[k] = ps[k].replace('6 · Espectáculos', '7 · Espectáculos', 1)
ps.insert(k, nuevo)
mk = {}
for key, v in e['marcas'].items(): mk[str(int(key) + 1) if int(key) >= k else key] = v
mk[str(k)] = [[0, nuevo.index('. ') + 1, 'b']]
e['marcas'] = dict(sorted(mk.items(), key=lambda kv: int(kv[0]))); e['texto'] = '\n\n'.join(ps)
if 'orden' in e:
    raise SystemExit('el recuadro tiene orden: revisar')
log.append(('5.5-r11', '(punto nuevo 6; el de espectáculos pasa a 7)', nuevo))
# 3 · cuánto cuesta
rep('5.5-r11', 'De ese canon, en los lugares del convenio queda el 60%.',
    'De ese canon, en los lugares del convenio queda el 60%. No cobrarles a los instructores casi no cambia lo que recauda el Municipio: todo el derecho por usar espacios públicos, que incluye cables, postes, toldos y mesas en la vereda, recaudó 929 millones en 2025, y no se publica cuánto pagan los instructores. Proteger el lugar de la clase no suma gastos: lo hacen la inteligencia artificial del Municipio y los inspectores que ya existen.')
# 4 · Ordenanza 14, artículo 6
rep('anexo-14', 'El registro no da lugares ni horarios exclusivos.',
    'Cada instructor registrado tiene un lugar y un horario garantizados, que asigna la inteligencia artificial del Municipio; fuera de ese horario, el lugar es de uso común. Los instructores registrados no pagan el derecho por ocupación o uso de espacios públicos de la Ordenanza Impositiva. Durante la clase, nadie puede estacionar ni ocupar ese lugar; quien lo haga comete una falta, con la multa que fija la reglamentación.')
# 5 · lo que tiene que confirmar un abogado
rep('metodo-abogado', 'El registro de instructores privados sin sitios ni horarios exclusivos, y la prioridad del 75% para los vecinos de San Isidro.',
    'El lugar y el horario garantizados de los instructores registrados, la multa a quien estacione u ocupe ese lugar durante la clase, y la prioridad del 75% para los vecinos de San Isidro.')
# 6 · fuentes del 5.5
f0 = by['5.5']['fuentes']; add = ' Lo que se puede cobrar por usar un espacio público: Ordenanza Impositiva 2026 (Ordenanza 9415), artículo 17, inciso d.1; lo recaudado en 2025, ejecución de recursos del Municipio, «Ocupación y uso de espacios y espectáculos públicos».'
by['5.5']['fuentes'] = f0.rstrip() + add; log.append(('5.5', 'fuentes (al final)', add.strip()))
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
# controles
for eid in ['5.5-r11', 'anexo-14', 'metodo-abogado']:
    e = by[eid]; ps = e['texto'].split('\n\n')
    for key, ms in e.get('marcas', {}).items():
        for a, z, _ in ms: assert 0 <= a < z <= len(ps[int(key)]), (eid, key)
txt = ' '.join(x[2] for x in log).lower()
for bad in ['plata', 'mafia', 'sobreprecio', 'candidat', ' partido ']: assert bad not in txt, bad
for eid in ['5.5-r11']:
    for p in by[eid]['texto'].split('\n\n'):
        body = re.sub(r'^\d+ · ', '', p); s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', body) if x]
        f = [x.split()[0].lower() for x in s]
        dup = {w for w in f if f.count(w) > 1}; bad = [x[:30] for x in s if re.match(r'^(Y|Que)\b', x)]
        if dup or bad: print('REGLA', dup, bad, p[:60])
Path(S + '/log_instructores.json').write_text(json.dumps(log, ensure_ascii=False, indent=1))
print(len(log), 'cambios')
