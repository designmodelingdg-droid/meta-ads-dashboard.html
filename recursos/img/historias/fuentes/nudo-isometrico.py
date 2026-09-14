# -*- coding: utf-8 -*-
"""
Estructura metalica en isometrico con UNA conexion destacada · Design
Modeling Academy.

Dibujada, no generada, por lo de siempre: "isometrico" y "una de sus
conexiones" son propiedades exactas. Un generador da una perspectiva
cualquiera y reparte el ambar por donde le parece; aqui la proyeccion es
isometrica de verdad (ejes a 30 grados, sin punto de fuga) y el ambar cae en
un nudo concreto, el de la esquina que queda mas cerca del observador.

El truco del encargo -una destacada, el resto en blanco tenue- se resuelve
dibujando la estructura DOS veces: una entera en blanco tenue y otra en
ambar, esta solo con las barras que LLEGAN al nudo y recortada a un circulo
de detalle. Dentro del circulo, y solo ahi, aparecen la chapa de testa y los
tornillos, que es lo que hace que se lea como una conexion y no como un
cruce de lineas.

La primera pasada recortaba la estructura entera al circulo, sin filtrar por
nudo, y salio un roseton: en isometrico media docena de barras de otras
alineaciones cruzan ese mismo punto de la pantalla. Por lo mismo el nudo no
esta en el eje central sino en la arista izquierda de la silueta, donde el
vecino mas cercano queda a 159 px y el circulo mide 115 de radio: se
comprueba y se imprime.

El circulo de detalle es ademas la convencion de un plano de verdad
-"detalle A"-, no un efecto: por eso remata la idea sin una sola letra.

Y una trampa de la isometrica que costo dos pasadas: si la altura de planta
iguala al vano, la diagonal del arriostre cae exactamente a 30 grados, o sea
paralela a las vigas de los vanos vecinos, y el conjunto deja de parecer una
estructura para parecer un cristal hexagonal. Con HS = 1.32 * DX la diagonal
sale a 43 grados y la retícula se rompe. El angulo se imprime al final.

Sin texto: el texto va con las herramientas de Instagram.
Zonas libres: nada importante sobre y=480 ni bajo y=1440 (se comprueba y se
imprime al final).
"""
import math

W, H = 1080, 1920

NAVY   = '#0E2438'
AMBAR  = '#E8A04A'
BLANCO = '#E7F0F8'

NX, NZ, PISOS = 3, 2, 3             # vanos en x, vanos en z, plantas
DX, DZ, HS    = 140.0, 140.0, 185.0  # la altura NO puede igualar al vano: ver abajo
COS30, SIN30  = math.cos(math.radians(30)), 0.5

NUDO   = (0.0, 1*HS, NZ*DZ)         # arista izquierda de la silueta, primera planta
BARRAS_NUDO = (('x', +1), ('z', -1))  # por donde le llegan las dos vigas
RADIO  = 105.0                      # circulo de detalle
CHAPA  = 26.0                       # medio lado de la chapa de testa
RETIRO = 24.0                       # cuanto se retira la chapa del eje

GRUESO = {'pilar': 5.2, 'viga': 3.2, 'diagonal': 2.2}
BRILLO = {'pilar': 1.30, 'viga': 1.0, 'diagonal': 0.85}   # el pilar manda


def iso(p):
    """Isometrica pura: los dos ejes horizontales a 30 grados, el vertical
    vertical. Sin punto de fuga, que es lo que pide el encargo."""
    x, y, z = p
    return ((x - z) * COS30, -y + (x + z) * SIN30)


def miembros():
    m = []
    for i in range(NX + 1):                              # pilares
        for k in range(NZ + 1):
            for lvl in range(PISOS):
                m.append(((i*DX, lvl*HS, k*DZ), (i*DX, (lvl+1)*HS, k*DZ), 'pilar'))
    for lvl in range(PISOS + 1):                         # vigas en x
        for k in range(NZ + 1):
            for i in range(NX):
                m.append(((i*DX, lvl*HS, k*DZ), ((i+1)*DX, lvl*HS, k*DZ), 'viga'))
    for lvl in range(PISOS + 1):                         # vigas en z
        for i in range(NX + 1):
            for k in range(NZ):
                m.append(((i*DX, lvl*HS, k*DZ), (i*DX, lvl*HS, (k+1)*DZ), 'viga'))
    for lvl in range(PISOS):                             # arriostres
        y0, y1 = lvl*HS, (lvl+1)*HS
        m.append((((NX-1)*DX, y0, 0), (NX*DX, y1, 0), 'diagonal'))
        m.append(((NX*DX, y0, 0), ((NX-1)*DX, y1, 0), 'diagonal'))
    # de atras hacia delante: lo que esta lejos se dibuja primero y se apaga
    m.sort(key=lambda t: t[0][0] + t[0][2] + t[1][0] + t[1][2])
    return m


MIEMBROS = miembros()
PLANOS = [p for a, b, _ in MIEMBROS for p in (iso(a), iso(b))]
BX0 = min(p[0] for p in PLANOS); BX1 = max(p[0] for p in PLANOS)
BY0 = min(p[1] for p in PLANOS); BY1 = max(p[1] for p in PLANOS)
UX0 = min(BX0, iso(NUDO)[0] - RADIO)          # el circulo tambien cuenta
UX1 = max(BX1, iso(NUDO)[0] + RADIO)
CX = W/2 - (UX0 + UX1) / 2
CY = H/2 - (BY0 + BY1) / 2


def pantalla(p):
    u, v = iso(p)
    return (CX + u, CY + v)


HONDO = [a[0] + a[2] + b[0] + b[2] for a, b, _ in MIEMBROS]
HMIN, HMAX = min(HONDO), max(HONDO)


def toca_nudo(a, b):
    return a == NUDO or b == NUDO


def trazos(color, factor, opaco=None, solo_nudo=False):
    """Con opaco=None cada miembro se apaga segun lo lejos que este (pase en
    blanco tenue). Con solo_nudo, unicamente las barras que llegan al nudo:
    es lo que evita el roseton."""
    salida = []
    for (a, b, tipo), hondo in zip(MIEMBROS, HONDO):
        if solo_nudo and not toca_nudo(a, b):
            continue
        t = (hondo - HMIN) / (HMAX - HMIN)
        op = opaco if opaco is not None else min(0.62, (0.17 + 0.30 * t) * BRILLO[tipo])
        salida.append('    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                      'stroke="%s" stroke-width="%.1f" opacity="%.2f" '
                      'stroke-linecap="round"/>'
                      % (pantalla(a) + pantalla(b)
                         + (color, GRUESO[tipo] * factor, op)))
    return '\n'.join(salida)


def chapa(eje, signo):
    """Chapa de testa y sus cuatro tornillos, en la testa de la viga que sale
    del nudo por ese eje y ese sentido. La chapa es perpendicular a la viga,
    asi que en isometrico sale como un paralelogramo, no como un rectangulo."""
    x, y, z = NUDO
    p = (x + signo*RETIRO, y, z) if eje == 'x' else (x, y, z + signo*RETIRO)
    def v(dy, dw):
        return pantalla((p[0], p[1] + dy, p[2] + dw) if eje == 'x'
                        else (p[0] + dw, p[1] + dy, p[2]))
    esquinas = [v(-CHAPA, -CHAPA), v(CHAPA, -CHAPA), v(CHAPA, CHAPA), v(-CHAPA, CHAPA)]
    d = ('    <polygon points="%s" fill="%s" fill-opacity="0.18" stroke="%s" '
         'stroke-width="2.6" stroke-linejoin="round"/>\n'
         % (' '.join('%.1f,%.1f' % q for q in esquinas), AMBAR, AMBAR))
    for dy in (-CHAPA*0.55, CHAPA*0.55):
        for dw in (-CHAPA*0.55, CHAPA*0.55):
            d += '    <circle cx="%.1f" cy="%.1f" r="4.0" fill="%s"/>\n' % (v(dy, dw) + (AMBAR,))
    return d


nx, ny = pantalla(NUDO)

reticula = []
for x in range(0, W + 1, 72):
    reticula.append('    <line x1="%d" y1="0" x2="%d" y2="%d"/>' % (x, x, H))
for y in range(0, H + 1, 72):
    reticula.append('    <line x1="0" y1="%d" x2="%d" y2="%d"/>' % (y, W, y))

svg = '''<style>
  html,body{{margin:0;padding:0;background:{navy};width:1080px;height:1920px;overflow:hidden}}
  svg{{display:block}}
</style>
<!--
  Estructura metalica en isometrico, una conexion destacada.
  La misma estructura dibujada dos veces: entera en blanco tenue y en ambar
  recortada al circulo de detalle. Dentro del circulo, y solo ahi, la chapa
  de testa y los tornillos.
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
      <stop offset="0" stop-color="{ambar}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="{ambar}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="detalle">
      <circle cx="{nx:.1f}" cy="{ny:.1f}" r="{radio:.1f}"/>
    </clipPath>
  </defs>

  <rect width="1080" height="1920" fill="{navy}"/>

  <g mask="url(#banda)" stroke="#1B3A57" stroke-width="1" opacity="0.55">
{reticula}
  </g>

  <ellipse cx="{nx:.1f}" cy="{ny:.1f}" rx="{halo:.0f}" ry="{halo:.0f}" fill="url(#halo)"/>

  <g>
{tenue}
  </g>

  <g clip-path="url(#detalle)">
{fuerte}
{chapas}  </g>

  <circle cx="{nx:.1f}" cy="{ny:.1f}" r="{radio:.1f}" fill="none" stroke="{ambar}"
          stroke-width="2.6" opacity="0.85"/>
</svg>
'''.format(navy=NAVY, ambar=AMBAR, nx=nx, ny=ny, radio=RADIO, halo=RADIO * 1.55,
           reticula='\n'.join(reticula),
           tenue=trazos(BLANCO, 1.0),
           fuerte=trazos(AMBAR, 1.9, opaco=0.95, solo_nudo=True),
           chapas=''.join(chapa(e, sg) for e, sg in BARRAS_NUDO))

import sys
destino = sys.argv[1] if len(sys.argv) > 1 else 'nudo-isometrico.svg.html'
open(destino, 'w').write(svg)

# --- lo que hay que comprobar antes de darla por buena ---------------------
x0, y0 = CX + BX0, CY + BY0
x1, y1 = CX + BX1, CY + BY1
print('  miembros                %d   (pilares, vigas y arriostres)' % len(MIEMBROS))
print('  estructura              x %.0f..%.0f   y %.0f..%.0f' % (x0, x1, y0, y1))
print('  margenes laterales      %.0f a la izquierda del circulo, %.0f a la derecha'
      % (nx - RADIO, W - x1))
print('  nudo destacado          (%.0f, %.0f)   radio del detalle %.0f' % (nx, ny, RADIO))
print('  circulo dentro del alto y %.0f..%.0f' % (ny - RADIO, ny + RADIO))
print('  ejes isometricos        %.1f grados; diagonal del arriostre %.1f grados'
      % (math.degrees(math.atan2(SIN30, COS30)),
         math.degrees(math.atan2(HS - DX*SIN30, DX*COS30))))
nudos = set()
for a, b, _ in MIEMBROS:
    nudos.add(a); nudos.add(b)
vecino = min(math.hypot(pantalla(n)[0]-nx, pantalla(n)[1]-ny)
             for n in nudos if n != NUDO)
barras = sum(1 for a, b, _ in MIEMBROS if toca_nudo(a, b))
print('  barras en el nudo       %d   (dos tramos de pilar y dos vigas)' % barras)
print('  nudo vecino mas cercano %.0f px   frente a %.0f de radio  ->  %s'
      % (vecino, RADIO, 'el circulo aisla el nudo' if vecino > RADIO else 'SE CUELA OTRO NUDO'))
print('  zonas libres (480/1440) %s'
      % ('respetadas' if y0 > 480 and y1 < 1440 else 'INVADIDAS'))
