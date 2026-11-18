import json,subprocess,sys
SRC='../ws-drive/grabacion-drive.mp4'
ev=[l.split(':') for l in open('../ws-drive/silencios.txt').read().split('\n') if l]
sil=[];s=None
for k,v in ev:
    v=float(v)
    if k=='silence_start': s=v
    elif s is not None: sil.append((s,v)); s=None
CROP={'chat':(620,230,1220,770),'revit':(640,280,1280,680),'full':(0,0,1920,1080),'claude':(480,60,920,940)}
def speech(a,b,minsil=1.0,pad=0.15):
    segs=[];cur=a
    for x,y in sil:
        if y-x<minsil or y<=a or x>=b: continue
        x2=max(a,x+pad); y2=min(b,y-pad)
        if x2>cur: segs.append((cur,x2))
        cur=max(cur,y2)
    if b>cur: segs.append((cur,b))
    return [(x,y) for x,y in segs if y-x>0.35]
for c in json.load(open('clips.json')):
    parts=[]
    for a,b,kind in c['win']:
        for x,y in speech(a,b): parts.append((x,y,kind))
    dur=sum(y-x for x,y,_ in parts)
    print(c['id'],len(parts),'tramos',round(dur,1),'s',file=sys.stderr)
    args=['ffmpeg','-v','error','-y']
    for x,y,_ in parts: args+=['-ss',f'{x:.2f}','-t',f'{y-x:.2f}','-i',SRC]
    args+=['-loop','1','-i',f'marco-{c["id"]}.png']
    f=[]
    for i,(x,y,k) in enumerate(parts):
        cx,cy,cw,ch=CROP[k]
        f.append(f'[{i}:v]crop={cw}:{ch}:{cx}:{cy},scale=1080:1100:force_original_aspect_ratio=decrease:flags=lanczos,pad=1080:1100:(ow-iw)/2:(oh-ih)/2:color=0x0f2a4a,setsar=1,fps=30[v{i}]')
        f.append(f'[{i}:a]aresample=48000,afade=t=in:d=0.04,afade=t=out:st={max(0,y-x-0.05):.2f}:d=0.05[a{i}]')
    n=len(parts)
    f.append(''.join(f'[v{i}][a{i}]' for i in range(n))+f'concat=n={n}:v=1:a=1[cv][ca]')
    f.append('color=c=0x0f2a4a:s=1080x1920:r=30[bg]')
    f.append('[bg][cv]overlay=0:480:shortest=1[b1]')
    f.append(f'[b1][{n}:v]overlay=0:0:shortest=1,format=yuv420p[ov]')
    f.append('[ca]loudnorm=I=-14:TP=-1.5:LRA=11[oa]')
    args+=['-filter_complex',';'.join(f),'-map','[ov]','-map','[oa]','-t',f'{dur:.2f}','-c:v','libx264','-crf','20','-preset','medium','-c:a','aac','-b:a','192k','-movflags','+faststart',f'{c["id"]}.mp4']
    subprocess.run(args,check=True)
