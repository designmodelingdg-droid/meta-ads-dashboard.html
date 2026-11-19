#!/usr/bin/env python3
"""Suma piezas nuevas a guiones-completos.json con el formato que lee la app.

    python3 scripts/sumar_piezas.py archivo1.json [archivo2.json ...] [--nota "texto"] [--reemplazar]

Cada archivo trae {"piezas": [...]}. Se normaliza cada pieza igual que las de
octubre que ya están en la app:
  · formato corto (carrusel/reel/post/historias/mensaje/linkedin/blog/correo) y
    el largo en formato_detalle;
  · red_principal y cta_por_red si faltan;
  · guion [[tiempo, plano, voz, pantalla]] → guion_reel [{tiempo, accion, voz}];
  · condicion → notas_produccion si falta.
Una pieza con un id que ya existe se salta, salvo con --reemplazar.
Al final comprueba la regla de la app: slides / historias / guion_reel son listas.
"""
import copy
import json
import pathlib
import sys

G = pathlib.Path("matriz-viral/matriz/guiones-completos.json")
CORTOS = ("carrusel", "reel", "historias", "historia", "post", "mensaje", "linkedin", "blog", "correo", "anuncio")


def normalizar(p):
    q = copy.deepcopy(p)
    f = str(p.get("formato", ""))
    low = f.lower()
    corto = next((c for c in CORTOS if c in low), low)
    q["formato"] = "historias" if corto == "historia" else corto
    q.setdefault("formato_detalle", f if f.lower() != q["formato"] else f.upper())
    redes = p.get("redes") or []
    q.setdefault("red_principal", redes[0] if redes else "instagram")
    q.setdefault("cta_por_red", p.get("cta", {}))
    if "guion" in p and not p.get("guion_reel") and isinstance(p["guion"], list) and p["guion"] and isinstance(p["guion"][0], list):
        q["guion_reel"] = [{"tiempo": r[0], "accion": f"{r[1]} · En pantalla: {r[3]}" if len(r) > 3 else r[1],
                            "voz": r[2] if len(r) > 2 else ""} for r in p["guion"]]
    if p.get("condicion"):
        q.setdefault("notas_produccion", p["condicion"])
    return q


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    reemplazar = "--reemplazar" in sys.argv
    nota = sys.argv[sys.argv.index("--nota") + 1] if "--nota" in sys.argv else None
    if nota in args:
        args.remove(nota)
    g = json.load(open(G, encoding="utf-8"))
    por_id = {p["id"]: i for i, p in enumerate(g["piezas"])}
    nuevas = saltadas = cambiadas = 0
    for a in args:
        for p in json.load(open(a, encoding="utf-8"))["piezas"]:
            q = normalizar(p)
            if q["id"] in por_id:
                if reemplazar:
                    g["piezas"][por_id[q["id"]]] = q
                    cambiadas += 1
                else:
                    saltadas += 1
                continue
            por_id[q["id"]] = len(g["piezas"])
            g["piezas"].append(q)
            nuevas += 1
    g["total"] = len(g["piezas"])
    if nota:
        g["nota_octubre"] = (g.get("nota_octubre", "") + " " + nota).strip()
    malas = [p["id"] for p in g["piezas"] for k in ("slides", "historias", "guion_reel") if k in p and not isinstance(p[k], list)]
    if malas:
        raise SystemExit(f"NO se guarda: estas piezas traen slides/historias/guion_reel que no son lista: {malas}")
    json.dump(g, open(G, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok · {nuevas} nuevas · {cambiadas} reemplazadas · {saltadas} ya existían · total {g['total']}")


if __name__ == "__main__":
    main()
