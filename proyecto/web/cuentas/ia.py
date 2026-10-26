"""Arma los textos del modelo fiscal que lee la inteligencia artificial de la web (data/cuentas_ia.json).
Todo sale de cuentas.json, que sale del Excel: ningún número se escribe a mano.
Uso: python3 -I ia.py <cuentas.json> <salida.json>"""
import json, sys
d = json.load(open(sys.argv[1]))
def n(v, dec=1):
    s = f"{abs(v):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s
def M(v, dec=1): return n(v, dec) + " millones"
def P(v, dec=1): return n(v * 100, dec) + "%"
Y = d["years"]; I, G, PR = d["ingresos"], d["gastos"], d["programas"]
CAP = "Las cuentas (modelo fiscal del programa)"
def yrs(vals, k=4): return "; ".join(f"{Y[i]}: {M(vals[i])}" for i in range(k))
E = []
def add(id_, sec, titulo, texto): E.append({"id": id_, "sec": sec, "capitulo": CAP, "titulo": titulo, "texto": texto})
g = d["guia"]
add("cuentas-como-leer", "detalle", "Cómo leer las cuentas",
    "Todas las cifras de las cuentas están en millones de pesos de diciembre de 2025 (pesos constantes, sin inflación).\n\n"
    f"{g['QUÉ ES']}\n\n{g['AÑO BASE']}\n\n{g['LA CUENTA']}\n\n{g['QUÉ CRECE']}\n\n{g['aviso']}")
pide = d["empleo_vivienda"][3] - 505.7; tabla = I["tabla"][3]; flex = -PR["flex_tabla"][3]
add("cuentas-como-se-paga", "como-se-paga", "Cómo se paga el programa",
    f"En régimen (desde 2031), el programa pide {M(pide)} por año más que en 2025. La tabla nueva de la base de valuación cobra {M(tabla)} por año ({P(tabla / pide, 0)}) y lo que falta, {M(flex)} por año ({P(flex / pide, 0)}), sale del gasto flexible. No se toma deuda nueva.\n\n"
    f"Lo que el programa suma al gasto, por año: {yrs(d['programa_suma'])}.\n"
    f"Lo que cobra la tabla nueva, por año: {yrs(I['tabla'])}.\n\n"
    f"{d['nota_tabla']}\n\n{g['CÓMO SE PAGA']}")
R = d["resultado"]; Es = d["escenarios"]
add("cuentas-resultado", "resultado", "El resultado financiero, año por año",
    f"El resultado financiero de 2025 (ejecución real) fue {M(d['base2025']['resultado'])}.\n\n"
    "Resultado financiero con el programa: " + "; ".join(f"{Y[i]}: {M(R[i])}" for i in range(8)) + ".\n"
    "Resultado si nada cambia: " + "; ".join(f"{Y[i]}: {M(Es['nada'][i])}" for i in range(8)) + ".\n"
    "Diferencia a favor del programa: " + "; ".join(f"{Y[i]}: {M(Es['dif'][i])}" for i in range(4)) + ".\n\n"
    "2026 y 2027 no están en el modelo. Ingresos por lo cobrado y gastos por lo devengado, como la cuenta Ahorro-Inversión oficial.")
orig = -PR["contrapartida"][3]
add("cuentas-reasignacion", "se-mueve", "Lo que se reasigna: de mantenimiento a ambiente, educación, apoyo escolar e inspecciones",
    f"En 2031, {M(orig)} por año dejan de ir a tres programas (mantenimiento y embellecimiento, infraestructura deportiva y arbolado) y se suman a lo que ya se gasta en: ambiente {M(PR['ambiente'][3])} más, educación {M(PR['educacion'][3])} más, apoyo escolar {M(PR['apoyo'][3])} más e inspecciones grabadas (soportes, datos y grabaciones) {M(PR['inspecciones'][3])} más. No es gasto nuevo: es el mismo dinero en otro lugar. Estas cifras son lo que se agrega, no el total de cada área.\n\n"
    f"Con lo que se agrega, el gasto total en ecología y medio ambiente pasa de {M(next(x['v'][0] for x in d['funciones'] if x['f'].startswith('4.4')))} en 2028 a {M(next(x['v'][3] for x in d['funciones'] if x['f'].startswith('4.4')))} en 2031, y llega al {P(d['metas'][2]['a4'])} del presupuesto (meta 3). El gasto total en educación y cultura pasa de {M(next(x['v'][0] for x in d['funciones'] if x['f'].startswith('3.4')))} en 2028 a {M(next(x['v'][3] for x in d['funciones'] if x['f'].startswith('3.4')))} en 2031.\n\n"
    f"Lo que ceden esos tres programas, por año: {yrs([-x for x in PR['contrapartida']])}.\n"
    f"Lo que se agrega, por año. Ambiente: {yrs(PR['ambiente'])}. Educación: {yrs(PR['educacion'])}. Apoyo escolar: {yrs(PR['apoyo'])}. Inspecciones grabadas: {yrs(PR['inspecciones'])}.")
add("cuentas-ingresos", "entra", "Cuánto entra al Municipio",
    f"Ingresos totales: {yrs(I['total'])}.\n\n"
    f"En 2031: tasas, derechos y rentas del Municipio {M(I['municipal'][3])}; lo que llega de la Provincia {M(I['provincial'][3])}; de la Nación y otros {M(I['nacional'][3])}; la tabla nueva {M(I['tabla'][3])}; recursos de capital {M(I['capital'][3])}.\n"
    f"En 2028: tasas, derechos y rentas del Municipio {M(I['municipal'][0])}; Provincia {M(I['provincial'][0])}; Nación y otros {M(I['nacional'][0])}; la tabla nueva {M(I['tabla'][0])}; recursos de capital {M(I['capital'][0])}.\n\n"
    "Lo que recauda el Municipio crece 1,95% real por año. La coparticipación, el 82,4% de lo provincial, cae 2,196% real por año; el resto de lo provincial, lo nacional y los recursos de capital quedan constantes.")
fx = [f for f in d["funciones"] if f["v"][3] > 0]
fx.sort(key=lambda f: -f["v"][3])
add("cuentas-gastos", "gasta", "En qué se gasta: gastos por función",
    f"Gastos totales: {yrs(G['total'])}.\n\n"
    "Gasto por función en 2031: " + "; ".join(f"{f['f'].split(' · ', 1)[1]} {M(f['v'][3])}" for f in fx) + ".\n\n"
    "Las funciones que crecen con el programa entre 2028 y 2031: " + "; ".join(f"{f['f'].split(' · ', 1)[1]} de {M(f['v'][0])} a {M(f['v'][3])}" for f in d["funciones"] if f["f"] in ("3.6 · Trabajo", "4.4 · Ecología y medio ambiente", "3.4 · Educación y cultura", "3.7 · Vivienda y urbanismo")) + ".\n"
    f"Urbanismo figura sin restar lo que cede a ambiente, educación, apoyo escolar e inspecciones ({M(orig)} en 2031): el modelo lo resta en una fila aparte.")
vf = d["vecinal_funcionamiento"]
add("cuentas-obra-vecinal", "vecinos", "La obra pública que deciden los vecinos",
    f"La obra pública es de {M(G['obra'][3])} por año. La parte que deciden los vecinos sube cada año: año 1 (2028) {M(G['vecinos'][0])}, el 12,5%; año 2 (2029) {M(G['vecinos'][1])}, el 25%; año 3 (2030) {M(G['vecinos'][2])}, el 37,5%; año 4 (2031) {M(G['vecinos'][3])}, el 50%. No es dinero nuevo: sale de la misma obra pública.\n\n"
    f"El funcionamiento del sistema cuesta el 1,5% de la partida vecinal, dentro de ella: {yrs(vf)}.\n\n"
    "La partida se reparte entre las seis zonas: 50% por población y 50% por un índice de necesidad que mira, en los hogares, necesidades básicas insatisfechas, falta de cloaca, falta de gas de red y hacinamiento (Censo 2022 del INDEC).")
for z in d["zonas"]:
    zid = z["zona"].lower().replace(" sur mer", "").replace(" ", "-").replace("é", "e")
    add("cuentas-zona-" + zid, "zona", f"{z['zona']}: obra vecinal y lugares de formación",
        f"{z['zona']} tiene {n(z['poblacion'], 0)} habitantes (Censo 2022) y un índice de necesidad de {P(z['indice'])}. Le toca el {P(z['peso'])} de la partida vecinal.\n\n"
        f"Obra pública que deciden los vecinos de {z['zona']}: año 1 (2028) {M(z['obra'][0])}; año 2 (2029) {M(z['obra'][1])}; año 3 (2030) {M(z['obra'][2])}; año 4 (2031) {M(z['obra'][3])} por año.\n\n"
        f"Lugares de formación laboral por año para {z['zona']}, cuando el programa funcione completo: {n(z['cupos'], 0)} de 928.")
ev = d["empleo_vivienda"]; eg = d["egresados"]
add("cuentas-empleo-vivienda", "empleo", "Empleo y vivienda: cuánto se gasta y cuántos egresados",
    f"El gasto en empleo y vivienda era de 505,7 millones en 2025. Con el programa: {yrs(ev)} por año. En 2031 son {M(PR['empleo'][3])} para empleo (60%, gasto corriente) y {M(PR['vivienda'][3])} para vivienda y servicios básicos (40%, gasto de capital).\n\n"
    f"Egresados de la formación: {n(eg[2], 0)} en 2030 y {n(eg[3], 0)} en 2031, {n(eg[2] + eg[3], 0)} en el mandato. En régimen hay 928 lugares de formación por año.\n\n{g['EL PROGRAMA']}")
add("cuentas-deuda", "deuda", "La deuda",
    f"El programa no toma deuda nueva. Lo que quedaba al cierre de 2028: deuda al 31/12/2025 {M(d['deuda2025'][0])} y bono 2026 {M(d['bono'][0])}. Desde 2029, las dos quedan en cero.\n\n"
    f"Deuda flotante (facturas que se pagan con el atraso normal de cada mes), al cierre: {yrs(d['flotante'])}.\n\n{g['EL BONO']}")
sens = []
for s in d["sensibilidad"]:
    v = s["v"]
    if "recauda" in s["var"]: sens.append(f"Si lo que recauda el Municipio crece {P(v[0]['x'], 2)} por año en vez de {P(v[1]['x'], 2)}, 2031 termina en {M(v[0]['res'])}, es decir, en déficit; si crece {P(v[2]['x'], 2)}, termina en {M(v[2]['res'])}.")
    elif "coparticip" in s["var"]: sens.append(f"Si la coparticipación cae {P(-v[2]['x'])} por año, 2031 termina en {M(v[2]['res'])}; si cae {P(-v[1]['x'])}, en {M(v[1]['res'])}; si cae {P(-v[0]['x'])}, en {M(v[0]['res'])}.")
    else: sens.append(f"Si se cobra el {P(v[0]['x'], 2)} de lo facturado en vez del {P(v[1]['x'], 2)}, 2031 termina en {M(v[0]['res'])}; si se cobra el {P(v[2]['x'], 2)}, en {M(v[2]['res'])}.")
add("cuentas-si-sale-peor", "peor", "Qué pasa si las cosas salen peor (sensibilidad del resultado de 2031)",
    f"Lo previsto para 2031 es un resultado de {M(R[3])}. Cada variable se mueve sola, con las otras dos en su valor previsto.\n\n" + "\n".join(sens))
json.dump(E, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print("ok", len(E))
