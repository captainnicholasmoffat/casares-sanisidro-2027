#!/bin/bash
# uso: sibom.sh "consulta" archivo_salida
O=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/q_automatica/busquedas_sibom
Q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")
curl -sS -g -L --max-time 90 "https://sibom.slyt.gba.gob.ar/search?q%5Bsimple_query_string%5D=$Q" -o "$O/$2" -w "%{http_code} %{size_download}\n"
python3 -c "
import re,html,sys
t=open('$O/$2',encoding='utf-8',errors='ignore').read()
for m in re.finditer(r'<a[^>]+href=\"(/bulletins/\d+/contents/\d+)\"[^>]*>(.*?)</a>',t,re.S):
    print(m.group(1), re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.group(2)))).strip()[:200])
" | head -60
