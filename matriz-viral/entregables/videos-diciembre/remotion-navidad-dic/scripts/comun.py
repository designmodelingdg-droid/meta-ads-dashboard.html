import json, os, re, subprocess, sys, wave
import numpy as np
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(P))
SR = 48000

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-2500:]); sys.exit(1)
    return r

def lufs(path, ss=None, t=None):
    cmd = ['ffmpeg', '-hide_banner', '-nostats']
    if ss is not None: cmd += ['-ss', str(ss)]
    if t is not None: cmd += ['-t', str(t)]
    r = run(cmd + ['-i', path, '-af', 'ebur128', '-f', 'null', '-']).stderr
    return float(re.findall(r'I:\s+([-\d.]+) LUFS', r)[-1])

def loudnorm2(src, dst, I=-14.0, TP=-1.5, LRA=11, extra=None):
    """loudnorm en dos pasadas (lineal): no bombea ni cambia el balance voz/música."""
    r = run(['ffmpeg', '-hide_banner', '-nostats', '-i', src, '-af', f'loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json', '-f', 'null', '-']).stderr
    m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
    af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-af', af, '-ar', str(SR), '-ac', '2', *(extra or []), dst])

def rd(path):
    w = wave.open(path); n = w.getnchannels(); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    x = x.reshape(-1, n)
    if n == 1: x = np.repeat(x, 2, axis=1)
    if sr != SR:
        m = int(len(x) * SR / sr); i = np.linspace(0, len(x) - 1, m)
        x = np.stack([np.interp(i, np.arange(len(x)), x[:, c]) for c in range(2)], axis=1)
    return x

def wr(path, x):
    x = np.clip(x, -1, 1)
    w = wave.open(path, 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

def mux(video, audio, out):
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-shortest', '-movflags', '+faststart', out])
