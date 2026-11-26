#!/usr/bin/env python3
"""Arma la voz de un reel animado y su línea de tiempo (regla de la casa: motion-dma/voz/armar.py).
Por frase: sin pausas internas de más de 0,1 s, atempo 1,12; 0,1 s entre frases; Whisper comprueba que cada frase dice el guion
y da los tiempos por palabra, que se alinean con el texto del guion (el subtítulo muestra el guion, no lo que oyó Whisper).
Mezcla: voz + música lo-fi de la casa (plantillas/scripts/musica_original.py, volume 0.13 bajo la voz) + efectos, a −14 LUFS.
Uso: armar_voz.py <reel> [--sin-voz]  → audio/reel-<k>.wav y reels/<k>.json {escenas:[{s,dur}], palabras:[{w,s,e}], total}"""
import difflib, json, os, re, subprocess, sys, unicodedata, wave
import numpy as np
from comun import P, REPO, SR, rd, wr, run, lufs, loudnorm2
VOZ = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/videos-dic/work/voz'
INTRO, GAP, AIRE = 0.35, 0.1, float(os.environ.get('AIRE', 0.55))      # AIRE: respiro al final de cada escena para que la animación termine
k = sys.argv[1]; SIN = '--sin-voz' in sys.argv
G = json.load(open(f'{P}/reels/guiones.json'))[k]; E = G['escenas']
UNI = dict(cero=0, uno=1, un=1, una=1, dos=2, tres=3, cuatro=4, cinco=5, seis=6, siete=7, ocho=8, nueve=9, diez=10, once=11, doce=12, trece=13, catorce=14, quince=15,
           dieciseis=16, diecisiete=17, dieciocho=18, diecinueve=19, veinte=20, veintiuno=21, veintidos=22, veintitres=23, veinticuatro=24, veinticinco=25, veintiseis=26,
           veintisiete=27, veintiocho=28, veintinueve=29)
DEC = dict(treinta=30, cuarenta=40, cincuenta=50, sesenta=60, setenta=70, ochenta=80, noventa=90)
ABR = dict(cm='centimetros', mm='milimetros', km='kilometros', m='metros')
# la misma palabra escrita como se lee (texto para la voz) y como la escribe Whisper
ALIAS = [(' chat ye pe te ', ' chatgpt '), (' pai revit ', ' pyrevit '), (' eme ce pe ', ' mcp '), (' clod ', ' claude '), (' nonica tab ', ' nonicatab '), (' test beam ', ' test bim '),
         (' testbeam ', ' test bim '), (' i a ', ' ia '), (' a c i ', ' aci '), (' ve raro ', ' ver raro '), (' mayores ', ' mayoras '), (' demedios ', ' de medios ')]
# frases revisadas a mano: Whisper escribe un homófono de lo que dice el guion (se oye igual)
ACEPTA = {('uniones', 1): '«pasan momento» ≈ «pasa un momento»', ('uniones', 7): '«alma soldadas» ≈ «almas soldadas»',
          ('combos', 0): 'Whisper escribe «1,4D más 1,7L» (la voz dice «uno coma cuatro de más uno coma siete ele»)',
          ('medidas', 2): '«distancia d, de esa cara. d es el peralte»: Whisper escribe «D»; el «Dos.» inicial viene de la primera toma'}
def norm(s):
    """minúsculas sin tildes ni signos, y los números siempre en dígitos (Whisper los escribe así): «uno coma veintitrés» → 1 23"""
    s = unicodedata.normalize('NFD', s.lower().replace('ñ', '\x00')); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('\x00', 'ñ')
    s = s.replace('%', ' por ciento '); s = ' ' + ' '.join(re.sub(r'[^a-z0-9ñ ]', ' ', s).split()) + ' '
    for a, b in ALIAS: s = s.replace(a, b)
    w = s.split(); out = []; i = 0
    while i < len(w):
        x = w[i]
        if x in ('ciento', 'cien') : 
            v = 100; j = i + 1
            if j < len(w) and w[j] in DEC: v += DEC[w[j]]; j += 1
            if j + 1 < len(w) and w[j] == 'y' and w[j + 1] in UNI: v += UNI[w[j + 1]]; j += 2
            elif j < len(w) and w[j] in UNI and w[j] not in ('un', 'una'): v += UNI[w[j]]; j += 1
            out.append(str(v)); i = j; continue
        if x in DEC:
            v = DEC[x]; j = i + 1
            if j + 1 < len(w) and w[j] == 'y' and w[j + 1] in UNI: v += UNI[w[j + 1]]; j += 2
            out.append(str(v)); i = j; continue
        if x in UNI and x not in ('un', 'una'): out.append(str(UNI[x])); i += 1; continue
        if x == 'coma' and out and out[-1].isdigit(): i += 1; continue
        out.append(ABR.get(x, x)); i += 1
    return out
def tok(s): return [w for w in s.split() if re.sub(r'[^\wáéíóúñÁÉÍÓÚÑ0-9]', '', w)]
esc = []; pal = []; pistas = []; t = INTRO; malas = []
if not SIN:
    from faster_whisper import WhisperModel
    wm = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=4)
for i, e in enumerate(E):
    cierre = i == len(E) - 1
    if SIN:
        d = float(e['dur']); ws = tok(e['voz']); a = t + 0.3; dd = min(0.36, (d - 0.9) / len(ws))
        pal += [dict(w=w, s=round(a + j * dd, 3), e=round(a + (j + 1) * dd, 3)) for j, w in enumerate(ws)]
        esc.append(dict(s=round(t, 3), dur=round(d, 3))); t += d; continue
    src = f'{VOZ}/{k}/s{i}.wav'; dst = f'{VOZ}/{k}/c{i}.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af',
         'silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.02,'
         'silenceremove=stop_periods=-1:stop_threshold=-32dB:stop_duration=0.1:stop_silence=0.06,'
         'areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03,areverse,atempo=1.12', '-ar', str(SR), '-ac', '1', dst])
    x = rd(dst); d = len(x) / SR
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', dst, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
    segs, _ = wm.transcribe(np.frombuffer(raw, np.float32), language='es', word_timestamps=True, condition_on_previous_text=False,
                            initial_prompt='Zapata, cortante, punzonamiento, peralte efectivo, Revit, pyRevit, MCP, ChatGPT, Claude, NonicaTab, ACI, momento, alma, alas.')
    hw = [(q.word.strip(), q.start, q.end) for s in segs for q in s.words]
    oido = norm(' '.join(w for w, _, _ in hw)); esperado = norm(e['tts'])
    r = difflib.SequenceMatcher(None, oido, esperado).ratio()
    if r < 0.9:   # Whisper a veces se come una palabra en la versión sin pausas: segunda comprobación sobre la frase tal como salió de la voz
        raw2 = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
        s2, _ = wm.transcribe(np.frombuffer(raw2, np.float32), language='es', condition_on_previous_text=False)
        r = max(r, difflib.SequenceMatcher(None, norm(' '.join(q.text for q in s2)), esperado).ratio())
    if r < 0.9 and (k, i) in ACEPTA: print(f'  (aceptada a mano: {ACEPTA[(k, i)]})'); r = 0.9
    if r < 0.9: malas.append(i)
    print(f"  {'OK ' if r >= 0.9 else 'MAL'} {k} s{i} {d:5.2f}s (guion {e['dur']}s) r={r:.2f} | {' '.join(w for w, _, _ in hw)}", flush=True)
    # tiempos: las palabras del guion (texto en pantalla) se reparten sobre los tiempos que oyó Whisper, por posición relativa de caracteres
    ws = tok(e['voz']); tot = sum(len(w) for w in ws) or 1
    if hw:
        hc = np.cumsum([0] + [len(w) for w, _, _ in hw]) / max(1, sum(len(w) for w, _, _ in hw)); ht = [hw[0][1]] + [b for _, _, b in hw]
        at = lambda f: float(np.interp(f, hc, ht))
    else: at = lambda f: f * d
    c = 0
    for w in ws:
        a = at(c / tot); c += len(w); b = at(c / tot)
        pal.append(dict(w=w, s=round(t + a, 3), e=round(t + max(b, a + 0.08), 3)))
    pistas.append((t, x)); dur = max(d + GAP + AIRE, 2.2 if not cierre else d + 2.6)
    esc.append(dict(s=round(t, 3), dur=round(dur, 3))); t += dur
total = round(t, 3)
N = int(total * SR)
mus = f'{P}/audio/musica-reel-{k}.wav'
subprocess.run([sys.executable, f'{REPO}/plantillas/scripts/musica_original.py', f'{total + 0.5:.2f}', mus], check=True, capture_output=True)
m = rd(mus)[:N]; tt = np.arange(N) / SR
rng = np.random.default_rng(5)
def papel():
    n = int(0.3 * SR); x = rng.standard_normal(n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X *= (f / 2500) / (1 + (f / 2500) ** 2) * 2 / (1 + (f / 9000) ** 4)
    x = np.fft.irfft(X, n); return x / np.max(np.abs(x)) * np.sin(np.pi * (np.arange(n) / n) ** 0.6) ** 2
def ding():
    u = np.arange(int(1.1 * SR)) / SR
    return sum(a * np.sin(2 * np.pi * f * u) * np.exp(-u / d) for f, a, d in ((1318.5, 1, 0.36), (2637, 0.4, 0.2), (3955, 0.16, 0.12))) * np.minimum(1, u / 0.003)
sfx = np.zeros((N, 2))
for i, s in enumerate(esc):
    if i:
        x = papel() * 0.5; a = int(max(0, s['s'] - 0.1) * SR); b = min(N, a + len(x)); sfx[a:b] += x[:b - a, None]
x = ding() * 0.5; a = int((esc[-1]['s'] + 0.6) * SR); b = min(N, a + len(x)); sfx[a:b] += x[:b - a, None]
fo = np.clip((total - tt) / 0.8, 0, 1)[:, None]
if SIN:
    mix = (m * 0.8 + sfx * 0.35) * fo
else:
    voz = np.zeros((N, 2))
    for t0, x in pistas:
        a = int(t0 * SR); b = min(N, a + len(x)); voz[a:b] += x[:b - a]
    vraw = f'{P}/out/tmp/reel-{k}-voz.wav'; os.makedirs(f'{P}/out/tmp', exist_ok=True); wr(vraw, voz)
    vn = f'{P}/out/tmp/reel-{k}-vn.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-i', vraw, '-af', 'acompressor=threshold=-20dB:ratio=3:attack=5:release=60,loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', str(SR), '-ac', '2', vn])
    v = rd(vn)[:N]; lv = lufs(vn); lm = lufs(mus)
    sube = 1 + 1.6 * np.clip((tt - (esc[-1]['s'] + esc[-1]['dur'] - 2.3)) / 0.5, 0, 1)[:, None]   # la música sube al final, ya sin voz
    mix = v + (m * 0.13 * sube + sfx * 0.1) * fo                                                      # volume 0.13 bajo la voz (regla de la casa)
    ms = f'{P}/out/tmp/reel-{k}-ms.wav'; wr(ms, m * 0.13); print(f'  voz {lv:.1f} LUFS · música bajo la voz {lufs(ms, ss=2, t=max(3, total - 6)) - lv:+.1f} dB')
raw = f'{P}/out/tmp/reel-{k}-mix.wav'; wr(raw, mix / max(1.0, np.max(np.abs(mix)))); out = f'{P}/audio/reel-{k}.wav'; loudnorm2(raw, out, I=-14)
json.dump(dict(id=G['id'], voz=not SIN, escenas=esc, palabras=pal, total=total), open(f'{P}/reels/{k}.json', 'w'), ensure_ascii=False, indent=1)
print(f'{k}: total {total}s · {len(esc)} escenas · mezcla {lufs(out):.1f} LUFS' + (f' · frases a regenerar: {malas}' if malas else ''))
