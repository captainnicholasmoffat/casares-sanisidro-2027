# Arma un video sintético 1080p 30 fps de 60 s con caras (foto de dominio público de la NASA incluida en scikit-image: skimage.data.astronaut)
# para medir la velocidad de deface en CPU. Uso: python -I hacer_video_prueba.py SALIDA.mp4
import sys, numpy as np, imageio.v2 as iio
from skimage import data, transform
out = sys.argv[1]
ast = data.astronaut()  # 512x512 RGB
face = ast[20:260, 140:340]  # recorte cabeza y hombros
rng = np.random.default_rng(1)
bg = (rng.random((1080, 1920, 3)) * 60 + 90).astype(np.uint8)
sizes = [(120, 100), (200, 166), (300, 250), (80, 66), (450, 375)]
crops = [(transform.resize(face, s, anti_aliasing=True) * 255).astype(np.uint8) for s in sizes]
w = iio.get_writer(out, fps=30, codec='libx264', quality=None, bitrate='5M', macro_block_size=8)
for t in range(1800):
    fr = bg.copy()
    for k, c in enumerate(crops):
        h, ww = c.shape[:2]
        x = int((200 + k * 330 + t * (2 + k)) % (1920 - ww))
        y = int(100 + k * 120 + 40 * np.sin(t / 30 + k)) % (1080 - h)
        fr[y:y + h, x:x + ww] = c
    w.append_data(fr)
w.close()
print('ok', out)
