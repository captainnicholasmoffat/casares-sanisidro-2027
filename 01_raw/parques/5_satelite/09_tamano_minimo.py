# -*- coding: utf-8 -*-
"""Simulacion del tamano minimo detectable con el metodo (Sentinel-2, pixel 10 m, umbrales NDVI 0,40 -> 0,20).
Modelo: escena de 1 m de resolucion con cesped/arboles; se 'pavimenta' un cuadrado de lado L (o una franja de ancho W y 100 m de largo)
en posicion y orientacion (0 o 45 grados) aleatorias respecto de la grilla; se degrada a 10 m con una PSF gaussiana (sigma 4,5 m ~ MTF
de S2 en B04/B08) + desplazamiento de corregistro aleatorio (sigma 3 m) y mezcla lineal de reflectancias; se cuenta si al menos
1 pixel (o >= 3 pixeles) pasa de NDVI >= 0,40 a <= 0,20.
Espectros (reflectancia rojo, NIR): cesped verde (0,05, 0,35); cesped seco (0,08, 0,24); pavimento/hormigon (0,18, 0,22); baldosa oscura/asfalto (0,08, 0,11).
Salida: tamano_minimo_simulacion.csv
Uso: python3 09_tamano_minimo.py [sigma_psf_m]  (4,5 m por defecto; se corrio tambien con 3,0 m como escenario optimista)
"""
import numpy as np, csv, os
from scipy import ndimage
from common import OUT
rng = np.random.default_rng(42)
VEG = {"cesped_verde": (0.05, 0.35), "cesped_seco": (0.08, 0.24)}
PAV = {"hormigon_claro": (0.18, 0.22), "asfalto_oscuro": (0.08, 0.11)}
TV, TN = 0.40, 0.20
N = 200
import sys
SIG = float(sys.argv[1]) if len(sys.argv) > 1 else 4.5  # sigma de la PSF en metros

def simulate(shape_kind, size, veg, pav):
    det1 = det3 = 0
    for _ in range(N):
        H = 120
        m = np.zeros((H, H), bool)
        cx, cy = 60 + rng.uniform(-5, 5), 60 + rng.uniform(-5, 5)
        ang = rng.choice([0, np.pi / 4]) + rng.normal(0, 0.05)
        yy, xx = np.mgrid[:H, :H] + 0.5
        u = (xx - cx) * np.cos(ang) + (yy - cy) * np.sin(ang)
        v = -(xx - cx) * np.sin(ang) + (yy - cy) * np.cos(ang)
        if shape_kind == "cuadrado":
            m = (np.abs(u) <= size / 2) & (np.abs(v) <= size / 2)
        else:  # franja (sendero) de ancho 'size' y 100 m de largo
            m = (np.abs(u) <= size / 2) & (np.abs(v) <= 50)
        res = []
        for when in ("antes", "despues"):
            red = np.full((H, H), veg[0]); nir = np.full((H, H), veg[1])
            if when == "despues":
                red[m] = pav[0]; nir[m] = pav[1]
            sh = rng.normal(0, 3, 2)
            red = ndimage.shift(ndimage.gaussian_filter(red, SIG), sh, mode="nearest")
            nir = ndimage.shift(ndimage.gaussian_filter(nir, SIG), sh, mode="nearest")
            R = red.reshape(12, 10, 12, 10).mean(axis=(1, 3)); Nn = nir.reshape(12, 10, 12, 10).mean(axis=(1, 3))
            res.append((Nn - R) / (Nn + R))
        f = (res[0] >= TV) & (res[1] <= TN)
        det1 += f.sum() >= 1; det3 += f.sum() >= 3
    return det1 / N, det3 / N

rows = []
for vk, veg in VEG.items():
    for pk, pav in PAV.items():
        for kind, sizes in (("cuadrado", [8, 10, 12, 15, 18, 20, 25, 30]), ("franja", [2, 3, 5, 8, 10, 12, 15])):
            for s in sizes:
                p1, p3 = simulate(kind, s, veg, pav)
                rows.append({"psf_sigma_m": SIG, "vegetacion_antes": vk, "solado_despues": pk, "forma": kind, "lado_o_ancho_m": s,
                             "area_m2": s * s if kind == "cuadrado" else s * 100, "P_detectar_1px": round(p1, 2), "P_detectar_3px": round(p3, 2)})
                print(rows[-1], flush=True)
with open(os.path.join(OUT, "tamano_minimo_simulacion.csv"), "a" if SIG != 4.5 else "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    if SIG == 4.5: w.writeheader()
    w.writerows(rows)
