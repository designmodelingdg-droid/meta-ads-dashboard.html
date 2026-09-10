# -*- coding: utf-8 -*-
"""
Acabado del perfil de acero tipo I (10-sep-2026).

Esta pieza SI se genera, al reves que las tres anteriores: el encargo pide
profundidad de campo e iluminacion de estudio, que son propiedades de una
foto. Dibujarla en vector habria ignorado dos de las cuatro cosas que pedia.
Con 3,11 creditos en Higgsfield -y 2 por tirada- hubo una sola oportunidad,
asi que el prompt cargaba de una vez las dos trampas conocidas de la serie:
"fills the entire frame edge to edge, no bands, no letterbox" y "no text, no
numbers, no labels". Las dos funcionaron: la foto vino a sangre (el mayor
salto entre filas contiguas es 1,9) y sin una palabra legible.

Lo que NO salio bien es el encuadre. El acero ocupa del 4% al 75% del alto,
asi que la franja superior de Instagram queda tomada por el ala desenfocada:
desviacion 80 y brillo 80, la peor de toda la serie. La inferior, en cambio,
sale impecable -desviacion 5,4, brillo 23,5-.

No se puede recortar para arreglarlo: la foto ya viene casi en 9:16 (0,558
frente a 0,5625), asi que no sobra alto por ningun lado, y cualquier recorte
que conserve la testa enfocada vuelve a dejar el acero pegado arriba.

La variante B apaga el ala hacia el azul de la casa con un fundido que
termina justo donde empieza la parte enfocada, para no tocar el sujeto. No es
un parche: es la caida de luz que tendria un plato de estudio con una sola
fuente, y deja la franja superior limpia.

Uso:  python3 perfil-acero-acabado.py <origen.png> <destino/>
"""
import sys, pathlib
import numpy as np
from PIL import Image

NAVY = np.array([0x0E, 0x24, 0x38], dtype=float)
SALIDA = (1080, 1920)

APAGA_DESDE = 0.250    # por encima de aqui, azul liso (la franja de Instagram)
APAGA_HASTA = 0.345    # aqui empieza la testa enfocada: no se toca


def _a_9_16(arr):
    h, w = arr.shape[:2]
    alto = round(w * 16 / 9)
    if h > alto:
        arr = arr[:alto]
    elif h < alto:
        ancho = round(h * 9 / 16)
        x0 = (w - ancho) // 2
        arr = arr[:, x0:x0 + ancho]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize(SALIDA, Image.LANCZOS)


def apaga_arriba(src):
    """Fundido suave del ala desenfocada hacia el azul. Curva suavizada
    (3t^2-2t^3): con una rampa recta se ve el canto del fundido."""
    h = src.shape[0]
    y = np.arange(h) / h
    t = np.clip((y - APAGA_DESDE) / (APAGA_HASTA - APAGA_DESDE), 0, 1)
    peso = 1.0 - (3 * t**2 - 2 * t**3)          # 1 arriba, 0 en la zona nitida
    return src * (1 - peso)[:, None, None] + NAVY * peso[:, None, None]


if __name__ == '__main__':
    origen, destino = sys.argv[1], pathlib.Path(sys.argv[2])
    destino.mkdir(parents=True, exist_ok=True)
    src = np.asarray(Image.open(origen).convert('RGB')).astype(float)
    _a_9_16(src.copy()).save(destino / 'perfil-acero-A.jpg', quality=93, subsampling=1)
    _a_9_16(apaga_arriba(src)).save(destino / 'perfil-acero-B.jpg', quality=93, subsampling=1)

    for nombre in ('perfil-acero-A.jpg', 'perfil-acero-B.jpg'):
        g = np.asarray(Image.open(destino / nombre).convert('RGB')).astype(float).mean(axis=2)
        b = int(g.shape[0] * 0.25)
        print('  %s   superior desv %5.1f brillo %5.1f   inferior desv %5.1f brillo %5.1f'
              % (nombre, g[:b].std(), g[:b].mean(), g[-b:].std(), g[-b:].mean()))
