# Arma REVISION.md a partir de acciones.json.
import json
import re
import sys
from collections import Counter

from cal import D, M, E, fecha_larga

SRC = sys.argv[1]
OUT = sys.argv[2]
d = json.load(open(SRC))
O = {o["code"]: o for o in d}


def f(iso):
    return fecha_larga(D.fromisoformat(iso))


def fd(iso):
    x = D.fromisoformat(iso)
    return f"{x.day:02d}/{x.month:02d}/{x.year}"


n = len(d)
hitos = sum(o["milestone"] for o in d)
crit = [o for o in d if o["critical"]]
casi = [o for o in d if 0 < o["float"] <= 5]
est = [o for o in d if not o["milestone"] and "Duración estimada" in o["note"]]
prog = [o for o in d if not o["milestone"] and "Duración del programa" in o["note"]]
fest = [o for o in d if "Fecha estimada" in o["note"] or "Supuesto" in o["note"]]
streams = Counter(o["stream"] for o in d)
start = min(o["start"] for o in d)
end = max(o["finish"] for o in d)

L = []
w = L.append

w("# Plan de despliegue «San Isidro 2027» · Revisión")
w("")
w("Datos del plan de despliegue del programa de gobierno, sacados del texto final (commit c462fcf). "
  "La página todavía no está armada. Este archivo explica cómo se armaron los datos de `acciones.json`, "
  "qué supuestos se tomaron, cuál es el camino crítico y qué huecos o contradicciones aparecieron en el programa.")
w("")
w("## 1. Qué hay en acciones.json")
w("")
w(f"- {n} acciones, de las cuales {hitos} son hitos (duración 0).")
w(f"- {len(crit)} acciones críticas y {len(casi)} casi críticas (holgura de 1 a 5 días hábiles).")
w(f"- Desde el {f(start)} (elección, fecha estimada) hasta el {f(end)} (fin del mandato).")
w("- Trece líneas de trabajo: «0 Transición» y las doce del pedido.")
w("- Los mismos campos del ejemplo (code, task, stream, owner, team, dur, start, finish, float, critical, milestone, "
  "decision, steps, moves, sne, needs, note), más «fuente». El campo «moves» va vacío.")
w("- En «steps» van los pasos o lo que hace falta. Cuando el programa lo dice, termina con «Cómo se comprueba», "
  "copiado de los cuadros 40, 41 y 42.")
w("- En «sne» va la fecha desde la que la acción puede empezar: el primer día de su mes en el calendario, o una fecha fija.")
w("")
w("| Línea de trabajo | Acciones |")
w("|---|---|")
for s in sorted(streams, key=lambda x: int(x.split()[0])):
    w(f"| {s} | {streams[s]} |")
w("")

w("## 2. Reglas del plan")
w("")
w("**Los meses del programa.** El mes n empieza el día 10 y termina el día 9 del mes siguiente. "
  "El mes 1 va del 10 de diciembre de 2027 al 9 de enero de 2028. "
  "El mes 3 va del 10 de febrero al 9 de marzo de 2028. "
  "El mes 12 va del 10 de noviembre al 9 de diciembre de 2028. "
  "El mes 48 va del 10 de noviembre al 9 de diciembre de 2031. "
  "Es la única regla que deja el 1 de marzo dentro del mes 3, como dice el calendario (cuadro 42). "
  "Con meses de calendario, el 1 de marzo caería en el mes 4. "
  "Se aplica igual a todo el plan.")
w("")
w("**Días hábiles.** Se cuentan de lunes a viernes. No se descuentan feriados nacionales, provinciales ni municipales. "
  "Tampoco se descuenta el receso del Concejo, salvo donde el programa lo nombra: las sesiones ordinarias abren el 1 de marzo (6.6). "
  "Por eso las ordenanzas que entran en diciembre se tratan desde el 1 de marzo.")
w("")
w("**Inicio y fin.** «start» es el primer día de trabajo. «finish» es el primer día hábil después del último día de trabajo, "
  "como en el ejemplo. Un hito tiene el mismo inicio y fin.")
w("")
w("**Dependencias.** «FS» quiere decir que la acción empieza cuando termina la anterior. "
  "«SS» quiere decir que empieza cuando empieza la otra. «lag» son días hábiles de espera.")
w("")
w("**Holgura y camino crítico.** La holgura («float») son los días hábiles que una acción se puede atrasar sin romper tres cosas: "
  "lo que destraba, el último día de su mes en el calendario del programa y el fin del mandato. "
  "Es el método del camino crítico, con los plazos del programa como fecha límite. "
  "Una acción es crítica si su holgura es cero. "
  "Las cuatro fechas fijas (elección, asunción, cien días y fin del mandato) tienen holgura cero.")
w("")
w("**La asunción.** El texto lo confirma: «El mandato empieza el 10 de diciembre de 2027» (6.1). "
  "Lo repiten «Qué proponemos hacer» y «Para cerrar».")
w("")
w("**Los cien días.** El texto dice que se cumplen el 19 de marzo de 2028 (6.1). Es domingo. "
  "En el plan, todo lo que exige ese hito termina a más tardar el viernes 17. "
  "Todo lo que el calendario pone en los meses 1 a 3 termina el 9 de marzo, diez días antes.")
w("")
w("**La elección.** El programa no da la fecha. "
  "La regla nacional es el cuarto domingo de octubre anterior al fin de los mandatos (Código Electoral Nacional, artículo 53): "
  "el 24 de octubre de 2027. "
  "A agosto de 2026, la Provincia todavía no había fijado su fecha ni decidido si separa su elección de la nacional. "
  "El plan supone que vota el mismo día que la Nación, y lo marca como fecha estimada. Fuentes consultadas:")
w("")
w("- Decreto 335/2025, que cita el artículo 53 del Código Electoral Nacional: https://www.argentina.gob.ar/normativa/nacional/norma-412945/texto")
w("- Letra P, 22 de agosto de 2026, «Buenos Aires 2027: hola PASO, chau desdoblamiento»: https://www.letrap.com.ar/politica/buenos-aires-2027-hola-paso-chau-desdoblamiento-n5426002")
w("- Aire de Santa Fe, 1 de agosto de 2026, «Elecciones 2027: qué provincias desdoblan y cuáles tienen fecha confirmada»: https://www.airedesantafe.com.ar/politica/elecciones-2027-que-provincias-desdoblan-y-cuales-tienen-fecha-confirmada-n665155")
w("")
w("**Nivel de detalle.** Los primeros 18 meses van acción por acción. Después, el plan usa bloques de seis meses o de un año: "
  "los años de la rampa, los grupos de la formación, los presupuestos anuales y las aperturas de la costa.")
w("")
w("**Responsables.** Siempre por cargo o por organismo, nunca por persona. "
  "En la transición, el responsable es el «Intendente electo». "
  "El anexo pide que un abogado especialista en municipios revise cada ordenanza antes de que entre al Concejo, "
  "y la nota de método lista lo que necesita su dictamen: por eso aparece como responsable de tres revisiones y un dictamen. "
  "Los equipos («team») son seis: Intendencia, Secretarías, Concejo, Vecinos, Equipo de la IA y Externos.")
w("")
w("**Áreas sin línea propia.** El pedido fija doce líneas. Estas áreas del programa se ubicaron así:")
w("")
w("- Niñez (centros de apoyo escolar) y la tecnicatura: 5 Empleo y formación. El profesor digital: 4 Inteligencia artificial del Municipio.")
w("- Personas mayores y discapacidad (los cien cuidadores a domicilio): 7 Salud.")
w("- Género (atención en cada zona, hogares y patrocinio): 8 Seguridad. Su partida propia: 3 Presupuesto y tasas.")
w("- Multas de tránsito: 8 Seguridad, como seguridad vial.")
w("- Empleados del Municipio (atención los siete días y teléfono propio): 11 Habilitaciones e inspecciones.")
w("- Recolección de residuos, ruido y ambiente: 9 Costa y espacio público.")
w("- Excepciones urbanísticas: 6 Vivienda, porque el 15% de la valorización va a vivienda.")
w("- Fondo Educativo, pedidos de informes y gasto por zona: 12 Transparencia.")
w("- El hito de los cien días y el fin del mandato: 1 Mecanismo vecinal y obra pública.")
w("")
w("**Fuente.** El campo «fuente» lleva el apartado del programa: «6.4», «5.5», «4.11». "
  "Para el anexo usa «anexo.N» (N es el número de la ordenanza) o «anexo» para las reglas generales. "
  "«nota de método» es la lista de lo que tiene que confirmar un abogado.")
w("")
w("**Metas sin fecha.** Las veinte metas del cuadro 41 están todas en el plan. "
  "Las que el calendario fecha van en su mes. Las demás van en el mes 48, porque son metas de los cuatro años.")
w("")
w("**Riesgos.** Del 6.6 entran los riesgos que tienen una acción que los reduce. "
  "Cada una lo dice en su nota («Riesgo del 6.6: …»). "
  "Los riesgos sin acción propia (la recaudación, la coparticipación, la tasa del bono, la reforma de la Ley Orgánica) no generan acciones.")
w("")

w("## 3. Supuestos de duración")
w("")
w("Toda duración que el programa no da es un supuesto. Cada una dice «Duración estimada» en su nota. "
  "Las que el programa sí da dicen «Duración del programa». "
  "Para el tratamiento de cada ordenanza se usaron 22 días hábiles: es lo que tardó la única reforma de las reglas de urbanismo "
  "que pasó por el Concejo (Ordenanza 9432, citada en el 5.5).")
w("")
w(f"### 3.1 Duraciones que da el programa ({len(prog)})")
w("")
w("| Código | Acción | Días hábiles | Base |")
w("|---|---|---|---|")
for o in sorted(prog, key=lambda o: o["code"]):
    base = re.search(r"Duración del programa: ([^.]*)\.", o["note"]).group(1)
    w(f"| {o['code']} | {o['task']} | {o['dur']} | {base} |")
w("")
w(f"### 3.2 Duraciones estimadas ({len(est)})")
w("")
w("| Código | Acción | Días hábiles | Base |")
w("|---|---|---|---|")
for o in sorted(est, key=lambda o: o["code"]):
    m = re.search(r"Duración estimada: ([^.]*)\.", o["note"])
    base = m.group(1) if m else "estimación propia"
    if "Ordenanza 9432" in o["note"]:
        base = "precedente de la Ordenanza 9432"
    w(f"| {o['code']} | {o['task']} | {o['dur']} | {base} |")
w("")
w(f"### 3.3 Fechas estimadas y otros supuestos ({len(fest)})")
w("")
w("Acciones cuya fecha o cuyo orden no sale del texto. El motivo está en la nota de cada una.")
w("")
w("| Código | Acción | Fecha en el plan |")
w("|---|---|---|")
for o in sorted(fest, key=lambda o: o["code"]):
    w(f"| {o['code']} | {o['task']} | {fd(o['start'])} |")
w("")

w("## 4. Camino crítico")
w("")
w("Las acciones críticas no se pueden atrasar ni un día hábil sin romper una fecha del programa.")
w("")
w("| Código | Acción | Inicio | Fin |")
w("|---|---|---|---|")
for o in sorted(crit, key=lambda o: (o["start"], o["code"])):
    w(f"| {o['code']} | {o['task']} | {fd(o['start'])} | {fd(o['finish'])} |")
w("")
w("Cómo se lee:")
w("")
w("- La columna vertebral es la rampa de la obra vecinal desde el año 2: M15, M17, M18, M19, M20 y M21, hasta el fin del mandato (M23). "
  "Cada año de la rampa dura lo que dice el programa, un año, y el siguiente empieza el día después. "
  "Si un año se atrasa, el 50% no llega al mes 48. Con la rampa también queda crítica la meta de las cloacas en Boulogne y Béccar (V03).")
w("- Antes del año 2 no hay acciones críticas en la rampa. El año 1 (M11) tiene unos 20 días hábiles de margen antes del mes 13.")
w("- La prueba a ciegas del profesor digital (I07) es crítica porque dura un mes y el calendario le da exactamente el mes 3.")
w("- Las dos ordenanzas de las multas (C18 y C21) son críticas porque el programa las fija el 1 de marzo de 2028.")
w("- La elección (T01), la asunción (T07), los cien días (M22) y el fin del mandato (M23) son fechas fijas.")
w("")
w("Casi críticas (holgura de 1 a 5 días hábiles). Casi todas caen en los primeros cien días:")
w("")
w("| Código | Acción | Holgura | Inicio |")
w("|---|---|---|---|")
for o in sorted(casi, key=lambda o: (o["float"], o["start"])):
    w(f"| {o['code']} | {o['task']} | {o['float']} | {fd(o['start'])} |")
w("")
w("- La sesión extraordinaria de diciembre tiene un día de margen: convocatoria, entrada de los proyectos y voto de la ordenanza preparatoria antes del 22 de diciembre. "
  "Si el aviso de la asamblea se cuenta en días hábiles y no corridos, el margen de la asamblea baja de tres días a uno.")
w("- La inteligencia artificial del Municipio tiene cuatro días de margen para estar en el mes 3. "
  "De ella dependen, además del compromiso 14, otros cuatro compromisos de los cien días: G02, U02, H07 y X02.")
w("- Los presupuestos 2030 y 2031 tienen un día de margen, porque se votan entre el cierre de un año de la rampa y el inicio del siguiente.")
w("")
HUECOS = open("huecos.md").read()
w(HUECOS.strip())
w("")
w("## 6. Validaciones hechas")
w("")
w("- Sin ciclos: el orden de las dependencias se recorre de punta a punta.")
w("- Cada código de «needs» existe.")
w("- Ninguna acción empieza antes de lo que necesita (fin de la anterior para «FS», inicio para «SS», más los días de espera).")
w("- Cada acción con mes en el calendario cae dentro de su mes: empieza el primer día del mes o después, y su último día de trabajo cae el último día del mes o antes.")
w("- La holgura no es negativa en ninguna acción: todo entra en las fechas del programa con las duraciones supuestas.")
w("- Los hitos tienen duración 0. Inicio, fin y duración cuadran en días hábiles.")
w("- Hay trece líneas de trabajo con los nombres del pedido.")
w("- Ninguna oración de los textos empieza con «Y» ni con «Que».")
w("- Toda duración dice si es del programa o estimada.")
w("- El pedido a la Provincia de la Ordenanza 14 (K29) cae dentro de los 180 días de su aprobación.")
w("")

txt = "\n".join(L) + "\n"
bad = []
for line in txt.splitlines():
    for sent in re.split(r"(?<=[.!?])\s+", line.strip("-| *")):
        first = sent.strip().split(" ")[0] if sent.strip() else ""
        if first in ("Y", "Que"):
            bad.append(sent[:80])
open(OUT, "w").write(txt)
print("REVISION escrita", len(txt), "caracteres; oraciones con Y/Que:", bad)
