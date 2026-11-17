"""Plan de despliegue, 17/11/2026: lleva al plan los cambios del programa de esta fecha (decisiones de Nick del 16 y
17/11 y los 30 huecos resueltos). Edita acciones_def.py; después se corre build.py y gen_revision.py."""
from pathlib import Path
P = Path(__file__).with_name('acciones_def.py'); s = P.read_text()

def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old)); s = s.replace(old, new, 1)

# Obras del año 1: se eligen en la primera ronda (Nick, 16/11)
rep('act("M03", "Primera ronda de asambleas en las seis zonas: informar y anotar qué necesita cada zona (compromiso 11)",',
    'act("M03", "Primera ronda de asambleas en las seis zonas: informar, elegir las obras del año 1 y contar los terrenos sin uso (compromiso 11)",')
rep('    steps="Se informa a los vecinos y se completa el diagnóstico de cada zona. Las actas y los asistentes se pueden consultar.",\n    note="La primera ronda informa. Las obras se eligen en la segunda (6.1).")',
    '    steps=("Se informa a los vecinos y se eligen las obras del año: un voto por persona desde los 16 años, en la asamblea o por internet. "\n           "El primer año las hace el Ejecutivo, porque las comisiones todavía se están formando. Se cuentan los baldíos, las ruinas y las obras paradas (5.4)."),\n    note="Cambio del 16/11/2026: las obras de cada año se eligen en la primera ronda, para que tengan tiempo de licitarse y terminarse en el mismo año (6.1).")')
rep('act("M08", "Segunda ronda de asambleas: los vecinos eligen las obras de su zona", "Comisiones vecinales",',
    'act("M08", "Segunda ronda de asambleas: los vecinos siguen las obras del año y preparan las del año siguiente", "Comisiones vecinales",')
rep('act("M09", "El Ejecutivo responde por escrito a cada decisión de las zonas, con sus razones", "Intendente",',
    'act("M09", "El Ejecutivo responde por escrito a cada pedido de la segunda ronda, con sus razones", "Intendente",')
rep('"Secretaría de Obras con las comisiones vecinales", dur=70, est=True, needs=["M09", "P09"],\n    win=(M(6), E(12), "dentro del año 1, hasta el mes 12"), fuente="6.2",',
    '"Secretaría de Obras con las comisiones vecinales", dur=70, est=True, needs=["M25", "P09"],\n    win=(M(4), E(12), "dentro del año 1, hasta el mes 12"), fuente="6.2",')
rep('act("M11", "Año 1 de la rampa, cumplido", "Intendente", ms=True, needs=["M10", "M07"], win=W(12), fuente="6.4",',
    'act("M11", "Termina el año 1 de la rampa: el escalón se cuenta por ejercicio, que cierra el 31 de diciembre", "Intendente", ms=True, needs=["M10", "M07"], win=W(12), fuente="6.4",')
# Segundo centro de apoyo escolar en el mes 6
rep('act("E38", "Abre el segundo centro de apoyo escolar", "Educación (área municipal)", ms=True, needs=["E37"], win=AÑO1,\n    fuente="6.4",\n    note="Supuesto: abre antes de la prueba del profesor digital, que se hace «en los primeros centros» (mes 7).")',
    'act("E38", "Abre el segundo centro de apoyo escolar", "Educación (área municipal)", ms=True, needs=["E37"], win=W(6),\n    fuente="6.4",\n    note="El calendario lo pone en el mes 6, antes de la prueba del profesor digital en los primeros centros (mes 7).")')
# Ordenanza 19 del anexo
rep('act("C52", "Redactar la ordenanza de foodtrucks y el cambio del artículo 9 de la Ordenanza 5824", "Intendente",\n    dur=15, est=True, needs=["T07"], fuente="5.5",\n    note="Estas dos ordenanzas no están en el anexo.")',
    'act("C52", "Revisar la Ordenanza 19 del anexo: foodtrucks y cambio del artículo 9 de la Ordenanza 5824", "Intendente",\n    dur=15, est=True, needs=["T07"], fuente="anexo.19",\n    note="Desde el 17/11/2026 su texto está en el anexo (Ordenanza 19).")')
# Denuncias antes de la auditoría externa
rep('    steps=("La denuncia va a la Comisión de Obras y Servicios Públicos del Concejo, a la auditoría externa y, si hay delito, a la fiscalía. "\n           "Nunca sólo al jefe del denunciado. Con la misma prueba sellada se puede denunciar un ruido."),',
    '    steps=("La denuncia va a la Comisión de Obras y Servicios Públicos del Concejo, a la auditoría externa y, si hay delito, a la fiscalía. "\n           "Hasta que se contrata la auditoría externa, va a la Comisión y a la fiscalía, y la auditoría recibe después las anteriores. "\n           "Mientras no llega el certificado de firma digital, cada grabación se guarda con su fecha, su hora y su huella. "\n           "Nunca sólo al jefe del denunciado. Con la misma prueba sellada se puede denunciar un ruido."),')

s += '''

# ---------------------------------------------------------------- Cambios del 17/11/2026
act("M24", "El Ejecutivo responde por escrito a cada obra elegida en la primera ronda, con sus razones", "Intendente",
    dur=22, needs=["M03"], win=W(3, 4), fuente="anexo.1", durnote=TREINTA,
    steps="Toda persona puede ver cada respuesta desde el día en que sale. Ningún silencio reemplaza la respuesta.")
act("M25", "Licitar y adjudicar las obras del año 1", "Secretaría de Obras", dur=66, needs=["M24", "P09"], fuente="6.4",
    durnote=LIC, steps="Cada obra se licita por separado, con su precio y su plazo.")
act("M26", "La auditoría externa certifica que se cumplió el año 1, y se libera el escalón del año 2", "Secretaría de Hacienda",
    ms=True, needs=["M11", "I17"], win=W(15, 16), fuente="6.2",
    decision="¿Se ejecutó y justificó todo el escalón? Si el Tribunal de Cuentas objeta después un año, se congela el escalón siguiente.",
    note="Decisión del 16/11/2026: el presupuesto incluye el escalón siguiente, y el dinero se libera con la certificación, hacia marzo.")
act("I19", "Pagar el uso de la inteligencia artificial con compras chicas, sin licitación pública, mientras corre la primera licitación",
    "Ciencia y Técnica", dur=55, est=True, needs=["T07"], win=W(1, 3), fuente="6.4",
    note="Ley Orgánica de las Municipalidades, artículo 151; montos actualizados por la Resolución 248/2026. Decisión del 16/11/2026.")
act("V06", "Presentar la Ordenanza 20 (garantía de alquiler) y la 21 (viviendas en el lote y terrenos sin uso)", "Intendente",
    ms=True, needs=["T07"], win=W(4, 6), fuente="6.4")
act("V07", "Tratamiento de las Ordenanzas 20 y 21 en el Concejo", "Concejo Deliberante", dur=22, est=True, needs=["V06"],
    fuente="5.4", note=TRAT)
act("V08", "Empieza la garantía de alquiler del Municipio, con su fondo propio y sin dinero del Municipio", "Secretaría de Hacienda",
    ms=True, needs=["V07"], win=W(7, 12), fuente="5.4",
    steps="Comisión del 3% por mes de cada lado, depósito del 12% de un mes, alquiler hasta el 40% del ingreso, freno si la mora es alta.")
act("V09", "Notificar a los dueños de los terrenos sin uso contados en la primera ronda: desde ahí corren sus tres años", "Secretaría de Obras",
    dur=20, est=True, needs=["V07", "M03"], win=W(7, 12), fuente="5.4",
    note="Ley 14.449: los plazos no cambian aunque el terreno se venda, y la obligación se anota en la escritura.")
act("S14", "Empieza la formación de los primeros acompañantes terapéuticos, entre empleados cuyo trabajo ya hace la inteligencia artificial",
    "Secretaría de Salud", ms=True, needs=["I04"], win=W(7, 12), fuente="6.4",
    note="Con la formación que fija la Provincia (Resolución 592/2022). No suma sueldos.")
'''
P.write_text(s); print('ok')
