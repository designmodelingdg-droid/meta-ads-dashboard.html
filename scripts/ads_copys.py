#!/usr/bin/env python3
"""
Baja TODOS los anuncios con gasto de la cuenta publicitaria, con su copy
COMPLETO Y LITERAL y sus números, y lo deja en un JSON del repositorio.

Por qué existe, habiendo ya `ads_creativos.py`: ese script pide
`object_story_spec` —que es donde vive el texto del anuncio— y lo TIRA. Se
queda solo con la imagen para la presentación de cierre. Para revisar copys
hace falta el texto, y hasta ahora había que copiarlo a mano de Ads Manager,
uno por uno.

Usa el mismo token de System User que el resto («Design Modeling - Ads CLI»,
no expira), leído de META_TOKEN. El token vive en los secretos del
repositorio: este script NUNCA lo imprime ni lo escribe en ninguna parte.

Uso:  META_TOKEN=... python3 scripts/ads_copys.py
Vars: DESDE (def. hace 30 días), HASTA (def. ayer), MIN_GASTO (def. 0.5)

Por qué HASTA es AYER por defecto: un día sin cerrar da cifras cortas. Es el
mismo error que se le señaló a la agencia el 3-ago-2026.

Nunca inventa: el campo que Meta no devuelve queda vacío, no se rellena.
"""
import datetime, json, os, sys, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "matriz-viral", "fuentes", "ads-copys")
BASE = "https://graph.facebook.com/v21.0"
CUENTA = "act_1159622151150228"

TOKEN = os.environ.get("META_TOKEN", "").strip()
_hoy = datetime.date.today()
DESDE = os.environ.get("DESDE") or str(_hoy - datetime.timedelta(days=31))
HASTA = os.environ.get("HASTA") or str(_hoy - datetime.timedelta(days=1))
MIN_GASTO = float(os.environ.get("MIN_GASTO") or "0.5")

# Un «resultado» no es lo mismo en todas las campañas: las de formulario dan
# leads y las de WhatsApp dan conversaciones. Se cuentan por separado y el
# JSON dice cuál es cuál, para no sumar peras con manzanas.
#
# UN solo action_type por vía. Meta devuelve el mismo lead bajo varios nombres
# y sumarlos lo cuenta más de una vez:
#   · `lead` YA es el total de formulario: incluye
#     `onsite_conversion.lead_grouped` (formulario instantáneo) y
#     `offsite_conversion.fb_pixel_lead` (píxel). Con los tres en el conjunto,
#     cada anuncio salía con exactamente 2 × `lead` (por-dia.json,
#     21-oct → 19-nov-2026: lead 346 = lead_grouped 262 + fb_pixel_lead 84).
#   · WhatsApp es `messaging_conversation_started_7d`.
#     `total_messaging_connection` es OTRA métrica de la misma conversación:
#     sumarla casi la duplicaba.
# Es el criterio de la casa (cierre-mes, matriz-mensual): formulario +
# WhatsApp, sin duplicar. scripts/prueba_ads_copys.py falla si se vuelve atrás.
LEADS = {"lead"}
CONVERS = {"onsite_conversion.messaging_conversation_started_7d"}


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=90) as r:
        return json.load(r)


def suma(row, tipos):
    return sum(float(a.get("value", 0)) for a in (row.get("actions") or [])
               if a.get("action_type") in tipos)


def resultados_de(row):
    """Leads de formulario y conversaciones de WhatsApp de una fila de insights,
    cada cifra por su lado. Un anuncio puede traer las dos (los de formulario
    también reciben conversaciones): antes, con un solo lead, las conversaciones
    se tiraban.

    `resultados` es leads + conversaciones —un prospecto por cada vía, sin
    duplicar— y `tipo_resultado` dice de qué está hecho. Solo si no hay ni
    leads ni conversaciones se cae a clics en el enlace, que nunca se suman con
    lo anterior.
    """
    leads, convers = int(suma(row, LEADS)), int(suma(row, CONVERS))
    if leads and convers:
        res, tipo = leads + convers, "lead + conversación"
    elif leads:
        res, tipo = leads, "lead"
    elif convers:
        res, tipo = convers, "conversación"
    else:
        res, tipo = int(suma(row, {"link_click"})), "clic"
    return {"leads": leads, "conversaciones": convers,
            "resultados": res, "tipo_resultado": tipo}


def copy_de(creative):
    """Saca el texto del anuncio. Meta lo guarda en tres sitios distintos según
    cómo se montó el anuncio, y hay que mirar los tres:

      · object_story_spec.link_data   — anuncio de imagen o carrusel
      · object_story_spec.video_data  — anuncio de video o reel
      · asset_feed_spec               — Advantage+ con varios textos: aquí
                                        `bodies` y `titles` son LISTAS, porque
                                        Meta rota entre ellas. Se devuelven
                                        todas: si solo se guardara la primera,
                                        se estaría revisando un copy que
                                        quizá ni se muestra.
    """
    oss = creative.get("object_story_spec") or {}
    datos = oss.get("link_data") or oss.get("video_data") or {}
    cta = (datos.get("call_to_action") or {})
    enlace = datos.get("link") or (cta.get("value") or {}).get("link") or ""

    # OJO: los dos formatos NO usan los mismos nombres de campo.
    #   link_data  → name             / description
    #   video_data → title            / link_description
    # Leer solo `name`/`description` deja SIN TITULAR a todos los anuncios de
    # video y reel, que aquí son la mayoría. Lo cazó la prueba de scripts/
    # prueba_ads_copys.py antes de la primera corrida de verdad.
    cuerpos = [datos["message"]] if datos.get("message") else []
    titulos = [t for t in (datos.get("name"), datos.get("title")) if t]
    descrips = [d for d in (datos.get("description"), datos.get("link_description")) if d]

    afs = creative.get("asset_feed_spec") or {}
    for campo, destino in (("bodies", cuerpos), ("titles", titulos),
                           ("descriptions", descrips)):
        for it in (afs.get(campo) or []):
            t = it.get("text")
            if t and t not in destino:
                destino.append(t)
    if not enlace:
        for lu in (afs.get("link_urls") or []):
            enlace = lu.get("website_url") or ""
            if enlace:
                break
    if not cta.get("type"):
        ctas = afs.get("call_to_action_types") or []
        if ctas:
            cta = {"type": ctas[0]}

    # Las tarjetas de un carrusel llevan su propio texto y su propio enlace.
    tarjetas = []
    for c in (datos.get("child_attachments") or []):
        tarjetas.append({
            "titular": c.get("name", ""),
            "descripcion": c.get("description", ""),
            "enlace": c.get("link", ""),
        })

    return {
        "cuerpo": cuerpos,          # texto principal, LITERAL
        "titular": titulos,
        "descripcion": descrips,
        "cta": cta.get("type", ""),
        "enlace": enlace,
        "tarjetas_carrusel": tarjetas,
    }


def main():
    if not TOKEN:
        print("ERROR: falta META_TOKEN en el entorno.")
        sys.exit(1)

    try:
        ins = api(f"{CUENTA}/insights", level="ad",
                  fields=("ad_id,ad_name,adset_name,campaign_name,objective,spend,"
                          "impressions,reach,frequency,clicks,inline_link_clicks,ctr,"
                          "actions,cost_per_action_type"),
                  time_range=json.dumps({"since": DESDE, "until": HASTA}),
                  limit="500")
    except urllib.error.HTTPError as e:
        # Igual que ads_creativos.py: si la API falla no se escribe nada a
        # medias. Un JSON incompleto que parece completo es peor que ninguno.
        print(f"AVISO: insights falló ({e.code}): {e.read()[:500]}")
        sys.exit(0)

    # Un anuncio con leads o conversaciones entra aunque gaste menos de
    # MIN_GASTO: si se quedara fuera, la suma por anuncio dejaría de cuadrar
    # con el total por campaña de fuentes/ads-insights/por-campana.json.
    filas = [f for f in ins.get("data", [])
             if float(f.get("spend") or 0) >= MIN_GASTO
             or suma(f, LEADS | CONVERS)]
    porid = {f["ad_id"]: f for f in filas}

    # Los insights SOLO devuelven anuncios que tuvieron entrega en la ventana.
    # Un anuncio ACTIVO recién subido, o activo pero sin gasto todavía, no
    # saldría — y «qué tengo colgado ahora mismo» es justo la pregunta que hay
    # que poder contestar. Así que se piden aparte los ACTIVE y se añaden los
    # que falten, con sus números a cero y marcados como tales.
    try:
        act = api(f"{CUENTA}/ads", limit="500",
                  effective_status='["ACTIVE"]',
                  fields="id,name,adset{name},campaign{name,objective}")
        for a in act.get("data", []):
            if a["id"] in porid:
                continue
            porid[a["id"]] = {
                "ad_id": a["id"], "ad_name": a.get("name", ""),
                "adset_name": (a.get("adset") or {}).get("name", ""),
                "campaign_name": (a.get("campaign") or {}).get("name", ""),
                "objective": (a.get("campaign") or {}).get("objective", ""),
                "spend": "0", "_sin_entrega": True,
            }
    except urllib.error.HTTPError as e:
        # No es fatal: se sigue con lo que dieron los insights, pero se dice.
        print(f"AVISO: no se pudo listar los anuncios ACTIVE ({e.code}); "
              f"solo van los que tuvieron entrega entre {DESDE} y {HASTA}.")

    filas = list(porid.values())
    if not filas:
        print(f"AVISO: ni anuncios activos ni gasto >= ${MIN_GASTO} entre {DESDE} y {HASTA}.")
        sys.exit(0)

    anuncios, fallos = [], 0
    for f in sorted(filas, key=lambda r: -float(r.get("spend") or 0)):
        gasto = float(f.get("spend") or 0)
        r = resultados_de(f)
        res = r["resultados"]

        texto, estado = {}, ""
        try:
            ad = api(f["ad_id"], fields=("status,effective_status,created_time,"
                                         "creative{object_story_spec,asset_feed_spec}"))
            texto = copy_de(ad.get("creative") or {})
            estado = ad.get("effective_status", "")
        except urllib.error.HTTPError as e:
            # Se anota el hueco en el propio registro. Un anuncio sin copy tiene
            # que verse como tal, no confundirse con uno de copy vacío.
            fallos += 1
            texto = {"ERROR": f"no se pudo leer el creativo (HTTP {e.code})"}
            print(f"  aviso: creativo de '{f.get('ad_name','')}' falló ({e.code})")

        anuncios.append({
            "sin_entrega_en_la_ventana": bool(f.get("_sin_entrega")),
            "anuncio": f.get("ad_name", ""),
            "conjunto": f.get("adset_name", ""),
            "campana": f.get("campaign_name", ""),
            "objetivo": f.get("objective", ""),
            "estado": estado,
            "gasto": round(gasto, 2),
            "impresiones": int(float(f.get("impressions") or 0)),
            "alcance": int(float(f.get("reach") or 0)),
            "frecuencia": round(float(f.get("frequency") or 0), 2),
            "clics_enlace": int(float(f.get("inline_link_clicks") or 0)),
            "ctr": round(float(f.get("ctr") or 0), 2),
            "leads": r["leads"],
            "conversaciones": r["conversaciones"],
            "resultados": res,
            "tipo_resultado": r["tipo_resultado"],
            "coste_resultado": round(gasto / res, 2) if res else None,
            "copy": texto,
        })

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "anuncios.json"), "w") as fh:
        json.dump({
            "generado": str(datetime.date.today()),
            "ventana": {"desde": DESDE, "hasta": HASTA},
            "cuenta": CUENTA,
            "min_gasto": MIN_GASTO,
            "creativos_no_leidos": fallos,
            "nota": ("El copy va LITERAL, tal como está en Meta. `cuerpo`, `titular` y "
                     "`descripcion` son listas porque un anuncio Advantage+ puede llevar "
                     "varios textos que Meta rota. `leads` son los leads de formulario "
                     "(action_type `lead`, que ya incluye lead_grouped y fb_pixel_lead) y "
                     "`conversaciones` las de WhatsApp (messaging_conversation_started_7d); "
                     "van siempre las dos, cada una por su lado, y sumadas por anuncio "
                     "cuadran con el total por campaña de ads-insights. `resultados` es "
                     "leads + conversaciones y `tipo_resultado` dice de qué está hecho: "
                     "«lead», «conversación» o «lead + conversación». Solo si no hay "
                     "ninguno de los dos pasa a «clic» (clics en el enlace), que nunca se "
                     "suma con lo anterior."),
            "anuncios": anuncios,
        }, fh, ensure_ascii=False, indent=2)
    print(f"Listo: {len(anuncios)} anuncios con copy en {OUTDIR}/anuncios.json"
          + (f" ({fallos} creativos no leídos)" if fallos else ""))


if __name__ == "__main__":
    main()
