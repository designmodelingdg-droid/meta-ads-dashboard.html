#!/usr/bin/env python3
"""Abre en lectura (solo con el ID) un almacén de Apify propio, para bajar desde la sesión
los videos que guardó un actor (p. ej. TikTok). No gasta crédito.

    python3 scripts/apify_acceso.py matriz-viral/pedidos/apify-acceso.json
Pedido: {"key_value_stores": ["<id>", ...], "acceso": "ANYONE_WITH_ID_CAN_READ"}
"""
import json, os, pathlib, sys, urllib.request, urllib.error

TOKEN = os.environ.get("APIFY_TOKEN", "").strip()
ped = json.loads(pathlib.Path(sys.argv[1]).read_text())
for sid in ped["key_value_stores"]:
    req = urllib.request.Request(f"https://api.apify.com/v2/key-value-stores/{sid}?token={TOKEN}", method="PUT",
                                 data=json.dumps({"generalAccess": ped["acceso"]}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode())["data"]
            print(sid, "→", d.get("generalAccess"))
    except urllib.error.HTTPError as e:
        print(sid, "HTTP", e.code, e.read().decode()[:200])
