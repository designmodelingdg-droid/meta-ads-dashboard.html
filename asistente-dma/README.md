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
asistente_agent.py   El cerebro: system prompt + 14 herramientas + loop de tool-use
google_client.py     Google Calendar + Tasks + Drive por REST, con OAuth propio
clickup_client.py    Tareas para el equipo: 6 personas y 12 listas reales
panorama.py          Agrega agenda, tareas, GHL, Meta Ads y académico en un solo texto
recordatorios.py     Avisos proactivos por WhatsApp (reuniones, vencimientos)
BLUEPRINT.md         La especificación completa (metodología de the-architect)
INTEGRACION.md       El parche exacto sobre server.py y la prueba end-to-end
GUIA-MONTAJE.md      Los 15 minutos de Google Cloud que solo puedes hacer tú
```

Los cinco `.py` van a la **raíz** de `designmodelingdg-droid/dma-sales-assistant`,
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

- [x] Credenciales de Google
- [x] Token de ClickUp
- [x] Disparador elegido: **"asistente"** (funciona desde los 6 números del equipo)
- [x] Parche de `server.py` aplicado y mergeado
- [ ] Plantilla de WhatsApp aprobada, para que los recordatorios pasen la
      ventana de 24 h de Meta
- [ ] `MODEL_PROVIDER=openrouter` + `OPENROUTER_API_KEY` en Render

> **Diagnóstico.** Si el asistente no responde, `/asistente-diag?secret=XXX`
> dice si el modelo contesta, si el tool use funciona y si Google y ClickUp
> autentican — sin pasar por WhatsApp. Con `&q=texto` ejecuta el agente entero.

Lo que queda aquí es la fuente y la documentación: si hay que cambiar el agente,
se cambia primero en esta carpeta y luego se lleva al repo del bot.
