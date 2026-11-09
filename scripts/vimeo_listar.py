"""Lista todas las carpetas de Vimeo con sus videos (solo lectura).
Escribe vimeo-clips/indice/carpetas.json y carpetas.md."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from vimeo_clips import paginar, hms  # noqa: E402

def main():
    os.makedirs('vimeo-clips/indice', exist_ok=True)
    cs = paginar('/me/projects', 'uri,name', 2000)
    out, md = [], ['# Carpetas de Vimeo\n']
    for c in sorted(cs, key=lambda c: c['name']):
        pid = c['uri'].split('/')[-1]
        vs = paginar(f'/me/projects/{pid}/videos', 'uri,name,duration,created_time', 500)
        vs = [{'id': v['uri'].split('/')[-1], 'name': v['name'], 'dur': v.get('duration', 0), 'creado': v.get('created_time', '')} for v in vs]
        out.append({'carpeta': c['name'], 'id': pid, 'videos': vs})
        md.append(f"\n## {c['name']} ({len(vs)} videos, {hms(sum(v['dur'] for v in vs))})\n")
        md += [f"- {v['id']} · {hms(v['dur'])} · {v['name']}" for v in sorted(vs, key=lambda v: v['creado'])]
        print(f"{c['name']}: {len(vs)}", flush=True)
    json.dump(out, open('vimeo-clips/indice/carpetas.json', 'w'), ensure_ascii=False, indent=1)
    open('vimeo-clips/indice/carpetas.md', 'w').write('\n'.join(md) + '\n')

if __name__ == '__main__':
    main()
