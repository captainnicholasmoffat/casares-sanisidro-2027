import json, shutil, re
from pathlib import Path
P = Path('/home/claude/proyecto/web/data/programa.json')
T = Path('/home/claude/proyecto/web/data/tonos.json')
shutil.copy(P, '/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/programa_antes_comercio.json')
d = json.loads(P.read_text()); by = {e['id']: e for e in d}
log = []

def bold_label(p):
    """Negrita del rótulo: hasta el primer punto seguido de espacio (incluido el punto)."""
    return [[0, p.index('. ') + 1, 'b']]

def entry(eid, titulo, paras, hoja, capitulo, recuadro_de=None, tono=None, marcas=None, subt=None, orden=None):
    e = {'id': eid, 'capitulo': capitulo, 'titulo': titulo, 'hoja_a4': hoja, 'hoja_a4_fin': hoja,
         'texto': '\n\n'.join(paras), 'cuadros': [], 'fuentes': ''}
    if subt is not None: e['subtitulos'] = subt
    if orden is not None: e['orden'] = orden
    if recuadro_de: e['recuadro_de'] = recuadro_de
    if marcas: e['marcas'] = marcas
    if tono: e['tono'] = tono
    return e

def box(eid, titulo, paras):
    m = {str(i): bold_label(p) for i, p in enumerate(paras)}
    return entry(eid, titulo, paras, 96, '5 · Qué hacemos en cada área', '5.11', 'g', m)

# ---------- 1. 5.11, párrafo 5: anuncia las cuatro medidas ----------
e = by['5.11']; ps = e['texto'].split('\n\n')
old = 'El centro comercial de un barrio también es parte de su infraestructura.'
assert ps[5].endswith(old)
add = (' Además, proponemos cuatro medidas para el comercio de cercanía, que se explican en los recuadros: '
       'que el comercio chico pague la tasa según lo que vende, que el Municipio le compre al comercio de San Isidro, '
       'que lo que sobra llegue a los comedores y que los hornos gasten menos luz.')
ps[5] += add; e['texto'] = '\n\n'.join(ps)
log.append(('5.11', 'párrafo 5 (se agrega al final)', old, old + add))

# ---------- 2. Cuatro recuadros nuevos ----------
r3 = box('5.11-r3', 'Nuestra propuesta: la tasa del comercio chico, a la medida de lo que vende', [
 'La tasa de seguridad e higiene es lo que más cobra el propio Municipio. En 2025 fueron 89.391 millones, el 29% de todo lo que entró. Pero no pesa igual en todos. El último dato publicado de cómo se reparte es de 2020: de unos 10.900 comercios, el 17% pagaba el 86,5%. El comercio chico paga una cuota fija por mes, venda mucho o poco. Con la cuota de 70.000 pesos y ventas de 2,5 millones por mes, paga el 2,8% de lo que vende. Un comercio que vende más de 33 millones por mes paga el 0,9%.',
 '1 · La inteligencia artificial del Municipio asesora al comerciante. Le explica cada impuesto, tasa y costo, y le dice cómo pagar lo menos posible sin salirse de la ley. Le aplica sola lo más barato que la norma ya permite: el régimen simplificado, la rebaja por antigüedad, la del primer empleo y el mínimo reducido. Le arma la declaración jurada, sin trámites.',
 '2 · Un tope atado al monotributo. Para el comercio monotributista, la cuota de la tasa no va a poder pasar de un porcentaje de lo máximo que puede vender su categoría de monotributo. Por ejemplo, la categoría D vende hasta 2,55 millones de pesos por mes, y la K, hasta 10,55 millones. Guaminí ya cobra así: el 0,75% de lo máximo de cada grupo de categorías (Decreto 372/2025).',
 '3 · Mentirle al Municipio no sirve. La categoría la controla Nación con la factura electrónica, y la ley deja que el Municipio le pida ese dato (Ley 11.683, artículo 101). Lo que el comerciante declare al Municipio no cambia su tope.',
 '4 · Lo pagan los grandes, y el Municipio no cobra menos. Con el presupuesto de 2026, los comercios chicos dejarían de pagar entre 2.970 y 3.429 millones por año: un cuarto de lo que pagan hoy. Eso se cubre con una suba de alrededor de 4% en lo que pagan los comercios grandes. Un comercio grande que hoy paga el 0,9% de lo que vende pasaría a pagar el 0,94%. Cada año, la inteligencia artificial del Municipio calcula el tope para que el alivio entre justo en lo que suben los grandes. La suba la vota la Asamblea de Concejales y Mayores Contribuyentes, como cada aumento de una tasa (anexo, Ordenanza 17).',
 'Es un primer paso. El reparto publicado es de 2020, y desde 2025 existe el régimen simplificado. Por eso las cifras son un rango. Cuando se conozca el reparto de hoy, el alivio se puede ampliar. Las empresas que no son monotributistas siguen pagando como hoy. Un fallo de la Corte Suprema de 2026 sobre esta tasa es un riesgo para las cuentas, con o sin esta propuesta (3.6).',
 'Cuánto cuesta y de dónde sale. Nada: lo que dejan de pagar los comercios chicos lo pagan los grandes. El asesoramiento es parte de la inteligencia artificial del Municipio (4.11).',
])
r4 = box('5.11-r4', 'Nuestra propuesta: el Municipio le compra al comercio de San Isidro', [
 'El Municipio gasta unos 6.200 millones por año en cosas que un comercio chico de San Isidro podría venderle. En 2025 fueron 6.237 millones: 5.122 en alimentos, 446 en ferretería, pinturas y material eléctrico, 342 en artículos de limpieza, 318 en papel y útiles, y 8 en utensilios de cocina. Las compras grandes van a pocos distribuidores. Entre 2024 y 2026, siete compras de alimentos, por 1.485 millones, fueron al mismo proveedor.',
 '1 · Compre San Isidro. La ley provincial ya deja pagarle hasta 5% más a quien tiene domicilio o comercio en San Isidro, en cualquier compra (Ley Orgánica de las Municipalidades, artículo 156 bis). Coronel Dorrego y Pellegrini ya lo usan. Una ordenanza va a aplicar esa prioridad a los comercios habilitados en San Isidro hace al menos un año (anexo, Ordenanza 18).',
 '2 · Compras partidas. Cada compra se va a dividir por renglón y por zona, para que un comercio chico pueda cotizar lo suyo, como hizo Pellegrini.',
 '3 · La inteligencia artificial del Municipio trae al comercio. Arma el registro de proveedores con los comercios habilitados, le avisa a cada uno cuando hay una compra de su rubro y lo ayuda a cotizar.',
 '4 · El que dona suma puntaje. El comercio que dona lo que le sobra a los comedores suma puntaje en la calificación de cada compra. Con mejor puntaje, el Municipio le compra a él antes que a otro, siempre dentro del límite de 5% sobre la mejor oferta.',
 '5 · Todo a la vista. Cada compra se publica el día que se hace, con quién ganó, quiénes se presentaron, el precio y el domicilio del proveedor (anexo, Ordenanza 2).',
 '6 · Control. La inteligencia artificial del Municipio compara cada precio con el del mercado y avisa cuando uno se sale de lo normal, como propone el 5.6 para los insumos de salud. Cada asociación vecinal ve las compras de su zona y puede objetarlas. Así, una compra chica no abre la puerta al favoritismo.',
 'Cuánto cuesta y de dónde sale. Como mucho, 312 millones por año. Es el 5% de los 6.237 millones, si todo se le comprara a comercios de San Isidro y todos cotizaran 5% más caro. Sale de la parte libre del gasto flexible (3.4). A cambio, ese dinero queda en San Isidro. El trabajo de muchas compras chicas lo hace la inteligencia artificial del Municipio.',
])
r5 = box('5.11-r5', 'Nuestra propuesta: lo que sobra, a los comedores', [
 'La comida que a un comercio le sobra en el día puede llegar a un comedor esa misma tarde. La ley permite donar alimentos en buen estado y protege al que dona de buena fe: sólo responde si hubo dolo o culpa (Leyes 25.989 y 27.454). La Provincia adhirió e invitó a los municipios (Ley 15.202). Pero la ley pide papeles: el que dona anota qué donó, cuándo y a quién, con la firma del que recibe, y el comedor tiene que estar inscripto en un registro nacional. En 2020, el Municipio asistía a 55 comedores. No hay un dato más nuevo.',
 '1 · Todos los comercios, no sólo las panaderías. También verdulerías, carnicerías, rotiserías, restaurantes y supermercados.',
 '2 · La inteligencia artificial del Municipio conecta. El comercio le avisa lo que le sobra, con una foto o hablando. Ella lo asigna al comedor más cercano que lo necesita y que puede retirarlo a tiempo, y agenda el retiro.',
 '3 · Los papeles los lleva ella. Anota cada donación como pide la ley y lleva el registro de donantes. El comercio no llena nada.',
 '4 · Ayuda a los comedores a inscribirse. El registro nacional es lo que les permite recibir. Al comedor que no tiene forma legal, lo ayuda a conseguirla.',
 '5 · El retiro lo hace el comedor o una cooperativa del barrio. Va con el carnet de manipulador de alimentos. Lo que se echa a perder rápido tiene que llegar enseguida y, si hace falta, con frío.',
 '6 · Sin costo, con reconocimiento. El comercio que dona suma puntaje en las compras del Municipio (recuadro anterior).',
 'Cuánto cuesta y de dónde sale. Casi nada: es una función más de la inteligencia artificial del Municipio (4.11). Falta medir cuánto cuesta el retiro si lo hace una cooperativa. El comercio inscripto en IVA pierde el crédito del IVA de lo que dona, y eso lo decide Nación.',
])
r6 = box('5.11-r6', 'Nuestra propuesta: la luz de los hornos', [
 'Un diagnóstico gratis de cuánta luz gasta un comercio sirve sólo si después consigue el crédito para cambiar el equipo. Un programa nacional hizo 219 diagnósticos gratis en pymes, y sólo 13 terminaron en una inversión con crédito. Las empresas no sabían que el crédito existía, y el trámite era muy complicado (Banco Mundial, 2018). El ahorro típico es de cerca de 10% sin invertir casi nada, y llega a 30%. Con la tarifa alta, cada punto de ahorro vale más.',
 '1 · Diagnóstico gratis. Se hace con el programa del Consejo Federal de Inversiones, que forma gestores de energía con universidades y sigue activo en 2026.',
 '2 · La inteligencia artificial del Municipio arma el pedido de crédito. Le dice al comercio qué línea le corresponde y le prepara la carpeta. Así ataca justo la causa por la que falló el programa nacional.',
 '3 · Con líneas que ya existen. Una es el crédito PEM de la Provincia para eficiencia energética. Es para industria, así que una panadería inscripta sólo como comercio puede quedar afuera.',
 'Cuánto cuesta y de dónde sale. Para el Municipio, casi nada: el diagnóstico lo paga el Consejo Federal de Inversiones, y el crédito, los bancos. Falta confirmar que la Provincia participe de ese programa del Consejo.',
])
news = [r3, r4, r5, r6]
pos = d.index(by['5.11-r2']) + 1
for k, b in enumerate(news): d.insert(pos + k, b); by[b['id']] = b
o = by['5.11']['orden']; i = o.index(['p', 5]) + 1
o[i:i] = [['box', b['id']] for b in news]
tonos = json.loads(T.read_text())
for b in news: tonos[b['id']] = 'g'
for b in news: log.append((b['id'], 'recuadro nuevo · ' + b['titulo'], '', b['texto']))

# ---------- 3. 3.6: el riesgo del fallo Pergamino ----------
e = by['3.6']; ps = e['texto'].split('\n\n')
o3 = 'Es el riesgo más concreto de los cuatro.'; n3 = 'Es el riesgo más concreto de los cuatro primeros.'
assert ps[3].count(o3) == 1
pos3 = ps[3].index(o3); ps[3] = ps[3].replace(o3, n3)
for m in e['marcas']['3']:
    if m[0] >= pos3 + len(o3): m[0] += len(n3) - len(o3); m[1] += len(n3) - len(o3)
log.append(('3.6', 'punto 4', o3, n3))
p5 = ('5. La tasa de seguridad e higiene puede traer juicios por un fallo de la Corte Suprema. Es el fallo del 10 de septiembre de 2026 sobre la tasa de Pergamino. '
      'Dice que lo que se cobra no puede pasar de «una parte importante —por ejemplo, hasta el doble— del costo» del servicio, y que el Municipio tiene que probar que inspecciona. '
      'En 2026, San Isidro espera cobrar 96.593 millones por esta tasa, casi 35 veces lo que cuesta su Agencia de Fiscalización y Control, que inspecciona comercios y obras. '
      'La tasa es el 29% de lo que entra al Municipio. Este riesgo existe con o sin este programa. La propuesta para el comercio chico (5.11) no cambia esa cuenta, porque el Municipio cobra lo mismo en total. '
      'Las inspecciones grabadas y con fecha fija (5.9) son la prueba de servicio que pide la Corte, aunque no alcanzan para llegar al doble del costo. Lo tiene que estudiar un abogado tributarista.')
ps.insert(4, p5); e['texto'] = '\n\n'.join(ps)
mk = {}
for k, v in e['marcas'].items(): mk[str(int(k) + 1) if int(k) >= 4 else k] = v
mk['4'] = [[3, p5.index('. ', 3) + 1, 'b']]
e['marcas'] = dict(sorted(mk.items(), key=lambda kv: int(kv[0])))
o = e['orden']; new = []
for t, x in o:
    if t in ('p', 'h3') and isinstance(x, int) and x >= 4: x += 1
    new.append([t, x])
    if [t, x] == ['p', 3]: new.append(['p', 4])
e['orden'] = new
log.append(('3.6', 'punto 5 nuevo', '', p5))

# ---------- 4. Anexo: dos ordenanzas nuevas ----------
e = by['anexo']; o4 = 'y quince cortas'; n4 = 'y diecisiete cortas'
assert e['texto'].count(o4) == 1; e['texto'] = e['texto'].replace(o4, n4); log.append(('anexo', 'introducción', o4, n4))
def ordz(eid, titulo, arts):
    paras, subt, orden = [], [], []
    for h, t in arts:
        orden += [['h3', len(paras)], ['p', len(paras) + 1]]
        subt.append({'titulo': h, 'hoja_a4': 126}); paras += [h, t]
    return entry(eid, titulo, paras, 126, 'Anexo · Las ordenanzas que proponemos', subt=subt, orden=orden)
a17 = ordz('anexo-17', '17 · Ordenanza del tope de la tasa de seguridad e higiene', [
 ('Artículo 1 — Tope para el comercio monotributista', 'Quien paga la Tasa por Inspección de Seguridad e Higiene y está inscripto en el monotributo paga por mes, como máximo, un porcentaje de los ingresos brutos máximos de su categoría, dividido por doce. La Ordenanza Impositiva fija cada año ese porcentaje. Si la cuota que le corresponde es menor, paga la cuota.'),
 ('Artículo 2 — La categoría', 'La categoría es la que informa la Agencia de Recaudación y Control Aduanero (ARCA), a pedido del Departamento Ejecutivo (Ley 11.683, artículo 101). Lo que el contribuyente declare al Municipio no cambia su tope. Si no está en el monotributo o su categoría no se puede verificar, paga como hasta ahora.'),
 ('Artículo 3 — Sin que baje lo que se cobra', 'Lo que se deja de cobrar por el tope se cubre con una suba de las alícuotas sobre los ingresos de los demás contribuyentes, de modo que la recaudación total de la tasa no baje. El primer año, el tope alivia alrededor de un cuarto de lo que pagan los comercios alcanzados, y la suba es de alrededor de 4%. Cada año, el Departamento Ejecutivo publica el cálculo, que prepara la inteligencia artificial del Municipio con lo recaudado el año anterior.'),
 ('Artículo 4 — Asesoramiento', 'La inteligencia artificial del Municipio le explica a cada contribuyente cuánto le corresponde pagar y qué beneficios de la Ordenanza Fiscal puede usar, y le prepara la declaración jurada.'),
 ('Artículo 5 — Cómo se aprueba', 'Por aumentar alícuotas, esta ordenanza se vota en la Asamblea de Concejales y Mayores Contribuyentes (Constitución de la Provincia, artículo 193, inciso 2).'),
])
a18 = ordz('anexo-18', '18 · Ordenanza de compras al comercio de San Isidro y de donación de alimentos', [
 ('Artículo 1 — Prioridad local', 'En las compras del Municipio se prefiere la oferta de un comercio habilitado en San Isidro hace al menos un año, aunque sea más cara, siempre que no supere en más de 5% a la mejor oferta (Ley Orgánica de las Municipalidades, artículo 156 bis).'),
 ('Artículo 2 — Compras por renglón y por zona', 'Las compras de alimentos, artículos de limpieza, ferretería y útiles se licitan por renglón y por zona, y cada renglón se adjudica por separado, para que pueda cotizar un comercio chico. Dividir una compra no cambia el procedimiento que corresponde a su monto total. La inteligencia artificial del Municipio arma el registro de proveedores con los comercios habilitados, le avisa a cada uno las compras de su rubro y lo ayuda a cotizar.'),
 ('Artículo 3 — Donación de alimentos', 'La inteligencia artificial del Municipio conecta al comercio que dona alimentos con el comedor inscripto más cercano que pueda retirarlos a tiempo. Registra cada donación con los datos que pide la Ley 25.989, lleva el registro de donantes y ayuda a los comedores a inscribirse en el registro nacional de instituciones receptoras de alimentos.'),
 ('Artículo 4 — Puntaje del que dona', 'El comercio que dona alimentos suma puntaje en la calificación de las ofertas, dentro del límite de 5% del artículo 1. El Departamento Ejecutivo fija y publica cómo se calcula.'),
 ('Artículo 5 — Control', 'Cada compra se publica como manda el artículo 2 de la Ordenanza 2. La inteligencia artificial del Municipio marca los precios que se salen de lo normal. La asociación vecinal de cada zona ve las compras de su zona y puede objetarlas por escrito, y el Departamento Ejecutivo le responde con sus razones.'),
])
pos = d.index(by['anexo-16']) + 1
d.insert(pos, a17); d.insert(pos + 1, a18); by['anexo-17'] = a17; by['anexo-18'] = a18
for a in (a17, a18): log.append((a['id'], 'ordenanza nueva · ' + a['titulo'], '', a['texto']))

# ---------- 5. Lo que tiene que confirmar un abogado ----------
e = by['metodo-abogado']; ps = e['texto'].split('\n\n')
i36 = '• 3.6. El fallo de la Corte Suprema sobre la tasa de seguridad e higiene de Pergamino, y lo que significa para la tasa de San Isidro: lo tiene que estudiar un abogado tributarista.'
i511 = ['• 5.11. El tope de la tasa de seguridad e higiene atado a la categoría de monotributo, y el pedido de esa categoría a ARCA (Ley 11.683, artículo 101; Ordenanza 17 del anexo).',
        '• 5.11. El puntaje en las compras del Municipio para el comercio que dona alimentos, dentro del 5% de la Ley Orgánica de las Municipalidades (artículo 156 bis), y las compras por renglón y por zona (Ordenanza 18 del anexo).',
        '• 5.11. Quién lleva el registro de donantes de alimentos que pide la Ley 25.989 (Ordenanza 18 del anexo).']
last511 = max(i for i, p in enumerate(ps) if p.startswith('• 5.11.'))
ps[last511 + 1:last511 + 1] = i511
ps.insert(1, i36)
e['texto'] = '\n\n'.join(ps)
e['orden'] = [['p', i] for i in range(len(ps))]
e['marcas'] = {str(i): [[2, p.index('. ', 2) + 1, 'b']] for i, p in enumerate(ps) if p.startswith('• ')}
for x in [i36] + i511: log.append(('metodo-abogado', 'punto nuevo', '', x))

# ---------- 6. Fuentes del 5.11 ----------
f_add = (' 5.11 · el comercio de cercanía: tasa de seguridad e higiene, ejecución de recursos 2025 y Presupuesto 2026 del Municipio (programa 53, Agencia de Fiscalización y Control); '
         'el reparto de 2020, exposición de motivos de la Ordenanza Fiscal 2022; Ordenanzas Fiscal 9414 e Impositiva 9415; categorías de monotributo de ARCA desde el 1 de agosto de 2026; '
         'Ley 11.683, artículo 101; Guaminí, Decreto 372/2025; el alivio y la suba, cálculo propio sobre la tasa presupuestada para 2026 y el reparto de 2020. '
         'Compras: ejecución del gasto por objeto 2025 del Municipio y Boletín Oficial de San Isidro; Ley Orgánica de las Municipalidades, artículo 156 bis; Coronel Dorrego, Decreto 3007/2025, y Pellegrini, Decreto 862/2025. '
         'Donación de alimentos: Leyes 25.989 y 27.454; Ley provincial 15.202; comedores asistidos, Municipio de San Isidro, 2020. '
         'Energía: Banco Mundial, informe del proyecto de eficiencia energética, 2018; Secretaría de Industria, guía de energía para pymes, 2023; Consejo Federal de Inversiones; créditos PEM de la Provincia. '
         'El fallo de la Corte Suprema: CSJ 1105/2023, 10 de septiembre de 2026; Constitución de la Provincia, artículo 193, inciso 2.')
by['5.11']['fuentes'] += f_add; log.append(('5.11', 'fuentes (se agrega al final)', '', f_add.strip()))

# ---------- chequeos ----------
txt = ' '.join(x[3] for x in log).lower()
for bad in ['plata', 'mafia', 'sobreprecio', 'candidat', 'guamaní', ' ia ', 'partido']:
    assert bad not in txt, bad
for b in news + [by['3.6'], by['metodo-abogado']]:
    ps = b['texto'].split('\n\n')
    for k, ms in b.get('marcas', {}).items():
        for a, z, _ in ms: assert 0 <= a < z <= len(ps[int(k)]), (b['id'], k, a, z)
P.write_text(json.dumps(d, ensure_ascii=False, indent=1))
T.write_text(json.dumps(tonos, ensure_ascii=False, indent=0))
out = ['# Comercio de cercanía: cambios ya aplicados en la web (16 de octubre de 2026)', '',
       'Aprobados por Nick el 16 de octubre (propuestas del doc «Comercio de cercanía: cuatro propuestas nuevas»). El worker del documento tiene que copiar estos textos tal cual al PDF, la A4 y el Excel.', '']
for eid, where, old, new in log:
    out += [f'## {eid} · {where}']
    if old: out += [f'- Antes: «{old}»']
    out += [f'- Después: «{new}»' if old else new, '']
Path('/home/claude/proyecto/CAMBIOS_WEB_COMERCIO.md').write_text('\n'.join(out))
print(len(log), 'cambios')
for b in news + [by['3.6']]:
    for k, ms in b['marcas'].items():
        p = b['texto'].split('\n\n')[int(k)]
        print(b['id'], k, '|', ' / '.join(p[a:z] for a, z, _ in ms)[:90])
