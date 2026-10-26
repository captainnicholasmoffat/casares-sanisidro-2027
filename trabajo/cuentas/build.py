import json, sys
from pathlib import Path
here = Path(__file__).resolve().parent
d = json.loads((here / 'cuentas.json').read_text())
t = (here / 'cuentas.tpl.html').read_text()
out = t.replace('/*DATA*/null', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))
(here / 'cuentas.html').write_text(out); print('ok', len(out))
