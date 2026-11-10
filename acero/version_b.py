import json,subprocess,os,sys,re,wave,numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
les=sys.argv[1].zfill(3)
CU=json.load(open('plan/curso.json'));L={str(l['n']).zfill(3):l for l in CU['lecciones']}
C={k.zfill(3):v for k,v in json.load(open('plan/refinado.json')).items()}
os.makedirs('tmpB',exist_ok=True);mid=f'tmpB/{les}mid.mkv'
segs=C[les];FPS=25
MUTE=json.load(open('plan/mute.json')) if os.path.exists('plan/mute.json') else {}
# 1) intermedio igual que la versión normal
if not os.path.exists(mid):
    inp=['-loop','1','-t','3','-i',f'portadas/p{les}.png','-f','lavfi','-t','3','-i','anullsrc=r=48000:cl=mono']
    fc=['[0:v]scale=1280:720,fps=25,format=yuv420p,fade=t=out:st=2.5:d=0.5,setsar=1[v0]','[1:a]anull[a0]'];k=2;n=len(segs)
    for i,(tr,s,e) in enumerate(segs):
        inp+=['-ss',str(s),'-to',str(e),'-i',f'tramos/{tr}.mp4'];d=e-s
        fi=0.4 if i==0 else 0.15; fo=0.5 if i==n-1 else 0.15
        fc.append(f'[{k}:v]scale=1280:720,fps=25,format=yuv420p,setsar=1,fade=t=in:st=0:d={fi},fade=t=out:st={d-fo:.2f}:d={fo}[v{i+1}]')
        mu=''.join(f",volume=enable='between(t,{a:.2f},{b:.2f})':volume=0" for j,a,b in MUTE.get(les,[]) if j==i)
        fc.append(f'[{k}:a]aresample=48000,aformat=channel_layouts=mono{mu},afade=t=in:st=0:d={min(fi,.3)},afade=t=out:st={d-fo:.2f}:d={fo}[a{i+1}]');k+=1
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n+1))+f'concat=n={n+1}:v=1:a=1[v][ac]')
    fc.append('[ac]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]')
    subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','14','-c:a','pcm_s16le','-ac','1',mid],check=True)
# 2) subtítulos desde el audio
cues_f=f'tmpB/{les}cues.json'
if not os.path.exists(cues_f):
    from faster_whisper import WhisperModel
    M=WhisperModel('small',compute_type='int8',cpu_threads=os.cpu_count())
    subprocess.run(['ffmpeg','-v','error','-y','-i',mid,'-ac','1','-ar','16000','tmpB/a.wav'],check=True)
    wf=wave.open('tmpB/a.wav');au=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
    sg,_=M.transcribe(au,language='es',word_timestamps=True,initial_prompt='Revit Structure, BIM, metodología BIM, AutoCAD, Robot Structural Analysis, Advance Steel, zapatas, columnas, vigas, ejes, niveles, hormigón armado, acero estructural.')
    W=[(w.word.strip(),w.start,w.end) for s in sg for w in s.words if w.word.strip()]
    cues=[];cur=[]
    for w in W:
        if cur and (len(' '.join(x[0] for x in cur+[w]))>64 or w[2]-cur[0][1]>3.4 or w[1]-cur[-1][2]>0.7):
            cues.append([cur[0][1],cur[-1][2]+0.15,' '.join(x[0] for x in cur)]);cur=[]
        cur.append(w)
        if re.search(r'[.?!]$',w[0]) and len(' '.join(x[0] for x in cur))>18:
            cues.append([cur[0][1],cur[-1][2]+0.15,' '.join(x[0] for x in cur)]);cur=[]
    if cur: cues.append([cur[0][1],cur[-1][2]+0.15,' '.join(x[0] for x in cur)])
    json.dump(cues,open(cues_f,'w'),ensure_ascii=False)
cues=json.load(open(cues_f))
# 3) seguimiento del cursor
# elegir la plantilla de cursor que mejor encaja con esta grabación
_cap=cv2.VideoCapture(mid);_N=int(_cap.get(7));best=None
for _p in ['cur_a.png','cur_b.png']:
    _t=cv2.imread(_p,0);hits=0
    for _k in range(40):
        _cap.set(1,int(75+(_N-80)*_k/40));_ok,_f=_cap.read()
        if not _ok: continue
        if cv2.minMaxLoc(cv2.matchTemplate(cv2.cvtColor(_f,cv2.COLOR_BGR2GRAY),_t,cv2.TM_CCOEFF_NORMED))[1]>=0.7: hits+=1
    print('plantilla',_p,hits,flush=True)
    if best is None or hits>best[0]: best=(hits,_t)
_cap.release()
t2=best[1];TH,TW=t2.shape
cap=cv2.VideoCapture(mid);N=int(cap.get(7));pos=np.full((N,2),np.nan);score=np.zeros(N);last=None
prevg=None;chg=np.zeros(N)
for i in range(N):
    ok,f=cap.read()
    if not ok: break
    if i<75: continue
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    if i%2==0:
        r=cv2.matchTemplate(g,t2,cv2.TM_CCOEFF_NORMED);_,mx,_,loc=cv2.minMaxLoc(r)
        if last is not None:
            x0,y0=int(last[0]),int(last[1]);a=max(0,x0-40);b=max(0,y0-40)
            rr=cv2.matchTemplate(g[b:y0+40+TH,a:x0+40+TW],t2,cv2.TM_CCOEFF_NORMED)
            if rr.size:
                _,m2,_,l2=cv2.minMaxLoc(rr)
                if m2>=0.5 and m2>=mx-0.08: mx,loc=m2,(l2[0]+a,l2[1]+b)
        if mx>=0.7 or (mx>=0.55 and last is not None and abs(loc[0]-last[0])+abs(loc[1]-last[1])<40):
            pos[i]=loc;score[i]=mx;last=loc
        else: last=None if mx<0.45 else last
    if prevg is not None: chg[i]=cv2.absdiff(g,prevg).mean()
    prevg=g
# interpolar huecos cortos
idx=np.where(~np.isnan(pos[:,0]))[0]
P=np.full((N,2),np.nan)
for a,b in zip(idx[:-1],idx[1:]):
    P[a]=pos[a]
    if b-a<=12: 
        for j in range(a+1,b): P[j]=pos[a]+(pos[b]-pos[a])*(j-a)/(b-a)
if len(idx): P[idx[-1]]=pos[idx[-1]]
# clics: cursor quieto >=0.3 s y luego cambio de pantalla cerca
clicks=[];still=0
for i in range(76,N):
    if np.isnan(P[i,0]) or np.isnan(P[i-1,0]): still=0;continue
    still = still+1 if np.abs(P[i]-P[i-1]).sum()<1.5 else 0
    if still>=8 and chg[i:i+12].max()>2.0 and (not clicks or i-clicks[-1]>20):
        j=i+int(np.argmax(chg[i:i+12]>2.0)); clicks.append(j); still=0
print('cursor visible',round((~np.isnan(P[75:,0])).mean()*100),'% · clics',len(clicks),flush=True)
json.dump({'clicks':clicks},open(f'tmpB/{les}clicks.json','w'))
# 4) render: video reducido arriba, franja de subtítulos abajo, círculo y onda
font=ImageFont.truetype('fonts/mont800.ttf',21)
try: font.set_variation_by_name('ExtraBold')
except Exception: pass
SW,SH=1209,680;X0=(1280-SW)//2;BG=(48,30,10)
cap=cv2.VideoCapture(mid)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','25','-i','-','-i',mid,'-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','14','-pix_fmt','yuv420p','-c:a','copy',f'tmpB/{les}hq.mkv'],stdin=subprocess.PIPE)
OR=(58,137,232)  # BGR del naranja de marca
ci=0
for i in range(N):
    ok,f=cap.read()
    if not ok: break
    if i<75: enc.stdin.write(f.tobytes());continue
    t=i/FPS
    if not np.isnan(P[i,0]):
        x,y=int(P[i,0])+3,int(P[i,1])+5
        ov=f.copy();cv2.circle(ov,(x,y),20,OR,-1,cv2.LINE_AA);f=cv2.addWeighted(ov,0.28,f,0.72,0)
        cv2.circle(f,(x,y),20,OR,2,cv2.LINE_AA)
    for c in clicks:
        if 0<=i-c<12 and not np.isnan(P[c,0]):
            k=(i-c)/12;x,y=int(P[c,0])+3,int(P[c,1])+5
            ov=f.copy();cv2.circle(ov,(x,y),int(20+30*k),OR,3,cv2.LINE_AA);f=cv2.addWeighted(ov,1-k,f,k,0)
    small=cv2.resize(f,(SW,SH),interpolation=cv2.INTER_AREA)
    canvas=np.zeros((720,1280,3),np.uint8);canvas[:]=BG;canvas[0:SH,X0:X0+SW]=small
    txt=next((c[2] for c in cues if c[0]<=t<=c[1]),None)
    if txt:
        im=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(im)
        w=d.textlength(txt,font=font);d.text(((1280-w)/2,SH+8),txt,font=font,fill=(255,255,255))
        canvas=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
    enc.stdin.write(canvas.tobytes())
enc.stdin.close();enc.wait()
print('listo',f'tmpB/{les}hq.mkv')
