# Presentación del Tutor IA — 40 s, 16:9

Video de presentación del Tutor IA de la Especialización en Acero, construido con
**HyperFrames** sobre la grabación de pantalla real del tutor respondiendo.

## Cómo se vuelve a generar

```bash
cd video-tutor-ia
npx hyperframes check     # lint + runtime + contraste
npx hyperframes render    # deja el MP4 en renders/
```

Si falta el kit: `npx skills add heygen-com/hyperframes` desde la raíz del
repositorio.

## Los archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La composición. Es lo único que se edita |
| `22b41840-VIDEO-…mp4` | El metraje original tal como lo grabó Dayana, sin tocar |
| `tutor-limpio.mp4` | El metraje recortado al panel del tutor (ver abajo) |
| `fuentes/` | Overpass y Nunito en local |
| `vendor/gsap.min.js` | GSAP en local |
| `renders/` | Las salidas. No se versiona |

## Tres decisiones que conviene no deshacer

**1. El recorte se hace en el archivo, no en CSS.** El original es una captura de
1920×1080 con el navegador entero: barra de pestañas con las pestañas de trabajo
abiertas, y otra ventana asomando por debajo. `tutor-limpio.mp4` sale de:

```bash
ffmpeg -i <original> -an \
  -vf "crop=1594:830:176:178,scale=1856:966:flags=lanczos,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:0x001E30" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p tutor-limpio.mp4
```

Antes se intentó recortar con transformes en el CSS y se pasó media tarde
peleando con encuadres que cortaban el texto. Arreglarlo en el origen fue más
barato y salió mejor.

**2. El acto del pico no lleva zoom cerrado.** La respuesta ocupa el ancho entero
del panel, y cualquier acercamiento se come el principio y el final de la línea
de FUENTES, que es justo lo único que hay que leer. En su lugar hay una
respiración de 1.00 a 1.06 durante los 10,4 s del acto. **El pico se sostiene con
tiempo, no con zoom.**

**3. Fuentes y GSAP van en local.** Enlazados a un CDN, el render sale con una
tipografía del sistema o directamente no carga. Es la misma razón por la que el
verificador de landings corta la red externa.

## Cosas que se aprendieron peleándose con esto

- Un `<video>` **no puede ir dentro de un elemento con `data-start`**. El
  extractor resuelve el tiempo del vídeo por su cuenta y la visibilidad la
  resuelve el envoltorio: se ven fotogramas equivocados. El vídeo va al raíz.
- Un clip de raíz **siempre se estira a pantalla completa**. Un rótulo con
  `left/bottom` se convierte en un rectángulo gigante. La capa va transparente a
  pantalla completa y el rótulo posicionado **dentro**.
- **GSAP escribe su propio `transform-origin`** (50% 50%) y pisa el del CSS. Si
  el encuadre depende del origen, hay que pasarlo explícito en el tween.
- El vídeo original **no tiene voz**. Whisper transcribió «P-P-P-P-P». La pieza
  es muda a propósito: tipografía y movimiento.

## Los datos que aparecen, y de dónde salen

Todos están en la grabación, ninguno inventado: 4 cursos, 135 horas indexadas,
20 preguntas al día, la etiqueta BETA, y las tres fuentes citadas
(Cerchas y Naves · Clase 4 Naves SAP2000 · min 115:19 · Acero · Sesión 5 ·
min 133:34 · Acero · Sesión 4 · min 26:51).
