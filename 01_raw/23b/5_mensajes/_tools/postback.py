#!/usr/bin/env python3
# uso: python3 -I postback.py URL_PAGINA EVENTTARGET salida
# Hace GET de la pagina ASP.NET de COMPR.AR (con cookies), y luego el POST del __doPostBack indicado.
import sys, subprocess, re, html, os, urllib.parse
url, target, out = sys.argv[1], sys.argv[2], sys.argv[3]
T = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"
os.makedirs(T, exist_ok=True)
jar = T + "jar.txt"
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
base = ["curl", "-sSL", "-m", "180", "--cacert", "/root/.ccr/ca-bundle.crt", "-A", ua, "-b", jar, "-c", jar]
r = subprocess.run(base + ["-o", T + "pb_get.html", url], capture_output=True, text=True)
s = open(T + "pb_get.html", errors="replace").read()
fields = {}
for m in re.finditer(r'<input[^>]+type="hidden"[^>]*>', s):
    tag = m.group(0)
    n = re.search(r'name="([^"]+)"', tag)
    v = re.search(r'value="([^"]*)"', tag)
    if n:
        fields[n.group(1)] = html.unescape(v.group(1)) if v else ""
fields["__EVENTTARGET"] = target
fields["__EVENTARGUMENT"] = ""
action = re.search(r'<form[^>]+action="([^"]+)"', s)
post_url = urllib.parse.urljoin(url, html.unescape(action.group(1))) if action else url
data = urllib.parse.urlencode(fields)
open(T + "pb_data.txt", "w").write(data)
r = subprocess.run(base + ["-D", T + "pb_hdr.txt", "-o", out, "--data-binary", "@" + T + "pb_data.txt",
                           "-H", "Content-Type: application/x-www-form-urlencoded", "-e", url,
                           "-w", "%{http_code} %{content_type}", post_url], capture_output=True, text=True)
print(r.stdout, r.stderr[:300])
print(open(T + "pb_hdr.txt").read()[:1500])
