"""Música original enérgica (sin copyright), sincronizada a los cortes del reel.

Cada unión dura 1,75 s = 1 compás de 4 tiempos → 137,14 BPM. Intro con subida durante la
portada, «drop» justo en la primera unión, cierre sobre el CTA.
Uso: python3 musica_energica.py <intro_s> <compases> <cola_s> <out.wav>
"""
import sys, wave
import numpy as np

SR = 44100
INTRO, BARS, COLA, OUT = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
BEAT = 1.75 / 4
DUR = INTRO + BARS * 4 * BEAT + COLA
L = int((DUR + 0.5) * SR)
rng = np.random.default_rng(11)
mix = np.zeros((L, 2))
side = np.ones(L)


def t(sec): return np.arange(int(sec * SR)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)


def add(x, at, gain=1.0, pan=0.0):
    s = int(at * SR)
    if s >= L: return
    e = min(L, s + len(x)); x = x[:e - s] * gain
    mix[s:e, 0] += x * (1 - pan) ** 0.5
    mix[s:e, 1] += x * (1 + pan) ** 0.5


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y


def saw(f, sec, det=0.0):
    tt = t(sec); ph = (f * (1 + det) * tt + rng.random()) % 1
    return 2 * ph - 1


def kick():
    tt = t(0.35); f = 45 + 110 * np.exp(-tt / 0.035)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.16)
    x[:200] += rng.standard_normal(200) * np.linspace(0.6, 0, 200)
    return np.tanh(x * 1.8)


def clap():
    tt = t(0.25); n = rng.standard_normal(len(tt))
    env = np.exp(-tt / 0.06)
    for d in (0.0, 0.011, 0.022):
        s = int(d * SR); env[s:s + 80] += 0.8
    x = np.diff(np.r_[0, n]) * env
    return x / np.max(np.abs(x))


def hat(open_=False):
    tt = t(0.18 if open_ else 0.05); n = rng.standard_normal(len(tt))
    x = np.diff(np.r_[0, np.diff(np.r_[0, n])]) * np.exp(-tt / (0.06 if open_ else 0.012))
    return x / np.max(np.abs(x))


def pluck(m, sec=0.32):
    tt = t(sec)
    x = sum(saw(hz(m), sec, d) for d in (-0.006, 0, 0.006)) / 3
    x = lowpass(x * np.exp(-tt / 0.09), 4200) + np.sin(2 * np.pi * hz(m + 12) * tt) * 0.25 * np.exp(-tt / 0.06)
    return x * np.minimum(1, tt / 0.003)


def pad(ms, sec):
    tt = t(sec)
    x = sum(saw(hz(m), sec, d) for m in ms for d in (-0.012, -0.004, 0.004, 0.012)) / (4 * len(ms))
    x = lowpass(x, 2200)
    env = np.minimum(1, tt / 0.04) * np.minimum(1, (sec - tt) / 0.08)
    return x * env


def bass(m, sec):
    tt = t(sec)
    x = saw(hz(m), sec) * 0.6 + np.sin(2 * np.pi * hz(m) * tt) * 0.8
    x = lowpass(x, 600)
    return np.tanh(x * 1.5) * np.minimum(1, tt / 0.005) * np.minimum(1, (sec - tt) / 0.02)


# progresión Am – F – C – G (raíces y acordes)
PROG = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [64, 67, 72]), (55, [67, 71, 74])]
# gancho del arpegio (semicorcheas por compás, grados sobre el acorde)
HOOK = [0, 2, 1, 2, 0, 2, 1, 3, 0, 2, 1, 2, 3, 2, 1, 2]

K, C, HC, HO = kick(), clap(), hat(), hat(True)

# ---- intro: subida durante la portada ----
tt = t(INTRO)
noise = rng.standard_normal(len(tt))
riser = np.diff(np.r_[0, noise]) * (tt / INTRO) ** 2.5 * 0.35
sweep = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / INTRO) ** 2) / SR) * (tt / INTRO) ** 2 * 0.15
add(riser + sweep, 0, 1.0)
for i in range(int(INTRO / (BEAT / 2))):  # redoble que acelera
    at = INTRO - (i + 1) * BEAT / 2
    if at >= 0: add(C * 0.25, at, 0.6)
add(pad(PROG[0][1], INTRO), 0, 0.35)

# ---- cuerpo ----
t0 = INTRO
for b in range(BARS):
    root, chord = PROG[b % 4]
    bs = t0 + b * 4 * BEAT
    for k in range(4):
        at = bs + k * BEAT
        add(K, at, 1.0)
        s = int(at * SR); e = min(L, s + int(0.22 * SR))
        side[s:e] = np.minimum(side[s:e], 0.35 + 0.65 * np.linspace(0, 1, e - s) ** 0.6)
        if k in (1, 3): add(C, at, 0.55, 0.05)
        add(HO, at + BEAT / 2, 0.22, 0.3)
        for h in (0.25, 0.75):
            add(HC, at + BEAT * h, 0.16, -0.3)
    # bajo en corcheas con octava
    for q in range(8):
        add(bass(root - 12 + (12 if q % 2 else 0), BEAT / 2 * 0.9), bs + q * BEAT / 2, 0.55)
    add(pad(chord, 4 * BEAT), bs, 0.28)
    for q in range(16):
        g = HOOK[q]
        m = chord[g] if g < 3 else chord[0] + 12
        add(pluck(m + 12 if b % 2 else m, 0.28), bs + q * BEAT / 4, 0.22, 0.25 if q % 2 else -0.25)
    if b == BARS - 1:
        add(np.sin(2 * np.pi * np.cumsum(np.full(int(0.5 * SR), 1)) / SR), 0, 0)

# ---- cola: acorde final + impacto ----
ce = t0 + BARS * 4 * BEAT
add(K, ce, 1.0)
add(pad([69, 72, 76, 81], COLA), ce, 0.4)
add(bass(45, min(COLA, 1.2)), ce, 0.6)
add(pluck(81, 0.6), ce, 0.3)

# sidechain al pad/bajo (aproximado sobre toda la mezcla excepto el bombo, que ya lo marca)
mix *= side[:, None] ** 0.6
fin = int(DUR * SR); fo = int(0.6 * SR)
mix[fin - fo:fin] *= np.linspace(1, 0, fo)[:, None]
mix[fin:] = 0
mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.6) * 0.9
mix = mix[:fin]
w = wave.open(OUT, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print("ok", round(DUR, 2), "s")
