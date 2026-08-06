#!/usr/bin/env python3
"""
Descarga las imágenes de los anuncios ganadores de la cuenta publicitaria
(act_1159622151150228) para la presentación de cierre/apertura de mes.

- Consulta insights a nivel de anuncio en la ventana pedida, cuenta leads
  (lead + mensajes de WhatsApp iniciados) y rankea.
- Baja la imagen del creativo (image_url si existe; si no, thumbnail en alta)
  de los TOP_N anuncios a matriz-viral/fuentes/ads-creativos/.
- Escribe manifest.json con nombre, campaña, gasto, leads, CPL y CTR de cada uno.
- Defensivo: si la API falla, sale con código 0 sin escribir nada a medias.

Uso:  META_TOKEN=EAA... python3 scripts/ads_creativos.py
Vars: DESDE (def. 2026-07-05), HASTA (def. 2026-08-05), TOP_N (def. 6)
"""
import os, sys, json, urllib.request, urllib.parse, urllib.error, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "matriz-viral", "fuentes", "ads-creativos")
BASE = "https://graph.facebook.com/v20.0"
CUENTA = "act_1159622151150228"

TOKEN = os.environ.get("META_TOKEN", "").strip()
DESDE = os.environ.get("DESDE", "2026-07-05")
HASTA = os.environ.get("HASTA", "2026-08-05")
TOP_N = int(os.environ.get("TOP_N", "6"))

LEAD_TYPES = {"lead", "onsite_conversion.lead_grouped",
              "onsite_conversion.messaging_conversation_started_7d"}


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def slug(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:40] or "anuncio"


def leads_de(row):
    return sum(int(a.get("value", 0)) for a in row.get("actions", [])
               if a.get("action_type") in LEAD_TYPES)


def main():
    if not TOKEN:
        print("ERROR: falta META_TOKEN en el entorno."); sys.exit(1)

    try:
        ins = api(f"{CUENTA}/insights", level="ad",
                  fields="ad_id,ad_name,campaign_name,spend,ctr,actions",
                  time_range=json.dumps({"since": DESDE, "until": HASTA}),
                  limit="300")
    except urllib.error.HTTPError as e:
        print(f"AVISO: insights falló ({e.code}): {e.read()[:400]}"); sys.exit(0)

    filas = ins.get("data", [])
    for f in filas:
        f["leads"] = leads_de(f)
    filas.sort(key=lambda f: (-f["leads"], -float(f.get("spend") or 0)))
    top = [f for f in filas if f["leads"] > 0][:TOP_N]
    if not top:
        print("AVISO: la ventana no devolvió anuncios con leads."); sys.exit(0)

    os.makedirs(OUTDIR, exist_ok=True)
    manifest = []
    for i, f in enumerate(top, 1):
        nombre, gasto, leads = f.get("ad_name", ""), float(f.get("spend") or 0), f["leads"]
        img_url = ""
        try:
            ad = api(f['ad_id'],
                     fields="creative{id,image_url,thumbnail_url,object_story_spec,video_id}")
            cr = ad.get("creative", {})
            img_url = cr.get("image_url") or ""
            # Anuncio de video: el thumbnail escalado sale borroso; ir al video
            # y pedir sus thumbnails reales, quedándose con el preferido/más grande.
            vid = (cr.get("video_id")
                   or cr.get("object_story_spec", {}).get("video_data", {}).get("video_id"))
            if not img_url and vid:
                try:
                    th = api(f"{vid}/thumbnails", fields="uri,width,is_preferred")
                    cands = th.get("data", [])
                    if cands:
                        cands.sort(key=lambda t: (not t.get("is_preferred"),
                                                  -(t.get("width") or 0)))
                        img_url = cands[0].get("uri") or ""
                except urllib.error.HTTPError as e:
                    print(f"  aviso: thumbnails del video de '{nombre}' falló ({e.code})")
            if not img_url and cr.get("id"):
                cr2 = api(cr["id"], fields="thumbnail_url",
                          thumbnail_width="1080", thumbnail_height="1080")
                img_url = cr2.get("thumbnail_url") or cr.get("thumbnail_url") or ""
        except urllib.error.HTTPError as e:
            print(f"  aviso: creativo de '{nombre}' falló ({e.code})")

        archivo = ""
        if img_url:
            archivo = f"{i:02d}-{slug(nombre)}.jpg"
            try:
                urllib.request.urlretrieve(img_url, os.path.join(OUTDIR, archivo))
                print(f"  ✓ {archivo}  ({leads} leads · ${gasto:.2f})")
            except Exception as e:
                print(f"  aviso: descarga de '{nombre}' falló: {e}"); archivo = ""

        manifest.append({
            "rank": i, "anuncio": nombre, "campana": f.get("campaign_name", ""),
            "leads": leads, "gasto": round(gasto, 2),
            "cpl": round(gasto / leads, 2) if leads else None,
            "ctr": f.get("ctr"), "archivo": archivo,
        })

    with open(os.path.join(OUTDIR, "manifest.json"), "w") as fh:
        json.dump({"desde": DESDE, "hasta": HASTA, "anuncios": manifest}, fh,
                  ensure_ascii=False, indent=2)
    print(f"Listo: {len(manifest)} anuncios en {OUTDIR}")


if __name__ == "__main__":
    main()
