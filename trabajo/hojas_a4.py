"""Recalcula los números de hoja de la A4 en programa.json a partir del texto de la A4 publicada.
Uso: python3 -I hojas_a4.py <a4.txt de pdftotext> [--aplicar]"""
import json, re, sys
from pathlib import Path
A4 = sys.argv[1]; APLICAR = '--aplicar' in sys.argv
P = Path('/home/claude/proyecto/web/data/programa.json'); d = json.loads(P.read_text())
def nz(s):
    s = s.replace('­', '').replace('-\n', '')
    s = re.sub(r'\s+', '', s).lower()
    return re.sub(r'[«»"“”\'’]', '', s)
pages = [nz(p) for p in open(A4).read().split('\f')]
N = len(pages) - (1 if not pages[-1] else 0)
def find(snip, desde=1, hasta=None):
    k = nz(snip)
    if len(k) < 12: return None
    for i in range(desde - 1, (hasta or N)):
        if k in pages[i]: return i + 1
    # la oración puede caer entre dos hojas: probá con la primera mitad
    k2 = k[:max(12, len(k) // 2)]
    for i in range(desde - 1, (hasta or N)):
        if k2 in pages[i]: return i + 1
    return None
def first_sent(t):
    t = re.sub(r'^\d+ · |^\d+\. |^• ', '', t.strip())
    m = re.match(r'(.{20,160}?[.:;])(\s|$)', t)
    return (m.group(1) if m else t[:120])
def last_sent(t):
    t = t.strip(); parts = re.split(r'(?<=[.:;])\s+', t)
    s = parts[-1]
    return s if len(nz(s)) >= 15 else t[-120:]
INDICE_FIN = 4   # las hojas 2 a 4 son el índice
cambios, dudas = [], []
prev = INDICE_FIN + 1
for e in d:
    ps = [p for p in e['texto'].split('\n\n') if p.strip()]
    desde = max(INDICE_FIN + 1, prev - 6)
    tp = find(e['titulo'], desde) if e['titulo'] else None
    sp = find(first_sent(ps[0]), desde) if ps else None
    multi = ps and sum(nz(first_sent(ps[0])) in pg for pg in pages) > 1
    if tp and sp: ini = tp if (sp - 1 <= tp <= sp or multi) else sp
    else: ini = tp or sp
    if not ini: dudas.append((e['id'], 'sin inicio')); continue
    fin = find(last_sent(ps[-1]), ini) if ps else ini
    for c in e.get('cuadros', []):
        ct = c.get('texto', '').strip()
        if ct:
            cz = find(ct[-90:], ini, ini + 12)
            if cz and (not fin or cz > fin): fin = cz
    if not fin: fin = ini; dudas.append((e['id'], 'sin final'))
    if fin and fin < ini: fin = ini
    if fin - ini > 20: dudas.append((e['id'], f'rango raro {ini}-{fin}'))
    old = (e.get('hoja_a4'), e.get('hoja_a4_fin'))
    if old != (ini, fin): cambios.append((e['id'], old, (ini, fin)))
    e['hoja_a4'], e['hoja_a4_fin'] = ini, fin
    for st in e.get('subtitulos', []):
        h = find(st['titulo'], ini, fin + 1) or ini
        st['hoja_a4'] = h
    if e.get('fuentes_hojas_a4') and e.get('fuentes'):
        f = e['fuentes']; a = None; rest = f
        while a is None and rest:
            a = find(rest[:80], N - 12)
            if a is None: rest = rest.split(': ', 1)[1] if ': ' in rest[:150] else ''
        z = find(f[-80:], a or N - 12)
        if a and z: e['fuentes_hojas_a4'] = list(range(a, z + 1))
        else: dudas.append((e['id'], 'fuentes sin hoja'))
    if not e.get('recuadro_de'): prev = ini
print('hojas de la A4:', N)
print('entradas con cambio:', len(cambios))
for c in cambios[:400]:
    sh = c[2][0] - (c[1][0] or 0)
    print('  ', c, 'corre', sh)
print('dudas:', dudas)
if APLICAR: P.write_text(json.dumps(d, ensure_ascii=False, indent=1)); print('APLICADO')
