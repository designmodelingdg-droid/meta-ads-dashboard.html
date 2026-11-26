"""Islas de voz por energía (para comprobar que cada palabra del subtítulo cae donde de verdad se habla)."""
import numpy as np
from comun import rd
def islas(path, thr=-42, min_sil=0.14, min_isla=0.1, hop=0.01, win=0.03):
    x = rd(path)[:, 0]; h = int(hop * 48000); w = int(win * 48000)
    n = (len(x) - w) // h
    db = np.array([20 * np.log10(np.sqrt((x[i * h:i * h + w] ** 2).mean()) + 1e-9) for i in range(n)])
    on = db > thr; out = []; i = 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            out.append([i * hop, j * hop + win]); i = j
        else: i += 1
    m = []
    for a, b in out:
        if m and a - m[-1][1] < min_sil: m[-1][1] = b
        else: m.append([a, b])
    return [(round(a, 2), round(b, 2)) for a, b in m if b - a >= min_isla]
