# -*- coding: utf-8 -*-
import content_a as A
import content_b as B
import content_c as C
import content_d as D
import content_e as E
import content_f as F
import content_o as O
import content_s as S

DOC_TITLE = A.DOC_TITLE

def split_at(sec, marker, cont_id, cont_h1):
    """Parte una seccion en dos paginas, cortando antes de un subtitulo."""
    i = sec["html"].index(marker)
    a = dict(sec); a["html"] = sec["html"][:i]
    b = dict(sec); b["id"] = cont_id; b["html"] = cont_h1 + sec["html"][i:]
    return a, b

H_CONT = ""   # las páginas de continuación no repiten el encabezado del capítulo

C1A, C1A2 = split_at(A.C1A, '<h2><span class="n">1.2</span>', "cap1a2",
                     H_CONT.format(n=1, t="Diagn&oacute;stico"))
C4A, C4A2 = split_at(C.C4A, '<h2><span class="n">4.4</span>', "cap4a2",
                     H_CONT.format(n=4, t="El mecanismo"))
# el capitulo 4 entra en siete paginas: la aplicacion (4.11) es seccion
# propia y se lleva una entera.
_c4 = C.C4B
C4B,    _c4 = split_at(_c4, '<h3>Qu&eacute; no va a decidir una comisi&oacute;n zonal</h3>', "cap4bb", "")
C4B_B,  _c4 = split_at(_c4, '<h2><span class="n">4.7</span>', "cap4bb2", "")
C4B_B2, _c4 = split_at(_c4, '<h2><span class="n">4.9</span>', "cap4b2", "")
C4B2,  C4B_C = split_at(_c4, '<h2><span class="n">4.12</span>', "cap4bc", "")
# (dispatch 3, A12): la inteligencia artificial que escucha y el espacio de las asociaciones llevan el resto del 4.11 a otra pagina
C4B2, C4B2B = split_at(C4B2, '<h3>Escucha a los vecinos, les hace el seguimiento y les responde</h3>', "cap4b2b", "")
C5B_SRC, C5B2_SRC = split_at(C.C5B, '<h2><span class="n">5.8</span>', "cap5b2",
                     H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
# (dispatch 11) con el texto en lenguaje llano el 3.4 no entra en una pagina: lo que cuesta administrar pasa a la siguiente
C3B_A, C3B_B = split_at(B.C3B, '<h3>Cu&aacute;nto cuesta que los vecinos participen</h3>', "cap3b2",
                        H_CONT.format(n=3, t="Los fondos"))
C3B_B, C3B_C = split_at(C3B_B, '<h3>La deuda que ya existe', "cap3b3", "")
C2A, C2B  = split_at(B.C2,  '<h2><span class="n">2.2</span>', "cap2b",
                     H_CONT.format(n=2, t="El gobierno actual, medido"))
C5A, C5A2 = split_at(C.C5A, '<h2><span class="n">5.3</span>', "cap5a2",
                     H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5A2, C5A3 = split_at(C5A2, '<h3>Ense&ntilde;ar IA sin acceso', "cap5a3", "")
# correcciones 173-175: la pasantia y la piramide agrandan el 5.3, que pasa a cuatro paginas
C5A3, C5A4 = split_at(C5A3, '<h3>La pir&aacute;mide: del pasante al empleo</h3>', "cap5a4", "")
C6, C62_SRC = split_at(C.C6,  '<h2><span class="n">6.3</span>', "cap6b",
                     H_CONT.format(n=6, t="El plan, con fechas"))

C5B, C5B_B_SRC = split_at(C5B_SRC, '<h2><span class="n">5.6</span>', "cap5bb",
                      H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
# 5.5 crecio con el caso de la costa y el del Codigo Urbanistico: va en dos paginas
C5B, C5B_A2 = split_at(C5B, '<h3>El espacio p&uacute;blico: qui&eacute;n decide qu&eacute; se hace con &eacute;l</h3>',
                       "cap5ba2", "")
# la costa (189) abre el 5.5: la costa y la recoleccion en una pagina; el ruido y el urbanismo, en la siguiente
C5B, C5B_R = split_at(C5B, '<h3>El ruido es la contaminaci&oacute;n que nadie mide</h3>', "cap5br", "")
# la Escuela Nautica, la movida, los banos y las clases de la costa (dispatch 2, 03/10) llevan el resto del 5.5 a otra pagina
C5B_A2, C5B_A3 = split_at(C5B_A2, '<h3>La Escuela N&aacute;utica, en todos los parques de la costa</h3>', "cap5ba3", "")
# los espectaculos al aire libre (dispatch 3, parte B) abren pagina, con la obra en parques y costa
C5B_A3, C5B_A4 = split_at(C5B_A3, '<h3>Espect&aacute;culos al aire libre, en la semana</h3>', "cap5ba4", "")
# (dispatch 9) con sus tres fotos, los espectaculos van solos; la obra en parques y costa abre la pagina siguiente
C5B_A4, C5B_A5 = split_at(C5B_A4, '<h3>Cemento o naturaleza: la obra en parques y costa</h3>', "cap5ba5", "")
C5B_B, C5B_C = split_at(C5B_B_SRC, '<h2><span class="n">5.7</span>', "cap5bc",
                        H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5B2, C5B3 = split_at(C5B2_SRC, '<h2><span class="n">5.13</span>', "cap5b3",
                      H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5B2, C5B2B = split_at(C5B2, '<h2><span class="n">5.10</span>', "cap5b2b", "")
# los resumenes de cada capitulo (dispatch 3, A13) crecieron: el 5.14 y el 5.15 van en pagina propia
C5B3, C5B3B = split_at(C5B3, '<h2><span class="n">5.14</span>', "cap5b3b", "")
# las multas de transito (dispatch 1, 03/10) no entran con el 5.10 y el 5.11: van con el 5.12 en la pagina siguiente
C5B2B, C5B2C = split_at(C5B2B, '<h3>Multas de tr&aacute;nsito:', "cap5b2c", "")
# 5.8 y 5.9 ya no entran juntas: la inspeccion grabada se mudo al 5.9
C5B2, C5B2A2 = split_at(C5B2, '<h2><span class="n">5.9</span>', "cap5b2a2", "")
# dispatch 11: con el lenguaje llano el 6.4 crece, y el 6.5 pasa a la pagina del 6.6
C6B_A, C6B_B = split_at(C62_SRC, '<h2><span class="n">6.5</span>', "cap6c",
                        H_CONT.format(n=6, t="El plan, con fechas"))
# el calendario suma las fechas propuestas de multas y costa: el 6.4 en pagina propia
C6B_A, C6B_A2 = split_at(C6B_A, '<h2><span class="n">6.4</span>', "cap6b2", "")

# nota de metodo y notas de cada capitulo en una pagina; las fuentes del texto, en la
# siguiente, la ultima del documento (correccion 138, respuesta 6; la 40 pasaba de 2.700 pt)
# (dispatch 1 y 2, 03/10): con las filas de multas y de la costa las fuentes no entran en una pagina; la
# primera parte vuelve a la de la nota de metodo y el resto sigue en la ultima
_F_CORTE = F.FUENTES_HTML.index('<tr><td class="l">5.5 &middot; la costa toda la semana')
_F_CAB = ('<table>\n<colgroup><col style="width:158pt"><col></colgroup>\n'
          '<tr class="hd"><th>D&oacute;nde</th><th>Fuente</th></tr>\n')
# (dispatch 3, A9): las notas de cada capitulo crecieron con el detalle que salio de abajo de los cuadros; la nota de
# metodo vuelve a ir sola y las fuentes del texto van en dos paginas
# (dispatch 6): con las ciudades y las fuentes del 23 quater la segunda pasaba de 2.700 pt; el corte baja a «la costa toda la semana»
METODO = dict(A.METODO)
FUENTES = dict(id="fuentes", runhead=A.RH,
               html=F.FUENTES_HTML.replace('<div class="hairline"></div>\n', "", 1)[:F.FUENTES_HTML.replace('<div class="hairline"></div>\n', "", 1).index('<tr><td class="l">5.5 &middot; la costa toda la semana')] + "</table>\n")
FUENTES2 = dict(id="fuentes2", runhead=A.RH, html=_F_CAB + F.FUENTES_HTML[_F_CORTE:])

# dispatch 15: con el lenguaje llano y los tomografos, tres paginas del capitulo 5 pasaban de 2.700 pt
C5A3, C5A3B = split_at(C5A3, '<h3>Un puente con las empresas de inteligencia artificial</h3>', "cap5a3b", "")
C5B, C5B_REC = split_at(C5B, '<h3>Recolecci&oacute;n de residuos:', "cap5brec", "")
C5B_B, C5B_B2 = split_at(C5B_B, '<h3>El Municipio ya anunci&oacute; inteligencia artificial en salud.', "cap5bb2", "")

# dispatch 15: el 6.7 y las dos listas finales (lo que no hace y lo que confirma un abogado) van en pagina propia
C6B_B, C6B_C = split_at(C6B_B, '<h2><span class="n">6.7</span>', "cap6d", "")
FUENTES2, FUENTES3 = split_at(FUENTES2, '<h2>Lo que este programa no hace</h2>', "fuentes3", "")

# el anexo articulado entra en cuatro paginas (C1: crecieron la II, la VI y llegaron la XV y la XVI)
ORD_A, ORD_B = split_at(O.ORDENANZA,
                        '<h2>4 &middot; Ordenanza de grabaci&oacute;n de los actos de fiscalizaci&oacute;n</h2>',
                        "ordenanza2", "")
ORD_B, ORD_C = split_at(ORD_B, '<h2>8 &middot; Ordenanza de ruido</h2>', "ordenanza3", "")
# de la XI en adelante (costa, obra en parques y costa, excepciones, parques y cuotas de multas) va en una cuarta
ORD_C, ORD_D = split_at(ORD_C, '<h2>11 &middot; Ordenanza de la costa', "ordenanza4", "")

SECTIONS = [A.INDICE, A.INTRO, S.SINTESIS, C1A, C1A2, A.C1B, C2A, C2B, B.C3A, C3B_A, C3B_B, C3B_C,
            C4A, C4A2, C4B, C4B_B, C4B_B2, C4B2, C4B2B, C4B_C,
            C5A, C5A2, C5A3, C5A3B, C5A4, C5B, C5B_REC, C5B_R, C5B_A2, C5B_A3, C5B_A4, C5B_A5, C5B_B, C5B_B2, C5B_C, C5B2, C5B2A2, C5B2B, C5B2C, C5B3, C5B3B, C6, C6B_A, C6B_A2, C6B_B, C6B_C, E.CIERRE, ORD_A, ORD_B, ORD_C, ORD_D, D.GLOSARIO, METODO, FUENTES, FUENTES2, FUENTES3]

# las referencias [[n:clave]] a cuadros y graficos, con el numero ya asignado
for _s in SECTIONS:
    _s["html"] = A.resolver_refs(_s["html"])

# pagina 1 = tapa; el indice arranca en la 2
A.PAGES.update({k: i + 3 for i, k in enumerate(
    [s["id"] for s in SECTIONS[1:]])})
# el indice se arma al importar, asi que hay que rehacerlo con los numeros ya puestos
A.INDICE["html"] = A._indice()
SECTIONS[0] = A.INDICE
