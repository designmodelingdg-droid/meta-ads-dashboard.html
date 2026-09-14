"""Acabado de las dos piezas «manos sobre plano estructural» (10-sep-2026).

El generador devolvio las dos fotos en 1536x2752 pero NINGUNA llena el cuadro:
las dos vienen con franjas pegadas arriba y abajo, con costura visible. Es el
fallo ya documentado en LISTA-IMAGENES.md para la serie de detras de camaras, y
esta vez no se corrigio pidiendo «no bands, no letterbox» en el prompt.

Aqui se arregla midiendo, no a ojo:

  A  la foto real ocupa solo las filas 796-1955 (42% del alto) y es apaisada:
     recortarla a 9:16 dejaria 652 px de ancho y cortaria las dos manos. Asi que
     se queda como banda central sobre campo azul marino, con los bordes
     fundidos. Las franjas de Instagram quedan de azul liso.

  B  la foto real llega hasta la fila 2148 y desde ahi hay un rectangulo gris
     plano. No sirve prolongar el color de cada columna: justo encima de la
     costura hay papel blanco, y prolongarlo pinta una mancha clara donde en la
     escena real solo hay escritorio. Se sustituye por la penumbra del
     escritorio -el percentil 25 de las ultimas filas buenas- apagandose hacia
     el azul de la casa, con el cambio repartido en las 120 filas anteriores
     para que no haya linea.

Uso:  python3 manos-plano-acabado.py <origen-A.png> <origen-B.png> <destino/>
"""
import sys, pathlib
import numpy as np
from PIL import Image

NAVY = np.array([0x0E, 0x24, 0x38], dtype=float)   # el azul marino de la casa
SALIDA = (1080, 1920)                              # 9:16 exacto

A_FOTO = (796, 1955)     # primera y ultima fila de foto real en la variante A
B_CORTE = 2149           # primera fila del rectangulo pegado en la variante B
B_FUNDIDO = 120          # filas de foto real por las que se reparte el cambio


def _a_9_16(arr):
    """Recorta el alto sobrante y devuelve la imagen ya en 1080x1920."""
    h, w = arr.shape[:2]
    alto_9_16 = round(w * 16 / 9)
    if h > alto_9_16:                       # sobra alto: se quita por abajo
        arr = arr[:alto_9_16]
    elif h < alto_9_16:                     # falta alto: se quita ancho
        ancho = round(h * 9 / 16)
        x0 = (w - ancho) // 2
        arr = arr[:, x0:x0 + ancho]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return im.resize(SALIDA, Image.LANCZOS)


def variante_a(origen):
    """Banda de foto centrada sobre campo azul marino, bordes fundidos."""
    src = np.asarray(Image.open(origen).convert('RGB')).astype(float)
    y0, y1 = A_FOTO
    foto = src[y0:y1]
    h, w = src.shape[:2]

    lienzo = np.tile(NAVY, (h, w, 1))
    lienzo[y0:y1] = foto

    # fundido de 90 px en el borde superior e inferior de la banda
    fundido = 90
    for i in range(fundido):
        t = i / fundido                       # 0 en el borde, 1 hacia dentro
        lienzo[y0 + i] = NAVY * (1 - t) + foto[i] * t
        lienzo[y1 - 1 - i] = NAVY * (1 - t) + foto[-1 - i] * t
    return _a_9_16(lienzo)


def variante_b(origen, semilla=7):
    """Sustituye el rectangulo gris del pie por la penumbra del escritorio."""
    src = np.asarray(Image.open(origen).convert('RGB')).astype(float)
    h, w = src.shape[:2]
    corte = B_CORTE
    rng = np.random.default_rng(semilla)

    # penumbra del escritorio: percentil 25 de las ultimas filas de foto real.
    # La media serviria si debajo del papel hubiera papel, y no lo hay.
    sombra = np.percentile(src[corte - 200:corte].reshape(-1, 3), 25, axis=0)

    filas = h - corte
    t = (np.arange(filas) / filas) ** 0.75                     # se apaga suave
    cola = sombra * (1 - t)[:, None] + NAVY * t[:, None]
    cola = np.repeat(cola[:, None, :], w, axis=1)
    cola += rng.normal(0, 1.4, cola.shape)   # grano: si no, degradado a bandas
    src[corte:] = cola

    # el cambio se reparte hacia arriba para que no quede linea de corte
    for i in range(B_FUNDIDO):
        t = i / B_FUNDIDO                    # 1 en la costura, 0 al subir
        fila = corte - 1 - i
        src[fila] = src[fila] * t + sombra * (1 - t)
    return _a_9_16(src)


if __name__ == '__main__':
    a_src, b_src, destino = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    destino.mkdir(parents=True, exist_ok=True)
    variante_a(a_src).save(destino / 'manos-plano-A.jpg', quality=92, subsampling=1)
    variante_b(b_src).save(destino / 'manos-plano-B.jpg', quality=92, subsampling=1)
    print('escritas manos-plano-A.jpg y manos-plano-B.jpg en', destino)
