#!/usr/bin/env bash
# Voz sintética en español (Piper, es_MX-claude-high) frase por frase, y verificación con Whisper.
# Uso (desde la carpeta del proyecto):  ./voz.sh audio/guion.txt
#   guion.txt = una frase por línea, una línea por escena.
#   Deja audio/l1.wav … lN.wav, audio/duraciones.txt y audio/verificacion.txt (lo que entendió Whisper).
set -e
GUION=${1:-audio/guion.txt}
VOCES=${VOCES:-$HOME/.cache/piper-voces}
VOZ=${VOZ:-es_MX-claude-high}
mkdir -p "$VOCES" audio
python3 -c "import piper" 2>/dev/null || pip install -q piper-tts
if [ ! -f "$VOCES/$VOZ.onnx" ]; then
  B=https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX
  case $VOZ in
    es_MX-claude-high) R=claude/high ;;
    es_MX-ald-medium)  R=ald/medium ;;
    *) echo "Voz no prevista: $VOZ"; exit 1 ;;
  esac
  curl -sSL -o "$VOCES/$VOZ.onnx" "$B/$R/$VOZ.onnx"
  curl -sSL -o "$VOCES/$VOZ.onnx.json" "$B/$R/$VOZ.onnx.json"
fi
: > audio/duraciones.txt
i=0
while IFS= read -r line || [ -n "$line" ]; do
  [ -z "$line" ] && continue
  i=$((i+1))
  echo "$line" | python3 -m piper -m "$VOCES/$VOZ.onnx" --length-scale 0.95 --sentence-silence 0.25 -f "audio/l$i.wav" 2>/dev/null
  printf "%.2f\n" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "audio/l$i.wav")" >> audio/duraciones.txt
done < "$GUION"
echo "Duraciones (pégalas en VOD de scenes.js):"; paste -sd, audio/duraciones.txt
python3 -c "import faster_whisper" 2>/dev/null || pip install -q faster-whisper
python3 - "$i" <<'EOF' | tee audio/verificacion.txt
import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
for k in range(1, int(sys.argv[1]) + 1):
    segs, _ = m.transcribe(f"audio/l{k}.wav", language="es")
    print(k, " ".join(s.text.strip() for s in segs))
EOF
echo "Revisa verificacion.txt: si una palabra sale mal (p. ej. «BIM» → «Benjamin»), escríbela como suena en guion.txt y repite."
