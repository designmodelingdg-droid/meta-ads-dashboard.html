# Guía «Revit + ChatGPT» — montaje en GoHighLevel

Para **Ester y Aylin**. El recurso está construido y probado; falta conectarlo
al CRM y encender el bot de la palabra clave.

```
Landing   https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/guia-revit-ia/
Gracias   …/guia-revit-ia/gracias-agenda.html
La guía   …/guia-revit-ia/guia.html?acceso=dm2026
```

**Palabra clave del CTA: `GUIA`** · Etiquetas: `lead-revit-ia` · `origen-bot-GUIA`

---

## Qué es y por qué existe

Los 10 errores de Revit que más tiempo hacen perder, con el prompt exacto para
cada uno. No es una lista de prompts de internet: la mitad del valor está en las
dos páginas que casi nadie escribe — **cómo verificar la respuesta** antes de
aplicarla, y **qué no preguntarle nunca**.

Ese enfoque no es un adorno. Es lo que hace que el recurso lo pueda repartir una
academia de ingeniería sin quedar mal: decimos dónde la IA ayuda y dónde deja de
ayudar, y lo decimos antes de que alguien se meta en un problema.

Lo pide el reel del **miércoles 9**, cuyo CTA ya promete esta guía.

---

## PASO 1 — El formulario nativo de GHL

GHL → **Sites → Forms → New Form**. Nómbralo `Guía Revit + IA`.

Cuatro campos:

| Campo | Tipo | Obligatorio |
|---|---|---|
| Nombre y apellido | Texto | Sí |
| Correo | Email | Sí |
| WhatsApp | Teléfono | No |
| ¿Qué usas hoy para resolver un error de Revit? | Desplegable | Sí |

Opciones del desplegable, tal cual: *Busco en foros y Google · Le pregunto a un
compañero · Ya uso ChatGPT o similar · Abro un ticket de soporte · Lo resuelvo
probando hasta que sale*.

En **Settings → On Submit → Redirect URL**, pega la página de gracias con el
token:

```
https://designmodelingdg-droid.github.io/meta-ads-dashboard.html/guia-revit-ia/gracias-agenda.html?acceso=dm2026
```

Publica el formulario y copia su URL. Pégala en `index.html`, en la constante
`GHL_FORM_IFRAME_URL`.

> **Por qué formulario nativo y no webhook.** El Inbound Webhook de GHL es
> prémium y cobra por ejecución. El nativo es gratis y el contacto entra igual.

## PASO 2 — Las dos etiquetas, desde el primer segundo

Workflow **Form Submitted → Add Tag**, dos etiquetas:

- `lead-revit-ia` — el tema. Enciende la secuencia de correos.
- `origen-bot-GUIA` — de dónde vino.

Sin la etiqueta de origen, a fin de mes no se puede decir qué recurso trajo a
quién, y la pregunta de si el lead magnet sirvió se queda sin respuesta.

## PASO 3 — El bot de la palabra clave, con DOS ramas

Workflow con disparador de comentario **filtrado por la palabra `GUIA`**.
Y aquí va lo que costó 35 leads en julio:

> **Configura la acción de envío POR SEPARADO para cada red.**
> Rama Instagram → DM de Instagram. Rama Facebook → DM de Messenger.
> **Nunca una sola acción de DM compartida entre las dos.**

Cuando el post nace en Instagram y aparece también en Facebook, mucha gente
comenta en la copia de Facebook. Si el envío está atado solo al canal de
Instagram, falla — y el workflow igual marca el paso como ejecutado, porque el
ID de quien comentó es de Facebook. La respuesta pública sí sale siempre, y por
eso nadie se entera.

**La respuesta pública lleva SIEMPRE el enlace visible.** No «te escribí al DM».
Es gratis ponerlo y es lo único que salva la pieza cuando el canal falla en
silencio:

> Te dejo la guía aquí mismo 👇 los 10 errores de Revit con el prompt exacto
> para cada uno: [enlace de la landing]

## PASO 4 — La secuencia de correos, tres toques

Se enciende con la etiqueta `lead-revit-ia`, no a mano.

| | Cuándo | Qué dice |
|---|---|---|
| Correo 1 | Inmediato | El enlace otra vez. Mucha gente cierra la página de gracias sin leer. |
| Correo 2 | 48 h | Un uso concreto: el error 06 (duplicados) y por qué se descubre al presupuestar. |
| Correo 3 | Día 5 | El puente al módulo BIM + IA. **Sin precio**, con «agenda una cita». |

## PASO 5 — Notificación interna al setter

Cada lead nuevo avisa con el nombre del recurso **y la respuesta de perfil**.
Un lead que contestó «ya uso ChatGPT o similar» no se trabaja igual que uno que
contestó «busco en foros»: el primero ya está convencido de la herramienta y le
falta el método; el segundo todavía no sabe que esto existe.

---

## Comprobar antes de publicar el reel

No basta con que la landing cargue. Diez puntos, en orden:

1. Comentar `GUIA` **en Instagram** → llega el DM con el enlace.
2. Comentar `GUIA` **en la copia de Facebook** → llega el DM por Messenger.
3. La respuesta pública automática incluye el enlace visible.
4. El enlace abre la landing **en teléfono**, no solo en computador.
5. Enviar el formulario → redirige a la página de gracias.
6. El botón de la página de gracias abre la guía **sin pedir registro**.
7. Los botones «Copiar» de los prompts funcionan.
8. El contacto aparece en el CRM con sus **dos** etiquetas.
9. Llega el correo 1 con el enlace.
10. Borrar los contactos de prueba.

El punto 2 es el que se salta todo el mundo y es justo el que falló en julio.

### Si el candado no se abre

La guía se desbloquea con `?acceso=dm2026`, que además queda guardado en el
navegador. Si alguien dice que le pide registro habiendo llenado el formulario,
es casi siempre que abrió el enlace en otro dispositivo. Se le manda el enlace
con el token y entra.

---

## Lo que NO promete este recurso

Está escrito en la propia guía, y conviene que el equipo lo diga igual:

- **No reemplaza saber Revit.** La IA es buena para entender qué te está
  diciendo Revit y para ordenar por dónde buscar. Es mala para decidir.
- **No dimensiona, no verifica norma y no firma nada.** Hay una página entera
  sobre esto y es a propósito.
- **No hace falta pagar ChatGPT.** Los prompts funcionan en la versión gratuita.

Si alguien pregunta por WhatsApp «¿esto me resuelve los cálculos?», la respuesta
es no, y decirlo bien nos suma: es la diferencia entre una academia de ingeniería
y un vendedor de prompts.
