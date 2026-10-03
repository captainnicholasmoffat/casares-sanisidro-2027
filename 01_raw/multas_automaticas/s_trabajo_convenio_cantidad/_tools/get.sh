#!/bin/bash
# uso: get.sh URL nombre_archivo   (guarda en carpeta de trabajo; si es html genera .txt)
W=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/s_trabajo_convenio_cantidad
for i in 1 2 3; do
  code=$(curl -sS -g -L --max-time 120 -A "Mozilla/5.0 (X11; Linux x86_64)" -o "$W/$2" -w "%{http_code}" "$1")
  [ "$code" = "200" ] && break
  sleep 2
done
echo "$code $(stat -c %s "$W/$2" 2>/dev/null) $2"
case "$2" in
  *.html|*.htm) python3 $W/_tools/h2t.py "$W/$2" > "$W/${2%.*}.txt";;
  *.pdf) python3 -c "
import pymupdf,sys
d=pymupdf.open(sys.argv[1]); out=open(sys.argv[2],'w')
for i,p in enumerate(d): out.write(f'--- p{i+1}\n'+p.get_text()+'\n')
" "$W/$2" "$W/${2%.*}.txt";;
esac
echo "$(date +%F)|$2|$1" >> $W/_tools/log.tsv
