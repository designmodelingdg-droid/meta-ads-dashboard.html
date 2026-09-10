# -*- coding: utf-8 -*-
"""
Dos miradas sobre el mismo modelo · Design Modeling Academy.

Dibujada, no generada. El encargo tiene propiedades exactas -DOS siluetas,
de perfil, una mirando UNA pieza suelta y la otra el conjunto COMPLETO- y un
generador de imagen las aproxima: cambia el numero de figuras, les tuerce la
mirada y no sabe dibujar la relacion "esta mira esto y aquella mira aquello".
Ademas quedan 3.11 creditos en Higgsfield, que dan para una sola tirada.

Lo que hace legible la idea no son las figuras, es el par de corchetes:
  - el de A encierra una sola pieza      ->  17,300 px2
  - el de B encierra el modelo entero    ->  296,000 px2
La razon entre las dos areas (unas 17 veces) ES el mensaje. Las lineas de
mirada rematan en el corchete de cada uno, cortas en A -esta encima- y
largas en B -esta echado atras-.

La pieza suelta es la misma que falta en el modelo: en el portico hay un
hueco con el fantasma de la viga en linea discontinua, y una guia
discontinua ambar lo une con la pieza. Sin eso, "pieza suelta" seria solo
una barra flotando.

Sin texto: el texto va con las herramientas de Instagram.
Zonas libres: nada importante sobre y=480 ni bajo y=1440 (se comprueba al
final y se imprime).
"""
import math

W, H = 1080, 1920
SUELO = 1310.0

NAVY   = '#0E2438'
AMBAR  = '#E8A04A'
BLANCO = '#EEF4FA'
FIG    = '#B9CBDD'
FIG_BR = '#93AAC2'      # el brazo, un tono mas bajo, para que se lea
GRIS   = '#4E6A85'      # lineas de segundo plano del modelo

# --- el modelo: portico arriostrado de 2 vanos x 3 alturas -----------------
BX, DZ, HS = 106.0, 70.0, 150.0     # vano, fondo, altura de piso
VANOS, PISOS = 3, 4                 # celdas mas anchas que altas: portico, no estanteria
OX, OY     = 483.0, SUELO           # origen del modelo en pantalla
KX, KY     = 0.42, 0.24             # oblicua: cuanto corre el fondo

VIGA_H, VIGA_D = 22.0, 22.0         # seccion de la viga suelta
HUECO = (0, 3, 0)                   # vano, nivel y plano de la viga que falta
PIEZA_OFF = (-232.0, 0.0)           # de su hueco a donde flota, en pantalla

# --- las dos figuras -------------------------------------------------------
FIG_A = dict(cx=88.0, alto=720.0, mira=+1, inclina=+0.034)    # se echa sobre el detalle
FIG_B = dict(cx=975.0, alto=700.0, mira=-1, inclina=-0.014)   # echado atras, ve el conjunto


def proy(x, y, z):
    return (OX + x + z * KX, OY - y - z * KY)


# Silueta de perfil mirando a +x, en alturas de figura: coronilla en y=0,
# planta del pie en y=1. Se recorre por delante (frente, nariz, menton,
# pecho, muslo, pie) y se vuelve por detras (talon, gemelo, gluteo, espalda,
# nuca, craneo). Siete cabezas y media.
PERFIL = [
    ('M', (0.000, 0.000)),
    ('C', (0.026, 0.000), (0.044, 0.014), (0.046, 0.034)),    # frente
    ('C', (0.048, 0.046), (0.042, 0.050), (0.041, 0.058)),    # entrecejo
    ('C', (0.048, 0.064), (0.058, 0.070), (0.062, 0.079)),    # nariz
    ('C', (0.058, 0.084), (0.050, 0.084), (0.044, 0.086)),    # base de nariz
    ('C', (0.049, 0.091), (0.049, 0.095), (0.043, 0.099)),    # labios
    ('C', (0.049, 0.104), (0.050, 0.112), (0.046, 0.119)),    # menton
    ('C', (0.040, 0.127), (0.026, 0.133), (0.012, 0.134)),    # mandibula
    ('C', (0.004, 0.140), (0.014, 0.152), (0.020, 0.166)),    # cuello
    ('C', (0.030, 0.182), (0.044, 0.192), (0.050, 0.208)),    # hombro
    ('C', (0.056, 0.240), (0.055, 0.268), (0.052, 0.300)),    # pecho
    ('C', (0.048, 0.340), (0.042, 0.372), (0.041, 0.398)),    # cintura
    ('C', (0.040, 0.428), (0.046, 0.450), (0.047, 0.474)),    # vientre
    ('C', (0.048, 0.504), (0.052, 0.534), (0.052, 0.566)),    # muslo
    ('C', (0.051, 0.634), (0.043, 0.686), (0.041, 0.720)),    # rodilla
    ('C', (0.038, 0.778), (0.032, 0.848), (0.026, 0.928)),    # espinilla
    ('C', (0.025, 0.948), (0.033, 0.962), (0.045, 0.980)),    # empeine
    ('C', (0.055, 0.990), (0.062, 0.996), (0.068, 1.000)),    # punta del pie
    ('L', (-0.036, 1.000)),                                   # planta
    ('C', (-0.042, 0.992), (-0.044, 0.976), (-0.040, 0.958)), # talon
    ('C', (-0.034, 0.928), (-0.027, 0.898), (-0.031, 0.858)), # tobillo
    ('C', (-0.040, 0.818), (-0.047, 0.778), (-0.042, 0.734)), # gemelo
    ('C', (-0.036, 0.700), (-0.043, 0.658), (-0.050, 0.598)), # muslo atras
    ('C', (-0.059, 0.540), (-0.067, 0.500), (-0.064, 0.462)), # gluteo
    ('C', (-0.060, 0.430), (-0.040, 0.414), (-0.039, 0.394)), # lumbares
    ('C', (-0.037, 0.352), (-0.047, 0.312), (-0.048, 0.274)), # espalda
    ('C', (-0.049, 0.242), (-0.047, 0.218), (-0.040, 0.204)), # hombro atras
    ('C', (-0.033, 0.194), (-0.026, 0.186), (-0.025, 0.172)), # nuca
    ('C', (-0.028, 0.146), (-0.048, 0.112), (-0.050, 0.064)), # craneo
    ('C', (-0.052, 0.028), (-0.030, 0.000), (0.000, 0.000)),
]
BRAZO = [(0.006, 0.220), (0.020, 0.398), (0.026, 0.520), (0.022, 0.578)]
OJO   = (0.026, 0.056)
NARIZ = (0.062, 0.079)


def sitio(fig, p):
    """Un punto de la silueta normalizada, en pixeles del lienzo.

    El cizallamiento inclina la figura sin despegarle los pies: cero en la
    planta y maximo en la coronilla. A se echa adelante -esta encima de la
    pieza- y B se echa atras, que es lo que se hace para ver el conjunto."""
    sesgo = fig['inclina'] * (1.0 - p[1])
    return (fig['cx'] + fig['mira'] * (p[0] + sesgo) * fig['alto'],
            SUELO - fig['alto'] + p[1] * fig['alto'])


def ruta(fig):
    trozos = []
    for seg in PERFIL:
        if seg[0] == 'M':
            trozos.append('M %.2f %.2f' % sitio(fig, seg[1]))
        elif seg[0] == 'L':
            trozos.append('L %.2f %.2f' % sitio(fig, seg[1]))
        else:
            trozos.append('C %.2f %.2f %.2f %.2f %.2f %.2f'
                          % (sitio(fig, seg[1]) + sitio(fig, seg[2])
                             + sitio(fig, seg[3])))
    return ' '.join(trozos) + ' Z'


def caja(puntos):
    xs = [p[0] for p in puntos]; ys = [p[1] for p in puntos]
    return min(xs), min(ys), max(xs), max(ys)


def corchetes(bb, margen, brazo, ancho, color=AMBAR, opac=0.95):
    """Cuatro escuadras en las esquinas: encierran sin encerrar del todo."""
    x0, y0, x1, y1 = bb[0]-margen, bb[1]-margen, bb[2]+margen, bb[3]+margen
    d = []
    for (ex, ey, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1),
                             (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.append('M %.1f %.1f L %.1f %.1f M %.1f %.1f L %.1f %.1f'
                 % (ex, ey + sy*brazo, ex, ey, ex, ey, ex + sx*brazo, ey))
    return ('  <path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
            'stroke-linecap="round" opacity="%.2f"/>'
            % (' '.join(d), color, ancho, opac), (x0, y0, x1, y1))


def viga(x0, y0, color, ancho, discontinua=False, relleno=None):
    """Una viga en oblicua: cara superior, cara frontal y las dos testas."""
    L, hh, dd = BX, VIGA_H, VIGA_D
    def v(x, y, z):
        return (x0 + x + z*KX, y0 - y - z*KY)
    caras = [
        [v(0, hh, 0), v(L, hh, 0), v(L, hh, dd), v(0, hh, dd)],      # superior
        [v(0, 0, 0), v(L, 0, 0), v(L, hh, 0), v(0, hh, 0)],          # frontal
    ]
    testas = [[v(xp, -7, -7), v(xp, hh+7, -7), v(xp, hh+7, dd+7), v(xp, -7, dd+7)]
              for xp in (0.0, L)]
    guion = ' stroke-dasharray="9 7"' if discontinua else ''
    fondo = ''
    if relleno:
        fondo = ''.join(
            '  <polygon points="%s" fill="%s" opacity="%.2f"/>\n'
            % (' '.join('%.1f,%.1f' % q for q in c), relleno, op)
            for c, op in zip(caras, (0.22, 0.13)))
    trazo = ''.join(
        '  <polygon points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s '
        'stroke-linejoin="round"/>\n'
        % (' '.join('%.1f,%.1f' % q for q in c), color, ancho, guion)
        for c in caras + testas)
    pernos = ''
    if not discontinua:
        for (yy, zz) in ((1, 1), (1, dd-1), (hh-1, 1), (hh-1, dd-1)):
            pernos += '  <circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>\n' \
                      % (v(0, yy, zz) + (color,))
    pts = [q for c in caras + testas for q in c]
    return fondo + trazo + pernos, caja(pts)


# --------------------------------------------------------------------------
partes, marcas = [], []

# reticula de plano, solo en la banda central
reticula = []
for x in range(0, W + 1, 72):
    reticula.append('    <line x1="%d" y1="0" x2="%d" y2="%d"/>' % (x, x, H))
for y in range(0, H + 1, 72):
    reticula.append('    <line x1="0" y1="%d" x2="%d" y2="%d"/>' % (y, W, y))

# el modelo
lineas_modelo = []
for j in (1, 0):                                  # primero el plano de atras
    col, gr = (GRIS, 3.0) if j else (BLANCO, 5.0)
    for i in range(VANOS + 1):                    # pilares
        a, b = proy(i*BX, 0, j*DZ), proy(i*BX, PISOS*HS, j*DZ)
        lineas_modelo.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                             'stroke="%s" stroke-width="%.1f"/>' % (a + b + (col, gr)))
    for lvl in range(1, PISOS + 1):               # vigas del plano
        for i in range(VANOS):
            if (i, lvl, j) == HUECO:
                continue
            a = proy(i*BX, lvl*HS, j*DZ); b = proy((i+1)*BX, lvl*HS, j*DZ)
            lineas_modelo.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                                 'stroke="%s" stroke-width="%.1f"/>'
                                 % (a + b + (col, gr * 0.8)))
for lvl in range(1, PISOS + 1):                   # vigas de fondo
    for i in range(VANOS + 1):
        a, b = proy(i*BX, lvl*HS, 0), proy(i*BX, lvl*HS, DZ)
        lineas_modelo.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                             'stroke="%s" stroke-width="3.4"/>' % (a + b + (GRIS,)))
for lvl in range(1, PISOS + 1):                   # arriostres del vano derecho
    for (xa, ya, xb, yb) in (((VANOS-1)*BX, (lvl-1)*HS, VANOS*BX, lvl*HS),
                             (VANOS*BX, (lvl-1)*HS, (VANOS-1)*BX, lvl*HS)):
        a, b = proy(xa, ya, 0), proy(xb, yb, 0)
        lineas_modelo.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                             'stroke="%s" stroke-width="3.0" opacity="0.85"/>'
                             % (a + b + (BLANCO,)))

for j in (1, 0):                                  # vigas de arranque
    col, gr = (GRIS, 3.0) if j else (BLANCO, 4.0)
    a, b = proy(0, 0, j*DZ), proy(VANOS*BX, 0, j*DZ)
    lineas_modelo.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                         'stroke="%s" stroke-width="%.1f"/>' % (a + b + (col, gr)))
for i in range(VANOS + 1):
    a, b = proy(i*BX, 0, 0), proy(i*BX, 0, DZ)
    lineas_modelo.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                         'stroke="%s" stroke-width="3.0"/>' % (a + b + (GRIS,)))

modelo_bb = caja([proy(x, y, z) for x in (0, VANOS*BX) for y in (0, PISOS*HS) for z in (0, DZ)])

# el hueco: el fantasma de la viga que falta
hx, hy = proy(HUECO[0]*BX, HUECO[1]*HS, HUECO[2]*DZ)
fantasma, _ = viga(hx, hy, BLANCO, 3.2, discontinua=True)

# la pieza suelta, con su corchete
px, py = hx + PIEZA_OFF[0], hy + PIEZA_OFF[1]
pieza, pieza_bb = viga(px, py, AMBAR, 3.4, relleno=AMBAR)
corch_a, caja_a = corchetes(pieza_bb, 22, 26, 3.0)
corch_b, caja_b = corchetes(modelo_bb, 34, 48, 3.0, opac=0.75)

# lineas de mirada: cortas en A -esta encima-, largas en B -esta atras-
def mirada(fig, destino, holgura=20.0):
    """Una linea de la cara a la esquina del corchete. Remata en la esquina
    a proposito: si apunta al centro del lado, el trazo muere en el aire y
    parece un descuido -asi salio en la segunda pasada-."""
    n = sitio(fig, NARIZ); o = sitio(fig, OJO)
    salida = (n[0] + fig['mira'] * holgura, o[1])
    dx, dy = destino[0] - salida[0], destino[1] - salida[1]
    largo = math.hypot(dx, dy)
    ux, uy = dx / largo, dy / largo
    b = (destino[0] - ux * 9, destino[1] - uy * 9)
    return ('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="2.4" opacity="0.7" stroke-linecap="round"/>'
            % (salida + b + (AMBAR,)), math.hypot(b[0]-salida[0], b[1]-salida[1]))

# A remata en la esquina de arriba de su corchete -mira hacia abajo, de
# cerca-; B en la de abajo del suyo, barriendo los seis metros de altura.
# La diferencia de longitud es la misma diferencia que dice el encargo.
mir_a, largo_a = mirada(FIG_A, (caja_a[0], caja_a[1]))
mir_b, largo_b = mirada(FIG_B, (caja_b[2], caja_b[3]))

# figuras
figuras = []
for fig in (FIG_A, FIG_B):
    figuras.append('  <path d="%s" fill="%s"/>' % (ruta(fig), FIG))
    br = ' '.join('%.1f,%.1f' % sitio(fig, p) for p in BRAZO)
    figuras.append('  <polyline points="%s" fill="none" stroke="%s" '
                   'stroke-width="%.1f" stroke-linecap="round" '
                   'stroke-linejoin="round" opacity="0.72"/>' % (br, FIG_BR, 0.044 * fig['alto']))

sombras = []
for cx, rx in ((FIG_A['cx'], 78), (FIG_B['cx'], 74),
               ((modelo_bb[0] + modelo_bb[2]) / 2, 168)):
    sombras.append('  <ellipse cx="%.1f" cy="%.1f" rx="%d" ry="11" '
                   'fill="url(#sombra)"/>' % (cx, SUELO + 6, rx))

svg = '''<style>
  html,body{{margin:0;padding:0;background:{navy};width:1080px;height:1920px;overflow:hidden}}
  svg{{display:block}}
</style>
<!--
  Dos miradas sobre el mismo modelo. La de detalle y la de sistema.
  El corchete de la izquierda encierra una pieza; el de la derecha, el
  modelo entero. Esa diferencia de area es el mensaje.
  Sin texto: el texto va con las herramientas de Instagram.
-->
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.20" stop-color="#000"/>
      <stop offset="0.30" stop-color="#fff"/>
      <stop offset="0.70" stop-color="#fff"/>
      <stop offset="0.78" stop-color="#000"/>
    </linearGradient>
    <mask id="banda"><rect width="1080" height="1920" fill="url(#fade)"/></mask>
    <radialGradient id="halo">
      <stop offset="0" stop-color="{ambar}" stop-opacity="0.13"/>
      <stop offset="1" stop-color="{ambar}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sombra">
      <stop offset="0" stop-color="#06121D" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#06121D" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="piso" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{gris}" stop-opacity="0"/>
      <stop offset="0.18" stop-color="{gris}" stop-opacity="0.9"/>
      <stop offset="0.82" stop-color="{gris}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{gris}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1920" fill="{navy}"/>

  <g mask="url(#banda)" stroke="#1B3A57" stroke-width="1" opacity="0.55">
{reticula}
  </g>

  <ellipse cx="{halox:.0f}" cy="{haloy:.0f}" rx="205" ry="150" fill="url(#halo)"/>

  <g>
{sombras}
  </g>
  <line x1="40" y1="{suelo}" x2="1040" y2="{suelo}" stroke="url(#piso)" stroke-width="3.2"/>

  <g stroke-linecap="round">
{modelo}
  </g>
{fantasma}
{pieza}
{corch_a}
{corch_b}
{mir_a}
{mir_b}

  <g>
{figuras}
  </g>
</svg>
'''.format(navy=NAVY, ambar=AMBAR, gris=GRIS, suelo=SUELO,
           reticula='\n'.join(reticula), sombras='\n'.join(sombras),
           modelo='\n'.join(lineas_modelo), fantasma=fantasma,
           pieza=pieza, corch_a=corch_a, corch_b=corch_b,
           mir_a=mir_a, mir_b=mir_b, figuras='\n'.join(figuras),
           halox=(pieza_bb[0] + pieza_bb[2]) / 2, haloy=(pieza_bb[1] + pieza_bb[3]) / 2)

import sys
destino = sys.argv[1] if len(sys.argv) > 1 else 'dos-miradas.svg.html'
open(destino, 'w').write(svg)

# --- lo que hay que mirar antes de darla por buena -------------------------
area_a = (caja_a[2]-caja_a[0]) * (caja_a[3]-caja_a[1])
area_b = (caja_b[2]-caja_b[0]) * (caja_b[3]-caja_b[1])
todo = [caja_a, caja_b, pieza_bb, modelo_bb,
        (FIG_A['cx']-0.08*FIG_A['alto'], SUELO-FIG_A['alto'],
         FIG_A['cx']+0.08*FIG_A['alto'], SUELO),
        (FIG_B['cx']-0.08*FIG_B['alto'], SUELO-FIG_B['alto'],
         FIG_B['cx']+0.08*FIG_B['alto'], SUELO)]
arriba = min(b[1] for b in todo); abajo = max(b[3] for b in todo)
print('  corchete de la pieza    %6.0f x %4.0f px   area %9.0f' %
      (caja_a[2]-caja_a[0], caja_a[3]-caja_a[1], area_a))
print('  corchete del conjunto   %6.0f x %4.0f px   area %9.0f' %
      (caja_b[2]-caja_b[0], caja_b[3]-caja_b[1], area_b))
print('  razon conjunto/pieza    %.1fx' % (area_b / area_a))
print('  linea de mirada         A %.0f px   B %.0f px' % (largo_a, largo_b))
print('  hueco de la izquierda   pieza x %.0f..%.0f   modelo x %.0f..%.0f'
      % (pieza_bb[0], pieza_bb[2], modelo_bb[0], modelo_bb[2]))
print('  todo lo importante      y %.0f..%.0f' % (arriba, abajo))
print('  zonas libres (480/1440) %s'
      % ('respetadas' if arriba > 480 and abajo < 1440 else 'INVADIDAS'))
