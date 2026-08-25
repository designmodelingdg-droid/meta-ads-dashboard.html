#!/usr/bin/env python3
"""Comprueba que todo lo que prometemos en el contenido siga vivo.

Por que existe: el 24-ago-2026 el Test de Nivel BIM y la Calculadora de Zapatas
llevaban horas devolviendo 404. Las detecto Dayana de casualidad, y mientras
tanto cada persona que comentaba NIVEL o ZAPATA recibia un enlace roto. Esas
dos son el destino de dos palabras del bot.

No hace falta navegador: los 404 se ven con una peticion normal. Esto recorre
todas las URLs que el repositorio promete y avisa de las que se cayeron.

Que revisa:
  - Los enlaces del funnel y de la academia que aparecen en el contenido.
  - Los lead magnets publicados en GitHub Pages.
  - Marca aparte los que son DESTINO DE UNA PALABRA DEL BOT, porque esos no
    son un enlace roto cualquiera: son leads que se pierden en el momento.

Uso:
    python3 scripts/enlaces.py
    python3 scripts/enlaces.py --json      # solo el JSON, sin informe
"""

import argparse
import concurrent.futures
import datetime
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "matriz-viral/fuentes/enlaces.json"

# Navegador de verdad: sin esto Cloudflare devuelve 1010 y parece que la pagina
# esta caida cuando no lo esta. Es el mismo error que ya nos costo una lectura
# equivocada con la API de GoHighLevel.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# Los destinos de las palabras del bot. Si uno de estos cae, se pierden leads
# en vivo, asi que se reportan aparte y con otro nivel de alarma.
CRITICOS = {
    "https://funnel.dgdesignmodeling.com/test-nivel-bim": "palabra NIVEL",
    "https://funnel.dgdesignmodeling.com/calculadora-zapatas": "palabra ZAPATA",
    "https://designmodelingacademy.com/es/especializacion/diseno-estructural-bim-acero":
        "palabra ACERO",
}

# Los respaldos en GitHub Pages: si el destino principal cae, estos siguen
# sirviendo y el bot se puede reapuntar mientras se arregla.
RESPALDOS = {
    "https://funnel.dgdesignmodeling.com/test-nivel-bim":
        "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/",
    "https://funnel.dgdesignmodeling.com/calculadora-zapatas":
        "https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/",
}

DOMINIOS = ("funnel.dgdesignmodeling.com", "designmodelingacademy.com",
            "designmodelingdg-droid.github.io")

PATRON = re.compile(r"https://(?:" + "|".join(d.replace(".", r"\.") for d in DOMINIOS)
                    + r")/[A-Za-z0-9/_.-]*")


def recolectar():
    """Todas las URLs que el repositorio promete, con donde aparece cada una."""
    encontrado = {}
    for ext in ("*.md", "*.json", "*.html"):
        for f in RAIZ.rglob(ext):
            partes = f.parts
            if "node_modules" in partes or ".git" in partes:
                continue
            try:
                texto = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:                                   # noqa: BLE001
                continue
            for u in PATRON.findall(texto):
                u = u.rstrip(".,);:\"'")
                encontrado.setdefault(u, set()).add(str(f.relative_to(RAIZ)))
    for u in list(CRITICOS) + list(RESPALDOS.values()):
        encontrado.setdefault(u, set()).add("(destino del bot)")
    return {u: sorted(v) for u, v in encontrado.items()}


def probar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return url, r.status, None
    except urllib.error.HTTPError as e:
        return url, e.code, None
    except Exception as e:                                      # noqa: BLE001
        return url, None, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="solo escribe el JSON")
    args = ap.parse_args()

    urls = recolectar()
    resultados = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for url, cod, err in ex.map(probar, urls):
            resultados[url] = {"codigo": cod, "error": err,
                               "aparece_en": urls[url][:6],
                               "critico": CRITICOS.get(url)}

    caidas = {u: r for u, r in resultados.items() if r["codigo"] != 200}
    criticas = {u: r for u, r in caidas.items() if r["critico"]}

    salida = {
        "generado": datetime.date.today().isoformat(),
        "revisadas": len(resultados),
        "caidas": len(caidas),
        "criticas": len(criticas),
        "resultados": resultados,
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1),
                      encoding="utf-8")

    if not args.json:
        print(f"Revisadas {len(resultados)} · caidas {len(caidas)}\n")
        if criticas:
            print("CAIDAS QUE CUESTAN LEADS AHORA MISMO:")
            for u, r in criticas.items():
                print(f"  [{r['codigo']}] {u}")
                print(f"        es el destino de la {r['critico']}")
                sup = RESPALDOS.get(u)
                if sup:
                    print(f"        respaldo que si funciona: {sup}")
            print()
        otras = {u: r for u, r in caidas.items() if not r["critico"]}
        if otras:
            print("Otras caidas:")
            for u, r in otras.items():
                print(f"  [{r['codigo'] or r['error']}] {u}")
                print(f"        aparece en: {', '.join(r['aparece_en'][:3])}")
        if not caidas:
            print("Todo responde 200.")

    # Codigo 1 solo si cae algo critico: eso es lo que merece romper la corrida
    # y mandar un aviso. Un enlace secundario roto se anota y ya.
    return 1 if criticas else 0


if __name__ == "__main__":
    raise SystemExit(main())
