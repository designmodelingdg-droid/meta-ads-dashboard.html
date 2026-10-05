---
name: ventas-cierre-dma
description: >
  Revisa y mejora el agente de ventas de WhatsApp de Design Modeling Academy
  (el bot de Patricio / Olympus en GoHighLevel): audita los mensajes reales que
  manda, detecta dónde se cae la venta y reescribe sus instrucciones con métodos
  de cierre (Brian Tracy, SPIN, Gap Selling, Chris Voss, Hormozi, Cialdini,
  Sandler, Challenger, Jeb Blount, Ziglar). ACTIVA cuando Dayana diga: "el bot no
  cierra", "mejora el bot de ventas", "revisa los mensajes del bot", "el agente
  de Patricio", "estoy perdiendo ventas en WhatsApp", "objeciones", o mande
  capturas de conversaciones del bot.
---

# Agente de ventas de WhatsApp — DMA

## Dónde está todo

| Archivo | Qué es |
|---|---|
| `matriz-viral/ventas/PROMPT-AGENTE-VENTAS.md` | La instrucción de sistema del agente. Es lo que Patricio pega en el agente. |
| `matriz-viral/ventas/OBJECIONES-DMA.md` | Las respuestas a cada objeción, con el patrón reconocer → preguntar → responder corto → pedir el paso. |
| `matriz-viral/ventas/METODOS-DE-VENTA.md` | Los libros de ventas resumidos con palabras propias y aplicados a DMA. **No se copian los libros** (derechos de autor). |
| `matriz-viral/ventas/ANTES-Y-DESPUES.md` | Conversaciones reales (anonimizadas) reescritas: lo que mandó el agente y lo que debió mandar. |
| `matriz-viral/ventas/PLANTILLAS-GHL-A-CORREGIR.md` | Mensajes de los workflows de GHL con urgencia falsa, fechas vencidas o precios viejos. |
| `scripts/ghl_auditoria_bot.py` | Lee las conversaciones de GHL y mide cómo terminan, qué objeciones aparecen y qué contesta el agente. |
| `.github/workflows/auditoria-bot.yml` | Corre el script con el secreto `GHL_TOKEN` y guarda el resultado. |
| `matriz-viral/fuentes/ghl/auditoria-bot-ventas.json` | El resultado de la auditoría. Sin nombres, teléfonos ni correos. |

## Cómo se revisa el agente (cada semana o cuando Dayana traiga capturas)

1. Disparar la Action «Auditoría del bot de ventas (GHL)» (`workflow_dispatch`, o
   un push al script). Esperar a que termine y hacer `git pull`.
2. Leer `auditoria-bot-ventas.json`:
   - `terminan_con_mensaje_nuestro`: si casi todas terminan con nuestro mensaje,
     el agente habla y la persona se va. Es la señal principal.
   - `ultimo_mensaje_nuestro…`: cuántos de esos últimos mensajes no llevan
     pregunta, o dicen «revísalo y me cuentas».
   - `objeciones` y `respuesta_justo_despues_de_una_objecion`: qué objeción
     aparece más y si el agente la contesta con un párrafo o con una pregunta.
   - `frases_del_bot_mas_repetidas`: plantillas de los workflows. Buscar urgencia
     falsa («cerramos hoy», «últimos cupos», «solo por hoy») y seguimientos
     vacíos («¿lograste revisar?»).
   - `ejemplos_final_de_conversacion`: leer los 30, son el mejor diagnóstico.
3. Contrastar con las capturas que traiga Dayana y con las reglas del prompt.
4. Actualizar `ANTES-Y-DESPUES.md` con los casos nuevos y, si hace falta, una
   regla nueva en el prompt o una objeción nueva en `OBJECIONES-DMA.md`.
5. Entregar a Patricio solo lo que cambió, con la fecha.

## Reglas que no se rompen

- **Nada personal en el repo:** ni nombres, ni teléfonos, ni correos de leads.
  El script los enmascara; las capturas se transcriben sin nombre.
- **El token de GHL vive en el secreto `GHL_TOKEN`.** Nunca en el chat ni en un archivo.
- **El agente nunca niega que es un asistente** y pasa a una persona cuando se
  lo piden o cuando desconfían.
- **El precio del Máster no se da por chat.** Acero sí: USD 225 con el tutor IA.
- **Nada inventado:** ni cupos, ni fechas, ni alumnos, ni servicios que no están
  confirmados. Cualquier dato nuevo que no esté en el prompt lo valida Dayana antes de activarlo.
- **No hay promo de USD 100.** El 2x1 de la Especialización es el gancho para quien no le ve el valor, y a quien llega por un anuncio de USD 199,99 se le respeta ese precio sin el Tutor IA (Dayana, 5-oct-2026).
- **Los traspasos a una persona los recibe Ester**, a cualquier hora.
