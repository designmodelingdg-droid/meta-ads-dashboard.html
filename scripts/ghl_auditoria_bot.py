#!/usr/bin/env python3
"""¿Cómo vende el bot de WhatsApp y dónde se le cae la venta?

    GHL_TOKEN=... python3 scripts/ghl_auditoria_bot.py --limite 400
      → matriz-viral/fuentes/ghl/auditoria-bot-ventas.json

Por qué existe (5-oct-2026): el agente de ventas responde, manda el temario y
deja la conversación en «revísalo con calma y me cuentas». En 300
conversaciones recientes, el último mensaje fue nuestro en 291: la persona dejó
de contestar después de leer al bot. Este script mira QUÉ dice el bot y CÓMO
termina cada conversación, para escribirle instrucciones de cierre sobre
evidencia y no sobre impresiones.

Qué mide:
  - quién envía (fuente del mensaje saliente: agente, flujo, persona del equipo);
  - largo de los mensajes del bot y cuántos terminan en pregunta;
  - con qué termina la conversación: pregunta, temario o PDF, «revísalo y me
    cuentas», propuesta de llamada, enlace de pago, precio;
  - qué objeciones aparecen (precio, presupuesto, tiempo, confianza, «es un
    bot», clases grabadas, «lo pienso») y cómo responde el bot justo después;
  - cuántas conversaciones terminan en una etiqueta de compra.

Sin datos personales: se tapan el nombre y el apellido del contacto (los saca
de la propia conversación), correos, teléfonos y enlaces. Las frases del bot
se guardan porque son texto de la academia; de las personas solo se guardan
fragmentos cortos ya limpios en los ejemplos.
"""
import argparse
import json
import os
import re
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
SALIDA = os.path.join("matriz-viral", "fuentes", "ghl", "auditoria-bot-ventas.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"

# Con qué puede terminar un mensaje del bot. Un mismo mensaje puede caer en
# varias: se cuentan todas.
CIERRES = {
    "pregunta": r"\?\s*(\W{0,6})$",
    "revisalo_y_me_cuentas": r"(rev[ií]s(a|al)o|ech(a|ale) un vistazo|con calma|me cuentas|me comentas|qu[eé] te parece|cualquier duda|quedo atent|estoy atent|aqu[ií] estoy)",
    "temario_o_pdf": r"(temario|\.pdf|brochure|programa completo|drive\.google)",
    "propone_llamada": r"(llamada|videollamada|reuni[oó]n|agend|cita|calendario|horario para hablar|zoom|meet)",
    "enlace_de_pago": r"(link de pago|enlace de pago|pagar|checkout|paypal|stripe|hotmart|transferencia|inscr[ií]bete|reserva tu cupo)",
    "menciona_precio": r"(\$\s?\d|usd|d[oó]lares|precio|costo|inversi[oó]n)",
    "da_opciones": r"(\bo\b.*\?|cu[aá]l prefieres|qu[eé] prefieres|opci[oó]n a|ma[nñ]ana o)",
}

OBJECIONES = {
    "precio_caro": r"(caro|muy costoso|precio alto|no me alcanza|est[aá] elevado)",
    "sin_presupuesto": r"(no tengo (el )?(dinero|presupuesto|plata)|sin presupuesto|desemplead|no trabajo|sin trabajo)",
    "tiempo": r"(no tengo tiempo|poco tiempo|trabajo todo el d[ií]a|horario)",
    "confianza": r"(confia|estafa|seguro que|garant[ií]a|es real|referencias|no me da confianza|confiabilidad)",
    # «Robot» es Robot Structural Analysis: no cuenta como «es un bot».
    "es_un_bot": r"(\bbot\b|\bun robot\b|no es una persona|eres una ia|eres (un )?humano|persona real|hablar con (una )?persona|hablar con alguien)",
    "clases_grabadas": r"(grabad|en vivo|online en vivo|clases en directo|profesor real|tutor real)",
    "lo_pienso": r"(lo pienso|lo voy a pensar|despu[eé]s te (escribo|aviso|confirmo)|m[aá]s adelante|luego te)",
    "pide_descuento": r"(descuento|beca|rebaja|precio especial|m[aá]s barato)",
    "cuotas": r"(cuotas|pagar en partes|financ|mensualidad|a plazos)",
}

COMPRA = re.compile(r"(compr|inscrit|pagad|pago confirmado|cliente|alumno|matricul)", re.I)


def limpiar(texto, nombres=()):
    t = texto or ""
    for n in nombres:
        for parte in (n or "").split():
            if len(parte) > 2:
                t = re.sub(r"\b" + re.escape(parte) + r"\b", "[nombre]", t, flags=re.I)
    t = re.sub(r"(full ?name|nombre)\s*:\s*[^\n]{1,60}", r"\1: [nombre]", t, flags=re.I)
    t = re.sub(r"[\w\.\-+]+@[\w\.\-]+", "[correo]", t)
    t = re.sub(r"(?:\+?\d[\d\s\-\(\)]{7,}\d)", "[telefono]", t)
    t = re.sub(r"https?://\S+", "[enlace]", t)
    return " ".join(t.split())


def api(ruta, **params):
    url = f"{V2}{ruta}" + (("?" + urllib.parse.urlencode(params)) if params else "")
    cab = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json", "Version": "2021-07-28", "User-Agent": UA}
    for intento in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=cab), timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 * (intento + 1))
                continue
            return {"_error": f"HTTP {e.code}"}
        except Exception as e:  # noqa: BLE001
            return {"_error": str(e)[:120]}
    return {"_error": "HTTP 429 persistente"}


def lista(d, clave):
    v = d.get(clave)
    if isinstance(v, dict):
        v = v.get(clave)
    return v if isinstance(v, list) else []


def conversaciones(tope):
    out, cursor = [], None
    while len(out) < tope:
        p = {"locationId": LOCATION, "limit": 100}
        if cursor:
            p["startAfterDate"] = cursor
        d = api("/conversations/search", **p)
        lote = lista(d, "conversations")
        if not lote:
            break
        out += lote
        cursor = lote[-1].get("lastMessageDate")
        time.sleep(0.3)
    return out[:tope]


def clasifica(texto, reglas):
    return [k for k, p in reglas.items() if re.search(p, texto or "", re.I)]


def main():
    if not TOKEN:
        sys.exit("ERROR: falta GHL_TOKEN.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=400)
    a = ap.parse_args()

    convs = conversaciones(a.limite)
    fuentes, cierres_ultimo, cierres_todos = Counter(), Counter(), Counter()
    objeciones, respuesta_a_objecion = Counter(), Counter()
    ejemplos_objecion = defaultdict(list)
    largos_bot, frases_bot = [], Counter()
    revisadas = termina_nuestro = compra = con_llamada = con_pago = 0
    tras_objecion_largo, tras_objecion_pregunta, tras_objecion_n = [], 0, 0
    ejemplos = []

    tipos_conv, tipos_msg = Counter(), Counter()
    for c in convs:
        tipos_conv[c.get("type") or "?"] += 1
        d = api(f"/conversations/{c['id']}/messages", limit=100)
        ms = lista(d, "messages")
        for m in ms:
            tipos_msg[m.get("messageType") or "?"] += 1
        # Fuera llamadas, correos, comentarios internos y registros de actividad:
        # solo quedan mensajes de chat con texto.
        ms = [m for m in ms if (m.get("body") or "").strip()
              and not re.search(r"ACTIVITY|CALL|EMAIL|COMMENT|NOTE|CUSTOM_PROVIDER_EMAIL", m.get("messageType") or "")]
        if len(ms) < 3:
            continue
        ms.sort(key=lambda m: m.get("dateAdded") or "")
        nombres = [c.get("contactName"), c.get("fullName"), c.get("firstName"), c.get("lastName")]
        revisadas += 1
        hubo_llamada = hubo_pago = False
        for i, m in enumerate(ms):
            cuerpo = m.get("body") or ""
            if (m.get("direction") or "").lower() == "outbound":
                fuentes[str(m.get("source") or m.get("messageSource") or ("persona" if m.get("userId") else "sin dato"))] += 1
                largos_bot.append(len(cuerpo))
                tipos = clasifica(cuerpo.strip(), CIERRES)
                cierres_todos.update(tipos)
                hubo_llamada |= "propone_llamada" in tipos
                hubo_pago |= "enlace_de_pago" in tipos
                frase = limpiar(cuerpo, nombres)
                if 20 <= len(frase) <= 400:
                    frases_bot[frase] += 1
            else:
                obs = clasifica(cuerpo, OBJECIONES)
                objeciones.update(obs)
                for o in obs:
                    if len(ejemplos_objecion[o]) < 6:
                        ejemplos_objecion[o].append(limpiar(cuerpo, nombres)[:200])
                if obs:
                    sig = next((x for x in ms[i + 1:] if (x.get("direction") or "").lower() == "outbound"), None)
                    if sig:
                        tras_objecion_n += 1
                        tras_objecion_largo.append(len(sig.get("body") or ""))
                        t2 = clasifica((sig.get("body") or "").strip(), CIERRES)
                        tras_objecion_pregunta += "pregunta" in t2
                        respuesta_a_objecion.update(t2 or ["sin_pregunta_ni_paso"])
        con_llamada += hubo_llamada
        con_pago += hubo_pago
        ultimo = ms[-1]
        if (ultimo.get("direction") or "").lower() == "outbound":
            termina_nuestro += 1
            ult_out = ultimo
        else:
            ult_out = next((x for x in reversed(ms) if (x.get("direction") or "").lower() == "outbound"), None)
        if ult_out:
            cierres_ultimo.update(clasifica((ult_out.get("body") or "").strip(), CIERRES) or ["sin_pregunta_ni_paso"])
        compro = bool(COMPRA.search(" ".join(c.get("tags") or [])))
        compra += compro
        if len(ejemplos) < 30:
            cola = ms[-4:]
            ejemplos.append({
                "mensajes": len(ms),
                "compro_por_etiqueta": compro,
                "final": [{"de": "bot" if (x.get("direction") or "").lower() == "outbound" else "persona",
                           "texto": limpiar(x.get("body"), nombres)[:240]} for x in cola],
            })
        time.sleep(0.15)

    largos_bot.sort()
    res = {
        "generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "nota": "Agregados y ejemplos anonimizados (nombre del contacto, correos, teléfonos y enlaces tapados). Muestra de las conversaciones más recientes, no el total.",
        "conversaciones_traidas": len(convs),
        "conversaciones_revisadas": revisadas,
        "tipos_de_conversacion": dict(tipos_conv.most_common()),
        "tipos_de_mensaje": dict(tipos_msg.most_common()),
        "terminan_con_mensaje_nuestro": termina_nuestro,
        "con_etiqueta_de_compra": compra,
        "conversaciones_con_propuesta_de_llamada": con_llamada,
        "conversaciones_con_enlace_de_pago": con_pago,
        "fuente_de_los_mensajes_salientes": dict(fuentes.most_common()),
        "largo_mensajes_bot": {"mediana": largos_bot[len(largos_bot) // 2] if largos_bot else None,
                               "p90": largos_bot[int(len(largos_bot) * .9)] if largos_bot else None,
                               "n": len(largos_bot)},
        "como_terminan_los_mensajes_del_bot": dict(cierres_todos.most_common()),
        "ultimo_mensaje_nuestro_de_cada_conversacion": dict(cierres_ultimo.most_common()),
        "objeciones": dict(objeciones.most_common()),
        "ejemplos_de_objecion": {k: v for k, v in ejemplos_objecion.items()},
        "respuesta_justo_despues_de_una_objecion": {
            "n": tras_objecion_n,
            "largo_mediana": sorted(tras_objecion_largo)[len(tras_objecion_largo) // 2] if tras_objecion_largo else None,
            "terminan_en_pregunta": tras_objecion_pregunta,
            "tipos": dict(respuesta_a_objecion.most_common()),
        },
        "frases_del_bot_mas_repetidas": [[f, n] for f, n in frases_bot.most_common(40) if n >= 3],
        "ejemplos_final_de_conversacion": ejemplos,
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(f"ok → {SALIDA} · {revisadas} conversaciones · terminan nuestras {termina_nuestro}")


if __name__ == "__main__":
    main()
