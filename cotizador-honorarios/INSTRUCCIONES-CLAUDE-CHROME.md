# Instrucciones para el Claude del navegador — montaje en GoHighLevel

> **Cómo usar este archivo:** pégaselo completo al Claude de Chrome. Está
> escrito para que lo ejecute él directamente en la cuenta de GHL de Design
> Modeling. No hace falta pasarle ningún archivo: copia cada HTML desde las
> URLs de la tabla de abajo.

---

## Contexto

Vas a montar en GoHighLevel el funnel de un lead magnet ya construido y
probado: el **Cotizador de Honorarios Estructurales** de Design Modeling
Academy. La herramienta ya está publicada y funcionando. Tu trabajo es **solo
la parte de GHL**: el formulario, las dos páginas del funnel, el workflow de
etiquetas, la tarjeta en la página de recursos y, opcionalmente, la membresía.

**Todo tiene que verse bajo el dominio de Dayana** (`funnel.dgdesignmodeling.com`).
La herramienta en sí se sigue sirviendo desde GitHub Pages.

**No hay que escribir ni modificar código HTML.** Los archivos se pegan tal
cual en contenedores de Custom Code.

**La palabra clave COTIZA en Instagram (OpenReply) NO es parte de este
encargo:** se monta después de publicar el reel y el carrusel.

### Datos fijos que vas a necesitar

| Dato | Valor |
|---|---|
| Token de acceso | `dm2026` |
| **Página 1** · landing | `https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form` |
| **Página 2** · gracias | `https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-gracias` |
| La herramienta (no se monta, ya existe) | `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/app.html?acceso=dm2026` |
| Página de recursos (ya existe) | `https://funnel.dgdesignmodeling.com/recursos` |
| Imagen de la tarjeta y para compartir | `https://assets.cdn.filesafe.space/nkKbOarn5IwHeMv48uY9/media/6abd2bf5568b00dcf9fec8e1.png` |
| Calendario de agenda (ya embebido en la gracias) | `https://api.leadconnectorhq.com/widget/booking/bIVuNHNojGEgH3gf6yXe` |

⚠️ **Las rutas de las dos páginas tienen que ser exactamente esas.** La landing
ya redirige a la gracias con esa URL, y la tarjeta de la página de recursos ya
enlaza a la landing con la suya. Si cambias una ruta, se rompe el recorrido.

### De dónde copias cada HTML

Ábrelas en una pestaña normal: se muestran como **texto plano**. Seleccionas
todo (Ctrl/Cmd + A), copias y pegas.

| Qué | URL para copiar el HTML |
|---|---|
| 1 · landing | `https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/gh-pages/cotizador-honorarios/ghl-landing.html` |
| 2 · gracias | `https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/gh-pages/cotizador-honorarios/ghl-gracias.html` |
| Página de recursos completa | `https://raw.githubusercontent.com/designmodelingdg-droid/meta-ads-dashboard.html/gh-pages/recursos/ghl-recursos.html` |

Antes de pegar, comprueba que lo copiado empieza por `<style>` y termina en
`</script>`. Si no, se copió a medias.

---

## PASO 1 · Formulario

1. Ve a **Sites → Forms → Builder**. Busca `Calculadora de Zapatas - Registro`
   y **duplícalo** (así hereda el estilo y la configuración de la cuenta).
2. Nómbralo exactamente: `Cotizador de Honorarios - Registro`
3. Deja estos campos, todos **obligatorios**:
   - `Nombre` (First Name / texto)
   - `Email`
   - `Teléfono` (phone)
   - `¿Cómo trabajas hoy?` — **desplegable** con estas 6 opciones, escritas
     igual y en este orden:
     - Ingeniero independiente: cotizo mis proyectos
     - Trabajo en empresa y cotizo proyectos aparte
     - Tengo una empresa de diseño o construcción
     - Arquitecto
     - Estudiante
     - Otro

   Si en la cuenta no existe un campo personalizado para esa pregunta, créalo
   (tipo *Single Options / Dropdown*) con ese mismo nombre.
4. Texto del botón: `Calcular mi precio real`
5. **Settings → On Submit → Redirect to URL**, exactamente:
   ```
   https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-gracias
   ```
6. Guarda. Luego **Integrate Form → Embed** y copia la URL del iframe, que se
   ve así: `https://api.leadconnectorhq.com/widget/form/XXXXXXXXXXXX`

**➡️ Repórtale esa URL a Dayana.** Se pega en el repositorio y la landing pasa
a usar este formulario. **Mientras tanto la landing ya funciona** con su
formulario propio, que manda cada lead a GHL por el Inbound Webhook de
siempre (el de la Calculadora de Zapatas) con el dato
`fuente: cotizador-honorarios`. No hace falta esperar esto para seguir.

---

## PASO 2 · El funnel de dos páginas

1. **Sites → Funnels**. Busca el funnel de la **Calculadora de Zapatas** y
   **duplícalo**, o crea uno nuevo con **+ New Funnel**. Nombre:
   `Cotizador de Honorarios`.
2. **Página 1** · ruta exacta `acceso-gratis-cotizador-honorarios-form`:
   - Borra lo que traiga la página duplicada.
   - Añade una sección de **ancho completo**, sin padding arriba, abajo ni a
     los lados.
   - Dentro, un elemento **Custom Code / HTML** a ancho completo.
   - Pega **todo** `ghl-landing.html` (URL en la tabla de arriba).
   - **Settings → SEO**:
     - Título: `Cotizador de Honorarios Estructurales gratis · Design Modeling Academy`
     - Descripción: `¿Cuánto cobras de verdad por hora cuando cobras por m²? Calcula tu tarifa mínima, las horas del proyecto y arma la propuesta en PDF con los impuestos de tu país. Gratis.`
     - Imagen para compartir: la de la tabla de datos fijos.
3. **Página 2** · ruta exacta `acceso-gratis-cotizador-honorarios-gracias`:
   - Mismo procedimiento con **todo** `ghl-gracias.html`.
   - Trae el calendario de agenda ya embebido: comprueba que carga.
   - Si GHL tiene la opción, márcala como no indexable (*noindex*).
4. Si GHL añade cabecera o pie propios a las páginas, quítalos: el HTML ya
   trae los suyos.
5. **Publica las dos** y ábrelas desde un celular. No debe haber scroll
   horizontal ni márgenes blancos a los lados.

---

## PASO 3 · Workflow de etiquetas

1. **Automation → Workflows**. Duplica el workflow de etiquetas de la
   Calculadora de Zapatas, o crea uno nuevo llamado
   `Lead magnet · Cotizador de Honorarios`.
2. **Disparadores** (pon los dos, así cubre el formulario propio y el nativo):
   - `Form Submitted` → formulario `Cotizador de Honorarios - Registro`.
   - `Inbound Webhook` → el mismo webhook que usa zapatas, con el filtro
     `fuente` **es igual a** `cotizador-honorarios`.

     ⚠️ No cambies el workflow de zapatas que ya usa ese webhook: crea uno
     aparte con este filtro, para que los leads de zapatas no reciban las
     etiquetas del cotizador.
3. **Acciones**:
   - Crear o actualizar el contacto con nombre, correo, teléfono y la
     respuesta de «¿Cómo trabajas hoy?» (en el webhook viene como `perfil`).
   - Etiquetas: `lead-cotizador` y `origen-landing-cotizador`.
   - Notificación interna al equipo de ventas: «Nuevo lead del Cotizador de
     Honorarios: {{contact.name}} · {{contact.phone}}».
4. **No añadas** correos ni WhatsApp automáticos en este paso: los decide
   Dayana aparte.
5. Publica el workflow.

---

## PASO 4 · Página de recursos

⚠️ **Hazlo solo cuando la página 1 del paso 2 esté publicada.** La tarjeta
nueva enlaza a esa URL; si no existe todavía, lleva a un 404.

1. **Sites → Funnels/Websites →** la página
   `https://funnel.dgdesignmodeling.com/recursos`.
2. Abre el elemento **Custom Code** que ya tiene y **reemplaza todo su
   contenido** por `ghl-recursos.html` (URL en la tabla de arriba).
   No se añade una tarjeta a mano: el archivo nuevo ya la trae.
3. Guarda y publica.
4. Comprueba en el celular:
   - en «Herramientas gratuitas» hay **cuatro** tarjetas y la primera es
     **Cotizador de Honorarios Estructurales**, con la etiqueta «Nuevo» y la
     imagen del cotizador;
   - las otras tres (Test de Nivel BIM, 5 verificaciones en acero,
     Calculadora de Zapatas) siguen igual;
   - al tocar la del cotizador se abre la landing del paso 2.

---

## PASO 5 · Membresía (opcional, recomendado)

Para que el cotizador también viva dentro del portal de alumnos:

1. **Memberships → Products → + Create Product**: `Cotizador de Honorarios`.
2. Crea una categoría y dentro una lección: `Calcula tu precio real`.
3. En la lección, un elemento **iframe** con esta URL:
   ```
   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/app.html?acceso=dm2026
   ```
   Altura sugerida: 1600 px.
4. Crea una **Offer** del producto, tipo **Free**.
5. En el workflow del paso 3, añade al final la acción `Grant Offer` con esa
   oferta.

⚠️ Las dos causas típicas de «el portal se ve vacío»:
- No se publicó el **producto** (publicar solo la lección y la oferta no basta).
- No está habilitada la app de **Courses / Cursos** en el Client Portal.

---

## PASO 6 · Solo cuando Dayana avise que se publicó el reel · Facebook

La palabra **COTIZA** en Instagram la monta Patricio en OpenReply después de
publicar. Lo que sí es de GHL es la respuesta en **Facebook**:

1. Duplica el workflow de comentarios de **ZAPATA** y nómbralo
   `Comentario COTIZA`.
2. Disparador: comentario en **Facebook**, con el filtro de que el texto
   **contenga** `COTIZA`.
3. **Respuesta pública al comentario, siempre con el enlace** (alterna 3
   versiones para que no parezca bot):
   - «¡Listo! Aquí lo tienes: https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form 🙌»
   - «Te lo dejo aquí mismo 👉 https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form»
   - «Aquí está el cotizador gratis: https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form»
4. **DM por Facebook Messenger** (acción propia de ese canal, no compartida
   con Instagram):
   > ¡Hola! Aquí tienes el Cotizador de Honorarios Estructurales: calcula tu tarifa mínima por hora, las horas del proyecto y te arma la propuesta en PDF con los impuestos de tu país. 👉 https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form
5. Etiquetas: `lead-cotizador` y `origen-bot-cotiza`. Notificación interna.

⚠️ **Incidente conocido (julio de 2026, unos 35 leads perdidos):** cuando el
post sale de Instagram y se replica en Facebook, la gente comenta en la copia
de Facebook. Si la acción de DM está atada solo a Instagram, falla en
silencio. Por eso la respuesta pública **siempre lleva el enlace**, y el DM de
Facebook va por Messenger en su propia acción.

**Prueba:** comenta `COTIZA` desde una cuenta que no sea la de la academia en
la copia de Facebook del post publicado, y confirma que llegan la respuesta
pública y el DM.

---

## Checklist final — recórrelo entero antes de dar por terminado

Hazlo desde un teléfono o una ventana de incógnito, no desde la sesión donde
estuviste configurando:

- [ ] 1. La landing del funnel abre y se ve bien en el celular.
- [ ] 2. El formulario rechaza un correo mal escrito.
- [ ] 3. Al enviarlo bien, redirige a la página de gracias del funnel.
- [ ] 4. El botón «Abrir mi cotizador» abre la herramienta **sin candado**.
- [ ] 5. En la herramienta, el resultado de ejemplo dice «14,71 USD por hora»
        y el botón «Descargar la propuesta en PDF» abre la vista de impresión.
- [ ] 6. El contacto aparece en **Contacts** con nombre, correo, teléfono,
        su respuesta de «¿Cómo trabajas hoy?» y la etiqueta `lead-cotizador`.
- [ ] 7. El calendario de la gracias carga y deja agendar.
- [ ] 8. En `/recursos` la primera tarjeta es la del cotizador y abre la landing.
- [ ] 9. Si hiciste el paso 5: la oferta se otorgó y el portal muestra la lección.
- [ ] 10. **Borra el contacto de prueba** del CRM.

---

## Qué reportar de vuelta

1. La **URL de embed del formulario** (paso 1).
2. Las **URLs finales** de las dos páginas publicadas, y confirmación de que
   `/recursos` quedó actualizada.
3. El nombre del workflow creado y sus disparadores.
4. Cualquier punto del checklist que **no** haya pasado, con lo que viste.

> Si algo no coincide con estas instrucciones (nombres de menú distintos,
> opciones que no aparecen), **no improvises con el código HTML**: repórtalo
> y se ajusta desde el repositorio.
