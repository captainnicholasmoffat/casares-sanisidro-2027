"""Arma web/index.html (diseño B2 aprobado) desde index_b.tpl.html y nueve.json.
Uso: python3 -I build_b.py <ruta nueve.json>
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads(Path(sys.argv[1]).read_text())
nueve = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
tpl = (HERE / "index_b.tpl.html").read_text()
out = tpl.replace("{{NUEVE_JSON}}", nueve).replace("{{INTRO}}", html.escape(data["intro"]))
assert "{{" not in out
(HERE / "index.html").write_text(out)
print("ok", len(out.encode()))
