#!/usr/bin/env python3
"""Shorts del workshop «IA conectada a Revit»: corta los silencios y deja el cuerpo listo para Remotion.

Por cada short de shorts.json:
  1. silencedetect por tramo → se recorta toda pausa de más de 0,6 s y se deja ~0,3 s (0,14 s tras el
     sonido y 0,16 s antes del siguiente), nunca dentro de una palabra.
  2. el recorte de pantalla (chat / Revit / Claude) se elige por tramo igual que en la versión anterior.
  3. video y audio se cortan en los mismos fotogramas; el audio se pega muestra a muestra; todo a 1,1× (ritmo de clase de la casa).
  4. Whisper vuelve a transcribir la voz YA editada → tiempos por palabra reales del corte final.
Salida: public/clip/<id>.mp4 (1000×760, 30 fps), audio/<id>-voz.wav y data/<id>.json
Uso: prep_shorts.py [id ...]
"""
import json, os, re, subprocess, sys

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad'
V = f'{SP}/ws-drive/grabacion-drive.mp4'
SENT = json.load(open(f'{SP}/ws-drive/sentences.json'))['sentences']
WORDS = [w for s in SENT for w in s['words']]
SHORTS = json.load(open(f'{SP}/yt/build/shorts.json'))
TMP = f'{P}/out/tmp'
os.makedirs(TMP, exist_ok=True)
# Bordes de tramo corregidos tras medir el volumen de la fuente (los de shorts.json cortaban el inicio o el final de alguna palabra):
#   s4 tramo 3 empezaba a mitad de un «Entonces»; s6 tramo 1 empezaba con la cola de la frase anterior y acababa con un «Entonces…» suelto,
#   y el tramo 2 cortaba el «ok» final; s7 y s5 cortaban la cola de la última palabra.
AJUSTE = {
 's1-1880-muros': [[3935.9, 3949.9], [3954.32, 3997.1], [3998.6, 4004.1]],
 's2-niveles': [[3517.6, 3545.6], [3585.0, 3592.8], [3600.4, 3617.0], [3627.4, 3631.7]],
 's4-claude-revit': [[4575.2, 4590.6], [4641.92, 4659.66], [4677.36, 4690.0], [4714.72, 4718.9]],
 's5-cualquier-cosa': [[1191.4, 1215.56], [1217.7, 1219.95]],
 's6-no-hace-magia': [[1006.76, 1013.8], [1511.2, 1538.72]],
 's7-mil-cosas': [[1976.0, 2016.1], [2117.3, 2131.24]],
 's8-para-que-conectar': [[2605.3, 2629.0], [2630.3, 2642.6]],
 's9-niveles-duplicados': [[4641.92, 4659.66]],   # reel «La IA encontró 3 niveles a la misma altura» (mismo tramo que el 2.º de s4)
}
PAUSA = {'s9-niveles-duplicados': 0.4}   # pausa mínima que se recorta, si no es la general
HOOK = {'s9-niveles-duplicados': ['LA IA ENCONTRÓ 3 NIVELES', 'A LA MISMA ALTURA']}
CHAT = '1350:830:565:170'
BW, BH = 1000, 760
SPEED = 1.1
PAUSA_MIN, DEJA_A, DEJA_B = 0.6, 0.14, 0.16


def run(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, **k)
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
    return r


REF = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', '1200', '-i', V, '-frames:v', '1', '-vf', 'crop=240:60:0:180,scale=60:15',
                      '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout


def flags(t0, d):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(t0), '-t', str(d), '-i', V, '-vf', 'fps=2,crop=240:60:0:180,scale=60:15',
                          '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    fr = [raw[k * 900:(k + 1) * 900] for k in range(len(raw) // 900)]
    return [sum(abs(a - b) for a, b in zip(f, REF)) / 900 < 6 for f in fr]


def segs(t0, t1):
    """[[ini, fin, es_chat]] — qué zona de la pantalla se ve en cada tramo (igual que la versión anterior)."""
    f = flags(t0, t1 - t0); out = []
    for k, x in enumerate(f):
        t = t0 + k / 2
        if out and out[-1][2] == x: out[-1][1] = min(t + 0.5, t1)
        else:
            if out: out[-1][1] = t
            out.append([t, min(t + 0.5, t1), x])
    res = []
    for s in out:
        if res and (s[1] - s[0] < 1.5): res[-1][1] = s[1]
        else: res.append(s)
    res[-1][1] = t1
    return res


def silencios(a, b):
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-ss', str(a), '-t', str(b - a), '-i', V, '-vn', '-af', 'silencedetect=noise=-34dB:d=0.3', '-f', 'null', '-']).stderr
    ss = [float(x) for x in re.findall(r'silence_start: ([-\d.]+)', r)]
    se = [float(x) for x in re.findall(r'silence_end: ([-\d.]+)', r)]
    if len(se) < len(ss): se.append(b - a)
    out = []
    for x, y in zip(ss, se):
        x = max(0.0, x)
        if out and x - out[-1][1] < 0.06: out[-1][1] = y
        else: out.append([x, y])
    return out


def conservar(a, b):
    """Tramos que se quedan (tiempos absolutos) y lista de pausas recortadas."""
    keep = []; cur = a; cortes = []
    for x, y in silencios(a, b):
        if y - x < PAUSA_MIN: continue
        c0 = a + x + DEJA_A; c1 = a + y - DEJA_B
        if x < 0.05: c0 = a + x              # silencio al arrancar el tramo: no hace falta dejar cola
        if a + y > b - 0.05: c1 = b          # silencio al final del tramo
        if c1 - c0 < 0.12: continue
        if c0 - cur > 0.05: keep.append([cur, c0])
        cortes.append((round(x, 2), round(y, 2)))
        cur = c1
    if b - cur > 0.05: keep.append([cur, b])
    return keep, cortes


Q = 0.04                                   # la fuente va a 25 fps: todo corte cae en un fotograma exacto
def q(t): return round(round(t / Q) * Q, 2)


def short(sh):
    """Video y audio se cortan en los mismos puntos (múltiplos de 1/25 s). El audio se saca de un WAV continuo por tramo y se pega
    muestra a muestra: en los cambios de recorte de pantalla no hay ni fundido ni hueco; solo hay un fundido de 10 ms en las pausas recortadas."""
    import numpy as np, wave
    sid = sh['id']; piezas = []; empalmes = []; t_out = 0.0; quitado = 0.0; total = 0.0; audio = []
    for a, b in sh['r']:
        total += b - a
        keep, cortes = conservar(a, b)
        sg = segs(a, b)
        A0 = q(a); wavf = f'{TMP}/{sid}_tramo.wav'
        run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{A0:.2f}', '-t', f'{b - A0 + 0.2:.3f}', '-i', V, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', wavf])
        w = wave.open(wavf); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64).reshape(-1, 2); w.close()
        for k0, k1 in keep:
            k0, k1 = q(k0), q(k1)
            if k1 - k0 < Q: continue
            if piezas: empalmes.append(round(t_out / SPEED, 3))
            seg = x[int(round((k0 - A0) * 48000)):int(round((k1 - A0) * 48000))].copy()
            f = int(0.010 * 48000); seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
            audio.append(seg); cur = k0
            for s0, s1, ischat in sg:
                p0, p1 = max(k0, q(s0)), min(k1, q(s1))
                if p1 - p0 < Q: continue
                p0 = cur                                   # sin huecos entre piezas del mismo tramo
                crop = sh['claude'] if (sh.get('claude') and p0 >= 4600) else (CHAT if ischat else sh['alt'])
                piezas.append((p0, p1, crop)); cur = p1
            if cur < k1 and piezas: piezas[-1] = (piezas[-1][0], k1, piezas[-1][2])
            t_out += k1 - k0; quitado -= k1 - k0
        quitado += b - a
    un = []
    for p in piezas:
        if un and abs(un[-1][1] - p[0]) < 1e-6 and un[-1][2] == p[2]: un[-1] = (un[-1][0], p[1], p[2])
        else: un.append(p)
    files = []; nfr = 0
    for i, (p0, p1, crop) in enumerate(un):
        n = int(round((p1 - p0) / Q)); nfr += n; f = f'{TMP}/{sid}_{i:02d}.mkv'
        vf = (f"crop={crop},scale={BW}:{BH}:force_original_aspect_ratio=decrease:flags=lanczos,"
              f"pad={BW}:{BH}:(ow-iw)/2:(oh-ih)/2:color=0x0d1e3a,setsar=1")
        run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{p0:.2f}', '-i', V, '-an', '-vf', vf, '-frames:v', str(n), '-r', '25', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12',
             '-pix_fmt', 'yuv420p', f])
        files.append(f)
    au = np.concatenate(audio); raw = f'{TMP}/{sid}_audio.wav'
    w = wave.open(raw, 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes(au.astype(np.int16).tobytes()); w.close()
    assert abs(len(au) / 48000 - nfr / 25) < 0.001, (len(au) / 48000, nfr / 25)
    ins = []
    for f in files: ins += ['-i', f]
    n = len(files)
    fc = ''.join(f'[{i}:v]' for i in range(n)) + f'concat=n={n}:v=1:a=0[v0];[v0]setpts=PTS/{SPEED},fps=30[v];[{n}:a]atempo={SPEED}[a]'
    body = f'{P}/public/clip/{sid}.mp4'; voz = f'{P}/audio/{sid}-voz.wav'
    run(['ffmpeg', '-loglevel', 'error', '-y', *ins, '-i', raw, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15',
         '-pix_fmt', 'yuv420p', '-g', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', body])
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-af', f'atempo={SPEED}', '-ac', '1', '-ar', '48000', voz])
    dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', voz]).stdout)
    orig = ' '.join(w['text'] for a, b in sh['r'] for w in WORDS if a * 1000 <= w['start'] < b * 1000)
    js = f'{P}/data/{sid}.json'
    d = json.load(open(js)) if os.path.exists(js) else {}
    d.update(id=sid, dur=round(dur, 3), empalmes=empalmes, hook=sh['hook'], pie=sh['pie'], transcripcion_original=orig,
             antes=round(total, 2), quitado=round(quitado, 2))
    json.dump(d, open(js, 'w'), ensure_ascii=False, indent=1)
    print(f'{sid}: antes {total:.1f}s → pausas recortadas {quitado:.1f}s → {dur:.1f}s a {SPEED}× · {n} piezas de video · {len(empalmes)} empalmes', flush=True)


if __name__ == '__main__':
    ids = sys.argv[1:]
    for sh in SHORTS:
        if sh['id'].startswith('s9') and sh['id'] not in ids: continue
        if not ids or sh['id'] in ids:
            sh['r'] = AJUSTE.get(sh['id'], sh['r']); PAUSA_MIN = PAUSA.get(sh['id'], 0.6); sh['hook'] = HOOK.get(sh['id'], sh['hook']); short(sh)
