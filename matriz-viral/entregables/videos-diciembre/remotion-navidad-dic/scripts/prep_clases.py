#!/usr/bin/env python3
"""Fragmentos de clase (Vimeo) de la promo de Navidad: mismo corte que la versión anterior, listo para Remotion."""
import json, os, subprocess
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIM = '/tmp/claude-0/-home-user-meta-ads-dashboard-html/05f669de-6191-5810-b979-eadda86d755b/scratchpad/videos-dic/vim'
CL = [
 dict(id='nav-fragmento-clase-1-reel', vid='1236311667', t0=134.4, t1=169.4, crop='880:640:230:55', hook=['ASÍ SE VE POR DENTRO', 'UN CURSO DE $46.50'], pie='Naves Industriales PRO · 30 horas en SAP2000'),
 dict(id='nav-fragmento-clase-2-reel', vid='1236306840', t0=3.4, t1=33.4, crop='880:640:330:30', hook=['¿ASÍ DISEÑAS', 'TUS ZAPATAS?'], pie='Diseño de Cimentaciones Superficiales aplicado a Proyectos Reales'),
]
for c in CL:
    d = c['t1'] - c['t0']; body = f"{P}/public/clip/{c['id']}.mp4"; voz = f"{P}/audio/{c['id']}-voz.wav"
    vf = f"crop={c['crop']},scale=1000:760:force_original_aspect_ratio=decrease:flags=lanczos,pad=1000:760:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1,fps=30"
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(c['t0']), '-t', str(d), '-i', f"{VIM}/c{c['vid']}.mp4", '-vf', vf,
                    '-af', f'afade=t=in:d=0.1,afade=t=out:st={d - 0.3}:d=0.3', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-g', '30',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', body], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', body, '-vn', '-ac', '1', '-ar', '48000', voz], check=True)
    js = f"{P}/data/{c['id']}.json"; j = json.load(open(js)) if os.path.exists(js) else {}
    j.update(id=c['id'], dur=d, empalmes=[], hook=c['hook'], pie=c['pie'], vtt=f"c{c['vid']}.vtt", t0=c['t0'])
    json.dump(j, open(js, 'w'), ensure_ascii=False, indent=1); print(c['id'], d)
