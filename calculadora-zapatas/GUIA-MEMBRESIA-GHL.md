# Guía: montar la Calculadora de Zapatas dentro de GoHighLevel

Guía paso a paso para que TÚ montes todo dentro de GHL (Sharp CRM):
la landing con formulario, y la calculadora como producto de membresía
con inicio de sesión. Todo referenciado a tu CRM.

---

## 0. Qué está hecho y qué falta (mapa rápido)

| Pieza | Estado | Quién |
|---|---|---|
| Calculadora funcionando en línea | ✅ Publicada en GitHub Pages | Hecho |
| Landing publicada (diseño DMA) con formulario | ✅ En línea, enviando leads a tu webhook | Hecho |
| Copia de la landing lista para pegar en GHL | ✅ `ghl-landing.html` en el repo | Hecho |
| Mapeo del webhook en GHL (o cambio a form nativo) | ⚠️ Pendiente | Tú (5 min) |
| Landing dentro de tu funnel de GHL | ⚠️ Pendiente | Tú (10 min) |
| Membresía con la calculadora embebida | ⚠️ Pendiente | Tú (15 min) |

**URLs fijas que vas a usar:**

- Calculadora: `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/app.html`
- Con acceso directo (para iframe/membresía): agrega `?acceso=dm2026` al final.
- Landing pública: `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/`

---

## 1. El formulario: cómo llegan los contactos a GHL (elige UNA vía)

### Vía A — La que está activa hoy: webhook

El formulario de la landing ya envía cada registro a tu workflow
"Webhook Entrante". Para que se conviertan en contactos:

1. Abre la landing publicada y **envía tú mismo un registro de prueba**
   (nombre, correo, WhatsApp y "¿A qué te dedicas?"). Esto es lo que GHL
   está esperando — por eso te dice "No hemos recibido ninguna solicitud".
2. Vuelve al disparador → **Referencia de mapeo → "Buscar nuevas
   solicitudes"** → selecciona la petición que acaba de llegar.
3. Guarda el trigger, agrega la acción **Create/Update Contact** mapeando
   `nombre` → Full Name, `email` → Email, `telefono` → Phone y `perfil` →
   campo personalizado. Añade la etiqueta `lead-calculadora-zapatas`.
4. **Publica el workflow** y encadena tu bot de seguimiento.

> ⚠️ Ojo: GHL te avisó que el Inbound Webhook es un **activador prémium
> con cargo por ejecución**. Si prefieres no pagar por lead, usa la Vía B.

### Vía B — Recomendada si montas todo en GHL: formulario nativo (gratis)

1. En GHL: **Sites → Forms → Builder → Add Form**. Campos: Nombre completo,
   Email, Teléfono, y un campo desplegable "¿A qué te dedicas?" (Estudiante /
   Independiente / Constructora / Docente / Otro).
2. En opciones del formulario → **On Submit → Redirect to URL**:
   `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/app.html?acceso=dm2026`
3. Los contactos llegan **directo a tu CRM sin webhook ni cargos**, y ahí
   mismo puedes dispararles un workflow normal (trigger "Form Submitted").
4. Pásale la URL del formulario (o su Form ID) a Claude para que la deje
   conectada en la landing (`GHL_FORM_IFRAME_URL` en `index.html` y
   `ghl-landing.html`), o pégala tú en esa constante: el formulario nativo
   reemplaza automáticamente al formulario propio de la página.

---

## 2. Montar la landing dentro de tu funnel de GHL

1. En GHL: **Sites → Funnels → New Funnel** (ej. "Calculadora de Zapatas").
2. Crea el **Paso 1** ("calculadora-zapatas") y abre el editor de la página.
3. Añade una **sección de ancho completo** (full width, sin padding) y dentro
   un elemento **Custom Code / HTML**.
4. Abre el archivo `calculadora-zapatas/ghl-landing.html` del repositorio
   (o pídeselo a Claude), **copia TODO su contenido y pégalo** en el elemento.
5. Guarda y publica. La página ocupa todo el ancho, con tu navbar, marquee
   de avales, formulario y footer DMA.
6. Si elegiste la Vía B del formulario, reemplaza antes la constante
   `GHL_FORM_IFRAME_URL = ''` (al final del código) por la URL de tu
   formulario nativo.

Con esto tu landing vive en `funnel.dgdesignmodeling.com` con tu dominio.
La de GitHub Pages puede seguir viva como respaldo o para tráfico directo.

---

## 3. Montar la calculadora como PRODUCTO de membresía (con login)

Objetivo: que el cliente inicie sesión en tu portal de GHL, quede siempre
registrado en el CRM, y la calculadora viva como un producto de tu comunidad.

1. En GHL: **Memberships → Courses → Products → Create Product**
   (ej. "Calculadora de Zapatas · Herramienta DMA"). Plantilla en blanco,
   una sola categoría/lección: "Tu calculadora".
2. En la lección, agrega la descripción y en el editor pega este código
   (usa el widget **Custom Code / HTML** si tu builder lo tiene, o el modo
   "código fuente" del editor de texto):

   ```html
   <iframe
     src="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/app.html?acceso=dm2026"
     style="width:100%;min-height:1700px;border:none;border-radius:12px"
     title="Calculadora de Zapatas · Design Modeling Academy">
   </iframe>
   ```

   > El `?acceso=dm2026` abre la calculadora ya desbloqueada: el candado
   > no molesta a tus miembros (la membresía ya hace el control de acceso).

3. Crea la **Offer**: Memberships → Offers → New Offer → agrega el producto
   → precio **Free** (es lead magnet) → guarda y publica.
4. Conecta la entrega automática: en el workflow del lead (webhook o form),
   añade la acción **Membership Grant Offer** → tu oferta. GHL crea el
   usuario del portal y le envía sus credenciales solo.
5. El cliente entra por tu portal (ej. `portal.dgdesignmodeling.com` o la
   URL del client portal), inicia sesión, y abre la calculadora. Cada
   acceso queda ligado a su contacto en el CRM.

### ¿Por qué iframe y no pegar el código de la calculadora?

Porque la calculadora "fuente" vive en GitHub Pages: cualquier mejora
(nuevos tipos de zapata, correcciones) se publica una vez y **se refleja
sola** en la membresía, el funnel y el enlace público. Si pegaras el código
dentro de GHL, tendrías que actualizarlo a mano en cada lugar.

---

## 4. Checklist final

- [ ] Registro de prueba enviado desde la landing publicada
- [ ] Webhook mapeado y workflow publicado (o formulario nativo conectado)
- [ ] Landing pegada en el funnel de GHL (`ghl-landing.html`)
- [ ] Producto de membresía creado con el iframe
- [ ] Offer gratuita + acción "Membership Grant Offer" en el workflow
- [ ] Prueba completa: registro → contacto en CRM → acceso al portal → calculadora
