# Bot de historias — disparador de DM en GHL

**Para:** Gabriel Pantoja (GoHighLevel y configuración técnica)
**De:** Dayana + Claude
**Fecha:** 16-ago-2026

Montar el disparador que recoge las **respuestas a historias de Instagram** con
tres palabras clave: `ACERO`, `CUPO` y `NIVEL`.

> **Esto bloquea tres piezas de contenido que ya están escritas y aprobadas.**
> Las tres historias de venta llevan escrito en sus notas de producción «no
> publicar hasta que el disparador esté montado». Si se graban antes, la
> persona responde con la palabra y **no pasa absolutamente nada**: se pierde
> el lead y queda esperando.

---

## 1. Por qué esto NO es el bot que ya existe

El bot de `ZAPATA` que ya funciona escucha **comentarios en publicaciones**
(`Instagram → Comment on Post`). Esto es distinto y hay que montarlo aparte.

**Las historias no tienen comentarios.** Cuando alguien responde a una historia,
esa respuesta **entra a la bandeja de mensajes directos** como un mensaje
normal. Por eso el disparador tiene que ser de **mensaje entrante**, no de
comentario.

Y de ahí sale toda la estrategia. Los stickers no sirven para automatizar:

| Sticker | ¿Dónde cae la respuesta? | ¿Se automatiza? |
|---|---|---|
| Encuesta, quiz, deslizador, caja de preguntas | Solo en el panel de la historia | ❌ **No.** Hay que mirarlo y escribir a mano |
| **Responder a la historia** (la persona escribe) | **Bandeja de DM** | ✅ **Sí — es lo que montamos aquí** |
| Enlace, cuenta regresiva | No hay respuesta | ✅ Cero trabajo |

Los cuatro primeros son los que hacían inviable la estrategia: obligaban a
Dayana a responder a mano todos los días. Por eso el frame que convierte pide
**«respóndeme con la palabra X»**.

---

## 2. Lo PRIMERO que hay que comprobar

**Antes de montar nada**, hay que resolver esta duda, porque si la respuesta es
mala hay que cambiar de enfoque:

> El disparador **Customer Replied** escucha mensajes entrantes. La
> documentación oficial no dice si dispara **solo con contactos que ya
> existen** en el CRM, o también con gente nueva.

Y eso es justo el caso que nos importa: **la mayoría de quien responde una
historia todavía NO es contacto.** Si el disparador solo funciona con contactos
existentes, este montaje no sirve tal cual y hay que buscar la alternativa
(probablemente la acción **Instagram Interactive Messenger**, que sí está
pensada para responder DMs y comentarios de Instagram).

**Cómo comprobarlo, en 5 minutos:** monta el workflow del punto 3 con una sola
palabra de prueba, y responde a una historia desde una cuenta de Instagram que
**no esté** en el CRM. Si el workflow no se dispara, avísanos antes de seguir.

---

## 3. El workflow

**Automation → Workflows → Create.** Nómbralo `Bot HISTORIAS — palabras clave`.

> Requisito: Instagram conectado en **Settings → Integrations** de la subcuenta.

### Disparador

**Customer Replied**, con dos filtros:

| Filtro | Valor |
|---|---|
| **Reply Channel** | Instagram DM |
| **Contains Phrase** | la palabra clave |

La documentación confirma que este disparador admite los dos filtros. El
nombre exacto del canal puede variar según la versión de la cuenta — si no
aparece «Instagram DM», usa el que corresponda a Instagram y anótalo.

> **Un workflow por palabra**, no los tres en uno. Cada palabra entrega algo
> distinto, y separarlos hace que se pueda medir cuál convierte y apagar uno
> sin tocar los otros.

### Acciones

**Paso 1 · Responder por DM** con el texto de la palabra (punto 4).

**Paso 2 · Etiquetar** — `Add Tag`:
- `origen-historia` (todos)
- más la etiqueta de la palabra: `historia-acero`, `historia-cupo` o
  `historia-nivel`

Sin esto no se puede medir si las historias venden. Con esto, en un mes
sabemos qué palabra trajo qué.

**Paso 3 · Notificación interna** al asesor, solo en `ACERO` y `CUPO`: son
intención de compra, no de contenido.

---

## 4. Qué responde cada palabra

Los textos van tal cual. **No improvisar sobre estos**: hay reglas de marca
detrás de cada línea (punto 6).

### `ACERO` — pide el temario de la Especialización

> ¡Hola! 👋 Aquí va el detalle de la **Especialización en Diseño Estructural
> BIM en Acero**.
>
> 🔹 4 meses · 110-130 horas · **100% asincrónico** (sin horario al que llegar
> tarde, y el acceso no caduca)
> 🔹 4 certificaciones Autodesk + aval de 120 horas
> 🔹 Robot Structural · Advance Steel · Revit
>
> 👉 https://designmodelingacademy.com/es/especializacion/diseno-estructural-bim-acero
>
> Cuéntame una cosa para orientarte mejor: ¿ya trabajas con estructuras
> metálicas o estás empezando en el tema?

### `CUPO` — pregunta por disponibilidad

> ¡Hola! 👋 La cohorte de **ACERO** es de **10 cupos** y ahora mismo quedan
> **8**.
>
> Abre todos los meses, así que si esta se llena entras a la siguiente — pero
> los que están dentro empiezan ya.
>
> 🔹 4 meses · 110-130 horas · 100% asincrónico
> 🔹 4 certificaciones Autodesk
> 👉 https://designmodelingacademy.com/es/especializacion/diseno-estructural-bim-acero
>
> ¿Te reservo el detalle de inscripción?

> ⚠️ **El número de cupos hay que actualizarlo cada vez que se publica la
> historia.** Al 16-ago-2026 son 10 por cohorte, 2 vendidos, quedan 8. **Nunca
> se inventa:** esta gente vuelve el mes siguiente a comprobarlo, y si el
> número no cuadra se pierde la credibilidad, que es lo único que vendemos.

### `NIVEL` — quiere el test

> ¡Hola! 👋 Aquí está tu acceso al **Test de Nivel BIM GRATIS**
>
> 👉 https://funnel.dgdesignmodeling.com/acceso-gratis-test-nivel-bim-form
>
> Son 20 preguntas, 5 minutos, y al terminar sabes en cuál de los 4 niveles
> estás y qué competencias concretas te faltan para el siguiente.
>
> Antes de que lo hagas, cuéntame: ¿en qué nivel crees que vas a salir? 🙂
> 1️⃣ Modelador BIM
> 2️⃣ Coordinador BIM
> 3️⃣ BIM Manager 4D-5D
> 4️⃣ Especialista BIM+IA

---

## 5. La prueba, antes de dar por bueno nada

Con una cuenta de Instagram real que **no** sea contacto del CRM:

1. [ ] Publicar una historia de prueba que pida responder con `ACERO`.
2. [ ] Responderla desde la cuenta que no es contacto.
3. [ ] **Confirmar que el DM llegó de verdad**, abriendo la conversación — no
       basta con que el workflow marque el paso como ejecutado.
4. [ ] Comprobar en Contacts que se creó el contacto con las dos etiquetas.
5. [ ] Repetir con `CUPO` y con `NIVEL`.
6. [ ] Borrar los contactos de prueba.

> **Por qué insistimos en el punto 3.** En julio, el bot de ZAPATA marcaba los
> pasos como ejecutados y el DM no llegaba: el envío salía por el canal
> equivocado y **fallaba en silencio**. Se perdieron unos 35 leads del primer
> post antes de que alguien abriera una conversación a comprobarlo. Un paso en
> verde no prueba que el mensaje llegara.

---

## 6. Reglas que no se rompen

1. **El precio del Máster no se menciona nunca**, ni «desde», ni por
   aproximación. El Máster no se cotiza por chat. El de ACERO sí puede ir en
   un DM.
2. **Nunca decir «inscríbete»** ni cerrar la venta por chat. El bot entrega y
   **abre conversación**.
3. **Nunca llamar certificación ni diploma** a una herramienta gratuita. El
   test es un diagnóstico.
4. **No prometer lo que no existe**: no hay envío por correo automático ni PDF
   de resultados. El test se ve en pantalla, al momento.
5. Si alguien **pregunta precio o quiere inscribirse → pasar a humano.** No
   improvisar cifras.
6. **Ventana de 24 horas de Meta:** el DM tiene que salir dentro de las 24 h
   siguientes a la interacción. El seguimiento posterior va por correo, con las
   secuencias que están en `matriz-viral/seguimiento/`.

---

## 7. Cuando esté listo

Avisar a Dayana. Se desbloquean las tres historias de venta —
`venta-acero-objecion`, `venta-acero-cupos` y `venta-master-espejo` — que ya
están guionadas cuadro a cuadro y esperando.

El guion completo de cada una se pide al asistente por WhatsApp con su nombre,
o se saca de `matriz/guiones-completos.json`.
