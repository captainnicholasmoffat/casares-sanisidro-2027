"""Actualización del 17/11/2026, parte H: la nota del cuadro 42 decía «No hay ninguna obra elegida por los vecinos antes
del primer ciclo de asambleas», y el chat la leía como que las obras no tienen fecha. Ahora dice cuándo se eligen."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text())
c = [c for e in d if e['id'] == '6.4' for c in e['cuadros'] if c['titulo'].startswith('Cuadro 42')][0]
old = 'No hay ninguna obra elegida por los vecinos antes del primer ciclo de asambleas.'
new = 'Los vecinos eligen las obras del año 1 en la primera ronda de asambleas, en el mes 3.'
assert c['texto'].count(old) == 1; c['texto'] = c['texto'].replace(old, new)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
