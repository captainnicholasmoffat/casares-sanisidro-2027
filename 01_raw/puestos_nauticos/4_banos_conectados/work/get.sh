#!/bin/bash
# uso: get.sh NOMBRE_ARCHIVO URL "descripcion" [cacert]
W=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u2_banos_conectados
f="$1"; url="$2"; desc="$3"; ca="${4:-}"
args=(-sS -L --max-time 120 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36" -o "$W/$f")
if [ -n "$ca" ]; then args+=(--cacert "$ca"); fi
http=$(curl "${args[@]}" -w "%{http_code}" "$url")
sz=$(stat -c %s "$W/$f" 2>/dev/null || echo 0)
echo "HTTP $http bytes $sz -> $f"
python3 $W/work/ext.py "$W/$f"
if [ "$http" = "200" ] && [ "$sz" -gt 500 ]; then
  echo "$f | $sz | $url | 03/10/2026 | $desc" >> $W/work/fuentes_pendientes.txt
fi
