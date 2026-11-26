#!/usr/bin/env python3
"""Fragmento de clase con las pausas recortadas (pedido de Dayana del 26-nov: «añade música movida y corta los silencios»).
Mismo método que los shorts: silencedetect, fuera toda pausa de más de PAUSA_MIN dejando ~0,3 s, cortes en fotogramas exactos de la fuente (25 fps),
audio pegado muestra a muestra con fundido de 10 ms, todo a 1,1×. Salida: public/clip/<id>.mp4, audio/<id>-voz.wav, data/<id>.json (dur, empalmes).
Uso: prep_clase_corte.py"""
import json, os, re, subprocess, sys, wave
import numpy as np
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIM = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/videos-dic/vim'
CL = [dict(id='nav-fragmento-clase-2-reel', vid='1236306840', t0=3.4, t1=33.4, crop='880:640:330:30', hook=['¿ASÍ DISEÑAS', 'TUS ZAPATAS?'],
           pie='Diseño de Cimentaciones Superficiales aplicado a Proyectos Reales', musica='energica')]
PAUSA_MIN, DEJA_A, DEJA_B, SPEED, Q = 0.45, 0.14, 0.16, 1.1, 0.04
TMP = f'{P}/out/tmp'
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
    return r
q = lambda t: round(round(t / Q) * Q, 2)
for c in CL:
    V = f"{VIM}/c{c['vid']}.mp4"; a, b = c['t0'], c['t1']; sid = c['id']
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-ss', str(a), '-t', str(b - a), '-i', V, '-vn', '-af', 'silencedetect=noise=-34dB:d=0.3', '-f', 'null', '-']).stderr
    ss = [float(x) for x in re.findall(r'silence_start: ([-\d.]+)', r)]; se = [float(x) for x in re.findall(r'silence_end: ([-\d.]+)', r)]
    if len(se) < len(ss): se.append(b - a)
    keep = []; cur = a
    for x, y in zip(ss, se):
        if y - x < PAUSA_MIN: continue
        c0 = a + max(0, x) + DEJA_A; c1 = a + y - DEJA_B
        if a + y > b - 0.05: c1 = b
        if c1 - c0 < 0.12: continue
        if c0 - cur > 0.05: keep.append([q(cur), q(c0)])
        cur = c1
    if b - cur > 0.05: keep.append([q(cur), q(b)])
    A0 = q(a); wavf = f'{TMP}/{sid}_tramo.wav'
    run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{A0:.2f}', '-t', f'{b - A0 + 0.3:.3f}', '-i', V, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', wavf])
    w = wave.open(wavf); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64).reshape(-1, 2); w.close()
    audio = []; files = []; empalmes = []; t_out = 0.0; nfr = 0
    vf = f"crop={c['crop']},scale=1000:760:force_original_aspect_ratio=decrease:flags=lanczos,pad=1000:760:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1"
    for i, (k0, k1) in enumerate(keep):
        n = int(round((k1 - k0) / Q)); k1 = k0 + n * Q
        if i: empalmes.append(round(t_out / SPEED, 3))
        seg = x[int(round((k0 - A0) * 48000)):int(round((k0 - A0) * 48000)) + n * 1920].copy(); f = 480
        seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]; audio.append(seg)
        fn = f'{TMP}/{sid}_{i:02d}.mkv'; files.append(fn); nfr += n; t_out += n * Q
        run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{k0:.2f}', '-i', V, '-an', '-vf', vf, '-frames:v', str(n), '-r', '25', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-pix_fmt', 'yuv420p', fn])
    au = np.concatenate(audio); raw = f'{TMP}/{sid}_audio.wav'
    w = wave.open(raw, 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes(au.astype(np.int16).tobytes()); w.close()
    assert abs(len(au) / 48000 - nfr / 25) < 0.001
    ins = []; [ins.extend(['-i', f]) for f in files]; n = len(files)
    fc = ''.join(f'[{i}:v]' for i in range(n)) + f'concat=n={n}:v=1:a=0[v0];[v0]setpts=PTS/{SPEED},fps=30[v];[{n}:a]atempo={SPEED}[a]'
    body = f'{P}/public/clip/{sid}.mp4'; voz = f'{P}/audio/{sid}-voz.wav'
    run(['ffmpeg', '-loglevel', 'error', '-y', *ins, '-i', raw, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-g', '30',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', body])
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-af', f'atempo={SPEED}', '-ac', '1', '-ar', '48000', voz])
    dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', voz]).stdout)
    js = f'{P}/data/{sid}.json'; d = json.load(open(js)) if os.path.exists(js) else {}
    d.update(id=sid, dur=round(dur, 3), empalmes=empalmes, hook=c['hook'], pie=c['pie'], musica=c['musica'], antes=round(b - a, 2), quitado=round(b - a - t_out, 2))
    json.dump(d, open(js, 'w'), ensure_ascii=False, indent=1)
    print(f'{sid}: antes {b - a:.1f}s → pausas recortadas {b - a - t_out:.1f}s → {dur:.1f}s a {SPEED}× · {len(empalmes)} empalmes', flush=True)
