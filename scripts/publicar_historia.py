#!/usr/bin/env python3
"""Publica una historia en Instagram (@design_modeling_dg) y/o en la página de Facebook.

    python3 scripts/publicar_historia.py --url <URL pública .mp4/.jpg/.png> --red instagram|facebook|ambas \
        --modo previa|publicar [--huella XXXXXXXXXX] [--a-las 2026-11-04T09:30-05:00]

Dos pasos, igual que el envío a los grupos de WhatsApp:
  1. modo=previa   → NO publica. Baja el archivo, revisa formato (9:16, duración, códec) y
                     deja en el resumen qué se publicaría, dónde y su HUELLA.
  2. modo=publicar → solo con la misma huella (mismo archivo, misma red, misma hora) y después
                     del «sí» de Dayana. Si se da --a-las, espera hasta esa hora (máx. 5 h 50 min)
                     y publica.

Límite de Meta: por la API una historia sale SIN stickers (ni enlace, ni cuenta regresiva, ni
encuesta). Para el enlace se usa «Responde PALABRA» y la automatización de DM.

Usa META_TOKEN (System User «Design Modeling - Ads CLI»). El token nunca se imprime.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

BASE = "https://graph.facebook.com/v22.0"
IG_ID = os.environ.get("META_IG_ID", "17841404048578200")      # @design_modeling_dg
PAGE_ID = os.environ.get("META_PAGE_ID", "101355061550758")      # Design Modeling DG
TOKEN = os.environ.get("META_TOKEN", "").strip()
ECU = timezone(timedelta(hours=-5))
RESUMEN = os.environ.get("GITHUB_STEP_SUMMARY")
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def fecha_es(d):
    d = d.astimezone(ECU)
    return f"{DIAS[d.weekday()]} {d.day}-{MESES[d.month - 1]} {d:%H:%M} (Ecuador)"


def out(*lineas):
    txt = "\n".join(lineas)
    print(txt)
    if RESUMEN:
        with open(RESUMEN, "a", encoding="utf-8") as f:
            f.write(txt + "\n")


def http(method, url, data=None, headers=None, timeout=120):
    body = urllib.parse.urlencode(data).encode() if isinstance(data, dict) else data
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        raw = e.read()
    try:
        return json.loads(raw or b"{}")
    except ValueError:
        return {"raw": raw[:300].decode("utf-8", "replace")}


def graph(method, path, token, **params):
    params["access_token"] = token
    if method == "GET":
        return http("GET", f"{BASE}/{path}?" + urllib.parse.urlencode(params))
    return http("POST", f"{BASE}/{path}", data=params)


def err(d):
    e = d.get("error")
    return e.get("message", str(e)) if isinstance(e, dict) else (str(e) if e else "")


# ---------- revisión del archivo ----------
def revisar(url):
    tmp = tempfile.mkdtemp()
    ruta = os.path.join(tmp, "archivo")
    r = subprocess.run(["curl", "-sSL", "--fail", "-o", ruta, url], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"No se pudo bajar el archivo (¿la URL es pública?): {r.stderr.strip()[:200]}")
    sha = hashlib.sha256(open(ruta, "rb").read()).hexdigest()
    peso = os.path.getsize(ruta) / 1e6
    p = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", ruta],
                       capture_output=True, text=True)
    info = json.loads(p.stdout or "{}")
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    fmt = info.get("format", {}).get("format_name", "")
    es_video = bool(v) and not any(x in fmt for x in ("png", "jpeg", "image2", "webp"))
    dur = float(info.get("format", {}).get("duration") or 0) if es_video else 0
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    avisos = []
    if not w:
        sys.exit("El archivo no es un video ni una imagen que se pueda leer.")
    if abs(w / h - 9 / 16) > 0.02:
        avisos.append(f"No es 9:16 ({w}×{h}): Instagram lo recorta o le pone bandas.")
    if es_video:
        if dur < 3 or dur > 60:
            avisos.append(f"Dura {dur:.1f} s: Instagram acepta historias de 3 a 60 s.")
        if v.get("codec_name") != "h264":
            avisos.append(f"Códec {v.get('codec_name')}: conviene H.264.")
        if a is None:
            avisos.append("No tiene audio (se publica igual).")
        if peso > 100:
            avisos.append(f"Pesa {peso:.0f} MB: el máximo es 100 MB.")
    elif peso > 8:
        avisos.append(f"La imagen pesa {peso:.1f} MB: el máximo es 8 MB.")
    return {"sha": sha, "es_video": es_video, "dur": dur, "w": w, "h": h, "peso": peso, "avisos": avisos}


def huella(url, red, a_las, sha):
    return hashlib.sha256(f"{url}|{red}|{a_las or ''}|{sha}".encode()).hexdigest()[:10]


# ---------- Instagram ----------
def publicar_ig(url, es_video):
    campo = "video_url" if es_video else "image_url"
    c = graph("POST", f"{IG_ID}/media", TOKEN, media_type="STORIES", **{campo: url})
    if err(c):
        return f"Instagram: no se creó la historia — {err(c)}"
    cid = c["id"]
    for _ in range(60):                      # hasta ~10 min de procesado
        s = graph("GET", cid, TOKEN, fields="status_code,status")
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") in ("ERROR", "EXPIRED"):
            return f"Instagram: Meta no pudo procesar el archivo — {s.get('status')}"
        time.sleep(10)
    else:
        return "Instagram: Meta tardó más de 10 min en procesar el archivo; no se publicó."
    p = graph("POST", f"{IG_ID}/media_publish", TOKEN, creation_id=cid)
    if err(p):
        return f"Instagram: no se publicó — {err(p)}"
    return f"Instagram: publicada ✅ (id {p.get('id')})"


# ---------- Facebook (página) ----------
def publicar_fb(url, es_video):
    pt = graph("GET", PAGE_ID, TOKEN, fields="access_token").get("access_token")
    if not pt:
        return "Facebook: no se obtuvo el token de la página."
    if es_video:
        ini = graph("POST", f"{PAGE_ID}/video_stories", pt, upload_phase="start")
        if err(ini):
            return f"Facebook: no se inició la subida — {err(ini)}"
        up = http("POST", ini["upload_url"], data=b"", headers={"Authorization": f"OAuth {pt}", "file_url": url})
        if not up.get("success"):
            return f"Facebook: falló la subida del video — {json.dumps(up)[:200]}"
        fin = graph("POST", f"{PAGE_ID}/video_stories", pt, upload_phase="finish", video_id=ini["video_id"])
        if err(fin) or not fin.get("success", True):
            return f"Facebook: no se publicó — {err(fin) or json.dumps(fin)[:200]}"
        return f"Facebook: publicada ✅ (video {ini['video_id']})"
    foto = graph("POST", f"{PAGE_ID}/photos", pt, url=url, published="false")
    if err(foto):
        return f"Facebook: no se subió la imagen — {err(foto)}"
    st = graph("POST", f"{PAGE_ID}/photo_stories", pt, photo_id=foto["id"])
    if err(st):
        return f"Facebook: no se publicó — {err(st)}"
    return f"Facebook: publicada ✅ (post {st.get('post_id', '')})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--red", choices=["instagram", "facebook", "ambas"], default="instagram")
    ap.add_argument("--modo", choices=["previa", "publicar"], default="previa")
    ap.add_argument("--huella", default="")
    ap.add_argument("--a-las", default="", help="Hora de publicación, ISO con zona (p. ej. 2026-11-04T09:30-05:00)")
    a = ap.parse_args()
    if not TOKEN:
        sys.exit("Falta META_TOKEN.")
    if not a.url.startswith("https://"):
        sys.exit("La URL tiene que ser pública y empezar por https://")

    cuando = None
    if a.a_las:
        cuando = datetime.fromisoformat(a.a_las)
        if cuando.tzinfo is None:
            cuando = cuando.replace(tzinfo=ECU)

    r = revisar(a.url)
    h = huella(a.url, a.red, a.a_las, r["sha"])
    tipo = f"video de {r['dur']:.1f} s" if r["es_video"] else "imagen"
    destino = {"instagram": "Instagram @design_modeling_dg", "facebook": "página de Facebook Design Modeling DG",
               "ambas": "Instagram @design_modeling_dg y página de Facebook"}[a.red]
    out(f"## Historia · {a.modo}", "",
        f"- **Archivo:** {a.url}", f"- **Qué es:** {tipo}, {r['w']}×{r['h']}, {r['peso']:.1f} MB",
        f"- **Dónde:** {destino}",
        f"- **Cuándo:** {fecha_es(cuando) if cuando else 'en cuanto se corra'}",
        "- **Sin stickers** (la API de Meta no los permite).")
    for av in r["avisos"]:
        out(f"- ⚠ {av}")

    if a.modo == "previa":
        out("", f"**HUELLA: `{h}`** — para publicar, correr de nuevo con modo=publicar y esta huella "
                "(mismo archivo, misma red y misma hora).")
        return

    if a.huella != h:
        sys.exit(f"La huella no coincide (dada «{a.huella}», calculada «{h}»): algo cambió desde la previa. "
                 "No se publica; hay que hacer otra previa.")
    if cuando:
        espera = (cuando - datetime.now(timezone.utc)).total_seconds()
        if espera > 5 * 3600 + 50 * 60:
            sys.exit("La hora queda a más de 5 h 50 min: GitHub no espera tanto. Se programa más cerca de la hora.")
        if espera > 0:
            out(f"", f"Esperando {espera / 60:.0f} min hasta la hora indicada…")
            time.sleep(espera)

    out("")
    if a.red in ("instagram", "ambas"):
        out("- " + publicar_ig(a.url, r["es_video"]))
    if a.red in ("facebook", "ambas"):
        out("- " + publicar_fb(a.url, r["es_video"]))


if __name__ == "__main__":
    main()
