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
                                    "previewUrl": t.get("previewUrl"),
                                    "actualizado": t.get("lastUpdated") or t.get("updatedAt")}
                                   for t in filas]}
        fallos[ruta] = {"error": d["_error"], "lectura": d.get("_lectura")}
        time.sleep(0.3)
    return {"_error": "ninguna ruta de plantillas respondio", "intentos": fallos}



def texto_de(html):
    """Saca el texto legible de un HTML de correo, sin traerse el CSS."""
    import re
    h = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", html)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|tr|h[1-6]|li)>", "\n", h)
    t = re.sub(r"<[^>]+>", " ", h)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
          .replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">"))
    lineas = [" ".join(l.split()) for l in t.split("\n")]
    return "\n".join(l for l in lineas if l)


def cuerpos(lista, tope=200):
    """Baja el contenido de cada plantilla desde su previewUrl.

    Se prueba primero SIN token: el enlace de vista previa suele ser publico,
    y si lo es no hace falta mandar la credencial a un host distinto del de la
    API. Solo si falla se reintenta con el token.
    """
    out, sin_url, fallos = [], 0, 0
    for t in lista[:tope]:
        url = t.get("previewUrl")
        if not url:
            sin_url += 1
            continue
        html = None
        for cab in ({"User-Agent": UA},
                    {"User-Agent": UA, "Authorization": f"Bearer {TOKEN}"}):
            try:
                r = urllib.request.Request(url, headers=cab)
                with urllib.request.urlopen(r, timeout=40) as resp:
                    html = resp.read().decode("utf-8", "replace")
                break
            except Exception:                    # noqa: BLE001
                continue
        if html is None:
            fallos += 1
            out.append({**t, "_error": "no se pudo abrir la vista previa"})
            continue
        cuerpo = texto_de(html)
        out.append({**t, "caracteres_html": len(html), "cuerpo": cuerpo})
        time.sleep(0.2)
    return {"bajadas": len([x for x in out if x.get("cuerpo")]),
            "sin_previewUrl": sin_url, "fallos": fallos, "plantillas": out}



def dentro_de_carpetas(lista):
    """Mira si las carpetas guardan plantillas que la lista plana no trae.

    La primera corrida devolvio 82 entradas: 18 del sistema, 31 plantillas y
    33 CARPETAS. Si cada carpeta tiene correos dentro, el inventario real es
    mucho mayor que 31 — y entregar 31 como si fuera todo seria justo el error
    que hay que evitar.

    No se supone: se le pregunta a la API. Se prueban los nombres de parametro
    mas probables sobre una carpeta real y se anota cual responde.
    """
    carpetas = [t for t in lista if (t.get("tipo") or "") == "folder"]
    if not carpetas:
        return {"nota": "no hay carpetas"}

    # 1) La lista completa, por si 82 era solo un tope y no el total real.
    amplio = api("/emails/builder", locationId=LOCATION, limit=500)
    total_amplio = None
    if "_error" not in amplio:
        for k in ("data", "builders", "templates"):
            if isinstance(amplio.get(k), list):
                total_amplio = len(amplio[k]); break
        total_amplio = {"total_declarado": amplio.get("total"), "filas": total_amplio}

    # 2) Pedir el contenido de una carpeta concreta, probando nombres de parametro.
    prueba = carpetas[0]
    intentos = {}
    for clave in ("parentId", "folderId", "parent", "categoryId"):
        d = api("/emails/builder", locationId=LOCATION, limit=100, **{clave: prueba["id"]})
        if "_error" in d:
            intentos[clave] = d["_error"]
            continue
        filas = next((d[k] for k in ("data", "builders", "templates")
                      if isinstance(d.get(k), list)), [])
        intentos[clave] = {"filas": len(filas), "total": d.get("total"),
                           "nombres": [f.get("name") for f in filas[:6]]}
        time.sleep(0.3)

    return {"carpetas": len(carpetas),
            "carpeta_probada": {"id": prueba["id"], "nombre": prueba["nombre"]},
            "lista_con_limit_500": total_amplio,
            "intentos_de_parametro": intentos}


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

    if "_error" not in res["plantillas"]:
        print("→ ¿Las carpetas esconden mas correos?…")
        res["carpetas"] = dentro_de_carpetas(res["plantillas"]["plantillas"])
        print("   ", json.dumps(res["carpetas"], ensure_ascii=False)[:400])

        print("→ Contenido de cada plantilla…")
        propias = [t for t in res["plantillas"]["plantillas"]
                   if not str(t.get("nombre") or "").startswith("Default -")]
        c = cuerpos(propias)
        print(f"   {c['bajadas']} cuerpos bajados · {c['fallos']} fallos "
              f"· {c['sin_previewUrl']} sin enlace de vista previa")
        json.dump({"generado": res["generado"], **c},
                  open(f"{SALIDA}/correos-contenido.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        res["contenido"] = {"bajadas": c["bajadas"], "fallos": c["fallos"],
                            "sin_previewUrl": c["sin_previewUrl"]}

    json.dump(res, open(f"{SALIDA}/correos.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n   resultado en {SALIDA}/correos.json y correos-contenido.json")


if __name__ == "__main__":
    main()
