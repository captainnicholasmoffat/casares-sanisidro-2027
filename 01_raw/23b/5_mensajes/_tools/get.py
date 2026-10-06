#!/usr/bin/env python3
# uso: python3 -I get.py URL nombre "descripcion" [--noappend] [--es] [--post DATA] [--hdr "K: V"]
# Descarga el original a z6_sms/<nombre>, extrae <nombre>.txt y anota ambos en FUENTES.txt.
# Nunca desactiva TLS: usa el bundle del proxy; para sanisidro.gob.ar agrega la cadena OV/DV del repo.
import sys, subprocess, os, datetime, re, html, json
D = "/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23b_raw/z6_sms/"
T = D + "_tools/"
url, name, desc = sys.argv[1], sys.argv[2], sys.argv[3]
path = os.path.join(D, name)
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
args = ["curl", "-sSL", "-m", "180", "-A", ua, "-c", "/dev/null", "-o", path, "-w", "%{http_code} %{content_type}"]
if "--es" in sys.argv:
    args += ["-H", "Accept-Language: es-AR,es;q=0.9"]
if "--post" in sys.argv:
    args += ["--data", sys.argv[sys.argv.index("--post") + 1]]
for i, a in enumerate(sys.argv):
    if a == "--hdr":
        args += ["-H", sys.argv[i + 1]]
if "sanisidro.gob.ar" in url:
    bundle = T + "ca_sanisidro_bundle.pem"
    if not os.path.exists(bundle):
        a = open("/etc/ssl/certs/ca-certificates.crt").read()
        b = open("/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/work/ca_plus_ov_dv.pem").read()
        open(bundle, "w").write(a + "\n" + b + "\n" + open("/root/.ccr/ca-bundle.crt").read())
    args += ["--cacert", bundle]
else:
    args += ["--cacert", "/root/.ccr/ca-bundle.crt"]
r = subprocess.run(args + [url], capture_output=True, text=True)
print("curl:", r.stdout, r.stderr[:300])
code = (r.stdout.split() or ['000'])[0]
if code.startswith(('4', '5', '0')):
    print("FALLO http", code)
    if os.path.exists(path):
        os.rename(path, T + "_fallo_" + name)
    sys.exit(1)
if not os.path.exists(path) or os.path.getsize(path) == 0:
    print("FALLO vacio"); sys.exit(1)
b = open(path, 'rb').read()
txt = None
if b[:4] == b'%PDF':
    import pymupdf
    doc = pymupdf.open(path)
    txt = "\n".join(f"=== p{i+1} ===\n" + p.get_text() for i, p in enumerate(doc))
elif b[:2] == b'PK' and name.endswith('.xlsx'):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(f"[hoja {ws.title}]")
        for row in ws.iter_rows(values_only=True):
            if any(c is not None for c in row):
                out.append(" | ".join("" if c is None else str(c) for c in row))
    txt = "\n".join(out)
elif name.endswith(('.html', '.htm')) or b'<html' in b[:3000].lower() or b'<!doctype' in b[:300].lower():
    s = b.decode('utf-8', 'replace')
    s = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>|</li>', '\n', s)
    s = re.sub(r'(?i)</td>|</th>', ' | ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\r\f\v]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    txt = s
elif name.endswith(('.md', '.txt', '.json', '.csv')):
    txt = b.decode('utf-8', 'replace')
today = "2026-10-06"
lines = [f"{name} | {os.path.getsize(path)} | {url} | {today} | {desc}"]
if txt is not None:
    open(path + ".txt", "w").write(txt)
    print("txt chars", len(txt))
    lines.append(f"{name}.txt | {os.path.getsize(path + '.txt')} | {url} | {today} | Texto extraido de {name}")
if "--noappend" not in sys.argv:
    with open(os.path.join(D, "FUENTES.txt"), "a") as f:
        f.write("\n".join(lines) + "\n")
print("bytes", os.path.getsize(path))
