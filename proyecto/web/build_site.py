"""Arma el sitio propio (Cloudflare Pages) desde la misma plantilla de la página de Claude.
Uso: python3 -I build_site.py <ruta nueve.json>
Salida: /home/claude/proyecto/sitio/public/ y /home/claude/proyecto/sitio/lib/rules.js
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parent
SITE = WEB.parent / "sitio"
data = json.loads(Path(sys.argv[1]).read_text())
tpl = (WEB / "index_b.tpl.html").read_text()

# 1) El chat pasa a la función propia
start = tpl.index("  var sampleP = null, history = [], busy = false, ctl = null;")
end_marker = "      document.querySelectorAll(\".go,.chip-q,.ask-it\").forEach(function(b){ b.disabled = true; });\n    }\n  });\n"
end = tpl.index(end_marker, start) + len(end_marker)
tpl = tpl[:start] + (WEB / "site_adapter.js").read_text() + tpl[end:]

# 2) Mensajes de error propios del sitio
old = '    if (c === "prompt_too_large") return "La pregunta es muy larga. Probá con una más corta.";'
assert old in tpl
tpl = tpl.replace(old, old + '\n    if (c === "no_credits") return "El chat llegó a su límite de este mes. Mientras tanto, podés leer las propuestas y el programa completo más abajo.";'
                  '\n    if (c === "not_configured") return "El chat todavía no está activado. Mientras tanto, podés leer las propuestas y el programa completo más abajo.";'
                  '\n    if (c === "invalid_request") return "No pude procesar esa pregunta. Probá escribirla de otra forma.";'
                  '\n    if (c === "daily_limit") return "El chat llegó al máximo de preguntas de hoy. Volvé mañana. Mientras tanto, podés leer el programa completo más abajo.";')

# 3) Las reglas del chat, del lado del servidor (mismo texto que la página)
m = re.search(r"  var RULES = \[\n(.*?)\n  \]\.join\(\"\\n\"\);", tpl, re.S)
assert m, "no encontré RULES"
(SITE / "lib").mkdir(parents=True, exist_ok=True)
(SITE / "lib" / "rules.js").write_text("// Mismo texto que las reglas de la página (index_b.tpl.html).\nexport const RULES = [\n" + m.group(1) + "\n].join(\"\\n\");\n")

# 3 bis) La búsqueda de pasajes, del lado del servidor: el mismo código que la página
i0 = tpl.index("  var STOP = {};"); i1 = tpl.index("\n", tpl.index("  function cleanInforme")) + 1
j0 = tpl.index("  function buildContext(qSearch){"); j1 = tpl.index("    return {text: out, refs: refs};\n  }\n", j0) + len("    return {text: out, refs: refs};\n  }\n")
(SITE / "lib" / "context.js").write_text("""// GENERADO por web/build_site.py con el mismo código de búsqueda de la página (index_b.tpl.html). No editar a mano.
var CH_P = [], CH_I = [], DF_P = {}, DF_I = {}, AVG_P = 1, AVG_I = 1, READY = null;
""" + tpl[i0:i1] + tpl[j0:j1] + """
async function getJSON(env, origin, path) {
  const r = await env.ASSETS.fetch(new Request(origin + path));
  if (!r.ok) throw new Error(path);
  return r.json();
}
export function ready(env, origin) {
  if (!READY) READY = (async () => {
    const [prog, inv, cu, pl] = await Promise.all([getJSON(env, origin, "/data/programa.json"), getJSON(env, origin, "/data/investigaciones.json").catch(() => []), getJSON(env, origin, "/data/cuentas_ia.json").catch(() => []), getJSON(env, origin, "/data/plan_ia.json").catch(() => [])]);
    (cu || []).concat(pl || []).forEach(function(e){ var plan = /^plan-/.test(e.id); String(e.texto || "").split(/\\n\\n+/).forEach(function(t){ if (t.trim()) CH_P.push({e: e, text: t.trim(), search: e.titulo + " " + e.titulo + (plan ? " plan despliegue cuando fecha quien " : " cuentas modelo fiscal plata presupuesto ") + t, boost: plan ? .85 : 1}); }); });
    prog.forEach(function(e){
      var paras = String(e.texto || "").split(/\\n\\n+/), buf = "";
      function push(t){ if (t.trim()) CH_P.push({e: e, text: t.trim(), search: e.titulo + " " + e.titulo + " " + t, boost: /^glosario-/.test(e.id) ? .7 : 1}); }
      paras.forEach(function(p){ if ((buf + "\\n\\n" + p).length > 1500 && buf) { push(buf); buf = p; } else buf = buf ? buf + "\\n\\n" + p : p; });
      push(buf);
      (e.cuadros || []).forEach(function(c){ push((c.titulo || "Cuadro") + "\\n" + String(c.texto || "").slice(0, 2200)); });
    });
    AVG_P = indexChunks(CH_P, DF_P);
    (inv || []).forEach(function(x){ CH_I.push({x: x, text: String(x.texto || "").slice(0, 1900), search: (x.seccion || "") + " " + (x.temas || []).join(" ") + " " + x.texto, boost: x.descartado ? .6 : 1}); });
    AVG_I = indexChunks(CH_I, DF_I);
    return true;
  })().catch((e) => { READY = null; CH_P = []; CH_I = []; DF_P = {}; DF_I = {}; throw e; });
  return READY;
}
export function context(search) {
  const c = buildContext(search), refs = {};
  for (const k in c.refs) { const r = c.refs[k]; refs[k] = r.kind === "p" ? "p:" + r.e.id : "i:" + r.x.id; }
  return { text: c.text, refs };
}
""")

# 4) Datos de las nueve tarjetas
nueve = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
tpl = tpl.replace("{{NUEVE_JSON}}", nueve).replace("{{INTRO}}", html.escape(data["intro"]))
assert "{{" not in tpl

# 5) Documento completo
cut = tpl.index("</style>") + len("</style>")
head, body = tpl[:cut], tpl[cut:]
desc = "Programa de gobierno San Isidro 2027. Preguntale al programa qué propone para tu barrio, tu trabajo o tu comercio."
doc = (
    '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + head.replace('<meta name="description" content="Programa de gobierno San Isidro 2027. Preguntale al programa.">',
                   '<meta name="description" content="' + desc + '">\n'
                   '<meta property="og:title" content="San Isidro 2027">\n'
                   '<meta property="og:description" content="' + desc + '">\n'
                   '<meta property="og:image" content="https://sanisidro2027.pages.dev/img/og.jpg">\n'
                   '<meta property="og:image:width" content="1200">\n'
                   '<meta property="og:image:height" content="630">\n'
                   '<meta property="og:url" content="https://sanisidro2027.pages.dev/">\n'
                   '<meta property="og:type" content="website">')
    + '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
    + '</head>\n<body>\n' + body + '\n' + (WEB / "menu_movil.html").read_text() + '\n</body>\n</html>\n'
)
pub = SITE / "public"
(pub / "data").mkdir(parents=True, exist_ok=True)
(pub / "img").mkdir(parents=True, exist_ok=True)
(pub / "index.html").write_text(doc)
for f in ["programa.json", "investigaciones.json"]:
    shutil.copy(WEB / "data" / f, pub / "data" / f)
for f in json.loads((WEB / "img" / "fotos.json").read_text())["fotos"]:
    if f.get("en_programa") or f["archivo"] == "f_estacion":
        for s in ("800", "1600"):
            shutil.copy(WEB / "img" / f"{f['archivo']}-{s}.webp", pub / "img" / f"{f['archivo']}-{s}.webp")
for g in (WEB / "img").glob("g_*.webp"):
    shutil.copy(g, pub / "img" / g.name)
shutil.copy(WEB / "img" / "og.jpg", pub / "img" / "og.jpg")
(pub / "panel").mkdir(exist_ok=True)
shutil.copy(WEB / "panel.tpl.html", pub / "panel" / "index.html")
(pub / "contacto").mkdir(exist_ok=True)
shutil.copy(WEB / "contacto.tpl.html", pub / "contacto" / "index.html")
for f in ["favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png"]:
    shutil.copy(WEB / "img" / "icono" / f, pub / f)
(pub / "despliegue").mkdir(exist_ok=True)
_d = (WEB / "despliegue.tpl.html").read_text(); assert _d.count("</body>") == 1
(pub / "despliegue" / "index.html").write_text(_d.replace("</body>", (WEB / "menu_movil.html").read_text() + "\n</body>"))
shutil.copy(WEB.parent / "despliegue" / "acciones.json", pub / "data" / "acciones.json")
# El plan de despliegue, en textos cortos para la IA (una acción por texto)
import datetime as _dt
_MES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
def _f(d):
    x = _dt.date.fromisoformat(d); return f"{x.day} de {_MES[x.month - 1]} de {x.year}"
_acc = json.loads((WEB.parent / "despliegue" / "acciones.json").read_text()); _by = {a["code"]: a for a in _acc}; _plan = []
for a in _acc:
    cuando = ("Es un hito: " + _f(a["start"]) + ".") if a["milestone"] else ("Empieza el " + _f(a["start"]) + " y termina el " + _f((_dt.date.fromisoformat(a["finish"]) - _dt.timedelta(days=1)).isoformat()) + f" ({a['dur']} días hábiles).")
    t = [f"Acción {a['code']} del plan de despliegue, línea «{a['stream'].split(' ', 1)[1]}»: {a['task']}.", cuando, f"Responsable: {a['owner']}. Equipo: {a['team']}."]
    if a.get("critical"): t.append("Está en el camino crítico: si se atrasa, se corre una fecha del programa.")
    if a.get("decision"): t.append("La decisión que pide: " + a["decision"])
    if a.get("steps"): t.append("Qué se hace: " + a["steps"])
    if a.get("needs"): t.append("Necesita antes: " + "; ".join(n["code"] + " (" + _by[n["code"]]["task"] + ")" for n in a["needs"] if n["code"] in _by) + ".")
    if a.get("note"): t.append("Nota: " + a["note"])
    if a.get("fuente"): t.append("Sale del programa: " + a["fuente"] + ".")
    _plan.append({"id": "plan-" + a["code"], "code": a["code"], "capitulo": "Plan de despliegue", "titulo": a["code"] + " · " + a["task"], "texto": " ".join(t)})
(pub / "data" / "plan_ia.json").write_text(json.dumps(_plan, ensure_ascii=False))
(pub / "_headers").write_text(
    "/*\n"
    "  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; object-src 'none'\n"
    "  X-Frame-Options: SAMEORIGIN\n"
    "  Strict-Transport-Security: max-age=31536000\n"
    "  Permissions-Policy: microphone=(self), camera=(), geolocation=(), payment=()\n"
    "  X-Content-Type-Options: nosniff\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
    "/panel/*\n  X-Robots-Tag: noindex, nofollow\n  Cache-Control: no-store\n"
    "/data/*\n  Cache-Control: public, max-age=3600\n/img/*\n  Cache-Control: public, max-age=86400\n/data/*.xlsx\n  Content-Disposition: attachment\n")
# Las cuentas: todo sale del Excel del modelo fiscal
import subprocess
CU = WEB / "cuentas"
subprocess.run([sys.executable, "-I", str(CU / "extract.py"), str(CU / "modelo_fiscal.xlsx"), str(CU / "cuentas.json")], check=True)
subprocess.run([sys.executable, "-I", str(CU / "ia.py"), str(CU / "cuentas.json"), str(WEB / "data" / "cuentas_ia.json")], check=True)
subprocess.run([sys.executable, "-I", str(CU / "check.py"), str(CU / "cuentas.json"), str(WEB / "data" / "programa.json")], check=True)
shutil.copy(WEB / "data" / "cuentas_ia.json", pub / "data" / "cuentas_ia.json")
shutil.copy(CU / "modelo_fiscal.xlsx", pub / "data" / "modelo-fiscal-san-isidro-2028-2035.xlsx")
ct = (CU / "cuentas.tpl.html").read_text().replace("/*DATA*/null", (CU / "cuentas.json").read_text().replace("</", "<\\/"))
cut2 = ct.index("</style>") + len("</style>")
cdesc = "Las cuentas del programa San Isidro 2027: cuánto entra, cuánto sale y cómo se paga cada propuesta, año por año, del modelo fiscal."
cdoc = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + ct[:cut2].replace("<title>Las cuentas</title>", "<title>Las cuentas · San Isidro 2027</title>")
        + '\n<meta property="og:title" content="Las cuentas · San Isidro 2027">\n<meta property="og:description" content="' + cdesc + '">\n'
        + '<meta property="og:image" content="https://sanisidro2027.pages.dev/img/og.jpg">\n<meta property="og:url" content="https://sanisidro2027.pages.dev/cuentas/">\n<meta property="og:type" content="website">\n'
        + '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n</head>\n<body>\n' + ct[cut2:] + '\n' + (WEB / "menu_movil.html").read_text() + '\n</body>\n</html>\n')
(pub / "cuentas").mkdir(exist_ok=True)
(pub / "cuentas" / "index.html").write_text(cdoc)
print("ok", len(doc.encode()))
