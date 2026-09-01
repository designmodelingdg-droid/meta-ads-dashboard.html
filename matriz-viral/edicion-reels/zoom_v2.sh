#!/bin/bash
# Zoom in/out + snaps por segmento sobre los comp_ (fondo nuevo) o pre_ (pantalla real)
set -e
cd "$(dirname "$0")"

zf() { # nombre fuente z0 z1
  local name=$1 srcf=$2 z0=$3 z1=$4
  local N=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of default=noprint_wrappers=1:nokey=1 "$srcf")
  ffmpeg -y -v error -i "$srcf" \
    -vf "zoompan=z='$z0+($z1-$z0)*on/$N':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p" \
    -c:v libx264 -crf 15 -preset fast -c:a aac -b:a 256k "segf_$name.mp4"
  echo "segf_$name.mp4"
}

zf H1  comp_H1.mp4  1.00 1.06
zf H2a comp_H2a.mp4 1.06 1.00
zf H2b comp_H2b.mp4 1.12 1.16
zf D1  pre_D1.mp4   1.00 1.05
zf D2a pre_D2a.mp4  1.10 1.13
zf D2b pre_D2b.mp4  1.04 1.001
zf D3  pre_D3.mp4   1.00 1.06
zf C1  comp_C1.mp4  1.06 1.00
zf C2a comp_C2a.mp4 1.00 1.03
zf C2b comp_C2b.mp4 1.12 1.16

for f in segf_*.mp4; do
  printf "%s %s\n" "$f" "$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $f)"
done
