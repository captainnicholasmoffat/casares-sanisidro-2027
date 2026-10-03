#!/bin/bash
# get.sh URL archivo  (TLS verificado; CA del proxy + intermedios públicos Sectigo OV/DV R36 para sanisidro.gob.ar / aysa.com.ar)
U=/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque
curl -sS -L -m 120 --cacert $U/work/ca_plus_ov_dv.pem -A "Mozilla/5.0 (X11; Linux x86_64)" -o "$2" -w "%{http_code} %{size_download} %{content_type} $1\n" "$1"
