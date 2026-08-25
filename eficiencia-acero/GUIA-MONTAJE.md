# Montaje en GHL — «Las 5 verificaciones en acero»

**Para la sesión de Claude Code del Mac, con browser-harness.**
Todo lo que va aquí ya está construido y publicado. Esto es solo el montaje
dentro de GoHighLevel, que es lo único que no se puede hacer desde el
repositorio: su API v2 tiene tres `GET` para Funnels y Sites, y nada de
escritura.

---

## Lo que ya existe

Publicado en GitHub Pages en cuanto se fusione la rama:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/eficiencia-acero/
  index.html           landing de captura
  guia.html            la guía, 5 verificaciones con norma citada
  app.html             el verificador de eficiencia
  gracias-agenda.html  página de gracias con los dos accesos + calendario
```

| | |
|---|---|
| Palabra del bot | `ACERO` |
| Token de acceso | `dm2026` (igual que zapatas y test — mismo esquema) |
| Piezas de la matriz que cubre | `ago-acero-conexiones` (Mié 20) · `ago-blog-acero-verificaciones` (Sáb 23) · `ago-acero-sobredimensionado` (Mié 27) |

---

## Paso 1 · El formulario

**No crear uno nuevo si ya existe el de lead magnets con el campo de perfil.**
Ester lo subió a los siete formularios el 25-ago; reutilizar ese esquema.

Campos: nombre, correo, WhatsApp y **¿Cuál es tu perfil actualmente?**
(desplegable único, obligatorio, mapeado al campo personalizado del contacto
`{{contact.cul_es_tu_perfil_actualmente}}` — ojo, la clave lleva `cul_`, no
`cual_`; GHL se comió la tilde al generarla, y escribirla bien no da error:
sale vacío).

Al terminar, el formulario **redirige** a la página de gracias.

Cuando exista, hay que pegar su URL en `index.html`:

```js
const GHL_FORM_IFRAME_URL = '';   // ← aquí va la URL del form nativo
```

Con eso el formulario nativo de GHL reemplaza al propio y el contacto entra
al CRM directo, sin webhook y sin costo por ejecución.

> `GHL_WEBHOOK_URL` se deja **vacío a propósito**. El Inbound Webhook de GHL
> es premium y cobra por ejecución. Con el formulario nativo no hace falta.

---

## Paso 2 · El funnel, dos páginas

**Página 1 — captura.** Elemento Custom Code, ancho completo, sin padding, con
el contenido de `index.html`.

**Página 2 — gracias.** Igual, con `gracias-agenda.html`. Ya trae el
calendario de booking embebido (`bIVuNHNojGEgH3gf6yXe`, el mismo de zapatas) y
los dos botones de acceso con el token.

Nombrar siguiendo la convención que ya usa el equipo:

```
acceso-gratis-verificaciones-acero-form
acceso-gratis-verificaciones-acero-gracias
```

> **Y avisar a Dayana del nombre exacto.** El 25-ago un renombrado sin aviso
> dejó dos lead magnets en 404 durante días, porque esos enlaces viven
> embebidos en la página de recursos, en los bots y en el blog. Ese es el
> acuerdo nuevo.

---

## Paso 3 · La membresía — así entregan los demás

**Esto es lo que hacía falta para que funcione igual que los otros.**
Comprobado el 25-ago contra la página viva de la Calculadora de Zapatas: no
entrega el enlace directo, entrega un **producto de membresía** en el portal.
El acceso queda ligado al contacto en el CRM y se concede por workflow.

1. **Memberships → Courses → Products → Create Product.**
   Nombre: `5 Verificaciones en Acero · Herramienta DMA`. Plantilla en blanco.

2. **Dos lecciones**, una por entregable. En cada una, widget Custom Code:

   ```html
   <!-- Lección 1 · La guía -->
   <iframe
     src="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/eficiencia-acero/guia.html?acceso=dm2026"
     style="width:100%;min-height:2400px;border:none;border-radius:12px"
     title="Las 5 verificaciones en acero"></iframe>
   ```

   ```html
   <!-- Lección 2 · El verificador -->
   <iframe
     src="https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/eficiencia-acero/app.html?acceso=dm2026"
     style="width:100%;min-height:1700px;border:none;border-radius:12px"
     title="Verificador de eficiencia en acero"></iframe>
   ```

   > El `?acceso=dm2026` las abre ya desbloqueadas: el candado no molesta a
   > los miembros, porque la membresía ya hace el control de acceso.

   > **Iframe y no pegar el código**: la fuente vive en GitHub Pages. Cualquier
   > corrección se publica una vez y se refleja sola en la membresía, en el
   > funnel y en el enlace público.

3. **Offer** → Memberships → Offers → New Offer → agrega el producto →
   precio **Free** → guardar **y publicar**.

4. En el workflow del formulario, añadir **Membership Grant Offer** → esa
   oferta. GHL crea el usuario del portal y le manda sus credenciales.

5. **Publicar el PRODUCTO**, no solo la lección y la oferta, y habilitar la
   app de Cursos en el Client Portal. Son las dos causas típicas de «el
   portal se ve vacío».

6. Cuando exista, pegar su URL en `gracias-agenda.html`:

   ```js
   const URL_MEMBRESIA = '';   // ← aquí
   ```

   Mientras esté vacío, la página de gracias entrega el acceso directo con
   token. Nadie se queda esperando a que el portal exista.

---

## Paso 4 · El workflow de la palabra — no es el bot

**Dos cosas distintas, y conviene no mezclarlas:**

| | Qué hace | Quién lo monta |
|---|---|---|
| **El workflow** | Alguien comenta la palabra en **esa publicación** → le llega por DM el texto y los recursos, automático | Aquí, en este montaje |
| **El bot** | Cuando esa persona **responde** al DM, el bot toma la conversación | Patricio. A él se le dice qué contestar cuando pregunten por estas guías |

Lo que se monta en este paso es **el workflow**. El bot no se toca.

### El workflow

**Disparador:** comentario con la palabra `ACERO`, **acotado a la publicación
concreta** — la pieza `ago-blog-acero-verificaciones` (Sáb 23). No a cualquier
post: si se deja abierto, se dispara con comentarios de piezas viejas que
prometían otra cosa.

**Qué manda por DM:** el texto de entrega más los dos enlaces —la guía y el
verificador—, o el acceso al portal si la membresía ya está montada.

### Lo que no se puede omitir, y cuesta caro

**Una acción de envío por cada disparador, separadas.** Rama Instagram → DM
por Instagram. Rama Facebook → DM por Facebook Messenger. **Nunca una sola
acción compartida entre las dos.**

Cuando el post nace en Instagram y aparece también en Facebook, quien comenta
en la copia de Facebook tiene un ID de Facebook. Si el envío está atado solo al
canal de Instagram, **el workflow marca el paso como ejecutado y el DM nunca
sale**. En julio se perdieron unos 35 leads así, y nadie lo vio porque la
respuesta pública sí salía siempre.

**La respuesta pública lleva siempre el enlace directo**, nunca solo «te
escribí al DM». Es la red de seguridad real si el canal falla.

**Probar comentando de verdad en las dos superficies** antes de publicar el
post — en Instagram y en la copia de Facebook. Es la única forma de detectar
esa falla antes de que la paguen los leads.

Etiquetas del contacto: `lead-acero-verificaciones` + `origen-bot-acero`.

### Y aparte, lo de Patricio

A él se le pasa el texto de qué responder cuando alguien pregunte por estas
guías — eso vive en el bot, no en el workflow, y no bloquea este montaje.

---

## Paso 5 · Comunidades

Las comunidades son de GHL. Vincular la guía en la pestaña Learning de cada
grupo y publicar el anuncio con el enlace de la landing.

---

## Paso 6 · La verificación que no se salta

Después de montar, **no basta con que los botones se pongan verdes**. Hay que
recorrerlo entero como lo haría un lead:

1. Comentar `ACERO` en **la publicación del Sáb 23**, en Instagram **y** en la
   copia de Facebook.
2. Que llegue el DM en las dos, con los enlaces dentro.
3. Abrir el enlace → llenar el formulario → llegar a la página de gracias.
4. Abrir el verificador y la guía desde los botones: deben entrar **sin
   candado**.
5. Confirmar que **llegó la oferta de membresía** y que se puede entrar al
   portal con esas credenciales.
6. Buscar el contacto en el CRM y confirmar que **el campo de perfil quedó
   guardado**. Que el formulario tenga la pregunta no significa que el dato
   llegue al contacto — eso solo se sabe mirando la ficha.
7. Pedir la página pública por HTTP y confirmar que carga.

El punto 6 es el que más veces falla en silencio, y es justo el dato que
Dayana necesita para mover la pauta.

---

## Lo que queda pendiente y no bloquea el montaje

- **Ejemplos numéricos de placa base.** La §5 es una lista de qué verificar,
  sin cifras — no las necesita. Si algún día se quiere un ejemplo trabajado,
  sale de un cálculo real del equipo, nunca inventado.
- **Rangos de kg/m² por tipología.** El verificador muestra el kg/m² como dato
  sin juicio. No existe rango normativo: AISC y la NEC no lo traen, es dato de
  obra. Se enciende el panel comparativo el día que haya rangos de proyectos
  reales de DMA.
