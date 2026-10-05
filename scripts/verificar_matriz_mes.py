#!/usr/bin/env python3
"""Revisa que la matriz de un mes cumpla las reglas antes de pasarla al equipo.

    python3 scripts/verificar_matriz_mes.py --mes 2026-10

Lee matriz-viral/matriz/calendario-<mes>.json, guiones-completos.json e
historico-2026.json. Imprime cada regla con OK / FALLA / AVISO y sale con
código 1 si alguna FALLA. No arregla nada: dice qué pieza y por qué.

Reglas (de COMPRADORES-VS-NO.md, HISTORICO-JUL-SEP.md y la casa):
  · todo id del calendario, de la pauta y de banco_reserva existe en guiones;
  · slides / historias / guion_reel son listas (la app de Daniela lo exige);
  · feed 40/40/20 de formato y 50/20/30 de intención (±10 puntos);
  · ninguna pieza de OBRA en el feed;
  · a lo sumo una venta por semana en historias;
  · ningún id ya usado y ningún gancho casi igual a uno ya usado;
  · las palabras de comentario están en la lista viva;
  · anuncios: primera línea ≤ 125 caracteres, «WhatsApp» solo con botón de WhatsApp;
  · el Máster nunca lleva precio; ACERO $225 solo en pauta y correo.
"""
import argparse
import json
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from historico_matriz import ya_usado  # noqa: E402

M = pathlib.Path("matriz-viral/matriz")
MESES = {"10": "octubre", "11": "noviembre", "12": "diciembre", "09": "septiembre"}
PALABRAS_VIVAS = {"NIVEL", "ACERO", "ZAPATA", "MEMORIA", "COTIZA", "DIPLOMADO", "BIM", "IA",
                  "GUIA"}  # GUIA: OpenReply, campaña «Guía Revit» (reel del Mié 7, cambio del 5-oct)
PRECIO_MASTER = re.compile(r"2[.,]?699|\$\s?499|\$\s?500\b|\$\s?160\b|12 cuotas", re.I)

resultado = {"FALLA": 0, "AVISO": 0}


def informe(estado, regla, detalle=""):
    if estado in resultado:
        resultado[estado] += 1
    print(f"[{estado:5}] {regla}" + (f"\n        {detalle}" if detalle else ""))


def texto(p):
    return json.dumps(p, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", required=True, help="AAAA-MM, p. ej. 2026-10")
    a = ap.parse_args()
    nombre = MESES.get(a.mes[5:7])
    cal = json.load(open(M / f"calendario-{nombre}.json", encoding="utf-8"))
    G = {p["id"]: p for p in json.load(open(M / "guiones-completos.json", encoding="utf-8"))["piezas"]}
    hist = json.load(open(M / "historico-2026.json", encoding="utf-8"))

    grupos = {g["n"]: [e for e in g["calendario"] if e.get("id")] for g in cal["grupos"]}
    ads = [x["id"] for c in cal.get("publicidad", {}).get("campanas", []) for x in c["piezas"]]
    ids = [e["id"] for es in grupos.values() for e in es] + ads + list(cal.get("banco_reserva", []))
    ids += [c["id"] for c in cal.get("correos", []) if c.get("id")]

    faltan = sorted({i for i in ids if i not in G})
    informe("FALLA" if faltan else "OK", "Todo id existe en guiones-completos.json", ", ".join(faltan))

    malas = [p["id"] for p in G.values() for k in ("slides", "historias", "guion_reel") if k in p and not isinstance(p[k], list)]
    informe("FALLA" if malas else "OK", "slides / historias / guion_reel son listas", ", ".join(malas))

    feed = cal["grupos"][0]["calendario"]
    n = len(feed)
    fmt = Counter("reel" if "REEL" in (e.get("formato_publicacion") or "").upper() else
                  "carrusel" if "CARRUSEL" in (e.get("formato_publicacion") or "").upper() else "post" for e in feed)
    pct = {k: round(100 * v / n) for k, v in fmt.items()}
    ok = abs(pct.get("reel", 0) - 40) <= 10 and abs(pct.get("carrusel", 0) - 40) <= 10 and abs(pct.get("post", 0) - 20) <= 10
    informe("OK" if ok else "FALLA", f"Feed 40/40/20 de formato ({n} piezas)", str(pct))

    inten = Counter("objeción/testimonio" if e.get("intencion") in ("objeción", "testimonio") else e.get("intencion") for e in feed)
    pi = {k: round(100 * v / n) for k, v in inten.items()}
    ok = abs(pi.get("problema", 0) - 50) <= 10 and abs(pi.get("solución", 0) - 20) <= 10 and abs(pi.get("objeción/testimonio", 0) - 30) <= 10
    informe("OK" if ok else "FALLA", "Feed 50/20/30 de intención", str(pi))

    obra = [e["id"] for e in feed if "OBRA" in str(G.get(e["id"], {}).get("eje", "")).upper()]
    informe("FALLA" if obra else "OK", "Cero piezas de OBRA en el feed", ", ".join(obra))

    ventas = Counter()
    for e in grupos.get(5, []):
        p = G.get(e["id"], {})
        if p.get("venta") or "VENTA" in str(p.get("tipo", "")).upper():
            ventas[e.get("semana")] += 1
    exceso = {k: v for k, v in ventas.items() if v > 1}
    informe("FALLA" if exceso else ("OK" if ventas else "AVISO"),
            "A lo sumo una venta por semana en historias", str(dict(ventas)) if ventas else "No hay historias marcadas como venta.")

    usados = set(hist["usados_ids"])
    rep = [i for i in ids if i in usados]
    informe("FALLA" if rep else "OK", "Ningún id ya usado en julio–septiembre", ", ".join(rep))
    parecidos = [e["id"] for e in feed if ya_usado(G.get(e["id"], {}).get("hook", ""), hist)]
    informe("AVISO" if parecidos else "OK", "Ningún gancho del feed casi igual a uno ya usado", ", ".join(parecidos))

    malas_pal = []
    for i in set(ids):
        p = G.get(i, {})
        for v in (p.get("cta") or {}).values() if isinstance(p.get("cta"), dict) else []:
            for w in re.findall(r"(?:[Cc]omenta|con)\s+«?([A-ZÁÉÍÓÚ]{2,})", str(v)):
                if w not in PALABRAS_VIVAS:
                    malas_pal.append(f"{i}: {w}")
    informe("FALLA" if malas_pal else "OK", "Palabras de comentario en la lista viva", "; ".join(sorted(set(malas_pal))))

    # Una palabra, una automatización (auditoría de septiembre: MEMORIA y DYNAMO
    # escuchadas a la vez por OpenReply y GHL, 34 DM fallidos).
    orp = json.load(open("matriz-viral/fuentes/openreply/campanas.json", encoding="utf-8")) if pathlib.Path("matriz-viral/fuentes/openreply/campanas.json").exists() else {}
    en_or = {p for c in orp.get("campanas", []) if c.get("activa") for p in c.get("palabras", [])}
    en_ghl = {p for p, w in ((orp.get("workflows_ghl") or {}).get("por_palabra") or {}).items() if w.get("publicados")}
    pedidas = set()
    for i in set(ids):
        for v in (G.get(i, {}).get("cta") or {}).values() if isinstance(G.get(i, {}).get("cta"), dict) else []:
            pedidas |= set(re.findall(r"(?:[Cc]omenta|con)\s+«?([A-ZÁÉÍÓÚ]{2,})", str(v)))
    dobles = sorted(p for p in pedidas if p in en_or and p in en_ghl)
    informe("AVISO" if dobles else "OK", "Cada palabra que pide el mes la contesta UNA sola automatización (OpenReply o GHL)",
            ("Montadas en las dos: " + ", ".join(dobles) + ". Dejar una antes de publicar.") if dobles else "")

    largas, wa = [], []
    for i in ads:
        p = G.get(i, {})
        primera = str(p.get("texto_principal", "")).split("\n")[0]
        if len(primera) > 125:
            largas.append(f"{i} ({len(primera)})")
        if "whatsapp" in str(p.get("texto_principal", "")).lower() and not re.search(r"whatsapp|mensaje", str(p.get("boton", "")), re.I):
            wa.append(i)
    informe("FALLA" if largas else "OK", "Anuncios: primera línea ≤ 125 caracteres", ", ".join(largas))
    informe("FALLA" if wa else "OK", "Anuncios: «WhatsApp» en el texto solo con botón de WhatsApp", ", ".join(wa))

    pm, acero = [], []
    for i in set(ids):
        p = G.get(i, {})
        t = texto({k: v for k, v in p.items() if k not in ("condicion", "notas_produccion", "por_que", "que_medir")})
        if PRECIO_MASTER.search(t):
            pm.append(i)
        if re.search(r"\$\s?225|225\s?(USD|dólares)", t) and p.get("formato") not in ("anuncio", "correo"):
            acero.append(i)
    informe("FALLA" if pm else "OK", "El Máster nunca lleva precio", ", ".join(sorted(pm)))
    informe("FALLA" if acero else "OK", "ACERO $225 solo en pauta y correo", ", ".join(sorted(acero)))

    print(f"\n{resultado['FALLA']} fallas · {resultado['AVISO']} avisos")
    sys.exit(1 if resultado["FALLA"] else 0)


if __name__ == "__main__":
    main()
