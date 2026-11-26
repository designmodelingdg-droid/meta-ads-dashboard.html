#!/usr/bin/env python3
"""Whisper (faster-whisper, CPU) sobre la voz ya editada → data/<id>.json: words [{w,s,e,p}] con tiempos reales del corte final.
Uso: transcribir.py <modelo> <id> [id ...]   (el wav sale de audio/<id>-voz.wav)"""
import json, os, sys, wave
import numpy as np
from faster_whisper import WhisperModel
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = WhisperModel(sys.argv[1], device='cpu', compute_type='int8', cpu_threads=4)
PROMPT = ('Workshop de Design Modeling Academy: IA conectada a Revit. BIM Manager, Revit, pyRevit, MCP, ChatGPT, Claude, NonicaTab, '
          'prompt maestro, GPT especializado, plugin, SAP2000, zapata, cimentación, nave industrial.')
for sid in sys.argv[2:]:
    w = wave.open(f'{P}/audio/{sid}-voz.wav'); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    if sr != 16000:
        n = int(len(x) * 16000 / sr); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    segs, _ = m.transcribe(x, language='es', word_timestamps=True, vad_filter=True, initial_prompt=PROMPT, condition_on_previous_text=False, beam_size=5)
    words = [{'w': q.word.strip(), 's': round(q.start, 3), 'e': round(q.end, 3), 'p': round(q.probability, 2)} for s in segs for q in s.words]
    js = f'{P}/data/{sid}.json'; d = json.load(open(js)) if os.path.exists(js) else {'id': sid}
    d['whisper'] = words
    json.dump(d, open(js, 'w'), ensure_ascii=False, indent=1)
    print(sid, len(words), 'palabras |', ' '.join(q['w'] for q in words), flush=True)
    print('   dudosas:', [(q['w'], q['s'], q['p']) for q in words if q['p'] < 0.6], flush=True)
