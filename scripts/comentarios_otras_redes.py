#!/usr/bin/env python3
"""Lee los comentarios recientes de YouTube (shorts), TikTok, Threads y LinkedIn con Apify.

    python3 scripts/comentarios_otras_redes.py matriz-viral/comentarios/otras-redes.json

Por qué existe: GHL solo trae comentarios de lo que se publica DESDE GHL. Los
shorts, los TikTok y los posts que se suben directo a cada red no aparecen ahí,
así que la revisión diaria no los veía (Dayana, 23-nov). Esto solo LEE:
responder sigue siendo a mano en cada red, o desde GHL si la pieza salió por GHL.

Pedido (JSON): {"dias": 2, "redes": ["youtube", "tiktok", "threads", "linkedin"],
                "nota": "..."}
Cada actor lleva su tope duro de gasto; el total no pasa de ~0,46 USD por corrida.
Imprime los comentarios de los últimos `dias` entre ===OTRAS_REDES_JSON=== y
===FIN_JSON===, uno por línea con FILA {json} (el log de Actions corta líneas largas),
y avisa de las redes que no devolvieron nada. Vacío antes que inventado.
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()

YOUTUBE = "DesignModelingDG"
TIKTOK = "designmodelingdg"
THREADS = "design_modeling_dg"
LINKEDIN = ["https://www.linkedin.com/company/65456800/", "https://www.linkedin.com/company/98810392/"]
NUESTROS = {"designmodelingdg", "@designmodelingdg", "design_modeling_dg", "design modeling academy",
            "design modeling dg", "design modeling", "designmodelingacademy"}

TOPES = {"yt_shorts": 0.06, "yt_comentarios": 0.10, "tiktok": 0.12, "threads": 0.08, "linkedin": 0.10}


def actor(nombre, entrada, tope):
    url = (f"https://api.apify.com/v2/acts/{nombre}/run-sync-get-dataset-items"
           f"?token={TOKEN}&maxTotalChargeUsd={tope}")
    req = urllib.request.Request(url, data=json.dumps(entrada).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=290) as r:
            datos = json.loads(r.read().decode())
            return datos if isinstance(datos, list) else []
    except urllib.error.HTTPError as e:
        print(f"AVISO Apify HTTP {e.code} en {nombre}: {e.read().decode()[:300]}")
    except Exception as e:  # noqa: BLE001
        print(f"AVISO fallo de red con Apify ({nombre}): {e}")
    return []


def primero(d, *claves):
    """Devuelve el primer valor no vacío entre varias claves (admite 'a.b')."""
    for c in claves:
        v = d
        for parte in c.split("."):
            v = v.get(parte) if isinstance(v, dict) else None
        if v not in (None, "", [], {}):
            return v
    return None


def fecha(v):
    if v in (None, ""):
        return None
    try:
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v / 1000 if v > 1e11 else v, tz=timezone.utc)
        return datetime.fromisoformat(str(v).replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def es_nuestro(autor):
    a = str(autor or "").strip().lower()
    return a in NUESTROS or a.lstrip("@") in NUESTROS


def muestra(red, items):
    """Para la primera corrida: qué campos devuelve cada actor (sin datos personales)."""
    if items:
        print(f"CAMPOS {red}: {sorted(items[0].keys())[:40]}")


def youtube(desde):
    shorts = actor("streamers~youtube-shorts-scraper",
                   {"channels": [YOUTUBE], "maxResultsShorts": 12, "sortChannelShortsBy": "NEWEST"},
                   TOPES["yt_shorts"])
    muestra("youtube_shorts", shorts)
    urls = [s.get("url") for s in shorts if s.get("url")]
    titulos = {s.get("url"): (s.get("title") or "")[:90] for s in shorts}
    if not urls:
        return [], "sin shorts"
    coms = actor("streamers~youtube-comments-scraper",
                 {"startUrls": [{"url": u} for u in urls], "maxComments": 40,
                  "sortCommentsBy": "NEWEST_FIRST", "oldestCommentDate": desde.strftime("%Y-%m-%d")},
                 TOPES["yt_comentarios"])
    muestra("youtube_comentarios", coms)
    filas = []
    for c in coms:
        autor = primero(c, "author", "authorText", "authorName")
        url = primero(c, "pageUrl", "videoUrl", "url")
        filas.append({"red": "youtube", "autor": autor, "texto": primero(c, "comment", "text", "content"),
                      "fecha": primero(c, "publishedTimeText", "date", "publishedAt"),
                      "_f": fecha(primero(c, "date", "publishedAt", "publishedTime")),
                      "respuestas": primero(c, "replyCount", "repliesCount") or 0,
                      "publicacion": titulos.get(url) or primero(c, "title", "videoTitle"), "url": url,
                      "nuestro": bool(c.get("authorIsChannelOwner")) or es_nuestro(autor)})
    return filas, f"{len(urls)} shorts revisados"


def tiktok(desde):
    items = actor("clockworks~tiktok-scraper",
                  {"profiles": [TIKTOK], "resultsPerPage": 12, "profileSorting": "latest",
                   "excludePinnedPosts": False, "commentsPerPost": 40, "maxRepliesPerComment": 3,
                   "shouldDownloadVideos": False, "shouldDownloadCovers": False},
                  TOPES["tiktok"])
    muestra("tiktok", items)
    filas, videos = [], 0
    for it in items:
        # El actor devuelve videos y, si se piden, comentarios en el mismo dataset.
        if primero(it, "cid", "commentId") or "comment" in it and not it.get("videoMeta"):
            autor = primero(it, "uniqueId", "user.uniqueId", "author", "authorMeta.name")
            filas.append({"red": "tiktok", "autor": autor, "texto": primero(it, "text", "comment"),
                          "fecha": primero(it, "createTimeISO", "createTime"),
                          "_f": fecha(primero(it, "createTimeISO", "createTime")),
                          "respuestas": primero(it, "replyCommentTotal", "repliesCount") or 0,
                          "publicacion": primero(it, "videoWebUrl", "postUrl"), "url": primero(it, "videoWebUrl"),
                          "nuestro": es_nuestro(autor), "es_respuesta": bool(primero(it, "repliesToId"))})
        else:
            videos += 1
            for c in it.get("comments") or []:
                autor = primero(c, "uniqueId", "user.uniqueId", "author")
                filas.append({"red": "tiktok", "autor": autor, "texto": primero(c, "text", "comment"),
                              "fecha": primero(c, "createTimeISO", "createTime"),
                              "_f": fecha(primero(c, "createTimeISO", "createTime")),
                              "respuestas": primero(c, "replyCommentTotal") or 0,
                              "publicacion": (it.get("text") or "")[:90], "url": it.get("webVideoUrl"),
                              "nuestro": es_nuestro(autor)})
    return filas, f"{videos} videos revisados"


def threads(desde):
    items = actor("futurizerush~meta-threads-scraper",
                  {"mode": "user", "usernames": [THREADS], "max_posts": 10,
                   "start_date": desde.strftime("%Y-%m-%d")},
                  TOPES["threads"])
    muestra("threads", items)
    filas = []
    for it in items:
        autor = primero(it, "username", "author.username", "user.username")
        if es_nuestro(autor) and not primero(it, "reply_to", "parent_id", "in_reply_to"):
            continue  # nuestros posts: solo cuentan las respuestas de otros
        filas.append({"red": "threads", "autor": autor, "texto": primero(it, "text", "caption", "content"),
                      "fecha": primero(it, "published_on", "created_at", "timestamp"),
                      "_f": fecha(primero(it, "published_on", "created_at", "timestamp")),
                      "respuestas": primero(it, "reply_count", "replies") or 0,
                      "publicacion": primero(it, "reply_to_text", "parent_text"), "url": primero(it, "url", "link"),
                      "nuestro": es_nuestro(autor)})
    return filas, f"{len(items)} elementos"


def linkedin(desde):
    items = actor("harvestapi~linkedin-company-posts",
                  {"targetUrls": LINKEDIN, "maxPosts": 8, "scrapeComments": True, "maxComments": 30,
                   "scrapeReactions": False, "includeReposts": False},
                  TOPES["linkedin"])
    muestra("linkedin", items)
    filas, posts = [], 0
    for it in items:
        tipo = str(it.get("type") or "").lower()
        if tipo == "comment" or primero(it, "commentary", "comment") and not primero(it, "content.text"):
            autor = primero(it, "actor.name", "author.name", "authorName")
            filas.append({"red": "linkedin", "autor": autor, "texto": primero(it, "commentary", "comment", "text"),
                          "fecha": primero(it, "createdAt", "postedAt.date"),
                          "_f": fecha(primero(it, "createdAt", "postedAt.timestamp", "postedAt.date")),
                          "respuestas": primero(it, "numComments", "replies") or 0,
                          "publicacion": primero(it, "postId", "post.url"), "url": primero(it, "linkedinUrl", "url"),
                          "nuestro": es_nuestro(autor)})
        else:
            posts += 1
            for c in it.get("comments") or []:
                autor = primero(c, "actor.name", "author.name")
                filas.append({"red": "linkedin", "autor": autor, "texto": primero(c, "commentary", "text"),
                              "fecha": primero(c, "createdAt"), "_f": fecha(primero(c, "createdAt")),
                              "respuestas": primero(c, "numComments") or 0,
                              "publicacion": (primero(it, "content", "text") or "")[:90],
                              "url": primero(it, "linkedinUrl", "url"), "nuestro": es_nuestro(autor)})
    return filas, f"{posts} posts revisados"


def main():
    if not TOKEN:
        print("Sin APIFY_TOKEN: no se corre nada.")
        return
    pedido = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    dias = int(pedido.get("dias", 2))
    redes = pedido.get("redes") or ["youtube", "tiktok", "threads", "linkedin"]
    desde = datetime.now(timezone.utc) - timedelta(days=dias)
    print(f"Ventana: desde {desde:%Y-%m-%d %H:%M} UTC · redes: {', '.join(redes)} · "
          f"tope total {sum(TOPES.values()):.2f} USD")
    fn = {"youtube": youtube, "tiktok": tiktok, "threads": threads, "linkedin": linkedin}
    todas, resumen = [], {}
    for red in redes:
        filas, nota = fn[red](desde)
        recientes = [f for f in filas if f["_f"] is None or f["_f"] >= desde]
        externos = [f for f in recientes if not f["nuestro"]]
        resumen[red] = {"nota": nota, "comentarios_leidos": len(filas), "recientes_de_otros": len(externos),
                        "sin_fecha": sum(1 for f in externos if f["_f"] is None)}
        todas += externos
        if not filas:
            print(f"AVISO {red}: no devolvió comentarios ({nota}). Puede ser que no haya, o que el actor falló.")
    print("===RESUMEN=== " + json.dumps(resumen, ensure_ascii=False))
    print("===OTRAS_REDES_JSON===")
    for f in sorted(todas, key=lambda f: (f["red"], str(f["fecha"]))):
        f = {k: v for k, v in f.items() if k != "_f"}
        print("FILA " + json.dumps(f, ensure_ascii=False, default=str))
    print("===FIN_JSON===")


if __name__ == "__main__":
    main()
