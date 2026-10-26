import sys, json
sys.path.insert(0, sys.argv[1])
import content
out=[]
for s in content.SECTIONS:
    out.append({"id":s["id"],"html":s["html"]})
json.dump(out, open(sys.argv[2],"w"), ensure_ascii=False, indent=0)
print(len(out))
for s in out: print(s["id"], len(s["html"]))
