"""Detecta la tira de participantes de Zoom (recuadros oscuros con el nombre) y devuelve cuándo y dónde taparla.
uso como módulo: intervalos(ruta_video) -> [(t0, t1, x, y, w, h)] en píxeles del video."""
import subprocess, sys, json
import numpy as np, cv2
SW, SH = 640, 360

def cajas(fr):
    g = fr.max(axis=2)
    dark = (g < 52).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(dark, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        vert = 50 <= w <= 115 and h >= 30
        horiz = 30 <= h <= 65 and w >= 55
        if not (vert or horiz) or w * h > SW * SH * 0.2: continue
        roi = g[y:y + h, x:x + w]
        # el texto blanco queda dentro del recuadro: se cuenta sobre la caja completa
        fill = (roi < 52).mean(); br = (roi > 170).mean()
        if fill < 0.72 or not (0.002 <= br <= 0.12): continue
        if y + h > SH * 0.93: continue  # barra de tareas o franja de subtítulos
        out.append((x, y, w, h))
    return out

def intervalos(path, fps=1.0, pad=2.5):
    W, H = [int(v) for v in subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path]).decode().strip().split(',')[:2]]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={SW}:{SH}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    hits = []; k = 0
    while True:
        b = p.stdout.read(SW * SH * 3)
        if len(b) < SW * SH * 3: break
        cs = cajas(np.frombuffer(b, np.uint8).reshape(SH, SW, 3))
        if cs: hits.append((k / fps, cs))
        k += 1
    p.wait(); dur = k / fps
    iv = []
    for t, cs in hits:
        x0 = min(c[0] for c in cs); x1 = max(c[0] + c[2] for c in cs); y1 = max(c[1] + c[3] for c in cs); y0 = min(min(c[1] for c in cs), 36)
        if iv and t - iv[-1][1] <= 2 * pad + 1:
            a = iv[-1]; iv[-1] = [a[0], t, min(a[2], x0), min(a[3], y0), max(a[4], x1), max(a[5], y1)]
        else: iv.append([t, t, x0, y0, x1, y1])
    sx, sy = W / SW, H / SH; res = []
    for a, b, x0, y0, x1, y1 in iv:
        X = max(0, int((x0 - 4) * sx)); Y = max(0, int((y0 - 4) * sy))
        res.append((round(max(0, a - pad), 2), round(min(dur + 1, b + pad), 2), X, Y, min(W, int((x1 + 4) * sx)) - X, min(H, int((y1 + 4) * sy)) - Y))
    return res

def filtro(iv, color='0x0A1624'):
    return ','.join(f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}:t=fill:enable='between(t,{a},{b})'" for a, b, x, y, w, h in iv)

if __name__ == '__main__':
    print(json.dumps(intervalos(sys.argv[1])))
