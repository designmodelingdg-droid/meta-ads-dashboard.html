#!/usr/bin/env python3
"""Saca del cuerpo de cada clip el fotograma real de la portada (sin las franjas de relleno) y el primer fotograma.
Uso: portadas.py → public/clip/<id>-cover.jpg y <id>-f0.jpg (los tiempos están en data/<id>.json: portada.t)"""
import json, glob, os, subprocess
import numpy as np
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for js in sorted(glob.glob(f'{P}/data/*.json')):
    d = json.load(open(js)); sid = d['id']
    if 'portada' not in d: continue
    body = f'{P}/public/clip/{sid}.mp4'
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(d['portada']['t']), '-i', body, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(760, 1000, 3).astype(int)
    pad = (np.abs(im - np.array([13, 30, 58])).sum(2) < 40)
    rows = np.where(pad.mean(1) < 0.9)[0]; cols = np.where(pad.mean(0) < 0.9)[0]
    y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(d['portada']['t']), '-i', body, '-frames:v', '1', '-vf', f'crop={x1 - x0}:{y1 - y0}:{x0}:{y0}', '-q:v', '2', f'{P}/public/clip/{sid}-cover.jpg'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', body, '-frames:v', '1', '-q:v', '2', f'{P}/public/clip/{sid}-f0.jpg'], check=True)
    print(sid, 'portada', x1 - x0, 'x', y1 - y0)
