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


# origen → destino
PAGINAS = [
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

    # ./algo  →  https://…/<carpeta>/algo   (en href, src y en el JS)
    # El patrón del JS admite query strings ('./app.html?acceso='), que es
    # justo el caso que se escapaba antes.
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
    for origen_, destino_ in PAGINAS:
        salida_ = construir(sys.argv[1], origen_, destino_)
        kb = salida_.stat().st_size / 1024
        print(f"OK → {salida_}  ({kb:.0f} KB)")
