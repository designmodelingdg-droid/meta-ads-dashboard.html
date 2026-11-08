"""Baja tramos largos de clases de Vimeo (lecciones cortas del Campus).

Solo LEE de Vimeo. Los tramos salen en 720p a la carpeta tramos/ y la Action
los sube como artefacto (no se guardan en git).

    VIMEO_TOKEN=xxx python3 scripts/vimeo_tramos.py "01=1174402667@7:40-15:20;02a=..."
Cada tramo: nombre=video@desde-hasta, máximo 15 min.
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from vimeo_clips import api, elegir_archivo, a_segundos  # noqa: E402

def main(spec):
    os.makedirs('tramos', exist_ok=True)
    links = {}
    for parte in [p.strip() for p in spec.split(';') if p.strip()]:
        nombre, resto = parte.split('=')
        video, rango = resto.split('@')
        d, h = (a_segundos(x) for x in rango.split('-'))
        if not (0 <= d < h) or h - d > 900:
            sys.exit(f'ERROR en {nombre}: el tramo debe durar como mucho 15 min.')
        if video not in links:
            v = api(f'/videos/{video}?fields=name,download,files')
            link, alto = elegir_archivo(v)
            if not link:
                sys.exit(f'ERROR: Vimeo no da archivo descargable para {video}.')
            links[video] = link
            print(f'→ {video} «{v.get("name","")}» desde {alto}p')
        salida = f'tramos/{nombre}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{d:.2f}', '-to', f'{h:.2f}', '-i', links[video],
                        '-vf', 'scale=-2:720', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', salida],
                       check=True)
        print(f'  {nombre}: {os.path.getsize(salida)/1e6:.1f} MB')

if __name__ == '__main__':
    main(sys.argv[1])
