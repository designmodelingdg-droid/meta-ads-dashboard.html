#!/usr/bin/env node
/* Captura la sesion de GoHighLevel para guardarla como secreto del repositorio.
 *
 * Esto se corre UNA VEZ, en la computadora de Dayana, no en el servidor. Abre
 * un Chromium limpio, espera a que ella entre a GHL normal (con su clave y su
 * 2FA), y guarda la sesion ya iniciada en un archivo.
 *
 * POR QUE UNA SESION Y NO LA CONTRASENA
 *   1. Caduca sola. Una sesion muere en semanas; la contrasena de GHL no, y es
 *      la llave maestra: quien la tenga puede borrar la cuenta entera.
 *   2. Sortea el 2FA. GHL manda un codigo al correo, y un navegador sin nadie
 *      delante no lo puede resolver.
 *   3. Se revoca cerrando sesion, sin cambiar nada mas.
 *
 * Uso:
 *   node scripts/navegador/capturar-sesion.js
 *
 * Deja un sesion.json en la carpeta actual. Ese archivo NO va al repositorio:
 * se pega en Settings -> Secrets and variables -> Actions como GHL_STORAGE_STATE
 * y despues se borra del disco.
 */

const fs = require('fs');
const path = require('path');

const SALIDA = path.resolve(process.cwd(), 'sesion.json');
const ESPERA_MAX_MIN = 15;
const SECRETO = 'GHL_STORAGE_STATE';

// Los dominios que de verdad importan para entrar. Sirve para avisar si la
// captura salio vacia en vez de guardar un archivo inutil que falla despues,
// en mitad de una corrida, sin que nadie entienda por que.
const DOMINIOS = /gohighlevel|leadconnector|msgsndr/i;

function playwright() {
  try {
    return require('playwright');
  } catch (_) {
    try {
      const { execSync } = require('child_process');
      const g = execSync('npm root -g', { encoding: 'utf8' }).trim();
      return require(path.join(g, 'playwright'));
    } catch (e) {
      console.error(
        '\nNo encuentro Playwright. Instalalo con:\n' +
        '   npm install -g playwright\n' +
        '   npx playwright install chromium\n');
      process.exit(2);
    }
  }
}

function resumen(estado) {
  const cookies = estado.cookies || [];
  const origenes = estado.origins || [];
  const dominios = [...new Set(cookies.map(c => c.domain))].sort();
  const utiles = cookies.filter(c => DOMINIOS.test(c.domain)).length +
                 origenes.filter(o => DOMINIOS.test(o.origin)).length;
  return { cookies: cookies.length, origenes: origenes.length, dominios, utiles };
}

(async () => {
  const { chromium } = playwright();

  console.log('\n─── Capturar la sesion de GoHighLevel ───\n');
  console.log('Se va a abrir un Chromium limpio (no usa tu Chrome ni tus perfiles).');
  console.log('Entra a GHL como siempre: correo, clave y el codigo de verificacion');
  console.log('si te lo pide. Cuando estes DENTRO y veas la subcuenta, este');
  console.log('programa lo detecta solo y guarda la sesion.\n');

  let navegador;
  try {
    navegador = await chromium.launch({ headless: false, args: ['--start-maximized'] });
  } catch (e) {
    console.error('\nNo pude abrir Chromium: ' + String(e.message).split('\n')[0]);
    console.error('Casi siempre es una de dos:');
    console.error('  · falta bajarlo  ->  npx playwright install chromium');
    console.error('  · lo estas corriendo en un servidor sin pantalla. Esto va en');
    console.error('    tu computadora: necesita una ventana para que escribas la clave.\n');
    process.exit(2);
  }
  const contexto = await navegador.newContext({ viewport: null, locale: 'es-EC' });
  const pagina = await contexto.newPage();
  await pagina.goto('https://app.gohighlevel.com/', { waitUntil: 'domcontentloaded' });

  console.log(`Esperando (hasta ${ESPERA_MAX_MIN} min)… entra con calma.\n`);

  const limite = Date.now() + ESPERA_MAX_MIN * 60_000;
  let dentro = false;
  let ultimo = '';

  while (Date.now() < limite) {
    if (pagina.isClosed()) break;
    let url = '';
    try { url = pagina.url(); } catch (_) { break; }

    if (url !== ultimo) {
      ultimo = url;
      console.log('   …' + url.slice(0, 88));
    }

    // Se comprueba por la URL, no por un texto de la interfaz: GHL cambia los
    // textos y las traducciones, pero /v2/location/<id> es estable y es la
    // senal de que ya estamos dentro de una subcuenta.
    if (/\/v2\/location\/|\/v2\/agency\//.test(url)) { dentro = true; break; }
    await pagina.waitForTimeout(2000);
  }

  if (!dentro) {
    console.error('\nNo llegue a ver una subcuenta abierta. No guardo nada:');
    console.error('un archivo a medias falla despues, en mitad de una corrida,');
    console.error('y ahi cuesta mucho mas entender que paso.');
    console.error('Vuelve a lanzarlo y entra hasta ver el panel de la subcuenta.\n');
    await navegador.close();
    process.exit(1);
  }

  console.log('\n   dentro. Guardando la sesion…');
  const estado = await contexto.storageState();
  await navegador.close();

  const r = resumen(estado);
  if (!r.utiles) {
    console.error('\nLa sesion salio vacia de lo que hace falta: no hay cookies');
    console.error('ni almacenamiento de GoHighLevel. No la guardo.\n');
    process.exit(1);
  }

  fs.writeFileSync(SALIDA, JSON.stringify(estado));
  const kb = Math.round(fs.statSync(SALIDA).size / 1024);

  console.log(`\n   ${r.cookies} cookies · ${r.origenes} origenes · ${kb} KB`);
  console.log('   dominios: ' + r.dominios.slice(0, 8).join(', ') +
              (r.dominios.length > 8 ? ` (+${r.dominios.length - 8})` : ''));

  console.log(`
─────────────────────────────────────────────────────────────
Listo:  ${SALIDA}

ESTE ARCHIVO ES UNA SESION ABIERTA DE TU CRM. Quien lo tenga entra
sin clave y sin 2FA. No lo mandes por WhatsApp ni por correo, y no lo
dejes en la carpeta del repositorio mas de lo necesario.

Que hacer con el, en orden:

  1. Abre el archivo y copia TODO el contenido (Cmd/Ctrl + A, Cmd/Ctrl + C).

  2. Ve a:
     github.com/designmodelingdg-droid/meta-ads-dashboard.html
     -> Settings -> Secrets and variables -> Actions
     -> New repository secret

     Name:   ${SECRETO}
     Secret: (pega todo el contenido)

  3. Borra el archivo del disco:
     rm "${SALIDA}"

  4. Comprueba que quedo bien, sin tocar nada:
     Actions -> Navegador GHL -> Run workflow
       tarea = sesion · aplicar = false

Cuando caduque, la corrida lo dira con todas las letras y se repite
este mismo proceso. Para revocarla antes: cierra sesion en GHL.
─────────────────────────────────────────────────────────────
`);
})();
