#!/bin/bash
# uso: _get.sh URL nombre_archivo "descripcion"
W=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/agua_raw/w6_plan_provincia
URL="$1"; F="$2"; D="$3"
curl -sSL --max-time 120 --max-filesize 20000000 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" -o "$W/$F" "$URL"
rc=$?
B=$(stat -c %s "$W/$F" 2>/dev/null || echo 0)
echo "rc=$rc bytes=$B $F"
if [ "$rc" = "0" ] && [ "$B" -gt 500 ]; then
  echo "$F | $B | $URL | 2026-10-01 | $D" >> $W/FUENTES.txt
fi
