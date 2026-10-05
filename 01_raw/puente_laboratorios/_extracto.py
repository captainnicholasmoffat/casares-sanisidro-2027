#!/usr/bin/env python3
"""Uso: _extracto.py NOMBRE URL "descripcion" < texto
Guarda un extracto obtenido por WebFetch/WebSearch (cuando la descarga directa fallo) y lo registra en FUENTES.txt."""
import sys, os, datetime
D = os.path.dirname(os.path.abspath(__file__))
name, url, desc = sys.argv[1], sys.argv[2], sys.argv[3]
body = sys.stdin.read()
p = os.path.join(D, name + ".txt")
with open(p, "w", encoding="utf-8") as f:
    f.write("URL: " + url + "\nFecha de consulta: " + datetime.date.today().isoformat() +
            "\nATENCION: NO es copia del original. La descarga directa fallo; esto es el extracto que devolvio la herramienta WebFetch/WebSearch (resumen con citas).\n\n" + body)
with open(os.path.join(D, "FUENTES.txt"), "a", encoding="utf-8") as f:
    f.write(f"{name}.txt | {os.path.getsize(p)} | {url} | {datetime.date.today().isoformat()} | {desc} [EXTRACTO, no original]\n")
print("OK", p)
