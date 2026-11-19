#!/usr/bin/env python3
"""Sonido del marcador y de las páginas a partir de la línea de tiempo de la pizarra.

    node dump.js > els.json          # ELS, PAGE_START y TOTAL de escenas-*.ts (ver README)
    python3 sfx_desde_escenas.py els.json > sfx.json
    python3 sfx_mix.py <duración> sfx.wav            # sfx_mix.py de video-publicidad-dma/assets/pizarra
    ffmpeg -i voz.wav -i sfx.wav -filter_complex "[1]volume=0.45,aformat=channel_layouts=stereo[s];[0][s]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89" mezcla.wav
"""
import json, sys
d = json.load(open(sys.argv[1]))
ev = sorted([e for e in d["els"] if e["k"] != "fill" and e["t0"] >= 0.3], key=lambda e: e["t0"])
tramos = []
for e in ev:  # trazos seguidos = un solo sonido de marcador
    a, b = e["t0"], e["t0"] + e["dur"]
    if tramos and a - tramos[-1][1] < 0.1:
        tramos[-1][1] = max(tramos[-1][1], b)
    else:
        tramos.append([a, b])
S = [{"name": "scr_marker", "t": round(a, 3), "dur": round(b - a, 3), "gain": 0.55} for a, b in tramos]
S += [{"name": "paper", "t": round(p, 3), "gain": 0.8} for p in d["pages"][1:]]
cta = [e for e in d["els"] if e["k"] == "text" and e["scene"] == max(x["scene"] for x in d["els"])]
if len(cta) > 1:
    S.append({"name": "ding", "t": round(cta[1]["t0"] + 0.1, 3), "gain": 0.5})
json.dump(S, sys.stdout)
