"""Busca silencios largos con la pantalla quieta en una clase de Vimeo (solo LEE).
Salida: whisper/<id>.sil.json = {"id","sil":[[inicio,fin,cambio_de_pantalla],...]}"""
import json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from vimeo_clips import api, elegir_archivo  # noqa: E402

def cuadro(f, t):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', f, '-frames:v', '1', '-vf', 'scale=320:180,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    if len(r) < 320 * 180:
        return None
    return np.frombuffer(r[:320 * 180], np.uint8).reshape(180, 320)[12:150].astype(int)

def main(vid):
    os.makedirs('whisper', exist_ok=True)
    v = api(f'/videos/{vid}?fields=name,duration,download,files')
    link, alto = elegir_archivo(v)
    if not link:
        sys.exit(f'ERROR: sin archivo descargable para {vid}')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', link, '-c', 'copy', '/tmp/v.mp4'], check=True)
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', '/tmp/v.mp4', '-vn', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11,silencedetect=noise=-33dB:d=12', '-f', 'null', '-'], capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    out = []
    for s, e in zip(ini, fin):
        d = e - s
        F = [cuadro('/tmp/v.mp4', s + 0.6 + i * (d - 1.2) / 4) for i in range(5)]
        if any(x is None for x in F):
            continue
        ch = max(float((abs(F[i] - F[0]) > 28).mean()) for i in range(1, 5))
        out.append([round(s, 2), round(e, 2), round(ch, 4)])
    json.dump({'id': vid, 'sil': out}, open(f'whisper/{vid}.sil.json', 'w'))
    print(f'{vid}: {len(out)} silencios, {sum(1 for x in out if x[2] < 0.006)} con pantalla quieta', flush=True)

if __name__ == '__main__':
    main(sys.argv[1])
