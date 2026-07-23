---
name: chequeo-seguridad
description: >
  Chequeo de seguridad específico de ESTE repositorio (repo PÚBLICO de DMA con
  GitHub Pages, lead magnets GHL y workflows de Actions). Úsalo SIEMPRE que el
  usuario pida "chequeo de seguridad", "auditoría de seguridad", "revisar
  seguridad", "¿hay secretos expuestos?", "security review/audit", o antes de:
  hacer merge a la rama por defecto, publicar una landing o calculadora nueva a
  Pages/GHL, agregar un workflow de Actions, o agregar un script que use tokens
  (Apify u otros). También proactivamente si detectas un posible secreto
  committeado o PII de leads en el repo. Produce un reporte con hallazgos por
  severidad, archivo:línea, cómo se explota, arreglo concreto y lo NO revisado.
---

# Chequeo de seguridad — meta-ads-dashboard.html (DMA)

## Contexto: qué es este repo y por qué importa

- **Repo PÚBLICO** (`designmodelingdg-droid/meta-ads-dashboard.html`) con
  **GitHub Pages activo** (rama `gh-pages`). Todo lo committeado lo puede leer
  cualquiera, y `matriz-viral/matriz/matriz.json` + `calculadora-zapatas/**` se
  publican además como sitio en
  `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/`.
  Consecuencia: **un secreto committeado una sola vez está quemado para
  siempre** (el historial es público) — el arreglo siempre incluye ROTAR la
  credencial, no solo borrarla del archivo.
- **Stack**: HTML estático autocontenido (sin npm, sin package.json, sin
  build), un script Python de stdlib (`scripts/refresh_matriz.py`), dos
  workflows de Actions (`.github/workflows/refresh-matriz.yml` y
  `publish-matriz.yml`), y skills DMA con templates HTML en `.claude/skills/`.
- **No hay backend propio, ni logins, ni pagos en este código.** Los datos
  delicados reales son: (1) los **leads** (nombre, email, WhatsApp) que los
  formularios envían a GoHighLevel/Sharp CRM, (2) el **APIFY_TOKEN** del
  scraper, (3) los workflows con `contents: write`, y (4) todo lo que termina
  publicado en Pages.
- **Cómo se corre**: no hay build. HTML: `python3 -m http.server 8000` y abrir
  `calculadora-zapatas/index.html`. Script:
  `APIFY_TOKEN=xxx python3 scripts/refresh_matriz.py`. Lint: `htmlhint` (lo
  instala `.claude/hooks/session-start.sh`).
- **Rama por defecto**: `claude/remote-control-setup-GUe3f` (no `main`). Los
  pushes a ella disparan `publish-matriz.yml` → publicación a Pages.

## La regla de oro

Cada hallazgo lleva: **archivo:línea, severidad (CRÍTICA/ALTA/MEDIA/BAJA), y
cómo se explota en UNA frase** ("un atacante puede X haciendo Y"). Si no
puedes escribir esa frase, no es hallazgo: es opinión o mejora de higiene, y
va en una sección aparte o no va.

Antes de reportar, **intenta tumbar cada hallazgo propio**: ¿de verdad es
alcanzable por un atacante? ¿el dato ya es público por diseño? ¿el "secreto"
es un placeholder de documentación? Solo sobreviven los que resisten. En este
repo hay varias trampas conocidas — ver "Falsos positivos conocidos" abajo.

## El chequeo, en este orden

### 1. Secretos expuestos o committeados (lo primero, siempre)

El repo es público: buscar en el árbol actual **y en todo el historial**.

```bash
# Árbol actual + historial completo (el .pyc committeado mete ruido binario; ignóralo)
git grep -IiE '(apify_api_[a-zA-Z0-9]|sk-[a-zA-Z0-9]{20}|ghp_[a-zA-Z0-9]|github_pat_|xox[bp]-|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|-----BEGIN (RSA|EC|OPENSSH)|eyJhbGciOi)' $(git rev-list --all) -- ':!*.pyc' || echo "limpio"

# Archivos sospechosos agregados alguna vez (dumps, exports, .env)
git log --all --diff-filter=A --name-only --pretty=format: | sort -u | grep -iE '\.(env|csv|sqlite|bak)$|export|leads|contactos' || echo "limpio"
```

- `APIFY_TOKEN` debe existir SOLO como secreto de Actions
  (Settings → Secrets → Actions). Referencias como `${{ secrets.APIFY_TOKEN }}`
  o `APIFY_TOKEN=xxxx` en docs son correctas; un token real empieza con
  `apify_api_`.
- Si aparece un token real en cualquier commit: severidad CRÍTICA, y el
  arreglo es **rotarlo en el proveedor** + limpiar; borrar el archivo no basta.

### 2. Validación de lo que entra, por cada entrada real

Entradas de este proyecto (no hay más endpoints que estos):

| Entrada | Dónde | Qué revisar |
|---|---|---|
| `leadForm` (nombre/email/telefono/perfil) | `calculadora-zapatas/index.html` y `ghl-landing.html` (~línea 440) | Va como JSON al webhook GHL vía `fetch`. La validación real la hace GHL; aquí solo confirmar que el JS no meta esos valores al DOM con `innerHTML`. |
| Parámetro `?acceso=` | `calculadora-zapatas/app.html:175-182` | Solo se compara contra `TOKEN_ACCESO` — verificar que nunca se inserte al DOM ni se use para otra cosa. |
| Inputs numéricos de la calculadora | `app.html` (motor de cálculo → `innerHTML` en líneas ~332-398) | Todo lo que entre a `resBody.innerHTML` debe pasar antes por `parseFloat`/formateo numérico. Un input que llegue como string crudo a ese template = XSS. |
| **Datos de Apify** (captions de Instagram) | `scripts/refresh_matriz.py:139-149` | Es la entrada externa MENOS confiable: texto de captions escrito por terceros entra sin sanitizar a `matriz.json` (`tema`, `hook`), se committea solo (workflow) y se publica en Pages. Cualquier consumidor que renderice `matriz.json` con `innerHTML` hereda un XSS almacenado. Revisar consumidores nuevos de `matriz.json`. |

### 3. Quién puede tocar qué (autorización, no solo autenticación)

- **Workflows**: ambos tienen `permissions: contents: write` y
  `refresh-matriz.yml` **commitea y pushea a la rama por defecto sin revisión
  humana** con datos que vienen de Apify/Instagram. Revisar que ningún
  workflow nuevo amplíe permisos (`id-token`, `pull-requests: write`, PATs) ni
  use `pull_request_target` con checkout del PR.
- **Cadena de publicación**: Apify → `matriz.json` → commit automático → Pages
  público. Todo lo que entre a esa cadena termina publicado con la marca DMA.
- **`?acceso=dm2026` NO es autorización**: es un candado de marketing
  client-side (cualquiera lee el token en el fuente público). Aceptado por
  diseño para la calculadora gratuita. Se vuelve hallazgo ALTO solo si algún
  cambio pone contenido **de pago o privado** detrás de ese mecanismo.

### 4. Inyección

- XSS: `grep -rn "innerHTML\|insertAdjacentHTML\|document.write" --include='*.html' .`
  y verificar que cada uso reciba solo constantes o números formateados
  (estado conocido: `index.html:421` y `ghl-landing.html:421` usan constantes;
  `app.html:332-398` usa números calculados — mantenerlo así).
- Inyección en workflows: nada de `${{ }}` con contenido controlado por
  terceros (títulos de issues/PRs, captions) dentro de `run:`.
- No hay SQL, ni shell sobre input de usuario, ni server-side templates aquí
  — no inventar hallazgos de esas clases sin código que los sustente.

### 5. Datos sensibles en logs, respuestas o en el repo

- `refresh_matriz.py:96-97` manda el token de Apify **en la query string**
  (`?token=...`): si alguien agrega un `print(url)` o el error HTTP incluye la
  URL, el token queda en los logs públicos de Actions. Vigilar que los
  mensajes de error nunca impriman `url`. (Arreglo preferido: mandarlo como
  header `Authorization: Bearer`.)
- **PII de leads**: los leads viven en GHL, no aquí. NUNCA aceptar en el repo
  exports de contactos (CSV de GHL, listas de WhatsApp/correos). Revisar
  también `matriz-viral/fuentes/*.json` (scrapes de IG): métricas y captions
  propios OK; usernames/comentarios de terceros identificables, no.
- Los logs de Actions son públicos (repo público): cualquier `print`/`echo`
  de un workflow es visible para el mundo.

### 6. Dependencias con hoyos conocidos

No hay package.json — las "dependencias" de este repo son otras:

- **Actions de terceros**: `grep -rn "uses:" .github/workflows/`. Estado:
  `actions/checkout@v4` (oficial, OK) y `peaceiris/actions-gh-pages@v4`
  (tercero, pineado por tag mutable — un compromiso de ese tag publicaría
  contenido arbitrario en el sitio DMA; recomendar pin por SHA de commit).
- **JS de terceros que ejecuta en las páginas**: `link.msgsndr.com/js/form_embed.js`
  (GHL, necesario para forms/calendario), iframes de
  `api.leadconnectorhq.com`, imágenes de `assets.cdn.filesafe.space`, y
  Tailwind por CDN en los templates de `.claude/skills/*/assets/`. Listar
  cualquier dominio NUEVO que aparezca: cada script externo puede ejecutar JS
  con acceso total a la página del formulario de leads.

## Falsos positivos conocidos (no reportarlos como críticos)

- Las URLs GHL committeadas — webhook
  `services.leadconnectorhq.com/hooks/nkKbOarn5IwHeMv48uY9/...`
  (`index.html:407`), formulario `omuCtBdv0ZWbP9kAS5TB`, calendario
  `bIVuNHNojGEgH3gf6yXe` — **no son secretos**: van al navegador de cada
  visitante por diseño. El riesgo real asociado es otro y es MEDIO: el
  Inbound Webhook es un activador prémium de GHL (cobra por ejecución) y
  cualquiera puede hacerle POST con leads falsos (costo + basura en el CRM).
  Mitigación: preferir el formulario nativo (Vía B, ya activa) y desactivar
  el workflow del webhook si no se usa.
- `TOKEN_ACCESO = 'dm2026'`: candado cosmético aceptado (ver §3).
- `APIFY_TOKEN=xxxx` en docstrings/READMEs: placeholder, no token real.
- `scripts/__pycache__/*.pyc` committeado: higiene (BAJA), no vulnerabilidad.

## Formato del reporte (siempre este)

```markdown
# Chequeo de seguridad — <fecha> — <rama/commit>

## CRÍTICA / ALTA / MEDIA / BAJA  (una sección por severidad, omitir vacías)
- **<título corto>** — `archivo:línea`
  - Cómo se explota: <una frase>
  - Arreglo: <acción concreta: comando, diff o paso en GHL/GitHub>

## Intenté tumbar y no sobrevivieron
- <hallazgo descartado> — por qué se descartó (1 línea c/u)

## Lo que NO se revisó (honesto)
- <p.ej.: configuración interna de GHL, workflows/permisos del CRM, la cuenta
  de Apify, DNS de dgdesignmodeling.com, ajustes del repo en GitHub que
  requieren admin, ramas no revisadas>
```

Cierra siempre con el arreglo más urgente en una línea ("Si solo haces una
cosa hoy: ..."). Si no sobrevivió ningún hallazgo, dilo explícitamente — un
reporte vacío honesto vale más que hallazgos inflados.
