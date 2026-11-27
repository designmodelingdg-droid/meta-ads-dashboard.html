#!/usr/bin/env python3
"""Voz de Gabriel con IA para los reels animados (regla de la casa: plantillas/pizarra-dibujada/voz_clonada.py).
Chatterbox Multilingual en CPU. La muestra de referencia y los wav quedan SOLO en el scratchpad (nunca en el repo ni en el artefacto).
Uso (con el python del venv cbx): voz_reels.py [reel | reel:escena[:semilla]] ...   → <VOZ>/<reel>/s<i>.wav"""
import json, os, sys
import torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOZ = os.environ.get('VOZ_DIR', '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/videos-dic/work/voz')
REF = f'{VOZ}/gabriel_ref.wav'
G = json.load(open(f'{P}/reels/guiones.json'))
torch.set_num_threads(int(os.environ.get('HILOS', os.cpu_count() or 2)))
sel = sys.argv[1:] or list(G)
m = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
for s in sel:
    parts = s.split(':'); k = parts[0]; solo = int(parts[1]) if len(parts) > 1 else None; seed = int(parts[2]) if len(parts) > 2 else 0
    os.makedirs(f'{VOZ}/{k}', exist_ok=True)
    for i, e in enumerate(G[k]['escenas']):
        out = f'{VOZ}/{k}/s{i}.wav'
        if solo is None and os.path.exists(out): continue
        if solo is not None and i != solo: continue
        torch.manual_seed(1000 + seed * 17 + i)
        wav = m.generate(e['tts'], language_id='es', audio_prompt_path=REF, exaggeration=0.55, cfg_weight=0.5, temperature=0.7 if seed == 0 else 0.6)
        ta.save(out, wav, m.sr)
        print(f'{k} s{i}.wav {wav.shape[-1] / m.sr:.2f}s  {e["tts"]}', flush=True)
