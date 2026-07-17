#!/usr/bin/env python3
"""
Refresca matriz-viral/matriz/matriz.json con datos frescos de Apify.

- Actualiza métricas (views/likes/comentarios) de los reels/posts ya listados.
- Agrega los posts nuevos (reels, carruseles, imágenes) clasificados por eje y
  estructura, con hook desde el caption.
- Conserva los campos curados a mano (tema/estructura/hook/nota/eje) de los que
  ya existen; solo refresca los números.
- Defensivo: si Apify falla o no devuelve datos, NO escribe nada y sale limpio
  (código 0) para que la Action no rompa cuando el plan free está sin crédito.

Uso local:  APIFY_TOKEN=xxxx python3 scripts/refresh_matriz.py [--limit 40]
Variables:  APIFY_TOKEN (obligatoria), USERNAME (def. design_modeling_dg),
            LIMIT (def. 40)
"""
import os, sys, json, re, unicodedata, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIZ = os.path.join(ROOT, "matriz-viral", "matriz", "matriz.json")
ACTOR = "apify~instagram-scraper"   # posts (reels + carruseles + imágenes)

USERNAME = os.environ.get("USERNAME_IG", "design_modeling_dg")
LIMIT = int(os.environ.get("LIMIT", "40"))
TOKEN = os.environ.get("APIFY_TOKEN", "").strip()


# ---------- clasificación (misma lógica del análisis manual) ----------
def _norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()

def _body(cap):
    """Cuerpo del caption SIN el bloque de hashtags (que en toda pieza trae
    #BIM #Revit #IA aunque el video sea de obra)."""
    keep = []
    for ln in (cap or "").split("\n"):
        toks = ln.split()
        h = sum(1 for t in toks if t.startswith("#"))
        if toks and h >= max(1, len(toks) // 2):
            continue
        keep.append(" ".join(t for t in toks if not t.startswith("#")))
    return _norm(" ".join(keep))

_BIM = ["revit","navisworks","dynamo","autodesk","power bi","powerbi","coordinacion bim",
        "coordinador bim","bim manager","modelador bim","clash","interferencia","parametro",
        "modelo bim","metodologia bim","gemelo digital", r"\bbim\b"]
_IA = ["inteligencia artificial","chatgpt","ia aplicada","automatiz", r"\bia\b"]
_PROMO = [r"\bmaster\b", r"\bcurso", "especializacion", "certificacion", "senescyt",
          "matricula", "diplomado", "quien puede estudiar"]

def _hit(b, ks):
    return any(re.search(k, b) for k in ks)

def clasificar_eje(cap):
    b = _body(cap)
    if _hit(b, _IA):  return "NÚCLEO-IA"
    if _hit(b, _BIM): return "NÚCLEO-BIM"
    if _hit(b, _PROMO): return "PROMO"
    return "OBRA"

def clasificar_estructura(cap):
    c = (cap or "").lower()
    first = (cap or "").split("\n")[0]
    if re.search(r"(arquitecto|inge|cliente|contratista|jefe|maestro|practicante)\w*\s*[:“\"]", c) \
       or any(k in c for k in ["😂","😎","cc de tiktok","chisme"]):
        return "DIÁLOGO-HUMOR"
    if any(k in c for k in ["¿sabías","sabías que","ya no significa","a veces los ingenieros"]):
        return "REVELACIÓN-TÉCNICA"
    if re.search(r"\b\d+\s+(cosas|tareas|criterios|errores|razones|tips|claves|preguntas)", c):
        return "LISTICLE-REVELACIÓN"
    if first.strip().startswith("¿"):
        return "PREGUNTA-REVELACIÓN"
    return "TUTORIAL-TÉCNICO"

def _firstline(cap):
    line = (cap or "").strip().split("\n")[0].strip()
    return re.sub(r"^[\W_]+", "", line)[:88]

def _tipo(post):
    t = (post.get("type") or "").lower()
    if t == "sidecar": return "carrusel"
    if t == "video":   return "reel"
    if t == "image":   return "imagen"
    return "post"


# ---------- Apify ----------
def scrape():
    if not TOKEN:
        print("ERROR: falta APIFY_TOKEN"); sys.exit(1)
    payload = json.dumps({
        "directUrls": [f"https://www.instagram.com/{USERNAME}/"],
        "resultsType": "posts", "resultsLimit": LIMIT, "addParentData": False,
    }).encode()
    url = (f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items"
           f"?token={TOKEN}")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=280) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Apify HTTP {e.code}: {e.read().decode()[:200]}")
        print("Sin datos frescos (¿límite del plan free?). No se modifica la matriz.")
        sys.exit(0)
    except Exception as e:
        print(f"Fallo de red con Apify: {e}. No se modifica la matriz.")
        sys.exit(0)
    rows = [x for x in data if isinstance(x, dict) and "error" not in x and x.get("shortCode")]
    if not rows:
        err = data[0] if isinstance(data, list) and data else data
        print(f"Apify no devolvió posts: {err}. No se modifica la matriz.")
        sys.exit(0)
    return rows


def main():
    with open(MATRIZ, encoding="utf-8") as f:
        matriz = json.load(f)
    by_sc = {r["shortCode"]: r for r in matriz["reels"]}
    ids = [int(r["id"][2:]) for r in matriz["reels"] if r["id"][2:].isdigit()]
    next_id = max(ids) + 1

    posts = scrape()
    upd, add = 0, 0
    for p in posts:
        sc = p["shortCode"]
        views = p.get("videoPlayCount")
        likes = p.get("likesCount")
        comm = p.get("commentsCount")
        if sc in by_sc:                       # refresca métricas, conserva lo curado
            r = by_sc[sc]
            changed = (r.get("views") != views or r.get("likes") != likes or r.get("comentarios") != comm)
            if views is not None: r["views"] = views
            if likes is not None: r["likes"] = likes
            if comm is not None:  r["comentarios"] = comm
            if changed: upd += 1
        else:                                 # post nuevo
            cap = p.get("caption") or ""
            matriz["reels"].append({
                "id": f"DM{next_id}", "shortCode": sc, "cuenta": USERNAME,
                "tipo": _tipo(p), "eje": clasificar_eje(cap),
                "fecha": (p.get("timestamp") or "")[:10],
                "duracion_s": round(p.get("videoDuration") or 0, 1) or None,
                "views": views, "likes": likes, "comentarios": comm, "shares": None,
                "tema": _firstline(cap)[:60], "estructura": clasificar_estructura(cap),
                "hook": _firstline(cap), "nota": "⟨auto⟩ agregado por refresh_matriz",
                "url": f"https://www.instagram.com/p/{sc}/",
            })
            next_id += 1; add += 1

    if upd == 0 and add == 0:
        print("Sin cambios. Matriz ya estaba fresca."); return

    matriz["reels"].sort(key=lambda r: (r.get("views") is None, -(r.get("views") or 0)))
    matriz["total_reels"] = len(matriz["reels"])
    with open(MATRIZ, "w", encoding="utf-8") as f:
        json.dump(matriz, f, ensure_ascii=False, indent=1)
    print(f"Matriz actualizada: {upd} con métricas nuevas, {add} posts nuevos. "
          f"Total: {matriz['total_reels']}.")


if __name__ == "__main__":
    main()
