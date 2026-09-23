#!/usr/bin/env python3
"""Embudo de cada lead magnet, contado con las etiquetas de GoHighLevel.

Por qué existe (23-sep): la matriz sabía cuántos comentarios tenía una pieza
(Instagram) y cuántos DM mandaba OpenReply, pero no qué pasaba en GoHighLevel,
que es donde viven los disparadores de las seis palabras. Y GHL ya deja el
rastro: cada workflow pone etiquetas por etapa.

    origen-bot-<x>   la persona escribió la palabra y el bot la recogió
    lead-<x>         quedó registrada como lead de ese recurso
    acceso-<x>       recibió el acceso al recurso

Solo cuenta. No baja ni un nombre, correo o teléfono: lo que la matriz
necesita son cuántos, no quiénes (misma regla que ghl_datos.py).

TRES NÚMEROS POR ETIQUETA, y no significan lo mismo:
  total          todos los contactos que la tienen, desde siempre
  nuevos_7d      contactos CREADOS en los últimos 7 días con esa etiqueta
  tocados_desde  contactos con la etiqueta MODIFICADOS desde una fecha.
                 GHL no guarda cuándo se puso cada etiqueta, así que esto es
                 una cota: alguien que ya tenía la etiqueta y al que se le
                 cambió otra cosa también cuenta. Sirve para ver si una pieza
                 movió algo, no para medirlo al contacto.

    GHL_TOKEN=... python3 scripts/embudo_leadmagnets.py [--desde 2026-09-22T21:00Z]
"""
import argparse, datetime, json, os, sys, urllib.error, urllib.request

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"
V2 = "https://services.leadconnectorhq.com"
SALIDA = os.path.join("matriz-viral", "fuentes", "ghl", "embudo-leadmagnets.json")
CAB = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json",
       "Content-Type": "application/json", "Version": "2021-07-28",
       "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")}

# Las etiquetas salen de etiquetas.json (las que existen de verdad en GHL),
# no de cómo «deberían» llamarse. Por eso no son simétricas.
EMBUDOS = {
    "DYNAMO":  {"recurso": "Pack de 5 scripts de Dynamo",
                "etapas": [("bot", "origen-bot-dynamo"), ("lead", "lead-dynamo"),
                           ("acceso", "acceso-script-dynamo")]},
    "CHATGPT": {"recurso": "Guía Revit + ChatGPT",
                "etapas": [("bot", "origen-bot-chatgpt"), ("lead", "lead-chatgpt"),
                           ("acceso", "acceso-guia-revitchatgpt")]},
    "MEMORIA": {"recurso": "Guía de memoria de cálculo",
                "etapas": [("bot", "origen-bot-memoria"), ("lead", "lead-memoria"),
                           ("acceso", "acceso-memoria-calculo")]},
    "ZAPATA":  {"recurso": "Calculadora de zapatas",
                "etapas": [("bot", "origen-bot-zapata"), ("lead", "lead-calculadora-zapatas"),
                           ("acceso", "guia-zapata")]},
    "NIVEL":   {"recurso": "Test de nivel BIM",
                "etapas": [("bot", "origen-bot-nivel"), ("lead", "lead-test-nivel"),
                           ("acceso", "acceso-test-nivel")]},
}


def buscar(filtros):
    """Total de contactos que cumplen los filtros. None si GHL lo rechaza."""
    cuerpo = json.dumps({"locationId": LOCATION, "pageLimit": 1,
                         "filters": filtros}).encode()
    r = urllib.request.Request(f"{V2}/contacts/search", data=cuerpo,
                               headers=CAB, method="POST")
    try:
        with urllib.request.urlopen(r, timeout=40) as x:
            return json.load(x).get("total")
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:200]
        print(f"    GHL {e.code}: {cuerpo}")
        return None


def por_etiqueta(tag, desde_7d, desde):
    base = {"field": "tags", "operator": "contains", "value": tag}
    return {
        "etiqueta": tag,
        "total": buscar([base]),
        "nuevos_7d": buscar([base, {"field": "dateAdded", "operator": "range",
                                    "value": {"gte": desde_7d}}]),
        "tocados_desde": buscar([base, {"field": "dateUpdated", "operator": "range",
                                        "value": {"gte": desde}}]) if desde else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", help="ISO UTC; por defecto, hace 7 días")
    a = ap.parse_args()
    if not TOKEN:
        sys.exit("ERROR: falta GHL_TOKEN.")
    ahora = datetime.datetime.now(datetime.timezone.utc)
    hace7 = (ahora - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    desde = a.desde or hace7

    salida = {"generado": ahora.strftime("%Y-%m-%dT%H:%MZ"),
              "ventana_7d_desde": hace7, "tocados_desde": desde,
              "nota": ("Solo cuentas, ningún dato personal. «tocados_desde» es una cota: "
                       "GHL no guarda cuándo se puso cada etiqueta."),
              "embudos": {}}
    for palabra, e in EMBUDOS.items():
        print(f"{palabra} · {e['recurso']}")
        etapas = {}
        for nombre, tag in e["etapas"]:
            etapas[nombre] = por_etiqueta(tag, hace7, desde)
            x = etapas[nombre]
            print(f"   {nombre:<7} {tag:<26} total {x['total']} · nuevos 7d {x['nuevos_7d']}"
                  f" · tocados {x['tocados_desde']}")
        salida["embudos"][palabra] = {"recurso": e["recurso"], "etapas": etapas}

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(salida, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"→ {SALIDA}")


if __name__ == "__main__":
    main()
