#!/bin/bash
# uso: rmsrc.sh nombre
D=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y3_seguridad_barrido
rm -f "$D/$1" "$D/$1.txt"; sed -i "/^$1 /d" "$D/FUENTES.txt"
