import json, sys, urllib.request
for p in sys.argv[1:]:
    d = json.load(urllib.request.urlopen("https://registry.npmjs.org/" + p.replace("/", "%2F"), timeout=30))
    t = d["time"]
    vs = sorted([(t[v], v) for v in d["versions"] if v in t and "-" not in v])[-6:]
    print(p, [(v, ts[:10]) for ts, v in vs])
