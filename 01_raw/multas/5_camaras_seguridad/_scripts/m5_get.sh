#!/bin/bash
# usage: m5_get.sh filename url "descripcion"
D=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/m5_camaras_seguridad
f="$1"; u="$2"; desc="$3"
curl -sSL --max-time 90 --max-filesize 20000000 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36" -o "$D/$f" "$u"
rc=$?
if [ -s "$D/$f" ]; then
  b=$(stat -c %s "$D/$f")
  echo "$f | $b | $u | 2026-10-02 | $desc" >> "$D/FUENTES.txt"
  echo "OK rc=$rc $f $b bytes"; file "$D/$f"
else
  echo "FAIL rc=$rc $f"; rm -f "$D/$f"
fi
