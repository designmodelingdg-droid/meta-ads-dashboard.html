#!/bin/bash
# v2: pre-segmentos a 1188x2112@30 (sin zoom todavia; el zoom va despues de componer el fondo)
set -e
cd "$(dirname "$0")"

pre() { # nombre src inicio fin
  ffmpeg -y -v error -ss $3 -to $4 -i "$2" \
    -vf "fps=30,scale=1188:2112,setsar=1,format=yuv420p" \
    -c:v libx264 -crf 14 -preset fast -c:a aac -b:a 256k -ar 48000 -ac 2 "pre_$1.mp4"
  echo "pre_$1.mp4"
}

pre H1  valor6-hook.mov        0.000 1.600
pre H2a valor6-hook.mov        1.950 4.780
pre H2b valor6-hook.mov        4.780 6.756
pre D1  valor6-desarrollo.mov  0.300 4.100
pre D2a valor6-desarrollo.mov  4.400 6.450
pre D2b valor6-desarrollo.mov  6.450 10.000
pre D3  valor6-desarrollo.mov 10.300 14.100
pre C1  valor6-cta.mov         0.000 3.620
pre C2a valor6-cta.mov         3.950 5.420
pre C2b valor6-cta.mov         5.420 8.300
