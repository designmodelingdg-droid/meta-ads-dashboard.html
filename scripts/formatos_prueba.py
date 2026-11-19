#!/usr/bin/env python3
"""Revisión mensual de los formatos en prueba: ¿generan interés, interacción y ventas?

    python3 scripts/formatos_prueba.py --mes 2026-11

Lee el bloque `formatos_prueba` de calendario-<mes>.json. Cada pieza se mide
contra la mediana de reels de los 90 días anteriores (matriz.json, Graph API).
La venta no está en Meta: sale de los campos `whatsapp_14d` y `ventas_14d` que
Ester anota por pieza desde GHL. Sin ese dato, el veredicto de venta queda
«sin dato» y el formato no puede entrar fijo.

Escribe matriz-viral/auditorias/<mes>-formatos-prueba.md.
"""
import argparse
import datetime
import json
import pathlib
import re
import statistics
import unicodedata

R = pathlib.Path(__file__).resolve().parent.parent
M = R / "matriz-viral" / "matriz"
MESES = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril", "05": "mayo", "06": "junio", "07": "julio",
         "08": "agosto", "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"}


def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", "", t).strip()


def inter(r):
    return 1000 * sum(r.get(k) or 0 for k in ("comentarios", "guardados", "shares")) / r["views"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", required=True)
    ap.add_argument("--hoy", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    hoy = datetime.date.fromisoformat(a.hoy)
    cal = json.load(open(M / f"calendario-{MESES[a.mes[5:]]}.json", encoding="utf-8"))
    fp = cal.get("formatos_prueba")
    if not fp:
        raise SystemExit(f"calendario de {a.mes} sin bloque formatos_prueba")
    reels = [r for r in json.load(open(M / "matriz.json", encoding="utf-8"))["reels"] if r.get("tipo") == "reel" and r.get("views")]
    G = {p["id"]: p for p in json.load(open(M / "guiones-completos.json", encoding="utf-8"))["piezas"]}

    desde = (hoy - datetime.timedelta(days=90)).isoformat()
    base = [r for r in reels if desde <= r["fecha"] <= hoy.isoformat()]
    med_v = statistics.median(r["views"] for r in base)
    med_i = statistics.median(inter(r) for r in base)
    med_c = statistics.median(1000 * (r.get("comentarios") or 0) / r["views"] for r in base)

    def buscar(pz):
        if pz.get("shortCode"):
            return next((r for r in reels if r.get("shortCode") == pz["shortCode"]), None)
        g = G.get(pz.get("id"))
        if not g:
            return None
        for txt in (g.get("caption"), g.get("hook")):
            k = norm(txt)[:28]
            if len(k) >= 15:
                hit = next((r for r in reels if norm(r.get("tema"))[:28] == k), None)
                if hit:
                    return hit
        return None

    o = [f"# Formatos en prueba · {MESES[a.mes[5:]]} {a.mes[:4]}", "",
         f"Revisión al {hoy.isoformat()}. Línea base: {len(base)} reels del {desde} al {hoy.isoformat()} · "
         f"mediana {med_v:,.0f} vistas · {med_i:.1f} interacciones por 1.000 · {med_c:.2f} comentarios por 1.000.", "",
         "Umbrales: interés = vistas ≥ 1,5× la mediana · interacción = interacciones/1.000 ≥ 2× la mediana y comentarios/1.000 ≥ la mediana · "
         "venta = ≥ 10 al WhatsApp o a la palabra en 14 días y ≥ 1 venta (dato de GHL que anota Ester).", ""]
    for f in fp["formatos"]:
        o += [f"## {f['formato']}", "", f"Estado de partida: {f.get('estado', '—')}", "",
              "| Pieza | Fecha | Días | Vistas | Interacc./1.000 | Coment./1.000 | WhatsApp 14 d | Ventas 14 d | Interés | Interacción | Venta |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        validas = []
        for pz in f["piezas"]:
            r = buscar(pz)
            if not r:
                o.append(f"| {pz['id']} | sin publicar o sin encontrar | | | | | | | | | |")
                continue
            dias = (hoy - datetime.date.fromisoformat(r["fecha"])).days
            i, c = inter(r), 1000 * (r.get("comentarios") or 0) / r["views"]
            s_int = r["views"] >= 1.5 * med_v
            s_inx = i >= 2 * med_i and c >= med_c
            w, v = pz.get("whatsapp_14d"), pz.get("ventas_14d")
            s_ven = None if w is None or v is None else (w >= 10 and v >= 1)
            sn = lambda x: "—" if x is None else ("sí" if x else "no")
            o.append(f"| {pz['id']} ({r.get('shortCode')}) | {r['fecha']} | {dias} | {r['views']:,} | {i:.1f} | {c:.2f} | "
                     f"{'—' if w is None else w} | {'—' if v is None else v} | {sn(s_int)} | {sn(s_inx)} | {'sin dato' if s_ven is None else sn(s_ven)} |")
            if dias >= 7:
                validas.append((s_int, s_inx, s_ven))
        if len(validas) < 2:
            ver = f"SIN DECISIÓN: {len(validas)} pieza(s) con 7 días o más; hacen falta 2."
        else:
            tres = sum(1 for x in validas if x[0] and x[1] and x[2])
            sin_venta = any(x[2] is None for x in validas)
            puntos = max(sum(1 for y in x if y) for x in validas)
            if tres >= 2:
                ver = "ENTRA FIJO: 3 de 3 en al menos 2 piezas."
            elif puntos <= 1:
                ver = "SALE: 0 o 1 de 3."
            elif sin_venta:
                ver = "FALTA EL DATO DE VENTA: Ester tiene que anotar whatsapp_14d y ventas_14d por pieza. Sin venta no entra fijo."
            else:
                ver = "SE REPITE una vez más con otro tema (2 de 3)."
        o += ["", f"**Veredicto:** {ver}", ""]
        if f.get("que_falta_saber"):
            o += [f"Qué falta saber: {f['que_falta_saber']}", ""]
    out = R / "matriz-viral" / "auditorias" / f"{a.mes}-formatos-prueba.md"
    out.write_text("\n".join(o) + "\n", encoding="utf-8")
    print("\n".join(o))
    print("→", out.relative_to(R))


if __name__ == "__main__":
    main()
