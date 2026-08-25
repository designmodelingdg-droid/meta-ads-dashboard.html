#!/usr/bin/env node
/* Tareas de navegador sobre GoHighLevel.
 *
 * Uso (dentro del Action, que es donde viven los secretos):
 *
 *   node scripts/navegador/tareas.js sesion
 *       LECTURA. Comprueba que el secreto GHL_STORAGE_STATE sigue sirviendo y
 *       que alcanza la subcuenta correcta. Es lo primero que hay que correr
 *       despues de pegar el secreto, y lo primero que hay que correr cuando
 *       una tarea empieza a fallar sin motivo claro.
 *
 *   node scripts/navegador/tareas.js mapa-flujos
 *       LECTURA. Saca que plantilla de correo usa cada workflow. Es el limite
 *       conocido de la API: GET /workflows/ devuelve metadatos y nada de los
 *       pasos. Sin este mapa, editar los correos obliga a abrir flujo por
 *       flujo a mano.
 *
 *   node scripts/navegador/tareas.js paginas
 *       LECTURA. Inventario de Sites: que paginas existen y cuales estan
 *       publicadas. Sirve para ver si el Test y la Calculadora estan en la
 *       papelera o si hay que rehacerlas.
 *
 *   node scripts/navegador/tareas.js encender --flujo "NOMBRE" [--aplicar]
 *       ESCRITURA. Publica un workflow que esta en borrador.
 *
 *   node scripts/navegador/tareas.js restaurar-pagina --pagina "NOMBRE" [--aplicar]
 *       ESCRITURA. Restaura una pagina de Sites desde la papelera.
 *
 *   node scripts/navegador/tareas.js pegar-html --pagina "NOMBRE"
 *                --archivo recursos/ghl-recursos.html --url https://… [--aplicar]
 *       ESCRITURA. Reemplaza el contenido de un elemento Custom Code. Es lo que
 *       la API de GHL no deja hacer de ninguna forma: Funnels y Sites solo
 *       exponen tres GET. La verificacion NO mira la interfaz, pide la pagina
 *       publica por HTTP y comprueba que traiga los enlaces nuevos.
 *
 * SIN --aplicar no se toca nada: recorre, dice lo que haria y sale. Ese es el
 * modo por defecto a proposito.
 */

const fs = require('fs');
const path = require('path');
const { abrir, entrar, evidencia, escribir, tope, PRUEBAS, RAIZ } = require('./ghl');

const LOCATION = 'nkKbOarn5IwHeMv48uY9';
const BASE = `https://app.gohighlevel.com/v2/location/${LOCATION}`;

function args() {
  const a = process.argv.slice(2);
  const tarea = a[0];
  const op = {};
  for (let i = 1; i < a.length; i++) {
    if (a[i] === '--aplicar') op.aplicar = true;
    else if (a[i].startsWith('--')) op[a[i].slice(2)] = a[i + 1], i++;
  }
  return { tarea, op };
}

function guardar(nombre, datos) {
  fs.mkdirSync(PRUEBAS, { recursive: true });
  const f = path.join(PRUEBAS, nombre);
  fs.writeFileSync(f, JSON.stringify(datos, null, 1));
  console.log(`\n   escrito ${path.relative(RAIZ, f)}`);
}

/* ── LECTURA · comprobar que el secreto sirve ───────────────────── */
async function sesion(pagina) {
  console.log('\nComprobando la sesion…');
  const url = pagina.url();
  console.log(`   estamos en: ${url}`);

  // Se entra a dos secciones distintas porque una sesion puede seguir viva y
  // aun asi no tener permiso sobre la subcuenta que nos importa. Confirmar el
  // login no es confirmar el acceso.
  const puertas = [
    ['workflows', `${BASE}/automation/workflows`],
    ['sites', `${BASE}/funnels-websites/websites`],
  ];
  const visto = {};
  for (const [nombre, destino] of puertas) {
    await pagina.goto(destino, { waitUntil: 'domcontentloaded' });
    await pagina.waitForTimeout(6000);
    const actual = pagina.url();
    const echado = /\/login|\/oauth/i.test(actual);
    const cuenta = actual.includes(LOCATION);
    visto[nombre] = { alcanzado: !echado && cuenta };
    console.log(`   ${nombre}: ${visto[nombre].alcanzado ? 'OK' : 'NO'}` +
                (echado ? ' (nos mando al login)' : cuenta ? '' : ' (otra subcuenta)'));
    if (!visto[nombre].alcanzado) await evidencia(pagina, `sesion-${nombre}`);
  }

  const todo = Object.values(visto).every(v => v.alcanzado);
  // No se guarda nada de la pantalla: solo si sirve y cuando se comprobo. Con
  // eso basta para saber si hay que regenerar el secreto.
  guardar('sesion.json', {
    comprobado: new Date().toISOString().slice(0, 10),
    location: LOCATION, secciones: visto, sirve: todo,
  });
  if (!todo) {
    throw new Error('La sesion no llega a todo. Si dice «nos mando al login», ' +
                    'caduco: hay que regenerar GHL_STORAGE_STATE con ' +
                    'scripts/navegador/capturar-sesion.js.');
  }
  console.log('\n   La sesion sirve. No se toco nada.');
}

/* ── LECTURA · el mapa que la API no da ─────────────────────────── */
/* La lista de workflows NO se rasca de la pantalla: se lee de
 * fuentes/ghl/correos-contenido.json, que la escribe ghl_correos.py con
 * GET /workflows/ y trae los 148 con su id, nombre y estado.
 *
 * Por que asi. El 25-ago esta tarea rascaba la lista con un selector y
 * devolvio UNA entrada: «Global Workflow Settings», que es un elemento de
 * menu. No fallo —encontro algo— asi que salio en verde con un resultado
 * inservible. Rascar una lista que ya tenemos por API era fragil sin ganar
 * nada.
 *
 * Lo que la API no da son los PASOS del workflow: que plantilla de correo usa
 * cada uno. Para eso si hace falta abrir cada flujo, y ahora se abre por su
 * id —ruta directa y estable— en vez de por un enlace que haya que encontrar.
 */
const FUENTE_FLUJOS = path.join(RAIZ, 'matriz-viral/fuentes/ghl/correos-contenido.json');

async function mapaFlujos(pagina, op) {
  if (!fs.existsSync(FUENTE_FLUJOS)) {
    throw new Error('Falta ' + path.relative(RAIZ, FUENTE_FLUJOS) + '. Lo escribe ' +
                    'scripts/ghl_correos.py en la corrida de metricas semanales: ' +
                    'sin esa lista no se sabe a que workflows entrar.');
  }
  const fuente = JSON.parse(fs.readFileSync(FUENTE_FLUJOS, 'utf8'));
  const todos = (fuente.flujos || []).filter(f => f.id);
  if (!todos.length) throw new Error('La lista de flujos vino vacia o sin ids.');

  console.log(`\nLista de la API: ${todos.length} workflows (${fuente.generado})`);
  const limite = Number(op.limite || 25);
  const objetivo = tope(todos, limite, 'workflows');
  const mapa = [];
  let leidos = 0;

  for (const [i, f] of objetivo.entries()) {
    process.stdout.write(`   [${i + 1}/${objetivo.length}] ${(f.nombre || f.id).slice(0, 44)}… `);
    try {
      await pagina.goto(`${BASE}/automation/workflows/${f.id}`, { waitUntil: 'domcontentloaded' });
      // El lienzo del workflow tarda: se espera a que aparezca algo suyo en vez
      // de confiar en un timeout fijo, que fue justo lo que fallo antes.
      await pagina.waitForTimeout(3000);
      await pagina.waitForFunction(
        () => (document.body.innerText || '').length > 400, { timeout: 20000 }
      ).catch(() => {});

      const texto = await pagina.innerText('body').catch(() => '');
      // Un lienzo que no cargo devuelve el cascaron: se detecta y se marca.
      // Se anota la URL DONDE SE ACABO y cuanto texto habia: si GHL redirige
      // una ruta que no reconoce, la URL final lo delata y se arregla sin
      // adivinar. Y los primeros caracteres dicen si lo que llego fue un
      // error, un login o el cascaron de la aplicacion.
      if (texto.length < 400) {
        mapa.push({
          ...f, leido: false,
          error: 'la pagina no termino de cargar',
          url_final: pagina.url(),
          largo_texto: texto.length,
          asomo: texto.replace(/\s+/g, ' ').trim().slice(0, 160),
        });
        console.log(`SIN CARGAR (${texto.length} car · ${pagina.url().slice(-46)})`);
        continue;
      }
      const correos = [...new Set(
        (texto.match(/(Send Email|Enviar correo|Email)[\s\S]{0,120}/gi) || [])
          .map(s => s.replace(/\s+/g, ' ').trim().slice(0, 120))
      )].slice(0, 12);

      mapa.push({ ...f, pasos_correo: correos, leido: true });
      leidos++;
      console.log(`${correos.length} pasos de correo`);
    } catch (e) {
      mapa.push({ ...f, leido: false, error: String(e.message).slice(0, 120) });
      console.log('FALLO');
    }
  }

  // Si no se leyo ni la mitad, algo esta roto: se dice, no se entrega un
  // mapa a medias como si fuera el mapa.
  const salud = objetivo.length ? leidos / objetivo.length : 0;
  console.log(`\n   leidos de verdad: ${leidos}/${objetivo.length}`);

  guardar('mapa-flujos.json', {
    generado: new Date().toISOString().slice(0, 10),
    fuente_lista: path.relative(RAIZ, FUENTE_FLUJOS),
    total_en_la_cuenta: todos.length,
    intentados: objetivo.length,
    leidos,
    flujos: mapa,
  });

  if (salud < 0.5) {
    await evidencia(pagina, 'mapa-flujos-mayoria-fallida');
    throw new Error(`Solo se leyeron ${leidos} de ${objetivo.length}. El mapa se ` +
                    'guardo igual, pero no sirve como mapa: mira la evidencia.');
  }
}

/* ── LECTURA · inventario de Sites ──────────────────────────────── */
async function paginas(pagina) {
  console.log('\nLeyendo las paginas de Sites…');
  await pagina.goto(`${BASE}/funnels-websites/websites`, { waitUntil: 'domcontentloaded' });
  await pagina.waitForTimeout(6000);
  const texto = await pagina.innerText('body').catch(() => '');
  const enlaces = await pagina.$$eval('a', els => els
    .map(e => ({ t: (e.innerText || '').trim().slice(0, 70), h: e.getAttribute('href') || '' }))
    .filter(x => x.t && /funnel|website|page/i.test(x.h)));
  if (!enlaces.length) await evidencia(pagina, 'sites-sin-reconocer');
  console.log(`   ${enlaces.length} entradas reconocidas`);
  for (const e of enlaces.slice(0, 40)) console.log(`     ${e.t}`);
  guardar('paginas-sites.json', {
    generado: new Date().toISOString().slice(0, 10),
    entradas: enlaces,
    // El texto crudo se guarda porque si el selector falla, al menos queda de
    // donde sacarlo a mano en vez de tener que repetir la corrida.
    texto_crudo: texto.slice(0, 20000),
  });
}

/* ── ESCRITURA · encender un workflow ───────────────────────────── */
async function encender(pagina, op) {
  if (!op.flujo) throw new Error('Falta --flujo "NOMBRE DEL WORKFLOW"');
  console.log(`\nBuscando el workflow «${op.flujo}»…`);
  await pagina.goto(`${BASE}/automation/workflows`, { waitUntil: 'domcontentloaded' });
  await pagina.waitForTimeout(6000);

  const enlace = pagina.locator(`a:has-text("${op.flujo}")`).first();
  if (!await enlace.count()) {
    await evidencia(pagina, 'flujo-no-encontrado');
    throw new Error(`No aparece ningun workflow con ese nombre. No se toca nada.`);
  }
  await enlace.click();
  await pagina.waitForTimeout(5000);

  await escribir({
    que: `publicar el workflow «${op.flujo}»`,
    aplicar: !!op.aplicar,
    pagina,
    hacer: async () => {
      const sw = pagina.locator('[role="switch"], .publish-toggle, button:has-text("Publish")').first();
      if (!await sw.count()) {
        await evidencia(pagina, 'sin-interruptor');
        throw new Error('No se encontro el interruptor de publicar.');
      }
      await sw.click();
      await pagina.waitForTimeout(4000);
    },
    // Se vuelve a LEER la pagina para confirmar. Un clic dado no es un cambio
    // guardado: esa leccion ya la pagamos con el bot de ZAPATA en julio.
    verificar: async () => {
      await pagina.reload({ waitUntil: 'domcontentloaded' });
      await pagina.waitForTimeout(5000);
      const t = (await pagina.innerText('body')).toLowerCase();
      return /published|publicado/.test(t) && !/draft|borrador/.test(t.slice(0, 400));
    },
  });
}

/* ── ESCRITURA · restaurar una pagina de la papelera ─────────────── */
async function restaurarPagina(pagina, op) {
  if (!op.pagina) throw new Error('Falta --pagina "NOMBRE"');
  console.log(`\nBuscando «${op.pagina}» en la papelera de Sites…`);
  await pagina.goto(`${BASE}/funnels-websites/websites`, { waitUntil: 'domcontentloaded' });
  await pagina.waitForTimeout(6000);

  const papelera = pagina.locator('button:has-text("Trash"), button:has-text("Papelera"), [href*="trash"]').first();
  if (await papelera.count()) { await papelera.click(); await pagina.waitForTimeout(4000); }
  else console.log('   (no se vio pestana de papelera; se busca en la lista normal)');

  const fila = pagina.locator(`text=${op.pagina}`).first();
  if (!await fila.count()) {
    await evidencia(pagina, 'pagina-no-esta-en-papelera');
    throw new Error('No aparece en la papelera. Si no esta ahi, no se borro: ' +
                    'se despublico o se renombro, y eso se mira a mano.');
  }
  await escribir({
    que: `restaurar la pagina «${op.pagina}»`,
    aplicar: !!op.aplicar,
    pagina,
    hacer: async () => {
      await fila.click({ button: 'right' }).catch(() => {});
      const b = pagina.locator('button:has-text("Restore"), button:has-text("Restaurar")').first();
      if (!await b.count()) {
        await evidencia(pagina, 'sin-boton-restaurar');
        throw new Error('No se encontro el boton de restaurar.');
      }
      await b.click();
      await pagina.waitForTimeout(5000);
    },
    verificar: async () => {
      await pagina.goto(`${BASE}/funnels-websites/websites`, { waitUntil: 'domcontentloaded' });
      await pagina.waitForTimeout(5000);
      return (await pagina.innerText('body')).includes(op.pagina);
    },
  });
}

/* ── ESCRITURA · pegar HTML en un elemento Custom Code ───────────── */

/* El constructor de GHL no es una pagina normal: mete el lienzo y el editor de
 * codigo en marcos anidados, y a veces cambia de libreria de editor entre
 * versiones. Por eso NO se busca por un selector fijo — se busca por rasgo, en
 * todos los marcos. Un selector escrito a ojo funciona el dia que se escribe y
 * se rompe en la siguiente actualizacion sin decir por que.
 */
const EDITORES = [
  { tipo: 'CodeMirror 6', sel: '.cm-content[contenteditable="true"]', teclado: true },
  { tipo: 'CodeMirror 5', sel: '.CodeMirror textarea',                teclado: true },
  { tipo: 'Monaco',       sel: '.monaco-editor textarea',             teclado: true },
  { tipo: 'textarea',     sel: 'textarea',                            teclado: false },
];

async function buscarEditor(pagina) {
  for (const marco of pagina.frames()) {
    for (const e of EDITORES) {
      const loc = marco.locator(e.sel).first();
      const hay = await loc.count().catch(() => 0);
      if (hay && await loc.isVisible().catch(() => false)) {
        return { marco, loc, tipo: e.tipo, teclado: e.teclado };
      }
    }
  }
  return null;
}

/* La unica verificacion que vale: pedir la pagina PUBLICA por HTTP y mirar que
 * dice. Que el editor acepte el texto y el boton se ponga verde no prueba nada
 * — el hub de /recursos estuvo semanas sirviendo dos enlaces muertos mientras
 * en el repositorio ya estaban corregidos. Se reintenta porque publicar en GHL
 * tarda unos segundos en propagarse.
 */
async function verificarPublicado(url, debeTener, noDebeTener) {
  for (let intento = 1; intento <= 6; intento++) {
    await new Promise(r => setTimeout(r, intento === 1 ? 4000 : 10000));
    let html = '';
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 (matriz-bot)' } });
      if (!r.ok) { console.log(`   [${intento}/6] la pagina respondio ${r.status}`); continue; }
      html = await r.text();
    } catch (e) {
      console.log(`   [${intento}/6] no se pudo leer: ${String(e.message).slice(0, 60)}`);
      continue;
    }
    const faltan = debeTener.filter(s => !html.includes(s));
    const sobran = (noDebeTener || []).filter(s => html.includes(s));
    if (!faltan.length && !sobran.length) {
      console.log(`   [${intento}/6] la pagina publica ya trae los cambios`);
      return true;
    }
    console.log(`   [${intento}/6] todavia no: faltan ${faltan.length}, sobran ${sobran.length}`);
  }
  return false;
}

async function pegarHtml(pagina, op) {
  if (!op.pagina)  throw new Error('Falta --pagina "NOMBRE DE LA PAGINA EN SITES"');
  if (!op.archivo) throw new Error('Falta --archivo ruta/al/archivo.html');
  if (!op.url)     throw new Error('Falta --url https://… (la direccion PUBLICA, para verificar). ' +
                                   'Sin ella no hay forma de saber si el cambio llego a la gente.');

  const ruta = path.resolve(RAIZ, op.archivo);
  if (!fs.existsSync(ruta)) throw new Error(`No existe el archivo: ${op.archivo}`);
  const html = fs.readFileSync(ruta, 'utf8');
  console.log(`\nArchivo: ${op.archivo} · ${Math.round(html.length / 1024)} KB`);

  // Lo que tiene que aparecer y desaparecer en la pagina publica. Se saca del
  // propio archivo en vez de escribirlo a mano: asi la comprobacion sigue
  // sirviendo cuando el contenido cambie.
  const enlaces = [...new Set((html.match(/https:\/\/funnel\.dgdesignmodeling\.com\/[a-z0-9/-]+/g) || []))];
  const debeTener = enlaces.filter(u => /acceso-gratis|descarga-gratis/.test(u)).slice(0, 4);
  if (!debeTener.length) throw new Error('No reconoci ningun enlace de embudo en el archivo. ' +
                                         'Sin algo concreto que buscar, la verificacion seria de mentira.');
  console.log('   se verificara que la pagina publica traiga:');
  for (const u of debeTener) console.log('     ' + u);

  console.log(`\nBuscando «${op.pagina}» en Sites…`);
  await pagina.goto(`${BASE}/funnels-websites/websites`, { waitUntil: 'domcontentloaded' });
  await pagina.waitForTimeout(6000);

  const fila = pagina.locator(`a:has-text("${op.pagina}"), tr:has-text("${op.pagina}")`).first();
  if (!await fila.count()) {
    await evidencia(pagina, 'pagina-no-encontrada');
    throw new Error(`No aparece ninguna pagina con ese nombre. No se toca nada. ` +
                    `Corre la tarea «paginas» para ver como se llama exactamente.`);
  }
  await fila.click();
  await pagina.waitForTimeout(6000);

  const editar = pagina.locator('button:has-text("Edit"), button:has-text("Editar"), a:has-text("Edit")').first();
  if (await editar.count()) { await editar.click(); await pagina.waitForTimeout(9000); }

  const ed = await buscarEditor(pagina);
  if (!ed) {
    await evidencia(pagina, 'sin-editor-de-codigo');
    throw new Error(
      'Llegue a la pagina pero no encontre el editor de codigo en ninguno de los ' +
      `${pagina.frames().length} marcos. Hay que abrir el elemento Custom Code a mano ` +
      'una vez y mirar la evidencia guardada para ajustar la busqueda.');
  }
  console.log(`   editor encontrado: ${ed.tipo}`);

  await escribir({
    que: `reemplazar el contenido de «${op.pagina}» con ${op.archivo}`,
    aplicar: !!op.aplicar,
    pagina,
    hacer: async () => {
      await ed.loc.click();
      await pagina.keyboard.press('ControlOrMeta+a');
      await pagina.keyboard.press('Delete');
      if (ed.teclado) {
        // insertText y no type(): 23 KB tecleados caracter a caracter tardan
        // minutos y cada autocompletado del editor los corrompe por el camino.
        await pagina.keyboard.insertText(html);
      } else {
        await ed.loc.fill(html);
      }
      await pagina.waitForTimeout(2500);

      const guardar_ = pagina.locator('button:has-text("Save"), button:has-text("Guardar")').first();
      if (!await guardar_.count()) {
        await evidencia(pagina, 'sin-boton-guardar');
        throw new Error('Escribi el contenido pero no encontre el boton de guardar. ' +
                        'Se corta aqui: dejarlo sin guardar es mejor que suponer.');
      }
      await guardar_.click();
      await pagina.waitForTimeout(8000);

      const publicar = pagina.locator('button:has-text("Publish"), button:has-text("Publicar")').first();
      if (await publicar.count()) { await publicar.click(); await pagina.waitForTimeout(6000); }
    },
    verificar: async () => {
      console.log(`\n   comprobando ${op.url} …`);
      return verificarPublicado(op.url, debeTener,
        ['funnel.dgdesignmodeling.com/test-nivel-bim"',
         'funnel.dgdesignmodeling.com/calculadora-zapatas"']);
    },
  });

  guardar('pegado.json', {
    fecha: new Date().toISOString().slice(0, 10),
    pagina: op.pagina, archivo: op.archivo, url: op.url,
    editor: ed.tipo, aplicado: !!op.aplicar, verificados: debeTener,
  });
}

const TAREAS = {
  'sesion': sesion,
  'mapa-flujos': mapaFlujos,
  'paginas': paginas,
  'encender': encender,
  'restaurar-pagina': restaurarPagina,
  'pegar-html': pegarHtml,
};

/* Se exporta para poder probar las piezas sueltas sin abrir un navegador ni
 * tocar el CRM. La comprobacion de la pagina publica, sobre todo: es la unica
 * que decide si un cambio de verdad llego a la gente, asi que tiene que poder
 * ejercitarse contra una URL real.
 */
module.exports = { verificarPublicado, buscarEditor, pegarHtml };

if (require.main !== module) return;

(async () => {
  const { tarea, op } = args();
  if (!TAREAS[tarea]) {
    console.error('Tareas: ' + Object.keys(TAREAS).join(' · '));
    process.exit(2);
  }
  if (!op.aplicar) console.log('MODO SIMULACRO — no se escribe nada. Anade --aplicar para actuar.\n');

  const { navegador, contexto } = await abrir();
  try {
    const pagina = await entrar(contexto);
    await TAREAS[tarea](pagina, op);
    console.log('\nListo.');
  } catch (e) {
    console.error('\nFALLO: ' + e.message);
    process.exitCode = 1;
  } finally {
    await navegador.close();
  }
})();
