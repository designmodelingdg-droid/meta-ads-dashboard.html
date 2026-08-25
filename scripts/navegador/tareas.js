#!/usr/bin/env node
/* Tareas de navegador sobre GoHighLevel.
 *
 * Uso (dentro del Action, que es donde viven los secretos):
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

/* ── LECTURA · el mapa que la API no da ─────────────────────────── */
async function mapaFlujos(pagina, op) {
  console.log('\nLeyendo los workflows y sus pasos de correo…');
  await pagina.goto(`${BASE}/automation/workflows`, { waitUntil: 'domcontentloaded' });
  await pagina.waitForTimeout(6000);

  const filas = await pagina.$$eval(
    '[class*="workflow"] a, table a[href*="/workflow"], a[href*="/automation/workflows/"]',
    els => [...new Set(els.map(e => JSON.stringify({
      nombre: (e.innerText || '').trim().slice(0, 90),
      href: e.getAttribute('href') || '',
    })))].map(JSON.parse).filter(x => x.nombre && x.href.includes('workflow')));

  if (!filas.length) {
    await evidencia(pagina, 'lista-flujos-vacia');
    throw new Error('No se reconocio la lista de workflows. La interfaz de GHL ' +
                    'cambio: hay que ajustar el selector. Mira la evidencia.');
  }
  console.log(`   ${filas.length} workflows en la lista`);

  const limite = Number(op.limite || 25);
  const objetivo = tope(filas, limite, 'workflows');
  const mapa = [];

  for (const [i, f] of objetivo.entries()) {
    process.stdout.write(`   [${i + 1}/${objetivo.length}] ${f.nombre.slice(0, 46)}… `);
    try {
      await pagina.goto(new URL(f.href, 'https://app.gohighlevel.com').href,
                        { waitUntil: 'domcontentloaded' });
      await pagina.waitForTimeout(4500);
      // Los pasos de "Enviar correo" llevan el nombre de la plantilla dentro.
      const correos = await pagina.$$eval('body', b => {
        const t = b.innerText || '';
        const out = [];
        const re = /(Send Email|Enviar correo|Email)[\s\S]{0,120}/gi;
        let m; while ((m = re.exec(t))) out.push(m[0].replace(/\s+/g, ' ').trim().slice(0, 120));
        return [...new Set(out)].slice(0, 12);
      });
      mapa.push({ ...f, pasos_correo: correos, leido: true });
      console.log(`${correos.length} pasos de correo`);
    } catch (e) {
      mapa.push({ ...f, leido: false, error: String(e.message).slice(0, 120) });
      console.log('FALLO');
    }
  }
  guardar('mapa-flujos.json', {
    generado: new Date().toISOString().slice(0, 10),
    total_en_lista: filas.length, leidos: mapa.length, flujos: mapa,
  });
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

const TAREAS = {
  'mapa-flujos': mapaFlujos,
  'paginas': paginas,
  'encender': encender,
  'restaurar-pagina': restaurarPagina,
};

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
