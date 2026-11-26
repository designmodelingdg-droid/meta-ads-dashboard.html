#!/usr/bin/env python3
"""Audio de los clips con voz (shorts y fragmentos de clase): voz normalizada + música de la casa por debajo.
Música: plantillas/scripts/musica_original.py (lo-fi generado por código, sin reclamos), 18,5 dB por debajo de la voz mientras se habla
y más alta en la portada y el cierre. Mezcla final a −14 LUFS en dos pasadas (no cambia el balance).
Uso: audio_clip.py <id> [id ...] → audio/<id>.wav"""
import json, subprocess, sys
import numpy as np
from comun import P, REPO, SR, rd, wr, run, lufs, loudnorm2
PRE = 0.5; BAJO_VOZ = 18.5; SIN_VOZ = 8.0
for sid in sys.argv[1:]:
    d = json.load(open(f'{P}/data/{sid}.json')); fin = d['fin']; post = d.get('post') or (4.0 if d['kind'] == 'clase' else 1.8); total = PRE + fin + post
    movida = d.get('musica') == 'energica'; BAJO_VOZ = 18.0 if movida else 18.5; SIN_VOZ = 9.0 if movida else 8.0
    vz = f'{P}/out/tmp/{sid}-vz.wav'
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{P}/audio/{sid}-voz.wav', '-t', f'{fin:.3f}', '-af',
         f'highpass=f=70,afade=t=in:d=0.03,afade=t=out:st={fin - 0.16:.3f}:d=0.16', '-ar', str(SR), vz])
    vn = f'{P}/out/tmp/{sid}-vn.wav'; loudnorm2(vz, vn, I=-16, TP=-2, LRA=11)
    v = rd(vn); lv = lufs(vn)
    mus = f'{P}/audio/musica-{"energica" if movida else "lofi"}-{sid}.wav'
    if movida:   # música movida de la casa (plantillas/scripts/musica_energica.py): la subida cae en la portada y el «drop» al empezar la clase
        import math
        subprocess.run([sys.executable, f'{REPO}/plantillas/scripts/musica_energica.py', f'{PRE:.2f}', str(math.ceil((fin + post) / 1.75)), '1.0', mus], check=True, capture_output=True)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', mus, '-ar', str(SR), '-ac', '2', mus.replace('.wav', '-48.wav')], check=True); mus = mus.replace('.wav', '-48.wav')
    else: subprocess.run([sys.executable, f'{REPO}/plantillas/scripts/musica_original.py', f'{total + 0.5:.2f}', mus], check=True, capture_output=True)
    m = rd(mus); lm = lufs(mus); N = int(total * SR); m = m[:N]
    g = 10 ** ((lv - BAJO_VOZ - lm) / 20)
    t = np.arange(N) / SR
    up = 10 ** ((BAJO_VOZ - SIN_VOZ) / 20)                       # portada y cierre: la música sube
    env = 1 + (up - 1) * (np.clip((PRE + 0.05 - t) / 0.35, 0, 1) + np.clip((t - (PRE + fin - 0.1)) / 0.45, 0, 1))
    fo = np.clip((total - t) / 0.7, 0, 1)                         # salida al final del cierre
    mm = m * g * env[:, None] * fo[:, None]
    mix = mm.copy(); a = int(PRE * SR); mix[a:a + len(v)] += v[:N - a]
    raw = f'{P}/out/tmp/{sid}-mix.wav'; wr(raw, mix); out = f'{P}/audio/{sid}.wav'; loudnorm2(raw, out, I=-14)
    # comprobación: nivel de la música sola frente a la voz sola, en el tramo hablado
    ms = f'{P}/out/tmp/{sid}-ms.wav'; wr(ms, mm); rel = lufs(ms, ss=PRE + 1.5, t=max(3, fin - 3)) - lv
    print(f'{sid}: total {total:.2f}s · voz {lv:.1f} LUFS · música bajo la voz {rel:+.1f} dB · mezcla {lufs(out):.1f} LUFS', flush=True)
