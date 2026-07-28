# DMA Chief of Staff — asistente ejecutivo por notas de voz

Un jefe de gabinete para Dayana. Le mandas una **nota de voz** por WhatsApp y
agenda, crea tareas, guarda notas y te devuelve el panorama de la empresa.

No es un bot nuevo: es el cerebro que le faltaba al que ya tienes corriendo.

---

## Por dónde empezar

| Si quieres… | Lee |
|---|---|
| Entender qué se construyó y por qué | `BLUEPRINT.md` |
| Montarlo en el bot | `INTEGRACION.md` |
| Sacar las credenciales de Google | `GUIA-MONTAJE.md` |

## Qué hay aquí

```
asistente_agent.py   El cerebro: system prompt + 24 herramientas + loop de tool-use
google_client.py     Google Calendar + Tasks + Drive por REST, con OAuth propio
gmail_client.py      Correo: buscar, leer, borradores y enviar (mismo OAuth)
clickup_client.py    Tareas para el equipo: 6 personas y 12 listas reales
ventas.py            Ventas e ingresos: Stripe (dinero) + GHL (inscritos), sin mezclarlos
fathom_client.py     Resúmenes y tareas de las reuniones que graba Fathom
panorama.py          Agrega agenda, tareas, GHL, Meta Ads y académico en un solo texto
recordatorios.py     Avisos proactivos por WhatsApp (reuniones, vencimientos)
BLUEPRINT.md         La especificación completa (metodología de the-architect)
INTEGRACION.md       El parche exacto sobre server.py y la prueba end-to-end
GUIA-MONTAJE.md      Los 15 minutos de Google Cloud que solo puedes hacer tú
```

Los ocho `.py` van a la **raíz** de `designmodelingdg-droid/dma-sales-assistant`,
junto a `server.py`. Aquí viven versionados como documentación viva del agente.

## Cómo se ve usándolo

```
Tú (nota de voz):
  "oye asistente, agéndame el jueves a las 10 con Ester para revisar
   el máster, y recuérdame llamar al proveedor de hosting el viernes"

Él:
  ✅ Agendado: Revisión Máster con Ester — jue 30/07, 10:00
  ✅ Tarea creada: Llamar al proveedor de hosting (vence 31/07)
```

```
Tú: "asistente ¿cómo vamos?"

Él:  📅 Agenda
     • 10:00 — Revisión Máster con Ester
     • 16:00 — Grabación reel · Plan de ventas

     📋 Tareas
     🔴 Llamar al proveedor de hosting

     💼 Comercial
     … 7 leads nuevos, 2 citas agendadas, 3 sin responder …
```

```
Tú: "escríbele a Carlos que la oferta vence hoy"

Él:  ⚠️ Antes de enviar, confirma:
     Para: Carlos Mendoza (GHL)
     Texto: "Hola Carlos, te recuerdo que la oferta vence hoy…"
     ¿Lo mando?
```

Lo reversible lo hace directo. Lo que sale hacia afuera, lo confirma. Esa es toda
la política de autonomía, y está tanto en el prompt como en el código.

## Estado — desplegado

El asistente está **en producción** desde el 28/07/2026.
La integración se mergeó en `dma-sales-assistant#5`; los 5 módulos viven en la
raíz de ese repo y `server.py` ya llama al agente.

- [x] Credenciales de Google (agenda, tareas, notas)
- [x] Token de ClickUp
- [x] Disparadores: **"asistente"** y **"agente"** (desde los 6 números del equipo)
- [x] Parche de `server.py` aplicado y mergeado
- [x] `MODEL_PROVIDER=openrouter` + `OPENROUTER_API_KEY` en Render
- [x] Funciona por **texto y por nota de voz**, con la agenda real
- [x] Ventas e ingresos (Stripe ya estaba conectado, no hace falta nada)
- [ ] **Re-autorizar Google con el scope de Gmail** — sin esto el correo no funciona
      (`GUIA-MONTAJE.md`, paso 4, recuadro naranja)
- [ ] **`FATHOM_API_KEY` en Render** — sin esto no hay resúmenes de reuniones
      (`GUIA-MONTAJE.md`, paso 7b)
- [ ] Plantilla de WhatsApp aprobada, para que los recordatorios pasen la
      ventana de 24 h de Meta

### Lo que se arregló probándolo en producción

El código vivía aquí, pero solo el uso real destapó cuatro fallos, todos ya
mergeados en el repo del bot:

| Síntoma | Causa |
|---|---|
| Ninguna nota de voz respondía | Al transcribir, el mensaje pasa a `"[Nota de voz]: asistente…"` y el disparador dejaba de estar al principio |
| Tardaba ~6 min en contestar | GHL no entrega los webhooks; respondía el scanner de rescate, que corre cada 5 min. Ahora hay uno de 1 min solo para admins |
| "No pude agendarte con Ester, su correo no es válido" | Se le pasaba el nombre a Google como si fuera un correo. Ahora se resuelve desde `clickup_client.EQUIPO` |
| Se quedaba sordo tras preguntar algo | Exigía "asistente" en cada mensaje, así que no oía la respuesta a su propia pregunta. Ahora hay ventana de conversación de 10 min |
| **Seguía sin responder a las notas de voz** | Ella dice **"agente"**, y la lista de disparadores solo tenía "asistente". Cada nota se descartaba en silencio, indistinguible de un bot caído. Ahora "agente" dispara, y el saludo de delante ya no estorba |

### Lo que se añadió después de usarlo

| Pedido | Qué se construyó |
|---|---|
| *"¿cuántas ventas vendimos hoy?"* | `ventas.py` — Stripe (dinero cobrado) y CRM (inscritos) **separados**, nunca sumados |
| *"el ingreso de cada cliente por día y por semana"* | `ingresos_por_cliente` y `ventas_por_dia` |
| *"que pueda leer y escribir los correos"* | `gmail_client.py` — ante la duda guarda **borrador**, no envía |
| *"que entre a las reuniones con Fathom y Zoom y me dé un resumen"* | No hizo falta integrar Zoom: **Fathom ya entra sola** a Zoom, Meet y Teams. Solo faltaba leerla |

> **Diagnóstico.** Si el asistente no responde, `/asistente-diag?secret=XXX`
> dice si el modelo contesta, si el tool use funciona y si Google y ClickUp
> autentican — sin pasar por WhatsApp. Con `&q=texto` ejecuta el agente entero.

Lo que queda aquí es la fuente y la documentación: si hay que cambiar el agente,
se cambia primero en esta carpeta y luego se lleva al repo del bot.
