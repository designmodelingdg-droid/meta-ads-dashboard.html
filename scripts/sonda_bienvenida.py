#!/usr/bin/env python3
"""Sonda temporal: qué integración envía qué. Solo metadatos y el inicio del texto de la academia."""
import os, re, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
import ghl_auditoria_bot as g

convs = g.conversaciones(int(os.environ.get("TOPE", "250")))
por_app, segundos, ej = Counter(), defaultdict(Counter), defaultdict(Counter)
for c in convs:
    for m in g.lista(g.api(f"/conversations/{c['id']}/messages", limit=60), "messages"):
        if m.get("direction") != "outbound" or not (m.get("body") or "").strip():
            continue
        app = ((m.get("meta") or {}).get("marketplace") or {}).get("appId") or "-"
        k = (m.get("source"), app)
        por_app[k] += 1
        t = m.get("dateAdded") or ""
        if len(t) > 18:
            segundos[k]["min%10=0 y seg<40" if t[15] == "0" and int(t[17:19]) < 40 else "otro"] += 1
        txt = re.sub(r"\s+", " ", g.limpiar(m.get("body"), [c.get("contactName"), c.get("firstName"), c.get("lastName")]))[:70]
        ej[k][txt] += 1
    time.sleep(0.15)
for k, n in por_app.most_common():
    print(n, k, dict(segundos[k]))
    for t, x in ej[k].most_common(12):
        print("    ", x, "·", t)
