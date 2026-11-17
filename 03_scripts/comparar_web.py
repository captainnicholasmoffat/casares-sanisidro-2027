#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Control: todo el texto de la web (programa.json) está en el documento, letra por letra.
Compara cada párrafo, cada fila de cuadro y cada fuente, sin etiquetas ni acentos codificados.
Uso: python3 03_scripts/comparar_web.py programa.json"""
import json, re, sys, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('w', Path(__file__).with_name('web_a_doc.py')); w = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0]] + sys.argv[1:]; spec.loader.exec_module(w)
todo = ' \n '.join(w.norm(re.sub(r'<br\s*/?>', ' ', w.TXT[f])) for f in w.FILES)
textos = {b['t'] for b in w.bloques()}
faltan = 0
for e in json.load(open(sys.argv[1])):
    for i, p in enumerate(w.pars(e)):
        t = w.norm(p)
        if t not in textos and w.sin_numero(t) not in textos and w.sin_numero(t) not in todo:
            faltan += 1; print(f'{e["id"]} p{i}: {t[:100]}')
    for c in e.get('cuadros', []):
        for l in c['texto'].split('\n'):
            for celda in [x.strip() for x in l.split('|')] if '|' in l else [l.strip()]:
                if celda and w.norm(celda) not in todo:
                    faltan += 1; print(f'{e["id"]} cuadro: {celda[:100]}')
    for p in [x for x in (e.get('fuentes') or '').split('\n\n') if x.strip()]:
        donde, _, que = p.partition(': ')
        if w.norm(que) not in todo:
            faltan += 1; print(f'{e["id"]} fuente: {p[:100]}')
print(f'\n{faltan} piezas de la web que no están en el documento.')
