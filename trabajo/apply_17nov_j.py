"""Actualización del 17/11/2026, parte J: los seis puntos nuevos de «Lo que tiene que confirmar un abogado» van en el
orden de las secciones, como los demás, y con el número de sección en negrita."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); e = [x for x in d if x['id'] == 'metodo-abogado'][0]
ps = e['texto'].split('\n\n'); mk = e.get('marcas', {})
items = [(p, mk.get(str(i))) for i, p in enumerate(ps)]
cab, resto = items[0], items[1:]
def clave(p):
    m = re.match(r'• (\d+)\.(\d+)\.', p)
    return (int(m.group(1)), int(m.group(2))) if m else (99, 0)        # «Anexo.» al final
for k, (p, m) in enumerate(resto):
    if m is None:
        n = len(re.match(r'• (\d+\.\d+\.)', p).group(1))
        resto[k] = (p, [[2, 2 + n, 'b']])
resto.sort(key=lambda x: clave(x[0]))                                   # estable: los de una misma sección siguen en su orden
nuevos = [cab] + resto
e['texto'] = '\n\n'.join(p for p, _ in nuevos)
e['marcas'] = {str(i): m for i, (p, m) in enumerate(nuevos) if m}
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
for i, (p, m) in enumerate(nuevos): print(i, m, p[:40])
