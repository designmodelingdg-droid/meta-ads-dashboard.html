#!/usr/bin/env python3
"""Qué edición gana en el nicho BIM + IA: reels, shorts, TikTok y anuncios que corren hace semanas.

    python3 scripts/edicion_ganadora.py matriz-viral/pedidos/edicion-ganadora.json

Para qué existe: Dayana quiere saber qué FORMATO y qué EDICIÓN funcionan en el
nicho (no solo en la competencia directa, que vende menos que DMA) para editar
mejor sus anuncios y sus videos de valor. Las páginas de etiqueta de Instagram
no traen reels ni vistas (comprobado el 26-ago), así que el nicho se busca por
PALABRA en TikTok y YouTube Shorts, por cuentas en Instagram y por palabra en la
Biblioteca de Anuncios de Meta.

Disciplina de gasto (es dinero de Dayana):
  - cada actor corre con `maxTotalChargeUsd` = su tope en el pedido; la suma de
    topes no puede pasar de `tope_total_usd` (si pasa, no corre nada);
  - solo contenido PÚBLICO.

Qué guarda (matriz-viral/fuentes/edicion-ganadora/datos-<fecha>.json):
  métricas públicas, texto, transcripción si la hay, URL del video (caducan),
  y para los mejores de cada fuente un análisis de edición hecho con ffmpeg
  (duración, cortes, cortes por segundo, segundo del primer corte). No se suben
  videos ni imágenes de terceros al repositorio.
Si una fuente falla, se anota el error y se sigue: vacío antes que inventado.
"""
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()
R = pathlib.Path(__file__).resolve().parent.parent
SAL = R / "matriz-viral" / "fuentes" / "edicion-ganadora"
API = "https://api.apify.com/v2"
HOY = datetime.now(timezone.utc)


def http(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def correr(actor, entrada, tope, espera_max=1200):
    """Lanza el actor en asíncrono (los run-sync cortan a los 300 s) y trae su dataset."""
    try:
        run = http(f"{API}/acts/{actor}/runs?token={TOKEN}&maxTotalChargeUsd={tope}",
                   {**entrada, "maxTotalChargeUsd": tope})["data"]
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} al lanzar: {e.read().decode()[:200]}"
    except Exception as e:  # noqa: BLE001
        return None, f"no se pudo lanzar: {e}"
    rid, t0 = run["id"], time.time()
    estado = run.get("status")
    while estado in ("READY", "RUNNING") and time.time() - t0 < espera_max:
        time.sleep(15)
        try:
            run = http(f"{API}/actor-runs/{rid}?token={TOKEN}")["data"]
            estado = run.get("status")
        except Exception:  # noqa: BLE001
            pass
    costo = run.get("usageTotalUsd")
    try:
        items = http(f"{API}/datasets/{run['defaultDatasetId']}/items?token={TOKEN}&clean=true", timeout=120)
    except Exception as e:  # noqa: BLE001
        return None, f"estado {estado}; no se pudo leer el dataset: {e}"
    return {"items": items, "estado": estado, "costo_usd": costo, "kv": run.get("defaultKeyValueStoreId")}, None


def num(*vals):
    for v in vals:
        if isinstance(v, (int, float)) and v >= 0:
            return v
    return None


def g(d, *ruta):
    for k in ruta:
        if isinstance(d, dict):
            d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and len(d) > k:
            d = d[k]
        else:
            return None
    return d


# ───────────────── normalizar cada fuente a una misma forma ─────────────────
def de_instagram(it):
    return {"fuente": "instagram", "cuenta": it.get("ownerUsername"), "url": it.get("url"),
            "fecha": it.get("timestamp"), "texto": (it.get("caption") or "")[:1500],
            "vistas": num(it.get("videoPlayCount"), it.get("videoViewCount")),
            "likes": num(it.get("likesCount")), "comentarios": num(it.get("commentsCount")),
            "duracion_s": num(it.get("videoDuration")), "transcripcion": it.get("transcript"),
            "video": it.get("videoUrl")}


def de_tiktok(it):
    medias = it.get("mediaUrls") or []
    return {"fuente": "tiktok", "cuenta": g(it, "authorMeta", "name"), "seguidores": num(g(it, "authorMeta", "fans")),
            "url": it.get("webVideoUrl"), "fecha": it.get("createTimeISO"), "texto": (it.get("text") or "")[:1500],
            "vistas": num(it.get("playCount")), "likes": num(it.get("diggCount")),
            "comentarios": num(it.get("commentCount")), "compartidos": num(it.get("shareCount")),
            "guardados": num(it.get("collectCount")), "duracion_s": num(g(it, "videoMeta", "duration")),
            "busqueda": it.get("searchQuery"), "video": medias[0] if medias else None,
            "subtitulos": [s.get("downloadLink") for s in (g(it, "videoMeta", "subtitleLinks") or []) if isinstance(s, dict)][:2]}


def segundos(txt):
    if isinstance(txt, (int, float)):
        return txt
    if not isinstance(txt, str):
        return None
    try:
        partes = [int(p) for p in txt.split(":")]
    except ValueError:
        return None
    s = 0
    for p in partes:
        s = s * 60 + p
    return s


def de_youtube(it):
    return {"fuente": "youtube_shorts", "cuenta": it.get("channelName"), "seguidores": num(it.get("numberOfSubscribers")),
            "url": it.get("url"), "fecha": it.get("date"), "texto": ((it.get("title") or "") + "\n" + (it.get("text") or ""))[:1500],
            "vistas": num(it.get("viewCount")), "likes": num(it.get("likes")), "comentarios": num(it.get("commentsCount")),
            "duracion_s": segundos(it.get("duration")), "busqueda": it.get("fromYTUrl") or it.get("input"),
            "video": None}


def de_anuncio(it):
    snap = it.get("snapshot") or {}
    vids = snap.get("videos") or []
    if not vids:
        for c in snap.get("cards") or []:
            if c.get("videoHdUrl") or c.get("videoSdUrl"):
                vids = [c]
                break
    v = vids[0] if vids else {}
    ini = it.get("startDate") or it.get("start_date")
    dias = None
    if isinstance(ini, (int, float)):
        dias = round((HOY.timestamp() - ini) / 86400)
    elif isinstance(ini, str):
        try:
            dias = (HOY - datetime.fromisoformat(ini.replace("Z", "+00:00"))).days
        except ValueError:
            pass
    cuerpo = g(snap, "body", "text") or ""
    return {"fuente": "anuncio_meta", "cuenta": it.get("pageName") or snap.get("pageName"),
            "url": f"https://www.facebook.com/ads/library/?id={it.get('adArchiveID') or it.get('adArchiveId')}",
            "activo": it.get("isActive"), "dias_activo": dias, "variantes": num(it.get("collationCount")),
            "texto": cuerpo[:1500], "titular": snap.get("title"), "boton": snap.get("ctaText"),
            "plataformas": it.get("publisherPlatform"), "busqueda": it.get("url") or it.get("inputUrl"),
            "video": v.get("videoHdUrl") or v.get("videoSdUrl"), "es_video": bool(v)}


# ───────────────── análisis de edición con ffmpeg ─────────────────
def bajar(url, destino):
    if not url:
        return False
    if url.startswith(API):
        url += ("&" if "?" in url else "?") + f"token={TOKEN}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as r, open(destino, "wb") as f:
            f.write(r.read())
        return os.path.getsize(destino) > 10000
    except Exception:  # noqa: BLE001
        return False


def bajar_youtube(url, destino):
    try:
        r = subprocess.run(["yt-dlp", "-q", "-f", "mp4[height<=720]/best[height<=720]/best", "-o", destino, url],
                           capture_output=True, timeout=180)
        return r.returncode == 0 and os.path.exists(destino)
    except Exception:  # noqa: BLE001
        return False


def editar(path):
    """Duración, número de cortes (cambios de plano), cortes por segundo y segundo del primer corte."""
    try:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                   capture_output=True, text=True, timeout=60).stdout.strip())
        out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-filter:v", "select='gt(scene,0.30)',showinfo",
                              "-f", "null", "-"], capture_output=True, text=True, timeout=300).stderr
        cortes = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out)]
        tiene_audio = "Audio:" in subprocess.run(["ffprobe", "-hide_banner", path], capture_output=True, text=True,
                                                  timeout=60).stderr
        return {"duracion_s": round(dur, 1), "cortes": len(cortes),
                "cortes_por_10s": round(len(cortes) / dur * 10, 1) if dur else None,
                "seg_medio_por_plano": round(dur / (len(cortes) + 1), 1) if dur else None,
                "primer_corte_s": round(cortes[0], 1) if cortes else None,
                "cortes_primeros_3s": sum(1 for c in cortes if c <= 3), "audio": tiene_audio}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:120]}


def main():
    if not TOKEN:
        print("Sin APIFY_TOKEN: no se hace nada.")
        return 0
    ped = json.loads(pathlib.Path(sys.argv[1]).read_text())
    topes = ped["topes_usd"]
    if sum(topes.values()) > ped["tope_total_usd"] + 1e-9:
        print("La suma de topes pasa del tope total. No se corre nada.")
        return 1
    salida = {"generado": HOY.strftime("%Y-%m-%dT%H:%MZ"), "motivo": ped.get("motivo"), "pedido": ped,
              "fuentes": {}, "piezas": []}

    tareas = [
        ("instagram", "apify~instagram-reel-scraper",
         {"username": ped["cuentas_instagram"], "resultsLimit": ped["por_cuenta"], "includeTranscript": True}, de_instagram),
        ("tiktok", "clockworks~tiktok-scraper",
         {"searchQueries": ped["busquedas_tiktok"], "resultsPerPage": ped["por_busqueda"], "searchSection": "/video",
          "shouldDownloadVideos": True, "shouldDownloadCovers": False, "shouldDownloadSubtitles": True,
          "shouldDownloadSlideshowImages": False}, de_tiktok),
        ("youtube_shorts", "streamers~youtube-scraper",
         {"searchQueries": ped["busquedas_youtube"], "maxResults": 0, "maxResultsShorts": ped["por_busqueda"],
          "maxResultStreams": 0, "sortingOrder": "views", "downloadSubtitles": True}, de_youtube),
        ("anuncio_meta", "apify~facebook-ads-scraper",
         {"startUrls": [{"url": u} for u in ped["biblioteca_anuncios"]], "resultsLimit": ped["anuncios_por_busqueda"],
          "activeStatus": "active"}, de_anuncio),
    ]
    for nombre, actor, entrada, norm in tareas:
        tope = topes.get(nombre, 0)
        if not tope:
            continue
        print(f"→ {nombre} ({actor}) · tope ${tope}")
        res, err = correr(actor, entrada, tope)
        if err:
            print("  ", err)
            salida["fuentes"][nombre] = {"error": err, "tope_usd": tope}
            continue
        piezas = []
        for it in res["items"]:
            if not isinstance(it, dict) or it.get("error"):
                continue
            try:
                piezas.append(norm(it))
            except Exception as e:  # noqa: BLE001
                print("   item raro:", str(e)[:80])
        salida["fuentes"][nombre] = {"estado": res["estado"], "costo_usd": res["costo_usd"], "items": len(res["items"]),
                                     "piezas": len(piezas), "tope_usd": tope}
        print(f"   {res['estado']} · {len(piezas)} piezas · ${res['costo_usd']}")
        salida["piezas"].extend(piezas)

    # sin duplicados (el mismo video puede salir en dos búsquedas)
    vistos, unicas = set(), []
    for p in salida["piezas"]:
        k = p.get("url")
        if k and k in vistos:
            continue
        vistos.add(k)
        unicas.append(p)
    salida["piezas"] = unicas

    # «se sale de su cuenta»: vistas contra la mediana de las vistas de esa misma cuenta en la muestra
    por_cuenta = {}
    for p in unicas:
        if p.get("vistas") is not None and p.get("cuenta"):
            por_cuenta.setdefault((p["fuente"], p["cuenta"]), []).append(p["vistas"])
    for p in unicas:
        vs = por_cuenta.get((p["fuente"], p.get("cuenta")))
        if vs and len(vs) >= 3 and p.get("vistas") is not None:
            med = statistics.median(vs)
            p["veces_su_mediana"] = round(p["vistas"] / med, 1) if med else None
        if p.get("vistas") and p.get("seguidores"):
            p["vistas_por_seguidor"] = round(p["vistas"] / p["seguidores"], 2)
        if p.get("vistas") and p.get("comentarios") is not None:
            p["comentarios_por_1000"] = round(p["comentarios"] / p["vistas"] * 1000, 2)

    # los mejores de cada fuente, para analizar la edición
    n = ped.get("analizar_por_fuente", 10)
    elegidos = []
    for f, clave in (("instagram", "veces_su_mediana"), ("tiktok", "vistas"), ("youtube_shorts", "vistas"),
                     ("anuncio_meta", "dias_activo")):
        grupo = [p for p in unicas if p["fuente"] == f and (f != "anuncio_meta" or p.get("es_video"))]
        grupo.sort(key=lambda p: (p.get(clave) or 0, p.get("vistas") or 0), reverse=True)
        for p in grupo[:n]:
            p["elegido_para_analisis"] = True
            elegidos.append(p)
    with tempfile.TemporaryDirectory() as tmp:
        for k, p in enumerate(elegidos):
            dest = os.path.join(tmp, f"v{k}.mp4")
            ok = bajar_youtube(p["url"], dest) if p["fuente"] == "youtube_shorts" else bajar(p.get("video"), dest)
            p["edicion"] = editar(dest) if ok else {"error": "no se pudo bajar el video"}
            print(f"   edición {p['fuente']} · {p.get('cuenta')} · {p['edicion']}")

    SAL.mkdir(parents=True, exist_ok=True)
    out = SAL / f"datos-{HOY.strftime('%Y-%m-%d')}.json"
    out.write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n")
    gastado = sum((v.get("costo_usd") or 0) for v in salida["fuentes"].values())
    print(f"OK → {out} · {len(unicas)} piezas · gastado ≈ ${gastado:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
