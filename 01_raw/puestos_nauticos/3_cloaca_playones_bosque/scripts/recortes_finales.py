# Recortes finales por puesto con las superficies candidatas marcadas + CSV de mediciones [cálculo propio; lo que sale de
# imagen es "probable"]. Imagen: Esri World Imagery (Vantor WV03 0,31 m, 03/01/2026; en 33 Orientales WV02 0,5 m, 28/12/2025).
import sys, csv, json
sys.path.insert(0,'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/u1_cloaca_playones_bosque/scripts')
from medir import medir
from zoom import zoom
from franja import franja
from transectas import way_ll
from geo import *
from shapely.geometry import LineString, Polygon
from shapely.ops import substring
G=(0,230,0); Y=(255,220,0); O=(255,120,0); M=(255,0,255); C=(0,200,255)
def strip(sitio,wid,half,s0=None,s1=None,quitar_pp=True):
    I=Img(sitio); L=LineString([I.ll2m(la,lo) for la,lo in way_ll(wid)])
    if s0 is not None: L=substring(L,s0,s1)
    b=L.buffer(half,cap_style=2)
    if quitar_pp: b=b.difference(Polygon([I.ll2m(la,lo) for la,lo in pp_polygon_ll()]).buffer(5))
    g=max(getattr(b,'geoms',[b]),key=lambda x:x.area)
    return list(g.exterior.coords)
S={
 '1_aguila':dict(crop=(-170,-80,70,90),polys=[
   ('A1','Playón pavimentado del Parque Águila Chico (en OSM, 545 m²)',[(-72,-17),(-58,-4),(-25,-25),(-35,-38)],G),
   ('A2','Lote de tierra/ripio al NO, con autos (en OSM como "ground", 961 m²)',[(-140,30),(-115,52),(-100,38),(-98,15),(-110,8),(-128,15)],O)]),
 '2_saenzpena':dict(crop=(-130,-40,90,110),polys=[
   ('B1','Playón de hormigón junto al muelle (en OSM, 1.585 m²)',[(-15,22),(57,13),(38,-22),(-17,4)],G),
   ('B2','Playón abierto al O de la rotonda (NO está en OSM)',[(-95,48),(-80,57),(-45,57),(-37,42),(-42,28),(-75,24),(-95,33)],Y)]),
 'BA_bosque_alegre':dict(crop=(-200,-170,60,130),polys=[
   ('C1','Calle ancha (Stella Maris en OSM): franja ±12 m del eje, menos el Paisaje Protegido + 5 m',None,M),
   ('C2','Explanada final de la calle, junto al río',[(-80,82),(-62,72),(-35,95),(-18,108),(-14,113),(-25,121),(-45,112),(-70,96)],Y),
   ('C3','Lote de ripio del Centro Municipal de Exposiciones',[(-142,-28),(-128,-10),(-110,-3),(-95,-5),(-88,-15),(-90,-35),(-105,-45),(-125,-45),(-140,-38)],O),
   ('C4','Vuelta de Obligado, últimos 150 m antes del cruce (±10 m del eje)',None,C)]),
 '4_puerto':dict(crop=(-70,-90,110,90),polys=[
   ('D1','Explanada de acceso al Parque Público del Puerto',[(-18,-5),(0,-3),(5,-12),(10,-25),(6,-40),(-5,-48),(-15,-40),(-20,-20)],Y),
   ('D2','Lote de ripio al NE (se ven 2 colectivos)',[(10,52),(20,58),(60,52),(62,32),(30,28),(12,38)],O),
   ('D3','Plazoleta parcialmente pavimentada al SO de la rotonda',[(-55,-48),(-20,-50),(-15,-68),(-45,-72)],G)]),
 '5_33orientales':dict(crop=(-130,-40,10,70),polys=[
   ('E1','Plaza dura al final de la calle (parte del Paseo)',[(-50,0),(-42,15),(-28,20),(-18,12),(-20,-12),(-35,-18),(-48,-10)],Y)]),
 '6_pacheco':dict(crop=(-45,-110,85,45),polys=[
   ('F1','Playón "Paseo Público Costero" (en OSM, 1.419 m²)',[(-11,-27),(15,-19),(5,-57),(12,-72),(5,-97),(-9,-97)],G),
   ('F2','Ripio al NE del playón, con autos (camino de servicio en OSM, sin área)',[(1,-29),(12,-17),(30,-10),(40,-14),(30,-26),(14,-34),(6,-40)],O)]),
}
rows=[]
for sitio,cfg in S.items():
    polys=[]
    for pid,desc,pts,col in cfg['polys']:
        if pid=='C1': pts=strip(sitio,'133213059',12)
        if pid=='C4': pts=strip(sitio,'36352224',10,250,400,quitar_pp=False)
        r=medir(sitio,pts); polys.append((pid,pts,col))
        extra=''
        if pid=='C1': extra=json.dumps(franja(sitio,'133213059'),ensure_ascii=False)
        if pid=='C4': extra=json.dumps(franja(sitio,'36352224',half=10,s0=250,s1=400),ensure_ascii=False)
        rows.append(dict(sitio=sitio,id=pid,descripcion=desc,area_poligono_m2=r['area_poligono_m2'],area_sin_vegetacion_m2=r['area_sin_veg_m2'],
            rgb_medio=' '.join(map(str,r['rgb_medio'])),parcelas_ARBA_cca_item_pct=' ; '.join(f'{c} (convenio ítem {it})' if it else c for c,it,p in r['parcelas_ARBA']) + (' — ' + ' / '.join(f'{p}%' for c,it,p in r['parcelas_ARBA']) if r['parcelas_ARBA'] else ''),
            pct_fuera_de_parcelas_ARBA=r['pct_fuera_de_parcelas'],dist_al_Paisaje_Protegido_m=r['dist_PP_BosqueAlegre_m'],centroide_lat=r['centroide'][0],centroide_lon=r['centroide'][1],
            vertices_m_locales=' '.join(f'({e:.0f},{n:.0f})' for e,n in pts[:12]),detalle_franja=extra,marca='[probable] (sale de imagen) / [cálculo propio]'))
    e0,n0,e1,n1=cfg['crop']
    print(sitio,zoom(sitio,e0,n0,e1,n1,f'{U}/recortes/{sitio}_playones_marcados.jpg',polys=polys,maxpx=1400))
with open(f'{U}/calculos/CALCULO_PROPIO_playones_desde_imagen.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r['sitio'],r['id'],r['area_poligono_m2'],r['area_sin_vegetacion_m2'],r['parcelas_ARBA_cca_item_pct'][:90],r['pct_fuera_de_parcelas_ARBA'],r['dist_al_Paisaje_Protegido_m'])
