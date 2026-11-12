"""Revisión mensual de la web de San Isidro: baja de la base D1 lo que dejó la gente desde la última corrida.

Uso: python3 -I revision/extraer.py <carpeta de salida> [--desde AAAA-MM-DD]
Necesita CLOUDFLARE_API_TOKEN en el entorno. No escribe nada en el repositorio: las preguntas de la gente
quedan sólo en la carpeta de salida (temporal), porque la nota de privacidad dice que se guardan hasta seis meses en la base.

Salida: <carpeta>/datos.json con
  preguntas  (sin las pruebas automáticas), con la respuesta, si el chat dijo que no lo cubre, si se cortó, y el «¿Le faltó algo?»
  mensajes   de «Escribinos» (sin el mail)
  resumen    números del período
  salud      estado de cada página y una pregunta real de prueba
"""
import datetime
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ACCOUNT = "b9ff0a47e862fc50eccca51708ec9fc7"
DB = "87a60bc8-908e-4ea3-b0ce-1f8592d26fd5"  # sanisidro2027 (sitio/wrangler.toml)
SITE = "https://sanisidro2027.pages.dev"
PAGES = ["/", "/cuentas/", "/despliegue/", "/contacto/", "/data/programa.json"]
TZ = datetime.timezone(datetime.timedelta(hours=-3))
REPO = Path(__file__).resolve().parent.parent
PRUEBA = re.compile(r"^\s*\[PRUEBA AUTOM", re.I)


def d1(sql, params=None):
    token = os.environ["CLOUDFLARE_API_TOKEN"]
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{DB}/query",
        data=json.dumps({"sql": sql, "params": params or []}).encode(),
        headers={"Authorization": "Bearer " + token, "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if not out.get("success"):
        raise SystemExit("D1 respondió con error: " + json.dumps(out.get("errors")))
    return out["result"][0]["results"]


def ultima_corrida():
    reg = REPO / "revision" / "REGISTRO.md"
    fechas = re.findall(r"^## Corrida del (\d{4}-\d{2}-\d{2})", reg.read_text(), re.M) if reg.exists() else []
    return max(fechas) if fechas else "2026-10-12"


def get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read().decode("utf-8", "replace")


def salud():
    out = []
    for p in PAGES:
        try:
            code, _ = get(SITE + p)
        except Exception as e:  # noqa: BLE001 — se informa tal cual
            code = str(e)
        out.append({"pagina": p, "estado": code})
    try:
        code, body = get(SITE + "/api/ask", json.dumps({"question": "[PRUEBA AUTOMATICA] ¿Qué propone el programa para el comercio chico? Una línea."}).encode(),
                         {"content-type": "application/json", "origin": SITE})
        ok = code == 200 and "text_delta" in body and "message_stop" in body
        out.append({"pagina": "/api/ask", "estado": code, "contesta": ok})
    except Exception as e:  # noqa: BLE001
        out.append({"pagina": "/api/ask", "estado": str(e), "contesta": False})
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    dest = Path(sys.argv[1]); dest.mkdir(parents=True, exist_ok=True)
    desde = sys.argv[sys.argv.index("--desde") + 1] if "--desde" in sys.argv else ultima_corrida()
    t0 = int(datetime.datetime.fromisoformat(desde).replace(tzinfo=TZ).timestamp() * 1000)

    filas = d1("SELECT id, ts, conn, pagina, pregunta, respuesta, fuentes, sin_dato, cortada, feedback FROM preguntas WHERE ts >= ?1 ORDER BY ts", [t0])
    pruebas = [f for f in filas if PRUEBA.match(f["pregunta"])]
    preguntas = [f for f in filas if not PRUEBA.match(f["pregunta"])]
    for f in preguntas:
        f["fecha"] = datetime.datetime.fromtimestamp(f.pop("ts") / 1000, TZ).strftime("%Y-%m-%d %H:%M")
        f["persona"] = (f.pop("conn") or "")[:8]  # ya es un hash; sólo sirve para ver repeticiones
    mensajes = d1("SELECT ts, pagina, texto FROM mensajes WHERE ts >= ?1 ORDER BY ts", [t0])
    for m in mensajes:
        m["fecha"] = datetime.datetime.fromtimestamp(m.pop("ts") / 1000, TZ).strftime("%Y-%m-%d %H:%M")

    resumen = {
        "desde": desde,
        "hasta": datetime.datetime.now(TZ).strftime("%Y-%m-%d %H:%M"),
        "preguntas": len(preguntas),
        "personas": len({f["persona"] for f in preguntas}),
        "no_lo_cubre": sum(1 for f in preguntas if f["sin_dato"]),
        "cortadas": sum(1 for f in preguntas if f["cortada"]),
        "le_falto": sum(1 for f in preguntas if f["feedback"]),
        "mensajes": len(mensajes),
        "pruebas_excluidas": len(pruebas),
    }
    out = {"resumen": resumen, "salud": salud(), "preguntas": preguntas, "mensajes": mensajes}
    (dest / "datos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(resumen, ensure_ascii=False))
    for s in out["salud"]:
        print(s)


if __name__ == "__main__":
    main()
