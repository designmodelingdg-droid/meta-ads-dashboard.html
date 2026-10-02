#!/usr/bin/env python3
"""¿Les llega de verdad el seguimiento por correo a los leads de cada lead magnet?

    GHL_TOKEN=... python3 scripts/seguimiento_correos_lm.py [--muestra 15]
      → matriz-viral/fuentes/ghl/seguimiento-correos-lm.json

Por qué existe: la API de GHL lista los workflows y su estado, pero no sus
pasos, y el editor de workflows no carga en un navegador sin pantalla (probado
el 25-ago). Así que en vez de mirar cómo está armado el workflow, se mira lo que
recibió la gente: para cada lead magnet se toman los contactos más recientes con
su etiqueta y se cuentan los correos SALIENTES de su conversación, con el asunto
y los días que pasaron desde el primero.

Si a los contactos de un recurso solo les llega un correo (el de acceso), no hay
seguimiento de nutrición activo para ese recurso, se llame como se llame el
workflow.

Sin datos personales: se guardan cuentas y asuntos. El nombre y el apellido del
contacto se tapan en el asunto antes de escribir nada, y también correos,
teléfonos y enlaces.
"""
import argparse
import json
import os
import re
import statistics as st
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"
V2 = "https://services.leadconnectorhq.com"
SALIDA = os.path.join("matriz-viral", "fuentes", "ghl", "seguimiento-correos-lm.json")
CAB = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json", "Content-Type": "application/json",
       "Version": "2021-07-28",
       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}

# La etiqueta que marca que la persona pidió el recurso (la más poblada de su embudo).
RECURSOS = {
    "ZAPATA": "lead-calculadora-zapatas",
    "NIVEL": "lead-test-nivel",
    "MEMORIA": "lead-memoria",
    "DYNAMO": "lead-dynamo",
    "GUIA REVIT+CHATGPT": "acceso-guia-revitchatgpt",
    "ACERO (5 verificaciones)": "lead-acero-verificaciones",
    "COTIZA": "lead-cotizador",
}


def pedir(ruta, cuerpo=None, **params):
    url = f"{V2}{ruta}" + (("?" + urllib.parse.urlencode(params)) if params else "")
    data = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(url, data=data, headers=CAB, method="POST" if cuerpo is not None else "GET")
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 * (intento + 1))
                continue
            return {"_error": f"HTTP {e.code}", "_detalle": e.read().decode("utf-8", "replace")[:200]}
        except Exception as e:  # noqa: BLE001
            return {"_error": str(e)[:200]}
    return {"_error": "HTTP 429 persistente"}


def contactos(tag, n):
    d = pedir("/contacts/search", {"locationId": LOCATION, "pageLimit": n,
                                   "filters": [{"field": "tags", "operator": "contains", "value": tag}],
                                   "sort": [{"field": "dateAdded", "direction": "desc"}]})
    return d.get("contacts") or [], d.get("total"), d.get("_error")


def limpiar(asunto, contacto):
    t = asunto or ""
    for k in ("firstName", "lastName", "contactName", "firstNameRaw", "lastNameRaw"):
        v = (contacto.get(k) or "").strip()
        for parte in v.split():
            if len(parte) > 2:
                t = re.sub(re.escape(parte), "[nombre]", t, flags=re.I)
    t = re.sub(r"[\w\.\-+]+@[\w\.\-]+", "[correo]", t)
    t = re.sub(r"(?:\+?\d[\d\s\-\(\)]{7,}\d)", "[telefono]", t)
    t = re.sub(r"https?://\S+", "[enlace]", t)
    return " ".join(t.split())[:140]


def correos_salientes(contacto):
    """Correos que GHL le mandó a este contacto: [(fecha, asunto)]."""
    d = pedir("/conversations/search", locationId=LOCATION, contactId=contacto["id"], limit=20)
    out = []
    for conv in d.get("conversations") or []:
        m = pedir(f"/conversations/{conv['id']}/messages", limit=100)
        msgs = m.get("messages")
        if isinstance(msgs, dict):
            msgs = msgs.get("messages")
        for x in msgs or []:
            tipo = str(x.get("messageType") or x.get("type") or "")
            if "EMAIL" not in tipo.upper() or str(x.get("direction")) != "outbound":
                continue
            asunto = x.get("subject") or ((x.get("meta") or {}).get("email") or {}).get("subject")
            if not asunto:
                ids = ((x.get("meta") or {}).get("email") or {}).get("messageIds") or []
                if ids:
                    e = pedir(f"/conversations/messages/email/{ids[0]}")
                    asunto = (e.get("emailMessage") or e).get("subject")
            out.append((x.get("dateAdded") or "", limpiar(asunto or "(sin asunto legible)", contacto)))
        time.sleep(0.2)
    return sorted(out)


def main():
    if not TOKEN:
        sys.exit("ERROR: falta GHL_TOKEN.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--muestra", type=int, default=15)
    a = ap.parse_args()
    salida = {"generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
              "metodo": "Contactos más recientes con la etiqueta del recurso; se cuentan los correos SALIENTES de sus conversaciones. Solo cuentas y asuntos, sin datos personales.",
              "recursos": {}}
    for recurso, tag in RECURSOS.items():
        cs, total, err = contactos(tag, a.muestra)
        por_contacto, asuntos, dias_ultimo = [], Counter(), []
        for c in cs:
            mails = correos_salientes(c)
            por_contacto.append(len(mails))
            for _, s in mails:
                asuntos[s] += 1
            if len(mails) >= 2:
                try:
                    f0 = datetime.fromisoformat(mails[0][0].replace("Z", "+00:00"))
                    f1 = datetime.fromisoformat(mails[-1][0].replace("Z", "+00:00"))
                    dias_ultimo.append(round((f1 - f0).total_seconds() / 86400, 1))
                except ValueError:
                    pass
        con_seguimiento = sum(1 for n in por_contacto if n >= 2)
        salida["recursos"][recurso] = {
            "etiqueta": tag, "contactos_con_etiqueta": total, "muestra": len(cs), "error": err,
            "correos_por_contacto": dict(sorted(Counter(por_contacto).items())),
            "contactos_con_2_o_mas_correos": con_seguimiento,
            "dias_entre_primer_y_ultimo_correo_mediana": st.median(dias_ultimo) if dias_ultimo else None,
            "asuntos_mas_frecuentes": asuntos.most_common(12),
            "lectura": ("sin muestra" if not cs else
                        "hay seguimiento por correo: a la mayoría le llegan 2 o más" if con_seguimiento * 2 >= len(cs) else
                        "NO hay seguimiento activo: a la mayoría solo le llega 1 correo (o ninguno)"),
        }
        print(f"{recurso}: {len(cs)} contactos · {con_seguimiento} con 2+ correos · {dict(Counter(por_contacto))}")
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    print("ok →", SALIDA)


if __name__ == "__main__":
    main()
