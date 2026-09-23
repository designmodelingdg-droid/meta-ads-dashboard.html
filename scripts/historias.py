#!/usr/bin/env python3
"""Métricas de las HISTORIAS de Instagram, antes de que desaparezcan.

Por qué existe (23-sep): meta_organico.py lee /{ig}/media, y ese listado NO
trae historias. Las historias salen por /{ig}/stories, y SOLO mientras están
publicadas: a las 24 h Instagram las retira de la API y sus números se pierden
para siempre. Así que esto tiene que correr VARIAS veces al día (ver
historias.yml): cada pasada actualiza las historias vivas y las que ya
caducaron se quedan con su última lectura.

Lo que guarda por historia: alcance, respuestas, compartidos, interacciones,
seguidores y visitas al perfil que trajo, y la NAVEGACIÓN — cuántos pasaron a
la siguiente, cuántos volvieron atrás y cuántos se fueron. Esa es la métrica
propia de una secuencia: dónde se cae la gente.

Ninguna métrica rompe la corrida: Meta cambia los nombres entre versiones
(«impressions» se retiró en 2025) y una que falle se registra como ausente.

    META_TOKEN=... python3 scripts/historias.py
"""
import datetime, json, os, sys, urllib.error, urllib.parse, urllib.request

BASE = "https://graph.facebook.com/v22.0"
TOKEN = os.environ.get("META_TOKEN", "").strip()
IG_ID = os.environ.get("META_IG_ID", "17841404048578200")   # @design_modeling_dg
SALIDA = os.path.join("matriz-viral", "fuentes", "historias", "historias.json")

# Una por una a propósito: si Meta rechaza una, las demás llegan igual.
METRICAS = ["reach", "views", "replies", "shares", "total_interactions",
            "follows", "profile_visits"]


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=40) as r:
        return json.load(r)


def metrica(mid, nombre, **extra):
    try:
        d = api(f"{mid}/insights", metric=nombre, **extra)
    except urllib.error.HTTPError:
        return None
    datos = d.get("data") or []
    if not datos:
        return None
    m = datos[0]
    if "total_value" in m:
        tv = m["total_value"]
        if "breakdowns" in tv:
            return {r["dimension_values"][0]: r["value"]
                    for b in tv["breakdowns"] for r in b.get("results", [])}
        return tv.get("value")
    vals = m.get("values") or []
    return vals[0].get("value") if vals else None


def main():
    if not TOKEN:
        sys.exit("ERROR: falta META_TOKEN.")
    ahora = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    previo = {}
    if os.path.exists(SALIDA):
        previo = json.load(open(SALIDA, encoding="utf-8"))
    guardadas = {h["id"]: h for h in previo.get("historias", [])}

    vivas = api(f"{IG_ID}/stories",
                fields="id,media_type,media_url,thumbnail_url,permalink,timestamp,caption")
    vivas = vivas.get("data", [])
    print(f"{len(vivas)} historias publicadas ahora mismo")

    for h in vivas:
        fila = guardadas.get(h["id"], {})
        fila.update({"id": h["id"], "tipo": h.get("media_type"),
                     "publicada": h.get("timestamp"), "enlace": h.get("permalink"),
                     "caption": h.get("caption")})
        for m in METRICAS:
            v = metrica(h["id"], m, metric_type="total_value")
            if v is None:
                v = metrica(h["id"], m)
            if v is not None:
                fila[m] = v
        nav = metrica(h["id"], "navigation", metric_type="total_value",
                      breakdown="story_navigation_action_type")
        if isinstance(nav, dict):
            fila["navegacion"] = nav
        fila["ultima_lectura"] = ahora
        guardadas[h["id"]] = fila
        print(f"  {h.get('timestamp','')[:16]} · alcance {fila.get('reach')} · "
              f"respuestas {fila.get('replies')} · nav {fila.get('navegacion')}")

    salida = {
        "generado": ahora,
        "nota": ("Las historias solo existen en la API 24 h. Cada fila guarda la "
                 "ÚLTIMA lectura antes de que caducara: si esto corre cada 4 h, el "
                 "número final puede quedarse corto hasta en 4 h de vida."),
        "historias": sorted(guardadas.values(), key=lambda x: x.get("publicada") or ""),
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(salida, open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"→ {SALIDA}: {len(guardadas)} historias guardadas en total")


if __name__ == "__main__":
    main()
