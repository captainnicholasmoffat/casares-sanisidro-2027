#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baja las TTF de Spectral e Inter a doc/_fonts/.

Estan versionadas en el repo, asi que esto normalmente no hace falta: sirve
para reponerlas o actualizarlas. El PDF NO puede pedirle las fuentes a Google
en tiempo de armado -Chromium rechaza el certificado del proxy y cae en
silencio a Liberation-, por eso van embebidas como data URI.
"""
import pathlib, urllib.request

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
DEST = pathlib.Path(__file__).parent / "_fonts"
ARCHIVOS = [
    (f"{BASE}/spectral/Spectral-Regular.ttf",          "Spectral-Regular.ttf"),
    (f"{BASE}/spectral/Spectral-Medium.ttf",           "Spectral-Medium.ttf"),
    (f"{BASE}/spectral/Spectral-SemiBold.ttf",         "Spectral-SemiBold.ttf"),
    (f"{BASE}/spectral/Spectral-Bold.ttf",             "Spectral-Bold.ttf"),
    (f"{BASE}/spectral/Spectral-Italic.ttf",           "Spectral-Italic.ttf"),
    (f"{BASE}/spectral/Spectral-MediumItalic.ttf",     "Spectral-MediumItalic.ttf"),
    (f"{BASE}/spectral/Spectral-SemiBoldItalic.ttf",   "Spectral-SemiBoldItalic.ttf"),
    (f"{BASE}/spectral/Spectral-BoldItalic.ttf",       "Spectral-BoldItalic.ttf"),
    (f"{BASE}/inter/Inter%5Bopsz,wght%5D.ttf",         "Inter-var.ttf"),
    (f"{BASE}/spectral/OFL.txt",                       "OFL-Spectral.txt"),
    (f"{BASE}/inter/OFL.txt",                          "OFL-Inter.txt"),
]

# Chromium NO embebe fuentes variables al exportar el PDF: las carga en pantalla
# y despues sustituye. Por eso de Inter se derivan cuatro instancias estaticas.
INSTANCIAS_INTER = [(400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")]


def instanciar_inter():
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    src = DEST / "Inter-var.ttf"
    for peso, nombre in INSTANCIAS_INTER:
        f = TTFont(str(src))
        # opsz 14 es el tamano optico de texto, que es como se usa en el documento
        inst = instancer.instantiateVariableFont(
            f, {"wght": peso, "opsz": 14}, inplace=True, updateFontNames=True)
        out = DEST / f"Inter-{nombre}.ttf"
        inst.save(str(out))
        print(f"  Inter-{nombre}.ttf{'':<{max(0,20-len(nombre))}} {out.stat().st_size/1e3:8.1f} kB")


def main():
    DEST.mkdir(exist_ok=True)
    for url, nombre in ARCHIVOS:
        d = urllib.request.urlopen(url, timeout=90).read()
        if nombre.endswith(".ttf") and d[:4] not in (b"\x00\x01\x00\x00", b"true", b"OTTO"):
            raise SystemExit(f"  !! {nombre} no es una TTF valida ({len(d)} bytes)")
        (DEST / nombre).write_bytes(d)
        print(f"  {nombre:32s} {len(d)/1e3:8.1f} kB")
    instanciar_inter()

if __name__ == "__main__":
    main()
