#!/usr/bin/env python3
"""Activa en OpenReply la campaña de cada publicación nueva de Instagram.

Regla de la casa: una palabra, una automatización. Cuando sale un post cuyo
caption pide comentar una palabra configurada (NIVEL, ACERO, ZAPATA…), este
script le crea en OpenReply la campaña de esa palabra, con el recurso, los
textos y las respuestas tocables de `openreply_campanas_config.json`.

Lo que hace, en orden:
  1. Lee las publicaciones recientes de la cuenta (API de OpenReply).
  2. Lee las campañas que ya existen, para no duplicar ninguna.
  3. Para cada post sin campaña, busca en el caption una palabra configurada
     (sin distinguir mayúsculas ni tildes). Si encuentra exactamente una, crea
     la campaña. Si encuentra varias o ninguna, lo dice y no toca nada.

Solo Instagram: OpenReply no actúa en Facebook. Facebook lo contesta GoHighLevel.

Uso:
  OPENREPLY_API_KEY=… python3 scripts/openreply_auto_campanas.py [--dry-run] [--horas 36]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = os.environ.get("OPENREPLY_URL", "https://openreply.dgdesignmodeling.com").rstrip("/")
CONFIG = Path(__file__).with_name("openreply_campanas_config.json")


def api(method: str, path: str, body: dict | None = None) -> dict:
    key = os.environ.get("OPENREPLY_API_KEY", "").strip()
    if not key:
        sys.exit("Falta OPENREPLY_API_KEY (secreto del repositorio).")
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        sys.exit(f"OpenReply respondió {e.code} en {method} {path}: {detail}")


def plano(texto: str) -> str:
    """Minúsculas y sin tildes, para comparar como compara OpenReply."""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return sin_tildes.lower()


def palabra_del_caption(caption: str, palabras: dict) -> tuple[str | None, list[str]]:
    """Devuelve la palabra configurada que pide el caption, o None.

    Busca cada palabra y sus variantes como palabra completa. Si el caption
    menciona varias, se queda con la que aparece después de «comenta», que es
    la que de verdad se pide; si aun así hay varias, no decide.
    """
    texto = plano(caption)
    halladas: dict[str, int] = {}
    for clave, cfg in palabras.items():
        for forma in [clave, *cfg.get("variantes", [])]:
            m = re.search(rf"(?<![a-z0-9]){re.escape(plano(forma))}(?![a-z0-9])", texto)
            if m:
                pos = halladas.get(clave)
                halladas[clave] = m.start() if pos is None else min(pos, m.start())
                break
    if not halladas:
        return None, []
    # Solo cuenta la palabra que el caption PIDE: la que sigue a «comenta».
    # «El acero resiste más» no es una campaña de ACERO.
    tras_comenta = {}
    for k in halladas:
        formas = [k, *palabras[k].get("variantes", [])]
        alternancia = "|".join(re.escape(plano(f)) for f in formas)
        if re.search(rf"coment[a-z]*[^.\n]{{0,40}}(?<![a-z0-9])(?:{alternancia})(?![a-z0-9])", texto):
            tras_comenta[k] = halladas[k]
    if len(tras_comenta) == 1:
        return next(iter(tras_comenta)), list(halladas)
    return None, list(halladas)


def nombre_campana(caption: str, palabra: str) -> str:
    primera = re.split(r"[.\n!?¿¡]", caption.strip(), maxsplit=1)[0]
    primera = re.sub(r"[^\w\s]", "", primera).strip()
    corto = " ".join(primera.split()[:5]).upper() or "POST"
    return f"{corto[:40]} {palabra}"


def cuerpo_campana(post: dict, palabra: str, cfg: dict, comun: dict) -> dict:
    p = cfg
    return {
        "name": nombre_campana(post.get("caption") or "", palabra),
        "instagramAccountId": comun["instagramAccountId"],
        "postId": post["id"],
        "postUrl": post.get("permalink"),
        "keywords": [palabra, *p.get("variantes", [])][:10],
        "wholeWordMatch": True,
        # OpenReply no puede contestar DMs en esta cuenta (la bandeja es de GHL).
        "dmTriggerEnabled": False,
        "dmMessage": p["dm"],
        "linkButtonLabel": p["boton"],
        "trackedDestinationUrl": p["enlace"],
        "requireFollow": True,
        "followGateWeb": True,
        "followPromptMessage": p["seguir"],
        "followPromptButtonLabel": comun["boton_seguir"],
        "followRepromptMessage": comun["reprompt"],
        "postDeliveryQuestion": p["pregunta"],
        "postDeliveryAnswers": p["respuestas"][:2],
        "publicReplyEnabled": True,
        "publicReplyMessages": comun["respuestas_publicas"],
        "isActive": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="Muestra qué haría sin crear nada")
    ap.add_argument("--horas", type=int, default=36, help="Mirar solo posts de las últimas N horas")
    ap.add_argument("--limite", type=int, default=12, help="Cuántos posts recientes pedir")
    args = ap.parse_args()

    conf = json.loads(CONFIG.read_text(encoding="utf-8"))
    palabras = conf["palabras"]

    posts_resp = api("GET", f"/api/instagram/posts?limit={args.limite}")
    data = posts_resp.get("data")
    posts = data if isinstance(data, list) else (data.get("posts") or data.get("media") or [])

    autos_resp = api("GET", "/api/automations")
    a = autos_resp.get("data")
    autos = a if isinstance(a, list) else a.get("automations", [])
    con_campana = {x.get("postId") for x in autos if x.get("postId")}

    desde = datetime.now(timezone.utc) - timedelta(hours=args.horas)
    creadas, saltadas = 0, 0
    print(f"{'PREVIA' if args.dry_run else 'EJECUCIÓN'} · {len(posts)} posts leídos · {len(con_campana)} ya con campaña · ventana {args.horas} h\n")

    for post in posts:
        ts = post.get("timestamp") or ""
        try:
            fecha = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            fecha = None
        etiqueta = f"{(ts or '')[:16]} {post.get('permalink')}"
        if fecha and fecha < desde:
            continue
        if post["id"] in con_campana:
            print(f"· ya tiene campaña      {etiqueta}")
            continue
        palabra, halladas = palabra_del_caption(post.get("caption") or "", palabras)
        if not palabra:
            motivo = "sin palabra configurada" if not halladas else f"menciona {halladas} pero no pide comentarla, o pide varias"
            print(f"· {motivo:22s} {etiqueta}")
            saltadas += 1
            continue
        cuerpo = cuerpo_campana(post, palabra, palabras[palabra], conf)
        if args.dry_run:
            print(f"→ CREARÍA «{cuerpo['name']}» [{', '.join(cuerpo['keywords'])}] → {palabras[palabra]['recurso']}  {etiqueta}")
            continue
        resp = api("POST", "/api/automations", cuerpo)
        nueva = resp.get("data") or {}
        print(f"✅ creada «{nueva.get('name')}» id {nueva.get('id')} [{', '.join(cuerpo['keywords'])}] → {palabras[palabra]['recurso']}  {etiqueta}")
        creadas += 1

    print(f"\nResumen: {creadas} creadas · {saltadas} sin decidir")
    return 0


if __name__ == "__main__":
    sys.exit(main())
