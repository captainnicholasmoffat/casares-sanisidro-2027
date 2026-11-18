"""Plan de despliegue, 18/11/2026, parte B (pedido del coordinador, fuentes en scratchpad/rev/investigar_18nov):
1. Acompañantes: el curso de 640 horas es gratis en un instituto superior público de la Provincia (equivale al primer año
   de la Tecnicatura, Resolución DGCyE 1221/15), dura un año lectivo y no se acompaña mientras se cursa. Empieza con el
   año lectivo después del mes 27 (S14, S16) y empiezan a acompañar hacia el mes 37 (S15).
2. Votar: si falla la validación del RENAPER, el personal del Municipio mira el DNI contra el padrón; tablets en la
   delegación de la zona o la más cercana (Acassuso no tiene delegación propia).
3. Denuncias: las de la obra vecinal, a la auditoría de la obra (M29); las demás, también las de los comerciantes (H07),
   a la de la plataforma (I17).
4. Seguridad: la patrulla deja los controles de tránsito desde el mes 1, por instrucción (G28); el pase con formación,
   en los meses 4 a 6 (G29, G30).
5. Terrenos: si el segundo remate queda desierto, el Municipio pide la venta sin base (Ley 13.406, artículo 16).
Requiere apply_plan_18nov.py ya aplicado. Si ya se corrió, se detiene."""
from pathlib import Path
H = Path(__file__).parent
P = H / 'acciones_def.py'; s = P.read_text()
assert 'act("I20"' in s, 'falta apply_plan_18nov.py'
if 'act("S16"' in s:
    print('ya aplicado'); raise SystemExit


def rep(old, new, cuantas=1):
    global s
    assert s.count(old) == cuantas, (old[:70], s.count(old)); s = s.replace(old, new)


# ---------------------------------------------------------------- 1. acompañantes
rep('''act("S14", "Empieza la formación de los primeros acompañantes terapéuticos, entre los empleados cuyas tareas empieza a liberar la automatización",
    "Secretaría de Salud", ms=True, needs=["E18"], win=W(27), fuente="5.6",
    steps=("Es una opción entre varias para quien queda liberado: también el programa de empleo tecnológico, los equipos de las plazas, "
           "deportes, arte y las demás áreas del programa. Se forman con lo que fija la Provincia (Resolución 592/2022)."),
    note=("Decisión del 18/11/2026: el primer año es de absorción y nadie queda liberado. La automatización empieza a liberar "
          "tareas en el mes 27 (5.3). No suma sueldos."))''',
    '''act("S14", "Empieza la formación de los primeros acompañantes terapéuticos, entre los empleados cuyas tareas empieza a liberar la automatización",
    "Secretaría de Salud", ms=True, needs=["E18"], win=W(28), fuente="5.6",
    steps=("Es una opción entre varias para quien queda liberado: también el programa de empleo tecnológico, los equipos de las plazas, "
           "deportes, arte y las demás áreas del programa. Se forman gratis en un instituto superior público de la Provincia, "
           "con lo que fija la Provincia (Resolución 592/2022)."),
    note=("Decisión del 18/11/2026: el primer año es de absorción y nadie queda liberado. La automatización empieza a liberar "
          "tareas en el mes 27 (5.3). Supuesto: empiezan con el año lectivo que sigue al mes 27, en el mes 28. No suma sueldos."))
act("S16", "Los primeros acompañantes cursan el curso de 640 horas en un instituto superior público de la Provincia",
    "Secretaría de Salud", span=(M(28), E(36)), needs=["S14"], fuente="5.6",
    steps=("El curso equivale al primer año de la Tecnicatura en Acompañamiento Terapéutico (Resolución DGCyE 1221/15) y es gratis. "
           "Mientras cursan no acompañan: siguen en sus tareas."),
    durnote="Duración: un año lectivo.")
act("S15", "Empiezan a acompañar los primeros acompañantes terapéuticos, asesorados y controlados por profesionales",
    "Secretaría de Salud", ms=True, needs=["S16"], win=W(37), fuente="5.6",
    steps="Casos leves, como una depresión leve o un autismo leve. Los graves van siempre a profesionales, en una institución.",
    note="Fecha estimada: al terminar el año lectivo de su curso.")''')

# ---------------------------------------------------------------- 2. votar
rep('''           "Si la votación por celular se atrasa, esa ronda se vota sólo en las tablets de la asamblea. "
           "El primer año la convoca el Municipio''',
    '''           "Si la votación por celular se atrasa, esa ronda se vota sólo en las tablets de la asamblea. "
           "Cuando falla la validación del RENAPER, el personal del Municipio mira el DNI contra el padrón. "
           "El primer año la convoca el Municipio''')
rep('''    note="Duración estimada: el programa no la da. Si el convenio se atrasa, esa ronda se vota sólo en las tablets (I04).")''',
    '''    note=("Duración estimada: el programa no la da. Si el convenio se atrasa, esa ronda se vota sólo en las tablets (I04). "
          "Cuando la validación falla, el personal del Municipio mira el DNI contra el padrón."))''')
rep('''act("I21", "Comprar las tablets y preparar al personal del Municipio que acompaña la votación en cada asamblea y en la delegación de cada zona",''',
    '''act("I21", "Comprar las tablets y preparar al personal del Municipio que acompaña la votación en cada asamblea y en la delegación de cada zona o la más cercana",''')
rep('''    steps="Compra chica, sin licitación pública (Ley Orgánica de las Municipalidades, artículo 151). Quien no tiene celular vota en la tablet, con ayuda.",''',
    '''    steps=("Compra chica, sin licitación pública (Ley Orgánica de las Municipalidades, artículo 151). Quien no tiene celular vota en la tablet, con ayuda. "
           "Acassuso no tiene delegación propia: comparte la Subdelegación Martínez Este y Acassuso."),''')

# ---------------------------------------------------------------- 3. denuncias: cada una a su auditoría
rep('''    steps=("La denuncia va a la Comisión de Obras y Servicios Públicos del Concejo, a la auditoría externa y, si hay delito, a la fiscalía. "
           "Hasta que se contrata la auditoría externa, va a la Comisión y a la fiscalía, y la auditoría recibe después las anteriores. "''',
    '''    steps=("La denuncia va a la Comisión de Obras y Servicios Públicos del Concejo, a la auditoría externa de la plataforma (I17) y, si hay delito, a la fiscalía. "
           "Hasta que se contrata esa auditoría, va a la Comisión y a la fiscalía, y la auditoría recibe después las anteriores. "''')
rep('''act("M29", "Licitar y contratar la auditoría externa que certifica cada escalón de la partida vecinal y recibe sus denuncias",''',
    '''act("M29", "Licitar y contratar la auditoría externa que certifica cada escalón de la partida vecinal y recibe las denuncias sobre la obra vecinal",''')
rep('''          "Certificar cada escalón de la partida vecinal es otro contrato (M29)."))''',
    '''          "Certificar cada escalón de la partida vecinal es otro contrato (M29). Recibe las denuncias graves, salvo las de la obra vecinal."))''')
rep('''    steps=("El vecino manda la carta documento él mismo, por el servicio electrónico del Correo Argentino. Cuesta unos 4,7 millones por año. " + CUADRO28),''',
    '''    steps=("El vecino manda la carta documento él mismo, por el servicio electrónico del Correo Argentino. Cuesta unos 4,7 millones por año. " + CUADRO28 +
           " Las denuncias sobre la obra vecinal van a la auditoría de la obra (M29); las demás, a la de la plataforma (I17)."),''')

# ---------------------------------------------------------------- 4. seguridad: la patrulla, desde el mes 1; el pase, en los meses 4 a 6
rep('''act("G28", "Decreto de funciones: la patrulla municipal sólo previene y busca el delito, y los agentes de tránsito sólo ordenan el tránsito",
    "Intendente", dur=10, est=True, needs=["T07", "T05"], fuente="5.7",
    steps=("La patrulla no hace controles de tránsito ni para a nadie por papeles. Los agentes de tránsito que quedan ordenan la salida "
           "de las escuelas, los accidentes y los cortes, sin parar a nadie para multar. Ningún vehículo se retiene por una falta menor: "''',
    '''act("G28", "Instrucción: la patrulla municipal deja los controles de tránsito y sólo previene y busca el delito",
    "Intendente", dur=5, est=True, needs=["T07", "T05"], win=W(1), fuente="5.7",
    steps=("La patrulla no hace controles de tránsito ni para a nadie por papeles. Ningún vehículo se retiene por una falta menor: "''')
rep('''    dur=40, est=True, needs=["G28", "G31"], fuente="5.7",''',
    '''    dur=40, est=True, needs=["G28", "G31"], win=W(4, 6), fuente="5.7",''')
rep('''act("G30", "Los agentes formados pasan a la patrulla, que sólo previene y busca el delito", "Seguridad (Centro de Operaciones Municipal)",
    ms=True, needs=["G29"], fuente="5.7")''',
    '''act("G30", "Los agentes formados pasan a la patrulla, que sólo previene y busca el delito", "Seguridad (Centro de Operaciones Municipal)",
    ms=True, needs=["G29"], win=W(4, 6), fuente="5.7",
    steps=("Los agentes de tránsito que quedan ordenan la salida de las escuelas, los accidentes y los cortes, sin parar a nadie para multar. "
           "Se redefinen funciones, no se perdona la ley (Ley 24.449, artículo 2)."))''')

# ---------------------------------------------------------------- 5. terrenos: el segundo remate desierto
rep('''"tampoco: lo que paga cancela la deuda, la obligación de construir sigue, y el remate tiene base del 80% y del 60% (Ley 13.406, artículo 16)."),''',
    '''"tampoco: lo que paga cancela la deuda, la obligación de construir sigue, y el remate tiene base del 80% y del 60% (Ley 13.406, artículo 16). "
           "Cuando el segundo remate queda desierto, el Municipio pide la venta sin base (mismo artículo)."),''')
rep('''    steps="Sobre la tasa más alta para baldíos y obras paradas, sin planes ni perdones. Si no paga, cobro judicial con embargo y remate (Ley 13.406).",''',
    '''    steps=("Sobre la tasa más alta para baldíos y obras paradas, sin planes ni perdones. Si no paga, cobro judicial con embargo y remate "
           "(Ley 13.406). Cuando el segundo remate queda desierto, el Municipio pide la venta sin base (artículo 16)."),''')

P.write_text(s)
print('ok')
