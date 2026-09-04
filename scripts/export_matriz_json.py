#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vuelca la matriz de septiembre entera a UN solo JSON.

    python3 scripts/export_matriz_json.py

Por que existe: el mes se escribe repartido en cinco archivos —el calendario en
JSON, los guiones en JSON, y las historias, los reels y los lead magnets en
Python, porque llevan texto largo que en JSON es ilegible de editar—. Eso esta
bien para trabajar, pero mal para entregar: quien recibe el mes quiere un
archivo, no cinco y una explicacion.

Esto no es una copia paralela que haya que mantener a mano: se genera de los
mismos archivos que alimentan el artefacto y el Word, asi que los tres siempre
dicen lo mismo. Si algo cambia, se vuelve a correr y ya.
"""
import importlib.util
import json
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MATRIZ = RAIZ / "matriz-viral" / "matriz"
SALIDA = RAIZ / "matriz-viral" / "entregables" / "matriz-septiembre-2026-COMPLETA.json"


def cargar(nombre):
    spec = importlib.util.spec_from_file_location(nombre, MATRIZ / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CAL = json.loads((MATRIZ / "calendario-septiembre.json").read_text(encoding="utf-8"))
GUI = json.loads((MATRIZ / "guiones-completos.json").read_text(encoding="utf-8"))
H = cargar("historias-septiembre")
R = cargar("reels-septiembre")
LM = cargar("leadmagnets-septiembre")

POR_ID = {p["id"]: p for p in GUI["piezas"]}


def con_guion(entrada):
    """Cada entrada del calendario sale con su contenido pegado dentro.

    En los archivos de trabajo el calendario guarda solo un id y el contenido
    vive aparte; aqui se juntan, porque quien abra este archivo no tiene por
    que resolver referencias a mano para leer un post.
    """
    e = dict(entrada)
    p = POR_ID.get(entrada.get("id"))
    if p:
        e["contenido"] = p
    return e


datos = {
    "_meta": {
        "titulo": "Matriz de contenido — Design Modeling Academy — septiembre 2026",
        "periodo": "lunes 7 de septiembre a viernes 2 de octubre de 2026",
        "generado": date.today().isoformat(),
        "origen": "matriz-viral/matriz/ (calendario + guiones + historias + reels + lead magnets)",
        "como_se_regenera": "python3 scripts/export_matriz_json.py",
        "artefacto": "https://claude.ai/code/artifact/fe162f8b-0441-46b3-8bb7-0f404ae3590f",
        "que_contiene": {
            "reglas_del_mes": "las 13 reglas que no se rompen, incluida la de precios",
            "checklist_tareas": "las tareas del mes con lo que desbloquea cada una",
            "grupos": "los 5 grupos con su calendario y el contenido de cada pieza pegado dentro",
            "historias": "80 historias, 4 al dia de lunes a viernes, con prompt de imagen",
            "reels": "los guiones segundo a segundo de los reels de feed",
            "publicidad": "los 10 anuncios con copy aprobado y ficha de montaje",
            "lead_magnets": "los 3 recursos nuevos, su post de lanzamiento y el montaje en GHL",
            "correos": "los correos del mes",
        },
    },
    "reglas_del_mes": CAL["reglas_del_mes"],
    "checklist_tareas": CAL.get("checklist_tareas", []),
    "grupos": [
        {**{k: v for k, v in g.items() if k != "calendario"},
         "calendario": [con_guion(x) for x in g.get("calendario", [])]}
        for g in CAL["grupos"]
    ],
    "historias": {
        "medida": H.MEDIDA,
        "semanas": H.SEMANAS,
    },
    "reels_de_feed": {
        "guiones": [{**r, "guion": [list(t) for t in r["guion"]]} for r in R.REELS],
        "prompts_de_imagen": {k: {"medida": v[0], "prompt": v[1]}
                              for k, v in R.FEED_PROMPTS.items()},
    },
    "publicidad": CAL["publicidad"],
    "lead_magnets": {
        "regla": LM.REGLA,
        "resumen_en_calendario": CAL.get("lead_magnets", {}),
        "recursos": [{**m, "ghl": [list(x) for x in m["ghl"]]} for m in LM.MAGNETS],
        "montaje_ghl": [list(x) for x in LM.PASOS_GHL],
        "incidente_conocido": LM.INCIDENTE,
        "prueba_punta_a_punta": LM.CHECKLIST,
    },
    "correos": CAL.get("correos", []),
    "artefactos": CAL.get("artefactos", {}),
}

SALIDA.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
kb = SALIDA.stat().st_size / 1024
piezas = sum(len(g["calendario"]) for g in datos["grupos"])
hist = sum(len(d["historias"]) for s in H.SEMANAS for d in s["dias"])
anuncios = sum(len(c["piezas"]) for c in datos["publicidad"]["campanas"])
print(f"OK → {SALIDA.relative_to(RAIZ)} ({kb:.0f} KB)")
print(f"   {piezas} piezas en 5 grupos · {hist} historias · {len(datos['reels_de_feed']['guiones'])} "
      f"guiones de reel · {anuncios} anuncios · {len(datos['lead_magnets']['recursos'])} lead magnets")
