#!/bin/bash
# Corta los segmentos hablados (sin silencios) con zoom in/out alternado, 1080x1920@30
set -e
cd "$(dirname "$0")"
MASTER=/home/user/dma-sales-assistant/tutor/videos/master-revit-ia-vertical-32s.mp4

seg() { # nombre archivo inicio fin zoom(in|out)
  local name=$1 src=$2 ss=$3 to=$4 dir=$5
  local dur=$(python3 -c "print($4-$3)")
  local N=$(python3 -c "print(round(($4-$3)*30))")
  local zexpr
  if [ "$dir" = "in" ]; then zexpr="min(1+0.09*on/$N,1.09)"; else zexpr="max(1.09-0.09*on/$N,1.001)"; fi
  ffmpeg -y -v error -ss $ss -to $to -i "$src" \
    -vf "fps=30,scale=1188:2112,zoompan=z='$zexpr':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p" \
    -c:v libx264 -crf 15 -preset fast -c:a aac -b:a 256k -ar 48000 -ac 2 "seg_$name.mp4"
  echo "seg_$name.mp4 dur=$dur"
}

seg H1 valor6-hook.mov        0.000 1.600 in
seg H2 valor6-hook.mov        1.950 6.756 out
seg D1 valor6-desarrollo.mov  0.300 4.100 in
seg D2 valor6-desarrollo.mov  4.400 10.000 out
seg D3 valor6-desarrollo.mov 10.300 14.100 in
seg C1 valor6-cta.mov         0.000 3.620 out
seg C2 valor6-cta.mov         3.950 8.300 in

# Placa final DMA (sin audio en el master -> pista silenciosa)
ffmpeg -y -v error -ss 30.0 -i "$MASTER" -f lavfi -i anullsrc=r=48000:cl=stereo -t 2.6 \
  -map 0:v -map 1:a -vf "fps=30,setsar=1,format=yuv420p" \
  -c:v libx264 -crf 15 -preset fast -c:a aac -b:a 256k "seg_PLATE.mp4"

# B-roll: clash (ambar) y resolucion ambar->verde
ffmpeg -y -v error -ss 20.5 -to 22.8 -i "$MASTER" -an -vf "fps=30,setsar=1,format=yuv420p" -c:v libx264 -crf 15 -preset fast broll1.mp4
ffmpeg -y -v error -ss 23.6 -to 26.4 -i "$MASTER" -an -vf "fps=30,setsar=1,format=yuv420p" -c:v libx264 -crf 15 -preset fast broll2.mp4

for f in seg_*.mp4 broll*.mp4; do
  printf "%s %s\n" "$f" "$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $f)"
done
