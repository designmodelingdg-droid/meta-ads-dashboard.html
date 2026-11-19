"""Convierte líneas de una captura de pantalla real en una tarjeta legible en vertical (9:16).

Una captura de 1920 px de ancho metida en un video de 1080 px deja el texto a ~8 pt en el celular:
ilegible. Esto recorta los renglones que importan (píxeles reales, sin redibujar nada) y los apila en
una tarjeta blanca de ≤ 520 px de ancho, que el video puede ampliar casi al doble.

Uso:
  python3 recortar_captura.py captura.png salida.png  "x0,y0,x1,y1" ["x0,y0,x1,y1" ...]  [--etiqueta "x0,y0,x1,y1"]

Cada caja es un trozo de renglón en coordenadas de la captura. Para partir un renglón largo en dos,
pasa dos cajas contiguas (mismo y0/y1). La etiqueta opcional (p. ej. «TUTOR DMA») va arriba.
Para encontrar los cortes entre palabras: mira la captura, o busca columnas sin tinta con numpy.
"""
import sys
from PIL import Image, ImageDraw


def caja(s):
    return tuple(int(v) for v in s.split(','))


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print(__doc__); sys.exit(1)
    src, out = args[0], args[1]
    etiqueta = None
    if '--etiqueta' in args:
        i = args.index('--etiqueta'); etiqueta = caja(args[i + 1]); args = args[:i] + args[i + 2:]
    cajas = [caja(a) for a in args[2:]]
    im = Image.open(src).convert('RGB')
    segs = [im.crop(b) for b in cajas]
    lab = im.crop(etiqueta) if etiqueta else None
    pad, gap = 34, 14
    W = max([s.width for s in segs] + ([lab.width] if lab else [])) + pad * 2
    H = pad * 2 + sum(s.height for s in segs) + gap * (len(segs) - 1) + ((lab.height + 18) if lab else 0)
    c = Image.new('RGB', (W, H), (255, 255, 255)); y = pad
    if lab:
        c.paste(lab, (pad, y)); y += lab.height + 18
    for s in segs:
        c.paste(s, (pad, y)); y += s.height + gap
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), 22, fill=255)
    o = Image.new('RGBA', (W, H)); o.paste(c, (0, 0), m); o.save(out)
    print(out, o.size)


if __name__ == '__main__':
    main()
