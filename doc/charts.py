#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rehace los 18 graficos como SVG vectorial, con la tipografia y la paleta
del documento. Los datos son los que figuran en los cuadros del propio
programa, para que texto y grafico no puedan discrepar.

Clave: figsize en pulgadas = ancho de columna (570 pt = 7,9167 in) y
svg.fonttype='none', asi 1 punto de matplotlib es 1 punto de la pagina y la
pagina presta su propia Inter."""
import os, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT = pathlib.Path(__file__).parent.parent / "assets" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

GROUND="#F5F0E8"; INK="#2A211C"; TAUPE="#6E625A"; OX="#7C2E23"; CORAL="#DB6B4B"
SAGE="#5F7057"; SAGED="#66734C"; AMBER="#B4863A"; HAIR="#D9CDBA"; SAND="#EAE0CF"
PALE="#C9CFBE"; PALEOX="#C89A8F"

W = 570/72.0                      # ancho de columna, en pulgadas
_RAIZ = pathlib.Path(__file__).parent.parent
BR = _RAIZ / "br" / "casares-sanisidro-2027-claude-rediseno-paleta-extratime" / "data"
if not BR.exists():                      # el directorio de trabajo de otra rama ya no esta
    BR = _RAIZ / "data"

def _csv(nombre):
    """Lee un csv del repo salteando las lineas de comentario."""
    import csv
    return list(csv.DictReader([l for l in open(BR/nombre) if not l.startswith("#")]))
matplotlib.rcParams.update({
    "svg.fonttype":"none",
    "font.family":"Inter",
    "font.size":6.4,
    "text.color":INK,
    "axes.edgecolor":TAUPE, "axes.labelcolor":TAUPE, "axes.labelsize":6.4,
    "xtick.color":TAUPE, "ytick.color":TAUPE,
    "xtick.labelsize":6.6, "ytick.labelsize":6.6,
    "xtick.major.size":0, "ytick.major.size":0,
    "xtick.major.pad":3, "ytick.major.pad":3,
    "legend.fontsize":6.4, "legend.frameon":False,
    "figure.facecolor":GROUND, "axes.facecolor":GROUND, "savefig.facecolor":GROUND,
    "axes.grid":False, "figure.dpi":100,
})

def nb(v, dec=0):
    s = f"{v:,.{dec}f}".replace(",", "\u00a0").replace(".", ",")
    return s.replace("\u00a0", ".")

def pc(v, dec=1):
    return f"{v:.{dec}f}%".replace(".", ",")

def frame(ax, left=True, bottom=True, grid="y"):
    for k, on in (("top",False),("right",False),("left",left),("bottom",bottom)):
        ax.spines[k].set_visible(on)
        if on: ax.spines[k].set_linewidth(.6); ax.spines[k].set_color(HAIR)
    if grid:
        ax.grid(axis=grid, color=HAIR, lw=.5, alpha=.85)
        ax.set_axisbelow(True)

def save(fig, name):
    fig.savefig(OUT/f"{name}.svg", format="svg", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig); print("  ", name)

ZONAS = ["Boulogne\nSur Mer","Béccar","Villa\nAdelina","San Isidro","Martínez","Acassuso"]

# --- 1. cuatro indicadores por zona -----------------------------------------
def g_indicadores():
    nbi=[5.09,4.93,2.73,1.83,1.43,0.94]; clo=[9.16,10.59,5.54,2.97,1.81,2.12]
    gas=[27.64,37.27,15.59,16.64,14.55,19.48]; hac=[12.42,12.67,7.28,4.18,2.96,2.50]
    fig, ax = plt.subplots(figsize=(W,2.25)); frame(ax)
    x=range(6); w=.20
    series=[("% hogares con NBI",nbi,SAGE),("% sin cloaca",clo,OX),
            ("% sin gas de red",gas,AMBER),("% con hacinamiento",hac,PALE)]
    for i,(lbl,v,c) in enumerate(series):
        ax.bar([j+(i-1.5)*w for j in x], v, w, label=lbl, color=c, edgecolor="none")
    ax.set_xticks(list(x)); ax.set_xticklabels(ZONAS)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:.0f}%"))
    ax.set_ylim(0,40)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(.5,1.14), handlelength=.9,
              handleheight=.9, columnspacing=1.4, borderpad=0)
    save(fig,"g_indicadores")

# --- 2. universitario por zona ----------------------------------------------
def g_universitario():
    v=[9.0,12.85,9.32,25.25,24.39,32.28]
    fig, ax = plt.subplots(figsize=(W,1.95)); frame(ax)
    b=ax.bar(ZONAS, v, .56, color=SAGED, edgecolor="none")
    for r,val in zip(b,v):
        ax.text(r.get_x()+r.get_width()/2, val+.8, f"{val:.1f}%".replace(".",","),
                ha="center", va="bottom", fontsize=7, color=INK, fontweight="semibold")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:.0f}%")); ax.set_ylim(0,37)
    save(fig,"g_universitario")

# --- 3. el gasto como proporcion de lo que el Municipio recauda --------------
def g_gasto_real():
    """Un nivel se puede leer como uno quiera segun donde se ponga el cero.
    Un cociente no: el gasto total dividido por lo que el Municipio recauda
    por su cuenta. Solo los siete anios en que las dos series tienen dato."""
    R = {2010:175.559, 2014:205.700, 2015:242.311, 2017:266.317,
         2022:267.591, 2024:232.229, 2025:234.560}          # recursos propios
    G = {2010:308.461, 2014:358.360, 2015:393.186, 2017:461.541,
         2022:382.390, 2024:300.698, 2025:348.876}          # gasto total
    years = list(range(2010, 2026))
    ratio = {y: G[y]/R[y] for y in R}
    base = ratio[2010]

    fig, ax = plt.subplots(figsize=(W, 2.35)); frame(ax)
    for i, y in enumerate(years):
        if y in ratio:
            v = ratio[y]
            col = INK if y == 2010 else (OX if v == min(ratio.values()) else SAGED)
            ax.bar(i, v, .62, color=col, edgecolor="none")
            ax.text(i, v + .03, nb(v, 2), ha="center", va="bottom",
                    fontsize=6.8, color=INK, fontweight="semibold")
        else:
            ax.text(i, .07, "sin dato", ha="center", va="bottom", rotation=90,
                    fontsize=5.4, color=TAUPE, style="italic")
    ax.axhline(base, color=INK, lw=.8, ls=(0, (3, 2.4)), zorder=3)
    ax.text(15.4, base, f"  nivel de 2010\n  {nb(base,2)}", va="center", fontsize=6.6,
            color=INK, fontweight="semibold")
    ax.set_xticks(range(len(years))); ax.set_xticklabels(years)
    ax.set_ylabel("gasto total por cada peso que el Municipio recauda", fontsize=6.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: nb(v, 2)))
    ax.set_ylim(0, 2.05); ax.set_xlim(-.7, 18.4)
    save(fig, "g_gasto_real")

# --- 4. coparticipacion ------------------------------------------------------
def g_copa():
    """Serie completa de data/coparticipacion_comparada.csv (anios de 12 meses)."""
    filas = [r for r in _csv("coparticipacion_comparada.csv") if r["meses"] == "12"]
    S = {}
    for r in filas:
        S.setdefault(r["municipio"].strip(), {})[int(r["anio"])] = float(r["participacion_pct"])
    ROT = {"SAN ISIDRO":("San Isidro",SAGED,0),"TIGRE":("Tigre",OX,.045),
           "VICENTE LOPEZ":("Vicente López",INK,0),"SAN FERNANDO":("San Fernando",PALE,0)}
    fig, ax = plt.subplots(figsize=(W,2.25)); frame(ax, left=False)
    yrs = sorted({a for d in S.values() for a in d})
    for m,(nom,c,nud) in ROT.items():
        if m not in S: continue
        d = S[m]; xs = [a for a in yrs if a in d]; ys = [d[a] for a in xs]
        ax.plot(xs, ys, color=c, lw=1.5, marker="o", ms=2.4, clip_on=False)
        ax.text(xs[-1]+.10, ys[-1]+nud, f"  {nom} {nb(ys[-1],4)}%", va="center",
                fontsize=7, color=c, fontweight="semibold")
    ax.set_xticks(yrs); ax.set_xlim(min(yrs)-.04, max(yrs)+.02)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v,1)+"%"))
    ax.set_ylim(.7,2.05)
    save(fig,"g_copa")

# --- 5. percepcion 2024 / 2025 ----------------------------------------------
def g_percepcion():
    fig, ax = plt.subplots(figsize=(W,2.15)); frame(ax)
    for i,(dev,per,pct,sin) in enumerate([(229946,215023,"93,51%",14922),
                                          (337149,301155,"89,32%",35994)]):
        ax.bar(i, per/1000, .42, color=SAGED, edgecolor="none")
        ax.bar(i, sin/1000, .42, bottom=per/1000, color="none",
               edgecolor=OX, lw=.9, linestyle=(0,(2.2,1.6)))
        ax.text(i, per/2000, f"percibido\n{nb(per)} M\n({pct})", ha="center", va="center",
                fontsize=6.8, color="#F7F2EB", fontweight="semibold")
        ax.text(i, dev/1000+9, f"devengado {nb(dev)} M", ha="center", va="bottom",
                fontsize=6.8, color=INK, fontweight="semibold")
        ax.text(i+.245, per/1000+sin/2000, f"  sin cobrar {nb(sin)} M", ha="left",
                va="center", fontsize=6.8, color=OX, fontweight="semibold")
    ax.set_xticks([0,1]); ax.set_xticklabels(["2024","2025"], fontsize=8.5)
    ax.set_ylabel("miles de millones de pesos de cada año", fontsize=6.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    ax.set_xlim(-.55,1.75); ax.set_ylim(0,385)
    save(fig,"g_percepcion")

# --- 6. de donde viene el deficit -------------------------------------------
def g_cascada():
    """Dos barras, no seis. La pregunta del exhibit es una sola: alcanzaba o
    no alcanzaba para la obra. Se dibuja eso y nada mas."""
    K = 1000.0
    HABIA, OBRA, FALTA = 51781, 57832, 6051
    fig, ax = plt.subplots(figsize=(W, 1.62))
    for k in ("top", "right", "left"): ax.spines[k].set_visible(False)
    ax.spines["bottom"].set_linewidth(.6); ax.spines["bottom"].set_color(HAIR)

    ax.barh(1, HABIA / K, .44, color=SAGED, edgecolor="none")
    ax.text(HABIA / K / 2, 1, nb(HABIA) + " M", ha="center", va="center",
            fontsize=8.2, color="#F7F2EB", fontweight="semibold")

    ax.barh(0, HABIA / K, .44, color=OX, edgecolor="none")
    ax.barh(0, FALTA / K, .44, left=HABIA / K, color=PALEOX, edgecolor="none",
            hatch="////")
    ax.text(HABIA / K / 2, 0, nb(OBRA) + " M", ha="center", va="center",
            fontsize=8.2, color="#F7F2EB", fontweight="semibold")

    ax.plot([HABIA / K] * 2, [-.42, 1.42], color=INK, lw=.7, ls=(0, (2.4, 2)))
    ax.annotate("faltaron " + nb(FALTA) + " M", (OBRA / K, -.30),
                xytext=(10, -16), textcoords="offset points", ha="left",
                fontsize=7.6, color=OX, fontweight="semibold",
                arrowprops=dict(arrowstyle="-", color=OX, lw=.7))

    ax.set_yticks([1, 0])
    ax.set_yticklabels(["Lo que había\npara invertir", "Lo que se invirtió\nen obra"],
                       fontsize=7.6)
    ax.tick_params(axis="y", pad=6)
    ax.set_xlim(0, 66); ax.set_ylim(-.95, 1.52)
    ax.set_xlabel("miles de millones de pesos de 2025", fontsize=6.2)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: nb(v)))
    ax.grid(axis="x", color=HAIR, lw=.5, alpha=.85); ax.set_axisbelow(True)
    save(fig, "g_cascada")

# --- 7. escenarios base / adverso -------------------------------------------
def _modelo():
    d = {}
    for r in _csv("modelo_flujo_caja.csv"):
        d.setdefault(r["escenario"], {})[int(r["anio"])] = float(r["resultado_financiero"])/1e6
    return d

def g_escenarios():
    """Resultado financiero proyectado, de data/modelo_flujo_caja.csv."""
    M = _modelo()
    yrs = sorted(M["base"])
    fig, ax = plt.subplots(figsize=(W,2.5)); frame(ax)
    for esc, col, rot, nud in [("reformista_percepcion", INK, "Con la propuesta,\ncobrando mejor", 1.8),
                               ("base", SAGED, "Sin cambios", -2.8), ("adverso", OX, "Adverso", 0)]:
        if esc not in M: continue
        ys = [M[esc][a]/1000 for a in yrs]
        ax.plot(yrs, ys, color=col, lw=1.6)
        ax.text(yrs[-1]+.20, ys[-1]+nud, " "+rot, fontsize=7.4, color=col,
                fontweight="semibold", va="center")
    ax.axhline(0, color=TAUPE, lw=.7)
    cero = next((a for a in yrs if M["base"][a] >= 0), None)
    cerop = next((a for a in yrs if M.get("reformista_percepcion",{}).get(a,-1) >= 0), None)
    if cerop and cerop != cero:
        ax.annotate(f"con la propuesta\ncruza en {cerop}", (cerop,0), textcoords="offset points",
                    xytext=(-2,14), ha="center", fontsize=6.6, color=INK, fontweight="semibold")
    if cero:
        ax.annotate(f"sin cambios\ncruza en {cero}", (cero,0), textcoords="offset points",
                    xytext=(6,-22), ha="center", fontsize=6.6, color=TAUPE)
    ax.set_xticks(range(min(yrs), max(yrs)+1, 2)); ax.set_xlim(min(yrs), max(yrs)+4.6)
    ax.set_ylabel("resultado financiero, miles de millones dic-2025", fontsize=6.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    save(fig,"g_escenarios")

# --- 8. rigidez del gasto ----------------------------------------------------
def g_rigidez():
    fig, ax = plt.subplots(figsize=(W,1.95))
    for k in ("top","right","left"): ax.spines[k].set_visible(False)
    ax.spines["bottom"].set_linewidth(.6); ax.spines["bottom"].set_color(HAIR)
    segs=[("Personal y deuda\nno se tocan",126488,INK),
          ("Contratos de servicios\nno dentro del ejercicio",110491,SAGE),
          ("Gasto flexible\nreasignable",87326,SAGED)]
    left=0
    for lbl,v,c in segs:
        ax.barh(1.6, v/1000, .46, left=left/1000, color=c, edgecolor="none")
        ax.text(left/1000, 2.05, lbl+f"\n{nb(v)} M · " + pc(v/324305*100),
                fontsize=6.6, color=INK, fontweight="semibold", va="bottom")
        left+=v
    ax.barh(.72, 7225/1000, .30, left=224979/1000, color=OX, edgecolor="none")
    ax.text(224979/1000-3, .72, "programa de empleo y vivienda: 7.225 M, el 8,3% del flexible  ",
            ha="right", va="center", fontsize=6.6, color=OX, fontweight="semibold")
    ax.barh(.20, 28908/1000, .30, left=224979/1000, color=SAGED, edgecolor="none")
    ax.text(224979/1000-3, .20, "obra pública vecinal: 28.908 M, el 33,1% del flexible  ",
            ha="right", va="center", fontsize=6.6, color=SAGED, fontweight="semibold")
    ax.plot([224979/1000]*2,[0,1.35], color=TAUPE, lw=.6, ls=(0,(2,2)))
    ax.set_yticks([]); ax.set_xlim(0,330); ax.set_ylim(-.1,2.55)
    ax.set_xlabel("miles de millones de pesos devengados en 2025", fontsize=6.2)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    save(fig,"g_rigidez")

# --- 9. base vs reformista ---------------------------------------------------
def g_reformista():
    """Base contra reformista cobrando mejor, de data/modelo_flujo_caja.csv."""
    M = _modelo()
    yrs = sorted(M["base"])
    base = [M["base"][a]/1000 for a in yrs]
    ref  = [M["reformista_percepcion"][a]/1000 for a in yrs]
    fig, ax = plt.subplots(figsize=(W,2.5)); frame(ax)
    ax.fill_between(yrs, base, ref, color=SAGED, alpha=.16, linewidth=0)
    ax.plot(yrs, ref, color=SAGED, lw=1.8)
    ax.plot(yrs, base, color=INK, lw=1.5)
    ax.text(yrs[-1]+.20, ref[-1], " Con la propuesta,\n cobrando mejor", fontsize=7.4,
            color=SAGED, fontweight="semibold", va="center")
    ax.text(yrs[-1]+.20, base[-1]-2.4, " Sin cambios", fontsize=7.4, color=INK,
            fontweight="semibold", va="center")
    ax.axhline(0, color=TAUPE, lw=.7)
    ax.set_xticks(range(min(yrs), max(yrs)+1, 2)); ax.set_xlim(min(yrs), max(yrs)+4.6)
    ax.set_ylabel("resultado financiero, miles de millones dic-2025", fontsize=6.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    save(fig,"g_reformista")

# --- 10. tornado de sensibilidad --------------------------------------------
def g_tornado():
    rows=[("Recursos propios: 2,95% anual",13990),("Recursos propios: 0,95% anual",-13321),
          ("Percepción de recursos: 86,32%",-10680),("Percepción de recursos: 92,32%",10652),
          ("Coparticipación: −3,5% anual",-4861),("Coparticipación: −1,5% anual",2731),
          ("Coparticipación: −2,5% anual",-1163),("Percepción de recursos: 89,32%",-14)]
    fig, ax = plt.subplots(figsize=(W,2.3)); frame(ax, grid="x")
    y=range(len(rows))[::-1]
    for yy,(lbl,v) in zip(y,rows):
        ax.barh(yy, v/1000, .52, color=(SAGED if v>0 else OX), edgecolor="none")
        ax.text(v/1000 + (1.1 if v>0 else -1.1), yy,
                ("+" if v>0 else "\u2212")+nb(abs(v))+" M",
                ha="left" if v>0 else "right", va="center",
                fontsize=6.8, color=INK, fontweight="semibold")
    ax.set_yticks(list(y)); ax.set_yticklabels([r[0] for r in rows], fontsize=7)
    ax.axvline(0, color=TAUPE, lw=.7)
    ax.set_xlim(-19,19)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    ax.set_xlabel("efecto sobre el resultado financiero de 2031, miles de millones", fontsize=6.2)
    save(fig,"g_tornado")

# --- 11. obra vecinal, año 1 y año 4 ----------------------------------------
def g_obra():
    TOT = 57816
    fig, ax = plt.subplots(figsize=(W, 1.85))
    for k in ("top","right","left"): ax.spines[k].set_visible(False)
    ax.spines["bottom"].set_linewidth(.6); ax.spines["bottom"].set_color(HAIR)
    for i,(lbl,vec,eje) in enumerate([("Año 1",7227,50589),("Año 4",28908,28908)]):
        y = 1-i
        ax.barh(y, vec/1000, .40, color=SAGED, edgecolor="none")
        ax.barh(y, eje/1000, .40, left=vec/1000, color=PALE, edgecolor="none")
        tv = f"deciden los vecinos\n{nb(vec)} M  ·  " + pc(vec/TOT*100)
        te = f"decide el Ejecutivo\n{nb(eje)} M  ·  " + pc(eje/TOT*100)
        # si el tramo verde es angosto, la etiqueta va arriba y no adentro
        if vec/TOT < .20:
            ax.text(0, y+.26, tv.replace("\n", ": "), ha="left", va="bottom",
                    fontsize=6.8, color=SAGED, fontweight="semibold")
        else:
            ax.text(vec/2000, y, tv, ha="center", va="center",
                    fontsize=6.8, color="#F7F2EB", fontweight="semibold")
        ax.text(vec/1000+eje/2000, y, te, ha="center", va="center",
                fontsize=6.8, color=INK, fontweight="semibold")
    ax.set_yticks([1,0]); ax.set_yticklabels(["Año 1","Año 4"], fontsize=8.5)
    ax.set_xlim(0,58); ax.set_ylim(-.55,1.72)
    ax.set_xlabel("miles de millones de pesos de diciembre de 2025", fontsize=6.2)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    save(fig,"g_obra")

# --- 12. reparto vecinal por zona -------------------------------------------
def g_reparto():
    z=["Béccar","Boulogne\nSur Mer","Villa\nAdelina","San Isidro","Acassuso","Martínez"]
    v=[123782,114508,89987,81297,74962,72285]
    col=[OX,OX,SAGED,SAGED,SAGED,SAGED]
    fig, ax = plt.subplots(figsize=(W,2.0)); frame(ax)
    b=ax.bar(z,[x/1000 for x in v], .56, color=col, edgecolor="none")
    for r,val in zip(b,v):
        ax.text(r.get_x()+r.get_width()/2, val/1000+2.5, nb(val),
                ha="center", va="bottom", fontsize=7.2, color=INK, fontweight="semibold")
    ax.set_ylabel("miles de pesos de dic-2025 por habitante", fontsize=6.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    ax.set_ylim(0,142)
    save(fig,"g_reparto")

# --- 13. gasto por funcion ---------------------------------------------------
FUNC=[("Salud",78217,24.1),("Urbanismo",70310,21.7),("Transporte",36356,11.2),
 ("Dirección superior ejecutiva",32552,10.0),("Seguridad interna",32446,10.0),
 ("Servicios de la deuda pública",14898,4.6),("Educación y cultura",13986,4.3),
 ("Vivienda y urbanismo",12336,3.8),("Ciencia y técnica",8155,2.5),
 ("Promoción y asistencia social",5914,1.8),("Legislativa",4571,1.4),
 ("Relaciones con la comunidad",4040,1.2),("Agua potable y alcantarillado",3320,1.0),
 ("Administración fiscal",2241,0.7),("Comercio, turismo y otros",2216,0.7),
 ("Ecología y medio ambiente",1410,0.4),("Judicial",727,0.2),
 ("Control de la gestión pública",267,0.1),("Trabajo",170,0.1)]
def g_funcion():
    fig, ax = plt.subplots(figsize=(W,3.5)); frame(ax, grid="x")
    y=range(len(FUNC))[::-1]
    for yy,(lbl,v,p) in zip(y,FUNC):
        c = OX if lbl in ("Agua potable y alcantarillado","Ecología y medio ambiente") else SAGED
        ax.barh(yy, v/1000, .58, color=c, edgecolor="none")
        ax.text(v/1000+1.6, yy, f"{nb(v)} M   " + pc(p), ha="left",
                va="center", fontsize=6.8, color=(OX if c==OX else INK), fontweight="semibold")
    ax.set_yticks(list(y)); ax.set_yticklabels([f[0] for f in FUNC], fontsize=7)
    ax.set_xlim(0,108)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    ax.set_xlabel("miles de millones de pesos devengados en 2025", fontsize=6.2)
    save(fig,"g_funcion")

# --- 14. variacion real por funcion -----------------------------------------
def g_variacion():
    rows=[("Servicios de la deuda pública",36.3),("Seguridad interna",34.8),
          ("Ecología y medio ambiente",23.1),("Salud",8.2),("Legislativa",-5.5),
          ("Educación y cultura",-11.6),("Urbanismo",-21.5),
          ("Dirección superior ejecutiva",-28.7),("Promoción y asistencia social",-32.5)]
    fig, ax = plt.subplots(figsize=(W,2.5)); frame(ax, grid="x")
    y=range(len(rows))[::-1]
    for yy,(lbl,v) in zip(y,rows):
        ax.barh(yy, v, .58, color=(SAGED if v>0 else OX), edgecolor="none")
        ax.text(v + (1.3 if v>0 else -1.3), yy, f"{v:+.1f}%".replace(".",",").replace("+","+"),
                ha="left" if v>0 else "right", va="center", fontsize=7.2,
                color=INK, fontweight="semibold")
    ax.set_yticks(list(y)); ax.set_yticklabels([r[0] for r in rows], fontsize=7)
    ax.axvline(0, color=TAUPE, lw=.7); ax.set_xlim(-46,48)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:.0f}%"))
    save(fig,"g_variacion")

# --- 15. empleo y vivienda contra el resto ----------------------------------
def g_empleo():
    """A escala real las dos partidas miden medio pixel. Arriba va el
    presupuesto entero con el tramo marcado; abajo, ese tramo ampliado."""
    RESTO, VIV, EMP = 308730.0, 335.4, 170.3
    TOT = RESTO + VIV + EMP
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(W, 2.05),
                                 gridspec_kw=dict(height_ratios=[1, 1], hspace=1.55))
    for ax in (a1, a2):
        for k in ("top","right","left"): ax.spines[k].set_visible(False)
        ax.spines["bottom"].set_linewidth(.6); ax.spines["bottom"].set_color(HAIR)
        ax.set_yticks([]); ax.set_ylim(-.62, .62)

    a1.barh(0, TOT/1000, .50, color=SAGED, edgecolor="none")
    a1.text(RESTO/2000, 0, "Todo el resto del presupuesto   " + nb(RESTO) + " M  ·  99,84%",
            ha="center", va="center", fontsize=7, color="#F7F2EB", fontweight="semibold")
    a1.plot([RESTO/1000]*2, [-.33, .33], color=OX, lw=1.4, solid_capstyle="butt", zorder=3)
    a1.annotate("acá están las dos partidas: 0,16% del presupuesto",
                (RESTO/1000, .33), xytext=(-6, 13), textcoords="offset points",
                ha="right", fontsize=6.9, color=OX, fontweight="semibold",
                arrowprops=dict(arrowstyle="-", color=OX, lw=.6, shrinkA=0, shrinkB=1))
    a1.set_xlim(0, TOT/1000*1.004)
    a1.xaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    a1.set_xlabel("miles de millones de pesos devengados en 2025", fontsize=6.2, labelpad=2)

    a2.barh(0, VIV, .50, color=SAGE, edgecolor="none")
    a2.barh(0, EMP, .50, left=VIV, color=OX, edgecolor="none")
    a2.text(VIV/2, 0, "Vivienda  335,4 M", ha="center", va="center",
            fontsize=7, color="#F7F2EB", fontweight="semibold")
    a2.text(VIV+EMP/2, 0, "Empleo  170,3 M", ha="center", va="center",
            fontsize=7, color="#F7F2EB", fontweight="semibold")
    a2.text(0, .80, "ese 0,16%, ampliado: las dos partidas juntas suman 505,7 millones",
            fontsize=6.9, color=TAUPE, style="italic", va="bottom")
    a2.set_xlim(0, (VIV+EMP)*1.004)
    a2.xaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    a2.set_xlabel("millones de pesos devengados en 2025", fontsize=6.2, labelpad=2)
    save(fig,"g_empleo")

# --- 16. hogares sin gas de red ---------------------------------------------
def g_gas():
    z=["Béccar","Boulogne\nSur Mer","Martínez","San Isidro","Villa\nAdelina","Acassuso"]
    v=[8221,6947,3806,3221,2034,936]; col=[OX,OX,SAGED,SAGED,SAGED,SAGED]
    fig, ax = plt.subplots(figsize=(W,2.0)); frame(ax)
    b=ax.bar(z,v,.56,color=col,edgecolor="none")
    for r,val in zip(b,v):
        ax.text(r.get_x()+r.get_width()/2, val+180, nb(val), ha="center", va="bottom",
                fontsize=7.2, color=INK, fontweight="semibold")
    ax.set_ylabel("hogares", fontsize=6.2); ax.set_ylim(0,9600)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:nb(v)))
    save(fig,"g_gas")

# --- 17. medidas de transparencia -------------------------------------------
def g_transparencia():
    rows=[("Publicar compras, contrataciones y licitaciones","No existe","no está en el portal de transparencia"),
          ("Publicar el organigrama municipal","No existe","no está en el portal de transparencia"),
          ("Publicar la planta de personal y la escala salarial","No existe","no está en el portal de transparencia"),
          ("Publicar las declaraciones juradas de funcionarios","Enlace incorrecto","lleva a declaraciones de contribuyentes"),
          ("Reponer el Portal de Datos Abiertos o publicar sus datasets","Caído","devuelve error 504"),
          ("Publicar la Ordenanza Fiscal e Impositiva vigente","Desactualizado","la última publicada es de 2024"),
          ("Publicar la rendición de cuentas","Desactualizado","la última publicada es de 2022")]
    fig, ax = plt.subplots(figsize=(W,2.35)); ax.axis("off")
    ax.text(0,1.035,"cumplidas hoy: 0 de 7", fontsize=6.6, color=TAUPE, transform=ax.transAxes)
    n=len(rows)
    for i,(m,st,det) in enumerate(rows):
        y=1-(i+1)/n*0.96
        ax.add_patch(plt.Rectangle((0.004,y+0.031),0.017,0.038, transform=ax.transAxes,
                     fill=False, ec=INK, lw=.8, clip_on=False))
        ax.text(0.038,y+0.049,m, fontsize=7.4, color=INK, va="center", transform=ax.transAxes)
        ax.text(0.038,y+0.008,st, fontsize=6.8, color=OX, fontweight="semibold",
                va="center", transform=ax.transAxes)
        ax.text(0.30,y+0.008,det, fontsize=6.6, color=TAUPE, va="center", transform=ax.transAxes)
        ax.plot([0,1],[y-0.012]*2, color=HAIR, lw=.6, transform=ax.transAxes, clip_on=False)
    save(fig,"g_transparencia")

# --- 18. peso de la obra publica contra los 106 -----------------------------
def g_dots():
    """Los 106 municipios, cada uno una marca sobre el eje. Se ve de un vistazo
    donde esta el grueso, donde la mediana y donde San Isidro.
    Datos: RAFAM 2025, data/rafam_2025_municipios.csv.
    El panel del peso del personal salio con la correccion 119: se leia como
    elogio de eficiencia, que no es lo que este capitulo dice."""
    import csv
    lineas = [l for l in open(BR/"rafam_2025_municipios.csv") if not l.startswith("#")]
    muni = list(csv.DictReader(lineas))
    obr = sorted(float(m["pct_obra"]) for m in muni)
    MED_O = 5.4397
    si = next(m for m in muni if m["municipio"].strip().lower().startswith("san isidro"))
    SI_O = float(si["pct_obra"])

    fig, a2 = plt.subplots(1, 1, figsize=(W, 1.05))
    paneles = [
        (a2, obr, MED_O, SI_O, int(si["puesto_obra"]), 26,
         "Peso de la obra pública", "bienes de uso sobre gasto devengado",
         "de 106 municipios, San Isidro es el 4º que más invierte en obra"),
    ]
    for ax, vals, med, mio, puesto, xmax, tit, sub, pie in paneles:
        for k in ("top","right","left"): ax.spines[k].set_visible(False)
        ax.spines["bottom"].set_linewidth(.6); ax.spines["bottom"].set_color(HAIR)
        ax.set_yticks([])
        # cada municipio, una marca
        for v in vals:
            ax.plot([v, v], [0, .40], color=SAGED, lw=.7, alpha=.55,
                    solid_capstyle="butt", zorder=2)
        # la mediana
        ax.plot([med, med], [-.10, .74], color=INK, lw=.9, ls=(0,(2.4,2)), zorder=3)
        ax.text(med, .80, "mediana  " + nb(med,1) + "%", ha="center", va="bottom",
                fontsize=6.4, color=INK, zorder=4)
        # San Isidro
        ax.plot([mio, mio], [0, .40], color=OX, lw=2.2, solid_capstyle="butt", zorder=5)
        ax.scatter([mio], [.40], s=16, color=OX, edgecolors="none", zorder=6)
        ax.annotate("San Isidro  " + nb(mio,1) + "%", (mio, .40),
                    xytext=(0, 16), textcoords="offset points", ha="center",
                    fontsize=7, color=OX, fontweight="semibold", zorder=7,
                    arrowprops=dict(arrowstyle="-", color=OX, lw=.6, shrinkA=1, shrinkB=2))
        # rotulo y bajada con distancia fija en puntos sobre el borde del eje:
        # con un solo panel, el pad del titulo y la bajada en fraccion del eje
        # caian en la misma linea (correccion 124)
        ax.annotate(tit, (0, 1), xycoords="axes fraction", xytext=(0, 13),
                    textcoords="offset points", va="bottom", fontsize=7.2,
                    color=INK, fontweight="semibold")
        ax.annotate(sub, (0, 1), xycoords="axes fraction", xytext=(0, 3),
                    textcoords="offset points", va="bottom", fontsize=6.4,
                    color=TAUPE)
        ax.set_xlim(0, xmax); ax.set_ylim(-.18, 1.05)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.0f}%"))
        ax.set_xlabel(pie, fontsize=6.3, labelpad=2)
    save(fig, "g_dots")


# ============================================================================
#  MAPAS
#  El partido es una banda diagonal: sin girar, la mitad del cuadro queda vacia.
#  Girando -33 grados la mancha llena el 85% del marco en vez del 49%, y el mapa
#  baja de ~590 pt de alto a ~360. La rosa de los vientos gira lo mismo, asi que
#  el norte sigue siendo el norte.
# ============================================================================
import math as _m
AGUA="#DCE2E3"; VECINO="#EAE5DC"; VIA="#D2C7B3"; GIRO=-33.0

def _proyector(kx, cx, cy, ang=GIRO):
    a = _m.radians(ang); ca, sa = _m.cos(a), _m.sin(a)
    def f(c):
        x = c[0]*kx - cx; y = c[1] - cy
        return (x*ca - y*sa, x*sa + y*ca)
    return f

def _capas(ax, proj, clip):
    import json
    from shapely.geometry import shape
    from matplotlib.patches import Polygon as MPoly
    from matplotlib.collections import PatchCollection
    def relleno(path, color, z):
        pats=[]
        for f in json.load(open(BR/path))["features"]:
            g = shape(f["geometry"]).intersection(clip)
            if g.is_empty: continue
            for q in ([g] if g.geom_type=="Polygon" else list(getattr(g,"geoms",[]))):
                if q.geom_type=="Polygon":
                    pats.append(MPoly([proj(c) for c in q.exterior.coords], closed=True))
        ax.add_collection(PatchCollection(pats, facecolors=color, edgecolors="none", zorder=z))
    relleno("partidos_vecinos_osm.geojson", VECINO, 0)
    relleno("agua_rio_de_la_plata_osm.geojson", AGUA, 0)
    for f in json.load(open(BR/"vias_principales_osm.geojson"))["features"]:
        if f["properties"].get("clase") not in ("autopista","ferrocarril"): continue
        g = shape(f["geometry"]).intersection(clip)
        for q in ([g] if g.geom_type=="LineString" else list(getattr(g,"geoms",[]))):
            if q.geom_type=="LineString" and not q.is_empty:
                xs, ys = zip(*[proj(c) for c in q.coords])
                ax.plot(xs, ys, color=VIA, lw=.4, zorder=1, solid_capstyle="round")

def _rosa(ax, x, y, h):
    a = _m.radians(GIRO)
    dx, dy = -_m.sin(a)*h, _m.cos(a)*h
    ax.annotate("", (x+dx, y+dy), (x, y),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=.85), zorder=9)
    ax.text(x+dx*1.34, y+dy*1.34, "N", ha="center", va="center", fontsize=6.4,
            color=INK, fontweight="semibold", zorder=9)

def _escala(ax, x, y, kx, alto):
    km2 = 2/111.32 * kx
    a = _m.radians(GIRO)
    dx, dy = _m.cos(a)*km2, _m.sin(a)*km2
    ax.plot([x, x+dx], [y, y+dy], color=INK, lw=1.4, zorder=9, solid_capstyle="butt")
    ax.text(x+dx/2 - _m.sin(a)*alto*.022, y+dy/2 + _m.cos(a)*alto*.022, "2 km",
            ha="center", va="bottom", fontsize=6.1, color=INK, zorder=9, rotation=GIRO)

def _marco(ax, geom, ancho_pt, margen=.02):
    x0,y0,x1,y1 = geom.bounds
    mx = (x1-x0)*margen; my = (y1-y0)*margen
    ax.set_xlim(x0-mx, x1+mx); ax.set_ylim(y0-my, y1+my)
    return (x1-x0+2*mx), (y1-y0+2*my)


def g_mapa_zonas():
    """Seis bloques de color: no necesita el ancho entero de la columna.
    Mapa a la izquierda, tabla de la leyenda a la derecha."""
    import json
    import matplotlib.patheffects as pe
    from matplotlib.patches import Polygon as MPoly
    from matplotlib.collections import PatchCollection
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    from shapely.geometry import shape, box
    from shapely.ops import unary_union

    geo = json.load(open(BR/"zonas_propuestas_sanisidro.geojson"))
    NOM = {"Beccar":"Béccar","Martinez":"Martínez"}
    val = {f["properties"]["zona"]: f["properties"]["pct_nbi"] for f in geo["features"]}
    formas = {f["properties"]["zona"]: shape(f["geometry"]) for f in geo["features"]}
    todo = unary_union(list(formas.values()))
    b = todo.bounds
    kx = _m.cos(_m.radians((b[1]+b[3])/2))
    cx, cy = todo.centroid.x*kx, todo.centroid.y
    proj = _proyector(kx, cx, cy)
    clip = box(b[0]-.06, b[1]-.06, b[2]+.06, b[3]+.06)

    ramp = LinearSegmentedColormap.from_list("nbi", ["#FBF8F3","#E4C6BC","#B4675A","#7C2E23"])
    norm = Normalize(0.9, 5.1)

    fig, (ax, lg) = plt.subplots(1, 2, figsize=(W, W*0.285),
                                 gridspec_kw=dict(width_ratios=[.685,.315], wspace=.02))
    for a_ in (ax, lg): a_.set_axis_off()
    ax.set_aspect("equal")
    _capas(ax, proj, clip)

    pats, cols = [], []
    for z, g in formas.items():
        for q in ([g] if g.geom_type=="Polygon" else list(g.geoms)):
            pats.append(MPoly([proj(c) for c in q.exterior.coords], closed=True))
            cols.append(ramp(norm(val[z])))
    ax.add_collection(PatchCollection(pats, facecolors=cols, edgecolors="#F5F0E8",
                                      linewidths=.7, zorder=2))
    gir = unary_union([shape(f["geometry"]) for f in geo["features"]])
    for q in ([gir] if gir.geom_type=="Polygon" else list(gir.geoms)):
        xs, ys = zip(*[proj(c) for c in q.exterior.coords])
        ax.plot(xs, ys, color=TAUPE, lw=.7, zorder=3)

    from shapely.geometry import Polygon as SPoly
    proyectado = SPoly([proj(c) for c in
                        (gir if gir.geom_type=="Polygon" else max(gir.geoms, key=lambda g:g.area)).exterior.coords])
    AN, AL = _marco(ax, proyectado, W, margen=.055)

    for z, g in formas.items():
        c = g.representative_point(); x, y = proj((c.x, c.y))
        osc = val[z] > 3.2
        ax.text(x, y, NOM.get(z,z), ha="center", va="center", fontsize=6.6,
                color=("#F7F2EB" if osc else INK), fontweight="semibold", zorder=6,
                path_effects=[pe.withStroke(linewidth=2.0,
                              foreground=("#6B2B22" if osc else "#FBF8F3"))])

    xa,xb=ax.get_xlim(); ya,yb=ax.get_ylim()
    _escala(ax, xa+AN*.025, ya+AL*.045, kx, AL)
    _rosa(ax, xb-AN*.05, ya+AL*.10, AL*.16)

    # la leyenda es una tabla, ordenada de peor a mejor
    lg.set_xlim(0,1); lg.set_ylim(0,1)
    lg.text(.06, .955, "% DE HOGARES CON NBI", fontsize=6.1, color=AMBER,
            fontweight="semibold", va="top")
    orden = sorted(val, key=lambda z:-val[z])
    for i, z in enumerate(orden):
        yy = .845 - .128*i
        lg.add_patch(plt.Rectangle((.06, yy-.037), .075, .075,
                     color=ramp(norm(val[z])), ec=HAIR, lw=.4))
        lg.text(.175, yy, NOM.get(z,z), fontsize=6.7, color=INK, va="center")
        lg.text(.98, yy, nb(val[z],2)+"%", fontsize=6.7, color=INK, va="center",
                ha="right", fontweight="semibold")
        lg.plot([.06,.98],[yy-.055]*2, color=HAIR, lw=.4)
    lg.text(.06, .045, "el partido promedia 3,16%", fontsize=6.1, color=TAUPE,
            style="italic", va="center")
    save(fig, "g_mapa_zonas")


def g_mapa_radios():
    """Los 360 radios, a ancho de columna porque el detalle es el argumento."""
    import csv, json
    import matplotlib.patheffects as pe
    from matplotlib.patches import Polygon as MPoly
    from matplotlib.collections import PatchCollection
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    from shapely.geometry import shape, box, Polygon as SPoly
    from shapely.ops import unary_union

    censo = {r["radio_id"]: r for r in csv.DictReader(open(BR/"censo2022_sanisidro_por_radio.csv"))}
    geo = json.load(open(BR/"radios_censales_sanisidro.geojson"))
    def pct(rid):
        r = censo.get(rid)
        if not r: return 0.0
        t=int(r["hogares_nbi__total"] or 0); si=int(r["hogares_nbi__si"] or 0)
        return si/t*100 if t else 0.0
    f32 = sorted([k for k in censo if k[5:7]=="32"], key=lambda k:-pct(k))[:9]

    todo = unary_union([shape(f["geometry"]) for f in geo["features"]])
    b = todo.bounds
    kx = _m.cos(_m.radians((b[1]+b[3])/2))
    cx, cy = todo.centroid.x*kx, todo.centroid.y
    proj = _proyector(kx, cx, cy)
    clip = box(b[0]-.06, b[1]-.06, b[2]+.06, b[3]+.06)

    ramp = LinearSegmentedColormap.from_list("nbi", ["#FBF8F3","#E4C6BC","#B4675A","#7C2E23"])
    norm = Normalize(0, 26.6)

    fig, ax = plt.subplots(figsize=(W*0.88, W*0.88*0.62))
    ax.set_axis_off(); ax.set_aspect("equal")
    _capas(ax, proj, clip)

    pats, cols, nueve = [], [], []
    for f in geo["features"]:
        rid=f["properties"]["radio_id"]; g=shape(f["geometry"])
        for q in ([g] if g.geom_type=="Polygon" else list(g.geoms)):
            pats.append(MPoly([proj(c) for c in q.exterior.coords], closed=True))
            cols.append(ramp(norm(pct(rid))))
        if rid in f32: nueve.append(g)
    ax.add_collection(PatchCollection(pats, facecolors=cols, edgecolors="#FFFFFF",
                                      linewidths=.16, zorder=2))
    for q in ([todo] if todo.geom_type=="Polygon" else list(todo.geoms)):
        xs, ys = zip(*[proj(c) for c in q.exterior.coords])
        ax.plot(xs, ys, color=TAUPE, lw=.7, zorder=3)
    cong = unary_union(nueve)
    for q in ([cong] if cong.geom_type=="Polygon" else list(cong.geoms)):
        xs, ys = zip(*[proj(c) for c in q.exterior.coords])
        ax.plot(xs, ys, color=INK, lw=1.4, zorder=5)

    proyectado = SPoly([proj(c) for c in
        (todo if todo.geom_type=="Polygon" else max(todo.geoms,key=lambda g:g.area)).exterior.coords])
    AN, AL = _marco(ax, proyectado, W, margen=.025)
    xa,xb=ax.get_xlim(); ya,yb=ax.get_ylim()
    ax.set_ylim(ya + AL*.02, yb + AL*.15)
    xa,xb=ax.get_xlim(); ya,yb=ax.get_ylim()
    def X(f): return xa+(xb-xa)*f
    def Y(f): return ya+(yb-ya)*f

    zonas = json.load(open(BR/"zonas_propuestas_sanisidro.geojson"))
    NOM = {"Beccar":"Béccar","Martinez":"Martínez"}
    for f in zonas["features"]:
        z=f["properties"]["zona"]; c=shape(f["geometry"]).representative_point()
        x,y = proj((c.x,c.y))
        ax.text(x, y, NOM.get(z,z), ha="center", va="center", fontsize=6.5, color=INK,
                fontweight="semibold", zorder=6,
                path_effects=[pe.withStroke(linewidth=2.1, foreground="#FBF8F3")])

    cc = cong.centroid; kxp = proj((cc.x, cc.y))
    ax.annotate("fracción censal 32\n9 radios · 8.749 hab\nel peor NBI del partido",
                kxp, xytext=(X(.735), Y(.235)), textcoords="data",
                ha="left", va="center", fontsize=6.4, color=INK, fontweight="semibold",
                zorder=7, bbox=dict(boxstyle="square,pad=.38", fc=GROUND, ec=INK, lw=.6),
                arrowprops=dict(arrowstyle="-", color=INK, lw=.6, shrinkA=3, shrinkB=3))

    lw_=(xb-xa)*.30; lx=X(.014); ly=Y(.945); lh=(yb-ya)*.017
    ax.add_patch(plt.Rectangle((lx-(xb-xa)*.010, ly-(yb-ya)*.036), lw_+(xb-xa)*.020,
                 (yb-ya)*.105, color=GROUND, ec="none", zorder=7))
    for i in range(140):
        ax.add_patch(plt.Rectangle((lx+lw_*i/140, ly), lw_/140*1.06, lh,
                     color=ramp(i/139), lw=0, zorder=8))
    ax.add_patch(plt.Rectangle((lx, ly), lw_, lh, fill=False, ec=TAUPE, lw=.4, zorder=9))
    ax.text(lx, ly+lh*1.9, "% DE HOGARES CON NBI, POR RADIO CENSAL", fontsize=5.5,
            color=AMBER, fontweight="semibold", zorder=9)
    ax.text(lx, ly-lh*.55, "0,0%", fontsize=5.8, color=TAUPE, va="top", zorder=9)
    ax.text(lx+lw_, ly-lh*.55, "26,6%", fontsize=5.8, color=TAUPE, va="top",
            ha="right", zorder=9)
    ax.text(X(.988), Y(.60), "RÍO DE LA PLATA", rotation=-72, ha="right", va="center",
            fontsize=6.2, color="#8FA1A4", style="italic", zorder=4)
    _escala(ax, X(.012), Y(.075), kx, (yb-ya))
    _rosa(ax, X(.952), Y(.10), (yb-ya)*.10)
    save(fig, "g_mapa_radios")


if __name__ == "__main__":
    print("graficos:")
    for f in (g_indicadores,g_universitario,g_gasto_real,g_copa,g_percepcion,g_cascada,
              g_escenarios,g_rigidez,g_reformista,g_tornado,g_obra,g_reparto,g_funcion,
              g_variacion,g_empleo,g_gas,g_dots,g_mapa_radios,g_mapa_zonas):
        f()
