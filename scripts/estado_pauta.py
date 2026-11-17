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
             fields="id,name,effective_status,daily_budget,lifetime_budget,updated_time")
sets = todo(f"{CUENTA}/adsets",
            fields="id,name,campaign_id,effective_status,daily_budget,updated_time,"
                   "targeting{geo_locations{countries}}")
ads = todo(f"{CUENTA}/ads",
           fields="id,name,adset_id,campaign_id,effective_status,created_time,updated_time,"
                  "creative{body,object_story_spec{link_data{message,call_to_action}}}")

out = {"campanas": [], "conjuntos": [], "anuncios": []}
for c in camps:
    out["campanas"].append({"id": c["id"], "nombre": c["name"], "estado": c.get("effective_status"),
                            "diario": usd(c.get("daily_budget")), "actualizado": c.get("updated_time")})
for s in sets:
    out["conjuntos"].append({"id": s["id"], "nombre": s["name"], "campana": s.get("campaign_id"),
                             "estado": s.get("effective_status"), "diario": usd(s.get("daily_budget")),
                             "paises": ((s.get("targeting") or {}).get("geo_locations") or {}).get("countries"),
                             "actualizado": s.get("updated_time")})
for a in ads:
    cr = a.get("creative") or {}
    ld = ((cr.get("object_story_spec") or {}).get("link_data") or {})
    texto = cr.get("body") or ld.get("message") or ""
    out["anuncios"].append({"id": a["id"], "nombre": a["name"], "conjunto": a.get("adset_id"),
                            "campana": a.get("campaign_id"), "estado": a.get("effective_status"),
                            "creado": a.get("created_time"), "actualizado": a.get("updated_time"),
                            "linea1": texto.split("\n")[0][:200], "largo_linea1": len(texto.split("\n")[0])})
print("===ESTADO_JSON===")
print(json.dumps(out, ensure_ascii=False))
print("===FIN_JSON===")
