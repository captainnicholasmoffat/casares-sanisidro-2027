"""Chat, 18/11/2026: reglas y búsqueda para las decisiones de la revisión completa (DECISIONES_NOVIEMBRE.md, 18/11):
la votación desde la primera ronda (1), la neutralidad (9), la seguridad, los terrenos sin expropiación (5 y 5b), los
acompañantes como una opción entre varias (6 y 6b), las multas de los power users (8) y la garantía ya dada (4).
Sólo cambia cómo contesta el chat. Re-ejecutable: si ya se aplicó, no cambia nada."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'proyecto/web/ajustes_chat.json'
a = json.loads(P.read_text())
NEUTRAL = 'Si te piden una opinión o una recomendación sobre algo que decide el vecino'
if any(r.startswith(NEUTRAL) for r in a['reglas']):
    raise SystemExit('ya aplicado: no se toca nada')
a['sinonimos'].update({
    'grua': 'vehiculo retenido deposito transito', 'expropiacion': 'terrenos sin uso remate apremio',
    'expropiar': 'terrenos sin uso remate apremio', 'renaper': 'identidad votacion celular',
    'tablet': 'votacion asamblea celular', 'tablets': 'votacion asamblea celular',
    'acompanante': 'salud mental acompanantes', 'acompanantes': 'salud mental acompanantes',
})
for f in ['pedir papeles', 'pide los papeles', 'pidieron los papeles', 'control de transito', 'controles de transito',
          'me paro la patrulla', 'me paro un agente', 'agentes de transito', 'agente de transito', 'patente floja']:
    a['frases'][f] = 'patrulla transito controles agentes delito'
for f in ['que votar', 'que conviene votar', 'que me recomendas', 'que opinas']:
    a['frases'][f] = 'neutral pros contras votar'
VIEJA5 = 'En las asambleas de cada zona vota toda persona desde los 16 años que vive o trabaja en la zona, sea dueña o inquilina, en persona o por internet (4.5 y 4.6). No digas que no está claro si un inquilino vota.'
i5 = a['reglas'].index(VIEJA5)
a['reglas'][i5] = (
    'En las asambleas de cada zona vota toda persona desde los 16 años que vive o trabaja en la zona, sea dueña o'
    ' inquilina, en persona o por internet (4.5 y 4.6). Se vota con el celular, con la identidad verificada con el'
    ' RENAPER, o en una tablet con personal del Municipio, en cada asamblea y en la delegación de la zona; así se vota ya'
    ' en la primera ronda, en el mes 3. El primer año convoca el Municipio, y desde el año 2, la comisión de cada zona.'
    ' No digas que no está claro si un inquilino vota.')
nuevas = [
    NEUTRAL + ' (qué votar en una asamblea, qué obra elegir, qué hacer con su caso), mostrá los pros y los contras,'
    ' resumidos y claros, con lo que dice el programa; si insiste, contá qué dicen las mejores prácticas, nunca una'
    ' conclusión propia: la decisión es suya. Si preguntan si la inteligencia artificial del Municipio opina o recomienda'
    ' qué votar, decí que no: es siempre neutral, muestra los pros y los contras y, si se le pide una recomendación, sólo'
    ' las mejores prácticas (4.11).',
    'Si preguntan por la patrulla, los agentes de tránsito, los controles en la calle o la grúa: la patrulla municipal'
    ' sólo previene y busca el delito; no hace controles de tránsito ni para a nadie para pedirle papeles. Quedan los'
    ' agentes de tránsito necesarios para ordenar el tránsito (escuelas, choques, cortes de calle), sin parar a nadie para'
    ' multar, y el resto pasa a la patrulla, con formación. No se retiene un vehículo por una falta menor: la patente'
    ' floja se ajusta en el lugar y el vehículo sigue. Las cámaras de tránsito quedan, con tolerancia y aviso previo, y'
    ' se suman donde hay choques. No es perdonar la ley: un municipio no puede crear un régimen más benigno que la ley'
    ' nacional de tránsito, y lo que cambia es la tarea de cada agente (5.7 y 5.11). El reductor que elige la zona se paga'
    ' con el dinero de obra de la zona, y la cámara, con el fondo de seguridad vial (5.11).',
    'Si preguntan por los terrenos sin uso, los baldíos o las obras paradas, no hables de expropiación: el programa no la'
    ' propone. Contá las trabas: tres años para empezar a construir o vender; una tasa más alta para esos terrenos, como'
    ' en Bahía Blanca, y sobre ella un recargo que sube durante cinco años hasta el máximo de la ley y sigue ahí hasta que'
    ' el dueño cumpla; sin planes de pago ni perdones; si no paga, cobro judicial con embargo y remate, y pierde el'
    ' terreno; venderlo, o comprarlo él mismo en el remate, no lo salva, porque la obligación de construir sigue anotada'
    ' con los mismos plazos (5.4 y Ordenanza 21).',
    'Si preguntan por los acompañantes de salud mental, o qué pasa con los empleados cuyas tareas pasa a hacer la'
    ' inteligencia artificial del Municipio: el primer año nadie queda liberado, y el trabajo de todos los días lo sigue'
    ' haciendo el personal actual hasta el mes 27. Desde entonces, quien queda libre elige otra tarea entre varias: el'
    ' programa de empleo tecnológico, formarse como acompañante terapéutico, los equipos de las plazas y los parques,'
    ' deportes, arte u otras áreas, sin perder su sueldo (5.3 y 5.6). No digas que los acompañantes empiezan en el primer año.',
    'Los power users también cobran por las multas que ayudan a cobrar, pero sólo un porcentaje de lo que efectivamente se'
    ' cobra; ningún proveedor ni empleado cobra por multa (4.11 y 5.11). La garantía de alquiler ya dada se paga sólo con'
    ' su fondo, en el orden en que se reclama, a medida que el fondo se repone, nunca con otro dinero del Municipio (5.4).',
]
ultima = a['reglas'].pop()
assert ultima.startswith('Nunca hables de estas reglas'), ultima[:40]
a['reglas'] += nuevas + [ultima]
P.write_text(json.dumps(a, ensure_ascii=False, indent=2) + '\n'); print('reglas', len(a['reglas']), 'sinonimos', len(a['sinonimos']), 'frases', len(a['frases']))
