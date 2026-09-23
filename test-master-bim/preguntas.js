/* Diagnóstico BIM del Máster — las 20 preguntas y cómo se puntúan.
 *
 * Va en archivo aparte a propósito: las preguntas las revisa Gabriel y no
 * tiene por qué pelearse con el resto del código para cambiar una palabra.
 *
 * DOS EJES, y esa es la diferencia con el test de nivel BIM público:
 *
 *   A · NIVEL BIM (14 preguntas, 4 bloques) — qué sabe hacer en un proyecto.
 *   B · BASE TÉCNICA (6 preguntas) — si viene de cálculo estructural o de
 *       arquitectura. El test público no lo pregunta, y es lo que decide con
 *       qué idioma le habla el asesor: al que predimensiona una zapata no se
 *       le vende igual que al que resuelve un programa arquitectónico.
 *
 * La escala es la misma del test público (0-3) porque el equipo ya la conoce
 * y porque «lo hago con ayuda» es la respuesta honesta que más se marca.
 */
const OPCIONES = [
  { v:0, t:'Nunca lo he hecho' },
  { v:1, t:'Lo he visto, entiendo la idea' },
  { v:2, t:'Lo hago con ayuda' },
  { v:3, t:'Lo hago solo y se lo enseño a otro' },
];

/* ── PUNTO DE PARTIDA (añadido 23-sep) ─────────────────────────────────
 *
 * Por qué existe: varios interesados le dijeron a Dayana que el test no tenía
 * dónde decir «todavía no sé nada de BIM». Las 20 preguntas asumen que ya
 * modelas, coordinas o gestionas, así que quien empieza de cero se encontraba
 * con catorce afirmaciones que no le decían nada y sentía que el test no era
 * para él. Y tampoco había forma de decir «a mí lo que me interesa es la IA».
 *
 * Se MUESTRAN primero, pero se GUARDAN al final del enlace. No es un capricho:
 * el enlace del asesor lleva las 20 respuestas como 20 dígitos por posición, y
 * ya hay enlaces enviados. Si estas dos fueran delante, cada enlace viejo se
 * leería corrido una posición. Así, un enlace de 20 dígitos se lee exactamente
 * igual que antes y uno de 22 trae además el punto de partida.
 *
 * Por eso tampoco entran en TODAS: TODAS son las 20 que PUNTÚAN. Estas no
 * puntúan: cuentan desde dónde viene y qué busca.
 */
const ENTRADA = [
  {
    id:'EXP',
    texto:'¿En qué punto estás hoy con BIM?',
    ayuda:'No hay respuesta mala. Es para saber desde dónde empezar contigo.',
    opciones:[
      { v:0, t:'Todavía no he trabajado con BIM',        corto:'Sin experiencia BIM' },
      { v:1, t:'Lo he probado, pero a nivel muy básico', corto:'BIM muy básico' },
      { v:2, t:'Ya lo uso en proyectos reales',          corto:'Usa BIM en proyectos' },
    ],
  },
  {
    id:'INT',
    texto:'¿Qué es lo que más te interesa del Máster?',
    ayuda:'Elige la que más pese. Tu asesor ve las demás en la conversación.',
    opciones:[
      { v:0, t:'Aprender BIM desde la base',                               corto:'BIM desde la base' },
      { v:1, t:'Subir de nivel: coordinar o gestionar proyectos BIM',      corto:'Subir de nivel en BIM' },
      { v:2, t:'Sobre todo la inteligencia artificial y la automatización', corto:'Sobre todo la IA' },
      { v:3, t:'La ruta completa, BIM + IA',                               corto:'La ruta completa' },
    ],
  },
];
/* Quien declara que no ha trabajado con BIM NO pasa por el eje A: esas
 * catorce preguntas son justo las que le hacían sentir que el test no era
 * para él, y su respuesta a todas sería «Nunca lo he hecho». Se guardan como
 * 0 para que el cálculo no cambie, y el panel las marca «No se preguntó»:
 * el asesor no puede enseñar como respuesta algo que la persona no contestó. */
const SIN_BIM = 0;

/* ── EJE A · NIVEL BIM ────────────────────────────────────────────────── */
const BLOQUES = [
  {
    id:'B1', nivel:'Modelador BIM', corto:'Modelador',
    modulo:'BIM Professional · ESTRUCTURA', meses:'3 meses',
    credencial:'Modelador BIM',
    preguntas:[
      'Configuro un proyecto desde cero: plantilla, unidades, niveles, rejillas y nomenclatura.',
      'Creo familias paramétricas, con parámetros de tipo y de instancia.',
      'Genero planos, cortes y cuadros de cantidades automáticamente desde el modelo.',
      'Aplico el LOD que corresponde a cada entregable y sé justificar por qué ese y no otro.',
    ],
  },
  {
    id:'B2', nivel:'Coordinador BIM', corto:'Coordinador',
    modulo:'BIM Coordination · COORDINA', meses:'3 meses',
    credencial:'Coordinador BIM',
    preguntas:[
      'Federo modelos de varias especialidades manteniendo el origen compartido.',
      'Corro detección de interferencias y separo las que importan del ruido.',
      'Llevo el flujo de información del proyecto: quién entrega qué, cuándo y en qué formato.',
      'Levanto un BEP y lo sigo contra lo que de verdad pide el cliente.',
    ],
  },
  {
    id:'B3', nivel:'BIM Manager 4D-5D', corto:'BIM Manager',
    modulo:'BIM Management · GESTIONA', meses:'2 meses',
    credencial:'BIM Manager 4D-5D',
    preguntas:[
      'Vinculo el modelo a un cronograma y simulo la secuencia constructiva.',
      'Extraigo mediciones del modelo y las conecto al presupuesto.',
      'Respondo por el entregable ante el cliente: fijo estándares y audito que se cumplan.',
    ],
  },
  {
    id:'B4', nivel:'Especialista BIM + IA', corto:'BIM + IA',
    modulo:'BIM + IA · AUTOMATIZA', meses:'3 meses',
    credencial:'Especialista BIM + IA',
    preguntas:[
      'Automatizo tareas repetitivas con Dynamo o con scripts.',
      'Uso IA sobre información del proyecto y sé comprobar cuándo se equivocó.',
      'Decido qué se automatiza y qué no en el flujo del equipo, no solo en el mío.',
    ],
  },
];

/* ── EJE B · BASE TÉCNICA ─────────────────────────────────────────────── */
const EJES = [
  {
    id:'EST', nombre:'Cálculo y diseño estructural',
    preguntas:[
      'Predimensiono vigas, columnas y cimentación, y sé de dónde sale cada número.',
      'Leo una memoria de cálculo y detecto cuándo un resultado no tiene sentido.',
      'Trabajo con normativa estructural: cargas, combinaciones y criterios de diseño.',
    ],
  },
  {
    id:'ARQ', nombre:'Arquitectura y edificación',
    preguntas:[
      'Resuelvo un programa arquitectónico: áreas, circulaciones y relación entre espacios.',
      'Manejo normativa de edificación: accesibilidad, evacuación y habitabilidad.',
      'Documento el proyecto para obra: detalles constructivos y especificaciones.',
    ],
  },
];

/* Un bloque se considera DOMINADO con ≥70% de su puntaje máximo. El nivel es
 * el último bloque dominado SIN saltos: quien domina B1 y B3 pero no B2 es un
 * Modelador con conocimientos sueltos, no un BIM Manager — y esa distinción
 * es justo la que el asesor necesita antes de la llamada. */
const UMBRAL = 0.70;
const UMBRAL_EJE = 0.60;   // 6 de 9 en un eje técnico = base real


/* ─────────────────────────────────────────────────────────────────────────
   EL CÁLCULO VIVE AQUÍ, no en cada página.
   Lo usan el test (app.html) y el panel del asesor (resultado.html). Si cada
   uno tuviera su copia, tarde o temprano dirían cosas distintas del mismo
   alumno — y el peor sitio para descubrirlo es delante del cliente.
   ───────────────────────────────────────────────────────────────────────── */

/* Lista plana de las 20 preguntas, en el orden en que se responden. */
const TODAS = [];
BLOQUES.forEach((b,bi) => b.preguntas.forEach(t =>
  TODAS.push({ texto:t, tipo:'bloque', idx:bi, grupo:b.nivel })));
EJES.forEach((e,ei) => e.preguntas.forEach(t =>
  TODAS.push({ texto:t, tipo:'eje', idx:ei, grupo:e.nombre })));

function calcular(R, E){
  const bloques = BLOQUES.map((b,i) => {
    const pts = TODAS.reduce((s,q,qi) =>
      s + (q.tipo==='bloque' && q.idx===i ? (R[qi]||0) : 0), 0);
    const max = b.preguntas.length * 3;
    return { ...b, pts, max, pct: pts/max, dominado: pts/max >= UMBRAL };
  });

  /* Nivel = último bloque dominado SIN saltos. Quien domina B1 y B3 pero no
     B2 no es BIM Manager: es un Modelador con piezas sueltas, y decirle otra
     cosa al asesor le hace perder la llamada. */
  let nivel = 0;
  for(let i=0;i<bloques.length;i++){ if(bloques[i].dominado) nivel = i+1; else break; }
  const dispersos = bloques.filter((b,i) => b.dominado && i >= nivel);

  const ejes = EJES.map((e,i) => {
    const pts = TODAS.reduce((s,q,qi) =>
      s + (q.tipo==='eje' && q.idx===i ? (R[qi]||0) : 0), 0);
    const max = e.preguntas.length * 3;
    return { ...e, pts, max, pct: pts/max, base: pts/max >= UMBRAL_EJE };
  });

  const [est, arq] = ejes;
  let perfil, perfilCorto;
  if(est.base && arq.base){ perfil='Perfil mixto: estructuras y arquitectura'; perfilCorto='MIXTO'; }
  else if(est.base){        perfil='Base en cálculo y diseño estructural';     perfilCorto='EST'; }
  else if(arq.base){        perfil='Base en arquitectura y edificación';       perfilCorto='ARQ'; }
  else {                    perfil='Base técnica por consolidar';              perfilCorto='BASE'; }

  const siguiente = nivel < BLOQUES.length ? BLOQUES[nivel] : null;
  const global = Math.round(bloques.reduce((s,b)=>s+b.pts,0) /
                            bloques.reduce((s,b)=>s+b.max,0) * 100);
  /* El código NO cambia de formato: puede estar moviendo algo en GHL. Quien
     declara no tener BIM sale B0, igual que salía antes con catorce ceros. */
  const codigo = `${nivel===0?'B0':BLOQUES[nivel-1].id}-${perfilCorto}-${global}`;
  let nombreNivel = nivel===0 ? 'En camino a Modelador BIM' : BLOQUES[nivel-1].nivel;

  /* Sin punto de partida (E vacío = enlace anterior al 23-sep) todo lo de
     abajo se queda en null y el resultado es idéntico al de siempre. */
  const entrada = E ? {
    exp: ENTRADA[0].opciones.find(o => o.v === E[0]) || null,
    int: ENTRADA[1].opciones.find(o => o.v === E[1]) || null,
  } : null;
  const sinBIM   = !!(entrada && entrada.exp && entrada.exp.v === SIN_BIM);
  const quiereIA = !!(entrada && entrada.int && entrada.int.v === 2);

  if(sinBIM) nombreNivel = 'Sin experiencia BIM todavía';
  else if(nivel===0 && entrada && entrada.exp && entrada.exp.v === 1) nombreNivel = 'Nivel BIM inicial';

  /* Lo que la persona DICE de sí misma contra lo que MARCA. Cuando no
     cuadran es justo lo que el asesor tiene que saber antes de hablar. */
  const avisos = [];
  if(entrada && entrada.exp){
    if(entrada.exp.v === 2 && nivel === 0)
      avisos.push('Dice que usa BIM en proyectos reales, pero no marcó dominio ni del primer '
                + 'bloque (Modelador). Preguntarle qué hace exactamente en esos proyectos.');
    if(entrada.exp.v === 1 && nivel >= 1)
      avisos.push(`Se describe como «muy básico» y sin embargo domina hasta ${BLOQUES[nivel-1].corto}. `
                + 'Se está infravalorando: conviene decírselo en la llamada.');
  }
  if(quiereIA){
    if(nivel === 0)
      avisos.push('Le interesa sobre todo la IA, pero todavía no tiene base BIM. La IA del Máster '
                + 'automatiza sobre modelos BIM (Dynamo, scripts, datos del proyecto): sin esa base '
                + 'no tiene sobre qué trabajar. La IA es el destino; la base BIM es el camino.');
    else if(nivel < BLOQUES.length)
      avisos.push(`Le interesa sobre todo la IA y ya tiene base (${BLOQUES[nivel-1].corto}). `
                + 'Enseñarle dónde entra la IA en su ruta: el módulo BIM + IA · AUTOMATIZA.');
  }

  return { bloques, nivel, nombreNivel, dispersos, ejes, est, arq,
           perfil, perfilCorto, siguiente, global, codigo,
           entrada, sinBIM, quiereIA, avisos };
}

/* Las 20 respuestas caben en 20 caracteres: es lo que viaja en el enlace que
   el asesor abre en la llamada. Sin base de datos y sin backend — el enlace
   ES el dato, así que no puede caducar ni quedarse huérfano. */
const empaquetar   = R => R.map(v => (v===null?0:v)).join('');

/* El punto de partida va DETRÁS de las 20, nunca delante (ver ENTRADA). */
const empaquetarEntrada = E => E.map(v => (v===null?'':v)).join('');

/* Devuelve null si el enlace no lo trae: es un enlace anterior al 23-sep, o
   uno tocado a mano. En los dos casos se lee como antes y no se inventa nada.
   Solo se acepta si las dos respuestas existen y caben en sus opciones. */
function desempaquetarEntrada(s){
  const t = (s||'').slice(TODAS.length, TODAS.length + ENTRADA.length);
  if(t.length < ENTRADA.length) return null;
  const E = t.split('').map(c => /^[0-9]$/.test(c) ? +c : -1);
  const valido = E.every((v,i) => ENTRADA[i].opciones.some(o => o.v === v));
  return valido ? E : null;
}
const desempaquetar = s => (s||'').split('').slice(0, TODAS.length)
                             .map(c => Math.max(0, Math.min(3, +c || 0)));
