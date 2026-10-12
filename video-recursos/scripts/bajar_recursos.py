#!/usr/bin/env python3
"""Baja los recursos de diseño y video de DMA desde Google Drive.

Carpeta: PLANIFICACIONES INTERNAS / Contenido Adicional (921 archivos, ~7,4 GB).
Los archivos están compartidos por enlace, así que basta con curl; no hace falta token.

El manifiesto (ruta · id · tipo · tamaño) NO está en este repo, que es público: vive en el
Drive de Dayana, en esa misma carpeta, como «manifest-recursos-video.tsv». Se baja con el
conector de Google Drive y se pasa con --manifiesto.

    python3 video-recursos/scripts/bajar_recursos.py --manifiesto manifest.tsv                     # todo
    python3 video-recursos/scripts/bajar_recursos.py "Logos de Marcas" --manifiesto manifest.tsv   # filtro por ruta

Destino por defecto: ~/drive-recursos/Contenido Adicional/<ruta del manifiesto>.
Se puede volver a correr: lo que ya está con el tamaño correcto no se baja otra vez.
"""
import argparse, concurrent.futures as cf, csv, os, subprocess


ap = argparse.ArgumentParser()
ap.add_argument('filtro', nargs='?', default='')
ap.add_argument('--manifiesto', required=True, help='manifest-recursos-video.tsv bajado del Drive')
ap.add_argument('--dest', default=os.path.expanduser('~/drive-recursos/Contenido Adicional'))
ap.add_argument('--hilos', type=int, default=6)
a = ap.parse_args()

filas = [r for r in csv.reader(open(a.manifiesto, encoding='utf-8'), delimiter='\t') if len(r) >= 4 and a.filtro.lower() in r[0].lower()]
print(f'{len(filas)} archivos, {sum(int(r[3]) for r in filas) / 1e9:.2f} GB → {a.dest}')


def bajar(r):
    ruta, fid, _, tam = r[:4]
    dst = os.path.join(a.dest, ruta)
    if os.path.exists(dst) and str(os.path.getsize(dst)) == tam:
        return 'ya', ruta
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(['curl', '-sSL', '--retry', '3', '-o', dst,
                    f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'])
    ok = os.path.exists(dst) and str(os.path.getsize(dst)) == tam
    return ('ok' if ok else 'FALLA'), ruta


cuenta = {'ok': 0, 'ya': 0, 'FALLA': 0}
with cf.ThreadPoolExecutor(a.hilos) as ex:
    for estado, ruta in ex.map(bajar, filas):
        cuenta[estado] += 1
        if estado == 'FALLA':
            print('  FALLA:', ruta)
print(f"listo: {cuenta['ok']} bajados, {cuenta['ya']} ya estaban, {cuenta['FALLA']} fallas")
