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

> ⚠️ **INCIDENTE CONOCIDO (18-jul-2026) — leer antes de montar el workflow:**
> cuando un post es de **origen Instagram y se muestra también en Facebook**
> ("cross-post"), la gente puede comentar **en la copia de Facebook**. Si el
> paso de "Send DM" del workflow está atado al canal de **Instagram** (porque
> el post "es de Instagram"), el mensaje se intenta enviar al ID equivocado
> (la persona comentó como usuario de Facebook, no de Instagram) y **falla en
> silencio**: el workflow marca el paso como ejecutado, la respuesta pública
> sí sale, pero el DM nunca llega. Así perdimos ~35 leads del primer post.
> **Mitigación obligatoria** (las dos, no una sola):
> 1. Separa la acción de envío por rama: el disparador de Instagram debe
>    enviar el DM por el canal de **Instagram**, y el disparador de Facebook
>    por **Facebook Messenger** — nunca una sola acción de "Send DM"
>    compartida entre ambos disparadores.
> 2. La respuesta pública (Paso 1 abajo) debe **incluir siempre el enlace
>    directo**, nunca solo "te escribí al DM" — así, aunque el canal del DM
>    falle, el lead igual recibe el acceso. Es la red de seguridad real.
> 3. Antes de lanzar cualquier post, **prueba con un comentario real en la
>    copia de Facebook del post** (no solo en Instagram) — es el caso que
>    falló y el que hay que confirmar que funciona.

### Acciones, en este orden

**Paso 1 · Responder al comentario (público)** — acción "Reply in Comment".
Incluye el enlace directo en la respuesta pública (no solo avisar que se
mandó el DM — ver incidente arriba):

> ¡Aquí tienes tu acceso directo! 🧱 Y por si acaso, también te escribí al DM 📩
> https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/calculadora-zapatas/

**Paso 2 · DM #1 — entrega del enlace** — acción "Send DM" (IG) / "Messenger" (FB).
Configura esta acción **por separado para cada disparador** (una rama para
Instagram → envío por Instagram; otra para Facebook → envío por Facebook
Messenger), nunca una sola acción compartida:

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

Hacerla con un usuario/correo de prueba real, en este orden. **Repetir los
puntos 1-2 dos veces: una comentando en Instagram y otra comentando en la
copia de Facebook del mismo post** (ver incidente de arriba — son canales de
envío distintos y uno puede funcionar mientras el otro falla en silencio).

1. [ ] Comentar `ZAPATA` en Instagram → llega respuesta pública **con el enlace visible** + DM #1 (verificar que el DM llegó de verdad, no solo que el paso "se marcó ejecutado").
1b. [ ] Comentar `ZAPATA` en la copia de Facebook del mismo post → mismo resultado: respuesta pública con enlace + DM #1 confirmado.
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
