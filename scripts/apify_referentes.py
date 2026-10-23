#!/usr/bin/env python3
"""Trae los últimos reels (con transcripción) y posts de cuentas públicas de
Instagram, con tope duro de gasto por actor y tope total.

Lo llama scripts/apify_post.py cuando el pedido trae "perfiles":

    {"perfiles": ["lexmrbim", "aecode.ai"], "reels_por_cuenta": 30,
     "posts_por_cuenta": 30, "tope_total_usd": 1.0, "url": "<reel opcional>"}

Topes (CLAUDE.md, regla 3): máximo 30 ítems por cuenta y actor y
maxTotalChargeUsd total ≤ 1.0. Usa la API asíncrona de Apify para poder
guardar el costo real de cada corrida (usageTotalUsd). Si Apify falla, no
escribe nada de esa cuenta: vacío antes que inventado.
"""
import json
import os
import pathlib
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()
R = pathlib.Path(__file__).resolve().parent.parent
SAL = R / "matriz-viral" / "fuentes" / "referentes"
API = "https://api.apify.com/v2"
MAX_ITEMS = 30
MAX_TOTAL = 1.0


def _get(url, data=None, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def correr(actor, entrada, tope, max_items):
    """Corre un actor con tope duro y devuelve (items, costo_info)."""
    tope = round(float(tope), 2)
    url = (f"{API}/acts/{actor}/runs?token={TOKEN}&maxTotalChargeUsd={tope}"
           f"&maxItems={max_items}&waitForFinish=60")
    try:
        run = _get(url, {**entrada, "maxTotalChargeUsd": tope})["data"]
        t0 = time.time()
        while run.get("status") in ("READY", "RUNNING") and time.time() - t0 < 900:
            run = _get(f"{API}/actor-runs/{run['id']}?token={TOKEN}&waitForFinish=60")["data"]
        items = _get(f"{API}/datasets/{run['defaultDatasetId']}/items?token={TOKEN}&clean=true"
                     f"&limit={max_items * 2}", timeout=180)
    except urllib.error.HTTPError as e:
        print(f"Apify HTTP {e.code} en {actor}: {e.read().decode()[:300]}")
        return None, None
    except Exception as e:  # noqa: BLE001
        print(f"Fallo con Apify ({actor}): {e}")
        return None, None
    costo = {"actor": actor, "run_id": run.get("id"), "estado": run.get("status"),
             "tope_usd": tope, "usageTotalUsd": run.get("usageTotalUsd"),
             "chargedEventCounts": run.get("chargedEventCounts"),
             "pricingModel": (run.get("pricingInfo") or {}).get("pricingModel"),
             "items": len(items) if isinstance(items, list) else None}
    print(f"{actor}: {costo['estado']} · {costo['items']} ítems · usage ${costo['usageTotalUsd']}")
    return items, costo


def reel(p):
    return {
        "codigo": p.get("shortCode"), "url": p.get("url"), "cuenta": p.get("ownerUsername"),
        "tipo": p.get("type"), "producto": p.get("productType"), "fecha": p.get("timestamp"),
        "texto": p.get("caption"), "hashtags": p.get("hashtags"),
        "likes": p.get("likesCount"), "comentarios": p.get("commentsCount"),
        "reproducciones": p.get("videoPlayCount"), "vistas_video": p.get("videoViewCount"),
        "duracion_s": p.get("videoDuration"), "audio": p.get("musicInfo"),
        "transcripcion": p.get("transcript"),
        "comentarios_muestra": [c.get("text") for c in (p.get("latestComments") or [])][:10],
        "fijado": p.get("isPinned"), "colaboradores": p.get("coauthorProducers"),
    }


def post(p):
    hijos = p.get("childPosts") or []
    return {
        "codigo": p.get("shortCode"), "url": p.get("url"), "cuenta": p.get("ownerUsername"),
        "tipo": p.get("type"), "producto": p.get("productType"), "fecha": p.get("timestamp"),
        "texto": p.get("caption"), "hashtags": p.get("hashtags"),
        "likes": p.get("likesCount"), "comentarios": p.get("commentsCount"),
        "reproducciones": p.get("videoPlayCount"), "vistas_video": p.get("videoViewCount"),
        "duracion_s": p.get("videoDuration"), "n_diapositivas": len(hijos) or None,
        "alt": p.get("alt"), "fijado": p.get("isPinned"),
        "comentarios_muestra": [c.get("text") for c in (p.get("latestComments") or [])][:10],
    }


def main(pedido):
    if not TOKEN:
        print("Sin APIFY_TOKEN: no se corre nada.")
        return
    perfiles = pedido.get("perfiles") or []
    n_reels = min(int(pedido.get("reels_por_cuenta", MAX_ITEMS)), MAX_ITEMS)
    n_posts = min(int(pedido.get("posts_por_cuenta", MAX_ITEMS)), MAX_ITEMS)
    total = min(float(pedido.get("tope_total_usd", MAX_TOTAL)), MAX_TOTAL)
    url_reel = (pedido.get("url") or "").split("?")[0]
    # Reparto del tope total: 0.16 al reel suelto (si lo hay), el resto por
    # cuenta, 60 % reels (llevan transcripción) y 40 % posts.
    resto = total - (0.16 if url_reel else 0)
    por_cuenta = resto / max(len(perfiles), 1)
    costos = []
    SAL.mkdir(parents=True, exist_ok=True)
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    if url_reel:
        codigo = url_reel.rstrip("/").split("/")[-1]
        items, c = correr("apify~instagram-scraper", {"directUrls": [url_reel], "resultsType": "posts",
                                                       "resultsLimit": 1, "addParentData": False}, 0.08, 1)
        costos.append(c)
        items2, c2 = correr("apify~instagram-reel-scraper", {"username": [url_reel], "resultsLimit": 1,
                                                             "includeTranscript": True}, 0.08, 1)
        costos.append(c2)
        salida = {"traido": ahora, "motivo": pedido.get("motivo"), "url": url_reel, "codigo": codigo,
                  "fuente": "Apify · instagram-scraper + instagram-reel-scraper (público)",
                  "post": post(items[0]) if items else None,
                  "reel": reel(items2[0]) if items2 else None,
                  "crudo_post": items[0] if items else None,
                  "crudo_reel": items2[0] if items2 else None}
        if items or items2:
            (SAL / f"post-{codigo}.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1),
                                                     encoding="utf-8")

    for u in perfiles:
        u = u.lstrip("@").strip()
        reels, c = correr("apify~instagram-reel-scraper", {"username": [u], "resultsLimit": n_reels,
                                                           "includeTranscript": True},
                          por_cuenta * 0.6, n_reels)
        costos.append(c)
        posts, c2 = correr("apify~instagram-scraper", {"directUrls": [f"https://www.instagram.com/{u}/"],
                                                        "resultsType": "posts", "resultsLimit": n_posts,
                                                        "addParentData": False}, por_cuenta * 0.4, n_posts)
        costos.append(c2)
        reels = [x for x in (reels or []) if not x.get("error")]
        posts = [x for x in (posts or []) if not x.get("error")]
        if not reels and not posts:
            print(f"{u}: sin datos. No se escribe nada.")
            continue
        salida = {"traido": ahora, "motivo": pedido.get("motivo"), "cuenta": u,
                  "fuente": "Apify · instagram-reel-scraper (reels+transcripción) + instagram-scraper (posts)",
                  "reels": [reel(x) for x in reels][:n_reels], "posts": [post(x) for x in posts][:n_posts]}
        (SAL / f"perfil-{u}.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"ok → perfil-{u}.json · {len(salida['reels'])} reels · {len(salida['posts'])} posts")

    costos = [c for c in costos if c]
    gasto = sum((c.get("usageTotalUsd") or 0) for c in costos)
    (SAL / f"costo-referentes-{ahora[:10]}.json").write_text(json.dumps(
        {"fecha": ahora, "tope_total_usd": total, "usage_total_usd": round(gasto, 4), "corridas": costos},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Gasto reportado por Apify (usageTotalUsd): ${gasto:.4f} (tope ${total})")
