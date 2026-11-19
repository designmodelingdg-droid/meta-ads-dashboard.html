#!/usr/bin/env python3
"""
Lista y responde los comentarios de Instagram y Facebook de Design Modeling,
los orgánicos y los de los anuncios, con el token del System User
«Design Modeling - Ads CLI» (META_TOKEN).

Por qué existe: el planificador de GoHighLevel deja de mostrar los comentarios
de Instagram y Facebook al día siguiente, y los comentarios de los anuncios no
salen en ningún sitio. Nadie los responde. Este script los lee
directamente de la API de Meta.

Dos modos:
  MODO=listar     NO publica nada. Busca los comentarios de los últimos DIAS
                  días que todavía no tienen respuesta nuestra y los imprime:
                  un resumen legible y una línea JSON entre marcadores.
  MODO=responder  Publica las respuestas de RESPUESTAS (JSON):
                    [{"red": "instagram"|"facebook", "comment_id": "...", "texto": "..."}]
                  Antes de cada una vuelve a mirar si ya respondimos, así que
                  correrlo dos veces no duplica nada.

El token nunca se imprime.
"""
import datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

BASE = "https://graph.facebook.com/v21.0"
CUENTA_ADS = "act_1159622151150228"
IG_ID = "17841404048578200"                      # @design_modeling_dg
PAGE_ID = os.environ.get("META_PAGE_ID", "101355061550758")   # Design Modeling Academy
IG_NUESTROS = {"design_modeling_dg", "design_modeling_constru"}

TOKEN = os.environ.get("META_TOKEN", "").strip()
MODO = (os.environ.get("MODO") or "listar").strip()
DIAS = int(os.environ.get("DIAS") or "7")
MAX_COMENT_POR_PUB = int(os.environ.get("MAX_COMENT") or "300")
AHORA = datetime.datetime.now(datetime.timezone.utc)
CORTE = AHORA - datetime.timedelta(days=DIAS)


def _req(path, metodo="GET", token=None, **params):
    params["access_token"] = token or TOKEN
    url = path if path.startswith("http") else f"{BASE}/{path}"
    data = None
    if metodo == "GET":
        if "?" not in url:
            url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=metodo)
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            cuerpo = e.read() or b"{}"
            try:
                err = json.loads(cuerpo).get("error", {})
            except ValueError:
                err = {"message": cuerpo[:200].decode("utf-8", "replace")}
            if e.code in (500, 502, 503) and intento < 2:
                time.sleep(3)
                continue
            return {"error": err.get("message", str(e)), "code": err.get("code")}
        except urllib.error.URLError as e:
            if intento < 2:
                time.sleep(3)
                continue
            return {"error": str(e)}


def get(path, token=None, **p):
    return _req(path, "GET", token, **p)


def paginar(path, token=None, tope=1000, **p):
    """Recorre las páginas de un edge. Devuelve (filas, error)."""
    d = get(path, token, **p)
    filas = []
    while True:
        if "error" in d:
            return filas, d["error"]
        filas += d.get("data", [])
        sig = (d.get("paging") or {}).get("next")
        if not sig or len(filas) >= tope:
            return filas, None
        d = get(sig, token)


def fecha(s):
    # Meta devuelve 2026-11-12T15:04:05+0000
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


def token_pagina():
    d = get(PAGE_ID, fields="access_token")
    if "error" in d:
        print("⚠️  Sin token de página:", d["error"])
        return None
    return d.get("access_token")


# ── qué publicaciones mirar ──────────────────────────────────────────────────
def objetivos(ptoken):
    """Lista de publicaciones cuyos comentarios hay que revisar."""
    obj, vistos = [], set()

    def add(red, oid, origen, enlace, texto):
        if oid and (red, oid) not in vistos:
            vistos.add((red, oid))
            obj.append({"red": red, "id": oid, "origen": origen,
                        "enlace": enlace or "", "pub": (texto or "").replace("\n", " ")[:90]})

    # Instagram orgánico: las últimas 60 publicaciones con comentarios
    media, err = paginar(f"{IG_ID}/media", tope=60, limit=50,
                         fields="id,caption,permalink,timestamp,comments_count")
    if err:
        print("⚠️  Instagram /media:", err)
    for m in media:
        if m.get("comments_count"):
            add("instagram", m["id"], "orgánico", m.get("permalink"), m.get("caption"))

    # Facebook orgánico: las últimas 60 publicaciones de la página
    if ptoken:
        posts, err = paginar(f"{PAGE_ID}/published_posts", ptoken, tope=60, limit=50,
                             fields="id,message,permalink_url,created_time")
        if err:
            print("⚠️  Facebook /published_posts:", err)
        for p in posts:
            add("facebook", p["id"], "orgánico", p.get("permalink_url"), p.get("message"))

    # Anuncios con entrega en la ventana: su publicación de FB y su media de IG
    hasta = AHORA.date()
    desde = (AHORA - datetime.timedelta(days=DIAS)).date()
    filas, err = paginar(f"{CUENTA_ADS}/insights", tope=500, level="ad", limit=200,
                         fields="ad_id,ad_name,spend",
                         time_range=json.dumps({"since": str(desde), "until": str(hasta)}))
    if err:
        print("⚠️  Anuncios /insights:", err)
    for f in filas:
        ad = get(f["ad_id"], fields="name,creative{effective_object_story_id,"
                                    "effective_instagram_media_id,instagram_permalink_url}")
        if "error" in ad:
            print("⚠️  Anuncio", f.get("ad_name"), ad["error"])
            continue
        cr = ad.get("creative") or {}
        nombre = "anuncio: " + (ad.get("name") or f.get("ad_name") or "")[:60]
        add("facebook", cr.get("effective_object_story_id"), nombre, "", "")
        add("instagram", cr.get("effective_instagram_media_id"), nombre,
            cr.get("instagram_permalink_url"), "")
    return obj


# ── comentarios sin respuesta ────────────────────────────────────────────────
def pendientes_ig(o):
    filas, err = paginar(f"{o['id']}/comments", tope=MAX_COMENT_POR_PUB, limit=50,
                         fields="id,text,username,timestamp,like_count,"
                                "replies{username,timestamp}")
    if err:
        return [], err
    out = []
    for c in filas:
        if not c.get("timestamp") or fecha(c["timestamp"]) < CORTE:
            continue
        if (c.get("username") or "").lower() in IG_NUESTROS:
            continue
        resp = (c.get("replies") or {}).get("data", [])
        if any((r.get("username") or "").lower() in IG_NUESTROS for r in resp):
            continue
        out.append({"red": "instagram", "comment_id": c["id"], "autor": c.get("username"),
                    "texto": c.get("text"), "fecha": c["timestamp"],
                    "otras_respuestas": len(resp)})
    return out, None


def pendientes_fb(o, ptoken):
    filas, err = paginar(f"{o['id']}/comments", ptoken, tope=MAX_COMENT_POR_PUB, limit=50,
                         filter="toplevel", order="reverse_chronological",
                         fields="id,message,from,created_time,comment_count,"
                                "comments.limit(25){from,created_time}")
    if err:
        return [], err
    out = []
    for c in filas:
        if not c.get("created_time"):
            continue
        if fecha(c["created_time"]) < CORTE:
            break                      # vienen del más nuevo al más viejo
        if (c.get("from") or {}).get("id") == PAGE_ID:
            continue
        resp = (c.get("comments") or {}).get("data", [])
        if any((r.get("from") or {}).get("id") == PAGE_ID for r in resp):
            continue
        out.append({"red": "facebook", "comment_id": c["id"],
                    "autor": (c.get("from") or {}).get("name") or "(sin nombre)",
                    "texto": c.get("message"), "fecha": c["created_time"],
                    "otras_respuestas": len(resp)})
    return out, None


def listar():
    ptoken = token_pagina()
    obj = objetivos(ptoken)
    print(f"Ventana: desde {CORTE:%Y-%m-%d %H:%M} UTC ({DIAS} días) · publicaciones revisadas: {len(obj)}")
    todos = []
    for o in obj:
        if o["red"] == "instagram":
            pend, err = pendientes_ig(o)
        elif ptoken:
            pend, err = pendientes_fb(o, ptoken)
        else:
            continue
        if err:
            print(f"⚠️  {o['red']} {o['origen']} {o['id']}: {err}")
            continue
        for p in pend:
            p.update({"origen": o["origen"], "publicacion": o["pub"], "enlace": o["enlace"],
                      "pub_id": o["id"]})
        todos += pend
    todos.sort(key=lambda p: p["fecha"], reverse=True)
    print(f"\nComentarios sin respuesta nuestra: {len(todos)}")
    for p in todos:
        print(f"- [{p['red']} · {p['origen']}] {p['fecha'][:16]} · {p['autor']}: "
              f"{(p['texto'] or '').replace(chr(10), ' ')[:160]}")
        print(f"    comment_id={p['comment_id']} · pub: {p['publicacion'][:70]}")
    print("===COMENTARIOS_JSON===")
    print(json.dumps(todos, ensure_ascii=False))
    print("===FIN_JSON===")


# ── responder ────────────────────────────────────────────────────────────────
def ya_respondido(red, cid, ptoken):
    if red == "instagram":
        d = get(cid, fields="replies{username}")
        return any((r.get("username") or "").lower() in IG_NUESTROS
                   for r in (d.get("replies") or {}).get("data", []))
    d = get(f"{cid}/comments", ptoken, fields="from", limit=50)
    return any((r.get("from") or {}).get("id") == PAGE_ID for r in d.get("data", []))


def responder():
    crudo = os.environ.get("RESPUESTAS") or "[]"
    try:
        lista = json.loads(crudo)
    except ValueError as e:
        sys.exit(f"RESPUESTAS no es JSON válido: {e}")
    ptoken = token_pagina()
    ok = 0
    for r in lista:
        red, cid, texto = r.get("red"), r.get("comment_id"), (r.get("texto") or "").strip()
        if red not in ("instagram", "facebook") or not cid or not texto:
            print("✖ Entrada incompleta, se salta:", json.dumps(r, ensure_ascii=False)[:120])
            continue
        if red == "facebook" and not ptoken:
            print("✖", cid, "sin token de página")
            continue
        if ya_respondido(red, cid, ptoken):
            print("= ya tenía respuesta nuestra:", red, cid)
            continue
        if red == "instagram":
            d = _req(f"{cid}/replies", "POST", message=texto)
        else:
            d = _req(f"{cid}/comments", "POST", ptoken, message=texto)
        if "error" in d:
            print("✖", red, cid, "→", d["error"])
        else:
            ok += 1
            print("✔", red, cid, "→ respuesta", d.get("id"))
        time.sleep(2)
    print(f"\nRespondidos {ok} de {len(lista)}")


if __name__ == "__main__":
    if not TOKEN:
        sys.exit("Falta META_TOKEN")
    responder() if MODO == "responder" else listar()
