#!/usr/bin/env python3
"""
Sonda de la API de GoHighLevel: qué se puede leer con nuestro token.

POR QUÉ EXISTE
    Hoy leemos GHL por el conector de Windsor, que expone una lista fija de
    tablas: Contacts, Conversations, Opportunities, Invoices, Location,
    Orders, Pipelines, Transactions y Users.

    **No expone memberships.** Y ahí está justo lo que falta para responder
    "¿este alumno está avanzando en el curso?" — que es la pregunta que
    permite detectar a quien compró y no está viendo nada, o sea a quien va a
    pedir reembolso antes de que lo pida.

    Esta sonda prueba, uno por uno, qué endpoints de la API directa responden
    con nuestro token, y deja el resultado en el repo. No baja datos de
    negocio: solo comprueba qué puertas están abiertas y cuántos registros hay
    detrás.

USO
    GHL_TOKEN=xxx python3 scripts/ghl_sonda.py

    Corre dentro de GitHub Actions, donde GHL_TOKEN vive cifrado como secreto.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import date

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"          # Design Modeling Academy
SALIDA = "matriz-viral/fuentes/ghl-sonda.json"

# (etiqueta, base, ruta, versión de cabecera)
# La API v2 (services.leadconnectorhq.com) pide la cabecera Version; la v1
# (rest.gohighlevel.com) no. Se prueban las dos porque según cómo se generó el
# token, funciona una u otra.
V2 = "https://services.leadconnectorhq.com"
V1 = "https://rest.gohighlevel.com/v1"

PRUEBAS = [
    # Lo que ya tenemos por Windsor — para confirmar que el token sirve
    ("contactos",            V2, f"/contacts/?locationId={LOCATION}&limit=1"),
    ("oportunidades",        V2, f"/opportunities/search?location_id={LOCATION}&limit=1"),
    ("pipelines",            V2, f"/opportunities/pipelines?locationId={LOCATION}"),

    # ⭐ LO QUE NO TENEMOS: progreso de alumnos
    ("cursos · productos",   V2, f"/courses/products?locationId={LOCATION}&limit=1"),
    ("membresías",           V2, f"/memberships/?locationId={LOCATION}&limit=1"),

    # Otras puertas que valdría la pena tener
    ("calendarios",          V2, f"/calendars/?locationId={LOCATION}"),
    ("citas agendadas",      V2, f"/calendars/events?locationId={LOCATION}&limit=1"),
    ("formularios",          V2, f"/forms/?locationId={LOCATION}&limit=1"),
    ("envíos de formulario", V2, f"/forms/submissions?locationId={LOCATION}&limit=1"),
    ("encuestas",            V2, f"/surveys/?locationId={LOCATION}&limit=1"),
    ("workflows",            V2, f"/workflows/?locationId={LOCATION}"),
    ("etiquetas",            V2, f"/locations/{LOCATION}/tags"),
    ("campos propios",       V2, f"/locations/{LOCATION}/customFields"),
    ("conversaciones",       V2, f"/conversations/search?locationId={LOCATION}&limit=1"),
    ("pagos · órdenes",      V2, f"/payments/orders?altId={LOCATION}&altType=location&limit=1"),
    ("pagos · suscripciones", V2, f"/payments/subscriptions?altId={LOCATION}&altType=location&limit=1"),
    ("pagos · transacciones", V2, f"/payments/transactions?altId={LOCATION}&altType=location&limit=1"),

    # v1, por si el token es de los antiguos
    ("v1 · contactos",       V1, "/contacts/?limit=1"),
    ("v1 · pipelines",       V1, "/pipelines/"),
]


def probar(base, ruta):
    # User-Agent de navegador: sin él, Cloudflare bloquea la IP del runner con
    # un 403 "Error 1010" que PARECE falta de permisos y no lo es. Pasó el
    # 15-ago: los 19 endpoints dieron 403 y la prueba no sirvió de nada.
    cab = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json",
           "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/126.0.0.0 Safari/537.36")}
    if base.startswith(V2):
        cab["Version"] = "2021-07-28"
    r = urllib.request.Request(base + ruta, headers=cab)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            d = json.load(resp)
        # ¿cuántos registros hay detrás?
        total = None
        for k in ("total", "totalCount", "count"):
            if isinstance(d.get(k), int):
                total = d[k]; break
        if total is None:
            for v in d.values():
                if isinstance(v, list):
                    total = f"{len(v)}+"; break
        return {"ok": True, "http": resp.status, "registros": total,
                "claves": sorted(d.keys())[:8]}
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode()[:160]
        bloqueo = "1010" in cuerpo or "cloudflare" in cuerpo.lower()
        return {"ok": False, "http": e.code, "detalle": cuerpo,
                "bloqueo_cloudflare": bloqueo}
    except Exception as e:
        return {"ok": False, "http": None, "detalle": str(e)[:160]}


def main():
    if not TOKEN:
        print("ERROR: falta GHL_TOKEN en el entorno.", file=sys.stderr)
        sys.exit(1)

    res = {"generado": date.today().isoformat(),
           "location": LOCATION,
           "nota": ("Sonda: comprueba QUE endpoints responden con nuestro token. "
                    "No baja datos de negocio. Lo importante es si abren "
                    "'cursos · productos' y 'membresias': ahi vive el progreso de "
                    "los alumnos, que Windsor NO expone."),
           "resultados": {}}

    abiertos, cerrados = [], []
    for etiqueta, base, ruta in PRUEBAS:
        r = probar(base, ruta)
        res["resultados"][etiqueta] = {**r, "ruta": ruta}
        marca = "OK " if r["ok"] else "NO "
        extra = f"· {r.get('registros')} registros" if r.get("registros") is not None else \
                f"· {r.get('http')} {str(r.get('detalle',''))[:60]}"
        print(f"  {marca} {etiqueta:24} {extra}")
        (abiertos if r["ok"] else cerrados).append(etiqueta)
        time.sleep(0.3)

    res["abiertos"] = abiertos
    res["cerrados"] = cerrados
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n  abiertos: {len(abiertos)} · cerrados: {len(cerrados)}")
    print(f"  resultado en {SALIDA}")

    bloqueados = [k for k, v in res["resultados"].items() if v.get("bloqueo_cloudflare")]
    if bloqueados:
        res["aviso"] = ("Cloudflare bloqueo la IP del runner (Error 1010) en "
                        f"{len(bloqueados)} endpoints. Eso NO significa que falten "
                        "permisos: la prueba no es concluyente para esos.")
        print(f"\n  AVISO: {len(bloqueados)} endpoints bloqueados por Cloudflare, "
              "no por permisos. Ese resultado no dice nada del token.")

    clave = [e for e in ("cursos · productos", "membresías") if e in abiertos]
    if clave:
        print(f"\n  ⭐ SE PUEDE LEER PROGRESO DE ALUMNOS: {', '.join(clave)}")
    else:
        print("\n  El token NO abre cursos ni membresías. Para el progreso de alumnos")
        print("  haría falta ampliar los permisos del token en GHL.")


if __name__ == "__main__":
    main()
