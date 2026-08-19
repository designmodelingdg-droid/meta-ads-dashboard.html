#!/usr/bin/env python3
"""
Baja los datos de GoHighLevel al repo, para que estén donde todo lo demás.

POR QUÉ EXISTE
    De GHL solo teníamos la sonda: dice QUÉ endpoints abren, pero no baja nada.
    Así que el CRM era el único sistema que no se podía mirar sin entrar a la
    plataforma — y quien lleva el contenido necesita ver de dónde vienen los
    leads sin pedirle a nadie una captura.

    La sonda del 15-ago confirmó 14 endpoints abiertos. Esto usa cinco:
    pipelines, oportunidades, etiquetas, formularios y transacciones de pago.

QUÉ NO BAJA, Y POR QUÉ
    No baja la lista de contactos con nombre, correo y teléfono. Son datos
    personales de miles de personas y el repositorio no es sitio para eso: lo
    que hace falta para decidir contenido son los AGREGADOS —cuántos, de dónde
    vienen, en qué etapa están—, no quién es cada uno.

    Tampoco baja el progreso de los alumnos: comprobado contra la documentación
    oficial de HighLevel, ese endpoint no existe en la API pública.

USO
    GHL_TOKEN=xxx python3 scripts/ghl_datos.py

    Corre dentro de GitHub Actions, donde GHL_TOKEN vive cifrado.
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error
from collections import Counter
from datetime import date

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"          # Design Modeling Academy
V2 = "https://services.leadconnectorhq.com"
SALIDA = "matriz-viral/fuentes/ghl"

# User-Agent de navegador: sin él Cloudflare bloquea la IP del runner con un
# 403 "Error 1010" que PARECE falta de permisos y no lo es. Pasó el 15-ago.
CAB = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json",
       "Version": "2021-07-28",
       "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36")}


def api(ruta, **params):
    url = f"{V2}{ruta}"
    if params:
        url += ("&" if "?" in ruta else "?") + urllib.parse.urlencode(params)
    r = urllib.request.Request(url, headers=CAB)
    try:
        with urllib.request.urlopen(r, timeout=40) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode()[:200]
        return {"_error": f"HTTP {e.code}", "_detalle": cuerpo}
    except Exception as e:                       # noqa: BLE001
        return {"_error": str(e)[:200]}


def pipelines():
    d = api(f"/opportunities/pipelines", locationId=LOCATION)
    if "_error" in d:
        return d
    salida = []
    for p in d.get("pipelines", []):
        salida.append({"id": p.get("id"), "nombre": p.get("name"),
                       "etapas": [{"id": s.get("id"), "nombre": s.get("name")}
                                  for s in p.get("stages", [])]})
    return {"total": len(salida), "pipelines": salida}


def oportunidades(paginas=12):
    """Agregados: por pipeline, por etapa, por fuente y por estado.

    Se recorre paginando y se cuenta al vuelo — no se guarda ni un nombre ni
    un correo, solo los totales. Es lo que hace falta para decidir contenido.
    """
    por_pipeline, por_etapa, por_fuente, por_estado = Counter(), Counter(), Counter(), Counter()
    por_mes, valor = Counter(), 0.0
    total, sig, vueltas = 0, None, 0
    while vueltas < paginas:
        p = {"location_id": LOCATION, "limit": 100}
        if sig:
            p["startAfterId"] = sig
        d = api("/opportunities/search", **p)
        if "_error" in d:
            return {**d, "parcial": total}
        lote = d.get("opportunities", []) or []
        if not lote:
            break
        for o in lote:
            total += 1
            por_pipeline[o.get("pipelineId") or "sin pipeline"] += 1
            por_etapa[o.get("pipelineStageId") or "sin etapa"] += 1
            por_fuente[(o.get("source") or "sin fuente").strip() or "sin fuente"] += 1
            por_estado[o.get("status") or "sin estado"] += 1
            fecha = (o.get("createdAt") or "")[:7]
            if fecha:
                por_mes[fecha] += 1
            try:
                valor += float(o.get("monetaryValue") or 0)
            except (TypeError, ValueError):
                pass
        sig = lote[-1].get("id")
        vueltas += 1
        time.sleep(0.3)
    return {"total": total, "valor_declarado": round(valor, 2),
            "por_pipeline": dict(por_pipeline), "por_etapa": dict(por_etapa),
            "por_fuente": dict(por_fuente.most_common(30)),
            "por_estado": dict(por_estado),
            "por_mes": dict(sorted(por_mes.items()))}


def etiquetas():
    d = api(f"/locations/{LOCATION}/tags")
    if "_error" in d:
        return d
    ts = [t.get("name") for t in d.get("tags", []) if t.get("name")]
    return {"total": len(ts), "etiquetas": sorted(ts)}


def formularios():
    d = api("/forms/", locationId=LOCATION, limit=100)
    if "_error" in d:
        return d
    fs = [{"id": f.get("id"), "nombre": f.get("name")} for f in d.get("forms", [])]
    return {"total": d.get("total", len(fs)), "formularios": fs}


def pagos():
    d = api("/payments/transactions", altId=LOCATION, altType="location", limit=100)
    if "_error" in d:
        return d
    filas = d.get("data", []) or []
    por_estado = Counter(t.get("status") or "sin estado" for t in filas)
    total = 0.0
    for t in filas:
        try:
            total += float(t.get("amount") or 0)
        except (TypeError, ValueError):
            pass
    return {"total_transacciones": d.get("totalCount", len(filas)),
            "en_esta_pagina": len(filas),
            "suma_pagina": round(total, 2),
            "por_estado": dict(por_estado),
            "nota": ("La suma es solo de la primera pagina. Para dinero manda "
                     "Stripe + PayPal (fuentes/ingresos/), que es lo cobrado de verdad.")}


def main():
    if not TOKEN:
        print("ERROR: falta GHL_TOKEN en el entorno.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(SALIDA, exist_ok=True)
    bloques = {"pipelines": pipelines, "oportunidades": oportunidades,
               "etiquetas": etiquetas, "formularios": formularios, "pagos": pagos}

    resumen = {"generado": date.today().isoformat(), "location": LOCATION,
               "nota": ("Agregados del CRM. No incluye datos personales: para decidir "
                        "contenido hacen falta los totales, no quien es cada persona."),
               "bloques": {}}

    for nombre, fn in bloques.items():
        try:
            r = fn()
        except Exception as e:                   # noqa: BLE001
            r = {"_error": str(e)[:200]}
        json.dump({"generado": resumen["generado"], **r},
                  open(f"{SALIDA}/{nombre}.json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        if "_error" in r:
            print(f"  {nombre}: ERROR · {r['_error']}", file=sys.stderr)
            resumen["bloques"][nombre] = {"error": r["_error"]}
        else:
            clave = r.get("total", r.get("total_transacciones", "—"))
            print(f"  {nombre}: {clave}")
            resumen["bloques"][nombre] = {"total": clave}

    json.dump(resumen, open(f"{SALIDA}/resumen.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n  resultado en {SALIDA}/")


if __name__ == "__main__":
    main()
