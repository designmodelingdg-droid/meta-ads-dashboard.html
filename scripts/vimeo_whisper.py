"""Transcribe una clase de Vimeo con faster-whisper (palabras con tiempos).
Solo LEE de Vimeo. Salida: whisper/<id>.json = {"id","name","dur","words":[[w,s,e],...],"segs":[[s,e,texto],...]}"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from vimeo_clips import api, elegir_archivo  # noqa: E402

def main(vid):
    os.makedirs('whisper', exist_ok=True)
    v = api(f'/videos/{vid}?fields=name,duration,download,files')
    link, alto = elegir_archivo(v)
    if not link:
        sys.exit(f'ERROR: sin archivo descargable para {vid}')
    print(f'→ {vid} «{v.get("name","")}» ({v.get("duration")} s, {alto}p)', flush=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', link, '-vn', '-ac', '1', '-ar', '16000', '/tmp/a.wav'], check=True)
    from faster_whisper import WhisperModel
    m = WhisperModel(os.environ.get('MODELO', 'small'), compute_type='int8', cpu_threads=os.cpu_count())
    segs, _ = m.transcribe('/tmp/a.wav', language='es', word_timestamps=True, vad_filter=True,
                           initial_prompt='Clase de ingeniería estructural en Revit, Robot Structural Analysis y Advance Steel: vigas, columnas, zapatas, losas, acero, hormigón armado, conexiones, cerchas, galpones.')
    words, out = [], []
    for s in segs:
        out.append([round(s.start, 2), round(s.end, 2), s.text.strip()])
        words += [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for w in (s.words or []) if w.word.strip()]
    json.dump({'id': vid, 'name': v.get('name', ''), 'dur': v.get('duration'), 'words': words, 'segs': out},
              open(f'whisper/{vid}.json', 'w'), ensure_ascii=False)
    print(f'  {len(words)} palabras', flush=True)

if __name__ == '__main__':
    main(sys.argv[1])
