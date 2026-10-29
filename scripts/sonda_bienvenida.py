#!/usr/bin/env python3
"""¿Quién envía la bienvenida «Soy el Supervisor Académico… tu pago quedó confirmado»?

Busca el mensaje en las conversaciones recientes y escribe solo metadatos
(fuente, usuario, workflow, fecha). Sin nombres, teléfonos ni correos.
"""
import json, os, re, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import ghl_auditoria_bot as g

PAT = re.compile(r"Supervisor Acad[eé]mico de Design Modeling|tu pago qued[oó] confirmado y ya activamos", re.I)
convs = g.conversaciones(int(os.environ.get("TOPE", "600")))
print("conversaciones revisadas:", len(convs))
hall, quien, wf, tags = [], Counter(), Counter(), Counter()
for c in convs:
    ms = g.lista(g.api(f"/conversations/{c['id']}/messages", limit=100), "messages")
    for m in ms:
        if m.get("direction") == "outbound" and PAT.search(m.get("body") or ""):
            meta = {k: v for k, v in m.items() if k not in ("body", "contactId", "conversationId", "locationId", "attachments", "id")}
            hall.append(meta)
            quien[(m.get("source"), m.get("userId"))] += 1
            for k in ("workflowId", "workflow_id"):
                if m.get(k): wf[m[k]] += 1
            if isinstance(m.get("meta"), dict):
                for k, v in m["meta"].items():
                    if "workflow" in k.lower(): wf[str(v)] += 1
    time.sleep(0.15)
print("mensajes encontrados:", len(hall))
print("por (source, userId):", dict(quien))
print("workflows:", dict(wf))
for h in hall[:8]:
    print(json.dumps(h, ensure_ascii=False, default=str)[:700])
for uid in {u for (_, u) in quien if u}:
    u = g.api(f"/users/{uid}")
    print("usuario", uid, "→", u.get("name") or u.get("firstName"), u.get("_error", ""))
w = g.api("/workflows/", locationId=g.LOCATION)
for x in g.lista(w, "workflows"):
    n = x.get("name") or ""
    if re.search(r"bienven|acceso|inscri|pago|onboard|supervisor|welcome", n, re.I) or x.get("id") in wf:
        print("workflow", x.get("id"), x.get("status"), "·", n)
