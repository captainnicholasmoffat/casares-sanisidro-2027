#!/bin/bash
# Uso: bajar.sh URL NOMBRE_ARCHIVO  (guarda en la carpeta v2 y crea NOMBRE.txt; registra en _tools/bajadas.log)
D=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas
URL="$1"; OUT="$D/$2"
code=$(curl -sS -L --compressed -m 90 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -H "Accept-Language: es-AR,es;q=0.9,en;q=0.8" -o "$OUT" -w "%{http_code}" "$URL" 2>>$D/_tools/bajadas_err.log)
sz=$(stat -c %s "$OUT" 2>/dev/null || echo 0)
echo "$(date -u +%Y-%m-%dT%H:%MZ) | $2 | $sz | $code | $URL" >> $D/_tools/bajadas.log
echo "HTTP $code  $sz bytes  $2"
if [ "$code" = "200" ] && [ "$sz" -gt 0 ]; then python3 -I $D/_tools/a_txt.py "$OUT" "$OUT.txt" >/dev/null; fi
