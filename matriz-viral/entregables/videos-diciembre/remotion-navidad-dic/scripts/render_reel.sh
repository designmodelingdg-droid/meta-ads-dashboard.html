#!/bin/bash
# render_reel.sh <corto> [<corto> ...] → out/final/<id>.mp4 (Remotion + audio/reel-<corto>.wav de armar_voz.py)
cd "$(dirname "$0")/.."; mkdir -p out/final out/v
for k in "$@"; do
  id=$(python3 -c "import json;print(json.load(open('reels/$k.json'))['id'])")
  npx remotion render src/index.ts reel-$k out/v/reel-$k.mp4 --muted --color-space=bt709 --crf=${CRF:-20} --concurrency=${CONC:-3} --log=error 2>&1 | grep -v "^$" | tail -3
  ffmpeg -loglevel error -y -i out/v/reel-$k.mp4 -i audio/reel-$k.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart out/final/$id.mp4
  ls -la out/final/$id.mp4 | awk '{print $5, $9}'
done
