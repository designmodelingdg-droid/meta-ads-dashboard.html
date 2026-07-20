---
name: landing-agenda
description: |
  Genera la página "gracias + agenda" (thank-you page / booking page) que aparece después de que un prospecto llena el formulario en la landing de un producto DMA.
  
  Usa este skill cuando el usuario diga: "landing-agenda", "página de gracias", "thank you page", "pagina de agenda", "crear página de agenda", "generar la página de agendamiento", "página después del formulario", "página de confirmación con calendario", "segunda página del embudo", o cuando quiera la página que sigue después de la landing de un Máster, Diplomado o Certificación DMA. Úsalo proactivamente si el contexto indica que están construyendo un embudo de ventas DMA y ya tienen la landing principal lista.
---

# Skill: landing-agenda

Genera el HTML completo de la página de agradecimiento + calendario de agendamiento que sigue a la landing de producto de DMA.

## Qué hace esta página

1. **Hero "gracias"** — confirma que la solicitud fue recibida y explica que un asesor contactará por WhatsApp
2. **Tarjeta "qué sigue"** — pasos del proceso para el prospecto
3. **Widget de calendario GHL** — iframe de booking de GoHighLevel/LeadConnector para agendar sesión estratégica
4. **Footer** — branding DMA

## Flujo: recopila datos en 4 bloques

Pide la información en orden. Si el usuario no tiene algún dato, usa el valor predeterminado indicado.

---

### Bloque 1 — Producto y hero

| Dato | Placeholder | Ejemplo / Default |
|------|-------------|-------------------|
| Nombre corto del producto (para el H1 accent) | `{{HERO_ACCENT}}` | `Máster BIM Manager + IA` |
| Badge encima del hero | `{{BADGE_TEXT}}` | `Aplicación recibida` |
| Frase principal H1 (antes del accent) | `{{HERO_H1_PREFIX}}` | `¡Gracias por aplicar al` |
| Párrafo lead (confirmación breve) | `{{HERO_LEAD}}` | `Recibimos tu solicitud correctamente.` |
| Párrafo cuerpo (quién contactará y por dónde) | `{{HERO_BODY}}` | `Un asesor comercial del equipo Design Modeling te contactará por WhatsApp en breve para presentarte el programa en detalle y resolver tus dudas.` |
| Título de página (pestaña del navegador) | `{{META_TITLE}}` | `¡Gracias! · [Producto] · Design Modeling Academy` |
| Meta description | `{{META_DESCRIPTION}}` | Breve descripción para SEO interno |

---

### Bloque 2 — Tarjeta "qué sigue"

| Dato | Placeholder | Ejemplo / Default |
|------|-------------|-------------------|
| Título de la tarjeta | `{{WHATSNEXT_TITLE}}` | `Qué sigue ahora` |
| Texto explicativo de la tarjeta | `{{WHATSNEXT_BODY}}` | `Para que aproveches el tiempo, en lugar de esperar la llamada, puedes agendar tú mismo tu sesión estratégica con el equipo académico desde el calendario que verás abajo.` |
| Paso 1 | `{{STEP_1}}` | `Eliges día y horario en el calendario` |
| Paso 2 | `{{STEP_2}}` | `Recibes confirmación al instante por correo y WhatsApp` |
| Paso 3 | `{{STEP_3}}` | `El asesor académico te contactará 5 minutos antes de tu sesión` |

---

### Bloque 3 — Sección calendario

| Dato | Placeholder | Ejemplo / Default |
|------|-------------|-------------------|
| Label (etiqueta pequeña sobre el título) | `{{CALENDAR_LABEL}}` | `Agenda tu sesión` |
| Título del calendario H2 | `{{CALENDAR_H2}}` | `Reserva tu cupo en menos de 1 minuto` |
| Descripción del calendario | `{{CALENDAR_DESC}}` | `Sesión estratégica gratuita de 30 minutos. Te explicamos el programa, validamos tu perfil y resolvemos cualquier duda antes de tu admisión.` |
| URL del widget de booking GHL | `{{CALENDAR_URL}}` | `https://api.leadconnectorhq.com/widget/booking/XXXX` |
| URL del script embed de GHL | `{{CALENDAR_SCRIPT_URL}}` | `https://link.msgsndr.com/js/form_embed.js` |

**Cómo encontrar la URL del calendario en GHL:**
En GoHighLevel (Sharp CRM) → Calendarios → [tu calendario] → Compartir → copia el link del widget embed.
El iframe src será: `https://api.leadconnectorhq.com/widget/booking/{ID}`

---

### Bloque 4 — Footer

| Dato | Placeholder | Ejemplo / Default |
|------|-------------|-------------------|
| Nombre de la marca | `{{FOOTER_BRAND}}` | `Design Modeling Academy` |
| Descripción del footer (producto + avales) | `{{FOOTER_DESC}}` | `Máster Internacional BIM Manager + IA · Avalado por Sabal University y Doctrina Qualitas` |
| URL del sitio web | `{{FOOTER_URL}}` | `https://www.dgdesignmodeling.com` |
| Texto del link del sitio | `{{FOOTER_URL_TEXT}}` | `dgdesignmodeling.com` |

---

## Instrucciones de generación

1. Lee el template en `assets/template.html`
2. Sustituye cada `{{PLACEHOLDER}}` con el valor proporcionado por el usuario (o el default si no especifica)
3. Entrega el HTML completo en un bloque de código listo para copiar
4. Recuerda al usuario que lo pegue en Sharp CRM → Sites → Funnels → [su funnel] → segunda página → Custom Code, o en la URL de redirección del formulario de la landing

## Notas de uso

- La página tiene `<meta name="robots" content="noindex, nofollow">` — es intencional para que no aparezca en Google
- El script `form_embed.js` de GHL es necesario para el widget de booking; está incluido en el template
- Si el usuario tiene otro calendario (Calendly, Google Calendar, iCloud), se puede cambiar el iframe src; ajusta también el script si es necesario
- Los colores y fuentes (Overpass + Nunito, azul #003e5c, naranja #ca7520, navy #001e30) son el brandkit DMA y no deben cambiarse
