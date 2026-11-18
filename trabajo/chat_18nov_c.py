"""Chat, 18/11/2026, parte C: la regla de los terrenos sigue la corrección del tercer remate (apply_18nov_e.py): si nadie
ofrece en el segundo remate, el Municipio pide venderlo sin base y el dueño pierde el terreno; si lo compra él mismo, no
se salva. Sólo cambia cómo contesta el chat. Re-ejecutable: si ya se aplicó, no cambia nada."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/ajustes_chat.json'
a = json.loads(P.read_text())
OLD = ('si no paga, cobro judicial con embargo y remate; si en el remate nadie ofrece, el Municipio no lo vende sin base ni'
       ' se queda con el terreno: sigue embargado y la deuda sigue corriendo; venderlo, o comprarlo él mismo en el remate,'
       ' no lo salva, porque la obligación de construir sigue anotada con los mismos plazos')
NEW = ('si no paga, cobro judicial con embargo y remate, y pierde el terreno: si en el segundo remate nadie ofrece, el'
       ' Municipio pide venderlo sin base (el Municipio no se queda con el terreno); venderlo, o comprarlo él mismo en el'
       ' remate, no lo salva, porque la obligación de construir sigue anotada con los mismos plazos, y la tasa más alta y'
       ' el recargo siguen corriendo')
if any(NEW in r for r in a['reglas']):
    raise SystemExit('ya aplicado: no se toca nada')
hits = [i for i, r in enumerate(a['reglas']) if OLD in r]; assert len(hits) == 1
a['reglas'][hits[0]] = a['reglas'][hits[0]].replace(OLD, NEW, 1)
P.write_text(json.dumps(a, ensure_ascii=False, indent=2) + '\n'); print('reglas', len(a['reglas']))
