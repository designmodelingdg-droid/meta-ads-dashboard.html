#!/bin/bash
# fmt.sh entrada.png prefijo  → prefijo-1x1.jpg, -4x5.jpg, -9x16.jpg, -16x9.jpg (fondo desenfocado + original completo + sello DG|ATC)
IN=$1; P=$2; D=$(dirname $0)
convert -size 560x120 xc:none -fill 'rgba(255,255,255,0.94)' -draw "roundrectangle 0,0 559,119 60,60" $D/sello-bg.png
ffmpeg -v error -y -i $D/sello-bg.png -i $D/dg-color.png -i $D/atc-blk.png -filter_complex "[1]scale=-1:52[a];[2]scale=-1:50[b];[0][a]overlay=36:(H-h)/2[x];[x]drawbox=x=278:y=30:w=2:h=60:color=0x0D1E3A@0.35:t=fill[y];[y][b]overlay=300:(H-h)/2+2" $D/sello.png
for f in "1x1 1080 1080" "4x5 1080 1350" "9x16 1080 1920" "16x9 1920 1080"; do set -- $f; N=$1; W=$2; H=$3
 SY=$([ $N = 9x16 ] && echo $((H-420)) || echo $((H-150)))
 ffmpeg -v error -y -i "$IN" -i $D/sello.png -filter_complex "[0]split[a][b];[a]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,boxblur=30:3,eq=brightness=-0.03[bg];[b]scale=$W:$H:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[c];[1]scale=-1:$([ $W -gt 1500 ] && echo 96 || echo 84)[s];[c][s]overlay=W-w-40:$SY" -q:v 2 "$P-$N.jpg"
done
# 9x16 recortado (si XOFF está definido): llena el alto y recorta el ancho desde XOFF (fracción)
if [ -n "$XOFF" ]; then
 ffmpeg -v error -y -i "$IN" -i $D/sello.png -filter_complex "[0]scale=-2:1920[f];[f]crop=1080:1920:'(iw-1080)*$XOFF':0[c];[1]scale=-1:72[s];[c][s]overlay=30:420" -q:v 2 "$P-9x16.jpg"
fi
