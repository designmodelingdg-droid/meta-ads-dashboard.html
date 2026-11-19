// Tutor IA · DMA — video para publicidad (9:16, ~41 s, solo texto en pantalla).
// Datos: matriz-viral/matriz/lanzamiento-tutor-ia-octubre.json (hechos_del_tutor) y el reel propio del tutor.
// Capturas: recortes reales de video-tutor-ia/tutor-limpio.mp4 (tutor de la Especialización en Acero).
export default {
  style: 'dma-plano',
  format: '9:16',
  fps: 30,
  person: false,
  mascot: 'bot',
  mascotColor: '#E8A04A',
  captions: false,
  scenes: [
    { type: 'hook', dur: 4.2, kicker: 'Tutor IA · Design Modeling', title: 'Tienes la respuesta *grabada* en algún minuto de tus clases.' },
    { type: 'statement', dur: 3.2, title: 'Lo difícil era *encontrarla.*', sub: '133 horas de clase en el Diplomado. 135 en la Especialización en Acero.' },
    { type: 'media', dur: 4.2, src: 'assets/cap-cabecera.png', title: 'Ahora tu curso tiene *Tutor IA*', caption: 'Dentro del curso, a cualquier hora.' },
    { type: 'hook', dur: 5.0, kicker: 'Ejemplo real', title: 'Le preguntas *con tus palabras*', prompt: '¿Cómo creo el espectro sísmico y lo ingreso en Robot?' },
    { type: 'statement', dur: 4.0, kicker: 'Módulo 2 · te dice la lección y el minuto', title: 'Lección 25\n*min 04:09*', sub: 'Respuesta del tutor del Diplomado BIM en Estructuras.', mascot: true },
    { type: 'media', dur: 5.0, src: 'assets/cap-fuentes.png', title: 'Y te cita *la fuente*', caption: 'Respuesta real del tutor de la Especialización en Acero.' },
    { type: 'media', dur: 4.4, src: 'assets/cap-sin-inventar.png', title: 'Si no está en tus clases, *te lo dice*', caption: 'Y las cifras de norma te las manda a verificar en la norma vigente.' },
    { type: 'stat', dur: 3.6, kicker: 'Incluido en tu programa', value: 20, label: 'preguntas al día, sin salir de la clase', countDur: 1.1 },
    { type: 'list', dur: 4.2, title: 'Ya lo *tienen*', items: ['Diplomado BIM en Estructuras', 'Especialización en Acero'] },
    { type: 'cta', dur: 4.6, title: 'Pregúntale a *tus clases*', sub: 'Diplomado BIM en Estructuras · Especialización en Acero', button: 'Pide información' },
  ],
};
