#!/bin/bash
# uso: oa.sh DOI archivo_base "descripcion"  -> guarda JSON de OpenAlex + resumen reconstruido
D=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/educ_raw/w1_evidencia
DOI="$1"; F="$2"; DESC="$3"
URL="https://api.openalex.org/works/doi:$DOI"
curl -sS --max-time 60 -o "$D/$F.json" "$URL"
python3 - "$D/$F.json" <<'PY'
import sys,json
p=sys.argv[1]
try:
    d=json.load(open(p))
except Exception as e:
    print("ERR",e); sys.exit()
inv=d.get("abstract_inverted_index") or {}
pos={}
for w,ix in inv.items():
    for i in ix: pos[i]=w
ab=" ".join(pos[i] for i in sorted(pos))
src=(d.get("primary_location") or {}).get("source") or {}
t=f"TITULO: {d.get('title')}\nANIO: {d.get('publication_year')}\nREVISTA: {src.get('display_name')}\nDOI: {d.get('doi')}\nOA: {(d.get('open_access') or {}).get('oa_url')}\nRESUMEN: {ab}\n"
open(p[:-5]+".txt","w").write(t); print(t[:1500])
PY
B=$(stat -c %s "$D/$F.json" 2>/dev/null || echo 0)
echo "$F.json | $B | $URL | 2026-10-05 | $DESC (metadatos y resumen via OpenAlex; texto completo no leido salvo que se indique)" >> "$D/FUENTES.txt"
