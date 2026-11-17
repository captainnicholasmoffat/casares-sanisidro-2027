"""Actualización del 17/11/2026, parte G: el cuadro 43 (qué no prometemos) suma que el Municipio no construye viviendas
(decisión de Nick del 17/11)."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/data/programa.json'
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
c = [c for c in by['6.5']['cuadros'] if c['titulo'].startswith('Cuadro 43')][0]
ancla = '\nUn refugio propio para víctimas de violencia |'; assert c['texto'].count(ancla) == 1
fila = ('\nConstruir viviendas del Municipio | Construir con dinero propio no entra en las cuentas: el presupuesto de vivienda de este '
        'programa ya tiene destino (5.4). Cuando la Provincia abra un plan, la inteligencia artificial del Municipio va a avisar, '
        'y el Municipio se va a anotar.')
c['texto'] = c['texto'].replace(ancla, fila + ancla, 1)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('ok')
