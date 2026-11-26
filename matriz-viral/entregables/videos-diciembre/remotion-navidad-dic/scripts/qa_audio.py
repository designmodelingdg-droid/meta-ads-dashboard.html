#!/usr/bin/env python3
"""Control de los empalmes: nivel de la voz justo en cada pausa recortada (si es alto, se cortó una palabra) y pausas que quedan."""
import json, glob, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from comun import P, rd
from islas import islas
for js in sorted(glob.glob(f'{P}/data/s*.json')):
    d = json.load(open(js)); sid = d['id']; x = rd(f'{P}/audio/{sid}-voz.wav')[:, 0]
    lv = []
    for e in d['empalmes']:
        a = int((e - 0.03) * 48000); seg = x[max(0, a):a + int(0.06 * 48000)]; lv.append(round(20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)))
    I = islas(f'{P}/audio/{sid}-voz.wav', min_sil=0.1); gaps = [round(I[i + 1][0] - I[i][1], 2) for i in range(len(I) - 1)]
    print(f"{sid}: empalmes {len(lv)} · nivel en el corte (dB) máx {max(lv) if lv else '-'} {lv} · pausa más larga que queda {max(gaps):.2f}s · pausas > 0,6 s: {sum(g > 0.6 for g in gaps)}")
