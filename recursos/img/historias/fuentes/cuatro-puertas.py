# -*- coding: utf-8 -*-
"""
Cuatro puertas alineadas en perspectiva · Design Modeling Academy.

Quinta pasada. Las cuatro anteriores, y por que se cayo cada una:
  1. Puertas centradas en el eje: se leian como marcos concentricos.
  2. Con espesor de muro seguian anidadas; el problema era la camara.
  3. Vanos de un muro paralelo al eje: por fin cuatro puertas, pero el
     muro se metia en la franja superior de Instagram.
  4. Reencuadrado y correcto en geometria, pero mudo: con el muro paralelo
     al eje el ancho aparente cae con 1/d^2 y el alto con 1/d, asi que
     salian ranuras de 5:1 y la cuarta -- la de ambar, la que lleva el
     mensaje -- medía 29 px, el elemento mas pequeño del cuadro.

Aqui la fila va girada 44 grados respecto al eje de camara. El escorzo
horizontal pasa a ser casi constante, cada puerta conserva proporcion de
puerta, y la fila sigue alejandose: la primera es 2.25 veces mas ancha
que la cuarta. Los tres parametros de camara salen de una busqueda
(buscar_camara.py), no de mover numeros a ojo.

CX y HOR son traslaciones puras, asi que el encuadre se resuelve al final
centrando la caja de las cuatro puertas en el lienzo.
"""
import math

W, H = 1080, 1920
K, CAM_H = 1750.0, 1.62
PHI = math.radians(44.0)
Z0, PASO, X0 = 6.25, 1.55, -0.80

VANO_W, VANO_H = 1.02, 2.16
JAMB, DINTEL   = 0.17, 0.19
ESPESOR        = 0.22
ZNEAR          = 1.30

SU = (math.sin(PHI),  math.cos(PHI))    # a lo largo de la fila
NU = (math.cos(PHI), -math.sin(PHI))    # normal; la camara cae del lado +NU

def mundo(t, off=0.0):
    return (X0 + SU[0]*t + NU[0]*off, Z0 + SU[1]*t + NU[1]*off)

# la camara esta en el origen: se comprueba de que lado del muro cae
_p = mundo(0.0)
LADO = 1.0 if (-_p[0]*NU[0] - _p[1]*NU[1]) > 0 else -1.0   # +1 => camara en +NU

CX = HOR = 0.0
def proj(t, y, off=0.0):
    x, z = mundo(t, off)
    return (CX + x*K/z, HOR + (CAM_H - y)*K/z)

# ── centrado: primero la caja con origen 0, luego se traslada ──────────
_c = [proj(t, y) for i in range(4)
      for t in (i*PASO - JAMB, i*PASO + VANO_W + JAMB)
      for y in (0.0, VANO_H + DINTEL)]
CX  = 540.0 - (min(p[0] for p in _c) + max(p[0] for p in _c)) / 2
HOR = 960.0 - (min(p[1] for p in _c) + max(p[1] for p in _c)) / 2

def poly(pts, close=True):
    return ('M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p for p in pts[1:])
            + (' Z' if close else ''))

def recorta(p1, p2):
    """recorta el segmento al plano cercano: sin esto los puntos que quedan
       detras de la camara proyectan a coordenadas absurdas"""
    (x1, z1), (x2, z2) = p1, p2
    if z1 < ZNEAR and z2 < ZNEAR: return None
    if z1 < ZNEAR:
        u = (ZNEAR - z1) / (z2 - z1); x1, z1 = x1 + u*(x2-x1), ZNEAR
    elif z2 < ZNEAR:
        u = (ZNEAR - z2) / (z1 - z2); x2, z2 = x2 + u*(x1-x2), ZNEAR
    return ((CX + x1*K/z1, HOR + CAM_H*K/z1),
            (CX + x2*K/z2, HOR + CAM_H*K/z2))

# ── las cuatro puertas ────────────────────────────────────────────────
E = -ESPESOR * LADO      # el hueco se hunde hacia el lado contrario a la camara
partes, sombras, diag = [], [], []

for i in range(4):
    a, b   = i*PASO, i*PASO + VANO_W
    ao, bo = a - JAMB, b + JAMB
    hh     = VANO_H + DINTEL
    ult    = (i == 3)
    col    = '#E8A04A' if ult else '#FFFFFF'
    gw     = 3.1 - i*0.30

    ext = [proj(ao, 0), proj(ao, hh), proj(bo, hh), proj(bo, 0)]
    ins = [proj(a, 0), proj(a, VANO_H), proj(b, VANO_H), proj(b, 0)]
    fon = [proj(a, 0, E), proj(a, VANO_H, E), proj(b, VANO_H, E), proj(b, 0, E)]

    if ult:
        partes.append('    <path d="%s" fill="url(#luz)" stroke="none"/>' % poly(ins))
        # el charco de luz sale del vano HACIA la camara, sobre el suelo
        # la luz cae hacia +NU, que es el lado de la camara. Con d grande
        # el charco se iba fuera del cuadro por la derecha: se queda corto.
        d = 1.35 * LADO
        char = [proj(a, 0), proj(b, 0), proj(b + 0.30, 0, d), proj(a - 0.45, 0, d)]
        partes.append('    <path d="%s" fill="url(#charco)" stroke="none"/>' % poly(char))

    partes.append('    <path d="%s" stroke="%s" stroke-width="%.2f"/>' % (poly(ext), col, gw))
    partes.append('    <path d="%s" stroke="%s" stroke-width="%.2f"/>'
                  % (poly(ins), col, gw*0.82))
    partes.append('    <path d="%s" stroke="%s" stroke-width="%.2f" opacity="0.62"/>'
                  % (poly(fon), col, gw*0.55))
    # aristas del vano: solo donde la mocheta mira de verdad a la camara
    visibles = []
    if fon[0][0] > ins[0][0] + 1: visibles += [0, 1]     # jamba izquierda
    if fon[3][0] < ins[3][0] - 1: visibles += [2, 3]     # jamba derecha
    if fon[1][1] > ins[1][1] + 1: visibles += [1, 2]     # dintel por debajo
    if fon[0][1] < ins[0][1] - 1: visibles += [0, 3]     # umbral por arriba
    for k in sorted(set(visibles)):
        partes.append('    <path d="M%.1f %.1f L%.1f %.1f" stroke="%s" '
                      'stroke-width="%.2f" opacity="0.62"/>'
                      % (ins[k][0], ins[k][1], fon[k][0], fon[k][1], col, gw*0.55))

    # sombra de contacto: sin ella los portales flotan sobre la reticula
    sd = 0.85 * LADO
    sombras.append('    <path d="%s" fill="#0A1B2B" opacity="%.2f" stroke="none"/>'
                   % (poly([proj(ao, 0), proj(bo, 0),
                           proj(bo - 0.12, 0, sd), proj(ao - 0.28, 0, sd)]),
                     0.5 - i*0.07))

    xs = [p[0] for p in ext]; ys = [p[1] for p in ext]
    diag.append((i+1, min(xs), max(xs), max(xs)-min(xs), min(ys), max(ys), max(ys)-min(ys)))

# ── suelo: la reticula sigue la direccion de la fila ──────────────────
lar, tra = [], []
for j in range(-16, 17):
    s = recorta(mundo(-16.0, j*0.95), mundo(20.0, j*0.95))
    if s: lar.append('      <path d="M%.1f %.1f L%.1f %.1f"/>' % (s[0][0], s[0][1], s[1][0], s[1][1]))
for j in range(-12, 22):
    s = recorta(mundo(j*0.95, -15.0), mundo(j*0.95, 15.0))
    if s: tra.append('      <path d="M%.1f %.1f L%.1f %.1f"/>' % (s[0][0], s[0][1], s[1][0], s[1][1]))

halo = proj(3*PASO + VANO_W/2, VANO_H/2)

svg = '''<style>
  html,body{{margin:0;padding:0;background:#0E2438;width:1080px;height:1920px;overflow:hidden}}
  svg{{display:block}}
</style>
<!--
  Las cuatro puertas · los cuatro modulos del Master.
  Fila girada 44deg respecto al eje de camara: dos puntos de fuga, los dos
  fuera del lienzo. Es lo que hace que cada puerta conserve proporcion de
  puerta en vez de quedar en ranura. Camara a 1.62 m, f=1750 px.
  Sin texto: el texto va con las herramientas de Instagram.
  Zonas libres respetadas: nada importante sobre y=480 ni bajo y=1440.
-->
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0.43" stop-color="#000"/>
      <stop offset="0.51" stop-color="#fff"/>
      <stop offset="0.68" stop-color="#fff"/>
      <stop offset="0.75" stop-color="#000"/>
    </linearGradient>
    <mask id="mSuelo"><rect width="1080" height="1920" fill="url(#fade)"/></mask>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#E8A04A" stop-opacity="0.24"/>
      <stop offset="55%"  stop-color="#E8A04A" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#E8A04A" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="charco" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0%"   stop-color="#E8A04A" stop-opacity="0.17"/>
      <stop offset="100%" stop-color="#E8A04A" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="luz" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#E8A04A" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#E8A04A" stop-opacity="0.15"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1920" fill="#0E2438"/>

  <g mask="url(#mSuelo)" fill="none" stroke-linecap="round">
    <g stroke="#1E3F58" stroke-width="1.2">
{lar}
    </g>
    <g stroke="#24506D" stroke-width="1.2">
{tra}
    </g>
  </g>

  <ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="340" ry="310" fill="url(#halo)"/>

  <g>
{sombra}
  </g>

  <g fill="none" stroke-linejoin="round" stroke-linecap="round">
{cuerpo}
  </g>
</svg>
'''.format(lar='\n'.join(lar), tra='\n'.join(tra),
           hx=halo[0], hy=halo[1], sombra='\n'.join(sombras),
           cuerpo='\n'.join(partes))

open('/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/puertas.html','w').write(svg)

print('  puerta   x izq  x der  ancho    y sup  y inf   alto   proporcion')
for n, x0_, x1_, aw, y0_, y1_, ah in diag:
    print('    %d     %6.0f %6.0f %6.0f   %6.0f %6.0f %6.0f     1:%.1f'
          % (n, x0_, x1_, aw, y0_, y1_, ah, ah/aw))
tx = [d[1] for d in diag] + [d[2] for d in diag]
ty = [d[4] for d in diag] + [d[5] for d in diag]
print('\n  conjunto        x %.0f..%.0f    y %.0f..%.0f' % (min(tx), max(tx), min(ty), max(ty)))
print('  recesion 1a/4a  %.2fx' % (diag[0][3] / diag[3][3]))
print('  separacion min  %.0f px' % min(diag[i+1][1]-diag[i][2] for i in range(3)))
print('  zona libre de Instagram (y<480 y y>1440):  %s'
      % ('respetada' if min(ty) > 480 and max(ty) < 1440 else 'INVADIDA'))
