#!/usr/bin/env python3
"""Comentarios de TikTok, LinkedIn y YouTube por sus APIs oficiales.

  python3 scripts/comentarios_redes.py tiktok|linkedin|youtube

Lee la orden de matriz-viral/comentarios/orden-redes.json (si el flujo corrió
por push) o de las variables IN_MODO, IN_DIAS, IN_REDES e IN_RESP.

  modo=listar     no publica: deja en el registro los comentarios de los últimos
                  N días que no tienen respuesta nuestra, cada uno con su «ref».
  modo=responder  publica las respuestas de la orden ({"red", "ref", "texto"}).
                  Antes de cada una comprueba que el comentario siga sin
                  respuesta nuestra, así que no duplica.

Nunca imprime tokens. Los tokens de TikTok y LinkedIn viven cifrados en
matriz-viral/<red>/token.enc; si se renuevan, el flujo guarda el archivo.
"""
import json, os, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

RED = sys.argv[1]
AHORA = int(time.time())
ORGS = {"65456800": "Design Modeling Academy", "98810392": "Design Modeling DG"}


def orden():
    if os.environ.get("EVENTO") == "push":
        o = json.load(open("matriz-viral/comentarios/orden-redes.json"))
        return o.get("modo", "listar"), int(o.get("dias", 7)), o.get("redes") or ["tiktok", "linkedin", "youtube"], o.get("respuestas") or []
    redes = [r.strip() for r in (os.environ.get("IN_REDES") or "tiktok,linkedin,youtube").split(",") if r.strip()]
    return (os.environ.get("IN_MODO") or "listar", int(os.environ.get("IN_DIAS") or 7), redes,
            json.loads(os.environ.get("IN_RESP") or "[]"))


def ocultar(v):
    if v:
        print(f"::add-mask::{v}")


def http(url, metodo="GET", cabeceras=None, cuerpo=None, forma=None):
    data = None
    cab = dict(cabeceras or {})
    if cuerpo is not None:
        data = json.dumps(cuerpo).encode(); cab.setdefault("Content-Type", "application/json")
    if forma is not None:
        data = urllib.parse.urlencode(forma).encode(); cab.setdefault("Content-Type", "application/x-www-form-urlencoded")
    req = urllib.request.Request(url, data=data, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            t = r.read().decode()
            d = json.loads(t) if t.strip() else {}
            if isinstance(d, dict):
                d.setdefault("_http", r.status); d["_cab"] = dict(r.headers)
            return d
    except urllib.error.HTTPError as e:
        t = e.read().decode("utf-8", "replace")
        try:
            d = json.loads(t)
        except Exception:
            d = {"message": t[:300]}
        if isinstance(d, dict):
            d["_http"] = e.code
        return d


def cifrar(archivo, clave_env, texto):
    subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-salt", "-a", "-A",
                    "-out", archivo, "-pass", "env:" + clave_env], input=texto.encode(), check=True)


def descifrar(archivo, clave_env):
    r = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-a", "-A",
                        "-in", archivo, "-pass", "env:" + clave_env], capture_output=True, check=True)
    return json.loads(r.stdout.decode())


def fecha(ts):
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(int(ts)))


def mostrar(pend):
    for p in pend:
        print(f"· {p['red']} | {p['fecha']} | {p['autor']} | {p['post'][:70]}")
        print(f"    «{p['texto'][:400]}»")
        print("    ref: " + json.dumps(p["ref"], ensure_ascii=False))
    print(f"PENDIENTES {RED}: {len(pend)}")


# ───────────────────────────── TikTok ─────────────────────────────
class TikTok:
    BASE = "https://business-api.tiktok.com/open_api/v1.3"
    ARCHIVO = "matriz-viral/tiktok/token.enc"

    def __init__(self):
        if not os.environ.get("TIKTOK_APP_ID") or not os.environ.get("TIKTOK_APP_SECRET"):
            sys.exit("Faltan TIKTOK_APP_ID o TIKTOK_APP_SECRET.")
        g = descifrar(self.ARCHIVO, "TIKTOK_APP_SECRET")
        ocultar(g.get("refresh_token"))
        r = http(self.BASE + "/tt_user/oauth2/refresh_token/", "POST", cuerpo={
            "client_id": os.environ["TIKTOK_APP_ID"], "client_secret": os.environ["TIKTOK_APP_SECRET"],
            "grant_type": "refresh_token", "refresh_token": g["refresh_token"]})
        d = r.get("data") or {}
        ocultar(d.get("access_token")); ocultar(d.get("refresh_token"))
        if not d.get("access_token"):
            sys.exit(f"TikTok no renovó el token: code={r.get('code')} · {r.get('message')}")
        self.token, self.bid = d["access_token"], d.get("open_id") or g.get("open_id")
        if d.get("refresh_token") and d["refresh_token"] != g.get("refresh_token"):
            cifrar(self.ARCHIVO, "TIKTOK_APP_SECRET", json.dumps({
                "refresh_token": d["refresh_token"], "open_id": self.bid, "guardado": AHORA,
                "refresh_expira_en_s": d.get("refresh_token_expires_in")}))
            print("TikTok: el refresh token cambió; se guarda cifrado.")

    def get(self, ruta, **q):
        return http(self.BASE + ruta + "?" + urllib.parse.urlencode(q), cabeceras={"Access-Token": self.token})

    def comentarios(self, video_id):
        r = self.get("/business/comment/list/", business_id=self.bid, video_id=video_id,
                     include_replies="true", max_count=30)
        if r.get("code") not in (0, None):
            print(f"  TikTok comment/list {video_id}: code={r.get('code')} · {str(r.get('message'))[:200]}")
        return (r.get("data") or {}).get("comments") or []

    def pendientes(self, dias):
        v = self.get("/business/video/list/", business_id=self.bid, max_count=20,
                     fields=json.dumps(["item_id", "create_time", "caption", "comments", "share_url"]))
        vids = (v.get("data") or {}).get("videos") or []
        print(f"TikTok: {len(vids)} videos leídos | code {v.get('code')} {v.get('message')}")
        pend, visto = [], False
        for x in vids:
            if not int(x.get("comments") or 0):
                continue
            cs = self.comentarios(x["item_id"])
            if cs and not visto:
                print("  campos de un comentario:", sorted(cs[0].keys())); visto = True
            for c in cs:
                hijos = c.get("reply_list") or []
                propio = c.get("owner") is True
                respondido = any(h.get("owner") is True for h in hijos)
                if propio or respondido or c.get("parent_comment_id") not in (None, "", "0", 0, c.get("comment_id")):
                    continue
                if AHORA - int(c.get("create_time") or 0) > dias * 86400:
                    continue
                pend.append(dict(red="tiktok", fecha=fecha(c.get("create_time") or 0),
                                 autor=c.get("display_name") or c.get("username") or "(sin nombre)",
                                 post=(x.get("caption") or x.get("share_url") or "").replace("\n", " "),
                                 texto=c.get("text") or "",
                                 ref=dict(video_id=x["item_id"], comment_id=c.get("comment_id"))))
        return pend

    def responder(self, ref, texto):
        r = http(self.BASE + "/business/comment/reply/create/", "POST", cabeceras={"Access-Token": self.token},
                 cuerpo={"business_id": self.bid, "video_id": ref["video_id"], "comment_id": ref["comment_id"], "text": texto[:150]})
        return r.get("code") == 0, f"code={r.get('code')} · {str(r.get('message'))[:200]}"

    @staticmethod
    def clave(ref):
        return ref.get("comment_id")


# ───────────────────────────── LinkedIn ─────────────────────────────
class LinkedIn:
    ARCHIVO = "matriz-viral/linkedin/token.enc"

    def __init__(self):
        if not os.environ.get("LINKEDIN_CLIENT_ID") or not os.environ.get("LINKEDIN_CLIENT_SECRET"):
            sys.exit("Faltan LINKEDIN_CLIENT_ID o LINKEDIN_CLIENT_SECRET.")
        g = descifrar(self.ARCHIVO, "LINKEDIN_CLIENT_SECRET")
        ocultar(g.get("access_token")); ocultar(g.get("refresh_token"))
        if int(g.get("access_expira") or 0) - AHORA < 5 * 86400 and g.get("refresh_token"):
            d = http("https://www.linkedin.com/oauth/v2/accessToken", "POST", forma={
                "grant_type": "refresh_token", "refresh_token": g["refresh_token"],
                "client_id": os.environ["LINKEDIN_CLIENT_ID"].strip(), "client_secret": os.environ["LINKEDIN_CLIENT_SECRET"].strip()})
            ocultar(d.get("access_token")); ocultar(d.get("refresh_token"))
            if not d.get("access_token"):
                sys.exit(f"LinkedIn no renovó el token: {d.get('error')} · {d.get('error_description')}")
            g.update(access_token=d["access_token"], access_expira=AHORA + int(d.get("expires_in") or 0), guardado=AHORA)
            if d.get("refresh_token"):
                g["refresh_token"] = d["refresh_token"]
            if d.get("refresh_token_expires_in"):
                g["refresh_expira"] = AHORA + int(d["refresh_token_expires_in"])
            cifrar(self.ARCHIVO, "LINKEDIN_CLIENT_SECRET", json.dumps(g))
            print("LinkedIn: token renovado; se guarda cifrado.")
        self.token = g["access_token"]
        print("LinkedIn: al token de acceso le quedan", round((int(g.get("access_expira") or 0) - AHORA) / 86400), "días")
        t = time.gmtime()
        for k in range(14):
            y, m = t.tm_year, t.tm_mon - k
            while m <= 0:
                y, m = y - 1, m + 12
            self.version = f"{y}{m:02d}"
            if self.api("/organizationAcls?q=roleAssignee&state=APPROVED").get("_http") != 426:
                break
        print("LinkedIn: versión de la API", self.version)

    def api(self, ruta, metodo="GET", cuerpo=None):
        return http("https://api.linkedin.com/rest" + ruta, metodo, cuerpo=cuerpo, cabeceras={
            "Authorization": f"Bearer {self.token}", "LinkedIn-Version": self.version, "X-Restli-Protocol-Version": "2.0.0"})

    @staticmethod
    def q(urn):
        return urllib.parse.quote(urn, safe="")

    def hilo(self, urn):
        r = self.api(f"/socialActions/{self.q(urn)}/comments?count=50")
        if r.get("_http", 200) >= 400:
            print(f"  LinkedIn comentarios {urn}: {r.get('_http')} · {str(r.get('message'))[:160]}")
        return r.get("elements") or []

    def pendientes(self, dias):
        pend = []
        for oid, nombre in ORGS.items():
            org = f"urn:li:organization:{oid}"
            r = self.api(f"/posts?author={self.q(org)}&q=author&count=20&sortBy=LAST_MODIFIED")
            posts = r.get("elements") or []
            print(f"LinkedIn · {nombre}: {len(posts)} publicaciones leídas | {r.get('_http')} {str(r.get('message') or '')[:160]}")
            for p in posts:
                urn = p.get("id")
                for c in self.hilo(urn):
                    curn = c.get("commentUrn") or c.get("$URN") or f"urn:li:comment:({c.get('object')},{c.get('id')})"
                    if c.get("actor") == org or c.get("parentComment"):
                        continue
                    if AHORA - int((c.get("created") or {}).get("time", 0)) / 1000 > dias * 86400:
                        continue
                    n = ((c.get("commentsSummary") or {}).get("aggregatedTotalComments") or 0)
                    if n and any(h.get("actor") == org for h in self.hilo(curn)):
                        continue
                    pend.append(dict(red="linkedin", fecha=fecha(int((c.get("created") or {}).get("time", 0)) / 1000),
                                     autor=c.get("actor", ""), post=f"{nombre} · " + (p.get("commentary") or "").replace("\n", " "),
                                     texto=(c.get("message") or {}).get("text") or "",
                                     ref=dict(org=oid, post=urn, object=c.get("object"), comment=curn)))
        return pend

    def responder(self, ref, texto):
        org = f"urn:li:organization:{ref['org']}"
        r = self.api(f"/socialActions/{self.q(ref['post'])}/comments", "POST", cuerpo={
            "actor": org, "object": ref.get("object") or ref["post"], "message": {"text": texto[:1250]},
            "parentComment": ref["comment"]})
        return r.get("_http") in (200, 201), f"{r.get('_http')} · {str(r.get('message') or '')[:200]}"

    @staticmethod
    def clave(ref):
        return ref.get("comment")


# ───────────────────────────── YouTube ─────────────────────────────
class YouTube:
    API = "https://www.googleapis.com/youtube/v3/"

    def __init__(self):
        faltan = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
        if faltan:
            sys.exit("Faltan secretos: " + ", ".join(faltan))
        r = http("https://oauth2.googleapis.com/token", "POST", forma=dict(
            client_id=os.environ["YT_CLIENT_ID"].strip(), client_secret=os.environ["YT_CLIENT_SECRET"].strip(),
            refresh_token=os.environ["YT_REFRESH_TOKEN"].strip(), grant_type="refresh_token"))
        ocultar(r.get("access_token"))
        if not r.get("access_token"):
            sys.exit(f"YouTube no dio acceso: {r.get('error')} · {r.get('error_description')}")
        self.token = r["access_token"]
        c = self.get("channels", part="id,snippet", mine="true")
        self.canal = c["items"][0]["id"]
        print("YouTube: canal", c["items"][0]["snippet"]["title"])

    def get(self, ruta, **q):
        return http(self.API + ruta + "?" + urllib.parse.urlencode(q), cabeceras={"Authorization": "Bearer " + self.token})

    def nuestro(self, com):
        return ((com.get("snippet") or {}).get("authorChannelId") or {}).get("value") == self.canal

    def pendientes(self, dias):
        pend, titulos, pag = [], {}, None
        limite = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(AHORA - dias * 86400))
        for _ in range(3):
            q = dict(part="snippet,replies", allThreadsRelatedToChannelId=self.canal, order="time", maxResults=100)
            if pag:
                q["pageToken"] = pag
            r = self.get("commentThreads", **q)
            if r.get("_http", 200) >= 400:
                print("  YouTube commentThreads:", r.get("_http"), str((r.get("error") or {}).get("message"))[:200]); break
            fin = False
            for t in r.get("items") or []:
                top = t["snippet"]["topLevelComment"]; s = top["snippet"]
                if s["publishedAt"] < limite:
                    fin = True; continue
                if self.nuestro(top):
                    continue
                hijos = (t.get("replies") or {}).get("comments") or []
                if t["snippet"].get("totalReplyCount", 0) > len(hijos):
                    hijos = self.get("comments", part="snippet", parentId=top["id"], maxResults=100).get("items") or []
                if any(self.nuestro(h) for h in hijos):
                    continue
                vid = s.get("videoId") or t["snippet"].get("videoId") or ""
                if vid and vid not in titulos:
                    v = self.get("videos", part="snippet", id=vid).get("items") or []
                    titulos[vid] = v[0]["snippet"]["title"] if v else vid
                pend.append(dict(red="youtube", fecha=s["publishedAt"][:16].replace("T", " "), autor=s.get("authorDisplayName", ""),
                                 post=titulos.get(vid, "(canal)"), texto=s.get("textOriginal") or s.get("textDisplay") or "",
                                 ref=dict(comment_id=top["id"], video_id=vid)))
            pag = r.get("nextPageToken")
            if fin or not pag:
                break
        return pend

    def responder(self, ref, texto):
        r = http(self.API + "comments?part=snippet", "POST", cabeceras={"Authorization": "Bearer " + self.token},
                 cuerpo={"snippet": {"parentId": ref["comment_id"], "textOriginal": texto}})
        return bool(r.get("id")), f"{r.get('_http')} · {str((r.get('error') or {}).get('message') or '')[:200]}"

    @staticmethod
    def clave(ref):
        return ref.get("comment_id")


def main():
    modo, dias, redes, respuestas = orden()
    if RED not in redes:
        print(f"{RED}: no está en la orden; no se hace nada."); return
    print(f"RED {RED} · MODO {modo} · {dias} días")
    api = {"tiktok": TikTok, "linkedin": LinkedIn, "youtube": YouTube}[RED]()
    if modo == "listar":
        mostrar(api.pendientes(dias)); return
    mias = [r for r in respuestas if r.get("red") == RED and r.get("texto") and r.get("ref")]
    if not mias:
        print(f"{RED}: la orden no trae respuestas para esta red."); return
    libres = {api.clave(p["ref"]) for p in api.pendientes(max(dias, 60))}
    hechas = 0
    for r in mias:
        k = api.clave(r["ref"])
        if k not in libres:
            print(f"  SALTADO {k}: ya tiene respuesta nuestra o no se encontró."); continue
        ok, nota = api.responder(r["ref"], r["texto"])
        hechas += ok
        print(f"  {'RESPONDIDO' if ok else 'FALLÓ'} {k} · {nota}")
        libres.discard(k); time.sleep(2)
    print(f"Respondidos {hechas} de {len(mias)} en {RED}")


if __name__ == "__main__":
    main()
