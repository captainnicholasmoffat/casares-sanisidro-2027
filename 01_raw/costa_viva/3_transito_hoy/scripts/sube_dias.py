# Extrae del archivo oficial "SUBE - Cantidad de transacciones (usos) por fecha" (datos.transporte.gob.ar)
# sólo los días pedidos, con pedidos HTTP Range (el archivo completo pesa >50 MB y no se descarga entero).
# El archivo está ordenado por fecha: se busca por bisección el byte donde empieza cada día.
import urllib.request, sys, csv, io, json, datetime
URL={'2026':'https://archivos-datos.transporte.gob.ar/upload/Dat_Ab_Usos/dat-ab-usos-2026.csv',
     '2025':'https://archivos-datos.transporte.gob.ar/upload/Dat_Ab_Usos/dat-ab-usos-2025.csv'}
OUT='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/sube/'
nbytes=0
import time, os
def rng(u,a,b):
    global nbytes
    for k in range(6):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'Range':f'bytes={a}-{b}','User-Agent':'investigacion-costa-sanisidro/1.0'}),timeout=60).read()
            nbytes+=len(r); return r
        except Exception as e:
            print('reintento',k,e,flush=True); time.sleep(3)
    raise SystemExit('falló')
SIZES={}
def size(u):
    if u in SIZES: return SIZES[u]
    for k in range(6):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,method='HEAD'),timeout=60); SIZES[u]=int(r.headers['Content-Length']); return SIZES[u]
        except Exception as e: time.sleep(3)
def date_at(u,off):
    b=rng(u,off,off+600).decode('utf-8','ignore')
    ln=b.split('\n')[1]; return ln[:10], off+len(b.split('\n')[0].encode())+1
def find_start(u,day,S):
    lo,hi=0,S-1
    while hi-lo>4000:
        mid=(lo+hi)//2
        d,_=date_at(u,mid)
        if d<day: lo=mid
        else: hi=mid
    return lo
def get_day(u,day,S):
    a=find_start(u,day,S)
    rows=[];off=a;buf=b''
    while True:
        chunk=rng(u,off,off+262143); off+=len(chunk); buf+=chunk
        txt=buf.decode('utf-8','ignore'); lines=txt.split('\n')
        done=any(l[:10]>day and l[:4].isdigit() for l in lines[1:-1])
        if done or len(chunk)<262144: break
    for l in txt.split('\n')[1:-1]:
        if l.startswith(day): rows.append(l)
    return rows
days=sys.argv[1:]
res={}
for day in days:
    if os.path.exists(OUT+f'sube_usos_{day}.csv'): continue
    u=URL[day[:4]]; S=size(u)
    rows=get_day(u,day,S)
    res[day]=rows
    open(OUT+f'sube_usos_{day}.csv','w').write('\n'.join(rows)+'\n')
    print(day,len(rows),'filas', 'bytes descargados acumulados',nbytes, flush=True)
