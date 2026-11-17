"""Plan de despliegue, 17/11/2026, parte C: pasa a la fuente los textos que se habían corregido sólo en acciones.json
(huecos 13, 16 y 23) y marca la duración de C67."""
from pathlib import Path
P = Path(__file__).with_name('acciones_def.py')

# ---- textos que se habían corregido sólo en acciones.json (huecos 13, 16 y 23): pasan a la fuente
s = P.read_text()
def rep2(path, old, new):
    t = path.read_text(); assert t.count(old) == 1, (path.name, old[:60]); path.write_text(t.replace(old, new, 1))
rep2(P, 'act("G12", "Abre la oficina de delitos por internet, con pasantes de la tecnicatura como personal técnico",',
        'act("G12", "Abre la oficina de delitos por internet, junto al equipo técnico de las cámaras",')
rep2(P, '    note="Desde el mes 27, el personal técnico son egresados (cuadro 42).")',
        '    note="Su personal técnico sale de la tecnicatura: desde el mes 27, los egresados; hasta entonces la atiende el equipo técnico de las cámaras (cuadro 42).")')
rep2(P, '    note="Supuesto: la consecuencia rige desde que empiezan las grabaciones. El programa no dice desde cuándo rige.")',
        '    note="La consecuencia rige desde que el sistema de grabación sellada funciona en todas las inspecciones (Ordenanza 4, artículo 3).")')
rep2(P, 'act("C67", "Asamblea de Concejales y Mayores Contribuyentes por la Ordenanza 17", "Concejo Deliberante",\n    dur=11,',
        'act("C67", "Asamblea de Concejales y Mayores Contribuyentes por la Ordenanza 17", "Concejo Deliberante",\n    dur=11, durnote="Duración del programa: la Asamblea se cita dentro de los quince días de aprobada la ordenanza preparatoria.",')
X = P.with_name('pasos_extra.py')
SEM = 'porque los grupos de egresados crecen de a poco. Cuando el programa funciona completo, son diez por convocatoria (5.3).'
for c, n in (('E23', 3), ('E26', 5), ('E29', 5)):
    rep2(X, f'    "{c}": "Diez empresas por convocatoria cuando el programa funciona completo (5.3).",',
            f'    "{c}": "Nacen {n} empresas en esta convocatoria: 3, 3, 5 y 5 en el mandato, {SEM}",')
rep2(P, 'steps="Un año de incubación en las sedes', f'steps="Nacen 3 empresas en esta convocatoria: 3, 3, 5 y 5 en el mandato, {SEM} Un año de incubación en las sedes')
print('textos ok')
