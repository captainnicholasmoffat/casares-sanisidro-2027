"""Arma web/index.html (borrador: portada con scroll de la costanera + los nueve puntos).
Uso: python3 -I build_index.py <ruta nueve.json>
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads(Path(sys.argv[1]).read_text())
E = html.escape

items_html = []
for it in data["items"]:
    cap = (
        f'<span class="chip">Capítulo {it["cap"]}</span>' if it["cap"] else ""
    )
    items_html.append(
        f'''<li class="pt">
  <details>
    <summary><span class="pt-n">{it["n"]}</span><span class="pt-lead">{E(it["lead"])}</span><span class="pt-tog" aria-hidden="true"></span></summary>
    <div class="pt-body"><p>{E(it["body"])}</p>{cap}</div>
  </details>
</li>'''
    )

cien = data["cien"]
assert cien.startswith("Los primeros cien días. ")
cien_body = cien[len("Los primeros cien días. "):]

tpl = (HERE / "index.tpl.html").read_text()
out = (
    tpl.replace("{{INTRO}}", E(data["intro"]))
    .replace("{{ITEMS}}", "\n".join(items_html))
    .replace("{{CIEN}}", E(cien_body))
)
(HERE / "index.html").write_text(out)
print("ok", len(out))
