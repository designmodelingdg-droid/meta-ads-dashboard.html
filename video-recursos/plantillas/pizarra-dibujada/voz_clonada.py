#!/usr/bin/env python3
"""Voz de Gabriel con IA (Chatterbox Multilingual, licencia MIT, corre en CPU, sin créditos).

Gabriel aprobó el uso de su voz clonada (19-oct-2026). La muestra de referencia NO se sube
al repo (es su voz): se arma en local con 15–20 s de clips suyos limpios, sin música.

Instalar una vez (en un venv; torch CPU para no llenar el disco):
    python3 -m venv cbx
    cbx/bin/pip install --no-cache-dir "torch==2.6.0" "torchaudio==2.6.0" --index-url https://download.pytorch.org/whl/cpu
    cbx/bin/pip install --no-cache-dir chatterbox-tts

Uso:
    cbx/bin/python voz_clonada.py frases.json gabriel_ref.wav salida/
      frases.json = ["Frase de la escena 0.", "Frase de la escena 1.", ...]  (una por escena)
    → salida/s0.wav, s1.wav, …  (una por escena, para anclar cada página a su frase)

Después: recortar silencios, atempo 1.1, unir con 0.25 s entre frases (eso da timing.json),
loudnorm a −14 LUFS y transcribir con Whisper para words.json. Comprobar con Whisper que cada
frase dice exactamente el guion.
"""
import json, os, sys
import torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

torch.set_num_threads(os.cpu_count() or 2)
frases, ref, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
for i, txt in enumerate(frases):
    wav = m.generate(txt, language_id="es", audio_prompt_path=ref, exaggeration=0.55, cfg_weight=0.5, temperature=0.7)
    ta.save(os.path.join(out, f"s{i}.wav"), wav, m.sr)
    print(f"s{i}.wav  {wav.shape[-1] / m.sr:.2f} s  {txt}", flush=True)
