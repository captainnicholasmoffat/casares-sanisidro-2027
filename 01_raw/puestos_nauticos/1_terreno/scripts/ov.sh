#!/bin/bash
# uso: ov.sh archivo_salida "consulta overpass QL"
OUT="$1"; Q="$2"
for EP in https://overpass.kumi.systems/api/interpreter https://maps.mail.ru/osm/tools/overpass/api/interpreter; do
  curl -sS -m 300 --data-urlencode "data=$Q" "$EP" -o "$OUT" && head -c 200 "$OUT" | grep -q '"elements"' && { echo "OK $EP $(wc -c <"$OUT")"; echo "$EP" > "$OUT.endpoint"; exit 0; }
  echo "fallo $EP"; head -c 300 "$OUT"; echo
done
exit 1
