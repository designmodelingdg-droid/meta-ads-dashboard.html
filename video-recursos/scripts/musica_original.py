#!/usr/bin/env python3
# Uso: python3 musica_original.py <duración_s> <salida.wav>   → mezclar a volume=0.13 bajo la voz
# Música original generada por código (sin muestras ni loops de terceros → sin copyright ajeno).
# Lo-fi suave: pads de 4 acordes, bajo, bombo suave y hi-hat, 96 BPM.
import numpy as np, wave, sys
SR=44100; BPM=96; DUR=float(sys.argv[1]); rng=np.random.default_rng(3)
beat=60/BPM; N=int(DUR*SR); t=np.arange(N)/SR
out=np.zeros((N,2))
def note(f): return 440*2**((f-69)/12)
prog=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]  # Am7 Fmaj7 Cmaj7 G7
bar=4*beat
for i in range(int(DUR/bar)+1):
    ch=prog[i%4]; s=int(i*bar*SR); e=min(N,int((i+1)*bar*SR))
    if s>=N: break
    tt=np.arange(e-s)/SR; env=np.minimum(1,tt/0.4)*np.minimum(1,(bar-tt)/0.5)
    pad=sum(np.sin(2*np.pi*note(m)*tt+0.3*np.sin(2*np.pi*0.25*tt))*0.18 + np.sin(2*np.pi*note(m)*2.003*tt)*0.04 for m in ch)
    bass=np.sin(2*np.pi*note(ch[0]-12)*tt)*0.35*np.exp(-((tt%beat*2)%beat)/0.5)
    out[s:e,0]+=(pad*0.9+bass)*env; out[s:e,1]+=(pad*1.0+bass)*env
for k in range(int(DUR/beat)):
    s=int(k*beat*SR)
    if k%2==0:
        L=int(0.25*SR); tt=np.arange(L)/SR
        kick=np.sin(2*np.pi*(50+70*np.exp(-tt/0.03))*tt)*np.exp(-tt/0.12)*0.55
        e=min(N,s+L); out[s:e]+=kick[:e-s,None]
    s2=int((k+0.5)*beat*SR); L=int(0.05*SR)
    if s2+L<N:
        h=rng.standard_normal(L); h=np.diff(np.concatenate([[0],h]))*np.exp(-np.arange(L)/SR/0.012)*0.08
        out[s2:s2+L]+=h[:,None]
# filtro paso bajo suave (lo-fi) y fades
from numpy.fft import rfft, irfft, rfftfreq
for c in range(2):
    X=rfft(out[:,c]); f=rfftfreq(N,1/SR); X*=1/(1+(f/3500)**4); out[:,c]=irfft(X,N)
fade=int(1.5*SR); out[:fade]*=np.linspace(0,1,fade)[:,None]; out[-fade*2:]*=np.linspace(1,0,fade*2)[:,None]
out/=np.max(np.abs(out))*1.1
w=wave.open(sys.argv[2],'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
