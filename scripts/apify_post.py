#!/usr/bin/env python3
"""Trae UN post público de Instagram por su enlace, con Apify y tope duro de gasto.

    python3 scripts/apify_post.py matriz-viral/pedidos/apify-post.json

El pedido es un JSON: {"url": "...", "tope_usd": 0.10, "motivo": "..."}.
Sale en matriz-viral/fuentes/referentes/post-<código>.json con el texto, el
tipo, las métricas públicas, las URL de las imágenes y, si es video, la
transcripción (actor de reels). No se guardan imágenes de terceros en el repo:
solo sus URL, que caducan.

Lo corre la Action «Traer un post (Apify)» cuando cambia el pedido. Sin
APIFY_TOKEN no hace nada. Si Apify falla, no escribe nada: vacío antes que
inventado.
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()
R = pathlib.Path(__file__).resolve().parent.parent
SAL = R / "matriz-viral" / "fuentes" / "referentes"


def actor(nombre, entrada, tope):
    url = (f"https://api.apify.com/v2/acts/{nombre}/run-sync-get-dataset-items"
           f"?token={TOKEN}&maxTotalChargeUsd={tope}")
    req = urllib.request.Request(url, data=json.dumps({**entrada, "maxTotalChargeUsd": tope}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=280) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Apify HTTP {e.code} en {nombre}: {e.read().decode()[:300]}")
    except Exception as e:  # noqa: BLE001
        print(f"Fallo de red con Apify ({nombre}): {e}")
    return None


def main():
    if not TOKEN:
        print("Sin APIFY_TOKEN: no se corre nada.")
        return
    pedido = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    url = pedido["url"].split("?")[0]
    tope = min(float(pedido.get("tope_usd", 0.10)), 0.25)
    items = actor("apify~instagram-scraper", {"directUrls": [url], "resultsType": "posts", "resultsLimit": 1,
                                              "addParentData": False}, tope)
    if not items:
        print("Sin datos. No se escribe nada.")
        return
    p = items[0]
    if p.get("error"):
        print(f"Apify no pudo leer el post: {p.get('error')} {p.get('errorDescription', '')}")
        return
    codigo = p.get("shortCode") or url.rstrip("/").split("/")[-1]
    hijos = p.get("childPosts") or []
    salida = {
        "traido": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "fuente": "Apify · apify~instagram-scraper (post público)",
        "motivo": pedido.get("motivo"),
        "url": url, "codigo": codigo, "cuenta": p.get("ownerUsername"), "nombre_cuenta": p.get("ownerFullName"),
        "tipo": p.get("type"), "producto": p.get("productType"), "fecha": p.get("timestamp"),
        "texto": p.get("caption"), "hashtags": p.get("hashtags"),
        "likes": p.get("likesCount"), "comentarios": p.get("commentsCount"),
        "vistas_video": p.get("videoViewCount") or p.get("videoPlayCount"), "duracion_s": p.get("videoDuration"),
        "texto_alternativo": p.get("alt"),
        "imagenes": [p.get("displayUrl")] + [h.get("displayUrl") for h in hijos if h.get("displayUrl")],
        "diapositivas": [{"n": i + 1, "tipo": h.get("type"), "alt": h.get("alt")} for i, h in enumerate(hijos)],
        "video_url": p.get("videoUrl"),
        "comentarios_muestra": [c.get("text") for c in (p.get("latestComments") or [])][:15],
        "transcripcion": None,
    }
    if p.get("type") == "Video":
        r = actor("apify~instagram-reel-scraper", {"username": [url], "resultsLimit": 1, "includeTranscript": True}, tope)
        if r:
            salida["transcripcion"] = r[0].get("transcript")
    SAL.mkdir(parents=True, exist_ok=True)
    f = SAL / f"post-{codigo}.json"
    f.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok → {f.relative_to(R)} · {salida['cuenta']} · {salida['tipo']} · {len(salida['imagenes'])} imágenes")


if __name__ == "__main__":
    main()
