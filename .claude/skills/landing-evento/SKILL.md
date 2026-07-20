---
name: landing-evento
description: Genera landing pages HTML completas para eventos, workshops y webinars de Design Modeling Academy (DMA). Úsalo SIEMPRE que el usuario quiera crear o actualizar una landing page de evento/workshop/webinar/masterclass o necesite el código HTML de una página de registro para Sharp CRM. El output es HTML completo listo para pegar en Sharp CRM → Sites → Custom Code container. El HTML incluye countdown en vivo, formulario Sharp CRM embebido, SEO completo, Open Graph, Schema.org Event, countdown JS y el brandkit DMA. ACTIVA este skill cuando el usuario mencione: "landing-evento", "crear landing", "nueva landing workshop", "generar landing page", "landing para webinar", "página de registro evento", "html landing DMA", "nueva landing page", "landing del workshop", "crear página para el evento".
---

# Landing Page Generator — Design Modeling Academy

Genera el HTML completo de una landing page de evento DMA. El template base está en `assets/template.html` dentro de este directorio de skill.

**Brandkit DMA (siempre fijo):**
- Fuentes: Overpass (headings) + Nunito (body) — vía Google Fonts
- Paleta: Azul `#003e5c` · Naranja `#ca7520` · Navy `#001e30`
- Tailwind CDN con config extendida

---

## Paso 1: Recopilar datos del evento

Pide los datos al usuario en grupos. Si el usuario ya proporcionó algunos datos en su mensaje inicial, extráelos directamente. Para datos faltantes, usa AskUserQuestion o pide en texto. Los datos con ★ son obligatorios; los demás tienen defaults razonables.

### Bloque A — Básico
| Campo | Ejemplo | Obligatorio |
|---|---|---|
| Título del evento | "Workshop: Automatización con Dynamo" | ★ |
| Parte del título en naranja | "Automatización con Dynamo" | ★ |
| Fecha (texto para badge) | "JUE 15 JUN" | ★ |
| Fecha ISO completa | "2026-06-15T19:00:00-05:00" | ★ |
| Fecha fin ISO | "2026-06-15T20:30:00-05:00" | ★ |
| Hora para badge | "7:00 PM ECU" | ★ |
| Duración | "90 minutos" | ★ |
| Tipo de evento (badge) | "EN VIVO ZOOM" / "PRESENCIAL" | ★ |
| Form ID Sharp CRM | `h9NZipnVKXK5CfjmPTHS` | ★ |

### Bloque B — SEO y URLs
| Campo | Ejemplo | Obligatorio |
|---|---|---|
| URL canónica | `https://designmodelingacademy.com/workshop-dynamo` | ★ |
| OG Image URL (1200×630) | `https://assets.cdn.filesafe.space/…/imagen.png` | ★ |
| URL del Zoom/evento | `https://us06web.zoom.us/…` | — |
| Meta description (≤155 chars) | Texto descriptivo del evento | — |
| Keywords | Lista separada por comas | — |

### Bloque C — Hero copy
| Campo | Ejemplo |
|---|---|
| Headline h1 (parte fija) | "El nuevo estándar de" |
| Headline h1 (parte naranja) | "certificación profesional BIM" |
| Párrafo intro del hero | "Descubre el beneficio que está transformando…" |
| Número de registrados | "+248" |

### Bloque D — Contenido del workshop
- **3 Beneficios** (cards "¿Por qué asistir?"): título + descripción para cada card
- **8 Bullets de contenido** (qué aprenderán)
- **Sección de comparación**: 4 puntos del método viejo (rojo) + 4 del nuevo (verde) + nombre de ambas columnas + badge del nuevo (e.g., "Nuevo estándar")

### Bloque E — Expositor
- Nombre completo con título (e.g., "Ing. Gabriel Pantoja")
- Cargo/especialidad (e.g., "Especialista BIM, Revit & Automatización · Design Modeling DG")
- URL de imagen del expositor
- Bio: 2 párrafos
- 3 stats: número + etiqueta (e.g., "500+ / Alumnos formados")

### Bloque F — Sección temática especial
Esta sección es el "corazón del tema" del evento (e.g., NFT Badges, herramienta, metodología). Pide:
- Eyebrow, título principal, subtítulo acento (naranja)
- Descripción
- Imágenes/badges opcionales (URLs) — omite esta subsección si no hay imágenes
- 3 features: título + descripción cada uno

### Bloque G — Testimonios y horarios
- 4 testimonios: cita + URL foto + nombre + cargo/país
- Ajuste de horarios por país si el evento NO es a las 7 PM Ecuador

**Default de horarios (7 PM Ecuador GMT-5):**
```
6:00 PM → México, Costa Rica, Guatemala, Honduras
7:00 PM → Ecuador (resaltado), Colombia, Panamá
8:00 PM → Chile
9:00 PM → Uruguay
```
Si el usuario no provee testimonios, reutiliza los cuatro defaults:
1. Javier Solórzano — Coordinador BIM · México
2. Albino Piñeiro — BIM Manager · España
3. Luis Fernández — Arquitecto · BIM Lead · Colombia
4. Edy Díaz — BIM Coordinator · Perú

---

## Paso 2: Construir el HTML

1. Lee el archivo `assets/template.html` (en el mismo directorio de este skill)
2. Sustituye cada `{{PLACEHOLDER}}` por los datos del usuario
3. Para `{{TIMEZONE_ROWS}}` genera las filas `<li>` con esta estructura, resaltando la fila del país anfitrión:
   ```html
   <li class="flex items-baseline gap-2">
     <strong class="font-heading font-bold text-azul w-[58px] flex-shrink-0">X:00 PM</strong>
     <span>País, País</span>
   </li>
   <!-- Fila resaltada (Ecuador/anfitrión): -->
   <li class="flex items-baseline gap-2 bg-naranja-pal/50 -mx-2 px-2 py-1 rounded">
     <strong class="font-heading font-bold text-naranja w-[58px] flex-shrink-0">X:00 PM</strong>
     <span><strong class="text-azul">País anfitrión</strong> · País, País</span>
   </li>
   ```
4. Para `{{COMPARISON_OLD_BULLETS}}` genera 4 `<li>`:
   ```html
   <li class="flex items-start gap-3">
     <span class="text-red-500 font-bold flex-shrink-0 mt-0.5">✕</span>
     <span class="text-gris-text">Texto del punto</span>
   </li>
   ```
5. Para `{{COMPARISON_NEW_BULLETS}}` genera 4 `<li>`:
   ```html
   <li class="flex items-start gap-3">
     <span class="text-green-600 font-bold flex-shrink-0 mt-0.5">✓</span>
     <span class="text-azul-navy"><strong>Término clave</strong>, resto del texto</span>
   </li>
   ```
6. Para `{{SPECIAL_BADGES_ROW}}` — si hay URLs de imágenes, genera:
   ```html
   <div class="flex flex-wrap items-center justify-center gap-6 md:gap-8 lg:gap-10">
     <img src="URL" alt="Badge N" class="w-24 md:w-32 lg:w-36 h-auto hover:scale-110 transition-transform" loading="lazy" decoding="async">
   </div>
   ```
   Si no hay imágenes, deja el bloque vacío (string vacío).
7. Para convertir fecha a ISO: "28 de mayo 2026 7 PM Ecuador" → `2026-05-28T19:00:00-05:00` (Ecuador = GMT-5)

### Tabla de placeholders

| Placeholder | Dato |
|---|---|
| `{{META_TITLE}}` | `<title>` completo |
| `{{META_DESCRIPTION}}` | Meta description |
| `{{META_KEYWORDS}}` | Keywords |
| `{{OG_TITLE}}` | OG title |
| `{{OG_DESCRIPTION}}` | OG description |
| `{{OG_IMAGE}}` | URL imagen OG |
| `{{OG_IMAGE_ALT}}` | Alt text imagen OG |
| `{{OG_URL}}` | OG URL = canonical |
| `{{CANONICAL_URL}}` | Canonical URL |
| `{{SCHEMA_NAME}}` | Nombre evento Schema.org |
| `{{SCHEMA_START}}` | Fecha inicio ISO |
| `{{SCHEMA_END}}` | Fecha fin ISO |
| `{{SCHEMA_ZOOM_URL}}` | URL evento para Schema.org |
| `{{SCHEMA_PERFORMER}}` | Nombre expositor |
| `{{SCHEMA_DESCRIPTION}}` | Descripción Schema.org |
| `{{BADGE_DATE}}` | Badge fecha hero |
| `{{BADGE_TIME}}` | Badge hora hero |
| `{{BADGE_TYPE}}` | Badge tipo |
| `{{EYEBROW_HERO}}` | Eyebrow hero |
| `{{H1_MAIN}}` | Texto fijo del h1 |
| `{{H1_HIGHLIGHT}}` | Texto naranja del h1 |
| `{{HERO_INTRO}}` | Párrafo intro hero |
| `{{COUNTDOWN_TARGET}}` | ISO date para countdown JS |
| `{{TIMEZONE_ROWS}}` | HTML filas tabla horarios |
| `{{REGISTRADOS}}` | Número registrados |
| `{{FORM_ID}}` | Form ID Sharp CRM |
| `{{FORM_EYEBROW}}` | Eyebrow del form box |
| `{{FORM_TITLE}}` | Título del form box |
| `{{FORM_SUBTITLE}}` | Subtítulo del form box |
| `{{BENEFITS_EYEBROW}}` | Eyebrow sección beneficios |
| `{{BENEFITS_TITLE}}` | Título sección beneficios |
| `{{BENEFITS_SUBTITLE}}` | Subtítulo sección beneficios |
| `{{BENEFIT_1_TITLE}}` / `{{BENEFIT_1_DESC}}` | Beneficio 1 |
| `{{BENEFIT_2_TITLE}}` / `{{BENEFIT_2_DESC}}` | Beneficio 2 |
| `{{BENEFIT_3_TITLE}}` / `{{BENEFIT_3_DESC}}` | Beneficio 3 |
| `{{COMPARISON_EYEBROW}}` | Eyebrow comparación |
| `{{COMPARISON_TITLE}}` | Título comparación |
| `{{COMPARISON_OLD_COL}}` | Nombre columna izquierda |
| `{{COMPARISON_NEW_COL}}` | Nombre columna derecha |
| `{{COMPARISON_NEW_BADGE}}` | Badge columna nueva |
| `{{COMPARISON_OLD_BULLETS}}` | 4 `<li>` método viejo |
| `{{COMPARISON_NEW_BULLETS}}` | 4 `<li>` método nuevo |
| `{{CONTENT_EYEBROW}}` | Eyebrow sección contenido |
| `{{CONTENT_TITLE}}` | Título sección contenido |
| `{{CONTENT_SUBTITLE}}` | Subtítulo sección contenido |
| `{{CONTENT_1}}` … `{{CONTENT_8}}` | 8 bullets de contenido |
| `{{EXPOSITOR_EYEBROW}}` | Eyebrow expositor |
| `{{EXPOSITOR_NAME}}` | Nombre expositor |
| `{{EXPOSITOR_TITLE}}` | Cargo expositor |
| `{{EXPOSITOR_IMAGE}}` | URL imagen expositor |
| `{{EXPOSITOR_BIO_1}}` | Bio párrafo 1 |
| `{{EXPOSITOR_BIO_2}}` | Bio párrafo 2 |
| `{{STAT_1_NUM}}` / `{{STAT_1_LABEL}}` | Stat 1 |
| `{{STAT_2_NUM}}` / `{{STAT_2_LABEL}}` | Stat 2 |
| `{{STAT_3_NUM}}` / `{{STAT_3_LABEL}}` | Stat 3 |
| `{{SPECIAL_EYEBROW}}` | Eyebrow sección especial |
| `{{SPECIAL_TITLE}}` | Título sección especial |
| `{{SPECIAL_SUBTITLE_ACCENT}}` | Subtítulo acento (naranja) |
| `{{SPECIAL_DESC}}` | Descripción sección especial |
| `{{SPECIAL_BADGES_ROW}}` | HTML imágenes/badges (o vacío) |
| `{{SPECIAL_F1_TITLE}}` / `{{SPECIAL_F1_DESC}}` | Feature especial 1 |
| `{{SPECIAL_F2_TITLE}}` / `{{SPECIAL_F2_DESC}}` | Feature especial 2 (borde naranja) |
| `{{SPECIAL_F3_TITLE}}` / `{{SPECIAL_F3_DESC}}` | Feature especial 3 |
| `{{TESTIMONIO_1_QUOTE}}` … `{{TESTIMONIO_4_QUOTE}}` | Citas |
| `{{TESTIMONIO_1_IMAGE}}` … `{{TESTIMONIO_4_IMAGE}}` | URLs fotos |
| `{{TESTIMONIO_1_NAME}}` … `{{TESTIMONIO_4_NAME}}` | Nombres |
| `{{TESTIMONIO_1_ROLE}}` … `{{TESTIMONIO_4_ROLE}}` | Cargos y países |
| `{{CTA_EYEBROW}}` | Eyebrow CTA final |
| `{{CTA_TITLE}}` | Título CTA final |
| `{{CTA_DESC}}` | Descripción CTA final |
| `{{CTA_DATE_SUMMARY}}` | Fecha/hora/duración en CTA |
| `{{FOOTER_COPYRIGHT}}` | Texto copyright footer |
| `{{FOOTER_EVENT_DATE}}` | Fecha evento en footer |

---

## Paso 3: Output al usuario

1. Presenta un resumen de 5–8 líneas con los datos clave usados
2. Presenta el HTML completo en un bloque de código ` ```html `
3. Incluye estas instrucciones:
```
📋 CÓMO PEGAR:
Sharp CRM → Sites → DMA → Embudo del evento
→ Custom Code container → Pegar todo el HTML
```
4. Si faltó algún dato crítico (Form ID, imagen OG, canonical URL), márcalo con 📌
5. Ofrece ajustar cualquier sección si el usuario quiere cambios

---

## Logos del footer (estáticos para todos los eventos DMA)

El footer siempre usa estos logos CDN (no cambies las URLs):
- **Producido por**: `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04bbc1138c806d2dce58f9.png`
- **Acreditado 1**: `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d1f060b8c350d3e114d7.png`
- **Acreditado 2**: `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d1f0f7d455340c70e652.png`
- **Software**: `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d1738c6475e185dfddb1.png`
- **Navbar**: `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04bbc1fa8afa3be0bb00d8.png`
