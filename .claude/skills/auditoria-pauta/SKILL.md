---
name: auditoria-pauta
description: |
  Audita el reporte semanal de campañas que manda la agencia (Olympus), verificando cada cifra contra la API de Meta y contra el CRM, y devuelve el mensaje de feedback listo para el grupo.

  Usa este skill cuando Dayana diga: "auditoria-pauta", "llegó el reporte de la agencia", "revisa el reporte de los viernes", "el reporte semanal de campañas", "mira lo que mandó el equipo de marketing", "revisa si hicieron los cambios", o cuando pegue el texto o el enlace de un reporte de olympus-os.vercel.app.

  Se corre **todos los viernes**, cuando llega el reporte.
---

# Skill: auditoria-pauta

Audita el reporte semanal de la agencia. La regla de oro: **ninguna cifra del
reporte se da por buena sin verificarla contra Meta.** En la primera auditoría
(3-ago-2026) *todas* las cifras de volumen estaban cortas y el alcance estaba
mal por un factor de 4.

---

## 0. Conseguir el reporte

`olympus-os.vercel.app` está **bloqueado por la política de red** del entorno
donde corre Claude. No se puede abrir el enlace.

Pídele a Dayana que **copie y pegue el texto completo** de la página. Si el
equipo puede dejarlo en un Drive compartido o mandarlo en PDF, mejor —
cualquier formato que no sea el enlace sirve.

Guarda el texto en `matriz-viral/auditorias/AAAA-MM-DD-reporte.md` para poder
comparar semanas.

---

## 1. Sacar los datos reales de Meta

El token de página vive en el scratchpad de la sesión (`page_token`) y tiene
`ads_read`. Cuenta: `act_1159622151150228`.

```python
# insights por campaña del periodo del reporte
GET act_1159622151150228/insights
    level=campaign
    time_range={"since":"AAAA-MM-DD","until":"AAAA-MM-DD"}
    fields=campaign_name,spend,impressions,reach,frequency,clicks,ctr,cpc,
           actions,action_values,purchase_roas,objective
```

Y **siempre** el desglose diario (`time_increment=1`): es lo que destapó que
el reporte se generaba antes de cerrar el último día.

Para las campañas con geo-split, `level=adset` — el reporte nunca las abre y
ahí suele estar la decisión de presupuesto.

---

## 2. La lista de comprobación

Cada cifra del reporte contra la de Meta. Estas son las que han fallado antes:

| Qué revisar | Cómo se detecta | Qué pasó el 3-ago |
|---|---|---|
| **¿Se generó antes de cerrar el último día?** | gasto diario real vs el del reporte | el último día marcaba $11 y cerró en $32,67 |
| **Gasto total** | suma real vs reportada | $231,38 real vs $210 reportado |
| **Alcance** | `reach` por campaña | reportaban ~23K, el real era 90.115 |
| **Frecuencia** | debe ser **≥ 1 siempre** | reportaron 0,86, que es imposible |
| **Costo por resultado** | dividir a mano gasto ÷ resultados | decían $0,40; era $0,50 |
| **Sumas que mezclan cosas** | conversaciones ≠ leads | sumaron 221 conv + 67 leads = "288 conversaciones" |
| **CTR promedio** | ¿lo infla la campaña de tráfico? | 5,07% real, pero las de venta iban a 2,3% |
| **¿Abrieron el geo-split?** | `level=adset` | nunca lo abren |
| **Métricas de retorno** | `purchase_roas`, `action_values` | existían en Meta y no las pusieron |

**Frecuencia por debajo de 1 es matemáticamente imposible** — es la señal más
rápida de que el dato no salió de Meta.

---

## 3. Cruzar con el CRM

El píxel y el CRM nunca coinciden, y esa diferencia es la conversación real.

Con el conector de GoHighLevel (Windsor):
- **Oportunidades creadas** en el periodo, por pipeline
- **Ganadas y su valor**, separando lo cerrado de las **reservas de $100** del
  Máster, que no son ventas completas
- **Cuántas siguen abiertas** — el cuello de botella suele estar aquí, no en
  el costo por lead
- **Contactos duplicados** entre pipelines: una persona puede aparecer como
  tres "ganadas"

Con eso se calcula el retorno honesto: gasto real vs valor **registrado**,
diciendo qué parte es reserva y qué parte falta por registrar.

---

## 4. Comprobar que aplicaron lo acordado

Lo pedido el 3-ago-2026. Revisar en cada reporte nuevo:

1. **Generar el reporte con el mes/semana cerrado**, no el mismo viernes.
2. **Corregir alcance y frecuencia.**
3. **Incluir métricas de retorno** y conciliar píxel contra CRM.
4. **Abrir el geo-split** de ACERO por país.

Si algo sigue igual, decirlo con la fecha en que se pidió. Si lo corrigieron,
reconocerlo — el objetivo es que el reporte mejore, no ganar la discusión.

---

## 5. Lo que se entrega

**A Dayana**, en lenguaje llano:
- ¿Vamos bien o mal? Una frase.
- Qué cifras del reporte no cuadran y cuáles son las buenas.
- Qué decisión toca tomar esta semana (mover presupuesto, cambiar creativo).
- Recordar que **la frecuencia arriba de 3** es la señal de desgaste.

**Un mensaje listo para el grupo**: cordial, concreto, con las cifras reales y
una pregunta al final. Nunca acusar — mostrar el número correcto y pedir el
cambio.

**El archivo de la semana** en `matriz-viral/auditorias/`, para comparar.

---

## Reglas

- **Nunca dar una cifra por buena sin verificarla.** Si algo no se puede
  verificar, se dice que no se pudo.
- **Nunca inventar el dato que falta.** Si el reporte no trae costo por
  agenda, se pide; no se estima.
- El Máster **no se cotiza** por aquí: el precio no entra en ningún mensaje.
- Las **reservas de $100 no son ventas**. Separarlas siempre.
- Si una campaña pasa de **frecuencia 3**, avisar aunque el reporte no lo
  mencione.
- El costo por lead barato **no es buena noticia por sí solo** si las
  oportunidades se quedan abiertas. Mirar siempre las dos cosas juntas.
