#!/bin/bash
# render_nav.sh papeles regalo escondido → out/final/nav-…-reel.mp4 (video de Remotion + banda sonora de audio_nav.py)
cd "$(dirname "$0")/.."; mkdir -p out/final out/v
declare -A NOMBRE=( [papeles]=nav-lanzamiento-papeles-reel [regalo]=nav-regalo-reel [escondido]=nav-equipo-escondido-reel )
for k in "$@"; do
  npx remotion render src/index.ts nav-$k out/v/nav-$k.mp4 --muted --color-space=bt709 --crf=19 --concurrency=${CONC:-3} --log=error 2>&1 | grep -v "^$" | tail -3
  ffmpeg -loglevel error -y -i out/v/nav-$k.mp4 -i audio/nav-$k.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart out/final/${NOMBRE[$k]}.mp4
  ls -la out/final/${NOMBRE[$k]}.mp4
done
