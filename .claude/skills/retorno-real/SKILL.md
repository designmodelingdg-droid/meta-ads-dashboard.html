---
name: retorno-real
description: |
  Cruza el dinero que de verdad entró (Stripe + PayPal) con el gasto de pauta de Meta y con las oportunidades del CRM, y dice el retorno honesto por producto y por país.

  Usa este skill cuando Dayana diga: "retorno-real", "cuánto vendimos de verdad", "cruza las ventas con la pauta", "cuánto entró por Stripe", "cuánto por PayPal", "el ROAS real", "cuánto cobramos este mes", "compara el CRM con lo cobrado", o cuando pregunte si una campaña se pagó sola.

  Se corre cuando haga falta, y siempre en el cierre de mes y en la auditoría de los viernes.
---

# Skill: retorno-real

Responde una sola pregunta: **de cada dólar que se puso en pauta, ¿cuánto volvió
de verdad?**

No «cuánto se marcó ganado en el CRM». Cuánto **entró a la cuenta**.

---

## 0. Dónde están los datos (no hace falta ningún token)

Todo lo baja sola la Action `metricas-semanales.yml` —lunes y viernes— usando
los secretos que viven cifrados en GitHub. Los datos se commitean al repo:

| Carpeta | Qué trae | Secreto que usa |
|---|---|---|
| `matriz-viral/fuentes/ingresos/stripe.json` | cada cobro: fecha, neto, correo, descripción | `STRIPE_SECRET_KEY` |
| `matriz-viral/fuentes/ingresos/paypal.json` | ídem, de PayPal | `CLIEND_ID_PAYPAL` + `SECRET_KEY_PAYPAL` |
| `matriz-viral/fuentes/ingresos/resumen.json` | totales y ventana | — |
| `matriz-viral/fuentes/ads-insights/` | gasto por campaña, adset, día y país | `META_TOKEN` |
| `matriz-viral/matriz/matriz.json` | métricas orgánicas | `META_TOKEN` |

El CRM se lee aparte, en vivo, con el conector de GoHighLevel (Windsor).

> **Si un archivo falta o está viejo:** se corre la Action a mano en
> **Actions → Métricas semanales → Run workflow**. Nunca se pide un token en el
> chat pudiendo correr la Action.

---

## 1. Las tres fuentes y qué vale cada una

Esta jerarquía es lo que hace útil el skill. No son tres formas de contar lo
mismo: son tres cosas distintas.

| Fuente | Qué dice | Cuánto pesa |
|---|---|---|
| **Stripe + PayPal** | el dinero que **entró** | 🥇 **La verdad.** No opina |
| **CRM (GoHighLevel)** | lo que alguien **marcó** ganado | 🥈 Intención, no caja |
| **Píxel de Meta** | lo que el píxel **creyó** ver | 🥉 Estimación |

**La diferencia entre las tres es el hallazgo, no un error a corregir.**

- CRM **mayor** que lo cobrado → hay ganadas sin cobrar, o reservas contadas
  como venta completa. Es lo más común.
- Cobrado **mayor** que el CRM → entró plata que nadie registró. Suele ser
  orgánico o recompra.
- Píxel muy por encima de los dos → atribución inflada.

---

## 2. Cómo se cruza

1. **Ventana igual para todos.** Los tres archivos traen `ventana` en su
   cabecera. Si no coinciden, se recorta a la más corta y se dice.
2. **Sumar lo cobrado**: Stripe neto + PayPal neto. El neto ya lleva los
   reembolsos descontados.
3. **Traer el gasto** de `ads-insights/por-campana.json`.
4. **Retorno real = cobrado ÷ gasto.**
5. **Cruzar por correo** cuando se pueda: Stripe y PayPal traen el correo del
   pagador, y el CRM también. Eso permite decir qué compras vinieron de un
   lead de pauta y cuáles no.
6. **Separar las reservas de $100** del Máster. Un cobro de $100 con
   descripción de Máster es anticipo, no venta cerrada.

---

## 3. Lo que se entrega

**A Dayana**, en lenguaje llano:

- **Una frase**: se puso X, volvió Y, o sea Z por cada dólar.
- **Por producto**: qué se vendió de verdad.
- **La diferencia CRM vs cobrado**, con nombre y apellido: cuántas
  oportunidades ganadas no tienen un cobro detrás.
- **Qué campaña se pagó sola** y cuál no.
- **Una decisión** para la semana.

**Y se anota en `matriz-viral/RECOMENDACIONES.md`**, en «Historial», con la
fecha y el retorno del periodo, para poder compararlo el mes siguiente.

---

## Reglas

- **Lo cobrado manda.** Si el CRM dice una cosa y Stripe otra, gana Stripe.
- **Nunca sumar Stripe + PayPal + CRM.** Son la misma venta contada dos veces.
- **Las reservas de $100 no son ventas.** Se separan siempre, en las tres
  fuentes.
- **Si una fuente falló** (el JSON trae `error`), se dice y se calcula sin
  ella, diciendo qué falta. Nunca se estima el hueco.
- **La ventana termina ayer.** Un día sin cerrar da cifras cortas.
- **Nunca pedir un token en el chat** si se puede correr la Action.
- El Máster **no se cotiza** por aquí: el precio no entra en ningún mensaje.
