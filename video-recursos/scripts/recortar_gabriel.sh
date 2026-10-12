#!/usr/bin/env bash
# Recorta a Gabriel de un video vertical (1080x1920) y deja un WebM VP9 con transparencia,
# para el estilo 8a «Gabriel + motion graphics» (gráficas detrás de él).
#   bash video-recursos/scripts/recortar_gabriel.sh gabriel_editado.mp4 gabriel_fg.webm
# Requiere: pip install --break-system-packages "rembg[cpu]"  (el modelo u2net_human_seg baja de GitHub)
# Tarda ~1,5 s por fotograma con dos procesos: un video de 34 s, unos 25-30 min. Correrlo en segundo plano.
set -euo pipefail
IN="$1"; OUT="$2"; W="$(mktemp -d)"
mkdir -p "$W/fr" "$W/mask"
ffmpeg -v error -y -i "$IN" -vf "scale=540:960" "$W/fr/%05d.png"
cat > "$W/mask.py" <<'PY'
import os, sys
from rembg import remove, new_session
from PIL import Image
w, k, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
s = new_session('u2net_human_seg')
for i, f in enumerate(sorted(os.listdir(f'{w}/fr'))):
    if i % n != k or os.path.exists(f'{w}/mask/{f}'):
        continue
    remove(Image.open(f'{w}/fr/{f}'), session=s, only_mask=True).save(f'{w}/mask/{f}')
PY
python3 "$W/mask.py" "$W" 0 2 & python3 "$W/mask.py" "$W" 1 2 & wait
ffmpeg -v error -y -i "$IN" -framerate 30 -i "$W/mask/%05d.png" -filter_complex \
  "[1:v]scale=1080:1920:flags=bicubic,format=gray,gblur=sigma=1.6,lutyuv=y='clip((val-30)*1.25,0,255)'[m];[0:v]format=yuva420p[v];[v][m]alphamerge[o]" \
  -map "[o]" -an -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 6M -deadline good -cpu-used 4 -row-mt 1 "$OUT"
echo "listo: $OUT  (en Remotion: <OffthreadVideo src=... transparent />)"
