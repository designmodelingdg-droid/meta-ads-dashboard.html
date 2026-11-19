# Tutor IA · DMA — video para publicidad

Primera prueba del skill `video-pizarra` con la marca (28-sep-2026). Vertical 9:16, ~42 s, solo texto en
pantalla y efectos de sonido (sin voz ni música: no hay llave de Suno). Estilo `dma-plano`.

Se vuelve a generar copiando `.claude/skills/video-pizarra/template-estilos/` a una carpeta de trabajo,
poniendo aquí dentro `video.js` y `assets/cap-*.png`, y corriendo
`CHROME_PATH=/opt/pw-browsers/chromium ./build.sh tutor-ia-dma`.

| # | Escena | Texto en pantalla | Qué pasa | Fuente del dato |
|---|---|---|---|---|
| 1 | hook | Tienes la respuesta **grabada** en algún minuto de tus clases. | Se dibuja el pórtico del plano y aparece el robot ámbar del tutor | Copy del reel propio del tutor |
| 2 | statement | Lo difícil era **encontrarla.** · 133 horas en el Diplomado, 135 en la Especialización en Acero | — | `lanzamiento-tutor-ia-octubre.json` (133 h) y la cabecera real del tutor del Acero (135 h) |
| 3 | media | Ahora tu curso tiene **Tutor IA** | Cabecera real del tutor: «Responde con las clases de tus 4 cursos — 135 horas indexadas · 0 de 20» | `video-tutor-ia/tutor-limpio.mp4` |
| 4 | hook + pregunta | Le preguntas **con tus palabras** | Se teclea «¿Cómo creo el espectro sísmico y lo ingreso en Robot?» | Prueba real del tutor del Diplomado |
| 5 | statement | Módulo 2 · Lección 25 · **min 04:09** | El robot aparece debajo | La misma prueba real |
| 6 | media | Y te cita **la fuente** | Línea real de FUENTES del tutor del Acero, en 4 renglones | `tutor-limpio.mp4`, segundo 70 |
| 7 | media | Si no está en tus clases, **te lo dice** · las cifras de norma, a la norma vigente | «Lo que no esté en las clases, te lo digo sin inventar», real | `tutor-limpio.mp4`, saludo del tutor |
| 8 | stat | **20** preguntas al día, sin salir de la clase | Cuenta de 0 a 20 | `hechos_del_tutor` y la cabecera real |
| 9 | list | Ya lo **tienen**: Diplomado BIM en Estructuras · Especialización en Acero | — | Los dos únicos programas con tutor |
| 10 | cta | Pregúntale a **tus clases** · botón «Pide información» | Pórtico y robot; logo DMA abajo en todas las escenas | — |

## Lo que no dice, a propósito

- Que sigue el progreso del alumno, que «sabe todo de ingeniería» o que reemplaza al instructor.
- Que lo tienen todos los programas (solo el Diplomado BIM en Estructuras y la Especialización en Acero).
- Precios, ni la palabra TUTOR (dispara lo del Acero). Como es para pauta, el cierre es «Pide información»,
  y el botón del anuncio lleva al formulario o a WhatsApp.
