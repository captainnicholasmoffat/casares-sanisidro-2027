"""Plan de despliegue, 18/11/2026: lo que decidió Nick en la revisión completa (DECISIONES_NOVIEMBRE, 18/11).
- Decisión 1: la primera ronda (mes 3) se vota con la cuarta parte de la inteligencia artificial del Municipio: por
  celular, con el DNI y la foto verificados contra el RENAPER (convenio por TAD), y en tablets con personal del Municipio
  en cada asamblea y en la delegación. Si se atrasa, esa ronda se vota sólo en las tablets. El primer año convoca el
  Municipio; desde el año 2, la comisión de cada zona (I02, I04, I09, I10, M03, M08; nuevas I20 e I21).
- Decisión 2: cada función nueva de la inteligencia artificial del Municipio con su fecha y su costo (I22 a I28). La
  arquitectura y el esqueleto se preparan antes de asumir: baja el riesgo de las fechas (nota de I02).
- Decisión 3: dos contratos de auditoría externa (I17, la de la plataforma; M29, la que certifica cada escalón).
- Decisiones 5 y 5b: terrenos sin uso con las cuatro trabas (V09, ciclo 2029 y V10).
- Decisiones 6 y 6b: acompañantes desde el mes 27, una opción entre varias (S14).
- Decisión 7: estudiar las reglas de detalle de la tercera fórmula de los power users (I24).
- Seguridad: la patrulla sólo previene y busca el delito; los agentes de tránsito que pasan a la patrulla se forman
  (G07; nuevas G28 a G30).
Edita acciones_def.py y pasos_extra.py. Cada reemplazo comprueba que el texto viejo existe: si ya se aplicó, se detiene.
Después: cd trabajo/despl && python3 build.py ../../proyecto/despliegue/acciones.json && python3 gen_revision.py ..."""
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()
if 'act("I20"' in s:
    print('ya aplicado'); raise SystemExit


def rep(old, new, cuantas=1):
    global s
    assert s.count(old) == cuantas, (old[:70], s.count(old)); s = s.replace(old, new)


rep('# Cada acción sale del texto final del programa (commit c462fcf).',
    '# Cada acción sale del texto final del programa (versión del 18 de noviembre de 2026).')

# ---------------------------------------------------------------- decisión 1: la votación desde el mes 3
rep('act("I02", "Construir las tres primeras partes: la que responde consultas, la que saca el turno médico conversando y la que escucha a los vecinos",',
    'act("I02", "Construir las cuatro primeras partes: la que responde consultas, la que saca el turno médico conversando, la que escucha a los vecinos y la votación",')
rep('           "de violencia, con un modo discreto. Cada tema tiene un plazo; si el responsable no contesta, pasa a su jefe. Una cuenta por persona, con identidad verificada."),\n'
    '    note="Riesgo crítico del 6.6: la inteligencia artificial del Municipio no se construye o llega tarde. Por eso se entrega por partes.")',
    '           "de violencia, con un modo discreto. Cada tema tiene un plazo; si el responsable no contesta, pasa a su jefe. Una cuenta por persona, con identidad verificada. "\n'
    '           "La votación de la primera ronda funciona por celular, con el DNI y la foto verificados contra el RENAPER, y en tablets que lleva el personal del Municipio."),\n'
    '    note=("Riesgo crítico del 6.6: la inteligencia artificial del Municipio no se construye o llega tarde. Por eso se entrega por partes, "\n'
    '          "y su arquitectura y su esqueleto se preparan antes de asumir: eso baja el riesgo de las fechas, sin cambiar quién la construye "\n'
    '          "ni cómo la recibe el Municipio. Decisión del 18/11/2026."))')
rep('act("I04", "Empiezan a funcionar las tres primeras partes de la inteligencia artificial del Municipio (compromiso 14)",\n'
    '    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I03", "S01"], win=W(3), fuente="6.4")',
    'act("I04", "Empiezan a funcionar las cuatro primeras partes de la inteligencia artificial del Municipio, con la votación (compromiso 14)",\n'
    '    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I03", "S01", "I20", "I21"], win=W(3), fuente="6.4",\n'
    '    note="Si la votación por celular se atrasa, la primera ronda se vota sólo en las tablets de la asamblea (decisión del 18/11/2026).")\n'
    'act("I20", "Firmar con el RENAPER el Convenio Único de Confronte de Datos, por TAD, para verificar el DNI y la foto de quien vota",\n'
    '    "Gobierno y Legal y Técnica", dur=20, est=True, needs=["T07"], win=W(1, 3), fuente="4.6",\n'
    '    steps=("Es el trámite que pide el RENAPER a quien quiere usar sus servicios de validación de identidad: datos del DNI y foto. "\n'
    '           "Cada validación cuesta 60 pesos por los datos del DNI y 70 por la prueba de vida (cuadro tarifario del RENAPER, 26/2/2026): "\n'
    '           "unos 3,1 millones por año si validan 25.000 personas."),\n'
    '    note="Duración estimada: el programa no la da. Si el convenio se atrasa, esa ronda se vota sólo en las tablets (I04).")\n'
    'act("I21", "Comprar las tablets y preparar al personal del Municipio que acompaña la votación en cada asamblea y en la delegación de cada zona",\n'
    '    "Ciencia y Técnica", dur=20, est=True, needs=["T07"], win=W(1, 3), fuente="4.6",\n'
    '    steps="Compra chica, sin licitación pública (Ley Orgánica de las Municipalidades, artículo 151). Quien no tiene celular vota en la tablet, con ayuda.",\n'
    '    note=("Duración estimada. El programa no dice cuántas tablets: con una por asamblea y una por delegación, 12, cuestan unos "\n'
    '          "4,3 millones una vez, con el precio de la tienda oficial de Samsung del 18/11/2026."))')
rep('    steps=("Se informa a los vecinos y se eligen las obras del año: un voto por persona desde los 16 años, en la asamblea o por internet. "\n'
    '           "El primer año las hace el Ejecutivo, porque las comisiones todavía se están formando. También se cuentan los baldíos, las ruinas y las obras paradas (5.4)."),',
    '    steps=("Se informa a los vecinos y se eligen las obras del año: un voto por persona desde los 16 años, por celular con el DNI y la foto "\n'
    '           "verificados contra el RENAPER, o en las tablets que lleva el personal del Municipio a cada asamblea y a la delegación de la zona. "\n'
    '           "Si la votación por celular se atrasa, esa ronda se vota sólo en las tablets de la asamblea. "\n'
    '           "El primer año la convoca el Municipio y las obras las hace el Ejecutivo, porque las comisiones todavía se están formando; "\n'
    '           "desde el año 2 convoca la comisión de cada zona. También se cuentan los baldíos, las ruinas y las obras paradas (5.4)."),')
rep('    "Intendente", dur=15, est=True, needs=["M02"], win=W(3), fuente="6.4",',
    '    "Intendente", dur=15, est=True, needs=["M02", ("I04", "SS", 0)], win=W(3), fuente="6.4",')
rep('    steps=("Un voto por persona desde los 16 años, en la asamblea o por internet con identidad verificada. "',
    '    steps=("Un voto por persona desde los 16 años, en la asamblea, en las tablets o por celular con el DNI y la foto verificados contra el RENAPER. "')
rep('act("I09", "Construir las tres partes siguientes: la partida vecinal, el seguimiento de cada obra y el espacio de cada asociación",',
    'act("I09", "Construir las tres partes siguientes: el resto de la partida vecinal, el seguimiento de cada obra y el espacio de cada asociación",')
rep('    steps=("Votación con el padrón de la zona y acta el mismo día. Aviso cuando una obra se atrasa. "',
    '    steps=("Padrón de cada zona y acta de cada votación el mismo día. Aviso cuando una obra se atrasa. "')
rep('act("I10", "Suman tres partes: la partida vecinal, el seguimiento de cada obra y el espacio propio de cada asociación inscripta (meta 19)",',
    'act("I10", "Suman tres partes: el resto de la partida vecinal, el seguimiento de cada obra y el espacio propio de cada asociación inscripta (meta 19)",')

# la Ordenanza 1 (y la derogación) en la sesión extraordinaria, para que la primera ronda elija con la partida creada
rep('    sne=D(2028, 3, 1), needs=["C01"], fuente="4.10", note=TRAT + " " + RECESO)',
    '    needs=["C01"], fuente="4.10",\n'
    '    note=TRAT + " El intendente pide tratarla en la sesión extraordinaria, junto con la Ordenanza 1 (Ley Orgánica, artículo 68, inciso 5).")')
rep('    sne=D(2028, 3, 1), needs=["C04"], fuente="anexo.1", note=TRAT + " " + RECESO)',
    '    needs=["C04"], fuente="anexo.1",\n'
    '    note=TRAT + " Para que la primera ronda elija las obras con la partida ya creada, el intendente pide tratarla en la sesión "\n'
    '                "extraordinaria (Ley Orgánica, artículo 68, inciso 5).")')
rep('    "Intendente", dur=15, est=True, needs=["M02", ("I04", "SS", 0)], win=W(3), fuente="6.4",',
    '    "Intendente", dur=15, est=True, needs=["M02", "C06", ("I04", "SS", -11)], win=W(3), fuente="6.4",')
rep('    note="Cambio del 16/11/2026: las obras de cada año se eligen en la primera ronda, para que tengan tiempo de licitarse y terminarse en el mismo año (6.1).")',
    '    note=("Cambio del 16/11/2026: las obras de cada año se eligen en la primera ronda, para que tengan tiempo de licitarse y terminarse en el mismo año (6.1). "\n'
    '          "Supuesto: las asambleas empiezan hasta 11 días hábiles antes de que funcione la votación (I04); las primeras informan, y "\n'
    '          "la votación de cada zona se hace desde que funciona, dentro del mes 3."))')

# ---------------------------------------------------------------- decisión 3: dos contratos de auditoría externa
rep('act("I17", "Licitar y contratar la auditoría externa de la inteligencia artificial del Municipio", "Ciencia y Técnica",',
    'act("I17", "Licitar y contratar la auditoría externa de la plataforma de la inteligencia artificial del Municipio", "Ciencia y Técnica",')
rep('    note="Riesgo del 6.6: la inteligencia artificial del Municipio contesta mal. La auditoría externa está en el cuadro 28.")',
    '    note=("Riesgo del 6.6: la inteligencia artificial del Municipio contesta mal. La auditoría externa de la plataforma está en el cuadro 28. "\n'
    '          "Certificar cada escalón de la partida vecinal es otro contrato (M29)."))')
for n, m in ((1, 'M26'), (2, 'M27'), (3, 'M28')):
    rep(f'act("{m}", "La auditoría externa certifica que se cumplió el año {n}',
        f'act("{m}", "La auditoría externa de la obra certifica que se cumplió el año {n}')
rep('        decision=(f"Incluir la partida de obra vecinal al {pct}. Ese dinero se libera cuando la auditoría externa certifica que se cumplió "',
    '        decision=(f"Incluir la partida de obra vecinal al {pct}. Ese dinero se libera cuando la auditoría externa de la obra certifica que se cumplió "')
for m in ('M26', 'M27', 'M28'):
    k = s.index(f'act("{m}"'); j = s.index('"I17"]', k)
    assert j - k < 300, m
    s = s[:j] + '"M29"]' + s[j + len('"I17"]'):]

# ---------------------------------------------------------------- decisiones 6 y 6b: acompañantes desde el mes 27
rep('act("S14", "Empieza la formación de los primeros acompañantes terapéuticos, entre empleados cuyo trabajo ya hace la inteligencia artificial del Municipio",\n'
    '    "Secretaría de Salud", ms=True, needs=["I04"], win=W(7, 12), fuente="6.4",\n'
    '    note="Con la formación que fija la Provincia (Resolución 592/2022). No suma sueldos.")',
    'act("S14", "Empieza la formación de los primeros acompañantes terapéuticos, entre los empleados cuyas tareas empieza a liberar la automatización",\n'
    '    "Secretaría de Salud", ms=True, needs=["E18"], win=W(27), fuente="5.6",\n'
    '    steps=("Es una opción entre varias para quien queda liberado: también el programa de empleo tecnológico, los equipos de las plazas, "\n'
    '           "deportes, arte y las demás áreas del programa. Se forman con lo que fija la Provincia (Resolución 592/2022)."),\n'
    '    note=("Decisión del 18/11/2026: el primer año es de absorción y nadie queda liberado. La automatización empieza a liberar "\n'
    '          "tareas en el mes 27 (5.3). No suma sueldos."))')

# ---------------------------------------------------------------- decisiones 5 y 5b: terrenos sin uso, las cuatro trabas
rep('     "Partida de obra vecinal al 25%. Fondo de seguridad vial con renglón propio. Ambiente, empleo y vivienda, y centros de apoyo escolar."),',
    '     "Partida de obra vecinal al 25%. Fondo de seguridad vial con renglón propio. Ambiente, empleo y vivienda, y centros de apoyo escolar. "\n'
    '     "Tasa más alta para los baldíos y las obras paradas, como en Bahía Blanca: es la base del recargo a los terrenos sin uso (5.4)."),')
rep('    note="Ley 14.449: los plazos no cambian aunque el terreno se venda, y la obligación se anota en la escritura.")',
    '    steps=("Quien no construye en tres años paga el recargo de la Ley 14.449 sobre la tasa más alta para baldíos y obras paradas, "\n'
    '           "sin planes ni perdones (Decreto-Ley 8912, artículo 86). Si no paga, cobro judicial con embargo y remate del terreno (Ley 13.406). "\n'
    '           "Vender no lo salva: la obligación queda anotada en el Registro, con los mismos plazos (artículo 85). Comprarse el propio remate "\n'
    '           "tampoco: lo que paga cancela la deuda, la obligación de construir sigue, y el remate tiene base del 80% y del 60% (Ley 13.406, artículo 16)."),\n'
    '    note="Ley 14.449: los plazos no cambian aunque el terreno se venda, y la obligación se anota en la escritura.")\n'
    'act("V10", "Empieza el recargo a los terrenos notificados que siguen sin construir", "Secretaría de Hacienda",\n'
    '    ms=True, needs=[("V09", "FS", 750)], win=W(43, 48), fuente="5.4",\n'
    '    steps="Sobre la tasa más alta para baldíos y obras paradas, sin planes ni perdones. Si no paga, cobro judicial con embargo y remate (Ley 13.406).",\n'
    '    note="Supuesto: tres años desde la notificación (Ley 14.449) son unos 750 días hábiles.")')

# ---------------------------------------------------------------- seguridad: la patrulla previene; tránsito ordena
rep('    steps="Es la misma patrulla, en otro lugar y a otra hora (5.7).")',
    '    steps="Es la misma patrulla, en otro lugar y a otra hora (5.7). Sólo previene y busca el delito: no hace controles de tránsito ni para a nadie por papeles.")')
rep('# ---------------------------------------------------------------- 9 Costa y espacio público',
    'act("G28", "Decreto de funciones: la patrulla municipal sólo previene y busca el delito, y los agentes de tránsito sólo ordenan el tránsito",\n'
    '    "Intendente", dur=10, est=True, needs=["T07", "T05"], fuente="5.7",\n'
    '    steps=("La patrulla no hace controles de tránsito ni para a nadie por papeles. Los agentes de tránsito que quedan ordenan la salida "\n'
    '           "de las escuelas, los accidentes y los cortes, sin parar a nadie para multar. Ningún vehículo se retiene por una falta menor: "\n'
    '           "la patente floja se ajusta en el lugar y el auto sigue. Las cámaras quedan todas, con tolerancia y aviso previo, y se suman donde haga falta."),\n'
    '    note=("Se redefinen funciones, no se perdona la ley: el Municipio no puede crear un régimen más benigno (Ley 24.449, artículo 2). "\n'
    '          "Cuántos de los 120 agentes de tránsito pasan a la patrulla lo fija el relevamiento (G31)."))\n'
    'act("G31", "Relevar cuántos agentes de tránsito hacen falta para ordenar el tránsito: salidas de las escuelas, accidentes y cortes",\n'
    '    "Tránsito y Juzgado de Faltas", dur=20, est=True, needs=["T07"], fuente="5.7",\n'
    '    steps="De los 120 agentes de tránsito de hoy, el resto pasa a la patrulla.",\n'
    '    note="Duración estimada. El programa no le pone fecha.")\n'
    'act("G29", "Formar en el Centro de Formación Santa Rita a los agentes de tránsito que pasan a la patrulla", "Seguridad (Centro de Operaciones Municipal)",\n'
    '    dur=40, est=True, needs=["G28", "G31"], fuente="5.7",\n'
    '    steps=("Pasan con el mismo sueldo y conservan su compensación de inspector de tránsito (Ley 14.656, artículo 8). "\n'
    '           "Formarlos cuesta de 0,15 a 0,92 millones por agente, una vez: de 9,2 a 55,0 millones por cada grupo de hasta 60, "\n'
    '           "con el presupuesto de Seguridad (programa 47.01)."),\n'
    '    note="Duración estimada: dos meses, como el curso de la patrulla de marzo de 2026.")\n'
    'act("G30", "Los agentes formados pasan a la patrulla, que sólo previene y busca el delito", "Seguridad (Centro de Operaciones Municipal)",\n'
    '    ms=True, needs=["G29"], fuente="5.7")\n'
    '\n'
    '# ---------------------------------------------------------------- 9 Costa y espacio público')

rep('desde que la auditoría externa libera el escalón (6.2)', 'desde que la auditoría externa de la obra libera el escalón (6.2)', 3)

# ---------------------------------------------------------------- decisiones 8 y 11: multas, power users y reductor
rep('    steps="Renglón propio en el presupuesto. No se puede usar para otra cosa (Ley 24.449, artículo 85).",',
    '    steps=("Renglón propio en el presupuesto. No se puede usar para otra cosa, salvo la parte del vecino que avisó la falta, "\n'
    '           "sólo sobre lo que efectivamente se cobra (4.11; Ley 24.449, artículo 85)."),')
rep('act("G23", "Nadie gana dinero por cada multa: los proveedores cobran sólo los equipos y su mantenimiento, a precio fijo (meta 20)",',
    'act("G23", "Ningún proveedor ni empleado gana dinero por cada multa: los proveedores cobran sólo los equipos y su mantenimiento, a precio fijo (meta 20)",')
rep('    steps="No puede elegir no hacer nada. El reductor se paga con el dinero de obra de la zona. En las avenidas que cruzan varias zonas opina el panel (5.11).")',
    '    steps=("No puede elegir no hacer nada. El reductor es obra y se paga con el dinero de obra de la zona; la cámara, con el fondo de "\n'
    '           "seguridad vial. En las avenidas que cruzan varias zonas opina el panel (5.11)."))')

# ---------------------------------------------------------------- decisiones 2, 3 y 7: funciones nuevas, su fecha y su costo
s = s.rstrip('\n') + '\n' + '''
# ---------------------------------------------------------------- Decisiones del 18/11/2026
CUADRO28 = "Lo que usa del modelo, las imágenes y el video entra en infraestructura y licencias (cuadro 28)."
act("I22", "Suman las denuncias y las cartas documento: la inteligencia artificial del Municipio explica la ley, junta la prueba sellada y las redacta",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "T05"], win=W(6, 9), fuente="4.11",
    steps=("El vecino manda la carta documento él mismo, por el servicio electrónico del Correo Argentino. Cuesta unos 4,7 millones por año. " + CUADRO28),
    note="Fecha decidida el 18/11/2026: después de la parte que recibe reclamos y del dictamen del abogado.")
act("I23", "Suman las historias cortas, también en video, para aprender a usar la inteligencia artificial del Municipio",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "T05"], win=W(6, 9), fuente="4.11",
    steps=("Cada vecino ve primero las que le sirven, con su permiso dado aparte. Cuestan unos 2,6 millones por año. " + CUADRO28),
    note="Fecha decidida el 18/11/2026.")
act("I24", "Estudiar las reglas de detalle de la tercera fórmula de los power users", "Equipo de la inteligencia artificial del Municipio",
    dur=20, est=True, needs=["T05", "T07"], fuente="4.11",
    steps=("Si una mejora no trae cobro ni ahorro directo, la inteligencia artificial del Municipio calcula la productividad que suma "
           "(horas que ahorra, vecinos que la usan) y una persona lo confirma. Cuenta sólo una propuesta bien armada, presentada y argumentada. "
           "Todo sale de un mismo fondo, que se llena con lo que las mejoras hacen ganar o ahorrar."),
    note="Decisión del 18/11/2026: las reglas de detalle se siguen estudiando.")
act("I25", "Suman los power users: vecinos y empleados cobran una parte de lo que su aviso le hace cobrar o ahorrar al Municipio",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "T05", "I24"], win=W(7, 12), fuente="4.11",
    steps=("Una multa cuenta sólo por lo que efectivamente se cobra de ella, y ningún proveedor ni empleado cobra por multa (5.11). "
           "Calcular cada pago cuesta unos 4,0 millones por año. " + CUADRO28),
    note="Fecha decidida el 18/11/2026: después del dictamen del abogado.")
act("I26", "Suman los contratos de alquiler: la inteligencia artificial del Municipio los redacta, con la garantía del Municipio",
    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "V08"], win=W(7, 12), fuente="5.4",
    steps=("También revisa la declaración de ingresos de quien no tiene recibo, que después aprueba una persona del Municipio. "
           "Cuesta unos 0,4 millones por año. " + CUADRO28),
    note="Fecha decidida el 18/11/2026: con la garantía de alquiler (V08).")
act("I27", "Suma la conversación de salud mental, a cualquier hora", "Secretaría de Salud con el equipo de la inteligencia artificial",
    ms=True, needs=["I04", "T05", ("S11", "SS", 0)], win=W(12, 18), fuente="5.6",
    steps=("No hace terapia ni diagnostica: acompaña y avisa, bajo un profesional responsable. Con permiso del vecino, le pasa un resumen "
           "a su acompañante y al profesional. Cuesta unos 43,1 millones por año, la más cara de las funciones nuevas. " + CUADRO28),
    note="Fecha decidida el 18/11/2026: con la parte de salud (S11).")
act("I28", "Suma la consulta de lugares: mostrarle un lugar con la cámara del teléfono y saber qué se puede hacer ahí",
    "Habilitaciones con el equipo de la inteligencia artificial", ms=True, needs=["I04", "T05", ("H12", "SS", 0)], win=W(18, 24),
    fuente="5.9",
    steps=("Lee el Código de Ordenamiento Urbano y el catastro, y dibuja sobre el video del vecino cómo quedaría, marcado como ilustración. "
           "Cuesta unos 15,9 millones por año. " + CUADRO28),
    note="Fecha decidida el 18/11/2026: con las habilitaciones (H12).")
act("M29", "Licitar y contratar la auditoría externa que certifica cada escalón de la partida vecinal y recibe sus denuncias",
    "Secretaría de Hacienda", dur=66, needs=["C06"], win=W(7, 12), fuente="6.2", durnote=LIC,
    steps=("Es otro contrato, aparte del de la plataforma (I17). Cuesta de 15,7 millones el año 1 a 62,7 millones el año 4, con la "
           "auditoría de un programa de obra pública comparable. Se paga con lo que sobra del 1,5% de funcionamiento de la partida. "
           "Con obras promedio de 50 millones no alcanza, y lo que falta, de 7,6 a 28,7 millones por año, sale del gasto flexible."),
    note="Decisión del 18/11/2026, «por ahora».")
'''
P.write_text(s)

E = H / 'pasos_extra.py'; e = E.read_text()
old = '"I17": "La auditoría externa cuesta 135,4 millones por año (cuadro 28).",'
assert e.count(old) == 1
E.write_text(e.replace(old, '"I17": "La auditoría externa de la plataforma cuesta 135,4 millones por año (cuadro 28).",'))
R = H / 'gen_revision.py'; g = R.read_text()


def repg(old, new):
    global g
    assert g.count(old) == 1, old[:70]; g = g.replace(old, new)


repg('w("Datos del plan de despliegue del programa de gobierno, sacados del texto final (commit c462fcf). "',
     'w("Datos del plan de despliegue del programa de gobierno, sacados del texto final (versión del 18 de noviembre de 2026). "')
repg('''w("- La columna vertebral es la rampa de la obra vecinal desde el año 2: M15, M17, M18, M19, M20 y M21, hasta el fin del mandato (M23). "
  "Cada año de la rampa dura lo que dice el programa, un año, y el siguiente empieza el día después. "
  "Si un año se atrasa, el 50% no llega al mes 48. Con la rampa también queda crítica la meta de las cloacas en Boulogne y Béccar (V03).")
w("- Antes del año 2 no hay acciones críticas en la rampa. El año 1 (M11) tiene unos 20 días hábiles de margen antes del mes 13.")''',
     '''w("- La columna vertebral es la rampa: cada año va desde que la auditoría externa de la obra libera su escalón (M26, M27 y M28, hacia marzo) "
  "hasta el cierre del ejercicio (M11, M17 y M19, el 31 de diciembre), y el año 4 hasta el fin del mandato (M23). "
  "Si un año se atrasa, el 50% no llega al mes 48." + (" Con la rampa también queda crítica la meta de las cloacas en Boulogne y Béccar (V03)." if O["V03"]["critical"] else ""))
if O["M03"]["critical"]:
    w("- La primera ronda de asambleas (M03) es crítica: se vota con la cuarta parte de la inteligencia artificial del Municipio, que llega con "
      f"las otras tres el {f(O['I04']['start'])} (I01 a I04). Por eso las asambleas empiezan antes, informando, y la votación de cada zona "
      "entra en los últimos días del mes 3 (supuesto de M03). De la primera ronda dependen la respuesta del Ejecutivo (M24) y los cien días (M22).")''')
repg('''w("- La inteligencia artificial del Municipio tiene cuatro días de margen para estar en el mes 3. "
  "De ella dependen, además del compromiso 14, otros cuatro compromisos de los cien días: G02, U02, H07 y X02.")''',
     '''w(("- La inteligencia artificial del Municipio no tiene margen para estar en el mes 3: es crítica (I04). " if O["I04"]["float"] == 0 else
   f"- La inteligencia artificial del Municipio tiene {O['I04']['float']} días de margen para estar en el mes 3. ") +
  "De ella dependen, además del compromiso 14 y la votación de la primera ronda, otros cuatro compromisos de los cien días: "
  f"G02, U02, H07 y X02, con {min(O[c]['float'] for c in ('G02', 'U02', 'H07', 'X02'))} días de margen.")''')
repg('''w("- Los presupuestos 2030 y 2031 tienen un día de margen, porque se votan entre el cierre de un año de la rampa y el inicio del siguiente.")''',
     '''_pf = [O[c]["float"] for c in ("P15", "P19", "P23")]
w("- Los presupuestos se votan a mediados de noviembre, con el escalón siguiente incluido: ya no esperan que se cumpla el anterior, "
  f"y tienen de {min(_pf)} a {max(_pf)} días hábiles de margen.")''')
R.write_text(g)
print('ok')
