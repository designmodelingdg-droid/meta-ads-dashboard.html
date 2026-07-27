#!/usr/bin/env python3
"""
Actualiza matriz.json con las métricas semanales pegadas a mano (IG/FB Insights).

Pensado para el periodo SIN Apify (hasta que el crédito se reinicie). Lee una
tabla en Markdown o TSV con las métricas de la semana, la cruza contra las
piezas ya registradas y:
  - actualiza las que ya existen (por id, shortCode o parecido de título),
  - agrega las nuevas con su eje/formato,
  - calcula el ranking de la semana y las señales para el brief.

Uso:
    python3 scripts/matriz_semanal.py semana.md            # aplica cambios
    python3 scripts/matriz_semanal.py semana.md --dry-run  # solo muestra

Columnas reconocidas (en cualquier orden, con o sin acentos):
    publicacion/post/titulo | vistas/views | alcance | interacciones
    me gusta/likes | comentarios | guardados | compartidos/shares
    visitas a perfil | nuevos seguidores | vistas en facebook | comentarios facebook
Filas de "Total" se ignoran.
"""
import json, os, re, sys, unicodedata, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIZ = os.path.join(ROOT, "matriz-viral", "matriz", "matriz.json")

# ---------- normalización ----------
def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()

COLS = {
    "titulo": ["publicacion", "post", "titulo", "pieza", "nombre"],
    "views": ["vistas", "views", "reproducciones"],
    "alcance": ["alcance", "cuentas alcanzadas", "alcance (cuentas)"],
    "interacciones": ["interacciones"],
    "likes": ["me gusta", "likes", "megusta"],
    "comentarios": ["comentarios", "comments"],
    "guardados": ["guardados", "guardado", "saves"],
    "shares": ["compartidos", "veces que se compartio", "shares"],
    "cuentas_con_interaccion": ["cuentas con interaccion"],
    "visitas_perfil": ["visitas a perfil", "visitas al perfil"],
    "nuevos_seguidores": ["nuevos seguidores"],
    "views_facebook": ["vistas en facebook", "views facebook", "facebook"],
    "comentarios_facebook": ["comentarios facebook", "comentarios en facebook"],
}

def match_col(header):
    h = norm(header)
    # 1) las columnas de Facebook se revisan PRIMERO (si no, "vistas en facebook"
    #    cae en "vistas" y se pisa el dato de Instagram)
    if "facebook" in h:
        return "comentarios_facebook" if "comentario" in h else "views_facebook"
    # 2) match exacto
    for key, alts in COLS.items():
        if any(h == a for a in alts):
            return key
    # 3) match por contención, priorizando el alias más largo (más específico)
    mejor, largo = None, 0
    for key, alts in COLS.items():
        for a in alts:
            if a in h and len(a) > largo:
                mejor, largo = key, len(a)
    return mejor

def to_int(v):
    if v is None: return None
    s = re.sub(r"[^\d]", "", str(v))
    return int(s) if s else None

# ---------- parseo de la tabla ----------
def parse_tabla(texto):
    filas = []
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    # detectar separador: markdown (|) o tabulaciones
    md = [l for l in lineas if l.count("|") >= 3]
    if md:
        celdas = [[c.strip() for c in l.strip().strip("|").split("|")] for l in md]
        celdas = [c for c in celdas if not all(re.fullmatch(r"-{2,}|:-*:?|-*", x) for x in c)]
    else:
        celdas = [l.split("\t") for l in lineas if "\t" in l]
    if not celdas:
        return []
    header = celdas[0]
    mapa = {i: match_col(h) for i, h in enumerate(header)}
    if "titulo" not in mapa.values():
        mapa[0] = "titulo"  # asumir que la 1ª columna es el título
    for fila in celdas[1:]:
        d = {}
        for i, val in enumerate(fila):
            k = mapa.get(i)
            if not k: continue
            d[k] = val.strip() if k == "titulo" else to_int(val)
        t = norm(d.get("titulo", ""))
        if not t or t.startswith("total") or "**total" in t:
            continue
        d["titulo"] = re.sub(r"\*+", "", d.get("titulo", "")).strip()
        filas.append(d)
    return filas

# ---------- cruce con la matriz ----------
def buscar(pieza_titulo, reels):
    t = norm(pieza_titulo)
    # 1) por id exacto (DM123)
    m = re.fullmatch(r"dm\d+", t)
    if m:
        for r in reels:
            if r["id"].lower() == t: return r
    # 2) por shortCode
    for r in reels:
        if r.get("shortCode") and norm(r["shortCode"]) == t: return r
    # 3) por parecido de tema/título
    cands = {}
    for r in reels:
        for campo in ("tema", "titulo", "hook"):
            v = r.get(campo)
            if v: cands.setdefault(norm(v), r)
    if not cands: return None
    best = difflib.get_close_matches(t, list(cands), n=1, cutoff=0.78)
    if best: return cands[best[0]]
    # 4) contención (solo si el título es largo y específico)
    for k, r in cands.items():
        if len(t) > 20 and (t in k or k in t): return r
    return None

CAMPOS = ["views","alcance","interacciones","likes","comentarios","guardados","shares",
          "cuentas_con_interaccion","visitas_perfil","nuevos_seguidores",
          "views_facebook","comentarios_facebook"]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        print(__doc__); sys.exit(1)
    texto = open(args[0], encoding="utf-8").read()
    fecha = os.environ.get("FECHA", "")  # opcional: FECHA=2026-08-04

    filas = parse_tabla(texto)
    if not filas:
        print("No se reconoció ninguna fila. Revisa el formato de la tabla."); sys.exit(1)

    d = json.load(open(MATRIZ, encoding="utf-8"))
    reels = d["reels"]
    maxid = max(int(r["id"][2:]) for r in reels if r["id"][2:].isdigit())

    actualizadas, nuevas = [], []
    for f in filas:
        r = buscar(f["titulo"], reels)
        datos = {k: f[k] for k in CAMPOS if f.get(k) is not None}
        if r:
            r.update(datos)
            r["fuente_metricas"] = f"Instagram/Facebook Insights (manual){' ' + fecha if fecha else ''}"
            actualizadas.append((r["id"], f["titulo"], f.get("views")))
        else:
            maxid += 1
            nueva = {"id": f"DM{maxid}", "shortCode": None, "cuenta": "design_modeling_dg",
                     "tipo": None, "eje": None, "fecha": fecha or None,
                     "tema": f["titulo"], "estructura": None, "hook": None,
                     "nota": "⟨pendiente⟩ revisar tipo/eje y añadir nota de lectura.",
                     "fuente_metricas": f"Instagram/Facebook Insights (manual){' ' + fecha if fecha else ''}",
                     "url": None, "reconciliar_shortcode": True}
            nueva.update(datos)
            reels.append(nueva)
            nuevas.append((nueva["id"], f["titulo"], f.get("views")))

    # ranking de la semana
    orden = sorted(filas, key=lambda x: -(x.get("views") or 0))
    print(f"\n=== SEMANA: {len(filas)} piezas ===")
    for i, f in enumerate(orden, 1):
        v = f.get("views") or 0
        c = f.get("comentarios") or 0
        g = f.get("guardados") or 0
        a = f.get("alcance") or 0
        eng = f" · interacc/alcance {round((f.get('interacciones') or 0)/a*100,1)}%" if a else ""
        fb = f" · FB {f['views_facebook']:,}" if f.get("views_facebook") else ""
        print(f"{i}. {f['titulo'][:45]:47} {v:>7,} views · {c:>3} comm · {g:>3} guard{eng}{fb}")
    tot_v = sum(f.get("views") or 0 for f in filas)
    top = orden[0]
    print(f"\nTotal semana: {tot_v:,} views")
    if tot_v:
        print(f"Ganador: “{top['titulo'][:45]}” con {(top.get('views') or 0)/tot_v*100:.0f}% de las vistas")
    ceros = [f["titulo"][:40] for f in filas if (f.get("comentarios") or 0) == 0]
    if ceros:
        print(f"⚠️ Sin comentarios ({len(ceros)}): " + " · ".join(ceros))
        print("   → revisar si cerraron con pregunta directa (regla comprobada).")

    print(f"\nActualizadas: {len(actualizadas)} | Nuevas: {len(nuevas)}")
    for i, t, v in actualizadas: print(f"  ~ {i}: {t[:40]} ({v:,})" if v else f"  ~ {i}: {t[:40]}")
    for i, t, v in nuevas:       print(f"  + {i}: {t[:40]} ({v:,}) ⟵ completar tipo/eje" if v else f"  + {i}: {t[:40]}")

    if dry:
        print("\n(--dry-run: no se escribió nada)"); return

    reels.sort(key=lambda r: (r.get("views") is None, -(r.get("views") or 0)))
    d["total_reels"] = len(reels)
    if fecha: d["generado"] = fecha
    json.dump(d, open(MATRIZ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n✓ matriz.json actualizado ({d['total_reels']} piezas)")

if __name__ == "__main__":
    main()
