#!/usr/bin/env bash
set -e
CHROME_PATH=/opt/pw-browsers/chromium ./build.sh tutor-sfx
# voz encima de los efectos: efectos al 35 %, voz al 100 %, loudness -14 LUFS
ffmpeg -y -v error -i tutor-sfx.mp4 -i audio/vo.wav -filter_complex "[0:a]volume=0.35[s];[1:a]volume=1.0[v];[s][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart tutor-ia-pizarra.mp4
ffmpeg -y -v error -i tutor-ia-pizarra.mp4 -c:v libx264 -preset slow -b:v 2600k -pass 1 -an -f mp4 /dev/null
ffmpeg -y -v error -i tutor-ia-pizarra.mp4 -c:v libx264 -preset slow -b:v 2600k -pass 2 -c:a aac -b:a 128k -movflags +faststart tutor-ia-pizarra-movil.mp4
rm -f ffmpeg2pass*
echo LISTO; ls -la tutor-ia-pizarra*.mp4
