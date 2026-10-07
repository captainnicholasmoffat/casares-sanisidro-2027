#!/usr/bin/env python3
# Extrae de la página de precios de Cloud Storage (HTML con datos embebidos en JS) los precios por región europea.
import re, sys
s = open(sys.argv[1], encoding='utf-8', errors='replace').read()
pat = re.compile(r'"([A-Z][A-Za-z ]+ \((?:europe|us|southamerica)-[a-z0-9]+\))"')
marks = [(m.start(), m.group(1)) for m in pat.finditer(s)]
out = []
for i, (pos, name) in enumerate(marks):
    end = marks[i+1][0] if i+1 < len(marks) else pos + 3000
    seg = s[pos:end]
    prices = re.findall(r'"(\$[0-9.]+ / [^"]{0,40})"', seg)
    if prices and ('europe-west1)' in name or 'europe-west3)' in name or 'europe-west4)' in name or 'europe-north1)' in name or 'europe-north2)' in name or 'europe-west9)' in name or 'southamerica-east1)' in name):
        out.append(f"occ@{pos} | {name} | " + " ; ".join(prices[:12]))
open(sys.argv[2], 'w').write("\n".join(out) + "\n")
print("\n".join(out))
