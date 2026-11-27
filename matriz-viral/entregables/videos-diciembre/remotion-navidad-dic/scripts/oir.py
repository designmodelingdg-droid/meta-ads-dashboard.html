#!/usr/bin/env python3
"""Qué oye Whisper (medium) en unos wav. Uso: oir.py a.wav b.wav ..."""
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
wm = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=2)
for f in sys.argv[1:]:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
    segs, _ = wm.transcribe(np.frombuffer(raw, np.float32), language='es', condition_on_previous_text=False,
                            initial_prompt='Zapata, cortante, punzonamiento, peralte efectivo, Revit, pyRevit, MCP, ChatGPT, Claude, NonicaTab, ACI, momento, alma, alas, IA.')
    print('OIDO', f.split('/')[-1], '|', ' '.join(s.text.strip() for s in segs), flush=True)
