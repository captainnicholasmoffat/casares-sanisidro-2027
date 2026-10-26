import re,sys,pathlib
for f in sorted(pathlib.Path(sys.argv[1]).glob("*.md")):
    lines=f.read_text(encoding="utf-8").split("\n")
    print(f"\n######## {f.name}")
    cur=None; wc=0; fence=False
    out=[]
    for l in lines:
        if l.startswith("```"): fence=not fence
        m=re.match(r"^(#{1,6})\s+(.*)",l) if not fence else None
        if m:
            if cur: out.append((cur,wc))
            cur=(len(m.group(1)),m.group(2)); wc=0
        else:
            wc+=len(l.split())
    if cur: out.append((cur,wc))
    for (lv,t),w in out: print("  "*(lv-1)+f"{'#'*lv} {t[:110]}  [{w}]")
