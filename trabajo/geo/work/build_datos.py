# -*- coding: utf-8 -*-
"""Arma web/data/zonas_datos.json con las cifras por zona que da el programa final (c462fcf).

Cada cifra lleva "como_figura": el texto exacto con que aparece en el programa. Antes de escribir,
el script comprueba que cada uno de esos textos esté en el texto del PDF de pantalla final
(v21/pj.txt, idéntico a salida/PROGRAMA_SAN_ISIDRO_2027.pdf de c462fcf). Si falta alguno, no escribe.

Uso: python3 -I build_datos.py <pj.txt> <final.txt> <salida.json>
"""
import json, re, sys

PJ, HTMLTXT, SALIDA = sys.argv[1], sys.argv[2], sys.argv[3]
# el texto del PDF de pantalla (trae lo que dicen los graficos) y el texto de las paginas HTML del
# programa (doc/content*.py de c462fcf), que no corta las frases en los saltos de pagina
TXT = re.sub(r"\s+", " ", open(PJ, encoding="utf-8").read()) + " || " + \
      re.sub(r"\s+", " ", open(HTMLTXT, encoding="utf-8").read())
FALTAN = []


def c(valor, como, fuente, unidad=None, nota=None, contexto=None):
    """Una cifra. `como` es el texto exacto del programa; `contexto` (opcional) es una frase
    más larga del programa que la contiene y que también se comprueba."""
    for t in [como] + ([contexto] if contexto else []):
        if re.sub(r"\s+", " ", t) not in TXT:
            FALTAN.append(t)
    d = {"valor": valor, "como_figura": como, "fuente": fuente}
    if unidad:
        d["unidad"] = unidad
    if nota:
        d["nota"] = nota
    return d


G1, G2, G3 = "1.1 · Gráfico 1", "1.1 · Gráfico 2", "1.1 · Gráfico 3"
C17, C21, C22, G23 = "3.5 · Cuadro 17", "4.3 · Cuadro 21", "4.4 · Cuadro 22", "4.4 · Gráfico 23"
NOTA3, NOTA4 = "Nota de método · Capítulo 3 (Cuadro 17)", "Nota de método · Capítulo 4"

U_POB = "personas en viviendas particulares (Censo 2022)"
U_PCT_HOG = "% de los hogares de la zona"
U_HOG = "hogares"
U_PARTE = "% del total de San Isidro"


def zona(nombre, otros_nombres, pob, nbi, clo, gas, hac, uni, h_nbi, h_clo, h_gas, h_hac, indice,
         monto, porhab, formacion, tabla, prov, recon, parte_hoy, parte_nueva, variacion, secciones):
    z = {"nombre": nombre, "nombres_en_programa": otros_nombres, "cifras": {}}
    k = z["cifras"]
    k["poblacion"] = c(pob[0], pob[1], G2, U_POB,
                       "Base de todos los datos por zona: las 295.978 personas en viviendas particulares (1.1).")
    k["pct_hogares_nbi"] = c(nbi[0], nbi[1], "1.1 · Gráficos 1 y 2", U_PCT_HOG,
                             "NBI: necesidades básicas insatisfechas.")
    k["pct_hogares_sin_cloaca"] = c(clo[0], clo[1], G2, U_PCT_HOG)
    k["pct_hogares_sin_gas_de_red"] = c(gas[0], gas[1], G2, U_PCT_HOG)
    k["pct_hogares_con_hacinamiento"] = c(hac[0], hac[1], G2, U_PCT_HOG)
    k["pct_personas_con_universidad_terminada"] = c(uni[0], uni[1], G3, "% de las personas de la zona")
    k["hogares_nbi"] = c(h_nbi[0], h_nbi[1], C22, U_HOG)
    k["hogares_nbi_parte_del_total"] = c(h_nbi[2], h_nbi[3], C22, U_PARTE)
    k["hogares_sin_cloaca"] = c(h_clo[0], h_clo[1], C22, U_HOG)
    k["hogares_sin_cloaca_parte_del_total"] = c(h_clo[2], h_clo[3], C22, U_PARTE)
    k["hogares_sin_gas_de_red"] = c(h_gas[0], h_gas[1], C22, U_HOG)
    k["hogares_sin_gas_de_red_parte_del_total"] = c(h_gas[2], h_gas[3], C22, U_PARTE)
    k["hogares_con_hacinamiento"] = c(h_hac[0], h_hac[1], C22, U_HOG)
    k["hogares_con_hacinamiento_parte_del_total"] = c(h_hac[2], h_hac[3], C22, U_PARTE)
    k["indice_de_necesidad"] = c(indice[0], indice[1], C22, "% (promedio de las cuatro partes)",
                                 "Con este índice se reparte la mitad del dinero de obra que deciden los vecinos.")
    k["obra_vecinal_anio4_monto"] = c(monto[0], monto[1], G23, "millones de pesos por año (pesos de diciembre de 2025)",
                                      "Reparto de los 28.908 millones del cuarto año: mitad por población y mitad por el índice de necesidad.")
    k["obra_vecinal_anio4_por_habitante"] = c(porhab[0], porhab[1], G23, "pesos por habitante por año (pesos de diciembre de 2025)")
    k["formacion_lugares_por_anio"] = c(formacion[0], formacion[1], "5.3", "lugares por año",
                                        "Los 928 lugares de formación laboral, repartidos con el índice de necesidad.",
                                        contexto=formacion[2])
    k["tierra_veces_boulogne_tabla_municipal"] = c(tabla[0], tabla[1], C17, "veces el valor de Boulogne Sur Mer (tabla municipal de 2008)")
    k["tierra_veces_boulogne_valuacion_provincial"] = c(prov[0], prov[1], C17, "veces el valor de Boulogne Sur Mer (valuación de ARBA)")
    if recon:
        k["tierra_reconocido"] = c(recon[0], recon[1], C17, "% (tabla municipal / valuación provincial)",
                                   "Menos de 100%: la tabla de 2008 cobra de menos.")
    k["tierra_parte_del_total_hoy"] = c(parte_hoy[0], parte_hoy[1], "3.5", "% de lo que se cobra por la tierra",
                                        contexto=parte_hoy[2])
    k["tierra_parte_del_total_con_tabla_nueva"] = c(parte_nueva[0], parte_nueva[1], "3.5", "% de lo que se cobra por la tierra",
                                                    contexto=parte_hoy[2])
    k["tierra_variacion_de_lo_que_paga"] = c(variacion[0], variacion[1], "3.5", "% (cambio de lo que paga la localidad por la tierra con la tabla nueva)",
                                             variacion[3] if len(variacion) > 3 else None, contexto=variacion[2])
    k["secciones_catastrales"] = c(secciones[0], secciones[1], NOTA3, "circunscripciones y secciones del catastro donde está la mayor parte de la localidad")
    return z


ZONAS = {}

ZONAS["boulogne"] = zona(
    "Boulogne Sur Mer", ["Boulogne Sur Mer", "Boulogne"],
    (74832, "74.832 hab."), (5.09, "5,09%"), (9.16, "9,16"), (27.64, "27,64"), (12.42, "12,42"), (9.0, "9,0%"),
    (1280, "1.280", 36.6, "1.280 (36,6%)"), (2295, "2.295", 35.4, "2.295 (35,4%)"),
    (6947, "6.947", 27.6, "6.947 (27,6%)"), (3121, "3.121", 36.4, "3.121 (36,4%)"), (34.0, "34,0%"),
    (8569, "8.569 M al año"), (114508, "114.508"),
    (315, "315 en Boulogne", "Son 315 en Boulogne, 307 en Béccar, 98 en Martínez, 96 en San Isidro, 94 en Villa Adelina y 18 en Acassuso."),
    (1, "1×"), (1, "1×"), None,
    (16.8, "16,8%", "Villa Adelina baja del 6,3% al 3,8%, y Boulogne del 16,8% al 14,5%."),
    (14.5, "14,5%"),
    (-4.5, "4,5% menos", "Villa Adelina paga 33,8% menos por la tierra, y Boulogne, 4,5% menos."),
    ("V-A, V-C, V-E y VI-A a VI-J", "Boulogne Sur Mer: V-A, V-C, V-E y VI-A a VI-J"))

ZONAS["beccar"] = zona(
    "Béccar", ["Béccar"],
    (63719, "63.719 hab."), (4.93, "4,93%"), (10.59, "10,59"), (37.27, "37,27"), (12.67, "12,67"), (12.8, "12,8%"),
    (1088, "1.088", 31.1, "1.088 (31,1%)"), (2321, "2.321", 35.8, "2.321 (35,8%)"),
    (8221, "8.221", 32.7, "8.221 (32,7%)"), (2794, "2.794", 32.6, "2.794 (32,6%)"), (33.0, "33,0%"),
    (7887, "7.887 M al año"), (123782, "123.782"),
    (307, "307 en Béccar", "Son 315 en Boulogne, 307 en Béccar, 98 en Martínez, 96 en San Isidro, 94 en Villa Adelina y 18 en Acassuso."),
    (1.21, "1,21×"), (1.27, "1,27×"), (95, "95%"),
    (15.1, "15,1%", "Béccar pasa del 15,1% al 13,6%."),
    (13.6, "13,6%"),
    (0, "Béccar paga lo mismo que hoy", "Béccar paga lo mismo que hoy.", "El programa dice «paga lo mismo que hoy»; el 0 es esa frase."),
    ("VII-A, VII-B, VII-E a VII-G y VIII-A a VIII-E", "Béccar: VII-A, VII-B, VII-E a VII-G y VIII-A a VIII-E"))

ZONAS["villa_adelina"] = zona(
    "Villa Adelina", ["Villa Adelina"],
    (35542, "35.542 hab."), (2.73, "2,73%"), (5.54, "5,54"), (15.59, "15,59"), (7.28, "7,28"), (9.3, "9,3%"),
    (356, "356", 10.2, "356 (10,2%)"), (722, "722", 11.1, "722 (11,1%)"),
    (2034, "2.034", 8.1, "2.034 (8,1%)"), (950, "950", 11.1, "950 (11,1%)"), (10.1, "10,1%"),
    (3198, "3.198 M al año"), (89987, "89.987"),
    (94, "94 en Villa Adelina", "Son 315 en Boulogne, 307 en Béccar, 98 en Martínez, 96 en San Isidro, 94 en Villa Adelina y 18 en Acassuso."),
    (0.96, "0,96×"), (0.67, "0,67×"), (144, "144%"),
    (6.3, "6,3%", "Villa Adelina baja del 6,3% al 3,8%, y Boulogne del 16,8% al 14,5%."),
    (3.8, "3,8%"),
    (-33.8, "33,8% menos", "Villa Adelina paga 33,8% menos por la tierra, y Boulogne, 4,5% menos."),
    ("V-B, V-D, V-F y V-G", "Villa Adelina: V-B, V-D, V-F y V-G"))

ZONAS["san_isidro"] = zona(
    "San Isidro", ["San Isidro", "localidad de San Isidro", "Localidad de San Isidro", "ciudad de San Isidro"],
    (45872, "45.872 hab."), (1.83, "1,83%"), (2.97, "2,97"), (16.64, "16,64"), (4.18, "4,18"), (25.2, "25,2%"),
    (354, "354", 10.1, "354 (10,1%)"), (574, "574", 8.8, "574 (8,8%)"),
    (3221, "3.221", 12.8, "3.221 (12,8%)"), (809, "809", 9.4, "809 (9,4%)"), (10.3, "10,3%"),
    (3729, "3.729 M al año"), (81297, "81.297"),
    (96, "96 en San Isidro", "Son 315 en Boulogne, 307 en Béccar, 98 en Martínez, 96 en San Isidro, 94 en Villa Adelina y 18 en Acassuso."),
    (1.61, "1,61×"), (2.16, "2,16×"), (75, "75%"),
    (28.7, "28,7%", "La localidad de San Isidro pasa del 28,7% de ese total al 33,2%."),
    (33.2, "33,2%"),
    (28, "28%", "La que más sube es la localidad de San Isidro, que es el centro del municipio: 28%."),
    ("I-A, I-B, II-A a II-C, III-K, IV-E, VII-C, VII-D y VII-H",
     "Localidad de San Isidro: I-A, I-B, II-A a II-C, III-K, IV-E, VII-C, VII-D y VII-H"))

ZONAS["martinez"] = zona(
    "Martínez", ["Martínez"],
    (64978, "64.978 hab."), (1.43, "1,43%"), (1.81, "1,81"), (14.55, "14,55"), (2.96, "2,96"), (24.4, "24,4%"),
    (374, "374", 10.7, "374 (10,7%)"), (474, "474", 7.3, "474 (7,3%)"),
    (3806, "3.806", 15.1, "3.806 (15,1%)"), (775, "775", 9.0, "775 (9,0%)"), (10.5, "10,5%"),
    (4697, "4.697 M al año"), (72285, "72.285"),
    (98, "98 en Martínez", "Son 315 en Boulogne, 307 en Béccar, 98 en Martínez, 96 en San Isidro, 94 en Villa Adelina y 18 en Acassuso."),
    (1.75, "1,75×"), (2.16, "2,16×"), (81, "81%"),
    (25.7, "25,7%", "Martínez pasa del 25,7% al 27,3%, y Acassuso del 7,3% al 7,6%."),
    (27.3, "27,3%"),
    (17.8, "17,8%", "Martínez sube 17,8% y Acassuso, 15,6%."),
    ("III-B, III-D a III-J y IV-A a IV-D", "Martínez: III-B, III-D a III-J y IV-A a IV-D"))

ZONAS["acassuso"] = zona(
    "Acassuso", ["Acassuso"],
    (11035, "11.035 hab."), (0.94, "0,94%"), (2.12, "2,12"), (19.48, "19,48"), (2.50, "2,50"), (32.3, "32,3%"),
    (45, "45", 1.3, "45 (1,3%)"), (102, "102", 1.6, "102 (1,6%)"),
    (936, "936", 3.7, "936 (3,7%)"), (120, "120", 1.4, "120 (1,4%)"), (2.0, "2,0%"),
    (827, "827 M al año"), (74962, "74.962"),
    (18, "18 en Acassuso", "Son 315 en Boulogne, 307 en Béccar, 98 en Martínez, 96 en San Isidro, 94 en Villa Adelina y 18 en Acassuso."),
    (2.32, "2,32×"), (2.80, "2,80×"), (83, "83%"),
    (7.3, "7,3%", "Martínez pasa del 25,7% al 27,3%, y Acassuso del 7,3% al 7,6%."),
    (7.6, "7,6%"),
    (15.6, "15,6%", "Martínez sube 17,8% y Acassuso, 15,6%."),
    ("III-A y III-C", "Acassuso: III-A y III-C"))

for zid in ("beccar", "san_isidro"):
    ZONAS[zid]["cifras"]["pct_personas_con_universidad_terminada"]["nota"] = (
        "Cifra tal como la muestra el Gráfico 3, que redondea dos veces (a dos decimales y después a uno); "
        "ver GEO_INFORME.md. Se deja la del programa.")

# ---- cifras que el programa da sólo para algunas zonas --------------------------------------------
E = "5.13"
ZONAS["beccar"]["cifras"]["pct_personas_hasta_14_anios"] = c(
    21.0, "21,0%", E, "% de las personas de la zona",
    "El texto dice «menos de 14 años»; el promedio de San Isidro que da el 5.13 es «hasta los 14 años».",
    contexto="Los chicos están sobre todo en Béccar, donde el 21,0% tiene menos de 14 años, y en Boulogne, con el 18,7%.")
ZONAS["boulogne"]["cifras"]["pct_personas_hasta_14_anios"] = c(
    18.7, "18,7%", E, "% de las personas de la zona",
    contexto="Los chicos están sobre todo en Béccar, donde el 21,0% tiene menos de 14 años, y en Boulogne, con el 18,7%.")
ZONAS["acassuso"]["cifras"]["pct_personas_65_y_mas"] = c(
    22.5, "22,5%", E, "% de las personas de la zona",
    contexto="Las personas mayores están sobre todo en Acassuso, con el 22,5%, y en Martínez, con el 22,4%.")
ZONAS["martinez"]["cifras"]["pct_personas_65_y_mas"] = c(
    22.4, "22,4%", E, "% de las personas de la zona",
    contexto="Las personas mayores están sobre todo en Acassuso, con el 22,5%, y en Martínez, con el 22,4%.")

U = "5.5"
DEC = "De los 73 decretos con inmueble identificado, el 28,8% es en Martínez, el 27,4% en la ciudad de San Isidro y el 19,2% en Boulogne."
ZONAS["martinez"]["cifras"]["pct_decretos_urbanisticos"] = c(28.8, "28,8%", U, "% de los 73 decretos de urbanismo con inmueble identificado (feb. 2024 a sep. 2026)", contexto=DEC)
ZONAS["san_isidro"]["cifras"]["pct_decretos_urbanisticos"] = c(27.4, "27,4%", U, "% de los 73 decretos de urbanismo con inmueble identificado (feb. 2024 a sep. 2026)", contexto=DEC)
ZONAS["boulogne"]["cifras"]["pct_decretos_urbanisticos"] = c(19.2, "19,2%", U, "% de los 73 decretos de urbanismo con inmueble identificado (feb. 2024 a sep. 2026)", contexto=DEC)
ZONAS["villa_adelina"]["cifras"]["decretos_urbanisticos"] = c(3, "Villa Adelina tiene tres en dos años y medio", U, "decretos de urbanismo en dos años y medio",
                                                             contexto="En cambio, Villa Adelina tiene tres en dos años y medio.")

ZONAS["boulogne"]["cifras"]["tierra_rebaja_que_no_llega_si_no_se_ajusta_el_minimo"] = c(
    410, "410 en Boulogne", "3.5", "millones de pesos por año", "Sólo la tierra; parte de los 789 millones del partido.",
    contexto="789 millones de rebaja no llegarían a los vecinos: 410 en Boulogne, 241 en Villa Adelina y 124 en Béccar.")
ZONAS["villa_adelina"]["cifras"]["tierra_rebaja_que_no_llega_si_no_se_ajusta_el_minimo"] = c(
    241, "241 en Villa Adelina", "3.5", "millones de pesos por año", "Sólo la tierra; parte de los 789 millones del partido.")
ZONAS["beccar"]["cifras"]["tierra_rebaja_que_no_llega_si_no_se_ajusta_el_minimo"] = c(
    124, "124 en Béccar", "3.5", "millones de pesos por año", "Sólo la tierra; parte de los 789 millones del partido.")

for zid in ("villa_adelina", "san_isidro", "martinez", "acassuso"):
    ZONAS[zid]["cifras"]["espacios_de_apoyo_escolar_hoy"] = c(
        0, "En las otras cuatro localidades no hay ninguno", "5.8 · Cuadro 41", "espacios",
        "Hoy hay cinco espacios pequeños, todos en Béccar y Boulogne (ver «grupos»).")

ZONAS["acassuso"]["cifras"]["radios_censales"] = c(16, "Sus dieciséis radios", NOTA4, "radios censales",
                                                   contexto="Sus dieciséis radios tienen NBI de 0,0% a 2,4%")

# ---- datos de radios o barrios dentro de una zona (no son promedios de zona) ---------------------
ZONAS["beccar"]["dentro_de_la_zona"] = [
    {"que": "Fracción censal 32 (nueve radios pegados; coincide con el barrio La Cava)",
     "cifras": {
         "radios": c(9, "9 radios", "4.4 · Gráfico 24", "radios censales"),
         "habitantes": c(8749, "8.749 hab", "4.4 · Gráfico 24", "personas",
                         contexto="Esos nueve radios tienen 8.749 habitantes y el peor NBI de San Isidro."),
         "superficie_km2": c(0.28, "0,28 km²", "5.3", "km²", contexto="Esa zona mide 0,28 km²."),
         "distancia_al_centro_del_barrio_m": c(136, "136 metros", "5.3", "metros",
                                               "Distancia entre el punto central de La Cava en OpenStreetMap y el centro de la zona del capítulo 4."),
     },
     "texto": "el peor NBI del partido"},
    {"que": "Centro de Formación Laboral Nº 404 Barrio La Cava: hoy, la única sede de formación laboral",
     "cifras": {"sedes_de_formacion_laboral_hoy": c(1, "Hoy hay una sola sede de formación laboral, la del Barrio La Cava", "6.3 · Cuadro 41", "sedes")}},
]
ZONAS["boulogne"]["dentro_de_la_zona"] = [
    {"que": "Radio censal 067562205",
     "cifras": {
         "pct_hogares_nbi": c(13.7, "13,7%", "5.8", U_PCT_HOG.replace("zona", "radio"),
                              contexto="En un sector chico de Boulogne, que el censo identifica como radio 067562205, el 13,7% de los hogares tiene necesidades básicas insatisfechas."),
         "pct_cocina_sin_gas_de_red": c(95.8, "95,8%", "5.8", "% de los hogares del radio",
                                        contexto="el 95,8% cocina sin gas de red"),
     }},
    {"que": "Tomógrafos que el Municipio va a tener propios: uno es el de Boulogne (el otro, el del Central)",
     "cifras": {"tomografos": c(1, "el de Boulogne", "5.6", "tomógrafo",
                                contexto="Proponemos que los dos tomógrafos, el del Central y el de Boulogne, sean del Municipio.")}},
]
ZONAS["san_isidro"]["dentro_de_la_zona"] = [
    {"que": "Franja baja de la costa: tres radios vecinos de la fracción 02 (terminados en 03, 04 y 05)",
     "cifras": {
         "radios": c(3, "Hay tres radios vecinos de la fracción 02", NOTA4, "radios censales"),
         "pct_hogares_nbi_rango": c([4.3, 11.8], "entre 4,3% y 11,8%", NOTA4, "% de los hogares de cada radio (mínimo y máximo)"),
         "pct_hogares_sin_gas_de_red_rango": c([24.8, 63.1], "entre 24,8% y 63,1%", NOTA4, "% de los hogares de cada radio (mínimo y máximo)"),
     },
     "texto": "Las carencias de la franja baja de la costa se cuentan en la zona San Isidro."},
    {"que": "Dirección de género: su única sede está en la ciudad de San Isidro",
     "cifras": {"sedes": c(1, "una sola sede, en la ciudad de San Isidro", "5.13", "sede")}},
]
ZONAS["acassuso"]["dentro_de_la_zona"] = [
    {"que": "Los dieciséis radios de Acassuso",
     "cifras": {"pct_hogares_nbi_rango": c([0.0, 2.4], "NBI de 0,0% a 2,4%", NOTA4, "% de los hogares de cada radio (mínimo y máximo)")},
     "texto": "En Acassuso no hay un bolsón de pobreza."},
    {"que": "Radio censal 067560403, el único donde pesa la falta de cloaca",
     "cifras": {
         "pct_hogares_sin_cloaca": c(17.4, "17,4% sobre 316 hogares", NOTA4, "% de los hogares del radio"),
         "hogares": c(316, "316 hogares", NOTA4, "hogares"),
         "pct_hogares_nbi": c(0.6, "0,6% de NBI", NOTA4, "% de los hogares del radio"),
     }},
    {"que": "Formación laboral: la sede de Acassuso va a ir rotando (sede móvil)",
     "cifras": {"sedes_fijas": c(0, "en Acassuso la sede va a ir rotando", "5.3", "sedes fijas",
                                 "Cinco sedes fijas en las otras localidades y una móvil en Acassuso.")}},
]

# ---- el partido entero ------------------------------------------------------------------------------
SAN_ISIDRO = {
    "nombre": "Partido de San Isidro",
    "cifras": {
        "poblacion_total": c(297282, "297.282 habitantes", "1.1", "personas (Censo 2022)"),
        "poblacion_en_viviendas_particulares": c(295978, "295.978 personas", "1.1", U_POB,
                                                 "Suma de las seis zonas; base de todos los datos por zona."),
        "poblacion_en_viviendas_colectivas": c(1304, "1.304 personas", "1.1", "personas (no se pueden asignar a una zona)"),
        "hogares": c(110559, "110.559 hogares", "1.1", U_HOG),
        "radios_censales": c(360, "360 radios censales", "1.1 · Gráfico 1 (nota)", "radios"),
        "fracciones_censales": c(35, "San Isidro tiene 35 fracciones", "Glosario", "fracciones"),
        "pct_hogares_nbi": c(3.16, "3,16%", "1.1 · Gráficos 1 y 2", "% de los hogares (promedio de San Isidro)"),
        "hogares_nbi": c(3497, "3.497", C22, U_HOG),
        "hogares_sin_cloaca": c(6488, "6.488", C22, U_HOG),
        "hogares_sin_gas_de_red": c(25165, "25.165", C22, U_HOG),
        "hogares_con_hacinamiento": c(8569, "8.569", C22, U_HOG),
        "personas_hasta_14_anios": c(51388, "51.388 personas", E, "personas"),
        "pct_personas_hasta_14_anios": c(17.4, "17,4%", E, "% de las personas (promedio de San Isidro)",
                                        contexto="Hasta los 14 años hay 51.388 personas, el 17,4%."),
        "personas_65_y_mas": c(52769, "52.769", E, "personas"),
        "pct_personas_65_y_mas": c(17.8, "17,8%", E, "% de las personas (promedio de San Isidro)",
                                  contexto="De 65 años para arriba hay 52.769, el 17,8%."),
        "chicos_en_hogares_nbi": c(1810, "1.810 chicos", E, "chicos"),
        "obra_publica_2025": c(57816, "57.816 millones", "4.3", "millones de pesos (base de la partida vecinal)"),
        "obra_vecinal_anio1_monto": c(7227, "7.227 M", C21, "millones de pesos por año", "12,5% de la obra pública de 2025."),
        "obra_vecinal_anio1_por_habitante": c(24310, "24.310 $", C21, "pesos por habitante por año"),
        "obra_vecinal_anio2_monto": c(14454, "14.454 M", C21, "millones de pesos por año", "25,0% de la obra pública."),
        "obra_vecinal_anio2_por_habitante": c(48620, "48.620 $", C21, "pesos por habitante por año"),
        "obra_vecinal_anio3_monto": c(21681, "21.681 M", C21, "millones de pesos por año", "37,5% de la obra pública."),
        "obra_vecinal_anio3_por_habitante": c(72930, "72.930 $", C21, "pesos por habitante por año"),
        "obra_vecinal_anio4_monto": c(28908, "28.908 M", C21, "millones de pesos por año", "50,0% de la obra pública."),
        "obra_vecinal_anio4_por_habitante": c(97241, "97.241 $", C21, "pesos por habitante por año"),
        "funcionamiento_comisiones_1_5_pct_anio1": c(108.4, "108,4 millones", "3.4 y 4.6", "millones de pesos (todas las zonas juntas)"),
        "funcionamiento_comisiones_1_5_pct_anio4": c(433.6, "433,6 millones", "3.4 y 4.6", "millones de pesos (todas las zonas juntas)"),
        "formacion_lugares_por_anio": c(928, "928 alumnos por año", "5.3 · Cuadro 31", "lugares por año"),
        "decretos_urbanisticos_con_inmueble": c(73, "73 decretos", U, "decretos (feb. 2024 a sep. 2026)"),
        "tierra_parcelas_que_bajan": c(34998, "Bajan 34.998 parcelas", "3.5", "parcelas"),
        "tierra_parcelas_que_suben": c(33619, "suben 33.619", "3.5", "parcelas"),
        "tierra_rebaja_que_no_llega_si_no_se_ajusta_el_minimo": c(789, "789 millones", "3.5", "millones de pesos por año"),
    },
}

GRUPOS = [
    {"zonas": ["boulogne", "beccar"], "nombre": "Boulogne Sur Mer y Béccar, juntas",
     "cifras": {
         "poblacion": c(138551, "138.551 personas", "1.1", U_POB),
         "hogares": c(47193, "47.193 hogares", "1.1", U_HOG),
         "pct_de_la_poblacion": c(46.8, "46,8%", "1.1", "% de las 295.978 personas en viviendas particulares"),
         "pct_de_la_poblacion_sobre_297282": c(46.6, "46,6%", "1.1", "% de los 297.282 habitantes"),
         "pct_de_los_hogares_sin_gas_de_red": c(60, "el 60% de los 25.165 hogares sin gas de red", "1.1", "% del total de San Isidro",
                                               "La introducción lo dice así: «seis de cada diez hogares sin gas»."),
         "pct_de_los_hogares_sin_cloaca": c(71, "el 71% de los 6.488 hogares que no tienen cloaca", "1.1", "% del total de San Isidro",
                                           "La introducción lo dice así: «siete de cada diez sin cloaca»."),
         "hogares_sin_cloaca": c(4616, "4.616 hogares", "6.3 · Cuadro 41", U_HOG, "Meta del mandato: reducirlos a la mitad."),
         "pct_de_los_chicos_en_hogares_nbi": c(76, "El 76% de ellos vive en Boulogne y Béccar", E, "% de los 1.810 chicos en hogares con NBI"),
         "espacios_de_apoyo_escolar_hoy": c(5, "cinco espacios pequeños, sólo en Béccar y Boulogne", "5.8 · Cuadro 41", "espacios"),
         "alumnos_de_apoyo_escolar_hoy": c(100, "unos cien alumnos", "5.8 · Cuadro 41", "alumnos (aproximado)"),
     }},
]

COMPARACIONES = [
    {"texto": "Un hogar de Boulogne o de Béccar tiene tres veces y media más probabilidad de tener necesidades básicas insatisfechas que uno de Martínez.",
     "valor": 3.5, "fuente": "1.1"},
    {"texto": "Ese mismo hogar tiene cinco veces y media más probabilidad de no tener cloaca, y cuatro veces más probabilidad de vivir hacinado",
     "valor": {"sin_cloaca": 5.5, "hacinamiento": 4}, "fuente": "1.1"},
    {"texto": "En Boulogne y Béccar, tomadas juntas, la proporción de gente con la universidad terminada es menos de la mitad que en Martínez.",
     "valor": None, "fuente": "1.1"},
    {"texto": "Con nuestra propuesta, Béccar recibe 1,71 veces por habitante lo que recibe Martínez. Boulogne recibe 1,58 veces.",
     "valor": {"beccar_vs_martinez": 1.71, "boulogne_vs_martinez": 1.58}, "fuente": "4.4 · Gráfico 23"},
    {"texto": "el dinero de obra que deciden los vecinos llega 71% más por habitante a Béccar que a Martínez",
     "valor": 71, "fuente": "4.4 · Gráfico 23 (título)"},
    {"texto": "En Boulogne y Béccar están cerca de dos tercios de los hogares de San Isidro que tienen estas carencias",
     "valor": None, "fuente": "1.1 · Gráfico 2 (título)"},
    {"texto": "Según esa tabla, la tierra de Acassuso vale poco más del doble que la de Boulogne. Para la Provincia, vale casi el triple.",
     "valor": None, "fuente": "3.5"},
    {"texto": "a Villa Adelina le cobra de más. Casi la iguala con Boulogne, cuando para la Provincia Villa Adelina vale un tercio menos.",
     "valor": None, "fuente": "3.5"},
    {"texto": "Si se toman las secciones enteras, Acassuso da 2,37 veces Boulogne Sur Mer, en vez de 2,94.",
     "valor": {"secciones_enteras": 2.37, "parcela_por_parcela": 2.94}, "fuente": NOTA3,
     "aviso": "El 2,94 de esta nota no coincide con el 2,80× del Cuadro 17 para Acassuso (valuación provincial). Se copia tal cual; ver GEO_INFORME.md."},
    {"texto": "Acassuso tiene el NBI más bajo de todo San Isidro: 0,94%. Sin embargo, el 19,48% de sus hogares no tiene gas de red. Es más que en Martínez, en la localidad de San Isidro y en Villa Adelina.",
     "valor": None, "fuente": "4.4"},
    {"texto": "Boulogne es la localidad con más habitantes de San Isidro y la que menos espacio verde tiene.",
     "valor": None, "fuente": "5.5"},
]
for x in COMPARACIONES:
    if re.sub(r"\s+", " ", x["texto"]) not in TXT:
        FALTAN.append(x["texto"])

REGLAS_POR_ZONA = [
    {"texto": "Seis zonas, una por localidad.", "fuente": "4.5 · Gráfico 25"},
    {"texto": "La mitad se reparte según cuánta gente vive en cada zona, y la otra mitad, según un índice de necesidad.", "fuente": "4.4"},
    {"texto": "Hay cuatro asambleas por zona y por año, 24 en total", "fuente": NOTA4},
    {"texto": "Proponemos un centro de apoyo escolar gratuito en cada localidad.", "fuente": "5.8"},
    {"texto": "Los seis centros de apoyo escolar abiertos, uno por localidad: abren de a dos por año, los dos primeros en el año 1", "fuente": "6.4 · Cuadro 42 (mes 25)"},
    {"texto": "Habrá cinco sedes fijas, y en Acassuso la sede va a ir rotando, porque dieciocho personas por año no justifican un edificio.", "fuente": "5.3"},
    {"texto": "6 que atienden, uno en cada zona, a quien no puede usar solo la inteligencia artificial del Municipio", "fuente": "5.3"},
]
for x in REGLAS_POR_ZONA:
    if re.sub(r"\s+", " ", x["texto"]) not in TXT:
        FALTAN.append(x["texto"])

FALTANTES = [
    {"dato": "Reparto del dinero de obra vecinal del año 1 por zona (total y por habitante)",
     "estado": "No está en el programa final. Sólo da el total del año 1 (7.227 M, 24.310 $ por habitante, Cuadro 21) y el reparto por zona del año 4 (Gráfico 23). No se calculó."},
    {"dato": "Total de hogares por zona",
     "estado": "No está en el programa final. Da los hogares con cada carencia por zona (Cuadro 22), el total de San Isidro (110.559) y el de Boulogne y Béccar juntas (47.193)."},
    {"dato": "Porcentaje de chicos (hasta 14 años) y de personas mayores (65 y más) en todas las zonas",
     "estado": "El 5.13 da sólo los dos más altos de cada grupo: chicos en Béccar (21,0%) y Boulogne (18,7%); mayores en Acassuso (22,5%) y Martínez (22,4%)."},
    {"dato": "Promedio de San Isidro en % sin cloaca, sin gas de red, hacinamiento y universidad terminada",
     "estado": "El programa no lo da como porcentaje (sí da los totales de hogares del Cuadro 22). Sólo da el promedio de NBI: 3,16%."},
]

if FALTAN:
    print("!! textos que no están en el programa final:")
    for t in FALTAN:
        print("   ", t)
    sys.exit(1)

salida = {
    "descripcion": "Cifras por zona (localidad) del programa de gobierno «San Isidro 2027», versión final. Sólo cifras que están en el programa; ninguna calculada aparte.",
    "version_programa": "c462fcf",
    "fuente_texto": "Cada cifra trae «fuente» (apartado y, si corresponde, cuadro o gráfico del programa) y «como_figura» (el texto exacto con que aparece). Todos los «como_figura» se comprobaron contra el texto del PDF de pantalla final.",
    "zonas_ids": ["boulogne", "beccar", "villa_adelina", "san_isidro", "martinez", "acassuso"],
    "nota_zonas": "Las zonas son las seis localidades, con límites de OpenStreetMap aplicados a los 360 radios censales del Censo 2022 (nota del Gráfico 1 y Nota de método). No son límites oficiales. Los ids son los mismos que en zonas.geojson.",
    "zonas": ZONAS,
    "san_isidro": SAN_ISIDRO,
    "grupos": GRUPOS,
    "comparaciones": COMPARACIONES,
    "reglas_por_zona": REGLAS_POR_ZONA,
    "no_figura_en_el_programa": FALTANTES,
}
with open(SALIDA, "w", encoding="utf-8") as f:
    json.dump(salida, f, ensure_ascii=False, indent=1)
n = sum(len(z["cifras"]) for z in ZONAS.values())
print("ok:", SALIDA, "cifras por zona:", n, "| partido:", len(SAN_ISIDRO["cifras"]))
