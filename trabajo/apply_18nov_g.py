"""Actualización del 19/11/2026, parte G: cámaras (decisión de Nick, 19/11): la revisión anual puede mudar una cámara a
otro lugar con choques, pero la cantidad de cámaras no baja nunca. Se saca el ejemplo de Nueva Gales del Sur, que sacó
cámaras. Re-ejecutable sólo una vez: si ya se aplicó, se detiene sin tocar nada.
Uso: python3 trabajo/apply_18nov_g.py [ruta de programa.json, para probar sobre una copia]
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
if 'Nunca baja la cantidad de cámaras' in by['5.11-r1']['texto']:
    raise SystemExit('ya aplicado: no se toca nada')


def rep(eid, old, new):
    """Cambia old por new en el único párrafo que lo tiene; corre las marcas que siguen y se niega si toca una."""
    e = by[eid]; ps = e['texto'].split('\n\n')
    hits = [i for i, p in enumerate(ps) if old in p]
    assert len(hits) == 1 and ps[hits[0]].count(old) == 1, (eid, old[:60], hits)
    i = hits[0]; pos = ps[i].index(old); end = pos + len(old); delta = len(new) - len(old)
    for m in e.get('marcas', {}).get(str(i), []):
        if m[0] >= end: m[0] += delta; m[1] += delta
        elif m[1] > pos and delta: raise SystemExit(f'marca dentro del cambio {eid} p{i} {m}')
    ps[i] = ps[i][:pos] + new + ps[i][end:]; e['texto'] = '\n\n'.join(ps)


rep('5.11-r1', 'Una vez por año, la inteligencia artificial del Municipio revisará cada cámara para decidir si sigue o se'
    ' saca. Nueva Gales del Sur, en Australia, hizo una revisión así en 2023, y sacó 3 de sus 92 cámaras fijas.',
    'Una vez por año, la inteligencia artificial del Municipio revisará cada cámara, y la que ya no baje los choques se'
    ' va a mudar a otro lugar donde los haya. Nunca baja la cantidad de cámaras.')
old = 'la revisión anual (92 fijas, 3 retiradas en 2023) y el fondo de seguridad vial, Nueva Gales del Sur'
assert by['5.11']['fuentes'].count(old) == 1
by['5.11']['fuentes'] = by['5.11']['fuentes'].replace(old, 'el fondo de seguridad vial, Nueva Gales del Sur')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
