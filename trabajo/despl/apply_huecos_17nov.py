"""Plan de despliegue, 17/11/2026: anota en huecos.md cómo quedó resuelto cada hueco (decisiones de Nick del 16 y 17/11
y arreglos obvios hechos en el programa)."""
import re
from pathlib import Path
P = Path(__file__).with_name('huecos.md'); t = P.read_text()
t = t.replace('No se resuelven acá: se listan para decidir.', 'Se listaron para decidir, y quedaron resueltos el 16 y el 17 de noviembre de 2026: al final de cada punto se dice cómo.', 1)
R = {
 1: 'El calendario dice ahora que cada escalón se cuenta por ejercicio, que cierra el 31 de diciembre (M11).',
 2: 'Decisión: el presupuesto incluye el escalón siguiente, y el dinero se libera cuando la auditoría externa certifica que se cumplió el anterior, hacia marzo (6.2, Ordenanza 1, artículo 1, y M26).',
 3: 'Decisión: si el Tribunal de Cuentas objeta después un año, se congela el escalón que sigue (6.2 y Ordenanza 1, artículo 1).',
 4: 'La ordenanza preparatoria va primera en el orden del día; la derogación es la primera en entrar (6.6).',
 5: 'A los cien días, la primera asamblea de cada zona ya se hizo (6.1, introducción y cierre).',
 6: 'Decisión: la promesa queda, con la aclaración de que depende de que el Concejo apruebe la ordenanza antes de los cien días (cuadro 40).',
 7: 'El calendario dice que el quinto y el sexto centro abren al empezar el año 3 (mes 25).',
 8: 'El calendario abre el segundo centro en el mes 6 (E38).',
 9: 'Se sacó «apenas»: el panel se sortea una vez aprobada la Ordenanza 12, en los meses 7 a 12.',
 10: 'Decisión: las obras de cada año se eligen en la primera ronda (mes 3), se licitan y se terminan dentro del mismo año; la segunda ronda sigue las obras y prepara las del año siguiente (6.1, cuadro 42, M24, M25 y M10).',
 11: 'Queda resuelto con el punto 10.',
 12: 'El calendario del mes 15 suma la beca municipal si el título todavía no vale en todo el país.',
 13: 'Ya estaba resuelto en el programa: la oficina la atiende el equipo técnico de las cámaras, y desde el mes 27 los egresados (G12).',
 14: 'Decisión: mientras corre la primera licitación, el uso se paga con las compras chicas que la ley permite sin licitación pública (Ley Orgánica, artículo 151; I19).',
 15: 'Hasta que se contrata la auditoría externa, la denuncia va a la Comisión del Concejo y a la fiscalía, y la auditoría recibe después las anteriores; mientras no llega el certificado, cada grabación se guarda con su fecha, su hora y su huella (Ordenanza 4 y cuadro 42).',
 16: 'Ya estaba resuelto: la Ordenanza 4 dice que la consecuencia rige desde que la grabación sellada funciona en todas las inspecciones (H09).',
 17: 'La Ordenanza 9 suma un artículo con el 20% para pymes y el 5% para empresas nuevas; la prioridad del semillero vale para las subcontrataciones nuevas.',
 18: 'Su texto está ahora en el anexo: Ordenanza 19 (C52).',
 19: 'La meta queda «todas las semanas»: al aire libre de septiembre a abril, y bajo techo el resto del año (cuadro 41).',
 20: 'Durante la prueba se usa el sonido que ya tiene el Municipio, o se alquila (5.5).',
 21: 'El calendario ordena los pasos del tramo de arena, y «el primer verano» es el de 2028 a 2029.',
 22: 'Los puestos abren una vez aprobada la Ordenanza 11 (cuadro 42).',
 23: 'Ya estaba resuelto en el 5.3: 3, 3, 5 y 5 empresas en el mandato (E17, E23, E26 y E29).',
 24: 'Sin cambios: la fecha de la elección no va en el programa.',
 25: 'El 6.2 dice ahora que el presupuesto se presenta antes del 31 de octubre (Ley Orgánica, artículo 109), que el de 2028 lo presenta el gobierno que termina y que la partida del año 1 se crea con el artículo 119.',
 26: 'El cuadro 42 aclara que sus fechas son las de entrada, y que cuándo se aprueba cada ordenanza lo decide el Concejo.',
 27: 'El cuadro 43 suma una fila con cada plazo de otros y su plan mientras tanto.',
 28: 'El cuadro 43 suma una fila que dice de qué depende cada cosa sin fecha.',
 29: 'El calendario suma una fila: las dos rondas se repiten cada año en los mismos meses.',
 30: 'El calendario fecha la entrada de los grupos 3 y 4 en los meses 15 y 21.'}
lines = t.split('\n')
for i, l in enumerate(lines):
    m = re.match(r'^(\d+)\. \*\*', l)
    if m and int(m.group(1)) in R:
        lines[i] = l + ' **Resuelto:** ' + R[int(m.group(1))]
P.write_text('\n'.join(lines)); print('ok', sum(1 for l in lines if '**Resuelto:**' in l))
