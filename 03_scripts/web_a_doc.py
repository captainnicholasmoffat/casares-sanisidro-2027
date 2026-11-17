#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lleva al documento (doc/content_*.py) los cambios de texto de la web entre dos versiones de su programa.json.

La web (rama web-sanisidro, proyecto/web/data/programa.json) tiene el texto de cada apartado en párrafos, con sus
marcas (negrita «b», resaltado «sg», cursiva «i»), sus cuadros como tablas con «|» y el orden de cada pieza. El
documento tiene el mismo texto en HTML. Este script compara la versión vieja con la nueva y, en el HTML:
  - reemplaza cada párrafo, título, punto de lista o fila de cuadro que cambió;
  - agrega los párrafos, recuadros, filas y ordenanzas nuevos donde los pone la web;
  - agrega a la tabla de fuentes las fuentes nuevas.
Encuentra cada pieza vieja por su texto (sin etiquetas, sin acentos codificados y con los [[n:clave]] resueltos), así
que sólo funciona si el documento tenía todo el texto de la versión vieja (lo dice el Dispatch 20).

Uso: python3 03_scripts/web_a_doc.py viejo.json nuevo.json [--aplicar]
Sin --aplicar sólo informa qué encontró y qué haría.
"""
import difflib, html, json, re, sys
from html.entities import codepoint2name
from pathlib import Path

DOC = Path(__file__).resolve().parents[1] / 'doc'
FILES = ['content_a.py', 'content_b.py', 'content_c.py', 'content_d.py', 'content_e.py', 'content_f.py',
         'content_o.py', 'content_s.py']
sys.path.insert(0, str(DOC))
import content  # noqa: E402  (arma las secciones y numera cuadros y gráficos)
REFS = content.A._REFS

BLOCK = re.compile(r'<(p|li|h3|h2|td|th)\b([^>]*)>(.*?)</\1>|<div class="(clabel|stand)">(.*?)</div>', re.S)
TXT = {f: (DOC / f).read_text(encoding='utf-8') for f in FILES}
LOG, FALTAS, AVISOS = [], [], []


def ent(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return ''.join(f'&{codepoint2name[ord(c)]};' if ord(c) > 127 and ord(c) in codepoint2name
                   else (f'&#{ord(c)};' if ord(c) > 127 else c) for c in s)


def norm(s):
    s = re.sub(r'\[\[n:([a-z0-9_]+)\]\]', lambda m: str(REFS.get(m.group(1), m.group(0))), s)
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    return re.sub(r'\s+', ' ', s).strip()


def sin_numero(p):
    return re.sub(r'^(\d+\. |• )', '', p)


def bloques():
    out = []
    for f in FILES:
        for m in BLOCK.finditer(TXT[f]):
            tag = m.group(1) or 'div'
            attrs = m.group(2) or (f' class="{m.group(4)}"' if m.group(4) else '')
            out.append(dict(f=f, a=m.start(), b=m.end(), tag=tag, attrs=attrs, t=norm(m.group(0))))
    return out


def buscar(texto, cerca=None, tags=None):
    """El bloque del documento con ese texto. Si hay varios, el más cercano a 'cerca' (archivo, posición)."""
    cands = [b for b in bloques() if (b['t'] == texto or b['t'] == sin_numero(texto)) and (not tags or b['tag'] in tags)]
    if not cands:
        return None
    if len(cands) > 1 and cerca:
        cands.sort(key=lambda b: (b['f'] != cerca[0], abs(b['a'] - cerca[1])))
    return cands[0]


def inline(texto, marcas):
    """Texto con sus marcas, en HTML del documento."""
    abre = {'b': '<b>', 'sg': '<span class="sg">', 'i': '<i>'}
    cierra = {'b': '</b>', 'sg': '</span>', 'i': '</i>'}
    out, pos = [], 0
    for a, b, k in sorted(marcas or [], key=lambda m: m[0]):
        out += [ent(texto[pos:a]), abre[k], ent(texto[a:b]), cierra[k]]
        pos = b
    out.append(ent(texto[pos:]))
    return ''.join(out)


def con_refs(h, viejo_html):
    for clave in set(re.findall(r'\[\[n:([a-z0-9_]+)\]\]', viejo_html or '')):
        h = re.sub(rf'((?:cuadros?|gr&aacute;ficos?) ){REFS[clave]}\b', rf'\g<1>[[n:{clave}]]', h)
    return h


def bloque_html(tag, attrs, texto, marcas, viejo_html=''):
    if viejo_html:
        otras = set(re.findall(r'<([a-z0-9]+)', viejo_html)) - {'b', 'i', 'span', 'p', 'li', 'h3', 'h2', 'td', 'div'}
        if otras or 'class="m"' in viejo_html or 'class="n"' in viejo_html:
            AVISOS.append(f'párrafo con <{",".join(otras) or "span m/n"}>: revisar a mano: {norm(viejo_html)[:70]}')
    if tag == 'li':
        m = re.match(r'^(\d+\. |• )', texto)
        if m:
            n = len(m.group(1)); texto = texto[n:]
            marcas = [[max(0, a - n), b - n, k] for a, b, k in (marcas or [])]
    return con_refs(f'<{tag}{attrs}>{inline(texto, marcas)}</{tag}>', viejo_html)


def poner(f, a, b, nuevo):
    TXT[f] = TXT[f][:a] + nuevo + TXT[f][b:]


def fin_callout(f, pos):
    """Fin del <div class="callout"> que contiene la posición pos."""
    t = TXT[f]
    ini = t.rfind('<div class="callout', 0, pos)
    prof, i = 0, ini
    for m in re.finditer(r'<div\b|</div>', t[ini:]):
        prof += 1 if m.group(0) == '<div' else -1
        if prof == 0:
            return ini + m.end()
    raise SystemExit(f'callout sin cierre en {f}:{ini}')


# ------------------------------------------------------------------ párrafos de los apartados que cambiaron
def pars(e):
    return e['texto'].split('\n\n') if e['texto'] else []


def marcas(e, i):
    return (e.get('marcas') or {}).get(str(i), [])


def tipo(e, i):
    return 'h3' if ['h3', i] in (e.get('orden') or []) else None


def portar_parrafos(k, V, N):
    pv, pn = pars(V), pars(N)
    sm = difflib.SequenceMatcher(None, [norm(x) for x in pv], [norm(x) for x in pn], autojunk=False)
    ultimo = None  # (archivo, fin) del último bloque ubicado: ahí van los insertos
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        viejos = []
        for i in range(i1, i2):
            b = buscar(norm(pv[i]), cerca=(ultimo[0], ultimo[1]) if ultimo else None)
            if not b:
                FALTAS.append(f'{k} p{i}: no está en el documento: {norm(pv[i])[:90]}'); return
            viejos.append(b)
        if op == 'equal':
            for i, j, b in zip(range(i1, i2), range(j1, j2), viejos):
                if marcas(V, i) != marcas(N, j):
                    poner(b['f'], b['a'], b['b'], bloque_html(b['tag'], b['attrs'], pn[j], marcas(N, j), TXT[b['f']][b['a']:b['b']]))
                    LOG.append(f'{k} p{j}: marcas'); b = buscar(norm(pn[j]), cerca=(b['f'], b['a']))
                ultimo = (b['f'], b['b'])
            continue
        if op in ('replace', 'delete'):
            molde = viejos[0]
            f = molde['f']
            viejos_html = [TXT[b['f']][b['a']:b['b']] for b in viejos]
            # de atrás para adelante, así las posiciones no se corren
            for b in sorted(viejos[1:], key=lambda b: -b['a']):
                t = TXT[b['f']]; fin = b['b'] + (1 if t[b['b']:b['b'] + 1] == '\n' else 0)
                poner(b['f'], b['a'], fin, '')
            b = buscar(molde['t'], cerca=(f, molde['a']))
            nuevos = [bloque_html(tipo(N, j) or b['tag'], '' if tipo(N, j) and tipo(N, j) != b['tag'] else b['attrs'],
                                  pn[j], marcas(N, j), viejos_html[min(n, len(viejos_html) - 1)] if viejos_html else '')
                      for n, j in enumerate(range(j1, j2))]
            poner(f, b['a'], b['b'], '\n'.join(nuevos))
            LOG.append(f'{k}: {op} p{i1}-{i2 - 1} -> p{j1}-{j2 - 1}')
            ultimo = (f, b['a'] + len('\n'.join(nuevos)))
            continue
        if op == 'insert':
            if ultimo is None:
                FALTAS.append(f'{k}: inserto al principio (p{j1}) sin lugar'); continue
            f, pos = ultimo
            antes = [b for b in bloques() if b['f'] == f and b['b'] == pos]
            molde = antes[0] if antes else dict(tag='p', attrs='')
            nuevos = [bloque_html(tipo(N, j) or molde['tag'], '' if tipo(N, j) else molde['attrs'], pn[j], marcas(N, j))
                      for j in range(j1, j2)]
            ins = '\n' + '\n'.join(nuevos)
            poner(f, pos, pos, ins)
            LOG.append(f'{k}: insert p{j1}-{j2 - 1}')
            ultimo = (f, pos + len(ins))


# ------------------------------------------------------------------ recuadros y ordenanzas nuevos
def callout_html(e):
    partes = [f'<div class="callout {e.get("tono") or "g"}">', f'<div class="clabel">{ent(e["titulo"])}</div>']
    orden = e.get('orden') or [['p', i] for i in range(len(pars(e)))]
    for o in orden:
        if o[0] in ('p', 'h3'):
            partes.append(bloque_html(o[0], '', pars(e)[o[1]], marcas(e, o[1])))
    return '\n'.join(partes) + '\n</div>'


def ordenanza_html(e):
    partes = [f'<h2>{ent(e["titulo"])}</h2>', '']
    for o in e['orden']:
        tag, attrs = ('h3', '') if o[0] == 'h3' else ('p', ' class="tight"')
        partes.append(bloque_html(tag, attrs, pars(e)[o[1]], marcas(e, o[1])))
        if o[0] == 'p':
            partes.append('')
    return '\n'.join(partes)


def lugar_despues_de(pieza, padre):
    """(archivo, posición) justo después de una pieza del orden del apartado padre."""
    if pieza[0] in ('p', 'h3'):
        b = buscar(norm(pars(padre)[pieza[1]]))
        return (b['f'], b['b']) if b else None
    if pieza[0] == 'box':
        e = NUEVO[pieza[1]]
        b = buscar(norm(e['titulo']), tags=['div'])
        return (b['f'], fin_callout(b['f'], b['a'])) if b else None
    return None


def portar_nuevo(k):
    e = NUEVO[k]
    if k.startswith('anexo-'):
        prev = IDS[IDS.index(k) - 1]
        pe = NUEVO[prev]
        b = buscar(norm(pars(pe)[-1]))
        if not b:
            FALTAS.append(f'{k}: no encuentro el final de {prev}'); return
        poner(b['f'], b['b'], b['b'], '\n\n' + ordenanza_html(e))
        LOG.append(f'{k}: ordenanza nueva después de {prev}'); return
    padre = NUEVO[e['recuadro_de']]
    orden = padre['orden']; i = orden.index(['box', k])
    lugar = lugar_despues_de(orden[i - 1], padre)
    if not lugar:
        FALTAS.append(f'{k}: no encuentro {orden[i - 1]} de {padre["id"]}'); return
    f, pos = lugar
    # si la pieza es la última de un bloque de dos columnas, el recuadro va después del bloque, no adentro
    resto = TXT[f][pos:]
    if resto.lstrip().startswith('</div>'):
        abre = TXT[f].rfind('<div', 0, pos)
        if TXT[f][abre:abre + 18] == '<div class="cols">':
            pos += len(resto) - len(resto.lstrip()) + len('</div>')
    poner(f, pos, pos, '\n' + callout_html(e))
    LOG.append(f'{k}: recuadro nuevo después de {orden[i - 1]} de {padre["id"]}')


# ------------------------------------------------------------------ cuadros
CELDA = re.compile(r'<(td|th)([^>]*)>(.*?)</\1>', re.S)


def filas(c):
    """Las filas del cuadro (líneas con «|») y las líneas sueltas (subtítulo, fuente, nota), en orden."""
    return [l for l in c['texto'].split('\n') if l.strip()]


def es_fila(l):
    return '|' in l


def celdas(l):
    return [x.strip() for x in l.split('|')]


def trs():
    """Todas las filas de tabla del documento: (archivo, inicio, fin, textos de sus celdas)."""
    out = []
    for f in FILES:
        for m in re.finditer(r'<tr\b[^>]*>.*?</tr>', TXT[f], re.S):
            out.append((f, m.start(), m.end(), [norm(c.group(3)) for c in CELDA.finditer(m.group(0))]))
    return out


def buscar_tr(fila, cerca=None):
    quiero = [norm(x) for x in celdas(fila)]
    cands = [t for t in trs() if t[3] == quiero]
    if len(cands) > 1 and cerca:
        cands.sort(key=lambda t: (t[0] != cerca[0], abs(t[1] - cerca[1])))
    return cands[0] if cands else None


def adaptar(viejo_html, nuevo_texto, marcas_nuevas=None):
    """HTML del texto nuevo con las costumbres del bloque viejo: los [[n:clave]], los <br> antes de «1) », y la
    negrita o el resaltado de los pedazos que siguen igual."""
    h = inline(nuevo_texto, marcas_nuevas) if marcas_nuevas is not None else ent(nuevo_texto)
    for clave in set(re.findall(r'\[\[n:([a-z0-9_]+)\]\]', viejo_html)):
        h = re.sub(rf'((?:cuadros?|gr&aacute;ficos?) ){REFS[clave]}\b', rf'\g<1>[[n:{clave}]]', h)
    if '<br>' in viejo_html:
        h = re.sub(r'(:?) (\d+\) )', lambda m: m.group(1) + '<br>' + m.group(2), h)
    if marcas_nuevas is None:
        for tag, cuerpo in re.findall(r'<(b|span class="sg")>(.*?)</(?:b|span)>', viejo_html, re.S):
            e = ent(norm(cuerpo))
            if e and h.count(e) == 1:
                cierre = '</b>' if tag == 'b' else '</span>'
                h = h.replace(e, f'<{tag}>{e}{cierre}')
    otras = set(re.findall(r'<([a-z0-9]+)', viejo_html)) - {'b', 'i', 'span', 'br', 'td', 'th', 'p', 'li', 'h3', 'tr'}
    if otras:
        AVISOS.append(f'el bloque viejo tenía <{",".join(otras)}>: revisar a mano: {norm(viejo_html)[:60]}')
    return h


def tr_nuevo(molde_tr, fila_vieja, fila_nueva, mantener_clase=True):
    abre = re.match(r'<tr[^>]*>', molde_tr).group(0)
    if not mantener_clase:
        abre = abre.replace(' class="hi"', '')
    cs = list(CELDA.finditer(molde_tr))
    viejas = celdas(fila_vieja) if fila_vieja else [None] * len(cs)
    out = []
    for i, x in enumerate(celdas(fila_nueva)):
        c = cs[min(i, len(cs) - 1)]
        if fila_vieja and i < len(viejas) and norm(viejas[i]) == norm(x):
            out.append(c.group(0))
        else:
            out.append(f'<{c.group(1)}{c.group(2)}>{adaptar(c.group(3) if fila_vieja else "", x)}</{c.group(1)}>')
    sep = '\n' if '\n' in molde_tr else ''
    return abre + sep.join(out) + '</tr>'


def suelta(k, vieja, nueva):
    """Una línea suelta del cuadro (subtítulo, nota) cambiada: se cambia sólo el pedazo distinto, si es único."""
    b = buscar(norm(vieja))
    if b:
        t = TXT[b['f']][b['a']:b['b']]
        m = re.match(r'(<[^>]+>)', t); abre = m.group(1) if m else ''
        cierre = t[t.rfind('</'):]
        cuerpo = t[len(abre):len(t) - len(cierre)]
        poner(b['f'], b['a'], b['b'], abre + adaptar(cuerpo, re.sub(r'^Nota: ', '', nueva) if '<b>Nota:</b>' in cuerpo else nueva) + cierre)
        if '<b>Nota:</b>' in cuerpo:
            t2 = TXT[b['f']]; pos = t2.find(abre, b['a']) + len(abre)
            poner(b['f'], pos, pos, '<b>Nota:</b> ')
        LOG.append(f'{k}: línea suelta del cuadro'); return
    ops = [o for o in difflib.SequenceMatcher(None, vieja, nueva, autojunk=False).get_opcodes() if o[0] != 'equal']
    for op, a1, a2, b1, b2 in [('replace', ops[0][1], ops[-1][2], ops[0][3], ops[-1][4])]:
        for ctx in (12, 25, 40):
            antes, despues = vieja[max(0, a1 - ctx):a1], vieja[a2:a2 + ctx]
            viejo_e, nuevo_e = ent(antes + vieja[a1:a2] + despues), ent(antes + nueva[b1:b2] + despues)
            hits = [f for f in FILES if TXT[f].count(viejo_e) == 1]
            if len(hits) == 1 and sum(TXT[f].count(viejo_e) for f in FILES) == 1:
                TXT[hits[0]] = TXT[hits[0]].replace(viejo_e, nuevo_e); break
        else:
            FALTAS.append(f'{k}: línea suelta sin lugar: {vieja[:70]}'); return
    LOG.append(f'{k}: línea suelta del cuadro (pedazo)')


def portar_cuadro(k, cv, cn):
    fv, fn = filas(cv), filas(cn)
    if norm(cv['titulo']) != norm(cn['titulo']):
        FALTAS.append(f'{k}: cambió el título del cuadro: {cn["titulo"]}')
    sm = difflib.SequenceMatcher(None, fv, fn, autojunk=False)
    ultimo = None
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for i in range(i1, i2):
                if es_fila(fv[i]):
                    t = buscar_tr(fv[i], ultimo)
                    if t: ultimo = (t[0], t[2])
            continue
        viejas = [fv[i] for i in range(i1, i2)]
        nuevas = [fn[j] for j in range(j1, j2)]
        if (viejas and not all(es_fila(x) for x in viejas)) or (nuevas and not all(es_fila(x) for x in nuevas)):
            if len(viejas) == len(nuevas) == 1 and not es_fila(viejas[0]) and not es_fila(nuevas[0]):
                suelta(k, viejas[0], nuevas[0]); continue
            FALTAS.append(f'{k}: cambio mezclado de filas y líneas sueltas en «{cn["titulo"][:30]}»'); continue
        ubic = []
        for x in viejas:
            t = buscar_tr(x, ultimo)
            if not t:
                FALTAS.append(f'{k}: fila no encontrada: {x[:70]}'); return
            ubic.append(t)
        if ubic:
            f = ubic[0][0]; molde = TXT[f][ubic[0][1]:ubic[0][2]]
            html_nuevo = [tr_nuevo(TXT[t[0]][t[1]:t[2]], viejas[n], nuevas[n]) for n, t in enumerate(ubic[:len(nuevas)])]
            html_nuevo += [tr_nuevo(molde, None, x, mantener_clase=False) for x in nuevas[len(ubic):]]
            for t in sorted(ubic[1:], key=lambda t: -t[1]):
                fin = t[2] + (1 if TXT[t[0]][t[2]:t[2] + 1] == '\n' else 0); poner(t[0], t[1], fin, '')
            t0 = buscar_tr(viejas[0], (f, ubic[0][1]))
            poner(f, t0[1], t0[2], '\n'.join(html_nuevo)); ultimo = (f, t0[1] + len('\n'.join(html_nuevo)))
        else:
            f, pos = ultimo
            a0 = TXT[f].rfind('<tr', 0, pos); molde = TXT[f][a0:pos]
            ins = '\n' + '\n'.join(tr_nuevo(molde, None, x, mantener_clase=False) for x in nuevas)
            poner(f, pos, pos, ins); ultimo = (f, pos + len(ins))
        LOG.append(f'{k} «{cn["titulo"][:28]}»: {op} filas {i1}-{i2 - 1} -> {j1}-{j2 - 1}')


# ------------------------------------------------------------------ fuentes
def portar_fuentes(k, viejas, nuevas):
    pv = [x for x in (viejas or '').split('\n\n') if x.strip()]
    for p in [x for x in (nuevas or '').split('\n\n') if x.strip()]:
        if p in pv:
            continue
        donde, _, que = p.partition(': ')
        fila = f'<tr><td class="l">{ent(donde)}</td><td>{ent(que)}</td></tr>'
        # va después de la última fila de su apartado o de uno anterior
        sec = donde.split(' · ')[0]
        clave = [int(x) if x.isdigit() else 0 for x in sec.split('.')]
        t = TXT['content_f.py']; mejor = None
        for m in re.finditer(r'<tr><td class="l">([^<]*)</td>', t):
            s = html.unescape(m.group(1)).split(' · ')[0]
            try:
                c = [int(x) for x in s.split('.')]
            except ValueError:
                continue
            if c <= clave:
                mejor = t.find('</tr>', m.start()) + 5
        if mejor is None:
            FALTAS.append(f'{k}: no sé dónde va la fuente «{donde}»'); continue
        poner('content_f.py', mejor, mejor, '\n' + fila)
        LOG.append(f'{k}: fuente «{donde[:40]}»')


if __name__ == '__main__':
    VIEJO = {e['id']: e for e in json.load(open(sys.argv[1]))}
    lista = json.load(open(sys.argv[2])); NUEVO = {e['id']: e for e in lista}; IDS = [e['id'] for e in lista]
    cambiados = [k for k in IDS if k in VIEJO and json.dumps(NUEVO[k], sort_keys=True) != json.dumps(VIEJO[k], sort_keys=True)]
    for k in cambiados:
        portar_parrafos(k, VIEJO[k], NUEVO[k])
        for cv, cn in zip(VIEJO[k]['cuadros'], NUEVO[k]['cuadros']):
            if cv['texto'] != cn['texto'] or cv['titulo'] != cn['titulo']:
                portar_cuadro(k, cv, cn)
        if len(NUEVO[k]['cuadros']) != len(VIEJO[k]['cuadros']):
            FALTAS.append(f'{k}: cambió la cantidad de cuadros')
        if NUEVO[k].get('fuentes') != VIEJO[k].get('fuentes'):
            portar_fuentes(k, VIEJO[k].get('fuentes'), NUEVO[k].get('fuentes'))
        if NUEVO[k].get('titulo') != VIEJO[k].get('titulo'):
            FALTAS.append(f'{k}: cambió el título: {NUEVO[k]["titulo"]}')
    for k in [k for k in IDS if k not in VIEJO]:
        portar_nuevo(k)
        if NUEVO[k].get('fuentes'):
            portar_fuentes(k, '', NUEVO[k]['fuentes'])
    print('\n'.join(LOG)); print(f'\n{len(LOG)} cambios.')
    if AVISOS:
        print('\nAVISOS:'); print('\n'.join(AVISOS))
    if FALTAS:
        print('\nSIN RESOLVER:'); print('\n'.join(FALTAS))
    if '--aplicar' in sys.argv:
        for f in FILES:
            (DOC / f).write_text(TXT[f], encoding='utf-8')
        print('\nEscrito en doc/.')
