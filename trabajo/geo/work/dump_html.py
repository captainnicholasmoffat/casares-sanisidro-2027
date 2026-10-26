import sys, json, html, re
sys.path.insert(0, sys.argv[1])
import content as C
out = []
for s in C.SECTIONS:
    out.append({"id": s["id"], "html": s["html"]})
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(out), [s["id"] for s in out])
