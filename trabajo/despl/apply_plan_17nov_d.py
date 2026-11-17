"""Plan de despliegue, 17/11/2026, parte D: los arreglos obvios de la revisión completa del 17/11.
- Presupuesto (decisión 2+3 del 16/11): el Concejo vota cada presupuesto con el escalón siguiente incluido, sin esperar
  el anterior; el dinero se libera cuando la auditoría externa certifica el escalón anterior, hacia marzo (M26, y ahora
  también M27 y M28). Cada año de la rampa va por ejercicio (cierra el 31 de diciembre, hueco 1) y empieza cuando se libera.
- Las asambleas de los años 2 a 4 en los pasos de cada año (hueco 29); las Ordenanzas 5 y 7 en la sesión extraordinaria
  para cumplir los compromisos 4 y 5 (hueco 6); la grabación sin esperar el certificado (hueco 15); la pasantía sin esperar
  el título (hueco 12); «una vez aprobada» la Ordenanza 12 (hueco 9).
- La Ordenanza 19 es una sola (foodtrucks y artículo 9 de la 5824): sale el trámite aparte de la 5824 (C56 a C58).
- La audiencia pública de la Ordenanza 21; el dictamen del abogado antes de la garantía; la meta de los espectáculos.
- Reglas de escritura: «la inteligencia artificial del Municipio» y oraciones que empiezan igual.
Edita acciones_def.py, y en pasos_extra.py y pruebas.py sólo saca los códigos C56 a C58, dos textos y un error de tipeo
(«La propia la inteligencia artificial»). Después se corre build.py y gen_revision.py."""
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()


def rep(old, new, cuantas=1):
    global s
    assert s.count(old) == cuantas, (old[:70], s.count(old)); s = s.replace(old, new)


IA = 'la inteligencia artificial del Municipio'

# ---- Presupuesto: se vota con el escalón siguiente incluido; la plata se libera con la certificación
rep('        needs=[f"P{k+1}", gate], win=(D(y - 1, 11, 1), D(y - 1, 12, 31), f"antes de que empiece {y}"), win_est=True, fuente="anexo",\n'
    '        decision=f"Subir la partida de obra vecinal al {pct} sólo si el escalón anterior se ejecutó y justificó entero (Ordenanza 1, artículo 1).",',
    '        needs=[f"P{k+1}"], win=(D(y - 1, 11, 1), D(y - 1, 12, 31), f"antes de que empiece {y}"), win_est=True, fuente="anexo",\n'
    '        decision=(f"Incluir la partida de obra vecinal al {pct}. Ese dinero se libera cuando la auditoría externa certifica que se cumplió "\n'
    '                  "el escalón anterior, hacia marzo, y se congela si después el Tribunal de Cuentas objeta un año (6.2; Ordenanza 1, artículo 1)."),')

# ---- Cada año de la rampa, por ejercicio y desde que se libera su escalón
rep('act("M11", "Termina el año 1 de la rampa: el escalón se cuenta por ejercicio, que cierra el 31 de diciembre", "Intendente", ms=True, needs=["M10", "M07"], win=W(12), fuente="6.4",',
    'act("M11", "Termina el año 1 de la rampa: el escalón se cuenta por ejercicio, que cierra el 31 de diciembre", "Intendente", ms=True, needs=["M10", "M07"],\n'
    '    win=(D(2028, 12, 29), D(2028, 12, 31), "cierre del ejercicio 2028, en el mes 13"), fuente="6.4",')
rep('              "Si una comisión falla, el Ejecutivo la interviene y llama a una nueva asamblea en treinta días (6.6)."))',
    '              "Cuando una comisión falla, el Ejecutivo la interviene y llama a una nueva asamblea en treinta días (6.6)."))')
ASAMB = ('La primera ronda de asambleas del año elige las obras, en el mes {a}; la segunda, entre los meses {b} y {c}, '
         'las sigue y prepara las del año siguiente (cuadro 42). ')
rep('    "Comisiones vecinales con la Secretaría de Obras", span=(M(13), E(24)), cierre=True, needs=["M11", "P15"], win=W(13, 24), fuente="6.2",\n'
    '    steps="Contrato directo con la firma del 60% de los vecinos beneficiados (Ley Orgánica, artículo 132). Unos 14.454 millones.",\n'
    '    durnote="Duración del programa: un año.")',
    '    "Comisiones vecinales con la Secretaría de Obras", span=(M(15), D(2029, 12, 31)), cierre=True, needs=["M26", "P15"],\n'
    '    win=(M(15), D(2029, 12, 31), "ejercicio 2029, desde que se libera el escalón (meses 15 a 25)"), fuente="6.2",\n'
    f'    steps="{ASAMB.format(a=15, b=18, c=21)}Contrato directo con la firma del 60% de los vecinos beneficiados (Ley Orgánica, artículo 132). Unos 14.454 millones.",\n'
    '    durnote="Duración del programa: el ejercicio 2029, desde que la auditoría externa libera el escalón (6.2).")')
rep('act("M17", "Año 2 de la rampa, cumplido", "Intendente", ms=True, needs=["M15"], win=W(24), fuente="6.4",',
    'act("M17", "Año 2 de la rampa, cumplido", "Intendente", ms=True, needs=["M15"],\n'
    '    win=(D(2029, 12, 31), D(2029, 12, 31), "cierre del ejercicio 2029, en el mes 25"), fuente="6.4",')
rep('    "Comisiones vecinales con la Secretaría de Obras", span=(M(25), E(36)), cierre=True, needs=["M17", "M05", "P19"], win=W(25, 36),\n'
    '    fuente="6.2", steps="Unos 21.681 millones.", durnote="Duración del programa: un año.")',
    '    "Comisiones vecinales con la Secretaría de Obras", span=(M(27), D(2030, 12, 31)), cierre=True, needs=["M27", "M05", "P19"],\n'
    '    win=(M(27), D(2030, 12, 31), "ejercicio 2030, desde que se libera el escalón (meses 27 a 37)"),\n'
    f'    fuente="6.2", steps="{ASAMB.format(a=27, b=30, c=33)}Unos 21.681 millones.",\n'
    '    durnote="Duración del programa: el ejercicio 2030, desde que la auditoría externa libera el escalón (6.2).")')
rep('act("M19", "Año 3 de la rampa, cumplido", "Intendente", ms=True, needs=["M18"], win=W(36), fuente="6.4",',
    'act("M19", "Año 3 de la rampa, cumplido", "Intendente", ms=True, needs=["M18"],\n'
    '    win=(D(2030, 12, 31), D(2030, 12, 31), "cierre del ejercicio 2030, en el mes 37"), fuente="6.4",')
rep('    span=(M(37), E(48)), cierre=True, needs=["M19", "P23"], win=W(37, 48), fuente="6.2",\n'
    '    steps="Unos 28.908 millones por año. La otra mitad, la obra que sirve a varias zonas, sigue en manos del Ejecutivo y del Concejo.",\n'
    '    durnote="Duración del programa: un año.")',
    '    span=(M(39), E(48)), cierre=True, needs=["M28", "P23"], win=W(39, 48, "año 4, desde que se libera el escalón (meses 39 a 48)"), fuente="6.2",\n'
    f'    steps=("{ASAMB.format(a=39, b=42, c=45)}Unos 28.908 millones por año; "\n'
    '           "la otra mitad, la obra que sirve a varias zonas, sigue en manos del Ejecutivo y del Concejo."),\n'
    '    durnote="Duración del programa: hasta el fin del mandato, desde que la auditoría externa libera el escalón (6.2).")')
CERT = ('    decision="¿Se ejecutó y justificó todo el escalón? Si el Tribunal de Cuentas objeta después un año, se congela el escalón siguiente.",\n'
        '    note="Decisión del 16/11/2026: el presupuesto incluye el escalón siguiente, y el dinero se libera con la certificación, hacia marzo.")')
s += ('\n# ---------------------------------------------------------------- Revisión completa del 17/11/2026\n'
      'act("M27", "La auditoría externa certifica que se cumplió el año 2, y se libera el escalón del año 3", "Secretaría de Hacienda",\n'
      '    ms=True, needs=["M17", "I17"], win=W(27, 28), fuente="6.2",\n' + CERT + '\n'
      'act("M28", "La auditoría externa certifica que se cumplió el año 3, y se libera el escalón del año 4", "Secretaría de Hacienda",\n'
      '    ms=True, needs=["M19", "I17"], win=W(39, 40), fuente="6.2",\n' + CERT + '\n')

# ---- Ordenanzas 5 y 7 en la sesión extraordinaria (compromisos 4 y 5, hueco 6)
for n, comp in ((5, 4), (7, 5)):
    k = {5: '09', 7: '12'}[n]; prev = {5: 'C08', 7: 'C11'}[n]
    rep(f'act("C{k}", "Tratamiento de la Ordenanza {n} en el Concejo", "Concejo Deliberante", dur=22, est=True,\n'
        f'    sne=D(2028, 3, 1), needs=["{prev}"], fuente="anexo.{n}", note=TRAT + " " + RECESO)',
        f'act("C{k}", "Tratamiento de la Ordenanza {n} en el Concejo", "Concejo Deliberante", dur=22, est=True,\n'
        f'    needs=["{prev}"], fuente="anexo.{n}",\n'
        f'    note=TRAT + " Para cumplir el compromiso {comp}, el intendente pide tratarla en la sesión extraordinaria (Ley Orgánica, artículo 68, inciso 5). "\n'
        f'         "Si el Concejo no la aprueba antes del 19 de marzo, el compromiso se cumple cuando la apruebe (cuadro 40).")')
rep('    note="Fecha del programa: los cien días se cumplen el 19 de marzo de 2028. Es domingo: todo lo anterior termina el viernes 17.")',
    '    note=("Fecha del programa: los cien días se cumplen el 19 de marzo de 2028. Es domingo: todo lo anterior termina el viernes 17. "\n'
    '          "Los compromisos 4 y 5 dependen de que el Concejo apruebe a tiempo las Ordenanzas 5 y 7 (C10 y C13)."))')

# ---- La grabación no espera el certificado (hueco 15); la pasantía no espera el título (hueco 12)
rep('    note="El programa no dice cuánto tarda la Nación. Sin el certificado no se pueden sellar las grabaciones.")',
    '    note="El programa no dice cuánto tarda la Nación. Mientras llega, cada grabación se guarda con su fecha, su hora y su huella (cuadro 42).")')
rep('"Equipo de la inteligencia artificial del Municipio", dur=60, est=True, needs=["I04", "I06"], fuente="5.9",',
    '"Equipo de la inteligencia artificial del Municipio", dur=60, est=True, needs=["I04"], fuente="5.9",')
rep('act("H07", "El comerciante ya puede denunciar coimas, presiones y amenazas ante la inteligencia artificial, con grabación sellada (compromiso 16)",\n'
    '    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "I06", "H01"],',
    f'act("H07", "El comerciante ya puede denunciar coimas, presiones y amenazas ante {IA}, con grabación sellada (compromiso 16)",\n'
    '    "Equipo de la inteligencia artificial del Municipio", ms=True, needs=["I04", "H01"],')
rep('    needs=["E06", "E07", "E09", "E10"], win=W(15), fuente="6.4")', '    needs=["E06", "E07", "E10"], win=W(15), fuente="6.4")')

# ---- Textos que ya estaban resueltos en el programa
rep('act("M12", "Sortear el primer panel de vecinos, apenas se aprueba la Ordenanza 12",', 'act("M12", "Sortear el primer panel de vecinos, una vez aprobada la Ordenanza 12",')
rep('    note=("El programa no dice cómo entra el 12,5% en el presupuesto de 2028. "\n'
    '          "El 4.9 dice que con recursos afectados el Ejecutivo puede crear la partida sin volver al Concejo."))',
    '    note="El de 2028 lo presenta el gobierno que termina, y la partida del año 1 se crea con el artículo 119 (6.2 y 4.9).")')
rep('    note="Duración estimada: dos meses, como el ciclo de la Ciudad de Buenos Aires que cita el 6.1.")',
    '    note="Duración estimada: dos meses, como el ciclo de la Ciudad de Buenos Aires que cita la nota del capítulo 4.")')
rep('"Cada proyecto se revisa antes de votar. Cada comisión decide si el tendido', '"Cada proyecto se revisa antes de votar, y cada comisión decide si el tendido')
rep('"El primer año las hace el Ejecutivo, porque las comisiones todavía se están formando. Se cuentan los baldíos,',
    '"El primer año las hace el Ejecutivo, porque las comisiones todavía se están formando. También se cuentan los baldíos,')
rep('act("U10", "Doscientos shows por año de artistas nuevos de San Isidro, y espectáculos al aire libre todas las semanas, de lunes a jueves (meta 17)",',
    'act("U10", "Doscientos shows por año de artistas nuevos de San Isidro, y espectáculos todas las semanas, de lunes a jueves: al aire libre de septiembre a abril, y bajo techo el resto del año (meta 17)",')

# ---- Ordenanza 19: una sola, revisada por el abogado
rep('act("C52", "Revisar la Ordenanza 19 del anexo: foodtrucks y cambio del artículo 9 de la Ordenanza 5824", "Intendente",',
    'act("C52", "Revisión legal de la Ordenanza 19 del anexo: foodtrucks y cambio del artículo 9 de la Ordenanza 5824", "Abogado especialista en municipios",')
rep('act("C53", "Entra la ordenanza de foodtrucks: canon por mes y 75% de empleo local", "Intendente", ms=True,',
    'act("C53", "Entra la Ordenanza 19: foodtrucks, con canon por mes y 75% de empleo local, y cambio del artículo 9 de la Ordenanza 5824", "Intendente", ms=True,')
rep('act("C54", "Tratamiento de la ordenanza de foodtrucks en el Concejo", "Concejo Deliberante", dur=22, est=True,\n    needs=["C53"], fuente="5.5", note=TRAT)',
    'act("C54", "Tratamiento de la Ordenanza 19 en el Concejo", "Concejo Deliberante", dur=22, est=True,\n    needs=["C53"], fuente="anexo.19", note=TRAT)')
rep('act("C55", "El Concejo aprueba la ordenanza de foodtrucks", "Concejo Deliberante", ms=True, needs=["C54"],\n    fuente="5.5", decision=TRECE)',
    'act("C55", "El Concejo aprueba la Ordenanza 19", "Concejo Deliberante", ms=True, needs=["C54"],\n    fuente="anexo.19", decision=TRECE)')
rep('act("C56", "Entra el cambio del artículo 9 de la Ordenanza 5824, que hoy sólo permite vender bebidas en kioscos en el Bosque Alegre",\n'
    '    "Intendente", ms=True, needs=["C52"], win=W(4, 6), fuente="6.4")\n'
    'act("C57", "Tratamiento del cambio de la Ordenanza 5824 en el Concejo", "Concejo Deliberante", dur=22, est=True,\n'
    '    needs=["C56"], fuente="5.5", note=TRAT)\n'
    'act("C58", "El Concejo aprueba el cambio de la Ordenanza 5824", "Concejo Deliberante", ms=True, needs=["C57"],\n'
    '    fuente="5.5", decision=TRECE)\n', '')
rep('(lo destraba la ordenanza de foodtrucks)', '(lo destraba la Ordenanza 19)')
rep('act("K26", "Centro de foodtrucks y actividades en el Bosque Alegre (lo destraba el cambio de la Ordenanza 5824)",\n'
    '    "Habilitaciones y Agencia de Control", dur=20, est=True, needs=["C58", "K25"], fuente="5.5",',
    'act("K26", "Centro de foodtrucks y actividades en el Bosque Alegre (lo destraba la Ordenanza 19)",\n'
    '    "Habilitaciones y Agencia de Control", dur=20, est=True, needs=["C55", "K25"], fuente="5.5",')

# ---- Abogado, audiencia pública de la Ordenanza 21 y garantía
rep('    steps=("El convenio con el banco de los sueldos. La compensación del teléfono propio. Quién ve cada grabación. "\n'
    '           "El registro de instructores y artistas. Los shows que no cuentan como ruido molesto. Los datos de los chicos "\n'
    '           "en el profesor digital. Las cuotas de las multas."),',
    '    steps=("Entre otras: el convenio con el banco de los sueldos, la compensación del teléfono propio, quién ve cada grabación, "\n'
    '           "el registro de instructores y artistas, los shows que no cuentan como ruido molesto, los datos de los chicos en el profesor digital, "\n'
    '           "las cuotas de las multas, la garantía de alquiler y el descuento del sueldo, las viviendas en el lote y los terrenos sin uso (Ordenanza 21), "\n'
    '           "el pago a los power users, las denuncias con firma digital, las historias según lo que usa cada vecino, la salud mental y la consulta de lugares."),')
rep('act("V07", "Tratamiento de las Ordenanzas 20 y 21 en el Concejo", "Concejo Deliberante", dur=22, est=True, needs=["V06"],\n    fuente="5.4", note=TRAT)',
    'act("V07", "Tratamiento de las Ordenanzas 20 y 21 en el Concejo", "Concejo Deliberante", dur=22, est=True, needs=["V06"],\n'
    '    fuente="5.4", note=TRAT, steps="Antes de votar la 21, el Concejo hace una audiencia pública (5.4).")')
rep('    ms=True, needs=["V07"], win=W(7, 12), fuente="5.4",\n    steps="Comisión del 3% por mes',
    '    ms=True, needs=["V07", "T05"], win=W(7, 12), fuente="5.4",\n    steps="Comisión del 3% por mes')

# ---- Reglas de escritura
for old, new in [
        ('"Pagar el uso de la inteligencia artificial con compras chicas', f'"Pagar el uso de {IA} con compras chicas'),
        ('entre empleados cuyo trabajo ya hace la inteligencia artificial",', f'entre empleados cuyo trabajo ya hace {IA}",'),
        ('La inteligencia artificial avisa a cada vecino cuánto debe', 'La inteligencia artificial del Municipio avisa a cada vecino cuánto debe'),
        ('la pide sólo la persona acusada y la inteligencia artificial la resuelve en horas', f'la pide sólo la persona acusada y {IA} la resuelve en horas'),
        ('act("G18", "La inteligencia artificial propone', 'act("G18", "La inteligencia artificial del Municipio propone'),
        ('act("K35", "La inteligencia artificial dice', 'act("K35", "La inteligencia artificial del Municipio dice'),
        ('"Los vecinos proponen en la inteligencia artificial a qué artistas', f'"Los vecinos proponen en {IA} a qué artistas'),
        ('act("H12", "Habilitaciones en la inteligencia artificial:', f'act("H12", "Habilitaciones en {IA}:'),
        ('lo que los vecinos le plantean a la inteligencia artificial (meta 15)', f'lo que los vecinos le plantean a {IA} (meta 15)'),
        ('"Guarda el ingreso y cuántas personas viven en el hogar. Se usa sólo para las multas. Se presenta',
         '"Guarda el ingreso y cuántas personas viven en el hogar, sólo para las multas. Se presenta'),
        ('note="El número sale del registro de inserción laboral. El primer registro da el punto de partida (cuadro 41).")',
         'note="Lo da el registro de inserción laboral, y su primer dato es el punto de partida (cuadro 41).")'),
        ('nunca como imagen. La comparación avisa cuando algo se sale de lo normal.', 'nunca como imagen. Cuando algo se sale de lo normal, la comparación avisa.'),
        ('Si es la red de AySA, se le exige el arreglo. Si son casas,', 'Si es la red de AySA, se le exige el arreglo; si son casas,'),
        ('steps="El Municipio no adelanta dinero. El riesgo de cobro lo toma el banco.")', 'steps="El Municipio no adelanta dinero: el riesgo de cobro lo toma el banco.")')]:
    rep(old, new)
P.write_text(s)

# ---- pasos_extra.py y pruebas.py: salen C56 a C58, dos textos y el error de tipeo
X = H / 'pasos_extra.py'; t = X.read_text()
for old, new in [('"C47", "C50", "C54", "C57", "P14"', '"C47", "C50", "C54", "P14"'), ('"C48", "C51", "C55", "C58"]', '"C48", "C51", "C55"]'),
                 ('"La lista de los seis proyectos del mes 1 (cuadro 42). La revisión del abogado (T02)."',
                  '"La lista de los seis proyectos del mes 1 (cuadro 42), con la revisión del abogado (T02)."'),
                 ('la parte de la inteligencia artificial que saca el turno', 'la parte de la inteligencia artificial del Municipio que saca el turno'),
                 ('"La inteligencia artificial arma el caso', '"La inteligencia artificial del Municipio arma el caso')]:
    assert t.count(old) == 1, old; t = t.replace(old, new)
X.write_text(t)
Q = H / 'pruebas.py'; t = Q.read_text()
assert t.count('    "C56": "Expedientes y Boletín Oficial Municipal.",\n') == 1 and t.count('f"La propia {IA}."') == 5
t = t.replace('    "C56": "Expedientes y Boletín Oficial Municipal.",\n', '').replace('f"La propia {IA}."', '"La propia inteligencia artificial del Municipio."')
Q.write_text(t)
print('ok')
