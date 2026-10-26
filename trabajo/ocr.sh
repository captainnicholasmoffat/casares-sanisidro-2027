#!/bin/bash
# usage: ocr.sh pdf outdir first last
pdf=$1; out=$2; first=$3; last=$4
export TESSDATA_PREFIX=/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/tessdata
for ((p=first; p<=last; p++)); do
  pg=$(printf "%03d" $p)
  [ -s $out/p$pg.txt ] && continue
  pdftoppm -r 200 -gray -f $p -l $p -png "$pdf" $out/img$pg
  img=$(ls $out/img$pg*.png | head -1)
  tesseract "$img" $out/p$pg -l spa --psm 6 >/dev/null 2>&1
  rm -f "$img"
done
