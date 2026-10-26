import json, re, difflib
from pathlib import Path
S = '/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad'
base = {e['id']: e for e in json.load(open(S + '/programa_antes_comercio.json'))}
cur = {e['id']: e for e in json.load(open('/home/claude/proyecto/web/data/programa.json'))}
P = lambda e: e['texto'].split('\n\n')
def sents(p): return [x for x in re.split(r'(?<=[.:;])\s+(?=[A-ZÁÉÍÓÚÑ¿«•\d])', p) if x]
def para_changes(eid):
    a, b = P(base[eid]), P(cur[eid]); out = []
    sm = difflib.SequenceMatcher(None, a, b)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        if op == 'insert':
            prev = a[i1 - 1] if i1 else ''
            for p in b[j1:j2]: out.append(f'- Párrafo nuevo, después del que empieza «{prev[:60]}…»:\n  «{p}»')
            continue
        for k in range(max(i2 - i1, j2 - j1)):
            pa = a[i1 + k] if i1 + k < i2 else ''; pb = b[j1 + k] if j1 + k < j2 else ''
            if not pa: out.append(f'- Párrafo nuevo, después del que empieza «{a[i2-1][:60]}…»:\n  «{pb}»'); continue
            if pb.startswith(pa):
                out.append(f'- Al final del párrafo que empieza «{pa[:60]}…», agregá:\n  «{pb[len(pa):].strip()}»'); continue
            sa, sb = sents(pa), sents(pb); ss = difflib.SequenceMatcher(None, sa, sb)
            for o2, x1, x2, y1, y2 in ss.get_opcodes():
                if o2 == 'equal': continue
                if o2 == 'insert':
                    out.append(f'- Después de «{sa[x1-1]}», agregá:\n  «{" ".join(sb[y1:y2])}»')
                else:
                    out.append(f'- Antes: «{" ".join(sa[x1:x2])}»\n  Después: «{" ".join(sb[y1:y2])}»')
    return out

L = []
w = L.append
w('DISPATCH 18 DEL DOCUMENTO · Lo que cambió en la web, al PDF y a la A4 (16 de octubre)')
w('')
w('Base: commit 917c9fe. La web (sanisidro2027.pages.dev) es la versión al día del programa. Estos textos ya están publicados y aprobados por Nick: copialos tal cual al PDF de pantalla y a la A4, con el diseño aprobado. El Excel no cambia: ninguna cifra del modelo se mueve (el 51,8%, el 48,2% y el 44,7% quedan).')
w('')
w('Reglas de siempre: sin «plata», «mafia» ni «sobreprecio»; siempre «la inteligencia artificial del Municipio»; «San Isidro», nunca «partido»; ninguna oración ni punto empieza con «Y» o con «Que»; en un mismo párrafo, dos oraciones no empiezan con la misma palabra; sin fechas de actualización en el cuerpo.')
w('')
w('A · CAMBIOS DEL 12 DE OCTUBRE (versión 1.1), que todavía no están en el PDF')
w('')
v11 = Path('/home/claude/proyecto/CAMBIOS_WEB_V1_1.md').read_text().split('\n')
n = 0
for line in v11:
    if line.startswith('## '): n += 1; w(f'A{n} · {line[3:].replace(" · texto", "")}')
    elif line.startswith('- Antes') or line.startswith('- Después'): w(line)
w('')
w('B · COMERCIO DE CERCANÍA (16 de octubre): cuatro propuestas nuevas para el comercio chico, un riesgo nuevo y dos ordenanzas')
w('')
w('B1 · 5.11, párrafo de comercio (el que empieza «Proponemos dos medidas…»)')
L += para_changes('5.11'); w('')
w('B2 · 5.11: cuatro recuadros nuevos, verdes, como los otros «Nuestra propuesta». Van justo después de ese párrafo y antes del subtítulo «Multas de tránsito: que todos las puedan pagar…», en este orden. En negrita: la primera oración del primer párrafo de cada recuadro y, en cada punto, el rótulo hasta el primer punto (por ejemplo, «1 · Compre San Isidro.»), y también «Cuánto cuesta y de dónde sale.» y «Es un primer paso.».')
for k, rid in enumerate(['5.11-r3', '5.11-r4', '5.11-r5', '5.11-r6'], 1):
    e = cur[rid]; w(''); w(f'Recuadro {k} · {e["titulo"]}'); w('')
    for p in P(e): w(p); w('')
w('B3 · 3.4, párrafo que empieza «Cada año, el Municipio puede decidir libremente…»')
L += para_changes('3.4'); w('')
w('B4 · 3.6 «Qué habría que vigilar». El punto 5 va después del punto 4 y antes del gráfico 19; la primera oración del punto 5 en negrita, como en los otros cuatro.')
L += para_changes('3.6'); w('')
w('B5 · Anexo')
L += para_changes('anexo')
w('- Dos ordenanzas nuevas, después de la 16 y antes de «Lo que estas ordenanzas no dicen, y por qué», con el mismo formato que las otras:')
for aid in ['anexo-17', 'anexo-18']:
    e = cur[aid]; ps = P(e); w(''); w(e['titulo']); w('')
    for i in range(0, len(ps), 2): w(ps[i]); w(ps[i + 1]); w('')
w('B6 · Nota de método, «Lo que tiene que confirmar un abogado»: cuatro puntos nuevos, en el orden de los apartados (el del 3.6 va primero; los del 5.11, después del último punto del 5.11 que ya está). En negrita, el número de apartado, como en los otros.')
L += [x for x in para_changes('metodo-abogado')]; w('')
w('B7 · Fuentes del 5.11 (anexo de fuentes): al final de lo que ya dice el 5.11, agregá:')
w('«' + cur['5.11']['fuentes'][len(base['5.11']['fuentes']):].strip() + '»'); w('')
w('C · CONTROLES Y ENTREGA')
w('- Ningún cuadro ni gráfico nuevo: la numeración de cuadros no cambia.')
w('- Si el índice lista las ordenanzas del anexo, sumá la 17 y la 18; actualizá los números de hoja del índice y las remisiones.')
w('- A4: ninguna hoja con más de un tercio en blanco (salvo la última), cada capítulo arriba de su hoja, ninguna sección que empiece al pie con sólo el título, sin texto escondido (una frase buscada cae en una sola hoja). Pantalla: ninguna página de más de 2.700 pt.')
w('- Barrido sobre los textos nuevos: «Y» y «Que» al empezar = 0; dos oraciones que empiezan igual en un párrafo = 0; palabras prohibidas = 0.')
w('- Números: la lista de números de cada capítulo, antes y después, igual salvo los nuevos de este dispatch.')
w('- Al terminar: PDF de pantalla y A4 a salida/. En el informe, decime en qué hoja de la A4 queda cada cambio de A y B, y en qué hoja empieza cada capítulo.')
out = '\n'.join(L)
Path(S + '/DISPATCH_18_DOCUMENTO.txt').write_text(out)
print(len(out)); print(out[:200])
