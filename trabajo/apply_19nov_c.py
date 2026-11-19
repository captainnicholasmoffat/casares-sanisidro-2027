"""Actualización del 19/11/2026, parte C: la promesa de no subir la tasa se aclara para casas y comercios, porque la
tasa del baldío sube de 26 a 48 por mil (decisión de Nick, 19/11). Re-ejecutable sólo una vez.
Uso: python3 trabajo/apply_19nov_c.py [ruta de programa.json, para probar sobre una copia]
Base: parte E: corrección del coordinador sobre el tercer remate. Vuelve atrás «el Municipio
no pide la venta sin base» (parte D), porque choca con la decisión de Nick («Quien no paga, pierde el terreno»): si nadie
ofrece en el segundo remate (60%), el Municipio pide la venta sin base (Ley 13.406, art. 16), y el terreno se vende. Si
lo compra el mismo dueño, no se salva: la obligación de construir sigue anotada en el Registro con los mismos plazos
(Decreto-Ley 8912/77, art. 85), y la tasa más alta y el recargo siguen corriendo. No se promete que el Municipio se
quede con el terreno. Re-ejecutable sólo una vez: si ya se aplicó, se detiene sin tocar nada.
Uso: python3 trabajo/apply_18nov_e.py [ruta de programa.json, para probar sobre una copia]"""
import json, sys
from pathlib import Path
P = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
if 'para casas y comercios' in by['cierre']['texto']:
    raise SystemExit('ya aplicado: no se toca nada')


def rep(eid, old, new):
    """Cambia old por new en el único párrafo que lo tiene; corre las marcas que siguen y se niega si toca una."""
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[0] <= pos and m[1] >= end: m[1] += delta  # la marca contiene todo el cambio: crece con él
        elif m[1] > pos and delta: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


rep('proponemos', 'sin subir el porcentaje de la tasa de servicios generales y sin tomar deuda.',
    'sin subir el porcentaje de la tasa de servicios generales para casas y comercios, y sin tomar deuda.')
rep('cierre', 'No hace falta subir el porcentaje de la tasa, ni tomar deuda,',
    'No hace falta subir el porcentaje de la tasa para casas y comercios, ni tomar deuda,')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
