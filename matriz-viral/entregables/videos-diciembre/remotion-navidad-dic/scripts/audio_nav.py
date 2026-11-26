#!/usr/bin/env python3
"""Banda sonora de los reels de Navidad (van sin voz): la música de la casa generada por código
(plantillas/scripts/musica_energica.py; compás de 1,75 s = cada corte del reel) + efectos sintetizados aquí mismo
(whoosh en los cambios, pop en fichas, golpe en precios y sellos, ding en el CTA). Sale a −14 LUFS.
Uso: audio_nav.py [papeles|regalo|escondido ...] → audio/nav-<k>.wav"""
import subprocess, sys
import numpy as np
from comun import P, REPO, SR, rd, wr, loudnorm2, lufs
INTRO, BAR, COLA = 0.5, 1.75, 2.0
V = {  # igual que src/navs.ts: (tipo, compases, eventos relativos al inicio de la escena)
 'papeles': [('clip', 2, dict(golpe=[2.25])), ('clip', 2, dict(golpe=[1.75])), ('price', 2, {}), ('list', 3, {}), ('deadline', 2, {}), ('cta', 2, {})],
 'regalo': [('clip', 2, dict(golpe=[2.25])), ('clip', 2, dict(golpe=[1.75], pop=[0.9, 1.75])), ('price', 2, {}), ('list', 3, {}), ('deadline', 2, {}), ('cta', 2, {})],
 'escondido': [('clip', 2, dict(golpe=[2.25])), ('cal', 2, {}), ('clip', 2, dict(golpe=[1.75], pop=[1.0, 1.75])), ('list', 3, {}), ('cta', 2, {})],
}
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(d * SR)) / SR
def whoosh(d=0.42):
    t = tt(d); n = rng.standard_normal(len(t)); X = np.fft.rfft(n); f = np.fft.rfftfreq(len(t), 1 / SR)
    X *= (f / 900) / (1 + (f / 900) ** 2) * 2 / (1 + (f / 5000) ** 4); n = np.fft.irfft(X, len(t))
    env = np.sin(np.pi * (t / d) ** 0.7) ** 2
    return n / np.max(np.abs(n)) * env
def pop():
    t = tt(0.09); f = 520 + 520 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.025) * np.minimum(1, t / 0.002)
def golpe():
    t = tt(0.4); f = 48 + 90 * np.exp(-t / 0.04)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.13)
    x[:300] += rng.standard_normal(300) * np.linspace(0.5, 0, 300)
    return np.tanh(x * 1.5)
def ding():
    t = tt(1.2)
    return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, a, d in ((1318.5, 1, 0.38), (2637, 0.42, 0.22), (3955, 0.18, 0.12))) * np.minimum(1, t / 0.003)
SFX = dict(whoosh=(whoosh, 0.20), pop=(pop, 0.26), golpe=(golpe, 0.42), ding=(ding, 0.30))

for k in sys.argv[1:] or list(V):
    sc = V[k]; bars = sum(b for _, b, _ in sc); dur = INTRO + bars * BAR + COLA
    mus = f'{P}/audio/musica-{k}.wav'
    subprocess.run([sys.executable, f'{REPO}/plantillas/scripts/musica_energica.py', str(INTRO), str(bars), str(COLA), mus], check=True, capture_output=True)
    m = rd(mus); N = int(dur * SR); mix = np.zeros((N, 2)); mix[:min(N, len(m))] += m[:N] * 0.8
    ev = []; s = 0.0
    for i, (tp, b, e) in enumerate(sc):
        d = b * BAR + (INTRO if i == 0 else 0) + (COLA if i == len(sc) - 1 else 0)
        if i: ev.append(('whoosh', s - 0.14))
        for g in e.get('golpe', []): ev.append(('golpe', s + g))
        for g in e.get('pop', []): ev.append(('pop', s + g))
        if tp == 'price': ev += [('golpe', s + 22 / 30), ('pop', s + 34 / 30)]
        if tp == 'deadline': ev.append(('golpe', s + 9 / 30))
        if tp == 'cal': ev += [('pop', s + 24 / 30), ('golpe', s + 50 / 30)]
        if tp == 'list':
            n = 4; step = max(8, min(20, (round(d * 30) - 40) // n)); ev += [('pop', s + (16 + j * step) / 30) for j in range(n)]
        if tp == 'cta': ev.append(('ding', s + 14 / 30))
        s += d
    for name, at in ev:
        fn, g = SFX[name]; x = fn() * g; a = int(max(0, at) * SR); b = min(N, a + len(x)); mix[a:b] += x[:b - a, None]
    raw = f'{P}/audio/nav-{k}-raw.wav'; out = f'{P}/audio/nav-{k}.wav'
    wr(raw, mix / max(1.0, np.max(np.abs(mix)))); loudnorm2(raw, out, I=-14)
    print(k, f'{dur:.2f}s', len(ev), 'efectos', 'LUFS', lufs(out))
