import json, os, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(os.cpu_count() or 2)
L=json.load(open('lines.json'))
m=ChatterboxMultilingualTTS.from_pretrained(device="cpu")
for k,fr in L.items():
    os.makedirs(k,exist_ok=True)
    for i,txt in enumerate(fr):
        p=f"{k}/s{i}.wav"
        if os.path.exists(p): continue
        wav=m.generate(txt,language_id="es",audio_prompt_path=os.environ["VOZ_REF"],exaggeration=0.55,cfg_weight=0.5,temperature=0.7)
        ta.save(p,wav,m.sr); print(p, round(wav.shape[-1]/m.sr,2), txt, flush=True)
