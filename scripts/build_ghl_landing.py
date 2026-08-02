#!/usr/bin/env python3
"""Genera <carpeta>/ghl-landing.html a partir de <carpeta>/index.html.

La versión para GoHighLevel es el mismo landing pero listo para pegarse en un
contenedor "Custom Code": sin <html>/<head>/<body>, con el <style> incrustado y
con TODAS las rutas relativas convertidas en absolutas (porque el HTML va a
vivir en el dominio de GHL, no en GitHub Pages).

Uso:  python3 scripts/build_ghl_landing.py test-nivel-bim
No editar ghl-landing.html a mano: se regenera.
"""
import re
import sys
from pathlib import Path

BASE_PAGES = "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html"


def construir(carpeta: str) -> Path:
    raiz = Path(__file__).resolve().parent.parent
    src = raiz / carpeta / "index.html"
    dst = raiz / carpeta / "ghl-landing.html"
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
    body = re.sub(r'(href|src)="\./', rf'\1="{base}/', body)
    body = re.sub(r"'\./([\w.\-/]+)'", rf"'{base}/\1'", body)

    # Las fuentes se cargan aparte porque <head> no viaja en el Custom Code.
    fuentes = ('<link href="https://fonts.googleapis.com/css2?family=Overpass:'
               'wght@500;600;700;800;900&family=Nunito:wght@400;500;600;700'
               '&display=swap" rel="stylesheet">')

    salida = (
        "<!-- ============================================================\n"
        f"     {carpeta} · versión para GoHighLevel (Custom Code)\n"
        "     GENERADO AUTOMÁTICAMENTE — no editar a mano.\n"
        "     Se regenera con: python3 scripts/build_ghl_landing.py "
        f"{carpeta}\n"
        "     Pegar en: Sites → página → elemento Custom Code,\n"
        "     a ancho completo y sin padding.\n"
        "     ============================================================ -->\n"
        f"{fuentes}\n<style>{css}</style>\n{body}\n"
    )
    dst.write_text(salida, encoding="utf-8")
    return dst


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 scripts/build_ghl_landing.py <carpeta>")
    destino = construir(sys.argv[1])
    kb = destino.stat().st_size / 1024
    print(f"OK → {destino}  ({kb:.0f} KB)")
