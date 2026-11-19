/* Tutor IA · Design Modeling Academy — video pizarrón para publicidad (9:16, con voz).
 * Cada escena dura lo que su frase de voz (audio/lN.wav) + un respiro. window.__VO guarda cuándo empieza
 * cada frase para montar la voz encima. Datos: lanzamiento-tutor-ia-octubre.json y el tutor real.
 */
const VOD = [5.99, 8.38, 4.13, 7.03, 7.27, 4.50, 8.58, 4.39, 7.65];   // duración de cada frase (s)
const AMBAR = '#E8A04A', NAVY = '#0E2438', AZUL = '#003E5C', NARANJA = '#CA7520';

bootVideo(async (V) => {
  const { el, P, T, H, PAL, INK, draw, write, pop, popIn, type, comic, stamp, wobble, mover, jump, bubble, sfx,
          face, emote, arms, wave, blink, wink, hop, wiggle, take,
          mascot, drawMascot, popMascot, person, popPerson, image,
          newScene, show, BG, TR, finale, setTool, tl, S } = V;
  const { chalk: CHALK, chalkB: CHALK_B, graphite: GRAPHITE, cream: CREAM } = PAL;
  const VO = window.__VO = [];
  const vo = a => VO.push(+(a + 0.15).toFixed(3));
  const plano = g => {   // fondo de marca: navy con cuadrícula de plano
    el('rect', { x: -60, y: -60, width: 1200, height: 2040, fill: NAVY }, g);
    el('rect', { x: -60, y: -60, width: 1200, height: 2040, fill: 'url(#bpMinor)' }, g);
    el('rect', { x: -60, y: -60, width: 1200, height: 2040, fill: 'url(#bpMajor)' }, g);
  };
  const azul = g => { el('rect', { x: -60, y: -60, width: 1200, height: 2040, fill: AZUL }, g); el('rect', { x: -60, y: -60, width: 1200, height: 2040, fill: 'url(#halftone)' }, g); };
  let t = 0;

  /* 1 · GANCHO (papel + plumón): rebobinar la clase */
  const s1 = newScene('paper'); show(s1, 0); setTool('marker');
  { const g = s1.g, a = 0.1; vo(a);
    write(T(g, 540, 330, '¿En qué clase', { size: 140 }), a + 0.15, 0.6);
    write(T(g, 540, 470, 'lo explicaron?', { size: 140, color: NARANJA }), a + 0.8, 0.6);
    draw(P(g, 'M150,640 L930,640 L930,1120 L150,1120 Z', { w: 8, fill: H('black') }), a + 1.3, 0.5);
    draw(P(g, 'M490,800 L490,960 L620,880 Z', { color: CREAM, w: 7, fill: H('white') }), a + 1.8, 0.3, { sound: false });
    draw(P(g, 'M170,1210 L910,1210', { w: 10, color: '#B9B2A6' }), a + 2.0, 0.4, { sound: false });
    const ph = el('circle', { cx: 800, cy: 1210, r: 24, fill: NARANJA, stroke: INK, 'stroke-width': 6, opacity: 0 }, g);
    tl.to(ph, { attr: { opacity: 1 }, duration: S(0.1) }, S(a + 2.3));
    [[260, 0.5], [640, 0.45], [330, 0.45], [720, 0.4], [210, 0.45]].forEach(([x, d], k) => { tl.to(ph, { attr: { cx: x }, duration: S(d), ease: 'power2.inOut' }, S(a + 2.5 + k * 0.62)); sfx('whoosh', a + 2.5 + k * 0.62, { gain: 0.35 }); });
    pop(T(g, 540, 1320, 'rebobinando una hora de video...', { size: 58, color: PAL.red, cls: 'kalam' }), a + 3.3, { rot: -3 });
    const pm = mover(g, 820, 1790, 1.1), d = person(pm.g, 0, 0, 1, { shirt: 'teal', glasses: true });
    popPerson(d, a + 2.6); face(d, a + 3.4, 'swirl', { mouth: 'flat', emote: 'sweat' }); face(d, a + 5.0, 'sad', { mouth: 'frown' });
    t = a + VOD[0] + 0.5;
  }
  const s2 = newScene('chalk', { filter: 'url(#chalk)' });
  t = TR.zoomInto(s1, s2, t, { x: 540, y: 880 });

  /* 2 · EL PROBLEMA (pizarra + gis): 133 horas */
  setTool('chalk');
  { const g = s2.g, a = t; vo(a);
    write(T(g, 540, 330, 'Diplomado BIM en Estructuras', { size: 66, color: '#C9D2CC', cls: 'kalam' }), a + 0.2, 1.0);
    write(T(g, 540, 590, '133 horas', { size: 230, color: PAL.chalkO }), a + 1.6, 0.9);
    write(T(g, 540, 680, 'de clase grabada', { size: 70, color: CHALK, cls: 'kalam' }), a + 2.5, 0.7);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
      const x = 130 + c * 140, y = 790 + r * 110, k = r * 6 + c;
      draw(P(g, `M${x},${y} L${x + 110},${y} L${x + 110},${y + 80} L${x},${y + 80} Z`, { color: CHALK, w: 5 }), a + 3.0 + k * 0.05, 0.12, { sound: k === 0 });
      draw(P(g, `M${x + 45},${y + 22} L${x + 45},${y + 58} L${x + 72},${y + 40} Z`, { color: CHALK, w: 4 }), a + 3.1 + k * 0.05, 0.08, { sound: false, tool: null });
    }
    write(T(g, 540, 1370, 'la respuesta está grabada...', { size: 78, color: CHALK }), a + 4.6, 1.0);
    write(T(g, 540, 1540, '¿pero en qué minuto?', { size: 118, color: CHALK_B, rot: -4 }), a + 6.0, 0.9);
    draw(P(g, wobble(760, 1050, 80, 55, 1.1, 3), { color: PAL.chalkO, w: 9 }), a + 6.9, 0.5);
    t = a + VOD[1] + 0.5;
  }
  const s3 = newScene(plano);
  t = TR.eraser(s2, s3, t);

  /* 3 · EL GIRO (plano DMA): el Tutor IA */
  setTool(null);
  let bot3;
  { const g = s3.g, a = t; vo(a);
    pop(T(g, 540, 330, 'Por eso, ahora tu curso tiene', { size: 84, color: '#FFFFFF' }), a + 0.1);
    const m = mover(g, 298, 560, 2.2); bot3 = mascot(m.g, 0, 0, 1, { theme: 'brand', ink: '#FFFFFF', ground: null, shadow: 'shadowW' });
    drawMascot(bot3, a + 0.4, 1.0);
    pop(T(g, 540, 1250, 'Tutor IA', { size: 220, color: AMBAR, stroke: '#FFFFFF' }), a + 1.9, { sound: 'ding' });
    pop(T(g, 540, 1370, 'dentro de tu curso', { size: 70, color: '#C9D8E6', cls: 'kalam' }), a + 2.6, { rot: 0, sound: false });
    face(bot3, a + 2.1, 'happy', { mouth: 'grin', emote: 'sparkle' }); wave(bot3, 'R', a + 2.4, 3, { from: 110, to: 70 });
    t = a + VOD[2] + 0.5;
  }
  const s4 = newScene(azul);
  t = TR.iris(s3, s4, t, { x: 540, y: 740 });

  /* 4 · CÓMO SE USA (azul DMA): la pregunta con tus palabras */
  let q;
  { const g = s4.g, a = t; vo(a);
    pop(T(g, 540, 300, 'Le escribes la duda', { size: 104, color: '#FFFFFF' }), a + 0.1);
    pop(T(g, 540, 410, 'con tus palabras', { size: 104, color: AMBAR }), a + 0.6, { rot: 0 });
    q = bubble(g, 90, 620, 990, 1060, 330, 1400);
    popIn(q, a + 2.0, { origin: '30% 100%' });
    type(T(q, 150, 780, '¿Cómo creo el espectro sísmico', { size: 50, anchor: 'start', cls: 'kalam', color: INK }), a + 2.6, 1.6, NARANJA);
    type(T(q, 150, 880, 'y lo ingreso en Robot?', { size: 50, anchor: 'start', cls: 'kalam', color: INK }), a + 4.3, 1.1, NARANJA);
    pop(T(q, 540, 990, 'pregunta real de un alumno', { size: 36, color: '#6B6259', cls: 'kalam' }), a + 5.6, { rot: 0, sound: false });
    const pm = mover(g, 330, 1790, 1.15), d = person(pm.g, 0, 0, 1, { shirt: 'teal', glasses: true });
    popPerson(d, a + 1.0); face(d, a + 1.6, 'lookU', { mouth: 'smile' }); face(d, a + 5.2, 'happy', { mouth: 'grin' });
    t = a + VOD[3] + 0.5;
  }
  const s5 = newScene('notebook');
  t = TR.burstDrop(s4, s5, t, { burst: q });

  /* 5 · LA RESPUESTA (cuaderno + lápiz): lección y minuto */
  setTool('pencil');
  { const g = s5.g, a = t; vo(a);
    write(T(g, 560, 300, 'Te responde con tus clases:', { size: 84, color: GRAPHITE }), a + 0.2, 1.1);
    draw(P(g, 'M150,430 L930,430 L930,960 L150,960 Z', { color: GRAPHITE, w: 6, fill: H('cream') }), a + 1.5, 0.5);
    write(T(g, 540, 580, 'Módulo 2', { size: 120, color: GRAPHITE }), a + 3.3, 0.5);
    write(T(g, 540, 730, 'Lección 25', { size: 120, color: GRAPHITE }), a + 4.4, 0.6);
    write(T(g, 540, 900, 'min 04:09', { size: 150, color: NARANJA }), a + 5.6, 0.7);
    draw(P(g, 'M160,1110 L920,1110', { color: '#B9B2A6', w: 10 }), a + 2.0, 0.4, { sound: false });
    const ph = el('circle', { cx: 160, cy: 1110, r: 22, fill: NARANJA, stroke: GRAPHITE, 'stroke-width': 5, opacity: 0 }, g);
    tl.to(ph, { attr: { opacity: 1 }, duration: S(0.1) }, S(a + 2.4));
    tl.to(ph, { attr: { cx: 590 }, duration: S(0.5), ease: 'back.out(1.6)' }, S(a + 6.1)); sfx('ding', a + 6.6);
    pop(T(g, 540, 1210, 'Diplomado BIM en Estructuras · respuesta real', { size: 42, color: '#6E6A63', cls: 'kalam' }), a + 6.3, { rot: 0, sound: false });
    const m = mover(g, 610, 1330, 1.05), c = mascot(m.g, 0, 0, 1, { theme: 'brand' });
    popMascot(c, a + 1.0); face(c, a + 3.0, 'lookU', { mouth: 'smile' }); face(c, a + 6.4, 'star', { mouth: 'grin', emote: 'sparkle' }); hop(c, a + 6.8, 2);
    t = a + VOD[4] + 0.5;
  }
  const s6 = newScene('graph');
  t = TR.slideUp(s5, s6, t);

  /* 6 · PRUEBA (papel milimetrado + captura real): cita la fuente */
  setTool(null);
  { const g = s6.g, a = t; vo(a);
    pop(T(g, 540, 330, 'Te cita la fuente', { size: 116 }), a + 0.1);
    pop(T(g, 540, 440, 'para ir directo al minuto exacto', { size: 58, color: PAL.gray, cls: 'kalam' }), a + 0.6, { rot: 2 });
    const cap = el('g', {}, g); el('rect', { x: 84, y: 594, width: 912, height: 499, rx: 26, fill: '#D5E1F4' }, cap);
    image(cap, 'assets/cap-fuentes.png', 90, 600, 900, 487); popIn(cap, a + 1.0, { origin: '50% 50%' });
    draw(P(g, wobble(849, 839, 125, 52, 1.12, 5), { color: NARANJA, w: 8 }), a + 2.6, 0.5, { tool: 'marker' });
    pop(T(g, 540, 1180, 'respuesta real del tutor de la Especialización en Acero', { size: 38, color: '#6E7B8F', cls: 'kalam' }), a + 1.6, { rot: 0, sound: false });
    const m = mover(g, 610, 1330, 1.0), c = mascot(m.g, 0, 0, 1, { theme: 'brand', ground: null });
    popMascot(c, a + 1.8); arms(c, a + 2.5, { R: -65, dur: 0.2 }); face(c, a + 2.6, 'lookU', { mouth: 'o', emote: '!' });
    t = a + VOD[5] + 0.5;
  }
  const s7 = newScene('kraft');
  t = TR.flip(s6, s7, t);

  /* 7 · CONFIANZA (kraft + pincel): no inventa */
  setTool('brush');
  let card7;
  { const g = s7.g, a = t; vo(a);
    write(T(g, 540, 320, 'Si no está en tus clases...', { size: 96, color: '#2A1B10' }), a + 0.2, 1.0);
    card7 = el('g', {}, g); el('rect', { x: 134, y: 474, width: 812, height: 380, rx: 26, fill: '#9C7F45', opacity: .5 }, card7);
    image(card7, 'assets/cap-sin-inventar.png', 140, 470, 800, 369); popIn(card7, a + 1.3, { origin: '50% 50%' });
    stamp(g, 700, 960, 'NO INVENTA', a + 3.3, { color: '#1F7A4D', rot: -10, size: 92 });
    const m = mover(g, 180, 1060, 1.2), c = mascot(m.g, 0, 0, 1, { theme: 'brand' });
    popMascot(c, a + 2.2); face(c, a + 2.6, 'normal', { mouth: 'flat', emote: '?' }); face(c, a + 3.6, 'happy', { mouth: 'grin' });
    write(T(g, 540, 1500, 'Las cifras de norma:', { size: 84, color: '#2A1B10' }), a + 5.0, 0.8);
    write(T(g, 540, 1620, 'a verificar en la norma vigente', { size: 66, color: '#1F3F5B', cls: 'kalam' }), a + 6.0, 1.0);
    t = a + VOD[6] + 0.5;
  }
  const s8 = newScene(BG.sunburst(AMBAR, '#EDB468'));
  t = TR.expand(s7, s8, t, { x: 134, y: 474, w: 812, h: 380, color: AMBAR });

  /* 8 · ACCESO (sol ámbar, tipografía cinética): a cualquier hora, 20 al día */
  { const g = s8.g, a = t; vo(a);
    pop(T(g, 540, 320, 'Dentro de tu curso', { size: 104, color: CREAM, stroke: INK }), a + 0.1);
    pop(T(g, 540, 430, 'a cualquier hora', { size: 90 }), a + 0.7, { rot: 4 });
    el('circle', { cx: 540, cy: 800, r: 210, fill: CREAM, stroke: INK, 'stroke-width': 9 }, g);
    for (let k = 0; k < 12; k++) { const an = k / 12 * Math.PI * 2; el('line', { x1: 540 + Math.sin(an) * 180, y1: 800 - Math.cos(an) * 180, x2: 540 + Math.sin(an) * 198, y2: 800 - Math.cos(an) * 198, stroke: INK, 'stroke-width': 7 }, g); }
    const hand = el('g', {}, g); el('line', { x1: 540, y1: 800, x2: 540, y2: 640, stroke: INK, 'stroke-width': 10, 'stroke-linecap': 'round' }, hand);
    const hr = { r: 0 }; tl.to(hr, { r: 720, duration: S(3.6), ease: 'power1.inOut' }, S(a + 0.4));
    V.onFrame(() => hand.setAttribute('transform', `rotate(${hr.r.toFixed(2)} 540 800)`));
    el('circle', { cx: 540, cy: 800, r: 16, fill: INK }, g);
    pop(T(g, 540, 1340, '20', { size: 280, color: CREAM, stroke: INK }), a + 2.2, { sound: 'stamp' });
    pop(T(g, 540, 1460, 'preguntas al día', { size: 96 }), a + 2.7, { rot: -3 });
    t = a + VOD[7] + 0.5;
  }
  const s9 = newScene('paper');
  t = TR.flash(s8, s9, t);

  /* 9 · CIERRE (papel + plumón): quién lo tiene */
  setTool('marker');
  { const g = s9.g, a = t; vo(a);
    write(T(g, 540, 330, 'Ya lo tienen:', { size: 130 }), a + 0.2, 0.7);
    draw(P(g, 'M110,430 L970,430 L970,640 L110,640 Z', { w: 7, fill: H('cream') }), a + 1.0, 0.35);
    write(T(g, 540, 525, 'Diplomado BIM', { size: 96 }), a + 1.3, 0.6);
    write(T(g, 540, 605, 'en Estructuras', { size: 62, color: NARANJA, cls: 'kalam' }), a + 1.9, 0.5);
    draw(P(g, 'M110,700 L970,700 L970,910 L110,910 Z', { w: 7, fill: H('cream') }), a + 2.5, 0.35);
    write(T(g, 540, 795, 'Especialización', { size: 96 }), a + 2.8, 0.6);
    write(T(g, 540, 875, 'en Acero', { size: 62, color: NARANJA, cls: 'kalam' }), a + 3.4, 0.4);
    const m = mover(g, 364, 1000, 1.6), c = mascot(m.g, 0, 0, 1, { theme: 'brand' });
    drawMascot(c, a + 3.6, 0.9); face(c, a + 4.7, 'happy', { mouth: 'grin' }); wave(c, 'R', a + 4.8, 3, { from: 110, to: 70 });
    write(T(g, 540, 1500, 'Pregúntale a tus clases', { size: 116, color: NARANJA }), a + 5.2, 0.9);
    draw(P(g, 'M170,1540 C400,1560 700,1525 910,1545', { color: AZUL, w: 8 }), a + 6.2, 0.4);
    t = a + VOD[8] + 0.6;
  }

  /* FINAL + CTA: mosaico de escenas, «Pide información» y el logo */
  t = finale(t, {
    resets: [[q, { scale: 1, opacity: 1 }]],
    cta: (layer, at) => {
      const m = mover(layer, 90, 1560, 0.62), c = mascot(m.g, 0, 0, 1, { theme: 'brand', ground: null });
      popMascot(c, at + 1.6); face(c, at + 2.1, 'happy', { mouth: 'grin' }); hop(c, at + 2.4, 4, false);
      pop(T(layer, 600, 1690, 'Pide información', { size: 108, color: '#FBF3E6' }), at + 1.9, { sound: 'ding' });
      const lg = el('g', { opacity: 0 }, layer); image(lg, 'assets/logo.png', 330, 1740, 480, 148);
      tl.to(lg, { attr: { opacity: 1 }, duration: S(0.4) }, S(at + 2.4));
    },
  });
  return t;
}, {
  speed: 1, mode: 'B',
  palette: { orange: NARANJA },
  hatches: { brand: [AMBAR, '#B7792F'] },
  mascotTheme: 'brand',
  // robot del Tutor IA: cabeza-cuerpo redondeada con antena, dos piernas y brazos cortos
  mascotShape: {
    body: 'M20,6 Q100,0 180,6 Q198,8 198,26 L198,118 Q198,138 180,138 L20,138 Q2,138 2,118 L2,26 Q2,8 20,6 Z M94,6 L94,-26 L106,-26 L106,6 Z M88,-38 A12,12 0 1,1 112,-38 A12,12 0 1,1 88,-38 Z',
    armL: 'M3,62 L-22,62 Q-28,62 -28,68 L-28,90 Q-28,96 -22,96 L3,96 Z',
    armR: 'M197,62 L222,62 Q228,62 228,68 L228,90 Q228,96 222,96 L197,96 Z',
    legs: [48, 128].map(x => `M${x},136 L${x},164 Q${x},171 ${x + 7},171 L${x + 17},171 Q${x + 24},171 ${x + 24},164 L${x + 24},136 Z`),
    eyes: [[66, 66], [134, 66]], mouth: [100, 106],
    pivotL: [3, 79], pivotR: [197, 79], handL: [-28, 79], handR: [228, 79],
    width: 220, height: 171, offsetX: 10, emoteAt: [205, -50],
  },
});
