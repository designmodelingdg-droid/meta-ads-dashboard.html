# Reemplaza el fondo de cada pre-segmento: segmenta a la persona (MediaPipe
# selfie multiclass) y la compone sobre el fondo blueprint de Revit.
import subprocess, sys
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

W, H = 1188, 2112
SW, SH = 297, 528  # resolucion de inferencia (1/4)
FONDO = cv2.imread("fondo_1188x2112.png").astype(np.float32)

SEGS = ["H1", "H2a", "H2b", "D1", "D2a", "D2b", "D3", "C1", "C2a", "C2b"]

def make_segmenter():
    opts = vision.ImageSegmenterOptions(
        base_options=mp_python.BaseOptions(model_asset_path="selfie_multiclass.tflite"),
        running_mode=vision.RunningMode.VIDEO,
        output_confidence_masks=True,
        output_category_mask=False,
    )
    return vision.ImageSegmenter.create_from_options(opts)

for name in SEGS:
    seg = make_segmenter()
    cap = cv2.VideoCapture(f"pre_{name}.mp4")
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
         "-s", f"{W}x{H}", "-r", "30", "-i", "-",
         "-c:v", "libx264", "-crf", "14", "-preset", "fast",
         "-pix_fmt", "yuv420p", f"compv_{name}.mp4"],
        stdin=subprocess.PIPE)
    n = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.resize(frame, (SW, SH), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        res = seg.segment_for_video(mp_img, int(n * 33.34))
        bg_conf = res.confidence_masks[0].numpy_view()
        person = 1.0 - bg_conf
        # apretar el borde (evita halo de la pared) y emplumar
        person = np.clip((person - 0.35) / 0.35, 0, 1).astype(np.float32)
        person = cv2.erode(person, np.ones((5, 5), np.uint8))
        person = cv2.GaussianBlur(person, (0, 0), 3)
        m = cv2.resize(person, (W, H), interpolation=cv2.INTER_LINEAR)
        m = cv2.GaussianBlur(m, (0, 0), 2)[:, :, None]
        out = frame.astype(np.float32) * m + FONDO * (1 - m)
        enc.stdin.write(out.astype(np.uint8).tobytes())
        n += 1
    cap.release()
    enc.stdin.close()
    enc.wait()
    seg.close()
    # audio del pre-segmento
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"compv_{name}.mp4",
                    "-i", f"pre_{name}.mp4", "-map", "0:v", "-map", "1:a",
                    "-c", "copy", f"comp_{name}.mp4"], check=True)
    print(f"comp_{name}.mp4 ({n} frames)")
print("listo")
