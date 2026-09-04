---
name: video-reel-edicion
description: |
  Edita un video crudo y lo deja publicable como reel de Design Modeling Academy: corta silencios, pone subtítulos con la tipografía de la casa, mete b-roll en los empalmes, hace zoom in/out y snaps entre cortes, reemplaza el fondo por un blueprint de Revit y cierra con la placa del logo.

  Usa este skill cuando Dayana diga: "video-reel-edicion", "te paso un video crudo", "edítame este video", "córtale los silencios", "ponle subtítulos", "móntame el reel", "hazlo como los videos que hacemos nosotros", "cámbiame el fondo del video", o cuando mande un enlace de Drive con metraje sin editar.

  Probado el 1-sep-2026 con los crudos de "Valor 6" (3 clips de iPhone 4K → reel de 30,4 s).
---

# Skill: video-reel-edicion

Convierte metraje crudo en un reel publicable **sin salir de la sesión**: ffmpeg
y Whisper hacen todo. No hace falta editor de video ni la Mac.

---

## 0. Lo que hay que instalar (una vez por sesión)

```bash
apt-get update -qq && apt-get install -y ffmpeg          # el update primero: sin él da 404
pip install -q faster-whisper                            # el modelo small se baja solo
apt-get install -y libegl1 libgles2                      # solo si se va a cambiar el fondo
pip install -q mediapipe opencv-python-headless          # idem
mkdir -p /usr/share/fonts/truetype/montserrat && cd $_ && \
curl -sL -o Montserrat-ExtraBold.ttf \
  "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-ExtraBold.ttf" && \
fc-cache -f
```

**La fuente variable de google/fonts NO sirve**: libass la renderiza en peso Thin.
Hay que usar la estática del repo de JulietaUla.

---

## 1. Traer el crudo

Si viene en Google Drive, el conector lo lista y la descarga directa funciona
cuando la carpeta está compartida por enlace:

```bash
curl -sL -o crudo.mov "https://drive.google.com/uc?export=download&id=<FILE_ID>"
```

Comprobar SIEMPRE la rotación: los videos de teléfono traen `rotation=-90` en
los metadatos y ffmpeg los endereza solo, pero conviene verlo antes:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream_side_data=rotation -of default=nw=1 crudo.mov
```

---

## 2. Cortar los silencios

```bash
ffmpeg -i crudo.mov -af "silencedetect=noise=-35dB:d=0.45" -f null - 2>&1 | grep silence_
```

Con esos tiempos se arma la lista de segmentos a conservar. **Dejar ~0.1 s de
aire en cada borde**: un corte pegado a la palabra suena cortado.

---

## 3. Transcribir (para los subtítulos)

`faster-whisper`, modelo `small`, español, con timestamps por palabra.

**NUNCA subtitular a ciegas lo que devuelve Whisper.** En la prueba escribió
"chacepete" por ChatGPT y "Forus" por foros. Y hay un error que cuesta dinero:
oyó "comenta bien o guía" donde el CTA real era una palabra clave del bot —
**la palabra del CTA se confirma con Dayana antes de renderizar**, porque es la
que dispara la automatización.

---

## 4. Cortar los segmentos con movimiento

Cada segmento hablado lleva:

- **Zoom lento** in u out, alternando entre segmentos (`zoompan`, de 1.00 a 1.09).
- **Snap de zoom** en el corte: el segmento siguiente arranca en otro nivel
  (uno termina en 1.00 y el próximo entra en 1.12). Eso es lo que da el ritmo.

Escalar la fuente a 1188×2112 ANTES del zoompan y sacar a 1080×1920: si se hace
al revés, el zoom pierde nitidez.

---

## 5. B-roll en los empalmes

Los insertos tapan los saltos entre tomas y las pausas cortadas, además de
ilustrar. Fuente habitual: el comercial Revit+IA
(`dma-sales-assistant/tutor/videos/master-revit-ia-vertical-32s.mp4`).

Entrada y salida con fundido alfa de 0.15 s, nunca corte seco:

```
[broll]format=yuva420p,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=<dur-0.15>:d=0.15:alpha=1,setpts=PTS+<inicio>/TB[b]
[base][b]overlay=enable='between(t,<inicio>,<fin>)':eof_action=pass
```

El audio de la persona sigue corriendo debajo: el overlay es solo video.

---

## 6. Subtítulos estilo DMA

Un `.ass` con: Montserrat ExtraBold 74, MAYÚSCULAS, blanco con borde negro de 6,
bloques de 2-5 palabras, **la palabra clave en ámbar `&H4AA0E8&`** (que es
#E8A04A en BGR — el ASS invierte el orden), pop de entrada
(`\fscx85\fscy85\t(0,90,\fscx100\fscy100)`) y `MarginV 460` para que queden por
encima de la interfaz de reels.

Los tiempos del crudo se mapean al timeline editado sumando el offset de cada
segmento.

---

## 7. Cambiar el fondo (opcional pero es lo que más impresiona)

Segmentación de la persona frame a frame con MediaPipe ImageSegmenter
(`selfie_multiclass_256x256.tflite`, se baja de
`storage.googleapis.com/mediapipe-models/image_segmenter/...`), inferencia a 1/4
de resolución, y el borde apretado con erosión + desenfoque para que no quede
halo de la pared.

El fondo por defecto: un plano real de Revit **invertido estilo blueprint** —
líneas claras sobre azul marino DMA con degradado. Se construye desde
`dma-sales-assistant/tutor/frames-revit/`.

**REGLA: el fondo solo se cambia donde la persona está a cámara.** Los tramos
donde se graba el monitor (el error, ChatGPT, el modelo) se dejan intactos: esa
pantalla ES el contenido y la segmentación la borraría.

---

## 8. Ensamblado final

- Concat **por filtro**, no por demuxer con `-c copy`: el demuxer deja los
  timestamps de audio sucios (DTS no monotónico).
- Placa final: últimos 2,6 s del comercial vertical, o la placa del logo.
- `loudnorm=I=-14:TP=-1.5:LRA=11` — el estándar de loudness de reels.
- Salida H.264 CRF 18, AAC 192k, `+faststart`.
- **Si pasa de 30 MB no se puede enviar por chat**: sacar una copia CRF 22.

---

## 9. Verificar antes de entregar

Extraer un frame por momento clave (hook, cada resalte ámbar, cada b-roll, CTA,
placa) y **mirarlos**. Un subtítulo desincronizado o un b-roll que entra tarde
solo se ve mirando.

---

## Reglas

- **La palabra clave del CTA se confirma antes de renderizar.** Es la que
  dispara el bot; si el subtítulo dice otra cosa, la automatización no salta.
- **Nunca inventar lo que dice la persona.** Si Whisper duda, se pregunta.
- El b-roll ilustra lo que se está diciendo en ese segundo exacto, no se pone
  "para rellenar".
- Verificar con frames, no de memoria.

El método completo, con los tiempos de la primera pieza, está en
`matriz-viral/edicion-reels/PIPELINE.md`.
