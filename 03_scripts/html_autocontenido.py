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

def img64(ruta, ancho=1100, calidad=80, recorte=None):
    """La imagen en base64. Con `recorte` se entrega ya cortada a ese aspecto.

    LA TAPA VA PRE-RECORTADA. En el PDF la foto se coloca en 628,6 x 841,9 pt
    sobre una hoja de 595,3 y el overflow oculto la recorta; en el navegador
    eso lo hace `object-fit: cover`, que es la unica propiedad de la que
    depende toda la pagina de tapa. Entregando la foto ya cortada a 210:297,
    la tapa se arma con un `width:100%; height:100%` y no depende de nada.
    """
    im=Image.open(ruta).convert("RGB")
    if recorte:
        objetivo = recorte
        actual = im.width / im.height
        if actual > objetivo:                      # sobra ancho: cortar a los lados
            w = int(round(im.height * objetivo))
            x = (im.width - w) // 2
            im = im.crop((x, 0, x + w, im.height))
        elif actual < objetivo:                    # sobra alto: cortar arriba y abajo
            h = int(round(im.width / objetivo))
            y = (im.height - h) // 2
            im = im.crop((0, y, im.width, y + h))
    if im.width>ancho: im=im.resize((ancho,int(im.height*ancho/im.width)), Image.LANCZOS)
    b=io.BytesIO(); im.save(b,"JPEG",quality=calidad,optimize=True)
    return "data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()

# 1. imagenes
rutas=sorted(set(re.findall(r'src="(file://[^"]+)"', cuerpo)))
tapa = re.search(r'class="tapa-img[^"]*" src="(file://[^"]+)"', cuerpo)
tapa = tapa.group(1) if tapa else None
for u in rutas:
    q=u.replace("file://","")
    if not os.path.exists(q): print("  falta:",q); continue
    if u == tapa:
        dato = img64(q, ancho=1400, calidad=86, recorte=210.0/297.0)
    else:
        dato = img64(q)
    cuerpo=cuerpo.replace('src="%s"'%u, 'src="%s"'%dato)
print(f"  {len(rutas)} imagenes adentro (la tapa, ya recortada a 210:297)")

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
   un cuerpo.

   EL PADDING VA EN LAS SECCIONES, NO EN EL BODY. Puesto en el body, la tapa
   —que mide 210 x 297 mm exactos y lleva la imagen a sangre— quedaba metida
   adentro del margen y se veia distinta de la del PDF. La tapa no lleva
   margen: es una pagina entera. */
@media screen{
 html{background:#C9C3B8;}
 body{width:210mm;margin:0 auto;padding:0;background:#F5F0E8;
      box-sizing:border-box;box-shadow:0 0 30px rgba(0,0,0,.28);}
 section.indice, section.cap{display:block;padding:12mm 14.3mm 15mm;}
 section.tapa{width:210mm;height:297mm;margin:0;}
 /* el filete del pie es un elemento fijo de impresion: en pantalla se
    quedaria pegado al borde de la ventana toda la lectura */
 .filete-pie{display:none;}
 img:not(.tapa-img){max-width:100%;height:auto;}
 /* LA TAPA, CON LA MISMA GEOMETRIA QUE EN EL PDF.
    En el PDF la imagen se coloca en 628,6 x 841,9 pt sobre una hoja de
    595,3: se desborda 16,7 pt por lado y el overflow:hidden de la seccion
    la recorta. Sin forzarlo, en el navegador la imagen se ajustaba al ancho
    y quedaba una franja de papel abajo, con la foto mas abierta que en el
    PDF. Se declara con !important porque la regla del cuerpo del documento
    convive con la del bloque de pantalla y aca no puede perder. */
 section.tapa{position:relative!important;width:210mm!important;
              height:297mm!important;overflow:hidden!important;}
 section.tapa img.tapa-img{position:absolute!important;left:0!important;
              top:0!important;width:100%!important;height:100%!important;
              max-width:none!important;max-height:none!important;
              display:block!important;}
}
"""
# 3bis. FUERA LAS @font-face DEL DOCUMENTO. El CSS del PDF declara las mismas
# familias apuntando a file:///home/user/.../05_tipografia/*.ttf, y van DESPUES
# de las que acabo de embeber: en CSS gana la ultima, asi que en cualquier
# maquina que no sea esta las fuentes no cargan y el documento entero cae a
# Georgia. Aca no se notaba porque esas rutas existen.
css = re.sub(r'@font-face\s*\{[^}]*\}', '', css)
print("  @font-face del documento: fuera")

cuerpo=cuerpo.replace("</head>",
    "<style>%s\n%s\n%s</style></head>" % (faces, css, navegador))
io.open(SAL,"w",encoding="utf-8").write(cuerpo)
print("  %.1f MB" % (os.path.getsize(SAL)/1e6))
