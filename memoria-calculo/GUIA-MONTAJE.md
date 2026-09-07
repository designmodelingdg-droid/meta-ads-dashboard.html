# Guía + plantilla de memoria de cálculo — montaje en GoHighLevel

Para **Ester y Aylin**. Construido y probado; falta conectarlo al CRM.

```
Landing   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/memoria-calculo/
Gracias   …/memoria-calculo/gracias-agenda.html
La guía   …/memoria-calculo/guia.html?acceso=dm2026
Word      …/memoria-calculo/Plantilla-Memoria-de-Calculo-DMA.docx
Excel     …/memoria-calculo/Resumen-Verificaciones-DMA.xlsx
```

**Palabra clave: `MEMORIA`** · Etiquetas: `lead-memoria-calculo` · `origen-bot-MEMORIA`

---

## ⚠️ ANTES DE PUBLICAR EL CTA — lo revisa Gabriel

La matriz lo dice y hay que respetarlo: **este es el único de los tres recursos
que puede terminar dentro de un documento que alguien firma.** Si la estructura
que proponemos está incompleta, el problema deja de ser de marketing.

Lo que Gabriel tiene que mirar, en concreto:

1. **Que las 13 secciones estén completas** para el tipo de memoria que
   entregamos en la región. Si falta una, se añade antes de publicar.
2. **Que los 5 errores de devolución** correspondan a lo que de verdad devuelve
   una entidad revisora aquí, no a lo que es teóricamente correcto.
3. **Que la plantilla de Word no induzca a nadie a omitir algo.** Una plantilla
   que se usa tal cual acaba definiendo el alcance del documento.

Hasta que lo revise, el recurso puede estar publicado (no hace daño estando ahí),
pero **el CTA no sale en ninguna pieza**. Si toca la fecha y no hay revisión, la
matriz ya tiene el reemplazo previsto: el CTA cambia a las 5 Verificaciones de
Acero, que ya existe.

---

## Lo que este recurso NO hace, y por qué

Está escrito así a propósito, y conviene que el equipo lo repita igual:

- **No calcula nada.** Es estructura documental: cómo se organiza y se justifica
  la memoria. Los valores y los criterios son del ingeniero.
- **No transcribe ninguna cifra normativa.** Se remite siempre a la norma vigente
  aplicable. Es la misma regla del tutor de IA.
- **La hoja de Excel calcula un ratio y marca CUMPLE / NO CUMPLE.** Nada más.
  No conoce ninguna norma: el límite admisible lo escribe el usuario. En el
  momento en que la hoja propusiera una sección o un valor, tendría que responder
  por ese número.

Esa contención es justamente lo que hace que podamos repartirlo. Un recurso que
propusiera valores de diseño no lo podríamos firmar.

---

## PASO 1 — El formulario nativo

GHL → **Sites → Forms → New Form**. Nómbralo `Memoria de cálculo`.

| Campo | Tipo | Obligatorio |
|---|---|---|
| Nombre y apellido | Texto | Sí |
| Correo | Email | Sí |
| WhatsApp | Teléfono | No |
| ¿Cada cuánto entregas memorias de cálculo? | Desplegable | Sí |

Opciones: *Varias al mes · Algunas al año · Voy a entregar la primera · Las
reviso, no las escribo · Todavía no, pero quiero aprender*.

**Redirect URL** al terminar:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/memoria-calculo/gracias-agenda.html?acceso=dm2026
```

Pega la URL del formulario en `index.html`, en `GHL_FORM_IFRAME_URL`.

## PASO 2 — Las dos etiquetas

`lead-memoria-calculo` (enciende la secuencia) y `origen-bot-MEMORIA`.

## PASO 3 — El bot, con DOS ramas separadas

Disparador de comentario filtrado por `MEMORIA`. **Rama Instagram → DM de
Instagram. Rama Facebook → DM de Messenger. Nunca una acción compartida** — es
lo que costó 35 leads en julio, y falla en silencio porque la respuesta pública
sí sale siempre.

La respuesta pública lleva **siempre el enlace visible**:

> Te la dejo aquí 👇 las 13 secciones de una memoria que se sostiene ante
> revisión, con la plantilla en Word y la hoja de verificaciones: [enlace]

## PASO 4 — La secuencia, con el puente que depende del perfil

| | Cuándo | Qué dice |
|---|---|---|
| Correo 1 | Inmediato | Los enlaces otra vez: guía, Word y Excel. |
| Correo 2 | 48 h | El error 3 (hipótesis listadas, no justificadas) y por qué es el que delata una memoria reciclada. |
| Correo 3 | Día 5 | **El puente cambia según lo que contestó.** |

**El correo 3, según el perfil:**

- *Varias al mes* / *Algunas al año* / *Las reviso* → **ACERO, $225, con el tutor
  de IA incluido.** Aquí el precio **sí** va: es alguien que ya trabaja y para
  quien $225 es una decisión pequeña.
- *Voy a entregar la primera* / *Todavía no* → **módulo BIM Professional**, sin
  precio, con «agenda una cita».

Esta bifurcación es la razón de que la pregunta de perfil esté en el formulario.
Si todos reciben el mismo correo 3, la pregunta sobra.

## PASO 5 — Notificación al setter

Con el nombre del recurso **y la respuesta de perfil**. Quien entrega varias
memorias al mes y quien va a entregar la primera no se trabajan igual, y esa
diferencia se pierde si todos caen en la misma bandeja.

---

## Comprobar antes de publicar

1. Comentar `MEMORIA` **en Instagram** → llega el DM.
2. Comentar `MEMORIA` **en la copia de Facebook** → llega el DM por Messenger.
3. La respuesta pública incluye el enlace visible.
4. El enlace abre la landing **en teléfono**.
5. Enviar el formulario → redirige a gracias.
6. El botón de la guía abre **sin pedir registro**.
7. **El botón de Word descarga un .docx que abre en Word.**
8. **El botón de Excel descarga un .xlsx y las fórmulas calculan el ratio.**
9. El contacto aparece en el CRM con sus dos etiquetas.
10. Borrar los contactos de prueba.

> **Los puntos 7 y 8 hay que hacerlos a mano.** Los dos ficheros se generan desde
> `scripts/build_memoria_plantilla.js` y `scripts/build_memoria_excel.py`, y
> están comprobados en cuanto a estructura y lógica — pero **en este entorno no
> hay forma de abrirlos en Word ni en Excel de verdad.** La primera vez que
> alguien los abra, que avise si algo se ve raro.
