#!/usr/bin/env python3
"""
Prueba del extractor de copys, SIN tocar la API ni ningún token.

Existe porque `ads_copys.py` corre en una Action y solo se ve el resultado
cuando ya se gastó la corrida. La primera versión dejaba sin titular a todos
los anuncios de VIDEO y reel —que en esta cuenta son la mayoría— y eso lo
cazó esta prueba, no la corrida real.

Uso:  python3 scripts/prueba_ads_copys.py
"""
import importlib.util, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ac", os.path.join(AQUI, "ads_copys.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

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

    print()
    if fallos:
        for f in fallos:
            print("✖", f)
        sys.exit(1)
    print("Todas las comprobaciones pasan.")


if __name__ == "__main__":
    main()
