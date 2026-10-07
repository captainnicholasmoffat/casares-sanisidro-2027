#!/bin/bash
# Mide cuánto tarda deface 1.5.0 (CPU, onnxruntime) en anonimizar 60 s de video 1080p 30 fps en esta máquina (4 núcleos)
cd /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface
lscpu | grep -E "Model name|^CPU\(s\)" > /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface/cpu.txt
for cfg in "full:" "720:--scale 1280x720" "540:--scale 960x540" "360:--scale 640x360"; do
  name=${cfg%%:*}; opts=${cfg#*:}
  s=$(date +%s.%N)
  /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/venv/bin/deface /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface/prueba_1080p_60s.mp4 -o /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface/salida_$name.mp4 $opts > /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface/log_$name.txt 2>&1
  e=$(date +%s.%N)
  echo "$name | opciones: $opts | segundos: $(echo "$e - $s" | bc)" >> /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface/tiempos.txt
done
echo FIN >> /tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas/_tools/prueba_deface/tiempos.txt
