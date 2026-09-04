# Pipeline de edición de reels (probado con "Valor 6")

Primera prueba completa: 2026-09-01, con los 3 crudos de la carpeta de Drive
"Valor 6" (Hook 6.8s + Desarrollo 15.3s + CTA 8.6s, iPhone 4K vertical HEVC).
Resultado: reel de 30.4s en 1080×1920 con silencios cortados, subtítulos,
b-roll del comercial de Revit y placa DMA de cierre.

## Los pasos, en orden

1. **Bajar los crudos de Drive** (si la carpeta está compartida por enlace,
   `curl "https://drive.google.com/uc?export=download&id=<ID>"` funciona directo).
2. **Detectar silencios**: `ffmpeg -af "silencedetect=noise=-35dB:d=0.45"` por clip.
   Con esos tiempos se arma la lista de segmentos a conservar (dejar ~0.1s de aire
   en cada borde del corte).
3. **Transcribir con timestamps por palabra**: `transcribir.py` (faster-whisper,
   modelo `small`, español). OJO: corregir a mano los errores típicos del ASR
   ("chacepete"→ChatGPT, "Forus"→foros) antes de subtitular. Nunca subtitular
   a ciegas lo que devuelve Whisper.
4. **Cortar segmentos con zoom alternado**: `cortar_segmentos.sh`. Cada segmento
   hablado lleva un zoom lento (in o out, alternando) hecho con `zoompan` sobre
   la fuente escalada a 1188×2112 para que el zoom no pierda nitidez al salir
   en 1080×1920. Los cortes de silencio + el cambio de dirección de zoom son
   la "transición" — así se ven los reels de la casa.
5. **B-roll**: los insertos tapan los empalmes feos (el salto entre tomas y las
   pausas cortadas) y se colocan donde el guion los pide. En Valor 6:
   - "me salió este error en Revit" → escena del clash (máster Revit+IA 20.5–22.8s)
   - "una solución que me ahorra 2 horas" → ámbar→verde (máster 23.6–26.4s)
   El audio de ella/él sigue corriendo debajo; el overlay es solo video.
6. **Subtítulos**: `generar_subs.py` produce el .ass — Montserrat ExtraBold 72,
   blanco con borde negro, MAYÚSCULAS, bloques de 2–5 palabras, palabra clave en
   ámbar DMA (#E8A04A), pop de entrada (85%→100% en 90ms), centrados a ~460px
   del borde inferior (zona segura de la UI de reels). Los tiempos se mapean del
   crudo al timeline editado con el offset de cada segmento.
7. **Placa final**: últimos 2.6s del máster vertical de Revit+IA
   (`dma-sales-assistant/tutor/videos/master-revit-ia-vertical-32s.mp4`, 30.0–32.6s)
   con pista de audio silenciosa.
8. **Ensamblado final**: concat por FILTRO (no por demuxer con `-c copy`, que deja
   timestamps de audio sucios), overlays con `enable=between(t,...)`, quemado del
   .ass, y `loudnorm=I=-14:TP=-1.5:LRA=11` (el estándar de loudness de reels).
   Salida: H.264 CRF 18, AAC 192k, `+faststart`.
9. **Verificar con frames**: extraer un frame por momento clave (hook, resaltes,
   cada b-roll, CTA, placa) y mirarlos antes de entregar.

## Herramientas que hay que instalar en la sesión

- `apt-get update && apt-get install -y ffmpeg` (el update primero, si no da 404)
- `pip install faster-whisper` (modelo small se baja solo, ~460MB)
- Montserrat ExtraBold estática (la variable de google/fonts sale en peso Thin
  con libass): `raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-ExtraBold.ttf`
  → `/usr/share/fonts/truetype/montserrat/` + `fc-cache -f`.

## v2: reemplazo de fondo y más transiciones (mismo día)

Dayana pidió mejorar el fondo (la pared mostaza) rellenándolo con una imagen
degradada de Revit, y más transiciones. Lo que se agregó:

- **Fondo nuevo por segmentación de persona** (`componer.py`): MediaPipe
  ImageSegmenter (modelo `selfie_multiclass_256x256.tflite`) saca la máscara de
  la persona frame a frame (inferencia a 1/4 de resolución, borde apretado con
  erosión + desenfoque para que no quede halo de la pared) y la compone sobre
  un fondo fijo. El fondo es un plano real de Revit de su propia clase
  (VIVIENDA) **invertido estilo blueprint** — líneas claras sobre azul marino
  DMA con degradado — para que se reconozca Revit sin competir con la persona.
  REGLA: el fondo solo se cambia en los segmentos donde la persona está a
  cámara (hook y CTA). Los segmentos donde se graba el monitor (el error real,
  ChatGPT) se dejan intactos: esa pantalla ES el contenido, la segmentación
  la borraría.
  Dependencias extra: `pip install mediapipe opencv-python-headless` +
  `apt-get install libegl1 libgles2` + el .tflite de
  `storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/`.
- **Más transiciones**: los segmentos largos se parten en cortes de ~1.5–3s con
  "snap de zoom" (el nivel de zoom salta en el corte: p.ej. un segmento termina
  en 1.00 y el siguiente arranca en 1.12) además del zoom lento in/out dentro
  de cada corte. 10 cortes hablados en 27s.
- **B-roll con fundido**: entrada y salida del b-roll con fade alfa de 0.15s
  en vez de corte seco (`format=yuva420p,fade=...:alpha=1` + overlay).

## Transcripción confirmada por Dayana

- "valides todo lo que hagas **con la IA**" (Whisper había oído "con la guía";
  Dayana confirmó que dice IA). Corregido en v2.
- El CTA quedó subtitulado `COMENTA "GUÍA"`. Whisper oyó "comenta bien o guía";
  si la palabra clave del bot resulta ser otra (¿"QUIERO GUÍA"?), corregir y
  regenerar.
