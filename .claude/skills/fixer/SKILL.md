---
name: fixer
description: Método y comandos de verificación para arreglar bugs en ESTE repo (meta-ads-dashboard.html de Design Modeling Academy). ACTIVA siempre que el usuario reporte que algo está roto, falla o dejó de funcionar - "hay un bug", "arregla", "no funciona", "está fallando", "la calculadora se rompió", "el candado no abre", "la landing no redirige", "la matriz no se actualizó", "la Action falló", "el sitio publicado no refleja el cambio", "debug", "revisa por qué…" - o cuando otro modelo/sesión afirme que algo "ya quedó arreglado" y haya que comprobarlo. También al verificar la salud del repo antes de un merge o publicación.
---

# FIXER — Cómo se arreglan bugs en este proyecto

Este repo NO tiene framework de tests, ni package.json, ni build. Es HTML
autocontenido + un script Python + GitHub Actions. Verificar aquí significa
**correr los comandos concretos de abajo y mirar su output**, no `npm test`.

## Mapa del proyecto

| Pieza | Qué es | Cómo se verifica |
|---|---|---|
| `calculadora-zapatas/app.html` | Calculadora (lead magnet), JS puro con candado por token | Test del núcleo en Node + smoke Playwright (abajo) |
| `calculadora-zapatas/index.html` | Landing de captura | htmlhint + smoke Playwright |
| `calculadora-zapatas/gracias-agenda.html` | Página de gracias + agenda | htmlhint + abrir en Playwright |
| `calculadora-zapatas/ghl-landing.html` | **Generado** desde index.html para pegar en GHL. NO editar a mano | Se regenera; htmlhint da falso positivo (ver Trampas) |
| `matriz-viral/matriz/matriz.json` | Datos de contenido (fuente de verdad, se publica a Pages) | JSON válido + invariantes (abajo) |
| `scripts/refresh_matriz.py` | Refresco semanal vía Apify (Action) | `py_compile` + corrida con token |
| `.github/workflows/*.yml` | refresh semanal + publicación a gh-pages | Logs en la pestaña Actions |

- Rama por defecto: `claude/remote-control-setup-GUe3f` (no hay main/master).
- `matriz-viral/fuentes/` es dato crudo: **solo lectura, jamás se edita**.
- Métricas: lo que no venga del scraper se marca `s/d` o `null`. Nunca inventar.

## El método (obligatorio, en este orden)

1. **Reproducir primero.** Haz que el bug pase frente a ti con los comandos de
   abajo ANTES de tocar código. Si no puedes reproducirlo, todavía no
   entiendes el bug — sigue investigando, no "arregles" a ciegas.
   Ejemplo real: un chequeo de duplicados en matriz.json "encontró" un bug…
   que era un placeholder documentado (`shortCode: null` con nota "pendiente
   de reconciliar"). Reproducir + leer el dato evitó un arreglo falso.
2. **Causa raíz, no síntoma.** Pregunta "¿por qué?" hacia atrás hasta llegar
   al código que DECIDE, no al que muestra el error. Si el chip dice
   VERIFICAR ✖, el bug puede estar en `calcularZapata()` (decide), no en el
   render (muestra). Si Pages sirve contenido viejo, la causa puede ser la
   lista de ramas de `publish-matriz.yml` o la caché del CDN, no el HTML.
3. **Arreglo mínimo.** Solo las líneas que corrigen la causa raíz. Cero
   refactors de "ya que estamos aquí". Un diff que un humano lee en 1 minuto.
4. **Probar con evidencia.** Vuelve a correr EXACTAMENTE el caso que fallaba
   con los comandos reales de abajo y pega el output en tu reporte.
   La frase "debería funcionar" está prohibida en este repo.
5. **Regla anti-"ya quedó".** Si otro modelo, una sesión anterior, un commit
   o un comentario de PR dice que algo "ya está arreglado": exige el output
   que lo demuestra. Sin evidencia ejecutada, se trata como NO arreglado y
   se re-verifica desde cero con los comandos de abajo.
6. **Reporte fiel.** Si la prueba falla, se dice "falló" y se pega el output
   completo del fallo. Nunca se maquilla, se recorta ni se omite un error.

## Comandos de verificación reales

### Salud global del repo (correr siempre al empezar y antes de cerrar)

```bash
cd /home/user/meta-ads-dashboard.html   # o la raíz del clon
python3 -m json.tool matriz-viral/matriz/matriz.json > /dev/null \
  && python3 - <<'EOF'
import json
m = json.load(open('matriz-viral/matriz/matriz.json'))
assert m['total_reels'] == len(m['reels']), 'total_reels desincronizado'
sc = [r['shortCode'] for r in m['reels'] if r.get('shortCode')]
assert len(sc) == len(set(sc)), 'shortCodes duplicados'
pend = sum(1 for r in m['reels'] if not r.get('shortCode'))
print(f"matriz OK: {m['total_reels']} reels ({pend} con shortCode pendiente de reconciliar)")
EOF
python3 -m py_compile scripts/refresh_matriz.py && echo "refresh_matriz.py compila"
htmlhint calculadora-zapatas/app.html calculadora-zapatas/index.html \
         calculadora-zapatas/gracias-agenda.html
```

Si todo eso pasa, el repo está sano. Output esperado hoy: `matriz OK: 127
reels (2 con shortCode pendiente…)` + `compila` + `Scanned 3 files, found 0 errors`.

### Núcleo de cálculo de la calculadora (cuando el bug es de números)

El cálculo vive como función pura entre `/* CALC-START */` y `/* CALC-END */`
en `app.html`. Se extrae y se prueba en Node contra el caso de la hoja Z-1
del Excel fuente (los `value="…"` por defecto del propio formulario SON ese
caso de referencia):

```bash
sed -n '/CALC-START/,/CALC-END/p' calculadora-zapatas/app.html > /tmp/calc.js
node - <<'EOF'
const src = require('fs').readFileSync('/tmp/calc.js','utf8');
const calcularZapata = new Function(src + '; return calcularZapata;')();
const B58 = {n:'5/8"', db:1.59, ab:2.00};
const r = calcularZapata({ PD:63.70, PV:0.13, sigmaT:1.00, hf:1.45, SC:0,
  gS:1.8, gC:2.4, fc:210, fy:4200, a:0.45, b:0.45, pos:'interior',
  T:3.25, S:3.25, h:0.50, rec:7.5, barX:B58, barY:B58 });
console.log({sigmaN:+r.sigmaN.toFixed(3), Az:+r.Az.toFixed(3), Pu:+r.Pu.toFixed(2),
  okArea:r.okArea, okCorte:r.okCorte, okPunz:r.okPunz, okFlex:r.okFlex, okTodo:r.okTodo});
if (!r.okTodo) { console.error('FALLO caso de referencia'); process.exit(1); }
console.log('CALC OK');
EOF
```

Valores esperados del caso de referencia (verificados): `sigmaN 6.955`,
`Az 9.178`, `Pu 89.40`, `Wnu 8.464`, `As 24.86 cm²` por dirección,
13 varillas 5/8" @ 25 cm, todos los `ok* = true`. Si cambias una fórmula,
compara **cada magnitud** contra el Excel fuente (tolerancia relativa 1e-6).

### Smoke test en navegador real (cuando el bug es de UI/candado/flujo)

Playwright está instalado global en `/opt/node22/lib/node_modules` y el
Chromium en `/opt/pw-browsers` (variable `PLAYWRIGHT_BROWSERS_PATH` ya
apunta ahí — NO correr `playwright install`). ⚠️ Usar **CommonJS** (`.cjs` +
`require`): los `import` ESM ignoran `NODE_PATH` y no encuentran playwright.

```bash
cat > /tmp/smoke.cjs <<'EOF'
const { chromium } = require('playwright');
const APP = 'file:///home/user/meta-ads-dashboard.html/calculadora-zapatas/app.html';
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errs = []; page.on('pageerror', e => errs.push(e.message));
  await page.route('**fonts.g**', r => r.abort());   // sin red a Google Fonts en sandbox
  await page.goto(APP);                               // 1) sin token → candado
  console.log('candado sin token:', await page.locator('#lock').isVisible());
  await page.goto(APP + '?acceso=dm2026');            // 2) token → desbloquea (dm2026 = TOKEN_ACCESO en app.html)
  await page.waitForTimeout(500);
  const lock2 = await page.locator('#lock').isVisible();
  const chip = await page.locator('text=CUMPLE').first().isVisible();
  console.log('con token — candado:', lock2, '| chip CUMPLE:', chip);
  console.log('errores JS:', errs.length ? errs : 'ninguno');
  await browser.close();
  if (lock2 || !chip || errs.length) process.exit(1);
  console.log('SMOKE OK');
})();
EOF
NODE_PATH=/opt/node22/lib/node_modules node /tmp/smoke.cjs
```

Output sano: `candado sin token: true`, `con token — candado: false | chip
CUMPLE: true`, `errores JS: ninguno`, `SMOKE OK`. Los errores de consola del
navegador se capturan ahí mismo (`pageerror` / `page.on('console')`) — esta
app no tiene otro sistema de logs.

### Script de refresco de la matriz (cuando la Action falla o los datos no llegan)

```bash
python3 -m py_compile scripts/refresh_matriz.py          # sintaxis
USERNAME_IG=cuenta LIMIT=5 APIFY_TOKEN=xxx python3 scripts/refresh_matriz.py
```

- La variable de cuenta es **`USERNAME_IG`** (no `USERNAME` — esa la define
  el sistema operativo con el usuario de login y por eso el script no la usa).
- Sin `APIFY_TOKEN` → `ERROR: falta APIFY_TOKEN` y exit 1. Con token pero
  Apify caído o sin crédito → mensaje y **exit 0 sin tocar la matriz** (es
  defensivo a propósito: la Action semanal no debe romperse cuando el plan
  free se queda sin crédito). No "arregles" ese exit 0: es diseño.
- El token real vive en el secreto del repo `APIFY_TOKEN` (Settings →
  Secrets → Actions); localmente no lo tienes — pide el token o valida solo
  la lógica con `py_compile` + lectura.

## Dónde se ven los logs y los errores

- **GitHub Actions** (pestaña Actions del repo
  `designmodelingdg-droid/meta-ads-dashboard.html`): workflow "Refrescar
  matriz.json (Apify)" (lunes 13:00 UTC + manual) y "Publicar matriz.json
  (GitHub Pages)". El stdout de `refresh_matriz.py` sale en el paso
  "Refrescar matriz.json". Desde Claude: herramientas MCP
  `mcp__github__actions_list` / `mcp__github__get_job_logs`.
- **Navegador**: no hay logging propio; se capturan errores con Playwright
  (`page.on('pageerror')`, `page.on('console')`) como en el smoke de arriba.
- **Sitio publicado**: `curl -sI https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/matriz.json`
  (y `/calculadora-zapatas/`). Para saltarte la caché del CDN: `?v=N` o
  `https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/gh-pages/...`.

## Trampas conocidas (revisar antes de culpar al código)

1. `ghl-landing.html` **se genera** desde `index.html` (script que extrae
   `<style>` + body y absolutiza URLs). No se edita a mano, y `htmlhint` le
   marca `doctype-first` — **falso positivo por diseño**: es un fragmento
   para pegar en GHL Custom Code. Por eso el comando de salud lintéa solo
   los otros 3 HTML.
2. `publish-matriz.yml` solo publica en push a las ramas **listadas en su
   `on.push.branches`**. Si tu arreglo "no se ve" en Pages, primero mira si
   tu rama está en esa lista o si falta el merge a la rama por defecto.
3. En `matriz.json` hay entradas con `shortCode: null` y nota "pendiente de
   reconciliar con Apify": son placeholders honestos (regla: no inventar
   datos), **no** duplicados a deduplicar. Ojo: `refresh_matriz.py` indexa
   por shortCode, así que cuando Apify traiga esos posts los agregará como
   filas nuevas — la reconciliación es fusionar a mano la fila curada.
4. Playwright: solo CommonJS + `NODE_PATH` (ver arriba); bloquear
   `**fonts.g**` y widgets externos en sandbox.
5. Los campos curados de la matriz (tema/estructura/hook/nota/eje) los
   escribe un humano o una sesión de análisis; el refresco automático solo
   toca views/likes/comentarios. Un fix nunca debe pisar lo curado.
6. Nunca mergear ramas de otras sesiones sin `git diff --stat` primero: una
   rama vieja puede borrar trabajo. Rescate puntual:
   `git checkout <rama> -- <archivo>`.

## Checklist de cierre de un fix

- [ ] El bug se reprodujo con output ANTES del cambio (pegado en el reporte).
- [ ] El diff es mínimo y ataca la causa raíz.
- [ ] El caso exacto que fallaba ahora pasa, con output pegado DESPUÉS.
- [ ] El comando de salud global sigue pasando completo.
- [ ] Si tocaste la calculadora: test del núcleo + smoke Playwright pasan.
- [ ] Si tocaste matriz/refresh: invariantes de matriz.json pasan.
- [ ] Commit descriptivo en la rama designada + PR a la rama por defecto.
