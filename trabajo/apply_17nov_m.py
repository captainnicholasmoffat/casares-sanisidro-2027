"""Actualización del 17/11/2026, parte M (revisión completa): la encuesta de UADE (CIS, informe de situación habitacional,
2026) encuestó a 1.040 personas de 17 a 75 años, con 27 de promedio; el 44% es de todos los encuestados («El 44% de los
encuestados vive con su madre o padre»), no sólo de los jóvenes. Verificado en el PDF de UADE el 17/11/2026."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); e = [x for x in d if x['id'] == '5.4-r1'][0]
old = 'Según una encuesta nacional, el 44% de los jóvenes vive con sus padres,'
new = 'Según una encuesta nacional a personas de 17 a 75 años, con una edad promedio de 27, el 44% vive con sus padres,'
ps = e['texto'].split('\n\n'); i = [k for k, p in enumerate(ps) if old in p]; assert len(i) == 1; i = i[0]
pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
for m in e.get('marcas', {}).get(str(i), []):
    if m[0] >= end: m[0] += delta; m[1] += delta
    elif m[1] > pos: raise SystemExit(f'marca {m}')
ps[i] = ps[i].replace(old, new, 1); e['texto'] = '\n\n'.join(ps)
f_old = 'informe de situación habitacional (1.040 encuestados de todo el país;'
assert e['fuentes'].count(f_old) == 1
e['fuentes'] = e['fuentes'].replace(f_old, 'informe de situación habitacional (1.040 encuestados de todo el país, de 17 a 75 años;', 1)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
