#!/usr/bin/env python3
# uso: python3 -I comprar_buscar.py "texto" salida.html
# Busqueda avanzada publica de COMPR.AR por nombre descriptivo del proceso (sin registrarse).
import sys, subprocess, re, html, os, urllib.parse
q, out = sys.argv[1], sys.argv[2]
T = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
jar = T + "jar_b.txt"
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
base = ["curl", "-sSL", "-m", "180", "--cacert", "/root/.ccr/ca-bundle.crt", "-A", ua, "-b", jar, "-c", jar]
url = "https://comprar.gob.ar/BuscarAvanzado.aspx"
subprocess.run(base + ["-o", T + "b_get.html", url], capture_output=True, text=True)
s = open(T + "b_get.html", errors="replace").read()
action = re.search(r'<form[^>]+action="([^"]+)"', s)
post_url = urllib.parse.urljoin("https://comprar.gob.ar/", html.unescape(action.group(1))) if action else url
fields = {}
for m in re.finditer(r'<input[^>]*>', s):
    tag = m.group(0)
    n = re.search(r'name="([^"]+)"', tag); v = re.search(r'value="([^"]*)"', tag)
    t = re.search(r'type="([^"]+)"', tag)
    if n and (not t or t.group(1) in ("hidden", "text")):
        fields[n.group(1)] = html.unescape(v.group(1)) if v else ""
for m in re.finditer(r'<select[^>]+name="([^"]+)"[^>]*>(.*?)</select>', s, re.S):
    sel = re.search(r'<option[^>]+selected="selected"[^>]+value="([^"]*)"', m.group(2)) or re.search(r'<option[^>]+value="([^"]*)"', m.group(2))
    fields[m.group(1)] = html.unescape(sel.group(1)) if sel else ""
fields["ctl00$CPH1$txtNombrePliego"] = q
fields["__EVENTTARGET"] = "ctl00$CPH1$btnListarPliegoAvanzado"
fields["__EVENTARGUMENT"] = ""
open(T + "b_data.txt", "w").write(urllib.parse.urlencode(fields))
r = subprocess.run(base + ["-o", out, "--data-binary", "@" + T + "b_data.txt", "-H", "Content-Type: application/x-www-form-urlencoded",
                           "-e", url, "-w", "%{http_code} %{content_type}", post_url], capture_output=True, text=True)
print(r.stdout, r.stderr[:200])
# Opcional: 3er argumento = event target de una fila del resultado; 4to = archivo de salida de la pagina del proceso
if len(sys.argv) > 4:
    tgt, out2 = sys.argv[3], sys.argv[4]
    s = open(out, errors="replace").read()
    action = re.search(r'<form[^>]+action="([^"]+)"', s)
    post_url = urllib.parse.urljoin("https://comprar.gob.ar/", html.unescape(action.group(1))) if action else url
    f2 = {}
    for m in re.finditer(r'<input[^>]*>', s):
        tag = m.group(0)
        n = re.search(r'name="([^"]+)"', tag); v = re.search(r'value="([^"]*)"', tag); t = re.search(r'type="([^"]+)"', tag)
        if n and (not t or t.group(1) in ("hidden", "text")):
            f2[n.group(1)] = html.unescape(v.group(1)) if v else ""
    for m in re.finditer(r'<select[^>]+name="([^"]+)"[^>]*>(.*?)</select>', s, re.S):
        sel = re.search(r'<option[^>]+selected="selected"[^>]+value="([^"]*)"', m.group(2)) or re.search(r'<option[^>]+value="([^"]*)"', m.group(2))
        f2[m.group(1)] = html.unescape(sel.group(1)) if sel else ""
    f2["__EVENTTARGET"] = tgt; f2["__EVENTARGUMENT"] = ""
    open(T + "b_data2.txt", "w").write(urllib.parse.urlencode(f2))
    r = subprocess.run(base + ["-o", out2, "--data-binary", "@" + T + "b_data2.txt", "-H", "Content-Type: application/x-www-form-urlencoded",
                               "-e", post_url, "-w", "%{http_code} %{url_effective}", post_url], capture_output=True, text=True)
    print("fila:", r.stdout, r.stderr[:200])
