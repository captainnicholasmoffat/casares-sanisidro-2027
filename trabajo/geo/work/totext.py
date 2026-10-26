import sys, json, html, re
secs = json.load(open(sys.argv[1]))
lines = []
for s in secs:
    h = s["html"]
    h = re.sub(r'<h2><span class="n">([^<]+)</span>', r'\n\n@@SEC \1 @@ ', h)
    h = re.sub(r'<h1[^>]*>', r'\n\n@@H1 ', h)
    h = re.sub(r'<div class="exlabel">([^<]+)</div>', r'\n@@EX \1 @@ ', h)
    h = re.sub(r'<img src="asset:([^"]+)"[^>]*>', r' @@IMG \1 @@ ', h)
    h = re.sub(r'<figcaption[^>]*>', r'\n@@CAP ', h)
    h = re.sub(r'</(p|tr|h2|h3|li|div|figcaption|table)>', '\n', h)
    h = re.sub(r'<(td|th)[^>]*>', ' | ', h)
    h = re.sub(r'<h3[^>]*>', '\n@@H3 ', h)
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h).replace('\xa0', ' ')
    lines.append(f"\n\n######## PAGE {s['id']}\n" + h)
t = "".join(lines)
t = re.sub(r'[ \t]+', ' ', t)
t = re.sub(r'\n\s*\n+', '\n', t)
open(sys.argv[2], "w").write(t)
