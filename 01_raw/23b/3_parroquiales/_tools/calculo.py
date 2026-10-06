#!/usr/bin/env python3
# Programa San Isidro 2027 - Escuelas parroquiales y cooperativas (z3)
# Uso: python3 -I calculo.py  (escribe CSVs en la carpeta z3_parroquiales y la salida en _tools/calculo_salida.txt)
# Base: padrón oficial PBA (Datos Abiertos, corte 28/09/2026, matrícula Relevamiento Inicial 2026),
#       copiado por el trabajo previo en c23_raw/y2_canon_privados/ (sólo lectura).
import csv, os, sys
from collections import defaultdict

S = "/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad"
PADRON = S + "/c23_raw/y2_canon_privados/pba_establecimientos_SanIsidro_28092026.csv"
Z = S + "/c23b_raw/z3_parroquiales"
OUT_LISTA = Z + "/z3_lista_parroquiales_cooperativas.csv"
OUT_TODOS = Z + "/z3_clasificacion_111_unidades_privadas.csv"

TOTAL_PRIVADOS_2026 = 31234          # prim + sec privados, Relevamiento Inicial 2026 (padrón)
TOTAL_PARTIDO_2025 = 50833           # alumnos de primaria y secundaria del partido, 2025 (informe 22/23)
PRIV_2025 = {"Primario": 15142, "Secundario": 16978}   # matrícula privada 2025 DGCyE (reporte Y2)

# ---------------------------------------------------------------------------
# Clasificación por clave DGCyE.
# categoria: PARROQUIAL | DIOCESANA | CONGREGACION | CATOLICA_SIN_CONFIRMAR | OTRA_PRIVADA | COOPERATIVA
# marca: verificado | probable | sin confirmar | inferencia
# ---------------------------------------------------------------------------
F_PADRON = "padrón PBA 28/09/2026 (nombre oficial)"
C = {}
def put(claves, cat, marca, entidad, como, fuente):
    for k in claves:
        C[k] = dict(categoria=cat, marca=marca, entidad=entidad, como=como, fuente=fuente)

# --- PARROQUIALES -----------------------------------------------------------
put(["4096PP0542", "4096MS4688"], "PARROQUIAL", "verificado",
    "Parroquia Santa Teresita del Niño Jesús (Martínez) - Obispado de San Isidro [nombre exacto de la parroquia: probable]",
    "La web del colegio dice 'Colegio Parroquial Santa Teresa del Niño Jesús' fundado en 1956 por el párroco y 'perteneciente al Obispado de San Isidro'",
    "web_stateresa_historia.html; web_stateresa_inicio.html")
put(["4096PP0532", "4096MS5709"], "PARROQUIAL", "verificado",
    "Parroquia Nuestra Señora de Lourdes (Beccar) - Obispado de San Isidro (dueño del inmueble por Ley 10.668)",
    "Ley provincial 10.668 (1988) dona el inmueble al Obispado 'con destino al Colegio Parroquial N.S. de Lourdes'; la web del colegio dice 'Colegio Parroquial Nuestra Señora de Lourdes' (Beccar)",
    "ngba_ley10668_1988_*.html; web_lourdes_historia.html")
put(["4096PP0528", "4096MS4654"], "PARROQUIAL", "verificado",
    "Parroquia no identificada (Boulogne) - Obispado de San Isidro",
    "Nombre oficial en el padrón: 'ESCUELA PARROQUIAL JUAN XXIII'; la web dice 'Colegio Parroquial Juan XXIII'; figura en la guía del Obispado (resultado de búsqueda)",
    F_PADRON + "; web_juanxxiii_inicio.html")
put(["4096PP5075", "4096MS5459"], "PARROQUIAL", "verificado",
    "Parroquia Nuestra Señora del Refugio (Boulogne) [probable] - Obispado de San Isidro",
    "Nombre oficial en el padrón: 'COLEGIO PARROQUIAL NUESTRA SEÑORA (DEL) REFUGIO'; existe la parroquia homónima en Boulogne (lista de parroquias)",
    F_PADRON + "; wiki_anexo_parroquias_diocesis_san_isidro.html")
put(["4096PP0520", "4096MS5053"], "PARROQUIAL", "verificado",
    "Parroquia (probable: Nuestra Señora de la Cava, Beccar) - Obispado de San Isidro",
    "La web del colegio se titula 'Santo Domingo Savio - Colegio Parroquial' (leída con WebFetch, sin copia guardada); figura en la guía del Obispado; el Decreto 624/1985 habla de la 'escuela parroquial de Villa La Cava' [probable que sea esta]",
    "colegiodomingosavio.edu.ar (leído, no guardado); ngba_dec624_1985_*.html")
put(["4096PP5581"], "PARROQUIAL", "probable",
    "Obispado de San Isidro; parroquia probable: Resurrección del Señor (Martínez)",
    "CUIT 30-68640907-0 a nombre de 'ESCUELA SAN FRANCISCO JAVIER OBISPADO SAN ISIDRO' (Nosis); figura en la guía del Obispado; el buscador devolvió una página 'San Francisco Javier' del sitio de la parroquia Resurrección (no carga); el Decreto-ley 8683/1976 habla del 'colegio de la parroquia Resurrección del Señor' en Martínez",
    "nosis_cuit_30686409070_*.html; ngba_dl8683_1976_*.html")

# --- DIOCESANAS (del Obispado directamente) ---------------------------------
put(["4096PP0784", "4096MS4707", "4096PP0541", "4096MS5763", "4096PP6047", "4096MS7812"], "DIOCESANA", "verificado",
    "Obispado de San Isidro - Grupo Educativo Marín (Comisión Administradora designada por el Obispo)",
    "La web del Grupo Marín dice 'El Grupo Educativo Marín pertenece al Obispado de San Isidro' e incluye Carmen Arriola de Marín, Santa María de Luján y Plácido Marín",
    "web_grupomarin_historia.html; web_grupomarin_inicio.html")
put(["4096PP0534", "4096MS6929"], "DIOCESANA", "verificado",
    "Obispado de San Isidro ('Iglesia Diocesana'); existe la Parroquia San Andrés Avelino en Villa Adelina [si el titular es la parroquia o el Obispado: sin confirmar]",
    "La web del colegio dice 'Nuestro Colegio es una Institución perteneciente a la Iglesia Diocesana, Obispado de San Isidro'",
    "web_sanandresavelino_ideario.html; web_sanandresavelino_inicio.html")

# --- CONGREGACIONES / fundaciones o asociaciones religiosas (quedan afuera) ---
put(["4096PP0533", "4096MS4687"], "CONGREGACION", "verificado",
    "Orden de los Clérigos Regulares (Teatinos)",
    "La web dice 'pertenecemos a la Orden de los Clérigos Regulares'. HUECO: la parroquia Sagrado Corazón de Boulogne existe y un resultado de búsqueda lo llama 'colegio parroquial'",
    "web_sagradoboulogne_inicio.html")
put(["4096PP0535", "4096MS7016"], "CONGREGACION", "probable",
    "Orden Teatina (probable)",
    "La web tiene una sección 'Orden Teatina'. HUECO: existe la parroquia San Cayetano de Villa Adelina",
    "web_sancayetanova_inicio.html")
put(["4096PP0537", "4096MS4685"], "CONGREGACION", "verificado",
    "Congregación de las Hermanas Adoratrices, Esclavas del Santísimo Sacramento y de la Caridad",
    "La web (Identidad) describe la obra de esa congregación. HUECO: existe la parroquia San José de San Isidro",
    "web_sanjosemartinez_identidad.html")
put(["4096PP0780", "4096MS4679"], "CONGREGACION", "verificado",
    "FEM - Fundación Educación y Misión",
    "La web dice 'pertenece a la FEM (Fundación Educación y Misión)'", "web_spinola_quienes.html")
put(["4096PP0779", "4096MS4673"], "CONGREGACION", "verificado",
    "Hermanas de la Caridad Cristiana (fundadoras; titular actual sin confirmar)",
    "La web cuenta que lo fundaron las Hermanas de la Caridad Cristiana", "web_mallinckrodt_historia.html")
put(["4096PP0530", "4096MS4678"], "CONGREGACION", "probable",
    "Salesianas (Hijas de María Auxiliadora) [probable]",
    "La web habla de 'propuesta educativa salesiana' y 'carisma salesiano'", "web_imasanisidro_inicio.html")
put(["4096PP5338", "4096MS5370"], "CONGREGACION", "verificado",
    "APDES (asociación sin fines de lucro; red de colegios)",
    "La web de APDES: 'Apdes es una asociación sin fines de lucro'; el mail de la secundaria es @apdes.edu.ar", "web_apdes_nosotros.html")
put(["4096PP1361", "4096MS4698"], "CONGREGACION", "sin confirmar",
    "No verificado en esta sesión (se lo asocia públicamente a una congregación de hermanos)",
    "Las páginas guardadas no dicen quién es el titular", "web_newman_historia.html")

# --- CATÓLICAS LAICAS u otras con titular identificado (quedan afuera) ---------
put(["4096PP1848", "4096MS4662"], "OTRA_PRIVADA", "verificado",
    "Fundado por una familia (católico, bilingüe); titular sin confirmar",
    "La web (Historia) cuenta que lo fundó una familia en 1981", "web_holycross_historia.html")
put(["4096PP1195", "4096MS4691"], "OTRA_PRIVADA", "verificado",
    "Fundado en 1969 por dos fundadoras laicas; titular sin confirmar",
    "La web (El colegio) cuenta su fundación por dos personas", "web_launidad_elcolegio.html")
put(["4096PP0696", "4096MS4677", "4096MS4693"], "OTRA_PRIVADA", "probable",
    "Colegio Santos Unidos (San Juan el Precursor + Santa Inés), 'comunidad educativa católica' de familias; titular sin confirmar",
    "La web cuenta que las familias de ambos colegios se unieron en 2024", "web_santosunidos_historia.html")
put(["4096PP0516", "4096MS4669"], "CATOLICA_SIN_CONFIRMAR", "sin confirmar",
    "Sin confirmar (católico, 'desde 1935'; la parroquia de Fátima de Martínez es de 1956)",
    "La web no dice quién es el titular", "web_fatima_inicio.html")

# --- CATÓLICAS (por nombre) SIN TITULAR CONFIRMADO --------------------------
for claves, nota in [
    (["4096PP0539", "4096MS4697"], "Instituto San Juan Bosco (Villa Adelina): existe la parroquia San Juan Bosco (San Isidro); la web no cargó (certificado incompleto / 503)"),
    (["4096PP5046", "4096MS8040"], "Ceferino Namuncurá (Boulogne): la guía del Obispado tiene un 'Colegio Ceferino Namuncurá' cuya dirección web sugiere N.S. de la Guardia (otra zona); el dominio del colegio hoy es un sitio de casino"),
    (["4096MS4699"], "Instituto Santísima Trinidad (Boulogne, secundaria): sin web; la parroquia Santísima Trinidad de la diócesis está en Tigre"),
    (["4096MS4695"], "Instituto Sagrada Familia (secundaria): sin web; no hay parroquia Sagrada Familia en San Isidro (la hay en Carapachay)"),
    (["4096PP1127", "4096MS6188"], "San Miguel Arcángel: sin web; no hay parroquia homónima en San Isidro"),
    (["4096PP0540", "4096MS4671"], "Instituto Santa Isabel: la web (casasantaisabel.edu.ar) da 404"),
]:
    put(claves, "CATOLICA_SIN_CONFIRMAR", "sin confirmar", "Sin confirmar", nota, "padrón; búsquedas")

def tramo(sub):
    s = sub.strip()
    if s.startswith("Sin"): return "Sin aporte"
    return s.split()[-1]  # '100%','80%',...

def main():
    rows = [x for x in csv.DictReader(open(PADRON, encoding="utf-8"))
            if x["sector"] == "Privado" and x["nivel"] in ("Nivel Primario", "Nivel Secundario")
            and x["modalidad"] in ("Educación Común", "Educación Técnico Profesional")]
    out = []
    tot = sum(int(x["matricula"]) for x in rows)
    out.append(f"Unidades privadas de primaria y secundaria (común + técnica): {len(rows)}; matrícula {tot} (control: {TOTAL_PRIVADOS_2026})")
    assert tot == TOTAL_PRIVADOS_2026
    for x in rows:
        if x["clave"] not in C:
            C[x["clave"]] = dict(categoria="OTRA_PRIVADA", marca="inferencia",
                                 entidad="Sin dato", como="Sin indicios de parroquia ni de cooperativa (nombre, web o INAES); no se investigó el titular",
                                 fuente="padrón; INAES")
    claves_padron = {x["clave"] for x in rows}
    faltan = [k for k in C if k not in claves_padron]
    out.append(f"Claves clasificadas que no están en el padrón prim/sec: {faltan}")

    # CSV completo de 111 unidades
    with open(OUT_TODOS, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escuela", "cue", "cueanexo", "clave", "nivel", "matricula_RI2026", "aporte", "entidad_propietaria", "categoria", "marca", "como_se_identifico", "fuente"])
        for x in sorted(rows, key=lambda r: (C[r["clave"]]["categoria"], r["establecimiento_nombre"], r["nivel"])):
            c = C[x["clave"]]
            w.writerow([x["establecimiento_nombre"], x["cue"], x["cueanexo"], x["clave"], x["nivel"].replace("Nivel ", ""), x["matricula"],
                        tramo(x["subvencion"]), c["entidad"], c["categoria"], c["marca"], c["como"], c["fuente"]])
    # CSV de la lista pedida (parroquiales, diocesanas, cooperativas y pendientes)
    with open(OUT_LISTA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escuela", "cue", "cueanexo", "clave", "nivel", "matricula_RI2026", "aporte", "entidad_propietaria", "categoria", "marca", "como_se_identifico", "fuente"])
        for cat in ["PARROQUIAL", "DIOCESANA", "COOPERATIVA", "CATOLICA_SIN_CONFIRMAR"]:
            for x in sorted([r for r in rows if C[r["clave"]]["categoria"] == cat], key=lambda r: (r["establecimiento_nombre"], r["nivel"])):
                c = C[x["clave"]]
                w.writerow([x["establecimiento_nombre"], x["cue"], x["cueanexo"], x["clave"], x["nivel"].replace("Nivel ", ""), x["matricula"],
                            tramo(x["subvencion"]), c["entidad"], cat, c["marca"], c["como"], c["fuente"]])

    # Totales
    TR = ["100%", "80%", "70%", "60%", "50%", "40%", "Sin aporte"]
    agg = defaultdict(lambda: defaultdict(int))   # agg[cat][(nivel,tramo)]
    nunits = defaultdict(lambda: defaultdict(int))
    for x in rows:
        cat = C[x["clave"]]["categoria"]
        if cat == "PARROQUIAL" and C[x["clave"]]["marca"] == "probable":
            cat2 = "PARROQUIAL_PROBABLE"
        else:
            cat2 = cat
        niv = x["nivel"].replace("Nivel ", "")
        for k in (cat, cat2) if cat2 != cat else (cat,):
            agg[k][(niv, tramo(x["subvencion"]))] += int(x["matricula"])
            nunits[k][niv] += 1

    def bloque(nombre, cats):
        p = sum(agg[c][("Primario", t)] for c in cats for t in TR)
        s = sum(agg[c][("Secundario", t)] for c in cats for t in TR)
        up = sum(nunits[c]["Primario"] for c in cats); us = sum(nunits[c]["Secundario"] for c in cats)
        out.append("")
        out.append(f"== {nombre} ==  unidades prim {up} / sec {us}")
        out.append(f"{'tramo':<11}{'prim':>7}{'sec':>7}{'total':>8}{'%priv31234':>12}{'%partido50833':>15}")
        for t in TR:
            a = sum(agg[c][("Primario", t)] for c in cats); b = sum(agg[c][("Secundario", t)] for c in cats)
            if a + b:
                out.append(f"{t:<11}{a:>7}{b:>7}{a+b:>8}{100*(a+b)/TOTAL_PRIVADOS_2026:>11.2f}%{100*(a+b)/TOTAL_PARTIDO_2025:>14.2f}%")
        out.append(f"{'TOTAL':<11}{p:>7}{s:>7}{p+s:>8}{100*(p+s)/TOTAL_PRIVADOS_2026:>11.2f}%{100*(p+s)/TOTAL_PARTIDO_2025:>14.2f}%")
        # escalado a 2025 (cálculo propio): mismas proporciones por nivel
        p25 = p * PRIV_2025["Primario"] / 14483; s25 = s * PRIV_2025["Secundario"] / 16751
        out.append(f"   escalado a 2025 [cálculo propio]: prim {p25:,.0f} + sec {s25:,.0f} = {p25+s25:,.0f}  ({100*(p25+s25)/TOTAL_PARTIDO_2025:.2f}% de 50.833)")
        return p, s

    # separar verificadas de probables
    agg["PARROQUIAL_V"] = defaultdict(int); nunits["PARROQUIAL_V"] = defaultdict(int)
    for k, v in agg["PARROQUIAL"].items():
        agg["PARROQUIAL_V"][k] = v - agg["PARROQUIAL_PROBABLE"][k]
    for k in ("Primario", "Secundario"):
        nunits["PARROQUIAL_V"][k] = nunits["PARROQUIAL"][k] - nunits["PARROQUIAL_PROBABLE"][k]
    bloque("A. PARROQUIALES verificadas (= Variante 1, estricta)", ["PARROQUIAL_V"])
    bloque("B. PARROQUIAL probable (San Francisco Javier)", ["PARROQUIAL_PROBABLE"])
    bloque("C. DIOCESANAS (Obispado directo: Grupo Marín + San Andrés Avelino)", ["DIOCESANA"])
    bloque("D. COOPERATIVAS", ["COOPERATIVA"])
    bloque("Variante 2: parroquiales verificadas + probable (sin diocesanas)", ["PARROQUIAL", "COOPERATIVA"])
    pA, sA = bloque("Variante 3 = definición del pedido (parroquia u Obispado): parroquiales (verif.+prob.) + diocesanas + cooperativas", ["PARROQUIAL", "DIOCESANA", "COOPERATIVA"])
    bloque("PENDIENTES: católicas sin titular confirmado (NO incluidas)", ["CATOLICA_SIN_CONFIRMAR"])
    bloque("Máximo si todas las pendientes resultaran parroquiales", ["PARROQUIAL", "DIOCESANA", "COOPERATIVA", "CATOLICA_SIN_CONFIRMAR"])
    bloque("Congregaciones y fundaciones/asociaciones religiosas (NO incluidas)", ["CONGREGACION"])
    bloque("Resto de privadas (pagan costo completo)", ["OTRA_PRIVADA"])
    # control de suma
    s_all = sum(sum(agg[c].values()) for c in ["PARROQUIAL", "DIOCESANA", "COOPERATIVA", "CATOLICA_SIN_CONFIRMAR", "CONGREGACION", "OTRA_PRIVADA"])
    out.append("")
    out.append(f"Control: suma de categorías excluyentes = {s_all} (debe ser {TOTAL_PRIVADOS_2026})")
    assert s_all == TOTAL_PRIVADOS_2026
    out.append(f"Privados que pagarían costo completo con la Variante 3: {TOTAL_PRIVADOS_2026 - pA - sA}")
    txt = "\n".join(out)
    print(txt)
    open(Z + "/_tools/calculo_salida.txt", "w").write(txt + "\n")

if __name__ == "__main__":
    main()
