"""Actualización del 17/11/2026, parte C: arreglos de redacción en tres celdas de cuadros (oraciones que empezaban igual)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
def cuadro(eid, old, new, ci=0):
    c = by[eid]['cuadros'][ci]; assert c['texto'].count(old) == 1, (eid, old[:60]); c['texto'] = c['texto'].replace(old, new, 1)
cuadro('6.4', 'La 20 crea la garantía de alquiler', 'Otra, la 20, crea la garantía de alquiler')
cuadro('6.4', 'Nota: las fechas de este cuadro son las de entrada de cada ordenanza; cuándo se aprueba cada una lo decide el Concejo. La comisión se forma en los meses 4 a 6', 'Nota: la comisión se forma en los meses 4 a 6')
cuadro('6.4', 'para que cada agente tenga un teléfono que sirva.', 'para que cada agente tenga un teléfono que sirva. Las fechas de este cuadro son las de entrada de cada ordenanza: cuándo se aprueba cada una lo decide el Concejo.')
cuadro('6.5', 'La partida propia de género entra en el presupuesto siguiente a su ordenanza. La conexión de cada casa se paga a medida que la obra vecinal hace las redes de la calle. La transmisión de las asambleas empieza con la inteligencia artificial del Municipio.',
       'Para la partida propia de género, hace falta el presupuesto siguiente a su ordenanza. Cada casa se conecta a medida que la obra vecinal hace las redes de la calle. Las asambleas se transmiten desde que funciona esa parte de la inteligencia artificial del Municipio.')
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print('ok')
