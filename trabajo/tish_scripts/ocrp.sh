#!/bin/bash
# usage: ocrp.sh first last dpi  -> writes tish/o26/pNNN.txt (auto-rotated)
export TESSDATA_PREFIX=/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/tessdata
S=/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad
P=$S/repo/01_raw/presupuestos/ordenanza_del_presupuesto_2026_1.pdf
O=$S/tish/o26
for ((p=$1; p<=$2; p++)); do
  pg=$(printf "%03d" $p)
  [ -s $O/p$pg.txt ] && continue
  pdftoppm -r ${3:-150} -gray -f $p -l $p -png $P $O/img$pg
  img=$(ls $O/img$pg*.png | head -1)
  rot=$(tesseract "$img" - --psm 0 2>/dev/null | grep "Rotate:" | awk '{print $2}')
  if [ -n "$rot" ] && [ "$rot" != "0" ]; then python3 -I -c "
from PIL import Image; import sys
im=Image.open(sys.argv[1]); im.rotate(-int(sys.argv[2]),expand=True).save(sys.argv[1])" "$img" "$rot"; fi
  tesseract "$img" $O/p$pg -l spa --psm 6 >/dev/null 2>&1
  echo "rot=$rot" >> $O/p$pg.txt
  rm -f "$img"
done
