# Cotizador de Honorarios Estructurales · montaje

Para **Ester y Aylin** (GHL), **Patricio** (OpenReply) y **Gabriel** (horas de ejemplo).
Palabra clave: **COTIZA**. Lanzamiento propuesto: semana del 12 de octubre.

```
Landing   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/
App       https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/app.html?acceso=dm2026
Gracias   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/cotizador-honorarios/gracias-agenda.html
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

1. Sites → Forms → duplicar «Calculadora de Zapatas - Registro».
2. Nombre: **Cotizador de Honorarios - Registro**.
3. Campos: nombre, correo, teléfono y «¿Cómo trabajas hoy?» con estas opciones,
   escritas igual:
   - Ingeniero independiente: cotizo mis proyectos
   - Trabajo en empresa y cotizo proyectos aparte
   - Tengo una empresa de diseño o construcción
   - Arquitecto
   - Estudiante
   - Otro
4. Al enviar: **redirigir** a la página de gracias del funnel (paso 2).
5. Etiquetas al enviar: `lead-cotizador` y `origen-landing-cotizador`.
6. Pasar a Claude la URL del formulario
   (`https://api.leadconnectorhq.com/widget/form/<ID>`): se pega en
   `GHL_FORM_IFRAME_URL` de `index.html` y se regenera `ghl-landing.html`.

### 2 · El funnel en GHL

- Página 1 · slug sugerido `cotizador-honorarios`: Custom Code a ancho completo,
  sin padding, con el contenido de **`ghl-landing.html`**.
- Página 2 · slug sugerido `cotizador-honorarios-gracias`: Custom Code con
  **`ghl-gracias.html`**.
- Los `ghl-*.html` se generan solos: `python3 scripts/build_ghl_landing.py cotizador-honorarios`.
  No se editan a mano.

### 3 · La palabra COTIZA (Patricio)

**Instagram · OpenReply.** Campaña nueva «COTIZA · Cotizador de honorarios»:
palabra **COTIZA**, sin coincidencia parcial, exige seguir, DM con el enlace de
la landing. Como las campañas de OpenReply van atadas a un post, conviene
activar **«cualquier publicación»**: COTIZA solo se usa para este recurso.

DM sugerido:

> ¡Hola! Aquí tienes el Cotizador de Honorarios Estructurales: calcula tu tarifa mínima por hora, las horas del proyecto y te arma la propuesta en PDF con los impuestos de tu país. 👉 <URL de la landing>

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

### 4 · Opcional · en la membresía

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
