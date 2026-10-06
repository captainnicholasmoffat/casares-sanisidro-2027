#!/bin/bash
# descarga award.csv en 8 tramos en paralelo
U="https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-economia-y-finanzas/buenos-aires-compras/award.csv"
O="/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23b_raw/z2_telefonos/_tools/bac_parts"
L=616470431; N=8; S=$(( (L+N-1)/N ))
for i in $(seq 0 $((N-1))); do a=$((i*S)); b=$(( (i+1)*S-1 )); [ $b -ge $L ] && b=$((L-1)); curl -sS -m 3500 --retry 3 -r $a-$b "$U" -o "$O/part$i" & done
wait
cat $O/part0 $O/part1 $O/part2 $O/part3 $O/part4 $O/part5 $O/part6 $O/part7 > $O/award.csv
ls -la $O
