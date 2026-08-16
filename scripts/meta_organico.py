#!/usr/bin/env python3
"""
Recolecta métricas ORGÁNICAS de Instagram y Facebook con la Graph API oficial
de Meta y alimenta matriz-viral/matriz/matriz.json.

Reemplaza a Apify: es oficial, gratis y sin límite mensual de créditos.
Usa el mismo token de System User que ya usa dma-sales-assistant (no expira).

Requisitos del token (verificados): instagram_basic, instagram_manage_insights,
pages_read_engagement, pages_show_list, read_insights.

Uso:
    export META_TOKEN=EAA...            # token de System User
    python3 scripts/meta_organico.py --dry-run      # solo mostrar
    python3 scripts/meta_organico.py --limit 25     # aplicar a la matriz

Notas:
  - Las "views" de la Graph API son SOLO de Instagram. Las de Facebook se
    consultan aparte y se guardan en `views_facebook` (en julio, FB fue más
    de la mitad del alcance real).
  - Nunca inventa datos: la métrica que Meta no devuelve queda vacía.
"""
import datetime, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIZ = os.path.join(ROOT, "matriz-viral", "matriz", "matriz.json")
BASE = "https://graph.facebook.com/v20.0"

TOKEN = os.environ.get("META_TOKEN", "").strip()
PAGE_ID = os.environ.get("META_PAGE_ID", "101355061550758")       # Design Modeling Academy
IG_ID = os.environ.get("META_IG_ID", "17841404048578200")         # @design_modeling_dg

# Los REELS no aceptan profile_visits/follows — hay que pedir métricas por tipo.
IG_METRICS_FEED = "views,reach,likes,comments,saved,shares,total_interactions,profile_visits,follows"
IG_METRICS_REEL = "views,reach,likes,comments,saved,shares,total_interactions"
MAP = {  # métrica de Meta -> campo en la matriz
    "views": "views", "reach": "alcance", "likes": "likes", "comments": "comentarios",
    "saved": "guardados", "shares": "shares", "total_interactions": "interacciones",
    "profile_visits": "visitas_perfil", "follows": "nuevos_seguidores",
}


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        body = ""
        if hasattr(e, "read"):
            try: body = e.read().decode()[:200]
            except Exception: pass
        return {"error": {"message": f"{e} {body}"}}


# ---------- Instagram ----------
def ig_posts(limit):
    d = api(f"{IG_ID}/media",
            fields="id,shortcode,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count",
            limit=limit)
    if "error" in d:
        print("✗ Instagram:", d["error"]["message"]); return []
    return d.get("data", [])


def ig_insights(media_id, product_type=""):
    metrics = IG_METRICS_REEL if product_type == "REELS" else IG_METRICS_FEED
    d = api(f"{media_id}/insights", metric=metrics)
    if "error" in d:  # último recurso: el set mínimo que todos aceptan
        d = api(f"{media_id}/insights", metric="views,reach,likes,comments,saved,shares")
        if "error" in d:
            d = api(f"{media_id}/insights", metric="reach,likes,comments,saved")
            if "error" in d: return {}
    out = {}
    for m in d.get("data", []):
        campo = MAP.get(m["name"])
        vals = m.get("values") or [{}]
        if campo and vals[0].get("value") is not None:
            out[campo] = vals[0]["value"]
    return out


# ---------- Facebook ----------
def fb_page_token():
    d = api(PAGE_ID, fields="access_token")
    return d.get("access_token", "")


def fb_posts(limit, page_tok):
    global TOKEN
    orig, TOKEN = TOKEN, (page_tok or TOKEN)
    d = api(f"{PAGE_ID}/posts", fields="id,message,created_time,permalink_url", limit=limit)
    posts = [] if "error" in d else d.get("data", [])
    if "error" in d: print("⚠ Facebook:", d["error"]["message"][:120])
    res = []
    for p in posts:
        # OJO: Meta ELIMINÓ post_impressions/views por post en v20+ (probado hasta
        # v23). Las vistas de FB solo se ven en la UI de Insights → se cargan a
        # mano. Lo que SÍ sigue disponible es la actividad (comentarios, likes,
        # compartidos) y los clics.
        ins = api(f"{p['id']}/insights",
                  metric="post_activity_by_action_type,post_video_views,post_clicks")
        vals = {}
        for m in (ins.get("data") or []):
            v = (m.get("values") or [{}])[0].get("value")
            if v is None: continue
            if m["name"] == "post_activity_by_action_type" and isinstance(v, dict):
                if v.get("comment") is not None: vals["comentarios_facebook"] = v["comment"]
                if v.get("like") is not None: vals["likes_facebook"] = v["like"]
                if v.get("share") is not None: vals["shares_facebook"] = v["share"]
            else:
                vals[m["name"]] = v
        p["_insights"] = vals
        res.append(p)
    TOKEN = orig
    return res


def norm(s):
    """Normaliza texto para cruzar posts de IG y FB (quita emojis, markdown, tildes)."""
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[*_#]", "", s.lower())
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def main():
    if not TOKEN:
        print("ERROR: falta META_TOKEN en el entorno."); sys.exit(1)
    dry = "--dry-run" in sys.argv
    limit = 25
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    print(f"→ Instagram: leyendo últimas {limit} publicaciones…")
    posts = ig_posts(limit)
    if not posts: sys.exit(1)

    datos = []
    for p in posts:
        ins = ig_insights(p["id"], p.get("media_product_type", ""))
        datos.append({
            "shortCode": p.get("shortcode"), "media_id": p["id"],
            "fecha": (p.get("timestamp") or "")[:10],
            "tipo": {"REELS": "reel", "FEED": "post", "STORY": "story"}.get(p.get("media_product_type"), "post"),
            "caption": p.get("caption") or "", "url": p.get("permalink"),
            "likes": p.get("like_count"), "comentarios": p.get("comments_count"),
            **ins,
        })
        time.sleep(0.15)  # cortesía con la API

    # Facebook: cruzar por texto del post
    print("→ Facebook: leyendo publicaciones de la página…")
    ptok = fb_page_token()
    fb = fb_posts(limit, ptok)
    for f in fb:
        k = norm(f.get("message"))
        if len(k) < 25: continue           # mensajes muy cortos dan falsos positivos
        firma = k[:45]
        for d in datos:
            cap = norm(d["caption"])
            if firma in cap or cap[:45] in k:
                v = f["_insights"]
                for campo in ("comentarios_facebook", "likes_facebook", "shares_facebook"):
                    if v.get(campo) is not None: d[campo] = v[campo]
                if v.get("post_video_views"):          # solo videos nativos de FB
                    d["views_facebook"] = v["post_video_views"]
                break

    # Mostrar
    print(f"\n{'FECHA':11} {'TIPO':6} {'VIEWS':>7} {'ALC':>6} {'LIKE':>5} {'COM':>4} {'GUAR':>5} {'FBcom':>7}  TEMA")
    for d in datos:
        cap = d["caption"].replace("\n", " ")[:38]
        print(f"{d['fecha']:11} {d['tipo']:6} {str(d.get('views','-')):>7} {str(d.get('alcance','-')):>6} "
              f"{str(d.get('likes','-')):>5} {str(d.get('comentarios','-')):>4} {str(d.get('guardados','-')):>5} "
              f"{str(d.get('comentarios_facebook','-')):>7}  {cap}")

    # Aplicar a la matriz
    m = json.load(open(MATRIZ, encoding="utf-8"))
    by_sc = {r.get("shortCode"): r for r in m["reels"] if r.get("shortCode")}
    maxid = max(int(r["id"][2:]) for r in m["reels"] if r["id"][2:].isdigit())
    upd = new = 0
    CAMPOS = ["views", "alcance", "likes", "comentarios", "guardados", "shares",
              "interacciones", "visitas_perfil", "nuevos_seguidores",
              "views_facebook", "comentarios_facebook", "likes_facebook", "shares_facebook"]
    for d in datos:
        vals = {k: d[k] for k in CAMPOS if d.get(k) is not None}
        r = by_sc.get(d["shortCode"])
        if r:
            r.update(vals); r["media_id"] = d["media_id"]
            r["fuente_metricas"] = "Meta Graph API (oficial)"
            r.pop("reconciliar_shortcode", None)
            upd += 1
        else:
            maxid += 1
            nuevo = {"id": f"DM{maxid}", "shortCode": d["shortCode"], "media_id": d["media_id"],
                     "cuenta": "design_modeling_dg", "tipo": d["tipo"], "eje": None,
                     "fecha": d["fecha"], "tema": d["caption"].split("\n")[0][:60],
                     "estructura": None, "hook": d["caption"].split("\n")[0][:88],
                     "nota": "⟨auto⟩ agregado por meta_organico — completar eje y lectura.",
                     "fuente_metricas": "Meta Graph API (oficial)", "url": d["url"], **vals}
            m["reels"].append(nuevo); new += 1

    print(f"\nActualizadas: {upd} · Nuevas: {new}")
    if dry:
        print("(--dry-run: no se escribió nada)"); return
    m["reels"].sort(key=lambda r: (r.get("views") is None, -(r.get("views") or 0)))
    m["total_reels"] = len(m["reels"])

    # Sello de frescura. Son DOS fechas distintas y hay que separarlas:
    #
    #   generado    = el barrido completo, cuando se construyó toda la matriz.
    #   actualizado = esta corrida, que solo refresca las últimas `limit`
    #                 piezas. Las más viejas conservan sus números de entonces.
    #
    # Hasta hoy solo existía `generado`, y esta función no lo tocaba: la matriz
    # se refrescaba de verdad pero seguía sellada el 28-jul. El asistente la
    # anunciaba como «datos de hace 18 días» cuando eran de esa mañana, y se
    # reportó como si el refresco estuviera roto. No lo estaba: mentía el sello.
    hoy = datetime.date.today().isoformat()
    m["actualizado"] = hoy
    m["actualizado_piezas"] = upd + new
    m["actualizado_fuente"] = "Meta Graph API (oficial)"
    m.setdefault("generado", hoy)

    json.dump(m, open(MATRIZ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"✓ matriz.json actualizado ({m['total_reels']} piezas · "
          f"{upd + new} refrescadas hoy · barrido completo del {m['generado']})")


if __name__ == "__main__":
    main()
