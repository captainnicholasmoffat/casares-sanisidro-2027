import json, sys, urllib.request, datetime
pkgs = sys.argv[1:]
cutoff = datetime.datetime(2026,9,26, tzinfo=datetime.timezone.utc)
for p in pkgs:
    try:
        url = "https://registry.npmjs.org/" + p.replace("/", "%2F")
        d = json.load(urllib.request.urlopen(url, timeout=30))
        latest = d.get("dist-tags",{}).get("latest")
        t = d.get("time",{})
        # versions published before cutoff (no prerelease)
        vs = [(v, t[v]) for v in d.get("versions",{}) if v in t and "-" not in v]
        vs = [(v, datetime.datetime.fromisoformat(ts.replace("Z","+00:00"))) for v,ts in vs]
        old = [x for x in vs if x[1] <= cutoff]
        old.sort(key=lambda x: x[1])
        best = old[-1] if old else None
        print(f"{p}: latest={latest} ({t.get(latest,'?')[:10]}) | newest>=2wk-old={best[0] if best else None} ({best[1].date() if best else ''}) | license={d.get('license')}")
    except Exception as e:
        print(p, "ERR", e)
