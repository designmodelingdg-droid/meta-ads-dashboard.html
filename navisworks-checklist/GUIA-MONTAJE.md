# Checklist de coordinación BIM en Navisworks — montaje en GoHighLevel

Para **Ester y Aylin**. Construido y probado en navegador; falta conectarlo al
CRM y al embudo.

```
Landing      https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/navisworks-checklist/
Gracias      …/navisworks-checklist/gracias-agenda.html
El checklist …/navisworks-checklist/guia.html?acceso=dm2026
```

**Palabras clave: `BIM` y `IA`** · Campaña de OpenReply: **CHECKLIST NAVISWORKS**
(ya existe) · Etiquetas: `lead-navisworks-checklist` · `origen-bot-BIM`

---

## De dónde sale este recurso

El carrusel **«Mejores prácticas para la coordinación en Navisworks»**
(Instagram, 14-sep, https://www.instagram.com/p/DdRyKTvm9mI/) promete en el
caption y en la última slide: *«Comenta BIM o IA y te paso mi checklist de
coordinación»*.

Ese checklist **no existía**. La campaña CHECKLIST NAVISWORKS de OpenReply
estaba mandando el formulario de la Guía Revit + ChatGPT
(`acceso-gratis-guia-revit-chatgpt-form`) porque no había otra cosa que mandar.
Quien comentaba BIM pedía un checklist de Navisworks y recibía una guía de
Revit. Es la misma forma del fallo del post de conexiones de agosto.

Esta carpeta es el checklist. Desarrolla las 5 prácticas del carrusel en 7
fases y 51 puntos de control, con casillas que se guardan en el navegador y un
botón para imprimir a PDF.

## Qué está montado hoy y qué falta

| | Estado | Dónde |
|---|---|---|
| El checklist (`guia.html`) | **Listo**, publicado en GitHub Pages | repo |
| Landing y gracias en GitHub Pages | **Listas** | repo |
| **La campaña de OpenReply** | Apunta a la **guía directa con token** (`guia.html?acceso=dm2026`), como paso provisional | OpenReply |
| Formulario nativo de GHL | **Falta** — Paso 1 | GHL |
| Páginas del embudo en `funnel.dgdesignmodeling.com` | **Falta** — Paso 3 | GHL |
| Cambiar el enlace de la campaña al formulario | **Falta** — Paso 4, cuando exista el Paso 3 | OpenReply |
| Membresía (lección con iframe) | **Falta** — Paso 5 | GHL |
| Tarjeta en el hub `/recursos` | **Falta** — Paso 6 | repo + GHL |
| Aviso a Patricio | **Falta** — Paso 7 | mensaje |

**Mientras el formulario no exista, la gente que comenta BIM recibe el
checklist directo con token.** Prometimos acceso inmediato y se cumple. Lo que
no tenemos hasta el Paso 1 es el contacto en el CRM.

## Lo que este recurso NO hace, y por qué

Conviene que el equipo lo repita igual cuando alguien pregunte:

- **No da tolerancias «oficiales».** Las tolerancias de clash no están en
  ninguna norma; las fija el BEP de cada proyecto. El checklist da valores de
  arranque y lo dice en cada sitio donde aparece un número.
- **No enseña Navisworks desde cero.** Da por sabido dónde está cada botón.
- **No exporta BCF.** Navisworks no lo trae de fábrica; el checklist lo dice y
  dice qué hacer (complemento o plataforma), pero no lo resuelve.
- Todo lo que afirma sobre funciones de Navisworks está **cruzado contra la
  documentación oficial de Autodesk** (Navisworks Manage 2026 y 2027).

---

## PASO 0 — Acordar el slug ANTES de escribir nada

**Se pregunta el slug exacto antes de escribir el primer enlace, y quien lo
publica lo confirma tal cual quedó.** El 26-ago nos costó siete archivos un
singular/plural entre lo que escribimos y lo que se publicó.

Propuesta, siguiendo la convención `acceso-gratis-<tema>-form` / `-gracias`:

```
https://funnel.dgdesignmodeling.com/acceso-gratis-navisworks-checklist-form
https://funnel.dgdesignmodeling.com/acceso-gratis-navisworks-checklist-gracias
```

Si se cambia, se avisa antes de publicar y se corrige aquí, en `recursos/` y en
OpenReply. **GHL no deja redirección del path anterior**: renombrar después de
publicado rompe el hub, el bot y el blog.

## PASO 1 — El formulario nativo

GHL → **Sites → Forms → New Form**. Nómbralo `Checklist Navisworks`.

**Créalo desde cero, no clonando otro.** Si lo clonas, revisa las cinco cosas
que viajan con la copia: la regla condicional de redirección, el destino por
defecto, el texto del botón, el asunto del correo y el nombre del campo. El
25-ago los ocho formularios de lead magnet mandaban a la confirmación de un
webinar de febrero por una regla heredada que no se veía en la configuración.

| Campo | Tipo | Obligatorio |
|---|---|---|
| Nombre y apellido | Texto | Sí |
| Correo | Email | Sí |
| WhatsApp | Teléfono | No |
| ¿Cuál es tu perfil actualmente? | Desplegable | Sí |

Opciones del perfil: *Ingeniero civil / estructural · Arquitecto · Constructor /
contratista · Estudiante · Otro*.

**El perfil va mapeado al campo personalizado del contacto**, no solo al
formulario. La clave en GHL es `{{contact.cul_es_tu_perfil_actualmente}}` — con
`cul_`, sin la `a`. Escribirla «bien» no da error: sale vacío.

Texto del botón: `Ver el checklist →`.

**Redirect URL** al terminar (provisional, hasta que exista la página del
Paso 3):

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/navisworks-checklist/gracias-agenda.html?acceso=dm2026
```

Cuando exista la página de gracias del embudo, el redirect pasa a ser esa.

**Qué pegar en el repo:** la URL del widget del formulario
(`https://api.leadconnectorhq.com/widget/form/<ID>`) va en `index.html`, en la
constante `GHL_FORM_IFRAME_URL`. Está vacía a propósito: mientras esté vacía la
landing usa su formulario propio y manda directo a gracias, sin pasar por el
CRM.

**Comprobación:** llenar el formulario de verdad **una vez**, ver que cae en
la gracias de este recurso (no en otra), y abrir la ficha del contacto para
ver que el perfil llegó al campo. Después, borrar el contacto de prueba.

## PASO 2 — Las dos etiquetas

`lead-navisworks-checklist` (enciende la secuencia) y `origen-bot-BIM`.

Si la palabra que disparó fue `IA`, la campaña es la misma; la etiqueta de
origen se queda en `origen-bot-BIM` para no partir el dato en dos.

## PASO 3 — Las páginas del embudo

Con el slug del Paso 0 confirmado:

1. **Página 1 (form):** Custom Code a ancho completo, sin padding, con el
   contenido de `index.html`. Se genera con
   `python3 scripts/build_ghl_landing.py navisworks-checklist` (vuelve
   absolutas las rutas relativas) y se pega el resultado.
2. **Página 2 (gracias):** ídem con `gracias-agenda.html`.
3. Con el slug confirmado, añadir la carpeta a `FUNNEL_POR_CARPETA` en
   `scripts/build_ghl_landing.py` (como está `test-nivel-bim`), para que la
   versión de GHL de la landing enlace a la gracias del embudo y no a la de
   GitHub Pages. Sin esa entrada el script funciona igual, pero deja los
   enlaces a Pages.
4. **Revisar la URL del paso del embudo, no solo lo que se ve.** Un clon
   arrastra su URL: en agosto la página de acero conservaba la URL de la
   calculadora de zapatas y al abrirla salía la calculadora.

**Comprobación:** `curl -sI` de las dos URLs devuelve 200, y abrirlas en
teléfono muestra este recurso, no otro.

## PASO 4 — Cambiar el enlace de la campaña de OpenReply

La campaña **CHECKLIST NAVISWORKS** (palabras `BIM` e `IA`, acotada al post
DdRyKTvm9mI, exige seguir) hoy apunta al checklist directo con token. Cuando
las páginas del Paso 3 existan y den 200, el enlace principal de la campaña
pasa a:

```
https://funnel.dgdesignmodeling.com/acceso-gratis-navisworks-checklist-form
```

Así el contacto entra al CRM antes de recibir el recurso. **No se cambia antes
de que la página dé 200**: un enlace roto en el DM es peor que un enlace que
salta el CRM.

La respuesta pública lleva **siempre el enlace visible**, nunca solo «te
escribí al DM»:

> Te lo dejo aquí 👇 el checklist de coordinación en Navisworks, 7 fases del
> NWC a la reunión, con las tolerancias de arranque por disciplina: [enlace]

**Comprobación:** comentar `BIM` de verdad en Instagram **y** en la copia de
Facebook del post, y recibir el DM en las dos. Después mirar en
`matriz-viral/fuentes/openreply/campanas.json` que la campaña sigue `activa`
y que el enlace rastreado es el nuevo.

## PASO 5 — La membresía

Patrón real de Zapatas y del Test (comprobado el 25-ago):

1. Producto en el portal → una lección → el checklist embebido **por iframe**
   con `https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/navisworks-checklist/guia.html?acceso=dm2026`.
   Iframe y no código pegado: una corrección se publica una vez en Pages y se
   refleja sola.
2. Oferta **Free**.
3. En el workflow del formulario: acción **Membership Grant Offer**.
4. **Publicar el producto**, no solo la lección y la oferta, y tener la app de
   Cursos habilitada en el Client Portal. Son las dos causas típicas de «el
   portal se ve vacío».
5. La URL del producto termina en `/purchase-course`. Pegarla en
   `gracias-agenda.html`, en `URL_PRODUCTO`. Mientras esté vacía, el botón abre
   el checklist directo con token.

**Comprobación:** entrar al portal con las credenciales de un contacto de
prueba y ver el checklist dentro de la lección, sin doble barra de scroll en
teléfono (la guía avisa su alto al iframe).

## PASO 6 — El hub de recursos

Sumar la tarjeta a `recursos/index.html` (con la URL del Paso 3), regenerar
`ghl-recursos.html` con `python3 scripts/build_ghl_landing.py recursos` y
volver a pegar en GHL. Hace falta una imagen de tarjeta **1672 × 941, fondo
claro** — se pinta con `contain` y una pieza navy deja dos bandas.

**Comprobación:** `curl` de `/recursos` y ver la tarjeta dentro.

## PASO 7 — Avisar a Patricio

Mensaje con tres cosas:

- **Palabras:** `BIM` e `IA`, en el post del carrusel de Navisworks.
- **Enlace:** el del Paso 3 (o el directo con token mientras no exista).
- **Qué contestar** si alguien pregunta por el checklist: que es gratis, que
  se abre desde el enlace, que las casillas se guardan en el navegador y se
  imprime a PDF, y que las tolerancias son de arranque, no de norma.

El bot no se toca desde aquí. Si no se le avisa, va a responder otra cosa.

---

## La secuencia de correo (cuando exista el Paso 1)

| | Cuándo | Qué dice |
|---|---|---|
| Correo 1 | Inmediato | El enlace otra vez, y qué hacer primero: imprimirlo y pasarlo con el modelo del proyecto actual. |
| Correo 2 | 48 h | El error 3 (borrar en vez de aprobar) y por qué es el que hace que cada ciclo empiece de cero. |
| Correo 3 | Día 5 | El puente: cómo se monta esto para un equipo entero en el módulo BIM Coordination del Máster. **Sin precio.** Agenda una cita. |

El precio del Máster no va en ningún correo. ACERO no encaja con este recurso;
no se menciona.

---

## Comprobar antes de dar por cerrado

1. Comentar `BIM` **en Instagram** → llega el DM.
2. Comentar `BIM` **en la copia de Facebook** → llega el DM por Messenger.
3. La respuesta pública incluye el enlace visible.
4. El enlace abre la landing **en teléfono**, sin scroll horizontal.
5. Enviar el formulario → redirige a la gracias **de este recurso**.
6. El botón del checklist abre **sin pedir registro**.
7. Marcar tres casillas, recargar: siguen marcadas.
8. El botón «Imprimir / PDF» abre el diálogo de impresión con las casillas.
9. El contacto aparece en el CRM con sus dos etiquetas y con el perfil en su
   campo.
10. Borrar los contactos de prueba.

Lo que se verificó en el repo antes de entregar: las tres páginas a 390 px y a
1280 px con Chromium, sin scroll horizontal; el candado (sin `?acceso=` no se ve
el checklist, con él sí); y las casillas persisten al recargar. Lo que **no** se
pudo verificar desde aquí: nada de GHL ni de OpenReply — eso es de los pasos de
arriba.
