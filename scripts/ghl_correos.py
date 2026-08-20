#!/usr/bin/env python3
"""
Inventario completo de los correos de GoHighLevel: recorre las carpetas,
baja cada plantilla y deja el contenido legible en el repo.

QUÉ RESUELVE
    El skill `auditoria-correos-sharp-crm` hace esto a mano con el navegador:
    entrar carpeta por carpeta, abrir cada workflow y cada plantilla. Son
    decenas, y es facil dejarse alguna.

CÓMO SE LLEGÓ AQUÍ (importa, porque el primer intento se quedaba corto)
    /emails/builder devuelve 82 entradas y parece el inventario entero. No lo
    es: de esas 82, 18 son plantillas del sistema, 31 son plantillas reales y
    **33 son CARPETAS**. Solo la carpeta "SEGUIMIENTO" guarda 7 correos que la
    lista plana no menciona.

    Se probaron cuatro nombres de parametro contra una carpeta real y el que
    funciona es `parentId`. Los otros tres se ignoran y devuelven la lista de
    siempre — o sea que un error de nombre NO da error: da un resultado
    plausible y equivocado. Por eso se comprueba, no se supone.

LÍMITE CONOCIDO
    Sigue sin salir por API que workflow usa que plantilla: GET /workflows/
    devuelve solo metadatos. Ese cruce se hace leyendo los nombres, que en
    esta cuenta estan puestos por flujo.

USO
    GHL_TOKEN=xxx python3 scripts/ghl_correos.py
"""
import json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
from datetime import date

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"
V2 = "https://services.leadconnectorhq.com"
SALIDA = "matriz-viral/fuentes/ghl"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
MAX_PROFUNDIDAD = 4     # tope de seguridad: si hubiera un ciclo, no gira sin fin


def api(ruta, version="2021-07-28", **params):
    url = f"{V2}{ruta}"
    if params:
        url += ("&" if "?" in ruta else "?") + urllib.parse.urlencode(params)
    cab = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json",
           "Version": version, "User-Agent": UA}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=cab), timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}", "_detalle": e.read().decode()[:200]}
    except Exception as e:                       # noqa: BLE001
        return {"_error": str(e)[:200]}


def filas_de(d):
    for k in ("data", "builders", "templates", "docs"):
        if isinstance(d.get(k), list):
            return d[k]
    return next((v for v in d.values() if isinstance(v, list)), [])


def listar(parent=None):
    p = {"locationId": LOCATION, "limit": 500}
    if parent:
        p["parentId"] = parent
    d = api("/emails/builder", **p)
    return [] if "_error" in d else filas_de(d)


def recorrer(parent=None, ruta="", nivel=0, vistos=None):
    """Baja el arbol entero de carpetas. Devuelve (plantillas, carpetas)."""
    vistos = vistos if vistos is not None else set()
    plantillas, carpetas = [], []
    for t in listar(parent):
        tid = t.get("id") or t.get("_id")
        nombre = t.get("name") or "(sin nombre)"
        if tid in vistos:
            continue
        vistos.add(tid)
        if (t.get("templateType") or "") == "folder":
            aqui = f"{ruta} > {nombre}" if ruta else nombre
            carpetas.append({"id": tid, "nombre": nombre, "ruta": aqui})
            if nivel < MAX_PROFUNDIDAD:
                time.sleep(0.25)
                sub_p, sub_c = recorrer(tid, aqui, nivel + 1, vistos)
                plantillas += sub_p
                carpetas += sub_c
        else:
            plantillas.append({"id": tid, "nombre": nombre,
                               "carpeta": ruta or "(raiz)",
                               "tipo": t.get("templateType"),
                               "previewUrl": t.get("previewUrl"),
                               "actualizado": t.get("lastUpdated")})
    return plantillas, carpetas


def texto_de(html):
    """El texto legible de un correo, sin CSS y conservando los parrafos."""
    h = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", html)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|tr|h[1-6]|li|td)>", "\n", h)
    t = re.sub(r"<[^>]+>", " ", h)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&quot;", '"'),
                 ("&#39;", "'"), ("&lt;", "<"), ("&gt;", ">")):
        t = t.replace(a, b)
    lineas = [" ".join(l.split()) for l in t.split("\n")]
    return "\n".join(l for l in lineas if l)


def bajar(plantillas):
    ok = fallo = sin_url = 0
    for t in plantillas:
        url = t.get("previewUrl")
        if not url:
            t["_nota"] = "sin enlace de vista previa"
            sin_url += 1
            continue
        html = None
        # Primero sin token: el enlace de vista previa suele ser publico, y si
        # lo es no hace falta mandar la credencial a otro host.
        for cab in ({"User-Agent": UA},
                    {"User-Agent": UA, "Authorization": f"Bearer {TOKEN}"}):
            try:
                with urllib.request.urlopen(
                        urllib.request.Request(url, headers=cab), timeout=40) as r:
                    html = r.read().decode("utf-8", "replace")
                break
            except Exception:                    # noqa: BLE001
                continue
        if html is None:
            t["_nota"] = "no se pudo abrir la vista previa"
            fallo += 1
        else:
            t["cuerpo"] = texto_de(html)
            ok += 1
        time.sleep(0.2)
    return {"con_cuerpo": ok, "fallos": fallo, "sin_enlace": sin_url}


def escribir_md(plantillas, carpetas, cuenta):
    """El inventario en Markdown, agrupado por carpeta — como pide la guia."""
    por_carpeta = {}
    for t in plantillas:
        por_carpeta.setdefault(t["carpeta"], []).append(t)

    L = ["# Inventario de correos — GoHighLevel", "",
         f"Generado el {date.today().isoformat()}.", "",
         f"**{len(plantillas)} plantillas** en **{len(carpetas)} carpetas**. "
         f"{cuenta['con_cuerpo']} con contenido descargado, {cuenta['fallos']} fallidas, "
         f"{cuenta['sin_enlace']} sin enlace de vista previa.", "",
         "> Lo que NO sale por API: que workflow usa que plantilla. El endpoint "
         "de automatizaciones devuelve solo metadatos. En esta cuenta las "
         "plantillas estan nombradas por su flujo, asi que el cruce se puede "
         "hacer leyendo.", ""]

    for carpeta in sorted(por_carpeta):
        L += [f"## {carpeta}", ""]
        for t in sorted(por_carpeta[carpeta], key=lambda x: x["nombre"]):
            L += [f"### {t['nombre']}", "",
                  f"- **id:** `{t['id']}`",
                  f"- **tipo:** {t.get('tipo') or '—'}",
                  f"- **actualizada:** {t.get('actualizado') or '—'}"]
            if t.get("cuerpo"):
                L += ["- **Cuerpo:**", "", "```", t["cuerpo"][:6000], "```", ""]
            else:
                L += [f"- ⚠️ **Sin contenido:** {t.get('_nota')}", ""]
    open(f"{SALIDA}/INVENTARIO-CORREOS.md", "w", encoding="utf-8").write("\n".join(L))


def main():
    if not TOKEN:
        print("ERROR: falta GHL_TOKEN en el entorno.", file=sys.stderr)
        sys.exit(1)
    os.makedirs(SALIDA, exist_ok=True)

    print("→ Recorriendo carpetas…")
    plantillas, carpetas = recorrer()
    propias = [t for t in plantillas if not str(t["nombre"]).startswith("Default -")]
    print(f"   {len(carpetas)} carpetas · {len(plantillas)} plantillas "
          f"({len(propias)} propias, {len(plantillas)-len(propias)} del sistema)")

    print("→ Bajando el contenido…")
    cuenta = bajar(propias)
    print(f"   {cuenta['con_cuerpo']} con cuerpo · {cuenta['fallos']} fallos "
          f"· {cuenta['sin_enlace']} sin enlace")

    ws = api("/workflows/", version="v3", locationId=LOCATION)
    n_ws = len(ws.get("workflows", [])) if "_error" not in ws else None

    json.dump({"generado": date.today().isoformat(),
               "carpetas": carpetas, "plantillas": propias,
               "cuenta": cuenta, "workflows_en_la_cuenta": n_ws,
               "limite_conocido": ("La API no dice que workflow usa que plantilla: "
                                   "GET /workflows/ solo devuelve metadatos.")},
              open(f"{SALIDA}/correos-contenido.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    escribir_md(propias, carpetas, cuenta)
    print(f"\n   {SALIDA}/INVENTARIO-CORREOS.md y correos-contenido.json")


if __name__ == "__main__":
    main()
