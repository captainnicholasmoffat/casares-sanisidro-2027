# -*- coding: utf-8 -*-
"""El MISMO documento que el PDF, en un solo archivo HTML: el mismo cuerpo, el
mismo CSS, y las fuentes y las imagenes adentro en base64. Abre en cualquier
navegador sin nada mas al lado."""
import base64, io, os, re, sys
from PIL import Image
RAIZ="/home/user/casares-sanisidro-2027"
sys.path.insert(0, os.path.join(RAIZ,"03_scripts"))
os.chdir(RAIZ)
import armar_pdf as A
SAL=("/tmp/claude-0/-home-user-casares-sanisidro-2027/"
     "e718506c-f800-59cb-a388-d13f7f594b6c/scratchpad/PROGRAMA_SAN_ISIDRO_2027.html")

cuerpo=io.open(os.path.join(RAIZ,"_pdf_build.html"),encoding="utf-8").read()
css=A.CSS

def b64(ruta, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(ruta,"rb").read()).decode())

def img64(ruta, ancho=1500, calidad=84):
    im=Image.open(ruta)
    if im.width>ancho: im=im.resize((ancho,int(im.height*ancho/im.width)), Image.LANCZOS)
    b=io.BytesIO(); im.convert("RGB").save(b,"JPEG",quality=calidad,optimize=True)
    return "data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()

# 1. imagenes
rutas=sorted(set(re.findall(r'src="(file://[^"]+)"', cuerpo)))
for u in rutas:
    p=u.replace("file://","")
    if not os.path.exists(p): print("  falta:",p); continue
    cuerpo=cuerpo.replace('src="%s"'%u, 'src="%s"'%img64(p))
print(f"  {len(rutas)} imagenes adentro")

# 2. fuentes: el CSS del PDF las pide por familia instalada; aca van embebidas
caras=[("Spectral","400","normal","Spectral-Regular.ttf"),
       ("Spectral","500","normal","Spectral-Medium.ttf"),
       ("Spectral","600","normal","Spectral-SemiBold.ttf"),
       ("Spectral","700","normal","Spectral-Bold.ttf"),
       ("Spectral","400","italic","Spectral-Italic.ttf"),
       ("Spectral","500","italic","Spectral-MediumItalic.ttf"),
       ("Inter","100 900","normal","Inter[opsz,wght].ttf"),
       ("Inter","100 900","italic","Inter-Italic[opsz,wght].ttf")]
faces="\n".join(
  '@font-face{font-family:"%s";font-weight:%s;font-style:%s;src:url("%s") format("truetype");}'
  % (f,w,s,b64(os.path.join(RAIZ,"05_tipografia",a),"font/ttf"))
  for f,w,s,a in caras)
print("  8 caras adentro")

# 3. el CSS del PDF, mas lo minimo para que un navegador pagine como una hoja
navegador = """
/* ---- SOLO PARA PANTALLA ----
   El PDF pagina con @page y un navegador no. Esto no cambia ni un color ni
   un cuerpo: le da a la mancha el ancho, el margen y el fondo del A4 para
   que se lea igual que impresa. */
@media screen{
 html{background:#C9C3B8;}
 body{width:210mm;margin:0 auto;padding:12mm 14.3mm 15mm;background:#F5F0E8;
      box-sizing:border-box;box-shadow:0 0 30px rgba(0,0,0,.28);}
 img{max-width:100%;height:auto;}
 .tapa{margin:-12mm -14.3mm 0;}
}
"""
cuerpo=cuerpo.replace("</head>",
    "<style>%s\n%s\n%s</style></head>" % (faces, css, navegador))
io.open(SAL,"w",encoding="utf-8").write(cuerpo)
print("  %.1f MB" % (os.path.getsize(SAL)/1e6))
