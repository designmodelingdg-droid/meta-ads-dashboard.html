# Bot "ZAPATA" — flujo de Instagram/Facebook en GHL + prueba end-to-end

Configuración del flujo que responde a los comentarios con la palabra
**ZAPATA** en Instagram y Facebook, y checklist de la prueba completa del
funnel. Los textos están listos para copiar y pegar.

---

## 1. Workflow "Bot ZAPATA — IG/FB" (Automation → Workflows → Create)

> Requisito: Instagram y la página de Facebook deben estar conectados en
> **Settings → Integrations** de la subcuenta.

### Disparadores (agrega los 2 al mismo workflow)

1. **Instagram → Comment on Post** — filtro: el comentario **contiene** `zapata`
   (sin mayúsculas; GHL no distingue). Alcance: todos los posts, o limita al
   post/reel del lead magnet cuando esté publicado.
2. **Facebook → Comment on Post** — mismo filtro.

### Acciones, en este orden

**Paso 1 · Responder al comentario (público)** — acción "Reply in Comment":

> ¡Te lo mandé por DM! 📩 Revisa tus mensajes 🧱

**Paso 2 · DM #1 — entrega del enlace** — acción "Send DM" (IG) / "Messenger" (FB):

> ¡Hola! 👋 Soy del equipo de Design Modeling Academy.
>
> Aquí está tu acceso a la **Calculadora de Zapatas GRATIS** 🧱
> 👉 https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/
>
> Regístrate (20 segundos) y la usas de inmediato desde el celular:
> dimensiones, verificaciones y acero de tu zapata en 2 minutos.

*(Cuando la landing esté en el funnel de GHL, cambiar por la URL de
`funnel.dgdesignmodeling.com`.)*

**Paso 3 · Espera** — acción "Wait": 2 minutos (o "hasta respuesta del contacto",
lo que ocurra primero).

**Paso 4 · DM #2 — calificación** — "Send DM":

> Mientras la pruebas, cuéntame algo para ayudarte mejor 🙂
> ¿A qué te dedicas?
>
> 1️⃣ Estudiante de ingeniería/arquitectura
> 2️⃣ Ingeniero(a) o arquitecto(a) independiente
> 3️⃣ Trabajo en constructora/consultora
> 4️⃣ Docente

**Paso 5 · Etiquetas** — acción "Add Tag": `lead-calculadora-zapatas` +
`origen-bot-zapata` (para distinguirlos de los que llegan directo a la landing).

**Paso 6 · Notificación interna** — acción "Internal Notification" al asesor
(coordinar con **Pato** quién la recibe): "Nuevo lead del bot ZAPATA respondió
la calificación — revisar conversación".

### Rama de seguimiento (coordinar con Pato)

- Si el contacto **responde 2 o 3** (independiente/constructora): son los de
  mayor intención → seguimiento humano con invitación a la **sesión
  estratégica** (la misma agenda de la página de gracias).
- Si responde 1 o 4: entra a la secuencia de nutrición normal.
- ⚠️ Regla de Meta: los DMs deben enviarse dentro de la **ventana de 24 h**
  tras la interacción; el seguimiento posterior va por email/WhatsApp con los
  datos que dejó en el formulario.

---

## 2. Prueba end-to-end (checklist)

Hacerla con un usuario/correo de prueba real, en este orden:

1. [ ] Comentar `ZAPATA` en un post de prueba de IG → llega respuesta pública + DM #1 con el enlace.
2. [ ] Esperar el DM #2 (pregunta de calificación) y responder → se agregan las etiquetas y llega la notificación interna.
3. [ ] Abrir la landing del DM → se ve el diseño DMA y el **formulario nativo** "Calculadora de Zapatas - Registro".
4. [ ] Enviar el formulario → redirige a la **página de gracias**.
5. [ ] En la página de gracias: el botón **"ABRIR MI CALCULADORA AHORA"** abre la calculadora **sin candado**, y el calendario de booking carga y permite agendar.
6. [ ] En GHL → Contacts: el contacto de prueba existe con nombre, email, teléfono y perfil; con la etiqueta del formulario.
7. [ ] El workflow "Calculadora Zapatas - Acceso Membresía" se ejecutó → el contacto recibió la **oferta del curso** (revisar en Membresías → Miembros) y el email de credenciales del portal.
8. [ ] Iniciar sesión en el portal como el usuario de prueba → la lección muestra la calculadora embebida y funcional (probar un cálculo).
9. [ ] Agendar una sesión de prueba en el calendario → la cita aparece en el calendario del equipo.
10. [ ] Borrar/archivar el contacto y la cita de prueba.

Si el punto 5 falla con candado: el iframe/botón debe usar la URL con
`?acceso=dm2026`. Si el calendario no carga: autorizar el dominio del widget
en la configuración del calendario de GHL.
