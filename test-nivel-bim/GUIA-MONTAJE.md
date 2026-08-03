# Guía de montaje — Test de Nivel BIM

Lead magnet interactivo que ubica a la persona en uno de los 4 niveles de la
ruta del Máster (Modelador · Coordinador · BIM Manager 4D-5D · Especialista
BIM+IA) y le dice qué competencias concretas le faltan para el siguiente.

> **Por qué esta herramienta:** el brochure del Máster (pág. 9) ya promete un
> «Test de Nivelación Gratuito». Hasta ahora esa promesa no tenía producto
> detrás. Esto lo es.

---

## URLs (una vez publicado)

| Pieza | URL |
|---|---|
| Landing de captura | `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/` |
| Página de gracias | `…/test-nivel-bim/gracias-agenda.html` |
| El test | `…/test-nivel-bim/app.html?acceso=dmbim26` |
| Versiones para GHL | `ghl-landing.html`, `ghl-gracias.html` y `ghl-test.html` (se pegan, no se enlazan) |

**El funnel vive entero bajo el dominio propio** — el usuario nunca ve github.io:

| Página | Ruta en GHL |
|---|---|
| 1 · landing | `funnel.dgdesignmodeling.com/test-nivel-bim` |
| 2 · gracias | `funnel.dgdesignmodeling.com/test-nivel-bim/gracias` |
| 3 · el test | `funnel.dgdesignmodeling.com/test-nivel-bim/test` (embebe la app por iframe) |

Solo las imágenes y la app se sirven desde GitHub Pages, embebidas.

**Token de acceso:** `dmbim26` — debe coincidir en `app.html`, `index.html` y
`gracias-agenda.html`. Cámbialo en los tres si quieres invalidar enlaces
compartidos.

---

## ⚠️ PASO 1 — Sin esto NO se captura ningún lead

Hoy `index.html` tiene vacías las dos constantes de GoHighLevel. **El test se
abre igual, pero nadie entra al CRM.** Hay que llenar una de las dos:

### Vía A — Formulario nativo de GHL (recomendada)

1. GHL → **Sites → Forms → New Form**. Nómbralo `Test de Nivel BIM - Registro`.
2. Campos: `Nombre`, `Email`, `Teléfono` y un desplegable `Perfil` con las
   mismas opciones de la landing (estudiante, arquitecto/a, ingeniero/a,
   modelador/a, coordinador/a, BIM Manager, otro).
3. En **Settings → On Submit → Redirect URL** pon:
   `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/test-nivel-bim/gracias-agenda.html?acceso=dmbim26`
4. Copia la URL de embed (`https://api.leadconnectorhq.com/widget/form/XXXX`).
5. Pégala en `index.html`:
   ```js
   const GHL_FORM_IFRAME_URL = 'https://api.leadconnectorhq.com/widget/form/XXXX';
   ```
6. Regenera la versión de GHL:
   ```bash
   python3 scripts/build_ghl_landing.py test-nivel-bim
   ```

Ventaja: los contactos llegan nativos al CRM y **no cuesta nada por ejecución**.

### Vía B — Inbound Webhook (respaldo)

Solo si por alguna razón no se puede usar el formulario nativo. ⚠️ El Inbound
Webhook de GHL es **prémium y cobra por ejecución**. Pega la URL en
`GHL_WEBHOOK_URL` y listo — el formulario propio de la landing la usará.

---

## PASO 2 — El funnel en GHL

1. **Sites → Funnels → New Funnel**: `Test de Nivel BIM`.
2. **Página 1** (`/test-nivel-bim`): elemento **Custom Code** a ancho completo
   y sin padding. Pega ahí el contenido de `ghl-landing.html`.
3. **Página 2** (`/test-nivel-bim/gracias`): pega **`ghl-gracias.html`** —
   esa, no `gracias-agenda.html`. La versión `ghl-` es la que lleva las rutas
   absolutas hacia el test; la otra apuntaría a un archivo que no existe
   dentro del dominio de GHL. Es a donde redirige el formulario.
4. **Página 3** (`/test-nivel-bim/test`): pega `ghl-test.html`. Es el test
   embebido. ⚠️ Ancho completo y **sin padding** — si la sección deja
   márgenes aparece una doble barra de scroll.
5. Publica las tres y prueba el recorrido completo en el móvil.

## PASO 3 — Membresía (opcional pero recomendado)

Para que el test viva también dentro del portal de alumnos:

1. **Memberships → Products → New**: `Test de Nivel BIM`.
2. Una lección con un elemento **iframe** apuntando a
   `…/test-nivel-bim/app.html?acceso=dmbim26`.
3. Crea una **oferta gratuita** del producto.
4. Workflow: **Form Submitted → Grant Offer**.

⚠️ Las dos causas típicas de «el portal se ve vacío»:
- No se publicó el **producto** (publicar la lección y la oferta no basta).
- No está habilitada la app de **Cursos** en el Client Portal.

## PASO 4 — Comunidades

En cada grupo de la comunidad: pestaña **Learning → vincular el curso**, y un
post de anuncio con el enlace de la landing (no el del test directo, para que
pase por la captura).

## PASO 5 — Bot de palabra clave IG/FB

Palabra clave: **NIVEL**. Mismo patrón que `BOT-ZAPATA-GHL.md`:

1. Disparadores: comentario en Instagram + comentario en Facebook, filtrados
   por que el texto contenga `NIVEL`.
2. Respuesta pública al comentario (varía el texto para no parecer bot).
3. **DM 1** con el enlace de la **landing** (no del test directo).
4. Espera 24 h → **DM 2** de calificación («¿qué nivel te salió?»).
5. Etiquetas: `lead-test-nivel` + `origen-bot-nivel`.
6. Notificación interna al equipo comercial.

⚠️ Respetar la ventana de 24 h de Meta para mensajes.

---

## Checklist E2E antes de anunciarlo

Recórrelo entero desde un teléfono que no sea el tuyo:

- [ ] 1. Comentar `NIVEL` en el post → llega el DM con el enlace
- [ ] 2. El enlace abre la landing y se ve bien en móvil
- [ ] 3. El formulario valida (probar con un correo mal escrito)
- [ ] 4. Al enviar, redirige a la página de gracias
- [ ] 5. El botón grande abre el test **sin candado**
- [ ] 6. Responder las 20 → sale nivel, brecha y siguiente paso
- [ ] 7. El contacto aparece en el CRM con su perfil
- [ ] 8. La oferta de membresía se otorgó y el login funciona
- [ ] 9. El calendario de la página de gracias carga y permite agendar
- [ ] 10. Borrar el contacto de prueba

---

## Mantenimiento

- **El contenido del test** (preguntas, bloques, textos de resultado) está en
  `app.html`, en las constantes `BLOQUES` y `NIVELES`. Si cambia el temario del
  Máster, se actualiza ahí.
- **La regla de nivel** está entre los marcadores `/* CALC-START */` y
  `/* CALC-END */`. Umbral de dominio: 70% por bloque; el nivel se cuenta de
  forma consecutiva desde el Bloque 1.
- **`ghl-landing.html` y `ghl-gracias.html` se generan** desde `index.html` y
  `gracias-agenda.html` con `python3 scripts/build_ghl_landing.py test-nivel-bim`
  — no editarlos a mano. El script aborta si alguna ruta relativa se le escapa,
  y reescribe los enlaces entre páginas al dominio propio (`RUTAS_FUNNEL`).
- **`ghl-test.html` sí se mantiene a mano** (es el envoltorio del iframe, no
  tiene fuente ni rutas relativas).
- Si cambian las rutas del funnel en GHL, actualizar `RUTAS_FUNNEL` en
  `scripts/build_ghl_landing.py` y regenerar.
- Para saltar la caché del CDN de GitHub Pages: añade `?v=2` a la URL.
