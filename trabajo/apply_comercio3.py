import json, re
from pathlib import Path
P = Path('/home/claude/proyecto/web/data/programa.json'); d = json.loads(P.read_text()); by = {e['id']: e for e in d}
def rep(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]; assert len(hits) == 1, (eid, old[:40], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)
rep('5.11-r3', 'El comercio chico paga una cuota fija por mes', 'Hoy, el comercio chico paga una cuota fija por mes')
rep('5.11-r3', 'Le aplica sola lo más barato', 'También le aplica sola lo más barato')
rep('5.11-r3', 'Le arma la declaración jurada, sin trámites.', 'Además, le arma la declaración jurada, sin trámites.')
rep('5.11-r4', 'El comercio que dona lo que le sobra a los comedores suma puntaje', 'Si un comercio le da a los comedores lo que le sobra, suma puntaje')
rep('5.11-r5', 'La ley permite donar alimentos', 'Hoy la ley permite donar alimentos')
rep('5.11-r5', 'La Provincia adhirió e invitó', 'Además, la Provincia adhirió e invitó')
rep('5.11-r6', 'Un programa nacional hizo 219', 'Ya se probó: un programa nacional hizo 219')
rep('anexo-18', 'El comercio que dona alimentos suma puntaje', 'Todo comercio que dona alimentos suma puntaje')
rep('anexo-18', 'La inteligencia artificial del Municipio marca los precios', 'Además, la inteligencia artificial del Municipio marca los precios')
rep('3.6', 'La tasa es el 29% de lo que entra al Municipio.', 'Esa tasa es el 29% de lo que entra al Municipio.')
rep('3.6', 'La propuesta para el comercio chico (5.11)', 'Nuestra propuesta para el comercio chico (5.11)')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
# control: ningún párrafo nuevo con dos oraciones que empiezan igual, ni con «Y» o «Que»
ids = ['5.11-r3','5.11-r4','5.11-r5','5.11-r6','anexo-17','anexo-18']
paras = [(i, p) for i in ids for p in by[i]['texto'].split('\n\n')]
paras += [('5.11', by['5.11']['texto'].split('\n\n')[5]), ('3.6', by['3.6']['texto'].split('\n\n')[4]), ('3.4', by['3.4']['texto'].split('\n\n')[8])]
bad = 0
for i, p in paras:
    body = re.sub(r'^\d+ · ', '', p); body = re.sub(r'^\d+\. ', '', body)
    s = [x for x in re.split(r'(?<=[.:])\s+(?=[A-ZÁÉÍÓÚÑ¿«])', body) if x]
    f = [x.split()[0].lower() for x in s]
    if any(f.count(w) > 1 for w in f) or any(re.match(r'^(Y|Que)\b', x) for x in s): bad += 1; print('FALLA', i, p[:60])
print('párrafos con falla:', bad)
for e in d:
    for k, ms in e.get('marcas', {}).items():
        ps = e['texto'].split('\n\n')
        for a, z, _ in ms: assert 0 <= a < z <= len(ps[int(k)]), (e['id'], k)
