#!/usr/bin/env python3
"""Referentes por la Graph API oficial (business_discovery), sin Apify.

    python3 scripts/referentes_meta.py matriz-viral/pedidos/referentes-meta.json

Plan B cuando Apify no está disponible (p. ej. «Monthly usage hard limit
exceeded»). Gratis. Lee datos PÚBLICOS de cuentas business/creator: seguidores,
y por publicación caption, likes, comentarios, tipo, fecha, enlace y —si Meta
lo entrega— vistas. Para los reels pedidos en «transcribir» baja el video
desde media_url (o yt-dlp como respaldo), mide la edición con ffmpeg y lo
transcribe con faster-whisper (transcripción automática, marcada como tal).
No se guarda ningún video ni imagen de terceros en el repo; los fotogramas
van a un artefacto temporal de la Action.

Pedido: {"cuentas": [...], "por_cuenta": 50, "reel": "<url>",
         "transcribir_top": 4, "respaldo_video": ["<url tiktok>"]}
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

R = pathlib.Path(__file__).resolve().parent.parent
SAL = R / "matriz-viral" / "fuentes" / "referentes"
FRAMES = pathlib.Path(os.environ.get("FRAMES_DIR", "/tmp/frames"))
BASE = "https://graph.facebook.com/v20.0"
TOKEN = os.environ.get("META_TOKEN", "").strip()
IG_ID = os.environ.get("META_IG_ID", "17841404048578200")
CAMPOS = "id,caption,like_count,comments_count,timestamp,media_type,media_product_type,permalink,media_url"


def api(**params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{IG_ID}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode())
    except Exception as e:  # noqa: BLE001
        body = e.read().decode()[:300] if hasattr(e, "read") else ""
        return {"error": {"message": f"{e} {body}"}}


def cuenta(u, n):
    for extra in (",view_count", ""):
        d = api(fields=(f"business_discovery.username({u}){{username,name,biography,followers_count,media_count,"
                        f"media.limit({n}){{{CAMPOS}{extra}}}}}"))
        if "error" not in d:
            return d.get("business_discovery"), bool(extra)
        print(f"  @{u} ({'con' if extra else 'sin'} view_count): {d['error']['message'][:200]}")
    return None, False


def bajar(url, destino):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(destino, "wb") as f:
            f.write(r.read())
        return os.path.getsize(destino) > 10000
    except Exception as e:  # noqa: BLE001
        print(f"  no se pudo bajar: {e}")
        return False


def bajar_ytdlp(url, destino):
    try:
        r = subprocess.run(["yt-dlp", "-q", "-f", "mp4/best", "-o", destino, url], capture_output=True,
                           text=True, timeout=240)
        if r.returncode:
            print(f"  yt-dlp {url}: {r.stderr[-300:]}")
        return r.returncode == 0 and os.path.exists(destino)
    except Exception as e:  # noqa: BLE001
        print(f"  yt-dlp falló: {e}")
        return False


def edicion(path):
    try:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    path], capture_output=True, text=True, timeout=60).stdout.strip())
        out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-filter:v", "select='gt(scene,0.30)',showinfo",
                              "-f", "null", "-"], capture_output=True, text=True, timeout=300).stderr
        cortes = [round(float(m), 2) for m in re.findall(r"pts_time:([0-9.]+)", out)]
        return {"duracion_s": round(dur, 1), "cortes": len(cortes), "tiempos_de_corte_s": cortes,
                "cortes_por_10s": round(len(cortes) / dur * 10, 1) if dur else None,
                "primer_corte_s": cortes[0] if cortes else None,
                "cortes_primeros_3s": sum(1 for c in cortes if c <= 3)}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


def fotogramas(path, codigo):
    d = FRAMES / codigo
    d.mkdir(parents=True, exist_ok=True)
    # 1 fotograma por segundo (para leer texto en pantalla y estructura).
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-vf", "fps=1,scale=360:-2",
                    str(d / "s%03d.jpg")], timeout=300)


_modelo = None


def transcribir(path):
    global _modelo
    try:
        from faster_whisper import WhisperModel
        if _modelo is None:
            _modelo = WhisperModel("small", device="cpu", compute_type="int8")
        segs, info = _modelo.transcribe(path, language="es", vad_filter=False)
        segs = [{"ini": round(s.start, 1), "fin": round(s.end, 1), "texto": s.text.strip()} for s in segs]
        return {"motor": "faster-whisper small (automática, revisar)", "idioma": info.language,
                "texto": " ".join(s["texto"] for s in segs), "segmentos": segs}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


def analizar_video(p, respaldos, codigo):
    v = f"/tmp/{codigo}.mp4"
    ok = bool(p.get("media_url")) and bajar(p["media_url"], v)
    origen = "media_url (Graph API)" if ok else None
    for u in ([p.get("permalink")] if not ok else []) + (respaldos if not ok else []):
        if u and bajar_ytdlp(u, v):
            ok, origen = True, f"yt-dlp {u}"
            break
    if not ok:
        return {"video": "s/d (no se pudo bajar)"}
    fotogramas(v, codigo)
    return {"video_origen": origen, "edicion": edicion(v), "transcripcion": transcribir(v)}


def main():
    if not TOKEN:
        print("Sin META_TOKEN: no se corre nada.")
        return
    pedido = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    n = min(int(pedido.get("por_cuenta", 50)), 50)
    reel = (pedido.get("reel") or "").rstrip("/").split("?")[0]
    cod_reel = reel.split("/")[-1] if reel else None
    top_n = int(pedido.get("transcribir_top", 3))
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    SAL.mkdir(parents=True, exist_ok=True)
    for u in pedido.get("cuentas", []):
        b, con_vistas = cuenta(u, n)
        if not b:
            print(f"@{u}: sin datos (no es business/creator, no existe o error). No se escribe nada.")
            continue
        media = []
        for m in (b.get("media", {}).get("data") or []):
            cod = (m.get("permalink") or "").rstrip("/").split("/")[-1]
            media.append({"codigo": cod, "url": m.get("permalink"), "fecha": m.get("timestamp"),
                          "tipo": m.get("media_type"), "producto": m.get("media_product_type"),
                          "texto": m.get("caption"), "likes": m.get("like_count"),
                          "comentarios": m.get("comments_count"), "vistas": m.get("view_count"),
                          "_media_url": m.get("media_url")})
        for m in media:
            m["engagement"] = (m["likes"] or 0) + (m["comentarios"] or 0)
        videos = sorted([m for m in media if m["tipo"] == "VIDEO"], key=lambda m: -m["engagement"])
        elegir = [m for m in videos[:top_n]]
        objetivo = next((m for m in media if cod_reel and m["codigo"] == cod_reel), None)
        if objetivo and objetivo not in elegir:
            elegir.insert(0, objetivo)
        for m in elegir:
            print(f"  analizando {m['codigo']} …")
            resp = pedido.get("respaldo_video", []) if m is objetivo else []
            m["analisis_video"] = analizar_video({"media_url": m["_media_url"], "permalink": m["url"]}, resp,
                                                 m["codigo"])
        for m in media:
            m.pop("_media_url", None)
        salida = {"traido": ahora, "fuente": "Meta Graph API · business_discovery (datos públicos)",
                  "motivo": pedido.get("motivo"), "cuenta": b.get("username"), "nombre": b.get("name"),
                  "bio": b.get("biography"), "seguidores": b.get("followers_count"),
                  "publicaciones_totales": b.get("media_count"), "vistas_disponibles": con_vistas,
                  "reel_objetivo_encontrado": bool(objetivo) if cod_reel else None,
                  "nota": "Meta no entrega guardados, compartidos ni alcance de cuentas ajenas. "
                          "Transcripciones automáticas (faster-whisper): revisar antes de citar literal.",
                  "media": media}
        f = SAL / f"meta-{u}.json"
        f.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"ok → {f.relative_to(R)} · {len(media)} publicaciones · vistas={con_vistas} · "
              f"objetivo={'sí' if objetivo else 'no'}")
    # Si el reel objetivo no salió en ninguna cuenta, se intenta igual por los respaldos.
    if cod_reel and not any((SAL / f"meta-{u}.json").exists() and json.loads(
            (SAL / f"meta-{u}.json").read_text())["reel_objetivo_encontrado"] for u in pedido.get("cuentas", [])):
        a = analizar_video({"media_url": None, "permalink": reel}, pedido.get("respaldo_video", []), cod_reel)
        (SAL / f"video-{cod_reel}.json").write_text(json.dumps({"traido": ahora, "url": reel, **a},
                                                               ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"reel objetivo por respaldo → video-{cod_reel}.json")


if __name__ == "__main__":
    main()
