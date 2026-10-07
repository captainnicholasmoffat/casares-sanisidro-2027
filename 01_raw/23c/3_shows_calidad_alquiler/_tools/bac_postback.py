# Descarga un documento de una vista de pliego de Buenos Aires Compras (BAC) haciendo el postback ASP.NET.
# uso: python3 -I bac_postback.py URL_VISTA EVENTTARGET SALIDA
import sys; sys.path.append("/root/.local/lib/python3.11/site-packages")
import re, html, requests
url, target, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
r = s.get(url, timeout=90)
form = {}
for m in re.finditer(r'<input[^>]+type="hidden"[^>]*>', r.text):
    n = re.search(r'name="([^"]+)"', m.group(0)); v = re.search(r'value="([^"]*)"', m.group(0))
    if n: form[html.unescape(n.group(1))] = html.unescape(v.group(1)) if v else ''
form['__EVENTTARGET'] = target; form['__EVENTARGUMENT'] = ''
r2 = s.post(r.url, data=form, timeout=120, allow_redirects=True)
ct = r2.headers.get('content-type', ''); cd = r2.headers.get('content-disposition', '')
print(r2.status_code, ct, cd, len(r2.content))
# a veces devuelve un HTML con un window.open a un handler de descarga
if 'html' in ct:
    for m in re.finditer(r"(?:window\.open|location\.href)\s*\(?\s*['\"]([^'\"]+)['\"]", r2.text):
        print('LINK', m.group(1))
open(out, 'wb').write(r2.content)
