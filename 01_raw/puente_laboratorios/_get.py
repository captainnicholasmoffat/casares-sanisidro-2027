#!/usr/bin/env python3
"""Uso: _get.py NOMBRE URL "descripcion"
Baja la URL a NOMBRE.<ext>, genera NOMBRE.txt y agrega una linea a FUENTES.txt.
"""
import sys, os, subprocess, datetime, re

D = os.path.dirname(os.path.abspath(__file__))
name, url, desc = sys.argv[1], sys.argv[2], sys.argv[3]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
tmp = os.path.join(D, name + ".download")
r = subprocess.run(["curl", "-sSL", "--max-time", "90", "-A", UA, "-H", "Accept-Language: en-US,en;q=0.9,es;q=0.8",
                    "-o", tmp, "-w", "%{http_code} %{content_type}", url], capture_output=True, text=True)
code_ct = r.stdout.strip()
print("HTTP:", code_ct, r.stderr.strip()[:200])
if not os.path.exists(tmp) or os.path.getsize(tmp) == 0:
    print("FALLO: vacio"); sys.exit(1)
with open(tmp, "rb") as f:
    head = f.read(8)
ct = code_ct.split(" ", 1)[1] if " " in code_ct else ""
if head.startswith(b"%PDF"):
    ext = ".pdf"
elif "json" in ct:
    ext = ".json"
elif "xml" in ct and "html" not in ct:
    ext = ".xml"
else:
    ext = ".html"
orig = os.path.join(D, name + ext)
os.replace(tmp, orig)
txt = os.path.join(D, name + ".txt")
text = ""
if ext == ".pdf":
    import fitz
    doc = fitz.open(orig)
    text = "\n".join(p.get_text() for p in doc)
elif ext in (".json", ".xml"):
    text = open(orig, encoding="utf-8", errors="replace").read()
else:
    from bs4 import BeautifulSoup
    html = open(orig, encoding="utf-8", errors="replace").read()
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "svg"]):
        t.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
with open(txt, "w", encoding="utf-8") as f:
    f.write("URL: " + url + "\nFecha de consulta: " + datetime.date.today().isoformat() + "\nHTTP: " + code_ct + "\n\n" + text)
size = os.path.getsize(orig)
code = code_ct.split(" ")[0]
if code.startswith("4") or code.startswith("5") or len(text.strip()) < 200:
    os.remove(orig); os.remove(txt)
    with open(os.path.join(D, "_fallos.txt"), "a") as f:
        f.write(f"{name} | {url} | HTTP {code} | chars {len(text.strip())}\n")
    print("FALLO", code, len(text.strip())); sys.exit(2)
with open(os.path.join(D, "FUENTES.txt"), "a", encoding="utf-8") as f:
    f.write(f"{os.path.basename(orig)} | {size} | {url} | {datetime.date.today().isoformat()} | {desc} (HTTP {code})\n")
print("OK", os.path.basename(orig), size, "txt chars", len(text))
