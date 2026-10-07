# Convierte un archivo descargado (html/pdf/json/txt) a texto plano. Uso: python3 -I a_txt.py ENTRADA SALIDA
import sys, re, html, json, subprocess, os
src, dst = sys.argv[1], sys.argv[2]
data = open(src, 'rb').read()
low = src.lower()
txt = ''
if data[:5] == b'%PDF-':
    try:
        import pymupdf
        doc = pymupdf.open(src)
        txt = ''.join('\n=== PAGINA %d ===\n' % (i+1) + pg.get_text() for i, pg in enumerate(doc))
    except Exception as e:
        txt = 'ERROR pdf: %s' % e
elif low.endswith('.json'):
    try:
        txt = json.dumps(json.loads(data.decode('utf-8', 'replace')), ensure_ascii=False, indent=1)
    except Exception:
        txt = data.decode('utf-8', 'replace')
else:
    try:
        s = data.decode('utf-8')
    except UnicodeDecodeError:
        s = data.decode('cp1252', 'replace')
    if '<html' in s[:5000].lower() or '<!doctype' in s[:500].lower() or '<body' in s.lower():
        s = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', s)
        s = re.sub(r'(?i)<br\s*/?>', '\n', s)
        s = re.sub(r'(?i)</(p|div|li|tr|h[1-6]|table|section|article|td|th)>', '\n', s)
        s = re.sub(r'<[^>]+>', ' ', s)
        s = html.unescape(s)
        s = re.sub(r'[ \t\r\f\v]+', ' ', s)
        s = re.sub(r'\n\s*\n+', '\n', s)
    txt = s
open(dst, 'w', encoding='utf-8').write(txt)
print(dst, len(txt))
