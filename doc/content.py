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
C4B_SRC, C4B2_SRC = split_at(C.C4B, '<h2><span class="n">4.8</span>', "cap4b2",
                     H_CONT.format(n=4, t="El mecanismo"))
C4B, C4B_B_SRC = split_at(C4B_SRC, '<h3>Para lo que excede al barrio: un panel sorteado</h3>', "cap4bb",
                      H_CONT.format(n=4, t="El mecanismo"))
C4B_B, C4B_B2 = split_at(C4B_B_SRC, '<h3>La plataforma no se inventa', "cap4bb2", "")
C4B2, C4B_C = split_at(C4B2_SRC, '<h3>Lo que el propio Ejecutivo dice', "cap4bc",
                       H_CONT.format(n=4, t="El mecanismo"))
C5B_SRC, C5B2_SRC = split_at(C.C5B, '<h2><span class="n">5.8</span>', "cap5b2",
                     H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C3B_A, C3B_B = split_at(B.C3B, '<h2><span class="n">3.6</span>', "cap3b2",
                        H_CONT.format(n=3, t="Los fondos"))
C3B_B, C3B_C = split_at(C3B_B, '<h3>La tabla con la que San Isidro val', "cap3b3", "")
C2A, C2B  = split_at(B.C2,  '<h2><span class="n">2.5</span>', "cap2b",
                     H_CONT.format(n=2, t="La gesti&oacute;n, medida"))
C5A, C5A2 = split_at(C.C5A, '<h2><span class="n">5.3</span>', "cap5a2",
                     H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C6, C62_SRC = split_at(C.C6,  '<h2><span class="n">6.4</span>', "cap6b",
                     H_CONT.format(n=6, t="Contra qu&eacute; queremos que nos midan"))

C5B, C5B_B_SRC = split_at(C5B_SRC, '<h2><span class="n">5.6</span>', "cap5bb",
                      H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5B_B, C5B_C = split_at(C5B_B_SRC, '<h2><span class="n">5.7</span>', "cap5bc",
                        H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C5B2, C5B3 = split_at(C5B2_SRC, '<h2><span class="n">5.12</span>', "cap5b3",
                      H_CONT.format(n=5, t="Qu&eacute; hacemos en cada &aacute;rea"))
C6B_A, C6B_B = split_at(C62_SRC, '<h2><span class="n">6.7</span>', "cap6c",
                        H_CONT.format(n=6, t="Contra qu&eacute; queremos que nos midan"))

SECTIONS = [A.INDICE, S.SINTESIS, A.INTRO, C1A, C1A2, A.C1B, C2A, C2B, B.C3A, C3B_A, C3B_B, C3B_C,
            C4A, C4A2, C4B, C4B_B, C4B_B2, C4B2, C4B_C, C5A, C5A2, C5B, C5B_B, C5B_C, C5B2, C5B3, C6, C6B_A, C6B_B, E.CIERRE, O.ORDENANZA, D.GLOSARIO]

# pagina 1 = tapa; el indice arranca en la 2
A.PAGES.update({
    "sintesis":3, "intro":4, "c1a":5, "c1a2":6, "c1b":7, "c2":8, "c2b":9, "c3a":10, "c3b":11, "c3b2":12, "c3b3":13, "c4a":14, "c4a2":15, "c4b":16, "c4bb":17, "c4bb2":18, "c4b2":19, "c4bc":20, "c5a":21, "c5a2":22, "c5b":23, "c5bb":24, "c5bc":25, "c5b2":26, "c5b3":27, "c6":28, "c6b":29, "c6c":30, "cierre":31, "ordenanza":32, "glosario":33
})
# el indice se arma al importar, asi que hay que rehacerlo con los numeros ya puestos
A.INDICE["html"] = A._indice()
SECTIONS[0] = A.INDICE
