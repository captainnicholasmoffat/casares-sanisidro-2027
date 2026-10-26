#!/bin/bash
export TESSDATA_PREFIX=/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/tessdata
P=/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/repo/01_raw/presupuestos/ordenanza_del_presupuesto_2026_1.pdf
OUT=/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compras_local/ocr
for ((p=$1; p<=$2; p++)); do
  pg=$(printf "%03d" $p)
  [ -s $OUT/q$pg.txt ] && continue
  pdftoppm -r 300 -gray -f $p -l $p -png "$P" $OUT/img$pg
  img=$(ls $OUT/img$pg*.png | head -1)
  tesseract "$img" $OUT/q$pg -l spa --psm 6 >/dev/null 2>&1
  rm -f "$img"
done
echo done $1 $2
