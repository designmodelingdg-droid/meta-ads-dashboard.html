#!/usr/bin/env python3
"""
Prueba del extractor de copys, SIN tocar la API ni ningún token.

Existe porque `ads_copys.py` corre en una Action y solo se ve el resultado
cuando ya se gastó la corrida. La primera versión dejaba sin titular a todos
los anuncios de VIDEO y reel —que en esta cuenta son la mayoría— y eso lo
cazó esta prueba, no la corrida real.

También vigila CÓMO SE CUENTAN los resultados, en `ads_copys.py` y en
`ads_creativos.py`. Los dos sumaban `lead` + `onsite_conversion.lead_grouped`,
y `lead` ya lo incluye: cada lead de formulario salía dos veces (nov-2026: el
manifiesto decía 54 leads para un anuncio que tenía 27). Si alguien vuelve a
meter `lead_grouped` en la suma, esta prueba falla.

Uso:  python3 scripts/prueba_ads_copys.py
"""
import importlib.util, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ac", os.path.join(AQUI, "ads_copys.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)
spec = importlib.util.spec_from_file_location("cr", os.path.join(AQUI, "ads_creativos.py"))
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

# Las cuatro formas en que Meta devuelve un creativo, más el caso vacío.
CASOS = {
    "imagen (link_data)": {"object_story_spec": {"link_data": {
        "message": "Sabes usar Revit. Pero, ¿sabes implementar BIM?",
        "name": "BIM Professional · 3 meses",
        "description": "Microcredencial incluida",
        "link": "https://fb.me/form1",
        "call_to_action": {"type": "LEARN_MORE"}}}},

    "video / reel (video_data)": {"object_story_spec": {"video_data": {
        "message": "Si el choque lo descubres en obra, ya lo pagaste dos veces.",
        "title": "Especialización en Acero · $225",
        "link_description": "Ahora con tutor de IA",
        "call_to_action": {"type": "WHATSAPP_MESSAGE",
                           "value": {"link": "https://wa.me/593"}}}}},

    "carrusel (child_attachments)": {"object_story_spec": {"link_data": {
        "message": "¿En qué etapa BIM estás?", "link": "https://x.com",
        "child_attachments": [
            {"name": "BIM Professional", "description": "3 meses", "link": "https://a"},
            {"name": "BIM Coordination", "description": "3 meses", "link": "https://b"}]}}},

    "Advantage+ (asset_feed_spec)": {"asset_feed_spec": {
        "bodies": [{"text": "Texto A"}, {"text": "Texto B"}, {"text": "Texto C"}],
        "titles": [{"text": "Titular 1"}, {"text": "Titular 2"}],
        "descriptions": [{"text": "Desc"}],
        "link_urls": [{"website_url": "https://dg.com"}],
        "call_to_action_types": ["SIGN_UP"]}},

    "vacío": {},
}


def fila(**acciones):
    """Una fila de insights como la devuelve Meta: `actions` es una lista de
    {action_type, value} y el valor llega como TEXTO."""
    return {"actions": [{"action_type": t.replace("__", "."), "value": str(v)}
                        for t, v in acciones.items()]}


# Filas con la forma REAL de la cuenta. Meta devuelve el mismo lead bajo varios
# action_type a la vez; lo que hay que contar es UNO por vía.
FILAS = {
    # Formulario instantáneo: `lead` y `lead_grouped` traen el MISMO número.
    # Es «MasterNOV16-9v3 - Copia»: 27 leads, y se publicaron 54.
    "formulario instantáneo": fila(
        lead=27, onsite_conversion__lead_grouped=27, link_click=310),

    # Formulario + píxel: lead = lead_grouped + fb_pixel_lead (185 = 159 + 26).
    "formulario + píxel": fila(
        lead=185, onsite_conversion__lead_grouped=159,
        offsite_conversion__fb_pixel_lead=26, onsite_web_lead=26),

    # WhatsApp: dos métricas de la MISMA conversación.
    "whatsapp": fila(
        onsite_conversion__messaging_conversation_started_7d=94,
        onsite_conversion__total_messaging_connection=118, link_click=200),

    # Anuncio de formulario que además recibe conversaciones: van las dos.
    "formulario y whatsapp": fila(
        lead=14, onsite_conversion__lead_grouped=14,
        onsite_conversion__messaging_conversation_started_7d=9,
        onsite_conversion__total_messaging_connection=9),

    "solo clics": fila(link_click=401, post_engagement=900),
    "sin acciones": {},
}

# (leads, conversaciones, resultados, tipo_resultado) que tiene que salir.
ESPERADO = {
    "formulario instantáneo": (27, 0, 27, "lead"),
    "formulario + píxel": (185, 0, 185, "lead"),
    "whatsapp": (0, 94, 94, "conversación"),
    "formulario y whatsapp": (14, 9, 23, "lead + conversación"),
    "solo clics": (0, 0, 401, "clic"),
    "sin acciones": (0, 0, 0, "clic"),
}


def main():
    fallos = []

    def exigir(cond, msg):
        if not cond:
            fallos.append(msg)

    for nombre, creativo in CASOS.items():
        r = ac.copy_de(creativo)
        print(f"— {nombre}: cuerpos={len(r['cuerpo'])} titulares={len(r['titular'])} "
              f"descrips={len(r['descripcion'])} cta={r['cta']!r} "
              f"tarjetas={len(r['tarjetas_carrusel'])}")

    img = ac.copy_de(CASOS["imagen (link_data)"])
    exigir(img["titular"] == ["BIM Professional · 3 meses"], "link_data: falta el titular (name)")

    vid = ac.copy_de(CASOS["video / reel (video_data)"])
    # El fallo que motivó esta prueba: video_data usa `title` y
    # `link_description`, no `name` y `description`.
    exigir(vid["titular"] == ["Especialización en Acero · $225"],
           "video_data: el titular vive en `title`, no en `name`")
    exigir(vid["descripcion"] == ["Ahora con tutor de IA"],
           "video_data: la descripción vive en `link_description`")
    exigir(vid["enlace"] == "https://wa.me/593",
           "video_data: el enlace de WhatsApp está dentro de call_to_action.value")

    car = ac.copy_de(CASOS["carrusel (child_attachments)"])
    exigir(len(car["tarjetas_carrusel"]) == 2, "carrusel: se pierden las tarjetas")

    adv = ac.copy_de(CASOS["Advantage+ (asset_feed_spec)"])
    exigir(adv["cuerpo"] == ["Texto A", "Texto B", "Texto C"],
           "Advantage+: hay que guardar TODOS los cuerpos, no solo el primero")
    exigir(adv["titular"] == ["Titular 1", "Titular 2"], "Advantage+: faltan titulares")
    exigir(adv["cta"] == "SIGN_UP" and adv["enlace"] == "https://dg.com",
           "Advantage+: cta o enlace mal leídos")

    vac = ac.copy_de(CASOS["vacío"])
    exigir(vac["cuerpo"] == [] and vac["cta"] == "" and vac["enlace"] == "",
           "vacío: debe devolver campos vacíos, nunca inventarlos")

    # ── Conteo de resultados ────────────────────────────────────────────
    for nombre, f in FILAS.items():
        r = ac.resultados_de(f)
        sale = (r["leads"], r["conversaciones"], r["resultados"], r["tipo_resultado"])
        print(f"— {nombre}: leads={sale[0]} conversaciones={sale[1]} "
              f"resultados={sale[2]} tipo={sale[3]!r}")
        exigir(sale == ESPERADO[nombre],
               f"ads_copys · {nombre}: sale {sale}, tenía que salir {ESPERADO[nombre]}")
        # ads_creativos da un solo número: formulario + WhatsApp, sin duplicar.
        total = ESPERADO[nombre][0] + ESPERADO[nombre][1]
        exigir(cr.leads_de(f) == total,
               f"ads_creativos · {nombre}: leads_de da {cr.leads_de(f)}, tenía que dar {total}")

    # El fallo que motivó esto, dicho con todas las letras.
    exigir(ac.resultados_de(FILAS["formulario instantáneo"])["leads"] == 27,
           "ads_copys: `lead` YA incluye `lead_grouped`; sumarlos da 54 donde hay 27")
    exigir(cr.leads_de(FILAS["formulario instantáneo"]) == 27,
           "ads_creativos: `lead` YA incluye `lead_grouped`; sumarlos da 54 donde hay 27")
    exigir(ac.resultados_de(FILAS["whatsapp"])["conversaciones"] == 94,
           "ads_copys: las conversaciones son solo messaging_conversation_started_7d; "
           "total_messaging_connection es otra métrica de lo mismo")

    # Lo que tiene que cuadrar: la suma por anuncio contra el total de la
    # campaña (el `lead` y el messaging_conversation_started_7d de
    # fuentes/ads-insights/por-campana.json).
    anuncios = [FILAS["formulario instantáneo"], FILAS["formulario y whatsapp"],
                fila(lead=42, onsite_conversion__lead_grouped=42)]
    exigir(sum(ac.resultados_de(a)["leads"] for a in anuncios) == 83,
           "la suma de leads por anuncio no cuadra con el `lead` de la campaña (83)")
    exigir(sum(ac.resultados_de(a)["conversaciones"] for a in anuncios) == 9,
           "la suma de conversaciones por anuncio no cuadra con la campaña (9)")

    print()
    if fallos:
        for f in fallos:
            print("✖", f)
        sys.exit(1)
    print("Todas las comprobaciones pasan.")


if __name__ == "__main__":
    main()
