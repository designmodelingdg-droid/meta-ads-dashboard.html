/* Base para automatizar GoHighLevel con un navegador.
 *
 * POR QUE EXISTE
 * La API v2 de GHL es de solo lectura para lo que mas falta: no deja crear ni
 * editar workflows, no deja tocar paginas de Sites, y no dice que plantilla usa
 * cada workflow. Comprobado contra la documentacion oficial el 24-ago-2026:
 * Workflows expone solo GET /workflows/, y Funnels solo tres GET.
 *
 * Lo que la API no escribe, un navegador si. Esto es esa puerta.
 *
 * LOS TRES FRENOS, QUE VAN DENTRO Y NO EN UN COMENTARIO
 *
 * 1. Credenciales. Nunca en el repo ni en el chat. Se leen del entorno, que en
 *    la practica significa secretos de GitHub Actions. Y se prefiere la sesion
 *    exportada (GHL_STORAGE_STATE) sobre usuario y contrasena, porque una
 *    sesion caduca sola y una contrasena de GHL es la llave maestra de la
 *    cuenta entera.
 *
 * 2. Simulacro por defecto. Ninguna funcion que escriba hace nada sin que se
 *    le pase aplicar:true. El modo por defecto recorre, dice lo que HARIA y no
 *    toca nada.
 *
 * 3. Fallo ruidoso. Cada paso que no encuentra lo que espera guarda captura y
 *    HTML antes de rendirse. Un fallo silencioso en un CRM con 1.200
 *    oportunidades es peor que no automatizar nada — ya nos mordio dos veces
 *    este mes con cosas mas pequenas.
 */

const fs = require('fs');
const path = require('path');

const RAIZ = path.resolve(__dirname, '..', '..');
const PRUEBAS = path.join(RAIZ, 'matriz-viral/fuentes/navegador');

function playwright() {
  // El paquete vive global en el runner; require normal falla desde aqui.
  const { execSync } = require('child_process');
  const global_ = execSync('npm root -g', { encoding: 'utf8' }).trim();
  return require(path.join(global_, 'playwright'));
}

/** Arranca Chromium. Respeta el proxy del entorno si lo hay. */
async function abrir({ visible = false } = {}) {
  const { chromium } = playwright();
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const navegador = await chromium.launch({
    headless: !visible,
    proxy: proxy ? { server: proxy } : undefined,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  // Sesion exportada: el camino preferido. Se genera una vez a mano y se
  // guarda como secreto. Evita mandar la contrasena y sortea el 2FA, que en
  // headless normalmente no se puede resolver.
  const estado = process.env.GHL_STORAGE_STATE;
  const contexto = await navegador.newContext({
    storageState: estado ? JSON.parse(estado) : undefined,
    viewport: { width: 1440, height: 900 },
    locale: 'es-EC',
  });
  contexto.setDefaultTimeout(45000);
  return { navegador, contexto };
}

/** Guarda captura y HTML. Se llama SIEMPRE que algo no sale como se espera. */
async function evidencia(pagina, nombre) {
  fs.mkdirSync(PRUEBAS, { recursive: true });
  const base = path.join(PRUEBAS, nombre.replace(/[^\w.-]+/g, '_'));
  try { await pagina.screenshot({ path: base + '.png', fullPage: true }); } catch (_) {}
  try { fs.writeFileSync(base + '.html', await pagina.content()); } catch (_) {}
  console.log(`   evidencia guardada: ${path.relative(RAIZ, base)}.{png,html}`);
  return base;
}

/**
 * Deja la pagina dentro de GoHighLevel, o falla diciendo exactamente por que.
 * Devuelve la pagina lista para trabajar.
 */
async function entrar(contexto) {
  const pagina = await contexto.newPage();
  await pagina.goto('https://app.gohighlevel.com/', { waitUntil: 'domcontentloaded' });

  // Si la sesion exportada sigue viva, ya estamos dentro y no hay que teclear
  // nada. Se comprueba por la URL, no por un texto de la interfaz, que cambia.
  await pagina.waitForTimeout(3000);
  if (!/\/login/i.test(pagina.url())) {
    console.log('   sesion reutilizada, sin pedir credenciales');
    return pagina;
  }

  const usuario = process.env.GHL_USER;
  const clave = process.env.GHL_PASS;
  if (!usuario || !clave) {
    await evidencia(pagina, 'sin-credenciales');
    throw new Error(
      'La sesion caduco y no hay GHL_USER/GHL_PASS. Lo recomendable es ' +
      'regenerar GHL_STORAGE_STATE: es una sesion, caduca sola, y no expone ' +
      'la contrasena de la cuenta.');
  }

  console.log('   entrando con usuario y contrasena');
  await pagina.fill('input[type="email"], #email', usuario);
  await pagina.fill('input[type="password"], #password', clave);
  await pagina.click('button[type="submit"], button:has-text("Sign in")');
  await pagina.waitForTimeout(6000);

  // El 2FA no se puede resolver aqui: GHL manda un codigo al correo. Se
  // detecta y se dice claramente, en vez de quedarse colgado hasta el timeout.
  const cuerpo = (await pagina.content()).toLowerCase();
  if (/security code|codigo de seguridad|verification code|2-step|two.factor/.test(cuerpo)) {
    await evidencia(pagina, 'pide-2fa');
    throw new Error(
      'GHL pidio codigo de verificacion. Un navegador sin persona delante no ' +
      'lo puede resolver. Hay que generar GHL_STORAGE_STATE una vez a mano ' +
      '(ver scripts/navegador/README.md) y guardarlo como secreto.');
  }
  if (/\/login/i.test(pagina.url())) {
    await evidencia(pagina, 'login-rechazado');
    throw new Error('Las credenciales no entraron. Revisa la evidencia guardada.');
  }
  console.log('   dentro');
  return pagina;
}

/**
 * Envoltorio de toda escritura. Sin aplicar:true no toca nada, solo cuenta.
 * Y despues de escribir VERIFICA, porque en este proyecto ya aprendimos que un
 * paso marcado como ejecutado no prueba que la accion ocurriera: el bot de
 * ZAPATA marcaba los pasos en verde y el DM no salia.
 */
async function escribir({ que, aplicar, hacer, verificar, pagina }) {
  if (!aplicar) {
    console.log(`   [SIMULACRO] haria: ${que}`);
    return { aplicado: false, que };
  }
  console.log(`   [APLICANDO] ${que}`);
  await hacer();
  if (verificar) {
    const ok = await verificar();
    if (!ok) {
      await evidencia(pagina, 'verificacion-fallida-' + Date.now());
      throw new Error(`Se ejecuto «${que}» pero la verificacion dice que NO ` +
                      'quedo aplicado. Se corta aqui a proposito.');
    }
    console.log('   verificado');
  }
  return { aplicado: true, que };
}

/** Tope de seguridad: nunca tocar mas de N objetos en una corrida. */
function tope(lista, n, etiqueta) {
  if (lista.length <= n) return lista;
  console.log(`   ⚠ ${lista.length} ${etiqueta}: se limita a ${n} en esta corrida. ` +
              'Volver a lanzar para continuar.');
  return lista.slice(0, n);
}

module.exports = { abrir, entrar, evidencia, escribir, tope, PRUEBAS, RAIZ };
