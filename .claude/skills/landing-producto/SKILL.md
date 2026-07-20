---
name: landing-producto
description: Genera landing pages HTML completas para programas robustos de Design Modeling Academy (DMA): Másters, Diplomados, Certificaciones y cualquier producto de alto ticket. ÚSALO cuando el usuario quiera crear o actualizar una página de ventas para un programa de formación largo (meses), con secciones de currículum, bonos, certificaciones universitarias, testimonios y FAQ. El output es HTML completo listo para pegar en Sharp CRM / GHL → Sites → Custom Code container. CSS propio (sin Tailwind), formulario GHL embebido, marquee animado de avales, sección de diplomas universitarios. ACTIVA cuando el usuario diga: "landing-producto", "landing del máster", "landing del diplomado", "página de ventas del máster", "landing programa", "crear landing para el diplomado", "nueva landing de certificación", "página de aplicación", "sales page programa".
---

# Landing de Producto Robusto — Design Modeling Academy

Genera el HTML completo para una landing de ventas de programa largo (Máster, Diplomado, Certificación). El template está en `assets/template.html`. CSS propio con variables CSS DMA — no usa Tailwind.

**Brandkit DMA (siempre fijo):**
- Fuentes: Overpass (headings/UI) + Nunito (body)
- Paleta: `--azul-principal: #003e5c` · `--naranja: #ca7520` · `--azul-navy: #001e30`
- CSS con custom properties — no modificar las variables de color

---

## Paso 1: Recopilar datos del programa

Los datos con ★ son obligatorios; los demás tienen defaults razonables del template.

### Bloque A — Producto y hero
| Campo | Ejemplo | ★ |
|---|---|---|
| Nombre del producto | "Máster Internacional BIM Manager + IA" | ★ |
| Eyebrow del hero | "Inscripciones abiertas · Cupos limitados" | |
| Titular h1 (texto fijo) | "Asegura tu lugar y accede al Máster más completo en" | ★ |
| Titular h1 (parte `<em>` naranja) | "BIM Management + IA aplicada a la construcción" | ★ |
| Párrafo lead del hero | "Eleva tu perfil profesional este 2026…" | ★ |
| Frase destacada (quote lateral) | "Estudia desde donde estés. Aplica desde el primer mes." | |
| Stat 1: número + etiqueta | "+4.500 / Egresados activos" | |
| Stat 2: número + etiqueta | "3 continentes / LATAM · EE.UU. · Europa" | |
| Stat 3: número + etiqueta | "1:1 / Mentorías personalizadas" | |
| Texto botón navbar | "Aplicar al Máster" | ★ |

### Bloque B — Formulario GHL
| Campo | Ejemplo | ★ |
|---|---|---|
| Form ID | `u6Z0RJDMYa01AqsoyX34` | ★ |
| Fuente del embed | `api.leadconnectorhq.com` ó `link.apisystem.tech` | |
| Nombre del form (data-form-name) | "FORMULARIO MASTER (LANDING + IA)" | |
| Título del form card | "Postula al Máster en 60 segundos" | |
| Subtítulo del form card | "Completa el formulario. Un asesor te contacta en 24h." | |
| Pie del form card | "100% gratis · Sin compromiso · Solo para perfiles que califiquen" | |
| Height del iframe | 1180 | |

**URL base del embed:**
- Si viene de Sharp CRM: `https://link.apisystem.tech/widget/form/{{FORM_ID}}`
- Si viene de GHL directo: `https://api.leadconnectorhq.com/widget/form/{{FORM_ID}}`
- Script: Sharp → `https://link.apisystem.tech/js/form_embed.js` · GHL → `https://link.msgsndr.com/js/form_embed.js`

### Bloque C — Stack técnico (herramientas)
Lista de 5–10 herramientas que dominará el alumno. Cada una tiene:
- Nombre corto (e.g., "Revit")
- Rol (e.g., "Modelado BIM")

Default del Máster BIM+IA: Revit, Navisworks, Dynamo, Python, IA

### Bloque D — Para quién
- **Título sección**: "¿Es para ti?"
- **H2**: texto del headline
- **Lead**: párrafo introductorio
- **Lista SÍ**: 5 bullets (con `<strong>` en los términos clave)
- **Lista NO**: 4 bullets

### Bloque E — Currículum / Módulos
| Campo | Ejemplo |
|---|---|
| Subtítulo currículum | "12 meses · 12 módulos aplicados con mentoría personalizada" |
| Lead currículum | "Cada módulo combina clases en vivo…" |
| Módulos | Lista de N módulos: número + nombre + horas/submódulos |
| URL PDF Temario | Google Drive link |
| URL PDF Brochure | Google Drive link |

Genera cada módulo como:
```html
<div class="module">
  <div class="module-num">Módulo 01</div>
  <div class="module-meta">9h 10m · 6 submódulos</div>
  <h3>Nombre del módulo</h3>
</div>
```

### Bloque F — Bonos (4 bonos)
Cada bono: tag (e.g., "Bono exclusivo · 01") + título + descripción + valor

### Bloque G — Beneficios (6-8)
Cada beneficio: número de ícono (01-08) + título + descripción

### Bloque H — Certificación
- Eyebrow, H2, lead
- Lista de certificaciones incluidas (★ format en la lista)
- **3 diplomas universitarios**: para cada uno → imagen URL + nombre institución + detalle + flag (país) + si es `featured` (el primero por default)
- **3 certificados técnicos** (thumbs pequeños): imagen URL + alt text

### Bloque I — VSL (video)
- Poster URL (imagen de preview)
- Video source URL (puede ser .mov o .mp4)

### Bloque J — FAQ
Lista de preguntas y respuestas. Genera cada una como:
```html
<details class="faq-item">
  <summary>Pregunta aquí</summary>
  <div class="faq-content">Respuesta con <strong>bold</strong> donde aplique.</div>
</details>
```

### Bloque K — CTA final y footer
- H2, párrafo y texto del botón del CTA final
- Nombre del producto para el footer
- Texto descriptivo del footer
- Links de redes sociales (Instagram, etc.)

---

## Paso 2: Construir el HTML

1. Lee `assets/template.html`
2. Sustituye cada `{{PLACEHOLDER}}` con los datos del usuario
3. Para `{{STACK_TOOLS}}` genera los `.stack-tool` cards
4. Para `{{FOR_YES_ITEMS}}` y `{{FOR_NO_ITEMS}}` genera `<li>` con `<strong>` en términos clave
5. Para `{{MODULES}}` genera los `.module` divs
6. Para `{{DIPLOMAS}}` genera los `.diploma-card` divs completos (ver patrón en template)
7. Para `{{FAQ_ITEMS}}` genera los `<details class="faq-item">` blocks
8. Para `{{FOOTER_LINKS}}` genera los `<a>` links con href y texto correctos

### Tabla de placeholders principales

| Placeholder | Dato |
|---|---|
| `{{NAV_CTA}}` | Texto botón navbar |
| `{{NAV_ANCHOR}}` | ID del anchor (e.g., `aplicar`) |
| `{{HERO_EYEBROW}}` | Eyebrow del hero |
| `{{HERO_H1_MAIN}}` | Texto fijo del h1 |
| `{{HERO_H1_EM}}` | Parte em (naranja) del h1 |
| `{{HERO_LEAD}}` | Párrafo lead hero |
| `{{HERO_QUOTE}}` | Frase quote lateral |
| `{{HERO_S1_NUM}}` / `{{HERO_S1_LBL}}` | Stat 1 |
| `{{HERO_S2_NUM}}` / `{{HERO_S2_LBL}}` | Stat 2 |
| `{{HERO_S3_NUM}}` / `{{HERO_S3_LBL}}` | Stat 3 |
| `{{FORM_ID}}` | GHL Form ID |
| `{{FORM_BASE_URL}}` | URL base del embed (api.leadconnectorhq.com o link.apisystem.tech) |
| `{{FORM_SCRIPT_URL}}` | URL del script de embed |
| `{{FORM_NAME}}` | data-form-name |
| `{{FORM_HEIGHT}}` | Altura del iframe |
| `{{FORM_BADGE}}` | Badge mini del form card |
| `{{FORM_H3}}` | Título del form card |
| `{{FORM_SUBTITLE}}` | Subtítulo del form card |
| `{{FORM_FOOTER}}` | Pie del form card |
| `{{STACK_EYEBROW}}` / `{{STACK_H2}}` / `{{STACK_LEAD}}` | Sección stack |
| `{{STACK_TOOLS}}` | HTML de `.stack-tool` cards |
| `{{FOR_EYEBROW}}` / `{{FOR_H2}}` / `{{FOR_LEAD}}` | Sección para quién |
| `{{FOR_YES_H3}}` / `{{FOR_YES_ITEMS}}` | Lista sí |
| `{{FOR_NO_H3}}` / `{{FOR_NO_ITEMS}}` | Lista no |
| `{{CURR_EYEBROW}}` / `{{CURR_H2}}` / `{{CURR_LEAD}}` | Sección currículum |
| `{{MODULES}}` | HTML de `.module` cards |
| `{{PDF_TEMARIO_URL}}` / `{{PDF_BROCHURE_URL}}` | Links PDFs |
| `{{BONOS_EYEBROW}}` / `{{BONOS_H2}}` / `{{BONOS_LEAD}}` | Sección bonos |
| `{{BONO_1_TAG}}` … `{{BONO_4_VALUE}}` | 4 bonos completos |
| `{{BEN_EYEBROW}}` / `{{BEN_H2}}` / `{{BEN_LEAD}}` | Sección beneficios |
| `{{BENEFICIOS}}` | HTML de `.beneficio-card` items |
| `{{CERT_EYEBROW}}` / `{{CERT_H2}}` / `{{CERT_LEAD}}` | Sección cert |
| `{{CERT_LIST_ITEMS}}` | HTML de `<li>` certificaciones |
| `{{DIPLOMAS}}` | HTML de `.diploma-card` cards |
| `{{CERT_THUMBS_LABEL}}` | Label de thumbs técnicos |
| `{{CERT_T1_IMG}}` / `{{CERT_T1_ALT}}` | Thumb cert 1 |
| `{{CERT_T2_IMG}}` / `{{CERT_T2_ALT}}` | Thumb cert 2 |
| `{{CERT_T3_IMG}}` / `{{CERT_T3_ALT}}` | Thumb cert 3 |
| `{{VSL_EYEBROW}}` / `{{VSL_H2}}` / `{{VSL_LEAD}}` | Sección VSL |
| `{{VSL_POSTER}}` | URL poster del video |
| `{{VSL_SRC}}` | URL source del video |
| `{{TEST_EYEBROW}}` / `{{TEST_H2}}` / `{{TEST_LEAD}}` | Sección testimonios |
| `{{TEST_MORE_URL}}` | URL "Ver más historias" |
| `{{TEST_1_TEXT}}` … `{{TEST_4_ROLE}}` | 4 testimonios |
| `{{FAQ_EYEBROW}}` / `{{FAQ_H2}}` | Sección FAQ |
| `{{FAQ_ITEMS}}` | HTML de `<details>` FAQ |
| `{{FINAL_H2}}` / `{{FINAL_P}}` / `{{FINAL_BTN}}` | CTA final |
| `{{FOOTER_PRODUCT}}` | Nombre producto footer |
| `{{FOOTER_COPY}}` | Texto descriptivo footer |
| `{{FOOTER_LINKS}}` | HTML `<a>` links footer |
| `{{FOOTER_FINEPRINT}}` | Texto legal footer |

---

## Paso 3: Output al usuario

1. Resumen de 5-8 líneas con los datos clave (nombre, form ID, módulos, diplomas)
2. HTML completo en bloque ` ```html `
3. Instrucciones de uso:
```
📋 CÓMO PEGAR:
Sharp CRM/GHL → Sites → DMA → Embudo/Funnel del producto
→ Custom Code container → Pegar todo el HTML
Nota: GHL provee <html><head><body> automáticamente.
```
4. Marca con 📌 si falta el Form ID, URLs de diplomas o PDF links

---

## Avales en el marquee (estáticos para todos los productos DMA)

El authority marquee usa estas 8 imágenes siempre (duplicadas para loop infinito):
1. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d173601d54df8246caa4.png` — Autodesk Partner
2. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d1738c6475e185dfddb1.png` — Autodesk Training
3. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d2928c6475e185e02739.png` — Sabal University
4. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d1f0f7d455340c70e652.png` — Doctrina Qualitas
5. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d23b51d5d92ddcacf917.png` — U. de las Naciones
6. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d23b601d54df8246fbf8.webp` — ISTE Universidad
7. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d23b601d54df8246fbf7.png` — UAIII
8. `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6a04d23b8c6475e185e00d3e.png` — Sello EQS/IQS
