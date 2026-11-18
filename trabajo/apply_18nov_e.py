"""Actualización del 18/11/2026, parte E: corrección del coordinador sobre el tercer remate. Vuelve atrás «el Municipio
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
if 'el Municipio pide venderlo sin base' in by['5.4-r3']['texto']:
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


assert 'Quien no paga, pierde el terreno' in by['5.4-r3']['texto']
rep('5.4-r3', 'Comprarse el propio terreno en el remate tampoco sirve: lo que paga cancela la deuda, pero la obligación de'
    ' construir sigue anotada, con los mismos plazos (artículo 85). Además, el remate tiene una base del 80% de la'
    ' tasación, y del 60% si en el primero nadie ofrece (Ley 13.406, artículo 16). Si en el segundo tampoco hay ofertas,'
    ' el Municipio no pide venderlo sin base, aunque la ley se lo permite: el terreno sigue embargado, la deuda y el'
    ' recargo siguen corriendo, y la obligación de construir sigue anotada.',
    'Además, el remate tiene una base del 80% de la tasación, y del 60% si en el primero nadie ofrece; si en el segundo'
    ' tampoco hay ofertas, el Municipio pide venderlo sin base, y el terreno se vende (Ley 13.406, artículo 16).'
    ' Comprarse el propio terreno en el remate no lo salva: lo que paga cancela la deuda, pero la obligación de construir'
    ' sigue anotada en el Registro, con los mismos plazos (artículo 85), y la tasa más alta y el recargo siguen corriendo.')
rep('anexo-21', 'Lo pagado en la subasta cancela la deuda, y la obligación de edificar subsiste con los mismos plazos,'
    ' conforme el artículo 85, inciso d), del Decreto-Ley 8912/77. En la subasta, el Departamento Ejecutivo no solicita la'
    ' venta sin limitación de precio del artículo 16 de la Ley 13.406: si la segunda subasta fracasa, el inmueble sigue'
    ' embargado y el gravamen sigue corriendo.',
    'Lo pagado en la subasta cancela la deuda, y la obligación de edificar subsiste con los mismos plazos, conforme el'
    ' artículo 85, inciso d), del Decreto-Ley 8912/77, aunque el comprador sea el mismo propietario; también siguen la tasa'
    ' del artículo 5 y el gravamen del artículo 4. Si la segunda subasta fracasa por falta de postores, el Departamento'
    ' Ejecutivo solicita la venta sin limitación de precio del artículo 16 de la Ley 13.406.')

P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
