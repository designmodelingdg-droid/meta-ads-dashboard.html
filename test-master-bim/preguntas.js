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
