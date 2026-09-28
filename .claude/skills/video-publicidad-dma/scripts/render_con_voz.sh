#!/usr/bin/env bash
# Render final con voz: lee cuándo empieza cada escena (window.__VO en scenes.js), monta audio/lN.wav
# en esos tiempos, renderiza el video con sus efectos y deja la voz encima.
# Uso (desde la carpeta del proyecto, con vo_times.mjs copiado ahí):  ./render_con_voz.sh nombre
set -e
NAME=${1:-video}
export CHROME_PATH=${CHROME_PATH:-/opt/pw-browsers/chromium}
node vo_times.mjs > vo_times.json
python3 - <<'EOF'
import json, subprocess
d = json.load(open('vo_times.json')); st, dur = d['vo'], d['dur']
ins, flt = [], []
for i, t in enumerate(st):
    ins += ['-i', f'audio/l{i+1}.wav']; ms = int(t * 1000)
    flt.append(f'[{i}:a]aresample=44100,adelay={ms}|{ms}[a{i}]')
flt.append(''.join(f'[a{i}]' for i in range(len(st))) + f'amix=inputs={len(st)}:normalize=0,apad=whole_dur={dur}[vo]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(flt), '-map', '[vo]', '-ac', '2', 'audio/vo.wav'], check=True)
print('voz montada:', len(st), 'frases ·', round(dur, 2), 's')
EOF
./build.sh "_$NAME-sfx"
# efectos al 35 %, voz al 100 %, volumen normalizado a -14 LUFS (redes)
ffmpeg -y -v error -i "_$NAME-sfx.mp4" -i audio/vo.wav -filter_complex \
  "[0:a]volume=0.35[s];[1:a]volume=1.0[v];[s][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart "$NAME.mp4"
ffmpeg -y -v error -i "$NAME.mp4" -c:v libx264 -preset slow -b:v 2600k -pass 1 -an -f mp4 /dev/null
ffmpeg -y -v error -i "$NAME.mp4" -c:v libx264 -preset slow -b:v 2600k -pass 2 -c:a aac -b:a 128k -movflags +faststart "$NAME-movil.mp4"
rm -f ffmpeg2pass* "_$NAME-sfx.mp4" "_$NAME-sfx-movil.mp4"
echo "LISTO: $NAME.mp4 · $NAME-movil.mp4 (esta es la que se manda por chat)"
