# -*- coding: utf-8 -*-
"""
De donde salen los tres numeros de camara de cuatro-puertas.py.

El problema: hay tension real entre RECESION (que se note la perspectiva)
y PROPORCION (que cada puerta siga pareciendo una puerta). Con la fila muy
girada hacia la camara las cuatro miden casi lo mismo y no hay perspectiva;
con la fila casi paralela al eje el escorzo horizontal las convierte en
ranuras. Filtrar con reglas duras da CERO candidatos, asi que se puntua.

Resultado: phi=44 grados, Z0=6.25 m, paso=1.55 m, X0=-0.80 m.
"""
import math

K, CAM_H, HOR = 1750.0, 1.62, 905.0
VANO_W, VANO_H, JAMB, DINTEL = 1.02, 2.16, 0.17, 0.19

# CX y HOR son traslaciones puras (x = CX + X*K/Z), asi que aqui no importan:
# el encuadre se resuelve al final centrando la caja en el lienzo.
OBJ = dict(ancho=800, alto=780, a1=2.5, a4=3.4, rec=2.05, sep=26)


def caja(phi, z0, paso, x0):
    """caja envolvente de cada una de las cuatro puertas, en pixeles"""
    su = (math.sin(phi), math.cos(phi))
    out = []
    for i in range(4):
        a, b = i*paso - JAMB, i*paso + VANO_W + JAMB
        xs, ys = [], []
        for t in (a, b):
            X, Z = x0 + su[0]*t, z0 + su[1]*t
            if Z < 0.8:
                return None
            xs.append(X*K/Z)
            for y in (0.0, VANO_H + DINTEL):
                ys.append(HOR + (CAM_H - y)*K/Z)
        out.append((min(xs), max(xs), min(ys), max(ys)))
    return out


def buscar():
    res = []
    for gphi in [x*0.5 for x in range(40, 90)]:
        for z0 in [x*0.25 for x in range(12, 44)]:
            for paso in [x*0.05 for x in range(22, 64)]:
                for x0 in [x*0.2 for x in range(-22, 4)]:
                    c = caja(math.radians(gphi), z0, paso, x0)
                    if not c:
                        continue
                    ancho = max(p[1] for p in c) - min(p[0] for p in c)
                    alto = max(p[3] for p in c) - min(p[2] for p in c)
                    if ancho > 860 or alto > 920:
                        continue
                    cy = (max(p[3] for p in c) + min(p[2] for p in c)) / 2
                    w = [p[1] - p[0] for p in c]
                    h = [p[3] - p[2] for p in c]
                    sep = min(c[i + 1][0] - c[i][1] for i in range(3))
                    if sep < 8:
                        continue
                    a1, a4, rec = h[0] / w[0], h[3] / w[3], w[0] / w[3]
                    pena = (abs(ancho - OBJ['ancho']) / 40
                            + abs(alto - OBJ['alto']) / 40
                            + abs(a1 - OBJ['a1']) * 3.2
                            + abs(a4 - OBJ['a4']) * 2.2
                            + abs(rec - OBJ['rec']) * 4.5
                            + abs(sep - OBJ['sep']) / 12
                            + abs(cy - 960) / 25)
                    res.append((pena, gphi, z0, paso, x0, ancho, alto,
                                a1, a4, rec, w[3], sep, cy))
    res.sort()
    return res


if __name__ == '__main__':
    res = buscar()
    print('  pena   phi    z0  paso     x0  ancho alto    a1    a4   rec   w4  sep   cy')
    for r in res[:10]:
        print('%7.2f %5.1f %5.2f %5.2f %6.2f %5.0f %5.0f 1:%.1f 1:%.1f %5.2f %4.0f %4.0f %5.0f'
              % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8],
                 r[9], r[10], r[11], r[12]))
