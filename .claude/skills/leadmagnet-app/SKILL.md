---
name: leadmagnet-app
description: Construye lead magnets interactivos completos para Design Modeling Academy (DMA) — calculadoras de ingeniería, mini-apps y herramientas gratuitas de captura — replicando el sistema probado con la Calculadora de Zapatas. Cubre el ciclo completo end-to-end - app HTML autocontenida con brandkit DMA, verificación de fórmulas contra el Excel fuente, landing de captura, página de gracias+agenda, publicación en GitHub Pages, integración GoHighLevel (formulario nativo, membresía con iframe, bot de palabra clave IG/FB), brief de contenido y tarea para el equipo. ACTIVA cuando el usuario diga - "leadmagnet-app", "nueva calculadora", "crear calculadora de [tema]", "otra app como la de zapatas", "lead magnet nuevo", "herramienta gratuita para captar leads", "mini app de ingeniería", "calculadora para regalar", o pida convertir un Excel de cálculo en una app de captura.
---

# LEADMAGNET-APP — Lead magnets interactivos de Design Modeling Academy

Convierte una hoja de cálculo o metodología de un curso DMA en un **lead
magnet completo en producción**: app + funnel + GHL + contenido. La
**implementación de referencia es `calculadora-zapatas/`** en el repo
`meta-ads-dashboard.html` — copia sus patrones, no reinventes.

## Brandkit DMA (fijo, no modificar)

- Fuentes: **Overpass** (títulos/UI) + **Nunito** (cuerpo), vía Google Fonts.
- Paleta: `--azul-principal:#003e5c` · `--azul-medio:#0a5a80` ·
  `--azul-navy:#001e30` · `--naranja:#ca7520` · `--naranja-claro:#e8a04a` ·
  `--naranja-palido:#f7e8cc` · `--crema:#fafaf7`.
- Logo: `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04bbc1fa8afa3be0bb00d8.png`
- Marquee de avales y patrones de secciones: usar el skill **landing-producto**
  (`.claude/skills/landing-producto/`).

## Workflow completo (10 pasos)

### 1. Fuente de la lógica
Pide el Excel o la especificación del cálculo. Léelo con el skill **xlsx**
(dos pasadas: fórmulas + valores). Extrae: entradas, fórmulas paso a paso,
valores de ejemplo para verificar, y unidades. Si una celda de la hoja está
rota o es ambigua, usa el criterio estándar de ingeniería y documenta la
decisión.

### 2. La app (patrón `calculadora-zapatas/app.html`)
HTML **autocontenido** (un solo archivo, sin dependencias — debe poder
pegarse como Custom Code en GHL):
- Núcleo de cálculo como **función pura** entre marcadores
  `/* CALC-START */ ... /* CALC-END */` (permite extraerla y testearla).
- Columna de entradas (cards numeradas) + columna de resultados en vivo.
- Chips **CUMPLE ✔ / VERIFICAR ✖** para cada verificación.
- Botón "✨ Sugerir dimensiones" (o equivalente) que itere hasta cumplir.
- Esquema SVG que se redibuja con los datos.
- **Candado**: `REQUIERE_REGISTRO`, `TOKEN_ACCESO` (formato `dmAAAA`), y
  `URL_LANDING`. Se desbloquea con `?acceso=TOKEN` (que además persiste en
  localStorage) o desde la landing.
- Disclaimer fijo: herramienta educativa/predimensionamiento; el diseño
  definitivo lo firma un ingeniero responsable. Nunca prometer más.

### 3. Verificación (obligatoria antes de publicar)
- `sed -n '/CALC-START/,/CALC-END/p' app.html > calc.js` + test en node que
  compare **cada magnitud** contra los valores del Excel fuente (tolerancia
  1e-6 relativa). Cero diferencias o no se publica.
- Smoke test Playwright (chromium en `/opt/pw-browsers/chromium`; bloquear
  `**fonts.g**` y widgets GHL en el sandbox): candado sin registro →
  formulario → redirección con token → resultados renderizados → caso que
  falla marca VERIFICAR → botón sugerir → sin errores JS.

### 4. Landing de captura (patrón `calculadora-zapatas/index.html`)
Usar la estructura del skill **landing-producto** adaptada a producto
gratuito: nav + hero con form card + marquee de avales + "qué obtienes"
(stack-tools) + metodología (módulos) + "así se usa" (captura real de la
app en `img/`) + para quién (sí/no) + FAQ + CTA final + footer.
Formulario con dos vías (constantes en el script):
- `GHL_FORM_IFRAME_URL` — **preferida**: formulario nativo de GHL embebido
  (iframe con data-attributes + `https://link.msgsndr.com/js/form_embed.js`);
  contactos directo al CRM sin costo. GHL redirige al terminar.
- `GHL_WEBHOOK_URL` — respaldo: POST JSON `{nombre,email,telefono,perfil,
  fuente,pagina}` con `mode:'no-cors'`; nunca bloquear el acceso si falla.
  ⚠️ El Inbound Webhook de GHL es prémium (cobra por ejecución).

### 5. Página de gracias + agenda (patrón `gracias-agenda.html`)
Hero de confirmación + **botón grande de acceso directo a la app CON el
token** (⚠️ nunca prometer "te lo enviamos por correo/WhatsApp" — no existe
ese workflow) + calendario de booking embebido para la sesión estratégica
(puente al Máster) + pasos del proceso.

### 6. Publicación (GitHub Pages vía gh-pages)
- Carpeta nueva en la raíz del repo (ej. `calculadora-<tema>/`) con:
  `index.html`, `app.html`, `gracias-agenda.html`, `ghl-landing.html`,
  `img/`, `GUIA-MONTAJE.md`.
- Añadir la carpeta a `.github/workflows/publish-matriz.yml` (paso "Armar
  carpeta pública" + `paths:`). El workflow publica con peaceiris a la rama
  `gh-pages` — no requiere configuración manual de Pages.
- `ghl-landing.html` se **genera desde index.html** (script python: extrae
  `<style>` + body, vuelve absolutas las URLs relativas). No editar a mano.
- Git: desarrollar en la rama designada, PR a la rama por defecto
  (`claude/remote-control-setup-GUe3f` — no hay main/master) y merge.
  ⚠️ Nunca mergear ramas de otras sesiones sin verificar que no estén
  desactualizadas (`git diff --stat` primero): una rama vieja puede borrar
  trabajo. Rescatar archivos con `git checkout <rama> -- <archivo>`.
- URLs resultantes: `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/<carpeta>/…`
  Para saltar la caché del CDN: `?v=N` o
  `https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/gh-pages/<carpeta>/<archivo>`.

### 7. Montaje en GHL (lo ejecuta el usuario o su Claude de navegador)
Entregar instrucciones copy-paste (patrón `GUIA-MONTAJE.md` y
`GUIA-MEMBRESIA-GHL.md`):
- Funnel: página 1 = `ghl-landing.html` en Custom Code ancho completo sin
  padding; página 2 = `gracias-agenda.html`; el form nativo redirige a la
  página 2.
- Membresía: producto con lección que embebe la app por **iframe con
  `?acceso=TOKEN`** + oferta Free + workflow "Form Submitted → Grant Offer".
  ⚠️ Publicar el **producto** (no solo la lección y la oferta) y habilitar
  la app de Cursos en el Client Portal — son las 2 causas típicas de
  "portal vacío".
- Comunidades: vincular el curso en la pestaña Learning de cada grupo +
  post de anuncio; opcional concesión masiva de la oferta a miembros.

### 8. Bot de palabra clave IG/FB (patrón `BOT-ZAPATA-GHL.md`)
Workflow con disparadores de comentario IG+FB filtrados por la palabra
clave del CTA → respuesta pública → DM 1 con la URL de la landing → espera →
DM 2 de calificación → etiquetas (`lead-<tema>` + `origen-bot-<palabra>`) →
notificación interna. Respetar la ventana de 24 h de Meta.

### 9. Contenido
Brief para la conversación de la matriz viral en
`matriz-viral/BRIEF-<TEMA>.md` (patrón `BRIEF-CALCULADORA-ZAPATAS.md`):
qué es, funnel, momento "wow" para el screen-recording, conexión con reels
que ya funcionaron, hooks, CTA "Comenta <PALABRA>", reglas de precisión.
Post de comunidades con el enlace de la landing.

### 10. Cierre operativo
- Tarea en ClickUp (lista "Configuración dentro de Go High Level",
  espacio Tech + Bot) asignada a **Ester Alvarez y Aylin Tapia** con el
  resumen, enlaces y pendientes.
- Checklist E2E de 10 puntos (patrón en `BOT-ZAPATA-GHL.md` §2): comentario
  → DM → landing → formulario → gracias → app sin candado → contacto en CRM
  → membresía otorgada + login → cita de prueba → limpieza.

## Reglas de oro

1. Fórmulas verificadas 1:1 contra la fuente antes de publicar. Siempre.
2. Todo autocontenido y con URLs absolutas en las versiones para GHL.
3. El acceso es instantáneo por token — nunca prometer envíos por
   correo/WhatsApp que no existen.
4. Brandkit DMA exacto en todas las piezas.
5. Disclaimer educativo en la app y en el copy (no exagerar capacidades).
6. Probar en navegador real (Playwright) antes de cada publicación.
