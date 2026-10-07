#!/usr/bin/env python3
# Completa FUENTES.txt: una línea por archivo de la carpeta que todavía no figure.
import os, sys
W = sys.argv[1]; Z = sys.argv[2]; Y = sys.argv[3]
fu = os.path.join(W, "FUENTES.txt")
lines = open(fu).read().splitlines()
ya = {l.split(" | ")[0] for l in lines if " | " in l}
prev = {}
for f in (os.path.join(Z, "FUENTES.txt"), os.path.join(Y, "FUENTES.txt")):
    for l in open(f, errors="replace"):
        p = l.rstrip("\n").split(" | ")
        if len(p) >= 5: prev.setdefault(p[0], p)
nuevas = []
desc_tools = {
 "_tools/get.py": "script propio de descarga (curl + extracción de texto); adaptado del de z2",
 "_tools/aws_resumen.py": "script propio: resume los index.json de la AWS Price List API en .txt",
 "_tools/gcp_extraer.py": "script propio: extrae de la página de precios de Google Cloud los precios por región europea embebidos en JavaScript",
 "_tools/gcp_precios_extraidos.txt": "salida de gcp_extraer.py: precios por GiB-mes de Standard/Nearline/Coldline/Archive por región (orden de columnas de la página)",
 "_tools/fuentes_completar.py": "script propio: completa este FUENTES.txt",
 "_tools/calculo.py": "cuentas de este informe (pesos de dic-2025)",
 "_tools/calculo_salida.txt": "salida de calculo.py",
 "_tools/errores.log": "registro de descargas fallidas",
 "_tools/aws_offers_index.json": "AWS Price List API, índice de ofertas (https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json), para ubicar S3, Deep Archive y transferencia",
 "_tools/muestra_huella/manifiesto.json": "muestra propia: manifiesto JSON de un bloque (dos huellas, hora, GPS, huella anterior) para medir bytes",
 "_tools/muestra_huella/firma_ecdsa_p256.der": "muestra propia: firma ECDSA P-256 del manifiesto (openssl 3.0.13), 71 bytes",
 "_tools/muestra_huella/firma_ecdsa_p256.b64": "muestra propia: la misma firma en base64, 96 bytes",
 "_tools/muestra_huella/firma_ed25519.bin": "muestra propia: firma Ed25519 del manifiesto, 64 bytes",
 "_tools/muestra_huella/firma_ed25519.b64": "muestra propia: la misma firma en base64, 88 bytes",
 "_tools/muestra_huella/manifiesto.json.gz": "muestra propia: manifiesto comprimido con gzip -9, 366 bytes",
}
for root, dirs, files in os.walk(W):
    for fn in sorted(files):
        rel = os.path.relpath(os.path.join(root, fn), W)
        if rel == "FUENTES.txt" or rel in ya: continue
        size = os.path.getsize(os.path.join(root, fn))
        base = fn
        if rel.startswith("copias_previas/"):
            orig = base[:-4] if base.endswith(".txt") and base[:-4] in prev else base
            p = prev.get(base) or prev.get(orig)
            if p:
                url, fecha, que = p[2], p[3], p[4]
                nuevas.append(f"{rel} | {size} | {url} | {fecha} | COPIA de material previo (z2 o y3, sin cambios): {que}")
            else:
                nuevas.append(f"{rel} | {size} | (copia de material previo; ver FUENTES de z2/y3 o repo) | 2026-10-07 | copia sin cambios")
        elif rel.startswith("_tools/"):
            nuevas.append(f"{rel} | {size} | (propio) | 2026-10-07 | {desc_tools.get(rel, 'archivo de trabajo propio')}")
        elif fn.endswith(".txt"):
            nuevas.append(f"{rel} | {size} | (derivado de {fn[:-4]}) | 2026-10-07 | texto extraído o resumen propio del original")
        else:
            nuevas.append(f"{rel} | {size} | (ver línea del original) | 2026-10-07 | sin descripción")
open(fu, "a").write("\n".join(nuevas) + "\n")
print(len(nuevas))
