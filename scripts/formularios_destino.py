#!/usr/bin/env python3
"""A donde manda DE VERDAD el formulario de cada lead magnet.

Por que existe: el 25-ago-2026 Dayana lleno el formulario de ACERO y cayo en la
confirmacion de un webinar de FEBRERO DE 2025. Nunca recibio la guia. Lo mismo
en los ocho lead magnets.

Y no se veia mirando la configuracion. El destino "por defecto" de cada
formulario era el correcto — se comprobo uno por uno y los ocho apuntaban a su
propia pagina de gracias. Lo que mandaba era una REGLA CONDICIONAL, que en GHL
gana sobre el destino por defecto:

    si  full_name esta lleno  O  email esta lleno  O  phone esta lleno
    entonces  redirigir a  /webinar-certificados-confirmacion

Con «o» y con «esta lleno» en campos obligatorios, esa regla se cumple SIEMPRE.

Como se lee: el widget de GHL viene como payload de Nuxt, donde los objetos no
traen valores sino INDICES a una tabla de cadenas. Buscar la URL que aparece
cerca de «redirectUrl» no sirve: en el payload hay varias y solo una es la
activa. Hay que resolver el indice contra la tabla. Eso es lo que hace esto.

    python3 scripts/formularios_destino.py
"""
import json, re, sys, urllib.request

BASE   = "https://funnel.dgdesignmodeling.com"
WIDGET = "https://link.apisystem.tech/widget/form"
SALIDA = "matriz-viral/fuentes/ghl/formularios-destino.json"

LANDINGS = [
    "acceso-gratis-verificaciones-acero-form",
    "acceso-gratis-calculadora-zapatas-form",
    "acceso-gratis-test-nivel-bim-form",
    "acceso-gratis-curso-introductorio-bim-form",
    "acceso-gratis-modulo-diplomado-bim-form",
    "descarga-gratis-ebook-bim-form",
    "descarga-gratis-guia-bim-form",
    "descarga-gratis-ai-pro-form",
]

UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/126.0.0.0 Safari/537.36")}


def bajar(url):
    r = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(r, timeout=40).read().decode("utf-8", "replace")


def tabla(texto, ancla):
    """Aisla el array del payload de Nuxt que contiene `ancla`."""
    i = texto.find(ancla)
    if i < 0:
        return None
    pos = i
    for _ in range(400):
        pos = texto.rfind("[", 0, pos)
        if pos < 0:
            return None
        for fin in re.finditer(r"\]", texto[pos:pos + 900000]):
            cand = texto[pos:pos + fin.end()]
            if len(cand) < 5000:
                continue
            try:
                a = json.loads(cand)
                if isinstance(a, list) and len(a) > 100:
                    return a
            except Exception:
                pass
    return None


def revisar(landing):
    out = {"landing": landing}
    try:
        html = bajar(f"{BASE}/{landing}")
    except Exception as e:
        return {**out, "error": f"no carga la landing: {e}"}

    m = re.search(r"widget.{0,12}form.{0,14}([A-Za-z0-9]{20})", html)
    if not m:
        return {**out, "error": "no hay formulario nativo embebido"}
    out["formulario"] = m.group(1)

    try:
        f = bajar(f"{WIDGET}/{out['formulario']}")
    except Exception as e:
        return {**out, "error": f"no carga el widget: {e}"}

    # 1 · el destino POR DEFECTO
    mm = re.search(r'\{"actionType":(\d+)[^{}]*?"redirectUrl":(\d+)', f)
    if mm:
        arr = tabla(f, mm.group(0))
        if arr:
            out["accion"] = str(arr[int(mm.group(1))])
            out["destino_por_defecto"] = arr[int(mm.group(2))] or ""

    # 2 · la REGLA CONDICIONAL, que gana sobre el destino por defecto
    cond = re.search(r'"redirectToUrl","([^"]*)"', f)
    if cond:
        out["regla_condicional"] = cond.group(1).replace("\\u002F", "/")
        ctx = f[max(0, f.find('"redirectToUrl"') - 400):f.find('"redirectToUrl"')]
        out["condiciones"] = re.findall(
            r'"([a-z_]{4,30})","(isFilled|isEmpty|isEqualTo)"', ctx)

    # 3 · el veredicto: a donde cae la persona de verdad
    real = out.get("regla_condicional") or out.get("destino_por_defecto", "")
    esperado = landing.replace("-form", "-gracias")
    out["destino_real"] = real
    out["correcto"] = esperado in real
    return out


def main():
    filas, malos = [], []
    print(f"{'LANDING':46} DESTINO REAL")
    print("-" * 124)
    for l in LANDINGS:
        r = revisar(l)
        filas.append(r)
        if r.get("error"):
            print(f"   {l:44} ERROR: {r['error']}")
            continue
        marca = "   " if r["correcto"] else " ⚠️"
        print(f"{marca}{l:44} {r['destino_real']}")
        if r.get("regla_condicional"):
            print(f"{'':47} ↑ por REGLA CONDICIONAL, no por el destino por defecto")
            print(f"{'':47}   (el por defecto es {r.get('destino_por_defecto')})")
        if not r["correcto"]:
            malos.append(r)

    res = {"comprobado": __import__("datetime").date.today().isoformat(),
           "formularios": filas,
           "mal_apuntados": [m["landing"] for m in malos]}
    import os
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print()
    if malos:
        print(f"MAL APUNTADOS: {len(malos)} de {len(LANDINGS)}")
        print("Quien llena esos formularios NO llega a su recurso.")
        sys.exit(1)
    print(f"Los {len(LANDINGS)} mandan a su propia pagina de gracias.")


if __name__ == "__main__":
    main()
