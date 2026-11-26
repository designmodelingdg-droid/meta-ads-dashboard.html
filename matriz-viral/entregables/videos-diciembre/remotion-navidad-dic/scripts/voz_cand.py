#!/usr/bin/env python3
"""Candidatas de una frase con otra semilla u otra grafía (misma voz y parámetros que voz_reels.py). Uso: voz_cand.py nombre:semilla "texto" ... → <VOZ>/_cand/<nombre>.wav"""
import os, sys, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
VOZ = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/videos-dic/work/voz'
torch.set_num_threads(int(os.environ.get('HILOS', 2))); os.makedirs(f'{VOZ}/_cand', exist_ok=True)
m = ChatterboxMultilingualTTS.from_pretrained(device='cpu'); a = sys.argv[1:]
for i in range(0, len(a), 2):
    n, seed = a[i].split(':'); torch.manual_seed(4000 + int(seed) * 31)
    wav = m.generate(a[i + 1], language_id='es', audio_prompt_path=f'{VOZ}/gabriel_ref.wav', exaggeration=0.55, cfg_weight=0.5, temperature=0.6)
    ta.save(f'{VOZ}/_cand/{n}.wav', wav, m.sr); print(f'CAND {n} {wav.shape[-1] / m.sr:.2f}s {a[i + 1]}', flush=True)
