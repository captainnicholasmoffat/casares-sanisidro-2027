#!/bin/bash
# uso: get.sh URL nombre_archivo "descripcion" [extra curl opts]
O=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/educ_raw/w2_competencia_datos
URL="$1"; F="$2"; DESC="$3"; shift 3
code=$(curl -sS -g -L --max-time 120 "$@" -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -o "$O/$F" -w "%{http_code}" "$URL" 2>"$O/_tools/err_$F.txt")
rc=$?
sz=$(stat -c %s "$O/$F" 2>/dev/null || echo 0)
echo "HTTP $code rc=$rc size=$sz $F"
head -3 "$O/_tools/err_$F.txt"
if [ "$rc" = "0" ] && [ "$sz" -gt 0 ] && [ "$code" = "200" ]; then
  case "$F" in
    *.pdf) python3 $O/_tools/pdf2txt.py "$O/$F" "$O/${F%.pdf}.txt" ;;
    *.html|*.htm) python3 $O/_tools/h2t.py "$O/$F" > "$O/${F%.*}.txt"; echo "txt $(stat -c %s "$O/${F%.*}.txt")";;
  esac
  echo -e "$F\t$sz\t$URL\t2026-10-05\t$DESC" >> $O/_tools/fuentes_log.tsv
else
  echo "NO GUARDADO en log"
fi
