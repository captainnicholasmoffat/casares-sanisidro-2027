# Para cada CSV de NOAA ISD guarda un .txt reducido (DATE;REPORT_TYPE;TMP;WND) y escribe las líneas de FUENTES
import csv, glob, os, datetime
D = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v3_invierno_espacios'
lines = []
for f in sorted(glob.glob(os.path.join(D, 'noaa_isd', '87553099999_*.csv'))):
    y = f[-8:-4]
    with open(f, newline='') as fh, open(f + '.txt', 'w') as out:
        out.write('DATE_UTC;REPORT_TYPE;TMP(°C x10,calidad);WND(dir,cal,tipo,vel m/s x10,cal)\n')
        for r in csv.DictReader(fh):
            out.write(f"{r['DATE']};{r['REPORT_TYPE'].strip()};{r['TMP']};{r['WND']}\n")
    url = f'https://www.ncei.noaa.gov/data/global-hourly/access/{y}/87553099999.csv'
    lines.append(f'noaa_isd/{os.path.basename(f)} | {os.path.getsize(f)} | {url} | {datetime.date.today()} | NOAA NCEI Integrated Surface Database (global-hourly) {y}, San Fernando Aero (OMM 87553): observaciones SYNOP y METAR del SMN, hora UTC')
    lines.append(f'noaa_isd/{os.path.basename(f)}.txt | {os.path.getsize(f + ".txt")} | idem | {datetime.date.today()} | [extracto propio] sólo columnas DATE, REPORT_TYPE, TMP y WND de idem')
with open(os.path.join(D, 'FUENTES.txt'), 'a') as fh: fh.write('\n'.join(lines) + '\n')
print(len(lines))
