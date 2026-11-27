"""Prepara la carpeta de trabajo: horas por pieza e inventario de imágenes locales.
Uso: PROG_DIR=<carpeta> python3 -I preparar.py CALENDARIO.json CARPETA_DE_IMAGENES [CARPETA...]
- horas.json: {id: [hora ISO en UTC]} sacado del calendario del mes (campos id + hora).
- img_local.json: {id_de_imagen: ruta absoluta}. Los archivos locales deben llamarse <id_de_imagen>.jpg|png|pdf,
  con el id que la ficha trae en imagenes[].u ("/_blob/<id>"). Avisa de las que falten."""
import json,glob,os,sys
B=os.environ.get('PROG_DIR') or os.getcwd()
H={}
def walk(o):
    if isinstance(o,dict):
        if 'id' in o and isinstance(o.get('hora'),str) and 'T' in o['hora']: H.setdefault(o['id'],set()).add(o['hora'])
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(json.load(open(sys.argv[1])))
json.dump({k:sorted(v) for k,v in H.items()},open(f'{B}/horas.json','w'))
loc={}
for d in sys.argv[2:]:
    for f in glob.glob(os.path.join(d,'**','*'),recursive=True):
        k,ext=os.path.splitext(os.path.basename(f))
        if os.path.isfile(f) and len(k)==32 and ext in('.jpg','.png','.pdf'): loc.setdefault(k,os.path.abspath(f))
need={};miss=[]
for f in sorted(glob.glob(f'{B}/db/piezas/*.json')):
    d=json.load(open(f)); d=d.get('data',d)
    if d.get('grupo') in('pauta','historias','correos','comunidades'): continue
    if (d.get('estado_prod') or '').startswith(('DESCARTADA','YA ESCRITA','POR GRABAR','EN RESERVA')): continue
    for im in (d.get('imagenes') or [])+([d['pdf']] if d.get('pdf') else []):
        a=im['u'].split('/')[-1]
        if a in loc: need[a]=loc[a]
        else: miss.append((d['id'],a))
json.dump(need,open(f'{B}/img_local.json','w'),indent=1)
print('horas',len(H),'· imágenes necesarias',len(need),'· faltan',miss)
