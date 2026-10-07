# Baja del Servicio de Hidrografía Naval (Observatorio Naval) las tablas de salida y puesta del Sol
# para BUENOS AIRES, 12 meses de 2026, vía el formulario Astronomia.asp?op=1 -> REsol.asp (POST).
import subprocess, re, os, sys, datetime
D = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v3_invierno_espacios'
ck = os.path.join(D, '_tmp', 'shn_cookies.txt')
def curl(args):
    return subprocess.run(['curl', '-sS', '-L', '--max-time', '60', '-A', 'Mozilla/5.0', '-c', ck, '-b', ck] + args, capture_output=True)
r = curl(['https://www.hidro.gob.ar/Observatorio/Astronomia.asp?op=1'])
s = r.stdout.decode('utf-8', 'replace')
tok = re.search(r'name="CSRFToken" value="([^"]+)"', s).group(1)
for mes in (sys.argv[1:] or ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']):
    out = os.path.join(D, 'shn', f'SHN_sol_BUENOS_AIRES_2026_{mes}.html')
    r = curl(['-o', out, '-w', '%{http_code}', '-e', 'https://www.hidro.gob.ar/Observatorio/Astronomia.asp?op=1',
              '--data-urlencode', f'CSRFToken={tok}', '--data-urlencode', 'Localidad=BUENOS AIRES',
              '--data-urlencode', f'Mes={mes}', '--data-urlencode', 'Fanio=2026',
              'https://www.hidro.gob.ar/Observatorio/REsol.asp'])
    print(mes, r.stdout.decode(), os.path.getsize(out) if os.path.exists(out) else 0)
