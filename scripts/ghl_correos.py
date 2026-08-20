#!/usr/bin/env python3
"""
Saca el inventario de correos de las automatizaciones de GoHighLevel.

POR QUÉ EXISTE
    El skill `auditoria-correos-sharp-crm` hace este inventario a mano, con el
    navegador: entrar carpeta por carpeta, workflow por workflow, y abrir cada
    plantilla. Son decenas de workflows y es facil dejarse alguno.

    Esto intenta lo mismo por API. Y hay un limite conocido, comprobado contra
    la documentacion oficial el 19-ago-2026:

        GET /workflows/ devuelve SOLO metadatos — id, name, status, version,
        createdAt, updatedAt, locationId. NO devuelve los pasos del workflow,
        ni el asunto, ni el cuerpo, ni el id de la plantilla.

    O sea: la API da la LISTA de automatizaciones y (si el endpoint de
    plantillas abre) el CONTENIDO de los correos, pero no el mapa de que
    workflow usa que plantilla. Ese cruce sigue siendo trabajo de navegador.

    Esta sonda existe para saber exactamente cuanto se puede automatizar antes
    de mandar a nadie a hacer 40 clics.

USO
    GHL_TOKEN=xxx python3 scripts/ghl_correos.py
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error
from datetime import date

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"
V2 = "https://services.leadconnectorhq.com"
SALIDA = "matriz-viral/fuentes/ghl"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def api(ruta, version="2021-07-28", **params):
    """Una peticion. `version` importa: /workflows/ pide v3 y el resto 2021-07-28."""
    url = f"{V2}{ruta}"
    if params:
        url += ("&" if "?" in ruta else "?") + urllib.parse.urlencode(params)
    cab = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json",
           "Version": version, "User-Agent": UA}
    r = urllib.request.Request(url, headers=cab)
    try:
        with urllib.request.urlopen(r, timeout=40) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode()[:220]
        lectura = {401: "el token no autentica aqui",
                   403: "autentica pero sin permiso (o Cloudflare: mirar el cuerpo)",
                   404: "la ruta no existe en la API",
                   422: "la ruta existe y el token entra: faltan parametros"}
        return {"_error": f"HTTP {e.code}", "_lectura": lectura.get(e.code),
                "_detalle": cuerpo}
    except Exception as e:                       # noqa: BLE001
        return {"_error": str(e)[:200]}


def workflows():
    """La lista de automatizaciones. Solo metadatos: la API no da los pasos."""
    for v in ("v3", "2021-07-28"):
        d = api("/workflows/", version=v, locationId=LOCATION)
        if "_error" not in d:
            ws = d.get("workflows", []) or []
            return {"version_que_funciono": v, "total": len(ws),
                    "workflows": [{"id": w.get("id"), "nombre": w.get("name"),
                                   "estado": w.get("status"),
                                   "actualizado": w.get("updatedAt")} for w in ws],
                    "aviso": ("Solo metadatos. Los pasos de cada workflow —y por tanto "
                              "que plantilla usa cada 'Enviar correo'— NO los expone la "
                              "API: eso sigue siendo trabajo de navegador.")}
    return d


def plantillas():
    """Las plantillas de correo. Se prueban varias rutas: la doc no es publica."""
    intentos = [
        ("/emails/builder", {"locationId": LOCATION, "limit": 100}),
        ("/emails/builder/", {"locationId": LOCATION, "limit": 100}),
        ("/emails/templates", {"locationId": LOCATION, "limit": 100}),
        ("/templates/", {"locationId": LOCATION, "limit": 100, "type": "email"}),
        (f"/locations/{LOCATION}/templates", {"limit": 100, "type": "email"}),
    ]
    fallos = {}
    for ruta, params in intentos:
        d = api(ruta, **params)
        if "_error" not in d:
            filas = None
            for k in ("data", "templates", "builders", "docs"):
                if isinstance(d.get(k), list):
                    filas = d[k]; break
            if filas is None:
                filas = [v for v in d.values() if isinstance(v, list)]
                filas = filas[0] if filas else []
            return {"ruta_que_funciono": ruta, "total": d.get("total", len(filas)),
                    "en_esta_pagina": len(filas),
                    "campos_de_una": sorted(filas[0].keys())[:25] if filas else [],
                    "plantillas": [{"id": t.get("id") or t.get("_id"),
                                    "nombre": t.get("name") or t.get("templateName"),
                                    "tipo": t.get("templateType") or t.get("type"),
                                    "actualizado": t.get("updatedAt") or t.get("dateUpdated")}
                                   for t in filas]}
        fallos[ruta] = {"error": d["_error"], "lectura": d.get("_lectura")}
        time.sleep(0.3)
    return {"_error": "ninguna ruta de plantillas respondio", "intentos": fallos}


def main():
    if not TOKEN:
        print("ERROR: falta GHL_TOKEN en el entorno.", file=sys.stderr)
        sys.exit(1)
    os.makedirs(SALIDA, exist_ok=True)

    res = {"generado": date.today().isoformat(), "location": LOCATION,
           "para_que": ("Saber cuanto del inventario de correos se puede sacar por API "
                        "y cuanto necesita navegador.")}

    print("→ Automatizaciones…")
    res["workflows"] = workflows()
    if "_error" in res["workflows"]:
        print(f"   ERROR: {res['workflows']['_error']} · {res['workflows'].get('_lectura','')}")
    else:
        print(f"   {res['workflows']['total']} workflows (via {res['workflows']['version_que_funciono']})")

    print("→ Plantillas de correo…")
    res["plantillas"] = plantillas()
    if "_error" in res["plantillas"]:
        print("   ninguna ruta respondio:")
        for ruta, f in res["plantillas"]["intentos"].items():
            print(f"     {ruta:44} {f['error']} · {f.get('lectura') or ''}")
    else:
        p = res["plantillas"]
        print(f"   {p['total']} plantillas via {p['ruta_que_funciono']}")
        print(f"   campos disponibles: {', '.join(p['campos_de_una'])}")

    json.dump(res, open(f"{SALIDA}/correos.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n   resultado en {SALIDA}/correos.json")


if __name__ == "__main__":
    main()
