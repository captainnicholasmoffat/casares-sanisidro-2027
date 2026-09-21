# -*- coding: utf-8 -*-
import content_a as A
import content_b as B
import content_c as C
import content_d as D
import content_e as E
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
C4B,    _c4 = split_at(_c4, '<h3>Lo que una comisi&oacute;n zonal no decide</h3>', "cap4bb", "")
C4B_B,  _c4 = split_at(_c4, '<h2><span class="n">4.7</span>', "cap4bb2", "")
C4B_B2, _c4 = split_at(_c4, '<h2><span class="n">4.9</span>', "cap4b2", "")
C4B2,  C4B_C = split_at(_c4, '<h2><span class="n">4.12</span>', "cap4bc", "")
C5B_SRC, C5B2_SRC = split_at(C.C5B, '<h2><span class="n">5.8</span>', "cap5b2",
                     H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C3B_A, C3B_B = split_at(B.C3B, '<h2><span class="n">3.5</span>', "cap3b2",
                        H_CONT.format(n=3, t="Los fondos"))
C3B_B, C3B_C = split_at(C3B_B, '<h3>La deuda que ya existe', "cap3b3", "")
C2A, C2B  = split_at(B.C2,  '<h2><span class="n">2.3</span>', "cap2b",
                     H_CONT.format(n=2, t="La gesti&oacute;n, medida"))
C5A, C5A2 = split_at(C.C5A, '<h2><span class="n">5.3</span>', "cap5a2",
                     H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5A2, C5A3 = split_at(C5A2, '<h3>Ense&ntilde;ar IA sin acceso', "cap5a3", "")
C6, C62_SRC = split_at(C.C6,  '<h2><span class="n">6.3</span>', "cap6b",
                     H_CONT.format(n=6, t="El plan, con fechas"))

C5B, C5B_B_SRC = split_at(C5B_SRC, '<h2><span class="n">5.6</span>', "cap5bb",
                      H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
# 5.5 crecio con el caso de la costa y el del Codigo Urbanistico: va en dos paginas
C5B, C5B_A2 = split_at(C5B, '<h3>El espacio p&uacute;blico: qui&eacute;n decide qu&eacute; se hace con &eacute;l</h3>',
                       "cap5ba2", "")
C5B_B, C5B_C = split_at(C5B_B_SRC, '<h2><span class="n">5.7</span>', "cap5bc",
                        H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5B2, C5B3 = split_at(C5B2_SRC, '<h2><span class="n">5.13</span>', "cap5b3",
                      H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5B2, C5B2B = split_at(C5B2, '<h2><span class="n">5.10</span>', "cap5b2b", "")
# 5.8 y 5.9 ya no entran juntas: la inspeccion transmitida se mudo al 5.9
C5B2, C5B2A2 = split_at(C5B2, '<h2><span class="n">5.9</span>', "cap5b2a2", "")
C6B_A, C6B_B = split_at(C62_SRC, '<h2><span class="n">6.6</span>', "cap6c",
                        H_CONT.format(n=6, t="El plan, con fechas"))

# el anexo articulado entra en dos paginas
ORD_A, ORD_B = split_at(O.ORDENANZA,
                        '<h2>V &middot; Ordenanza de asociaciones de parque</h2>',
                        "ordenanza2", "")

SECTIONS = [A.INDICE, S.SINTESIS, A.INTRO, C1A, C1A2, A.C1B, C2A, C2B, B.C3A, C3B_A, C3B_B, C3B_C,
            C4A, C4A2, C4B, C4B_B, C4B_B2, C4B2, C4B_C,
            C5A, C5A2, C5A3, C5B, C5B_A2, C5B_B, C5B_C, C5B2, C5B2A2, C5B2B, C5B3, C6, C6B_A, C6B_B, E.CIERRE, ORD_A, ORD_B, D.GLOSARIO]

# pagina 1 = tapa; el indice arranca en la 2
A.PAGES.update({k: i + 3 for i, k in enumerate(
    [s["id"] for s in SECTIONS[1:]])})
# el indice se arma al importar, asi que hay que rehacerlo con los numeros ya puestos
A.INDICE["html"] = A._indice()
SECTIONS[0] = A.INDICE
