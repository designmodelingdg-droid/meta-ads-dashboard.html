# Cotizador de Honorarios Estructurales · montaje

Para **Ester y Aylin** (GHL), **Patricio** (OpenReply) y **Gabriel** (horas de ejemplo).
Palabra clave: **COTIZA**. Lanzamiento propuesto: semana del 12 de octubre.

```
Landing   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/
App       https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/app.html?acceso=dm2026
Gracias   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/gracias-agenda.html

En GHL (se crean en el paso 2):
Landing   https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form
Gracias   https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-gracias
```

## Qué funciona ya, sin montar nada

- La landing, la app y la gracias están publicadas en GitHub Pages.
- El formulario propio de la landing **ya manda cada lead a GHL** por el Inbound
  Webhook de siempre (el de la Calculadora de Zapatas), con
  `fuente: "cotizador-honorarios"`. Es la vía de respaldo: funciona, pero el
  webhook de GHL cobra por ejecución.
- El acceso a la app es instantáneo por token (`dm2026`). No se promete nada
  por correo ni por WhatsApp.

## Antes de publicar el primer post (bloqueante)

### 0 · Gabriel revisa las horas de ejemplo

La app trae horas de EJEMPLO por entregable (fijas + por cada 100 m²). No son
un estándar y la app lo dice. Aun así, son lo primero que ve un ingeniero y
tienen que ser defendibles. Gabriel las revisa en `app.html`, constante
`ENTREGABLES`, y las cambia por las de su práctica si no le cuadran:

| Entregable | Fijas | Por 100 m² |
|---|---|---|
| Modelo y análisis estructural | 8 | 6 |
| Diseño de elementos y cimentación | 6 | 5 |
| Planos estructurales (Revit) | 8 | 6 |
| Memoria de cálculo | 4 | 2 |
| Planilla de acero y cantidades (apagado) | 2 | 2 |
| Coordinación con arquitectura e instalaciones | 4 | 0 |

Si cambian, hay que actualizar las cifras del ejemplo en la landing
(«14,71 USD por hora», «17,31», «5,88», «317,77») y volver a tomar
`img/resultado.jpg` y `img/propuesta.jpg`. La prueba `prueba/calc.test.js`
también fija esos números: se corre después del cambio.

### 1 · El formulario nativo de GHL (Ester y Aylin)

1. Sites → Forms → **duplicar** «Calculadora de Zapatas - Registro».
2. Nombre: **Cotizador de Honorarios - Registro**.
3. Campos: nombre, correo, teléfono y una pregunta desplegable **«¿Cómo trabajas
   hoy?»** con estas opciones, escritas igual:
   - Ingeniero independiente: cotizo mis proyectos
   - Trabajo en empresa y cotizo proyectos aparte
   - Tengo una empresa de diseño o construcción
   - Arquitecto
   - Estudiante
   - Otro
4. Opciones del formulario → al enviar: **Redirect to URL** →
   `https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-gracias`
5. Guardar y copiar la URL del formulario
   (`https://api.leadconnectorhq.com/widget/form/<ID>`) y pasársela a Claude:
   va en `GHL_FORM_IFRAME_URL` de `index.html` y se regenera `ghl-landing.html`.
   Hasta entonces la landing usa el formulario propio y el webhook: funciona
   igual, así que **esto no bloquea el lanzamiento**.

### 2 · El funnel en GHL (Ester y Aylin)

Los nombres de las páginas van **exactamente así**: `ghl-landing.html` ya
redirige a la gracias con esa dirección, y la tarjeta del hub enlaza a la
primera.

1. Sites → Funnels → **duplicar** el funnel de la Calculadora de Zapatas.
   Nombre: **Cotizador de Honorarios**.
2. Página 1 · path **`acceso-gratis-cotizador-honorarios-form`**:
   - borrar lo que traiga y dejar una sola sección a ancho completo, sin padding;
   - elemento **Custom Code** con TODO el contenido de `cotizador-honorarios/ghl-landing.html`;
   - SEO: título «Cotizador de Honorarios Estructurales gratis · Design Modeling
     Academy» y la imagen para compartir
     `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/img/resultado.jpg`.
3. Página 2 · path **`acceso-gratis-cotizador-honorarios-gracias`**: igual, con
   `cotizador-honorarios/ghl-gracias.html`.
4. Guardar y publicar. Abrir las dos en el celular.
5. **Workflow de etiquetas** (duplicar el de zapatas): disparador «Form
   Submitted: Cotizador de Honorarios - Registro» o «Inbound Webhook» con
   `fuente = cotizador-honorarios` → etiquetas `lead-cotizador` y
   `origen-landing-cotizador` → notificación interna al equipo de ventas.
   El seguimiento natural después es la Especialización en Acero o el
   Diplomado en Estructuras: quien cotiza estructuras es el perfil que compra.

### 3 · La palabra COTIZA (Patricio)

**Instagram · OpenReply.** Campaña nueva «COTIZA · Cotizador de honorarios»:
palabra **COTIZA**, sin coincidencia parcial, exige seguir, DM con el enlace de
la landing. Como las campañas de OpenReply van atadas a un post, conviene
activar **«cualquier publicación»**: COTIZA solo se usa para este recurso.

DM sugerido:

> ¡Hola! Aquí tienes el Cotizador de Honorarios Estructurales: calcula tu tarifa mínima por hora, las horas del proyecto y te arma la propuesta en PDF con los impuestos de tu país. 👉 https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form

**Facebook · GHL.** Workflow «Comentario COTIZA», copia del de ZAPATA:
disparador de comentario de Facebook filtrado por COTIZA → respuesta pública
**con el enlace** → DM por Messenger con el enlace → etiquetas `lead-cotizador`
y `origen-bot-cotiza` → notificación interna.

> ⚠️ Incidente conocido (jul-2026, ~35 leads perdidos): si el post sale de
> Instagram y se replica en Facebook, la gente comenta en la copia de Facebook.
> La acción de DM tiene que ir **por separado en cada canal**, y la respuesta
> pública siempre lleva el enlace, nunca solo «te escribí al DM».

**Prueba obligatoria:** comentar COTIZA desde una cuenta ajena en Instagram y
en la copia de Facebook del mismo post. Llegan los dos DM, o no se publica.

**Y la matriz:** COTIZA pasa a ser la séptima palabra. La lista «solo estas
seis» del calendario hay que ampliarla, y `fuentes/openreply/campanas.json` la
mostrará como viva cuando dispare el primer DM.

### 4 · En la página de recursos (Ester y Aylin, después del paso 2)

La tarjeta ya está en `recursos/index.html`, primera de «Herramientas
gratuitas», con la etiqueta **Nuevo**, enlazando a
`https://funnel.dgdesignmodeling.com/acceso-gratis-cotizador-honorarios-form`.

1. **Solo cuando la página 1 del funnel esté publicada** (si no, la tarjeta
   lleva a un 404): abrir en GHL la página
   `https://funnel.dgdesignmodeling.com/recursos`.
2. Reemplazar el contenido del Custom Code por TODO `recursos/ghl-recursos.html`.
3. Guardar, publicar y comprobar en el celular que la tarjeta abre la landing.
4. La imagen de la tarjeta (`cotizador-honorarios/tarjeta-hub.png`, 1672×941,
   fondo claro, igual que las demás) ya se sirve desde GitHub Pages. Si se
   prefiere en el CDN de GHL como las otras: subirla a Media Storage y pasarle
   la URL a Claude para cambiarla en la tarjeta.

### 5 · Opcional · en la membresía

Igual que zapatas: una lección que embebe la app por iframe con
`?acceso=dm2026`, y la oferta gratis concedida con «Form Submitted».

## Checklist de punta a punta

1. Comentario COTIZA en Instagram → llega el DM con el enlace.
2. Lo mismo en la copia de Facebook.
3. El enlace abre la landing del funnel.
4. El formulario valida y redirige a la gracias.
5. La gracias abre el cotizador sin candado.
6. El contacto aparece en el CRM con `lead-cotizador` y su respuesta de perfil.
7. El calendario de la gracias carga y deja agendar.
8. La propuesta se descarga en PDF desde el celular.
9. Se borra el contacto de prueba.

## Lo que la herramienta NO hace (y no se dice que haga)

- No da precios de mercado ni el arancel de ningún colegio profesional.
- No reemplaza al contador: las retenciones dependen de quién es el cliente.
- No envía los números del proyecto a ninguna parte. Solo recuerda en el
  navegador el nombre, el registro y el contacto del profesional.

## Tasas verificadas (30-sep-2026)

| País | Impuesto | Retenciones cargadas | Fuente |
|---|---|---|---|
| Ecuador | IVA 15 % | IR 10 % a honorarios de personas naturales | SRI, circular NAC-DGECCGC25-00000006; tabla de retenciones vigente desde el 1-mar-2026 |
| México | IVA 16 % | ISR 10 % y 2/3 del IVA (persona física → persona moral) | LIVA art. 1-A |
| Colombia | IVA 19 % | manuales | tarifa general |
| Perú | IGV 18 % (15,5 % + 2,5 % IPM) | manuales | SUNAT, Ley 32387 |
| Rep. Dominicana | ITBIS 18 % | ISR 15 % desde el 1-jul-2026 (Ley 30-26, art. 309) y 100 % del ITBIS | DGII |

Una tasa que cambie se corrige en `PAISES` (`app.html`), en la tabla de la
landing y en esta guía, con la fecha nueva.
