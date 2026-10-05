#!/bin/bash
# uso: get.sh URL archivo "descripcion"
D=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/educ_raw/w1_evidencia
URL="$1"; F="$2"; DESC="$3"
curl --http1.1 -sSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" --max-time 120 -o "$D/$F" "$URL"
RC=$?
B=$(stat -c %s "$D/$F" 2>/dev/null || echo 0)
T=$(file -b "$D/$F" | cut -c1-40)
echo "rc=$RC bytes=$B type=$T"
case "$F" in
  *.pdf) python3 - "$D/$F" <<'PY'
import sys, pymupdf
p=sys.argv[1]
try:
    d=pymupdf.open(p); t="\n".join(pg.get_text() for pg in d)
    open(p[:-4]+".txt","w").write(t); print("pages",len(d),"chars",len(t))
except Exception as e: print("ERR",e)
PY
  ;;
  *.html) python3 - "$D/$F" <<'PY'
import sys,re,html
p=sys.argv[1]
s=open(p,encoding="utf-8",errors="ignore").read()
s=re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>"," ",s)
s=re.sub(r"(?s)<br\s*/?>|</p>|</div>|</h\d>|</li>|</tr>","\n",s)
s=re.sub(r"(?s)<[^>]+>"," ",s); s=html.unescape(s)
s=re.sub(r"[ \t]+"," ",s); s=re.sub(r"\n\s*\n+","\n\n",s)
open(p[:-5]+".txt","w").write(s); print("chars",len(s))
PY
  ;;
esac
echo "$F | $B | $URL | 2026-10-05 | $DESC" >> "$D/FUENTES.txt"
