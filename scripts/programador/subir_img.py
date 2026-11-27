"""Sube las imágenes finales al almacenamiento de la app de contenido y guarda su enlace público.
Uso: PROG_DIR=<carpeta> python3 subir_img.py   (lee img_local.json: {id_de_imagen: ruta absoluta}; escribe img_urls.json)
No envía encabezado Authorization: la llave la pone el proxy del entorno."""
import json,os,subprocess,urllib.request,sys,time
B=os.environ.get('PROG_DIR') or os.getcwd(); U=os.environ.get('DG_CONTENIDO_URL','https://contenido.dgdesignmodeling.com')
need=json.load(open(f'{B}/img_local.json'))
out=f'{B}/img_urls.json'; urls=json.load(open(out)) if os.path.exists(out) else {}
T={'.jpg':'image/jpeg','.png':'image/png','.pdf':'application/pdf'}
for a,rel in need.items():
    if a in urls: continue
    f=rel; ext=os.path.splitext(f)[1]; typ=T[ext]
    try:
        req=urllib.request.Request(f'{U}/api/subir/firmar',data=json.dumps({'files':[{'name':f'{a}{ext}','type':typ}]}).encode(),headers={'Content-Type':'application/json'},method='POST')
        up=json.load(urllib.request.urlopen(req,timeout=60))['uploads'][0]
        r=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-m','120','-X','PUT','-H',f'Content-Type: {typ}','--data-binary',f'@{f}',up['signedUrl']],capture_output=True,text=True)
        if r.stdout!='200': print('FALLO',a,r.stdout,flush=True); continue
        urls[a]=up['publicUrl']; json.dump(urls,open(out,'w'),indent=1)
    except Exception as e:
        print('ERROR',a,str(e)[:200],flush=True); time.sleep(3)
print('hecho',len(urls),'de',len(need))
