"""Chat, 18/11/2026, parte B: las reglas del chat siguen la tercera tanda del programa (apply_18nov_d.py): la delegación
de la zona o la más cercana, la formación gratis de los acompañantes (un año lectivo; acompañan cerca del mes 37) y el
remate sin venta sin base. Sólo cambia cómo contesta el chat. Re-ejecutable: si ya se aplicó, no cambia nada."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/ajustes_chat.json'
a = json.loads(P.read_text())
CAMBIOS = [
    ('en cada asamblea y en la delegación de la zona; así se vota',
     'en cada asamblea y en la delegación de la zona o la más cercana; así se vota'),
    ('si no paga, cobro judicial con embargo y remate, y pierde el terreno;',
     'si no paga, cobro judicial con embargo y remate; si en el remate nadie ofrece, el Municipio no lo vende sin base ni'
     ' se queda con el terreno: sigue embargado y la deuda sigue corriendo;'),
    ('sin perder su sueldo (5.3 y 5.6). No digas que los acompañantes empiezan en el primer año.',
     'sin perder su sueldo (5.3 y 5.6). Para ser acompañante se forma gratis, en horario de trabajo, durante un año lectivo'
     ' en un instituto superior público, y empieza a acompañar cerca del mes 37. No digas que los acompañantes empiezan en'
     ' el primer año.'),
]
texto = json.dumps(a['reglas'], ensure_ascii=False)
if CAMBIOS[0][1] in texto:
    raise SystemExit('ya aplicado: no se toca nada')
for old, new in CAMBIOS:
    hits = [i for i, r in enumerate(a['reglas']) if old in r]
    assert len(hits) == 1, old[:50]
    a['reglas'][hits[0]] = a['reglas'][hits[0]].replace(old, new, 1)
P.write_text(json.dumps(a, ensure_ascii=False, indent=2) + '\n'); print('reglas', len(a['reglas']))
