"""Prueba el chat de una dirección del sitio con las preguntas de revision/pruebas.json.

Uso: python3 -I revision/probar.py <dirección>   (por ejemplo https://anticipo.sanisidro2027.pages.dev)
Cada pregunta va marcada «[PRUEBA AUTOMATICA]» para que la revisión mensual no la cuente como de la gente.
Cuesta unos 3 centavos de dólar por pregunta. Sale con error si alguna falla.
"""
import json
import sys
import urllib.request
from pathlib import Path

PALABRAS_PROHIBIDAS = ["plata", "mafia", "sobreprecio"]


def preguntar(base, q):
    req = urllib.request.Request(base.rstrip("/") + "/api/ask",
                                 data=json.dumps({"question": "[PRUEBA AUTOMATICA] " + q}).encode(),
                                 headers={"content-type": "application/json", "origin": base.rstrip("/"),
                                          "user-agent": "Mozilla/5.0 (revision-mensual-sanisidro2027)"})
    with urllib.request.urlopen(req, timeout=180) as r:
        body = r.read().decode("utf-8", "replace")
    texto, fin = "", False
    for ev in body.split("\n\n"):
        data = "".join(l[5:].strip() for l in ev.split("\n") if l.startswith("data:"))
        if not data:
            continue
        try:
            j = json.loads(data)
        except ValueError:
            continue
        if j.get("type") == "content_block_delta" and j.get("delta", {}).get("type") == "text_delta":
            texto += j["delta"]["text"]
        if j.get("type") == "message_stop":
            fin = True
    return texto, fin


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    base = sys.argv[1]
    casos = json.loads((Path(__file__).resolve().parent / "pruebas.json").read_text())
    fallas = 0
    for c in casos:
        try:
            texto, fin = preguntar(base, c["pregunta"])
        except Exception as e:  # noqa: BLE001 — se informa tal cual
            texto, fin = "ERROR: " + str(e), False
        respuesta = texto.split("\nFUENTES:")[0].lower()
        problemas = []
        if not fin or not texto.strip():
            problemas.append("no terminó de contestar")
        problemas += ["dice «" + p + "»" for p in PALABRAS_PROHIBIDAS if p in respuesta.split()]
        problemas += ["no menciona «" + p + "»" for p in c.get("debe_decir", []) if p.lower() not in respuesta]
        problemas += ["dice «" + p + "»" for p in c.get("no_debe_decir", []) if p.lower() in respuesta]
        fallas += bool(problemas)
        print(("FALLA " if problemas else "ok    ") + c["pregunta"][:70] + ("  →  " + "; ".join(problemas) if problemas else ""))
    print(f"{len(casos) - fallas} de {len(casos)} bien")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
