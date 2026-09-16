#!/usr/bin/env python3
"""Arma el brief de artes de la pauta de septiembre, en PDF, para el disenador.

Por que existe: las indicaciones de los 6 anuncios del Master ya estaban
escritas en `calendario-septiembre.json` —formato, medidas, prompt de IA,
texto que va dentro de la imagen— pero repartidas entre el JSON y el
artefacto, que es una pagina web con pestanas. Al encargado de las artes
hay que mandarle UN archivo que se abra en cualquier parte y se pueda
imprimir.

Se genera DESDE el JSON a proposito: transcribir seis prompts a mano es
como se cuelan las erratas, y un prompt con una cifra de mas rompe la regla
de oro del mes (el Master no lleva precio en ninguna pieza).

Uso:
    python3 scripts/brief_artes_pauta.py
    python3 scripts/brief_artes_pauta.py --salida /ruta/brief.pdf
"""

import argparse
import html
import json
import pathlib
import shutil
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "matriz-viral/matriz/calendario-septiembre.json"
SALIDA = RAIZ / "matriz-viral/entregables/BRIEF-ARTES-PAUTA-SEPTIEMBRE.pdf"

# Chromium viene preinstalado en el entorno; se usa para imprimir el HTML.
CHROMIUM = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
]

# El verbo y el sello de cada modulo salen del texto de `creativo`, pero se
# fijan aqui explicitos porque son LO QUE EL DISENADOR ESCRIBE EN LA IMAGEN
# y no puede quedar a interpretacion.
DENTRO = {
    "mod1": {"verbo": "ESTRUCTURA", "sello": "MODELADOR BIM",
             "titulo_img": "BIM PROFESSIONAL"},
    "mod2": {"verbo": "COORDINA", "sello": "COORDINADOR BIM",
             "titulo_img": "BIM COORDINATION"},
    "mod3": {"verbo": "GESTIONA", "sello": "BIM MANAGER 4D-5D",
             "titulo_img": "BIM MANAGEMENT"},
    "mod4": {"verbo": "AUTOMATIZA", "sello": "ESPECIALISTA BIM + IA",
             "titulo_img": "BIM + IA"},
}

# Que archivos entrega cada pieza. Sale de la fila «Medidas» del cfg y del
# campo `formato`; se explicita para que el disenador cuente archivos, no
# interprete una frase.
ENTREGA = {
    "mod1": [("Post plano", "1080 x 1350 px", "4:5", 1),
             ("Tarjetas de carrusel", "1080 x 1080 px", "1:1", 3)],
    "mod2": [("Post plano", "1080 x 1350 px", "4:5", 1),
             ("Tarjetas de carrusel", "1080 x 1080 px", "1:1", 3)],
    "mod3": [("Post plano", "1080 x 1350 px", "4:5", 1),
             ("Tarjetas de carrusel", "1080 x 1080 px", "1:1", 3)],
    "mod4": [("Post plano", "1080 x 1350 px", "4:5", 1),
             ("Tarjetas de carrusel", "1080 x 1080 px", "1:1", 3)],
    "diagnostico": [("Post plano (adaptar el existente)", "1080 x 1350 px", "4:5", 1)],
    "ruta": [("Tarjetas de carrusel", "1080 x 1080 px", "1:1", 5)],
}

# Las 3 tarjetas del carrusel de modulo. La estructura esta escrita en el
# campo `creativo` del Modulo 1 y el formato es identico en los cuatro, asi
# que se aplica a los cuatro — y se dice de donde sale, para que si alguien
# quiere otra cosa en el Modulo 3 sepa que aqui hubo una decision.
TARJETAS_MODULO = [
    ("Tarjeta 1", "El dolor", "La frase del gancho, grande. Es el mismo texto del hook del anuncio."),
    ("Tarjeta 2", "Lo que sales sabiendo", "Lo que se aprende en el modulo, en 3 lineas como maximo."),
    ("Tarjeta 3", "Microcredencial + CTA", "El sello grande y la llamada a la accion. Sin cifras."),
]


def esc(t):
    return html.escape(str(t or "")).replace("\n", "<br>")


def bloque_cfg(cfg, claves):
    """Devuelve las filas del cfg que le sirven al disenador, no al que pauta."""
    d = {k: v for k, v in cfg}
    return [(k, d[k]) for k in claves if k in d]


def construir_html(datos):
    pub = datos["publicidad"]
    piezas = pub["campanas"][0]["piezas"]
    ind = {k: v for k, v in pub["indicaciones"]}
    cfg0 = dict(piezas[0]["cfg"])

    total = sum(n for p in piezas for *_, n in ENTREGA[p["id"]])

    P = []
    A = P.append

    A(f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Brief de artes - Pauta septiembre</title><style>
@page {{ size: A4; margin: 15mm 14mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: "Liberation Sans", "DejaVu Sans", sans-serif; font-size: 10pt;
  line-height: 1.5; color: #14212E; margin: 0; }}
h1,h2,h3,h4 {{ margin: 0; }}
code, .mono {{ font-family: "DejaVu Sans Mono", monospace; }}

.portada {{ background: #0E2438; color: #fff; padding: 26mm 16mm; margin: -15mm -14mm 0;
  min-height: 262mm; page-break-after: always; }}
.portada .marca {{ font-size: 9pt; letter-spacing: .28em; color: #E8A04A; font-weight: bold;
  text-transform: uppercase; }}
.portada h1 {{ font-size: 34pt; line-height: 1.05; margin: 9mm 0 6mm; letter-spacing: -.5pt; }}
.portada .sub {{ font-size: 12.5pt; color: #A9C0D4; max-width: 125mm; line-height: 1.55; }}
.portada .caja {{ border: 1.4pt solid #E8A04A; padding: 7mm 8mm; margin-top: 16mm;
  max-width: 128mm; }}
.portada .caja b {{ color: #E8A04A; }}
.portada .pie {{ margin-top: 18mm; font-size: 9pt; color: #7F9AB3; }}
.portada .cifra {{ font-size: 46pt; font-weight: bold; color: #E8A04A; line-height: 1; }}

.sec {{ page-break-before: always; }}
h2.tit {{ font-size: 17pt; color: #0E2438; border-bottom: 2.4pt solid #E8A04A;
  padding-bottom: 2.5mm; margin-bottom: 5mm; }}
h3.sub {{ font-size: 11.5pt; color: #B8752A; margin: 7mm 0 2.5mm;
  text-transform: uppercase; letter-spacing: .07em; }}
p {{ margin: 0 0 3mm; }}
.intro {{ color: #44586C; max-width: 165mm; }}

table {{ width: 100%; border-collapse: collapse; margin: 3mm 0 5mm; font-size: 9.2pt; }}
th {{ background: #0E2438; color: #fff; text-align: left; padding: 2.2mm 3mm;
  font-size: 8pt; letter-spacing: .06em; text-transform: uppercase; }}
td {{ padding: 2.2mm 3mm; border-bottom: .5pt solid #CFDAE4; vertical-align: top; }}
tr:nth-child(even) td {{ background: #F4F7FA; }}
td.m {{ font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt; color: #B8752A;
  white-space: nowrap; }}

.regla {{ border-left: 3.5pt solid #E8A04A; background: #FBF4E9; padding: 3.5mm 5mm;
  margin: 3.5mm 0; }}
.regla b {{ color: #B8752A; }}
.stop {{ border-left: 3.5pt solid #A33B2A; background: #FAECE8; padding: 3.5mm 5mm;
  margin: 3.5mm 0; }}
.stop b {{ color: #A33B2A; }}
.paleta {{ display: flex; gap: 4mm; margin: 3mm 0 5mm; }}
.chip {{ flex: 1; border: .5pt solid #CFDAE4; }}
.chip .col {{ height: 17mm; }}
.chip .et {{ padding: 2mm 3mm; font-size: 8.4pt; }}
.chip .et b {{ display: block; font-size: 9.5pt; }}

/* ── ficha de anuncio ── */
.ad {{ page-break-before: always; }}
.ad-cab {{ background: #0E2438; color: #fff; padding: 5mm 6mm; margin-bottom: 4mm; }}
.ad-cab .n {{ font-size: 8.5pt; color: #E8A04A; letter-spacing: .2em; font-weight: bold; }}
.ad-cab h2 {{ font-size: 18pt; margin: 1.5mm 0 2mm; }}
.ad-cab .fmt {{ font-size: 9.2pt; color: #A9C0D4; }}
.dentro {{ border: 1.2pt solid #0E2438; padding: 4mm 5mm; margin: 3mm 0 4mm; }}
.dentro h4 {{ font-size: 9pt; letter-spacing: .1em; text-transform: uppercase;
  color: #0E2438; margin-bottom: 2.5mm; }}
.kv {{ display: flex; gap: 3mm; padding: 1.6mm 0; border-top: .5pt solid #E3EAF1; }}
.kv:first-of-type {{ border-top: 0; }}
.kv .k {{ width: 42mm; font-size: 8.6pt; color: #5A6F84; flex: none; padding-top: .6mm; }}
.kv .v {{ font-weight: bold; font-size: 11pt; color: #0E2438; }}
.kv .v.norm {{ font-weight: normal; font-size: 9.6pt; }}
.prompt {{ background: #F4F7FA; border: .5pt solid #CFDAE4; border-left: 3.5pt solid #B8752A;
  padding: 3.5mm 4.5mm; font-family: "DejaVu Sans Mono", monospace; font-size: 8.3pt;
  line-height: 1.55; white-space: pre-wrap; }}
.copy {{ background: #F4F7FA; border-left: 3.5pt solid #0E2438; padding: 3.5mm 4.5mm;
  font-size: 9.4pt; line-height: 1.6; }}
.nota {{ font-size: 8.6pt; color: #5A6F84; font-style: italic; margin: 2mm 0 0; }}
ol.tarj {{ padding-left: 5mm; margin: 2mm 0 0; font-size: 9.3pt; }}
ol.tarj li {{ margin-bottom: 2mm; }}
ol.tarj b {{ color: #B8752A; }}
ul.chk {{ list-style: none; padding: 0; margin: 3mm 0; }}
ul.chk li {{ padding: 2.4mm 0 2.4mm 8mm; border-bottom: .5pt solid #CFDAE4;
  position: relative; font-size: 9.6pt; }}
ul.chk li:before {{ content: ""; position: absolute; left: 0; top: 2.8mm;
  width: 4.2mm; height: 4.2mm; border: 1.1pt solid #7A8CA0; }}
.pie-doc {{ margin-top: 8mm; padding-top: 3mm; border-top: .5pt solid #CFDAE4;
  font-size: 8pt; color: #7A8CA0; font-family: "DejaVu Sans Mono", monospace; }}

/* Cada ficha de anuncio ocupa unas dos paginas. Lo que importa no es que
   quepa en una, sino DONDE cae el corte: un prompt partido por la mitad es
   justo el bloque que el disenador tiene que copiar entero. */
.prompt, .copy, .dentro, .regla, .stop, table, ol.tarj, ul.chk,
.ad-cab, .paleta {{ page-break-inside: avoid; break-inside: avoid; }}
h2.tit, h3.sub, h4 {{ page-break-after: avoid; break-after: avoid; }}
tr {{ page-break-inside: avoid; break-inside: avoid; }}
</style></head><body>""")

    # ── PORTADA ─────────────────────────────────────────────────────────
    A(f"""<div class="portada">
<div class="marca">Design Modeling Academy</div>
<h1>Brief de artes<br>Pauta de septiembre</h1>
<p class="sub">Los 6 anuncios de la campana del Master BIM Management + IA,
con lo que hay que disenar en cada uno: medidas exactas, que texto va dentro
de la imagen y el prompt para generar el fondo.</p>
<div class="caja">
<div class="cifra">{total}</div>
<p style="margin:3mm 0 0"><b>archivos en total</b>, repartidos en 6 anuncios.<br>
Todos suben JUNTOS el lunes 7 de septiembre.</p>
</div>
<p class="pie">Generado desde <code>matriz-viral/matriz/calendario-septiembre.json</code>,
que es la matriz de contenido del mes. Si algo cambia ahi, este documento se
vuelve a generar — no se edita a mano.</p>
</div>""")

    # ── COMO SE USA ─────────────────────────────────────────────────────
    A("""<div class="sec"><h2 class="tit">Antes de empezar</h2>
<p class="intro">Cada anuncio de este documento trae tres cosas separadas a
proposito, porque las hace gente distinta:</p>
<table><thead><tr><th style="width:38mm">Bloque</th><th>Que es</th><th style="width:38mm">Quien lo usa</th></tr></thead><tbody>
<tr><td><b>Que entregas</b></td><td>Los archivos y sus medidas exactas.</td><td>Tu</td></tr>
<tr><td><b>Texto DENTRO de la imagen</b></td><td>Lo unico que se escribe encima del arte. Va tal cual: no se reescribe ni se resume.</td><td>Tu</td></tr>
<tr><td><b>Prompt del fondo</b></td><td>Se pega tal cual en la IA de imagen. Genera el fondo, no el texto.</td><td>Tu</td></tr>
<tr><td>Copy del anuncio</td><td>El texto que va en la publicacion, fuera de la imagen. Esta aqui solo para que sepas de que va la pieza.</td><td>Quien monta en Meta</td></tr>
</tbody></table>""")

    A(f"""<div class="stop"><b>LA REGLA QUE NO SE ROMPE — ninguna cifra en las artes del Master.</b><br>
{esc(ind.get('REGLA DE ORO — el Máster no lleva precio', ''))}
<br><br><b>En la practica, para ti:</b> si en una imagen te sale un numero de
precio, esta mal, aunque el texto que te pasaron lo tenga. Los meses SI van
(«3 meses» es duracion, no precio).</div>""")

    A(f"""<div class="stop"><b>EL SELLO ES BLOQUEANTE.</b><br>
{esc(ind.get('El sello es bloqueante', ''))}
<br><br><b>Para ti:</b> los cuatro anuncios de modulo llevan el sello de su
microcredencial DENTRO de la imagen, abajo a la derecha. Si el PNG con fondo
transparente todavia no te llego, pidelo antes de empezar — no montes el arte
pensando en anadirlo despues, porque hay que dejarle el hueco desde el principio.</div>""")

    # ── MARCA ───────────────────────────────────────────────────────────
    A("""<h3 class="sub">La paleta</h3>
<div class="paleta">
<div class="chip"><div class="col" style="background:#0E2438"></div>
<div class="et"><b>#0E2438</b>Azul marino. El fondo de todo.</div></div>
<div class="chip"><div class="col" style="background:#E8A04A"></div>
<div class="et"><b>#E8A04A</b>Ambar. Acento: lineas, el verbo, lo que hay que mirar.</div></div>
<div class="chip"><div class="col" style="background:#FFFFFF;border-bottom:.5pt solid #CFDAE4"></div>
<div class="et"><b>#FFFFFF</b>Blanco. Titulares y geometria.</div></div>
</div>
<h3 class="sub">Tipografia y estilo</h3>
<table><tbody>
<tr><td style="width:44mm"><b>Tipografia</b></td><td>Sans-serif de palo seco, muy gruesa. Titulares en mayuscula y con peso alto.</td></tr>
<tr><td><b>Composicion</b></td><td>Limpia y con aire. Mejor un elemento grande y bien puesto que tres pequenos.</td></tr>
<tr><td><b>Referencia visual</b></td><td>Estetica tecnica de ingenieria — Autodesk Revit, plano, blueprint, diagrama. Linea fina sobre fondo oscuro.</td></tr>
<tr><td><b>Iluminacion</b></td><td>Sobria. Sin brillos, sin degradados vistosos, sin efectos de neon.</td></tr>
</tbody></table>
<div class="stop"><b>Lo que NO va, en ninguna pieza:</b> stock corporativo, gente
sonriendo a camara, ciencia ficcion, logos de software reales (ni Revit ni
Autodesk), texto generado por la IA dentro de la imagen, y ninguna cifra de
precio.</div>""")

    # ── MEDIDAS Y ZONAS SEGURAS ─────────────────────────────────────────
    A(f"""<h3 class="sub">Medidas y margenes de seguridad</h3>
<table><thead><tr><th>Formato</th><th>Medida</th><th>Proporcion</th><th>Donde sale</th></tr></thead><tbody>
<tr><td>Post plano</td><td class="m">1080 x 1350 px</td><td class="m">4:5</td><td>Feed de Instagram y Facebook</td></tr>
<tr><td>Tarjeta de carrusel</td><td class="m">1080 x 1080 px</td><td class="m">1:1</td><td>Carrusel en feed</td></tr>
<tr><td>Version vertical</td><td class="m">1080 x 1920 px</td><td class="m">9:16</td><td>Historias y Reels</td></tr>
</tbody></table>
<div class="regla"><b>Los margenes de la version 9:16, que es donde se pierde el
trabajo.</b> Nada importante en los <b>250 px de arriba</b> ni en los <b>320 px
de abajo</b>: ahi es donde Instagram monta su propia interfaz y te tapa el
titular o el sello. Si el arte se va a usar tambien en historias, esa zona se
deja libre desde el diseno, no se recorta despues.</div>
<p class="nota">La fila completa de medidas, tal como esta escrita en la matriz:
"{esc(cfg0.get('Medidas',''))}"</p>""")

    # ── RESUMEN DE ENTREGA ──────────────────────────────────────────────
    A("""<h3 class="sub">Todo lo que hay que entregar</h3>
<table><thead><tr><th style="width:8mm">#</th><th>Anuncio</th><th>Que</th><th style="width:30mm">Medida</th><th style="width:16mm">Archivos</th></tr></thead><tbody>""")
    for i, p in enumerate(piezas, 1):
        filas = ENTREGA[p["id"]]
        for j, (que, med, prop, n) in enumerate(filas):
            A("<tr>")
            if j == 0:
                A(f'<td rowspan="{len(filas)}"><b>{i}</b></td>'
                  f'<td rowspan="{len(filas)}">{esc(p["titulo"])}</td>')
            A(f'<td>{esc(que)}</td><td class="m">{med}</td>'
              f'<td class="m" style="text-align:center">{n}</td></tr>')
    A(f'<tr><td colspan="4" style="text-align:right"><b>TOTAL</b></td>'
      f'<td class="m" style="text-align:center"><b>{total}</b></td></tr>')
    A("</tbody></table>")
    A(f"""<div class="regla"><b>Fecha.</b> {esc(ind.get('Fecha',''))}</div></div>""")

    # ── UNA FICHA POR ANUNCIO ───────────────────────────────────────────
    for i, p in enumerate(piezas, 1):
        pid = p["id"]
        A(f"""<div class="ad"><div class="ad-cab">
<div class="n">ANUNCIO {i} DE 6</div>
<h2>{esc(p['titulo'])}</h2>
<div class="fmt">{esc(p['formato'])} &nbsp;·&nbsp; {esc(p['precio'])}</div>
</div>""")

        # que entregas
        A('<h3 class="sub">Que entregas</h3><table><thead><tr>'
          '<th>Archivo</th><th style="width:34mm">Medida</th>'
          '<th style="width:20mm">Proporcion</th><th style="width:20mm">Cantidad</th>'
          '</tr></thead><tbody>')
        for que, med, prop, n in ENTREGA[pid]:
            A(f'<td>{esc(que)}</td><td class="m">{med}</td><td class="m">{prop}</td>'
              f'<td class="m" style="text-align:center">{n}</td></tr>')
        A("</tbody></table>")

        # texto dentro de la imagen
        A('<div class="dentro"><h4>Texto que va DENTRO de la imagen</h4>')
        if pid in DENTRO:
            dd = DENTRO[pid]
            A(f'<div class="kv"><div class="k">Titular grande</div>'
              f'<div class="v">{esc(dd["titulo_img"])}</div></div>')
            A(f'<div class="kv"><div class="k">Verbo, debajo, en ambar</div>'
              f'<div class="v" style="color:#B8752A">{esc(dd["verbo"])}</div></div>')
            A(f'<div class="kv"><div class="k">Sello, abajo a la derecha</div>'
              f'<div class="v">{esc(dd["sello"])}</div></div>')
            A('<div class="kv"><div class="k">Cifras</div>'
              '<div class="v norm">Ninguna. Ni precio ni suma. La duracion en meses '
              'va en el titular del anuncio, no dentro de la imagen.</div></div>')
        elif pid == "diagnostico":
            A('<div class="kv"><div class="k">Cuatro frases, una por banda</div>'
              '<div class="v norm">'
              '1. Necesito implementar BIM<br>'
              '2. Quiero coordinar disciplinas<br>'
              '3. Quiero costos y liderazgo<br>'
              '4. Quiero IA y automatizacion</div></div>')
            A('<div class="kv"><div class="k">Cifras</div>'
              '<div class="v norm">Ninguna.</div></div>')
        else:
            A('<div class="kv"><div class="k">Tarjeta 1</div>'
              '<div class="v norm">En que etapa BIM estas?</div></div>')
            A('<div class="kv"><div class="k">Tarjetas 2 a 5</div>'
              '<div class="v norm">Una puerta por tarjeta, con su verbo, su duracion '
              'en meses y su microcredencial:<br>'
              '2. BIM Professional - ESTRUCTURA - 3 meses - MODELADOR BIM<br>'
              '3. BIM Coordination - COORDINA - 3 meses - COORDINADOR BIM<br>'
              '4. BIM Management - GESTIONA - 2 meses - BIM MANAGER 4D-5D<br>'
              '5. BIM + IA - AUTOMATIZA - 3 meses - ESPECIALISTA BIM + IA</div></div>')
            A('<div class="kv"><div class="k">Cifras</div>'
              '<div class="v norm">NINGUNA cifra en NINGUNA tarjeta. Los meses si van.</div></div>')
        A("</div>")

        # las 3 tarjetas del carrusel de modulo
        if pid in DENTRO:
            A('<h3 class="sub">Las 3 tarjetas del carrusel</h3><ol class="tarj">')
            for _, papel, det in TARJETAS_MODULO:
                A(f"<li><b>{esc(papel)}</b> — {esc(det)}</li>")
            A("</ol>")
            A('<p class="nota">Esta estructura esta escrita en la ficha del Modulo 1 '
              'y se aplica a los cuatro modulos, que llevan el mismo formato. Si en '
              'algun modulo conviene otra cosa, se decide antes de disenar, no despues.</p>')

        # descripcion del creativo
        A(f'<h3 class="sub">Como se ve</h3><div class="copy">{esc(p["creativo"])}</div>')

        # prompt
        A('<h3 class="sub">Prompt del fondo — se pega tal cual en la IA</h3>'
          f'<div class="prompt">{esc(p["prompt"])}</div>'
          '<p class="nota">La IA entrega el fondo y los elementos. El texto se monta '
          'encima en Canva: si la imagen sale con letras, se descarta y se vuelve a '
          'generar — las letras que inventa la IA salen mal escritas.</p>')

        # copy del anuncio, de contexto
        A('<h3 class="sub">Copy del anuncio <span style="font-weight:normal;'
          'text-transform:none;letter-spacing:0;color:#5A6F84">— va fuera de la '
          'imagen, es solo contexto</span></h3>')
        A('<table><tbody>'
          f'<tr><td style="width:34mm"><b>Titular</b></td><td>{esc(p["titular"])}</td></tr>'
          f'<tr><td><b>Descripcion</b></td><td>{esc(p["descripcion"])}</td></tr>'
          '</tbody></table>')
        A(f'<div class="copy">{esc(p["cuerpo"])}</div>')
        A("</div>")

    # ── CIERRE ──────────────────────────────────────────────────────────
    A("""<div class="sec"><h2 class="tit">Antes de entregar</h2>
<p class="intro">Una pasada por cada archivo. Las tres primeras son las que
mas veces han hecho repetir un arte.</p>
<ul class="chk">
<li>Ninguna cifra de precio en la imagen — ni en el fondo, ni en el sello, ni en letra pequena.</li>
<li>El sello de la microcredencial esta puesto, y es el que le toca a ese modulo.</li>
<li>Si el arte se va a usar en historias: nada importante en los 250 px de arriba ni en los 320 de abajo.</li>
<li>El fondo es #0E2438 y el acento es #E8A04A. Sin colores de fuera de la paleta.</li>
<li>No hay texto generado por la IA dentro de la imagen.</li>
<li>No hay logos de software reales ni marcas de terceros.</li>
<li>No hay personas sonriendo a camara ni stock corporativo.</li>
<li>Las tarjetas del carrusel tienen la misma composicion y la misma escala entre si.</li>
<li>El archivo esta a la medida exacta en px, no escalado.</li>
</ul>""")

    A(f"""<h3 class="sub">Dos cosas mas, que no son de diseno pero afectan al arte</h3>
<div class="regla"><b>Facebook no se apaga.</b> {esc(ind.get('Facebook no se apaga',''))}
Por eso el arte tiene que leerse bien tambien en Facebook, que recorta distinto.</div>
<div class="regla"><b>Los videos son un set.</b> {esc(ind.get('Los videos son un set',''))}</div>
<p class="pie-doc">Design Modeling Academy · Brief de artes de la pauta de septiembre 2026<br>
Generado desde matriz-viral/matriz/calendario-septiembre.json<br>
Dudas sobre el contenido: Dayana. Dudas sobre el montaje en Meta: Patricio.</p>
</div></body></html>""")

    return "\n".join(P)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=str(SALIDA))
    args = ap.parse_args()

    if not FUENTE.exists():
        print(f"::error::No esta {FUENTE}", file=sys.stderr)
        return 1

    datos = json.loads(FUENTE.read_text(encoding="utf-8"))
    doc = construir_html(datos)

    destino = pathlib.Path(args.salida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".html")
    tmp.write_text(doc, encoding="utf-8")

    binario = next((b for b in CHROMIUM if pathlib.Path(b).exists()), None)
    if not binario:
        binario = shutil.which("chromium") or shutil.which("google-chrome")
    if not binario:
        print("::error::No hay Chromium para imprimir el PDF.", file=sys.stderr)
        return 1

    r = subprocess.run([
        binario, "--headless", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={destino}", tmp.as_uri(),
    ], capture_output=True, text=True, timeout=180)

    if not destino.exists():
        print(f"::error::Chromium no genero el PDF.\n{r.stderr[:600]}", file=sys.stderr)
        return 1

    tmp.unlink(missing_ok=True)
    print(f"Escrito {destino} — {destino.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
