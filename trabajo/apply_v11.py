import json
from pathlib import Path
P = Path('/home/claude/proyecto/web/data/programa.json'); d = json.loads(P.read_text()); by = {e['id']: e for e in d}
log = []
def rep_text(eid, old, new):
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1, (eid, old[:50], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    ps[i] = ps[i].replace(old, new, 1)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and not (new.startswith(old) and m[1] <= end): raise SystemExit(f'marca dentro del cambio en {eid} p{i}: {m}')
    e['texto'] = '\n\n'.join(ps); log.append((eid, 'texto', old, new))
def rep_cuadro(eid, ctitle, old, new):
    cs = [c for c in by[eid]['cuadros'] if c['titulo'].startswith(ctitle)]
    assert len(cs) == 1 and cs[0]['texto'].count(old) == 1, (eid, ctitle, old[:50])
    cs[0]['texto'] = cs[0]['texto'].replace(old, new); log.append((eid, ctitle, old, new))
rep_text('5.3', 'En los cuatro años del mandato van a ser dieciséis en total, porque los primeros egresados recién salen en el mes 27.',
         'En los cuatro años del mandato van a ser dieciséis en total: 3, 3, 5 y 5 en las convocatorias de los meses 27, 33, 39 y 45, porque los primeros egresados recién salen en el mes 27 y los grupos crecen de a poco.')
rep_cuadro('6.4', 'Cuadro 42', 'Su personal técnico sale de la tecnicatura: primero los pasantes, y desde el mes 27, los egresados (5.7)',
           'Su personal técnico sale de la tecnicatura (5.7): desde el mes 27, los egresados. Hasta entonces la atiende el equipo técnico de las cámaras, con el que trabaja junta')
rep_text('anexo-4', 'Tampoco tienen validez la clausura ni la habilitación que surjan de esa inspección.',
         'Tampoco tienen validez la clausura ni la habilitación que surjan de esa inspección. Esta consecuencia rige desde que el sistema de grabación sellada funciona en todas las inspecciones.')
rep_cuadro('6.4', 'Cuadro 42', 'anula la clausura o la habilitación que salga de una inspección sin grabación sellada',
           'anula la clausura o la habilitación que salga de una inspección sin grabación sellada, desde que empiezan las grabaciones (mes 9)')
rep_text('anexo', 'Ninguna va más allá de lo que un municipio bonaerense puede aprobar.',
         'Ninguna va más allá de lo que un municipio bonaerense puede aprobar. Faltan dos cambios menores, que se redactan en los meses 4 a 6 (cuadro 42): la ordenanza de los foodtrucks y el cambio del artículo 9 de la Ordenanza 5824.')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
out = ['# Cambios de la versión 1.1 ya aplicados en la web (12 de octubre de 2026)', '', 'Aprobados por Nick (00:39). El worker del documento tiene que copiar estos textos tal cual al PDF, la A4 y el Excel.', '']
for eid, where, old, new in log:
    out += [f'## {eid} · {where}', f'- Antes: «{old}»', f'- Después: «{new}»', '']
Path('/home/claude/proyecto/CAMBIOS_WEB_V1_1.md').write_text('\n'.join(out))
print(len(log), 'cambios')
