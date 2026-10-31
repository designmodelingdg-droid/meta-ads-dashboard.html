"""Une las frases de cada reel: sin silencios, atempo 1.12, 0.1 s entre frases, intro 0.3 s.
Escribe proj/public/<id>_voz.wav y proj/src/data/<id>.json (scenes, words, total) y verifica con Whisper."""
import json, subprocess, os, sys
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
SR=48000; INTRO, GAP, COLA = 0.3, 0.1, 1.3
L=json.load(open('lines.json'))
m=WhisperModel("small", device="cpu", compute_type="int8")

for k in (sys.argv[1:] or L):
    parts=[]
    for i in range(len(L[k])):
        src=f"{k}/s{i}.wav"; dst=f"{k}/c{i}.wav"
        subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-af",
            "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.02,"
            "silenceremove=stop_periods=-1:stop_threshold=-32dB:stop_duration=0.1:stop_silence=0.06,"
            "areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03,areverse,atempo=1.12",
            "-ar",str(SR),"-ac","1",dst],check=True)
        a,_=sf.read(dst); parts.append(a)
    scenes=[]; out=[np.zeros(int(INTRO*SR))]; t=INTRO
    for a in parts:
        d=len(a)/SR; scenes.append({"start":round(t,3),"dur":round(d+GAP,3)}); out+=[a,np.zeros(int(GAP*SR))]; t+=d+GAP
    total=round(t+COLA,3)
    voz=np.concatenate(out+[np.zeros(int(COLA*SR))])
    sf.write(f"{k}/voz_raw.wav",voz,SR)
    dst=f"voz_{k}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{k}/voz_raw.wav","-af","acompressor=threshold=-20dB:ratio=3:attack=5:release=60,loudnorm=I=-14:TP=-1.5:LRA=9","-ar",str(SR),dst],check=True)
    raw=subprocess.run(["ffmpeg","-v","error","-i",dst,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True,check=True).stdout
    segs,_=m.transcribe(np.frombuffer(raw,np.float32),language="es",word_timestamps=True,initial_prompt="Diplomado BIM, Robot, Advance Steel, Revit, sismorresistentes, precalificadas, despiece, Tutor IA, DQ, Sabal University, Universidad de las Naciones.")
    words=[{"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2)} for s in segs for w in s.words]
    json.dump({"scenes":scenes,"words":words,"total":total},open(f"data_{k}.json","w"),ensure_ascii=False)
    print("==",k,"total",total)
    for i,sc in enumerate(scenes):
        txt=" ".join(w["w"] for w in words if sc["start"]-0.05<=w["s"]<sc["start"]+sc["dur"])
        print(f"{i} [{sc['start']:.2f}+{sc['dur']:.2f}] {txt}  ||  {L[k][i]}")
