#!/bin/bash
# hoja.sh <composición> [n_columnas] [props.json] → out/prev/<comp>.mp4 (escala 0,4) y out/prev/<comp>.jpg (hoja de contacto, 1 fotograma por segundo)
cd "$(dirname "$0")/.."; mkdir -p out/prev
C=$1; N=${2:-9}; PR=""; [ -n "$3" ] && PR="--props=$3"
O=out/prev/${4:-$C}
npx remotion render src/index.ts $C $O.mp4 --scale=0.4 --crf=28 --muted --concurrency=4 --log=error $PR 2>&1 | grep -v "^$" | tail -3
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $O.mp4); R=$(python3 -c "import math;print(math.ceil(math.ceil($D)/$N))")
ffmpeg -v error -y -i $O.mp4 -vf "fps=1,tile=${N}x${R}" -frames:v 1 -q:v 3 $O.jpg; echo "$O.jpg ($D s)"
