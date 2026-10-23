"""Recorta a la persona de un video vertical y saca un WebM con alfa (para texto detrás).

Uso: python3 matte.py <entrada.mp4> <salida.webm> [mascara_preview.jpg]
MediaPipe selfie_multiclass (256x256) + filtro guiado + suavizado temporal.
"""
import subprocess, sys, os
import numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

SRC, OUT = sys.argv[1], sys.argv[2]
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "selfie_multiclass.tflite")
cap = cv2.VideoCapture(SRC)
fps = cap.get(cv2.CAP_PROP_FPS); W = int(cap.get(3)); H = int(cap.get(4))
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=MODEL), running_mode=vision.RunningMode.VIDEO,
    output_confidence_masks=True))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "3M", "-deadline", "realtime", "-cpu-used", "8",
                       "-auto-alt-ref", "0", OUT], stdin=subprocess.PIPE)
prev = None; i = 0
while True:
    ok, bgr = cap.read()
    if not ok: break
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    small = cv2.resize(rgb, (W // 3, H // 3))
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=small), int(i * 1000 / fps))
    bg = r.confidence_masks[0].numpy_view()
    m = 1.0 - bg
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    guide = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    m = cv2.ximgproc.guidedFilter(guide, m, 8, 1e-3)
    m = np.clip((m - 0.35) / 0.3, 0, 1)
    # rellenar huecos interiores (camisa blanca confundida con fondo)
    bi = (m > 0.5).astype(np.uint8)
    cs, _ = cv2.findContours(bi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cs:
        big = max(cs, key=cv2.contourArea)
        llen = np.zeros_like(bi); cv2.drawContours(llen, [big], -1, 1, -1)
        llen = cv2.erode(llen, np.ones((9, 9), np.uint8))
        m = np.maximum(m, llen.astype(np.float32))
    if prev is not None:
        m = 0.6 * m + 0.4 * prev
    prev = m
    a = (m * 255).astype(np.uint8)
    ff.stdin.write(np.dstack([rgb, a]).tobytes())
    if i == 120 and len(sys.argv) > 3:
        vis = bgr.copy(); vis[m < 0.5] = (vis[m < 0.5] * 0.2 + np.array([60, 140, 215]) * 0.8).astype(np.uint8)
        cv2.imwrite(sys.argv[3], cv2.resize(vis, (W // 2, H // 2)))
    i += 1
ff.stdin.close(); ff.wait()
print("frames", i)
