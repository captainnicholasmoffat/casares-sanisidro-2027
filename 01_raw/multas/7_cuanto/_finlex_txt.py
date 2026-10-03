import re, json, sys
p, op = sys.argv[1], sys.argv[2]
raw = open(p, encoding='utf-8').read()
chunks = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', raw)
payload = "".join(json.loads(c) for c in chunks)
out = []
for m in re.finditer(r'"children":"((?:[^"\\]|\\.)*)"', payload):
    try: t = json.loads('"' + m.group(1) + '"')
    except Exception: continue
    t = re.sub(r'\s+', ' ', t).strip()
    if not t or t.startswith('$'): continue
    out.append(t)
open(op, 'w').write("\n".join(out))
print(op, len(out))
