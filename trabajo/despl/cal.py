# Calendario de días hábiles (lunes a viernes, sin feriados) y meses del programa.
import datetime as dt

D = dt.date
ONE = dt.timedelta(days=1)
H0, H1 = D(2027, 10, 1), D(2032, 1, 31)

WDS = []
_d = H0
while _d <= H1:
    if _d.weekday() < 5:
        WDS.append(_d)
    _d += ONE
IDX = {d: i for i, d in enumerate(WDS)}


def pos_on_or_after(d):
    while d not in IDX:
        d += ONE
    return IDX[d]


def pos_on_or_before(d):
    while d not in IDX:
        d -= ONE
    return IDX[d]


def date_of(p):
    return WDS[p]


def M(n):
    """Primer día del mes n del mandato (mes 1 = 10 de diciembre de 2027)."""
    k = 11 + (n - 1)
    return D(2027 + k // 12, k % 12 + 1, 10)


def E(n):
    """Último día del mes n del mandato (el 9 del mes siguiente)."""
    return M(n + 1) - ONE


def wd_span(a, b_incl):
    """Días hábiles desde a (incluido) hasta b (incluido)."""
    return pos_on_or_before(b_incl) - pos_on_or_after(a) + 1


MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_larga(d):
    return f"{d.day} de {MESES[d.month]} de {d.year}"
