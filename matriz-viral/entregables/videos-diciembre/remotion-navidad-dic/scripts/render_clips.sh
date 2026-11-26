#!/bin/bash
# render_clips.sh <id> [id ...] → out/final/<id>.mp4 (Remotion + audio de audio_clip.py) y out/final/<id>-portada.jpg
cd "$(dirname "$0")/.."; mkdir -p out/final out/v
for id in "$@"; do
  npx remotion render src/index.ts clip-$id out/v/$id.mp4 --muted --color-space=bt709 --crf=${CRF:-20} --concurrency=${CONC:-4} --log=error 2>&1 | grep -v "^$" | tail -3
  ffmpeg -loglevel error -y -i out/v/$id.mp4 -i audio/$id.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart out/final/$id.mp4
  npx remotion still src/index.ts portada-$id out/final/$id-portada.jpg --image-format=jpeg --jpeg-quality=93 --log=error 2>&1 | grep -v "^$" | tail -2
  ls -la out/final/$id.mp4 out/final/$id-portada.jpg | awk '{print $5, $9}'
done
