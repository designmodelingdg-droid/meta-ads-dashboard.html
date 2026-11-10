import subprocess,os,sys
src,out=sys.argv[1],sys.argv[2]
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout)
vk=int(0.86*(9.25e6*8/dur-54000)/1000)
for _ in range(5):
    base=['ffmpeg','-v','error','-y','-i',src,'-c:v','libx264','-preset','slow','-b:v',f'{vk}k','-profile:v','high','-pix_fmt','yuv420p','-x264-params','keyint=250:aq-mode=3']
    subprocess.run(base+['-pass','1','-passlogfile','tmpB/pl','-an','-f','mp4','/dev/null'],check=True)
    subprocess.run(base+['-pass','2','-passlogfile','tmpB/pl','-c:a','aac','-b:a','48k','-ac','1','-ar','48000','-movflags','+faststart',out],check=True)
    sz=os.path.getsize(out);print(f'{vk}kbps {sz/1e6:.2f}MB',flush=True)
    if sz<9.4e6: break
    vk=int((vk+48)*9.1e6/sz-48)
