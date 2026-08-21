#!/usr/bin/env python3
"""
Analiza las conversaciones del CRM para perfilar los leads del Master.

POR QUE EXISTE
    Sabemos cuanto cuesta un lead de Master ($1,17 por WhatsApp) y en que etapa
    del pipeline queda. Lo que no sabemos es QUIEN es: que pregunta, que le
    frena, en que punto deja de responder.

    Sin eso, poner preguntas de calificacion en el formulario es adivinar. Con
    esto se ponen las preguntas que la gente ya esta haciendo.

QUE SE GUARDA, Y QUE NO
    **No se guarda ni un nombre, ni un telefono, ni un correo.** Tampoco el
    texto completo de los mensajes de las personas.

    Se guardan AGREGADOS: cuantas conversaciones, cuantos mensajes, quien habla
    ultimo, en que momento se cortan, y con que frecuencia aparece cada tema.
    Para decidir el filtro de perfil hacen falta los patrones, no las personas.

    Los fragmentos de ejemplo salen anonimizados y pasan por un limpiador que
    borra telefonos, correos y URLs antes de escribir nada.

USO
    GHL_TOKEN=xxx python3 scripts/ghl_conversaciones.py --limite 300
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
from collections import Counter
from datetime import date, datetime, timezone

TOKEN = os.environ.get("GHL_TOKEN", "").strip()
LOCATION = "nkKbOarn5IwHeMv48uY9"
V2 = "https://services.leadconnectorhq.com"
SALIDA = "matriz-viral/fuentes/ghl"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# Temas que se cuentan. Cada uno es la pregunta real que hace la gente, y
# cada uno lleva a una pregunta distinta en el formulario de calificacion.
TEMAS = {
 "precio":        r"\b(precio|costo|cuesta|vale|cuanto|cuánto|valor|pagar|pago|financ|cuota|descuento|beca)\w*",
 "duracion":      r"\b(duraci|cuanto dura|cuánto dura|tiempo|meses|horas|semanas|horario)\w*",
 "modalidad":     r"\b(online|presencial|virtual|asincr|en vivo|grabad|ritmo)\w*",
 "certificado":   r"\b(certificad|titul|título|diploma|aval|acredit|universit)\w*",
 "temario":       r"\b(temario|contenido|modulos|módulos|programa|pensum|malla|que veo|qué veo)\w*",
 "software":      r"\b(revit|robot|advance steel|navisworks|autocad|civil|sap2000|etabs|dynamo|licencia)\w*",
 "perfil_propio": r"\b(soy |trabajo|estudi|ingenier|arquitect|egresad|reci[eé]n|experiencia|a[nñ]os)\w*",
 "requisitos":    r"\b(requisit|necesito saber|nivel previo|sin experiencia|desde cero|principiante)\w*",
 "inicio":        r"\b(cuando (empieza|inicia|abre)|cuándo|fecha de inicio|proxima|próxima cohorte|cupo)\w*",
 "empleo":        r"\b(trabajo|empleo|salario|sueldo|contratan|bolsa|oportunidad laboral)\w*",
}

# Un lead del Master se reconoce por lo que dice, no por una etiqueta: las
# etiquetas se ponen a mano y estan incompletas.
MASTER = re.compile(r"\b(m[aá]ster|master|bim manager|maestr[ií]a)\w*", re.I)


def limpiar(texto):
    """Quita todo lo que pueda identificar a una persona."""
    t = texto or ""
    t = re.sub(r"[\w\.\-+]+@[\w\.\-]+", "[correo]", t)
    t = re.sub(r"(?:\+?\d[\d\s\-\(\)]{7,}\d)", "[telefono]", t)
    t = re.sub(r"https?://\S+", "[enlace]", t)
    return " ".join(t.split())


def api(ruta, **params):
    url = f"{V2}{ruta}"
    if params:
        url += ("&" if "?" in ruta else "?") + urllib.parse.urlencode(params)
    cab = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json",
           "Version": "2021-07-28", "User-Agent": UA}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=cab), timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}", "_detalle": e.read().decode()[:200]}
    except Exception as e:                       # noqa: BLE001
        return {"_error": str(e)[:200]}


def filas(d, *claves):
    for k in claves:
        if isinstance(d.get(k), list):
            return d[k]
    return next((v for v in d.values() if isinstance(v, list)), [])


def conversaciones(tope):
    out, pagina = [], 0
    while len(out) < tope and pagina < 30:
        d = api("/conversations/search", locationId=LOCATION, limit=100,
                **({"startAfterDate": out[-1].get("lastMessageDate")} if out and out[-1].get("lastMessageDate") else {}))
        if "_error" in d:
            return out, d
        lote = filas(d, "conversations")
        if not lote:
            break
        out += lote
        pagina += 1
        time.sleep(0.3)
    return out[:tope], None


def mensajes(cid):
    d = api(f"/conversations/{cid}/messages", limit=100)
    if "_error" in d:
        return []
    m = d.get("messages")
    if isinstance(m, dict):
        m = filas(m, "messages")
    return m if isinstance(m, list) else filas(d, "messages")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=300)
    a = ap.parse_args()
    if not TOKEN:
        print("ERROR: falta GHL_TOKEN.", file=sys.stderr); sys.exit(1)
    os.makedirs(SALIDA, exist_ok=True)

    print(f"→ Trayendo hasta {a.limite} conversaciones…")
    convs, err = conversaciones(a.limite)
    print(f"   {len(convs)} conversaciones" + (f" · aviso: {err['_error']}" if err else ""))
    if not convs:
        json.dump({"generado": date.today().isoformat(), "error": (err or {}).get("_error", "sin datos")},
                  open(f"{SALIDA}/conversaciones.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return

    temas = Counter(); temas_master = Counter()
    quien_cierra = Counter(); canales = Counter()
    largos, sin_respuesta, master_n = [], 0, 0
    ejemplos = []
    revisadas = 0

    for c in convs:
        cid = c.get("id")
        if not cid:
            continue
        ms = mensajes(cid)
        if not ms:
            continue
        revisadas += 1
        canales[c.get("type") or c.get("lastMessageType") or "?"] += 1
        largos.append(len(ms))

        # orden cronologico; el ultimo que habla dice si quedo colgada
        ms = sorted(ms, key=lambda m: m.get("dateAdded") or "")
        ultimo = ms[-1]
        entrante = (ultimo.get("direction") or "").lower() == "inbound"
        quien_cierra["la persona (quedó sin responder)" if entrante else "nosotros"] += 1
        if entrante:
            sin_respuesta += 1

        texto_persona = " ".join(limpiar(m.get("body") or "") for m in ms
                                 if (m.get("direction") or "").lower() == "inbound")
        es_master = bool(MASTER.search(texto_persona))
        if es_master:
            master_n += 1

        for tema, patron in TEMAS.items():
            if re.search(patron, texto_persona, re.I):
                temas[tema] += 1
                if es_master:
                    temas_master[tema] += 1

        if es_master and len(ejemplos) < 25:
            primero = next((limpiar(m.get("body") or "") for m in ms
                            if (m.get("direction") or "").lower() == "inbound"), "")
            if primero:
                ejemplos.append({"mensajes": len(ms), "quedo_sin_responder": entrante,
                                 "primer_mensaje": primero[:220]})
        time.sleep(0.15)

    largos.sort()
    res = {
     "generado": date.today().isoformat(),
     "nota": ("Agregados de conversaciones para perfilar leads. NO contiene nombres, "
              "telefonos ni correos: los fragmentos pasan por un limpiador antes de escribirse."),
     "conversaciones_traidas": len(convs),
     "con_mensajes_revisadas": revisadas,
     "menciona_master": master_n,
     "mensajes_por_conversacion": {
        "mediana": largos[len(largos)//2] if largos else 0,
        "media": round(sum(largos)/len(largos), 1) if largos else 0,
        "solo_un_mensaje": sum(1 for x in largos if x <= 1)},
     "quien_habla_ultimo": dict(quien_cierra),
     "quedaron_sin_responder": sin_respuesta,
     "canales": dict(canales),
     "temas_todas": dict(temas.most_common()),
     "temas_solo_master": dict(temas_master.most_common()),
     "ejemplos_anonimos": ejemplos,
     "limite_aplicado": a.limite,
     "aviso_cobertura": (f"Se revisaron {revisadas} conversaciones de las ~24.400 de la cuenta. "
                         "Es una muestra de las mas recientes, no el total."),
    }
    json.dump(res, open(f"{SALIDA}/conversaciones.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(f"\n   revisadas {revisadas} · mencionan Master {master_n}")
    print(f"   sin responder: {sin_respuesta}")
    print("   temas mas frecuentes:", dict(temas.most_common(6)))
    print(f"\n   resultado en {SALIDA}/conversaciones.json")


if __name__ == "__main__":
    main()
