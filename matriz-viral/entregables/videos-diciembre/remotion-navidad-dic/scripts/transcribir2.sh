#!/bin/bash
# tercera opinión con large-v3 → data/<id>.json campo whisper_l
cd "$(dirname "$0")/.."
PY=/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/videos-dic/work/venv/bin/python
sed 's/d\[.whisper.\] = words/d["whisper_l"] = words/' scripts/transcribir.py > out/tmp/transcribir_l.py
sed -i "s#P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#P = '$(pwd)'#" out/tmp/transcribir_l.py
$PY out/tmp/transcribir_l.py large-v3 "$@" 2>&1 | grep -v Warning
