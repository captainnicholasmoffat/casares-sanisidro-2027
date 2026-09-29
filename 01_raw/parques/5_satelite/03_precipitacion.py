# -*- coding: utf-8 -*-
"""Precipitacion estacional (DJF, MAM, JJA, SON) en San Isidro (-34.47, -58.52) segun NASA POWER (PRECTOTCORR, MERRA-2
corregido, ~0.5 grado de resolucion: es un dato REGIONAL, no del partido) y anomalia contra 1991-2020 de la misma fuente.
Salida: precipitacion_estacional.csv
"""
import json, csv, os, calendar, collections
from common import OUT
d = json.load(open(os.path.join(OUT, "precip_nasapower_2022_2026.json")))["properties"]["parameter"]["PRECTOTCORR"]
c = json.load(open(os.path.join(OUT, "precip_nasapower_mensual_1991_2021.json")))["properties"]["parameter"]["PRECTOTCORR"]
mon = collections.defaultdict(float); ndays = collections.Counter()
for k, v in d.items():
    if v is None or v < 0:
        continue
    mon[(int(k[:4]), int(k[4:6]))] += v; ndays[(int(k[:4]), int(k[4:6]))] += 1
clim = collections.defaultdict(list)
for k, v in c.items():
    y, m = int(k[:4]), int(k[4:6])
    if m == 13 or y > 2020:
        continue
    clim[m].append(v * calendar.monthrange(y, m)[1])
climm = {m: sum(v) / len(v) for m, v in clim.items()}
SEAS = {"DJF": (12, 1, 2), "MAM": (3, 4, 5), "JJA": (6, 7, 8), "SON": (9, 10, 11)}
rows = []
for y in range(2022, 2027):
    for s, ms in SEAS.items():
        keys = [((y - 1) if (s == "DJF" and m == 12) else y, m) for m in ms]
        if any(k not in mon for k in keys):
            continue
        tot = sum(mon[k] for k in keys); cl = sum(climm[m] for m in ms)
        full = all(ndays[k] >= calendar.monthrange(*k)[1] - 1 for k in keys)
        rows.append({"estacion": f"{s} {keys[0][0]}/{keys[-1][0]}" if s == "DJF" else f"{s} {y}", "pp_mm": round(tot, 0),
                     "clima_1991_2020_mm": round(cl, 0), "anomalia_pct": round(100 * (tot - cl) / cl, 0), "completa": full})
with open(os.path.join(OUT, "precipitacion_estacional.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
