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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 scripts/build_ghl_landing.py <carpeta>")
    carpeta_ = sys.argv[1]
    paginas_ = PAGINAS_POR_CARPETA.get(carpeta_, PAGINAS_POR_DEFECTO)
    for origen_, destino_ in paginas_:
        salida_ = construir(carpeta_, origen_, destino_)
        kb = salida_.stat().st_size / 1024
        print(f"OK → {salida_}  ({kb:.0f} KB)")
