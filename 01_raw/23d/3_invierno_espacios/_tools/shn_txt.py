# Pasa a .txt las 12 tablas del SHN y arma shn/SHN_sol_BUENOS_AIRES_2026_resumen.csv (día 1, 15 y último; puesta y fin del crepúsculo civil vespertino)
import re, html, os, glob, datetime
D = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v3_invierno_espacios'
MES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
rows = ['mes;dia;crep_matutino;salida;azimut_salida;puesta;azimut_puesta;crep_vespertino']
fu = []
for m in MES:
    f = os.path.join(D, 'shn', f'SHN_sol_BUENOS_AIRES_2026_{m}.html')
    s = open(f, encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s); s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s); s = re.sub(r'\s+', ' ', s)
    open(f + '.txt', 'w').write(s)
    for d, cm, sa, az, pu, azp, cv in re.findall(r'\b(\d\d) (\d\d:\d\d) (\d\d:\d\d) (\d+) (\d\d:\d\d) (\d+) (\d\d:\d\d)', s):
        rows.append(';'.join([m, d, cm, sa, az, pu, azp, cv]))
    fu.append(f'shn/SHN_sol_BUENOS_AIRES_2026_{m}.html | {os.path.getsize(f)} | https://www.hidro.gob.ar/Observatorio/REsol.asp (POST: Localidad=BUENOS AIRES, Mes={m}, Fanio=2026; formulario en https://www.hidro.gob.ar/Observatorio/Astronomia.asp?op=1) | {datetime.date.today()} | Servicio de Hidrografía Naval (Observatorio Naval Buenos Aires): salida y puesta del Sol y crepúsculos, Buenos Aires, {m} 2026, hora oficial (UTC-3)')
    fu.append(f'shn/SHN_sol_BUENOS_AIRES_2026_{m}.html.txt | {os.path.getsize(f + ".txt")} | idem | {datetime.date.today()} | [texto extraído] idem')
open(os.path.join(D, 'shn', 'SHN_sol_BUENOS_AIRES_2026_todo.csv'), 'w').write('\n'.join(rows) + '\n')
with open(os.path.join(D, 'FUENTES.txt'), 'a') as fh:
    fh.write('\n'.join(fu) + '\n')
    fh.write(f'shn/SHN_sol_BUENOS_AIRES_2026_todo.csv | {os.path.getsize(os.path.join(D, "shn", "SHN_sol_BUENOS_AIRES_2026_todo.csv"))} | (elaboración propia con _tools/shn_txt.py) | {datetime.date.today()} | [cálculo propio] las 12 tablas del SHN en un CSV, 365 días\n')
print(len(rows) - 1, 'días')
