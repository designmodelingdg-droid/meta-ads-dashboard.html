#!/usr/bin/env python3
"""/editar · primer paso de cualquier reel de DMA: del crudo a la voz editada, con receta.

    python3 editar.py preparar  <carpeta> hook.mov d1.mov d2.mov cierre.mov
    python3 editar.py render    <carpeta>            # lee receta.json y rehace solo lo que cambió

`preparar` hace, por clip y en orden:
  1. audio 16 kHz mono;
  2. Silero (el VAD que trae faster-whisper, sin instalar nada) → tramos con voz;
  3. Whisper con tiempo por palabra → ningún corte se come una palabra: cada tramo se
     estira hasta el final de la última palabra que toca;
  4. si el clip es horizontal, YuNet (OpenCV) busca la cara y calcula el recorte 9:16
     centrado en ella (mediana de la posición, para que no baile);
  y escribe <carpeta>/receta.json, que es la fuente de verdad del corte: se puede editar a
  mano (quitar una frase, alargar una pausa, cambiar la velocidad) y volver a correr `render`.

`render` arma <carpeta>/gabriel_editado.mp4 (1080×1920, 30 fps):
  - corta y une los tramos de la receta (cada clip se cachea por su huella: si su parte de
    la receta no cambió, no se vuelve a cortar);
  - acelera a `velocidad` (Gabriel 1.2×, clases 1.1×) sin cambiar el tono;
  - normaliza a -14 LUFS en DOS pasadas (loudnorm medido y luego aplicado);
  - re-transcribe la voz editada → <carpeta>/words.json para los subtítulos de Remotion.

Requiere: ffmpeg, faster-whisper, opencv-python (cv2 ≥ 4.8) y el modelo YuNet en
~/.cache/dma-video/yunet.onnx (se baja solo la primera vez desde media.githubusercontent.com).
"""
import hashlib, json, os, re, subprocess, sys, wave

import numpy as np

CACHE = os.path.expanduser('~/.cache/dma-video')
YUNET = os.path.join(CACHE, 'yunet.onnx')
YUNET_URL = ('https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/'
             'face_detection_yunet/face_detection_yunet_2023mar.onnx')
_whisper = None


def sh(*a, **k):
    return subprocess.run(list(a), check=True, capture_output=True, text=True, **k)


def probe(path):
    out = sh('ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
             'stream=width,height:stream_side_data=rotation:format=duration', '-of', 'json', path).stdout
    d = json.loads(out)
    st = d['streams'][0]
    w, h = st['width'], st['height']
    rot = 0
    for sd in st.get('side_data_list', []) or []:
        rot = int(sd.get('rotation', 0) or 0)
    if abs(rot) == 90:
        w, h = h, w
    return w, h, float(d['format']['duration'])


def wav16(src, dst):
    sh('ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', '16000', dst)
    with wave.open(dst) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def whisper():
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel('medium', device='cpu', compute_type='int8')
    return _whisper


def palabras(audio, prompt='Design Modeling Academy, BIM, Revit, Gabriel.'):
    segs, _ = whisper().transcribe(audio, language='es', word_timestamps=True, initial_prompt=prompt)
    return [{'w': x.word.strip(), 's': round(x.start, 2), 'e': round(x.end, 2)} for s in segs for x in s.words]


def tramos_voz(audio, dur, words, pausa=0.15, margen=0.05):
    """Silero decide dónde hay voz. Whisper solo corrige los bordes: si una palabra empieza
    un poco antes del tramo (hasta 0,3 s) o termina un poco después (hasta 0,35 s) —los
    finales suaves que Silero suele recortar—, el tramo se estira para no comérsela."""
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    sr = 16000
    ts = get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=int(pausa * 1000), speech_pad_ms=30))
    out = []
    for t in ts:
        a, b = t['start'] / sr, t['end'] / sr
        for w in words:
            mid = (w['s'] + w['e']) / 2
            if a <= mid <= b:
                if a - 0.3 <= w['s'] < a:
                    a = w['s']
                if b < w['e'] <= b + 0.35:
                    b = w['e']
        a, b = max(0.0, a - margen), min(dur, b + margen)
        if out and a - out[-1][1] < 0.12:
            out[-1][1] = b
        elif b - a > 0.12:
            out.append([a, b])
    return [[round(a, 3), round(b, 3)] for a, b in out]


def centro_cara(src, w, h, muestras=24):
    """Para un clip horizontal: x central de la cara (mediana) para recortar a 9:16."""
    import cv2
    if not os.path.exists(YUNET):
        os.makedirs(CACHE, exist_ok=True)
        sh('curl', '-sSL', '-o', YUNET, YUNET_URL)
    cap = cv2.VideoCapture(src)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    det = None
    xs = []
    for i in range(muestras):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (i + 0.5) / muestras))
        ok, fr = cap.read()
        if not ok:
            continue
        if fr.shape[1] != w:  # vídeo rotado por metadatos
            fr = cv2.rotate(fr, cv2.ROTATE_90_CLOCKWISE)
        s = 640 / fr.shape[1]
        small = cv2.resize(fr, (640, int(fr.shape[0] * s)))
        if det is None:
            det = cv2.FaceDetectorYN.create(YUNET, '', (small.shape[1], small.shape[0]), 0.7)
        _, faces = det.detect(small)
        if faces is not None and len(faces):
            f = max(faces, key=lambda r: r[2] * r[3])
            xs.append((f[0] + f[2] / 2) / s)
    cap.release()
    return round(float(np.median(xs)), 1) if xs else w / 2


def preparar(carpeta, clips):
    os.makedirs(os.path.join(carpeta, 'trabajo'), exist_ok=True)
    receta = {'velocidad': 1.2, 'lufs': -14, 'clips': []}
    for c in clips:
        w, h, dur = probe(c)
        nombre = os.path.splitext(os.path.basename(c))[0]
        audio = wav16(c, os.path.join(carpeta, 'trabajo', nombre + '.wav'))
        words = palabras(audio)
        clip = {'archivo': os.path.abspath(c), 'nombre': nombre, 'dur': round(dur, 3),
                'texto': ' '.join(x['w'] for x in words), 'tramos': tramos_voz(audio, dur, words)}
        if w > h:  # horizontal → recorte 9:16 centrado en la cara
            cw = round(h * 9 / 16)
            cx = centro_cara(c, w, h)
            clip['recorte'] = {'x': int(min(max(cx - cw / 2, 0), w - cw)), 'ancho': cw, 'alto': h}
        receta['clips'].append(clip)
        print(f"· {nombre}: {len(clip['tramos'])} tramos · {clip['texto'][:70]}", flush=True)
    json.dump(receta, open(os.path.join(carpeta, 'receta.json'), 'w'), ensure_ascii=False, indent=1)
    print('receta →', os.path.join(carpeta, 'receta.json'))


def cortar_clip(carpeta, clip):
    """Un clip ya cortado y en vertical, cacheado por la huella de su parte de la receta."""
    huella = hashlib.sha1(json.dumps([clip['archivo'], clip['tramos'], clip.get('recorte')]).encode()).hexdigest()[:12]
    dst = os.path.join(carpeta, 'trabajo', f"{clip['nombre']}-{huella}.mp4")
    if os.path.exists(dst):
        return dst
    r = clip.get('recorte')
    vf = (f"crop={r['ancho']}:{r['alto']}:{r['x']}:0," if r else '') + 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30'
    fc = []
    for i, (a, b) in enumerate(clip['tramos']):
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,{vf}[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.02,afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03[a{i}]")
    n = len(clip['tramos'])
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
    sh('ffmpeg', '-v', 'error', '-y', '-i', clip['archivo'], '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
       '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', '-ar', '48000', dst.replace('.mp4', '.mkv'))
    os.replace(dst.replace('.mp4', '.mkv'), dst)
    return dst


def render(carpeta):
    receta = json.load(open(os.path.join(carpeta, 'receta.json')))
    piezas = [cortar_clip(carpeta, c) for c in receta['clips']]
    lista = os.path.join(carpeta, 'trabajo', 'lista.txt')
    open(lista, 'w').write(''.join(f"file '{p}'\n" for p in piezas))
    unido = os.path.join(carpeta, 'trabajo', 'unido.mkv')
    sh('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', unido)
    v = float(receta.get('velocidad', 1.2))
    lufs = float(receta.get('lufs', -14))
    # pasada 1: medir
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', unido, '-af', f'atempo={v},loudnorm=I={lufs}:TP=-1.0:LRA=11:print_format=json',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', out, re.S).group(0))
    ln = (f"loudnorm=I={lufs}:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=false")
    final = os.path.join(carpeta, 'gabriel_editado.mp4')
    # pasada 2: aplicar
    sh('ffmpeg', '-v', 'error', '-y', '-i', unido, '-filter_complex', f'[0:v]setpts=PTS/{v},fps=30[v];[0:a]atempo={v},{ln},aresample=48000[a]',
       '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', final)
    audio = wav16(final, os.path.join(carpeta, 'trabajo', 'editado.wav'))
    words = palabras(audio)
    json.dump(words, open(os.path.join(carpeta, 'words.json'), 'w'), ensure_ascii=False)
    dur = len(audio) / 16000
    print(f'listo → {final} ({dur:.1f} s) · words.json con {len(words)} palabras')
    print(' '.join(w['w'] for w in words))


if __name__ == '__main__':
    if len(sys.argv) >= 4 and sys.argv[1] == 'preparar':
        preparar(sys.argv[2], sys.argv[3:])
    elif len(sys.argv) == 3 and sys.argv[1] == 'render':
        render(sys.argv[2])
    else:
        sys.exit(__doc__)
