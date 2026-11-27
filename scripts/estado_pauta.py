#!/usr/bin/env python3
"""
Foto del estado ACTUAL de la cuenta de pauta, solo lectura: campañas, conjuntos
y anuncios con su estado efectivo, presupuesto diario, países y la primera línea
del copy. Sirve para verificar que los cambios que reporta la agencia estén
aplicados. No modifica nada. El token nunca se imprime.
"""
import json, os, urllib.parse, urllib.request

BASE = "https://graph.facebook.com/v21.0"
CUENTA = "act_1159622151150228"
TOKEN = os.environ.get("META_TOKEN", "").strip()


def todo(path, **p):
    p["access_token"] = TOKEN
    p.setdefault("limit", 200)
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(p)
    filas = []
    while url:
        with urllib.request.urlopen(url, timeout=90) as r:
            d = json.load(r)
        filas += d.get("data", [])
        url = (d.get("paging") or {}).get("next")
    return filas


def usd(c):
    return round(int(c) / 100, 2) if c else None


camps = todo(f"{CUENTA}/campaigns",
             fields="id,name,effective_status,daily_budget,lifetime_budget,updated_time,"
                    "start_time,stop_time")
sets = todo(f"{CUENTA}/adsets",
            fields="id,name,campaign_id,effective_status,daily_budget,lifetime_budget,updated_time,"
                   "start_time,end_time,"
                   "targeting{geo_locations{countries}}")
ads = todo(f"{CUENTA}/ads",
           fields="id,name,adset_id,campaign_id,effective_status,created_time,updated_time,"
                  "creative{body,object_story_spec{link_data{message,call_to_action}}}")

out = {"campanas": [], "conjuntos": [], "anuncios": []}
for c in camps:
    out["campanas"].append({"id": c["id"], "nombre": c["name"], "estado": c.get("effective_status"),
                            "diario": usd(c.get("daily_budget")), "actualizado": c.get("updated_time"),
                            "inicio": c.get("start_time"), "fin": c.get("stop_time")})
for s in sets:
    out["conjuntos"].append({"id": s["id"], "nombre": s["name"], "campana": s.get("campaign_id"),
                             "estado": s.get("effective_status"), "diario": usd(s.get("daily_budget")),
                             "paises": ((s.get("targeting") or {}).get("geo_locations") or {}).get("countries"),
                             "actualizado": s.get("updated_time"),
                             "total": usd(s.get("lifetime_budget")),
                             "inicio": s.get("start_time"), "fin": s.get("end_time")})
for a in ads:
    cr = a.get("creative") or {}
    ld = ((cr.get("object_story_spec") or {}).get("link_data") or {})
    texto = cr.get("body") or ld.get("message") or ""
    out["anuncios"].append({"id": a["id"], "nombre": a["name"], "conjunto": a.get("adset_id"),
                            "campana": a.get("campaign_id"), "estado": a.get("effective_status"),
                            "creado": a.get("created_time"), "actualizado": a.get("updated_time"),
                            "linea1": texto.split("\n")[0][:200], "largo_linea1": len(texto.split("\n")[0])})
VIVOS = {"ACTIVE", "PAUSED", "CAMPAIGN_PAUSED", "ADSET_PAUSED", "IN_PROCESS",
         "PENDING_REVIEW", "WITH_ISSUES", "DISAPPROVED", "PREAPPROVED", "PENDING_BILLING_INFO"}
# Una línea JSON por fila: el log de Actions corta las líneas muy largas.
for tipo, filas in out.items():
    for f in filas:
        if f["estado"] in VIVOS:
            print("FILA", json.dumps({"tipo": tipo, **f}, ensure_ascii=False))
# Entrega de HOY por conjunto (día sin cerrar: sirve para saber si algo está
# saliendo ahora mismo, no para reportar gasto).
try:
    hoy = todo(f"{CUENTA}/insights", level="adset", date_preset="today",
               fields="campaign_name,adset_name,adset_id,spend,impressions")
    for h in hoy:
        print("HOY", json.dumps({"campana": h.get("campaign_name"), "conjunto": h.get("adset_name"),
                                 "id": h.get("adset_id"), "gasto": h.get("spend"),
                                 "impresiones": h.get("impressions")}, ensure_ascii=False))
    print("FIN_HOY", len(hoy))
except Exception as e:  # la foto de estado vale aunque esto falle
    print("AVISO: no se pudo leer la entrega de hoy:", type(e).__name__)
print("FIN_ESTADO", {k: len(v) for k, v in out.items()})
