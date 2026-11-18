"""Modelo fiscal, 18/11/2026: lo que decidió Nick en la revisión completa (DECISIONES_NOVIEMBRE, 18/11), parte NÚMEROS.

1. Decisión 10: los 60 agentes de la patrulla se cuentan desde marzo de 2026. El modelo empieza en 2028 y ya los
   cuenta en todos sus años (fila 304); se agregan 2026 (diez meses, 842,8 M) y 2027 (1.011,4 M), que van al gráfico 13,
   y se corrigen las notas que decían «desde 2028» (Guía C9, Supuestos B70 y E304).
2. Decisión 2: el uso del modelo, las imágenes y el video de las seis funciones nuevas de la inteligencia artificial del
   Municipio, con el mismo método del cuadro 28 (precio por uso, escenario medio, 15% de contingencia, dólar de
   diciembre de 2025) y los precios publicados hoy por Z.ai, Cloudflare y Azure. Se suma a la plataforma (fila 161).
3. Decisión 3: la certificación de cada escalón de la partida vecinal, en un contrato aparte, pagado con lo que sobra del
   1,5% de funcionamiento; lo que falte, del gasto flexible (entra en el peor caso, fila 182).
4. Seguridad: lo que cuesta formar a los agentes de tránsito que pasan a la patrulla (sólo la formación).
Re-ejecutable: si el bloque AD ya existe, no hace nada.
Uso: python3 -I trabajo/cuentas_18nov.py   (después: soffice recalcula y extract.py rehace cuentas.json)"""
import copy
from pathlib import Path
import openpyxl

X = Path(__file__).resolve().parents[1] / 'proyecto/web/cuentas/modelo_fiscal.xlsx'
wb = openpyxl.load_workbook(X)
S, G = wb['Supuestos'], wb['Guía']
if any(isinstance(c.value, str) and c.value.startswith('AD · ') for c in S['B']):
    print('ya aplicado'); raise SystemExit

# ---------------------------------------------------------------- estilos copiados de filas que ya existen
EST = {'h': S['B285'], 'b': S['B286'], 'n': S['C286'], 'e': S['E286'], 'p': S['C252']}
r = S.max_row + 2


def fila(b, c=None, e=None, fmt='n', h=False):
    """Escribe una fila (B rótulo, C valor o fórmula, E nota) y devuelve su número."""
    global r
    S.cell(r, 2, b)._style = copy.copy(EST['h' if h else 'b']._style)
    if c is not None:
        S.cell(r, 3, c)._style = copy.copy(EST[fmt]._style)
    if e is not None:
        S.cell(r, 5, e)._style = copy.copy(EST['e']._style)
    r += 1
    return r - 1


def es(v, dec=0):
    """Número con punto de miles y coma decimal."""
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def nota(ws, ref, old, new):
    assert old in ws[ref].value, (ref, ws[ref].value[:120]); ws[ref] = ws[ref].value.replace(old, new, 1)


# ---------------------------------------------------------------- 1. los 60 agentes desde marzo de 2026
nota(S, 'E304', 'Cálculo propio. Entra en personal y en la función 2.1; sale del resultado.',
     'Cálculo propio. Se pagan desde marzo de 2026: 842,8 M en 2026, diez meses, y 1.011,4 M en 2027 (filas 305 y 306, '
     'gráfico 13). El modelo empieza en 2028 y los cuenta en personal y en la función 2.1 todos sus años; sale del resultado.')
assert S.max_row == 304, S.max_row  # debajo de la 304 no hay nada
S.cell(305, 2, 'Seguridad · los 60 agentes en 2026, de marzo a diciembre (diez meses): fuera del modelo')._style = copy.copy(EST['b']._style)
S.cell(305, 3, '=C304*10/12')._style = copy.copy(EST['n']._style)
S.cell(305, 5, 'Va sólo en los datos del gráfico 13, que proyecta desde 2025: el modelo empieza en 2028. 842,8 M.')._style = copy.copy(EST['e']._style)
S.cell(306, 2, 'Seguridad · los 60 agentes en 2027: fuera del modelo')._style = copy.copy(EST['b']._style)
S.cell(306, 3, '=C304')._style = copy.copy(EST['n']._style)
S.cell(306, 5, 'Va sólo en los datos del gráfico 13. 1.011,4 M.')._style = copy.copy(EST['e']._style)
r = S.max_row + 2
nota(S, 'B70', 'salvo lo que suma el programa y, desde 2028, los 60 agentes que se sumaron a la patrulla en 2026 (fila 304).',
     'salvo lo que suma el programa y los 60 agentes que se sumaron a la patrulla en marzo de 2026, que el modelo cuenta '
     'en todos sus años (fila 304; 2026 y 2027, filas 305 y 306).')
nota(G, 'C9', 'salvo el programa y, desde 2028, los 60 agentes que se sumaron a la patrulla en 2026: 1.011,4 M por año (Supuestos, fila 304).',
     'salvo el programa y los 60 agentes que se sumaron a la patrulla en marzo de 2026: 1.011,4 M por año, contados en '
     'todos los años del modelo (Supuestos, fila 304). En 2026 fueron 842,8 M, por diez meses.')

# ---------------------------------------------------------------- 2. funciones nuevas de la inteligencia artificial del Municipio
# Precios publicados hoy (18/11/2026), en dólares:
#   Z.ai, docs.z.ai/guides/overview/pricing: GLM-5.3 1,4 / 0,26 (entrada en caché) / 4,4 por millón de tokens;
#   GLM-5.3-Flash 0,15 / 0,03 / 0,50; GLM-4.6V 0,3 / 0,05 / 0,9; CogVideoX-3 0,2 por video.
#   Cloudflare Stream, developers.cloudflare.com/stream/pricing: 1 por cada 1.000 minutos vistos; 5 por mes por cada 1.000 guardados.
#   Azure, prices.azure.com (Suecia Central, Hot LRS): 0,0184 por GB por mes.
M5 = (1.4, 0.26, 4.4); FL = (0.15, 0.03, 0.50); V46 = (0.3, 0.05, 0.9)


def llamada(p, cache, entra, sale):
    """Dólares de una llamada: tokens en caché, de entrada sin caché y de salida, con el precio p por millón."""
    return (cache * p[1] + entra * p[0] + sale * p[2]) / 1e6


VIDEO, CF_VISTO, CF_GUARDA, BLOB = 0.2, 1 / 1000, 5 / 1000, 0.0184
F = [  # (rótulo, dólares por uso, usos por año medio, alto, ventana del cuadro 42, nota del uso)
    ('Denuncias y cartas documento: redactar, revisar y guardar la prueba sellada',
     2 * llamada(M5, 6000, 30000, 4000) + llamada(V46, 0, 20000, 1000) + 0.025 * 12 * BLOB * 2,
     20000, 50000, 'meses 6 a 9',
     'Por denuncia: dos llamadas a GLM-5.3 (redactar y revisar: 6.000 tokens en caché, 30.000 de entrada y 4.000 de salida), '
     'GLM-4.6V para mirar fotos y videos (20.000 y 1.000) y la prueba sellada guardada dos años (25 MB en promedio)'),
    ('Power users: calcular el pago de cada aviso o mejora',
     2 * llamada(M5, 6000, 60000, 8000), 10000, 40000, 'meses 7 a 12',
     'Por aviso: dos llamadas a GLM-5.3 (calcular y revisar: 6.000 en caché, 60.000 de entrada y 8.000 de salida). '
     'El pago a los power users sale de su propio fondo (4.11), no de aquí'),
    ('Historias cortas, también en video', None, None, None, 'meses 6 a 9',
     '300 historias por año de 30 segundos: seis tomas de CogVideoX-3 cada una, con tres intentos por toma; '
     'una historia vista por conversación (891.846 conversaciones por año en el escenario medio, 3.088.760 en el alto)'),
    ('Consulta de lugares con imágenes',
     llamada(V46, 0, 15000, 1000) + llamada(M5, 6000, 40000, 3000) + 2 * VIDEO, 20000, 60000, 'meses 18 a 24',
     'Por consulta: GLM-4.6V mira el video del vecino (15.000 y 1.000), GLM-5.3 calcula lo que permiten el Código de '
     'Ordenamiento Urbano y el catastro (6.000 en caché, 40.000 y 3.000) y CogVideoX-3 dibuja dos veces cómo quedaría'),
    ('Conversación de salud mental, a toda hora', None, 2500, 7500, 'meses 12 a 18',
     'Usuarios: 1% de los 241.666 vecinos de 16 años o más en el escenario medio y 3% en el alto. Cada uno conversa '
     'como en el ensayo de Therabot (seis horas en ocho semanas: 39 horas por año), 40 mensajes por hora, todos con '
     'GLM-5.3 (12.000 en caché, 1.000 de entrada y 400 de salida) y un filtro de emergencias con GLM-5.3-Flash'),
    ('Contratos de alquiler: redactar el contrato y revisar la declaración de ingresos',
     llamada(M5, 6000, 40000, 8000) + llamada(M5, 6000, 20000, 2000), 2000, 5000, 'meses 7 a 12',
     'Por contrato: GLM-5.3 lo redacta (6.000 en caché, 40.000 y 8.000) y revisa la declaración de ingresos (20.000 y 2.000). '
     'Unas 840 garantías por año (5.4), más las habitaciones y los demás contratos'),
]
TURNO = llamada(M5, 12000, 1000, 400) + llamada(FL, 0, 2000, 100)
SALUD_USUARIO = TURNO * 40 * 6 * 52 / 8
HIST_PROD = 300 * 6 * 3 * VIDEO
HIST = {'medio': HIST_PROD + 891846 * 0.5 * CF_VISTO + 12 * CF_GUARDA * 1000,
        'alto': HIST_PROD + 3088760 * 0.5 * CF_VISTO + 12 * CF_GUARDA * 1000}
CONT, USD = 0.15, 'Supuestos!$C$289'  # contingencia del cuadro 28 y dólar de diciembre de 2025

fila('AD · FUNCIONES NUEVAS DE LA INTELIGENCIA ARTIFICIAL DEL MUNICIPIO: LO QUE USAN DEL MODELO, LAS IMÁGENES Y EL VIDEO (4.11)', h=True)
fila('Cada función, en dólares por año en el escenario medio, con su fecha de inicio (cuadro 42)', None,
     'Mismo método que la infraestructura del cuadro 28: precio por uso, escenario medio, 15% de contingencia y el dólar de '
     'diciembre de 2025 (fila 289). Precios publicados por cada proveedor, consultados el 18/11/2026: Z.ai (GLM-5.3: 1,4, 0,26 '
     'en caché y 4,4 dólares por millón de tokens; GLM-5.3-Flash: 0,15, 0,03 y 0,50; GLM-4.6V: 0,3 y 0,9; CogVideoX-3: 0,2 '
     'por video), Cloudflare Stream (1 dólar por cada 1.000 minutos vistos y 5 por mes por cada 1.000 guardados) y Azure '
     '(0,0184 dólares por GB por mes). Los volúmenes son ESTIMACIÓN PROPIA, NO VERIFICADA. Cálculo propio')
filas_f = []
for rot, pu, med, alt, vent, nt in F:
    if rot.startswith('Historias'):
        usd_m, usd_a = HIST['medio'], HIST['alto']
        txt = f'{nt}. {es(usd_m)} dólares por año en el medio y {es(usd_a)} en el alto'
    elif rot.startswith('Conversación'):
        usd_m, usd_a = SALUD_USUARIO * med, SALUD_USUARIO * alt
        txt = (f'{nt}. {es(TURNO, 5)} dólares por mensaje; {es(SALUD_USUARIO, 2)} por usuario y por año. '
               f'{es(usd_m)} dólares por año en el medio y {es(usd_a)} en el alto')
    else:
        usd_m, usd_a = pu * med, pu * alt
        txt = (f'{nt}. {es(pu, 4)} dólares por uso; {es(med)} usos por año en el medio y {es(alt)} en el alto: '
               f'{es(usd_m)} y {es(usd_a)} dólares por año')
    txt += f'. Empieza en los {vent} (cuadro 42)'
    filas_f.append((fila(f'{rot}, dólares por año', round(usd_m, 2), txt), usd_a))
a, b = filas_f[0][0], filas_f[-1][0]
tot_usd = fila('Las seis funciones, dólares por año (escenario medio)', f'=SUM(C{a}:C{b})',
               f'Escenario alto: {es(sum(x[1] for x in filas_f))} dólares por año')
tot_ars = fila('Las seis funciones, en pesos por año, con 15% de contingencia', f'=ROUND(C{tot_usd}*(1+{CONT})*{USD},-5)',
               'Se suma a infraestructura y licencias del cuadro 28 y a la plataforma (fila 161), dentro de Ciencia y Técnica: '
               'no cambia el gasto total ni el resultado. En el escenario alto, unas tres veces más. La conversación de salud '
               'mental es más de la mitad. El primer año (2028) suma menos: cada función empieza en su fecha')
# la plataforma suma las funciones nuevas

# ---------------------------------------------------------------- 3. la certificación de cada escalón de la partida vecinal
r += 1
fila('AE · LA CERTIFICACIÓN DE CADA ESCALÓN DE LA PARTIDA VECINAL: OTRO CONTRATO, CON LO QUE SOBRA DEL 1,5% (6.2)', h=True)
pct = fila('Auditoría sobre el monto de las obras, en un programa de obra pública comparable', '=500/230600',
           'Programa de Saneamiento Ambiental de la Cuenca del Río Reconquista (Préstamo BID 3256/OC-AR), Reglamento Operativo '
           'del Ministerio de Infraestructura de la Provincia: «Auditoría, Monitoreo y Evaluación» 500 mil dólares, contra 230.600 '
           'mil de costos directos (obras). Esa línea paga «la contratación de una entidad auditora independiente que realice la '
           'auditoría del Programa» y además las evaluaciones intermedia y final: es un techo. Un programa de unos 38 millones de '
           'dólares de obra por año, del tamaño de la partida vecinal (de 7.227 a 28.908 M)', fmt='p')
S.cell(pct, 3).number_format = '0.000%'

sueldo = fila('Sueldo de ingreso municipal, categoría 6, 35 horas, por mes', 420507,
              'Ordenanza 9422 de presupuesto 2026: 432.624 pesos, a pesos de diciembre de 2025 (nota del capítulo 4)')
cuid = fila('Cuidado de los chicos en las asambleas, por año', 500000, 'Nota del capítulo 4: 24 asambleas, dos cuidadoras, cuatro horas cada una')
adm = fila('Administración de las obras que hacen las comisiones: 3% sobre la cuarta parte de la partida', 0.03 * 0.25,
           'Nota del capítulo 4. El año 1 las obras las hace el Ejecutivo, así que ese año sobra más de lo que muestra esta hoja', fmt='p')
S.cell(adm, 3).number_format = '0.00%'
for k, y in enumerate((2028, 2029, 2030, 2031), start=1):
    pc = f'$C${41 + k}'
    part = f'$C$21*(1+$C$36)^3*{pc}'
    c = fila(f'Año {k} ({y}) · certificación de su escalón', f'={part}*$C${pct}',
             'Partida del año por el porcentaje del programa comparable. Se paga cuando se certifica, hacia marzo del año siguiente')
    usado = f'$C${cuid}+{part}*$C${adm}'
    hon = f'*3*0.25*$C${sueldo}'
    s1 = fila(f'Año {k} ({y}) · lo que sobra del 1,5%, con obras de 100 M', f'={part}*$C$185-({usado}+{part}/100000000{hon})',
              'El 1,5% de la partida menos el cuidado de los chicos, el honorario de los tres vecinos que reciben cada obra '
              '(un cuarto del sueldo de ingreso cada uno) y la administración (nota del capítulo 4)')
    s2 = fila(f'Año {k} ({y}) · lo que sobra del 1,5%, con obras de 50 M (peor caso)', f'={part}*$C$185-({usado}+{part}/50000000{hon})',
              'Con obras más chicas hay el doble de recepciones')
    fila(f'Año {k} ({y}) · lo que falta y sale del gasto flexible, peor caso', f'=MAX(0,C{c}-C{s2})',
         f'Con obras de 100 M no falta nada (fila {s1})')
falta4 = r - 1
nota(S, 'E182', 'El 44,7%: el peor caso, con el ahorro de tomógrafos del peor caso (fila 298).',
     'El 44,7%: el peor caso, con el ahorro de tomógrafos del peor caso (fila 298) y lo que falta para la certificación '
     f'del escalón del año 4 (fila {falta4}).')
S['C182'] = f'=C181-(C174+C175+C296-C298+C{falta4})/C128'

# ---------------------------------------------------------------- 4. formar a los agentes de tránsito que pasan a la patrulla
r += 1
fila('AF · AGENTES DE TRÁNSITO QUE PASAN A LA PATRULLA: LA FORMACIÓN Y EL SUELDO (5.7)', h=True)
f6 = fila('Programa 47.01, Formación y capacitación de agentes de seguridad: los 5 docentes, por año', 28090599,
          'Ordenanza 9422 de presupuesto 2026, formulario F6 (hoja 160 del PDF, folio 1109): 4 de preceptoría (16.051.771) y un '
          'director institucional (12.039.828), sueldos básicos. En pesos del presupuesto 2026')
f7 = fila('Programa 47.01: compras y servicios, por año', 24118871,
          'Misma ordenanza, formulario F7 (folio 1221): «De capacitación» 13.126.254, mantenimiento 10.992.612 y gastos generales 5. '
          'En pesos del presupuesto 2026')
prog = fila('Programa 47.01 entero, un año, a pesos de diciembre de 2025', f'=(C{f6}+C{f7})*1.025*1.028',
            'Con el IPC de noviembre (2,5%) y diciembre (2,8%) de 2025, como la fila 304')
c2 = fila('Una cohorte de hasta 60 agentes, dos meses de curso, una vez', f'=C{prog}*2/12',
     'El curso de la patrulla dura dos meses, de lunes a viernes de 8 a 16 (Municipio, 3/3/2026, «Capacitan 60 nuevos '
     'agentes»), en el Centro de Formación Santa Rita. Dos meses del programa')
c12 = fila('Una cohorte de hasta 60 agentes, tope: un año entero del programa, una vez', f'=C{prog}',
     'Cuántos pasan no está decidido (lo fija un relevamiento): de 40 a 60, una cohorte; de 61 a 100, dos. Lo paga el '
     'presupuesto de Seguridad y no entra en el resultado hasta que se decida')
fila('Por agente, una vez: dos meses del programa', f'=C{c2}/60', 'Cohortes de 60, como la de marzo de 2026')
fila('Por agente, una vez: tope', f'=C{c12}/60', 'Cohortes de 60')
for n in (40, 60, 80, 100):
    k = 1 if n <= 60 else 2
    fila(f'Si pasan {n} agentes: formación, de', f'=C{c2}*{k}', f'Hasta: {k} cohorte{"s" if k > 1 else ""} al tope (fila {c12})')
fila('Si pasan 40 a 100 agentes: formación, tope máximo', f'=C{c12}*2', 'Dos cohortes al tope')
tr = fila('Compensación del inspector de tránsito, por mes', 31694,
          'Ordenanza 9422, artículo 17: «compensación especial de 31.694 módulos para el personal que cumpla funciones de '
          'inspector/a de Tránsito». El módulo vale un peso: la categoría 6 de 35 horas son 432.624 módulos (artículo 68), '
          'los mismos 432.624 pesos de la nota del capítulo 4. En pesos del presupuesto 2026')
pm = fila('Bonificación de la Patrulla Municipal, por mes', 126416,
          'Misma ordenanza, artículo 17: «bonificación de 126.416 módulos al personal que cumpla funciones en la Patrulla Municipal»')
pp = fila('Bonificación del Cuerpo de Patrulla a pie, por mes', 212153,
          'Misma ordenanza, artículo 17: «bonificación mensual de 212.153 módulos para el personal de la Secretaría de Seguridad '
          'que cumple funciones en el "Cuerpo de Patrulla a pie"». La ordenanza no dice si se suma a la anterior')
fila('Si conserva su compensación de tránsito: diferencia por agente y por año', 0,
     'Es lo decidido (sueldos iguales): la Ley 14.656, artículo 8, no permite que el pase lo afecte materialmente, y no lo afecta')
fila('Si cobra la bonificación de la Patrulla Municipal en lugar de la de tránsito: diferencia por agente y por año',
     f'=(C{pm}-C{tr})*13*(1+$C$227)*1.025*1.028',
     'Trece meses, con las cargas del empleador de la fila 227, a pesos de diciembre de 2025. Opción, no decidida')
fila('Si además cobra la del Cuerpo de Patrulla a pie: diferencia por agente y por año',
     f'=(C{pm}+C{pp}-C{tr})*13*(1+$C$227)*1.025*1.028', 'Opción, no decidida. Con 40 agentes, por 40; con 100, por 100')

# ---------------------------------------------------------------- 5. votar: el RENAPER y las tablets (4.6)
r += 1
fila('AG · VOTAR CON LA INTELIGENCIA ARTIFICIAL DEL MUNICIPIO: EL RENAPER Y LAS TABLETS (4.6)', h=True)
rdni = fila('RENAPER · validación de los datos del DNI, por persona', 60,
            'Cuadro tarifario del RENAPER (IF-2026-20279196-APN-RENAPER#MI, 26/2/2026), ítem 13, servicios por API con convenio: '
            '60 pesos por transacción hasta 40.000 por mes (35 hasta 2.000.000; 20 desde ahí). En pesos de febrero de 2026')
rvid = fila('RENAPER · prueba de vida pasiva (la foto), por persona', 70, 'Mismo cuadro tarifario, ítem 14: 70 pesos')
rcoef = fila('De pesos de febrero de 2026 a pesos de diciembre de 2025', 10121.3715 / 10714.6255,
             'IPC del INDEC: diciembre de 2025, 10.121,37; febrero de 2026, 10.714,63', fmt='p')
S.cell(rcoef, 3).number_format = '0.0000'
rn = fila('Personas que validan su identidad por año (escenario medio)', 25000,
          'ESTIMACIÓN PROPIA, NO VERIFICADA: uno de cada diez vecinos de 16 años o más (241.666). Si validaran todos, 241.666')
rtot = fila('RENAPER, por año', f'=(C{rdni}+C{rvid})*C{rcoef}*C{rn}',
            'Con todos los vecinos de 16 años o más, unos 29,7 M una vez. El RENAPER exime a los organismos públicos de otros '
            'trámites, no de éste: se toma la tarifa entera')
tprec = fila('Tablet con cámara, precio público', 429999,
             'Samsung Argentina, tienda oficial (samsung.com/ar/tablets/galaxy-tab-a), Galaxy Tab A11 de 64 GB, consultado el '
             '18/11/2026. En pesos de noviembre de 2026')
tcoef = fila('De pesos de noviembre de 2026 a pesos de diciembre de 2025', 10121.3715 / 12076.3937,
             'IPC del INDEC: diciembre de 2025 sobre julio de 2026, el último publicado en la serie de este libro (deja el precio '
             'un poco alto)', fmt='p')
S.cell(tcoef, 3).number_format = '0.0000'
tn = fila('Tablets: una por asamblea y una por delegación', 12,
          'Supuesto: seis asambleas a la vez, una por zona, y seis delegaciones. Es un parámetro: con dos por lugar, 24')
tvida = fila('Años de uso de cada tablet', 3, 'Supuesto')
tcompra = fila('Tablets, compra, una vez', f'=C{tprec}*C{tcoef}*C{tn}', 'Compra chica, sin licitación (Ley Orgánica, artículo 151)')
ttot = fila('Tablets, por año, con su reposición', f'=C{tcompra}/C{tvida}', '')
vot = fila('Votar: RENAPER y tablets, por año', f'=ROUND(C{rtot}+C{ttot},-5)',
           'Se suma a infraestructura y licencias del cuadro 28 y a la plataforma (fila 161). El personal que acompaña la '
           'votación es del Municipio y ya cobra su sueldo')

# ---------------------------------------------------------------- la plataforma suma las funciones nuevas y la votación
S['C161'] = f'=2000700000+C{tot_ars}+C{vot}'
nota(S, 'E161', 'auditoría externa 135,4 M, el 10% del sueldo del equipo de 59 personas.',
     'auditoría externa de la plataforma 135,4 M, el 10% del sueldo del equipo de 59 personas. Desde el 18/11/2026 suma '
     f'el uso de las seis funciones nuevas de la inteligencia artificial del Municipio (fila {tot_ars}) y la votación con el '
     f'RENAPER y las tablets (fila {vot}).')
VOTO = round(((60 + 70) * 10121.3715 / 10714.6255 * 25000) + 429999 * 10121.3715 / 12076.3937 * 12 / 3, -5)
NUEVAS = round(sum(S.cell(x, 3).value for x, _ in filas_f) * (1 + CONT) * S['C289'].value, -5)
PLAT = 2000700000 + NUEVAS + VOTO
PCT = (PLAT + S['C162'].value + S['C163'].value) / S['C199'].value
PCT_SIN = (PLAT + S['C162'].value) / S['C199'].value
nota(S, 'E161', 'Con los dispositivos, 2.091,7 M. ESTIMACIÓN PROPIA',
     f'Con los dispositivos, {es((PLAT + S["C162"].value) / 1e6, 1)} M. ESTIMACIÓN PROPIA')
nota(S, 'E164', 'El 27,1% del documento. Sin el semillero, 25,6%',
     f'El {es(PCT * 100, 1)}% del documento. Sin el semillero, {es(PCT_SIN * 100, 1)}%')
nota(G, 'C12', 'la plataforma y el semillero —dentro de Ciencia y Técnica, 27,1%—',
     f'la plataforma y el semillero —dentro de Ciencia y Técnica, {es(PCT * 100, 1)}%—')


# ---------------------------------------------------------------- Metas: la meta 20, como el cuadro 41 (decisiones 7 y 8)
M = wb['Metas']
assert M['B25'].value.startswith('Nadie va a ganar dinero por cada multa'), M['B25'].value
M['B25'] = ('Ningún proveedor ni empleado va a ganar dinero por cada multa que se pone. El dinero de las multas va a ir a '
            'un fondo de seguridad vial, que no se puede usar para otra cosa, salvo la parte del vecino que avisó la falta (4.11)')

wb.save(X)
print('ok · funciones nuevas: fila', tot_ars, '· certificación hasta la fila', falta4, '· formación hasta la fila', r - 1)
