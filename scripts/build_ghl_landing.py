#!/usr/bin/env python3
"""Genera las versiones para GoHighLevel de las páginas de un lead magnet.

De cada página hace una versión lista para pegarse en un contenedor
"Custom Code": sin <html>/<head>/<body>, con el <style> incrustado y con TODAS
las rutas relativas convertidas en absolutas — esto último es crítico, porque
el HTML va a vivir en el dominio de GHL mientras que la app y las imágenes
siguen en GitHub Pages.

    index.html          →  ghl-landing.html
    gracias-agenda.html →  ghl-gracias.html

Uso:  python3 scripts/build_ghl_landing.py test-nivel-bim
No editar los ghl-*.html a mano: se regeneran.
"""
import re
import sys
from pathlib import Path

BASE_PAGES = "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html"

# Dominio propio de DMA: las PÁGINAS del funnel viven aquí (GoHighLevel), para
# que el usuario nunca vea que cambia de dominio. Los ASSETS (imágenes) y la
# app en sí se siguen sirviendo desde GitHub Pages, embebidos por iframe.
DOMINIO = "https://funnel.dgdesignmodeling.com"

# Enlaces entre páginas del funnel: se reescriben al dominio propio SOLO donde
# la página de GHL ya existe y sabemos su URL exacta.
#
# Esto era un diccionario fijo con las rutas de test-nivel-bim que se aplicaba
# a TODAS las carpetas: las versiones de GHL de guia-revit-ia, memoria-calculo
# y pack-dynamo salieron enlazando a la página de gracias de OTRO lead magnet.
# Quien descargara la guía de Revit habría aterrizado en el test de nivel.
#
# El arreglo NO es deducir la ruta del nombre de la carpeta: el slug real de
# test-nivel-bim es «acceso-gratis-test-nivel-bim-gracias», no
# «test-nivel-bim/gracias». Inventar la URL rompe la página que hoy funciona.
# Carpeta que no esté aquí conserva sus enlaces a GitHub Pages, que existen.
FUNNEL_POR_CARPETA = {
    "test-nivel-bim": {
        "gracias-agenda.html": f"{DOMINIO}/acceso-gratis-test-nivel-bim-gracias",
        "app.html": f"{DOMINIO}/test-nivel-bim/test",
    },
}


def rutas_funnel(carpeta: str) -> dict:
    return FUNNEL_POR_CARPETA.get(carpeta, {})


# origen → destino, por carpeta. Cada lead magnet tiene sus propias páginas:
# el hub de recursos, por ejemplo, es una sola.
PAGINAS_POR_CARPETA = {
    "test-nivel-bim": [
        ("index.html", "ghl-landing.html"),
        ("gracias-agenda.html", "ghl-gracias.html"),
    ],
    "calculadora-zapatas": [
        ("index.html", "ghl-landing.html"),
        ("gracias-agenda.html", "ghl-gracias.html"),
    ],
    "recursos": [
        ("index.html", "ghl-recursos.html"),
    ],
}
# Todo lead magnet tiene landing y página de gracias: las dos hacen falta
# dentro de GHL, porque el formulario nativo redirige a la de gracias.
PAGINAS_POR_DEFECTO = [
    ("index.html", "ghl-landing.html"),
    ("gracias-agenda.html", "ghl-gracias.html"),
]

# Alto de reserva del marco de la lección, en píxeles. Es el alto REAL de cada
# guía a 400 px de ancho —el peor caso, el del teléfono— más un 5%. Medido con
# el navegador, esperando a que carguen imágenes y fuentes; medir a los 400 ms
# se queda corto y el contenido sale cortado.
#
# Solo se usa si el editor de GHL borra el <script> que ajusta el alto solo.
# Se prefiere que sobre hueco a que falte: un hueco en blanco es feo, contenido
# cortado es una guía que no se puede leer.
ALTO_LECCION = {
    "guia-revit-ia":   17200,
    "memoria-calculo": 13100,
    "pack-dynamo":      7300,
}


def construir(carpeta: str, origen: str, destino: str) -> Path:
    raiz = Path(__file__).resolve().parent.parent
    src = raiz / carpeta / origen
    dst = raiz / carpeta / destino
    if not src.exists():
        sys.exit(f"No existe {src}")

    html = src.read_text(encoding="utf-8")
    base = f"{BASE_PAGES}/{carpeta}"

    estilo = re.search(r"<style>(.*?)</style>", html, re.S)
    cuerpo = re.search(r"<body>(.*?)</body>", html, re.S)
    if not estilo or not cuerpo:
        sys.exit("index.html no tiene <style> o <body>; revisa la plantilla.")

    css, body = estilo.group(1), cuerpo.group(1)

    # 1) Los enlaces ENTRE PÁGINAS del funnel van al dominio propio, para que
    #    el usuario no vea nunca que salta a github.io.
    for pagina, destino in rutas_funnel(carpeta).items():
        body = body.replace(f'"./{pagina}', f'"{destino}')
        body = body.replace(f"'./{pagina}", f"'{destino}")

    # 2) Lo que queda relativo son assets (img/…): esos sí van a Pages.
    body = re.sub(r'(href|src)="\./', rf'\1="{base}/', body)
    body = re.sub(r"'\./([\w.\-/?=&%]*)'", rf"'{base}/\1'", body)

    # Las fuentes se cargan aparte porque <head> no viaja en el Custom Code.
    fuentes = ('<link href="https://fonts.googleapis.com/css2?family=Overpass:'
               'wght@500;600;700;800;900&family=Nunito:wght@400;500;600;700'
               '&display=swap" rel="stylesheet">')

    salida = (
        "<!-- ============================================================\n"
        f"     {carpeta}/{origen} · versión para GoHighLevel (Custom Code)\n"
        "     GENERADO AUTOMÁTICAMENTE — no editar a mano.\n"
        "     Se regenera con: python3 scripts/build_ghl_landing.py "
        f"{carpeta}\n"
        "     Pegar en: Sites → página → elemento Custom Code,\n"
        "     a ancho completo y sin padding.\n"
        "     ============================================================ -->\n"
        f"{fuentes}\n<style>{css}</style>\n{body}\n"
    )
    dst.write_text(salida, encoding="utf-8")

    # Red de seguridad: en la versión de GHL no puede quedar ninguna ruta
    # relativa, porque apuntaría al dominio de GHL en vez de a GitHub Pages.
    relativas = re.findall(r'(?:href|src)="\./[^"]*"|\'\./[^\']*\'', salida)
    if relativas:
        sys.exit(f"✖ {dst.name} quedó con rutas relativas: {relativas}")
    return dst


def construir_leccion(carpeta: str) -> Path:
    """El trozo que se pega en la lección del producto dentro de GHL.

    La guía va en un <iframe> porque es una página entera con su CSS y su JS:
    pegada en el editor de texto de la lección, GHL le borra el <style> y sale
    desmaquetada. El <iframe> la sirve tal cual desde GitHub Pages.

    El alto lo dice la propia guía por postMessage (ver el bloque «Modo
    incrustado» en guia.html) y este trozo lo escucha. Si GHL borra este
    <script>, queda el alto de reserva y no se corta nada.
    """
    raiz = Path(__file__).resolve().parent.parent
    alto = ALTO_LECCION.get(carpeta)
    if alto is None:
        sys.exit(f"Falta el alto de reserva de {carpeta} en ALTO_LECCION")
    guia = f"{BASE_PAGES}/{carpeta}/guia.html?acceso=dm2026"
    dst = raiz / carpeta / "ghl-leccion.html"
    dst.write_text(
        "<!-- ============================================================\n"
        f"     {carpeta} · para la LECCIÓN del producto en GoHighLevel\n"
        "     GENERADO AUTOMÁTICAMENTE — no editar a mano.\n"
        f"     Se regenera con: python3 scripts/build_ghl_landing.py {carpeta}\n"
        "     Pegar con el botón <> (código fuente) de la descripción\n"
        "     de la lección. No hace falta ningún botón: la guía se lee\n"
        "     dentro de la lección.\n"
        "     ============================================================ -->\n"
        f'<iframe id="dma-guia" src="{guia}"\n'
        f'        style="width:100%;height:{alto}px;border:0;display:block"\n'
        '        loading="lazy" title="Guía"></iframe>\n'
        "<script>\n"
        "/* La guía avisa de cuánto mide y el marco se ajusta: sin esto queda\n"
        "   una segunda barra de scroll dentro de la lección. Si GHL borra este\n"
        f"   script, el marco se queda en {alto} px y se lee igual. */\n"
        "addEventListener('message', function (e) {\n"
        "  if (!e.data || e.data.dma !== 'alto') return;\n"
        "  var f = document.getElementById('dma-guia');\n"
        "  if (f) f.style.height = (e.data.alto + 40) + 'px';\n"
        "});\n"
        "</script>\n",
        encoding="utf-8")
    return dst


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 scripts/build_ghl_landing.py <carpeta>")
    carpeta_ = sys.argv[1]
    paginas_ = PAGINAS_POR_CARPETA.get(carpeta_, PAGINAS_POR_DEFECTO)
    for origen_, destino_ in paginas_:
        salida_ = construir(carpeta_, origen_, destino_)
        kb = salida_.stat().st_size / 1024
        print(f"OK → {salida_}  ({kb:.0f} KB)")
    if carpeta_ in ALTO_LECCION:
        salida_ = construir_leccion(carpeta_)
        print(f"OK → {salida_}  (lección)")
