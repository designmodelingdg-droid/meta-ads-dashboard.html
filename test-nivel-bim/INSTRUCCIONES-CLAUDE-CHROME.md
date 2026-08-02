# Instrucciones para el Claude del navegador — montaje en GoHighLevel

> **Cómo usar este archivo:** pégaselo completo al Claude de Chrome junto con
> los archivos `ghl-landing.html` y `gracias-agenda.html`. Está escrito para
> que lo ejecute él directamente en la cuenta de GHL de Design Modeling.

---

## Contexto

Vas a montar en GoHighLevel el funnel de un lead magnet ya construido y
probado: el **Test de Nivel BIM** de Design Modeling Academy. El test ya está
publicado y funcionando en GitHub Pages — tu trabajo es **solo la parte de
GHL**: el formulario, las dos páginas del funnel y la membresía.

**No hay que escribir ni modificar código HTML.** Los dos archivos que
recibes se pegan tal cual en contenedores de Custom Code.

### Datos fijos que vas a necesitar

| Dato | Valor |
|---|---|
| Token de acceso | `dmbim26` |
| URL del test | `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/app.html?acceso=dmbim26` |
| URL de la landing publicada | `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/` |
| URL de la página de gracias publicada | `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/gracias-agenda.html` |
| Calendario de agenda (ya embebido) | `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe` |

---

## PASO 1 · Crear el formulario (lo más importante)

Sin esto el test funciona pero **ningún contacto entra al CRM**.

1. Ve a **Sites → Forms → Builder → + Add Form**.
2. Nómbralo exactamente: `Test de Nivel BIM - Registro`
3. Agrega estos campos, todos **obligatorios**:
   - `Nombre` (First Name / texto)
   - `Email` (email)
   - `Teléfono` (phone)
   - `Perfil` — **desplegable** con estas 7 opciones, en este orden:
     - Estudiante de arquitectura o ingeniería
     - Arquitecto/a
     - Ingeniero/a civil o estructural
     - Modelador/a BIM
     - Coordinador/a BIM
     - BIM Manager
     - Otro
4. Texto del botón: `Entrar al test →`
5. En **Settings → On Submit** elige **Redirect to URL** y pon exactamente:
   ```
   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/gracias-agenda.html?acceso=dmbim26
   ```
6. Guarda e **Integrate Form → Embed**. Copia la URL del iframe: se ve como
   `https://api.leadconnectorhq.com/widget/form/XXXXXXXXXXXX`

**➡️ Repórtale a Dayana esa URL.** Hay que pegarla en el repositorio
(`test-nivel-bim/index.html`, constante `GHL_FORM_IFRAME_URL`) y regenerar la
versión de GHL. Hasta que eso pase, la landing usa su formulario propio de
respaldo, que **no guarda nada en el CRM**.

---

## PASO 2 · El funnel de dos páginas

1. **Sites → Funnels → + New Funnel**, nómbralo `Test de Nivel BIM`.
2. **Página 1** — ruta `/test-nivel-bim`:
   - Añade una sección de **ancho completo**, sin padding lateral.
   - Dentro, un elemento **Custom Code / HTML**.
   - Pega ahí **todo el contenido del archivo `ghl-landing.html`**.
   - Importante: el elemento debe ocupar el 100% del ancho y la sección no
     debe tener márgenes, o el diseño se ve encajonado.
3. **Página 2** — ruta `/test-nivel-bim/gracias`:
   - Mismo procedimiento con **`gracias-agenda.html`**.
   - Esta página tiene el calendario de agenda ya embebido; verifica que carga.
4. **Publica ambas páginas** y ábrelas desde un móvil para revisar que se ven
   bien (el diseño es responsive, no debería haber scroll horizontal).

---

## PASO 3 · Membresía (opcional, recomendado)

Para que el test también viva dentro del portal de alumnos:

1. **Memberships → Products → + Create Product**: `Test de Nivel BIM`.
2. Crea una categoría y dentro una lección: `Haz tu test`.
3. En la lección, un elemento **iframe** con esta URL:
   ```
   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/app.html?acceso=dmbim26
   ```
   Altura sugerida: 1200 px.
4. Crea una **Offer** del producto, tipo **Free**.
5. **Automation → Workflows → + Create**: disparador `Form Submitted`
   (el formulario del paso 1) → acción `Grant Offer` (la oferta gratuita).

⚠️ **Las dos causas típicas de "el portal se ve vacío":**
- No se publicó el **producto** (publicar solo la lección y la oferta no basta).
- No está habilitada la app de **Courses / Cursos** en el Client Portal.

Revisa las dos antes de dar el paso por terminado.

---

## PASO 4 · Comunidades

En cada grupo de la comunidad:
1. Pestaña **Learning → vincular el curso** `Test de Nivel BIM`.
2. Publica un post de anuncio con **el enlace de la landing** (no el del test
   directo — queremos que pase por la captura). El texto sugerido está en
   `matriz-viral/BRIEF-TEST-NIVEL-BIM.md`, sección 9.

---

## PASO 5 · Bot de palabra clave (si Dayana lo confirma)

Palabra clave: **NIVEL**. Mismo patrón que el bot `ZAPATA` que ya existe en la
cuenta (ver `calculadora-zapatas/BOT-ZAPATA-GHL.md` como referencia).

1. Workflow con dos disparadores: comentario en **Instagram** y comentario en
   **Facebook**, ambos filtrados por que el texto contenga `NIVEL`.
2. Responder públicamente al comentario (varía el texto entre 3-4 versiones
   para que no parezca bot).
3. **DM 1** con el enlace de la **landing**.
4. Espera 24 h → **DM 2** de calificación: «¿qué nivel te salió?».
5. Etiquetas al contacto: `lead-test-nivel` y `origen-bot-nivel`.
6. Notificación interna al equipo comercial.

⚠️ Respeta la ventana de 24 horas de Meta para mensajes fuera de la
conversación.

---

## Checklist final — recórrelo entero antes de dar por terminado

Hazlo desde un teléfono o una ventana de incógnito, no desde la sesión donde
estuviste configurando:

- [ ] 1. La landing del funnel abre y se ve bien en móvil
- [ ] 2. El formulario rechaza un correo mal escrito
- [ ] 3. Al enviarlo correctamente, redirige a la página de gracias
- [ ] 4. El botón grande de la página de gracias abre el test **sin candado**
- [ ] 5. Se pueden responder las 20 preguntas y sale el resultado con nivel,
        brecha y siguiente paso
- [ ] 6. El contacto aparece en **Contacts** con su nombre, correo, teléfono y
        el campo Perfil relleno
- [ ] 7. La oferta de membresía se otorgó y el acceso al portal funciona
- [ ] 8. El calendario de la página de gracias carga y permite agendar
- [ ] 9. **Borra el contacto de prueba** del CRM

---

## Qué reportar de vuelta

1. La **URL de embed del formulario** (paso 1) — es lo que falta en el código.
2. Las **URLs finales** de las dos páginas del funnel ya publicadas.
3. Cualquier punto del checklist que **no** haya pasado, con lo que viste.
4. Si activaste el bot: confirmación de que el DM llega.

> Si algo no coincide con estas instrucciones (nombres de menú distintos,
> opciones que no aparecen), **no improvises con el código HTML** — repórtalo
> y que se ajuste desde el repositorio.
